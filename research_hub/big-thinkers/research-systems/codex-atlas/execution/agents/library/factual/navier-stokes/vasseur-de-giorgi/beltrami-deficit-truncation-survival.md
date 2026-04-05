---
topic: De Giorgi truncation preserves Beltrami structure — B_k = O(2^{-k})
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-007"
---

## Finding

The De Giorgi truncation u_below = u * min(1, lambda_k/|u|) preserves the Beltrami structure of ABC flows. The Beltrami deficit B_k = ||curl(u_below) - lambda_opt * u_below||_{L^2} / ||u_below||_{L^2} scales as O(2^{-k}), halving at each De Giorgi level.

### Beltrami Deficit Definition

For truncated velocity u_below at De Giorgi level k:

```
lambda_opt = <curl(u_below), u_below> / ||u_below||^2
B_k = ||curl(u_below) - lambda_opt * u_below||_{L^2} / ||u_below||_{L^2}
```

B_k = 0 iff u_below is an exact eigenfunction of curl (Beltrami condition).

### ABC Flow Results (all Re identical)

| k | lambda_k | B_k     | lambda_opt | B_k / B_{k-1} |
|---|----------|---------|------------|----------------|
| 1 | 0.500    | 0.2792  | -1.000     | --             |
| 2 | 0.750    | 0.1368  | -1.000     | 0.490          |
| 3 | 0.875    | 0.0690  | -1.000     | 0.504          |
| 4 | 0.9375   | 0.0333  | -1.000     | 0.483          |
| 5 | 0.9688   | 0.0148  | -1.000     | 0.443          |
| 6 | 0.9844   | 0.0057  | -1.000     | 0.383          |
| 7 | 0.9922   | 0.0022  | -1.000     | 0.392          |
| 8 | 0.9961   | 0.0009  | -1.000     | 0.398          |
| Full | 1.0   | 3.0e-15 | -1.000     | --             |

**Pattern:** B_k ~ 0.56 * 2^{-k}. The optimal eigenvalue lambda_opt = -1.000 at all k (matches exact curl eigenvalue of ABC flow). [COMPUTED]

### Control ICs: No Improvement

| IC | B_full  | B(k=4) | B(k=8) | Trend     |
|----|---------|--------|--------|-----------|
| TG Re=100  | 2.961 | 2.960 | 2.961 | ~ const |
| TG Re=1000 | 4.879 | 4.874 | 4.879 | ~ const |
| RG Re=100  | 3.022 | 3.022 | 3.022 | ~ const |
| RG Re=1000 | 12.41 | 12.41 | 12.41 | ~ const |

Non-Beltrami flows show B_k ~ B_full at all k -- no Beltrami structure to lose. [COMPUTED]

### Physical Mechanism

The truncation clips |u_below| <= lambda_k but does NOT destroy the directional alignment with curl. At level k, only the fraction of the domain with |u_norm| > lambda_k is modified, and that fraction shrinks as 2^{-k}. The perturbation to the Beltrami structure is confined to this shrinking set.

### Re-Independence

All ABC results are IDENTICAL across Re = 100, 500, 1000. The ABC flow decays self-similarly as u(t) = u(0)e^{-nu*t}, and after L^inf normalization the spatial pattern is Re-independent. The conditional regularity improvement from Beltrami structure is NOT a low-Re artifact. [CHECKED]

### Critical Subtlety: Truncation Breaks div-free

The truncation u_below = u * min(1, lambda_k/|u|) is NOT divergence-free even when u is. Measured ||div(u_below)||_{L^2} = O(2^{-k}), negligible for k >= 6. This means the standard Hessian/Lamb decomposition (requiring div=0) does not apply directly. Despite this, the total Beltrami deficit still vanishes as O(2^{-k}).

### Significance

This resolves the key obstacle identified in the near-Beltrami perturbation analysis (E006): the concern was that truncation might destroy Beltrami structure. It does not. The deficit scales with the truncation width, meaning the mechanism is strongest precisely at the high-k levels where the De Giorgi iteration needs it.

## E009 Adversarial Assessment — DOES NOT SURVIVE AS STATED

**The result is circular for exact Beltrami and unproven for near-Beltrami.**

For exact Beltrami flows: B_k = O(2^{-k}) is a trivial consequence of smooth truncation on smooth functions. The truncation only clips above lambda_k, and the fraction of the domain where clipping occurs shrinks geometrically. Any smooth function truncated at level L only modifies a set of measure ~ (||u||_infty - L) / ||nabla u||_infty, which shrinks as L -> ||u||_infty. This is not a deep property of the De Giorgi iteration — it's a property of smooth truncation.

For near-Beltrami flows (the ONLY interesting case): B_0 > 0 is the initial Beltrami deficit. The truncation could either decrease or increase this deficit depending on whether the non-Beltrami component correlates with the super-level sets. No evidence is provided for this case. Controls (TG, RG) confirm non-Beltrami flows show constant B_k — they do NOT show that near-Beltrami flows improve.

Additionally, div(u_below) != 0 is a serious problem. The entire Bernoulli/remainder decomposition relies on div u = 0. When div(u_below) != 0, the Lamb vector identity breaks down and "P_hessian = -|u_below|^2/2" is not the pressure of u_below.

**The MISSING connection to beta** — even if B_k shrinks, the claim never establishes that a small Beltrami deficit implies improved beta. This is the CRUCIAL link needed for the result to matter for regularity theory, and it is completely absent.

**Corrected framing:** "For exact Beltrami DNS flows, the truncation u_below shows geometrically decaying Beltrami deficit B_k ~ 0.56 * 2^{-k}, which is a trivial consequence of smooth truncation on smooth functions. However, (a) exact Beltrami is trivially regular, (b) near-Beltrami behavior is uncharacterized, (c) div(u_below) != 0 complicates the pressure interpretation, and (d) the connection to improved beta is not established." Grade: C+ (interesting computation, significant caveats). **This is the weakest claim in Strategy-001.**

**What would fix it:** (1) Analytical proof that B_k decays for epsilon-Beltrami flows (not exact Beltrami); (2) Rigorous bound connecting B_k to the Lamb vector contribution in the De Giorgi recurrence; (3) Resolution of div(u_below) != 0 — either show it's negligible or use Leray projection to preserve divergence-free structure.

## E010 Definitive Negative Result

**All three "fix" items from E009 have been tested computationally:**

1. **B_k does NOT decay for epsilon-Beltrami flows** — even at eps=0.01 (99% ABC + 1% random), B_k plateaus at ~0.063 rather than continuing to decay. For eps >= 0.05, B_k is flat across all k. The property is specific to exact eigenstates of curl.

2. **beta_eff degrades continuously** — from 1.01 (exact) through 1.07 (eps=0.01), 0.89 (eps=0.05), to 0.28 (eps=0.50). beta > 1 maintained only for eps < ~0.02.

3. **Leray projection is a minor correction** — drives div(u_below) to machine precision but does not change the qualitative picture. The largest correction is at k=1 (16% relative change); at k >= 5, it is < 0.4%.

**This confirms the E009 assessment: the truncation preservation result is specific to exact Beltrami and does not generalize.** See `../../near-beltrami-negative-result.md` for the full E010 data tables.
