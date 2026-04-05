#!/usr/bin/env python3

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib
import numpy as np
from scipy import optimize

matplotlib.use("Agg")
from matplotlib import pyplot as plt


H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_DE = 0.685
C_LIGHT = 3.0e8
A0_OBSERVED = 1.2e-10
MPC_TO_M = 3.085677581491367e22
SEC_PER_GYR = 365.25 * 24.0 * 3600.0 * 1.0e9
H0_SI = H0_KM_S_MPC * 1_000.0 / MPC_TO_M
H0_INV_GYR = 1.0 / H0_SI / SEC_PER_GYR
CH0 = C_LIGHT * H0_SI
Z_INIT = 50.0
Z_DESI_MAX = 2.3
X_INIT = -math.log1p(Z_INIT)
N_STEPS_FULL = 1_600
N_STEPS_ROOT = 900
Y_POSITIVE_FLOOR = 1.0e-12
MODEL_A_U_MAX = 300.0
MODEL_B_U_MAX = 15.0
PRIMARY_DATASET = "desy5sn"
DATASET_ORDER = ["cmb", "pantheonplus", "desy5sn", "union3"]
DATASET_LABELS = {
    "cmb": "DESI DR2 + CMB",
    "pantheonplus": "DESI DR2 + CMB + Pantheon+",
    "desy5sn": "DESI DR2 + CMB + DES Y5 SN",
    "union3": "DESI DR2 + CMB + Union3",
}
DATASET_COLORS = {
    "cmb": "#264653",
    "pantheonplus": "#d1495b",
    "desy5sn": "#2a9d8f",
    "union3": "#e9c46a",
}
TARGET_Z = np.array([0.0, 0.3, 0.5, 0.7, 1.0, 1.5, 2.3], dtype=float)


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[3]
CHAIN_ROOT = REPO_ROOT / "cosmic_shielding_desi" / "data" / "raw" / "desi_dr2_chains"
PLOT_ROOT = ROOT / "plots"
OUTPUT_ROOT = ROOT / "output"
SUMMARY_PATH = OUTPUT_ROOT / "vacuum_lag_summary.json"
REPORT_PATH = OUTPUT_ROOT / "summary.md"


@dataclass
class ChainSummary:
    name: str
    label: str
    weights: np.ndarray
    w0: np.ndarray
    wa: np.ndarray
    mean: np.ndarray
    cov: np.ndarray
    inv_cov: np.ndarray


@dataclass
class BackgroundSolution:
    x: np.ndarray
    z: np.ndarray
    a: np.ndarray
    y: np.ndarray
    y_eq: np.ndarray
    e: np.ndarray
    w: np.ndarray


@dataclass
class ModelPoint:
    model: str
    u: float
    tau_gyr: float
    bare_density: float
    w0: float
    wa: float
    cpl_rms: float
    delta: float | None
    beta: float | None
    y_init: float
    y_eq_init: float
    y_eq_today: float
    a0_predicted: float
    a0_factor_needed: float
    z_cross_w_minus_one: float | None
    z_h_equals_tau_inv: float | None
    h_ratio_z05: float
    h_ratio_z10: float
    hz_targets: list[float]
    wz_targets: list[float]


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(values * weights) / np.sum(weights))


def weighted_covariance(columns: np.ndarray, weights: np.ndarray) -> np.ndarray:
    mean = np.average(columns, axis=0, weights=weights)
    centered = columns - mean
    cov = np.einsum("i,ij,ik->jk", weights, centered, centered) / np.sum(weights)
    return cov


def load_chain_file(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    with path.open() as handle:
        header = handle.readline().lstrip("#").split()
    indices = {name: idx for idx, name in enumerate(header)}
    values = np.loadtxt(
        path,
        comments="#",
        usecols=[indices["weight"], indices["w"], indices["wa"]],
    )
    return values[:, 0], values[:, 1], values[:, 2]


def load_dataset(name: str) -> ChainSummary:
    weights_list: list[np.ndarray] = []
    w0_list: list[np.ndarray] = []
    wa_list: list[np.ndarray] = []
    for path in sorted((CHAIN_ROOT / name).glob("chain.[1-4].txt")):
        weights, w0, wa = load_chain_file(path)
        weights_list.append(weights)
        w0_list.append(w0)
        wa_list.append(wa)
    weights = np.concatenate(weights_list)
    w0 = np.concatenate(w0_list)
    wa = np.concatenate(wa_list)
    samples = np.column_stack([w0, wa])
    cov = weighted_covariance(samples, weights)
    return ChainSummary(
        name=name,
        label=DATASET_LABELS[name],
        weights=weights,
        w0=w0,
        wa=wa,
        mean=np.array([weighted_mean(w0, weights), weighted_mean(wa, weights)], dtype=float),
        cov=cov,
        inv_cov=np.linalg.inv(cov),
    )


def lcdm_e(z: np.ndarray) -> np.ndarray:
    return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_DE)


