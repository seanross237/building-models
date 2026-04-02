---
topic: Check for linearity/affinity in problem parameters before attempting bounds
category: methodology
date: 2026-03-29
source: "yang-mills-conjecture strategy-002 meta-exploration-005"
---

## Lesson

Before investing in bounding techniques (Cauchy-Schwarz variants, spectral bounds, perturbation theory), **check whether the quantity of interest is linear or affine in some of its parameters.** Affine dependence means you can minimize over those parameters independently and often get closed-form bounds. This structural insight can reduce an intractable high-dimensional optimization to a sequence of simple per-component problems.

## Evidence

**yang-mills-conjecture strategy-002 exploration-005** — The E005 explorer was tasked with proving sum_S(R, D, T) ≥ 0, where D = (D_{μ,ν}) ranges over SO(3)^6. The GOAL prescribed a polarization approach, which failed immediately (37% of trials negative, correction/baseline > 10). Seven other approaches had failed in E004.

The explorer discovered that **M9(R, D) is affine in D** (verified to 3.5e-15). Since each D_{μ,ν} enters only its own pair's contribution, the minimization over the 6 independent D matrices decomposes into 6 independent per-pair problems, each with a closed form via Cauchy-Schwarz: min_{D ∈ SO(3)} u^T D v = -||u||·||v||. This one structural observation unlocked the entire proof — the remaining steps (norm identity, combinatorial cancellation) were elementary.

Without checking for affinity, all 7 prior approaches tried to handle D jointly, which made the 18-dimensional minimization intractable.

## The Pattern

1. **Identify the "hard" parameters** — the ones whose range makes the problem difficult.
2. **Test affinity/linearity numerically** — perturb parameter values and check whether the change is linear (to machine precision).
3. **If affine:** decompose the optimization per-parameter. Each sub-problem is typically solvable by Cauchy-Schwarz or spectral bounds.
4. **If not affine:** check for convexity/concavity, which still enables powerful bounds (Jensen, etc.).

## Distinction from Related Entries

- **`special-case-proof-guides-generalization.md`** — That entry is about extracting proof strategy from a successful special case. This entry is about a specific structural CHECK to perform before attempting any proof strategy. Different trigger (before starting vs. after partial success).
- **`gradient-ascent-on-projected-quantity.md`** — That entry is about numerical testing strategy. This entry is about discovering algebraic structure that simplifies the proof itself.
