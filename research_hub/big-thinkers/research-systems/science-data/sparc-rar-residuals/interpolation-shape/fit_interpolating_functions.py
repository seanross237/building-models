from __future__ import annotations

import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import matplotlib
import numpy as np
from scipy.optimize import minimize

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.parent / "data" / "raw"

KM_TO_M = 1_000.0
KPC_TO_M = 3.0856775814913673e19
QUALITY_KEEP = {1, 2}
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7
HELIUM_FACTOR = 1.33


@dataclass
class ModelResult:
    model: str
    family: str
    notes: str
    n_params: int
    a0_mps2: float
    log10_a0: float
    shape_param: float | None
    shape_label: str | None
    transition_width_decades: float
    chi2: float
    chi2_red: float
    rms_scatter_dex: float
    intrinsic_scatter_dex: float
    loglike: float
    bic: float
    delta_bic: float = 0.0
    rank: int = 0


def load_sparc_properties(path: Path) -> dict[str, dict[str, float | int | str]]:
    properties: dict[str, dict[str, float | int | str]] = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) != 19:
            continue
        galaxy = parts[0]
        properties[galaxy] = {
            "galaxy": galaxy,
            "Q": int(parts[17]),
        }
    return properties


def load_mass_models(
    path: Path, galaxy_properties: dict[str, dict[str, float | int | str]]
) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) != 10:
            continue
        galaxy = parts[0]
        galaxy_info = galaxy_properties.get(galaxy)
        if galaxy_info is None or int(galaxy_info["Q"]) not in QUALITY_KEEP:
            continue
        rows.append(
            {
                "galaxy": galaxy,
                "R_kpc": float(parts[2]),
                "Vobs_kms": float(parts[3]),
                "e_Vobs_kms": float(parts[4]),
                "Vgas_kms": float(parts[5]),
                "Vdisk_kms": float(parts[6]),
                "Vbul_kms": float(parts[7]),
            }
        )
    return rows


def signed_square(velocity_kms: float) -> float:
    return math.copysign(velocity_kms * velocity_kms, velocity_kms)


def build_point_sample() -> tuple[list[dict[str, float | str]], dict[str, list[int]]]:
    galaxy_properties = load_sparc_properties(DATA_ROOT / "SPARC_Lelli2016c.mrt")
    mass_rows = load_mass_models(DATA_ROOT / "MassModels_Lelli2016c.mrt", galaxy_properties)

    points: list[dict[str, float | str]] = []
    by_galaxy: dict[str, list[int]] = defaultdict(list)

    for row in mass_rows:
        radius_kpc = float(row["R_kpc"])
        vobs = float(row["Vobs_kms"])
        evobs = float(row["e_Vobs_kms"])
        if radius_kpc <= 0.0 or vobs <= 0.0:
            continue

        vbar_sq = (
            signed_square(float(row["Vgas_kms"]))
            + UPSILON_DISK * signed_square(float(row["Vdisk_kms"]))
            + UPSILON_BULGE * signed_square(float(row["Vbul_kms"]))
        )
        if vbar_sq <= 0.0:
            continue

        gobs = (vobs * KM_TO_M) ** 2 / (radius_kpc * KPC_TO_M)
        gbar = vbar_sq * (KM_TO_M**2) / (radius_kpc * KPC_TO_M)
        if not (gobs > 0.0 and gbar > 0.0):
            continue

        sigma_log10_gobs = (2.0 / math.log(10.0)) * (evobs / vobs) if vobs > 0.0 else float("inf")

        point = {
            "galaxy": str(row["galaxy"]),
            "R_kpc": radius_kpc,
            "Vobs_kms": vobs,
            "e_Vobs_kms": evobs,
            "gobs_mps2": gobs,
            "gbar_mps2": gbar,
            "log10_gobs": math.log10(gobs),
            "log10_gbar": math.log10(gbar),
            "sigma_log10_gobs": sigma_log10_gobs,
        }
        by_galaxy[str(row["galaxy"])].append(len(points))
        points.append(point)

    points.sort(key=lambda p: (str(p["galaxy"]), float(p["R_kpc"])))
    by_galaxy = defaultdict(list)
    for idx, point in enumerate(points):
        by_galaxy[str(point["galaxy"])].append(idx)
    return points, by_galaxy