def eq_density(x: float, bare_density: float, beta: float) -> float:
    return bare_density + beta * OMEGA_M * math.exp(-3.0 * x)


def e_from_state(x: float, y: float) -> float:
    e2 = OMEGA_M * math.exp(-3.0 * x) + y
    if e2 <= 0.0:
        return math.nan
    return math.sqrt(e2)


def dydx(x: float, y: float, u: float, bare_density: float, beta: float) -> float:
    e = e_from_state(x, y)
    if not math.isfinite(e) or e <= 0.0:
        return math.nan
    return -(y - eq_density(x, bare_density, beta)) / (u * e)


def rk4_step(x: float, y: float, h: float, u: float, bare_density: float, beta: float) -> float:
    k1 = dydx(x, y, u, bare_density, beta)
    if not math.isfinite(k1):
        return math.nan
    k2 = dydx(x + 0.5 * h, y + 0.5 * h * k1, u, bare_density, beta)
    if not math.isfinite(k2):
        return math.nan
    k3 = dydx(x + 0.5 * h, y + 0.5 * h * k2, u, bare_density, beta)
    if not math.isfinite(k3):
        return math.nan
    k4 = dydx(x + h, y + h * k3, u, bare_density, beta)
    if not math.isfinite(k4):
        return math.nan
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate_background(
    u: float,
    bare_density: float,
    beta: float,
    steps: int = N_STEPS_FULL,
) -> BackgroundSolution | None:
    if u <= 0.0:
        return None

    x = np.linspace(0.0, X_INIT, steps + 1)
    y = np.empty_like(x)
    y[0] = OMEGA_DE

    for idx in range(steps):
        next_y = rk4_step(x[idx], y[idx], x[idx + 1] - x[idx], u, bare_density, beta)
        if not math.isfinite(next_y):
            return None
        if OMEGA_M * math.exp(-3.0 * x[idx + 1]) + next_y <= 0.0:
            return None
        y[idx + 1] = next_y

    a = np.exp(x)
    z = 1.0 / a - 1.0
    y_eq = bare_density + beta * OMEGA_M * (1.0 + z) ** 3
    e = np.sqrt(OMEGA_M * (1.0 + z) ** 3 + y)
    w = np.full_like(y, np.nan)
    positive = y > Y_POSITIVE_FLOOR
    w[positive] = -1.0 + (y[positive] - y_eq[positive]) / (3.0 * u * e[positive] * y[positive])

    return BackgroundSolution(x=x, z=z, a=a, y=y, y_eq=y_eq, e=e, w=w)


def fit_local_cpl(solution: BackgroundSolution, z_limit: float = 1.0) -> tuple[float, float]:
    w0 = float(solution.w[0])
    mask = (solution.z <= z_limit) & np.isfinite(solution.w)
    a = solution.a[mask]
    basis = 1.0 - a
    target = solution.w[mask] - w0
    denom = float(np.dot(basis, basis))
    wa = float(np.dot(basis, target) / denom) if denom > 0.0 else math.nan
    model = w0 + wa * basis
    rms = float(np.sqrt(np.mean((solution.w[mask] - model) ** 2)))
    return wa, rms


def find_crossing(solution: BackgroundSolution) -> float | None:
    mask = (solution.z <= Z_DESI_MAX) & np.isfinite(solution.w)
    z = solution.z[mask]
    offset = solution.w[mask] + 1.0
    if z.size < 2:
        return None
    if np.all(np.abs(offset) < 1.0e-8):
        return None
    for idx in range(len(z) - 1):
        left = offset[idx]
        right = offset[idx + 1]
        if abs(left) < 1.0e-8:
            prev_sign = math.copysign(1.0, offset[idx - 1]) if idx > 0 and abs(offset[idx - 1]) >= 1.0e-8 else 0.0
            next_sign = math.copysign(1.0, right) if abs(right) >= 1.0e-8 else 0.0
            if prev_sign != 0.0 and next_sign != 0.0 and prev_sign != next_sign:
                return float(z[idx])
            continue
        if left * right < 0.0:
            frac = abs(left) / (abs(left) + abs(right))
            return float(z[idx] + frac * (z[idx + 1] - z[idx]))
    return None


def find_h_equals_tau_inv(solution: BackgroundSolution, u: float) -> float | None:
    target = 1.0 / u
    if target < 1.0:
        return None
    e = solution.e
    z = solution.z
    for idx in range(len(z) - 1):
        left = e[idx] - target
        right = e[idx + 1] - target
        if left == 0.0:
            return float(z[idx])
        if left * right < 0.0:
            frac = abs(left) / (abs(left) + abs(right))
            return float(z[idx] + frac * (z[idx + 1] - z[idx]))
    return None


