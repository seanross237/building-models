#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import json
import math
import re
import tarfile
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, pstdev
from urllib.request import urlopen

import matplotlib.pyplot as plt
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
NOTES_DIR = ROOT / "notes"


ARXIV_EPRINTS = {
    "famaey_2024": "https://arxiv.org/e-print/2410.02612",
    "mistele_2025": "https://arxiv.org/e-print/2506.13716",
    "zhang_2026": "https://arxiv.org/e-print/2602.06082",
}


@dataclass
class SourceNote:
    label: str
    url: str
    note: str


def fetch_tex(eprint_url: str, tex_name: str) -> str:
    data = urlopen(eprint_url).read()
    archive = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
    return archive.extractfile(tex_name).read().decode("utf-8", errors="ignore")


def first_num(text: str) -> float | None:
    match = re.search(r"[-+]?[0-9]*\.?[0-9]+", text)
    return float(match.group()) if match else None


def norm_name(name: str) -> str:
    clean = name.replace("Abell", "A").replace("MACSJ", "MACS")
    return clean.replace(" ", "")


def save_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_famaey_clash_table() -> list[dict[str, object]]:
    text = fetch_tex(ARXIV_EPRINTS["famaey_2024"], "arxiv.tex")
    start = text.find("Cluster & $kT$(keV)")
    end = text.find("\\end{tabular}", start)
    block = text[start:end]

    rows: list[dict[str, object]] = []
    for raw in block.split("\\\\"):
        row = " ".join(raw.split())
        if "&" not in row or row.startswith("Cluster ") or row.startswith("\\hline") or not row:
            continue
        parts = [part.strip() for part in row.split("&")]
        if len(parts) == 6:
            parts.append("")
        if len(parts) != 7:
            continue
        name, temp, mgas, dmass, logeta, r0lam, diseq = parts
        mgas_value = first_num(mgas)
        dmass_value = first_num(dmass)
        logeta_value = first_num(logeta)
        rows.append(
            {
                "cluster": name,
                "cluster_key": norm_name(name),
                "temperature_keV": first_num(temp),
                "gas_mass_1e14_msun": mgas_value,
                "mond_missing_mass_1e14_msun": dmass_value,
                "approx_deficit_factor": 1.0 + dmass_value / mgas_value,
                "log10_eta": logeta_value,
                "eta": 10.0**logeta_value,
                "r0_over_lambda_mpc": first_num(r0lam),
                "disequilibrium_flag": "*" in diseq,
                "source": "Famaey et al. 2024/2025 CLASH lensing table",
            }
        )
    return rows


def parse_mistele_cluster_list() -> dict[str, dict[str, float]]:
    text = fetch_tex(ARXIV_EPRINTS["mistele_2025"], "plots/table-cluster-list.tex")
    rows = {}
    for raw in text.splitlines():
        row = raw.strip()
        if not row or "&" not in row:
            continue
        parts = [part.strip().replace("\\\\", "") for part in row.split("&")]
        if len(parts) != 5:
            continue
        name, z, rxmax, logm2h, logm200c = parts
        rows[norm_name(name)] = {
            "redshift": first_num(z),
            "rxmax_mpc": first_num(rxmax),
            "log10_m200c_msun": first_num(logm200c),
        }
    return rows


def parse_zhang_2mass_table() -> list[dict[str, object]]:
    text = fetch_tex(ARXIV_EPRINTS["zhang_2026"], "main.tex")
    start = text.rfind("Name &  $z$")
    end = text.find("From left to right: Name of cluster", start)
    block = text[start:end]

    rows: list[dict[str, object]] = []
    for raw in block.split("\\\\"):
        row = " ".join(raw.split())
        if "&" not in row or row.startswith("Name ") or row.startswith("\\hline") or not row:
            continue
        parts = [part.strip() for part in row.split("&")]
        if len(parts) != 12:
            continue
        name = parts[0]
        if name.startswith("%"):
            name = name.split()[-1]
        z, _, _, _, _, _, mtot_imf, mtot_ig, m_mond_dyn = (
            first_num(parts[1]),
            first_num(parts[2]),
            first_num(parts[3]),
            first_num(parts[4]),
            first_num(parts[5]),
            first_num(parts[6]),
            first_num(parts[7]),
            first_num(parts[8]),
            first_num(parts[9]),
        )
        rows.append(
            {
                "cluster": name,
                "redshift": z,
                "baryonic_mass_canonical_1e14_msun": mtot_imf,
                "baryonic_mass_igimf_1e14_msun": mtot_ig,
                "mond_dynamical_mass_1e14_msun": m_mond_dyn,
                "deficit_factor_canonical": m_mond_dyn / mtot_imf,
                "deficit_factor_igimf": m_mond_dyn / mtot_ig,
                "source": "Zhang et al. 2026 2MASS cluster table",
            }
        )
    return rows


