---
topic: Bottleneck exponent gamma from DNS — pressure integral P_k^{21} scaling
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-002"
---

## Finding

The bottleneck integral I_k = int int |P_k^{21}| * |d_k| * 1_{v_k>0} dx dt — the specific term limiting Vasseur's analytical beta to < 4/3 — was measured from DNS across 5 ICs and 3-4 Re values. The bottleneck exponent gamma is defined by I_k ~ U_{k-1}^gamma.

### Key Result

**The bottleneck exponent gamma DECREASES with increasing Re for ALL ICs.** At moderate-to-high Re, most ICs show gamma < 1, far below the analytical 4/3 = 1.333. The analytical bound becomes LESS loose, not more, as turbulence intensifies.

### Bottleneck Exponent Table

| IC | Re=100 | Re=500 | Re=1000 | Re=2000 |
|---|---|---|---|---|
| TaylorGreen | **1.403** ± 0.18 | 0.555 ± 0.05 | 0.632 ± 0.07 | 0.634 |
| VortexTubes | **1.500** ± 0.37 | 1.245 ± 0.17 | 1.154 ± 0.11 | — |
| RandomGauss | N/A | 0.654 ± 0.07 | 0.618 ± 0.08 | 0.613 |
| KidaVortex | N/A | 0.455 ± 0.04 | 0.459 ± 0.05 | — |
| ABC | **1.219** ± 0.03 | **1.146** ± 0.06 | 1.103 ± 0.06 | — |

Bold = above 1.0.

### Key Findings

**1. Gamma > 4/3 only for the smoothest cases.** VortexTubes Re=100 (gamma=1.50) and TaylorGreen Re=100 (gamma=1.40) — both marginally above 4/3 within error. These are low-Re laminar flows where pressure behaves very well.

**2. Gamma decreases with Re for ALL ICs.** As the flow becomes turbulent, the pressure integral's effective exponent WORSENS. At Re=500-2000, most ICs show gamma < 1. The 4/3 bound is not loose — it captures a genuine feature.

**3. ABC maintains gamma > 1 at all Re** (1.22 → 1.15 → 1.10), though still below 4/3. The Beltrami structure keeps the pressure integral well-behaved.

**4. Gamma saturates at moderate Re.** For Re >= 500-1000, the bottleneck exponent stabilizes. Understanding why (perhaps through the pressure Poisson equation at turbulent scales) could reveal where the proof has maximal leverage.

### Implications for the Regularity Program

1. **The gap between 4/3 and 3/2 is genuine, not just analytical looseness.** If 4/3 were a loose upper bound, DNS would show gamma >> 4/3. Instead, gamma drops far below 4/3 for turbulent flows.

2. **The pressure integral is the genuine bottleneck.** P_k^{21} contributes unfavorably in turbulent regimes. The analytical bound captures this correctly.

3. **Don't try to improve the general beta bound.** Pushing beta above 3/2 for general flows would require fundamentally new ideas, not refinement of the existing De Giorgi iteration.

4. **Structural properties provide genuine leverage.** ABC (Beltrami) flow's favorable gamma suggests conditional regularity results exploiting flow structure (related to Beirao da Veiga & Berselli on velocity-vorticity alignment).

## E009 Adversarial Assessment

**DNS evidence cannot diagnose the tightness of bounds designed for near-singular solutions.** The claim that "the gap is genuine" based on DNS data commits a category error: properties of smooth solutions cannot diagnose bounds designed for near-singular solutions. It is entirely possible that CZ tightness is k-independent on smooth flows but k-dependent on near-singular flows, or that gamma approaches or exceeds 4/3 near singularity.

**Corrected framing:** "The gap between 4/3 and 3/2 is supported by **analytical evidence**: two independent De Giorgi formulations both yield 4/3 from different mechanisms, and no improvement has been achieved in 17 years despite significant community effort. **DNS evidence** (gamma decreasing with Re, beta_eff < 4/3) characterizes smooth-flow pressure structure but cannot directly address near-singular behavior. The gap appears genuine based on analytical and sociological evidence, though a proof of optimality for De Giorgi methods remains open." Grade: C+ (multiple evidence lines, each individually weak; shared smooth-solution limitation). **Partially novel** — systematic cumulative argument combining analytical, computational, and sociological evidence is new.
