# Exploration 001 Report

Status: coarse first pass and full-covariance follow-up executed on 2026-04-02.

## Inputs Used

- `code/prepare_public_data.py`
- `code/data/pantheon_plus_mb_corr.csv` with 1580 rows
- `code/data/des_sn5yr_mu.csv` with 1820 rows
- `code/data/desi_dr2_bao_summary.csv` with 13 rows
- `code/data/desi_dr2_bao_covariance.txt` with the aligned `13 x 13` DESI DR2 covariance
- `code/grid_refined_lowz.json`
- model ladder: `LCDM -> wCDM -> CPL -> step`

## Data Handling Notes

- `Pantheon+` first pass uses `m_b_corr` with a floating intercept nuisance, not the full covariance release.
- `DES-SN5YR` uses the public Hubble-diagram file and per-SN diagonal uncertainties.
- The first screen used diagonalized `DESI DR2 BAO` errors; the follow-up reran the same pipeline with the full public BAO covariance.
- This is a triage run, not publication-grade inference.

## Joint Results

### `DESI + Pantheon+`

- `step`: `chi2=704.770`, `AIC=714.770`, `BIC=741.636`
  params: `Omega_m=0.30`, `H0=68.0`, `A=0.15`, `z_t=0.3`
- `cpl`: `chi2=713.154`
- `lcdm`: `chi2=726.690`
- `wcdm`: `chi2=726.690`

Relative to `LCDM`, the coarse step model improves `Δχ²=-21.920`.

Decomposition:

- `LCDM`: `chi2_sn=701.388`, `chi2_bao=25.302`
- `step`: `chi2_sn=694.141`, `chi2_bao=10.629`

### `DESI + DES-SN5YR`

- `step`: `chi2=1696.374`, `AIC=1706.374`, `BIC=1733.943`
  params: `Omega_m=0.30`, `H0=68.0`, `A=0.15`, `z_t=0.3`
- `cpl`: `chi2=1713.387`
- `wcdm`: `chi2=1720.885`
- `lcdm`: `chi2=1733.228`

Relative to `LCDM`, the coarse step model improves `Δχ²=-36.854`.

Decomposition:

- `LCDM`: `chi2_sn=1689.187`, `chi2_bao=44.041`
- `step`: `chi2_sn=1685.846`, `chi2_bao=10.528`

## Control Runs

### `DESI BAO` only

- `step`: `chi2=9.603`
- `lcdm`: `chi2=26.650`

This is the strongest driver of the apparent preference: `Δχ²=-17.047` for the step model relative to `LCDM`.

### `Pantheon+` only

- `step`: `chi2=694.079`
- `lcdm`: `chi2=694.376`

Pantheon+ alone is effectively indifferent at this coarse level.

### `DES-SN5YR` only

- `cpl`: `chi2=1683.595`
- `step`: `chi2=1685.157`
- `lcdm`: `chi2=1689.187`

DES-only mildly prefers non-`LCDM` late-time deformation, but not decisively.

## Coarse-Pass Interpretation

- The same qualitative signal survives the swap from `Pantheon+` to `DES-SN5YR`: a low-redshift deformation of late-time expansion outperforms coarse-grid `LCDM`.
- The present screen is driven primarily by `DESI DR2 BAO`, not by a strong supernova-only anomaly.
- The coarse step best fit repeatedly lands on the grid boundary at `H0=68.0` and often `z_t=0.3`, so the preferred region is not yet localized.
- The result was interesting enough to justify a second pass with full BAO covariance, refined low-`z_t` grids, and a real `w(z)` likelihood stack.

## Follow-Up: Full BAO Covariance + Refined Grid

### `DESI BAO` only

Default coarse grid with full covariance:

- `step`: `chi2=9.238`
- `lcdm`: `chi2=35.233`

Refined grid with full covariance:

- `cpl`: `chi2=8.521`
- `step`: `chi2=8.522`
- `wcdm`: `chi2=9.641`
- `lcdm`: `chi2=10.424`

This is the main correction to the coarse first pass:

- using the full `DESI` covariance keeps the signal alive
- refining the parameter grid removes the strong step-specific preference
- the BAO-only gain relative to `LCDM` shrinks from a dramatic coarse-screen effect to a modest `Δχ²≈-1.9`

### `DESI + Pantheon+`

Refined grid with full covariance:

- `wcdm`: `chi2=703.086`, `chi2_sn=693.911`, `chi2_bao=9.175`
- `cpl`: `chi2=703.086`, `chi2_sn=693.911`, `chi2_bao=9.175`
- `step`: `chi2=703.106`, `chi2_sn=694.263`, `chi2_bao=8.844`
- `lcdm`: `chi2=712.002`, `chi2_sn=701.388`, `chi2_bao=10.614`

Relative to `LCDM`, the best late-time deformation improves `Δχ²=-8.916`.

### `DESI + DES-SN5YR`

Refined grid with full covariance:

- `cpl`: `chi2=1692.224`, `chi2_sn=1683.341`, `chi2_bao=8.883`
- `step`: `chi2=1693.866`, `chi2_sn=1683.882`, `chi2_bao=9.984`
- `wcdm`: `chi2=1696.183`, `chi2_sn=1686.887`, `chi2_bao=9.295`
- `lcdm`: `chi2=1710.929`, `chi2_sn=1694.839`, `chi2_bao=16.091`

Relative to `LCDM`, the best late-time deformation improves `Δχ²=-18.706`.

## Updated Interpretation

- The full-covariance follow-up weakens the original claim that a step-like transition is the uniquely preferred explanation.
- What survives is narrower and more defensible: this screening pipeline continues to prefer some late-time dark-energy deformation over coarse `LCDM`, but `wCDM`, `CPL`, and `step` are now close competitors rather than a single standout winner.
- `Pantheon+` plus `DESI` prefers a mild `wCDM`-like shift near `Omega_m≈0.30`, `H0≈67.5`, `w0≈-0.9`.
- `DES-SN5YR` plus `DESI` prefers a somewhat stronger `CPL`-like deformation near `Omega_m≈0.32`, `H0≈67.5`, `w0≈-0.8`, `wa≈-0.8`.
- The follow-up result is interesting enough to justify a real likelihood-stage promotion, but it no longer justifies focusing specifically on the step model.

## Next Pass

- Promote the surviving late-time deformation family into `Cobaya/CLASS` with `Planck` or `ACT` anchors.
- Use the full public SN covariances instead of diagonal-only Hubble-diagram errors.
- Treat `wCDM` and `CPL` as the primary next-stage baselines; keep the step model as an exploratory alternative rather than the lead hypothesis.