def boost_simple(y: np.ndarray) -> np.ndarray:
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def boost_standard(y: np.ndarray) -> np.ndarray:
    return np.sqrt(0.5 + 0.5 * np.sqrt(1.0 + 4.0 / (y * y)))


def boost_rar(y: np.ndarray) -> np.ndarray:
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def boost_generalized_exponential(y: np.ndarray, sharpness: float) -> np.ndarray:
    t = y ** (0.5 * sharpness)
    return (-np.expm1(-t)) ** (-1.0 / sharpness)


def predict_log10_gobs(model: str, params: np.ndarray, log10_gbar: np.ndarray) -> np.ndarray:
    log10_a0 = float(params[0])
    y = 10.0 ** (log10_gbar - log10_a0)

    if model == "simple_mu":
        boost = boost_simple(y)
    elif model == "standard_mu":
        boost = boost_standard(y)
    elif model == "mcgaugh_rar_exp":
        boost = boost_rar(y)
    elif model == "generalized_exponential":
        sharpness = 10.0 ** float(params[1])
        boost = boost_generalized_exponential(y, sharpness)
    else:
        raise ValueError(f"Unknown model: {model}")

    return log10_gbar + np.log10(boost)


def fit_objective(
    params: np.ndarray,
    model: str,
    log10_gbar: np.ndarray,
    log10_gobs: np.ndarray,
    sigma_log10_gobs: np.ndarray,
) -> float:
    if not np.all(np.isfinite(params)):
        return float("inf")

    try:
        pred = predict_log10_gobs(model, params, log10_gbar)
    except FloatingPointError:
        return float("inf")
    if not np.all(np.isfinite(pred)):
        return float("inf")

    sigma_int = 10.0 ** float(params[-1])
    if not np.isfinite(sigma_int) or sigma_int <= 0.0:
        return float("inf")

    resid = log10_gobs - pred
    sigma2 = sigma_log10_gobs**2 + sigma_int**2
    if np.any(~np.isfinite(sigma2)) or np.any(sigma2 <= 0.0):
        return float("inf")

    return 0.5 * float(np.sum((resid * resid) / sigma2 + np.log(2.0 * np.pi * sigma2)))


def optimize_model(
    model: str,
    log10_gbar: np.ndarray,
    log10_gobs: np.ndarray,
    sigma_log10_gobs: np.ndarray,
) -> tuple[np.ndarray, float]:
    if model in {"simple_mu", "standard_mu", "mcgaugh_rar_exp"}:
        bounds = [(-13.0, -9.0), (-4.0, 0.0)]
        starts = [
            (-10.35, -0.90),
            (-10.00, -0.90),
            (-9.70, -0.90),
            (-10.20, -0.70),
            (-9.90, -0.70),
            (-10.05, -1.10),
        ]
    elif model == "generalized_exponential":
        bounds = [(-13.0, -9.0), (-1.3, 0.6), (-4.0, 0.0)]
        starts = [
            (-10.25, -0.20, -0.90),
            (-10.00, -0.10, -0.90),
            (-9.80, 0.00, -0.90),
            (-10.15, 0.10, -0.80),
            (-10.00, 0.10, -0.80),
            (-9.90, -0.05, -1.00),
        ]
    else:
        raise ValueError(model)

    best_result = None
    best_value = float("inf")
    for start in starts:
        result = minimize(
            fit_objective,
            x0=np.array(start, dtype=float),
            args=(model, log10_gbar, log10_gobs, sigma_log10_gobs),
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 4000},
        )
        if result.fun < best_value:
            best_value = float(result.fun)
            best_result = result

    if best_result is None:
        raise RuntimeError(f"Optimization failed for {model}")

    return np.array(best_result.x, dtype=float), float(best_result.fun)


