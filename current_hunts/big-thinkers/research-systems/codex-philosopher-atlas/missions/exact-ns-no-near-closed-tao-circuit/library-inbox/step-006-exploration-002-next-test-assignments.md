# Exploration 002 Report - Attach The First Exact Next Tests

## Goal

Attach one first exact next-test assignment to each promoted Step-6 object on
the frozen packet ledger:

- repaired `Template-Defect Near-Closure`
- repaired `Windowed Spectator-Leakage Budget`

For each object, identify the smallest carried-forward test object or family,
the exact invariant observable or admissibility sheet for the next phase, the
exact missing data still needed before any honest theorem or counterexample
claim, and the strongest claim currently supported.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-004-exploration-002-anti-circuit-dossier.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/template-defect-near-closure-compares-one-canonical-packet-to-one-fixed-five-channel-tao-template-on-one-window.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/windowed-spectator-leakage-budget-compares-off-template-mass-to-the-desired-five-channels-class-by-class.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/scale-separated-friendly-family-shows-the-remaining-ambiguity-is-event-trace-rigidity-not-leakage.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/near-degenerate-tiny-trigger-stress-fails-all-three-step-4-gates-on-one-fixed-exact-ledger.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `library/meta/obstruction-screening/separate-theorem-endpoints-from-mechanism-language-at-the-first-gate.md`
- `library/meta/obstruction-screening/record-when-a-candidate-claim-is-only-a-proxy-level-insertion-line.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-no-near-closed-tao-circuit-step-006-explorer-002`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-002/REPORT-SUMMARY.md`.
- `[VERIFIED]` Only a report skeleton landed within the bounded wait; no
  summary sentinel appeared.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record, in the same fallback style already used elsewhere in the
  mission when nested role work stalled before finishing its sentinel output.

## Next-Test Assignment 1 - Repaired `Template-Defect Near-Closure`

- `[INFERRED]` First exact theorem question:

  ```text
  On the frozen canonical packet sheet, does the scale-separated friendly
  family F_SL(rho), restricted to 0 < rho <= 1/16, satisfy

    G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)

  with

    Delta_tmpl <= 1/4,
    Delta_spec <= 49/256

  uniformly on the fixed window I = [0, 1],
  while the hostile comparator F_DT(delta, eta) remains excluded on the same
  observable?
  ```

- `[INFERRED]` Why this is the right first theorem test:
  the local record already identifies
  `Template-Defect Near-Closure`
  as the primary theorem-facing role-template gate,
  and
  `F_SL(1/16)`
  is the worst recorded friendly packet on both repaired defect coordinates.
  The smallest honest next step is therefore to try to lift that boundary
  witness into a one-parameter friendly theorem on the same frozen ledger,
  not to claim theorem success outright.
- `[INFERRED]` Smallest meaningful carried-forward test family:
  `F_SL(rho)` for
  `0 < rho <= 1/16`,
  with
  `F_SL(1/16)`
  kept as the already-recorded boundary witness inside that family.
- `[VERIFIED]` Invariant observable for the next phase:

  ```text
  G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)
  ```

  on the fixed canonical packet sheet and fixed window.
- `[INFERRED]` Exact data still missing before the next phase can claim a
  theorem result:
  1. one explicit closed-form or rigorously checked
     `rho`-dependent formula for
     `Delta_tmpl`
     and
     `Delta_spec`
     on the carried family;
  2. one proof that the friendly worst case really occurs at the recorded
     boundary witness
     `rho = 1/16`,
     or else one corrected extremal parameter on the same family;
  3. one exact hostile-side numerical separation for
     `Delta_tmpl`
     if the next phase wants a fully quantitative family-separation theorem,
     because the current Step-5 record preserves only the symbolic hostile
     defect
     `1/2 - O(delta)`;
  4. one explicit statement of whether the theorem is only a family-level
     admissibility result or is meant to feed a later theorem-facing transfer
     lemma.
- `[INFERRED]` Strongest claim allowed now:
  the object honestly supports a theorem-facing insertion line saying that one
  explicit friendly scale-separated family may remain within the repaired
  defect sheet on the frozen ledger while the hostile comparator fails on that
  same observable.
- `[VERIFIED]` What the local record still does **not** justify:
  any theorem that small
  `(Delta_tmpl, Delta_spec)`
  automatically forces the leakage sheet,
  automatically forces the Tao itinerary,
  or proves near-circuit behavior beyond the audited packet class and carried
  family.

## Next-Test Assignment 2 - Repaired `Windowed Spectator-Leakage Budget`

- `[INFERRED]` First exact theorem question:

  ```text
  On the frozen canonical packet sheet, is the repaired classwise leakage
  sheet

    G_leak(P_n; I)
      = (L_tot, L_mirror, L_companion, L_feedback, L_cross)

  with repaired budget vector

    (1/4, 1/12, 1/12, 1/16, 1/24)

  the smallest friendly-admissible sheet supported by the carried stress set
  {F_SS(1/12), F_SL(1/16)},
  while F_DT(delta, eta) remains excluded on the same ledger by the recorded
  total / mirror / companion / feedback overload?
  ```

- `[INFERRED]` Why this is the right first theorem test:
  the local record already treats
  `Windowed Spectator-Leakage Budget`
  as the primary obstruction-facing gate.
  Its repaired Step-5 form is a sharpened admissibility sheet, so the first
  honest next theorem is a sharpness/minimality theorem on that same sheet,
  not a premature global obstruction theorem.
- `[INFERRED]` Smallest meaningful carried-forward test object:
  the friendly calibration stress set
  `{F_SS(1/12), F_SL(1/16)}`.
  The record already says no single friendly packet saturates the repaired
  classwise sheet as sharply as this pair does jointly.
- `[VERIFIED]` Invariant admissibility sheet for the next phase:

  ```text
  G_leak(P_n; I)
    = (L_tot, L_mirror, L_companion, L_feedback, L_cross)
  ```

  on the fixed spectator partition and fixed window.
- `[INFERRED]` Exact data still missing before the next phase can claim a
  theorem result:
  1. one exact closed-form or rigorously checked classwise ratio ledger for the
     carried stress set on the repaired Step-5 sheet;
  2. one proof that each repaired coordinate is genuinely sharp on the carried
     stress set, rather than only numerically suggestive from the Step-4
     dossier;
  3. one explicit statement that hostile exclusion is driven by
     `L_tot`,
     `L_mirror`,
     `L_companion`,
     and
     `L_feedback`,
     because the present record does **not** yet land one separate uniform
     hostile cross-class gap above
     `1/24`;
  4. one same-currency transfer statement if the next phase wants to upgrade
     the admissibility theorem into a broader no-near-circuit obstruction
     claim.
- `[INFERRED]` Strongest claim allowed now:
  the object honestly supports an exact classwise admissibility theorem on the
  frozen packet ledger and gives the branch one concrete obstruction-facing
  screen for later exact search.
- `[VERIFIED]` What the local record still does **not** justify:
  any theorem that passing
  `G_leak`
  automatically forces template closeness,
  automatically rules out all near-circuit behavior,
  or defines a global near-circuit obstruction beyond the audited packet class
  and the carried calibration set.

## Rejected Next-Test Paths

- `[VERIFIED]` Do **not** treat the Step-4 or Step-5 dossier itself as an
  already completed theorem.
  The dossier is an audited calibration record, not final theorem delivery.
- `[VERIFIED]` Do **not** reuse the discarded itinerary route as a third next
  test.
  Its negative buckets are already frozen.
- `[INFERRED]` Do **not** assign a theorem claiming equivalence between
  `G_tmpl`
  and
  `G_leak`.
  No such implication is earned on the current record.

## Step-6 Handoff Memo

- `[INFERRED]` Exact next-test assignments for mission control:
  1. Repaired `Template-Defect Near-Closure`
     -> first exact theorem question on the carried scale-separated family
     `F_SL(rho)`, `0 < rho <= 1/16`, using
     `G_tmpl(P_n; I) = (Delta_tmpl, Delta_spec)`.
  2. Repaired `Windowed Spectator-Leakage Budget`
     -> first exact theorem question on the friendly calibration stress set
     `{F_SS(1/12), F_SL(1/16)}` using
     `G_leak(P_n; I) = (L_tot, L_mirror, L_companion, L_feedback, L_cross)`.
- `[INFERRED]` The shared hostile comparator for both next tests remains
  `F_DT(delta, eta)` on the same frozen packet ledger.
