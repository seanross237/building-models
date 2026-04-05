# Step 2 Goal: H^1 Structure Exploitation — Three Branches

## Mission Context

**Mission:** Determine whether the Vasseur pressure exponent gap (β = 4/3, need β > 3/2) can be closed using H^1 structure of the pressure.

**What Step 0+1 established:**

1. **β = 4/3 is confirmed current** — unchanged since Vasseur 2007. No improvement in 19 years.
2. **β > 3/2 is the correct threshold** for full regularity (Vasseur's Conjecture 14).
3. **"Tran-Yu 2014" does not exist.** The correct reference is **Choi-Vasseur 2014** (arXiv:1105.1526) — three-way pressure decomposition P = P_{1,k} + P_{2,k} + P_3, Lemma 3.3.
4. **H^1 + De Giorgi is well-studied** by the Vasseur school since 2007. BUT the specific **H^1-BMO duality angle has NOT been tried**. This is the genuine novel angle.
5. **The bottleneck is DISTRIBUTED** across two constraints:
   - CZ ceiling: u ∈ L^{3,∞} → p ∈ L^{3/2,∞} (weak type only)
   - Far-field pressure has a FIXED CONSTANT coefficient, not controlled by U_k
6. **Local pressure is NOT the problem** — δ_local = 3/5 > 0, the recursion closes for local terms.
7. **Far-field pressure IS the sole obstruction** — any technique bounding ||p_far||_{L^∞(Q_k)} in terms of U_k would close the recursion.
8. **Bogovskii corrector is DEAD** — 2^{2k} compound growth, strictly worse than the original. Do NOT pursue localization via cutoffs.
9. **The Vasseur school moved to vorticity in 2021** (Vasseur-Yang, ARMA), implicitly suggesting H^1 pressure has hit its ceiling without a new idea.
10. **The measure exponent 1/10 is β-independent** (structural universality).

## Your Objective

Test three routes for converting H^1 pressure structure into improved De Giorgi estimates. Focus on the **far-field pressure** (not local — local already closes).

**CRITICAL CONTEXT:** H^1 is NOT a better L^p space. H^1 ⊂ L^1 ⊂ L^{4/3} in Lebesgue inclusion. The gain is structural: cancellation, atomic decomposition, and duality with BMO. The question is whether this structure can make the far-field pressure coefficient U_k-dependent (instead of fixed constant).

### Branch 2B: H^1-BMO duality (MOST PROMISING — do this first)

The key identity: for f ∈ H^1 and g ∈ BMO,
  |∫ f · g| ≤ C ||f||_{H^1} ||g||_{BMO}

This replaces the Hölder estimate |∫ f · g| ≤ ||f||_{4/3} ||g||_4 currently used for the pressure term.

**The critical question:** Are the Choi-Vasseur 2014 De Giorgi test functions ψ_k uniformly bounded in BMO?

**Tasks:**
1. Write ψ_k explicitly from Choi-Vasseur 2014 (arXiv:1105.1526, Lemma 3.3 and surrounding).
2. Estimate ||ψ_k||_{BMO}. Two sub-cases:
   - ψ_k is a cutoff of (|u| − C_k)_+ type → likely BMO-bounded
   - ψ_k involves Sobolev-type corrections → check whether corrections destroy BMO
3. If ||ψ_k||_{BMO} ≤ M uniformly, substitute H^1-BMO into the far-field pressure estimate. Does the fixed constant become U_k-dependent?
4. Check: does H^1-BMO duality bypass the Bogovskii problem? (H^1 functions have mean zero → localization may be cleaner.)

**Success criterion:** The substitution yields an effective pressure exponent β > 4/3 in the recursion, OR identifies a specific obstruction (ψ_k BMO norm blows up, or H^1-BMO gain is absorbed).

### Branch 2A: Interpolation route (likely insufficient — do only if 2B fails)

Analyze (H^1, L^{4/3})_{θ,q} interpolation spaces. Step 0+1 pre-assessment: pure L^p interpolation stays ≤ 4/3. But H^1 is strictly smaller than L^1, so the interpolation space might have additional structure exploitable by De Giorgi.

**Success criterion:** Find θ, q such that the interpolation space has a property exploitable by De Giorgi.

### Branch 2C: Atomic decomposition route (do only if 2B fails)

Every f ∈ H^1 decomposes as f = Σ λ_j a_j where atoms a_j have cancellation (mean zero) and L^2 control.

**Tasks:**
1. Decompose far-field pressure into H^1 atoms
2. Atoms at scales much larger than supp(φ_k) may contribute negligibly due to cancellation
3. Test: does the atomic decomposition provide scale-by-scale estimate better than bulk L^{4/3}?

**Success criterion:** Atomic decomposition gives better far-field bound than Hölder.

## Execution Order

1. Branch 2B first (most promising, the novel untried angle)
2. If 2B fails, run 2A and 2C
3. If all three fail, collect the three obstruction mechanisms — this IS the mission's main negative finding

## Kill Condition

If all three branches fail: document the three specific obstruction mechanisms explaining WHY H^1 structure cannot improve De Giorgi for NS. This is a valuable negative result ("Why H^1 doesn't help"). Proceed to Step 4 for synthesis and fractional NS sharpness test.

## Available Tools

- Python (numpy, scipy, sympy, mpmath)
- SageMath 10.8
- Lean 4 + Mathlib
- Web search for papers
- Prior exploration reports in ../step-001/explorations/

## Key References

- **Choi-Vasseur 2014** (arXiv:1105.1526) — THE baseline. Three-way decomposition, Lemma 3.3.
- **Vasseur 2007** — Original De Giorgi approach, Conjecture 14.
- **Caffarelli-Vasseur 2010** — Drift-diffusion (no pressure), De Giorgi reaches criticality.
- **CLMS 1993** (Coifman-Lions-Meyer-Semmes) — compensated compactness, Hardy space.
- Step 001 exploration-002 REPORT.md — full annotated inequality chain.

## Validation

- Function spaces specified precisely (Hardy H^1, BMO, Lebesgue, Lorentz, Besov)
- Every claim tagged: [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- The Choi-Vasseur 2014 construction must be faithfully reproduced, not paraphrased
- Partial results valued — "ψ_k is BMO but the gain is absorbed by term X" is a result
