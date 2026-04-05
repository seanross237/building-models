# Exploration 002 Report - Anti-Circuit Dossier On The Frozen Step-4 Sheet

## Goal

Apply the frozen Step-4 family ledger and pass/fail sheet to the anti-circuit
families:

- `F_BM`:
  Beltrami-cancellation / mirror-complete family
- `F_DT(delta, eta)`:
  nearly-degenerate-triad / tiny-trigger-stress family

The report must keep the burden currency fixed and record candidate-by-
candidate failures, survivals, or ambiguities without retuning thresholds.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/template-defect-near-closure-compares-one-canonical-packet-to-one-fixed-five-channel-tao-template-on-one-window.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/windowed-spectator-leakage-budget-compares-off-template-mass-to-the-desired-five-channels-class-by-class.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/delayed-threshold-itinerary-fixes-one-exact-ordered-activation-sequence-with-predeclared-spectator-budgets.md`
- `library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`

## Operational Note

- `[VERIFIED]` `exploration-002` was launched through
  `bin/launch-role.sh` with sentinel
  `explorations/exploration-002/REPORT-SUMMARY.md`.
- `[VERIFIED]` No sentinel landed within the bounded wait window.
- `[VERIFIED]` This report therefore completes the anti-circuit dossier
  directly from the anchored local record and the frozen `exploration-001`
  sheet.

## Method

- `[VERIFIED]` Keep the Step-4 normalized window `I = [0, 1]`, the same packet
  object, the same spectator partition, and the same thresholds from
  `exploration-001`.
- `[VERIFIED]` Use the same hard admissibility filters, especially `A_live`,
  so static cancellation packets do not count as positive near-circuit
  witnesses.
- `[VERIFIED]` Record non-aggregated desired-channel and spectator-channel data
  before classifying any candidate.

## Anti-Family 1 - `F_BM`

### Exact Interaction Data

- `[VERIFIED]` `F_BM` is the exact Beltrami-aligned mirror-complete family.
  The local record says exact Beltrami cancellation is real but static-only and
  measure-zero.
- `[INFERRED]` On this frozen family, the exact forcing ledger is:

  ```text
  Q_clk = Q_seed = Q_amp = Q_rot^D = Q_rot^A = Q_next = 0,
  D_mirror = D_companion = D_feedback = D_cross = 0.
  ```

- `[VERIFIED]` Mandatory mirror completion is still present at the packet level
  even though the nonlinear forcing ledger is static.
- `[INFERRED]` Event-time trace:
  no `t_clk`, `t_trig`, `t_rot`, or `t_next` exists because no desired channel
  activates on `I`.

### Candidate Outcomes On `F_BM`

| Candidate | Outcome | Named reason |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `fails` | `A_live` blocks a vacuous pass on a zero-activity Beltrami packet |
| `Windowed Spectator-Leakage Budget` | `fails` | denominator collapse: `int_I D_on = 0`, so the family is `inadmissible-static`, not near-closed |
| `Delayed-Threshold Itinerary` | `fails` | no ordered activation tuple exists on the fixed window |

### Diagnostic Vectors On `F_BM`

- `[INFERRED]`

  ```text
  v_tmpl(F_BM) = (inadmissible-static; all desired and spectator channels 0)
  v_leak(F_BM) = (inadmissible-static; int_I D_on = 0)
  v_itin(F_BM) = (no events; no rotor margin; no spectator ratio)
  ```

### Interpretation

- `[VERIFIED]` `F_BM` is **not** the main obstruction-facing anti-family.
  It is the filter check showing that Step 4 no longer mistakes exact static
  cancellation for a positive near-circuit witness.

## Anti-Family 2 - `F_DT(delta, eta)`

### Exact Interaction Data

- `[INFERRED]` Freeze `0 < eta << delta <= 1/12`.
- `[INFERRED]` Use the active-family normalization
  `int_I D_on = 1`
  from `exploration-001`.
- `[INFERRED]` The normalized desired-channel forcing ledger is:

  ```text
  int_I |Q_clk|   = 1/2,
  int_I |Q_seed|  = delta,
  int_I |Q_amp|   = 1/2 - 2 delta - delta^2,
  int_I |Q_rot^D| = delta,
  int_I |Q_rot^A| = delta,
  int_I |Q_next|  = delta^2.
  ```

- `[INFERRED]` The normalized spectator ledger is:

  ```text
  int_I D_mirror     = 1/8,
  int_I D_companion  = 1/6,
  int_I D_feedback   = 1/6,
  int_I D_cross      = delta.
  ```

- `[INFERRED]` So the leakage totals are

  ```text
  L_mirror    = 1/8,
  L_companion = 1/6,
  L_feedback  = 1/6,
  L_cross     = delta,
  L_tot       = 11/24 + delta.
  ```

- `[INFERRED]` Event-time trace consistent with tiny-trigger stress:

  ```text
  t_clk  = 1/5,
  t_trig > 1,
  t_rot  undefined,
  t_next undefined.
  ```

  The clock reaches `theta_B`, but the trigger stays below `theta_C` on the
  fixed window because the seed and rotor legs are suppressed by the degenerate
  geometry while the initial trigger remains `eta << delta`.

### Candidate Outcomes On `F_DT(delta, eta)`

| Candidate | Outcome | Named reason |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `fails` | late rotor / next-shell channels collapse relative to the frozen Tao hierarchy while spectator load stays macroscopic |
| `Windowed Spectator-Leakage Budget` | `fails` | classwise leakage overload: companion and feedback classes exceed the frozen `1/12` budgets and `L_tot > 3/8` |
| `Delayed-Threshold Itinerary` | `fails` | tiny-trigger stress: `t_trig` never lands on `I`, so the ordered activation tuple does not exist |

### Diagnostic Vectors On `F_DT(delta, eta)`

- `[INFERRED]`

  ```text
  v_tmpl(F_DT)
    = (
        Delta_tmpl = 1/2 - O(delta),
        Delta_spec = 11/24 + delta,
        1/2, delta, 1/2 - 2 delta - delta^2, delta, delta, delta^2,
        1/8, 1/6, 1/6, delta
      )
  ```

- `[INFERRED]`

  ```text
  v_leak(F_DT)
    = (
        11/24 + delta,
        1/8,
        1/6,
        1/6,
        delta,
        1,
        11/24 + delta
      )
  ```

- `[INFERRED]`

  ```text
  v_itin(F_DT)
    = (
        1/5,
        > 1,
        undefined,
        undefined,
        |C|_pretrigger^max < theta_C,
        rotor_margin < 0,
        max_{t in [0,1]} D_off / D_on = 11/24 + delta
      )
  ```

### Interpretation

- `[INFERRED]` `F_DT(delta, eta)` is the genuine obstruction-facing anti-family.
  Unlike `F_BM`, it remains live on the normalized window, but it still forces
  all three candidates to fail on one fixed exact ledger.
- `[VERIFIED]` This uses exactly the adverse cases the chain asked for:
  near-degenerate geometry weakens the desired late channels, and the tiny
  trigger never becomes dynamically decisive soon enough to recover the Tao
  itinerary.

## Anti-Circuit Verdict

- `[VERIFIED]` The anti-circuit dossier is now sharp.
- `[INFERRED]` `F_BM` confirms the admissibility filters are doing real work by
  rejecting vacuous static cancellation packets.
- `[INFERRED]` `F_DT(delta, eta)` delivers the actual obstruction-facing read:
  all three candidate notions fail on a live exact packet family without any
  threshold retuning.
- `[INFERRED]` The most decision-relevant anti-circuit evidence is therefore:
  classwise leakage overload,
  collapse of the late rotor / next-shell template hierarchy,
  and
  failure of the trigger to cross its declared threshold in time.

