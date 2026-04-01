# Exploration 002: Code

## Scripts

1. **classicality_budget.py** — Main computation. Requires `numpy`, `scipy`. Outputs numerical results to stdout and `results.json`.
2. **plot_budget.py** — Generates 3 PNG plots from `results.json`. Requires `matplotlib`.

## To reproduce

```bash
cd code/
python3 classicality_budget.py
python3 plot_budget.py
```

## Output files

- `results.json` — Computed entropy bounds for all 6 systems (JSON)
- `classicality_budget_plot.png` — R_delta vs S_T log-log plot
- `entropy_bounds_comparison.png` — Bar chart of entropy bounds
- `tradeoff_curve.png` — Redundancy vs richness trade-off curves
