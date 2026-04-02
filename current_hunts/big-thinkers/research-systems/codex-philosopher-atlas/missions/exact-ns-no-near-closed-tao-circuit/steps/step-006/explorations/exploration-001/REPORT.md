# Exploration 001 Report - Freeze The Surviving Objects On The Repaired Ledger

## Goal

Determine, using the controlling Step-5 shortlist and inherited Step-1 through
Step-4 freezes, whether repaired `Template-Defect Near-Closure` and repaired
`Windowed Spectator-Leakage Budget` should remain two distinct downstream
objects, be narrowed into one smaller promoted object, or be rejected at Step
6.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-005-exploration-003-shortlist-and-step-6-readiness.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/template-defect-near-closure-compares-one-canonical-packet-to-one-fixed-five-channel-tao-template-on-one-window.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/windowed-spectator-leakage-budget-compares-off-template-mass-to-the-desired-five-channels-class-by-class.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-6-is-well-posed-because-the-post-repair-shortlist-freezes-to-two-repaired-objects.md`
- `library/meta/obstruction-screening/robustness-audits-may-keep-several-honest-survivors-with-different-statuses.md`
- `library/meta/obstruction-screening/when-one-ledger-is-frozen-collapse-family-labels-before-packaging-work.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-no-near-closed-tao-circuit-step-006-explorer-001`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` A partial `REPORT.md` skeleton landed, but no summary sentinel
  appeared within the bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record, following the same fallback style already used in earlier
  mission steps when nested role sessions stalled before writing their
  sentinel outputs.

## Frozen Survivor Sheets

### 1. Repaired `Template-Defect Near-Closure`

- `[VERIFIED]` Exact criterion and invariant downstream gate:

  ```text
  G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)
  ```

  on the canonical one-bridge role-labeled helical packet family with
  mandatory conjugate completion.
- `[VERIFIED]` Repaired thresholds:

  ```text
  Delta_tmpl <= 1/4
  Delta_spec <= 49/256
  ```

- `[VERIFIED]` Packet semantics:
  one canonical one-bridge packet
  `P_n = (A_n, B_n, C_n, D_n, E_n)`
  with desired exact core
  `A -> B`,
  `A -> C`,
  `B,C -> C`,
  `C,A <-> D`,
  `D,D -> E`,
  and the forced spectator classes
  `mirror`,
  `companion`,
  `feedback`,
  `cross`.
- `[VERIFIED]` Canonical representation policy:
  one frozen role order,
  one conjugate-completion convention,
  one helical sign sheet,
  one amplitude anchor,
  one phase anchor,
  and one helical basis choice.
- `[VERIFIED]` Fixed window:
  the normalized Step-4 activation window
  `I = [0, 1]`,
  inherited unchanged into Step 6.
- `[VERIFIED]` Carried-friendly witness:
  `F_SL(1/16)`,
  the worst recorded friendly packet on both repaired defect coordinates.
- `[VERIFIED]` Hostile comparator:
  `F_DT(delta, eta)`,
  which remains a named failure by late rotor / next-shell collapse on the
  same frozen ledger.
- `[INFERRED]` Step-6 status:
  `promoted unchanged`.
- `[INFERRED]` Why unchanged:
  the Step-5 repair only removed unused slack.
  It did not change the packet class, the template hierarchy, the window, the
  canonical sheet, or the observable.

### 2. Repaired `Windowed Spectator-Leakage Budget`

- `[VERIFIED]` Exact criterion and invariant downstream gate:

  ```text
  G_leak(P_n; I)
    = (L_tot, L_mirror, L_companion, L_feedback, L_cross)
  ```

  on the same canonical packet family and exact interaction currency.
- `[VERIFIED]` Repaired thresholds:

  ```text
  L_tot       <= 1/4
  L_mirror    <= 1/12
  L_companion <= 1/12
  L_feedback  <= 1/16
  L_cross     <= 1/24
  ```

- `[VERIFIED]` Packet semantics:
  the same one-bridge role-labeled helical packet family,
  the same five desired channels,
  and the same forced spectator partition into
  `mirror`,
  `companion`,
  `feedback`,
  and
  `cross`.
- `[VERIFIED]` Canonical representation policy:
  one frozen sign sheet,
  one amplitude normalization,
  one phase anchor,
  one conjugate-completion convention,
  and one fixed spectator partition with the same
  `D_on` / `D_off`
  split.
- `[VERIFIED]` Fixed window:
  the same normalized Step-4 activation window
  `I = [0, 1]`.
- `[VERIFIED]` Carried-friendly stress set:
  `F_SS(1/12)` together with `F_SL(1/16)`.
  The record already says no single friendly packet saturates the repaired
  classwise sheet as sharply as this pair does jointly.
