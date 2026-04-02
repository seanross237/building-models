# Exploration 001 Report - Lock The Authorized Step-5 Repair Sheet

## Goal

Determine the only honest Step-5 threshold repairs for:

- `Template-Defect Near-Closure`
- `Windowed Spectator-Leakage Budget`

using the already-landed Step-4 dossier and without changing packet
semantics, spectator classes, interaction currency, sign sheet, phase gauge,
or the fixed finite window.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/REASONING.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/code/pro_circuit_dossier_check.py`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `library/meta/exploration-goal-design/fix-the-class-partition-and-finite-window-normalization-before-writing-hard-admissibility-sheets.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-no-near-closed-tao-circuit-step-005-math-explorer-001`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` Within a bounded wait, no usable sentinel landed.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record, following the same fallback pattern already used elsewhere in
  this mission.

## Controlling Step-4 Dossier

- `[VERIFIED]` Step 5 inherits the Step-4 verdict as fixed input, so
  `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
  is the controlling dossier for this repair pass.
- `[VERIFIED]` One intermediate Step-4 anti-dossier report was narrower about
  the anti-family template/leakage verdicts.
- `[INFERRED]` For Step 5, the correct precedence is:
  use the final Step-4 result and the landed pro-side arithmetic artifact as
  the controlling branch record, then use the intermediate anti-side note only
  for provenance and caution.

## Friendly-Side Maxima Already On The Record

- `[VERIFIED]` From `F_SS(mu = 1/12)`:

  ```text
  Delta_tmpl = 1/6
  Delta_spec = 1/6

  L_tot       = 1/4
  L_mirror    = 1/12
  L_companion = 1/12
  L_feedback  = 1/24
  L_cross     = 1/24
  ```

- `[VERIFIED]` From `F_SL(rho = 1/16)`:

  ```text
  Delta_tmpl = 1/4
  Delta_spec = 49/256

  L_tot       = 49/256
  L_mirror    = 1/16
  L_companion = 1/16
  L_feedback  = 1/16
  L_cross     = 1/256
  ```

- `[INFERRED]` Therefore the worst friendly values that any honest Step-5
  repair must preserve are:

  ```text
  max friendly Delta_tmpl = 1/4
  max friendly Delta_spec = 49/256

  max friendly L_tot       = 1/4
  max friendly L_mirror    = 1/12
  max friendly L_companion = 1/12
  max friendly L_feedback  = 1/16
  max friendly L_cross     = 1/24
  ```

## Repair Ledger

### 1. Template-Defect Near-Closure

- `[VERIFIED]` Inherited Step-4 status:
  `survives`.
- `[VERIFIED]` Old thresholds:

  ```text
  lambda_tmpl = 1/3
  lambda_spec = 1/4
  ```

- `[VERIFIED]` Step-4 evidence used:
  the worst friendly survivor for `Delta_tmpl` is `F_SL(1/16)` at `1/4`,
  and the worst friendly survivor for `Delta_spec` is `F_SL(1/16)` at
  `49/256`.
- `[INFERRED]` Friendly-side unused slack under the old sheet:

  ```text
  1/3 - 1/4    = 1/12
  1/4 - 49/256 = 15/256
  ```

- `[INFERRED]` Honest repair:

  ```text
  lambda_tmpl: 1/3 -> 1/4
  lambda_spec: 1/4 -> 49/256
  ```

- `[INFERRED]` Why this is the right repair:
  the Step-4 dossier already shows that no recorded friendly witness needs more
  slack than these values, so the old extra slack was unused bookkeeping rather
  than live discriminatory burden.
- `[VERIFIED]` Anti-side evidence retained:
  `F_DT(delta, eta)` still fails by late rotor / next-shell collapse on the
  same frozen ledger.
  The repair does not change that failure mode and does not invent a new
  anti-family coefficient table.
- `[VERIFIED]` Downstream gate preserved:
  `G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)`.
  The repair changes only the admissibility cutoff, not the observable.

### 2. Windowed Spectator-Leakage Budget

- `[VERIFIED]` Inherited Step-4 status:
  `survives`.
- `[VERIFIED]` Old budgets:

  ```text
  Lambda_tot       = 3/8
  Lambda_mirror    = 1/8
  Lambda_companion = 1/12
  Lambda_feedback  = 1/12
  Lambda_cross     = 1/12
  ```

- `[VERIFIED]` Step-4 evidence used:
  the friendly maxima listed above from `F_SS(1/12)` and `F_SL(1/16)`, plus
  the hostile `F_DT(delta, eta)` spectator ledger recorded in the final
  Step-4 result:

  ```text
  int_I D_mirror     = 1/8
  int_I D_companion  = 1/6
  int_I D_feedback   = 1/6
  int_I D_cross      = delta
  ```

- `[INFERRED]` Friendly-side unused slack under the old sheet:

  ```text
  3/8 - 1/4   = 1/8         for total leakage
  1/8 - 1/12  = 1/24        for mirror
  1/12 - 1/12 = 0           for companion
  1/12 - 1/16 = 1/48        for feedback
  1/12 - 1/24 = 1/24        for cross
  ```

- `[INFERRED]` Honest repair:

  ```text
  Lambda_tot:       3/8  -> 1/4
  Lambda_mirror:    1/8  -> 1/12
  Lambda_companion: 1/12 -> 1/12   (unchanged; already saturated by F_SS)
  Lambda_feedback:  1/12 -> 1/16
  Lambda_cross:     1/12 -> 1/24
  ```

- `[INFERRED]` Why this is the right repair:
  each tightened value is exactly the largest recorded friendly load on the
  frozen Step-4 sheet.
  `Lambda_companion` cannot tighten further without ejecting `F_SS(1/12)`,
  so there is no honest unused slack left there.
- `[VERIFIED]` Anti-side separation retained and sharpened:
  the Step-4 hostile dossier already records companion and feedback loads of
  `1/6`, and the final Step-4 verdict explicitly marks the same family as
  failing by classwise leakage overload.
  Tightening the total, mirror, feedback, and cross budgets therefore removes
  unused slack without changing the failure mechanism.
- `[VERIFIED]` Downstream gate preserved:
  `G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)`.
  The repair changes only the admissibility sheet, not the interaction
  currency or class partition.

## Repaired Candidate Sheet

| Candidate | Old sheet | Repaired sheet | Honest effect |
| --- | --- | --- | --- |
| `Template-Defect Near-Closure` | `lambda_tmpl = 1/3`, `lambda_spec = 1/4` | `lambda_tmpl = 1/4`, `lambda_spec = 49/256` | removes unused pro-side slack while preserving both recorded friendly witnesses |
| `Windowed Spectator-Leakage Budget` | `Lambda_tot = 3/8`, `Lambda_mirror = 1/8`, `Lambda_companion = 1/12`, `Lambda_feedback = 1/12`, `Lambda_cross = 1/12` | `Lambda_tot = 1/4`, `Lambda_mirror = 1/12`, `Lambda_companion = 1/12`, `Lambda_feedback = 1/16`, `Lambda_cross = 1/24` | keeps the same classwise gate but strips unused friendly slack from every budget except the already-saturated companion ceiling |

## Main Result

- `[VERIFIED]` Step 5 now has one authorized repair sheet for the two algebraic
  / leakage candidates.
- `[INFERRED]` The repair is conservative:
  it uses only Step-4 recorded friendly maxima and hostile failure modes, so it
  does not amount to post hoc family search or packet-sheet drift.
- `[INFERRED]` Both repaired candidates remain viable for the final Step-5
  shortlist because their downstream gates stay exact and non-cosmetic on the
  same frozen burden currency.
