# Exploration 002 — Code

All scripts require Python 3 with numpy and scipy.

## Scripts (run in order)

1. **compute_nonequilibrium.py** — Main computation. Builds post-quench state, computes all three correlators for lambda sweep, runs Gibbs control checks and convergence checks. Outputs `nonequilibrium_results.json`. (~10s runtime)

2. **spectral_analysis.py** — High-resolution FFT with zero-padded analysis. Verifies numerical results against exact analytical formulas. Outputs `spectral_results.json`. (~30s runtime)

3. **analytical_comparison.py** — Pure analytical computation of discrepancies, asymptotic limits, and beat periods. No saved output (console only).

4. **squeezed_state_test.py** — Squeezed thermal state test (squeezing parameter r=0.3 on mode A). Outputs `squeezed_results.json`. (~10s runtime)

## Run all

```bash
python3 compute_nonequilibrium.py
python3 spectral_analysis.py
python3 analytical_comparison.py
python3 squeezed_state_test.py
```
