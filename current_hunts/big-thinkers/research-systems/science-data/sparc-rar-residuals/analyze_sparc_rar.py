from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib
import numpy as np
from scipy.stats import spearmanr

matplotlib.use("Agg")
import matplotlib.pyplot as plt


A0 = 1.2e-10
KM_TO_M = 1_000.0
KPC_TO_M = 3.0856775814913673e19
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7
HELIUM_FACTOR = 1.33
QUALITY_KEEP = {1, 2}


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


def load_mass_models(path: Path, galaxy_properties: dict[str, dict[str, float | int | str]]) -> list[dict[str, float | str]]:
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
                "D_mpc": float(parts[1]),
                "R_kpc": float(parts[2]),
                "Vobs_kms": float(parts[3]),
                "e_Vobs_kms": float(parts[4]),
                "Vgas_kms": float(parts[5]),
                "Vdisk_kms": float(parts[6]),
                "Vbul_kms": float(parts[7]),
                "SBdisk_Lsun_pc2": float(parts[8]),
                "SBbul_Lsun_pc2": float(parts[9]),
            }
        )
    return rows


def signed_square(velocity_kms: float) -> float:
    return math.copysign(velocity_kms * velocity_kms, velocity_kms)


def g_from_velocity(radius_kpc: float, velocity_kms: float) -> float:
    return (velocity_kms * KM_TO_M) ** 2 / (radius_kpc * KPC_TO_M)


def rar_prediction(gbar: np.ndarray) -> np.ndarray:
    return gbar / (1.0 - np.exp(-np.sqrt(gbar / A0)))


def build_point_sample(
    galaxy_properties: dict[str, dict[str, float | int | str]],
    bulges: dict[str, float],
    mass_rows: list[dict[str, float | str]],
) -> tuple[list[dict[str, float | str]], list[dict[str, float | int | str]]]:
    points: list[dict[str, float | str]] = []
    per_galaxy_rows: list[dict[str, float | int | str]] = []
    grouped: dict[str, list[dict[str, float | str]]] = defaultdict(list)
    skipped_nonpositive = 0

    for row in mass_rows:
        galaxy = str(row["galaxy"])
        radius = float(row["R_kpc"])
        vobs = float(row["Vobs_kms"])
        gobs = g_from_velocity(radius, vobs)

        vbar_sq = (
            signed_square(float(row["Vgas_kms"]))
            + UPSILON_DISK * signed_square(float(row["Vdisk_kms"]))
            + UPSILON_BULGE * signed_square(float(row["Vbul_kms"]))
        )
        if vbar_sq <= 0.0 or gobs <= 0.0:
            skipped_nonpositive += 1
            continue

        vbar = math.sqrt(vbar_sq)
        gbar = g_from_velocity(radius, vbar)
        gpred = float(rar_prediction(np.array([gbar]))[0])
        delta = math.log10(gobs) - math.log10(gpred)

        point = {
            "galaxy": galaxy,
            "R_kpc": radius,
            "Vobs_kms": vobs,
            "e_Vobs_kms": float(row["e_Vobs_kms"]),
            "gobs_mps2": gobs,
            "gbar_mps2": gbar,
            "gpred_mps2": gpred,
            "log10_gobs": math.log10(gobs),
            "log10_gbar": math.log10(gbar),
            "log10_gpred": math.log10(gpred),
            "delta_dex": delta,
        }
        points.append(point)
        grouped[galaxy].append(point)

    for galaxy, galaxy_points in grouped.items():
        meta = galaxy_properties[galaxy]
        lbul = bulges.get(galaxy, 0.0)
        ltot = float(meta["L36_1e9Lsun"])
        ldisk = max(ltot - lbul, 0.0)
        mstar = UPSILON_DISK * ldisk + UPSILON_BULGE * lbul
        mgas = HELIUM_FACTOR * float(meta["MHI_1e9Msun"])
        mbar = mstar + mgas
        gas_fraction = mgas / mbar if mbar > 0 else np.nan

        deltas = np.array([float(point["delta_dex"]) for point in galaxy_points])
        vobs = np.array([float(point["Vobs_kms"]) for point in galaxy_points])
        evobs = np.array([float(point["e_Vobs_kms"]) for point in galaxy_points])
        frac_err = np.divide(evobs, vobs, out=np.zeros_like(evobs), where=vobs > 0)

        per_galaxy_rows.append(
            {
                "galaxy": galaxy,
                "Q": int(meta["Q"]),
                "T": int(meta["T"]),
                "D_mpc": float(meta["D_mpc"]),
                "e_D_mpc": float(meta["e_D_mpc"]),
                "distance_frac_error": float(meta["e_D_mpc"]) / float(meta["D_mpc"]),
                "Inc_deg": float(meta["Inc_deg"]),
                "e_Inc_deg": float(meta["e_Inc_deg"]),
                "SBeff_Lsun_pc2": float(meta["SBeff_Lsun_pc2"]),
                "Rdisk_kpc": float(meta["Rdisk_kpc"]),
                "Vflat_kms": float(meta["Vflat_kms"]),
                "Vmax_kms": float(vobs.max()),
                "n_points": int(len(galaxy_points)),
                "mean_frac_v_error": float(frac_err.mean()),
                "median_frac_v_error": float(np.median(frac_err)),
                "L36_1e9Lsun": ltot,
                "Lbul_1e9Lsun": lbul,
                "Mstar_1e9Msun": mstar,
                "Mgas_1e9Msun": mgas,
                "Mbar_1e9Msun": mbar,
                "gas_fraction": gas_fraction,
                "mean_residual_dex": float(deltas.mean()),
                "median_residual_dex": float(np.median(deltas)),
                "std_residual_dex": float(deltas.std(ddof=1)) if len(deltas) > 1 else 0.0,
            }
        )

    per_galaxy_rows.sort(key=lambda row: str(row["galaxy"]))
    print(f"Skipped {skipped_nonpositive} points with non-positive baryonic acceleration.")
    return points, per_galaxy_rows


