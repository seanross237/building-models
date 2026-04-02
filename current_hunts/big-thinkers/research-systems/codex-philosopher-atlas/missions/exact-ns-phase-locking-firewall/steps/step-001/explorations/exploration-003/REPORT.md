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
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-001.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/mission-context.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT-SUMMARY.md`
- `library/factual/tao-circuit-feature-ledger/INDEX.md`
- `library/factual/tao-circuit-feature-ledger/admissible-leakage-must-be-declared-but-is-a-branch-level-policy-choice.md`
- `library/factual/tao-circuit-feature-ledger/delayed-threshold-trigger-logic-is-load-bearing.md`
- `library/factual/tao-circuit-feature-ledger/summable-time-scale-separation-is-essential-to-tao-likeness.md`
- `library/factual/tao-circuit-feature-ledger/tao-likeness-requires-a-five-part-canonicalization-screen.md`
- `library/factual/tao-circuit-feature-ledger/amplitude-hierarchy-is-load-bearing-even-when-literal-coefficients-are-not.md`
- `library/meta/obstruction-screening/robustness-audits-may-keep-several-honest-survivors-with-different-statuses.md`

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

### Recovered Freeze Inputs

- `[VERIFIED]` Exploration 001 already freezes the surviving intrinsic object
  as the coefficient-corrected exact triad-phase orbit measure
  `Mu_S(a)`,
  with scalar coherence summaries demoted to later diagnostics and any raw
  desired-vs-spectator split ruled inadmissible.
- `[VERIFIED]` Exploration 002 already freezes the Step-2 search class as
  finite helical support ledgers with mandatory conjugate completion,
  recursive exact closure, closure-time spectator inclusion, admissible
  enlargements, a smallest-first ordering, and an escalation ladder.
- `[VERIFIED]` The chain, attack packet, and judgment memo all require delayed
  transfer, spectator burden, and robustness to be explicit enough to reject
  rhetoric, threshold drift, and single-trajectory luck.
- `[VERIFIED]` The Tao-feature ledger says leakage control is required but the
  exact leakage functional is a branch-level policy choice, so this report must
  freeze one explicit support-level burden rule rather than inherit a packet
  rule verbatim.

Assume later steps have frozen, for one candidate closed support:

- one recursively closed exact support `S`;
- one predeclared source subset `A subset S`;
- one predeclared target subset `B subset S`;
- one spectator subset `R := S \\ (A union B)`;
- one support-respecting trajectory or trajectory family on the closed support.

The partition `A / B / R` must be declared **before** any trajectory is scored.
Later steps are not allowed to relabel the partition after seeing outcomes, and
the same partition must be held fixed across any later robustness family.

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

Define the cumulative turnover count by

```text
N_turn(t) := int_0^t Q_S(s) / E_S(s) ds,
E_S(t) := sum_{m in S} |a_m(t)|^2.
```

Define the fastest viscous clock on the support by

```text
tau_nu(S) := 1 / (nu max_{m in S} |k_m|^2).
```

- `[INFERRED]` `N_turn(t)` measures how many support-turnover units have
  elapsed by time `t`. This is sharper than using one instantaneous turnover
  value because it counts the actual accumulated nonlinear time before the
  event.
- `[INFERRED]` `tau_nu` uses the fastest-decaying active mode, so it is the
  strictest viscous deadline available on the support.

### Delayed-transfer event

Let `t_*` be the first time such that

```text
J_B(t_*) >= (1/4) E_A(0),
-J_A(t_*) >= (1/4) E_A(0).
```

The branch counts this as a delayed-transfer event only if all of the
following also hold:

```text
t_* <= (1/4) tau_nu(S),
N_turn(t_*) >= 3,
J_B(t) <= (1/16) E_A(0) for every t with N_turn(t) <= 2.
```

- `[PROPOSED]` Size choice:
  the simultaneous `1/4` target-gain and source-loss thresholds force a
  material transfer event rather than a tiny favorable blip or a target gain
  fed mainly from elsewhere.
- `[PROPOSED]` Turnover choice:
  `N_turn(t_*) >= 3` means at least three full support-turnover units have
  elapsed before the event lands, while the `1/16` dormancy cap up to
  `N_turn = 2` prevents ordinary early leakage from being rebranded as
  "delayed."
- `[PROPOSED]` Viscous choice:
  `t_* <= tau_nu / 4` requires the event to land while the full support still
  sits comfortably inside its own fastest viscous lifetime.

### Spectator-burden threshold

Define the positive-part spectator burden by

```text
J_R^+(t) := max(J_R(t), 0),
B_spec(t_*) := sup_{0 <= s <= t_*} J_R^+(s) / J_B(t_*).
```

The branch allows a candidate only if

```text
B_spec(t_*) <= 1/4.
```

- `[PROPOSED]` This is the branch's support-level spectator threshold.
- `[INFERRED]` Taking the positive part and the running supremum prevents
  cancellation tricks from hiding a large transient spectator load.
- `[INFERRED]` A candidate therefore fails if, at any time before the claimed
  event lands, the exact cumulative nonlinear inflow into the spectator set
  exceeds one quarter of the event-sized target inflow.

### Robustness standard

- `[PROPOSED]` A single favorable trajectory never counts.
- `[PROPOSED]` The minimum acceptable robustness level for this branch is an
  **open parameter regime on one fixed closed support ledger and one fixed
  `A / B / R` partition after quotienting exact symmetries and frozen
  canonicalization choices**.
- `[PROPOSED]` Concretely:
  there must exist at least one nonempty open set of reduced initial data and
  at least one non-symmetry free parameter or geometric parameter on which the
  delayed-transfer, viscous, and spectator inequalities all hold with the same
  thresholds.
- `[INFERRED]` An exact invariant family or a normally hyperbolic manifold with
  an open basin counts as stronger evidence and automatically passes this bar.
- `[INFERRED]` A symmetry-generated orbit copy, one isolated tuned trajectory,
  or a success that requires retuning `A / B / R` across cases does not.

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
- `[INFERRED]` No methodology failure remains at Step 1 because the only
  policy-level freedom left by the local record was the precise finite-window
  burden rule, and this report freezes that freedom rather than leaving it
  narrative.

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
- `[INFERRED]` Step 2 must record enough exact ledger data for later scoring:
  the closed support itself, its active triad-orbit list, its closure-forced
  spectator list, its helical sign sectors, and the exact coefficient support
  needed to build `Q_S`.
- `[INFERRED]` Later steps must instantiate `A / B / R` before scoring any
  trajectory and must use the frozen formulas for `J_X`, `Q_S`, `N_turn`,
  `tau_nu`, the `1/16` dormancy cap, the paired `1/4` transfer thresholds,
  the `1/4` spectator-burden threshold, and the open-regime robustness rule.

## Failed Attempts / Dead Ends

- `[VERIFIED]` The launched explorer did not finish a summary sentinel.
- `[INFERRED]` Defining delayed transfer by Tao-role itinerary times alone was
  rejected because the current mission brief requires intrinsic clocks tied to
  exact support dynamics rather than inherited packet-stage rhetoric.
- `[INFERRED]` Porting the predecessor mission's packet-class leakage vector
  directly was also rejected: the old `mirror / companion / feedback / cross`
  split is honest on the frozen packet ledger, but this branch needs one
  support-level spectator metric that is intrinsic to closed helical supports
  rather than to packet-role classes.