- `[VERIFIED]` Hostile comparator:
  `F_DT(delta, eta)`,
  which remains a named failure by classwise leakage overload.
- `[INFERRED]` Step-6 status:
  `promoted unchanged`.
- `[INFERRED]` Why unchanged:
  the Step-5 repair only tightened the already-frozen admissibility sheet.
  It did not alter the interaction currency, spectator partition, packet
  semantics, or window.

## Distinctness Test

- `[INFERRED]` The local record supports **two distinct promoted objects**,
  not one narrowed survivor.
- `[VERIFIED]` The Step-2 and Step-3 records already give them different
  downstream roles:
  `Template-Defect Near-Closure` is the primary theorem-facing role-template
  gate,
  while
  `Windowed Spectator-Leakage Budget` is the primary obstruction-facing exact
  gate.
- `[VERIFIED]` The two objects act on different frozen quantities:
  `Template-Defect Near-Closure` measures deviation from the Tao-like
  five-channel role template via
  `(Delta_tmpl, Delta_spec)`,
  while
  `Windowed Spectator-Leakage Budget` measures off-template forcing against the
  desired channels class by class via
  `(L_tot, L_mirror, L_companion, L_feedback, L_cross)`.
- `[VERIFIED]` The record does **not** prove a dominance relation in either
  direction.
  It does not show that passing
  `G_tmpl`
  forces passing
  `G_leak`,
  nor the converse.
  The fact that
  `F_SS(1/12)` and `F_SL(1/16)` pass both screens while `F_DT(delta, eta)`
  fails both screens is only co-orientation on the current dossier, not an
  equivalence theorem.
- `[INFERRED]` Collapsing the pair into one narrower object would therefore
  overclaim a packaging equivalence that the local record has not earned.
- `[INFERRED]` Rejecting either survivor on
  `precision`,
  `robustness`,
  or
  `usefulness`
  is also not supported locally.
  Step 5 already rated both as high on
  `precision`
  and
  `robustness`,
  and the weaker of the two,
  `Template-Defect Near-Closure`,
  still kept a concrete non-cosmetic downstream gate with `usefulness`
  recorded as `medium`, not failed.

## Rejected Collapse Paths

- `[VERIFIED]` Collapsing everything into the leakage object is a dead end.
  The local record does not say that the leakage sheet captures all
  role-template information already tracked by
  `G_tmpl`.
- `[VERIFIED]` Collapsing everything into the template object is also a dead
  end.
  The local record does not say that small role-template defect is equivalent
  to the repaired classwise spectator admissibility sheet.
- `[INFERRED]` Promoting a single conjunction object
  `G_tmpl + G_leak`
  would not be a no-overclaim narrowing.
  It would manufacture a new compound object rather than freeze the two
  repaired survivors already earned in Step 5.

## Required Background Status

- `[VERIFIED]` `pre-trigger delay filter` stays discarded as
  `not useful for the target theorem or counterexample question`.
- `[VERIFIED]` `next-stage transfer-start filter` stays discarded as
  `not well-defined`.
- `[INFERRED]` These fixed Step-5 buckets matter in Step 6 only as background.
  They no longer compete for promotion and should not be reintroduced as a
  soft third downstream object.

## No-Overclaim Guardrails

### Repaired `Template-Defect Near-Closure`

- `[INFERRED]` The strongest currently earned claim is:
  on the frozen canonical packet sheet and fixed window,
  one exact role-template defect object survives the repaired admissibility
  sheet and separates the carried friendly witness from the hostile comparator.
- `[VERIFIED]` The local record does **not** yet justify:
  a theorem that small
  `(Delta_tmpl, Delta_spec)`
  forces the full Tao itinerary,
  forces the leakage budgets,
  or defines a global near-circuit notion beyond the audited packet class and
  carried witnesses.

### Repaired `Windowed Spectator-Leakage Budget`

- `[INFERRED]` The strongest currently earned claim is:
  on the same frozen packet ledger,
  one exact classwise leakage object survives the repair pass and remains the
  cleanest obstruction-facing admissibility screen.
- `[VERIFIED]` The local record does **not** yet justify:
  a theorem that passing
  `G_leak`
  forces template closeness,
  forces the delayed-threshold itinerary,
  or proves a global no-near-circuit theorem beyond the audited packet class
  and carried stress set.

## Outcome

- `[VERIFIED]` Step-6 object-freeze verdict from this exploration:
  the local record supports **two distinct promoted objects**.
- `[INFERRED]` Final promoted set from the frozen survivor sheet:
  - repaired `Template-Defect Near-Closure`
  - repaired `Windowed Spectator-Leakage Budget`
- `[INFERRED]` Neither object needs narrowing before promotion, because no
  unearned generalization is required to state either one on the already
  frozen packet ledger.
