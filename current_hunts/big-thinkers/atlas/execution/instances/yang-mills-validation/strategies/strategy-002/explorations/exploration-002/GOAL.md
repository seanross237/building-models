# Exploration 002: Path D — Direct SU(2) Hessian Bound

## Mission Context

We are repairing a proof gap in a mass gap result for SU(2) Yang-Mills at β < 1/6. The proof uses the Bakry-Émery framework. The gap is that the formula HessS(v,v) = (β/(2N)) Σ|B□(Q,v)|² is NOT an identity for Q ≠ I, but we need it as an INEQUALITY:

> HessS(v,v) ≤ (β/(2N)) Σ|B□(Q,v)|² for the direction v that maximizes HessS

Equivalently: λ_max(H_actual(Q)) ≤ λ_max(H_formula(Q)) for all Q.

**Prior exploration (E001) confirmed this inequality holds numerically for ~300 configs with max non-flat ratio r = 0.981.** The key mechanism: v_top(H_actual)^T · C(Q) · v_top > 0 always, where C = H_formula - H_actual is the curvature correction.

## Your Task: Compute the Actual Hessian Analytically and Bound It

The B² formula gives M(Q) = Σ B□ᵀ B□ but the actual Hessian of the Wilson action is H(Q) = M(Q) - C(Q). **Your job is to compute C(Q) analytically for a single plaquette and determine whether the resulting bound can be proved.**

### Step 1: The Second Derivative of Re Tr(U□) for a Single Plaquette

Consider a plaquette □ with edges e₁, e₂, e₃, e₄ (e₃, e₄ traversed backward). The plaquette holonomy is:

U□ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹ Q_{e₄}⁻¹

Perturb link eₖ: Q_{eₖ} → exp(t·vₖ) Q_{eₖ} where vₖ ∈ su(2).

**Compute d²/dt² Re Tr(U□(t))|_{t=0} EXACTLY.** This should decompose into:
- A "w² · U□" term: Re Tr(w² · U□) where w = Σₖ sₖ Ad_{Pₖ}(vₖ) is the covariant sum
- Possible "cross terms" involving derivatives of the partial holonomies Pₖ

**The critical question is whether there are cross terms beyond Re Tr(w² U□).** If d²/dt² Re Tr(U□) = Re Tr(w² U□), then C(Q) = 0 and the formula IS an identity. If there are additional terms, those terms ARE C(Q).

### Step 2: SU(2) Simplification

For SU(2): if w ∈ su(2), then w² = -(|w|²/4)I where |w|² = -2 Tr(w²).

So Re Tr(w² U□) = -(|w|²/4) Re Tr(U□) = -(|w|²/2) cos θ where cos θ = Re Tr(U□)/2.

**If d²/dt² Re Tr(U□) = Re Tr(w² U□) (no cross terms):**
Then HessS(v,v) = (β/4) Σ□ |w□|² cos θ□ for a single perturbation direction.
And |w□|² = |Σₖ sₖ Ad_{Pₖ}(vₖ)|² ≤ (Σ|vₖ|)² ≤ 4Σ|vₖ|² by Cauchy-Schwarz (since Ad is an isometry for SU(2)).

**If there ARE cross terms:**
Identify them explicitly. Can they be bounded? Do they make HessS larger or smaller than the formula predicts?

### Step 3: Numerical Verification

For EVERY algebraic step, verify numerically on L=2, d=4 with β=1.0:

1. **Single plaquette test:** Pick one plaquette. Compute d²/dt² Re Tr(U□) by finite differences (h=1e-4, central differences). Compare to:
   - Your analytical formula
   - The w² · U□ term alone
   - The cross terms (if any)
   Do this for 5 random Q configurations and 3 random v directions each.

2. **Full Hessian test:** Build the full 192×192 H_actual (FD) and your analytical formula. Compare eigenvalues. They should match to O(h²).

3. **If cross terms exist:** Build the 192×192 matrix of JUST the cross terms. What is its spectrum? Is it positive-definite, negative-definite, or indefinite?

### Step 4: Attempt the Bound

Based on what Steps 1-3 reveal:

**Case A (no cross terms):** Write the complete proof. HessS = (β/4) Σ□ cos(θ□) |w□|². Since cos θ ≤ 1, this gives HessS ≤ (β/4) Σ□ |w□|². Then CS gives |w□|² ≤ 4Σ|v_e|², link counting gives 2(d-1) plaquettes per link, so HessS ≤ 4(d-1)β/2 · |v|² = 2(d-1)β |v|². For N=2: threshold is β < N/(4(d-1)) = 1/(2(d-1)).

Wait — check: is this consistent with β < 1/6 for d=4? 1/(2·3) = 1/6. Yes!

**Case B (cross terms exist but are bounded):** Write the bound on the cross terms and determine the final threshold.

**Case C (cross terms are unbounded):** Characterize the obstruction. What exactly prevents the proof?

## Conventions (MANDATORY)

- SU(2): N = 2, generators Tₐ = iσₐ/2 (a = 1,2,3)
- Inner product: ⟨X,Y⟩ = -2 Tr(XY), so |Tₐ|² = 1
- Wilson action: S(Q) = -(β/N) Σ_□ Re Tr(U□) = -(β/2) Σ_□ Re Tr(U□)
- LEFT perturbation: Q → exp(t·v) · Q (SZZ convention)
- B□ formula (LEFT, ADJOINT): B□(v) = v₁ + Ad_{Q₁}(v₂) - Ad_{Q₁Q₂Q₃⁻¹}(v₃) - Ad_{U□}(v₄)
  where Ad_Q(v) = QvQ⁻¹ (NOT Qv)
- At Q = I: H_actual = H_formula, λ_max = 4β

## Success Criteria

- **Full success:** Complete proof that HessS(v,v) ≤ (const) · |v|² with const ≤ 4(d-1)β/N
- **Partial success:** Analytical formula for H_actual with all cross terms identified and verified; clear statement of what remains to prove
- **Failure:** Identification of cross terms that cannot be bounded (with numerical evidence)

## Failure Criteria

- If your analytical formula doesn't match FD at Q ≠ I, there's a derivation error — stop and debug
- If eigenvalues at Q = I ≠ 4β, there's a convention error — stop and fix

## Output

Write REPORT.md incrementally (after each step). Include all derivations. Put code in code/ subdirectory. Write REPORT-SUMMARY.md when done (≤30 lines).