def interp_quantity(z_target: float, z: np.ndarray, values: np.ndarray) -> float:
    return float(np.interp(z_target, z, values))


def make_model_point(
    model: str,
    u: float,
    bare_density: float,
    solution: BackgroundSolution,
    beta: float | None,
    delta: float | None,
) -> ModelPoint:
    wa, cpl_rms = fit_local_cpl(solution)
    h_ratio_z05 = interp_quantity(0.5, solution.z, solution.e / lcdm_e(solution.z))
    h_ratio_z10 = interp_quantity(1.0, solution.z, solution.e / lcdm_e(solution.z))
    tau_gyr = u * H0_INV_GYR
    a0_pred = CH0 / u
    return ModelPoint(
        model=model,
        u=float(u),
        tau_gyr=float(tau_gyr),
        bare_density=float(bare_density),
        w0=float(solution.w[0]),
        wa=float(wa),
        cpl_rms=float(cpl_rms),
        delta=None if delta is None else float(delta),
        beta=None if beta is None else float(beta),
        y_init=float(solution.y[-1]),
        y_eq_init=float(solution.y_eq[-1]),
        y_eq_today=float(solution.y_eq[0]),
        a0_predicted=float(a0_pred),
        a0_factor_needed=float(A0_OBSERVED / a0_pred),
        z_cross_w_minus_one=find_crossing(solution),
        z_h_equals_tau_inv=find_h_equals_tau_inv(solution, u),
        h_ratio_z05=float(h_ratio_z05),
        h_ratio_z10=float(h_ratio_z10),
        hz_targets=[float(x) for x in np.interp(TARGET_Z, solution.z, solution.e)],
        wz_targets=[float(x) for x in np.interp(TARGET_Z, solution.z, solution.w)],
    )


def evaluate_model_a(u: float, w0_today: float) -> ModelPoint | None:
    bare_density = OMEGA_DE - 3.0 * u * OMEGA_DE * (w0_today + 1.0)
    solution = integrate_background(u=u, bare_density=bare_density, beta=0.0)
    if solution is None:
        return None
    if np.any((solution.z <= Z_DESI_MAX) & (solution.y <= Y_POSITIVE_FLOOR)):
        return None
    if not math.isfinite(solution.w[0]):
        return None
    delta = None
    if abs(bare_density) > 1.0e-12:
        delta = solution.y[-1] / bare_density - 1.0
    return make_model_point(
        model="A",
        u=u,
        bare_density=bare_density,
        solution=solution,
        beta=None,
        delta=delta,
    )


