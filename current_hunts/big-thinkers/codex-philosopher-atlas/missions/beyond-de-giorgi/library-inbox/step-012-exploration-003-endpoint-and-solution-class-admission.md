# Exploration 003 Report

## Goal

Freeze the endpoint-family priority and solution-class admission burden for the
stochastic branch, then decide whether the setup already appears too
smooth-flow dependent to justify Step 2.

## Sources Consulted

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-012/GOAL.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-012/REASONING.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/refined/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/selected/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/attacks/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/judgments/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/winning-chain.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/final-decider.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/planner.md`
- [VERIFIED] `library/factual/exact-rewrite-obstruction-audit/suitable-weak-leray-hopf-with-lei-is-the-fixed-solution-class.md`
- [VERIFIED] `library/factual/framework-endpoint-freezing/only-the-inherited-suitable-weak-leray-hopf-plus-lei-floor-has-a-locally-frozen-theorem-endpoint.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-008-exploration-001-framework-endpoint-menu.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-008/explorations/exploration-001/REPORT.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-001/REPORT.md`

## Findings Log

### Initial setup

- [VERIFIED] Created report skeleton before source reading.
- [VERIFIED] The task is an admission gate, not a stochastic literature survey.
  `step-012/GOAL.md` and `CHAIN.md` both treat Step 1 as a kill-or-admit stage
  before exact stochastic identity expansion.

### Endpoint-family priority

- [VERIFIED] The branch-wide default is already frozen on disk:
  `local concentration exclusion first`, with continuation allowed only if the
  observable already behaves like `near-coercive norm control`.
  Support:
  `step-012/GOAL.md`, `CHAIN.md`, `run-008/refined/chain-03.md`,
  `run-008/winning-chain.md`.
- [VERIFIED] The run-008 critique strengthens that default rather than opening
  a parallel continuation route.
  `run-008/attacks/chain-03.md` says continuation criteria, local concentration
  exclusion, and generic contradiction lines are not equally reachable;
  continuation usually needs a coercive norm-level quantity, while local
  concentration exclusion is more local and may fit stochastic transport
  better.
- [VERIFIED] The judgment then freezes the repair rule:
  treat local concentration exclusion as the natural first endpoint and allow
  continuation only if the observable is already close to norm-level control.
  Support:
  `run-008/judgments/chain-03.md`.
- [INFERRED] No local source shows that the current stochastic observable menu
  has already crossed the near-coercive threshold required for a continuation
  endpoint. So there is no honest basis on disk to deviate from the default.

### Frozen solution-class floor

- [VERIFIED] The broader mission still freezes exactly one theorem-facing
  solution-class floor:
  suitable weak solutions in the Leray-Hopf energy class with the local energy
  inequality.
  Support:
  `suitable-weak-leray-hopf-with-lei-is-the-fixed-solution-class.md`,
  `only-the-inherited-suitable-weak-leray-hopf-plus-lei-floor-has-a-locally-frozen-theorem-endpoint.md`,
  `step-008-exploration-001-framework-endpoint-menu.md`,
  `steps/step-008/explorations/exploration-001/REPORT.md`.
- [VERIFIED] On that frozen floor, the only locally supported theorem endpoint
  is the CKN/Lin epsilon-regularity contradiction package, i.e. endpoint
  regularity exclusion on the LEI floor.
  Support:
  `only-the-inherited-suitable-weak-leray-hopf-plus-lei-floor-has-a-locally-frozen-theorem-endpoint.md`,
  `steps/step-009/explorations/exploration-001/REPORT.md`.
- [VERIFIED] Step-008 explicitly rejects unsupported framework drift and rejects
  mixed-bridge claims that are not backed by an explicit architecture package.
  Support:
  `step-008-exploration-001-framework-endpoint-menu.md`,
  `steps/step-008/explorations/exploration-001/REPORT.md`.
- [INFERRED] The stochastic branch sits above, not inside, that floor.
  Reason:
  the live stochastic menu is framed in terms of stochastic circulation,
  stochastic Cauchy / backward-flow transport, and martingale observables,
  while the winning chain repeatedly says these objects must be screened for
  dependence on smooth stochastic flows, strong filtrations, stopping times,
  and extra regularity before they can count as usable near a singular regime.
  Support:
  `run-008/selected/chain-03.md`,
  `run-008/refined/chain-03.md`,
  `run-008/winning-chain.md`,
  `step-012/REASONING.md`.
- [INFERRED] No positive admissibility bridge from the inherited
  suitable-weak / Leray-Hopf plus LEI floor to those stochastic-flow objects is
  frozen on disk. The repository has a general anti-bridge discipline from
  Step-008, but no theorem packet that puts backward stochastic flow or
  martingale observables inside the inherited weak-solution architecture.

### Filtration, stopping, localization, and smooth-flow burdens

- [VERIFIED] The active chain requires these risks to be charged immediately,
  not deferred:
  smooth stochastic flows, strong filtrations, stopping times, regularity
  assumptions, cutoff/local martingale/commutator/pressure/reconstruction
  machinery, and localization collapse.
  Support:
  `CHAIN.md`,
  `run-008/refined/chain-03.md`,
  `run-008/winning-chain.md`.
- [VERIFIED] The earlier selected version already required optional stopping,
  localization, and regularity debt to be paid as soon as an endpoint-facing
  probabilistic line is attempted.
  Support:
  `run-008/selected/chain-03.md`.
- [VERIFIED] The attack says this burden is not cosmetic cleanup.
  It argues that a stronger framework may simply smuggle the deterministic hard
  part back in, and that solution-class mismatch is broader than formal
  existence of the stochastic representation because the representation may
  depend on smooth flows, strong filtration structure, or localization regimes
  that become unusable near singularity formation.
  Support:
  `run-008/attacks/chain-03.md`.
- [VERIFIED] The judgment accepts that critique and keeps the branch live only
  as a tightly screened audit whose positive route survives only if a candidate
  observable earns coercive, localizable, endpoint-relevant control before Tao
  comparison and before framework imports.
  Support:
  `run-008/judgments/chain-03.md`.
- [VERIFIED] The planner describes the stochastic branch as the
  highest-novelty route with the most solution-class risk.
  Support:
  `run-008/planner.md`.

### Failed support searches and dead ends

- [VERIFIED] Searching repository file names under `library/` and
  `missions/beyond-de-giorgi/` for `stochastic`, `martingale`, `circulation`,
  `backward-flow`, `back-to-label`, or `Constantin-Iyer` returned no dedicated
  factual-library file names. The support packet is planning-heavy rather than
  theorem-packet-heavy.
- [VERIFIED] The only explicit `Constantin-Iyer` naming I found is in planning
  or task scaffolding materials, not in a dedicated factual memo or frozen
  admissibility bridge.
- [VERIFIED] Adjacent Step-012 explorations `001` and `002` remain unfinished
  on disk, so this report cannot inherit a pre-frozen stochastic family or a
  completed comparator packet from them.

## Required Questions

### 1. Which endpoint family is the correct first priority?

- [VERIFIED] `local concentration exclusion` is the correct first priority.
- [VERIFIED] The default is stated directly in `step-012/GOAL.md`,
  `CHAIN.md`, `run-008/refined/chain-03.md`, and `run-008/winning-chain.md`.
- [VERIFIED] `run-008/attacks/chain-03.md` and
  `run-008/judgments/chain-03.md` both sharpen the same point:
  continuation is a stronger and more coercive target, and it should not be
  prioritized unless the observable already acts like norm-level control.
- [INFERRED] Another contradiction line is not equally live on the present
  record because the branch has not yet produced a concrete observable with
  stronger endpoint-facing content than local concentration exclusion.

### 2. What solution-class floor is frozen, and where does the stochastic branch sit relative to it?

- [VERIFIED] Frozen floor:
  suitable weak solutions in the Leray-Hopf energy class with LEI.
- [VERIFIED] Frozen theorem-facing cash-out on that floor:
  CKN/Lin epsilon-regularity contradiction / endpoint exclusion.
- [INFERRED] Relative position of the stochastic branch:
  above the frozen floor, not admitted inside it.
- [INFERRED] Reason:
  the stochastic branch is organized around stochastic transport, backward
  flow, and martingale observables whose own chain packet insists on screening
  dependence on smooth stochastic flows, strong filtrations, stopping times,
  and extra regularity before any endpoint claim is allowed.
- [INFERRED] No explicit bridge is frozen from the inherited weak-solution
  floor to these stochastic objects.

### 3. What do local sources say about strong filtrations, optional stopping, localization, and smooth stochastic-flow dependence as setup risks?

- [VERIFIED] They are first-order risks and kill conditions, not later cleanup.
- [VERIFIED] The winning chain says to charge dependence on smooth stochastic
  flows, strong filtrations, stopping times, and regularity assumptions
  immediately.
- [VERIFIED] The selected chain says to charge optional stopping,
  localization, and regularity debt immediately when writing the first
  endpoint-facing probabilistic line.
- [VERIFIED] The winning chain also elevates cutoff, local martingale,
  commutator, pressure, and reconstruction machinery to the same debt ledger.
- [VERIFIED] The attack warns that a route can be formally exact yet unusable
  near singularity because the needed localization/stopping framework and flow
  regularity already presuppose what the branch is trying to protect.

### 4. Does the branch already look too dependent on stronger structure than the inherited suitable-weak / Leray-Hopf plus LEI floor?

- [VERIFIED] The repository itself treats that as a live kill condition.
  Support:
  `step-012/GOAL.md`,
  `CHAIN.md`,
  `run-008/winning-chain.md`.
- [INFERRED] Yes, the branch already looks too dependent on stronger setup than
  the inherited floor if judged honestly at Step 1.
- [INFERRED] Basis for that verdict:
  the frozen mission floor is weak-solution-plus-LEI,
  the stochastic branch's usable objects are only described through planning
  menus and setup warnings,
  and the branch has not supplied a theorem-level bridge from that weak floor
  to the stochastic-flow / filtration / stopping machinery it expects to use.

### 5. Should Step 12 classify the branch as ready for exact-identity expansion or already obstructed?

- [INFERRED] Step 12 should classify the branch as already obstructed.
- [INFERRED] More precisely:
  the correct label is `solution-class setup obstruction, branch should stop
  before exact-identity expansion`.
- [INFERRED] Reason:
  the endpoint priority is frozen honestly as local concentration exclusion,
  but the solution-class admission burden is not cleared. The record shows a
  weak-solution floor on one side and planning-level stochastic-flow objects on
  the other, with no explicit admissibility bridge and with strong
  filtration/stopping/localization dependence already flagged as primary
  fatality checks.

## Admission Table

| item | frozen choice | status | support | main burden |
| --- | --- | --- | --- | --- |
| endpoint-family priority | `local concentration exclusion` first; continuation only after near-coercive norm-level behavior | `[VERIFIED]` | `step-012/GOAL.md`; `CHAIN.md`; `run-008/refined/chain-03.md`; `run-008/judgments/chain-03.md`; `run-008/winning-chain.md` | no on-disk observable has earned the coercive threshold needed to switch to continuation |
| solution-class floor | suitable weak / Leray-Hopf with LEI; CKN/Lin endpoint-exclusion package is the only frozen theorem-facing cash-out | `[VERIFIED]` | `suitable-weak-leray-hopf-with-lei-is-the-fixed-solution-class.md`; `only-the-inherited-suitable-weak-leray-hopf-plus-lei-floor-has-a-locally-frozen-theorem-endpoint.md`; Step-008 report | stochastic-flow observables are not admitted inside this floor by any explicit bridge |
| stochastic-branch placement relative to floor | branch sits above the frozen floor rather than inside it | `[INFERRED]` | `run-008/selected/chain-03.md`; `run-008/refined/chain-03.md`; `run-008/winning-chain.md`; `step-012/REASONING.md` | usable objects depend on smooth stochastic flow / filtration / stopping machinery not shown on the inherited weak-solution ledger |
| filtration / stopping / localization burden note | treat strong filtrations, optional stopping, localization, local martingale, pressure, commutator, reconstruction, and smooth-flow dependence as front-loaded fatality checks | `[VERIFIED]` | `CHAIN.md`; `run-008/selected/chain-03.md`; `run-008/attacks/chain-03.md`; `run-008/winning-chain.md` | these debts may erase any gain or reimport the deterministic hard part through a stronger framework |
| Step-1 admission verdict | `solution-class / setup obstruction already active` | `[INFERRED]` | all sources above, especially `step-012/GOAL.md`, `CHAIN.md`, `run-008/attacks/chain-03.md`, `run-008/judgments/chain-03.md`, Step-008 framework freeze materials | no explicit weak-solution-to-stochastic-object bridge; planning menu remains ahead of admissibility |

## Draft Verdict

- [VERIFIED] The endpoint-family freeze is clear:
  `local concentration exclusion` is the only honest first priority.
- [VERIFIED] The broader mission floor is still:
  suitable weak / Leray-Hopf plus LEI.
- [INFERRED] The stochastic branch has not cleared admission into that floor.
  Its setup still leans on stochastic-flow, filtration, stopping, and
  localization machinery that the local record treats as high-risk imports
  rather than as already-admitted structure.
- Explicit conclusion:
  `solution-class / setup obstruction already active`

## Source Map

### Planning-run evidence

- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/selected/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/refined/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/attacks/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/judgments/chain-03.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/winning-chain.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/final-decider.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-008/planner.md`