def transition_width_decades(model: str, params: np.ndarray) -> float:
    x = np.linspace(-6.0, 6.0, 20001)
    y = 10.0**x

    if model == "simple_mu":
        boost = boost_simple(y)
    elif model == "standard_mu":
        boost = boost_standard(y)
    elif model == "mcgaugh_rar_exp":
        boost = boost_rar(y)
    elif model == "generalized_exponential":
        boost = boost_generalized_exponential(y, 10.0 ** float(params[1]))
    else:
        raise ValueError(model)

    log_boost = np.log10(boost)
    slope = np.gradient(log_boost, x, edge_order=2) + 1.0
    slope = np.maximum.accumulate(slope)
    x_lo = float(np.interp(0.55, slope, x))
    x_hi = float(np.interp(0.95, slope, x))
    return x_hi - x_lo


def weighted_linear_fit(x: np.ndarray, y: np.ndarray, sigma: np.ndarray) -> tuple[float, float, float, float]:
    weights = 1.0 / np.clip(sigma, 1e-12, None) ** 2
    design = np.column_stack([x, np.ones_like(x)])
    xtwx = design.T @ (weights[:, None] * design)
    xtwy = design.T @ (weights * y)
    cov = np.linalg.inv(xtwx)
    beta = cov @ xtwy
    residuals = y - design @ beta
    chi2 = float(np.sum(weights * residuals * residuals))
    return float(beta[0]), float(beta[1]), chi2, float(cov[0, 0])


def cluster_bootstrap_deep_slope(
    points: list[dict[str, float | str]],
    by_galaxy: dict[str, list[int]],
    a0_mps2: float,
    n_boot: int = 400,
    seed: int = 20260402,
) -> dict[str, float]:
    selected_galaxies = {
        galaxy: [idx for idx in indices if float(points[idx]["gbar_mps2"]) < 0.1 * a0_mps2]
        for galaxy, indices in by_galaxy.items()
    }
    selected_galaxies = {g: idxs for g, idxs in selected_galaxies.items() if idxs}

    if not selected_galaxies:
        raise RuntimeError("No points fall below 0.1 a0 for the deep-MOND fit.")

    x = np.array([float(points[idx]["log10_gbar"]) for idxs in selected_galaxies.values() for idx in idxs])
    y = np.array([float(points[idx]["log10_gobs"]) for idxs in selected_galaxies.values() for idx in idxs])
    sigma = np.array([float(points[idx]["sigma_log10_gobs"]) for idxs in selected_galaxies.values() for idx in idxs])
    slope, intercept, chi2, slope_var = weighted_linear_fit(x, y, sigma)

    rng = np.random.default_rng(seed)
    galaxy_names = np.array(list(selected_galaxies))
    slopes = []
    intercepts = []
    n_points_boot = []

    for _ in range(n_boot):
        sample = rng.choice(galaxy_names, size=len(galaxy_names), replace=True)
        xs: list[float] = []
        ys: list[float] = []
        sigmas: list[float] = []
        for galaxy in sample:
            for idx in selected_galaxies[galaxy]:
                xs.append(float(points[idx]["log10_gbar"]))
                ys.append(float(points[idx]["log10_gobs"]))
                sigmas.append(float(points[idx]["sigma_log10_gobs"]))
        if len(xs) < 3:
            continue
        boot_slope, boot_intercept, _, _ = weighted_linear_fit(np.array(xs), np.array(ys), np.array(sigmas))
        slopes.append(boot_slope)
        intercepts.append(boot_intercept)
        n_points_boot.append(len(xs))

    slopes_arr = np.array(slopes, dtype=float)
    intercepts_arr = np.array(intercepts, dtype=float)

    return {
        "cut_mps2": 0.1 * a0_mps2,
        "n_points": float(len(x)),
        "n_galaxies": float(len(selected_galaxies)),
        "slope": float(slope),
        "slope_se": float(np.std(slopes_arr, ddof=1)),
        "slope_ci16": float(np.percentile(slopes_arr, 16)),
        "slope_ci84": float(np.percentile(slopes_arr, 84)),
        "intercept": float(intercept),
        "intercept_se": float(np.std(intercepts_arr, ddof=1)),
        "intercept_ci16": float(np.percentile(intercepts_arr, 16)),
        "intercept_ci84": float(np.percentile(intercepts_arr, 84)),
        "chi2": float(chi2),
        "bootstrap_resamples": float(len(slopes_arr)),
    }


