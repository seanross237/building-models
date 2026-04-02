# Step 2 Results - Candidate Definitions And Exact Interaction Templates

## Completion Status

- Step complete: **yes**
- Kill condition fired: **no**
- Branch status: **Chain Step 3 is now well-posed**
- Honest summary:
  `[INFERRED]` the Step-1 freezes support a bounded three-candidate family:
  one template-defect notion,
  one leakage-budget notion,
  and one delayed-threshold behavioral notion.
  All three are attached to the same exact role-labeled helical packet object,
  the same exact five-channel core, and one named downstream gate.
- Operational note:
  `[VERIFIED]` a fresh receptionist wrapper run created a specific search log
  but no formal receptionist result file; `[VERIFIED]` both explorer launches
  moved into `active` status without writing sentinels, so the exploration
  reports were completed directly from the anchored local source packet after a
  bounded dispatcher pass; `[VERIFIED]` curator launches were issued, but
  curation receipts are still pending.

## Source Basis

Primary step outputs:

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT-SUMMARY.md`
- `runtime/logs/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-002-receptionist-search-attempt-003.md`

Main inherited local sources:

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-001/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-001-feature-ledger.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-002-packet-language-memo.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN-HISTORY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/planner-chains/chain-02.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/final-decider.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `library/meta/obstruction-screening/a-scope-lock-is-not-real-until-baseline-cash-out-and-threshold-are-frozen-in-the-same-burden-currency.md`

## Common Packet Class And Notation

- `[INFERRED]` All three candidates live on one canonical one-bridge packet
  family
  `P_n = (A_n, B_n, C_n, D_n, E_n)`
  with role meanings:
  `A_n = active carrier`,
  `B_n = slow clock`,
  `C_n = tiny trigger`,
  `D_n = transfer conduit / rotor leg`,
  `E_n = next carrier = A_{n+1}`.
- `[INFERRED]` Packet identity lives at the finite role-labeled helical packet
  level, with mandatory conjugate completion only as canonical real-valued
  bookkeeping.
- `[VERIFIED]` The exact desired role channels are the Tao-like five-channel
  core inherited from the atlas packet:
  `A -> B`,
  `A -> C`,
  `B,C -> C`,
  `C,A <-> D`,
  `D,D -> E`.
- `[VERIFIED]` The exact forced extras later steps must audit are:
  mirror / conjugate companions,
  same-scale companion triads,
  long-leg feedback,
  and cross-scale next-shell feedback.

## Candidate Table

`[INFERRED]` The promoted candidate family is:

| Candidate | Intent | Classification | Packet class | Downstream gate |
| --- | --- | --- | --- | --- |
| `Template-Defect Near-Closure` | compare exact projected dynamics against one fixed Tao-like five-channel template | `dual-use` | one-bridge role-labeled helical packet with mandatory conjugate completion | invariant template-defect observable |
| `Windowed Spectator-Leakage Budget` | compare desired-channel forcing against structurally forced spectators in the same interaction currency | `obstruction-oriented` | same canonical one-bridge packet family | hard leakage admissibility sheet |
| `Delayed-Threshold Itinerary` | ask whether one finite exact activation itinerary survives without importing Tao's averaged coefficients | `construction-oriented` | same canonical one-bridge packet family | ordered-threshold admissibility sheet |

## Definition Sheet For Each Candidate

### 1. Template-Defect Near-Closure

- `[PROPOSED]` Exact criterion:

  ```text
  Fix one role hierarchy

    0 < h_seed << h_clk < 1 < h_amp < h_rot, h_next

  and one role-normalized Tao-like template

    F_h(A,B,C,D,E)
      := (
           -h_rot C D - h_clk A B - h_seed A C,
            h_clk A^2 - h_amp C^2,
            h_seed A^2 + h_amp B C,
            h_rot C A - h_next D E,
            h_next D^2
         ).

  Use the role norm

    ||X||_role
      := max(
           |X_A|,
           h_clk^(-1) |X_B|,
           h_seed^(-1) |X_C|,
           h_rot^(-1) |X_D|,
           h_next^(-1) |X_E|
         ).

  On one fixed window I = [0, T_act], define

    Delta_tmpl(P_n; I)
      := sup_{t in I}
         || Pi_{P_n} N(u,u)(t) - F_h(U_{P_n}(t)) ||_role
         /
         ( || F_h(U_{P_n}(t)) ||_role + eps_ref ),

    Delta_spec(P_n; I)
      := sup_{t in I}
         || Pi_{S_n} N(u,u)(t) ||_role
         /
         ( || F_h(U_{P_n}(t)) ||_role + eps_ref ).

  Near-closed means

    Delta_tmpl <= lambda_tmpl
    and
    Delta_spec <= lambda_spec

  for predeclared tolerances lambda_tmpl, lambda_spec in (0,1).
  ```

- `[INFERRED]` Packet class:
  the canonical one-bridge role-labeled helical packet `P_n`.
- `[INFERRED]` Threshold role:
  `lambda_tmpl` and `lambda_spec` are the only admissibility thresholds.
  They measure deviation from the declared five-channel template and the size
  of off-template forcing in the same role-normalized currency.
- `[INFERRED]` Finite window:
  one fixed activation window `I = [0, T_act]`.
- `[INFERRED]` Canonical inputs:
  one helical sign sheet,
  one amplitude anchor,
  one phase anchor,
  one conjugate-completion convention,
  one role order.
- `[VERIFIED]` Step-1 commitments used:
  packet-level support,
  delayed-threshold role ledger,
  amplitude hierarchy,
  time-scale separation,
  explicit sign / phase bookkeeping.
- `[VERIFIED]` Supporting files:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-001-feature-ledger.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `atlas-source/atlas-anatomy-exploration-002-REPORT.md`,
  `planning-runs/run-001/judgments/chain-01.md`,
  `planning-runs/run-001/attacks/chain-01.md`.

### 2. Windowed Spectator-Leakage Budget

- `[PROPOSED]` Exact criterion:

  ```text
  Let

    D_on(t)
      := |Q_clk(t)| + |Q_seed(t)| + |Q_amp(t)|
         + |Q_rot^A(t)| + |Q_rot^D(t)| + |Q_next(t)|.

  Partition forced off-template channels into

    S_mirror,
    S_companion,
    S_feedback,
    S_cross.

  Define

    D_off^class(t) := sum_{r in S_class} |Q_r(t)|,
    D_off(t)       := D_off^mirror + D_off^companion
                      + D_off^feedback + D_off^cross.

  On one fixed window I = [0, T_act], set

    L_class(P_n; I)
      := int_I D_off^class(t) dt / int_I D_on(t) dt,

    L_tot(P_n; I)
      := int_I D_off(t) dt / int_I D_on(t) dt.

  Near-closed means

    L_tot <= Lambda_tot
    and
    L_class <= Lambda_class

  for each predeclared spectator class.
  ```

- `[INFERRED]` Packet class:
  the same canonical one-bridge role-labeled helical packet family.
- `[INFERRED]` Threshold role:
  `Lambda_tot` and the class budgets `Lambda_class` are the only admissibility
  thresholds. They bound forced leakage in the same interaction ledger as the
  desired channels.
- `[INFERRED]` Finite window:
  one fixed activation window `I = [0, T_act]`.
- `[INFERRED]` Canonical inputs:
  one sign sheet,
  one amplitude normalization,
  one phase anchor,
  one frozen spectator partition,
  one conjugate-completion convention.
- `[VERIFIED]` Step-1 commitments used:
  packet-level support,
  predeclared leakage criteria,
  mandatory conjugate completion,
  one downstream gate.
- `[VERIFIED]` Supporting files:
  `steps/step-001/RESULTS.md`,
  `atlas-source/atlas-anatomy-exploration-002-REPORT.md`,
  `planning-runs/run-001/planner-chains/chain-02.md`,
  `planning-runs/run-001/final-decider.md`,
  `runtime/logs/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-002-receptionist-search-attempt-003.md`.

### 3. Delayed-Threshold Itinerary

- `[PROPOSED]` Exact criterion:

  ```text
  Fix thresholds

    0 < theta_B < theta_C < theta_D < theta_E <= 1,
    Lambda_itin in (0,1),
    kappa_rot > 1,

  together with the canonical amplitude anchor |A_n(0)| = 1
  and canonical phase anchor arg A_n(0) = 0.

  Near-closed means there exist times

    0 < t_clk < t_trig < t_rot < t_next <= T_act

  such that

  (i) clock growth:
      Re(conj(B_n) Q_clk) > 0 on [0, t_trig]
      and |B_n(t_clk)| = theta_B;

  (ii) delayed trigger:
       |C_n(t)| < theta_C for t < t_trig,
       |C_n(t_trig)| = theta_C,
       Re(conj(C_n)(Q_seed + Q_amp)) > 0 on [t_clk, t_trig];

  (iii) rotor event:
        Re(conj(D_n) Q_rot^D) - Re(conj(A_n) Q_rot^A)
          >= kappa_rot D_off(t)
        on [t_trig, t_rot],
        with |D_n(t_rot)| >= theta_D;

  (iv) next-stage transfer:
       Re(conj(E_n) Q_next) > 0 on [t_rot, t_next]
       and |E_n(t_next)| >= theta_E;

  (v) spectator screen:
      max_{t in [0, t_next]} D_off(t) / D_on(t) <= Lambda_itin.
  ```

- `[INFERRED]` Packet class:
  the same canonical one-bridge role-labeled helical packet family.
- `[INFERRED]` Threshold role:
  `theta_B, theta_C, theta_D, theta_E` define the ordered activation events,
  while `Lambda_itin` caps spectator interference and `kappa_rot` demands a
  genuine rotor-dominance event.
- `[INFERRED]` Finite window:
  one fixed activation window `I = [0, T_act]`, with ordered event times inside
  it.
- `[INFERRED]` Canonical inputs:
  one sign sheet,
  one amplitude anchor,
  one phase anchor,
  one conjugate-completion rule,
  one role order.
- `[VERIFIED]` Step-1 commitments used:
  stage order,
  delayed-threshold logic,
  tiny-trigger centrality,
  amplitude hierarchy,
  time-scale separation,
  explicit phase / sign sheet,
  fixed finite window.
- `[VERIFIED]` Supporting files:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-001-feature-ledger.md`,
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `atlas-source/atlas-anatomy-exploration-002-REPORT.md`,
  `planning-runs/run-001/judgments/chain-01.md`,
  `planning-runs/run-001/attacks/chain-01.md`.