def solve_bare_for_model_b(
    u: float,
    beta: float,
    guess: float | None = None,
) -> float | None:
    center = OMEGA_DE - beta * OMEGA_M if guess is None else guess

    def residual(bare_density: float) -> float:
        solution = integrate_background(u=u, bare_density=bare_density, beta=beta, steps=N_STEPS_ROOT)
        if solution is None:
            return math.nan
        return float(solution.y[-1] - solution.y_eq[-1])

    center_value = residual(center)
    if math.isfinite(center_value) and abs(center_value) < 1.0e-6:
        return center

    scale = max(1.0, abs(beta) * OMEGA_M * (1.0 + Z_INIT) ** 3)
    x0 = center
    x1 = center + 0.05 * scale if scale > 0.0 else center + 0.05
    try:
        secant = optimize.root_scalar(
            residual,
            x0=x0,
            x1=x1,
            method="secant",
            maxiter=20,
        )
        if secant.converged and math.isfinite(secant.root):
            check = residual(secant.root)
            if math.isfinite(check) and abs(check) < 1.0e-5:
                return float(secant.root)
    except (RuntimeError, ValueError, ZeroDivisionError):
        pass

    spans = scale * np.array([0.05, 0.15, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=float)
    for span in spans:
        left = center - span
        right = center + span
        left_value = residual(left)
        right_value = residual(right)
        if not math.isfinite(left_value) or not math.isfinite(right_value):
            continue
        if left_value == 0.0:
            return float(left)
        if right_value == 0.0:
            return float(right)
        if left_value * right_value < 0.0:
            root = optimize.brentq(residual, left, right, xtol=1.0e-8, rtol=1.0e-8, maxiter=80)
            return float(root)
    return None


def evaluate_model_b(u: float, beta: float, guess: float | None = None) -> tuple[ModelPoint | None, float | None]:
    bare_density = solve_bare_for_model_b(u=u, beta=beta, guess=guess)
    if bare_density is None:
        return None, None
    solution = integrate_background(u=u, bare_density=bare_density, beta=beta)
    if solution is None:
        return None, None
    if abs(solution.y[-1] - solution.y_eq[-1]) > 1.0e-4:
        return None, None
    if np.any((solution.z <= Z_DESI_MAX) & (solution.y <= Y_POSITIVE_FLOOR)):
        return None, None
    if not math.isfinite(solution.w[0]):
        return None, None
    point = make_model_point(
        model="B",
        u=u,
        bare_density=bare_density,
        solution=solution,
        beta=beta,
        delta=None,
    )
    return point, bare_density


def chain_chi2(point: ModelPoint, summary: ChainSummary) -> float:
    delta = np.array([point.w0, point.wa]) - summary.mean
    return float(delta @ summary.inv_cov @ delta)


def cpl_w(z: np.ndarray, w0: float, wa: float) -> np.ndarray:
    a = 1.0 / (1.0 + z)
    return w0 + wa * (1.0 - a)


def ellipse_points(mean: np.ndarray, cov: np.ndarray, delta_chi2: float, num: int = 300) -> tuple[np.ndarray, np.ndarray]:
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    theta = np.linspace(0.0, 2.0 * math.pi, num)
    circle = np.stack([np.cos(theta), np.sin(theta)])
    radii = np.sqrt(np.maximum(vals, 0.0) * delta_chi2)
    ellipse = mean[:, None] + vecs @ (radii[:, None] * circle)
    return ellipse[0], ellipse[1]


def scan_model_a() -> list[ModelPoint]:
    u_grid = np.geomspace(0.15, MODEL_A_U_MAX, 56)
    w0_grid = np.linspace(-1.45, -0.45, 56)
    results: list[ModelPoint] = []
    for u in u_grid:
        for w0_today in w0_grid:
            point = evaluate_model_a(float(u), float(w0_today))
            if point is not None:
                results.append(point)
    return results


def scan_model_b() -> list[ModelPoint]:
    u_grid = np.geomspace(0.15, MODEL_B_U_MAX, 36)
    beta_grid = np.linspace(-0.12, 0.12, 49)
    results: list[ModelPoint] = []
    for u in u_grid:
        previous_bare: float | None = None
        for beta in beta_grid:
            point, previous_bare = evaluate_model_b(float(u), float(beta), guess=previous_bare)
            if point is not None:
                results.append(point)
    return results


def tau_unconstrained_model_b(points: list[ModelPoint], summary: ChainSummary) -> bool:
    model_points = [point for point in points if point.model == "B"]
    if not model_points:
        return False
    chi2_values = np.array([chain_chi2(point, summary) for point in model_points], dtype=float)
    chi2_min = float(np.min(chi2_values))
    tied = [
        point
        for point, chi2 in zip(model_points, chi2_values, strict=True)
        if abs(chi2 - chi2_min) < 1.0e-9
    ]
    distinct_u = {round(point.u, 10) for point in tied}
    return len(distinct_u) > 1 and all(abs(point.beta or 0.0) < 1.0e-12 for point in tied)


def select_best_points(points: list[ModelPoint], summaries: dict[str, ChainSummary]) -> dict[str, dict[str, dict[str, float | str | None]]]:
    grouped: dict[str, dict[str, dict[str, float | str | None]]] = {"A": {}, "B": {}}
    for model_name in ("A", "B"):
        model_points = [point for point in points if point.model == model_name]
        for dataset_name, summary in summaries.items():
            best_point = min(model_points, key=lambda point: chain_chi2(point, summary))
            grouped[model_name][dataset_name] = {
                "chi2": chain_chi2(best_point, summary),
                "inside_95pct_ellipse": chain_chi2(best_point, summary) <= 5.99,
                "tau_unconstrained": tau_unconstrained_model_b(points, summary) if model_name == "B" else False,
                "u": best_point.u,
                "tau_gyr": best_point.tau_gyr,
                "w0": best_point.w0,
                "wa": best_point.wa,
                "bare_density": best_point.bare_density,
                "delta": best_point.delta,
                "beta": best_point.beta,
                "a0_predicted": best_point.a0_predicted,
                "a0_factor_needed": best_point.a0_factor_needed,
                "z_cross_w_minus_one": best_point.z_cross_w_minus_one,
                "z_h_equals_tau_inv": best_point.z_h_equals_tau_inv,
                "cpl_rms": best_point.cpl_rms,
                "h_ratio_z05": best_point.h_ratio_z05,
                "h_ratio_z10": best_point.h_ratio_z10,
            }
    return grouped


def dataset_summary_table(summaries: dict[str, ChainSummary]) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for name in DATASET_ORDER:
        summary = summaries[name]
        rows.append(
            {
                "name": name,
                "label": summary.label,
                "w0_mean": float(summary.mean[0]),
                "wa_mean": float(summary.mean[1]),
                "w0_sigma": float(math.sqrt(summary.cov[0, 0])),
                "wa_sigma": float(math.sqrt(summary.cov[1, 1])),
                "corr": float(summary.cov[0, 1] / math.sqrt(summary.cov[0, 0] * summary.cov[1, 1])),
            }
        )
    return rows


def primary_best_point(points: list[ModelPoint], summaries: dict[str, ChainSummary], model_name: str) -> ModelPoint:
    relevant = [point for point in points if point.model == model_name]
    summary = summaries[PRIMARY_DATASET]
    return min(relevant, key=lambda point: chain_chi2(point, summary))


def plot_w0_wa(points: list[ModelPoint], summaries: dict[str, ChainSummary]) -> None:
    primary = summaries[PRIMARY_DATASET]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.0), constrained_layout=True)
    for axis, model_name, color in zip(axes, ("A", "B"), ("#1f77b4", "#d95f02"), strict=True):
        model_points = [point for point in points if point.model == model_name]
        axis.scatter(
            [point.w0 for point in model_points],
            [point.wa for point in model_points],
            s=10,
            color=color,
            alpha=0.45,
            linewidths=0.0,
        )
        for delta_chi2, alpha in ((5.99, 0.18), (2.30, 0.35)):
            ex, ey = ellipse_points(primary.mean, primary.cov, delta_chi2)
            axis.fill(ex, ey, color=DATASET_COLORS[PRIMARY_DATASET], alpha=alpha, linewidth=0.0)
            axis.plot(ex, ey, color=DATASET_COLORS[PRIMARY_DATASET], linewidth=1.2)
        axis.scatter([primary.mean[0]], [primary.mean[1]], color="black", s=34, zorder=3)
        axis.set_title(f"Model {model_name}")
        axis.set_xlabel(r"$w_0$")
        axis.set_ylabel(r"$w_a$")
        axis.set_xlim(-1.55, -0.25)
        axis.set_ylim(-2.2, 0.8)
        axis.grid(alpha=0.2)
    fig.suptitle("Vacuum-lag model manifolds vs DESI DR2 + DES Y5 SN")
    fig.savefig(PLOT_ROOT / "vacuum_lag_w0_wa.png", dpi=200)
    plt.close(fig)


