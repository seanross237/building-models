# Exploration 010 Code

## Files

- `scan_hessian.py` — Main script. Builds 192×192 analytical Hessian for SU(2) Wilson gauge theory on L=2, d=4 lattice. Tests 100 configurations across 4 categories (random, Gibbs, perturbed identity, adversarial). Convention: S = -(β/N) Σ Re Tr(U_P).

- `verify_bp_bound.py` — Verifies the intermediate B_P bound sum_P |B_P(Q,v)|^2 ≤ 4d|v|^2 for various Q and eigenvectors v.

- `debug_compare.py` — Diagnostic script that compares E009-style K matrix with analytical Hessian at Q=I. Used to identify the 1/N convention issue.

- `results.json` — Full numerical results from the scan.

## Running

```bash
python scan_hessian.py      # ~5 min, produces results.json
python verify_bp_bound.py   # ~30 sec, verifies B_P bound
```

Requirements: numpy (standard Python scientific stack).
