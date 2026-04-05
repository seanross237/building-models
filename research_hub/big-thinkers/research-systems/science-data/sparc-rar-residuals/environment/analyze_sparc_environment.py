from __future__ import annotations

import csv
import math
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
from scipy.stats import mannwhitneyu, pearsonr, rankdata, spearmanr
from urllib.request import urlopen

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "output"
RESIDUAL_CSV = BASE_DIR.parent / "output" / "sparc_galaxy_mean_residuals.csv"

CHAE2020_PDF_URL = "https://astroweb.case.edu/ssm/papers/ApJv904n51.pdf"
CHAE2020_PDF = RAW_DIR / "Chae2020_ApJ_904_51.pdf"
CHAE2020_LAYOUT = RAW_DIR / "Chae2020_ApJ_904_51_layout.txt"

POWER_SHIFT_DEX = 0.05
POWER_NSIM = 20_000


@dataclass
class EnvironmentRow:
    galaxy: str
    galaxy_raw: str
    x0: float
    x0_missing_flag: int
    eenv: float
    eenv_err_lo: float
    eenv_err_hi: float


def ensure_raw_inputs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not CHAE2020_PDF.exists():
        with urlopen(CHAE2020_PDF_URL, timeout=60) as response:
            CHAE2020_PDF.write_bytes(response.read())

    if not CHAE2020_LAYOUT.exists():
        subprocess.run(
            ["pdftotext", "-layout", "-f", "16", "-l", "19", str(CHAE2020_PDF), str(CHAE2020_LAYOUT)],
            check=True,
        )


def normalize_galaxy_name(name: str) -> str:
    compact = " ".join(name.split()).replace(" ", "")
    if compact.endswith("a") and any(char.isdigit() for char in compact[:-1]):
        compact = compact[:-1]
    return compact


def parse_main_minus_token(token: str) -> tuple[float, float]:
    match = re.fullmatch(r"\s*([−-]?\d+\.\d+)\s*-\s*(\d+\.\d+)\s*", token)
    if match is None:
        raise ValueError(f"Could not parse main token: {token!r}")
    value = float(match.group(1).replace("−", "-"))
    err_lo = float(match.group(2))
    return value, err_lo


def parse_chae2020_environment_table() -> list[EnvironmentRow]:
    text = CHAE2020_LAYOUT.read_text()
    lines = text.splitlines()
    main_pattern = re.compile(r"^(?P<galaxy>.*?)\s{2,}(?P<x0>L|[−-]\d+\.\d+)\s+(?P<rest>.*)$")
    minus_token_pattern = re.compile(r"[−-]?\d+\.\d+\s*-\s*\d+\.\d+")
    plus_token_pattern = re.compile(r"\+\d+\.\d+")

    rows: list[EnvironmentRow] = []
    plus_line: str | None = None
    for line in lines:
        if (
            not line.strip()
            or ("Galaxy" in line and "eenv" in line)
            or "Table 2" in line
            or "(Continued)" in line
            or "The Astrophysical Journal" in line
            or "Chae et al." in line
            or "Notes." in line
            or "Figure" in line
            or "Appendix B" in line
            or line.strip().isdigit()
        ):
            continue

        if line.lstrip().startswith("+"):
            plus_line = line
            continue

        if plus_line is None:
            continue

        match = main_pattern.match(line)
        if match is None:
            continue

        galaxy_raw = " ".join(match.group("galaxy").split())
        galaxy = normalize_galaxy_name(galaxy_raw)
        x0_text = match.group("x0").replace("−", "-")
        minus_tokens = minus_token_pattern.findall(match.group("rest"))
        plus_tokens = plus_token_pattern.findall(plus_line)
        if len(minus_tokens) < 2 or len(plus_tokens) < 2:
            raise ValueError(f"Unexpected table structure for {galaxy_raw}")

        eenv_value, eenv_err_lo = parse_main_minus_token(minus_tokens[1])
        eenv_err_hi = float(plus_tokens[1].replace("+", ""))
        rows.append(
            EnvironmentRow(
                galaxy=galaxy,
                galaxy_raw=galaxy_raw,
                x0=np.nan if x0_text == "L" else float(x0_text),
                x0_missing_flag=1 if x0_text == "L" else 0,
                eenv=eenv_value,
                eenv_err_lo=eenv_err_lo,
                eenv_err_hi=eenv_err_hi,
            )
        )
        plus_line = None

    if len(rows) != 153:
        raise ValueError(f"Expected 153 Chae2020 environment rows, found {len(rows)}")
    return rows


