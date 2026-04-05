# Step 7 Goal: Chain Step 1 Freeze The Single Witness, Authority Sheet, And Honest Scorecard

## Mission Context

**Mission:** Exact NS No-Near-Closed Tao Circuit

**Active chain:**
`Chain - Exact Stress Test Of F_SS(1/12)`

**Why this step exists now:** this is a bootstrap step after planning run
`run-002`. `step-006` completed the prior chain by freezing two promoted
downstream objects on the canonical one-bridge ledger, and mission control then
replanned rather than continuing that completed branch. The new planning run
selected a narrower moonshot: test the strongest constructive-looking witness
already on disk, `F_SS(1/12)`, under one frozen exact scorecard. Before exact
closure or dynamics can be trusted, the branch must first freeze one
authoritative witness definition, one authoritative Step-6 threshold sheet, and
one explicit no-repair rule.

## This Step Covers

This strategizer execution covers **Chain Step 1 only**.

You must do all of the following, and only the following:

- freeze the single carried witness `F_SS(1/12)` on the canonical one-bridge
  role-labeled packet sheet, with the existing normalization, mandatory
  conjugate completion, fixed window `I = [0, 1]`, and the carried role / sign
  / phase conventions already on disk;
- treat the Step-6 repaired sheets as the controlling authority for this
  branch:
  `G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)` with thresholds
  `Delta_tmpl <= 1/4`, `Delta_spec <= 49/256`,
  and
  `G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)` with
  repaired budget vector
  `(1/4, 1/12, 1/12, 1/16, 1/24)`;
- log any earlier threshold drift, especially the leakage-side `L_cross`
  mismatch inside the Step-5 record, as historical record variance rather than
  as a live choice;
- freeze one same-currency protocol for all later gate comparisons on this
  branch;
- declare in advance that `t_clk`, `t_trig`, `t_rot`, and `t_next` may be
  recorded only as secondary diagnostics and are **not** promoted pass/fail
  gates;
- forbid discretionary repair: no extra bridge, shell-locked mode, post hoc
  companion, or witness swap is allowed unless a later step shows such content
  is already forced by exact closure, in which case it belongs to Step 2
  bookkeeping rather than rescue logic;
- state explicitly what this branch may claim after Step 1 and what it is not
  yet allowed to claim.

Do **not** derive exact closure yet. That belongs to Chain Step 2. Do **not**
integrate or analyze exact dynamics yet. That belongs to Chain Step 3. Do
**not** reopen broad planning, revive the itinerary route as a hard scorecard,
or slide from the frozen witness `F_SS(1/12)` back to the wider family
`F_SS(mu)`.

## Required Deliverables

Produce all of the following inside `RESULTS.md`:

1. **Frozen witness sheet**
   - identify exactly what object on the canonical one-bridge ledger is being
     called `F_SS(1/12)`;
   - restate the normalization, packet semantics, mandatory conjugate
     completion, fixed window, and carried sign / phase / role conventions;
   - state what data are already frozen at Step 1 and what closure-forced
     additions are reserved for Step 2 bookkeeping only.

2. **Authority-sheet memo**
   - restate the controlling repaired Step-6 gate sheets for `G_tmpl` and
     `G_leak`;
   - identify the authoritative local source path for each threshold sheet;
   - log the earlier `L_cross` drift and any related threshold ambiguity as
     historical record variance rather than a live branch choice;
   - freeze one same-currency comparison rule that later closure and dynamic
     work must inherit.

3. **Honest scorecard memo**
   - state exactly which quantities are hard pass/fail gates on this branch:
     repaired `G_tmpl` and repaired `G_leak`;
   - state exactly which quantities are secondary diagnostics only:
     `t_clk`, `t_trig`, `t_rot`, `t_next`, and any descriptive stage-order
     narrative;
   - state explicitly that a static dossier pass is not yet an exact dynamic
     pass.

