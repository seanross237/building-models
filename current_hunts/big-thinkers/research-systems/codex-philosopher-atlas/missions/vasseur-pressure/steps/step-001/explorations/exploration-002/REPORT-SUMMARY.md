# Exploration 002 Summary: Pressure Term Dissection in De Giorgi Energy Inequality

## Goal
Dissect the De Giorgi energy inequality for NS, trace exactly where β = 4/3 arises for the pressure exponent, compare with the pressure-free drift-diffusion case, and compute Bogovskii corrector scaling.

## What Was Tried
1. Derived the full De Giorgi energy inequality for NS, identifying all terms (dissipation, transport, pressure, cutoff corrections) with precise function space estimates.
2. Traced the chain of inequalities from the Leray-Hopf energy class through Sobolev embedding, parabolic interpolation, Calderón-Zygmund, and Hölder pairing to the pressure exponent β = 4/3.
3. Built term-by-term comparison table between drift-diffusion (CV 2010) and NS (V 2007).
4. Computed Bogovskii corrector W^{1,q} estimates on the De Giorgi annuli.

All exponent tracking done with Python/Sympy (3 scripts, ~500 lines).

## Outcome: SUCCEEDED (all 4 tasks completed)

### Verification Scorecard
- **[COMPUTED]:** 14 claims (exponent chain, power counting, Bogovskii growth, recursion structure)
- **[CHECKED]:** 5 claims (CZ theory, drift-diffusion closure, Bogovskii constants against literature)
- **[CONJECTURED]:** 1 claim (bottleneck distribution assessment)

## Key Takeaway

**The β = 4/3 bottleneck is DISTRIBUTED across two interacting constraints, not a single sharp inequality.**

1. **CZ ceiling (hard, from scaling):** u ∈ L^{3,∞} → p ∈ L^{3/2,∞} (weak type only). Strong-type L^β requires β < 3/2.
2. **De Giorgi recursion (structural):** The pressure decomposes into local and far-field parts. The local part closes the recursion (δ_local = 3/5 > 0). The far-field part has a FIXED CONSTANT coefficient that makes the U_k exponent sublinear (σ_far < 1). Only ε-regularity (smallness assumption) controls the constant.

The measure exponent 1/10 in the local pressure estimate is remarkably β-independent — a structural feature worth understanding deeper.

## Leads Worth Pursuing

1. **Far-field pressure is the sole obstruction.** Any technique bounding ||p_far||_{L^∞(Q_k)} in terms of U_k (not a fixed constant) would close the full recursion.
2. **Avoid pressure localization.** Bogovskii corrector FAILS — compounds to 2^{2k} growth (worse than the original pressure problem). The H^1 route should NOT pursue Bogovskii-type corrections.
3. **The 1/10 universality.** The β-independence of the measure exponent in local pressure suggests deeper structure that might extend to the far-field.
4. **Breaking the CZ ceiling.** Even a logarithmic improvement (u ∈ L^3(log L)^α instead of L^{3,∞}) might cross the 3/2 threshold.

## Proof Gaps Identified

- The far-field pressure estimate relies on ||u||_{L^2} being bounded (energy class). There is no mechanism in the standard De Giorgi framework to make this SMALL on the iteration cylinders.
- The gap between β = 4/3 (achievable) and β = 3/2 (needed) is exactly 1/6 in reciprocal: 1/(4/3) - 1/(3/2) = 3/4 - 2/3 = 1/12. This is a quantitative target for any improvement.

## Unexpected Findings

- **Bogovskii is strictly worse than the original pressure problem.** The corrector introduces 2^{2k} growth (vs. 2^k from pressure), and the resulting U_k exponent (best: 9/10) is worse than the far-field pressure exponent (6/5). This is a NEGATIVE result that should inform strategy.
- **Local pressure is NOT the problem.** The local part of the pressure contributes U_k^{8/5} to the recursion — comfortably superlinear. This means improving the CZ estimate for LOCAL pressure (e.g., via better Riesz transform bounds) would not help. The difficulty is entirely in the far-field.

## Computations Identified

1. Compute the far-field pressure decay rate: ||p_far||_{L^∞(Q_k)} as a function of the energy concentration on larger scales. Is there a logarithmic improvement available?
2. Test whether Helmholtz decomposition BEFORE truncation (splitting u into gradient and divergence-free parts) avoids the localization cost.
3. Quantify the relationship between the ε-regularity scale r₀ and the number of De Giorgi steps needed, as a function of β.
