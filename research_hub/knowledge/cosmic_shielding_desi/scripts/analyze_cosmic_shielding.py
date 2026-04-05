#!/usr/bin/env python3

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import gaussian_filter

matplotlib.use("Agg")
from matplotlib import pyplot as plt

C_LIGHT_KM_S = 299792.458
N_EFF = 3.044
OMEGA_GAMMA_H2 = 2.4728e-5

ROOT = Path(__file__).resolve().parents[1]
CHAIN_ROOT = ROOT / "data" / "raw" / "desi_dr2_chains"
BAO_ROOT = ROOT / "data" / "raw" / "bao_data" / "desi_bao_dr2"
PROCESSED_ROOT = ROOT / "data" / "processed"
PLOT_ROOT = ROOT / "plots"
SUMMARY_PATH = PROCESSED_ROOT / "shielding_summary.json"
REPORT_PATH = ROOT / "notes" / "shielding_report.md"

DATASETS = {
    "cmb": {
        "label": "DESI DR2 + CMB",
        "color": "#264653",
    },
    "pantheonplus": {
        "label": "DESI DR2 + CMB + Pantheon+",
        "color": "#d1495b",
    },
    "desy5sn": {
        "label": "DESI DR2 + CMB + DES Y5 SN",
        "color": "#2a9d8f",
    },
    "union3": {
        "label": "DESI DR2 + CMB + Union3",
        "color": "#e9c46a",
    },
}

W0_RANGE = (-1.6, -0.2)
WA_RANGE = (-2.7, 0.9)
BAO_DATA: tuple[list[tuple[float, float, str]], np.ndarray] | None = None
BAO_INV_COV: np.ndarray | None = None


@dataclass
class ChainData:
    weights: np.ndarray
    w0: np.ndarray
    wa: np.ndarray
    omegam: np.ndarray
    omegal: np.ndarray
    H0: np.ndarray
    rdrag: np.ndarray


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(values * weights) / np.sum(weights))


def weighted_std(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    variance = np.sum(weights * (values - mean) ** 2) / np.sum(weights)
    return float(np.sqrt(variance))


def load_chain_file(path: Path) -> ChainData:
    with path.open() as handle:
        header = handle.readline().lstrip("#").split()
    indices = {name: idx for idx, name in enumerate(header)}
    usecols = [
        indices["weight"],
        indices["w"],
        indices["wa"],
        indices["omegam"],
        indices["omegal"],
        indices["H0"],
        indices["rdrag"],
    ]
    values = np.loadtxt(path, comments="#", usecols=usecols)
    return ChainData(
        weights=values[:, 0],
        w0=values[:, 1],
        wa=values[:, 2],
        omegam=values[:, 3],
        omegal=values[:, 4],
        H0=values[:, 5],
        rdrag=values[:, 6],
    )


def load_dataset(name: str) -> ChainData:
    arrays = []
    for path in sorted((CHAIN_ROOT / name).glob("chain.[1-4].txt")):
        arrays.append(load_chain_file(path))
    return ChainData(
        weights=np.concatenate([item.weights for item in arrays]),
        w0=np.concatenate([item.w0 for item in arrays]),
        wa=np.concatenate([item.wa for item in arrays]),
        omegam=np.concatenate([item.omegam for item in arrays]),
        omegal=np.concatenate([item.omegal for item in arrays]),
        H0=np.concatenate([item.H0 for item in arrays]),
        rdrag=np.concatenate([item.rdrag for item in arrays]),
    )


def posterior_grid(
    chain: ChainData,
    bins: int = 320,
    smooth_sigma: float = 1.5,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float], RegularGridInterpolator]:
    hist, xedges, yedges = np.histogram2d(
        chain.w0,
        chain.wa,
        bins=[bins, bins],
        range=[W0_RANGE, WA_RANGE],
        weights=chain.weights,
    )
    density = gaussian_filter(hist, smooth_sigma)
    flat = np.sort(density.ravel())[::-1]
    cumulative = np.cumsum(flat)
    total = cumulative[-1]
    levels = {}
    for frac in (0.68, 0.95, 0.99):
        idx = np.searchsorted(cumulative, frac * total)
        idx = min(idx, flat.size - 1)
        levels[f"{int(frac * 100)}"] = float(flat[idx])
    xcenters = 0.5 * (xedges[:-1] + xedges[1:])
    ycenters = 0.5 * (yedges[:-1] + yedges[1:])
    interpolator = RegularGridInterpolator(
        (xcenters, ycenters),
        density,
        bounds_error=False,
        fill_value=0.0,
    )
    return density, xcenters, ycenters, levels, interpolator


