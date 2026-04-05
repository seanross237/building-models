# Exploration 001 Report - Lock The Authorized Step-5 Repair Sheet

## Goal

Determine the only honest Step-5 threshold repairs for:

- `Template-Defect Near-Closure`
- `Windowed Spectator-Leakage Budget`

using only the controlling Step-4 dossier and the landed Step-4 explorer
artifacts, with no new packet data, no packet-sheet drift, and no change to
the finite window, spectator partition, interaction currency, sign sheet, or
phase gauge.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/REASONING.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/code/pro_circuit_dossier_check.py`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-004-exploration-002-anti-circuit-dossier.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `library/meta/exploration-goal-design/fix-the-class-partition-and-finite-window-normalization-before-writing-hard-admissibility-sheets.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `code/repair_sheet_lock.py`
- `code/repair_sheet_lock.txt`

## Method And Provenance

- `[VERIFIED]` The controlling Step-4 branch verdict is
  `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`.
- `[VERIFIED]` One landed Step-4 anti-dossier note is narrower than the final
  Step-4 result about the hostile template/leakage arithmetic.
  For this Step-5 repair pass, the honest precedence rule is:
  take final `RESULTS.md` as the controlling branch verdict, then use the
  landed anti/pro explorer artifacts only to extract the recorded numbers that
  final `RESULTS.md` already promotes.
- `[CHECKED]` I encoded only the Step-4 numbers already recorded on disk in
  `code/repair_sheet_lock.py` and checked the friendly ceilings, removed slack,
  and exact hostile-side gap arithmetic in `code/repair_sheet_lock.txt`.

## Inherited Step-4 Status

- `[VERIFIED]` `Template-Defect Near-Closure` inherits Step-4 status
  `survives`.
- `[VERIFIED]` `Windowed Spectator-Leakage Budget` inherits Step-4 status
  `survives`.
- `[VERIFIED]` The inherited Step-4 threshold sheet is:

  ```text
  lambda_tmpl = 1/3
  lambda_spec = 1/4

  Lambda_tot       = 3/8
  Lambda_mirror    = 1/8
  Lambda_companion = 1/12
  Lambda_feedback  = 1/12
  Lambda_cross     = 1/12
  ```

## Friendly-Side Maxima Already Recorded

- `[VERIFIED]` The recorded friendly witness `F_SS(mu = 1/12)` carries:

  ```text
  Delta_tmpl = 1/6
  Delta_spec = 1/6

  L_tot       = 1/4
  L_mirror    = 1/12
  L_companion = 1/12
  L_feedback  = 1/24
  L_cross     = 1/24
  ```

- `[VERIFIED]` The recorded friendly witness `F_SL(rho = 1/16)` carries:

  ```text
  Delta_tmpl = 1/4
  Delta_spec = 49/256

  L_tot       = 49/256
  L_mirror    = 1/16
  L_companion = 1/16
  L_feedback  = 1/16
  L_cross     = 1/256
  ```

- `[COMPUTED]` The exact friendly-side maxima from those Step-4 witnesses are:

  ```text
  max friendly Delta_tmpl = 1/4
  max friendly Delta_spec = 49/256

  max friendly L_tot       = 1/4
  max friendly L_mirror    = 1/12
  max friendly L_companion = 1/12
  max friendly L_feedback  = 1/16
  max friendly L_cross     = 1/24
  ```

## Repair 1 - Template-Defect Near-Closure

- `[VERIFIED]` The inherited downstream gate is still
  `G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)`.
- `[VERIFIED]` The landed hostile Step-4 anti dossier records

  ```text
  Delta_tmpl = 1/2 - O(delta)
  Delta_spec = 11/24 + delta
  ```

  for `F_DT(delta, eta)`, while final Step-4 `RESULTS.md` promotes the same
  family to the controlling `fails` verdict for this candidate.
- `[COMPUTED]` The old unused friendly slack is

  ```text
  1/3 - 1/4    = 1/12
  1/4 - 49/256 = 15/256
  ```

- `[CHECKED][INFERRED]` The only honest repaired values are

  ```text
  lambda_tmpl = 1/4
  lambda_spec = 49/256
  ```

  because those are exactly the recorded friendly ceilings on the frozen
  Step-4 sheet.
- `[CHECKED][INFERRED]` `lambda_tmpl: 1/3 -> 1/4` is authorized because:
  the recorded friendly witness `F_SL(1/16)` already saturates `1/4`,
  leaving `1/12` of dead slack under the old sheet;
  the hostile family remains in the Step-4 fail bucket on the same gate;
  and the Step-4 record does **not** land a sharper exact hostile-side
  numerical margin than the symbolic `1/2 - O(delta)`.
  Any stronger exact tightening would therefore invent anti-side packet data.
- `[COMPUTED]` `lambda_spec: 1/4 -> 49/256` has an exact hostile-side gap on
  the recorded Step-4 ledger:

  ```text
  (11/24 + delta) - 49/256 = 205/768 + delta > 0.
  ```

