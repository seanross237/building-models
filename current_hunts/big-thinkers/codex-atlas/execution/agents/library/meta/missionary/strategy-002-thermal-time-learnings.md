---
topic: parallel computational probes for regime exploration
category: missionary
date: 2026-03-28
source: thermal-time, strategy-002
---

# Strategy-002 Thermal Time Learnings

## What was prescribed

Three mandatory parallel computational probes: (1) Rindler vacuum verification (control), (2) non-equilibrium post-quench test, (3) excited-state modular flow in QFT. Followed by a deepen phase and mandatory adversarial review. Budget: 6 explorations across 3 phases.

## What happened

The strategizer launched all 3 probes simultaneously. All 3 succeeded with decisive results. The strategizer correctly stopped after Phase 1 (3 explorations total), deeming the results sufficient for a final report. Phases 2 and 3 (deepen, adversarial, synthesis) were never executed.

## What worked

1. **All-mandatory parallel probes are the ideal Phase 1 design.** Three independent probes, all mandatory, all computational, all successful. Zero waste. The Yang-Mills and SED meta-lessons about "all explorations mandatory (no optional)" were validated again.

2. **Naming the probes explicitly in the strategy worked better than abstract methodology.** Each probe was a specific, well-defined computation. The strategizer translated them directly into GOALs. No ambiguity, no wasted iterations deciding what to do.

3. **Pre-loading strategy-001 context was critical.** Including normalization resolution, local interpretation confirmation, and code paths in the strategy prevented re-derivation. Every explorer started from the right place.

4. **The "control test" (Rindler vacuum) paid off immediately.** It caught a physics error in the GOAL (modular flow = boost, not time translation), which would have contaminated the other probes' interpretation.

## What didn't work

1. **The strategizer stopped too early.** 3 of 10 budgeted explorations used. No adversarial review, no coherent-state test, no synthesis. The results were strong enough that the strategizer felt done — but the Gaussian approximation caveat on the strongest claim (Claim 3) is a real gap that should have been resolved before declaring the strategy complete.

2. **The strategy should have made the adversarial review non-deferrable.** It was listed as "Phase 2, exploration 5: MANDATORY adversarial review" — but "mandatory" within a phase that the strategizer chose to skip. **Lesson: if adversarial review is truly mandatory, it should be Phase 1 (not Phase 2) or structurally enforced (e.g., "strategy is not complete until the adversarial exploration runs").**

3. **The coherent-state fallback for E003 was mentioned as a "Direction B recommendation" instead of a built-in escalation.** The Gaussian approximation was a known risk. The strategy should have said: "If the one-particle result uses Gaussian approximation, ALSO test with a coherent state in the same exploration."

## Generalizable lessons

- **Parallel mandatory probes + pre-loaded context is the highest-efficiency methodology pattern.** Three probes, three successes, zero waste. This pattern should be the default for Phase 1 of any computational strategy.

- **Adversarial review MUST be structurally enforced, not just labeled "mandatory."** If it's in Phase 2 and Phase 1 results are clean, the strategizer will skip it. Either include it as one of the parallel Phase 1 probes (running on prior-strategy claims), or add a structural rule: "strategy cannot be marked complete without an adversarial exploration."

- **Approximation caveats must have built-in resolution paths.** If a computation uses an approximation (Gaussian, perturbative, finite-size), the GOAL should include: "Also run the exact version on a simpler case to bound the approximation error." This prevents the caveat from surviving into the final report.

- **Early stopping by strategizers is a mixed signal.** Strategy-002 stopped at 3/10 explorations. The results were genuinely decisive — but the remaining work (adversarial, coherent test) would have strengthened the claims significantly. Missionaries should either (a) budget tighter (5 explorations, all mandatory) to prevent premature stopping, or (b) include an explicit "minimum exploration count" rule.

- **Physics errors in GOALs get caught but waste time.** E001's GOAL confused modular flow with time translation. The explorer caught it and corrected course — but this cost time and could have been worse. For relativistic / QFT problems, the strategy must specify which symmetry generator is being compared. "Compare to full QM" is ambiguous when there are multiple notions of time.
