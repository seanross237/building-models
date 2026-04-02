---
topic: Require an independent verification baseline for complex computations
category: goal-design
date: 2026-03-27
source: "amplituhedron strategy-001 meta-exploration-002"
---

## Lesson

When dispatching a goal that involves a complex recursive or algorithmic computation, provide a non-recursive independent formula as the ground truth baseline — or explicitly ask the explorer to find/derive one before attempting the main computation.

Without an independent baseline, the explorer has no way to verify its result. Two independent implementations of the same algorithm share the same fundamental difficulties (e.g., cyclic ordering conventions in BCFW), so they cannot cross-validate each other.

## Evidence

- **amplituhedron strategy-001 exploration 002** — The explorer implemented BCFW for 6-point NMHV using two independent shift choices ([1,2⟩ and [2,4⟩). The two implementations disagreed by 93%. Because neither had a non-recursive target to check against (the R-invariant / momentum twistor 5-bracket formula was not provided), there was no way to determine which (or whether either) was correct. The exploration ended with verified structural zeros but an unverified total amplitude.

## What to provide

For amplitude computations: the R-invariant formula or momentum twistor 5-brackets give A_n^NMHV directly, without recursion. These are independent of cyclic ordering conventions in sub-amplitudes.

More generally: if a problem has both a direct formula and a recursive/constructive method, implement the direct formula first. The direct formula's simplicity makes it easier to verify; the recursive method can then be checked against it.

## Key distinction

Two BCFW shifts are NOT independent verification — they share the same underlying structure (sub-amplitude cyclic orderings, internal helicity assignments, propagator conventions). When both are wrong in consistent ways, they can agree while both being wrong, or disagree for non-obvious reasons.

True independent verification requires a conceptually different approach: non-recursive direct formula, numerics from a separate code, or comparison to known limiting cases (e.g., collinear limits, factorization channels).

## When to apply

Any time the goal asks the explorer to "compute X and verify using Y" where X and Y are two implementations of the same algorithm. Split the goal: first ask for an independent baseline (direct formula, published numerical values, limiting cases), then ask for the computation.
