# Exploration 004 Code

Scripts for analyzing compensated compactness / commutator structure in the NS De Giorgi bottleneck.

## Dependencies
- Python 3, numpy, scipy, sympy
- NS solver from strategy-001: `../../../strategy-001/explorations/exploration-002/code/ns_solver.py`

## Scripts

| Script | Description | Run order |
|--------|-------------|-----------|
| `task1_bilinear_form.py` | Symbolic derivation of the exact bilinear form of I_k | 1 (standalone) |
| `task2_divcurl_analysis.py` | Analytical check of div-curl structure | 2 (standalone) |
| `task2c_numerical_compressibility.py` | Numerical compressibility error measurement on DNS | 3 (requires ns_solver) |
| `task3_commutator_analysis.py` | Commutator mechanism analysis + numerical verification | 4 (requires ns_solver) |
| `task4_obstruction.py` | Summary of the three-layer obstruction | 5 (standalone) |

## Run all
```bash
python task1_bilinear_form.py
python task2_divcurl_analysis.py
python task2c_numerical_compressibility.py
python task3_commutator_analysis.py
python task4_obstruction.py
```
