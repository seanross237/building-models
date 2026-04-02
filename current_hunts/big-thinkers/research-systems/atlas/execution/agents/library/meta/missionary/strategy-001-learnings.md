---
topic: Three-phase computational strategy evaluation
category: missionary
date: 2026-03-27
source: stochastic-electrodynamics, strategy-001
---

# Strategy-001 Learnings: Reproduce → Extend → Stress-Test

## What the strategy prescribed

A 3-phase methodology: (1) reproduce a known result to build computational infrastructure, (2) extend into novel territory, (3) stress-test the best result adversarially. Cross-phase rules: computation mandatory, numerical precision required, reuse code across phases.

## How well it worked

**Very well.** The Strategizer followed the phased structure faithfully and made good adaptive decisions. 6 of 10 explorations used, all produced code, the result reached Tier 3 (boundary identification with quantified mechanism). Key metrics:
- Phase 1: 2 explorations (1 computation, 1 survey). Survey was Strategizer's addition — not prescribed but excellent.
- Phase 2: 2 explorations. E003 found an unexpected O(β) failure; Strategizer correctly pivoted to E004 (ALD) rather than treating the Langevin failure as the final answer.
- Phase 3: 2 explorations (UV scan + adversarial review) in parallel. Decisive results.

## What I'd do differently

1. **Prescribe an early adversarial check after Phase 2, not just at the end.** E006's reframing of Finding 2 (Langevin failure = approximation failure, not SED failure) would have sharpened E004's design if known earlier.

2. **Require minimum 5 data points for any power-law fit.** The convergence exponents (τ^0.23, ω_max^(-0.18)) from 3 points each are the weakest part of the final report.

3. **Include a "landscape survey" exploration explicitly in Phase 1.** The Strategizer added E002 (literature survey) on its own initiative, and it was one of the most valuable explorations — it identified the optimal extension target. This should be standard methodology, not an improvisation.

4. **For a first strategy on a new domain, prioritize breadth over depth.** Strategy-001 went deep on one extension (anharmonic oscillator) and got a strong result, but the mission asks about 5 different directions. A wider first pass would have mapped the full frontier, enabling smarter allocation in later strategies.

## What surprised me

- **The Strategizer's best decisions weren't prescribed by the methodology.** Adding the survey exploration, pivoting from Langevin to ALD, and deciding to stop at 6/10 explorations were all Strategizer judgment calls that the methodology didn't dictate. The lesson: leave room for Strategizer initiative in the methodology rather than scripting every step.

- **Pre-loading verified formulas dramatically improved later explorations.** E004 (14 min) vs E003 (36 min) — same complexity of computation, but E004 had the noise normalization formula pre-loaded. This is a compounding advantage across explorations.

- **The most interesting finding was unexpected.** The O(β) Langevin failure wasn't what we were looking for (we expected O(β²) from Pesquera-Claverie). This serendipity happened because the methodology required starting from simpler approximations before going to the full dynamics — a methodological choice that produced a scientific discovery.

## Generalizable lessons

1. **Reproduce→Extend→Stress-Test is a solid default for computational missions.** Each phase feeds the next naturally.
2. **Survey explorations at the start pay for themselves.** They prevent blind direction choices and often identify better targets than the missionary can from the outside.
3. **Cross-phase knowledge transfer is the highest-leverage optimization.** Pre-loading formulas, reference values, and pitfall warnings into each goal is what turns a sequence of independent explorations into a coherent research program.
4. **Adversarial review shouldn't be saved for the end.** Run a lightweight version after the first major finding to correct framing before committing more explorations to that direction.
5. **"Computation mandatory" was the single most important cross-phase rule.** It prevented hand-waving and produced the evidence needed for the claims.
