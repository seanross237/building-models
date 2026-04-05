# Exploration 002: Derive the Wilson Action Hessian Analytically

## Mission Context

We are proving a mass gap bound for lattice SU(2) Yang-Mills on the d=4 hypercubic torus. The previous exploration (E001) made a critical discovery:

**Conjecture 1 (λ_max(M(Q)) ≤ 16) is FALSE.** At Q_e = iσ₃ (all links), λ_max(M(Q)) = 24. But the Hessian of the Wilson action HessS is NOT equal to (β/2N)M(Q) — there's a large curvature correction that suppresses the eigenvalues. At Q = iσ₃, λ_max(HessS) = 4.0 = (β/2N)×16, even though (β/2N)×λ_max(M) = 6.0.

**The revised conjecture is: λ_max(HessS(Q)) ≤ (β/2N) × 4d for all Q ∈ SU(2)^E.**

To prove this, we need the explicit formula for HessS. Your job: derive it.

## Definitions

**Wilson action:** S(Q) = −(β/N) Σ_□ Re Tr(U_□) where U_□ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹ Q_{e₄}⁻¹ is the plaquette holonomy.

**Parameters:** N = 2 (SU(2)), d = 4, β = 1.0 for testing.

**Tangent vectors:** v ∈ (su(2))^{|E|} ≅ ℝ^{3|E|}. For each edge e, v_e ∈ su(2) ≅ ℝ³.

**Perturbation:** Q_e → Q_e exp(ε v_e) where v_e ∈ su(2).

**Hessian:** HessS(v, w; Q) = d²/dε dδ S(Q_e exp(ε v_e + δ w_e)) evaluated at ε=δ=0.

**M(Q) operator:** Defined by v^T M(Q) v = Σ_□ |B_□(Q, v)|² where B_□(Q, v) is the parallel-transported curl:
B_□(Q,v) = v_{e₁} + Ad_{Q_{e₁}}(v_{e₂}) − Ad_{Q_{e₁}Q_{e₂}Q_{e₃}⁻¹}(v_{e₃}) − Ad_{U_□}(v_{e₄})

**Adjoint representation:** Ad_Q(v) = QvQ⁻¹, giving a 3×3 SO(3) matrix for each Q ∈ SU(2).

## Your Tasks

### Stage 1: Derive HessS for a Single Plaquette

Consider one plaquette □ with edges (e₁, e₂, e₃, e₄) traversed in order, with holonomy U_□ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹ Q_{e₄}⁻¹.

The contribution to S from this plaquette is: s_□(Q) = −(β/N) Re Tr(U_□).

Compute HessS_□(v, v; Q) = d²/dε² s_□(Q_e exp(ε v_e))|_{ε=0}.

You need to differentiate Re Tr(U_□) twice. When perturbing edge eᵢ by Q_{eᵢ} → Q_{eᵢ} exp(ε v_{eᵢ}):
- First derivative involves one insertion of v_{eᵢ} into U_□
- Second derivative involves: (a) two insertions from the same edge, (b) one insertion each from two different edges

**Write the result explicitly.** It should have the form:
HessS_□(v, v) = (β/2N) [Σ_□ |B_□(Q,v)|²] + correction terms involving Re Tr(U_□ ...) and the link variables.

The correction terms are the curvature correction C(Q). Identify them.

### Stage 2: Verify Analytically at Q = I

At Q = I: all U_□ = I, all Ad = I₃.

Compute HessS(v, v; I) using your formula. It should give (β/2N) × v^T M(I) v.
- If there's a correction: compute C(I). It should be zero (since HessS = (β/2N)M at Q=I, which is known).
- If the correction is NOT zero at Q=I, your derivation has an error.

### Stage 3: Verify Analytically at Q = iσ₃

At Q_e = iσ₃ for all edges:
- U_□ = (iσ₃)⁴ = I (flat connection)
- Ad_{iσ₃} = diag(−1, −1, +1)

Compute HessS(v, v; iσ₃) using your formula. The maximum should be 4.0 (from E001's finite-difference computation), not 6.0 = (β/2N)×24.

Identify which terms in the correction are responsible for suppressing the eigenvalue from 6.0 to 4.0.

### Stage 4: Numerical Cross-Check

Implement your analytical HessS formula in Python. For 10 random Q configurations:
1. Compute HessS analytically (from your formula)
2. Compute HessS by finite differences of S(Q)
3. Compare element-by-element. Relative error should be < 10⁻⁶.

If they don't match, your derivation has an error. Debug it.

### Stage 5: Structure of the Correction

Once you have the verified formula, characterize C(Q) = M(Q) - (2N/β) HessS(Q):
1. What is C(Q) at Q = I? (Should be 0)
2. What is C(Q) at Q = iσ₃? (Should suppress the 24 eigenvalue to 16 in the Hessian)
3. Is C(Q) positive semidefinite? (If so, HessS ≤ (β/2N)M trivially)
4. What is the spectrum of C(Q) for random Q?
5. Can you express C(Q) in a simple closed form?

**Key question:** Is HessS(v,v; Q) expressible as (β/2N) Σ_□ [|B_□(Q,v)|² − something_positive]? If so, the Hessian bound follows from the M(Q) bound plus the correction.

Wait — M(Q) doesn't satisfy the bound (it reaches 24). So we need HessS directly. The question is: what structural property of HessS keeps it bounded?

## Success Criteria

- Explicit formula for HessS(v, v; Q) in terms of link variables Q_e and tangent vectors v_e
- Formula verified at Q = I (matches known Hessian) and Q = iσ₃ (gives max eigenvalue 4.0)
- Numerical cross-check against finite differences for 10+ random configs
- Clear characterization of C(Q) = M(Q) - (2N/β)HessS(Q)
- Insight into WHY the Hessian stays bounded (structural property)

## Failure Criteria

- Cannot derive the formula (stuck on the differentiation)
- Formula doesn't match finite differences (derivation error that can't be resolved)

## Context from E001

E001 found numerically:
- Diagonal blocks of HessS: HessS_{ee} ∝ Σ_{□∋e} Re Tr(U_□) × I₃ — this is different from M_{ee} which is proportional to the number of plaquettes containing e
- Off-diagonal blocks involve Im Tr(σ_a U_□) — color mixing
- At random Q, the Hessian is much smaller than (β/2N)M (ratios 0.02–0.09)
- At Q = iσ₃ (flat connection), the Hessian max is exactly 4.0 = (β/2N)×16

This suggests the correction is large and has a definite structure related to plaquette holonomies.

## Output

Write your findings to REPORT.md (≤ 250 lines) and REPORT-SUMMARY.md (≤ 30 lines) in your exploration directory. Write incrementally after each stage.
