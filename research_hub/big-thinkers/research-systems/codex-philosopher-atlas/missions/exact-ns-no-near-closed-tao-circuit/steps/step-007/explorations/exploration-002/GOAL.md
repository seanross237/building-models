# Exploration 002 Goal - Freeze The Honest Scorecard, Guardrails, And Step-2 Verdict

## Objective

Using the witness and authority freeze from Exploration 001, write the branch
guardrail memo for Step 7:

- hard pass/fail gates versus secondary diagnostics;
- no-repair rule versus closure-forced bookkeeping;
- no-overclaim rule; and
- whether Chain Step 2 is now well posed.

The report must make mission-control-ready statements about what this branch is
allowed to claim after Step 1 and what it is not allowed to claim.

## Success Criteria

- The report states exactly that the hard gates are repaired `G_tmpl` and
  repaired `G_leak`.
- The report states exactly that `t_clk`, `t_trig`, `t_rot`, `t_next`, and any
  stage-order narrative are diagnostics only.
- The report cleanly separates closure-forced bookkeeping from illegitimate
  rescue.
- The report lands a decisive `Step 2 can start` or `branch stops here`
  verdict with inherited commitments listed explicitly.

## Failure Criteria

- The guardrail cannot distinguish forced bookkeeping from rescue.
- The verdict still depends on discretionary repair, threshold retuning, or
  alternate currency.
- Step 2 readiness remains vague after the Step-1 freeze.

## Relevant Context

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-009.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/final-decider.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/judgments/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/refined/chain-03.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-6-freeze-keeps-repaired-template-defect-and-repaired-leakage-as-two-distinct-promoted-objects.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-6-is-well-posed-because-the-post-repair-shortlist-freezes-to-two-repaired-objects.md`

## Constraints

- Do not derive exact closure or exact dynamics.
- Do not reintroduce itinerary timing as hard success language.
- Do not permit extra bridge, shell-locked mode, post hoc companion, witness
  swap, threshold retuning, alternate bookkeeping currency, or post hoc
  rephasing.
- If closure later forces additions, classify them as Step-2 bookkeeping only,
  not Step-1 rescue.

## Deliverables

- `REPORT.md`
- `REPORT-SUMMARY.md`
