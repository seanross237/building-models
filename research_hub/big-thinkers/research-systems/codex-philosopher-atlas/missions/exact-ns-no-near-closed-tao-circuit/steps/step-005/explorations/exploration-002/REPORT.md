# Exploration 002 Report - Split Or Discard The Itinerary Candidate

## Goal

Decide whether `Delayed-Threshold Itinerary` can be honestly split into:

- `pre-trigger delay filter`
- `next-stage transfer-start filter`

on the same frozen packet sheet, finite window, and threshold language, or
whether one or both pieces must be discarded.

## Sources Used

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/code/f_dt_trigger_bound.py`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-003-exploration-002-robustness-audit-and-step-4-readiness.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/delayed-threshold-itinerary-fixes-one-exact-ordered-activation-sequence-with-predeclared-spectator-budgets.md`
- `library/meta/obstruction-screening/use-the-low-leakage-friendly-family-to-distinguish-event-trace-rigidity-from-isolation-failure.md`
- `library/meta/obstruction-screening/a-tao-screen-can-be-operational-on-an-exact-but-noncoercive-ledger-if-it-is-only-used-as-an-admission-filter.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-no-near-closed-tao-circuit-step-005-explorer-002`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-002/REPORT-SUMMARY.md`.
- `[VERIFIED]` Within a bounded wait, only a placeholder summary landed and the
  exploration remained active.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Reconstruction Of The Original Step-2 Criterion

- `[VERIFIED]` Step 2 defines `Delayed-Threshold Itinerary` by requiring times

  ```text
  0 < t_clk < t_trig < t_rot < t_next <= T_act
  ```

  together with the exact clauses

  ```text
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

- `[VERIFIED]` The fixed threshold sheet inherited from Step 4 is

  ```text
  theta_B = 1/8,
  theta_C = 1/4,
  theta_D = 1/2,
  theta_E = 3/4,
  Lambda_itin = 1/3,
  kappa_rot = 2.
  ```

## Where The `F_SL(rho)` Ambiguity Actually Enters

- `[VERIFIED]` The Step-4 dossier for `F_SL(rho)` already fixes the early trace

  ```text
  t_clk  = 1/5,
  t_trig = 2/5,
  t_rot  = 4/5,
  |C|_pretrigger^max < theta_C,
  |D(t_rot)| >= theta_D,
  rotor_margin = 1/2.
  ```

- `[VERIFIED]` The same dossier also already fixes the spectator load tightly
  enough:

  ```text
  max_{t in [0,1]} D_off / D_on = 3 rho + rho^2 <= 37/144 < 1/3
  ```

  for the frozen family range `0 < rho <= 1/12`.
- `[INFERRED]` So the ambiguity is **not** a leakage-budget problem and **not**
  an early trigger / rotor problem.
- `[VERIFIED]` The unresolved entry is exactly

  ```text
  t_next = 1 - O(rho) or drifts beyond 1 as rho -> 0,
  |E(t_next)| unresolved on the full family.
  ```

- `[INFERRED]` Therefore the precise source of the Step-4 ambiguity is:
  clause `(iv)` demands one exact terminal witness `t_next <= T_act` with
  `|E_n(t_next)| >= theta_E`,
  and clause `(v)` also extends to that same terminal witness.
  The inherited local record does not pin that witness uniformly on
  `F_SL(rho)`.

## Honest Split Boundary

- `[INFERRED]` The split boundary that actually isolates the `F_SL(rho)`
  ambiguity is between clauses `(iii)` and `(iv)`, not between `(ii)` and
  `(iii)`.
- `[INFERRED]` In other words, the shorthand label
  `pre-trigger delay filter`
  can only be made honest if it includes the rotor event clause `(iii)`.
  Stopping strictly at `t_trig` would miss the fact that `F_SL(rho)` already
  has a fixed rotor witness and would therefore fail to isolate the real
  ambiguity source.

## Proposed Split Notion 1 - `Pre-Trigger Delay Filter`

### Exact Definition On The Frozen Language

- `[PROPOSED]` Keep the same frozen packet object, sign sheet, amplitude/phase
  anchors, finite window, and threshold sheet.
- `[PROPOSED]` Define the early split notion by requiring:

  ```text
  there exist times 0 < t_clk < t_trig < t_rot <= T_act such that

  (i) clock growth holds exactly as in Step 2;
  (ii) delayed trigger holds exactly as in Step 2;
  (iii) rotor event holds exactly as in Step 2;
  (v_early) max_{t in [0, t_rot]} D_off(t) / D_on(t) <= Lambda_itin.
  ```

- `[INFERRED]` This uses only event times already present in the frozen Step-2
  sheet. No threshold is changed, no new event is invented, and the window is
  not moved.

### Test Against The Step-4 Dossier

