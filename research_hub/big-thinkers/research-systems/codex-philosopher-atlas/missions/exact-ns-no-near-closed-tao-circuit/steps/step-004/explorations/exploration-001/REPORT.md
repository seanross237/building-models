# Exploration 001 Report - Freeze The Step-4 Normalized Test-Family Ledger

## Goal

Freeze one explicit Step-4 burden currency for the three surviving candidates:

- `Template-Defect Near-Closure`
- `Windowed Spectator-Leakage Budget`
- `Delayed-Threshold Itinerary`

The burden currency must choose explicit anti-circuit and pro-circuit packet
families on the frozen one-bridge role-labeled helical packet object, then fix
the normalization sheet, admissibility filters, quantitative pass/fail sheet,
diagnostic vectors, and no-retuning rule before any candidate outcomes are read
off.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/INDEX.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/template-defect-near-closure-compares-one-canonical-packet-to-one-fixed-five-channel-tao-template-on-one-window.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/windowed-spectator-leakage-budget-compares-off-template-mass-to-the-desired-five-channels-class-by-class.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/delayed-threshold-itinerary-fixes-one-exact-ordered-activation-sequence-with-predeclared-spectator-budgets.md`
- `library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`
- `library/factual/tao-circuit-feature-ledger/the-tiny-trigger-role-is-dynamically-central.md`

## Operational Note

- `[VERIFIED]` `exploration-001` was launched through
  `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` After a bounded wait, the launcher still had not produced the
  sentinel.
- `[VERIFIED]` Following the already-recorded Step-2 and Step-3 fallback
  pattern, this report is therefore completed directly from the anchored local
  record.
- `[VERIFIED]` The local record fixes the Step-4 menu slots but does **not**
  already freeze a sharper family replacement or a numeric Step-4 threshold
  sheet.
  This report is therefore the first explicit Step-4 family/threshold freeze.

## Frozen Normalization Sheet

- `[VERIFIED]` **Packet object.**
  Every family in this step lives on the same canonical one-bridge role-labeled
  helical packet family
  `P_n = (A_n, B_n, C_n, D_n, E_n)`
  with mandatory conjugate completion.
- `[VERIFIED]` **Shared exact core.**
  Every family is read on the same desired-channel ledger:
  `A -> B`,
  `A -> C`,
  `B,C -> C`,
  `C,A <-> D`,
  `D,D -> E`,
  together with the same forced spectator classes
  `mirror`,
  `companion`,
  `feedback`,
  `cross`.
- `[INFERRED]` **Canonical gauge.**
  Freeze the amplitude anchor
  `|A_n(0)| = 1`,
  the phase anchor
  `arg A_n(0) = 0`,
  one family-declared helical sign sheet written in role order as
  `sigma_F = (sigma_A, sigma_B, sigma_C, sigma_D, sigma_E)`,
  one role order,
  and one conjugate-representative convention.
- `[INFERRED]` **Window normalization.**
  For any family with nonzero on-template production, use the allowed whole-
  sheet exact scaling from Step 3 to transport the family to a normalized
  activation window
  `I = [0, 1]`
  with
  `int_I D_on(t) dt = 1`.
  If
  `int_I D_on(t) dt = 0`,
  the family is marked `inadmissible-static` rather than renormalized.
- `[INFERRED]` **Interaction currency.**
  The same projected forcing ledger is used throughout:

  ```text
  D_on(t)
    := |Q_clk(t)| + |Q_seed(t)| + |Q_amp(t)|
       + |Q_rot^D(t)| + |Q_rot^A(t)| + |Q_next(t)|

  D_off(t)
    := D_mirror(t) + D_companion(t) + D_feedback(t) + D_cross(t).
  ```

## Hard Admissibility Filters

- `[INFERRED]` **A_live.**
  A family may be evaluated positively only if
  `int_I D_on(t) dt > 0`.
  This blocks vacuous wins from static cancellation packets such as exact
  Beltrami alignment.
- `[VERIFIED]` **A_sheet.**
  The family must use the frozen packet semantics, mandatory conjugate
  completion, spectator partition, and one predeclared sign / phase / amplitude
  sheet.
- `[VERIFIED]` **A_closure.**
  The report must retain the full desired-channel ledger together with the
  classwise spectator ledger; dropping mirrors, companions, feedback, or
  cross-scale spill channels is inadmissible.
- `[INFERRED]` **A_trace.**
  Any positive `Delayed-Threshold Itinerary` verdict additionally requires an
  explicit ordered event trace on the normalized window.
  Without that trace the outcome is `ambiguous`, not `pass`.
- `[INFERRED]` **A_grid.**
  No later dossier may widen the Step-4 family search after outcomes are seen.
  The only nontrivial anti-circuit family points are
  `delta in {1/16, 1/8}`
  and
  `eta_C in {1/256, 1/128}`.
  The two pro-circuit families are tested exactly as frozen below, with no
  extra sign-sheet or scale-ratio search.
- `[INFERRED]` **A_empty.**
  If a frozen family cannot actually be realized on the fixed packet object
  with its declared sign / phase / scaling sheet, the later dossier must record
  `family empty` rather than replace it by a nearby variant.

## Frozen Step-4 Family Ledger

| Family | Type | Frozen definition | Cases covered |
| --- | --- | --- | --- |
| `F_BM` | anti-circuit | exact Beltrami-aligned role packet with mandatory mirror completion and frozen same-helicity sign sheet `sigma_BM`; the exact nonlinear forcing ledger is static so `int_I D_on = 0`, which later dossiers must read as `inadmissible-static` under `A_live` rather than as a positive witness | `Beltrami cancellation`, `mirror-mode completion` |
| `F_DT(delta, eta_C)` | anti-circuit | nearly-degenerate trigger-stress family on the same one-bridge packet with frozen baseline sign sheet `sigma_DT`; parameter grid `delta in {1/16, 1/8}`, `eta_C in {1/256, 1/128}`; initial amplitudes are `(|A_n(0)|, |B_n(0)|, |C_n(0)|, |D_n(0)|, |E_n(0)|) = (1, 1/32, eta_C, 0, 0)` and the trigger-facing desired coefficients satisfy `|c_seed| <= delta`, `|c_amp| <= delta` on the frozen exact coefficient ledger | `nearly degenerate triads`, `tiny trigger modes` |
| `F_SS` | pro-circuit | engineered-sign sparse-triad family with one primary mode per role, mandatory conjugates, and only closure-forced companions; frozen sign/phase sheets `sigma_SS`, `phi_SS`; normalized by `int_I D_on = 1`; the initial tiny trigger is fixed at `|C_n(0)| = 1/128`; each spectator-class coefficient envelope is required to be `<= 1/16` on the normalized initial ledger | `engineered helical sign patterns`, `sparse triad geometries` |
| `F_SL` | pro-circuit | scale-separated family with fixed shell ratio `|k_{n+1}|/|k_n| = 8`, frozen sign/phase sheets `sigma_SL`, `phi_SL`, and the same normalization `int_I D_on = 1`; spectator leakage is required to be nonzero in at least one class but each initial classwise coefficient envelope is `<= 1/12` on the normalized window | `scale-separated packets`, `leakage exists but may be dynamically negligible` |

- `[INFERRED]` The family labels
  `sigma_BM`,
  `sigma_DT`,
  `sigma_SS`,
  `sigma_SL`
  and any paired phase sheets are not later optimization variables.
  Each must be written once at the start of the corresponding dossier on the
  frozen role order and then kept fixed.

### Why These Four Families Are The Right Step-4 Menu

- `[VERIFIED]` The anti-circuit side must include Beltrami fragility,
  mirror completion, near-degenerate geometry, and tiny-trigger stress because
  those are the adverse cases the winning chain names explicitly.
- `[VERIFIED]` The pro-circuit side must include engineered sign patterns,
  sparse geometry, scale separation, and small-but-nonzero leakage because the
  Step-4 attack packet says the audit is biased without them.
- `[INFERRED]` This four-family menu is minimal while still covering the whole
  required adverse/favorable slate on one frozen burden currency.

## Predeclared Candidate Sheet

### 1. Template-Defect Near-Closure

- `[INFERRED]` Freeze the role hierarchy sheet

  ```text
  (h_seed, h_clk, h_amp, h_rot, h_next)
    = (1/16, 1/4, 1, 2, 2)
  ```

  with normalization floor

  ```text
  eps_ref = 1/64.
  ```

- `[INFERRED]` Freeze tolerances

  ```text
  lambda_tmpl = 1/3,
  lambda_spec = 1/4.
  ```

- `[INFERRED]` Candidate passes on a family only if

  ```text
  Delta_tmpl <= 1/3
  and
  Delta_spec <= 1/4.
  ```

- `[INFERRED]` Diagnostic vector to retain:

  ```text
  v_tmpl(F)
    = (
        Delta_tmpl,
        Delta_spec,
        Q_clk, Q_seed, Q_amp, Q_rot^D, Q_rot^A, Q_next,
        D_mirror, D_companion, D_feedback, D_cross
      ).
  ```

### 2. Windowed Spectator-Leakage Budget

- `[INFERRED]` Freeze leakage budgets

  ```text
  Lambda_tot      = 3/8,
  Lambda_mirror   = 1/8,
  Lambda_companion= 1/12,
  Lambda_feedback = 1/12,
  Lambda_cross    = 1/12.
  ```

- `[INFERRED]` Candidate passes on a family only if

  ```text
  L_tot        <= 3/8,
  L_mirror     <= 1/8,
  L_companion  <= 1/12,
  L_feedback   <= 1/12,
  L_cross      <= 1/12.
  ```

- `[INFERRED]` Diagnostic vector to retain:

  ```text
  v_leak(F)
    = (
        L_tot,
        L_mirror,
        L_companion,
        L_feedback,
        L_cross,
        int_I |Q_clk|,
        int_I |Q_seed|,
        int_I |Q_amp|,
        int_I |Q_rot^D|,
        int_I |Q_rot^A|,
        int_I |Q_next|,
        int_I D_on,
        int_I D_off
      ).
  ```

### 3. Delayed-Threshold Itinerary

- `[INFERRED]` Freeze event thresholds

  ```text
  theta_B = 1/8,
  theta_C = 1/4,
  theta_D = 1/2,
  theta_E = 3/4,
  Lambda_itin = 1/3,
  kappa_rot = 2.
  ```

- `[INFERRED]` Candidate passes on a family only if there exist

  ```text
  0 < t_clk < t_trig < t_rot < t_next <= 1
  ```

  satisfying the Step-2 ordered event conditions on the same normalized window.
- `[INFERRED]` Diagnostic vector to retain:

  ```text
  v_itin(F)
    = (
        t_clk,
        t_trig,
        t_rot,
        t_next,
        |B(t_clk)|,
        |C|_pretrigger^max,
        |D(t_rot)|,
        |E(t_next)|,
        max_{t in [0, t_next]} D_off / D_on,
        max_{t in [0, t_next]} D_mirror / D_on,
        max_{t in [0, t_next]} D_companion / D_on,
        max_{t in [0, t_next]} D_feedback / D_on,
        max_{t in [0, t_next]} D_cross / D_on,
        rotor_margin
      ).
  ```

## No-Retuning Discipline

- `[VERIFIED]` No later dossier may change:
  the packet object,
  the spectator partition,
  the finite window,
  the sign sheet of a given family,
  the phase sheet of a given family,
  the family table itself,
  the `F_DT` parameter grid,
  the role hierarchy sheet,
  `lambda_tmpl`,
  `lambda_spec`,
  `Lambda_tot`,
  class budgets,
  `theta_B`,
  `theta_C`,
  `theta_D`,
  `theta_E`,
  `Lambda_itin`,
  or
  `kappa_rot`
  after outcomes are seen.
- `[VERIFIED]` No family may be rescued by dropping mirror completion,
  redefining `D_on` / `D_off`,
  or importing Tao's averaged coefficient freedoms.

## Exploration-Ready Verdict

- `[VERIFIED]` Step 4 now has one fixed normalized family ledger and one fixed
  quantitative pass/fail sheet.
- `[INFERRED]` `exploration-002` can now run the anti-circuit dossier on
  `F_BM` and `F_DT(delta, eta_C)` without changing the burden currency.
- `[INFERRED]` `exploration-003` can now run the pro-circuit dossier on
  `F_SS` and `F_SL` on the same ledger.