### Prior mission evidence

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-012/GOAL.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-012/REASONING.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-008/explorations/exploration-001/REPORT.md`
- [VERIFIED] `missions/beyond-de-giorgi/steps/step-009/explorations/exploration-001/REPORT.md`

### Local factual freezes

- [VERIFIED] `library/factual/exact-rewrite-obstruction-audit/suitable-weak-leray-hopf-with-lei-is-the-fixed-solution-class.md`
- [VERIFIED] `library/factual/framework-endpoint-freezing/only-the-inherited-suitable-weak-leray-hopf-plus-lei-floor-has-a-locally-frozen-theorem-endpoint.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-008-exploration-001-framework-endpoint-menu.md`

## Failed Attempts / Dead Ends

- [VERIFIED] I did not find a dedicated local factual-library file that develops
  stochastic Kelvin, stochastic Cauchy, backward-flow, martingale,
  back-to-label, or `Constantin-Iyer` formulas as an admitted theorem-facing
  packet.
- [VERIFIED] I did not find an on-disk bridge theorem placing those objects
  inside the inherited suitable-weak / Leray-Hopf plus LEI floor.
- [VERIFIED] I did not find a source that upgrades the endpoint priority from
  local concentration exclusion to continuation by showing near-coercive
  norm-level behavior already on the record.

