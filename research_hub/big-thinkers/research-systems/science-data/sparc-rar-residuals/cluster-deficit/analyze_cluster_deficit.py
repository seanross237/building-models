#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean, median

from scipy.stats import mannwhitneyu, spearmanr


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"


CLASH_ROWS = [
    {
        "cluster": "MACS0329",
        "z": 0.450,
        "log10_M200c_Msun": 14.83,
        "temperature_keV": 8.0,
        "Mgas_1e14_Msun": 1.13,
        "deltaM_1e14_Msun": 1.79,
        "log10_eta": 1.27,
        "cutoff_mpc": 0.24,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS1115",
        "z": 0.352,
        "log10_M200c_Msun": 15.32,
        "temperature_keV": 8.0,
        "Mgas_1e14_Msun": 2.03,
        "deltaM_1e14_Msun": 3.17,
        "log10_eta": 0.66,
        "cutoff_mpc": 1.40,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MS2137",
        "z": 0.313,
        "log10_M200c_Msun": 15.07,
        "temperature_keV": 5.9,
        "Mgas_1e14_Msun": 0.77,
        "deltaM_1e14_Msun": 2.73,
        "log10_eta": 0.70,
        "cutoff_mpc": 4.14,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "RXJ1347",
        "z": 0.451,
        "log10_M200c_Msun": 15.44,
        "temperature_keV": 15.5,
        "Mgas_1e14_Msun": 5.28,
        "deltaM_1e14_Msun": 7.71,
        "log10_eta": 0.81,
        "cutoff_mpc": 1.61,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "RXJ2129",
        "z": 0.234,
        "log10_M200c_Msun": 14.96,
        "temperature_keV": 5.8,
        "Mgas_1e14_Msun": 1.03,
        "deltaM_1e14_Msun": 0.85,
        "log10_eta": 1.06,
        "cutoff_mpc": 0.23,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "A209",
        "z": 0.206,
        "log10_M200c_Msun": 15.29,
        "temperature_keV": 7.3,
        "Mgas_1e14_Msun": 2.33,
        "deltaM_1e14_Msun": 2.88,
        "log10_eta": 0.91,
        "cutoff_mpc": 0.60,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "A611",
        "z": 0.288,
        "log10_M200c_Msun": 15.15,
        "temperature_keV": 7.90,
        "Mgas_1e14_Msun": 1.62,
        "deltaM_1e14_Msun": 2.99,
        "log10_eta": 1.12,
        "cutoff_mpc": 0.48,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "A2261",
        "z": 0.224,
        "log10_M200c_Msun": 15.28,
        "temperature_keV": 7.6,
        "Mgas_1e14_Msun": 3.32,
        "deltaM_1e14_Msun": 4.46,
        "log10_eta": 1.05,
        "cutoff_mpc": 0.65,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS0416",
        "z": 0.396,
        "log10_M200c_Msun": 14.94,
        "temperature_keV": 7.5,
        "Mgas_1e14_Msun": 1.58,
        "deltaM_1e14_Msun": 1.61,
        "log10_eta": 1.28,
        "cutoff_mpc": 0.19,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS0429",
        "z": 0.399,
        "log10_M200c_Msun": 15.06,
        "temperature_keV": 6.00,
        "Mgas_1e14_Msun": 1.46,
        "deltaM_1e14_Msun": 1.61,
        "log10_eta": 1.03,
        "cutoff_mpc": 0.38,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS0647",
        "z": 0.584,
        "log10_M200c_Msun": 14.97,
        "temperature_keV": 13.3,
        "Mgas_1e14_Msun": 1.28,
        "deltaM_1e14_Msun": 2.95,
        "log10_eta": 1.07,
        "cutoff_mpc": 0.35,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS0744",
        "z": 0.686,
        "log10_M200c_Msun": 15.19,
        "temperature_keV": 8.9,
        "Mgas_1e14_Msun": 2.22,
        "deltaM_1e14_Msun": 4.18,
        "log10_eta": 1.01,
        "cutoff_mpc": 0.55,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS1149",
        "z": 0.544,
        "log10_M200c_Msun": 15.42,
        "temperature_keV": 8.7,
        "Mgas_1e14_Msun": 4.84,
        "deltaM_1e14_Msun": 4.65,
        "log10_eta": 1.07,
        "cutoff_mpc": 0.38,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS1206",
        "z": 0.440,
        "log10_M200c_Msun": 15.22,
        "temperature_keV": 10.8,
        "Mgas_1e14_Msun": 2.97,
        "deltaM_1e14_Msun": 3.24,
        "log10_eta": 0.98,
        "cutoff_mpc": 0.40,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "MACS1720",
        "z": 0.391,
        "log10_M200c_Msun": 15.07,
        "temperature_keV": 6.6,
        "Mgas_1e14_Msun": 1.58,
        "deltaM_1e14_Msun": 2.83,
        "log10_eta": 1.08,
        "cutoff_mpc": 0.46,
        "disequilibrium": 0,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
    {
        "cluster": "RXJ2248",
        "z": 0.348,
        "log10_M200c_Msun": 15.17,
        "temperature_keV": 12.4,
        "Mgas_1e14_Msun": 2.83,
        "deltaM_1e14_Msun": 2.55,
        "log10_eta": 0.81,
        "cutoff_mpc": 0.39,
        "disequilibrium": 1,
        "source": "Famaey et al. 2025 + Mistele et al. 2025",
    },
]

XCOP_ROWS = [
    {
        "cluster": "A1795",
        "z": 0.0622,
        "temperature_keV": 3.27,
        "Rout_mpc": 2.4,
        "Mbar_1e14_Msun": 1.18,
        "Mmm_over_Mbar_with_EFE": 1.10,
        "Mmm_over_Mbar_no_EFE": 0.76,
        "dynamical_state": "relaxed",
        "source": "Kelleher & Lelli 2024",
    },
    {
        "cluster": "A2029",
        "z": 0.0766,
        "temperature_keV": 5.75,
        "Rout_mpc": 2.7,
        "Mbar_1e14_Msun": 2.42,
        "Mmm_over_Mbar_with_EFE": 0.61,
        "Mmm_over_Mbar_no_EFE": 0.37,
        "dynamical_state": "relaxed",
        "source": "Kelleher & Lelli 2024",
    },
    {
        "cluster": "A2142",
        "z": 0.0900,
        "temperature_keV": 6.22,
        "Rout_mpc": 2.8,
        "Mbar_1e14_Msun": 2.84,
        "Mmm_over_Mbar_with_EFE": 0.38,
        "Mmm_over_Mbar_no_EFE": 0.26,
        "dynamical_state": "relaxed",
        "source": "Kelleher & Lelli 2024",
    },
    {
        "cluster": "A644",
        "z": 0.0704,
        "temperature_keV": 5.68,
        "Rout_mpc": 1.7,
        "Mbar_1e14_Msun": 1.09,
        "Mmm_over_Mbar_with_EFE": 5.43,
        "Mmm_over_Mbar_no_EFE": 3.38,
        "dynamical_state": "merger_signature",
        "source": "Kelleher & Lelli 2024",
    },
    {
        "cluster": "A2319",
        "z": 0.0557,
        "temperature_keV": 7.21,
        "Rout_mpc": 2.5,
        "Mbar_1e14_Msun": 3.05,
        "Mmm_over_Mbar_with_EFE": 3.99,
        "Mmm_over_Mbar_no_EFE": 1.29,
        "dynamical_state": "merger_signature",
        "source": "Kelleher & Lelli 2024",
    },
]


def save_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_json(path: Path, payload: object) -> None:
    with path.open("w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def log_scatter(values: list[float]) -> float:
    logs = [math.log10(value) for value in values]
    center = mean(logs)
    return math.sqrt(sum((value - center) ** 2 for value in logs) / (len(logs) - 1))


def spearman_summary(x: list[float], y: list[float]) -> dict[str, float]:
    result = spearmanr(x, y)
    return {"rho": float(result.statistic), "pvalue": float(result.pvalue)}


def summarize_clash() -> tuple[list[dict[str, object]], dict[str, object]]:
    rows = []
    for row in CLASH_ROWS:
        enriched = dict(row)
        enriched["eta"] = 10 ** row["log10_eta"]
        enriched["deltaM_over_Mgas"] = row["deltaM_1e14_Msun"] / row["Mgas_1e14_Msun"]
        rows.append(enriched)

    ratios = [row["deltaM_over_Mgas"] for row in rows]
    etas = [row["eta"] for row in rows]
    temperatures = [row["temperature_keV"] for row in rows]
    masses = [row["log10_M200c_Msun"] for row in rows]
    redshifts = [row["z"] for row in rows]
    diseq = [row["disequilibrium"] for row in rows]

    relaxed = [row["deltaM_over_Mgas"] for row in rows if row["disequilibrium"] == 0]
    disturbed = [row["deltaM_over_Mgas"] for row in rows if row["disequilibrium"] == 1]
    mwu = mannwhitneyu(relaxed, disturbed, alternative="two-sided")

    summary = {
        "n_clusters": len(rows),
        "proxy": "deltaM/Mgas and eta = rho_missing/rho_hot_gas from Famaey et al. 2025",
        "deltaM_over_Mgas": {
            "mean": mean(ratios),
            "median": median(ratios),
            "std_dex": log_scatter(ratios),
        },
        "eta": {
            "mean": mean(etas),
            "median": median(etas),
            "std_dex": log_scatter(etas),
        },
        "spearman": {
            "deltaM_over_Mgas_vs_temperature": spearman_summary(temperatures, ratios),
            "deltaM_over_Mgas_vs_log10_M200c": spearman_summary(masses, ratios),
            "deltaM_over_Mgas_vs_redshift": spearman_summary(redshifts, ratios),
            "deltaM_over_Mgas_vs_disequilibrium": spearman_summary(diseq, ratios),
            "eta_vs_temperature": spearman_summary(temperatures, etas),
            "eta_vs_log10_M200c": spearman_summary(masses, etas),
            "eta_vs_redshift": spearman_summary(redshifts, etas),
            "eta_vs_disequilibrium": spearman_summary(diseq, etas),
        },
        "deltaM_over_Mgas_relaxed_vs_disturbed": {
            "median_relaxed": median(relaxed),
            "median_disturbed": median(disturbed),
            "mann_whitney_u": float(mwu.statistic),
            "pvalue": float(mwu.pvalue),
        },
    }
    return rows, summary


def summarize_xcop() -> tuple[list[dict[str, object]], dict[str, object]]:
    rows = []
    for row in XCOP_ROWS:
        enriched = dict(row)
        enriched["disequilibrium"] = 0 if row["dynamical_state"] == "relaxed" else 1
        rows.append(enriched)

    values = [row["Mmm_over_Mbar_with_EFE"] for row in rows]
    temperatures = [row["temperature_keV"] for row in rows]
    redshifts = [row["z"] for row in rows]
    diseq = [row["disequilibrium"] for row in rows]
    relaxed = [row["Mmm_over_Mbar_with_EFE"] for row in rows if row["dynamical_state"] == "relaxed"]
    merging = [row["Mmm_over_Mbar_with_EFE"] for row in rows if row["dynamical_state"] != "relaxed"]

    summary = {
        "n_clusters": len(rows),
        "proxy": "M_missing/M_bar at Rout from Kelleher & Lelli 2024",
        "Mmm_over_Mbar_with_EFE": {
            "mean": mean(values),
            "median": median(values),
            "std_dex": log_scatter(values),
        },
        "spearman": {
            "with_EFE_vs_temperature": spearman_summary(temperatures, values),
            "with_EFE_vs_redshift": spearman_summary(redshifts, values),
            "with_EFE_vs_disequilibrium": spearman_summary(diseq, values),
        },
        "with_EFE_relaxed_vs_merging": {
            "median_relaxed": median(relaxed),
            "median_merging": median(merging),
        },
    }
    return rows, summary


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    clash_rows, clash_summary = summarize_clash()
    xcop_rows, xcop_summary = summarize_xcop()

    save_csv(DATA_DIR / "clash_inner_profile_proxy.csv", clash_rows)
    save_csv(DATA_DIR / "xcop_missing_mass_ratios.csv", xcop_rows)
    save_json(
        OUTPUT_DIR / "cluster_deficit_stats.json",
        {
            "clash_inner_profile_proxy": clash_summary,
            "xcop_missing_mass_ratios": xcop_summary,
        },
    )

    print(json.dumps({"clash": clash_summary, "xcop": xcop_summary}, indent=2))


if __name__ == "__main__":
    main()
