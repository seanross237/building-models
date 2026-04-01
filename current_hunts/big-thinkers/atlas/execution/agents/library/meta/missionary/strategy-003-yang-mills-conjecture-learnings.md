---
topic: Phase 0 upstream verification can redirect entire missions
category: missionary
date: 2026-03-29
source: yang-mills-conjecture, strategy-003
---

# Strategy 003 Learnings: Yang-Mills Conjecture

## What methodology was prescribed

A verify-first pipeline with mandatory Phase 0:
- Phase 0 (1 exploration, BLOCKING): Verify counterexample + clarify SZZ framework
- Phase 1 (1 exploration): Direction setting based on Phase 0
- Phase 2 (3-4 explorations): Execute based on scenario resolution
- 7-exploration budget

## How well it worked

**Exceptionally.** Phase 0 was the most valuable single exploration in the entire 20-exploration mission. It discovered that:
1. Conjecture 1 (on M(Q)) is FALSE — λ_max(M) = 6d, not 4d
2. The correct proof target is the Hessian HessS, not M(Q)
3. The two are equal only at flat connections; elsewhere HessS has a large curvature correction

This discovery invalidated the foundational assumption of Strategies 001-002 but opened a correct path forward. Without Phase 0, the mission would have continued pursuing a false conjecture.

**Strategy execution was efficient:** 6 of 7 explorations used. The strategizer correctly skipped Phase 1 (direction already clear from Phase 0), correctly identified the decoherence lemma as the key proof target, and correctly pivoted when it was falsified.

## Critical lesson: Phase 0 can redirect entire missions

The Strategy 002 meta-learning said "verify upstream logic before proof construction." Strategy 003 applied this as a mandatory Phase 0 and it produced the mission's most important discovery. **This is the highest-ROI exploration possible — it either confirms the target or prevents wasted strategies.**

Every strategy should start with Phase 0 if there is ANY uncertainty about:
- Whether the proof target implies the desired conclusion
- Whether the mathematical object being bounded is the correct one
- Whether the problem statement matches the source paper exactly

## Other lessons

1. **"N configs with zero violations" ≠ "the bound holds."** E004 tested 2000+ configs for ||C|| ≤ 10 and found zero violations. E005's gradient ascent found ||C|| = 11.68 (a 17% violation). The 48% gap between random and adversarial maxima is the lesson: always gradient-ascend on the EXACT quantity being bounded, not just test configs.

2. **Code written but not run is a budget planning failure.** E006 wrote code for the two most promising approaches (concavity, per-plaquette H bound) but only ran the LEAST promising one (anti-correlation bound, which failed). This happened because the anti-correlation bound was tested first and the exploration ran out of time. Lesson: in a multi-approach exploration, run the MOST promising approach first. Or: allocate separate explorations to each promising approach.

3. **Norm-additive bounds are a dead end class.** |λ(D+C)| ≤ |D|+||C|| loses eigenvector-level cancellation. For d≥3, this gap is structural. Any future proof must respect the cancellation — likely through concavity, per-plaquette direct bounds, or Fourier analysis.

4. **Library claims must be verified numerically before building strategies on them.** The library claimed HessS = (β/2N)M (from the prior yang-mills mission). This was wrong. Two strategies were built on this assumption. Phase 0 caught it, but the damage was already done (15 wasted explorations on M(Q) instead of HessS).

5. **Anti-instantons are the universal stress test for lattice gauge theory bounds.** Every falsification in this strategy involved anti-instanton or Z₂ configurations. Future goals should ALWAYS include these as mandatory test cases.

## Generalizable principles

1. **Phase 0 is non-negotiable for proof strategies.** The cost (1 exploration) is tiny compared to the cost of pursuing the wrong target (entire strategies).

2. **Gradient ascent on the exact bound target, every time.** Random config surveys give false confidence. The gap between random and adversarial can be 50%+.

3. **Run most promising approach first in multi-approach explorations.** Don't let time run out on the best ideas because you tested the least promising first.

4. **Library entries from prior missions should be marked with verification status.** "Proved" vs "computed" vs "assumed" — and strategies should verify assumed claims before building on them.

5. **Paradigm shifts (proving the wrong conjecture → finding the right one) are MORE valuable than incremental progress.** Strategy 003's falsification of Conjecture 1 and identification of the correct target was worth more than proving 10 more special cases.
