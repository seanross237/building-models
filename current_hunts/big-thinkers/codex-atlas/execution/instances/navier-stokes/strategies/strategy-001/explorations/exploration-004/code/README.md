# Exploration 004 Code

## Files

- `decomposition.py` — Main computation: runs NS simulation, computes all slack decomposition factors and alignment statistics at each timestep. Outputs `results_Re100.json` and `results_Re1000.json`. Run time: ~5 minutes.
- `alignment_analysis.py` — Post-processing: reads JSON results and prints formatted alignment statistics tables. Requires results files from `decomposition.py`.
- `verify_sqrt2.py` — Verification: tests the identity ||∇u|| = √2 ||S|| for random div-free fields on T³. Also verifies ||∇u|| = ||ω||.
- `sharp_lad_focused.py` — Sharp Ladyzhenskaya constant: surveys known maximizers, computes effective constants from simulation data. Does NOT require scipy.
- `sharp_ladyzhenskaya.py` — Extended Ladyzhenskaya optimizer (requires scipy, which has a numpy version conflict on this system).

## Dependencies

- numpy (>= 2.0)
- Python 3.9+
- No scipy required for the main computations

## Run Order

```bash
python decomposition.py          # Main simulation (required first)
python alignment_analysis.py     # Analysis (requires results JSONs)
python verify_sqrt2.py           # Identity verification (independent)
python sharp_lad_focused.py      # Sharp constant analysis (requires results JSONs)
```

## Output Files

- `results_Re100.json` — Full decomposition and alignment data at 16 timesteps, Re=100
- `results_Re1000.json` — Same for Re=1000
