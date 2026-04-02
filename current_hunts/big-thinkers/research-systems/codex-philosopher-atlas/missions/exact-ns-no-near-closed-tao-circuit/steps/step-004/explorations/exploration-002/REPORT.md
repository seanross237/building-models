# Exploration 002 Report - Anti-Circuit Dossier On The Frozen Step-4 Sheet

## Goal

Apply the frozen Step-4 family ledger and pass/fail sheet from
`exploration-001` to the anti-circuit families
`F_BM`
and
`F_DT(delta, eta)`,
while keeping the packet sheet, the thresholds, the spectator partition, and
the normalization frozen.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-02.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/planner-chains/chain-02.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-001-feature-ledger.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-002-packet-language-memo.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/template-defect-near-closure-compares-one-canonical-packet-to-one-fixed-five-channel-tao-template-on-one-window.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/windowed-spectator-leakage-budget-compares-off-template-mass-to-the-desired-five-channels-class-by-class.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/delayed-threshold-itinerary-fixes-one-exact-ordered-activation-sequence-with-predeclared-spectator-budgets.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/all-promoted-step-2-candidates-share-the-same-forced-exact-ns-extras-around-the-core.md`
- `library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`
- `runtime/results/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-004-receptionist.md`

## Operational Note

- `[VERIFIED]` A launcher run was attempted earlier in the step and did not land
  a usable sentinel, so this report is completed directly from the anchored
  local record.
- `[VERIFIED]` The local receptionist result is important here: the repository
  does **not** pin one concrete Step-4 wavevector/helicity triple for the
  anti-circuit families.
- `[INFERRED]` Therefore the honest `F_DT(delta, eta)` dossier can only use the
  symbolic family data that the repo actually froze. Any numeric coefficient
  table beyond that would be an unsupported invention.

## Frozen Sheet Reused Without Retuning

- `[VERIFIED]` Packet object:
  one canonical one-bridge role-labeled helical packet with mandatory conjugate
  completion.
- `[VERIFIED]` Desired ledger:
  `Q_clk`,
  `Q_seed`,
  `Q_amp`,
  `Q_rot^D`,
  `Q_rot^A`,
  `Q_next`.
- `[VERIFIED]` Spectator partition:
  `mirror`,
  `companion`,
  `feedback`,
  `cross`.
- `[VERIFIED]` Window rule:
  active families are normalized to
  `I = [0,1]`
  with
  `int_I D_on = 1`;
  static families with
  `int_I D_on = 0`
  are
  `inadmissible-static`.
- `[VERIFIED]` Hard admissibility filters:
  `A_live`,
  `A_sheet`,
  `A_closure`,
  and
  `A_trace`.
- `[VERIFIED]` Candidate thresholds:
  `lambda_tmpl = 1/3`,
  `lambda_spec = 1/4`,
  `Lambda_tot = 3/8`,
  `Lambda_mirror = 1/8`,
  `Lambda_companion = 1/12`,
  `Lambda_feedback = 1/12`,
  `Lambda_cross = 1/12`,
  `theta_B = 1/8`,
  `theta_C = 1/4`,
  `theta_D = 1/2`,
  `theta_E = 3/4`,
  `Lambda_itin = 1/3`,
  `kappa_rot = 2`.

## Anti-Family 1 - `F_BM`

### Exact Interaction Data Used

- `[VERIFIED]` `F_BM` is the frozen exact Beltrami-aligned mirror-complete
  family from `exploration-001`.
- `[VERIFIED]` The repo-level Beltrami record says exact Beltrami alignment is
  real but `static-only`, and `exploration-001` already freezes the Step-4
  consequence:
  the exact nonlinear forcing ledger is static with
  `int_I D_on = 0`.
- `[INFERRED]` On the frozen canonical sheet, the only interaction ledger that
  is actually used is

  ```text
  sigma_BM = same-helicity Beltrami-aligned sign sheet with mandatory mirrors

  Q_clk = Q_seed = Q_amp = Q_rot^D = Q_rot^A = Q_next = 0
  D_mirror = D_companion = D_feedback = D_cross = 0
  int_I D_on = 0
  int_I D_off = 0
  ```

- `[VERIFIED]` No event-time trace exists:
  there is no
  `t_clk`,
  `t_trig`,
  `t_rot`,
  or
  `t_next`
  because no desired channel activates on
  `I`.

### Candidate Outcomes On `F_BM`

| Candidate | Outcome | Named reason |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `fails` | `vacuous-live-filter`: `A_live` blocks a zero-activity Beltrami packet from counting as a positive witness |
| `Windowed Spectator-Leakage Budget` | `fails` | `denominator-collapse`: `int_I D_on = 0`, so the family is `inadmissible-static` rather than near-closed |
| `Delayed-Threshold Itinerary` | `fails` | `no-activation-trace`: the ordered event tuple does not exist on the frozen window |

### Diagnostic Vector Readout On `F_BM`

- `[INFERRED]`

  ```text
  v_tmpl(F_BM) = (inadmissible-static; all desired and spectator entries zero)
  v_leak(F_BM) = (inadmissible-static; int_I D_on = 0; int_I D_off = 0)
  v_itin(F_BM) = (no t_clk, no t_trig, no t_rot, no t_next)
  ```

### Interpretation

- `[VERIFIED]` `F_BM` is a **filter test**, not a live obstruction family.
- `[VERIFIED]` This is the correct anti-vacuity outcome:
  the Step-4 sheet no longer mistakes exact static cancellation for a positive
  near-circuit witness.

## Anti-Family 2 - `F_DT(delta, eta)`

### What The Local Record Actually Freezes

- `[VERIFIED]` `exploration-001` freezes `F_DT(delta, eta)` as the
  nearly-degenerate one-bridge anti-family with
  `0 < eta << delta << 1`,
  with tiny trigger initial data
  `|C_n(0)| = eta`,
  and with desired seed / rotor legs of size
  `O(delta)`.
- `[VERIFIED]` The exact-NS atlas packet says shell-rescaled exact triad
  coefficients are geometry- and helicity-fixed `O(1)` quantities rather than
  freely tunable Tao coefficients.
- `[VERIFIED]` The same atlas packet and the Step-2 interaction-template report
  say every promoted candidate must still carry the forced
  `mirror`,
  `companion`,
  `feedback`,
  and
  `cross`
  extras on the same closed packet ledger.
- `[VERIFIED]` The Step-4 receptionist note says the repo still lacks one
  concrete `k,p,q` tuple and hence lacks one fully explicit helical coefficient
  table for this family.

### Helical Coefficient / Sign Ledger Used

- `[INFERRED]` The only honest coefficient/sign dossier on the current record is
  symbolic:

  ```text
  sigma_DT = frozen family sign sheet is required, but the concrete helicity
             tuple is not pinned in the repo

  c_clk, c_seed, c_amp, c_rot^D, c_rot^A, c_next
    = exact geometry-fixed helical coefficients on the frozen packet sheet

  c_seed, c_rot^D, c_rot^A = O(delta) effective desired legs on F_DT
  ```

- `[VERIFIED]` This is enough to state the family-shape burden.
- `[INFERRED]` It is **not** enough to compute one numeric
  `Delta_tmpl`
  or one numeric classwise leakage vector without importing a missing
  wavevector/helicity ledger.

### Desired-Channel Forcing Data Used

- `[INFERRED]` On the active normalized subfamilies,
  `int_I D_on = 1`
  by the frozen Step-4 normalization.
- `[VERIFIED]` The resolved desired-channel data on the local record are:

  ```text
  |C_n(0)| = eta
  Q_seed    = O(delta)
  Q_rot^D   = O(delta)
  Q_rot^A   = O(delta)
  ```

- `[INFERRED]` The remaining desired entries
  `Q_clk`,
  `Q_amp`,
  and
  `Q_next`
  are not numerically frozen in the repo for `F_DT`.
  After normalization, they carry whatever remainder of
  `int_I D_on = 1`
  the exact family leaves after the declared `O(delta)` seed/rotor legs are
  accounted for.

### Classwise Spectator Forcing Data Used

- `[VERIFIED]` Mirror completion is mandatory, so the
  `mirror`
  class is always live in the packet bookkeeping even on anti-families.
- `[VERIFIED]` The Step-2 interaction-template report says the exact closed
  packet also forces:

  ```text
  companion spectators:
    role-preserving / role-damaging same-scale updates

  feedback spectators:
    long-leg or reciprocal updates on the same triads

  cross spectators:
    shell-n / shell-(n+1) spill and back-reaction channels
  ```

- `[INFERRED]` The current repo does **not** pin one exact `F_DT` classwise
  coefficient table or integrated class ledger
  `(L_mirror, L_companion, L_feedback, L_cross)`.
  Those entries therefore remain unresolved rather than being filled with
  invented fractions.

### Event-Time Trace Used

- `[VERIFIED]` The tiny trigger is load-bearing and dynamically central in the
  inherited Tao ledger.
- `[INFERRED]` For the one anti-family computation that *is* earned on the
  current record, use the symbolic trigger bound recorded in
  `code/f_dt_trigger_bound.py`
  and
  `code/f_dt_trigger_bound.txt`:

  ```text
  if |C'(t)| <= K_seed delta + K_amp |C(t)| on I = [0,1]
  and |C(0)| = eta,
  then
    |C(t)| <= exp(K_amp) (eta + K_seed delta).
  ```

- `[INFERRED]` On the explicit small-parameter subregime

  ```text
  eta <= delta^2,
  delta <= 1 / (4 exp(K_amp) (K_seed + 1)),
  ```

  one gets

  ```text
  |C(t)| <= theta_C = 1/4  on I,
  hence  t_trig > 1.
  ```

- `[INFERRED]` This is sufficient to kill the ordered itinerary on a genuine
  subfamily of the frozen
  `F_DT(delta, eta)`
  family without changing the Step-4 thresholds.

### Candidate Outcomes On `F_DT(delta, eta)`

| Candidate | Outcome | Named reason |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `ambiguous` | `missing-exact-coefficient-ledger`: the family-level `O(delta)` collapse of seed/rotor legs is clear, but `Delta_tmpl` still needs one concrete role-projected coefficient/sign sheet |
| `Windowed Spectator-Leakage Budget` | `ambiguous` | `unresolved-classwise-ledger`: the spectator classes are structurally forced, but the repo does not yet pin one exact `F_DT` class integral table in the frozen interaction currency |
| `Delayed-Threshold Itinerary` | `fails` | `tiny-trigger-nonactivation`: on the explicit small-parameter subregime above, `t_trig > 1`, so no ordered activation tuple exists on `I = [0,1]` |

### Diagnostic Vector Readout On `F_DT(delta, eta)`

- `[INFERRED]`

  ```text
  v_tmpl(F_DT)
    = (
        Delta_tmpl unresolved on current record,
        Delta_spec unresolved on current record,
        resolved raw entries:
          Q_seed = O(delta),
          Q_rot^D = O(delta),
          Q_rot^A = O(delta),
          |C(0)| = eta
      )
  ```

- `[INFERRED]`

  ```text
  v_leak(F_DT)
    = (
        L_tot unresolved,
        L_mirror unresolved,
        L_companion unresolved,
        L_feedback unresolved,
        L_cross unresolved,
        int_I D_on = 1 on active subfamilies,
        raw structural fact:
          mirror / companion / feedback / cross classes are all forced
      )
  ```

- `[INFERRED]`

  ```text
  v_itin(F_DT)
    = (
        t_clk unresolved,
        t_trig > 1 on the explicit small-parameter subregime,
        t_rot undefined,
        t_next undefined,
        |C|_pretrigger^max <= theta_C
      )
  ```

### Interpretation

- `[VERIFIED]` `F_DT(delta, eta)` is the genuine obstruction-facing anti-family;
  unlike `F_BM`, it is live rather than vacuous.
- `[INFERRED]` The raw packet dossier already distinguishes three different
  anti-circuit stresses:

  ```text
  desired-channel collapse:
    the family definition itself suppresses the seed and rotor legs to O(delta)

  spectator persistence:
    mirror / companion / feedback / cross channels remain forced on the same
    exact closure ledger

  delayed-activation failure:
    the trigger can be kept below theta_C on the fixed window inside the frozen
    parameter family
  ```

- `[INFERRED]` But only the third item is fully cashed out candidate-by-candidate
  on the current record.
  The two coefficient-sensitive candidates remain unresolved until the branch
  writes one explicit `F_DT` wavevector/helicity ledger instead of only a
  family-shape description.

## Anti-Circuit Verdict

- `[VERIFIED]` The anti-circuit dossier cleanly separates vacuous evidence from
  live obstruction evidence:
  `F_BM` is only the admissibility filter test,
  while
  `F_DT(delta, eta)`
  carries the real anti-circuit burden.
- `[INFERRED]` The current repo record **earns** the following negative facts:
  `F_BM` cannot be used as a positive witness,
  and
  the `Delayed-Threshold Itinerary` candidate fails on an explicit small-
  parameter subfamily of `F_DT(delta, eta)`.
- `[INFERRED]` The current repo record does **not yet** earn numeric
  `Template-Defect` or `Windowed Spectator-Leakage` verdicts on `F_DT` because
  the required exact helical coefficient/sign ledger was never frozen down to
  one concrete packet instance.
- `[INFERRED]` So the honest Step-4 anti-circuit read is:
  partially successful and still coefficient-incomplete.
  The branch has a clean vacuity screen and a clean itinerary failure, but not
  yet a fully cashed coefficient/leakage kill on the anchored local record.

## Dead Ends / Corrections

- `[VERIFIED]` An earlier workspace draft contained explicit fractions and event
  times for `F_DT` that were **not** traced back to any prior repository source.
  I did not retain those unsupported numbers.
- `[VERIFIED]` The receptionist note independently confirms the underlying
  problem:
  the repo still does not pin one concrete Step-4 `k,p,q` triple for the
  anti-families.