## Exact Interaction Template Sheet

### Template-Defect Near-Closure

- `[VERIFIED]` Desired couplings:
  `Q_clk, Q_seed, Q_amp, Q_rot^A, Q_rot^D, Q_next`.
- `[VERIFIED]` Automatically forced couplings:
  mirror partners,
  same-scale companion targets,
  long-leg rotor feedback,
  next-shell feedback.
- `[INFERRED]` Later Step-3 data still needed:
  exact helical coefficients and sign stability under the frozen canonical
  sheet,
  phase sensitivity of repeated target-role sums,
  and canonicalization stability of the role packet.

### Windowed Spectator-Leakage Budget

- `[VERIFIED]` Desired couplings:
  the same five-channel core, now only as the denominator ledger `D_on`.
- `[VERIFIED]` Automatically forced couplings:
  every off-template channel in the four spectator classes
  `mirror`,
  `companion`,
  `feedback`,
  `cross`.
- `[INFERRED]` Later Step-3 data still needed:
  whether the spectator partition is stable under canonicalization and whether
  any leakage budget is threshold-gerrymandered.

### Delayed-Threshold Itinerary

- `[VERIFIED]` Desired couplings:
  the same five-channel core, now only through the ordered activation events it
  induces.
- `[VERIFIED]` Automatically forced couplings:
  any spectator channel that can reorder
  `clock -> trigger -> rotor -> next-stage transfer`
  or destroy the gate-sized status of `B_n` and `C_n`.
