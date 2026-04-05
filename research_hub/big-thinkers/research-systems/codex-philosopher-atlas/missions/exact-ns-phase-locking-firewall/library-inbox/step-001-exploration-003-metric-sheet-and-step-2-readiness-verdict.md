# Exploration 003 Report - Metric Sheet And Step-2 Readiness Verdict

## Goal

Define quantitative delayed-transfer metrics for the
`exact-ns-phase-locking-firewall`
branch using the intrinsic-object and search-class freezes, and issue a clean
verdict on whether Chain Step 2 is now well-posed.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/MISSION.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/mission-context.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-001-explorer-003`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-003/REPORT-SUMMARY.md`.
- `[VERIFIED]` The session wrote only an initial report skeleton within the
  bounded wait and did not produce the summary sentinel.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Metric Sheet

Assume later steps have fixed:

- one recursively closed exact support `S`;
- one predeclared source subset `A subset S`;
- one predeclared target subset `B subset S`;
- one spectator subset `R := S \\ (A union B)`;
- one exact trajectory on the closed support.

The partition `A / B / R` must be declared **before** any trajectory is scored.
Later steps are not allowed to relabel the partition after seeing the run.

### Exact energy-transfer observable

For any subset `X subset S`, define

```text
E_X(t) := sum_{m in X} |a_m(t)|^2,
D_X(t) := sum_{m in X} |k_m|^2 |a_m(t)|^2,
J_X(t) := E_X(t) - E_X(0) + 2 nu int_0^t D_X(s) ds.
```

- `[INFERRED]` `J_X(t)` is the exact cumulative nonlinear inflow to `X` after
  removing viscous loss on the same set.
- `[INFERRED]` This avoids ambiguous packet bookkeeping and uses only the exact
  closed-support energy balance.

### Intrinsic clocks

Define the instantaneous quadratic activity on the closed support

```text
Q_S(t) := sum_{tau in T(S)} |C_tau| |a_p(t)| |a_q(t)| |a_k(t)|.
```

Then define the support's turnover clock over any interval `[0,t]` by

```text
tau_turn(t) := inf_{0 <= s <= t} E_S(s) / Q_S(s),
E_S(t) := sum_{m in S} |a_m(t)|^2.
```

Define the fastest viscous clock on the support by

```text
tau_nu(S) := 1 / (nu max_{m in S} |k_m|^2).
```

- `[INFERRED]` `tau_turn` is a conservative intrinsic nonlinear time scale:
  if a purported delayed event occurs before a few copies of this clock have
  passed, it is just ordinary turnover-scale transfer.
- `[INFERRED]` `tau_nu` uses the fastest-decaying active mode, so it is the
  strictest viscous deadline available on the support.

### Delayed-transfer event

Let `t_*` be the first time such that

```text
J_B(t_*) >= (1/4) E_A(0).
```

The branch counts this as a delayed-transfer event only if

```text
t_* >= 3 tau_turn(t_*),
t_* <= (1/4) tau_nu(S).
```

- `[PROPOSED]` Threshold choice:
  `1/4` of the initial source energy is large enough to exclude tiny favorable
  blips while staying below full-transfer demands.
- `[PROPOSED]` Timing choice:
  `3 tau_turn`
  prevents ordinary immediate exchange from counting as delay, and
  `tau_nu / 4`
  requires the event to occur well before the support's fastest viscous decay
  erases it.

### Spectator-burden threshold

At the same event time `t_*`, the allowed cumulative spectator burden is

```text
J_R(t_*) <= (1/4) J_B(t_*).
```

- `[PROPOSED]` This is the branch's total burden threshold.
- `[INFERRED]` A candidate therefore fails if more than one quarter of the
  exact cumulative nonlinear inflow supporting the claimed event is absorbed by
  the spectator set before the event lands.

### Robustness standard

- `[PROPOSED]` A single favorable trajectory never counts.
- `[PROPOSED]` The minimum acceptable robustness standard is:
  the delayed-transfer and spectator-burden inequalities must hold either
  on an open set of reduced initial data after quotienting exact symmetries,
  or on an exact invariant family / normally hyperbolic manifold with at least
  one non-symmetry parameter.
- `[INFERRED]` Symmetry-generated copies of one tuned orbit do not satisfy this
  standard.

## Step-2 Readiness Verdict

- `[INFERRED]` Chain Step 2 is now **well-posed**.
- `[INFERRED]` Why yes:
  1. the branch now has one admissible intrinsic object:
     the exact triad-phase orbit measure on a closed support ledger;
  2. it now has one frozen search class:
     finite helical supports with mandatory conjugate completion and recursive
     exact closure;
  3. it now has explicit closure, spectator, enlargement, ordering, and
     escalation rules;
  4. it now has quantitative event, burden, and robustness metrics.

## Frozen Commitments For Step 2

- `[INFERRED]` Step 2 must enumerate finite helical support ledgers, not
  packet-role objects.
- `[INFERRED]` Step 2 must use recursive exact closure and include
  closure-forced spectators from the start.
- `[INFERRED]` Step 2 must retain the intrinsic triad-phase ledger as the
  surviving phase/coherence object; any scalar coherence score is diagnostic
  only.
- `[INFERRED]` Step 2 must apply at least one admissible enlargement test to
  every apparent survivor before drawing search conclusions.
- `[INFERRED]` Step 2 must keep all negative claims class-limited to the
  current ladder level and budget.
- `[INFERRED]` Later steps must instantiate `A / B / R` before scoring any
  trajectory and must use the frozen formulas for `J_X`, `tau_turn`, `tau_nu`,
  the `1/4` target-transfer threshold, the `1/4` spectator-burden threshold,
  and the non-single-trajectory robustness rule.

## Failed Attempts / Dead Ends

- `[VERIFIED]` The launched explorer did not finish a summary sentinel.
- `[INFERRED]` Defining delayed transfer by Tao-role itinerary times alone was
  rejected because the current mission brief requires intrinsic clocks tied to
  exact support dynamics rather than inherited packet-stage rhetoric.
