# Exploration 007 Summary: Bound Non-Staggered Eigenvalues of M(Q)

## Goal
Prove that all eigenvalues of M(Q) = ∑B_p^T B_p ≤ 16 for the full 192×192 matrix on L=2, d=4, covering non-staggered modes.

## Outcome: CRITICAL NEGATIVE — Bound is FALSE

**The claim λ_max(M(Q)) ≤ 16 for all Q is FALSE.** Edge-by-edge gradient ascent found Q with λ_max ≈ 16.08 (0.5% above 16), reproduced across 5 independent trials. The violation is small but definitive.

However, for random gauge fields (2000+ configs), λ_max never exceeded 14.64. Violations require targeted optimization.

## Verification Scorecard
- **[VERIFIED]:** 3 claims (M(I) eigenstructure, uniform Q Fourier block analysis ≤ 16, B-field linearization formula correctness via numerical differentiation)
- **[COMPUTED]:** 8 claims (random Q eigenvalues, gradient ascent violations, L=3/L=4 bounds, R|_nonstag analysis, Tr(M²) analysis, M ≠ Hessian, top eigenvector composition)
- **[CONJECTURED]:** 0

## Key Takeaway

The operator M(Q) = ∑B_p^T B_p (covariant curl squared) does NOT satisfy λ_max ≤ 16 universally. The per-vertex staggered proof (F_x ≤ 16‖T‖²) is correct but only covers the 9D staggered subspace. Non-staggered eigenvalues can exceed 16 under optimization.

**Crucially:** M(Q) is NOT the Hessian of the Wilson action. The Hessian includes a curvature correction term C(Q) such that H(Q) = M(Q) − C(Q). The mass gap argument may need the Hessian bound rather than the M(Q) bound.

## Proof Gaps Identified
1. **λ_max ≤ 16 is false for M(Q) = B^T B.** The entire proof strategy based on bounding this operator at 16 needs revision.
2. **M(Q) ≠ Hessian distinction.** Previous explorations conflated the B-field norm squared with the Wilson action Hessian. The correct operator for the mass gap may be the Hessian, which has much smaller eigenvalues.
3. **What IS the correct bound?** For optimized Q, λ_max ≈ 16.08. The true supremum is unknown but appears close to 16.

## Computations Identified
- Determine the true sup_Q λ_max(M(Q)): is it exactly 16 + ε, or does it grow unboundedly?
- Derive and bound the correct Wilson action Hessian H(Q)
- Check whether the SZZ approach uses M(Q) or H(Q) — this determines whether the bound failure matters

## Unexpected Findings
- The two different B-field formulations (left vs right perturbation convention) give **identical M(Q) matrices** — a beautiful manifestation of gauge invariance
- For uniform Q (flat connections), λ_max = 16 exactly for ALL rotation angles, proved analytically via Fourier analysis and K_4 graph Laplacian theory
- The curvature correction Tr(C(Q)) ≈ −1148 is LARGE and negative, showing M(Q) dramatically overestimates the Hessian