def plot_wz(points: list[ModelPoint], summaries: dict[str, ChainSummary]) -> None:
    primary_summary = summaries[PRIMARY_DATASET]
    best_a = primary_best_point(points, summaries, "A")
    best_b = primary_best_point(points, summaries, "B")
    z = np.linspace(0.0, Z_DESI_MAX, 300)
    fig, ax = plt.subplots(figsize=(8.2, 5.4), constrained_layout=True)
    ax.plot(z, cpl_w(z, primary_summary.mean[0], primary_summary.mean[1]), color="black", linewidth=2.0, label="DESI mean CPL")
    ax.plot(TARGET_Z, best_a.wz_targets, color="#1f77b4", linewidth=2.0, marker="o", label="Model A best fit")
    ax.plot(TARGET_Z, best_b.wz_targets, color="#d95f02", linewidth=2.0, marker="s", label="Model B best fit")
    ax.axhline(-1.0, color="#666666", linestyle="--", linewidth=1.0)
    ax.set_xlabel("z")
    ax.set_ylabel("w(z)")
    ax.set_ylim(-1.4, -0.2)
    ax.grid(alpha=0.2)
    ax.legend()
    fig.savefig(PLOT_ROOT / "vacuum_lag_wz.png", dpi=200)
    plt.close(fig)


def plot_h_ratio(points: list[ModelPoint], summaries: dict[str, ChainSummary]) -> None:
    best_a = primary_best_point(points, summaries, "A")
    best_b = primary_best_point(points, summaries, "B")
    z = TARGET_Z
    fig, ax = plt.subplots(figsize=(8.2, 5.0), constrained_layout=True)
    ax.plot(z, np.array(best_a.hz_targets) / lcdm_e(z), color="#1f77b4", linewidth=2.0, marker="o", label="Model A / LCDM")
    ax.plot(z, np.array(best_b.hz_targets) / lcdm_e(z), color="#d95f02", linewidth=2.0, marker="s", label="Model B / LCDM")
    ax.axhline(1.0, color="#666666", linestyle="--", linewidth=1.0)
    ax.set_xlabel("z")
    ax.set_ylabel(r"$H(z) / H_{\Lambda{\rm CDM}}(z)$")
    ax.grid(alpha=0.2)
    ax.legend()
    fig.savefig(PLOT_ROOT / "vacuum_lag_h_ratio.png", dpi=200)
    plt.close(fig)


