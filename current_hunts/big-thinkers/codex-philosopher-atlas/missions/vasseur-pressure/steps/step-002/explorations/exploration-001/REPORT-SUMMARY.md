# Exploration 001 Summary: H^1-BMO Duality Route for Improving the Pressure Exponent

## Goal
Test whether H^1-BMO duality (Fefferman-Stein / CLMS 1993) can replace the Hölder pairing
for the pressure term in the Vasseur De Giorgi energy inequality, improving β beyond 4/3
toward the needed β > 3/2. This was labeled "most promising" and "novel — not tried by
Vasseur school."

## What Was Tried
1. Wrote ψ_k explicitly (De Giorgi test function paired with pressure in I_p^main)
2. Estimated ||ψ_k||_{BMO} analytically and numerically (two routes: L^∞ and W^{1,3}→BMO)
3. Compared the H^1-BMO estimate against the current Hölder estimate for the De Giorgi recursion
4. Analyzed whether H^1-BMO improves the far-field pressure coefficient
5. Checked whether φ_k·p preserves H^1 structure (localization question)
6. Ran the atomic decomposition / mean-zero analysis
7. Verified numerically: ||ψ_k||_{BMO} / ||ψ_k||_{L^4} ratio grows toward 1 as k → ∞

All exponent/norm computations supported by Python scripts (code/hbmo_exponent_analysis.py,
code/bmo_norm_model.py). Numerical BMO norm computed via ball sampling for 1D model.

## Outcome: DEAD END

H^1-BMO duality is provably no better than Hölder for this problem. Three independent
structural reasons:

