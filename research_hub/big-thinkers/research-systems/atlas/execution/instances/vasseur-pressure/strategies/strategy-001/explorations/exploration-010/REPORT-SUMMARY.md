# Exploration 010 Summary: Perturbed-ABC Near-Beltrami Test + Leray Projection

## Goal
Test whether the Beltrami-De Giorgi mechanism (B_k = O(2^{-k}), pressure >95% Bernoulli) extends from exact Beltrami to near-Beltrami flows; test Leray projection of u_below.

## Outcome: **Mechanism does NOT generalize** (critical negative result)

The B_k decay with k is **lost immediately for any perturbation eps > 0**. Even 1% random perturbation (eps=0.01) causes B_k to plateau at B_full ≈ 0.063 instead of continuing to decay. For eps >= 0.05, B_k is flat across all k.

beta_eff degrades continuously: 1.01 (exact Beltrami) → 0.89 (eps=0.05) → 0.59 (eps=0.2) → 0.28 (eps=0.5). The beta > 1 threshold (required for regularity) is crossed at eps ≈ 0.02 — a flow must be >98% Beltrami for the mechanism to work.

Leray projection is a minor correction: it fixes the div(u_below) ≠ 0 issue from E007 but doesn't change the qualitative picture. B_k and R_frac still decay as ~2^{-k} for exact Beltrami after projection.

## Verification Scorecard
- **[COMPUTED]**: 8 findings (DNS at Re=500, N=64, 6 perturbation levels)
- **[VERIFIED]**: 0
- **[CONJECTURED]**: 0

## Key Takeaway
The Beltrami-De Giorgi pressure mechanism is **specific to exact Beltrami flows** (a measure-zero set). Generic turbulent flows are far from Beltrami. This is the critical weakness of Claim 5 — the Bernoulli dominance and B_k decay cannot be invoked for realistic flows.

## Leads Worth Pursuing
- Could vortex tubes (which are locally near-Beltrami at their cores) provide partial B_k improvement even in generic flows? Would need to measure B_k conditioned on local helicity density.
- Is there a weaker structural property (e.g., alignment between u and curl(u) above some threshold) that degrades more gracefully than exact Beltrami?

## Unexpected Findings
- Viscous evolution at Re=500 actually *improves* Beltrami alignment (B_full drops ~50% from t=0 to t=2.0) because random high-frequency modes decay faster than the ABC base mode. But this is insufficient to restore B_k decay with k.
- At eps=0.5, the remainder fraction R_frac > 1, meaning the Bernoulli decomposition becomes meaningless (remainder exceeds total).
