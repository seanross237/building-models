# Exploration 008 Code

## Files

- `ald_sed_exploration008.py` — Main simulation script (reused from E007's `ald_sed_optimized.py`)
- `qm_reference.json` — QM reference values from matrix diagonalization
- `results_n2.25.json` — Task A: n=2.25 β-scan results
- `results_n2.5.json` — Task A: n=2.50 β-scan results
- `results_n2.75.json` — Task A: n=2.75 β-scan results
- `results_taskB_physical.json` — Task B: n=3 physical normalization results
- `final_results.json` — Complete summary of all results

## Running

```bash
cd code/
python ald_sed_exploration008.py
```

Runtime: ~18 minutes on Apple M-series CPU.

## Parameters

All parameters identical to E007: dt=0.05, T=20000, N_ensemble=200, tau=0.01, omega0=1, omega_max=10.

Task A calibration: T=5000, N=50 (then rescaled via linear response).
Task B: C_3 = 0.02 (physical ZPF normalization, 2×tau×hbar/m with hbar=m=1).
