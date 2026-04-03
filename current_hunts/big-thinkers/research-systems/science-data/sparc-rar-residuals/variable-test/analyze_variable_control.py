from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib
import numpy as np
from scipy.interpolate import LSQUnivariateSpline

matplotlib.use("Agg")
import matplotlib.pyplot as plt


KM_TO_M = 1_000.0
KPC_TO_M = 3.0856775814913673e19
G = 6.67430e-11
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7
HELIUM_FACTOR = 1.33
QUALITY_KEEP = {1, 2}
SPLINE_QUANTILES = np.array([0.15, 0.30, 0.45, 0.60, 0.75, 0.90])

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.parent / "data" / "raw"
OUTPUT_ROOT = ROOT / "output"


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


def load_bulges(path: Path) -> dict[str, float]:
    bulges: dict[str, float] = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 2:
            continue
        bulges[parts[0]] = float(parts[1])
    return bulges


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


def baryonic_mass_1e9msun(
    galaxy_properties: dict[str, float | int | str], bulges: dict[str, float]
) -> tuple[float, float]:
    galaxy = str(galaxy_properties["galaxy"])
    bulge_luminosity = bulges.get(galaxy, 0.0)
    total_luminosity = float(galaxy_properties["L36_1e9Lsun"])
    disk_luminosity = max(total_luminosity - bulge_luminosity, 0.0)
    stellar_mass = UPSILON_DISK * disk_luminosity + UPSILON_BULGE * bulge_luminosity
    gas_mass = HELIUM_FACTOR * float(galaxy_properties["MHI_1e9Msun"])
    return stellar_mass + gas_mass, gas_mass


def build_dataset() -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    galaxy_properties = load_sparc_properties(DATA_ROOT / "SPARC_Lelli2016c.mrt")
    bulges = load_bulges(DATA_ROOT / "Bulges.mrt")
    mass_rows = load_mass_models(DATA_ROOT / "MassModels_Lelli2016c.mrt", galaxy_properties)

    grouped: dict[str, list[dict[str, float | str]]] = defaultdict(list)
    for row in mass_rows:
        galaxy = str(row["galaxy"])
        radius = float(row["R_kpc"])
        vobs = float(row["Vobs_kms"])
        if radius <= 0.0 or vobs <= 0.0:
            continue
        vbar_sq = (
            signed_square(float(row["Vgas_kms"]))
            + UPSILON_DISK * signed_square(float(row["Vdisk_kms"]))
            + UPSILON_BULGE * signed_square(float(row["Vbul_kms"]))
        )
        if vbar_sq <= 0.0:
            continue
        gobs = g_from_velocity(radius, vobs)
        if gobs <= 0.0:
            continue
        grouped[galaxy].append(
            {
                "R_kpc": radius,
                "gobs_mps2": gobs,
                "vbar_sq_kms2": vbar_sq,
            }
        )

    points: list[dict[str, float | str]] = []
    galaxies: list[dict[str, float | str]] = []
    for galaxy, rows in grouped.items():
        rows.sort(key=lambda row: float(row["R_kpc"]))
        meta = galaxy_properties[galaxy]
        mbar_1e9msun, gas_mass_1e9msun = baryonic_mass_1e9msun(meta, bulges)
        gas_fraction = gas_mass_1e9msun / mbar_1e9msun if mbar_1e9msun > 0.0 else math.nan

        radius_kpc = np.array([float(row["R_kpc"]) for row in rows], dtype=float)
        radius_m = radius_kpc * KPC_TO_M
        gobs = np.array([float(row["gobs_mps2"]) for row in rows], dtype=float)
        vbar_sq = np.array([float(row["vbar_sq_kms2"]) for row in rows], dtype=float)
        gbar = vbar_sq * (KM_TO_M**2) / radius_m

        phi_depth = np.zeros_like(gbar)
        for idx in range(len(gbar) - 2, -1, -1):
            dr = radius_m[idx + 1] - radius_m[idx]
            phi_depth[idx] = phi_depth[idx + 1] + 0.5 * (gbar[idx + 1] + gbar[idx]) * dr

        sigma_bar = vbar_sq * (KM_TO_M**2) / (2.0 * math.pi * G * radius_m)
        dgbar_dr = np.abs(np.gradient(gbar, radius_m, edge_order=1))

        for idx in range(len(radius_kpc)):
            points.append(
                {
                    "galaxy": galaxy,
                    "R_kpc": radius_kpc[idx],
                    "gobs_mps2": gobs[idx],
                    "gbar_mps2": gbar[idx],
                    "Phi_bar_m2s2": phi_depth[idx],
                    "Sigma_bar_kgm2": sigma_bar[idx],
                    "abs_dgbar_dr_si": dgbar_dr[idx],
                    "Mbar_1e9Msun": mbar_1e9msun,
                    "SBeff_Lsun_pc2": float(meta["SBeff_Lsun_pc2"]),
                    "gas_fraction": gas_fraction,
                }
            )

        positive_phi = phi_depth[phi_depth > 0.0]
        galaxies.append(
            {
                "galaxy": galaxy,
                "Mbar_1e9Msun": mbar_1e9msun,
                "SBeff_Lsun_pc2": float(meta["SBeff_Lsun_pc2"]),
                "gas_fraction": gas_fraction,
                "median_log_gbar": float(np.median(np.log10(gbar))),
                "median_log_Phi_bar": float(np.median(np.log10(positive_phi))) if len(positive_phi) else math.nan,
                "median_log_Sigma_bar": float(np.median(np.log10(sigma_bar))),
                "median_log_abs_dgbar_dr": float(np.median(np.log10(dgbar_dr[dgbar_dr > 0.0]))),
            }
        )

    galaxies.sort(key=lambda row: str(row["galaxy"]))
    return points, galaxies