- `[CHECKED]` The repaired template gate is still non-cosmetic on the frozen
  packet sheet:
  `F_SL(1/16)` now sits exactly on both repaired friendly ceilings, while
  `F_DT(delta, eta)` still fails by the same late-rotor / next-shell collapse
  mechanism already recorded in Step 4.

## Repair 2 - Windowed Spectator-Leakage Budget

- `[VERIFIED]` The inherited downstream gate is still
  `G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)`.
- `[VERIFIED]` The landed hostile Step-4 anti dossier records

  ```text
  L_tot       = 11/24 + delta
  L_mirror    = 1/8
  L_companion = 1/6
  L_feedback  = 1/6
  L_cross     = delta
  ```

  for `F_DT(delta, eta)`, and final Step-4 `RESULTS.md` promotes the same
  family to the controlling `fails` verdict for this candidate.
- `[COMPUTED]` The old friendly-side slack by leakage entry is:

  ```text
  L_tot:       3/8  - 1/4  = 1/8
  L_mirror:    1/8  - 1/12 = 1/24
  L_companion: 1/12 - 1/12 = 0
  L_feedback:  1/12 - 1/16 = 1/48
  L_cross:     1/12 - 1/24 = 1/24
  ```

- `[CHECKED][INFERRED]` The authorized repaired leakage sheet is

  ```text
  Lambda_tot       = 1/4
  Lambda_mirror    = 1/12
  Lambda_companion = 1/12
  Lambda_feedback  = 1/16
  Lambda_cross     = 1/12
  ```

- `[COMPUTED]` `Lambda_tot: 3/8 -> 1/4` is justified by the exact Step-4 gap

  ```text
  (11/24 + delta) - 1/4 = 5/24 + delta > 0,
  ```

  and cannot tighten further because `F_SS(1/12)` already saturates `L_tot`.
- `[COMPUTED]` `Lambda_mirror: 1/8 -> 1/12` is justified by the exact Step-4
  gap

  ```text
  1/8 - 1/12 = 1/24,
  ```

  and cannot tighten further because `F_SS(1/12)` already saturates `L_mirror`.
- `[CHECKED][INFERRED]` `Lambda_companion` stays at `1/12` because the worst
  recorded friendly witness `F_SS(1/12)` already saturates that old budget
  exactly.
  There is no honest unused slack left there.
- `[COMPUTED]` `Lambda_feedback: 1/12 -> 1/16` is justified by the exact Step-4
  gap

  ```text
  1/6 - 1/16 = 5/48,
  ```

  and cannot tighten further because `F_SL(1/16)` already saturates `L_feedback`.
- `[CHECKED][INFERRED]` `Lambda_cross` is the one recorded friendly ceiling
  that is **not** promoted into a Step-5 repair.
  Step 4 records `max friendly L_cross = 1/24`, but the hostile entry is only
  `L_cross = delta`, so the Step-4 dossier does **not** land a uniform hostile
  cross-class overload gap above `1/24`.
  Tightening `Lambda_cross` on this record would therefore be cosmetic with
  respect to the live hostile obstruction, which still sits in
  `L_tot`, `L_mirror`, `L_companion`, and `L_feedback`.
- `[CHECKED]` The repaired leakage gate is still non-cosmetic on the frozen
  packet sheet:
  `F_SS(1/12)` and `F_SL(1/16)` saturate different repaired friendly ceilings,
  while `F_DT(delta, eta)` still overloads the same gate through exact total,
  mirror, companion, and feedback excess already recorded in Step 4.

## Authorized Step-5 Repair Sheet

- `[CHECKED][INFERRED]` The only honest repaired threshold sheet supported by
  the current Step-4 record is:

  ```text
  Template-Defect Near-Closure
    lambda_tmpl = 1/4
    lambda_spec = 49/256

  Windowed Spectator-Leakage Budget
    Lambda_tot       = 1/4
    Lambda_mirror    = 1/12
    Lambda_companion = 1/12
    Lambda_feedback  = 1/16
    Lambda_cross     = 1/12
  ```

## Gaps Identified

- `[CHECKED]` The Step-4 record does not land one exact hostile-side numerical
  margin for `Delta_tmpl`; it records only the symbolic hostile defect
  `1/2 - O(delta)` together with the controlling Step-4 fail verdict.
- `[CHECKED]` The Step-4 record does not land one uniform hostile-side
  cross-class overload gap above the friendly cross ceiling `1/24`, so
  `Lambda_cross` has no authorized tightening on the present dossier.
- `[VERIFIED]` No new packet family, no new coefficient table, and no window or
  class-partition change was introduced in this exploration.

## Outcome

- `[CHECKED]` Step 5 now has an exact authorized repair sheet for both
  algebraic candidates.
- `[CHECKED]` The repair is one-way only and stays inside the frozen Step-4
  burden currency.
- `[CHECKED]` The repaired downstream gates remain live:
  the template gate still separates the friendly scale-separated witness from
  the hostile late-channel-collapse family,
  and the leakage gate still acts on explicit total/mirror/companion/feedback
  overload entries on the same frozen packet sheet.
