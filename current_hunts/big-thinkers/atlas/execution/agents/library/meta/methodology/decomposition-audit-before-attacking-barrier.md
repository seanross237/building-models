---
topic: Run decomposition audit before attacking a mathematical barrier
confidence: confirmed
date: 2026-03-30
source: "vasseur-pressure s2-meta-001"
---

## Lesson

**Always run a decomposition audit (line-by-line proof reading + sharpness classification) before attacking a mathematical barrier.** The temptation is to jump straight into computational testing or analytical variations. But understanding the proof structure first — which steps are sharp, which have slack, which parameters are free — prevents wasting budget on provably closed directions.

## Evidence

Vasseur-pressure Strategy-002, Exploration 001: One exploration reading Proposition 3 line-by-line produced a definitive narrowing of the attack surface from 5 open Track B directions down to 1. This saved at least 3 explorations that would have been wasted on provably closed paths:

- Modified functional approach: CLOSED (truncation function is conventional but effectively optimal — any truncation with the same three properties gives identical exponents)
- Improved Sobolev approach: CLOSED (H^1 → L^6 is provably sharp in 3D; L^{10/3} is the unique interpolation exponent)
- Optimized truncation approach: CLOSED (five free parameters analyzed; none can improve beta)
- Holder optimization: CLOSED (different pairings trade off between factors, cannot improve sum)
- **Structural Chebyshev improvement: OPEN** (the only step sharp for general functions but potentially loose for NS solutions)

## When to Apply

Before any phase that attempts to improve, circumvent, or close a known mathematical barrier. Specifically:

1. After Phase 0 (definition extraction) confirms the team understands the target quantity
2. Before Phase 1 (computational testing or analytical attack) begins
3. When the barrier is a proof-theoretic obstruction (a bound that can't be improved), not just a computational difficulty

## What to Require

A decomposition audit exploration should deliver:

1. **Step-by-step inequality chain** with the mathematical tool used at each step
2. **Sharpness classification** per step: SHARP (provably optimal), POTENTIALLY LOOSE (optimal for general functions, may not be tight for the specific equation), or UNKNOWN
3. **Sensitivity table**: dβ/dδ for each sub-exponent (how much would improving this step help?)
4. **Free parameter catalog** with assessment: EXHAUSTED (cannot improve beta), LIMITED (marginal improvement possible), or OPEN
5. **Attack surface narrowing**: which directions are provably closed, which remain open

## Relationship to Other Lessons

Distinct from `definition-extraction-gates-computation` (which ensures the team computes the RIGHT quantity; this ensures they attack the RIGHT step). Distinct from `gap-finding-in-existing-programs` (which surveys the literature landscape; this analyzes a single proof's internal structure). Complementary to `require-sensitivity-table-for-proof-analysis` (a goal-design variant requiring the specific output format).
