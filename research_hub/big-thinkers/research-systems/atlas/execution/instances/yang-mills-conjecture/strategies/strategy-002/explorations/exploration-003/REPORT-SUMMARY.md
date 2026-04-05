# Exploration 003 Summary

## Goal
Prove LEMMA_D >= 0 and LEMMA_RDR >= 0 (or their sum) to close the 9D eigenspace gap.

## Outcome: Critical Discovery — Individual Lemmas are FALSE

**LEMMA_D is FALSE** (min eigenvalue = -2.13, verified to machine precision). **LEMMA_RDR is also FALSE** (min eigenvalue = -1.45). Both have genuine SO(3) counterexamples found via adversarial optimization. The 200K random tests from E002 missed these because uniform sampling on SO(3)^{10} doesn't hit the adversarial corners of the 30D parameter space.

**However, sum_S = LEMMA_D + LEMMA_RDR appears non-negative** — 200 independent optimizations ALL converge to min eigenvalue = 0 (tight). The individual lemmas compensate each other: when LEMMA_D is very negative, LEMMA_RDR is sufficiently positive.

## Verification Scorecard
- 2 VERIFIED (counterexamples), 1 VERIFIED (VCBL at R=I), ~10 COMPUTED, 1 CONJECTURED (sum_S >= 0)

## Key Structural Findings
1. **D = I gives sum_S = 0 for ANY R** — the zero set is parameterized by the R matrices alone when all D = I.
2. **At R = I, sum_S = 2·sum VCBL(D,D,-I,...) >= 0** — proved via Cauchy-Schwarz + AM-GM.
3. **Per-plaquette VCBL cannot work** for general R — the cross term is rank 3 but VCBL products are rank ≤ 2 (fundamental obstruction).
4. **The bound is tight** (sum_S touches 0) so any proof must be sharp — no epsilon room.

## Key Takeaway
The proof decomposition sum_S = LEMMA_D + LEMMA_RDR was too aggressive. The correct target is **sum_S >= 0 directly**. Neither piece is individually non-negative, but they always compensate. The next exploration should attempt to prove sum_S >= 0 using the combined cross term structure: U^T R_mu + U R_nu^T − 2I.

## Proof Gaps Identified
- **Need**: algebraic proof that the 9×9 projected matrix P^T M_{sum_S} P is PSD for all R, D in SO(3)
- **Available tools**: VCBL works at R=I; D=I gives trivial zero; Hessian is positive at Q=I
- **Missing**: a global argument connecting these local results, or a new decomposition that handles the rank-3 cross term

## Computations for Next Steps
1. **Prove sum_S(D=I) >= 0 algebraically** — this is a simplified problem (only R dependence, 12 parameters). The 9×9 matrix at D=I has off-diagonal blocks -(I-R_mu R_nu^T) and diagonal blocks involving sums of (I-R_mu). Its minimum eigenvalue is exactly 0.
2. **Interpolation approach**: Show sum_S >= 0 by interpolating between D=I (zero) and general D (positive Hessian contributes), using sum_S = 0 + O(||D-I||^2) near D=I.
3. **SDP certificate**: Numerically compute an SOS/SDP certificate for sum_S >= 0 (may need specialized tools for SO(3) parametrization).