def q_from_alpha(alpha: float, omegam: float, omegal: float) -> float:
    return alpha * omegam / omegal


def alpha_from_w0(w0: float, omegam: float, omegal: float) -> float:
    return -(1.0 + w0) * omegal / omegam


def model_w0_wa(alpha: float, omegam: float, omegal: float) -> tuple[float, float]:
    q = q_from_alpha(alpha, omegam, omegal)
    w0 = -1.0 - q
    wa = -3.0 * q * (1.0 + q)
    return w0, wa


def density_ratio_z(z: float, alpha: float, omegam: float, omegal: float) -> float:
    q = q_from_alpha(alpha, omegam, omegal)
    return 1.0 + q - q * (1.0 + z) ** 3


def w_eff(z: np.ndarray, alpha: float, omegam: float, omegal: float) -> np.ndarray:
    q = q_from_alpha(alpha, omegam, omegal)
    ratio = density_ratio_z(z, alpha, omegam, omegal)
    out = -1.0 - q * (1.0 + z) ** 3 / ratio
    out = np.where(ratio <= 0.0, np.nan, out)
    return out


def cpl_w(z: np.ndarray, w0: float, wa: float) -> np.ndarray:
    return w0 + wa * z / (1.0 + z)


def omega_radiation(h: float) -> float:
    return OMEGA_GAMMA_H2 * (1.0 + 0.22710731766 * N_EFF) / (h * h)


def e2(z: float, alpha: float, omegam_phys: float, H0: float) -> float:
    h = H0 / 100.0
    omega_r = omega_radiation(h)
    omega_lambda_bare = 1.0 - omega_r - (1.0 - alpha) * omegam_phys
    return (
        omega_r * (1.0 + z) ** 4
        + (1.0 - alpha) * omegam_phys * (1.0 + z) ** 3
        + omega_lambda_bare
    )


def comoving_distance(z: float, alpha: float, omegam_phys: float, H0: float) -> float:
    integrand = lambda zp: 1.0 / math.sqrt(e2(zp, alpha, omegam_phys, H0))
    integral, _ = quad(integrand, 0.0, z, epsabs=1e-9, epsrel=1e-7, limit=200)
    return C_LIGHT_KM_S / H0 * integral


def bao_prediction(
    z: float,
    quantity: str,
    alpha: float,
    omegam_phys: float,
    H0: float,
    rdrag: float,
) -> float:
    dm = comoving_distance(z, alpha, omegam_phys, H0)
    dh = C_LIGHT_KM_S / H0 / math.sqrt(e2(z, alpha, omegam_phys, H0))
    if quantity == "DM_over_rs":
        return dm / rdrag
    if quantity == "DH_over_rs":
        return dh / rdrag
    if quantity == "DV_over_rs":
        dv = (z * dm * dm * dh) ** (1.0 / 3.0)
        return dv / rdrag
    raise ValueError(f"Unsupported BAO quantity: {quantity}")


