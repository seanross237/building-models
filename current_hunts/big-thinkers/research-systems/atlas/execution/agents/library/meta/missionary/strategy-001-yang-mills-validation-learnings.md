---
topic: Adversarial proof audit for validation missions
category: missionary
date: 2026-03-28
source: yang-mills-validation, strategy-001
---

# Strategy 001: Yang-Mills Validation — Learnings

## What was prescribed

Three-phase adversarial audit: (1) Independent rederivation + novelty assessment + convention verification in parallel, (2) Numerical extensions (large lattice, SU(3), dimensional analysis), (3) Adversarial synthesis. 8 explorations, all mandatory, adversarial posture throughout. "Try to find errors, not confirm claims."

## What worked

1. **Adversarial posture is the most important rule for validation missions.** E007 found a genuine proof gap (Step 2: HessS formula is not an identity at generic Q). Without the adversarial mandate, this would likely have been glossed over. The gap is subtle — the formula overestimates λ_max for most Q, but the PSD inequality fails in some directions.

2. **Three parallel Phase 1 explorations were perfectly scoped.** Each addressed an independent question (correctness, novelty, convention). Results cross-pollinated: E001's "counterexample" was resolved by E003's convention verification, and E002's novelty assessment was cleanly independent.

3. **Convention precision saved the mission.** Specifying LEFT vs RIGHT formula explicitly in GOAL.md was critical. E001 independently reproduced the prior mission's convention error — proving that "independent rederivation" can reproduce known bugs if the convention isn't pinned down. Lesson: specify the perturbation convention (left vs right) explicitly in every math exploration GOAL.

4. **Phase 2 extensions produced corrections, not just confirmations.** The SU(3) exploration (E005) found N vs N² error in the conjecture. The d=5 exploration (E006) found the prior mission's odd-d formula was wrong. Validation isn't just about confirming — it's about finding the corrections.

5. **190+ configurations across multiple axes (L, N, d) with 0 violations is strong evidence.** The numerical evidence is more convincing than any single proof chain, precisely because it spans multiple dimensions of the parameter space.

## What didn't work

1. **"Independent rederivation without reading the prior proof" was a double-edged sword.** E001 independently re-derived β < 1/6 (good!) but used the wrong B□ formula (bad!). The explorer wasn't reading the prior proof, so it independently reproduced the very error the prior mission had corrected. Fix: either pre-load the convention or require the explorer to derive the formula from scratch (don't let it look up any version of the formula).

2. **E003 explorer stalled twice on a computation-heavy goal.** Math explorers with complex formula verification tasks still stall. The strategizer's workaround (running the computation directly) was effective but burned strategizer context. Fix: add "write code IMMEDIATELY, do not reason about the formula symbolically for more than 2 minutes" to math-heavy goals.

3. **E008 (final synthesis) timed out.** The strategizer incorporated its work into FINAL-REPORT directly. Final synthesis explorations may be unnecessary when the strategizer has enough context. Consider making the strategizer write the final report directly instead of delegating it.

4. **L=8/L=16 not reached.** E004 got to L=6 but the explorer got stuck in a 2.5-hour thinking loop. For large-scale computation, specify synchronous execution and timeout discipline.

## Generalizable lessons for validation missions

1. **Validation missions are 1-2 strategy affairs.** Strategy 001 addressed all 5 mission items. A second strategy should focus narrowly on repairing the one gap found, not re-exploring.

2. **The most valuable finding in a validation mission is a SPECIFIC gap, not a vague concern.** "Step 2 is not an identity but the λ_max inequality holds numerically" is far more useful than "the proof seems fishy." Design explorations to produce specific findings.

3. **Pre-load the exact claims to validate.** The strategy included a section with the prior mission's claims, prior mission file paths, and the specific proof chain steps. This saved significant context in every exploration.

4. **Convention verification deserves its own exploration.** Don't roll it into the proof rederivation — they'll interfere. E003 (convention-only) resolved the critical question that E001's "independent" rederivation muddied.

5. **Numerical extensions as Phase 2 work well because they're independent of the proof audit.** Even when the proof has a gap, the numerics remain valid evidence. The phases should be truly parallel in this sense.

## Methodology effectiveness: 8/10

The strategy found the gap, confirmed the novelty, corrected two errors, and covered all 5 mission items in 8 explorations. The main weakness was explorer stalling (E003, E004, E008), which the strategizer worked around effectively. The adversarial posture was the right call — without it, the proof gap would have been missed.
