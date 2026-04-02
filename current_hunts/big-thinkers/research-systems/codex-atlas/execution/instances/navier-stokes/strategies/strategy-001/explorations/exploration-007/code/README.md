# Exploration 007 Code

## Dependencies
- NumPy
- Exploration 002 code (ns_solver.py, slack_measurements.py) — referenced via relative path

## Scripts

1. **compute_all.py** — Main computation. Runs DNS at Re=100/500/1000/5000, computes:
   - BKM slack ratios (Part A)
   - BMO norms of vorticity (Part B)
   - Flatness, volume fractions, effective Ladyzhenskaya constants (Part C)
   - Conditional bound C(F4) (Part D)
   - Saves results to `../results_007.json`

2. **detailed_analysis.py** — Post-hoc analysis of saved results. Produces:
   - BKM constant calibration
   - Time-evolution tables
   - Flatness-C_Leff correlation fits
   - Conditional bound envelope analysis
   - Summary tables for the report

## Run order
```bash
cd /path/to/exploration-007/code
python compute_all.py      # ~3 minutes
python detailed_analysis.py  # ~1 second
```
