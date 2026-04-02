# Exploration 002 Report - Split Or Discard The Itinerary Candidate

## Goal

Decide whether `Delayed-Threshold Itinerary` can be honestly split into:

- `pre-trigger delay filter`
- `next-stage transfer-start filter`

on the same frozen packet sheet, finite window, and threshold language, or
whether the behavior-based route should be discarded after one repair pass.

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

## Original Itinerary Criterion

- `[VERIFIED]` The Step-2 criterion requires times

  ```text
  0 < t_clk < t_trig < t_rot < t_next <= T_act
  ```

  with five clauses:
  clock growth,
  delayed trigger,
  rotor event,
  next-stage transfer,
  and spectator screen.
- `[VERIFIED]` The ambiguity isolated by Step 4 is late-stage:
  `F_SS(mu)` fixes all four event times,
  while
  `F_SL(rho)` still lacks a uniformly fixed exact `t_next` trace on the local
  record.
- `[VERIFIED]` The same Step-4 dossier also shows that leakage is already small
  on `F_SL(rho)`, so the bottleneck is event-trace rigidity rather than
  isolation failure.

## Split Candidate A - `Pre-Trigger Delay Filter`

### Exact Definition

- `[PROPOSED]` Keep the original fixed packet sheet, thresholds, sign sheet,
  and finite window.
- `[PROPOSED]` Define `pre-trigger delay filter` by retaining only the early
  itinerary clauses:

  ```text
  there exist times 0 < t_clk < t_trig <= T_act such that

  (i)  Re(conj(B_n) Q_clk) > 0 on [0, t_trig]
       and |B_n(t_clk)| = theta_B;

  (ii) |C_n(t)| < theta_C for t < t_trig,
       |C_n(t_trig)| = theta_C,
       and Re(conj(C_n)(Q_seed + Q_amp)) > 0 on [t_clk, t_trig];

  (iii) max_{t in [0, t_trig]} D_off(t) / D_on(t) <= Lambda_itin.
  ```

- `[INFERRED]` This is an honest split notion because it uses the same fixed
  window and the same early threshold language rather than inventing new
  events.

### Step-4 Read

- `[VERIFIED]` `F_DT(delta, eta)`:
  fails.
  The trigger bound gives
  `t_trig > 1`,
  so no delayed-trigger event occurs on the frozen window.
- `[VERIFIED]` `F_SS(1/12)`:
  passes with
  `t_clk = 1/6`,
  `t_trig = 1/3`,
  and spectator ratio `1/4 < 1/3`.
- `[VERIFIED]` `F_SL(1/16)`:
  passes the early-stage read with
  `t_clk = 1/5`,
  `t_trig = 2/5`,
  `|C|_pretrigger^max < theta_C`,
  and spectator ratio `49/256 < 1/3`.

### Downstream-Gate Check

- `[PROPOSED]` Gate:
  one exact admissibility sheet

  ```text
  G_pre(P_n; I) = (t_clk, t_trig, max_{[0, t_trig]} D_off / D_on; sign sheet)
  ```

- `[VERIFIED]` This gate is precise and lives on the same frozen burden
  currency.
- `[INFERRED]` It is still too weak for the shortlist:
  it remains only a narrow admission filter and does not name a new theorem-
  facing or counterexample-facing quantity beyond the stronger template and
  leakage screens that already survive the same families.
- `[INFERRED]` Earned negative bucket:
  `not useful for the target theorem or counterexample question`.

### Status

- `[INFERRED]` `pre-trigger delay filter` is
  `discarded`
  after the repair pass.
  The notion is exact enough, but it does not justify a separate Step-6 object
  freeze.

## Split Candidate B - `Next-Stage Transfer-Start Filter`

### Can It Be Defined Honestly?

- `[INFERRED]` The late-stage ambiguity in Step 4 is exactly that the local
  record does not pin a uniformly fixed exact `t_next` trace on `F_SL(rho)`.
- `[VERIFIED]` If the split keeps the original late threshold language
  `|E_n(t_next)| >= theta_E`,
  then the same ambiguity remains.
- `[VERIFIED]` If the split instead weakens the late clause to a mere onset of
  positive `Q_next` or some earlier transfer-start event, then it changes the
  original event/threshold language after outcomes are known.
- `[INFERRED]` Therefore no honest Step-5 split notion removes the
  `F_SL(rho)` ambiguity while preserving the original late-stage threshold
  sheet.

### Status

- `[INFERRED]` `next-stage transfer-start filter` is
  `discarded`
  as
  `not well-defined`.

## Repair-Pass Verdict On The Itinerary Route

- `[VERIFIED]` The low-leakage friendly family already shows that the late-stage
  ambiguity is not caused by excessive spectators.
- `[INFERRED]` The split attempt therefore resolves the Step-4 bottleneck
  sharply:
  the early-stage piece is exact but not useful enough,
  and the late-stage piece is not well-defined without changing the event
  language.
- `[INFERRED]` `Delayed-Threshold Itinerary` should not survive into the final
  Step-5 shortlist.