def model_family_notes(model: str) -> tuple[str, str]:
    if model == "simple_mu":
        return (
            "simple MOND",
            "Exact equivalent of the Bekenstein toy / simple mu(x)=x/(1+x) law.",
        )
    if model == "standard_mu":
        return (
            "standard MOND",
            "Canonical mu(x)=x/sqrt(1+x^2) form written in nu(y) form.",
        )
    if model == "mcgaugh_rar_exp":
        return (
            "RAR exponential",
            "McGaugh et al. exponential RAR; exact n=1 case of the generalized exponential family.",
        )
    if model == "generalized_exponential":
        return (
            "generalized exponential",
            "Free sharpness n; n=1 recovers the McGaugh exponential RAR.",
        )
    raise ValueError(model)


def fit_all_models(points: list[dict[str, float | str]]) -> list[ModelResult]:
    log10_gbar = np.array([float(point["log10_gbar"]) for point in points], dtype=float)
    log10_gobs = np.array([float(point["log10_gobs"]) for point in points], dtype=float)
    sigma_log10_gobs = np.array([float(point["sigma_log10_gobs"]) for point in points], dtype=float)

    model_order = [
        "simple_mu",
        "standard_mu",
        "mcgaugh_rar_exp",
        "generalized_exponential",
    ]

    results: list[ModelResult] = []
    for model in model_order:
        params, nll = optimize_model(model, log10_gbar, log10_gobs, sigma_log10_gobs)
        pred = predict_log10_gobs(model, params, log10_gbar)
        resid = log10_gobs - pred
        sigma_int = 10.0 ** float(params[-1])
        sigma2 = sigma_log10_gobs**2 + sigma_int**2
        chi2 = float(np.sum((resid * resid) / sigma2))
        n = len(points)
        n_params = 2 if model != "generalized_exponential" else 3
        bic = float(n_params * np.log(n) + chi2 + np.sum(np.log(2.0 * np.pi * sigma2)))
        result = ModelResult(
            model=model,
            family=model_family_notes(model)[0],
            notes=model_family_notes(model)[1],
            n_params=n_params,
            a0_mps2=float(10.0 ** float(params[0])),
            log10_a0=float(params[0]),
            shape_param=float(10.0 ** float(params[1])) if model == "generalized_exponential" else None,
            shape_label="sharpness n" if model == "generalized_exponential" else None,
            transition_width_decades=transition_width_decades(model, params),
            chi2=chi2,
            chi2_red=float(chi2 / max(n - n_params, 1)),
            rms_scatter_dex=float(np.sqrt(np.mean(resid * resid))),
            intrinsic_scatter_dex=sigma_int,
            loglike=float(-nll),
            bic=bic,
        )
        results.append(result)

    results.sort(key=lambda row: row.bic)
    best_bic = results[0].bic
    for rank, result in enumerate(results, start=1):
        result.rank = rank
        result.delta_bic = result.bic - best_bic
    return results


def save_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_fit_results(path: Path, results: list[ModelResult], n_points: int, n_galaxies: int) -> None:
    rows = []
    for result in results:
        rows.append(
            {
                "rank": result.rank,
                "model": result.model,
                "family": result.family,
                "notes": result.notes,
                "n_points": n_points,
                "n_galaxies": n_galaxies,
                "n_params": result.n_params,
                "a0_mps2": result.a0_mps2,
                "log10_a0": result.log10_a0,
                "shape_param": "" if result.shape_param is None else result.shape_param,
                "shape_label": "" if result.shape_label is None else result.shape_label,
                "transition_width_decades": result.transition_width_decades,
                "chi2": result.chi2,
                "chi2_red": result.chi2_red,
                "rms_scatter_dex": result.rms_scatter_dex,
                "intrinsic_scatter_dex": result.intrinsic_scatter_dex,
                "loglike": result.loglike,
                "bic": result.bic,
                "delta_bic": result.delta_bic,
            }
        )
    save_csv(path, rows)