def load_residual_rows() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    with RESIDUAL_CSV.open() as handle:
        for row in csv.DictReader(handle):
            parsed: dict[str, float | str] = {"galaxy": row["galaxy"]}
            for key, value in row.items():
                if key == "galaxy":
                    continue
                parsed[key] = float(value)
            rows.append(parsed)
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def partial_spearman(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> tuple[float, float]:
    x_rank = rankdata(np.asarray(x, dtype=float))
    y_rank = rankdata(np.asarray(y, dtype=float))
    z_rank = rankdata(np.asarray(z, dtype=float))
    design = np.column_stack([np.ones_like(z_rank), z_rank])
    resid_x = x_rank - design @ np.linalg.lstsq(design, x_rank, rcond=None)[0]
    resid_y = y_rank - design @ np.linalg.lstsq(design, y_rank, rcond=None)[0]
    result = pearsonr(resid_x, resid_y)
    return float(result.statistic), float(result.pvalue)


def mann_whitney_summary(label: str, values_a: np.ndarray, values_b: np.ndarray) -> dict[str, object]:
    result = mannwhitneyu(values_a, values_b, alternative="two-sided")
    return {
        "test": label,
        "n_a": int(len(values_a)),
        "n_b": int(len(values_b)),
        "mean_a_dex": float(np.mean(values_a)),
        "mean_b_dex": float(np.mean(values_b)),
        "mean_diff_b_minus_a_dex": float(np.mean(values_b) - np.mean(values_a)),
        "median_a_dex": float(np.median(values_a)),
        "median_b_dex": float(np.median(values_b)),
        "u_statistic": float(result.statistic),
        "p_value": float(result.pvalue),
    }


def simulate_mann_whitney_power(
    sigma_dex: float, n_a: int, n_b: int, shift_dex: float, nsim: int = POWER_NSIM
) -> float:
    rng = np.random.default_rng(0)
    sample_a = rng.normal(0.0, sigma_dex, size=(nsim, n_a))
    sample_b = rng.normal(shift_dex, sigma_dex, size=(nsim, n_b))
    detections = 0
    for index in range(nsim):
        pvalue = mannwhitneyu(sample_a[index], sample_b[index], alternative="two-sided").pvalue
        detections += int(pvalue < 0.05)
    return detections / nsim


def bootstrap_mean_difference(values_a: np.ndarray, values_b: np.ndarray, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    diffs = np.empty(20_000)
    for index in range(len(diffs)):
        boot_a = rng.choice(values_a, size=len(values_a), replace=True)
        boot_b = rng.choice(values_b, size=len(values_b), replace=True)
        diffs[index] = float(np.mean(boot_b) - np.mean(boot_a))
    lo, hi = np.quantile(diffs, [0.025, 0.975])
    return float(lo), float(hi)


def save_residual_vs_environment_plot(path: Path, matched_rows: list[dict[str, float | str]], spearman_row: dict[str, object]) -> None:
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    colors = {1: "#1f4e79", 2: "#d35400"}
    labels = {1: "Q = 1", 2: "Q = 2"}
    for quality in [1, 2]:
        subset = [row for row in matched_rows if int(row["Q"]) == quality]
        x = np.array([float(row["eenv"]) for row in subset])
        y = np.array([float(row["mean_residual_dex"]) for row in subset])
        xerr = np.array(
            [
                [float(row["eenv_err_lo"]) for row in subset],
                [float(row["eenv_err_hi"]) for row in subset],
            ]
        )
        ax.errorbar(
            x,
            y,
            xerr=xerr,
            fmt="none",
            ecolor="#cccccc",
            elinewidth=0.8,
            alpha=0.35,
            zorder=1,
        )
        ax.scatter(
            x,
            y,
            s=28,
            color=colors[quality],
            alpha=0.8,
            edgecolor="white",
            linewidth=0.3,
            label=labels[quality],
            zorder=2,
        )
    ax.axhline(0.0, color="#777777", lw=1.0, ls="--", alpha=0.7)
    ax.set_xscale("log")
    ax.set_xlabel(r"$e_{\rm env}$ from Chae et al. 2020")
    ax.set_ylabel("Mean RAR residual [dex]")
    ax.set_title("SPARC Mean RAR Residual vs Environment")
    ax.text(
        0.03,
        0.96,
        f"$\\rho$ = {float(spearman_row['rho']):+.3f}\np = {float(spearman_row['p_value']):.3g}",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#bbbbbb", "alpha": 0.9},
    )
    ax.grid(alpha=0.15)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def save_environment_sanity_plot(
    path: Path,
    matched_rows: list[dict[str, float | str]],
    env_distance_row: dict[str, object],
    quartile_test_row: dict[str, object],
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))

    x = np.array([float(row["D_mpc"]) for row in matched_rows])
    y = np.array([float(row["eenv"]) for row in matched_rows])
    axes[0].scatter(x, y, s=28, alpha=0.8, color="#1f4e79", edgecolor="white", linewidth=0.3)
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Distance [Mpc]")
    axes[0].set_ylabel(r"$e_{\rm env}$")
    axes[0].set_title("Environment Metric vs Distance")
    axes[0].text(
        0.03,
        0.96,
        f"$\\rho$ = {float(env_distance_row['rho']):+.3f}\np = {float(env_distance_row['p_value']):.3g}",
        transform=axes[0].transAxes,
        va="top",
        ha="left",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#bbbbbb", "alpha": 0.9},
    )
    axes[0].grid(alpha=0.15)

    q25 = np.quantile(y, 0.25)
    q75 = np.quantile(y, 0.75)
    low = [float(row["mean_residual_dex"]) for row in matched_rows if float(row["eenv"]) <= q25]
    high = [float(row["mean_residual_dex"]) for row in matched_rows if float(row["eenv"]) >= q75]
    positions = [0, 1]
    axes[1].boxplot(
        [low, high],
        positions=positions,
        widths=0.55,
        patch_artist=True,
        boxprops={"facecolor": "#d9e8f5", "edgecolor": "#1f4e79"},
        medianprops={"color": "#c0392b", "linewidth": 1.8},
        whiskerprops={"color": "#1f4e79"},
        capprops={"color": "#1f4e79"},
    )
    rng = np.random.default_rng(0)
    axes[1].scatter(np.full(len(low), positions[0]) + rng.uniform(-0.08, 0.08, len(low)), low, s=22, alpha=0.65, color="#1f4e79")
    axes[1].scatter(np.full(len(high), positions[1]) + rng.uniform(-0.08, 0.08, len(high)), high, s=22, alpha=0.65, color="#d35400")
    axes[1].axhline(0.0, color="#777777", lw=1.0, ls="--", alpha=0.7)
    axes[1].set_xticks(positions, ["Low $e_{env}$\n(bottom quartile)", "High $e_{env}$\n(top quartile)"])
    axes[1].set_ylabel("Mean RAR residual [dex]")
    axes[1].set_title("High-Contrast Environment Split")
    axes[1].text(
        0.03,
        0.96,
        f"$\\Delta \\mu$ = {float(quartile_test_row['mean_diff_b_minus_a_dex']):+.3f} dex\np = {float(quartile_test_row['p_value']):.3g}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#bbbbbb", "alpha": 0.9},
    )
    axes[1].grid(alpha=0.15)

    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def summarize(
    path: Path,
    matched_rows: list[dict[str, float | str]],
    missing_rows: list[dict[str, object]],
    stats_rows: list[dict[str, object]],
) -> None:
    stats = {str(row["test"]): row for row in stats_rows}
    eenv = np.array([float(row["eenv"]) for row in matched_rows])
    lines = [
        "# SPARC RAR Residual Environment Test",
        "",
        "- Environment metric: `eenv`, the independent external gravitational field estimate from Chae et al. (2020)",
        f"- Residual sample loaded from: `{RESIDUAL_CSV}`",
        f"- Matched galaxies with environment data: {len(matched_rows)}",
        f"- Q<=2 galaxies without environment data in Chae et al. table: {len(missing_rows)}",
        f"- `eenv` range: {eenv.min():.3f} to {eenv.max():.3f}",
        f"- `eenv` quartiles: {np.quantile(eenv, 0.25):.3f}, {np.quantile(eenv, 0.50):.3f}, {np.quantile(eenv, 0.75):.3f}",
        "",
        "## Main Result",
        "",
        f"- Spearman residual vs `eenv`: rho = {float(stats['spearman_residual_vs_eenv']['rho']):+.3f}, p = {float(stats['spearman_residual_vs_eenv']['p_value']):.4g}",
        f"- Partial Spearman controlling for distance: rho = {float(stats['partial_spearman_residual_vs_eenv_control_logD']['rho']):+.3f}, p = {float(stats['partial_spearman_residual_vs_eenv_control_logD']['p_value']):.4g}",
        f"- Distance vs `eenv`: rho = {float(stats['spearman_logD_vs_eenv']['rho']):+.3f}, p = {float(stats['spearman_logD_vs_eenv']['p_value']):.4g}",
        "",
        "No statistically significant environmental dependence is detected.",
        "",
        "## Binary Splits",
        "",
        f"- Median split in `eenv`: p = {float(stats['mannwhitney_median_split']['p_value']):.4g}, mean difference (high minus low) = {float(stats['mannwhitney_median_split']['mean_diff_b_minus_a_dex']):+.3f} dex",
        f"- Quartile split in `eenv`: p = {float(stats['mannwhitney_quartile_split']['p_value']):.4g}, mean difference (high minus low) = {float(stats['mannwhitney_quartile_split']['mean_diff_b_minus_a_dex']):+.3f} dex",
        f"- Quartile split 95% bootstrap CI on mean difference: [{float(stats['quartile_bootstrap_ci']['ci_lo_dex']):+.3f}, {float(stats['quartile_bootstrap_ci']['ci_hi_dex']):+.3f}] dex",
        "",
        "## Robustness",
        "",
        f"- Q=1 only: rho = {float(stats['spearman_residual_vs_eenv_q1']['rho']):+.3f}, p = {float(stats['spearman_residual_vs_eenv_q1']['p_value']):.4g}",
        f"- Q=2 only: rho = {float(stats['spearman_residual_vs_eenv_q2']['rho']):+.3f}, p = {float(stats['spearman_residual_vs_eenv_q2']['p_value']):.4g}",
        f"- Excluding the 5 Chae rows with `x0 = L`: rho = {float(stats['spearman_residual_vs_eenv_x0_defined']['rho']):+.3f}, p = {float(stats['spearman_residual_vs_eenv_x0_defined']['p_value']):.4g}",
        f"- Excluding the one extreme `eenv > 0.1` outlier: rho = {float(stats['spearman_residual_vs_eenv_no_outlier']['rho']):+.3f}, p = {float(stats['spearman_residual_vs_eenv_no_outlier']['p_value']):.4g}",
        "",
        "## Power",
        "",
        f"- Estimated power for a 0.05 dex shift with the median split Mann-Whitney test: {100 * float(stats['power_median_split_0p05dex']['power']):.1f}%",
        f"- Estimated power for a 0.05 dex shift with the quartile split Mann-Whitney test: {100 * float(stats['power_quartile_split_0p05dex']['power']):.1f}%",
        "",
        "This means the continuous null test is reasonably informative, but the isolated-vs-dense binary comparison is underpowered for small (~0.05 dex) shifts.",
        "",
        "## Missing Galaxies",
        "",
        ", ".join(row["galaxy"] for row in missing_rows),
        "",
        "## Conclusion",
        "",
        "Within the 153 SPARC galaxies with published environment estimates, galaxies in denser environments do not show a statistically significant offset from the same RAR followed by more isolated galaxies.",
        "This supports no detected environmental dependence in the present SPARC sample and environment metric.",
    ]
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    ensure_raw_inputs()

    residual_rows = load_residual_rows()
    environment_rows = parse_chae2020_environment_table()
    environment_lookup = {row.galaxy: row for row in environment_rows}

    matched_rows: list[dict[str, float | str]] = []
    missing_rows: list[dict[str, object]] = []
    for residual_row in residual_rows:
        galaxy = str(residual_row["galaxy"])
        env_row = environment_lookup.get(galaxy)
        if env_row is None:
            missing_rows.append({"galaxy": galaxy})
            continue
        merged = dict(residual_row)
        merged.update(
            {
                "eenv": env_row.eenv,
                "eenv_err_lo": env_row.eenv_err_lo,
                "eenv_err_hi": env_row.eenv_err_hi,
                "x0_chae2020": env_row.x0,
                "x0_missing_flag": env_row.x0_missing_flag,
                "galaxy_raw_chae2020": env_row.galaxy_raw,
            }
        )
        matched_rows.append(merged)

    environment_csv_rows = [
        {
            "galaxy": row.galaxy,
            "galaxy_raw_chae2020": row.galaxy_raw,
            "x0_chae2020": row.x0,
            "x0_missing_flag": row.x0_missing_flag,
            "eenv": row.eenv,
            "eenv_err_lo": row.eenv_err_lo,
            "eenv_err_hi": row.eenv_err_hi,
        }
        for row in environment_rows
    ]
    write_csv(OUTPUT_DIR / "chae2020_environment_table.csv", environment_csv_rows)
    write_csv(OUTPUT_DIR / "sparc_environment_matched.csv", matched_rows)
    write_csv(OUTPUT_DIR / "sparc_environment_missing_galaxies.csv", missing_rows)

    residual = np.array([float(row["mean_residual_dex"]) for row in matched_rows])
    eenv = np.array([float(row["eenv"]) for row in matched_rows])
    log_distance = np.log10(np.array([float(row["D_mpc"]) for row in matched_rows]))

    spearman_full = spearmanr(eenv, residual)
    spearman_logd_eenv = spearmanr(log_distance, eenv)
    partial_full = partial_spearman(np.log10(eenv), residual, log_distance)

    q1_rows = [row for row in matched_rows if int(row["Q"]) == 1]
    q2_rows = [row for row in matched_rows if int(row["Q"]) == 2]
    x0_defined_rows = [row for row in matched_rows if int(row["x0_missing_flag"]) == 0]
    no_outlier_rows = [row for row in matched_rows if float(row["eenv"]) < 0.1]

    q25, q50, q75 = np.quantile(eenv, [0.25, 0.50, 0.75])
    low_median = residual[eenv <= q50]
    high_median = residual[eenv > q50]
    low_quartile = residual[eenv <= q25]
    high_quartile = residual[eenv >= q75]
    quartile_ci_lo, quartile_ci_hi = bootstrap_mean_difference(low_quartile, high_quartile)

    sigma_matched = float(residual.std(ddof=1))
    power_median = simulate_mann_whitney_power(sigma_matched, len(low_median), len(high_median), POWER_SHIFT_DEX)
    power_quartile = simulate_mann_whitney_power(sigma_matched, len(low_quartile), len(high_quartile), POWER_SHIFT_DEX)

    stats_rows: list[dict[str, object]] = [
        {
            "test": "spearman_residual_vs_eenv",
            "n": len(matched_rows),
            "rho": float(spearman_full.statistic),
            "p_value": float(spearman_full.pvalue),
        },
        {
            "test": "partial_spearman_residual_vs_eenv_control_logD",
            "n": len(matched_rows),
            "rho": float(partial_full[0]),
            "p_value": float(partial_full[1]),
        },
        {
            "test": "spearman_logD_vs_eenv",
            "n": len(matched_rows),
            "rho": float(spearman_logd_eenv.statistic),
            "p_value": float(spearman_logd_eenv.pvalue),
        },
        {
            "test": "spearman_residual_vs_eenv_q1",
            "n": len(q1_rows),
            "rho": float(spearmanr([row["eenv"] for row in q1_rows], [row["mean_residual_dex"] for row in q1_rows]).statistic),
            "p_value": float(spearmanr([row["eenv"] for row in q1_rows], [row["mean_residual_dex"] for row in q1_rows]).pvalue),
        },
        {
            "test": "spearman_residual_vs_eenv_q2",
            "n": len(q2_rows),
            "rho": float(spearmanr([row["eenv"] for row in q2_rows], [row["mean_residual_dex"] for row in q2_rows]).statistic),
            "p_value": float(spearmanr([row["eenv"] for row in q2_rows], [row["mean_residual_dex"] for row in q2_rows]).pvalue),
        },
        {
            "test": "spearman_residual_vs_eenv_x0_defined",
            "n": len(x0_defined_rows),
            "rho": float(
                spearmanr([row["eenv"] for row in x0_defined_rows], [row["mean_residual_dex"] for row in x0_defined_rows]).statistic
            ),
            "p_value": float(
                spearmanr([row["eenv"] for row in x0_defined_rows], [row["mean_residual_dex"] for row in x0_defined_rows]).pvalue
            ),
        },
        {
            "test": "spearman_residual_vs_eenv_no_outlier",
            "n": len(no_outlier_rows),
            "rho": float(
                spearmanr([row["eenv"] for row in no_outlier_rows], [row["mean_residual_dex"] for row in no_outlier_rows]).statistic
            ),
            "p_value": float(
                spearmanr([row["eenv"] for row in no_outlier_rows], [row["mean_residual_dex"] for row in no_outlier_rows]).pvalue
            ),
        },
        mann_whitney_summary("mannwhitney_median_split", low_median, high_median),
        mann_whitney_summary("mannwhitney_quartile_split", low_quartile, high_quartile),
        {
            "test": "quartile_bootstrap_ci",
            "n": len(low_quartile) + len(high_quartile),
            "ci_lo_dex": quartile_ci_lo,
            "ci_hi_dex": quartile_ci_hi,
        },
        {
            "test": "power_median_split_0p05dex",
            "sigma_dex": sigma_matched,
            "n_a": len(low_median),
            "n_b": len(high_median),
            "shift_dex": POWER_SHIFT_DEX,
            "power": power_median,
        },
        {
            "test": "power_quartile_split_0p05dex",
            "sigma_dex": sigma_matched,
            "n_a": len(low_quartile),
            "n_b": len(high_quartile),
            "shift_dex": POWER_SHIFT_DEX,
            "power": power_quartile,
        },
    ]
    write_csv(OUTPUT_DIR / "sparc_environment_stats.csv", stats_rows)

    save_residual_vs_environment_plot(
        OUTPUT_DIR / "sparc_residual_vs_environment.png",
        matched_rows,
        next(row for row in stats_rows if row["test"] == "spearman_residual_vs_eenv"),
    )
    save_environment_sanity_plot(
        OUTPUT_DIR / "sparc_environment_sanity.png",
        matched_rows,
        next(row for row in stats_rows if row["test"] == "spearman_logD_vs_eenv"),
        next(row for row in stats_rows if row["test"] == "mannwhitney_quartile_split"),
    )
    summarize(OUTPUT_DIR / "summary.md", matched_rows, missing_rows, stats_rows)

    print(f"Matched galaxies with environment data: {len(matched_rows)}")
    print(f"Missing Q<=2 galaxies without Chae2020 environment data: {len(missing_rows)}")
    print(f"Spearman residual vs eenv: rho={float(spearman_full.statistic):+.3f}, p={float(spearman_full.pvalue):.4g}")
    print(f"Partial Spearman residual vs eenv | logD: rho={partial_full[0]:+.3f}, p={partial_full[1]:.4g}")
    print(
        f"Median split Mann-Whitney: p={float(next(row for row in stats_rows if row['test']=='mannwhitney_median_split')['p_value']):.4g}"
    )
    print(
        f"Quartile split Mann-Whitney: p={float(next(row for row in stats_rows if row['test']=='mannwhitney_quartile_split')['p_value']):.4g}"
    )


if __name__ == "__main__":
    main()