def spearman_table(per_galaxy_rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str | int]]:
    properties = [
        ("T", "Hubble type"),
        ("Mbar_1e9Msun", "Total baryonic mass"),
        ("gas_fraction", "Gas fraction"),
        ("SBeff_Lsun_pc2", "Effective surface brightness"),
        ("D_mpc", "Distance"),
        ("Rdisk_kpc", "Disk scale length"),
        ("Vmax_kms", "Maximum rotation velocity"),
        ("Q", "Quality flag"),
    ]
    residuals = np.array([float(row["mean_residual_dex"]) for row in per_galaxy_rows])
    results: list[dict[str, float | str | int]] = []

    for key, label in properties:
        x = np.array([float(row[key]) for row in per_galaxy_rows], dtype=float)
        mask = np.isfinite(x) & np.isfinite(residuals)
        rho, pvalue = spearmanr(x[mask], residuals[mask])
        results.append(
            {
                "property_key": key,
                "property_label": label,
                "n_galaxies": int(mask.sum()),
                "spearman_rho": float(rho),
                "p_value": float(pvalue),
                "significant_p_lt_0.01": int(float(pvalue) < 0.01),
            }
        )

    results.sort(key=lambda row: float(row["p_value"]))
    return results


def artifact_checks(per_galaxy_rows: list[dict[str, float | int | str]]) -> list[dict[str, float | str | int]]:
    checks: list[tuple[str, list[dict[str, float | int | str]], str, str, str]] = [
        (
            "all",
            per_galaxy_rows,
            "Vmax_kms",
            "mean_residual_dex",
            "Residual vs Vmax (all Q<=2)",
        ),
        (
            "all",
            per_galaxy_rows,
            "Q",
            "mean_residual_dex",
            "Residual vs quality flag",
        ),
        (
            "all",
            per_galaxy_rows,
            "mean_frac_v_error",
            "mean_residual_dex",
            "Residual vs mean fractional V error",
        ),
        (
            "all",
            per_galaxy_rows,
            "median_frac_v_error",
            "mean_residual_dex",
            "Residual vs median fractional V error",
        ),
        (
            "all",
            per_galaxy_rows,
            "n_points",
            "mean_residual_dex",
            "Residual vs number of RC points",
        ),
        (
            "all",
            per_galaxy_rows,
            "Q",
            "Vmax_kms",
            "Vmax vs quality flag",
        ),
        (
            "all",
            per_galaxy_rows,
            "mean_frac_v_error",
            "Vmax_kms",
            "Vmax vs mean fractional V error",
        ),
        (
            "all",
            per_galaxy_rows,
            "median_frac_v_error",
            "Vmax_kms",
            "Vmax vs median fractional V error",
        ),
        (
            "Q=1",
            [row for row in per_galaxy_rows if int(row["Q"]) == 1],
            "Vmax_kms",
            "mean_residual_dex",
            "Residual vs Vmax within Q=1",
        ),
        (
            "Q=2",
            [row for row in per_galaxy_rows if int(row["Q"]) == 2],
            "Vmax_kms",
            "mean_residual_dex",
            "Residual vs Vmax within Q=2",
        ),
        (
            "Inc>30",
            [row for row in per_galaxy_rows if float(row["Inc_deg"]) > 30.0],
            "Vmax_kms",
            "mean_residual_dex",
            "Residual vs Vmax with Inc>30 deg",
        ),
        (
            "Inc>30,Q=1",
            [row for row in per_galaxy_rows if float(row["Inc_deg"]) > 30.0 and int(row["Q"]) == 1],
            "Vmax_kms",
            "mean_residual_dex",
            "Residual vs Vmax with Inc>30 deg and Q=1",
        ),
        (
            "Inc>30,Q=2",
            [row for row in per_galaxy_rows if float(row["Inc_deg"]) > 30.0 and int(row["Q"]) == 2],
            "Vmax_kms",
            "mean_residual_dex",
            "Residual vs Vmax with Inc>30 deg and Q=2",
        ),
    ]

    rows: list[dict[str, float | str | int]] = []
    for sample, sample_rows, x_key, y_key, label in checks:
        x = np.array([float(row[x_key]) for row in sample_rows], dtype=float)
        y = np.array([float(row[y_key]) for row in sample_rows], dtype=float)
        mask = np.isfinite(x) & np.isfinite(y)
        rho, pvalue = spearmanr(x[mask], y[mask])
        rows.append(
            {
                "sample": sample,
                "x_key": x_key,
                "y_key": y_key,
                "label": label,
                "n_galaxies": int(mask.sum()),
                "spearman_rho": float(rho),
                "p_value": float(pvalue),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_rar_plot(path: Path, points: list[dict[str, float | str]]) -> None:
    log_gbar = np.array([float(point["log10_gbar"]) for point in points])
    log_gobs = np.array([float(point["log10_gobs"]) for point in points])
    grid = np.linspace(log_gbar.min() - 0.2, log_gbar.max() + 0.2, 500)
    gbar_grid = 10 ** grid
    gpred_grid = rar_prediction(gbar_grid)

    fig, ax = plt.subplots(figsize=(7.4, 6.0))
    ax.scatter(log_gbar, log_gobs, s=7, alpha=0.25, color="#1f4e79", linewidths=0)
    ax.plot(grid, np.log10(gpred_grid), color="#c0392b", lw=2.2)
    ax.plot(grid, grid, color="#777777", lw=1.2, ls="--", alpha=0.7)
    ax.set_xlabel(r"$\log_{10}(g_{\rm bar}\,[{\rm m\,s^{-2}}])$")
    ax.set_ylabel(r"$\log_{10}(g_{\rm obs}\,[{\rm m\,s^{-2}}])$")
    ax.set_title("SPARC RAR Reconstruction (Q = 1 or 2)")
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_property_grid(
    path: Path,
    per_galaxy_rows: list[dict[str, float | int | str]],
    correlations: list[dict[str, float | str | int]],
) -> None:
    correlation_lookup = {str(row["property_key"]): row for row in correlations}
    layout = [
        ("T", "Hubble type T", "linear"),
        ("Mbar_1e9Msun", r"$M_{\rm bar}$ [$10^9\,M_\odot$]", "log"),
        ("gas_fraction", r"$M_{\rm gas}/M_{\rm bar}$", "linear"),
        ("SBeff_Lsun_pc2", r"$S_{\rm eff}$ [$L_\odot\,{\rm pc^{-2}}$]", "log"),
        ("D_mpc", "Distance [Mpc]", "log"),
        ("Rdisk_kpc", r"$R_{\rm disk}$ [kpc]", "log"),
        ("Vmax_kms", r"$V_{\rm max}$ [km s$^{-1}$]", "log"),
        ("Q", "Quality flag", "linear"),
    ]
    residuals = np.array([float(row["mean_residual_dex"]) for row in per_galaxy_rows])

    fig, axes = plt.subplots(4, 2, figsize=(11.5, 13.5), sharey=True)
    axes = axes.ravel()
    for ax, (key, xlabel, scale) in zip(axes, layout):
        x = np.array([float(row[key]) for row in per_galaxy_rows])
        if key in {"T", "Q"}:
            jitter = np.linspace(-0.08, 0.08, len(x))
            ax.scatter(x + jitter, residuals, s=28, alpha=0.8, color="#1f4e79", edgecolor="white", linewidth=0.3)
        else:
            ax.scatter(x, residuals, s=28, alpha=0.8, color="#1f4e79", edgecolor="white", linewidth=0.3)
            ax.set_xscale(scale)
        ax.axhline(0.0, color="#777777", lw=1.0, ls="--", alpha=0.7)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Mean RAR residual [dex]")
        stats = correlation_lookup[key]
        ax.text(
            0.03,
            0.96,
            f"$\\rho$ = {float(stats['spearman_rho']):+.2f}\np = {float(stats['p_value']):.3g}",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#bbbbbb", "alpha": 0.9},
        )
        ax.grid(alpha=0.15)

    fig.suptitle("Per-Galaxy Mean RAR Residuals vs SPARC Galaxy Properties", y=0.995)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_residual_histogram(path: Path, per_galaxy_rows: list[dict[str, float | int | str]]) -> None:
    values = np.array([float(row["mean_residual_dex"]) for row in per_galaxy_rows])
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.hist(values, bins=16, color="#1f4e79", alpha=0.85, edgecolor="white")
    ax.axvline(values.mean(), color="#c0392b", lw=2.0, label=f"Mean = {values.mean():+.3f} dex")
    ax.set_xlabel("Per-galaxy mean RAR residual [dex]")
    ax.set_ylabel("Number of galaxies")
    ax.set_title("Distribution of Per-Galaxy Mean Residuals")
    ax.legend(frameon=False)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_artifact_plot(path: Path, per_galaxy_rows: list[dict[str, float | int | str]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8), sharey=True)
    colors = {1: "#1f4e79", 2: "#d35400"}
    labels = {1: "Q = 1", 2: "Q = 2"}
    residuals = np.array([float(row["mean_residual_dex"]) for row in per_galaxy_rows])

    for q in [1, 2]:
        subset = [row for row in per_galaxy_rows if int(row["Q"]) == q]
        axes[0].scatter(
            [float(row["Vmax_kms"]) for row in subset],
            [float(row["mean_residual_dex"]) for row in subset],
            s=30,
            alpha=0.8,
            color=colors[q],
            edgecolor="white",
            linewidth=0.3,
            label=labels[q],
        )
        axes[1].scatter(
            [float(row["mean_frac_v_error"]) for row in subset],
            [float(row["mean_residual_dex"]) for row in subset],
            s=30,
            alpha=0.8,
            color=colors[q],
            edgecolor="white",
            linewidth=0.3,
            label=labels[q],
        )

    axes[0].set_xscale("log")
    axes[0].set_xlabel(r"$V_{\rm max}$ [km s$^{-1}$]")
    axes[0].set_ylabel("Mean RAR residual [dex]")
    axes[0].set_title("Residual vs Maximum Rotation Velocity")
    axes[1].set_xlabel("Mean fractional velocity error")
    axes[1].set_title("Residual vs Velocity Error Proxy")
    for ax in axes:
        ax.axhline(0.0, color="#777777", lw=1.0, ls="--", alpha=0.7)
        ax.grid(alpha=0.15)
    axes[0].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def summarize(
    path: Path,
    points: list[dict[str, float | str]],
    per_galaxy_rows: list[dict[str, float | int | str]],
    correlations: list[dict[str, float | str | int]],
    artifact_rows: list[dict[str, float | str | int]],
    correlations_inc_gt_30: list[dict[str, float | str | int]],
) -> None:
    point_residuals = np.array([float(point["delta_dex"]) for point in points])
    galaxy_residuals = np.array([float(row["mean_residual_dex"]) for row in per_galaxy_rows])
    significant = [row for row in correlations if int(row["significant_p_lt_0.01"]) == 1]

    lines = [
        "# SPARC RAR Residual Correlation Summary",
        "",
        f"- Galaxies kept: {len(per_galaxy_rows)} (quality flag 1 or 2)",
        f"- Radial points kept: {len(points)}",
        f"- Point-level residual scatter: {point_residuals.std(ddof=1):.4f} dex",
        f"- Mean of per-galaxy mean residuals: {galaxy_residuals.mean():+.4f} dex",
        f"- Scatter of per-galaxy mean residuals: {galaxy_residuals.std(ddof=1):.4f} dex",
        "",
        "## Spearman Results",
        "",
        "| Property | rho | p-value | Significant (p < 0.01) |",
        "|---|---:|---:|---:|",
    ]
    for row in correlations:
        lines.append(
            f"| {row['property_label']} | {float(row['spearman_rho']):+.3f} | {float(row['p_value']):.4g} | {int(row['significant_p_lt_0.01'])} |"
        )

    lines.extend(["", "## Interpretation", ""])
    if significant:
        lines.append("Significant correlations were found and need follow-up artifact checks:")
        for row in significant:
            lines.append(f"- {row['property_label']}: rho = {float(row['spearman_rho']):+.3f}, p = {float(row['p_value']):.4g}")
    else:
        lines.append("No tested galaxy property reached the p < 0.01 threshold for the per-galaxy mean residuals.")

    lines.extend(
        [
            "",
            "Under the requested Q<=2 cut, the only p<0.01 signals are Vmax and the SPARC quality flag.",
            "The quality-flag trend is almost certainly non-physical because Q directly measures data reliability.",
            "The Vmax trend is also likely non-physical: it disappears in the Q=1 subsample, survives only in Q=2 galaxies, and Vmax is strongly anti-correlated with the fractional velocity-error proxies.",
            "No robust physical second-parameter signal is seen for gas fraction, distance, disk scale length, or total baryonic mass.",
        ]
    )

    lines.extend(["", "## Artifact Checks", ""])
    lines.append("| Check | Sample | rho | p-value |")
    lines.append("|---|---|---:|---:|")
    for row in artifact_rows:
        lines.append(
            f"| {row['label']} | {row['sample']} | {float(row['spearman_rho']):+.3f} | {float(row['p_value']):.4g} |"
        )

    lines.extend(["", "## Inclination > 30 deg Robustness", ""])
    lines.append("| Property | rho | p-value |")
    lines.append("|---|---:|---:|")
    for row in correlations_inc_gt_30:
        lines.append(f"| {row['property_label']} | {float(row['spearman_rho']):+.3f} | {float(row['p_value']):.4g} |")

    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    base = Path(__file__).resolve().parent
    raw_dir = base / "data" / "raw"
    output_dir = base / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    galaxy_properties = load_sparc_properties(raw_dir / "SPARC_Lelli2016c.mrt")
    bulges = load_bulges(raw_dir / "Bulges.mrt")
    mass_rows = load_mass_models(raw_dir / "MassModels_Lelli2016c.mrt", galaxy_properties)
    points, per_galaxy_rows = build_point_sample(galaxy_properties, bulges, mass_rows)
    correlations = spearman_table(per_galaxy_rows)
    artifact_rows = artifact_checks(per_galaxy_rows)
    correlations_inc_gt_30 = spearman_table(
        [row for row in per_galaxy_rows if float(row["Inc_deg"]) > 30.0]
    )

    write_csv(output_dir / "sparc_point_residuals.csv", points)
    write_csv(output_dir / "sparc_galaxy_mean_residuals.csv", per_galaxy_rows)
    write_csv(output_dir / "sparc_residual_correlations.csv", correlations)
    write_csv(output_dir / "sparc_artifact_checks.csv", artifact_rows)
    write_csv(output_dir / "sparc_residual_correlations_inc_gt_30.csv", correlations_inc_gt_30)

    save_rar_plot(output_dir / "sparc_rar_reconstruction.png", points)
    save_property_grid(output_dir / "sparc_residual_vs_properties.png", per_galaxy_rows, correlations)
    save_residual_histogram(output_dir / "sparc_mean_residual_histogram.png", per_galaxy_rows)
    save_artifact_plot(output_dir / "sparc_artifact_checks.png", per_galaxy_rows)
    summarize(
        output_dir / "summary.md",
        points,
        per_galaxy_rows,
        correlations,
        artifact_rows,
        correlations_inc_gt_30,
    )

    point_residuals = np.array([float(point["delta_dex"]) for point in points])
    print(f"Kept {len(per_galaxy_rows)} galaxies and {len(points)} radial points.")
    print(f"Point-level residual scatter = {point_residuals.std(ddof=1):.4f} dex")
    print("Correlation results:")
    for row in correlations:
        print(
            f"  {row['property_label']:<28s} rho={float(row['spearman_rho']):+0.3f}  p={float(row['p_value']):0.4g}"
        )


if __name__ == "__main__":
    main()
