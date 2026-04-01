# Exploration 002 Summary: Wilson Action Hessian Formula

## Goal
Derive the explicit analytical formula for the Hessian of the lattice Wilson action for SU(2), verify it, and characterize the correction C(Q) = M(Q) - (2N/β)HessS(Q).

## What was tried
Derived the Hessian by Taylor-expanding the plaquette holonomy under Q_e → Q_e exp(Σ c_a iσ_a). Identified a key SU(2) identity (w² = -|c|²I) that trivializes the self-terms. Verified the formula against finite differences on 12 configurations. Analyzed the correction structure and scanned for the max eigenvalue bound via random sampling and gradient ascent.

## Outcome: SUCCESS

**The formula is:**
- Self-terms: H[(e,a),(e,b)] = (β/N) δ_{ab} Σ_{□∋e} Re Tr(U_□) — diagonal in color, proportional to the sum of plaquette traces.
- Cross-terms: H[(ep,a),(eq,b)] = -(β/N) sp sq Re Tr(Lp iσa mid iσb Rq) — involves transported basis elements.

**Key findings:**
1. At flat connections (U_□ = I): HessS = (β/2N)M exactly, C = 0.
2. The self-term correction C_self ≥ 0 always (from Re Tr(U) ≤ 2 for SU(2)).
3. The total correction C is NOT PSD — but the max eigenvalue of HessS is still bounded.
4. λ_max(HessS(Q)) ≤ 4d (in iσ_a basis), achieved at flat connections. Gradient ascent in d=4 reached only 85% of the bound.

## Verification scorecard
- 4 VERIFIED (key identity, self-term formula, flat-connection equality, C_self ≥ 0)
- 2 COMPUTED (FD cross-check, eigenvalue bound scan)
- 1 CONJECTURED (global max eigenvalue bound ≤ 4d)

## Key takeaway
The Hessian self-terms are suppressed by Re Tr(U_□)/2 away from flat connections, and cross-terms cannot compensate enough. The flat connection maximizes the Hessian. This supports the revised conjecture λ_max(HessS) ≤ (β/2N)×4d for all Q.

## Proof gaps
- No analytical proof that cross-terms cannot amplify the eigenvalue beyond the flat bound. The cross-term kernel has bounded operator norm but the bound isn't tight enough.
- The bound ≤ 4d is numerically convincing but unproven. Proving it likely requires Fourier analysis of the Hessian at flat connections plus a perturbative argument.

## Unexpected findings
- E001's claim that HessS ≠ (β/2N)M at Q=iσ₃ appears to be WRONG — both Q=I and Q=iσ₃ are flat connections where the equality is exact. E001 may have had a normalization error.
- The Hessian matrix requires anticommutator {iσ_a,iσ_b}/2 = -δ_{ab}I for self-terms, not the product — a subtle but critical distinction between the quadratic form and the bilinear Hessian.

## Computations for later
- Prove λ_max(HessS(Q)) ≤ 4d analytically, perhaps via convexity arguments or spectral analysis of the flat Hessian
- Extend to SU(N) for N > 2 (the identity w² = -|c|²I is specific to SU(2))
- Check whether the bound is tight for larger lattices (L > 2)
