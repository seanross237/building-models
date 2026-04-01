# Exploration 003 Code

All scripts use `python3` with numpy, scipy.

## Scripts

1. **numerical_verification.py** — Initial Monte Carlo tests for LEMMA_D, LEMMA_RDR, per-plaquette bounds, eigenvalue structure.
2. **minimizer_analysis.py** — Adversarial optimization to find LEMMA_D counterexample. Nelder-Mead on min eigenvalue of 9×9 projected form.
3. **verify_minimizer.py** — Cross-checks the LEMMA_D counterexample: matrix vs direct computation, SO(3) verification, per-plaquette breakdown.
4. **total_gap_investigation.py** — Tests sum_S = LEMMA_D + LEMMA_RDR and total_gap with adversarial optimization. Finds both LEMMA_D and LEMMA_RDR are individually false.
5. **sumS_algebraic.py** — Algebraic structure: VCBL decomposition at R=I, remainder analysis, identity D^T = U^T R_mu.
6. **vcbl_remainder.py** — Tests whether VCBL(-I) remainder is PSD on constraint subspace (it is NOT — -32).
7. **sumS_direct_proof.py** — Taylor expansion, plaquette grouping, Cholesky test, budget/cross ratio.
8. **zero_set_analysis.py** — Characterizes when sum_S = 0: D=I gives zero for any R. Null eigenvector analysis.

## Key result
Run `verify_minimizer.py` to reproduce the LEMMA_D counterexample (min = -2.12).
Run `zero_set_analysis.py` to verify sum_S >= 0 (200 optimizations all → 0).
