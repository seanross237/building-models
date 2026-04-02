---
topic: Require quantification in stress-test explorations, not just argumentation
category: goal-design
date: 2026-03-27
source: "classicality-budget strategy-001 meta-exploration-004"
---

## Lesson

When running a stress-test or devil's advocate exploration, explicitly ask the explorer to **compute quantitative bounds on each objection**, not just argue it. A quantified objection is far more convincing and actionable than a verbal argument — it either confirms the objection is a real constraint or shows it's hypothetical.

## Evidence

- **classicality-budget strategy-001 exploration 004** — The "catch-22" objection (tensor product fails where budget is interesting) was the most important finding of the stress-test. Without the quantitative computation, it would have remained a plausible argument. The explorer computed the radius at which the budget becomes tight for typical QD systems: R ~ 3.9 × 10^{-36} m ≈ 0.24 Planck lengths. This made the catch-22 concrete and unambiguous: the tight regime is sub-Planck, not a borderline case.

  Similarly, the saturation check (Objection 5) became definitive when the explorer computed R_actual/R_budget = 1.0000 for the spin model across N = 5, 10, 50, 100, 1000 — confirming exact saturation, not just "approximate" saturation.

## When to apply

Any exploration asking the explorer to evaluate objections, attack a result, or assess weaknesses. The goal should include instructions like:
- "For each objection, compute a quantitative bound or estimate that illustrates its severity"
- "Don't just argue — find the characteristic scale or magnitude that makes the objection concrete"
- "For each attack, determine whether it is a quantitative constraint (give numbers) or merely a conceptual argument (say so explicitly)"

The key distinction: an argued catch-22 is a concern; a computed catch-22 is a finding. The extra instruction to quantify is what elevates the output from editorial commentary to scientific result.

## Extension: Apply to Model Comparison Explorations Too

The same principle applies to model comparison explorations: require χ²/dof (or equivalent quantitative
metric), not just visual inspection of curves. "The curve looks similar" is not a finding; "χ²/dof =
1.21 vs. 132" is.

- **compton-unruh strategy-001 exploration-006** — Comparing the ratio model (a₀ = cH₀) against
  standard MOND and Verlinde (a₀ = cH₀/6) for NGC 3198 and NGC 2403. Without χ², the plots might
  look "close enough" for cH₀ vs. MOND. With χ²/dof: cH₀ gives 132–140 (100× worse than minimum),
  Verlinde gives 1.21 and 0.52. The cH₀ model is decisively ruled out, not just "worse." The
  quantitative comparison produced an unambiguous verdict.

  Prompt addition for model comparison explorations: "For each model, compute chi-squared/dof. State
  the verdict as a ratio: 'Model X is N× worse than the best-fit.' Visual inspection of curves is
  insufficient."

## Relationship to other entries

This extends **use-classification-schemes.md** (which covers rating systems for adversarial explorations) and **specify-computation-parameters.md** (which covers parameters for simulations). This entry is specifically about asking for quantitative backing for each objection in stress-test contexts — and now, for model comparison contexts. See also **require-baryonic-completeness.md** for galaxy-specific setup requirements.