def plot_a0(best_table: dict[str, dict[str, dict[str, float | str | None]]]) -> None:
    x = np.arange(len(DATASET_ORDER), dtype=float)
    width = 0.34
    fig, ax = plt.subplots(figsize=(9.0, 5.0), constrained_layout=True)
    model_a = [best_table["A"][name]["a0_predicted"] for name in DATASET_ORDER]
    model_b = [
        np.nan if bool(best_table["B"][name]["tau_unconstrained"]) else best_table["B"][name]["a0_predicted"]
        for name in DATASET_ORDER
    ]
    ax.bar(x - width / 2.0, model_a, width=width, color="#1f77b4", label="Model A")
    finite_mask = np.isfinite(model_b)
    if np.any(finite_mask):
        ax.bar(x[finite_mask] + width / 2.0, np.array(model_b)[finite_mask], width=width, color="#d95f02", label="Model B")
    ax.axhline(A0_OBSERVED, color="black", linestyle="--", linewidth=1.4, label="Observed a0")
    for idx, dataset_name in enumerate(DATASET_ORDER):
        if bool(best_table["B"][dataset_name]["tau_unconstrained"]):
            ax.text(x[idx] + width / 2.0, A0_OBSERVED * 1.8, "tau unconstrained", rotation=90, ha="center", va="bottom", fontsize=8, color="#555555")
    ax.set_xticks(x, ["CMB", "Pantheon+", "DES Y5", "Union3"])
    ax.set_ylabel(r"$a_0$ predicted from $c / \tau$ [m s$^{-2}$]")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(alpha=0.2, axis="y")
    fig.savefig(PLOT_ROOT / "vacuum_lag_a0_predictions.png", dpi=200)
    plt.close(fig)


def observed_tau_from_mond() -> dict[str, float]:
    tau_seconds = C_LIGHT / A0_OBSERVED
    tau_gyr = tau_seconds / SEC_PER_GYR
    u = H0_SI * tau_seconds
    return {
        "tau_seconds": float(tau_seconds),
        "tau_gyr": float(tau_gyr),
        "u": float(u),
        "h_equals_tau_inv_over_h0": float(1.0 / u),
    }


def count_crossings(points: list[ModelPoint], model_name: str) -> int:
    return sum(
        point.z_cross_w_minus_one is not None
        for point in points
        if point.model == model_name
    )


