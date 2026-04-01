# Code: Finite Group Approximation of SU(2)

## Files

- `finite_subgroups.py` — Constructs binary tetrahedral (2T, 24), octahedral (2O, 48), icosahedral (2I, 120) groups as quaternion sets. Precomputes multiplication/inverse tables.
- `finite_group_lattice.py` — Lattice gauge theory for finite groups (exact discrete heat bath) and continuous SU(2) (Kennedy-Pendleton heat bath). Measures plaquette, Wilson loops, Creutz ratios, Polyakov loop.
- `run_simulation.py` — Main simulation: runs all groups at β = 1.0–4.0, produces comparison tables and convergence analysis. Output: `results.json`.
- `phase_scan.py` — Fine β scan with hot/cold start hysteresis to locate phase transitions.
- `analysis.py` — Post-processing of results.json: phase transition detection, convergence rate fitting, area law analysis.

## Running

```bash
# Full simulation (~7 minutes)
python run_simulation.py

# Phase transition scan (~5 minutes)
python phase_scan.py

# Analysis of saved results
python analysis.py
```

## Dependencies
- Python 3, NumPy