def fit_log_spline(logx: np.ndarray, logy: np.ndarray) -> tuple[np.ndarray, callable]:
    order = np.argsort(logx)
    sx = logx[order]
    sy = logy[order]
    knot_candidates = np.quantile(sx, SPLINE_QUANTILES)
    knots = np.unique(knot_candidates[(knot_candidates > sx.min()) & (knot_candidates < sx.max())])
    if len(knots) >= 1:
        model = LSQUnivariateSpline(sx, sy, knots, k=3)
        return model(logx), model
    coeffs = np.polyfit(sx, sy, deg=3)
    return np.polyval(coeffs, logx), lambda values: np.polyval(coeffs, values)


def fit_relation(
    points: list[dict[str, float | str]], variable_key: str, label: str, notes: str
) -> tuple[dict[str, float | str], np.ndarray, np.ndarray, np.ndarray]:
    x = np.array([float(point[variable_key]) for point in points], dtype=float)
    y = np.array([float(point["gobs_mps2"]) for point in points], dtype=float)
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0.0) & (y > 0.0)
    x = x[mask]
    y = y[mask]
    logx = np.log10(x)
    logy = np.log10(y)
    pred_logy, model = fit_log_spline(logx, logy)
    residuals = logy - pred_logy
    row = {
        "variable": label,
        "n_points": int(mask.sum()),
        "scatter_dex": float(np.sqrt(np.mean(residuals**2))),
        "notes": notes,
    }
    grid = np.linspace(logx.min(), logx.max(), 300)
    return row, logx, logy, np.column_stack((grid, model(grid)))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def correlation_matrix(points: list[dict[str, float | str]]) -> list[dict[str, object]]:
    label_to_key = {
        "g_bar": "gbar_mps2",
        "Phi_bar": "Phi_bar_m2s2",
        "Sigma_bar": "Sigma_bar_kgm2",
        "|dg_bar/dr|": "abs_dgbar_dr_si",
    }
    logs: dict[str, np.ndarray] = {}
    for label, key in label_to_key.items():
        values = np.array([float(point[key]) for point in points], dtype=float)
        logged = np.full(values.shape, np.nan, dtype=float)
        positive = values > 0.0
        logged[positive] = np.log10(values[positive])
        logs[label] = logged

    rows: list[dict[str, object]] = []
    for row_label, row_values in logs.items():
        record: dict[str, object] = {"variable": row_label}
        for col_label, col_values in logs.items():
            mask = np.isfinite(row_values) & np.isfinite(col_values)
            record[col_label] = float(np.corrcoef(row_values[mask], col_values[mask])[0, 1])
        rows.append(record)
    return rows