| Family | Read | Reason |
| --- | --- | --- |
| `F_DT(delta, eta)` | `fails` | the trigger bound gives `t_trig > 1`, so the packet never reaches the early event tuple through `t_rot` |
| `F_SS(mu)` | `passes` | Step 4 records `t_clk = 1/6`, `t_trig = 1/3`, `t_rot = 2/3`, `|D(t_rot)| >= theta_D`, and spectator ratio `3 mu <= 1/4 < 1/3` |
| `F_SL(rho)` | `passes` | Step 4 already records `t_clk = 1/5`, `t_trig = 2/5`, `t_rot = 4/5`, `|C|_pretrigger^max < theta_C`, `|D(t_rot)| >= theta_D`, and `3 rho + rho^2 < 1/3` |

### Verdict

- `[INFERRED]` Overall status:
  `survives`.
- `[INFERRED]` This split notion removes the `F_SL(rho)` ambiguity honestly,
  because every datum it asks for is already fixed on the inherited frozen
  dossier.
- `[INFERRED]` Its concrete downstream gate is the early rotor-admission sheet

  ```text
  G_pre(P_n; I)
    = (
        t_clk,
        t_trig,
        t_rot,
        |C|_pretrigger^max,
        |D(t_rot)|,
        max_{t in [0, t_rot]} D_off / D_on,
        rotor_margin;
        sign sheet
      ).
  ```

- `[INFERRED]` This gate remains only a construction-facing admission filter,
  not a coercive theorem observable, but it is still concrete rather than
  cosmetic or bookkeeping-only. It asks one exact question on the frozen
  burden currency:
  can the packet realize delayed trigger plus genuine rotor activation before
  late transfer is asked?

## Proposed Split Notion 2 - `Next-Stage Transfer-Start Filter`

### Can It Be Defined Honestly On The Same Frozen Language?

- `[VERIFIED]` The frozen Step-2 language does **not** contain a distinct
  `transfer-start` event. Its late clause is a terminal-threshold clause:

  ```text
  Re(conj(E_n) Q_next) > 0 on [t_rot, t_next]
  and |E_n(t_next)| >= theta_E.
  ```

- `[INFERRED]` Therefore there are only two options:
  - keep `t_next` and the `theta_E` threshold exactly as written, in which case
    the original `F_SL(rho)` ambiguity remains untouched;
  - invent a weaker start-only event after `t_rot`, in which case the notion
    is no longer on the original event language.
- `[VERIFIED]` The second option is forbidden by the Step-5 instructions,
  because it would remove the ambiguity only by deleting the late-stage
  threshold requirement.

### Test Against The Step-4 Dossier

| Family | Read | Reason |
| --- | --- | --- |
| `F_DT(delta, eta)` | `fails` | no trigger and no rotor event occur on the fixed window, so the late transfer clause is never entered |
| `F_SS(mu)` | `passes` | Step 4 records the full late witness `t_next = 5/6` with the original next-stage clause intact |
| `F_SL(rho)` | `remains ambiguous` | the family only gives `t_next = 1 - O(rho)` or `> 1`, so the exact terminal witness demanded by the frozen late clause is not fixed uniformly |

### Verdict

- `[INFERRED]` Overall status:
  `discarded`.
- `[INFERRED]` Earned negative bucket:
  `not well-defined`.
- `[INFERRED]` Reason:
  as a genuinely separate split notion named
  `next-stage transfer-start filter`,
  it cannot be defined on the frozen Step-2 language without either
  collapsing back to the original terminal `t_next` clause
  or inventing a new weaker event.
  In the first case the ambiguity survives unchanged.
  In the second case the event language has been softened after outcomes were
  seen.

## Dead Ends And Rejected Repairs

- `[VERIFIED]` A tempting repair is to stop the early split at `t_trig`.
  I reject that because `F_SL(rho)` already has a fixed rotor witness
  `t_rot = 4/5`; the ambiguity starts later.
- `[VERIFIED]` Another tempting repair is to define the late notion by
  “positive `Q_next` after `t_rot`.”
  I reject that because it deletes the original terminal threshold
  `|E_n(t_next)| >= theta_E` and therefore changes the admissibility sheet
  after seeing outcomes.

## Final Outcome

- `[INFERRED]` The Step-4 ambiguity can be resolved without moving the window
  or softening the threshold sheet, but only by splitting the itinerary at the
  true ambiguity boundary:
  after the rotor event and before the terminal next-stage witness.
- `[INFERRED]` Final classification:
  - `pre-trigger delay filter`:
    `survives`.
  - `next-stage transfer-start filter`:
    `discarded`
    as
    `not well-defined`.
- `[INFERRED]` The one useful survivor is the early rotor-admission filter.
  The late transfer piece should not be carried into Step 6 unless a later step
  independently freezes one exact family-wide terminal `t_next` witness on the
  same packet sheet.
