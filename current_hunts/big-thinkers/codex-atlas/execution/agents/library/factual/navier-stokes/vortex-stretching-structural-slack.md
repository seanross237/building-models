---
topic: Vortex stretching bound has ~158x structural slack (lower bound over tested ICs) — implications for regularity
confidence: provisional
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-003, adversarial review exploration-008"
---

## Overview

The minimum vortex stretching slack across all tested initial conditions is 157.70x (at N=128 convergence). No tested configuration achieved slack < 50x. This is a **lower bound over the 5 IC families tested** — NOT an irreducible structural constant.

**Adversarial caveat (E008):** The claim "irreducible" is unjustified. Protas-type PDE-constrained optimization ICs (Kang, Yun, Protas 2020, *J. Fluid Mech.* 893), which maximize enstrophy growth using gradient ascent, were NOT tested and could potentially achieve lower slack. The optimal sigma=2.5 ≈ 0.4L is domain-size dependent, suggesting the minimum slack is a property of the T^3 domain geometry, not an intrinsic flow constant.

---

## Bound Decomposition

The vortex stretching bound chains through:

|integral(S*omega*omega)| <= ||S||_{L2} * ||omega||_{L4}^2 <= ||omega||_{L2} * [C_L * ||omega||_{L2}^{1/4} * ||grad(omega)||_{L2}^{3/4}]^2

The slack comes from two sources:

1. **Holder step:** |integral(S*omega*omega)| <= ||S||_{L2} * ||omega||_{L4}^2. Loses a factor because S and omega are not maximally aligned. For div-free flows, ||S||_{L2} = ||omega||_{L2}/sqrt(2), contributing a geometric factor.

2. **Ladyzhenskaya step:** ||omega||_{L4}^2 <= C_L^2 * ||omega||_{L2}^{1/2} * ||grad(omega)||_{L2}^{3/2}. Sharp constant C_L on T^3 for vector fields involves Gagliardo-Nirenberg inequality, tight only for specific extremizer profiles.

---

## Implications for Regularity Theory

1. **Possible improvement:** A tighter bound exploiting the divergence-free constraint or Biot-Savart kernel structure might close some of the gap. The div-free constraint is only used in ||nabla u|| = ||omega|| (periodic domain); more refined estimates might exploit the curl structure.

2. **VS bound not the bottleneck for regularity:** If the VS bound has 158x slack, it is unlikely to be the inequality whose saturation drives blow-up. The other inequalities (Ladyzhenskaya, Agmon, etc.) may have less slack at critical times.

3. **Geometric universality:** The near-Re-independence of the minimum slack (157-175x across Re=100-1000) suggests the ~158x gap is a **geometric constant of the inequality**, not a dynamical effect. [CONJECTURED]

---

## 3-Factor Decomposition Caveat (E008)

The decomposition of 237x slack into alpha_geom (5.3x) × alpha_Lad (31x) × alpha_sym (sqrt(2)) contributing 31%/63%/6% of log-slack is **tautologically exact by construction** — any positive number can be factored this way. The scientific content is the identification of Ladyzhenskaya as the dominant bottleneck (63%), which is consistent with the independently known fact that Ladyzhenskaya optimizers (spike-like Aubin-Talenti profiles) are far from smooth NS solutions. However, the percentages are specific to TGV at Re=100 at the minimum-slack timestep and depend on the choice of sharp constant C_L.

## IC-Robust Slack Atlas (S002-E004 Adversarial Review)

Cross-inequality, cross-IC comparison of slack across 4 ICs (Taylor-Green, Gaussian, anti-parallel, random) at 2 Re values:

| Inequality | Slack Range | IC Variance | Classification |
|---|---|---|---|
| F5 CZ | 7.6-17.5x | Low (~2x) | Universally tight |
| F1 Ladyzhenskaya | 3.0-18.7x | Moderate (~6x) | Universally tight |
| F3 Sobolev | 2.7-27.5x | Moderate (~10x) | Universally tight |
| Vortex stretching | varies by 1238x | Very high | IC-specific |

**Anti-parallel tubes anomaly:** Ladyzhenskaya slack ~3.0 (tightest of all ICs) but vortex stretching slack ~267,516x. This "split personality" could indicate the Ladyzhenskaya bound is accidentally tight for this geometry, not fundamentally.

**Caveats (adversarial):**
- N=4 ICs is limited — "universally tight" overstates the evidence
- 2 Re values per IC; behavior at much higher Re unknown
- "Tight" is relative: even 3-18x slack is far from saturation (1x)
- Protas-type PDE-optimized ICs not tested
- The qualitative finding (VS is IC-specific, CZ/Lad are not) is robust; quantitative thresholds need more ICs

**Novelty:** PARTIALLY KNOWN — qualitative comparisons of inequality tightness are known. Quantitative slack measurements across multiple ICs and inequalities appear novel. **Defensibility: 3/5.**

## Limitations

- Results are on T^3 (periodic domain). Optimal sigma=2.5 ~ 0.4L suggests domain geometry matters.
- Only the E2E3 (vortex stretching) bound was adversarially searched; the other 7 inequality bounds from the 8-inequality infrastructure were not adversarially optimized.
- The 158x floor may decrease with further adversarial search (only anti-parallel tube family tested parametrically).
- **Protas-type adversarial ICs** (PDE-constrained optimization for maximum enstrophy growth) were not tested and represent the strongest untested challenge to the 158x lower bound.
- The 3-factor decomposition is IC-specific and time-specific (TGV at Re=100 at minimum-slack moment).