def diagnostic_galaxies(galaxies: list[dict[str, float | str]], top_n: int = 10) -> list[dict[str, object]]:
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
    for key in ranking_keys:
        values = np.array([float(galaxy[key]) for galaxy in galaxies], dtype=float)
        order = np.argsort(values)
        ranks = np.empty_like(values)
        ranks[order] = np.linspace(0.0, 1.0, len(values))
        for galaxy, rank in zip(galaxies, ranks):
            galaxy[f"rank_{key}"] = float(rank)

    ranked_rows: list[dict[str, object]] = []
    for galaxy in galaxies:
        ranks = np.array([float(galaxy[f"rank_{key}"]) for key in ranking_keys], dtype=float)
        max_gap = -1.0
        max_pair = ("", "")
        for idx, first_key in enumerate(ranking_keys):
            for second_key in ranking_keys[idx + 1 :]:
                gap = abs(float(galaxy[f"rank_{first_key}"]) - float(galaxy[f"rank_{second_key}"]))
                if gap > max_gap:
                    max_gap = gap
                    max_pair = (labels[first_key], labels[second_key])
        ranked_rows.append(
            {
                "galaxy": galaxy["galaxy"],
                "diagnostic_score": float(np.std(ranks)),
                "largest_rank_gap": max_gap,
                "pair_most_in_tension": f"{max_pair[0]} vs {max_pair[1]}",
                "Mbar_1e9Msun": float(galaxy["Mbar_1e9Msun"]),
                "SBeff_Lsun_pc2": float(galaxy["SBeff_Lsun_pc2"]),
                "gas_fraction": float(galaxy["gas_fraction"]),
            }
        )
    ranked_rows.sort(key=lambda row: float(row["diagnostic_score"]), reverse=True)
    return ranked_rows[:top_n]


def subgroup_scatter(
    points: list[dict[str, float | str]],
    sb_split: float,
    gas_split: float,
) -> list[dict[str, object]]:
    subgroups = [
        ("mass >= 1e10 Msun", lambda point: float(point["Mbar_1e9Msun"]) >= 10.0),
        ("mass < 1e10 Msun", lambda point: float(point["Mbar_1e9Msun"]) < 10.0),
        ("high surface brightness", lambda point: float(point["SBeff_Lsun_pc2"]) >= sb_split),
        ("low surface brightness", lambda point: float(point["SBeff_Lsun_pc2"]) < sb_split),
        ("gas-rich", lambda point: float(point["gas_fraction"]) >= gas_split),
        ("star-dominated", lambda point: float(point["gas_fraction"]) < gas_split),
    ]
    candidates = [
        ("gbar_mps2", "g_bar", "Baseline."),
        ("Phi_bar_m2s2", "Phi_bar", "Potential depth relative to the outermost SPARC point."),
        ("Sigma_bar_kgm2", "Sigma_bar", "Approximate disk surface density."),
        ("abs_dgbar_dr_si", "|dg_bar/dr|", "Magnitude of the radial acceleration gradient."),
    ]

    rows: list[dict[str, object]] = []
    for subgroup_label, selector in subgroups:
        subset = [point for point in points if selector(point)]
        fits: list[tuple[str, float]] = []
        for key, label, note in candidates:
            fit_row, _, _, _ = fit_relation(subset, key, label, note)
            fits.append((label, float(fit_row["scatter_dex"])))
            rows.append(
                {
                    "subgroup": subgroup_label,
                    "variable": label,
                    "n_points": int(fit_row["n_points"]),
                    "scatter_dex": float(fit_row["scatter_dex"]),
                }
            )
        winner, winner_scatter = sorted(fits, key=lambda item: item[1])[0]
        for row in rows[-len(candidates) :]:
            row["winner_for_subgroup"] = winner
            row["winning_scatter_dex"] = winner_scatter
    return rows


