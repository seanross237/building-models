---
topic: Three-phase reconnaissance for unsolved math problems
category: missionary
date: 2026-03-27
source: yang-mills, strategy-001
---

# Strategy-001 Learnings: Probe-Attack-Synthesize for Hard Unsolved Problems

## What the Strategy Prescribed

Three-phase "Probe-Attack-Synthesize" methodology: (1) Precision Probing — map technical obstructions at the theorem level, (2) Computational Attack — write code to test specific obstructions, (3) Synthesis — combine findings into novel contributions. Budget of 10 explorations allocated 3-4-3 (actual: 2-4-4).

## How Well It Worked

**Very well as ground-clearing. Limited for novelty production.** This matches the Riemann hypothesis missionary's finding that mapping strategies produce Tier 2-3 results but rarely Tier 1 novelty. The key difference: our computational attacks produced one genuine Tier 3 result (Adhikari-Cao bounds vacuousness) because the "computation mandatory" rule forced quantitative testing of claims.

- Phase 1 (2 explorations): Efficiently mapped Balaban's program and constructive QFT landscape. The UV/IR reframing (UV solved by MRS 1993, entire difficulty is IR) was the most important strategic insight and emerged naturally from the probing methodology.
- Phase 2 (4 explorations): Produced the strategy's strongest results. Lattice SU(2) simulations confirmed confinement. Finite-group convergence study was partially novel. Adhikari-Cao vacuousness computation was the most valuable output.
- Phase 3 (4 explorations): Novelty search, obstruction synthesis, and adversarial review. The adversarial review (exploration 10) was the single most valuable exploration — found a real definitional error that paradoxically strengthened the main claim.

## What I'd Do Differently

1. **Mandate adversarial review at exploration 6-7, not 10.** The Δ_G definitional error was caught at the very end. If caught earlier, the remaining explorations could have used corrected values and gone deeper. Multiple meta-library entries confirm this pattern — adversarial review early is a universal lesson.

2. **Bound the reconnaissance phase explicitly.** I said "~3 explorations" for Phase 1. The strategizer correctly used only 2, but this was its own good judgment, not my methodology. I should have said: "Phase 1 is ground-clearing. Maximum 3 explorations. Everything here confirms known results. Novelty starts in Phase 2."

3. **Prescribe computation scale, not just "computation."** The convergence rate claim (3 data points for a power law) was embarrassing in adversarial review. If I'd specified "minimum 5 data points for any scaling claim, minimum 10^5 samples per measurement," this overclaim wouldn't have happened.

4. **Include one constructive/formalization exploration.** The mission suggested Lean formalization. Strategy 001 never attempted it. Ground-clearing + computation was natural for a first strategy, but one "attempt to prove or formalize something" exploration would have tested a different modality and possibly found hidden assumptions.

5. **The RG+Bakry-Émery idea should have been tested, not just identified.** It was the most exciting output of the strategy, but it came out of exploration 9 (synthesis) with no explorations left to test it. If the synthesis phase had come at exploration 7, explorations 8-10 could have tested this computationally.

## What Surprised Me

- **The strategizer's best meta-contribution was the obstruction atlas format.** The 9-approach table with classifications (TRACTABLE / FUNDAMENTAL BARRIER / HARD) and 5 bottleneck theorems is a genuinely useful artifact — more useful than any individual computation.

- **Explorer crashes are a real budget cost.** 3 of 10 explorations had operational issues (context pollution from other missions, tmux crash, timeout). This is a ~30% failure rate. Strategies should account for this by building in slack or having fallback plans.

- **The Shen-Zhu-Zhu discovery was the most strategically important finding**, yet it wasn't what any exploration was specifically looking for. It emerged as a side-effect of the comprehensive obstruction mapping. This confirms the meta-library lesson that survey explorations at the start pay for themselves.

- **Negative results can be Tier 3.** The AC vacuousness computation is a negative result (these bounds don't work) but it's quantitative, novel, and adversarially verified. The key was that it was a COMPUTATION of a negative result, not just an argument.

## Generalizable Lessons

1. **First strategy = ground-clearing; second strategy = constructive.** For hard unsolved problems, the first strategy should map the landscape and find the best attack vector. The second strategy should focus all resources on that vector. Don't try to do both at once.

2. **"What exactly does [recent paper] prove?" is the highest-value probe question.** Explorations 004 and 006 (which probed Adhikari-Cao, Chatterjee, SZZ) produced the most strategically valuable output because they asked for exact theorem statements, not summaries.

3. **Require mathematical specificity in the methodology, not just the goals.** "Map obstructions at the theorem level" worked better than "explore the landscape" because it forced explorers to find and state precise results.

4. **Quantitative negative results are publishable; qualitative ones are not.** "AC bounds are vacuous" (Tier 1-2) vs. "AC bounds are 57-69x vacuous with diverging β_min" (Tier 3).

5. **Pre-load ALL prior strategy findings into Strategy N+1.** The complete obstruction atlas, novel claims, and identified directions should be explicitly given to the next strategizer so it doesn't redo any mapping work.
