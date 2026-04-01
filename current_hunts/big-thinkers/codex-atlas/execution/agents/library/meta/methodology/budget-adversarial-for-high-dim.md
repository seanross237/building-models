---
topic: Budget adversarial optimization from the start for high-dimensional verification
category: methodology
date: 2026-03-29
source: "yang-mills-conjecture strategy-002 meta-exploration-003"
---

## Lesson

When verifying a conjecture or bound over a high-dimensional parameter space (≥ 20D), **budget adversarial optimization from the start** — do not rely on random sampling alone. Random uniform sampling on spaces like SO(3)^10 (30D) almost never hits the specific adversarial corners where violations occur, even with 200K+ samples. A conjecture can appear true under random testing and be definitively false.

## Evidence

- **yang-mills-conjecture strategy-002 exploration-003** — LEMMA_D appeared to hold under 200K random tests on SO(3)^10 (30D parameter space). Adversarial optimization (Nelder-Mead, 20 independent runs) found a counterexample with min eigenvalue = -2.13, far from marginal. The counterexample occupies a specific corner (D angles ~128° on 3 plaquettes, near-identity on 3 others) that random sampling essentially never reaches.

## When to Apply

Any exploration that tests whether a bound or inequality holds over a parameter space of dimension ≥ ~15. Indicators that adversarial optimization is essential:

1. **High dimensionality**: The measure of the counterexample region shrinks exponentially with dimension
2. **Structured extremizers**: Counterexamples often require specific alignment patterns (e.g., particular rotation angles on particular subsets)
3. **Marginal claims**: If the conjecture is tight (infimum = 0 or supremum = bound), counterexamples may be marginal and hard to find randomly

## Design Pattern for GOAL.md

Include: "Run adversarial optimization (Nelder-Mead or gradient-based, ≥ 20 independent starts from random initializations) in addition to random sampling. Report both: (a) worst case found by random sampling across N tests, and (b) worst case found by adversarial optimization."

## Variant: Domain-Specific Structured Starts [yang-mills-conjecture S003-meta-004]

Beyond random starts + gradient descent, **include domain-specific structured configurations as starting points**. Structured physics configurations can reveal the true extremum that random + GD misses:

- **yang-mills-conjecture S003-E004** — anti-instanton configs Q_μ = iσ_{a(μ)} (domain-specific extremal class for Hessian eigenvalues) found sup|λ_min| = 14.73; random GD starts found only -12.06 (18% below the true value). Even after gradient descent, random-start GD underperformed anti-instanton-start GD by ~22%.

**When to use:** When the domain has a known "worst case configuration class" (e.g., anti-instantons for lattice gauge Hessians, fully aligned states for correlation tensors). Ask: "What is the theoretically extremal configuration, ignoring optimize-ability?" Seed GD from that structure.

## What NOT to Do

- Don't report "verified for 200K random samples" as conclusive — state the dimensionality and note the limitation
- Don't skip adversarial optimization because random tests pass — that's precisely when adversarial matters most
- Don't use a single adversarial start — use multiple (≥ 10) to avoid local optima
- Don't use only random seeds for GD — include domain-specific structured seeds when the extremal configuration class is known

## Relationship to Other Patterns

- Distinct from **gradient-ascent-on-projected-quantity.md** (that is about testing on a subspace; this is about testing methodology in high dimensions)
- Complements **verify-unexpected-findings-immediately.md** (adversarial is the verification method; this entry is about when to budget for it proactively)
- Complements **verify-identity-generalization-before-extending.md** (verify conjectures adversarially before designing proofs for them)
