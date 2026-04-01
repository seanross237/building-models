---
topic: Three-phase decompose-construct-verify pipeline for proof problems
category: missionary
date: 2026-03-28
source: yang-mills-conjecture, strategy-001
---

# Strategy 001 Learnings: Yang-Mills Conjecture

## What methodology was prescribed

A three-phase **Decompose-Construct-Verify** pipeline with 10-exploration budget:
- Phase 1: Three parallel algebraic decompositions (different mathematical lenses)
- Phase 2: Synthesis → proof attempt → mandatory adversarial → second attempt
- Phase 3: Consolidation

Key rules: compute first always, one approach per exploration, mandatory adversarial review, pre-load dead ends, incremental writing.

## How well it worked

**Extremely well.** 8 of 10 explorations used, produced a complete proof of a significant partial case plus precise gap characterization. The result (Combined Bound Lemma + cube-face inequality) was genuinely novel.

**Phase 1 (parallel decompositions) was the star.** All three explorations produced complementary findings. The cube-face grouping (E002) became the proof route, but E001's single-link theorem and E003's parallelogram identity provided structural support. Running them in parallel was high-value — each took ~1h and none depended on the others.

**Phase 2 adaptation was critical.** E005 stalled (47 min extended thinking), producing no proof but a KEY reformulation (3×3 matrix). The strategizer correctly deviated from the prescribed sequence (was supposed to do adversarial review next, but there was nothing to review), and instead launched E006 as a focused proof attempt that SUCCEEDED. This adaptation — repurposing the adversarial slot for a second proof attempt — was the right call.

**Adversarial review (E007) justified itself.** Found a real gap (3D vs 9D eigenspace) that prevented an overclaim. Without it, the final report would have claimed a complete proof when it wasn't.

## What I would do differently

1. **Limit goal stages to 4-5, never 12.** E003 had 12 stages and the explorer ran out of context at 70%. Should have been 4 focused stages with clear priority ordering.

2. **ONE approach per proof exploration, never three.** E005 presented three alternative proof approaches and the explorer stalled for 47 minutes trying to consider all three. E006 was given ONE target ("prove λ_max ≤ 64 for the 3×3 matrix") and succeeded cleanly. This is the single most important lesson.

3. **Pre-check key identities before pursuing proof technique.** E008 tried to extend E006's proof to the full eigenspace without first checking whether the trace identity (heart of the proof) held for general patterns. It doesn't. Wasted an exploration. Should have had a computational pre-check step.

4. **Cap extended thinking time in the goal.** E005 stalled for 47+ minutes. Goals should explicitly say: "If stuck in extended thinking for >10 minutes, write current state to file and pivot."

5. **Preload more aggressively.** E002 partially rederived the active/inactive plaquette split, which was already known. Pre-loading established structural features saves rederivation time.

## Surprises

- **The proof was discovered computationally, not algebraically.** The Combined Bound Lemma was found by E006 through numerical experimentation (testing subadditivity, finding it fails, then testing factorization patterns). The algebraic proof came AFTER the computational discovery. This strongly validates the "compute first" methodology.

- **Partial results from failed explorations had critical downstream value.** E005 "failed" (timed out), but its 3×3 matrix reformulation was the foundation for E006's success. This is a general pattern: exploration failure != wasted budget.

- **The strategizer's best decisions were deviations from the strategy.** Repurposing E006, choosing not to spend the last 2 explorations on gap closure — these improved outcomes. Good strategies should have enough structure to guide but enough flexibility for adaptation.

## Generalizable lessons

1. **For proof problems, the three-phase structure works**: decompose → construct → verify. But be flexible in Phase 2 — failed proof attempts should trigger re-scoping, not mechanical adversarial review of nothing.

2. **Parallel decompositions in Phase 1 are high-value** when the problem admits genuinely different algebraic perspectives. All three will usually produce something useful, and the synthesis exploration identifies which to pursue.

3. **"Compute first" is the methodology's most important rule.** It prevents false claims, guides proof search, and often discovers the key identity directly.

4. **Budget discipline matters.** The strategizer's decision to consolidate at 8/10 instead of chasing the last gap was correct — the marginal explorations would have needed a fundamentally different technique (SDP/SOS) better suited for a new strategy.

5. **Adversarial review should come AFTER a claimed proof, not at a fixed position in the sequence.** The strategy prescribed E6=adversarial, but E005 produced no proof. The strategizer correctly adapted.
