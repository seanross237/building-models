# Exploration 002 Summary: Path D — Direct SU(2) Hessian Computation

## Goal
Compute the actual second derivative d²/dt² Re Tr(U□) analytically for SU(2), identify all cross terms beyond the w²·U term, and verify numerically on L=2, d=4.

## Outcome: **PARTIAL SUCCESS — Formula complete, bound not proved**

The complete analytical formula for the Wilson action Hessian was derived and verified. The cross terms are COMMUTATOR terms with a clean SU(2) cross-product structure. However, the inequality H_actual ≤ H_formula cannot be proved by simple algebraic means because the correction matrix C is NOT positive semi-definite.

## Key Results

**The exact formula (SU(2)):**

d²/dt² Re Tr(U□) = -(|w|²/2)cos(θ/2) + (1/2)L⃗·b⃗

where L⃗ = Σ_{i<j} w⃗ᵢ × w⃗ⱼ and b⃗ is the su(2) part of U□.

**The correction matrix decomposes exactly as C = C_curv + C_comm:**
- C_curv = (β/4)(1-cos(θ/2)) BᵀB — PSD (curvature bonus)
- C_comm — indefinite (commutator terms)
- C itself has 41 negative eigenvalues (not PSD)

**But λ_max(H_actual) ≤ λ_max(H_formula) holds for all 50+ configs tested**, with ratio 0.61-0.74.

## Verification Scorecard
- [VERIFIED]: 11 claims (formula, decomposition, eigenvalues, flat check)
- [COMPUTED]: 5 claims (multi-config tests, per-plaquette analysis)
- [CONJECTURED]: 3 claims (proof strategies)

## Key Takeaway
The B² formula inequality HessS ≤ (β/4)Σ|B□|² is **NOT a matrix inequality** — it fails in ~20% of directions. But it holds at the top eigenvalue, which is what's needed. Proving this requires understanding why the top eigenspace of H_actual always sees positive C. The curvature bonus barely compensates the commutator (ratio ≈ 1.10 at v_top).

## Proof Gaps Identified
1. **C is not PSD**: Cannot use simple algebraic bound C(v,v) ≥ 0 for all v
2. **Per-plaquette bound fails**: Cannot prove the inequality plaquette-by-plaquette
3. **The eigenspace alignment mechanism**: v_top^T C v_top > 0 holds but lacks a proof

## Unexpected Findings
- Same-link, different-component entries of the Hessian are EXACTLY zero by su(2) anti-commutation (wₖₐwₖᵦ + wₖᵦwₖₐ = 0 for orthogonal generators)
- The commutator terms can dominate the w² term by factors up to 60×
- The eigenvalue inequality holds eigenvalue-by-eigenvalue (stronger than needed)

## Computations Identified
1. Test whether the direct bound H_actual ≤ 4β·I holds (would give β < 1/2)
2. Analyze the lattice cancellation structure of commutator terms
3. Check if a perturbative expansion near flat connections reveals the mechanism
