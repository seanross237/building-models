# Exploration 005 Code

## Files

- `run_all_scans_fixed_dt.py` — Main runner. Runs all 13 (β, ω_max, τ) combinations.
  Uses fixed dt=0.05 (same as E004) for stability. Saves to `scan_results_fixed_dt.json`.

- `ald_simulate_scan.py` — Single-case runner (command-line args: beta omega_max tau).
  Same physics, for quick one-off checks. Saves to `scan_results.json`.

- `run_all_scans.py` — DEPRECATED. First attempt using dt=π/ω_max (Nyquist limit).
  Fails for β=1.0 at ω_max=10,20 due to Euler-Cromer instability. Do not use.

- `scan_results_fixed_dt.json` — All 13 results from `run_all_scans_fixed_dt.py`.
  Keys: `beta{β}_omax{ω_max}_tau{τ}`.

- `scan_results.json` — Results from the (failed) Nyquist-dt attempt. Kept for reference.

## Running

```bash
# Run all cases (takes ~4 minutes total):
python run_all_scans_fixed_dt.py

# Run a single case:
python ald_simulate_scan.py 1.0 20 0.01
```

## Dependencies
numpy (standard installation). No special requirements.
