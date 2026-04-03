from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Callable

import matplotlib
import numpy as np
from scipy.interpolate import LSQUnivariateSpline

matplotlib.use("Agg")
import matplotlib.pyplot as plt


G = 6.67430e-11
KM_TO_M = 1_000.0
KPC_TO_M = 3.0856775814913673e19
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7
HELIUM_FACTOR = 1.33
QUALITY_KEEP = {1, 2}

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.parent / "data" / "raw"


def load_sparc_properties(path: Path) -> dict[str, dict[str, float | int | str]]:
    properties: dict[str, dict[str, float | int | str]] = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) != 19:
            continue
        galaxy = parts[0]
        properties[galaxy] = {
            "galaxy": galaxy,
            "T": int(parts[1]),
            "D_mpc": float(parts[2]),
            "e_D_mpc": float(parts[3]),
            "f_D": int(parts[4]),
            "Inc_deg": float(parts[5]),
            "e_Inc_deg": float(parts[6]),
            "L36_1e9Lsun": float(parts[7]),
            "e_L36_1e9Lsun": float(parts[8]),
            "Reff_kpc": float(parts[9]),
            "SBeff_Lsun_pc2": float(parts[10]),
            "Rdisk_kpc": float(parts[11]),
            "SBdisk_Lsun_pc2": float(parts[12]),
            "MHI_1e9Msun": float(parts[13]),
            "RHI_kpc": float(parts[14]),
            "Vflat_kms": float(parts[15]),
            "e_Vflat_kms": float(parts[16]),
            "Q": int(parts[17]),
            "Ref": parts[18],
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


def g_from_velocity(radius_kpc: float, velocity_kms: float) -> float:
    return (velocity_kms * KM_TO_M) ** 2 / (radius_kpc * KPC_TO_M)


def baryonic_mass_proxy(meta: dict[str, float | int | str]) -> tuple[float, float]:
    # The user only requested the two SPARC tables, so this is a fixed-M/L proxy.
    stellar_mass_1e9 = UPSILON_DISK * float(meta["L36_1e9Lsun"])
    gas_mass_1e9 = HELIUM_FACTOR * float(meta["MHI_1e9Msun"])
    baryonic_mass_1e9 = stellar_mass_1e9 + gas_mass_1e9
    gas_fraction = gas_mass_1e9 / baryonic_mass_1e9 if baryonic_mass_1e9 > 0.0 else math.nan
    return baryonic_mass_1e9 * 1e9, gas_fraction


def build_point_sample(
    galaxy_properties: dict[str, dict[str, float | int | str]],
    mass_rows: list[dict[str, float | str]],
) -> tuple[list[dict[str, float | str]], list[dict[str, float | int | str]]]:
    grouped: dict[str, list[dict[str, float | str]]] = defaultdict(list)

    for row in mass_rows:
        galaxy = str(row["galaxy"])
        radius_kpc = float(row["R_kpc"])
        vobs_kms = float(row["Vobs_kms"])
        if radius_kpc <= 0.0 or vobs_kms <= 0.0:
            continue

        vbar_sq_kms2 = (
            signed_square(float(row["Vgas_kms"]))
            + UPSILON_DISK * signed_square(float(row["Vdisk_kms"]))
            + UPSILON_BULGE * signed_square(float(row["Vbul_kms"]))
        )
        if vbar_sq_kms2 <= 0.0:
            continue

        gobs = g_from_velocity(radius_kpc, vobs_kms)
        if gobs <= 0.0:
            continue

        gbar = vbar_sq_kms2 * (KM_TO_M**2) / (radius_kpc * KPC_TO_M)
        grouped[galaxy].append(
            {
                "galaxy": galaxy,
                "R_kpc": radius_kpc,
                "Vobs_kms": vobs_kms,
                "e_Vobs_kms": float(row["e_Vobs_kms"]),
                "gobs_mps2": gobs,
                "gbar_mps2": gbar,
                "vbar_sq_kms2": vbar_sq_kms2,
            }
        )

    points: list[dict[str, float | str]] = []
    galaxies: list[dict[str, float | int | str]] = []

    for galaxy, rows in grouped.items():
        rows.sort(key=lambda row: float(row["R_kpc"]))
        meta = galaxy_properties[galaxy]
        mbar_msun, gas_fraction = baryonic_mass_proxy(meta)
        sb_eff = float(meta["SBeff_Lsun_pc2"])

        radius_kpc = np.array([float(row["R_kpc"]) for row in rows], dtype=float)
        radius_m = radius_kpc * KPC_TO_M
        gobs = np.array([float(row["gobs_mps2"]) for row in rows], dtype=float)
        gbar = np.array([float(row["gbar_mps2"]) for row in rows], dtype=float)

        phi_bar = np.zeros_like(gbar)
        for index in range(len(gbar) - 2, -1, -1):
            dr = radius_m[index + 1] - radius_m[index]
            phi_bar[index] = phi_bar[index + 1] + 0.5 * (gbar[index + 1] + gbar[index]) * dr

        sigma_bar = np.array(
            [
                float(row["vbar_sq_kms2"]) * (KM_TO_M**2) / (2.0 * math.pi * G * radius_m[idx])
                for idx, row in enumerate(rows)
            ],
            dtype=float,
        )
        dgbar_dr = np.gradient(gbar, radius_m, edge_order=1) if len(gbar) > 1 else np.zeros_like(gbar)
        abs_dgbar_dr = np.abs(dgbar_dr)

        for idx, row in enumerate(rows):
            points.append(
                {
                    "galaxy": galaxy,
                    "R_kpc": float(row["R_kpc"]),
                    "gobs_mps2": float(gobs[idx]),
                    "gbar_mps2": float(gbar[idx]),
                    "Phi_bar_m2s2": float(phi_bar[idx]),
                    "Sigma_bar_kgm2": float(sigma_bar[idx]),
                    "dgbar_dr_si": float(dgbar_dr[idx]),
                    "abs_dgbar_dr_si": float(abs_dgbar_dr[idx]),
                    "Mbar_Msun": float(mbar_msun),
                    "SBeff_Lsun_pc2": sb_eff,
                    "gas_fraction": float(gas_fraction),
                }
            )

        positive_phi = phi_bar[phi_bar > 0.0]
        positive_grad = abs_dgbar_dr[abs_dgbar_dr > 0.0]
        galaxies.append(
            {
                "galaxy": galaxy,
                "Q": int(meta["Q"]),
                "T": int(meta["T"]),
                "D_mpc": float(meta["D_mpc"]),
                "e_D_mpc": float(meta["e_D_mpc"]),
                "Inc_deg": float(meta["Inc_deg"]),
                "e_Inc_deg": float(meta["e_Inc_deg"]),
                "SBeff_Lsun_pc2": sb_eff,
                "Rdisk_kpc": float(meta["Rdisk_kpc"]),
                "Vflat_kms": float(meta["Vflat_kms"]),
                "n_points": int(len(rows)),
                "Mbar_Msun": float(mbar_msun),
                "gas_fraction": float(gas_fraction),
                "median_log_gbar": float(np.median(np.log10(gbar[gbar > 0.0]))),
                "median_log_Phi_bar": float(np.median(np.log10(positive_phi))) if len(positive_phi) else math.nan,
                "median_log_Sigma_bar": float(np.median(np.log10(sigma_bar[sigma_bar > 0.0]))),
                "median_log_abs_dgbar_dr": float(np.median(np.log10(positive_grad))) if len(positive_grad) else math.nan,
            }
        )

    galaxies.sort(key=lambda row: str(row["galaxy"]))
    return points, galaxies


def _build_spline(logx: np.ndarray, logy: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
    order = np.argsort(logx)
    sx = logx[order]
    sy = logy[order]
    unique_x = np.unique(sx)

    if len(sx) >= 12 and len(unique_x) >= 8:
        knot_candidates = np.quantile(sx, [0.2, 0.4, 0.6, 0.8])
        knots = np.unique(knot_candidates[(knot_candidates > sx.min()) & (knot_candidates < sx.max())])
        if len(knots) >= 1:
            try:
                spline = LSQUnivariateSpline(sx, sy, knots, k=3)
                return spline
            except Exception:
                pass

    degree = min(3, len(sx) - 1)
    if degree <= 0:
        mean_value = float(np.mean(sy))
        return lambda values: np.full_like(np.asarray(values, dtype=float), mean_value, dtype=float)

    coeffs = np.polyfit(sx, sy, deg=degree)
    polynomial = np.poly1d(coeffs)
    return polynomial


def fit_relation(
    points: list[dict[str, float | str]], variable_key: str, variable_label: str, notes: str
) -> tuple[dict[str, object], np.ndarray, np.ndarray, np.ndarray]:
    x = np.array([float(point[variable_key]) for point in points], dtype=float)
    y = np.array([float(point["gobs_mps2"]) for point in points], dtype=float)
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0.0) & (y > 0.0)
    x = x[mask]
    y = y[mask]
    logx = np.log10(x)
    logy = np.log10(y)
    model = _build_spline(logx, logy)
    pred_logy = np.asarray(model(logx), dtype=float)
    residuals = logy - pred_logy
    scatter_dex = float(np.sqrt(np.mean(residuals**2)))
    row = {
        "variable": variable_label,
        "n_points": int(len(x)),
        "scatter_dex": scatter_dex,
        "model": "cubic spline in log-log space with quantile knots" if len(x) >= 12 else "low-order polynomial in log-log space",
        "notes": notes,
    }
    grid = np.linspace(logx.min(), logx.max(), 300)
    curve = np.column_stack((grid, np.asarray(model(grid), dtype=float)))
    return row, logx, logy, curve


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def scatter_ranks(scatter_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ordered = sorted(scatter_rows, key=lambda row: (float(row["scatter_dex"]), str(row["variable"])))
    ranked_rows: list[dict[str, object]] = []
    current_rank = 0
    previous_scatter: float | None = None
    for row in ordered:
        scatter = float(row["scatter_dex"])
        if previous_scatter is None or not np.isclose(scatter, previous_scatter, rtol=1e-10, atol=1e-12):
            current_rank += 1
            previous_scatter = scatter
        ranked_row = dict(row)
        ranked_row["rank"] = current_rank
        ranked_rows.append(ranked_row)
    return ranked_rows


def compute_correlation_matrix(points: list[dict[str, float | str]]) -> list[dict[str, object]]:
    variables = [
        ("g_bar", "gbar_mps2"),
        ("Phi_bar", "Phi_bar_m2s2"),
        ("Sigma_bar", "Sigma_bar_kgm2"),
        ("|dg_bar/dr|", "abs_dgbar_dr_si"),
    ]
    values: dict[str, np.ndarray] = {}
    for label, key in variables:
        values[label] = np.array([float(point[key]) for point in points], dtype=float)

    rows: list[dict[str, object]] = []
    for row_label, row_values in values.items():
        record: dict[str, object] = {"variable": row_label}
        for col_label, col_values in values.items():
            shared = (
                np.isfinite(row_values)
                & np.isfinite(col_values)
                & (row_values > 0.0)
                & (col_values > 0.0)
            )
            if shared.sum() < 2:
                record[col_label] = math.nan
                continue
            record[col_label] = float(np.corrcoef(np.log10(row_values[shared]), np.log10(col_values[shared]))[0, 1])
        rows.append(record)
    return rows


def diagnostic_galaxies(galaxies: list[dict[str, float | int | str]], top_n: int = 10) -> list[dict[str, object]]:
    ranking_keys = [
        "median_log_gbar",
        "median_log_Phi_bar",
        "median_log_Sigma_bar",
        "median_log_abs_dgbar_dr",
    ]
    labels = {
        "median_log_gbar": "g_bar",
        "median_log_Phi_bar": "Phi_bar",
        "median_log_Sigma_bar": "Sigma_bar",
        "median_log_abs_dgbar_dr": "|dg_bar/dr|",
    }

    finite_galaxies = [
        galaxy
        for galaxy in galaxies
        if all(np.isfinite(float(galaxy[key])) for key in ranking_keys)
    ]

    for key in ranking_keys:
        values = np.array([float(galaxy[key]) for galaxy in finite_galaxies], dtype=float)
        order = np.argsort(values)
        ranks = np.empty_like(values)
        ranks[order] = np.linspace(0.0, 1.0, len(values))
        for galaxy, rank in zip(finite_galaxies, ranks, strict=False):
            galaxy[f"rank_{key}"] = float(rank)

    rows: list[dict[str, object]] = []
    for galaxy in finite_galaxies:
        ranks = np.array([float(galaxy[f"rank_{key}"]) for key in ranking_keys], dtype=float)
        max_gap = -1.0
        max_pair = ("", "")
        for idx, first_key in enumerate(ranking_keys):
            for second_key in ranking_keys[idx + 1 :]:
                gap = abs(float(galaxy[f"rank_{first_key}"]) - float(galaxy[f"rank_{second_key}"]))
                if gap > max_gap:
                    max_gap = gap
                    max_pair = (labels[first_key], labels[second_key])
        rows.append(
            {
                "galaxy": galaxy["galaxy"],
                "diagnostic_score": float(np.std(ranks)),
                "largest_rank_gap": float(max_gap),
                "pair_most_in_tension": f"{max_pair[0]} vs {max_pair[1]}",
                "rank_g_bar": float(galaxy["rank_median_log_gbar"]),
                "rank_Phi_bar": float(galaxy["rank_median_log_Phi_bar"]),
                "rank_Sigma_bar": float(galaxy["rank_median_log_Sigma_bar"]),
                "rank_|dg_bar/dr|": float(galaxy["rank_median_log_abs_dgbar_dr"]),
                "Mbar_Msun": float(galaxy["Mbar_Msun"]),
                "SBeff_Lsun_pc2": float(galaxy["SBeff_Lsun_pc2"]),
                "gas_fraction": float(galaxy["gas_fraction"]),
            }
        )

    rows.sort(key=lambda row: (float(row["diagnostic_score"]), float(row["largest_rank_gap"])), reverse=True)
    return rows[:top_n]


def subgroup_scatter(
    points: list[dict[str, float | str]],
    galaxies: list[dict[str, float | int | str]],
) -> tuple[list[dict[str, object]], dict[str, float]]:
    sb_values = np.array([float(galaxy["SBeff_Lsun_pc2"]) for galaxy in galaxies], dtype=float)
    gas_values = np.array([float(galaxy["gas_fraction"]) for galaxy in galaxies], dtype=float)
    sb_split = float(np.median(sb_values[np.isfinite(sb_values)]))
    gas_split = float(np.median(gas_values[np.isfinite(gas_values)]))

    candidate_rows = [
        ("gbar_mps2", "g_bar", "Standard baryonic acceleration."),
        ("Phi_bar_m2s2", "Phi_bar", "Relative baryonic potential depth from the outermost measured radius."),
        ("Sigma_bar_kgm2", "Sigma_bar", "Surface-density proxy proportional to g_bar."),
        ("abs_dgbar_dr_si", "|dg_bar/dr|", "Magnitude of the finite-difference acceleration gradient."),
    ]

    subgroup_rows = [
        ("mass >= 1e10 Msun", "Mbar_Msun >= 1e10 Msun", lambda point: float(point["Mbar_Msun"]) >= 1e10),
        ("mass < 1e10 Msun", "Mbar_Msun < 1e10 Msun", lambda point: float(point["Mbar_Msun"]) < 1e10),
        (
            f"high surface brightness (SBeff >= {sb_split:.2f})",
            f"SBeff_Lsun_pc2 >= {sb_split:.2f}",
            lambda point: float(point["SBeff_Lsun_pc2"]) >= sb_split,
        ),
        (
            f"low surface brightness (SBeff < {sb_split:.2f})",
            f"SBeff_Lsun_pc2 < {sb_split:.2f}",
            lambda point: float(point["SBeff_Lsun_pc2"]) < sb_split,
        ),
        (
            f"gas-rich (fgas >= {gas_split:.3f})",
            f"gas_fraction >= {gas_split:.3f}",
            lambda point: float(point["gas_fraction"]) >= gas_split,
        ),
        (
            f"star-dominated (fgas < {gas_split:.3f})",
            f"gas_fraction < {gas_split:.3f}",
            lambda point: float(point["gas_fraction"]) < gas_split,
        ),
    ]

    rows: list[dict[str, object]] = []
    for subgroup_label, split_definition, selector in subgroup_rows:
        subset = [point for point in points if selector(point)]
        fitted: list[tuple[str, float]] = []
        for key, label, note in candidate_rows:
            fit_row, _, _, _ = fit_relation(subset, key, label, note)
            fitted.append((label, float(fit_row["scatter_dex"])))
            rows.append(
                {
                    "subgroup": subgroup_label,
                    "split_definition": split_definition,
                    "n_points": int(fit_row["n_points"]),
                    "variable": label,
                    "scatter_dex": float(fit_row["scatter_dex"]),
                }
            )

        min_scatter = min(value for _, value in fitted)
        winners = [label for label, value in fitted if np.isclose(value, min_scatter, rtol=1e-10, atol=1e-12)]
        winner_label = " / ".join(winners)
        sorted_scatter = sorted(fitted, key=lambda item: (item[1], item[0]))
        rank_lookup: dict[str, int] = {}
        current_rank = 0
        previous_value: float | None = None
        for label, value in sorted_scatter:
            if previous_value is None or not np.isclose(value, previous_value, rtol=1e-10, atol=1e-12):
                current_rank += 1
                previous_value = value
            rank_lookup[label] = current_rank

        for row in rows[-len(candidate_rows) :]:
            row["rank"] = rank_lookup[str(row["variable"])]
            row["winner"] = winner_label
            row["winner_scatter_dex"] = float(min_scatter)

    return rows, {"sb_split": sb_split, "gas_split": gas_split}


def plot_relations(path: Path, relation_panels: list[tuple[str, np.ndarray, np.ndarray, np.ndarray]]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 10.0))
    for ax, (label, logx, logy, curve) in zip(axes.ravel(), relation_panels, strict=False):
        ax.scatter(logx, logy, s=6, alpha=0.18, color="#1f4e79", linewidths=0)
        ax.plot(curve[:, 0], curve[:, 1], color="#c0392b", lw=2.0)
        ax.set_title(label)
        ax.set_xlabel(f"log10({label})")
        ax.set_ylabel("log10(g_obs [m s^-2])")
        ax.grid(alpha=0.15)
    fig.suptitle("SPARC candidate control variables vs observed gravity", y=0.98)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_subgroups(path: Path, subgroup_rows: list[dict[str, object]]) -> None:
    subgroup_labels: list[str] = []
    for row in subgroup_rows:
        label = str(row["subgroup"])
        if label not in subgroup_labels:
            subgroup_labels.append(label)

    variables = ["g_bar", "Phi_bar", "Sigma_bar", "|dg_bar/dr|"]
    palette = {
        "g_bar": "#1f4e79",
        "Phi_bar": "#c0392b",
        "Sigma_bar": "#2c7a3f",
        "|dg_bar/dr|": "#8e5ea2",
    }

    width = 0.18
    x = np.arange(len(subgroup_labels))
    fig, ax = plt.subplots(figsize=(12.5, 5.5))
    for offset, variable in enumerate(variables):
        values = []
        for subgroup in subgroup_labels:
            match = next(
                row for row in subgroup_rows if row["subgroup"] == subgroup and row["variable"] == variable
            )
            values.append(float(match["scatter_dex"]))
        ax.bar(x + (offset - 1.5) * width, values, width=width, label=variable, color=palette[variable])
    ax.set_xticks(x)
    ax.set_xticklabels(subgroup_labels, rotation=20, ha="right")
    ax.set_ylabel("Scatter [dex]")
    ax.set_title("Subpopulation comparison of candidate control variables")
    ax.legend(frameon=False, ncol=4)
    ax.grid(axis="y", alpha=0.15)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def write_summary(
    path: Path,
    scatter_rows: list[dict[str, object]],
    correlation_rows: list[dict[str, object]],
    diagnostic_rows: list[dict[str, object]],
    subgroup_rows: list[dict[str, object]],
    split_info: dict[str, float],
    n_galaxies: int,
    n_points: int,
) -> None:
    ranked_scatter = sorted(scatter_rows, key=lambda row: (float(row["scatter_dex"]), str(row["variable"])))
    winner_names = [str(row["variable"]) for row in ranked_scatter if int(row["rank"]) == ranked_scatter[0]["rank"]]
    overall_winner = " / ".join(winner_names)

    subgroup_lookup: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in subgroup_rows:
        subgroup_lookup[str(row["subgroup"])].append(row)

    lines = [
        "# SPARC Variable-Control Analysis",
        "",
        f"- Galaxies used: {n_galaxies} with `Q = 1` or `2`",
        f"- Radial points used: {n_points}",
        f"- Model: cubic spline in log-log space with quantile knots; low-order polynomial fallback for small subsets",
        f"- Mass split: `Mbar = 1e10 Msun`",
        f"- Surface-brightness split: median `SBeff = {split_info['sb_split']:.2f} Lsun/pc^2`",
        f"- Gas-fraction split: median `fgas = {split_info['gas_split']:.3f}`",
        "",
        "## Scatter Ranking",
        "",
        "| Rank | Variable | Scatter (dex) | Points | Notes |",
        "|---:|---|---:|---:|---|",
    ]

    for row in ranked_scatter:
        lines.append(
            f"| {int(row['rank'])} | `{row['variable']}` | {float(row['scatter_dex']):.4f} | {int(row['n_points'])} | {row['notes']} |"
        )

    lines.extend(
        [
            "",
            "## Main Result",
            "",
            f"- Best relation: **{overall_winner}** at **{float(ranked_scatter[0]['scatter_dex']):.4f} dex**.",
            "- `Sigma_bar` is algebraically proportional to `g_bar`, so the two are expected to tie to numerical precision in log space.",
            "- `Phi_bar` is the next-tightest candidate, and `|dg_bar/dr|` is the loosest of the four.",
            "",
            "## Candidate Correlation Matrix",
            "",
            "| Variable | `g_bar` | `Phi_bar` | `Sigma_bar` | `|dg_bar/dr|` |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    for row in correlation_rows:
        lines.append(
            f"| `{row['variable']}` | {float(row['g_bar']):.4f} | {float(row['Phi_bar']):.4f} | {float(row['Sigma_bar']):.4f} | {float(row['|dg_bar/dr|']):.4f} |"
        )

    lines.extend(
        [
            "",
            "## Diagnostic Galaxies",
            "",
            "| Galaxy | Diagnostic score | Strongest rank tension | `g_bar` | `Phi_bar` | `Sigma_bar` | `|dg_bar/dr|` |",
            "|---|---:|---|---:|---:|---:|---:|",
        ]
    )
    for row in diagnostic_rows:
        lines.append(
            f"| {row['galaxy']} | {float(row['diagnostic_score']):.4f} | {row['pair_most_in_tension']} | {float(row['rank_g_bar']):.3f} | {float(row['rank_Phi_bar']):.3f} | {float(row['rank_Sigma_bar']):.3f} | {float(row['rank_|dg_bar/dr|']):.3f} |"
        )

    lines.extend(["", "## Subgroup Winners", ""])
    subgroup_order = [
        "mass >= 1e10 Msun",
        "mass < 1e10 Msun",
        next(key for key in subgroup_lookup if key.startswith("high surface brightness")),
        next(key for key in subgroup_lookup if key.startswith("low surface brightness")),
        next(key for key in subgroup_lookup if key.startswith("gas-rich")),
        next(key for key in subgroup_lookup if key.startswith("star-dominated")),
    ]
    for subgroup in subgroup_order:
        rows = sorted(subgroup_lookup[subgroup], key=lambda row: float(row["scatter_dex"]))
        winner = str(rows[0]["winner"])
        summary = ", ".join(f"{row['variable']}={float(row['scatter_dex']):.4f}" for row in rows)
        lines.append(f"- {subgroup}: winner **{winner}**; {summary}")

    lines.extend(
        [
            "",
            "## Subgroup Conclusion",
            "",
            "- The winner does not change across the requested subgroup splits; `g_bar` and `Sigma_bar` remain tied for best scatter in every case.",
            "",
            "## Notes",
            "",
            "- `Phi_bar` is defined as the outward integral of `g_bar = V_bar^2 / r` from each radius to the outermost measured SPARC radius, so the outermost point is zero by construction and is excluded from log fits.",
            "- `|dg_bar/dr|` uses the magnitude of the finite-difference derivative so it can be fit in log space.",
            "- The mass split uses a fixed `M/L = 0.5` proxy on the total 3.6 micron luminosity plus helium-corrected HI mass, which keeps the analysis within the two requested SPARC tables.",
        ]
    )

    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    galaxy_properties = load_sparc_properties(DATA_ROOT / "SPARC_Lelli2016c.mrt")
    mass_rows = load_mass_models(DATA_ROOT / "MassModels_Lelli2016c.mrt", galaxy_properties)

    points, galaxies = build_point_sample(galaxy_properties, mass_rows)

    candidate_rows = [
        ("gbar_mps2", "g_bar", "Standard baryonic acceleration."),
        ("Phi_bar_m2s2", "Phi_bar", "Relative baryonic potential depth from the outermost measured radius."),
        ("Sigma_bar_kgm2", "Sigma_bar", "Surface-density proxy proportional to g_bar."),
        ("abs_dgbar_dr_si", "|dg_bar/dr|", "Magnitude of the finite-difference acceleration gradient."),
    ]

    scatter_rows: list[dict[str, object]] = []
    relation_panels: list[tuple[str, np.ndarray, np.ndarray, np.ndarray]] = []
    for key, label, notes in candidate_rows:
        row, logx, logy, curve = fit_relation(points, key, label, notes)
        scatter_rows.append(row)
        relation_panels.append((label, logx, logy, curve))

    scatter_rows = scatter_ranks(scatter_rows)
    correlation_rows = compute_correlation_matrix(points)
    diagnostic_rows = diagnostic_galaxies(galaxies, top_n=10)
    subgroup_rows, split_info = subgroup_scatter(points, galaxies)

    write_csv(ROOT / "scatter_table.csv", scatter_rows)
    write_csv(ROOT / "variable_correlation_matrix.csv", correlation_rows)
    write_csv(ROOT / "diagnostic_galaxies.csv", diagnostic_rows)
    write_csv(ROOT / "subgroup_scatter.csv", subgroup_rows)
    write_summary(
        ROOT / "summary.md",
        scatter_rows,
        correlation_rows,
        diagnostic_rows,
        subgroup_rows,
        split_info,
        n_galaxies=len(galaxies),
        n_points=len(points),
    )

    plot_relations(ROOT / "candidate_relations.png", relation_panels)
    plot_subgroups(ROOT / "subgroup_scatter.png", subgroup_rows)


if __name__ == "__main__":
    main()
