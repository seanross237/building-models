# Exploration 002: Geodesic Convexity Approach to the B_□ Inequality

## Mission Context
This is a YANG-MILLS mission (strategy-003). Do not confuse with other missions.

## The One Inequality We Need to Prove

**The open problem:** For all Q ∈ SU(N)^E and all tangent vectors v ∈ ⊕_e su(N):

  ∑_□ |B_□(Q,v)|² ≤ 4d |v|²

**Convention (required):** S = −(β/N) Σ_□ Re Tr(U_□), |A|² = −2Tr(A²). The 1/N is essential.

**Why this matters:** This would prove β < 1/4 mass gap for SU(2) Yang-Mills in d=4 (12× SZZ arXiv:2204.12737, 6× CNS arXiv:2509.04688).

## B_□ Formula (for reference)

  B_□(Q,v) = Ã₁ + Ã₂ + Ã₃ + Ã₄

where each Ã_i = Ad_{P_i}(±v_{e_i}) is a parallel-transported tangent vector, |Ã_i| = |v_{e_i}|.

At Q=I: B_□ = discrete curl ω_{x,μν}(v). Bound ∑_□ |B_□|² ≤ 4d|v|² proved via Fourier (Strategy 002 E008). The inequality is TIGHT at Q=I — equality holds for the staggered mode.

Numerically (Strategy 002 E010, 100 diverse L=2 configs): max H_norm = 0.083331 < 1/12 = 0.083333 for all Q ≠ I. Adversarial search max = 0.063. Q=I is the unique worst case.

## Your Approach: Geodesic Convexity / Second Derivative Test

**Intuition:** If the function f(Q) = max_v [∑_□ |B_□(Q,v)|² / |v|²] (the operator norm of ∑_□ B_□ B_□^T) is geodesically concave on SU(N)^E with a unique maximum at Q=I, then f(Q) ≤ f(I) = 4d for all Q. This is exactly what we need.

Geodesic concavity of f on SU(N)^E means: for any geodesic γ(t) = (Q_{x,μ}(t)) in SU(N)^E, the function t ↦ f(γ(t)) is concave. This is implied by: the second derivative d²f/dt²|_{t=0} ≤ 0 for all geodesics through Q=I.

**Strategy:** Compute the second derivative of f at Q=I along all geodesics and show it's ≤ 0.

### Step 1: Define the Setup

Geodesic through Q=I in direction W = (W_{x,μ}) ∈ ⊕_e su(N): γ(t)_{x,μ} = exp(t W_{x,μ}).

Define F(t) = max_v ∑_□ |B_□(γ(t), v)|² / |v|².

At t=0: F(0) = 4d (achieved by staggered mode v_stag).
Goal: F''(0) ≤ 0 for all W.

### Step 2: Compute F'(t) and F''(t)

At t=0, the maximum in F(t) is achieved by v_stag (the staggered mode). By eigenvalue perturbation theory (assuming non-degenerate maximum eigenvalue — which needs to be checked, since E009 found 9-fold degeneracy):

  F'(0) = ⟨v_stag, (d/dt M(γ(t))|_{t=0}) v_stag⟩ / |v_stag|²

where M(Q) = ∑_□ B_□ B_□^T.

  F''(0) = ⟨v_stag, M''(0) v_stag⟩ / |v_stag|² + [terms from eigenvector perturbation]

Compute M'(0) and M''(0) explicitly. Each involves differentiating Ad_{exp(tW)}(v) with respect to t at t=0:

  d/dt [Ad_{exp(tW)}(v)]_{t=0} = [W, v] = ad_W(v)

So the first derivative of each Ã_i at t=0 involves commutators [W_{e_i}, v_{e_i}].

### Step 3: Check if F'(0) = 0

At Q=I, Q=I should be a critical point. Check: is F'(0) = 0 for all W? This would mean Q=I is an extremum (not just a point where the function is evaluated).

If F'(0) ≠ 0 for some W: Q=I is NOT a critical point, which would be surprising given E010 showed Q=I is the unique maximizer. Investigate.

If F'(0) = 0 for all W (Q=I is a critical point): then F''(0) determines whether it's a maximum.

### Step 4: Sign of F''(0)

Compute the second derivative:

  M''(0) = d²/dt² [∑_□ B_□(γ(t)) B_□(γ(t))^T]_{t=0}

This involves:
  - Second commutator terms: (d²/dt²)Ã_i = [W, [W, v]] = ad_W² (v) (at t=0, for Ã_i = Ad_{exp(tW)}v)
  - Cross terms: (d/dt Ã_i)(d/dt Ã_j)^T

Show that ⟨v_stag, M''(0) v_stag⟩ ≤ 0 for all W. This is the key computation.

### Step 5: Handle Degeneracy

E009 found the maximum eigenvalue 4d of M(I) has multiplicity 9 (for L=2, d=4, SU(2)). With degenerate eigenvalues, the perturbation theory is more complex:

  F'(0) = max_{w in eigenspace} ⟨w, M'(0) w⟩ / |w|²

And F''(0) involves a min-max over the eigenspace. Handle the degenerate case carefully.

## Required Elements

1. **Explicit second derivative computation.** Write out M'(0) and M''(0) explicitly in terms of structure constants and link tangents W_{x,μ}.

2. **Worked example.** Take W = (W_{0,0} = τ₁ = iσ₁/2, all other W = 0) on a 2⁴ lattice. Compute F'(0) and F''(0) explicitly. Verify the sign.

3. **Degeneracy analysis.** The maximum eigenvalue is degenerate (multiplicity ≥ 9). How does this affect the second-order analysis? Is F''(0) still well-defined?

4. **If F''(0) > 0 for some W:** Q=I is a local MINIMUM of f, not a maximum! This would falsify the convexity approach and is an important finding.

5. **If F''(0) ≤ 0 for all W (Q=I local max):** Show that f(Q) = 4d only at Q=I, establishing global concavity.

## Success Criteria

**Full success:** f''(0) ≤ 0 for all W and Q=I is a global maximum → H_norm ≤ 1/12 for all Q.

**Partial success:** f'(0) = 0 confirmed (critical point) and f''(0) ≤ 0 for all W (local max). Full success then requires ruling out other local maxima.

**Useful failure:** f''(0) > 0 for some W (Q=I is actually a saddle or local min). This would mean the convexity approach fails and the maximum of f(Q) is NOT at Q=I — potential counterexample direction!

## Output Format

Write REPORT.md section by section:
- Section 1: Setup — M(Q) and the second derivative approach
- Section 2: First derivative F'(0) at Q=I
- Section 3: Second derivative F''(0) at Q=I
- Section 4: Degeneracy analysis
- Section 5: Worked example
- Section 6: Conclusions

Write REPORT-SUMMARY.md (1 page): Is Q=I a local maximum of f(Q)? Is the inequality proved via convexity?

## Notes
- Write mathematics as you figure it out. Don't accumulate before writing.
- Focus on the second derivative computation — this is the key step.
- If the algebra becomes intractable, simplify to SU(2) with N=2 and d=4.