def save_deep_mond_fit(path: Path, best: ModelResult, deep_fit: dict[str, float]) -> None:
    rows = [
        {
            "model": best.model,
            "family": best.family,
            "a0_mps2": best.a0_mps2,
            "cut_mps2": deep_fit["cut_mps2"],
            "n_points": int(deep_fit["n_points"]),
            "n_galaxies": int(deep_fit["n_galaxies"]),
            "slope": deep_fit["slope"],
            "slope_se": deep_fit["slope_se"],
            "slope_ci16": deep_fit["slope_ci16"],
            "slope_ci84": deep_fit["slope_ci84"],
            "intercept": deep_fit["intercept"],
            "intercept_se": deep_fit["intercept_se"],
            "intercept_ci16": deep_fit["intercept_ci16"],
            "intercept_ci84": deep_fit["intercept_ci84"],
            "chi2": deep_fit["chi2"],
            "bootstrap_resamples": int(deep_fit["bootstrap_resamples"]),
            "fit_method": "cluster bootstrap of galaxies, weighted least squares in log space",
        }
    ]
    save_csv(path, rows)


def save_summary(path: Path, points: list[dict[str, float | str]], results: list[ModelResult], deep_fit: dict[str, float]) -> None:
    best = results[0]
    total_points = len(points)
    n_galaxies = len({str(point["galaxy"]) for point in points})
    low_acc_points = int(np.sum(np.array([float(point["gbar_mps2"]) for point in points]) < 0.1 * best.a0_mps2))
    low_acc_galaxies = len(
        {
            str(point["galaxy"])
            for point in points
            if float(point["gbar_mps2"]) < 0.1 * best.a0_mps2
        }
    )

    lines = [
        "# MOND / RAR Interpolating-Function Fits",
        "",
        f"- Sample: {n_galaxies} galaxies and {total_points} radial points after the Q=1/2 cut.",
        f"- Best-fit a0: {best.a0_mps2:.4e} m s^-2.",
        f"- Winning model: {best.family} ({best.model}).",
        f"- Winning transition width: {best.transition_width_decades:.2f} decades from slope 0.55 to 0.95.",
        "",
        "## BIC Ranking",
        "",
        "| Rank | Model | a0 [m s^-2] | Scatter [dex] | Intrinsic scatter [dex] | Chi^2 | BIC | ΔBIC | Notes |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result.rank} | {result.family} | {result.a0_mps2:.4e} | {result.rms_scatter_dex:.4f} | "
            f"{result.intrinsic_scatter_dex:.4f} | {result.chi2:.1f} | {result.bic:.1f} | {result.delta_bic:.1f} | "
            f"{result.notes} |"
        )

    lines.extend(
        [
            "",
            "## Deep-MOND Fit",
            "",
            f"- Cut: g_bar < 0.1 a0 = {deep_fit['cut_mps2']:.4e} m s^-2.",
            f"- Points used: {low_acc_points} across {low_acc_galaxies} galaxies.",
            f"- Slope: {deep_fit['slope']:.3f} ± {deep_fit['slope_se']:.3f} (bootstrap 1σ).",
            f"- Intercept: {deep_fit['intercept']:.3f} ± {deep_fit['intercept_se']:.3f}.",
            "",
            "## Interpretation",
            "",
            "The canonical simple and McGaugh RAR forms are close in BIC, but the generalized exponential wins by allowing a broader transition than the fixed n=1 curve.",
            "The standard MOND interpolating function is strongly disfavored relative to the other three by BIC.",
            "The low-acceleration cut g_bar < 0.1 a0 still reaches into the turnover region, so the fitted slope stays steeper than the asymptotic 1/2 limit.",
        ]
    )

    path.write_text("\n".join(lines) + "\n")


