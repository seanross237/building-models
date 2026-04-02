# Exploration 001 Report - Candidate Definition Family

## Goal

Promote a bounded family of exact candidate notions of `near-closed Tao
circuit` that inherit the Step-1 freezes and are sharp enough to be real test
objects rather than slogans.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-001/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-001-feature-ledger.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-002-packet-language-memo.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/planner-chains/chain-02.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/final-decider.md`
- `runtime/logs/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-002-receptionist-search-attempt-003.md`

## Common Packet And Channel Notation

- `[INFERRED]` Work on one canonical one-bridge packet family
  `P_n = (A_n, B_n, C_n, D_n, E_n)` with a finite spectator packet `S_n`, where:
  - `A_n` is the active carrier (`X1,n`);
  - `B_n` is the slow clock (`X2,n`);
  - `C_n` is the tiny trigger (`X3,n`);
  - `D_n` is the transfer conduit / rotor leg (`X4,n`);
  - `E_n` is the next carrier (`X1,n+1`);
  - `S_n` is the finite packet of forced non-role spectators kept after the same
    packet semantics and mandatory conjugate completion are applied.
- `[INFERRED]` Every packet is a finite role-labeled helical packet with
  mandatory conjugate completion, one frozen helical sign sheet, one amplitude
  normalization anchor, and one phase anchor.
- `[INFERRED]` Let `N(u,u)` be the exact quadratic NS nonlinearity in the fixed
  canonical representation, and let `Pi_R N(u,u)` denote the role projection
  onto `R in {A,B,C,D,E}`.
- `[INFERRED]` Let `U_{P_n}(t) := (A_n(t), B_n(t), C_n(t), D_n(t), E_n(t))`
  denote the canonically anchored role-amplitude vector on the declared
  sign/amplitude/phase sheet.
- `[INFERRED]` The desired Tao-like channel menu is:
  - `Q_clk`: `(A_n, A_n) -> B_n`
  - `Q_seed`: `(A_n, A_n) -> C_n`
  - `Q_amp`: `(B_n, C_n) -> C_n`
  - `Q_rot^A`: `(C_n, D_n) -> A_n`
  - `Q_rot^D`: `(C_n, A_n) -> D_n`
  - `Q_next`: `(D_n, D_n) -> E_n`
- `[VERIFIED]` The exact-NS danger classes are fixed by the local record:
  mirror / conjugate companions, same-scale companion triads, long-leg
  feedback, and cross-scale next-shell feedback; source:
  `atlas-anatomy-exploration-002-REPORT.md`.
- `[INFERRED]` Every hierarchy parameter, tolerance, and normalization floor
  appearing below is part of the candidate sheet and must be fixed once for the
  whole packet class before any audit. There is no packet-by-packet retuning.

## Promoted Candidate Menu

### Candidate 1 - Template-Defect Near-Closure

- Intent:
  compare the exact role-projected NS vector field against one fixed Tao-like
  five-channel template on a finite activation window.
- Classification:
  `dual-use`
- Uses frozen commitments:
  packet-level helical object,
  conjugate completion,
  stage order,
  delayed threshold,
  amplitude hierarchy,
  helical sign / phase sheet,
  fixed finite window,
  one downstream gate.
- Supporting files:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-001-feature-ledger.md`,
  `library-inbox/step-001-exploration-002-packet-language-memo.md`,
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `atlas-source/atlas-anatomy-exploration-002-REPORT.md`,
  `planning-runs/run-001/judgments/chain-01.md`,
  `planning-runs/run-001/attacks/chain-01.md`.
- Exact criterion:

  ```text
  Fix one role hierarchy

    0 < h_seed << h_clk < 1 < h_amp < h_rot, h_next

  and define

    F_h(A,B,C,D,E)
      := (
           -h_rot C D - h_clk A B - h_seed A C,
            h_clk A^2 - h_amp C^2,
            h_seed A^2 + h_amp B C,
            h_rot C A - h_next D E,
            h_next D^2
         ).

  Use the role-normalized norm

    ||X||_role
      := max(
           |X_A|,
           h_clk^(-1) |X_B|,
           h_seed^(-1) |X_C|,
           h_rot^(-1) |X_D|,
           h_next^(-1) |X_E|
         ).

  Then define, on one fixed window I = [0, T_act] and with one fixed
  normalization floor eps_ref > 0,

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

  Candidate condition:

    Delta_tmpl <= lambda_tmpl
    and
    Delta_spec <= lambda_spec

  for predeclared tolerances lambda_tmpl, lambda_spec in (0,1).
  ```

- Why it is honest:
  it does not import Tao's literal coefficients, but it does force one exact
  five-channel role template, one declared hierarchy, and one spectator budget.

### Candidate 2 - Windowed Spectator-Leakage Budget

