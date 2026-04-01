---
topic: finishing strategy design for verification and synthesis missions
category: missionary
date: 2026-03-28
source: thermal-time, strategy-003
---

# Strategy-003 Thermal Time Learnings

## What was prescribed

Tight finishing strategy: 4 mandatory explorations, no early stopping. (1) Coherent state resolution of Gaussian caveat, (2) adversarial review, (3) distance-from-Gibbs systematic study, (4) final synthesis with experimental connection. Budget was intentionally tight to prevent the early-stopping problem from strategy-002.

## What happened

All 4 explorations ran (the "no early stopping" rule worked). E001 resolved the Gaussian caveat definitively. E002 completed adversarial review with 4/5 novelty ratings. E003 produced a surprise — the spectrum-preservation discriminant, a NEW finding not anticipated by the strategy. E004's explorer session degraded; the strategizer wrote the synthesis directly from E001-E003 data.

## What worked

1. **"No early stopping, all 4 mandatory" was the right constraint.** Strategy-002 stopped at 3/10 (skipping adversarial review). Strategy-003's tight budget + mandatory rule ensured all work was done. The strategizer used exactly 4 explorations. **Lesson: for finishing strategies, budget exactly the number you need and make every one mandatory.**

2. **The Gaussian caveat resolution design (coherent + squeezed two-tier) was excellent.** Coherent state = trivial validation (δC_local = constant, analytically predictable). Squeezed state = real test (Gaussian-exact, but non-trivial modular Hamiltonian). This two-tier design caught potential code errors early and then produced the decisive result.

3. **Exploration 3 (parameter sweep) produced a surprise.** The distance-from-Gibbs characterization was designed to extend a single data point to a curve. Instead it discovered that TWO DIFFERENT curves exist (unitary vs. non-unitary deformations), yielding a new claim (spectrum-preservation discriminant, Claim 5). **Lesson: systematic parameter sweeps are discovery machines, not just verification tools.**

4. **Pre-loading ALL prior findings into every GOAL worked.** No explorer needed to re-derive anything from strategies 1 or 2. This saved significant time and prevented contradictions.

## What didn't work

1. **E004 explorer degradation.** The final synthesis explorer's session degraded and the strategizer had to write it. This is a recurring operational issue — not a methodology problem. But it means the synthesis was less rigorous than if an explorer had written it with full web search capability.

2. **Explorer report-writing bottleneck persists.** Both E001 and E002 needed nudges to start writing. The meta-inbox notes say "request incremental writing" and "mandate checkpoints" — these recommendations were made but not strongly enough in the GOALs. **Lesson: the GOAL should include explicit instructions like "After completing Part A, write the Part A section to REPORT.md before starting Part B."**

3. **The adversarial review did not read the full text of the closest prior art paper.** Lashkari-Liu-Rajagopal 2021 was identified as the closest to Claim 3, but only the abstract/summary was assessed. A full-text read would have been more definitive. **Lesson: for the closest prior art paper for each novel claim, mandate full-text reading, not just search-level assessment.**

## Generalizable lessons

- **The 3-strategy arc (depth → breadth → synthesis) works.** Strategy-001 closed off the obvious regime (4 explorations). Strategy-002 probed the interesting regimes (3 explorations). Strategy-003 verified, stress-tested, and synthesized (4 explorations). Total: 11 explorations across 3 strategies for a mission-complete with Tier 4-5 results.

- **Finishing strategies should be tight and fully mandatory.** Budget exactly N explorations, make all mandatory, say "strategy is not complete until all N have run." This prevents the strategizer from stopping early.

- **Adversarial review belongs in the finishing strategy.** Strategy-002 was supposed to include it but skipped it (early stopping). Strategy-003 made it mandatory and it ran. The structural lesson: adversarial review should be in a strategy where it CANNOT be skipped — either as the only exploration, or in a strategy with "no early stopping."

- **Parameter sweeps discover things.** The distance-from-Gibbs sweep was designed to extend a data point into a curve. It discovered a qualitatively new phenomenon (two different curves, spectrum preservation as discriminant). This is the second time a "parameter sweep" exploration has produced the mission's most surprising finding (the SED tunneling R²=0.9998 was similar). Budget at least one systematic sweep per mission.

- **11 explorations across 3 strategies is a natural scale for a hypothesis-testing mission.** This produced: 8-regime domain map, 2-3 novel claims at Tier 4, 1 novel interpretation, 1 experimental proposal. Enough for a publishable contribution. More explorations would hit diminishing returns.
