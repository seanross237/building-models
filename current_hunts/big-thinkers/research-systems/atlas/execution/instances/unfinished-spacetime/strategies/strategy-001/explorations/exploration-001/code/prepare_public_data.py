#!/usr/bin/env python3
"""Fetch and convert the smallest public datasets needed for the first pass.

Outputs clean CSV files for the background-only screen:

- pantheon_plus_mb_corr.csv
- des_sn5yr_mu.csv
- desi_dr2_bao_summary.csv
- desi_dr2_bao_covariance.txt

The conversions are intentionally simple and documented:

- Pantheon+ uses zHD, m_b_corr, and m_b_corr_err_DIAG, excluding calibrators.
- DES-SN5YR uses zHD, MU, and MUERR from the released Hubble diagram.
- DESI DR2 BAO uses the official ALL_GCcomb mean/cov files and writes both
  the aligned summary CSV and the full covariance matrix for follow-up runs.
"""

from __future__ import annotations

import base64
import csv
import json
import math
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data"

PANTHEON_BLOB_API = (
    "https://api.github.com/repos/PantheonPlusSH0ES/DataRelease/git/blobs/"
    "cce857db0c15e9ce7a0e0ce77452b6ff62af969a"
)
DES_SN_HD_URL = (
    "https://raw.githubusercontent.com/des-science/DES-SN5YR/main/"
    "4_DISTANCES_COVMAT/DES-Dovekie_HD.csv"
)
DESI_BAO_MEAN_URL = (
    "https://raw.githubusercontent.com/CobayaSampler/bao_data/master/"
    "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
)
DESI_BAO_COV_URL = (
    "https://raw.githubusercontent.com/CobayaSampler/bao_data/master/"
    "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"
)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "atlas-cosmology-screen/0.1"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def fetch_json(url: str) -> dict:
    return json.loads(fetch_text(url))


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    path.write_text(text)


def prepare_pantheon() -> dict:
    raw_path = RAW_DIR / "Pantheon+SH0ES.dat"
    try:
        blob = fetch_json(PANTHEON_BLOB_API)
        decoded = base64.b64decode(blob["content"]).decode("utf-8")
        write_text(raw_path, decoded)
    except (urllib.error.URLError, KeyError, ValueError):
        if not raw_path.exists():
            raise
        decoded = raw_path.read_text()

    lines = decoded.splitlines()
    header = lines[0].split()
    rows = [line.split() for line in lines[1:] if line.strip()]
    idx = {name: i for i, name in enumerate(header)}

    out_path = OUT_DIR / "pantheon_plus_mb_corr.csv"
    kept = 0
    with out_path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["z", "mu", "sigma"])
        for row in rows:
            z = float(row[idx["zHD"]])
            is_calibrator = int(float(row[idx["IS_CALIBRATOR"]]))
            mb = float(row[idx["m_b_corr"]])
            sigma = float(row[idx["m_b_corr_err_DIAG"]])
            if is_calibrator != 0:
                continue
            if z <= 0.01:
                continue
            if not math.isfinite(mb) or not math.isfinite(sigma):
                continue
            writer.writerow([f"{z:.8f}", f"{mb:.8f}", f"{sigma:.8f}"])
            kept += 1
    return {"rows_kept": kept, "output": str(out_path)}


def prepare_des_sn() -> dict:
    raw_path = RAW_DIR / "DES-Dovekie_HD.csv"
    try:
        text = fetch_text(DES_SN_HD_URL)
        write_text(raw_path, text)
    except urllib.error.URLError:
        if not raw_path.exists():
            raise
        text = raw_path.read_text()

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    varnames_line = next(line for line in lines if line.startswith("VARNAMES:"))
    columns = varnames_line.replace("VARNAMES:", "").strip().split()
    idx = {name: i for i, name in enumerate(columns)}
    sn_lines = [line for line in lines if line.startswith("SN:")]

    out_path = OUT_DIR / "des_sn5yr_mu.csv"
    kept = 0
    with out_path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["z", "mu", "sigma"])
        for line in sn_lines:
            payload = line.replace("SN:", "", 1).strip().split()
            z = float(payload[idx["zHD"]])
            mu = float(payload[idx["MU"]])
            sigma = float(payload[idx["MUERR"]])
            writer.writerow([f"{z:.8f}", f"{mu:.8f}", f"{sigma:.8f}"])
            kept += 1
    return {"rows_kept": kept, "output": str(out_path)}


def prepare_bao() -> dict:
    mean_raw_path = RAW_DIR / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
    cov_raw_path = RAW_DIR / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
    try:
        mean_text = fetch_text(DESI_BAO_MEAN_URL)
        write_text(mean_raw_path, mean_text)
    except urllib.error.URLError:
        if not mean_raw_path.exists():
            raise
        mean_text = mean_raw_path.read_text()
    try:
        cov_text = fetch_text(DESI_BAO_COV_URL)
        write_text(cov_raw_path, cov_text)
    except urllib.error.URLError:
        if not cov_raw_path.exists():
            raise
        cov_text = cov_raw_path.read_text()

    mean_rows = []
    for line in mean_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        z_str, value_str, quantity = line.split()
        mean_rows.append((float(z_str), float(value_str), quantity))

    cov_rows = []
    for line in cov_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cov_rows.append([float(x) for x in line.split()])

    if len(mean_rows) != len(cov_rows):
        raise ValueError("DESI BAO mean/cov dimension mismatch")

    out_path = OUT_DIR / "desi_dr2_bao_summary.csv"
    cov_path = OUT_DIR / "desi_dr2_bao_covariance.txt"
    with out_path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["z", "observable", "value", "sigma"])
        for i, (z, value, quantity) in enumerate(mean_rows):
            observable = quantity.replace("_over_rs", "_over_rd")
            sigma = math.sqrt(cov_rows[i][i])
            writer.writerow([f"{z:.8f}", observable, f"{value:.8f}", f"{sigma:.8f}"])
    write_text(
        cov_path,
        "\n".join(" ".join(f"{value:.12e}" for value in row) for row in cov_rows) + "\n",
    )
    return {
        "rows_kept": len(mean_rows),
        "output": str(out_path),
        "covariance_output": str(cov_path),
    }


def main() -> None:
    ensure_dirs()
    summary = {
        "pantheon_plus": prepare_pantheon(),
        "des_sn5yr": prepare_des_sn(),
        "desi_bao": prepare_bao(),
    }
    summary_path = OUT_DIR / "prepare_public_data_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
