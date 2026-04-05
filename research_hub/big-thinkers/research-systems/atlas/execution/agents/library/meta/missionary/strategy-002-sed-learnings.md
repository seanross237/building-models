---
topic: Breadth-first frontier mapping with parallel probes
category: missionary
date: 2026-03-27
source: stochastic-electrodynamics, strategy-002
---

# Strategy-002 Learnings: Parallel Probes → Root Cause → Adversarial Review

## What the strategy prescribed

A breadth-first frontier mapping: 3 parallel probes of independent systems (tunneling, coupled oscillators, hydrogen), followed by root cause diagnosis, then adversarial synthesis. Cross-phase rules: ALD mandatory (learned from Strategy-001), computation mandatory, pre-load verified formulas. Target: "minimal modification" question.

## How well it worked

**Very well — produced the mission's strongest quantitative result.** The tunneling formula ln(Γ_SED/Γ_exact) = 0.072 + 1.049(S_WKB − √2/(4λ)) with R²=0.9998 across 4 decades is the kind of result you can present to a physicist. The breadth approach was vindicated — all three probes produced useful data, and the root cause synthesis (ω³ feedback unifies everything) only worked because we had data from 4 independent systems.

6 of 10 explorations used. All produced useful results. No failures.

## What I'd do differently

1. **Double-check physical constants in the strategy itself.** The τ value for hydrogen was wrong by 60× in the exploration goal. The missionary should have verified τ = e²/(6πε₀mₑc³) in atomic units and written it explicitly in STRATEGY.md. Cross-phase rules should include "verify all physical constants against known references before any simulation."

2. **Don't prescribe "compute a modification" for Phase 2 if the literature survey is more valuable.** The strategy said to computationally test a proposed modification, but the Strategizer correctly judged that the literature survey was higher-value (it showed all known modifications fail). The methodology should have said "diagnose the root cause, using literature or computation as appropriate" rather than mandating computation for Phase 2.

3. **The "minimal modification" question was the weakest part of the strategy.** It was the stated objective, but the answer was essentially "no simple modification exists — all three fixes fail." This is a valid finding but it's negative. The mission wants a constructive answer. Next strategy should flip this: instead of "what's the smallest fix for SED?", ask "what's the smallest addition to classical electrodynamics that recovers QM?" — which is Santos' ℏ-order framing.

4. **Run adversarial review on the strongest claim FIRST, not all claims simultaneously.** E006 reviewed all four claims at once, which diluted attention. The tunneling formula deserved a dedicated adversarial exploration. The Faria-França prior art discovery was the most important output of E006 — if it had been a single-claim review, it could have gone deeper (e.g., reading Faria-França in detail to identify exactly what's new vs. what's repackaged).

## What surprised me

- **The tunneling formula R²=0.9998 was far stronger than expected.** I designed the probes as quick surveys, not expecting any of them to produce a publishable quantitative law. The formula emerged from E001 as a conjecture and was confirmed in E005 — the two-phase discovery→verification cycle worked perfectly.

- **All three probes produced novel data.** I expected at least one to be a dead end (especially hydrogen, which the library flagged as "effectively closed"). Instead, all three contributed to the root cause story.

- **Prior art (Faria-França 2004) weakened the strongest claim.** The adversarial review was essential — without it, we would have overclaimed novelty for the tunneling formula.

## Generalizable lessons

1. **Parallel probes for frontier mapping is a strong methodology.** When you need to characterize a boundary across multiple independent systems, launch them all simultaneously. The root cause synthesis is only possible when you have data from diverse domains.

2. **The two-strategy arc (depth then breadth, or breadth then depth) is natural for computational missions.** Strategy-001 went deep on one system, Strategy-002 went wide across three. The combination is more powerful than either alone.

3. **Pre-loading ALD-mandatory and verified formulas from previous strategies is compounding advantage.** The "ALD not Langevin" rule saved every nonlinear simulation from false starts.

4. **Physical constant verification should be a cross-phase rule.** When simulations use physical units, wrong constants invalidate results even if the code is correct.

5. **Adversarial review MUST find prior art or it hasn't done its job.** E006 finding Faria-França (2004) was the single highest-value output of Strategy-002 — it correctly reframed the tunneling formula from "fully novel" to "marginally novel." Prior art search should be structured (specific databases, year ranges, author lists) not just "search the web."
