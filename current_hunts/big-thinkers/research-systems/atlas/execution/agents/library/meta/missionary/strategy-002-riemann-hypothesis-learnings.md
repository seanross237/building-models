---
topic: Tournament methodology for constructive research; adversarial review as essential quality control
category: missionary
date: 2026-03-27
source: riemann-hypothesis, strategy-002
---

# Strategy-002 Learnings: Riemann Hypothesis

## What Methodology Was Prescribed

An "Operator Construction Tournament" — three parallel constructive attempts (complex arithmetic matrices, optimization-based reverse engineering, two-point formula kernel operator), scored against a constraint catalog, deepened in Phase 2, with mandatory adversarial review in Phase 3. This was explicitly designed as a constructive complement to S-001's verification/testing approach.

## How Well It Worked

**The tournament format was the best methodology this mission has used.**

- Phase 1 parallel tournament produced one clear winner (C1, β=1.675) and two useful negatives (optimization fails due to non-differentiable loss; two-point formula needs careful normalization). The scoring against the catalog gave clear signals for Phase 2 allocation.

- Phase 2 deepened the winner and filled mandatory gaps (Berry saturation, two-point formula redo). Every exploration added specific, quantitative knowledge. The Gauss sum prime sweep and Dirichlet character impossibility proof were the mission's strongest novel results.

- **Phase 3 was critical and caught two false claims.** E007's adversarial review showed C1's pair correlation PASS was generic (any GUE matrix passes) and unstable (0/20 individual realizations pass). E009 showed C1's intermediate Δ₃ was generic GUE finite-size behavior, not arithmetic. Without Phase 3, the final report would have contained two overclaims.

**The two surviving novel claims (N²/p scaling, Dirichlet impossibility) are genuine but modest.** Both are specific, proved/computed, and absent from the literature, but both follow from general principles experts would consider expected. They're Tier 1 in form (novel, not previously published) but not in impact (an expert would say "interesting, expected").

## What I'd Do Differently

1. **The optimization entry (Tournament Entry B) was predictable dead end.** Eigenvalue statistics of sorted eigenvalues are piecewise-constant functions of matrix entries — non-differentiable by construction. I should have warned about this in the strategy or required gradient-free methods from the start. **Lesson: think through the mathematical feasibility of each tournament entry before prescribing it.**

2. **The strategy should have explicitly targeted the super-rigidity gap from Phase 2 onward.** By E004, it was clear that the Δ₃ gap (0.24 vs 0.155) was the central problem, but no exploration was designed to bridge it. The strategy focused on GUE statistics (easy to reproduce) rather than beyond-GUE rigidity (hard, actually important). **Lesson: the strategy should name the hardest target explicitly and allocate explorations to it, not just to the closest targets.**

3. **Explorer death rate (4/9 requiring manual completion) is the #1 operational problem.** The strategizer's workaround (manual recovery from computed data) was effective but expensive. The pattern: explorer computes results → enters extended thinking loop → writes skeleton with placeholders → dies. **Lesson: instruct "write each section immediately after its computation, mark [SECTION COMPLETE]" in every goal. Don't let explorers defer writing.**

4. **Two of three Phase 1 entries hit usage limits (E002, E003).** Parallel launch is good for wall-clock time but risky when explorers are unreliable. The strategizer correctly ran E006 as a redo of E003's failed normalization. **Lesson: budget at least one redo slot for parallel Phase 1.**

## Generalizable Lessons

1. **Tournament → Deep Dive → Mandatory Adversarial is an effective three-phase arc for constructive research.** The scoring metric (constraint catalog) makes the tournament objective and the Phase 2 allocation evidence-based. Phase 3 must be mandatory with minimum allocation (not optional).

2. **Adversarial review is the highest-ROI phase.** Strategy-001 skipped it and reported claims that wouldn't survive. Strategy-002 ran it and caught two false claims. The adversarial review (E007) was the single most valuable exploration in the entire strategy. **Make adversarial the FIRST thing in Phase 3, not the last.**

3. **"Construction" strategies naturally produce better novelty than "testing" strategies.** S-001 (test known candidates) produced zero novel claims. S-002 (build new operators) produced two. Building forces the explorer to create something new; testing only verifies what's known.

4. **The most important scientific result often emerges from the negative space.** The super-rigidity gap (Δ₃ = 0.155 vs 0.24) is a more important result than either novel claim — it precisely defines what any successful operator construction MUST achieve. But it wasn't the strategy's objective; it emerged as a side effect of the construction attempts failing to match it.

5. **Prescribe the specific control experiments in the strategy.** E007's null-matrix comparison and E009's flat-amplitude test were the most decisive computations. Both were designed by the strategizer, not prescribed. Future strategies should say: "For any positive claim, immediately test against the simplest null hypothesis (flat amplitude, random phases, different ensemble)."
