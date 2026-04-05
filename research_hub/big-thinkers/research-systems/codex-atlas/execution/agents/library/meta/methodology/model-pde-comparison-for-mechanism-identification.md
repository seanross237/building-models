---
topic: Model PDE comparisons as mechanism-identification tool
date: 2026-03-30
source: "vasseur-pressure s2-exploration-003 meta"
---

## Lesson

When investigating a mathematical barrier in a specific PDE, compare the barrier across structurally related model PDEs (different dimensions, dissipation orders, nonlinearities). The comparison reveals whether the barrier is:
- **Universal** (same formula, same mechanism across PDEs) — attack the mechanism, not the specific PDE
- **PDE-specific** (different PDEs avoid the barrier) — study WHAT structural feature the successful PDE has that the target PDE lacks

## Evidence

Vasseur-pressure S2-E003: Comparing the De Giorgi beta across Burgers (1D), 2D NS, 3D NS, SQG, MHD, and fractional NS in a single exploration produced TWO major insights that neither pure analysis nor pure literature survey would have found:

1. **Universal formula beta = 1 + s/n** — emerged from systematic tabulation across (dimension, dissipation order) pairs. This formula immediately shows 4/3 is not NS-specific but dimensional.

2. **SQG exception mechanism** — SQG achieves regularity despite generic beta = 5/4 < 3/2 because its nonlinearity is a drift (multiplicative constant) rather than a pressure (additional U power). The DIFFERENCE between the successful PDE and the target PDE pinpoints the obstruction: it is the pressure's non-divergence-form coupling, not the Chebyshev step.

The open question "does div(u)=0 improve level-set distribution?" also emerged from the systematic comparison, as did the observation that fractional NS regularity at alpha=5/4 (Lions) exceeds what De Giorgi can prove (alpha=3/2 threshold).

## Protocol

1. Identify the barrier (e.g., exponent beta = 4/3)
2. List 4-6 model PDEs that share structural features but differ in key parameters (dimension, dissipation, nonlinearity type)
3. Compute the barrier quantity for each model PDE
4. Tabulate results — look for a universal formula or a systematic exception
5. For exceptions: identify the structural feature that enables the exception
6. For universality: the barrier is deeper than the specific PDE — reframe the attack target

## Distinction from Existing Patterns

Distinct from **comparison-exploration-pattern** (compares two approaches to the same problem; this compares one approach across multiple problems). Distinct from **gap-finding-in-existing-programs** (surveys attempts within one framework; this surveys a barrier across frameworks). Complementary to **decomposition-audit-before-attacking-barrier** (audit identifies the step; model PDE comparison identifies the mechanism behind the step).
