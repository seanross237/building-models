# Exploration 003 Summary: Prove the Hessian Eigenvalue Bound

## Goal
Prove λ_max(HessS(Q)) ≤ 4d for all Q. Three proof approaches + SZZ threshold verification.

## Outcome: CONDITIONAL PROOF — one lemma away

Proof via D+C decomposition: H = D(self-term) + C(cross-term). D_max ≤ 2(d-1) [PROVED]. λ_max(C_flat) = 2(d+1) [VERIFIED]. Sum = 4d ✓. λ_max(C(Q)) ≤ 2(d+1) for ALL tested configs [COMPUTED, 200-1000 per d]. MISSING: proof of "cross-term decoherence lemma" (||C(Q)|| ≤ ||C_flat||).

Key algebraic result [VERIFIED]: Cross-term kernel ||F_{ab}||_op = 2 EXACTLY for all SU(2) — proved via û·iσ ∈ SU(2) ⟹ |Tr(UMVN)| ≤ 2. Gershgorin and per-plaquette approaches both FAIL (too loose by 50%). Normalization: GOAL's 4d·(β/N) wrong by factor 2; correct flat eigenvalue is 4d in iσ_a coords.

## Verification Scorecard
- **VERIFIED: 4** (Fourier formula, ||F||≤2 proof, self-term monotonicity, SZZ normalization)
- **COMPUTED: 5** (D+C bounds, eigenvalue surveys, perturbation, |λ_min|≤4d, proof failures)
- **CONJECTURED: 1** (cross-term decoherence: ||C(Q)|| ≤ ||C_flat||)

## Key Takeaway
The proof is 90% complete. The missing step: at flat, all cross-term 3×3 color kernels equal -2I₃ (maximally coherent); at non-flat they rotate independently, reducing ||C||. If proved, gives mass gap β < 1/8 (d=4), 1.5× over SZZ.

## Proof Gaps
- **Decoherence lemma**: C_flat = A⊗I₃ maximizes ||C||. Possible via SO(3)-averaging or matrix concentration.

## Unexpected Findings
- ||F||_op = 2 exactly for ALL SU(2) (algebraic invariant); |λ_min| ≈ 4d/2 ≪ 4d (asymmetric spectrum)

## Computations Identified
- Prove decoherence lemma (Schur product theorem? matrix concentration?)
- Tighter |λ_min| bound: if ≤ 2d (matching numerics), mass gap improves to β < 1/4
