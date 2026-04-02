# Exploration 002 Summary

## Goal

Resolve the Step-4 ambiguity in `Delayed-Threshold Itinerary` by deciding
whether it can honestly split into
`pre-trigger delay filter`
and
`next-stage transfer-start filter`
on the same frozen event language.

## What I Tried

- Reconstructed the exact Step-2 itinerary clauses and threshold sheet.
- Isolated which clauses belong to the early delayed-trigger / rotor block and
  which clauses are genuinely late transfer logic.
- Tested the honest split against the inherited Step-4 dossier:
  hostile `F_DT(delta, eta)`,
  friendly `F_SS(mu)`,
  and
  scale-separated `F_SL(rho)`.
- Checked whether either split notion has a concrete downstream gate that is
  not just vague bookkeeping.

## Outcome

- Outcome:
  `succeeded`.
- `[INFERRED]` `pre-trigger delay filter` survives.
  The honest early split must include the rotor clause and the spectator screen
  only up to `t_rot`.
  On that definition it fails on `F_DT`, passes on `F_SS`, and passes on
  `F_SL`.
- `[INFERRED]` `next-stage transfer-start filter` is discarded as
  `not well-defined`.
  The frozen Step-2 language has only the terminal late witness
  `t_next` with
  `|E(t_next)| >= theta_E`,
  not a separate start-only event.
  Keeping that late clause leaves the `F_SL` ambiguity unchanged; weakening it
  would change the event language after outcomes were seen.

## Key Takeaway

The `F_SL(rho)` ambiguity is exactly a terminal `t_next` witness problem.
It is not caused by leakage and not caused by the early trigger / rotor part of
the itinerary.

## Leads Worth Pursuing

- If Step 5 wants one repaired behavior-based survivor, carry forward only the
  early rotor-admission filter
  `G_pre(P_n; I)`.
- If a later step wants to revisit the late transfer block, it must first earn
  one exact family-wide `t_next` witness on the same frozen packet sheet.

## Unexpected Findings

- The natural-looking split point is not after `t_trig`; it is after `t_rot`.
  `F_SL(rho)` already has a fixed rotor witness, so a split stopping at
  `t_trig` would miss the real ambiguity source.
- The low-leakage friendly family shows that the remaining defect is event-
  trace rigidity rather than spectator-isolation failure.

## Computations Worth Doing Later

- If the branch later insists on saving the late transfer notion, the missing
  computation is one exact family-wide late-stage amplitude trace that fixes
  `t_next` and `|E(t_next)|` on `F_SL(rho)` without moving the window or
  thresholds.
