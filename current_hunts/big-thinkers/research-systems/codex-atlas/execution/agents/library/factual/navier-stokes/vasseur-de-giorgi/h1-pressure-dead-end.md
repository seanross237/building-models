---
topic: H^1 pressure route is a structural dead end — W^{1,3} wall
confidence: verified
date: 2026-03-31
source: "vasseur-pressure philosopher-atlas hunt; far-field-pressure-harmonic-loophole exploration-001"
---

## Main Result

Three independent H^1-based approaches to improving beta in the De Giorgi framework all fail for the same structural reason: the W^{1,3} wall.

### The W^{1,3} Wall (Universal Obstruction)

Every analytical route to improving beta hits the same barrier: Leray-Hopf gives W^{1,2} (nabla u in L^2), but every improvement route requires W^{1,3} (nabla u in L^3).

| What you need | Why | What you have |
|---|---|---|
| nabla u in L^3 for CZ strong-type | p in L^{3/2} requires it | nabla u in L^2 only |
| W^{1,3} for BMO embedding | psi_k in BMO needs it | W^{1,2} not embedded in BMO |
| p_theta > 4/3 in interpolation | De Giorgi recursion needs it | p_theta < 4/3 from H^1 subset L^1 |

The beta = 3/2 threshold and the W^{1,3} threshold are two faces of the same obstruction.

### Route 1: H^1-BMO Duality (Most Promising)

W^{1,2} does not embed into BMO — needs W^{1,3}. Even with hypothetical W^{1,3}, H^1-BMO duality is WORSE than Holder (loses a U_k^{1/2} factor). The tool is wrong entirely: it solves a problem the approach doesn't have.

### Route 2: Atomic Decomposition

Cancellation gain from H^1 atoms and gradient cost from localization exactly cancel at the optimal scale. De Giorgi test functions psi_k >= 0 (non-negative by construction as level-set truncations) waste all atomic cancellation — atoms require mean zero, which positive test functions cannot provide.

### Route 3: Complex Interpolation

[H^1, L^{4/3}]_theta gives L^{p_theta} with p_theta < 4/3 — weaker than the starting point. Goes the wrong direction.

## Key Secondary Findings

1. **The surviving lead is a harmonic far-field reformulation, not Vasseur's literal `P_{k21}` term.** In literal Vasseur notation, the bad bottleneck is the local non-divergence pressure `P_{k21}`, while the harmonic term is `P_{k1}` and is already favorable. The only coherent remaining lead is an alternative near/far decomposition that might absorb part of the bad local interaction into a harmonic `p_far`.
2. **Bogovskii correction is strictly worse.** Introduces 2^{2k} compound growth vs original 2^k. Eliminates all localization strategies.
3. **||p||_{H^1} <= C * E_0** — the H^1 norm of pressure is a fixed constant (total kinetic energy). H^1 structure can never make the far-field pressure U_k-dependent.

## Notation Correction

The earlier shorthand "far-field term `P_k^{21}`" should not be read literally. It mixes two different decompositions:

- Vasseur's split: harmonic/nonlocal `P_{k1}` plus local `P_{k2}`, with bad local subterm `P_{k21}`
- the later loophole framing: a Wolf-style or kernel-based near/far split `p = p_near + p_far` with harmonic `p_far` on the working cylinder

The remaining question is whether an alternative harmonic far-field split can recapture part of what Vasseur isolates as local `P_{k21}`. See `exact-far-field-pressure-obstruction.md`.

## Implications

- **Do NOT pursue H^1-based improvements to beta.** The obstruction is structural, not a proof artifact.
- **Any route within the Leray-Hopf energy class that pairs pressure against De Giorgi test functions cannot close the gap.**
- **Viable directions must either:** gain regularity beyond W^{1,2}, avoid pairing pressure against De Giorgi test functions, or abandon the De Giorgi framework entirely.

## Identified Leads (Not Tested)

1. Lorentz-space De Giorgi using weak-type L^{3/2,infinity}
2. Fractional regularity W^{s,2} with s > 1
3. Using div-free structure BEFORE localization cutoff
4. Exploiting an alternative harmonic far-field split `p = p_near + p_far` on `Q_k`, but only if it changes the bad pressure pairing itself from constant-scale to `U_k`-dependent; harmonicity alone is not enough
