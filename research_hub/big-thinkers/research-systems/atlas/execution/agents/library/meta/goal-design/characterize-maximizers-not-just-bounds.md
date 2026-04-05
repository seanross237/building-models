---
topic: Ask "characterize the maximizers" not just "is the bound tight"
category: goal-design
date: 2026-03-28
source: "yang-mills s003-meta-exploration-002"
---

## Lesson

When a proof strategy involves bounding λ_max or a similar extremum, frame goals as "characterize the set of maximizers" rather than just "prove the bound is tight." The structural characterization (e.g., "F = 4d if and only if Q is pure gauge") is often the most important finding — it reveals the geometry of the problem and suggests proof routes that tightness-checking alone does not.

## Evidence

Yang-mills S003-E002 (geodesic convexity): The most valuable finding was "F = 4d ↔ pure gauge configurations," not the bound verification itself. This structural insight — that the maximum is achieved exactly on the gauge orbit of the identity — immediately suggested the single-link theorem (proved via gauge equivalence) and the Weitzenböck approach (decompose into flat + curvature).

## Actionable

In goals involving extremal bounds, include: "Characterize the set of configurations achieving the bound (or approaching it). Is the maximum achieved on a specific geometric submanifold?" This is distinct from `allow-explorer-synthesis.md` (leave conclusions open) — this is about structuring the QUESTION to target the geometric characterization.
