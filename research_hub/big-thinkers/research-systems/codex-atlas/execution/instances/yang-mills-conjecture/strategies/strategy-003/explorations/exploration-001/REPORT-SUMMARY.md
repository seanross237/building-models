# Exploration 001 Summary

## Goal
Verify E007's counterexample (λ_max(M(Q)) ≈ 16.08) and clarify the SZZ Hessian relationship.

## Outcome: Conjecture 1 is FALSE, but the mass gap argument survives

**Conjecture 1 (λ_max(M(Q)) ≤ 16) is definitively false.** The clean counterexample Q_e = iσ₃ (all links) gives λ_max(M) = 24 exactly. This is a flat connection with Z₂ holonomy (-I around each torus cycle). Even random configs exceed 16 in 21% of cases.

**However, the Hessian of S is NOT (β/2N)M.** There is a large curvature correction. At Q = iσ₃, the full 192×192 Hessian (computed by finite differences) has λ_max = 4.0 = (β/2N)×16, even though (β/2N)M has λ_max = 6.0. The correction exactly compensates.

**The correct proof target is the Hessian, not M.** Numerical evidence suggests λ_max(HessS) ≤ (β/2N)×4d for all Q — verified at Q=I, Q=iσ₃, and random Q (where it's much smaller).

## Verification Scorecard
- **VERIFIED:** 5 (λ_max=16 at Q=I, λ_max=24 at Q=iσ₃, eigenvector construction, Hessian spectrum at iσ₃, gauge mode orthogonality)
- **COMPUTED:** 4 (1000-config random survey, gradient ascent, Stage 2 element comparison, staggered decomposition)
- **CONJECTURED:** 1 (λ_max(HessS) ≤ (β/2N)×4d universally)

## Key Takeaway
The E007 counterexample was real (correct formula), but it targets the wrong quantity. The mass gap argument needs the Hessian bound, not the M bound. The Hessian has a built-in curvature correction that tames M's large eigenvalues at non-trivial flat connections.

## Proof Gaps
- The exact formula for HessS in terms of M and curvature correction needs derivation (currently only numerically characterized)
- The revised conjecture λ_max(HessS) ≤ (β/2N)×4d needs proof — the mechanism is clear (curvature correction suppresses gauge-lifted modes) but not formalized

## Unexpected Findings
- sup λ_max(M) = 24 = 6d (not 4d=16), achieved at Z₂ flat connections
- The modes exceeding 16 in M are "gauge-lifted" modes: gauge zero-modes at Q=I that become physical at non-trivial flat connections, but remain in the Hessian nullspace
- At random Q: v^T HessS v / (β/2N) v^T M v ≈ 0.02–0.09, so the Hessian is far below (β/2N)M away from flat connections

## Computations Identified
- Analytical derivation of the curvature correction: HessS = (β/2N)[M(Q) - C(Q)] where C depends on Re Tr(U_□) and Im Tr(σ_a U_□)
- Test λ_max(HessS) ≤ 4 at more configurations (especially near saddle points of S)
- Prove the revised Hessian bound directly (may follow from the Bochner-Weitzenböck identity on the lattice)
