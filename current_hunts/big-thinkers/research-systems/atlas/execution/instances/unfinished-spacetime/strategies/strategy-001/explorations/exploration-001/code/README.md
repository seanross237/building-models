# Code for Exploration 001

## Files

### `prepare_public_data.py`
Downloads and converts a minimal first-pass dataset bundle:

- `Pantheon+` Hubble-diagram observables
- `DES-SN5YR` Hubble-diagram observables
- `DESI DR2 BAO` all-tracer summary points

It writes normalized screening inputs under `code/data/`, including:

- `desi_dr2_bao_summary.csv`
- `desi_dr2_bao_covariance.txt`

If a public source rate-limits, it falls back to the cached raw file in `code/data/raw/`.

### `background_only_analysis.py`
Coarse background-only screening pipeline for:

- `LCDM`
- constant-`w`
- CPL
- smooth-step `w(z)`

It supports:

- synthetic self-check mode
- simple BAO summary CSV input
- optional full BAO covariance input
- simple SN summary CSV input
- coarse grid search over model parameters
- cached background curves across the unique redshift grid for practical real-data runs

This is intentionally not a full `cobaya` / `CLASS` likelihood stack. It is the smallest honest first pass.

### `grid_refined_lowz.json`
Refined parameter grid centered on the low-`H0`, low-`z_t` region exposed by the first coarse run.

### `dataset_manifest.example.json`
Template describing the public datasets to wire in next. It documents expected local file paths and which stage each dataset belongs to.

## Expected CSV Schemas

### SN CSV

Headers:

`z,mu,sigma`

### BAO CSV

Headers:

`z,observable,value,sigma`

Where `observable` is one of:

- `DM_over_rd`
- `DH_over_rd`
- `DV_over_rd`

## Example Commands

Synthetic self-check:

```bash
python background_only_analysis.py --self-check
```

Prepare public summary files:

```bash
python prepare_public_data.py
```

Real-data first pass with `Pantheon+`:

```bash
python background_only_analysis.py \
  --sn-csv data/pantheon_plus_mb_corr.csv \
  --bao-csv data/desi_dr2_bao_summary.csv \
  --models lcdm wcdm cpl step
```

Sample swap with `DES-SN5YR`:

```bash
python background_only_analysis.py \
  --sn-csv data/des_sn5yr_mu.csv \
  --bao-csv data/desi_dr2_bao_summary.csv \
  --models lcdm wcdm cpl step
```

Full-covariance follow-up with the refined grid:

```bash
python background_only_analysis.py \
  --grid-config grid_refined_lowz.json \
  --sn-csv data/pantheon_plus_mb_corr.csv \
  --bao-csv data/desi_dr2_bao_summary.csv \
  --bao-cov data/desi_dr2_bao_covariance.txt \
  --models lcdm wcdm cpl step
```

## Known Limits

- No official `Planck` or `ACT` likelihoods yet
- SN covariances are not used yet
- No growth-sector modeling
- `r_d` is fixed by design in the first pass

Those limits are deliberate. This file is for screening, not publication-grade inference.