def load_bao_data() -> tuple[list[tuple[float, float, str]], np.ndarray]:
    global BAO_DATA
    if BAO_DATA is not None:
        return BAO_DATA
    mean_rows: list[tuple[float, float, str]] = []
    with (BAO_ROOT / "desi_gaussian_bao_ALL_GCcomb_mean.txt").open() as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            z_text, value_text, quantity = line.split()
            mean_rows.append((float(z_text), float(value_text), quantity))
    cov = np.loadtxt(BAO_ROOT / "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    BAO_DATA = (mean_rows, cov)
    return BAO_DATA


def bao_chi2(alpha: float, omegam_phys: float, H0: float, rdrag: float) -> float:
    global BAO_INV_COV
    mean_rows, cov = load_bao_data()
    if BAO_INV_COV is None:
        BAO_INV_COV = np.linalg.inv(cov)
    theory = np.array(
        [
            bao_prediction(z, quantity, alpha, omegam_phys, H0, rdrag)
            for z, _, quantity in mean_rows
        ]
    )
    data = np.array([value for _, value, _ in mean_rows])
    residual = theory - data
    chi2 = residual @ BAO_INV_COV @ residual
    return float(chi2)


def curve_fit_summary(
    chain: ChainData,
    levels: dict[str, float],
    interpolator: RegularGridInterpolator,
) -> dict[str, float | bool]:
    omegam = weighted_mean(chain.omegam, chain.weights)
    omegal = weighted_mean(chain.omegal, chain.weights)
    alphas = np.linspace(-2.0, 2.0, 12001)
    samples = []
    for alpha in alphas:
        w0, wa = model_w0_wa(alpha, omegam, omegal)
        if not (W0_RANGE[0] <= w0 <= W0_RANGE[1] and WA_RANGE[0] <= wa <= WA_RANGE[1]):
            continue
        density = float(interpolator((w0, wa)))
        samples.append((alpha, w0, wa, density))
    best_alpha, best_w0, best_wa, best_density = max(samples, key=lambda item: item[3])
    return {
        "best_alpha": float(best_alpha),
        "best_w0": float(best_w0),
        "best_wa": float(best_wa),
        "best_density": float(best_density),
        "inside_68_hpd": bool(best_density >= levels["68"]),
        "inside_95_hpd": bool(best_density >= levels["95"]),
        "inside_99_hpd": bool(best_density >= levels["99"]),
    }


def zero_crossing_redshift(alpha: float, omegam: float, omegal: float) -> float | None:
    q = q_from_alpha(alpha, omegam, omegal)
    if q <= 0.0:
        return None
    return float(((1.0 + q) / q) ** (1.0 / 3.0) - 1.0)


def build_summary() -> dict[str, object]:
    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
    PLOT_ROOT.mkdir(parents=True, exist_ok=True)

    summary: dict[str, object] = {
        "model_equations": {
            "rho_de_eff": "rho_Lambda_bare - alpha * rho_m0 * (1+z)^3",
            "w_eff": "-1 - q(1+z)^3 / [1 + q - q(1+z)^3], q = alpha * Omega_m0 / Omega_DE0",
            "cpl_mapping": "w0 = -1 - q, wa = -3 q (1 + q) = -3 w0 (1 + w0)",
            "background_equivalence": "H^2/H0^2 = Omega_r(1+z)^4 + (1-alpha)Omega_m(1+z)^3 + Omega_Lambda_bare",
        }
    }

    pantheon_chain: ChainData | None = None
    pantheon_grid = None

    datasets_summary = {}
    for name, info in DATASETS.items():
        chain = load_dataset(name)
        density, xcenters, ycenters, levels, interpolator = posterior_grid(chain)
        fit = curve_fit_summary(chain, levels, interpolator)
        omegam = weighted_mean(chain.omegam, chain.weights)
        omegal = weighted_mean(chain.omegal, chain.weights)
        H0 = weighted_mean(chain.H0, chain.weights)
        rdrag = weighted_mean(chain.rdrag, chain.weights)
        w0_mean = weighted_mean(chain.w0, chain.weights)
        wa_mean = weighted_mean(chain.wa, chain.weights)
        alpha_w0_only = alpha_from_w0(w0_mean, omegam, omegal)
        datasets_summary[name] = {
            "label": info["label"],
            "mean_w0": w0_mean,
            "mean_wa": wa_mean,
            "std_w0": weighted_std(chain.w0, chain.weights),
            "std_wa": weighted_std(chain.wa, chain.weights),
            "mean_omegam": omegam,
            "mean_omegal": omegal,
            "mean_H0": H0,
            "mean_rdrag": rdrag,
            "alpha_from_mean_w0": alpha_w0_only,
            "omega_m_eff_if_matched_to_mean_w0": (1.0 - alpha_w0_only) * omegam,
            "zero_crossing_redshift_if_matched_to_mean_w0": zero_crossing_redshift(
                alpha_w0_only, omegam, omegal
            ),
            "curve_fit": fit,
            "curve_relation_at_mean": wa_mean + 3.0 * w0_mean * (1.0 + w0_mean),
        }
        if name == "pantheonplus":
            pantheon_chain = chain
            pantheon_grid = (density, xcenters, ycenters, levels)

    summary["datasets"] = datasets_summary

    reference = datasets_summary["pantheonplus"]
    omegam_ref = reference["mean_omegam"]
    H0_ref = reference["mean_H0"]
    rdrag_ref = reference["mean_rdrag"]

    alpha_scan = np.linspace(-0.6, 0.6, 721)
    chi2_scan = np.array(
        [bao_chi2(alpha, omegam_ref, H0_ref, rdrag_ref) for alpha in alpha_scan]
    )
    best_idx = int(np.argmin(chi2_scan))
    chi2_min = float(chi2_scan[best_idx])
    inside_95 = alpha_scan[(chi2_scan - chi2_min) <= 3.84]
    bao_summary = {
        "reference_anchor": "Pantheon+ chain weighted means for Omega_m, H0, and rdrag",
        "best_alpha": float(alpha_scan[best_idx]),
        "chi2_min": chi2_min,
        "chi2_alpha_0": float(bao_chi2(0.0, omegam_ref, H0_ref, rdrag_ref)),
        "alpha_95_interval": [
            float(np.min(inside_95)),
            float(np.max(inside_95)),
        ],
    }
    for name in DATASETS:
        alpha = datasets_summary[name]["alpha_from_mean_w0"]
        bao_summary[f"chi2_alpha_from_{name}_mean_w0"] = float(
            bao_chi2(alpha, omegam_ref, H0_ref, rdrag_ref)
        )
    summary["bao_anchor_test"] = bao_summary

    pantheon_alpha = float(reference["alpha_from_mean_w0"])
    fit_alpha = float(reference["curve_fit"]["best_alpha"])
    z_grid = np.linspace(0.0, 4.0, 401)
    summary["predictions"] = {
        "z_grid": z_grid.tolist(),
        "pantheonplus_mean_cpl": cpl_w(
            z_grid, reference["mean_w0"], reference["mean_wa"]
        ).tolist(),
        "pantheonplus_mean_shielding": w_eff(
            z_grid, pantheon_alpha, omegam_ref, reference["mean_omegal"]
        ).tolist(),
        "best_curve_shielding": w_eff(
            z_grid, fit_alpha, omegam_ref, reference["mean_omegal"]
        ).tolist(),
        "lcdm": (-1.0 * np.ones_like(z_grid)).tolist(),
        "pantheonplus_mean_shielding_alpha": pantheon_alpha,
        "best_curve_alpha": fit_alpha,
    }

    if pantheon_chain is not None and pantheon_grid is not None:
        make_w0wa_plot(pantheon_chain, pantheon_grid, datasets_summary)
        make_wz_plot(summary, omegam_ref, reference["mean_omegal"])

    return summary


def make_w0wa_plot(
    pantheon_chain: ChainData,
    pantheon_grid: tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]],
    datasets_summary: dict[str, dict[str, float | dict[str, float | bool] | str]],
) -> None:
    density, xcenters, ycenters, levels = pantheon_grid
    X, Y = np.meshgrid(xcenters, ycenters, indexing="ij")

    fig, ax = plt.subplots(figsize=(9.5, 7.0))
    ax.contourf(
        X,
        Y,
        density,
        levels=[levels["95"], density.max()],
        colors=["#f7d6db"],
        alpha=0.8,
    )
    ax.contourf(
        X,
        Y,
        density,
        levels=[levels["68"], density.max()],
        colors=["#f08b98"],
        alpha=0.85,
    )
    ax.contour(
        X,
        Y,
        density,
        levels=[levels["95"], levels["68"]],
        colors=["#a11d33", "#7a0019"],
        linewidths=[1.1, 1.4],
    )

    omegam = weighted_mean(pantheon_chain.omegam, pantheon_chain.weights)
    omegal = weighted_mean(pantheon_chain.omegal, pantheon_chain.weights)
    alpha_curve = np.linspace(-2.0, 1.2, 4000)
    curve_points = np.array(
        [model_w0_wa(alpha, omegam, omegal) for alpha in alpha_curve]
    )
    valid = (
        (curve_points[:, 0] >= W0_RANGE[0])
        & (curve_points[:, 0] <= W0_RANGE[1])
        & (curve_points[:, 1] >= WA_RANGE[0])
        & (curve_points[:, 1] <= WA_RANGE[1])
    )
    ax.plot(
        curve_points[valid, 0],
        curve_points[valid, 1],
        color="#111111",
        lw=2.0,
        label="Shielding model curve",
    )
    ax.scatter([-1.0], [0.0], color="#111111", s=55, marker="x", zorder=5, label="LambdaCDM")

    for name, info in DATASETS.items():
        point = datasets_summary[name]
        ax.scatter(
            [point["mean_w0"]],
            [point["mean_wa"]],
            s=60,
            color=info["color"],
            edgecolors="white",
            linewidths=0.7,
            zorder=6,
            label=info["label"],
        )

    ax.set_xlim(W0_RANGE)
    ax.set_ylim(WA_RANGE)
    ax.set_xlabel(r"$w_0$")
    ax.set_ylabel(r"$w_a$")
    ax.set_title("DESI DR2 posterior geometry vs. the one-parameter shielding curve")
    ax.legend(loc="upper left", fontsize=9, frameon=False, ncol=2)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(PLOT_ROOT / "w0_wa_shielding_vs_desi.png", dpi=180)
    plt.close(fig)