def write_report(
    summaries: dict[str, ChainSummary],
    points: list[ModelPoint],
    best_table: dict[str, dict[str, dict[str, float | str | None]]],
) -> None:
    primary_summary = summaries[PRIMARY_DATASET]
    best_a = primary_best_point(points, summaries, "A")
    best_b = primary_best_point(points, summaries, "B")
    mond_link = observed_tau_from_mond()
    primary_cpl_cross = None
    if primary_summary.mean[1] != 0.0:
        numerator = -1.0 - primary_summary.mean[0]
        frac = numerator / primary_summary.mean[1]
        if 0.0 < frac < 1.0:
            primary_cpl_cross = frac / (1.0 - frac)

    lines: list[str] = []
    lines.append("# Vacuum Lag vs DESI DR2")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(
        f"I tested two late-time vacuum-lag backgrounds using the local official DESI DR2 public `base_w_wa` chains already present in the repo and fixed today's cosmology to `H0 = {H0_KM_S_MPC:.1f} km/s/Mpc`, `Omega_m = {OMEGA_M:.3f}`, `Omega_DE = {OMEGA_DE:.3f}`."
    )
    lines.append("")
    lines.append(
        f"- Model A: `d rho_vac / dt = -(rho_vac - rho_Lambda,bare) / tau`, with today's `w0` used as the stable second parameter and the implied early-time offset `delta` reported at `z_init = {Z_INIT:.0f}`"
    )
    lines.append(
        f"- Model B: `d rho_vac / dt = -(rho_vac - (rho_Lambda,bare + beta rho_m)) / tau`, with `beta` free and `rho_vac(z_init) = rho_eq(z_init)` enforced"
    )
    lines.append("")
    lines.append("Weighted DESI chain summaries are:")
    lines.append("")
    for row in dataset_summary_table(summaries):
        lines.append(
            f"- {row['label']}: `w0 = {row['w0_mean']:.3f} +- {row['w0_sigma']:.3f}`, `wa = {row['wa_mean']:.3f} +- {row['wa_sigma']:.3f}`"
        )
    lines.append("")
    lines.append("## Structural Result")
    lines.append("")
    lines.append(
        "For a first-order relaxation equation, `rho_vac(t)` is an exponential memory average of the target `rho_eq(t)`. If the target is constant (Model A), the sign of `rho_vac - rho_eq` never flips. If the target is monotonic in time (Model B with constant `beta` because `rho_m` is monotonic), the lag keeps the same sign as well."
    )
    lines.append("")
    lines.append(
        "Numerically, I found no phantom-to-quintessence crossing anywhere in the scanned parameter grids:"
    )
    lines.append("")
    lines.append(f"- Model A crossings found: `{count_crossings(points, 'A')}`")
    lines.append(f"- Model B crossings found: `{count_crossings(points, 'B')}`")
    lines.append("")
    lines.append(
        "So this specific ODE family does not realize the advertised `w < -1` at high z and `w > -1` at low z behavior. The sign of `w + 1` stays fixed."
    )
    lines.append("")
    lines.append("## Best Fits To DESI")
    lines.append("")
    lines.append(
        "I used the weighted DESI `w0-wa` means and covariances as a Gaussian proxy likelihood. `chi2 <= 5.99` corresponds roughly to being inside the 95% ellipse in the `w0-wa` plane."
    )
    lines.append("")
    for dataset_name in DATASET_ORDER:
        lines.append(f"### {DATASET_LABELS[dataset_name]}")
        lines.append("")
        row_a = best_table["A"][dataset_name]
        row_b = best_table["B"][dataset_name]
        lines.append(
            f"- Model A: `tau = {row_a['tau_gyr']:.2f} Gyr = {row_a['u']:.2f} / H0`, `delta(z={Z_INIT:.0f}) = {row_a['delta']:.3g}`, `w0 = {row_a['w0']:.3f}`, `wa = {row_a['wa']:.3f}`, `chi2 = {row_a['chi2']:.2f}`, inside 95% = `{row_a['inside_95pct_ellipse']}`"
        )
        if bool(row_b["tau_unconstrained"]):
            lines.append(
                f"- Model B: best fit is the exact `beta = 0` LCDM branch, so `tau` is unconstrained by DESI; representative background point has `w0 = {row_b['w0']:.3f}`, `wa = {row_b['wa']:.3f}`, `chi2 = {row_b['chi2']:.2f}`, inside 95% = `{row_b['inside_95pct_ellipse']}`"
            )
        else:
            lines.append(
                f"- Model B: `tau = {row_b['tau_gyr']:.2f} Gyr = {row_b['u']:.2f} / H0`, `beta = {row_b['beta']:.4f}`, `w0 = {row_b['w0']:.3f}`, `wa = {row_b['wa']:.3f}`, `chi2 = {row_b['chi2']:.2f}`, inside 95% = `{row_b['inside_95pct_ellipse']}`"
            )
        lines.append("")
    lines.append("For the DES Y5 combination, which matches the user-specified `w0 ~ -0.75`, `wa ~ -0.86`, the best fits are:")
    lines.append("")
    lines.append(
        f"- Model A: `tau = {best_a.tau_gyr:.2f} Gyr`, `u = {best_a.u:.2f}`, `delta = {best_a.delta:.3g}`, `w0 = {best_a.w0:.3f}`, `wa = {best_a.wa:.3f}`, `chi2 = {chain_chi2(best_a, primary_summary):.2f}`"
    )
    if tau_unconstrained_model_b(points, primary_summary):
        lines.append(
            f"- Model B: `beta = 0` collapses exactly to LCDM, so DESI leaves `tau` unconstrained; the background sits at `w0 = {best_b.w0:.3f}`, `wa = {best_b.wa:.3f}`, `chi2 = {chain_chi2(best_b, primary_summary):.2f}`"
        )
    else:
        lines.append(
            f"- Model B: `tau = {best_b.tau_gyr:.2f} Gyr`, `u = {best_b.u:.2f}`, `beta = {best_b.beta:.4f}`, `w0 = {best_b.w0:.3f}`, `wa = {best_b.wa:.3f}`, `chi2 = {chain_chi2(best_b, primary_summary):.2f}`"
        )
    lines.append("")
    lines.append("Both models miss the DESI-preferred quadrant for the same reason: they do not generate a sign flip in `w + 1`.")
    if best_a.u >= 0.98 * MODEL_A_U_MAX:
        lines.append("")
        lines.append(
            f"For Model A the fit keeps improving toward the slow-relaxation edge of the scan (`u = {MODEL_A_U_MAX:.0f}`), so DESI is effectively pushing this model toward the near-static limit rather than selecting a finite `tau`."
        )
    lines.append("")
    lines.append("## MOND Link Test")
    lines.append("")
    lines.append(
        f"The observed MOND scale implies `tau_MOND = c / a0 = {mond_link['tau_gyr']:.2f} Gyr = {mond_link['u']:.2f} / H0`."
    )
    lines.append("")
    lines.append(
        f"- Model A best-fit DES Y5 prediction within the scanned range: `a0 = {best_a.a0_predicted:.3e} m/s^2`, factor needed to hit the observed value = `{best_a.a0_factor_needed:.3f}`"
    )
    if tau_unconstrained_model_b(points, primary_summary):
        lines.append(
            "- Model B does not give a usable `a0` prediction here, because the DESI fit runs to the exact `beta = 0` LCDM branch where `tau` drops out of the background entirely."
        )
    else:
        lines.append(
            f"- Model B best-fit DES Y5 prediction: `a0 = {best_b.a0_predicted:.3e} m/s^2`, factor needed to hit the observed value = `{best_b.a0_factor_needed:.3f}`"
        )
    lines.append("")
    if best_a.a0_factor_needed <= 5.0:
        lines.append(
            "Model A is at least in the right ballpark numerically, but that near-miss does not rescue it because the `w(z)` shape still misses DESI badly."
        )
    else:
        lines.append(
            "Model A is not close to MOND once the fit is allowed to drift toward the slow-relaxation limit, and Model B does not constrain `tau` at all on its best-fit branch."
        )
    lines.append("")
    lines.append("## Cross-Checks")
    lines.append("")
    lines.append(
        f"- DES Y5 CPL mean crosses `w = -1` at `z ~= {primary_cpl_cross:.2f}`" if primary_cpl_cross is not None else "- The DES Y5 CPL mean does not cross `w = -1` in the past light cone."
    )
    lines.append(
        f"- Model A DES Y5 best-fit crossing: `{best_a.z_cross_w_minus_one}`"
    )
    lines.append(f"- Model B DES Y5 best-fit crossing: `{best_b.z_cross_w_minus_one}`")
    lines.append(
        f"- If you instead impose the hypothesis `H = 1 / tau` as the crossover condition, MOND's `tau` gives `1/tau = {mond_link['h_equals_tau_inv_over_h0']:.3f} H0`, which is below the entire past expansion history since `H(z >= 0) >= H0`. That criterion predicts no positive-redshift crossover at all."
    )
    lines.append(
        f"- Relative to LCDM with the same `H0`, Model A gives `H/H_LCDM = {best_a.h_ratio_z05:.3f}` at `z=0.5` and `{best_a.h_ratio_z10:.3f}` at `z=1.0`"
    )
    lines.append(
        f"- Relative to LCDM with the same `H0`, Model B gives `H/H_LCDM = {best_b.h_ratio_z05:.3f}` at `z=0.5` and `{best_b.h_ratio_z10:.3f}` at `z=1.0`"
    )
    lines.append(
        "- Lower-than-LCDM `H(z)` at intermediate redshift could in principle help with a higher local `H0`, but these backgrounds are not tuned enough to make a clean claim without refitting the actual distance data."
    )
    lines.append(
        "- The model does not supply a controlled definition of an effective dark-matter fraction. A proxy such as `|rho_vac - rho_eq|` can grow at high z, but that is not the same thing as producing the right clustering source term."
    )
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append("This two-parameter first-order vacuum-lag idea does not pass the DESI shape test.")
    lines.append("")
    lines.append("- The math is well behaved over part of parameter space, but the desired phantom-to-quintessence crossover does not happen in either simple model.")
    lines.append("- In `w0-wa` space, the accessible manifolds sit away from the DESI-preferred region; the best points generally remain outside the 95% ellipse for the main combined datasets.")
    lines.append("- The `a0 = c / tau` link does not survive the fit: Model A is driven toward `tau >> c / a0`, while Model B leaves `tau` unconstrained on its best-fit `beta = 0` branch.")
    lines.append("- Model B is especially fragile conceptually: `rho_eq = rho_Lambda,bare + beta rho_m` is monotonic, so with first-order relaxation it cannot make `w + 1` change sign without extra structure.")
    lines.append("")
    lines.append("The obvious next step, if this direction is to be salvaged at all, is not a different parameter fit. It needs a different dynamical law: a non-monotonic target, a time-dependent coupling, or higher-order vacuum dynamics that can overshoot.")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines))


def main() -> None:
    PLOT_ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    summaries = {name: load_dataset(name) for name in DATASET_ORDER}
    points_a = scan_model_a()
    points_b = scan_model_b()
    all_points = points_a + points_b
    best_table = select_best_points(all_points, summaries)

    plot_w0_wa(all_points, summaries)
    plot_wz(all_points, summaries)
    plot_h_ratio(all_points, summaries)
    plot_a0(best_table)
    write_report(summaries, all_points, best_table)

    payload = {
        "constants": {
            "H0_km_s_mpc": H0_KM_S_MPC,
            "H0_inverse_gyr": H0_INV_GYR,
            "Omega_m": OMEGA_M,
            "Omega_DE": OMEGA_DE,
            "a0_observed": A0_OBSERVED,
            "z_init": Z_INIT,
        },
        "datasets": dataset_summary_table(summaries),
        "best_fits": best_table,
        "mond_tau": observed_tau_from_mond(),
        "counts": {
            "model_a_points": len(points_a),
            "model_b_points": len(points_b),
            "model_a_crossings": count_crossings(all_points, "A"),
            "model_b_crossings": count_crossings(all_points, "B"),
        },
    }
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
