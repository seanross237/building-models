# Code for Exploration 001

All scripts use Python 3 with NumPy (no other dependencies).

## Files

### `derive_B_formula.py`
**Key result: GOAL.MD's B_□ formula is wrong.** Verifies the correct formula by finite differences. Run first to understand the correction.

### `verify_B_bound_L4_corrected.py`
Main verification: builds M(Q) = ∑_□ B_□^T B_□ on L=2 and L=4 lattices with **corrected** transport. Checks λ_max ≤ 4d for 28 configurations per lattice size. Zero violations found.

### `cross_check.py`
Cross-checks the matrix eigenvalue against direct B_□ computation. Confirmed 14-digit agreement.

### `perturbation_analysis.py`
Numerical perturbation analysis at Q=I on L=2. Confirms Q=I is a critical point (dλ/dε = 0) and local maximum (d²λ/dε² < 0).

### `uniform_config_proof.py`
Analytical proof for uniform configurations (Q_e = U for all e). Key inequality: (2I + R + R^T) ≼ 4I for R ∈ SO(3).

### `verify_B_bound_L4.py` (DEPRECATED)
Original verification with WRONG B_□ formula from GOAL.MD. Found spurious violations. Superseded by `verify_B_bound_L4_corrected.py`.

## Run order
1. `derive_B_formula.py` — establishes the correct formula
2. `verify_B_bound_L4_corrected.py` — main numerical results
3. `perturbation_analysis.py` — local analysis at Q=I
4. `uniform_config_proof.py` — analytical proof for special case