def merge_clash_data(
    famaey_rows: list[dict[str, object]],
    mistele_rows: dict[str, dict[str, float]],
) -> list[dict[str, object]]:
    merged = []
    for row in famaey_rows:
        merged_row = dict(row)
        merged_row.update(mistele_rows[row["cluster_key"]])
        merged.append(merged_row)
    return merged


def dex_scatter(values: list[float]) -> float:
    return pstdev([math.log10(value) for value in values])


def summarize_clash(rows: list[dict[str, object]]) -> dict[str, object]:
    factors = [row["approx_deficit_factor"] for row in rows]
    relaxed = [row["approx_deficit_factor"] for row in rows if not row["disequilibrium_flag"]]
    disturbed = [row["approx_deficit_factor"] for row in rows if row["disequilibrium_flag"]]
    rho_t, p_t = spearmanr([row["temperature_keV"] for row in rows], factors)
    rho_m, p_m = spearmanr([row["log10_m200c_msun"] for row in rows], factors)
    rho_z, p_z = spearmanr([row["redshift"] for row in rows], factors)
    rho_eta, p_eta = spearmanr([row["log10_eta"] for row in rows], factors)
    return {
        "n_clusters": len(rows),
        "mean_factor": mean(factors),
        "median_factor": median(factors),
        "std_factor": pstdev(factors),
        "dex_scatter": dex_scatter(factors),
        "min_factor": min(factors),
        "max_factor": max(factors),
        "spearman_temperature": {"rho": rho_t, "p_value": p_t},
        "spearman_mass": {"rho": rho_m, "p_value": p_m},
        "spearman_redshift": {"rho": rho_z, "p_value": p_z},
        "spearman_logeta": {"rho": rho_eta, "p_value": p_eta},
        "relaxed_mean_factor": mean(relaxed),
        "disturbed_mean_factor": mean(disturbed),
        "relaxed_n": len(relaxed),
        "disturbed_n": len(disturbed),
    }


def summarize_2mass(rows: list[dict[str, object]]) -> dict[str, object]:
    canonical = [row["deficit_factor_canonical"] for row in rows]
    igimf = [row["deficit_factor_igimf"] for row in rows]
    rho_c_m, p_c_m = spearmanr([row["mond_dynamical_mass_1e14_msun"] for row in rows], canonical)
    rho_i_m, p_i_m = spearmanr([row["mond_dynamical_mass_1e14_msun"] for row in rows], igimf)
    rho_c_z, p_c_z = spearmanr([row["redshift"] for row in rows], canonical)
    return {
        "n_clusters": len(rows),
        "canonical": {
            "mean_factor": mean(canonical),
            "median_factor": median(canonical),
            "std_factor": pstdev(canonical),
            "dex_scatter": dex_scatter(canonical),
            "min_factor": min(canonical),
            "max_factor": max(canonical),
            "spearman_mass": {"rho": rho_c_m, "p_value": p_c_m},
            "spearman_redshift": {"rho": rho_c_z, "p_value": p_c_z},
        },
        "igimf": {
            "mean_factor": mean(igimf),
            "median_factor": median(igimf),
            "std_factor": pstdev(igimf),
            "dex_scatter": dex_scatter(igimf),
            "min_factor": min(igimf),
            "max_factor": max(igimf),
            "spearman_mass": {"rho": rho_i_m, "p_value": p_i_m},
        },
    }


