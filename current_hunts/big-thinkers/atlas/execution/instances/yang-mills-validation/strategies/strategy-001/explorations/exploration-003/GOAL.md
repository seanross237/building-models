# Exploration 003: B-square Formula and Convention Verification

## Mission Context

A prior research program proved a mass gap for lattice SU(2) Yang-Mills at β < 1/6. During their work, they discovered and corrected an error in the B_□ (B-square) formula — the key object in the Wilson action Hessian. Your job is to verify the corrected formula is indeed correct, and that the conventions are consistent throughout the proof chain.

Convention errors are the highest-risk failure mode. This exploration is specifically designed to catch them.

## Goal

Independently derive and numerically verify the B_□ formula for the Wilson action Hessian, with particular attention to the parallel transport conventions for backward edges. Then verify that the eigenvalue structure at Q=I is consistent with the claimed H_norm = 1/12.

## Convention Reference (use throughout)

**SZZ convention (arXiv:2204.12737):**
- Action: S(Q) = −(β/N) Σ_□ Re Tr(U_□), where N=2 for SU(2)
- Inner product: ⟨A,B⟩ = −2 Re Tr(AB), |A|² = −2 Tr(A²)
- Generators: τ_a = iσ_a/2, so |τ_a|² = 1
- Plaquette: U_{x,μν} = Q_{x,μ} Q_{x+ê_μ,ν} Q_{x+ê_ν,μ}⁻¹ Q_{x,ν}⁻¹

