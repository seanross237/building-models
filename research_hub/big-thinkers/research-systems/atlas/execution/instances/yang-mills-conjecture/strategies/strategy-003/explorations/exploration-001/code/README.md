# Code for Exploration 001

All scripts run with `/opt/homebrew/bin/python3` (requires numpy, scipy).

## Files

- `stage0_sanity.py` — Validates M(Q) implementation: Q=I eigenvalues, B-field/matrix self-consistency
- `stage1_v3.py` — Random sampling (1000 configs) + grid-search refinement to maximize λ_max(M(Q))
- `stage2_hessian.py` — Compares HessS with (β/2N)M element-by-element and via quadratic forms
- `verify_counterexample.py` — Verifies Q=iσ₃ counterexample: adjoint rep, holonomies, eigenvector, gauge orthogonality
- `hessian_at_sigma3.py` — Computes full 192×192 Hessian at Q=iσ₃ by finite differences, compares spectrum with M

## Key Results

- `stage0_sanity.py`: λ_max(M(I)) = 16 ✓
- `stage1_v3.py`: λ_max(M(iσ₃)) = 24 (counterexample)
- `hessian_at_sigma3.py`: λ_max(HessS) = 4.0 at Q=iσ₃ (Hessian respects the bound even though M doesn't)
