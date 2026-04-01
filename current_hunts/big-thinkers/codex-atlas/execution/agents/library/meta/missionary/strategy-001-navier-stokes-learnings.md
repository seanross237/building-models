---
topic: Catalog-Measure-Tighten for computational inequality analysis
category: missionary
date: 2026-03-30
source: navier-stokes, strategy-001
---

# Strategy-001 Navier-Stokes Learnings

## What the methodology was

Three-phase **Catalog → Measure → Tighten** with a cross-phase rule requiring every identified inequality to be written as computable Python function pairs (bound vs actual). Prescribed computation scale: ≥5 Reynolds numbers, ≥3 initial conditions, two-resolution convergence. Budget: 20 explorations, 8 used.

## What worked exceptionally well

1. **Cross-phase computable function pairs.** Requiring every inequality to be written as `bound(u)` and `actual(u)` Python functions was the single best design decision. It made the catalog immediately actionable (Phase 1 → Phase 2 transition was seamless), forced precision in the catalog, and created reusable infrastructure that every subsequent exploration built on. **This should be a standard rule for any mission involving inequalities, estimates, or bounds.**

2. **Decomposition with multiplicative consistency checks.** Requiring α × β × γ = total slack, verified at every timestep, caught a critical error — exploration 002's rough estimates (9× geometric / 18.6× Ladyzhenskaya) were corrected by exploration 004 (5.3× / 31×). The correction reversed the strategic priority (Ladyzhenskaya dominates, not Hölder). **Always require consistency checks in decomposition explorations.**

3. **Survey first paid off again.** The literature catalog (exploration 001) with Tao's generic/NS-specific classification changed the entire strategic direction. This is now validated across 6+ missions. The innovation here was requiring a structural classification (generic vs NS-specific), not just a catalog.

4. **Prescribed computation scale.** Requiring ≥4 Reynolds numbers, convergence checks at two resolutions, and ≥5 initial condition types meant results had real statistical weight. The strategizer was disciplined about this.

5. **Budget efficiency.** 8 of 20 explorations used. The strategizer correctly stopped when the Phase 3 tightening paths were mapped rather than spending 12 more explorations on diminishing returns. This was the right call — the remaining budget is better spent on a focused constructive strategy.

## What didn't work

1. **Phase 3 (Tighten) never actually tightened.** The methodology said "tighten the loosest one" but didn't prescribe HOW. It listed approaches (sharp constant, better exponent, structural argument) without requiring a proof attempt. The result: Phase 3 became "characterize what a tighter bound would look like" rather than "prove a tighter bound." **For constructive phases, require a specific proof attempt with a stated theorem target.**

2. **Literature survey should have preceded the spectral Ladyzhenskaya computation.** Exploration 006 (spectral Ladyzhenskaya) was predictably a dead end if you read Tao (2014). The strategizer recognized this in hindsight. **When a direction depends on whether harmonic analysis alone can improve things, check for known obstructions FIRST.**

3. **Single-IC dependence.** Most findings (decomposition, BMO ratios, conditional bound) are Taylor-Green-specific. The adversarial search (exploration 003) tested multiple ICs for vortex stretching slack but not for the other quantities. **Cross-phase rules should require multi-IC validation for every key finding, not just the headline number.**

4. **Adversarial review was standard-only.** The review caught logical errors and did novelty search but couldn't independently recompute. A math explorer adversarial review on the 2-3 most important numerical claims would have been more powerful. **Budget one math-explorer adversarial and one standard-explorer adversarial for missions with heavy computation.**

## Surprising findings about methodology

- The correction of exploration 002 by exploration 004 was the single most valuable moment. It's worth designing strategies that expect to correct their own early estimates. One approach: always run a dedicated decomposition exploration rather than trusting back-of-envelope estimates.
- The strategizer pivoted well when directions failed (spectral Ladyzhenskaya → BKM). But the pivots were reactive, not proactive. The methodology could have structured alternative paths from the start.
- 8 explorations was the right scale for a ground-clearing + initial tightening strategy on a Millennium-adjacent problem. Consistent with the 24-30 exploration total seen in Yang-Mills and Riemann missions across 3 strategies.

## Lessons that generalize

1. **Cross-phase computable deliverables** (not just text reports) dramatically improve phase transitions. For inequality missions: function pairs. For proof missions: stated lemma targets. For construction missions: code artifacts.
2. **Decomposition explorations need multiplicative/additive consistency checks.** These catch real errors and are trivially cheap.
3. **Tightening phases need theorem targets.** "Try to prove a tighter version" produces characterization. "Prove this specific statement or identify exactly where the proof breaks" produces either a result or a precise obstruction.
4. **Match adversarial review type to exploration type.** Standard reviewers for logical claims + novelty. Math reviewers for numerical claims + recomputation.
5. **Ground-clearing strategies reach Tier 2-3. Constructive strategies are needed for Tier 4-5.** This is now validated across 8+ missions. The two-strategy arc (survey → construct) or three-strategy arc (survey → construct → verify) is the natural pattern.
