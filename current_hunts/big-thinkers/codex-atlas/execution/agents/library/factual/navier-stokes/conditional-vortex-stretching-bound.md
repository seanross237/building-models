---
topic: Conditional vortex stretching bound — C(F4) ~ 0.003/F4 gives 237-1659x improvement over standard Ladyzhenskaya
confidence: provisional
date: 2026-03-30
source: "navier-stokes strategy-001 exploration-007"
---

## Overview

For NS solutions with bounded vorticity flatness F4, the vortex stretching integral satisfies a conditional bound with effective constant ~0.003/F4, dramatically tighter than the standard Ladyzhenskaya constant (C_L^2 = 0.684). The bound quantifies the "price of smoothness": NS solutions with bounded flatness are far from the spike-like optimizer of the Ladyzhenskaya inequality.

**Status: CONJECTURED.** Determined empirically from Taylor-Green vortex DNS. Not verified on other initial conditions or flow geometries. Not theoretically derived.

---

## Global Fit (all Re, all timesteps)

**C(F4) = 0.00313 * F4^{-1.01} ~ 0.00313 / F4**

Remarkably close to exact **1/F4 scaling**. [COMPUTED]

---

## Envelope Fit (maximum C_emp in each F4 bin)

**C_max(F4) = 0.00346 * F4^{-0.85}**

| F4 range | max C_emp | # data points | Standard C_L^2 / max C_emp |
|---|---|---|---|
| [1.0, 1.5) | 0.00289 | 72 | 237x |
| [1.5, 2.0) | 0.00250 | 53 | 273x |
| [2.0, 3.0) | 0.00148 | 32 | 462x |
| [3.0, 4.0) | 0.00125 | 15 | 550x |
| [4.0, 6.0) | 0.00070 | 9 | 973x |
| [6.0, 8.0) | 0.00060 | 7 | 1136x |
| [8.0, 12.0) | 0.00053 | 17 | 1288x |
| [12.0, 16.0) | 0.00041 | 12 | 1659x |

[COMPUTED]

---

## Conjectured Theorem

For a divergence-free vector field omega on T^3 with vorticity flatness F4 = <|omega|^4>/<|omega|^2>^2 <= F_max:

|int S_{ij} omega_i omega_j dx| <= (0.0035 / F_max^{0.85}) * ||omega||_{L^2}^{3/2} * ||nabla omega||_{L^2}^{3/2}

Improvement over standard Ladyzhenskaya (C_L^2 = 0.684):
- At F_max = 5/3 (Gaussian): **237x**
- At F_max = 3 (mildly intermittent): **~400x**
- At F_max = 10 (strongly intermittent): **~1100x**

[CONJECTURED]

---

## Physical Interpretation

The standard C_L^2 must accommodate the worst-case field (a spike-like function achieving the sharp Ladyzhenskaya inequality). For NS solutions with bounded flatness, the vorticity is spread across the domain, and the effective constant is much smaller. The conditional bound quantifies this: **the price of smoothness (bounded flatness) is a factor of ~200-1000x tighter vortex stretching control.**

---

## Limitations

1. Empirical only — from Taylor-Green vortex DNS (Re=100-5000). Not verified on other initial conditions or flow geometries. [CONJECTURED]
2. The exponent -0.85 in the envelope fit is not theoretically derived. May not hold for more extreme flows. [CONJECTURED]
3. A rigorous proof would need to establish: for div-free fields with flatness <= F_max, the maximum of |int S omega omega| / (||omega||^{3/2} ||nabla omega||^{3/2}) is bounded by a decreasing function of F_max. The mechanism (Ladyzhenskaya optimizer is spike-like, so flat fields can't saturate it) is clear but hasn't been formalized. [CONJECTURED]

## C_Leff^4 = F4*R^3 Tautology — C(F4) Correlation Is an Artifact (S002-E004)

The algebraic identity C_Leff^4 = F4 * R^3 holds exactly, where C_Leff = ||omega||_L4 / (||omega||_L2^{1/4} * ||grad omega||_L2^{3/4}), F4 = ||omega||_L4^4 / ||omega||_L2^4, and R = ||omega||_L2 / ||grad omega||_L2. This is a **3-line tautology from substituting definitions** — verified to machine precision (max error 1.38e-15) on 894 fields.

**Implication:** Any empirical C_Leff(F4) correlation is trivially predetermined by this identity (mediated by R). The C(F4) ~ 0.003/F4 relationship includes R-dependence implicitly. **Research direction killed:** flatness alone cannot tighten bounds — the scale ratio R must be controlled independently. Correlating C_Leff with F4 is circular.

**Defensibility of the kill: 5/5** — The identity is exact and the implication is correct. But the identity itself should not be presented as a discovery (it's algebraic manipulation, not physics).

## Adversarial Caveats (E008)

4. **F₄ range too narrow.** F₄ varies from 3 to 12 across Re=100-5000 for TGV — less than an order of magnitude. The 1/F₄ vs 1/F₄^{0.85} exponent distinction is statistically indistinguishable over this range.
5. **No proof F₄ stays bounded under NS evolution.** For the conditional bound to be useful in regularity theory, one needs F₄(t) <= F_max provable for NS solutions. No such bound is established. If F₄ can grow without bound, the conditional bound is vacuous.
6. **TGV symmetry may bias the scaling.** TGV has cubic symmetry constraining the vorticity distribution. The F₄-C relationship might be specific to flows with this symmetry.
7. **The fit has no theoretical justification.** No argument for why C should scale as 1/F₄. The exploration itself notes this.

**Verdict (E008): INCONCLUSIVE.** The empirical scaling is observed but from a single IC over a narrow parameter range with no theoretical backing. Interesting lead, not a robust finding. [NOVEL — no published C(F₄) relationship found]