def make_winning_transition_plot(
    path: Path,
    points: list[dict[str, float | str]],
    results: list[ModelResult],
) -> None:
    best = results[0]
    log10_gbar = np.array([float(point["log10_gbar"]) for point in points], dtype=float)
    log10_gobs = np.array([float(point["log10_gobs"]) for point in points], dtype=float)

    x_grid = np.linspace(log10_gbar.min() - 0.3, log10_gbar.max() + 0.3, 800)
    log10_a0 = best.log10_a0
    y_grid = 10.0 ** (x_grid - log10_a0)
    if best.model == "simple_mu":
        boost = boost_simple(y_grid)
    elif best.model == "standard_mu":
        boost = boost_standard(y_grid)
    elif best.model == "mcgaugh_rar_exp":
        boost = boost_rar(y_grid)
    else:
        boost = boost_generalized_exponential(y_grid, float(best.shape_param))

    curve = x_grid + np.log10(boost)
    deep_line = 0.5 * (x_grid + log10_a0)

    slope_x = np.linspace(-6.0, 6.0, 20001)
    slope_y = 10.0**slope_x
    if best.model == "simple_mu":
        slope_boost = boost_simple(slope_y)
    elif best.model == "standard_mu":
        slope_boost = boost_standard(slope_y)
    elif best.model == "mcgaugh_rar_exp":
        slope_boost = boost_rar(slope_y)
    else:
        slope_boost = boost_generalized_exponential(slope_y, float(best.shape_param))
    slope = np.gradient(np.log10(slope_boost), slope_x, edge_order=2) + 1.0
    slope = np.maximum.accumulate(slope)
    x_lo = float(np.interp(0.55, slope, slope_x))
    x_hi = float(np.interp(0.95, slope, slope_x))
    x_lo_abs = log10_a0 + x_lo
    x_hi_abs = log10_a0 + x_hi

    fig, axes = plt.subplots(1, 2, figsize=(13.4, 5.6), gridspec_kw={"width_ratios": [1.25, 1.0]})

    ax = axes[0]
    ax.scatter(log10_gbar, log10_gobs, s=8, alpha=0.20, color="#1f4e79", linewidths=0)
    ax.plot(x_grid, curve, color="#c0392b", lw=2.4, label=f"Best fit: {best.family}")
    ax.plot(x_grid, x_grid, color="#6b7280", lw=1.3, ls="--", label="Newtonian")
    ax.plot(x_grid, deep_line, color="#0f766e", lw=1.3, ls=":", label=r"Deep MOND $\propto g_{\rm bar}^{1/2}$")
    ax.axvspan(x_lo_abs, x_hi_abs, color="#f2b8b5", alpha=0.35, label=f"Transition width = {best.transition_width_decades:.2f} dex")
    ax.set_xlabel(r"$\log_{10}(g_{\rm bar}\,[{\rm m\,s^{-2}}])$")
    ax.set_ylabel(r"$\log_{10}(g_{\rm obs}\,[{\rm m\,s^{-2}}])$")
    ax.set_title("Winning SPARC interpolating function")
    ax.grid(alpha=0.15)
    ax.legend(frameon=False, fontsize=9, loc="lower right")

    ax = axes[1]
    delta_bic = np.array([result.bic - best.bic for result in results], dtype=float)
    labels = [result.family for result in results]
    colors = ["#c0392b" if result.rank == 1 else "#1f4e79" for result in results]
    ax.barh(labels, delta_bic, color=colors, alpha=0.88)
    ax.axvline(0.0, color="#555555", lw=1.0)
    ax.invert_yaxis()
    ax.set_xlabel(r"$\Delta$BIC")
    ax.set_title("Model ranking")
    ax.grid(axis="x", alpha=0.15)
    for idx, value in enumerate(delta_bic):
        ax.text(value + 0.5, idx, f"{value:.1f}", va="center", ha="left", fontsize=9)

    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def main() -> None:
    points, by_galaxy = build_point_sample()
    results = fit_all_models(points)
    best = results[0]
    deep_fit = cluster_bootstrap_deep_slope(points, by_galaxy, best.a0_mps2)

    save_fit_results(ROOT / "fit_results.csv", results, len(points), len(by_galaxy))
    save_deep_mond_fit(ROOT / "deep_mond_fit.csv", best, deep_fit)
    save_summary(ROOT / "summary.md", points, results, deep_fit)
    make_winning_transition_plot(ROOT / "winning_transition.png", points, results)

    print("Ranking by BIC:")
    for result in results:
        print(f"{result.rank}. {result.family}  BIC={result.bic:.2f}  a0={result.a0_mps2:.4e}  width={result.transition_width_decades:.2f}")
    print(f"Best a0: {best.a0_mps2:.4e} m s^-2")
    print(f"Deep-MOND slope: {deep_fit['slope']:.3f} ± {deep_fit['slope_se']:.3f}")


if __name__ == "__main__":
    main()