- `[INFERRED]` Later Step-3 data still needed:
  event-time stability under canonicalization,
  sign stability under the frozen helical sheet,
  and performance on balanced anti-circuit and pro-circuit packet tests.

## Downstream-Gate Ledger

| Candidate | One downstream gate | Why this is the right next audit |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `[INFERRED]` one invariant template-defect observable `G_tmpl(P_n; I) := (Delta_tmpl, Delta_spec)` | it asks exactly whether the same canonically frozen packet keeps the same Tao-like vector-field defect after Step-3 robustness screening |
| `Windowed Spectator-Leakage Budget` | `[INFERRED]` one hard admissibility sheet `G_leak(P_n; I) := (L_tot, L_mirror, L_companion, L_feedback, L_cross)` | it is the cleanest way to test the spectator-leakage route in one fixed interaction currency without soft scoring |
| `Delayed-Threshold Itinerary` | `[INFERRED]` one ordered-threshold admissibility sheet `G_itin(P_n; I) := (t_clk, t_trig, t_rot, t_next; sign sheet; spectator pass/fail)` | it is the smallest honest gate for a pro-near-circuit-friendly candidate, because the candidate lives or dies on ordered exact activation events |

## Candidate Verdict

- `[VERIFIED]` Chain Step 3 is now well-posed.
- `[INFERRED]` Survivors into Step-3 robustness audit:
  `Template-Defect Near-Closure`,
  `Windowed Spectator-Leakage Budget`,
  `Delayed-Threshold Itinerary`.
- `[INFERRED]` Immediate failures:
  none of the three promoted candidates fails at Step-2 definition level.
- `[INFERRED]` Candidate filtered out before promotion:
  `projection-rigidity only`
  because the local record treats exact Leray / pressure projection as the
  enforcement mechanism behind the promoted objects, not as a distinct
  near-closure notion.
- `[INFERRED]` Candidate-specific risk ranking for Step 3:
  - lowest risk of immediate collapse:
    `Windowed Spectator-Leakage Budget`
  - strongest theorem-facing but more canonicalization-sensitive:
    `Template-Defect Near-Closure`
  - strongest pro-near-circuit-friendly but most sensitive to phase / sign /
    time-window choices:
    `Delayed-Threshold Itinerary`

## Surviving Candidates For Chain Step 3

- `[INFERRED]` `Template-Defect Near-Closure`
  survives as the cleanest role-template object if the canonicalized defect
  observable is stable.
- `[INFERRED]` `Windowed Spectator-Leakage Budget`
  survives as the cleanest obstruction-facing object if the spectator partition
  is canonical enough.
- `[INFERRED]` `Delayed-Threshold Itinerary`
  survives as the honest pro-near-circuit candidate if the ordered event sheet
  is not a representation artifact.
