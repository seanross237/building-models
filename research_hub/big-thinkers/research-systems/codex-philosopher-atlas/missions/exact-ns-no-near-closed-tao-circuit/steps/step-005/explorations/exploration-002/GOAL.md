# Exploration 002 Goal - Split Or Discard The Itinerary Candidate

## Objective

Resolve the Step-4 ambiguity in `Delayed-Threshold Itinerary` without changing
the frozen packet object, finite window, sign sheet, or threshold language.

The exploration must decide whether the candidate can honestly split into:

- `pre-trigger delay filter`
- `next-stage transfer-start filter`

or whether one or both parts must be discarded.

## Required Output

Produce a report that does all of the following:

1. Restates the original Step-2 itinerary criterion exactly enough to identify
   which clauses belong to the early delayed-trigger logic and which belong to
   the late transfer logic.
2. Defines the two proposed split notions on the same frozen event language if
   that is honestly possible.
3. Tests those notions against the inherited Step-4 dossier:
   hostile `F_DT(delta, eta)`,
   friendly `F_SS(mu)`,
   and
   scale-separated `F_SL(rho)`.
4. States, for each split notion, whether it
   `survives`,
   `fails`,
   or
   is
   `discarded`,
   with one of the allowed negative buckets if earned.
5. Names one concrete downstream gate for any surviving split notion, or
   states plainly that the gate remains too vague, cosmetic, or
   bookkeeping-dependent.

## Success Criteria

- The report isolates the exact source of the `F_SL(rho)` ambiguity rather than
  rephrasing it.
- Any kept split notion uses the same fixed window and threshold sheet instead
  of a softened event language.
- Any discard is tied to an earned reason:
  `not well-defined`,
  `not robust after canonicalization`,
  or
  `not useful for the target theorem or counterexample question`.

## Failure Criteria

- The exploration fails if it removes the `t_next` ambiguity only by deleting
  the late-stage threshold requirement or by moving the window.
- It fails if it turns the itinerary into a vague slogan about delayed
  behavior instead of one exact admissibility sheet.
- It fails if it keeps a survivor whose downstream gate is only bookkeeping.

## Key Local Context

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/code/f_dt_trigger_bound.py`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `library/meta/obstruction-screening/use-the-low-leakage-friendly-family-to-distinguish-event-trace-rigidity-from-isolation-failure.md`
- `library/meta/obstruction-screening/a-tao-screen-can-be-operational-on-an-exact-but-noncoercive-ledger-if-it-is-only-used-as-an-admission-filter.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## Constraints

- Do not weaken the original threshold sheet after reading outcomes.
- Do not import Tao's averaged transfer behavior.
- If the split cannot remove the `F_SL(rho)` ambiguity without changing the
  threshold or event language, say so explicitly and discard the affected
  notion.
