# Exploration 001: H^1-BMO Duality Route for Improving the Pressure Exponent

## Mission Context

We are investigating whether the Vasseur pressure exponent gap (β = 4/3, need β > 3/2) in the De Giorgi approach to Navier-Stokes regularity can be closed using the Hardy space (H^1) structure of the pressure.

**What is established (from prior explorations):**

1. β = 4/3 is the current best pressure exponent, unchanged since Vasseur 2007.
2. β > 3/2 is the threshold for full regularity (Vasseur's Conjecture 14).
3. **Local pressure is NOT the problem** — δ_local = 3/5 > 0, the recursion closes for local terms.
4. **Far-field pressure IS the sole obstruction** — its coefficient ||p_far||_{L^∞(Q_k)} ~ ||u||_{L^2}^2 / r_k^3 is a FIXED CONSTANT (not controlled by U_k). Only in ε-regularity (smallness assumption) is this manageable.
5. **Bogovskii corrector is DEAD** — 2^{2k} compound growth. Do NOT pursue localization via cutoffs.
6. **The Vasseur school has used H^1 structure since 2007**, but the specific H^1-BMO duality angle (testing whether De Giorgi functions ψ_k are uniformly BMO-bounded) has NOT been tried. This is the genuine novel angle.
7. **The baseline reference is Choi-Vasseur 2014** (arXiv:1105.1526), with three-way pressure decomposition P = P_{1,k} + P_{2,k} + P_3 in Lemma 3.3.

## Your Task

Test whether H^1-BMO duality can replace the Hölder pairing currently used for the pressure term in the De Giorgi energy inequality, and whether this substitution improves the effective pressure exponent beyond β = 4/3.

### The Current Pressure Estimate (What You're Trying to Improve)

The pressure integral in the De Giorgi energy inequality is:

    I_p = ∫∫ p · div(v_k φ_k² ê) dx dt

where:
- v_k = (|u| - C_k)_+ (De Giorgi truncation at level k, C_k = M(1 - 2^{-k}))
- φ_k is a smooth cutoff on parabolic cylinder Q_k (φ_k ≡ 1 on Q_{k+1}, ||∇φ_k||_∞ ~ 2^k)
- ê = u/|u| (unit velocity direction)

The dominant pressure error term is:

    I_p^main = 2∫∫ p · v_k · φ_k · (ê · ∇φ_k) dx dt

Currently estimated via Hölder:

    |I_p^main| ≤ ||p||_{L^β(Q_k)} · ||v_k · ∇φ_k||_{L^{β'}(Q_k)}

With β = 4/3 (from CZ applied to u ∈ L^{8/3}_t L^4_x), β' = 4, and ||v_k ∇φ_k||_{L^4} controlled by De Giorgi energy U_k.

**The key fact:** p = (-Δ)^{-1} ∂_i∂_j(u_i u_j) is a composition of Riesz transforms applied to u⊗u. By the Coifman-Lions-Meyer-Semmes (CLMS 1993) theorem on compensated compactness, because div(u) = 0, the pressure p lies in the real Hardy space H^1(ℝ^3), NOT just L^1:

    p ∈ H^1(ℝ^3) with ||p||_{H^1} ≤ C||u||_{L^2}^2

### The H^1-BMO Duality Substitution

The Fefferman-Stein duality: (H^1)* = BMO. For f ∈ H^1 and g ∈ BMO:

    |∫ f · g dx| ≤ C ||f||_{H^1} · ||g||_{BMO}

This replaces the Hölder pairing. The question is whether this is actually better for the De Giorgi recursion.

## Specific Tasks

### Task 1: Write ψ_k Explicitly

Write out the De Giorgi test function ψ_k that pairs with the pressure in the energy inequality. From the Choi-Vasseur 2014 construction (arXiv:1105.1526):

    ψ_k = v_k · φ_k · (ê · ∇φ_k / |∇φ_k|)  [or the actual form — get this right]

Be precise about what function the pressure pairs against. The function multiplying p in I_p^main above is ψ_k = v_k · φ_k · (ê · ∇φ_k). Write it in terms of:
- The truncation v_k = (|u| - C_k)_+
- The cutoff φ_k with known support and gradient bounds
- The unit direction ê = u/|u|

### Task 2: Estimate ||ψ_k||_{BMO}

This is the CRITICAL computation. Two scenarios:

**Scenario A: ψ_k is BMO-bounded uniformly in k.**
- Cutoffs of Lipschitz functions are typically BMO-bounded (John-Nirenberg). v_k = (|u| - C_k)_+ is Lipschitz with constant 1 in |u|. φ_k is smooth with bounded gradient. The product might be BMO with norm depending on ||∇φ_k||_∞ ~ 2^k.
- CAREFUL: If ||ψ_k||_{BMO} ~ 2^k (growing with k), this is NOT uniformly bounded. Check the k-dependence explicitly.

**Scenario B: ||ψ_k||_{BMO} grows with k.**
- Determine the growth rate. If ||ψ_k||_{BMO} ~ 2^{αk}, then the H^1-BMO estimate gives:
    |I_p| ≤ C ||p||_{H^1} · 2^{αk}
- Compare this with the current Hölder estimate. Is 2^{αk} · ||p||_{H^1} better or worse than ||p||_{L^{4/3}} · ||ψ_k||_{L^4}?

**Key subtlety:** BMO norm of ψ_k = v_k · φ_k · h_k (where h_k is the angular part) involves:
- v_k has jumps (the truncation (·)_+ creates a Lipschitz kink)
- φ_k has gradient ~ 2^k on the transition region (but is smooth)
- h_k = ê · ∇φ_k may have angular singularities where u = 0 (ê undefined)

Compute ||ψ_k||_{BMO} using the definition:
    ||g||_{BMO} = sup_B (1/|B|) ∫_B |g - g_B| dx

where the sup is over all balls B.

### Task 3: Substitute H^1-BMO into the Far-Field Pressure Estimate

**IF ||ψ_k||_{BMO} is controlled (uniformly or with known k-growth):**

Replace the Hölder pairing with H^1-BMO:

    |I_p^far| ≤ C ||p_far||_{H^1} · ||ψ_k||_{BMO}

The far-field pressure: p_far = CZ(u⊗u · 1_{Q_k^{*c}}). This is harmonic on Q_k, so smooth. Its H^1 norm involves:

    ||p_far||_{H^1(Q_k)} ~ ||Rp_far||_{L^1(Q_k)} where R = Riesz transforms

Since p_far is harmonic on Q_k, its Riesz transforms are also harmonic, so ||Rp_far||_{L^1(Q_k)} ~ C |Q_k|^{1/2} · ||p_far||_{L^2(Q_k)} by Harnack/mean-value.

Trace through: does the substitution make the far-field coefficient U_k-dependent (instead of the FIXED CONSTANT ||u||_{L^2}^2/r_k^3)?

Compute the effective pressure exponent β_eff that the H^1-BMO route yields. Is β_eff > 4/3? Is β_eff > 3/2?

### Task 4: Check Whether H^1-BMO Bypasses the Localization Problem

H^1 functions have mean zero. This is a structural property that L^{4/3} functions do not have.

Questions:
1. Does the mean-zero property of H^1 help with localization? Specifically, if we decompose p = p_local + p_far, does p_local ∈ H^1 automatically (since CZ preserves H^1)?
2. Does the localization via cutoffs φ_k preserve the H^1 structure? (φ_k · p may NOT be in H^1 even if p ∈ H^1.)
3. Is there a way to use the GLOBAL H^1 norm of p (without localizing) that still gives useful estimates in the De Giorgi framework?

## Success Criteria

**SUCCESS:** The H^1-BMO substitution yields an effective pressure exponent β_eff > 4/3 in the De Giorgi recursion. Document the exact value and the full chain of estimates.

**PARTIAL SUCCESS:** The substitution yields β_eff = 4/3 but with a LOGARITHMIC improvement (e.g., L^{4/3}(log L)^α instead of L^{4/3}). Document whether this logarithmic gain is sufficient for the recursion.

**INFORMATIVE FAILURE:** The substitution fails for a specific reason. Document:
- Whether the obstruction is ||ψ_k||_{BMO} blowing up with k
- Whether the obstruction is the H^1 norm of p_far not being better than the L^{4/3} norm
- Whether the H^1-BMO gain is absorbed by another term in the inequality chain
- The SPECIFIC step where the gain is lost

**DEAD END:** H^1-BMO is provably no better than Hölder for this problem. Explain why structurally.

## Required Output Format

### Section 1: The Test Function ψ_k (explicit formula)
### Section 2: ||ψ_k||_{BMO} Estimate (computation with verification tag)
### Section 3: H^1-BMO Substitution Result (effective β_eff with full chain)
### Section 4: Localization Analysis (does H^1 help or not?)
### Section 5: Verdict (SUCCESS / PARTIAL / FAILURE / DEAD END + one paragraph why)
### Section 6: The #1 Insight (what is the single most important structural lesson?)

## Verification Requirements

- Tag every claim: [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- Use Python/Sympy to verify all exponent computations
- Use dimensional analysis to check all inequalities (parabolic scaling: [x] = L, [t] = L^2, [u] = L^{-1}T = L/T)
- If ||ψ_k||_{BMO} depends on k, provide an explicit formula for the k-dependence
- The Choi-Vasseur 2014 construction must be faithfully used — if you cannot access the paper, state so clearly and work from the De Giorgi framework described above

## Available Tools

- Python (numpy, scipy, sympy, mpmath)
- SageMath 10.8
- Lean 4 + Mathlib
- Web search for papers (search arXiv:1105.1526 for Choi-Vasseur 2014)
