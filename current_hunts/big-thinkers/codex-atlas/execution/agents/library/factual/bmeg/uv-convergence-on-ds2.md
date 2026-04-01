---
topic: bmeg
confidence: provisional
date: 2026-03-24
source: exploration-007-BMEG-self-consistency
---

# UV Convergence Improvement on a d_s = 2 Background

A key technical finding: replacing the standard flat 4D background (G_bar ~ 1/p^2) with the BMEG background (G_bar ~ 1/p^4 in the UV) *improves* the UV convergence of the graviton self-energy, rather than disrupting it. This is the opposite of what one might naively fear.

## Three Channels of Background Influence

The FRG flow equation for the graviton two-point function is affected by the background through:

1. **The trace (heat kernel):** On d_s = 2 background, effective density of states at high momenta behaves as p dp instead of p^3 dp, *reducing* the number of UV modes and tending to decrease loop corrections.

2. **The vertices:** Graviton self-coupling depends on background through covariant derivatives. However, the d_s = 2 modification is in UV scaling, not curvature -- the background can still be approximately flat while having modified UV propagation.

3. **Internal propagators (most important):** Background propagator enters internal lines. With G_bar ~ 1/p^4, internal propagators are softer in the UV.

## Power-Counting Argument

### Standard flat background (G ~ 1/k^2):
- Graviton self-energy: Sigma ~ integral d^4k (kp)^2 / (k^2 (p-k)^2)
- Power count: integral k^{2+3} dk / k^4 = integral k dk -- **UV divergent**

### BMEG background (G_bar ~ 1/k^4):
- Graviton self-energy: Sigma ~ integral d^4k (kp)^2 / (k^4 (p-k)^4)
- Power count: integral k^{2+3} dk / k^8 = integral dk/k^3 -- **UV convergent**

The softer background propagator dramatically improves convergence.

## Scalar Proxy Model

A scalar field proxy (phi^2 * phi_bg coupling, G_bg = 1/p^4) gives:
- Superficial degree of divergence D = 4 - 2*4 = -4 (convergent)
- Self-energy correction ~ lambda^2 / p^4, subleading to tree-level
- Anomalous dimension contribution vanishes in the UV

**But this misses the key graviton feature:** derivative coupling. The graviton three-point vertex ~ p^2 introduces extra numerator powers.

## Graviton with Derivative Coupling

With derivative vertices (numerator ~ k^2 p^2):
- D = 4 + 2 - 8 = -2 (still convergent, but less so)
- Result: Sigma_grav(p) ~ G_N p^2 ln(p/mu)
- The logarithmic correction generates a nonzero eta_h

The sign is positive (antiscreening), so eta_h > 0 persists.

## Refined Estimate

- Standard (flat): Sigma ~ G_N p^2 (Lambda_UV^2 + ... + C_1 p^2 ln(p/mu))
- BMEG: Sigma ~ G_N p^2 (C_2 ln(p/mu)) -- quadratic divergence absent, different coefficient
- Expect |C_2| <= |C_1|, so eta_h^{BMEG} <= eta_h^{flat} ~ +1.03
- Plausible range: 0 < eta_h^{BMEG} < 1

## Implication

The d_s = 2 background is *friendlier* to the self-consistency of eta_h > 0 than the flat background, not hostile. It suppresses the UV while preserving the structural mechanism (derivative coupling) that generates the positive anomalous dimension.
