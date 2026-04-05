# SED Harmonic Oscillator — Code

## Files

- `sed_harmonic_oscillator.py` — Production simulation (corrected normalization). Frequency-domain solver with full Abraham-Lorentz transfer function, band-pass energy extraction, and multiple parameter runs. May require reducing N_modes or batch_size if memory is limited.

- `sed_corrected_run.py` — Lightweight corrected simulation. Runs 3 parameter sets with N=2000 ensemble, confirms var_x ~ 0.5 and demonstrates UV divergence of var_v. This is the script that produced the key numerical results in the report.

- `debug_normalization.py` — Normalization verification. Computes the spectral integral analytically, compares with FFT spectral sums and Monte Carlo, and demonstrates the factor-of-2 error in the original code.

## How to Run

```bash
# Quick results (recommended):
python sed_corrected_run.py

# Normalization verification:
python debug_normalization.py

# Full production run (memory-intensive, may need parameter adjustment):
python sed_harmonic_oscillator.py
```

## Dependencies
- numpy
- scipy (stats, integrate)

## Key Normalization

Correct one-sided PSD: `S_F(w) = 2 * tau * hbar * w^3 / m`

FFT amplitude (numpy convention): `|F_k| = sqrt(N * S_F(w_k) / (2 * dt))`

Expected position variance: `var_x = (2/N^2) * SUM |F_k|^2 / |H_k|^2`
