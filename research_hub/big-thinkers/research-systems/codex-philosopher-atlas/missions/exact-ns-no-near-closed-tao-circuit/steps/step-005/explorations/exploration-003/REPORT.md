# Exploration 003 Report - Freeze The Post-Repair Shortlist And Step-6 Readiness

## Goal

Using the inherited Step-4 dossier plus the completed Step-5 repair and
itinerary reports, determine the final post-repair shortlist and decide
whether Chain Step 6 is now well posed.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `library/meta/obstruction-screening/when-one-ledger-is-frozen-collapse-family-labels-before-packaging-work.md`
- `library/meta/obstruction-screening/a-tao-screen-can-be-operational-on-an-exact-but-noncoercive-ledger-if-it-is-only-used-as-an-admission-filter.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-no-near-closed-tao-circuit-step-005-explorer-003`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-003/REPORT-SUMMARY.md`.
- `[VERIFIED]` No sentinel landed within a bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Post-Repair Candidate Set

### 1. Repaired `Template-Defect Near-Closure`

- `[VERIFIED]` Exact criterion remains
  `G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)`
  on the same canonical one-bridge packet family and fixed window.
- `[INFERRED]` Repaired admissibility sheet:

  ```text
  Delta_tmpl <= 1/4
  Delta_spec <= 49/256.
  ```

- `[VERIFIED]` Step-4 read under the repaired sheet:
  `F_SS(1/12)` and `F_SL(1/16)` still pass;
  the hostile `F_DT(delta, eta)` remains a named failure by late rotor /
  next-shell collapse on the same frozen ledger.
- `[INFERRED]` Status:
  `survives`.

### 2. Repaired `Windowed Spectator-Leakage Budget`

- `[VERIFIED]` Exact criterion remains
  `G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)`
  on the same fixed interaction currency and class partition.
- `[INFERRED]` Repaired admissibility sheet:

  ```text
  L_tot       <= 1/4
  L_mirror    <= 1/12
  L_companion <= 1/12
  L_feedback  <= 1/16
  L_cross     <= 1/24.
  ```

- `[VERIFIED]` Step-4 read under the repaired sheet:
  the friendly dossiers still pass;
  the hostile `F_DT(delta, eta)` remains a named failure by classwise leakage
  overload on the same frozen ledger.
- `[INFERRED]` Status:
  `survives`.

### 3. Split `Delayed-Threshold Itinerary`

- `[VERIFIED]` The split attempt produced two post-repair notions:
  `pre-trigger delay filter`
  and
  `next-stage transfer-start filter`.
- `[INFERRED]` `pre-trigger delay filter` is exact on the frozen early-stage
  event language but is discarded because its downstream gate remains only a
  narrow admission filter and does not justify a separate Step-6 object freeze.
- `[INFERRED]` `next-stage transfer-start filter` is discarded as
  `not well-defined`
  because the `F_SL(rho)` ambiguity cannot be removed without changing the late
  event language after outcomes are known.

### 4. Unchanged candidates

- `[VERIFIED]` None.
  Both surviving algebraic candidates were repaired, and the behavior route was
  split and then discarded rather than carried forward unchanged.

### 5. Discarded notions

- `[VERIFIED]` The original `Delayed-Threshold Itinerary` label is retired
  after the split attempt.
  Carrying it forward beside the split children would silently keep multiple
  renamed versions of the same family alive.
- `[INFERRED]` The final discarded set is:
  original `Delayed-Threshold Itinerary`,
  `pre-trigger delay filter`,
  and
  `next-stage transfer-start filter`.

## Three-Axis Classification

| Candidate | Precision | Reason | Robustness | Reason | Usefulness | Reason | Negative bucket |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Repaired `Template-Defect Near-Closure` | `high` | one exact two-coordinate observable on one fixed packet sheet with repaired cutoffs and no free retuning left | `high` | same Step-3 `stable after canonicalization` status survives because only unused slack was removed | `medium` | gives one honest invariant defect observable for the exact search / comparison stage, but is less estimate-level direct than the leakage screen | none |
| Repaired `Windowed Spectator-Leakage Budget` | `high` | one exact classwise admissibility sheet on the frozen interaction currency and class partition | `high` | same Step-3 `stable after canonicalization` status survives because the repair leaves the class partition and window untouched | `high` | remains the sharpest obstruction-facing gate and answers the same burden-currency question in the most mechanical way | none |
| `Pre-trigger delay filter` | `high` | the early-stage event language is exact and fully frozen | `medium` | it stays tied to the same finite-window sheet, but only as a narrow admission filter | `low` | it does not name a new theorem-facing or counterexample-facing quantity beyond what the stronger survivors already screen | `not useful for the target theorem or counterexample question` |
| `Next-stage transfer-start filter` | `low` | no frozen exact definition removes the `t_next` ambiguity without changing the event language | `low` | the notion would require a substantive late-stage rewrite to survive | `low` | without a stable exact definition there is no honest downstream gate at all | `not well-defined` |

## Downstream-Gate Check

### Surviving Candidate 1 - Repaired `Template-Defect Near-Closure`

- `[PROPOSED]` Concrete downstream gate:
  one invariant defect-observable freeze

  ```text
  G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)
  ```

  on the repaired admissibility sheet
  `(1/4, 49/256)`.
- `[PROPOSED]` Smallest meaningful carried-forward family:
  the friendly stress witness `F_SL(rho = 1/16)`,
  because it is the worst recorded friendly packet for both repaired defect
  coordinates.
- `[INFERRED]` Why this gate is honest enough for Step 6:
  the object now says exactly what an exact friendly packet must keep small on
  the frozen ledger, and it still separates that witness from the hostile
  `F_DT(delta, eta)` failure mode.

### Surviving Candidate 2 - Repaired `Windowed Spectator-Leakage Budget`

- `[PROPOSED]` Concrete downstream gate:
  one invariant classwise admissibility freeze

  ```text
  G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)
  ```

  on the repaired budget sheet
  `(1/4, 1/12, 1/12, 1/16, 1/24)`.
- `[PROPOSED]` Smallest meaningful carried-forward stress set:
  the two friendly witnesses
  `F_SS(1/12)`
  and
  `F_SL(1/16)`,
  because together they saturate the repaired classwise sheet more sharply than
  any single recorded friendly family.
- `[INFERRED]` Why this gate is honest enough for Step 6:
  it remains the cleanest same-currency obstruction/admissibility sheet, and
  the hostile `F_DT(delta, eta)` still fails it by a named classwise overload.

### Rejected Candidate Gates

- `[VERIFIED]` `pre-trigger delay filter` is rejected because its gate is still
  only a narrow admission filter with no stronger same-currency cash-out.
- `[VERIFIED]` `next-stage transfer-start filter` is rejected because it does
  not have one frozen exact gate at all.

## Failed Attempts / Dead Ends

- `[VERIFIED]` Promoting `pre-trigger delay filter` as a Step-6 survivor is a
  dead end:
  the notion is exact but only adds early-event bookkeeping already dominated
  by the repaired template and leakage gates.
- `[VERIFIED]` Promoting `next-stage transfer-start filter` as a Step-6
  survivor is a dead end:
  any version sharp enough to remove the `F_SL(rho)` ambiguity would alter the
  late threshold language after the dossier is known.

## Step-6 Readiness Verdict

- `[VERIFIED]` Chain Step 6 is now well posed.
- `[INFERRED]` Final surviving shortlist:
  - repaired `Template-Defect Near-Closure`
  - repaired `Windowed Spectator-Leakage Budget`
- `[INFERRED]` Exact Step-6 object-freeze tasks should be:
  1. Freeze the repaired template-defect object on the canonical packet sheet
     with thresholds
     `lambda_tmpl = 1/4`
     and
     `lambda_spec = 49/256`.
  2. Freeze the repaired leakage object on the canonical packet sheet with
     budgets
     `Lambda_tot = 1/4`,
     `Lambda_mirror = 1/12`,
     `Lambda_companion = 1/12`,
     `Lambda_feedback = 1/16`,
     `Lambda_cross = 1/24`.
  3. Freeze `F_SL(1/16)` as the carried-forward friendly stress witness for the
     template object.
  4. Freeze the friendly stress set
     `F_SS(1/12)` and `F_SL(1/16)`
     for the leakage object.
  5. Keep the hostile `F_DT(delta, eta)` family as the reference negative
     comparator on the same frozen ledger.
- `[VERIFIED]` The branch should **not** stop at Step 5 because two survivors
  remain, both have non-cosmetic downstream gates, and the discarded itinerary
  route does not drag the whole branch into a failure bucket.
