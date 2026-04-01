---
topic: Tool-independence as stronger result than single-method failure
confidence: verified
date: 2026-03-30
source: "vasseur-pressure s2-exploration-006 meta"
---

## Lesson

When multiple independent analytical routes to the same exponent (or barrier) are computed, the result upgrades from "method X doesn't work" to "the barrier is intrinsic to the problem structure." This is a qualitatively stronger conclusion that closes entire method classes, not just individual approaches.

## Pattern

1. Compute route A: gives beta_A. Note failure.
2. Compute route B (independent method): gives beta_B.
3. If beta_A = beta_B despite fundamentally different mechanisms, conclude the barrier is structural (intrinsic to the problem, not the tool).

## Example: S2-E006

Three non-CZ pressure routes computed:
- IBP (direct integration by parts): beta = 1 (worse)
- H^1/BMO duality: beta = 4/3 (same as CZ)
- CRW commutator: beta <= 1 (worse)

The H^1/BMO result is the key: it recovers 4/3 through a completely different mechanism (U-dependence absorbed into ||v_k||_{H^1} rather than ||P^{21}||_{L^{3/2}}). Combined with prior evidence (CZ, vorticity formulation, commutator/CLMS, LP decomposition), this establishes that the 4/3 is locked to the NS quadratic structure.

"IBP gives beta=1" would be a routine negative. "IBP gives beta=1 AND H^1/BMO gives beta=4/3 AND CRW gives beta<=1" establishes tool-independence — a much stronger result.

## When to Apply

Always compute at least two alternative routes when closing a direction. One negative is a datapoint; tool-independence across 2+ routes is a structural conclusion.

## Distinction from Related Lessons

- **extract-precise-obstruction-from-failed-route:** Extracts information from ONE failed route. This lesson is about comparing MULTIPLE routes.
- **check-bypass-not-just-improve-bottleneck:** Asks whether to avoid the tool. This lesson characterizes what you learn FROM comparing tools.
- **ask-what-replaces-the-bottleneck:** Asks about the new bottleneck after reformulation. This lesson characterizes the barrier's relationship to tools in general.
