# Exploration 002 Report

## Goal

Freeze the Step-7 branch guardrails for the `F_SS(1/12)` audit:

- separate hard pass/fail gates from diagnostics;
- separate closure-forced bookkeeping from illegitimate rescue;
- state the no-overclaim rule after Step 1; and
- land a decisive Step-2 verdict.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-009.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/final-decider.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/judgments/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/refined/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/attacks/chain-01.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-6-freeze-keeps-repaired-template-defect-and-repaired-leakage-as-two-distinct-promoted-objects.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-6-is-well-posed-because-the-post-repair-shortlist-freezes-to-two-repaired-objects.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/windowed-spectator-leakage-budget-honest-step-5-repair-tightens-budgets-to-the-recorded-friendly-maxima.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-5-repair-pass-is-controlled-by-the-final-step-4-result-plus-the-landed-pro-side-arithmetic.md`

## Findings Log

### Initial Setup

- `[VERIFIED]` This report was created first and then filled incrementally from
  the local frozen record, per the explorer reporting rules.

### Operational Note

- `[VERIFIED]` `steps/step-007/explorations/exploration-001/REPORT.md` exists
  only as a skeleton and does not land a finished witness-freeze memo or
  summary sentinel.
- `[INFERRED]` To avoid blocking this guardrail memo on an unfinished sibling
  exploration, I anchored the verdict to the controlling Step-4 through Step-6
  results plus the run-002 planning record.

### 1. Controlling Authority Freeze

- `[VERIFIED]` The Step-6 freeze promotes exactly two repaired downstream
  objects on the same canonical one-bridge ledger:
  repaired `Template-Defect Near-Closure` and repaired
  `Windowed Spectator-Leakage Budget`.
  This is stated in:
  `steps/step-006/RESULTS.md`,
  `steps/step-006/explorations/exploration-001/REPORT.md`,
  and
  `library/factual/.../step-6-freeze-keeps-repaired-template-defect-and-repaired-leakage-as-two-distinct-promoted-objects.md`.
- `[VERIFIED]` The hard threshold sheet carried into Step 7 is:

  ```text
  G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)
  with
  Delta_tmpl <= 1/4,
  Delta_spec <= 49/256

  G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)
  with
  (L_tot, L_mirror, L_companion, L_feedback, L_cross)
    <= (1/4, 1/12, 1/12, 1/16, 1/24)
  ```

  The controlling branch authority is
  `steps/step-006/RESULTS.md`,
  with repair provenance in
  `steps/step-005/RESULTS.md`.
- `[VERIFIED]` The earlier Step-5 exploration record contains one stale
  leakage-cross entry:
  `steps/step-005/explorations/exploration-001/REPORT.md`
  still writes
  `Lambda_cross = 1/12`,
  while the controlling Step-5 result,
  the Step-6 freeze,
  and the factual repair note all carry
  `Lambda_cross = 1/24`.
- `[INFERRED]` Therefore the `L_cross` disagreement is historical record
  variance only.
  It is not a live Step-7 choice, not a new repair opportunity, and not
  license to reopen the leakage sheet.

### 2. Hard Gates Versus Diagnostics

- `[VERIFIED]` The branch hard pass/fail gates are repaired `G_tmpl` and
  repaired `G_leak` only.
  This is stated explicitly in
  `steps/step-007/GOAL.md`,
  `planning-runs/run-002/final-decider.md`,
  `planning-runs/run-002/winning-chain.md`,
  and
  `planning-runs/run-002/judgments/chain-03.md`.
- `[VERIFIED]` `t_clk`, `t_trig`, `t_rot`, `t_next`, and any stage-order
  narrative are diagnostics only.
  They may be recorded, but they are not promoted branch gates.
- `[INFERRED]` Timing or stage-order language may still appear later as
  descriptive evidence or as a mechanism label inside a failure atlas, but it
  cannot serve as an independent success currency and cannot override a gate
  failure.
- `[VERIFIED]` Step 7 also requires the branch to separate static dossier pass
  from exact dynamic pass.
  So a Step-4 or Step-6 static pass is not yet a Step-3 dynamic success.

### 3. Same-Currency Rule

- `[VERIFIED]` The branch must keep all later comparisons on one frozen exact
  ledger rather than switching bookkeeping mid-argument.
  This requirement is merged into the winner in
  `planning-runs/run-002/final-decider.md`
  and is consistent with the Step-4 and Step-6 result sheets.
- `[INFERRED]` The inherited same-currency protocol is:
  every later closure and dynamics comparison must evaluate the witness on the
  same canonical one-bridge role-labeled helical packet ledger, with:
  mandatory conjugate completion,
  fixed window `I = [0, 1]`,
  the same desired-channel ledger,
  the same spectator partition
  `mirror / companion / feedback / cross`,
  the same `D_on` / `D_off` split,
  the same sign / amplitude / phase bookkeeping,
  and the repaired Step-6 threshold sheets above.
- `[VERIFIED]` The branch may not switch to alternate bookkeeping currency,
  alternate packet semantics, alternate spectator partition, alternate window,
  silent threshold retuning, or post hoc rephasing.

### 4. No-Repair Rule Versus Closure-Forced Bookkeeping

- `[VERIFIED]` Discretionary repair is forbidden.
  The planning record explicitly rejects:
  extra bridge,
  shell-locked mode,
  post hoc companion,
  witness swap,
  threshold retuning,
  alternate bookkeeping currency,
  and post hoc rephasing.
- `[VERIFIED]` The refined Chain-03 judgment removes the discretionary repair
  step entirely and states that any added content must be either already forced
  by exact closure or disallowed.
- `[INFERRED]` Closure-forced bookkeeping therefore means only:
  1. mandatory conjugates already frozen by the packet definition; and
  2. any additional companion or mode that exact closure itself compels on the
     same frozen ledger during Step 2.
- `[INFERRED]` Illegitimate rescue means adding anything because it makes the
  witness look better after the fact rather than because the exact interaction
  ledger forces it.
  That includes class-changing extension, arbitrary truncation, swapping away
  from `F_SS(1/12)`, or rewriting the scorecard to accommodate the witness.
- `[VERIFIED]` If honest closure forces additions outside the audited
  one-bridge class or yields uncontrolled packet growth, Step 2 must stop with
  a negative branch verdict.
  That is a closure result, not permission to enlarge Step 1 retroactively.

### 5. No-Overclaim Rule After Step 1

- `[VERIFIED]` After Step 1 the branch is allowed to claim only that:
  1. one witness,
     `F_SS(1/12)`,
     is frozen on the canonical ledger;
  2. one authoritative scorecard is frozen, consisting only of repaired
     `G_tmpl` and repaired `G_leak`; and
  3. the inherited static dossier already records this witness as passing those
     two repaired gates on the frozen sheet.
- `[VERIFIED]` After Step 1 the branch is not allowed to claim:
  exact closure,
  finite closed-system isolation,
  class retention under honest closure,
  exact dynamic survival on `I = [0, 1]`,
  itinerary success,
  stage-order success,
  a near-circuit witness,
  a mission-level counterexample,
  or any broader statement about `F_SL` or the full one-bridge class.
- `[INFERRED]` The strongest honest Step-1 statement is therefore:
  witness-local static admissibility is frozen on an authoritative ledger, but
  honest closure and honest dynamics remain completely unearned.

### 6. Step-2 Verdict

- `[INFERRED]` **Verdict: Step 2 can start.**
- `[INFERRED]` Reason:
  the Step-1 freeze is now concrete enough to make Step 2 a clean closure test.
  The witness is frozen sharply enough,
  the authority sheet is explicit,
  the `L_cross` drift is demoted to historical variance,
  the diagnostics have been demoted,
  and the bookkeeping-versus-rescue line is concrete.
- `[VERIFIED]` This verdict does **not** assume closure has already been earned.
  The run-002 judgment explicitly says exact closure is not bookkeeping around
  the real task for this branch; it is the real task.
- `[INFERRED]` So Step 2 starts precisely as an honest attempt to compute all
  exact forced modes and interactions of the frozen witness on the frozen
  ledger, with immediate branch failure if that process requires
  class-changing additions,
  arbitrary truncation,
  alternate currency,
  or other rescue logic.

## Dead Ends / Failed Attempts

- `[VERIFIED]` Step-7 Exploration 001 did not finish beyond a skeleton, so it
  could not be used as a standalone inherited freeze memo.
- `[VERIFIED]` The Step-5 `Lambda_cross` disagreement is a genuine record
  blemish.
  I traced it, but the controlling Step-5 and Step-6 branch outputs already
  settle the branch authority in favor of `1/24`, so there is no live repair
  decision left to make here.

## Outcome

- `[INFERRED]` The guardrail memo succeeds.
  Hard gates are repaired `G_tmpl` and repaired `G_leak`.
  `t_clk`, `t_trig`, `t_rot`, `t_next`, and stage-order narrative are
  diagnostics only.
  Closure-forced bookkeeping is separated cleanly from illegitimate rescue.
  The branch may make only witness-local static freeze claims after Step 1.
  Chain Step 2 can start.

## Frozen Commitments For Chain Step 2

- `[VERIFIED]` Witness:
  `F_SS(1/12)` only.
  Do not reopen `mu` or swap witnesses.
- `[VERIFIED]` Ledger:
  canonical one-bridge role-labeled helical packet sheet with mandatory
  conjugate completion and fixed window `I = [0, 1]`.
- `[VERIFIED]` Hard gates:
  repaired `G_tmpl` with
  `Delta_tmpl <= 1/4`,
  `Delta_spec <= 49/256`,
  and repaired `G_leak` with
  `(1/4, 1/12, 1/12, 1/16, 1/24)`.
- `[VERIFIED]` Diagnostics only:
  `t_clk`,
  `t_trig`,
  `t_rot`,
  `t_next`,
  and any stage-order narrative.
- `[VERIFIED]` Same-currency rule:
  no silent sheet, threshold, partition, window, sign, phase, or burden-currency
  drift.
- `[VERIFIED]` No-repair rule:
  no extra bridge,
  shell-locked mode,
  post hoc companion,
  witness swap,
  threshold retuning,
  alternate bookkeeping currency,
  or post hoc rephasing.
- `[VERIFIED]` Allowed Step-2 additions:
  only exact-closure-forced bookkeeping on the same frozen ledger.
  If honest closure exits the class or grows uncontrollably, the branch stops.
- `[VERIFIED]` Scope rule:
  any later success remains witness-local unless a stronger transfer statement
  is actually proved.
