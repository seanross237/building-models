---
topic: Distinguish typical-case vs worst-case in bound-tightening explorations
category: goal-design
date: 2026-03-30
source: "navier-stokes strategy-001 meta-exploration-006"
---

## Lesson

When exploring whether a mathematical bound can be tightened (e.g., Ladyzhenskaya inequality with spectral information), the goal must explicitly require the explorer to distinguish:

1. **Worst-case bound** — holds for ALL configurations in the function class (usable in proofs)
2. **Typical-case value** — holds for MOST configurations or in expectation (a statistical property)

Without this instruction, the explorer may compute impressive typical-case improvements and present them as bound tightenings. The distinction is critical because typical-case values cannot be used in regularity proofs.

## Evidence

- **navier-stokes strategy-001 exploration-006** — The goal was framed positively: "compute effective Ladyzhenskaya constants for spectrally localized fields." The explorer found C_{L,eff} ≈ 1.707 × Re^{-3/8} for Kolmogorov spectra — a 632× improvement at Re=1000. However, this is the Gaussian random-phase TYPICAL value. Phase-optimized (adversarial) configurations achieve near-sharp constants regardless of spectral support, so this cannot be used as a worst-case bound. The negative result — "spectral support doesn't help for worst-case bounds" — would have been reached faster with explicit framing.

## Goal Template

For bound-tightening explorations, include:

> "For each tighter estimate you compute, classify it as:
> - **WORST-CASE BOUND**: holds for all f in the function class (prove this)
> - **TYPICAL-CASE VALUE**: holds for random/generic configurations (state assumptions)
>
> If the typical-case value is dramatically better than the worst-case bound, identify what structural property (phase correlations, intermittency, etc.) separates them."

## When to Apply

Any exploration that aims to improve a mathematical inequality (Sobolev, interpolation, energy estimates) using additional structural information (spectral support, divergence-free, specific function class). Especially important when the improvement will be used in a proof chain where worst-case bounds are required.

## Variant: Empirical Analogue vs Analytical Quantity

**NEW (vasseur-pressure E002):** When computing empirical analogues of analytical bounds, require the explorer to explicitly state what the empirical quantity IS and ISN'T relative to the analytical quantity. Vasseur-pressure E002: beta_eff (best-fit exponent from smooth DNS solutions) is fundamentally different from beta_p (worst-case exponent proved for all weak solutions). beta_eff < 4/3 does NOT mean the analytical bound is tight — smooth solutions decay faster than worst-case regardless. The bottleneck exponent gamma is more directly comparable. Goal template addition: "State explicitly: what does this empirical quantity measure, and what analytical claim does it test? What would the empirical result need to show to provide evidence for/against the analytical conjecture?"

## Relationship to Other Entries

- Distinct from **require-quantification-in-stress-tests.md** (quantifying objections, not bound classification)
- Distinct from **specify-failure-paths.md** (what to do when things fail, not classification of success types)
- Complements **allow-explorer-synthesis.md** (the typical/worst-case distinction is one the explorer can discover, but only if prompted)