- Intent:
  measure whether the desired channels dominate the structurally forced
  spectators on one fixed finite window.
- Classification:
  `obstruction-oriented`
- Uses frozen commitments:
  packet-level helical object,
  conjugate completion,
  explicit spectator classes,
  fixed finite window,
  one declared normalization,
  one downstream admissibility gate.
- Supporting files:
  `steps/step-001/RESULTS.md`,
  `atlas-source/atlas-anatomy-exploration-002-REPORT.md`,
  `planning-runs/run-001/planner-chains/chain-02.md`,
  `planning-runs/run-001/final-decider.md`,
  `runtime/logs/codex-patlas-exact-ns-no-near-closed-tao-circuit-step-002-receptionist-search-attempt-003.md`.
- Exact criterion:

  ```text
  Let

    D_on(t)
      := |Q_clk(t)| + |Q_seed(t)| + |Q_amp(t)|
         + |Q_rot^A(t)| + |Q_rot^D(t)| + |Q_next(t)|.

  Partition the forced off-template channels into

    S_mirror,
    S_companion,
    S_feedback,
    S_cross

  and define

    D_off^class(t) := sum_{r in S_class} |Q_r(t)|,
    D_off(t)       := D_off^mirror + D_off^companion
                      + D_off^feedback + D_off^cross.

  On one fixed window I = [0, T_act], set

    L_class(P_n; I)
      := int_I D_off^class(t) dt / int_I D_on(t) dt,

    L_tot(P_n; I)
      := int_I D_off(t) dt / int_I D_on(t) dt.

  Candidate condition:

    L_tot <= Lambda_tot
    and
    L_class <= Lambda_class

  for each predeclared spectator class.
  ```

- Why it is honest:
  it states exactly what is counted as on-template versus off-template forcing,
  keeps all comparisons in one declared interaction currency, and avoids vague
  "NS has too many couplings" rhetoric.

### Candidate 3 - Delayed-Threshold Itinerary

- Intent:
  keep the notion friendly to a genuine pro-near-circuit outcome by asking for
  one finite ordered activation itinerary rather than immediate coefficient
  matching.
- Classification:
  `construction-oriented`
- Uses frozen commitments:
  role hierarchy,
  stage order,
  tiny-trigger centrality,
  amplitude hierarchy,
  finite activation window,
  fixed sign / phase / normalization sheet,
  explicit spectator screen.
- Supporting files:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-001-feature-ledger.md`,
  `atlas-source/atlas-anatomy-exploration-001-REPORT.md`,
  `atlas-source/atlas-anatomy-exploration-002-REPORT.md`,
  `planning-runs/run-001/judgments/chain-01.md`,
  `planning-runs/run-001/attacks/chain-01.md`.
- Exact criterion:

  ```text
  Fix thresholds

    0 < theta_B < theta_C < theta_D < theta_E <= 1,
    Lambda_itin in (0,1),
    kappa_rot > 1,

  together with the canonical amplitude anchor |A_n(0)| = 1
  and canonical phase anchor arg A_n(0) = 0.

  Candidate condition:
  there exist times

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

- Why it is honest:
  it does not ask for Tao's averaged ODE by name. It asks for one finite exact
  activation itinerary written only in role-projected exact NS channel data.

## Candidate Rejected Before Promotion

- `[INFERRED]` A `graph-closure only` notion was not promoted.
- Reason:
  the attack memo is right that exact closure graphs by themselves are too
  combinatorial and basis-sensitive. They do not remember the frozen helical
  sign sheet, the phase anchor, or the amplitude hierarchy, so they are not
  honest near-closure objects under the Step-1 packet semantics.
- `[INFERRED]` A `projection-rigidity only` notion was not promoted.
- Reason:
  the local record treats exact Leray / pressure projection as the mechanism
  enforcing coefficient rigidity and spectator leakage, not as a distinct
  near-closure object. Promoting it as a fourth candidate would have produced a
  mechanism label instead of a test object.
- `[INFERRED]` A `threshold-only delayed-transfer slogan` was not promoted.
- Reason:
  a bare statement that some trigger crosses some threshold can always be tuned
  after the fact unless it is tied to exact role channels, one fixed window,
  and one spectator budget. Candidate 3 survives only because it adds those
  exact ingredients.

## Outcome

- `[INFERRED]` The honest promoted family has three candidates:
  `Template-Defect Near-Closure`,
  `Windowed Spectator-Leakage Budget`,
  `Delayed-Threshold Itinerary`.
- `[INFERRED]` None of the three fails immediately at definition level.
- `[INFERRED]` The definition-level lesson is a split outcome, not a single
  global object:
  one template-defect notion,
  one leakage-budget notion,
  and one behavioral itinerary notion.
- `[INFERRED]` The remaining work is to attach one exact interaction template
  sheet and one downstream gate to each candidate, then decide Step-3
  readiness.
