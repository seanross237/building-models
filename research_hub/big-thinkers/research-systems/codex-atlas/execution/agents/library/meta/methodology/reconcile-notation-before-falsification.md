---
topic: Reconcile notation before falsifying a surviving lead
confidence: confirmed
date: 2026-03-31
source: "far-field-pressure-harmonic-loophole meta-exploration-001"
---

## Lesson

When a surviving lead is inherited from earlier explorations that used **different decompositions or vocabularies**, force an explicit notation reconciliation before running a falsification pass. Otherwise the team may attack the wrong object while thinking it is testing the right one.

## Evidence

Far-field-pressure-harmonic-loophole exploration-001 inherited the phrase "far-field term `P_{k21}`" from prior notes. A reconciliation pass against Vasseur's actual notation showed:

- `P_{k1}` is the harmonic/nonlocal term,
- `P_{k21}` is the bad **local** term,
- the live loophole was not Vasseur's literal harmonic term at all, but an alternative Wolf-style near/far decomposition.

That one reconciliation step changed the downstream question from "can we improve the harmonic term?" to "can an alternative harmonic far-field split recapture the dangerous local interaction and change its scaling?" Without the reconciliation, the Tao-filter step would have tested the wrong obstruction.

## Protocol

1. List the key objects from each predecessor exploration side by side.
2. Mark which names are literal notation from the source proof and which are later shorthand.
3. Identify whether apparently similar phrases refer to the same decomposition or to different ones.
4. Rewrite the surviving lead as an equation-level question in a single consistent notation.
5. Treat phrases like "far-field term `P_{k21}`" as red-flag shorthand until reconciled.

## When to Apply

- Any follow-on exploration that inherits terminology from multiple predecessor missions
- Any task where the surviving lead is a decomposition, reformulation, or change of variables
- Especially when the next step is adversarial/falsification work and the cost of testing the wrong object is high

## Relationship to Other Lessons

Distinct from `decomposition-audit-before-attacking-barrier` (which analyzes one proof's internal chain; this reconciles multiple vocabularies across predecessor work). Complementary to `preload-context-from-prior-work` (which loads prior findings; this verifies that the loaded findings use compatible notation).
