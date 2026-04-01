---
topic: Useful failure — extract secondary results from failed explorations
category: methodology
date: 2026-03-28
source: "yang-mills s003-meta-exploration-s003-007"
---

## Lesson

When an exploration's main goal fails (e.g., "prove X" when X is false), the exploration often produces valuable secondary results: algebraic invariants, analytical proofs for special cases, structural constants, or characterizations of the failure itself. Design goals so that these secondary results are captured even when the primary objective is unachievable.

## Evidence

- **yang-mills strategy-003 exploration-007** — Main goal: prove M(Q) ≼ M(I) via pure gauge orbit + convexity argument. The goal was FALSE (M(Q) ≼ M(I) never holds for Q ≠ I). Despite this, the exploration produced:
  1. **Δ = 14(cosε − 1) ≤ 0 for single-link excitation** — a genuine analytical proof (not just numerical)
  2. **B_□ B_□^T = 4I₃** — algebraic invariant: each plaquette contributes exactly 4×(3×3 identity) regardless of Q
  3. **Haar average E[M(Q)] = 2(d−1)I = 6I** — structural constant computed in ~10 lines of code, revealing enormous average-case slack (6/16 = 37.5% of max)
  4. **Independent confirmation that R(Q) has mixed signs** — strengthened E005's finding

All four secondary results were valuable and filed in the factual library.

## Design Pattern

For proof or construction explorations where the main goal may fail:

1. **Include quick structural sub-tasks:** "Also compute: the Haar average of M(Q), the per-plaquette trace, any algebraic identities you notice." These take minutes and survive failure of the main goal.

2. **Request failure characterization:** "If the proof fails, characterize precisely when and why — find the smallest counterexample, identify the mathematical obstruction." (See also: specify-failure-paths.md.)

3. **Don't end the exploration at first failure:** After discovering the main goal is false, the explorer should still have budget for secondary investigations. The yang-mills E007 explorer pivoted after confirming falseness and still produced three valuable results.

## Why This Matters

An exploration that finds "X is false, nothing else" is a waste. An exploration that finds "X is false, BUT here are three structural invariants and an analytical result for a special case" is a major contribution. The secondary results often suggest the next proof strategy.

## Relationship to Other Patterns

- Complements **decisive-negative-pivot.md** (pivot immediately on hard negative; this entry says: extract value before pivoting)
- Complements **allow-explorer-synthesis.md** (leave conclusions open so the explorer can discover patterns)
- Distinct from **specify-failure-paths.md** (which instructs what to do if a step fails; this is about the overall exploration outcome)
