# Exploration 002: Code Directory

## Scripts (run in order)

1. **`compute_li_coefficients.py`** — Main computation. Pre-computes 2000 zeta zeros, then computes λ_n for n=1..500. Outputs: `zeros_cache.pkl`, `zeros.npz`, `li_coefficients.npz`. Runtime: ~11 minutes.

2. **`analyze_residuals.py`** — Tasks 3 & 4. Computes Bombieri-Lagarias and Coffey residuals, FFT analysis, prime correlation test, growth rate fitting. Outputs: `residuals.npz`, `fft_results.npz`, `analysis_results.json`.

3. **`gue_comparison.py`** — Tasks 4d & 5. GUE random matrix comparison and spectral rigidity (Δ₃). Outputs: `gue_results.npz`.

4. **`truncation_analysis.py`** — Analyzes convergence behavior as function of number of zeros (K=100..2000). Shows geometric convergence ratio ≈ 0.646.

## Requirements

- Python 3 with: `mpmath`, `numpy`, `sympy`
- No scipy required (scipy.optimize is broken in this environment)

## Data Files

- `zeros_cache.pkl` — Pickled mpmath complex zeros (2000 zeros, 50-digit precision)
- `li_coefficients.npz` — λ_n values: n_values, lambda_real, lambda_imag, zero_imag_parts
- `residuals.npz` — Asymptotic residuals: delta_bl, delta_coffey
- `fft_results.npz` — FFT of detrended Coffey residual
- `gue_results.npz` — GUE Li coefficients, Δ₃ values