def make_wz_plot(summary: dict[str, object], omegam: float, omegal: float) -> None:
    predictions = summary["predictions"]
    z_grid = np.array(predictions["z_grid"])

    fig, ax = plt.subplots(figsize=(9.5, 6.3))
    ax.plot(
        z_grid,
        predictions["pantheonplus_mean_cpl"],
        color="#d1495b",
        lw=2.3,
        label="DESI+Pantheon+ CPL mean",
    )
    ax.plot(
        z_grid,
        predictions["pantheonplus_mean_shielding"],
        color="#264653",
        lw=2.3,
        label="Shielding model matched to mean w0 only",
    )
    ax.plot(
        z_grid,
        predictions["best_curve_shielding"],
        color="#2a9d8f",
        lw=2.0,
        label="Best point on shielding curve",
    )
    ax.plot(
        z_grid,
        predictions["lcdm"],
        color="#111111",
        lw=1.7,
        ls="--",
        label="LambdaCDM",
    )
    ax.axvline(2.0, color="#555555", lw=1.0, ls=":")
    ax.text(2.04, -1.87, "DESI leverage weakens beyond z=2", fontsize=9, color="#555555")
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(-2.0, 0.1)
    ax.set_xlabel("z")
    ax.set_ylabel(r"$w(z)$")
    ax.set_title("High-z prediction: the shielding ansatz bends the wrong way")
    ax.grid(alpha=0.15)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(PLOT_ROOT / "wz_prediction_comparison.png", dpi=180)
    plt.close(fig)


