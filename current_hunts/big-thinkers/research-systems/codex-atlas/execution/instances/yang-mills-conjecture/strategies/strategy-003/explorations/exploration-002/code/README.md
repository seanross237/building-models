# Code for Exploration 002

All scripts use Python 3 with numpy only (no scipy needed).

## Files

- `derive_hessian.py` — Initial derivation and single-plaquette verification. Tests the quadratic form against finite differences for Q=I, Q=iσ₃, and 10 random configs.
- `test_qI_detail.py` — Detailed normalization analysis at Q=I. Establishes that HessS uses the Killing norm -2Tr(XY) on su(2).
- `hessian_correct.py` — **Main file.** Contains the correct Hessian formula with symmetrized self-terms ({iσ_a,iσ_b}/2 = -δ_{ab}I). Full cross-check against finite differences (12 configs, max rel err < 1.4e-6). Also verifies eigenvalue bound at d=2,3,4.
- `stage4_crosscheck_v2.py` — Detailed element-by-element cross-check.
- `stage5_correction.py` — Analysis of correction C(Q) = M - (2N/β)HessS. Shows C_self ≥ 0 but C_cross not PSD. Gradient ascent verification of the bound.
- `closed_form_hessian.py` — Decomposition of Hessian into self/cross terms (older version, uses unsymmetrized formula).
- `random_q_test.py` — Tests with random Q showing C ≠ 0 in general.
- `bound_scan.py` — Scan for max eigenvalue across many configs and dimensions.

## Key result

Run `python hessian_correct.py` to verify the formula and bound.