**1. BMO norm of ψ_k is not U_k-controlled:**
   ||ψ_k||_{BMO} requires either L^∞ or W^{1,3} bounds on v_k.
   - L^∞ on v_k is circular (what we're trying to prove)
   - W^{1,3} requires ||∇u||_{L^3} — NOT in Leray-Hopf class
   - The critical fact: W^{1,2}(ℝ^3) ↛ BMO(ℝ^3) (embedding fails — need W^{1,3})
   - U_k only controls W^{1,2}, so U_k → ||ψ_k||_{BMO} fails

**2. Global H^1 norm = SAME fixed-constant obstruction:**
   ||p||_{H^1(ℝ^3)} ≤ C·E_0 (CLMS 1993). This is the GLOBAL energy — same fixed
   constant as the current far-field L^∞ estimate. The H^1-BMO approach does NOT make
   the far-field coefficient U_k-dependent. The fundamental obstruction persists unchanged.

**3. H^1 localization fails:**
   φ_k · p ∉ H^1 when p ∈ H^1 (cutoffs destroy the mean-zero atom structure).
   The De Giorgi iteration must localize to Q_k — this destroys the H^1 structure.
   Once localized, the CLMS advantage evaporates.

**Effective β_eff from H^1-BMO: UNDEFINED** (the estimate is worse than Hölder —
it loses the U_k^{1/2} dependence that Hölder preserves via GNS).

## Verification Scorecard

- **[VERIFIED]:** 0
- **[COMPUTED]:** 8 (exponent chains, BMO vs L^4 numerical, atomic decomposition analysis,
  Sobolev gap, far-field coefficient comparison)
- **[CHECKED]:** 5 (CLMS theorem, W^{1,n}⊂BMO embedding, Hölder conjugates, GNS parabolic,
  far-field Green's function)
- **[CONJECTURED]:** 3 (Choi-Vasseur 2014 compatibility, local Hardy space failure, exact
  BMO constant)

## Key Takeaway

**The H^1 property of pressure (CLMS) and the De Giorgi iteration are structurally
incompatible.** H^1 is a global/cancellation-based structure; De Giorgi is
local/energy-based (W^{1,2}). These cannot be combined directly because:
(a) localization destroys H^1, (b) W^{1,2} ↛ BMO, and (c) global H^1 norms don't
encode local U_k information. The "novel angle" that was H^1-BMO duality turns out to
hit a structural wall at the W^{1,2}/W^{1,3} boundary.

## Leads Worth Pursuing

1. **The W^{1,3} gap is the actual target.** The H^1-BMO route fails because De Giorgi
   only gives W^{1,2} but BMO needs W^{1,3}. Any improvement that gives u ∈ L^2_t W^{1,3}_x
   (even locally, even with logarithmic margin) would make H^1-BMO available — AND would
   likely make CZ give β > 4/3 directly (since u ∈ L^3 gives p ∈ L^{3/2} exactly).
   So W^{1,3} is a threshold everywhere, not just for H^1-BMO.

2. **The far-field structure of p_far itself (harmonic on Q_k):** Harmonic functions have
   very fast decay of oscillation. The BMO norm of p_far ON Q_k is smaller than the L^∞
   norm (by Harnack). Could H^1-BMO work locally for p_far·ψ_k by using the HARMONIC
   structure of p_far rather than the global H^1 norm? This might give a different estimate
   than ||p_far||_{H^1}·||ψ_k||_{BMO}.

3. **Fractional Sobolev approach:** The step between W^{1,2} and W^{1,3} is a fractional
   Sobolev gap. Fractional De Giorgi methods (as in Caffarelli-Vasseur 2010 for fractional
   drift-diffusion) might give W^{s,2} for some s > 1 — enough for BMO if s·2 = 3, i.e.,
   s = 3/2. Is there a fractional regularity gain available in NS?

4. **The Riesz-Lorentz interpolation route:** The current β = 4/3 uses CZ on u ∈ L^{8/3}.
   The "weak" (Lorentz) estimate gives p ∈ L^{3/2,∞}. The gap between L^{4/3} and L^{3/2,∞}
   is EXACTLY 1/12 in reciprocal exponent. Is there a Lorentz-space version of De Giorgi
   that exploits weak-type norms?

## Proof Gaps Identified

The main "gap" this exploration identified is NOT in the proof — it's in the STRATEGY:
H^1-BMO is the wrong tool. The specific gaps for future work:

1. **W^{1,2} → BMO fails in ℝ^3:** This is the fundamental wall. Any strategy must either
   work within W^{1,2} (Leray-Hopf), or find a way to gain W^{1,3} (better regularity),
   or avoid BMO entirely.

2. **H^1 localization theorem needed:** If there exists a "truncated H^1" structure
   (some function space H^1_k that is preserved by φ_k-multiplication and still gives
   useful duality), this would unlock the CLMS structure. No such space is known.

3. **Far-field p_far: H^1 structure on Q_k:** Since p_far is harmonic on Q_k, it has
   a well-defined "Hardy space" structure on Q_k (mean value property → can define atoms).
   The local H^1 norm of p_far on Q_k might be much smaller than the global H^1 norm.
   This was not fully computed.

## Unexpected Findings

1. **The W^{1,3} threshold appears to be universal.** Both the CZ ceiling (u ∈ L^3 gives
   β = 3/2) and the BMO control of ψ_k require W^{1,3}. This is not a coincidence —
   both obstructions hit the SAME borderline Sobolev space. The β = 3/2 threshold and
   the W^{1,3} threshold are two faces of the same obstruction.

2. **The atomic decomposition exactly saturates.** The mean-zero cancellation of H^1
   helps for small atoms (scale << 2^{-2k}) but is exactly offset at the optimal scale
   (ρ ~ 2^{-2k}). The cancellation gain and the 2^{2k} "cost" of ψ_k's gradient exactly
   cancel. This is a sharp result, not just an order-of-magnitude analysis.

3. **Even with W^{1,3} regularity, H^1-BMO is WORSE than Hölder.** If ||∇u||_{L^3} were
   available (hypothetically), H^1-BMO would give |I_p| ≤ C·E_0·2^k (no U_k factor),
   while Hölder gives |I_p| ≤ C·E_0·2^k·U_k^{1/2} (with U_k factor). Hölder wins even
   with better regularity. This means H^1-BMO is structurally inappropriate for De Giorgi,
   not just insufficient due to Leray-Hopf limitations.

## Computations Identified

1. Compute ||p_far||_{H^1_local(Q_k)} using the harmonic structure of p_far on Q_k.
   Compare this LOCAL H^1 norm with the global ||p_far||_{H^1(ℝ^3)}.
2. Test: does the L^{3/2,∞} (weak Lorentz) structure of p give any advantage?
   Lorentz-space De Giorgi might extract something from weak-type.
3. Compute what β_eff would be needed to close the recursion if ONLY the far-field
   term contributes (upper bound on the "achievable β" from any modification of
   the pressure pairing that still uses global norms).