def write_report(summary: dict[str, object]) -> None:
    datasets = summary["datasets"]
    bao = summary["bao_anchor_test"]
    pantheon = datasets["pantheonplus"]
    desy5 = datasets["desy5sn"]
    union3 = datasets["union3"]
    cmb = datasets["cmb"]

    report = f"""# Cosmic shielding vs. DESI DR2

## Setup

I tested the simplest version of the hypothesis,

\\[
\\rho_{{\\rm DE,eff}}(z) = \\rho_{{\\Lambda, bare}} - \\alpha \\, \\rho_{{m,0}} (1+z)^3,
\\]

against the public DESI DR2 `base_w_wa` Cobaya chains and the public DESI DR2 compressed BAO points.

Weighted summaries from the official DESI public chains are:

- DESI + CMB: `w0 = {cmb["mean_w0"]:.3f} +- {cmb["std_w0"]:.3f}`, `wa = {cmb["mean_wa"]:.3f} +- {cmb["std_wa"]:.3f}`
- DESI + CMB + Pantheon+: `w0 = {pantheon["mean_w0"]:.3f} +- {pantheon["std_w0"]:.3f}`, `wa = {pantheon["mean_wa"]:.3f} +- {pantheon["std_wa"]:.3f}`
- DESI + CMB + DES Y5 SN: `w0 = {desy5["mean_w0"]:.3f} +- {desy5["std_w0"]:.3f}`, `wa = {desy5["mean_wa"]:.3f} +- {desy5["std_wa"]:.3f}`
- DESI + CMB + Union3: `w0 = {union3["mean_w0"]:.3f} +- {union3["std_w0"]:.3f}`, `wa = {union3["mean_wa"]:.3f} +- {union3["std_wa"]:.3f}`

## Exact prediction of the one-parameter model

Define

\\[
q \\equiv \\alpha \\frac{{\\Omega_{{m,0}}}}{{\\Omega_{{\\rm DE,0}}}}.
\\]

Then

\\[
w_{{\\rm eff}}(z) = -1 - \\frac{{q(1+z)^3}}{{1 + q - q(1+z)^3}}.
\\]

Expanding around today and matching to CPL,

\\[
w_0 = -1 - q,
\\qquad
w_a = -3 q (1+q) = -3 w_0 (1+w_0).
\\]

So the model does **not** fill the `w0-wa` plane. It is a single fixed curve:

- if `w0 > -1`, it predicts `wa > 0`
- if `w0 < -1`, it predicts `wa < 0`

DESI DR2 prefers `w0 > -1` and `wa < 0` in every main combined fit above, so the sign pattern is already wrong.

## Posterior test

I built smoothed posterior-density maps from the public chains and evaluated the maximum posterior density reachable anywhere along the shielding curve.

- DESI + CMB: best curve point `alpha = {cmb["curve_fit"]["best_alpha"]:.3f}`, `w0 = {cmb["curve_fit"]["best_w0"]:.3f}`, `wa = {cmb["curve_fit"]["best_wa"]:.3f}`, inside 95% HPD = `{cmb["curve_fit"]["inside_95_hpd"]}`
- DESI + CMB + Pantheon+: best curve point `alpha = {pantheon["curve_fit"]["best_alpha"]:.3f}`, `w0 = {pantheon["curve_fit"]["best_w0"]:.3f}`, `wa = {pantheon["curve_fit"]["best_wa"]:.3f}`, inside 95% HPD = `{pantheon["curve_fit"]["inside_95_hpd"]}`
- DESI + CMB + DES Y5 SN: best curve point `alpha = {desy5["curve_fit"]["best_alpha"]:.3f}`, `w0 = {desy5["curve_fit"]["best_w0"]:.3f}`, `wa = {desy5["curve_fit"]["best_wa"]:.3f}`, inside 95% HPD = `{desy5["curve_fit"]["inside_95_hpd"]}`
- DESI + CMB + Union3: best curve point `alpha = {union3["curve_fit"]["best_alpha"]:.3f}`, `w0 = {union3["curve_fit"]["best_w0"]:.3f}`, `wa = {union3["curve_fit"]["best_wa"]:.3f}`, inside 95% HPD = `{union3["curve_fit"]["inside_95_hpd"]}`

For the Pantheon+ combination, the DESI mean values imply `alpha = {pantheon["alpha_from_mean_w0"]:.3f}` if you force the model to reproduce `w0` alone. But that same alpha predicts `wa = {-3.0 * (pantheon["mean_w0"]) * (1.0 + pantheon["mean_w0"]):.3f}`, which has the wrong sign relative to the actual posterior mean `wa = {pantheon["mean_wa"]:.3f}`.

## Why the model is structurally too simple

Putting the ansatz into Friedmann gives

\\[
\\frac{{H^2(z)}}{{H_0^2}} =
\\Omega_r (1+z)^4 + (1-\\alpha) \\Omega_m (1+z)^3 + \\Omega_{{\\Lambda, bare}}.
\\]

So at the background level, the model is exactly equivalent to `LambdaCDM` with a rescaled matter term. It is not a genuinely new late-time evolution law.

That means any alpha large enough to create an apparent shift away from `w = -1` also forces a large shift in the matter contribution:

- Pantheon+ mean `w0` alone requires `alpha = {pantheon["alpha_from_mean_w0"]:.3f}`, which implies `Omega_m,eff = {pantheon["omega_m_eff_if_matched_to_mean_w0"]:.3f}` instead of the chain mean `Omega_m = {pantheon["mean_omegam"]:.3f}`
- DES Y5 mean `w0` alone requires `alpha = {desy5["alpha_from_mean_w0"]:.3f}`, giving `Omega_m,eff = {desy5["omega_m_eff_if_matched_to_mean_w0"]:.3f}`
- Union3 mean `w0` alone requires `alpha = {union3["alpha_from_mean_w0"]:.3f}`, giving `Omega_m,eff = {union3["omega_m_eff_if_matched_to_mean_w0"]:.3f}`

These are huge shifts, not subtle perturbations.

## BAO multi-redshift check

Using the public DESI DR2 compressed BAO points and fixing the non-alpha background parameters to the Pantheon+ chain weighted means, the one-parameter BAO scan gives:

- best BAO anchor-test fit at `alpha = {bao["best_alpha"]:.3f}`
- `chi2(alpha=0) = {bao["chi2_alpha_0"]:.2f}`
- `chi2_min = {bao["chi2_min"]:.2f}`
- approximate 95% interval in this anchored one-parameter test: `[{bao["alpha_95_interval"][0]:.3f}, {bao["alpha_95_interval"][1]:.3f}]`
- `chi2(alpha from Pantheon+ mean w0) = {bao["chi2_alpha_from_pantheonplus_mean_w0"]:.2f}`
- `chi2(alpha from DES Y5 mean w0) = {bao["chi2_alpha_from_desy5sn_mean_w0"]:.2f}`
- `chi2(alpha from Union3 mean w0) = {bao["chi2_alpha_from_union3_mean_w0"]:.2f}`

So the alpha values needed to mimic the DESI `w0 > -1` trend by themselves are catastrophic for the actual BAO distances.

## High-z prediction

If you nonetheless force the model to match the Pantheon+ mean `w0`, the shielding prediction bends toward matter-like behavior:

- `alpha = {pantheon["alpha_from_mean_w0"]:.3f}`
- `w_shield(z=2) = {w_eff(np.array([2.0]), pantheon["alpha_from_mean_w0"], pantheon["mean_omegam"], pantheon["mean_omegal"])[0]:.3f}`
- `w_CPL(z=2) = {cpl_w(np.array([2.0]), pantheon["mean_w0"], pantheon["mean_wa"])[0]:.3f}`
- `w_shield(z=4) = {w_eff(np.array([4.0]), pantheon["alpha_from_mean_w0"], pantheon["mean_omegam"], pantheon["mean_omegal"])[0]:.3f}`

That is the opposite of DESI's preferred CPL trend, which becomes more negative at higher redshift.

## Verdict

The constant-alpha linear shielding model is **garbage as an explanation of the DESI DR2 signal**.

- It predicts the wrong `w0-wa` sign correlation.
- In background evolution, it collapses to `LambdaCDM` with a rescaled matter term.
- The alpha needed to move `w0` appreciably away from `-1` implies a very large effective matter shift and fails the BAO check.
- The high-redshift prediction goes toward `w(z) -> 0` for the `w0 > -1` branch, not toward the DESI-preferred behavior.

What this means physically: if there is a viable "matter shielding" idea here, it cannot be this linear `rho_Lambda - alpha rho_m` model with constant alpha. You would need at least one extra ingredient that changes sign or geometry with time, such as a non-linear dependence on density, an explicit structure-formation variable, or a redshift-dependent coupling.
"""
    REPORT_PATH.write_text(report)


def main() -> None:
    summary = build_summary()
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2))
    write_report(summary)


if __name__ == "__main__":
    main()
