---
topic: Run gradient ascent on the projected quantity, not the full matrix
category: methodology
date: 2026-03-28
source: "yang-mills s003-meta-exploration-006"
---

## Lesson

When testing whether a bound holds on a specific eigenspace (e.g., R(Q)|_P ≼ 0 on the top eigenspace P of M(I)), run gradient ascent directly on the projected quantity (λ_max(P^T R P)) rather than on the full matrix (λ_max(M(Q)) or λ_max(R(Q))). The projected gradient ascent:

1. Tests the **correct target** — the inequality that needs to be proved
2. Is more informative — reveals the margin (how far the optimized value is from the violation threshold)
3. Is computationally cheaper — a 9×9 matrix (top eigenspace) vs. 192×192 (full operator)

## Evidence

- **yang-mills strategy-003 exploration-006** — Gradient ascent on λ_max(P^T R P) (9×9 matrix) stayed at −8 to −11 after 30 steps, never approaching 0 (the violation threshold). By contrast, gradient ascent on λ_max(M(Q)) (192×192) plateaued at 14.1–14.4, which is below 4d=16 but the margin (1.6) is less dramatic and harder to interpret. The projection approach gave a cleaner, more decisive result.

## When to Apply

Any exploration where the conjectured bound applies to a *subspace*, not the full operator. Common situations:
- Spectral bounds on the top (or bottom) eigenspace of a reference operator
- Curvature bounds that only need to hold on a specific mode family
- Any "X ≤ 0 on the top eigenspace of Y" inequality

## Design Pattern for GOAL.md

Include: "Run gradient ascent on λ_max(P^T X P) where P is the [eigenspace description]. Report the optimized value and the number of steps. If the optimized value approaches the violation threshold, report as potential counterexample."

## Relationship to Other Patterns

- Complements **characterize-maximizers-not-just-bounds** (goal-design) — the projection approach reveals which directions are hardest to bound
- Complements **verify-unexpected-findings-immediately** (methodology) — gradient ascent on the projection is a natural stress-test for a conjectured subspace bound