def make_plot(clash_rows: list[dict[str, object]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    colors = ["#d62728" if row["disequilibrium_flag"] else "#1f77b4" for row in clash_rows]

    axes[0].scatter(
        [row["temperature_keV"] for row in clash_rows],
        [row["approx_deficit_factor"] for row in clash_rows],
        c=colors,
    )
    axes[0].set_xlabel("Temperature [keV]")
    axes[0].set_ylabel("Approx. deficit factor")
    axes[0].set_title("CLASH: deficit vs temperature")

    axes[1].scatter(
        [row["log10_m200c_msun"] for row in clash_rows],
        [row["approx_deficit_factor"] for row in clash_rows],
        c=colors,
    )
    axes[1].set_xlabel("log10(M200c/Msun)")
    axes[1].set_ylabel("Approx. deficit factor")
    axes[1].set_title("CLASH: deficit vs mass")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "clash_deficit_scatter.png", dpi=200)
    plt.close(fig)


def write_sources() -> None:
    notes = [
        SourceNote(
            "Famaey et al. 2024/2025",
            "https://arxiv.org/abs/2410.02612",
            "CLASH lensing analysis; finds nearly constant missing-to-hot-gas density ratio and cut-off radius in inner parts.",
        ),
        SourceNote(
            "Mistele et al. 2025",
            "https://arxiv.org/abs/2506.13716",
            "Non-parametric weak-lensing reconstruction; finds baryonic fractions vary significantly cluster to cluster and RAR offset depends strongly on gas extrapolation.",
        ),
        SourceNote(
            "Kelleher et al. 2024",
            "https://arxiv.org/abs/2405.08557",
            "X-COP hydrostatic analysis; relaxed clusters have smaller deficit and mergers larger apparent deficit.",
        ),
        SourceNote(
            "Pointecouteau & Silk 2005",
            "https://arxiv.org/abs/astro-ph/0505017",
            "Classic MOND cluster constraints from XMM clusters; active neutrino requirement around 1-2 eV.",
        ),
        SourceNote(
            "KATRIN Collaboration 2024/2025",
            "https://arxiv.org/abs/2406.13516",
            "Direct neutrino mass limit m_nu < 0.45 eV (90% CL).",
        ),
        SourceNote(
            "Angus, Famaey, Diaferio 2009",
            "https://arxiv.org/abs/0906.3322",
            "11 eV sterile-neutrino equilibrium configurations in MOND clusters; Tremaine-Gunn saturation in central regions.",
        ),
        SourceNote(
            "Angus & Diaferio 2011",
            "https://arxiv.org/abs/1104.5040",
            "MOND cosmological simulations with massive sterile neutrinos; rich-cluster abundance and density-profile tensions remain.",
        ),
        SourceNote(
            "Giare et al. 2025",
            "https://journals.aps.org/prd/accepted/f407fQb8T9412b40b448025241c913c1245798caf",
            "Modified-growth example showing that cosmological neutrino-mass bounds can relax outside standard LCDM assumptions.",
        ),
        SourceNote(
            "Zhang et al. 2026",
            "https://arxiv.org/abs/2602.06082",
            "Recent re-analysis with IGIMF-enhanced baryons for 46 nearby clusters; claims much of the MOND deficit can be alleviated.",
        ),
    ]
    lines = ["# Sources", ""]
    for note in notes:
        lines.append(f"- {note.label}: {note.url}")
        lines.append(f"  {note.note}")
    (NOTES_DIR / "sources.md").write_text("\n".join(lines))


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    famaey_rows = parse_famaey_clash_table()
    mistele_rows = parse_mistele_cluster_list()
    clash_rows = merge_clash_data(famaey_rows, mistele_rows)
    zhang_rows = parse_zhang_2mass_table()

    clash_summary = summarize_clash(clash_rows)
    zhang_summary = summarize_2mass(zhang_rows)

    save_csv(DATA_DIR / "clash_cluster_deficit_table.csv", clash_rows)
    save_csv(DATA_DIR / "zhang_2mass_cluster_deficit_table.csv", zhang_rows)
    with (OUTPUT_DIR / "analysis_summary.json").open("w") as handle:
        json.dump(
            {
                "clash_summary": clash_summary,
                "zhang_2mass_summary": zhang_summary,
                "kelleher_2024_note": {
                    "relaxed_clusters": "A1795, A2029, A2142",
                    "relaxed_missing_to_visible_ratio_200_300kpc": "about 1 to 5",
                    "relaxed_missing_to_visible_ratio_2_3Mpc": "about 0.4 to 1.1",
                    "merging_clusters": "A644, A2319",
                    "merging_missing_to_visible_ratio": "up to about 5",
                    "note": "Authors caution that merger-related disequilibrium may mimic a larger deficit.",
                },
            },
            handle,
            indent=2,
            sort_keys=True,
        )
    write_sources()
    make_plot(clash_rows)


if __name__ == "__main__":
    main()
