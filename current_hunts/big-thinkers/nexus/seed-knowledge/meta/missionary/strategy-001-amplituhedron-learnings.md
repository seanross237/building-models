---
topic: Compute-first methodology for framework comparison missions
category: missionary
date: 2026-03-27
source: amplituhedron, strategy-001
---

# Strategy 001 Learnings — Amplituhedron Mission

## The Methodology

**"Compute First, Then Break It"** — Three-phase Verify–Extend–Falsify cycle. Phase 1: compute known amplitudes both ways, build infrastructure. Phase 2: stress-test by extending beyond safe territory. Phase 3: probe for physical divergence between frameworks. Exploration design rules: every exploration must produce code, failed computations are valuable, each gets one well-scoped task.

## What Worked

1. **The three-phase structure was natural and the Strategizer followed it well.** Ground truth → extension → probing is a logical progression. The Strategizer adapted the pacing (2/10 on Phase 1 instead of suggested half), which was correct.

2. **"Be brutally honest" framing in explorer goals produced excellent assessment.** Explorations that asked for honest evaluation of claims produced sharp REFORMULATION vs GENUINE CONTRIBUTION distinctions — the most valuable output of the strategy.

3. **Parallel exploration launches saved time.** The Strategizer ran explorations 005 and 006 concurrently (independent topics). Good throughput optimization.

4. **Early stop at 7/10 was wise.** The Strategizer recognized diminishing returns and synthesized instead of grinding out more explorations. This prevented the "one more exploration" trap.

5. **Standard explorers dominated** — 5/7 explorations were literature surveys, consistently completing in ~15 min with 400-500 lines. For topics where findings are structural rather than computational, surveys beat computation.

## What Didn't Work

1. **"Compute first" was the wrong emphasis for this domain.** The amplituhedron is a topic where the key findings are structural and conceptual — which theories it applies to, what it requires, how it relates to other programs. The most productive explorations were literature surveys, not computations. A "Survey first, then compute the interesting bits" approach would have been better.

2. **The computation mandate was too strong.** The strategy said "reasoning-only explorations are failures" — but the standard explorer surveys (which were effectively reasoning + literature review) produced the best results. For framework-comparison missions, the methodology should value structured synthesis equally with computation.

3. **Phase 1 scope was too ambitious.** The 6-point NMHV exploration (002) tried to compute AND compare two methods AND verify. Should have been either "compute via R-invariants" OR "compare BCFW vs Grassmannian given known result." One task per exploration means one SPECIFIC task, not one general direction.

4. **No adversarial phase.** The strategy didn't include a deliberate adversarial review of claims. The Strategizer produced honest self-assessments, but having a dedicated exploration try to BREAK the best findings would have strengthened or eliminated the novel claims.

## Generalizable Lessons

1. **Match methodology to domain type.** Computational missions need "compute first." Conceptual/structural missions need "survey first, compute the gaps." The amplituhedron is a conceptual topic — the key question was "what does this framework DO?" not "what does this formula PRODUCE?" Methodology should fit the nature of the question.

2. **Framework-comparison missions have a natural arc: map → characterize → probe → synthesize.** The mapping phase (which theories, which regimes) is more important than the computation phase for questions of the form "is X equivalent to Y?"

3. **Novel claims from well-studied fields will be synthesis, not discovery.** For topics actively researched by top physicists, expecting an AI exploration system to find genuinely new physics is unrealistic. The contribution is clean articulation, organized synthesis, and computational verification of known claims. Design strategies accordingly — don't set up validation criteria that require breakthrough novelty.

4. **One strategy can be sufficient.** For a clearly scoped question ("is X equivalent to Y?"), a single well-designed strategy with 7-10 explorations can produce a complete answer. Don't default to multi-strategy arcs when one strategy covers the landscape.

5. **The computation registry is a first-class output.** The 11 identified follow-up computations (COMPUTATIONS-FOR-LATER.md) are arguably as valuable as the novel claims — they give anyone who wants to push further a concrete roadmap. Require the Strategizer to maintain this throughout, not just at the end.

6. **Budget allocation: survey-heavy is fine.** Having 5/7 explorations be literature surveys isn't a failure — it's appropriate when the domain is well-studied and the question is structural. Don't force computation for its own sake.