**Expected results under this convention:**
- λ_max(Hessian) at Q=I = 4β (NOT 8β — if you get 8β, you're missing the 1/N factor)
- H_norm at Q=I = 4β/(48β) = 1/12

## Staged Tasks

### Stage 0: Derive the Hessian from Scratch
For a single plaquette □ = (x,μ,ν) with edges:
- e₁ = (x, μ) — forward, from x to x+ê_μ
- e₂ = (x+ê_μ, ν) — forward, from x+ê_μ to x+ê_μ+ê_ν
- e₃ = (x+ê_ν, μ) — backward (traversed as Q⁻¹), from x+ê_ν+ê_μ to x+ê_ν
- e₄ = (x, ν) — backward (traversed as Q⁻¹), from x+ê_ν to x

The plaquette holonomy is: U_□ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹ Q_{e₄}⁻¹

Now perturb Q_e → exp(t·v_e) Q_e for tangent vectors v_e ∈ su(N). Compute:

d²/dt² [−(β/N) Re Tr(U_□(t))] |_{t=0}

This should give (β/(2N)) |B_□(Q,v)|² for some B_□ that is linear in v.

**The claimed correct B_□ formula is:**
B_□(Q,v) = v_{e₁} + Ad_{Q_{e₁}}(v_{e₂}) − Ad_{Q_{e₁}Q_{e₂}Q_{e₃}⁻¹}(v_{e₃}) − Ad_{U_□}(v_{e₄})

where the parallel transport for each edge is:
- Edge e₁: no transport (identity)
- Edge e₂: transport by Q_{e₁} (partial holonomy from start to e₂)
- Edge e₃: transport by Q_{e₁}Q_{e₂}Q_{e₃}⁻¹ (partial holonomy through e₁, e₂, then e₃ backward — includes e₃'s own link)
- Edge e₄: transport by U_□ = Q_{e₁}Q_{e₂}Q_{e₃}⁻¹Q_{e₄}⁻¹ (full holonomy — includes e₄'s own link)

**Critical detail about backward edges:** For backward edges (e₃, e₄), the parallel transport includes the edge's own link. This was the error in the prior mission's original formula — they initially used Q_{e₁}Q_{e₂} for e₃ (without Q_{e₃}⁻¹) and Q_{e₁}Q_{e₂}Q_{e₃}⁻¹ for e₄ (without Q_{e₄}⁻¹).

### Stage 1: Numerical Verification of B_□ Formula
On a small lattice (L=2, d=4, SU(2)):

1. Set up a random configuration Q with each Q_e ∈ SU(2)
2. Pick a specific plaquette □
3. Compute B_□(Q,v) analytically using the formula above for a random tangent vector v
4. Compute the Hessian d²/dt² [−(β/N) Re Tr(U_□(t))] |_{t=0} numerically using finite differences (h = 10⁻⁵)
5. Compare: the numerical Hessian should equal (β/(2N)) |B_□(Q,v)|²
6. **Repeat for at least 5 different plaquettes and 5 different Q configurations**
7. **Also test with Q=I** — at Q=I, the formula simplifies to B_□(I,v) = v₁ + v₂ − v₃ − v₄ (discrete curl). Verify this.

Report the maximum discrepancy. It should be < 10⁻⁸.

### Stage 2: Structural Properties of B_□
Verify these claimed structural properties:

1. **B_□ B_□^T = 4I_{N²−1} for any Q and any plaquette**: This means the row space of B_□ always has the same structure. Verify numerically for 5 random (Q, □) pairs.

2. **Per-plaquette M_□ = B_□^T B_□ has eigenvalues {4,4,4,0,...,0}**: This is the per-plaquette Hessian matrix (12×12 for d=4, one plaquette touches 4 links × 3 generators). Verify.

3. **Tr(M(Q)) = 4 × n_plaquettes × (N²−1) independent of Q**: The total trace is Q-independent. Verify by computing Tr(M(Q)) for Q=I and 5 random Q.

### Stage 3: Full Hessian at Q=I — Eigenvalue Check
Build the full 192×192 Hessian matrix at Q=I on L=2, d=4:

1. Compute all eigenvalues. The claimed spectrum is:
   - 0 with multiplicity 57
   - β with multiplicity 36
   - 2β with multiplicity 54
   - 3β with multiplicity 36
   - 4β with multiplicity 9
   Total: 57+36+54+36+9 = 192 ✓

2. Verify λ_max = 4β with multiplicity 9 (= 3 K-eigenvalues × 3 generators)

3. Verify the staggered mode v_{x,μ,a} = (−1)^{|x|+μ} δ_{a,1} / ‖v‖ is an eigenvector with eigenvalue 4β:
   - Compute H·v_stag
   - Compare with 4β·v_stag
   - Report the residual ‖H·v_stag − 4β·v_stag‖

### Stage 4: Convention Chain Verification
Trace the full proof chain with explicit conventions:

1. SZZ Theorem 1.3: Mass gap if HessS(v,v) < (N/2)|v|² for all v
2. HessS(v,v) = (β/(2N)) v^T M(Q) v where M(Q) = Σ_□ B_□^T B_□
3. So condition becomes: (β/(2N)) λ_max(M(Q)) < N/2, i.e., β λ_max(M(Q)) < N²
4. Triangle inequality: λ_max(M(Q)) ≤ ??? (derive this number)
5. Threshold: β < N²/λ_max_bound

What threshold do you get? Is it 1/6?

**The critical check:** Does the factor 48 in "H_norm = λ_max/48" come from 8(d−1)N = 8×3×2 = 48? Or from 16(d−1) = 48? Or from some other combination? State exactly where each factor comes from.

### Stage 5: Random Q Hessian Check
For 5 random Haar-distributed Q configurations on L=2:

1. Build the full 192×192 Hessian
2. Compute λ_max
3. Compute H_norm = λ_max / (48β)
4. Verify H_norm ≤ 1/8 (the proved bound) and check if H_norm ≤ 1/12 (the conjectured bound)

## Success Criteria
- [ ] B_□ formula verified by finite differences to < 10⁻⁸ on at least 25 (Q, □, v) triples
- [ ] Structural properties (B·B^T = 4I, trace conservation) verified numerically
- [ ] Full eigenvalue spectrum at Q=I matches claimed values
- [ ] Staggered mode verified as eigenvector with eigenvalue 4β
- [ ] Convention chain explicitly traced with every factor accounted for
- [ ] H_norm ≤ 1/8 verified for 5 random Q

## Failure Criteria
- B_□ formula disagrees with finite differences → STOP, derive the correct formula, report the discrepancy
- λ_max ≠ 4β at Q=I → convention error, diagnose and report
- Any factor discrepancy in the proof chain → this is the most important finding

## What to Write
Write REPORT.md and REPORT-SUMMARY.md in your exploration directory. Include all code in a `code/` subdirectory. Every numerical result must have runnable code that reproduces it.
