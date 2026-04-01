---
topic: Sequence multi-method computation explorations; don't attempt them simultaneously
category: methodology
date: 2026-03-27
source: "amplituhedron strategy-001 meta-exploration-002"
---

## Lesson

When the goal is to compute something by two methods (e.g., BCFW + Grassmannian), split this into sequential explorations rather than simultaneous. The first exploration establishes a verified baseline; the second compares the second method against it.

## Evidence

- **amplituhedron strategy-001 exploration 002** — The goal was to compute A₆^NMHV via both BCFW recursion and G(3,6) Grassmannian residues, then compare term-by-term. The BCFW computation had bugs (two shifts disagreed by 93%). The explorer correctly declined to attempt the Grassmannian because without a verified BCFW target, any Grassmannian result would have no cross-check. Result: neither computation was verified, and the exploration ended with a partial result.

## The right structure

**Exploration N:** Compute via Method 1, verify against independent baseline (R-invariants, collinear limits, known limiting cases, published values). Only proceed when verified.

**Exploration N+1:** Compute via Method 2, compare against the verified Method 1 result.

This way, if Exploration N fails to produce a verified result, you learn this explicitly and can assign a targeted fix before wasting compute on Method 2.

## Why simultaneous attempts fail

The explorer cannot "partially verify" one method against another when both are in flight. If one method gives a wrong answer, it poisons the cross-check for the other. Both methods end up in an ambiguous state ("we got different answers but don't know which is right") — exactly the outcome that explorers cannot resolve on their own.

## Relationship to one-task-per-exploration

This is a corollary of the one-task rule (goal-design/one-task-per-exploration.md) applied specifically to multi-method verification. The tasks "compute via Method 1" and "compute via Method 2 and compare" are genuinely separate cognitive units, even when they look like one compound goal ("compute X two ways").

## When to apply

Any goal phrased as "compute X via A and B" or "verify X using both A and B." Rephrase as two sequential explorations.
