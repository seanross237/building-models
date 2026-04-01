---
topic: Constraint-catalog methodology for hard unsolved problems; verification vs. novelty tradeoff
category: missionary
date: 2026-03-27
source: riemann-hypothesis, strategy-001
---

# Strategy-001 Learnings: Riemann Hypothesis

## What Methodology Was Prescribed

A three-phase "Computational Constraint Cartography" protocol: (1) Extract mathematical constraints from multiple domains, each backed by computation; (2) Test specific operator candidates against the constraint catalog; (3) Synthesis and adversarial review. Designed for a hard unsolved problem where mapping the landscape first seemed prudent.

## How Well It Worked

**Good for ground-clearing, poor for novelty production.**

- Phase 1 was effective. Two explorations built a 10-point quantitative constraint catalog with reproducible code. The "every constraint must have a computation" rule was the strongest design choice — it prevented literature-summary explorations and produced concrete, verifiable results.

- Phase 2 produced useful negative results. All known Berry-Keating xp regularizations score 0/10 against the catalog. The trace formula reconstruction found a deep structural limitation (Gibbs phenomenon). Real symmetric arithmetic matrices can't reach GUE. These are all correct and well-characterized, but they're confirming what experts already know.

- Phase 3 was completely skipped. The strategizer wrote the final report after Phase 2 without running any synthesis or adversarial explorations. This is the biggest methodology failure: the strategy allocated 10 explorations but only used 6, and the most intellectually valuable phase (synthesis) was never attempted.

## What I'd Do Differently

1. **"Verify known results" is a valid Phase 1, but the strategy should have explicitly bounded it.** I should have written: "Phase 1 is ground-clearing. Everything here will confirm known results. The novelty comes in Phases 2 and 3." Instead, the entire strategy turned into Phase 1 work — testing known candidates against known predictions. A domain expert would recognize every finding as already published.

2. **Make Phase 3 (adversarial + synthesis) MANDATORY with minimum allocations.** The strategizer optimized for intellectual interest in Phase 2 and ran out of steam before Phase 3. Prescribe: "At minimum, exploration N-1 MUST be adversarial review and exploration N MUST be synthesis."

3. **The methodology should force constructive work, not just testing.** "Test candidates against constraints" is backward-looking by nature. A strategy for a hard unsolved problem needs at least some explorations that attempt something that hasn't been done. "Build an operator" is different from "test known operators."

4. **Scope the computation platform in the strategy.** Every exploration was limited by mpmath's ~2000-zero ceiling. If I'd specified "use precomputed zero tables from LMFDB or Odlyzko (millions of zeros)" in the strategy, the numerical results would have been 100x more precise and potentially novel in their precision.

5. **When an exploration crashes on a critical question, mandate a retry.** Exploration 005 (two-point correlation from prime pairs) was identified as the most important open question and it crashed. The strategizer chose not to retry because it wasn't "essential for the synthesis phase" — but the synthesis phase was never executed anyway. The methodology should say: "If an exploration fails on a question the strategizer judges critical, retry it before moving to synthesis."

## What Surprised Me

- **The strategizer's self-evaluation was accurate and honest.** The FINAL-REPORT says "No genuinely novel claims emerged that would survive expert scrutiny." This is correct. The honest assessment is valuable — no overclaiming.

- **The chain of reasoning across explorations was the most valuable output**, not any individual finding. GUE confirmed → super-rigidity from primes → xp alone fails → trace formula gives density not correlations → arithmetic matrices need complex structure. Each step constrained the next. This "insight chain" was emergent, not planned.

- **The constraint catalog was used as a checklist rather than a generative tool.** I designed it to be both: a way to test candidates AND a way to reverse-engineer new operators. The strategizer only used it as a checklist. Future strategies should explicitly ask the strategizer to use constraints as INPUT to a construction process.

- **Six of ten explorations were used.** The strategizer closed early because it felt it had exhausted the approach. This is actually good judgment — the remaining budget would have produced more negative results in the same frame. But the unused budget should have gone to synthesis/adversarial, not been left idle.

## Generalizable Lessons

1. **For hard unsolved problems, "map the landscape" strategies produce Tier 2-3 results (rigorous, evidenced) but not Tier 1 (novel).** Domain experts already know the landscape. Novelty requires going beyond the map — constructing, combining, or computing something that hasn't been done. Strategy-001 should have been the ground-clearing half of a two-strategy arc.

2. **The "constraint catalog" format is excellent for Phase 1-2 work.** It gives the strategizer a concrete, growing artifact to reference and a quantitative success metric for candidates. But it must be coupled with a constructive phase that uses the catalog as input.

3. **Negative results are valuable but only once.** "xp regularizations fail" is useful. "Trace formula can't reconstruct individual zeros" is useful. But a whole strategy of negative results doesn't advance the mission. One ground-clearing strategy is enough; strategy-002 must be constructive.

4. **Computation scale matters more than computation count.** Five explorations with 2000 zeros each produce five confirmations of known results. One exploration with a million zeros might produce a genuinely novel measurement. Prescribe the data scale in the strategy, not just "compute."

5. **Parallel Phase 1 explorations (from classicality-budget learnings) would have helped here too.** The first two explorations were sequential but independent. Running them in parallel would have freed budget for Phase 3.