4. **No-repair and no-overclaim guardrail**
   - define what later steps may count as closure-forced bookkeeping versus
     illegitimate rescue;
   - state that no class-changing extension, witness swap, threshold retuning,
     alternate bookkeeping currency, or post hoc rephasing is allowed;
   - state the strongest claim the branch is allowed to support after Step 1
     and what it is not yet allowed to claim.

5. **Step verdict**
   - state whether Chain Step 2 is now well-posed;
   - if yes, list the exact frozen commitments Chain Step 2 must inherit;
   - if no, state plainly that the branch should stop here and name the
     sharpest earned witness-freeze or record-stability failure.

## Exploration Scope

Use **2-3 explorations total** unless a kill condition fires early.

The work should rely first on the local Step-6 handoff and the run-002 planning
record:

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN-HISTORY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-009.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/final-decider.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/judgments/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/refined/chain-03.md`

Use older Step-1 through Step-4 material only as needed to anchor the frozen
`F_SS(1/12)` witness and the repaired threshold sheets already promoted by Step
6.

Do **not** reopen broad mission planning. Do **not** compute exact closure or
an ODE system yet. Do **not** run new packet-family search. Do **not** bring
back itinerary metrics as hidden success criteria.

## Suggested Exploration Split

### Exploration A: Freeze the witness object

Tasks:
- identify the exact carried witness `F_SS(1/12)` on the canonical ledger;
- restate the normalization, role labels, conjugate completion, and fixed
  window that define the frozen object;
- confirm whether any ambiguity remains that would block Step 2.

Success standard:
- the branch has one unambiguous witness object rather than a drifting family
  description.

### Exploration B: Freeze the authority sheet and scorecard

Tasks:
- restate the controlling repaired `G_tmpl` and `G_leak` sheets from the Step-6
  record;
- log the `L_cross` threshold drift as historical traceability only;
- write the same-currency rule and separate hard gates from secondary
  diagnostics.

Success standard:
- later closure and dynamic work inherit one authoritative scorecard with no
  silent threshold or currency drift.

### Exploration C: Write the branch guardrail verdict

Only run this after the witness object and authority sheet are explicit.

Tasks:
- state the no-repair rule and the no-overclaim rule;
- decide whether those freezes are concrete enough to make Chain Step 2
  well-posed;
- if not, state the sharpest earned branch-stop verdict.

Success standard:
- mission control receives a clean `Step 2 can start` or `branch stops at
  witness freeze` outcome with no vague middle ground.

## Kill Conditions

Trigger an early negative conclusion for this step if any of the following
happens:

- the branch cannot freeze `F_SS(1/12)` without reopening `mu`, changing the
  packet semantics, or switching to a different witness;
- the controlling Step-6 threshold sheet cannot be stated without interpretive
  patchwork or live record repair;
- the branch can only make its scorecard work by reviving `t_clk`, `t_trig`,
  `t_rot`, or `t_next` as hard gates;
- the no-repair rule cannot be stated concretely enough to distinguish
  closure-forced bookkeeping from discretionary rescue.

If any of those occur, report the sharpest earned failure verdict and recommend
that the branch stop before Chain Step 2.

## Constraints

- Do **not** derive exact closure, packet growth, or class exit results in this
  step. Those belong to Chain Step 2.
- Do **not** run exact dynamics or finite-window integration in this step.
- Do **not** broaden the branch from `F_SS(1/12)` to the full one-bridge class
  or to a new packet family.
- Do **not** change the Step-6 repaired thresholds, packet ledger, or window.
- Do **not** package a descriptive stage-order narrative as success for this
  step.

## Validation Requirements

- Tag each major conclusion as `[VERIFIED]`, `[INFERRED]`, or `[PROPOSED]`.
- Cite the exact local source files that justify the frozen witness, the
  repaired `G_tmpl` sheet, and the repaired `G_leak` sheet.
- Make the final authority and scorecard sheets explicit enough that Chain Step
  2 can either start immediately or be cancelled immediately.
- If the step succeeds, end with one short section called
  `Frozen commitments for Chain Step 2`.
- If the step fails, end with one short section called
  `Why the branch stops at witness freeze`.
