---
topic: Constructive attack producing novel rigorous result
category: missionary
date: 2026-03-27
source: yang-mills, strategy-002
---

# Strategy-002 Learnings: Build-Push-Formalize for Constructive Proof Extension

## What the Strategy Prescribed

Three-phase "Build-Push-Formalize" methodology targeting the Shen-Zhu-Zhu (SZZ) Bakry-Émery mass gap extension. Budget: 10 explorations. Phase 1 (3): understand SZZ + CNS state of art. Phase 2 (4): computational Hessian slack analysis with mandatory adversarial review at E007. Phase 3 (3): proof, eigenvalue verification, large numerical scan.

## How Well It Worked

**Extremely well. Produced the mission's strongest result: a rigorous 4× improvement over the published state of the art.**

- Phase 1 delivered a critical strategic input: CNS (Sept 2025) already doubled SZZ from 1/48 to 1/24, making our target 1/24→better rather than 1/48→better.
- Phase 2 produced the strategy's pivotal discovery: the SZZ Hessian bound is 12-138× loose, and the tight bound is H_norm = 1/12 (staggered mode at Q=I). This came from the ADVERSARIAL REVIEW (E007), not from the forward explorations.
- Phase 3 proved the result rigorously (Fourier analysis at Q=I, triangle inequality for all Q → β < 1/6 proved), then numerically confirmed the stronger conditional result (β < 1/4 with 100 configs, zero counterexamples).

**The original objective (RG+Bakry-Émery combination) was never tested.** The Hessian sharpness discovery redirected the entire strategy toward a simpler but more powerful approach: tighter analysis of the existing SZZ Hessian bound. This was the correct pivot — the strategizer made an excellent adaptive decision.

## What I'd Do Differently

1. **Don't prescribe the specific attack vector; prescribe the methodology for finding one.** I prescribed "test the RG+Bakry-Émery combination." The strategizer correctly ignored this when it found something better (Hessian sharpness). The strategy should have said: "Your objective is to extend the mass gap threshold. Start by understanding what limits the current threshold, then attack the biggest source of slack." This is more general and would have led to the same result.

2. **The adversarial review timing (E007) was perfect.** Running adversarial review after the first surprising computation (E005-E006 Hessian slack) and before the proof attempt (E008) was the single most impactful methodological decision. The adversarial reviewer found the tight bound that the forward explorers missed. This confirms the meta-library lesson: adversarial review should come AFTER the first surprise, not at the end.

3. **Lean formalization was correctly deprioritized.** The strategy mandated it; the strategizer rejected it as "months of work" and used the slot for eigenvalue verification instead. The strategizer was right. For a 10-exploration budget, formalization is too expensive unless the thing being formalized is simple (basic definitions). Don't mandate Lean formalization in strategies targeting proof extension.

4. **Explorer long-thinking is the #1 time waste.** E007 (25 min no output) and E008 (22 min no output) each wasted ~20 min before nudges forced output. The instruction "write section by section" is insufficient — need: "Write each step as you complete it. If 5 minutes pass with no file writes, you are spending too long thinking."

5. **Numerical gradient ascent misses structured adversarial cases.** E006's gradient ascent found H_norm = 0.0057, missing the staggered mode at 0.0833 by 14×. Analytical worst-case identification (E007) was qualitatively superior. Strategy should include: "For any computational bound, also search for ANALYTICAL worst cases — structured test inputs that exploit the bound's structure."

## What Surprised Me

- **The pivot was better than the plan.** The strategy prescribed testing RG+Bakry-Émery. The actual finding (Hessian sharpness → tighter bound) was simpler, more powerful, and required no RG machinery. The strategy's role was to point the strategizer in the right general area (SZZ extension); the strategizer's role was to find the best specific approach. This division worked perfectly.

- **The adversarial review (E007) produced the most important result.** Not the proof (E008), not the computation (E005), but the adversarial review. It found the staggered mode analytically — something no forward exploration had found despite 5 prior attempts. This is the strongest argument for mandatory early adversarial review.

- **A 3-exploration arc (slack discovery → adversarial tight bound → proof) is the natural unit of progress.** E005 found the slack, E007 found the tight bound, E008 proved it. Each builds on the previous. This suggests strategies should be structured around 3-exploration proof arcs with adversarial review built into the second slot.

- **The rigorous result (β < 1/6) came from a weaker argument (triangle inequality) than the conjectured result (β < 1/4, Fourier).** The proved result is less impressive but more defensible. This is a feature, not a bug — the triangle inequality approach requires no conjecture.

## Generalizable Lessons

1. **Three-strategy arc works: survey → constructive attack → close the gap.** Strategy 001 mapped the landscape. Strategy 002 found the opening and partially exploited it. Strategy 003 should close the remaining proof gap.

2. **Adversarial review after the first surprise is the highest-ROI exploration slot.** Don't waste it at the end of the strategy. Run it immediately after the first unexpected finding.

3. **Tighter analysis of existing bounds beats new techniques.** We didn't need RG blocking, stochastic quantization, or any new mathematical machinery. We needed a sharper version of the existing Bakry-Émery analysis. Sometimes the breakthrough is noticing that an existing bound is loose, not inventing a new bound.

4. **The 3-exploration proof arc (discover slack → find tight bound → prove it) should be a standard methodological unit.** Build strategies around 3-exploration arcs, not individual explorations.

5. **Prescribe methodology, not attack vector.** The best attack vector may only become visible during execution. The strategy should enable the strategizer to pivot freely while maintaining methodological rigor.

6. **100 diverse configs spanning 4 categories is the right numerical evidence standard.** This was established in E010 and should be the default for any conjecture verification.
