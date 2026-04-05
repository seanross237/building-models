---
topic: Focused-attack strategy for a quantitative gap; diminishing returns signal for mission completion
category: missionary
date: 2026-03-28
source: riemann-hypothesis, strategy-003
---

# Strategy-003 Learnings: Riemann Hypothesis

## What Methodology Was Prescribed

A focused, final strategy: "Bridging the Super-Rigidity Gap." Phase 1 attacked the gap from two independent angles (off-diagonal form factor corrections + Li criterion computation). Phase 2 deepened the best finding. Phase 3 was mandatory adversarial + synthesis. Every exploration was prescribed to target a specific quantitative question — no surveys, no open-ended construction.

## How Well It Worked

**The structure was correct but the primary attack failed for a predictable reason.**

- E001 (off-diagonal form factor) was designated "the single most important computation of the entire mission." It FAILED — the Berry-Keating perturbative expansion requires T >> 10^10, completely outside the regime of the first 2000 zeros (T ≈ 1682). This should have been anticipated from the asymptotic nature of the formula. The strategy put its highest-value computation on an approach that was fundamentally invalid for the available data.

- E002 (Li criterion) opened a genuinely novel line — comparing Li coefficients between zeta zeros and GUE, something never done in the literature. This was the strategy's best moment. But the finding (ratio < 1 crossover) was ultimately an artifact of the comparison methodology.

- The adversarial chain (E007→E008→E009) was the strategy's most valuable sequence. E007 confirmed the Li comparison was genuinely novel (4/5 novelty score). E008 found truncation sensitivity. E009 delivered the decisive refutation. This is the adversarial process working exactly as designed.

- E004 (N²/p verification) correctly killed Claim A from S-002 (universality rejected). This demonstrates the value of verification explorations in later strategies.

- E005 navigated to the WRONG DIRECTORY (strategy-002 instead of strategy-003). Basic operational failure that wasted an exploration. The "CWD check as Task 0" fix worked for subsequent explorations.

## What I'd Do Differently

1. **Check whether a formula is valid in the target regime BEFORE making it the centerpiece of a strategy.** Berry-Keating's perturbative expansion in powers of 1/⟨d⟩² requires ⟨d⟩ >> 1. At T=1682, ⟨d⟩ = 0.89 — the expansion diverges. A 5-minute back-of-envelope check (compute ⟨d⟩ at T=1682, compare to 1) would have flagged this. **Lesson: include a "feasibility pre-check" as exploration 0 or as a requirement before the strategy is finalized.**

2. **Don't designate a single computation as "the most important of the entire mission."** It creates psychological commitment that makes the strategizer reluctant to pivot when it fails. E001 failed and the strategy lost its center of gravity. Better: "two independent attacks on the gap; if one fails, the other carries the strategy."

3. **The Li coefficient investigation consumed 4 of 9 explorations (E002, E007, E008, E009) chasing what turned out to be an artifact.** The adversarial chain was correct and necessary, but it monopolized the strategy's budget. After E002 found the crossover and E007 confirmed novelty, a more efficient approach would have been: E008 = "run the decisive convergence test immediately" (which is what E009 ended up being). Instead, E008 did partial validation, required E009, and the two explorations could have been one.

4. **Explorer access to papers matters.** The strategy specified "extract formulas from Berry 1985, Bogomolny-Keating 1996." Math Explorers can't access papers (no web). Standard Explorers find abstracts, not equations. The explorer had to reconstruct formulas from fragments and secondary sources, introducing errors. **Lesson: provide the key formulas DIRECTLY in the GOAL.md**, extracted from papers by the strategizer or missionary before launch.

## Generalizable Lessons

1. **Three-strategy arc (survey → construct → focus) is natural for hard unsolved problems, but expect diminishing returns.** S-001 (6 explorations, 0 claims), S-002 (9 explorations, 2 claims), S-003 (9 explorations, 0 claims, 1 prior claim retracted). The system extracts most of its value from strategies 1-2. Strategy 3 is primarily for verification, adversarial review, and closing out open questions. Don't expect new breakthroughs.

2. **Verification explorations in later strategies are cheap and high-value.** E004 (N²/p verification) and E009 (Li convergence) each took one exploration and produced decisive results. Budget 1-2 verification slots in every strategy after the first.

3. **The adversarial self-refutation chain (find → validate → refute) is the most intellectually honest output of the system.** The Li crossover went from "novel 4/5" to "definitively refuted" across E007→E008→E009. This is better than a false positive. The system works.

4. **"Focused attack on one gap" strategies are brittle.** If the primary attack fails (E001), the strategy has nowhere to go. "Two independent attacks + adversarial review" is more robust than "one focused attack + backup + adversarial review."

5. **24 explorations across 3 strategies may be the natural scale for a mission on a hard unsolved problem.** After that, the system has mapped the landscape, tested constructions, found what it can find, and verified its claims. Further strategies would need genuinely new mathematical ideas, not technical fixes. The "technical fixes" recommendations from the strategizer (unfolded Li comparison, K→Σ₂ normalization) are diminishing-returns work.