def plot_relations(path: Path, relation_panels: list[tuple[str, np.ndarray, np.ndarray, np.ndarray]]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 10.0))
    for ax, (label, logx, logy, curve) in zip(axes.ravel(), relation_panels):
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
    subgroup_labels = []
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
    fig, ax = plt.subplots(figsize=(12.0, 5.5))
    for offset, variable in enumerate(variables):
        values = []
        for subgroup in subgroup_labels:
            match = next(row for row in subgroup_rows if row["subgroup"] == subgroup and row["variable"] == variable)
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
    sb_split: float,
    gas_split: float,
    n_galaxies: int,
    n_points: int,
) -> None:
    ranked_scatter = sorted(scatter_rows, key=lambda row: float(row["scatter_dex"]))
    lines = [
        "# Variable Test Summary",
        "",
        f"- Galaxies used: {n_galaxies} (Q = 1 or 2)",
        f"- Radial points used: {n_points}",
        f"- Surface-brightness split: median `SBeff = {sb_split:.2f} Lsun/pc^2`",
        f"- Gas-fraction split: median `fgas = {gas_split:.3f}`",
        "",
        "## Scatter ranking",
        "",
        "| Variable | Scatter (dex) | Notes |",
        "|---|---:|---|",
    ]
    for row in ranked_scatter:
        lines.append(
            f"| `{row['variable']}` | {float(row['scatter_dex']):.4f} | {row['notes']} |"
        )

    lines.extend(
        [
            "",
            "## Main takeaways",
            "",
            f"- `g_bar` is the tightest empirical variable in this SPARC implementation at {float(ranked_scatter[0]['scatter_dex']):.4f} dex.",
            "- `Sigma_bar` ties exactly with `g_bar` because the requested approximation `Sigma = V_bar^2 / (2 pi G r)` is algebraically proportional to `g_bar = V_bar^2 / r`.",
            "- `Phi_bar` is visibly looser, and `|dg_bar/dr|` is the loosest of the four.",
            "- Because `corr(g_bar, Sigma_bar) = 1.000`, SPARC cannot distinguish acceleration from this approximate surface-density proxy.",
            "",
            "## Correlation matrix",
            "",
            "| Variable | `g_bar` | `Phi_bar` | `Sigma_bar` | `|dg_bar/dr|` |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in correlation_rows:
        lines.append(
            f"| `{row['variable']}` | {float(row['g_bar']):.4f} | {float(row['Phi_bar']):.4f} | {float(row['Sigma_bar']):.4f} | {float(row['|dg_bar/dr|']):.4f} |"
        )

    lines.extend(["", "## Most diagnostic galaxies", "", "| Galaxy | Score | Main tension |", "|---|---:|---|"])
    for row in diagnostic_rows:
        lines.append(
            f"| {row['galaxy']} | {float(row['diagnostic_score']):.4f} | `{row['pair_most_in_tension']}` |"
        )

    subgroup_lookup: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in subgroup_rows:
        subgroup_lookup[str(row["subgroup"])].append(row)
    lines.extend(["", "## Subpopulation winners", ""])
    for subgroup, rows in subgroup_lookup.items():
        ranked = sorted(rows, key=lambda row: float(row["scatter_dex"]))
        summary = ", ".join(f"{row['variable']}={float(row['scatter_dex']):.4f}" for row in ranked)
        lines.append(f"- {subgroup}: {summary}")

    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- `Phi_bar` is a relative potential depth anchored to the outermost measured SPARC radius, so it is a practical proxy rather than an absolute potential.",
            "- `|dg_bar/dr|` uses the magnitude of the numerical gradient because a signed gradient mixes rising and falling parts of the curve and is not directly comparable in log space.",
            "- If surface density is computed from full photometric profiles instead of the requested approximation, the exact `g_bar`-`Sigma_bar` degeneracy could be broken.",
        ]
    )
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    points, galaxies = build_dataset()
    sb_split = float(np.median([float(galaxy["SBeff_Lsun_pc2"]) for galaxy in galaxies]))
    gas_split = float(np.median([float(galaxy["gas_fraction"]) for galaxy in galaxies]))

    candidate_rows = [
        ("gbar_mps2", "g_bar", "Baseline acceleration variable."),
        ("Phi_bar_m2s2", "Phi_bar", "Potential depth relative to the outermost SPARC point."),
        ("Sigma_bar_kgm2", "Sigma_bar", "Approximate disk surface density from V_bar^2 / (2 pi G r)."),
        ("abs_dgbar_dr_si", "|dg_bar/dr|", "Magnitude of the radial acceleration gradient."),
    ]

    scatter_rows: list[dict[str, object]] = []
    relation_panels: list[tuple[str, np.ndarray, np.ndarray, np.ndarray]] = []
    for key, label, notes in candidate_rows:
        row, logx, logy, curve = fit_relation(points, key, label, notes)
        scatter_rows.append(row)
        relation_panels.append((label, logx, logy, curve))

    correlation_rows = correlation_matrix(points)
    diagnostic_rows = diagnostic_galaxies(galaxies)
    subgroup_rows = subgroup_scatter(points, sb_split=sb_split, gas_split=gas_split)

    write_csv(OUTPUT_ROOT / "scatter_table.csv", scatter_rows)
    write_csv(OUTPUT_ROOT / "variable_correlation_matrix.csv", correlation_rows)
    write_csv(OUTPUT_ROOT / "diagnostic_galaxies.csv", diagnostic_rows)
    write_csv(OUTPUT_ROOT / "subpopulation_scatter.csv", subgroup_rows)
    plot_relations(OUTPUT_ROOT / "candidate_relations.png", relation_panels)
    plot_subgroups(OUTPUT_ROOT / "subpopulation_scatter.png", subgroup_rows)
    write_summary(
        OUTPUT_ROOT / "summary.md",
        scatter_rows=scatter_rows,
        correlation_rows=correlation_rows,
        diagnostic_rows=diagnostic_rows,
        subgroup_rows=subgroup_rows,
        sb_split=sb_split,
        gas_split=gas_split,
        n_galaxies=len(galaxies),
        n_points=len(points),
    )


if __name__ == "__main__":
    main()
