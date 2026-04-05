# Code for Exploration 003 — Excited-State Modular Flow

## Files

- **excited_state_test.py** — Main computation: builds lattice, computes vacuum/excited modular Hamiltonians, correlators, FFT. Runs N=50 main test + multi-mode comparison + convergence (N=20,30,50,100).

- **state_dependence_analysis.py** — Focused convergence analysis with mode 0 across N=20-200. Generates convergence plots and power-law fits.

- **spectral_analysis.py** — Initial spectral analysis (too-short tau window for mode 0).

- **spectral_detailed.py** — High-resolution spectral analysis with properly resolved frequencies. Tests both mode 0 (long tau window) and mode 5 (mid-frequency).

- **fixed_freq_convergence.py** — Critical test: convergence with FIXED physical frequency (omega ≈ 0.3 and 0.6) showing delta_disc GROWS with N.

## How to Run

```bash
# All files are self-contained (import from state_dependence_analysis.py)
python3 excited_state_test.py          # ~5 min
python3 state_dependence_analysis.py   # ~3 min
python3 spectral_detailed.py           # ~5 min
python3 fixed_freq_convergence.py      # ~5 min
```

## Dependencies

- numpy, scipy (for linear algebra, matrix exponential)
- matplotlib (for plots, uses Agg backend)

## Key Output

- `results.json` — Full results from excited_state_test.py
- `convergence_results.json` — Convergence data from state_dependence_analysis.py
- `*.png` — Plots
