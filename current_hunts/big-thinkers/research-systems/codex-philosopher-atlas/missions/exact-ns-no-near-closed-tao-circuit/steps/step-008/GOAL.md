# Step 8 Goal: Chain Step 2 Derive Honest Exact Closure Before Any Reduction

## Mission Context

**Mission:** Exact NS No-Near-Closed Tao Circuit

**Active chain:**
`Chain - Exact Stress Test Of F_SS(1/12)`

**Why this step exists now:** `step-007` succeeded at the branch's first gate.
It froze the single witness `F_SS(1/12)`, the authoritative repaired Step-6
`G_tmpl` / `G_leak` scorecard, the same-currency protocol, and the no-repair /
no-overclaim guardrail. Mission control therefore keeps the current chain
active. The next unresolved bottleneck is no longer witness identity or
threshold authority. It is whether honest exact bookkeeping for this frozen
witness closes finitely on the same ledger or immediately exits the audited
one-bridge class.

## This Step Covers

This strategizer execution covers **Chain Step 2 only**.

You must do all of the following, and only the following:

- compute all exact modes and interactions forced by the frozen witness
  `F_SS(1/12)` on the same canonical ledger, including mandatory conjugates
  and any closure-forced companions;
- separate what is already part of the Step-7 frozen witness sheet from what
  first appears only because exact closure forces it;
- determine whether honest closure stays inside the audited one-bridge class
  with one finite exact closed system, or whether exact bookkeeping instead
  forces class exit, arbitrary truncation, or uncontrolled packet growth;
- if a finite honest closed system exists, state it explicitly enough that
  Chain Step 3 can inherit it unchanged;
- if no finite honest closed system exists, package the earliest decisive
  constructive failure or non-isolability memo on the exact ledger;
- preserve the Step-7 same-currency rule and no-repair guardrail throughout.

Do **not** integrate or analyze exact dynamics yet. That belongs to Chain Step
3. Do **not** evaluate dynamic pass/fail against `G_tmpl` or `G_leak` yet. Do
**not** broaden the branch from `F_SS(1/12)` to `F_SS(mu)`, to `F_SL`, or to
the whole one-bridge class. Do **not** rescue any closure defect by adding
optional bridges, shell-locked modes, post hoc companions, new packet
semantics, or alternate bookkeeping currency.

## Frozen Commitments You Must Inherit

All Step-8 work must inherit the Step-7 freezes:

- the single carried witness is `F_SS(1/12)`, not the family `F_SS(mu)`;
- the packet object remains the canonical one-bridge role-labeled helical
  packet
  `P_n = (A_n, B_n, C_n, D_n, E_n)`;
- the shared desired interaction core remains
  `A -> B`,
  `A -> C`,
  `B,C -> C`,
  `C,A <-> D`,
  `D,D -> E`,
  with spectator classes
  `mirror`,
  `companion`,
  `feedback`,
  `cross`;
- mandatory conjugate completion, one role order, one helical basis choice,
  one sign sheet, one amplitude anchor, and one phase anchor remain frozen;
- the normalization remains
  `|A_n(0)| = 1`,
  `arg A_n(0) = 0`,
  `I = [0, 1]`,
  `int_I D_on(t) dt = 1`;
- repaired `G_tmpl` and repaired `G_leak` remain the only hard pass/fail gates
  for later stages;
- the same-currency rule keeps the same `D_on` / `D_off` split and the same
  spectator partition;
- itinerary timing and stage-order language remain diagnostics only; and
- closure-forced bookkeeping is allowed only if it leaves witness identity,
  packet semantics, window, packet-sheet conventions, and repaired Step-6
  gate sheets unchanged.

No Step-8 argument may change packet semantics, sign / phase / amplitude
bookkeeping, spectator partition, window, or scorecard in order to improve the
closure story. If honest closure leaves the audited one-bridge class, that is a
branch result, not a license to enlarge the witness.

## Required Deliverables

Produce all of the following inside `RESULTS.md`:

1. **Exact closure ledger**
   - list all exact modes and interaction terms forced by the frozen witness
     and mandatory conjugates on the same ledger;
   - separate pre-frozen witness content from genuinely closure-forced
     additions;
   - state whether closure stabilizes after finitely many forced additions or
     shows uncontrolled growth.

2. **Class-retention verdict**
   - state whether honest closure stays inside the audited one-bridge class;
   - if not, name the first decisive failure mode:
     class exit,
     arbitrary truncation requirement,
     uncontrolled packet growth,
     or another equally sharp exact-bookkeeping obstruction earned on the same
     ledger;
   - if yes, state the exact finite closed subsystem and the state variables it
     contains.

3. **Exact interaction sheet for later dynamics**
   - if a finite honest closed system exists, write the exact interaction table
     or equivalent ODE-ready bookkeeping for that system;
   - identify which couplings belong to the desired core, which belong to the
     spectator classes, and which appear only as closure-forced bookkeeping;
   - record any exact zero couplings, symmetry reductions, or sign constraints
     that later dynamics must inherit.

4. **No-rescue audit**
   - verify that no added mode or term was introduced as discretionary repair;
   - verify that the same-currency rule, packet semantics, and repaired
     scorecard remain unchanged;
   - state the strongest claim the branch is allowed to support after this step
     and what it is still not allowed to claim.

5. **Step verdict**
   - state whether Chain Step 3 is now well posed;
   - if yes, list the exact closed system and frozen commitments Chain Step 3
     must inherit;
   - if no, state plainly that the branch should stop at exact closure and name
     the sharpest earned constructive verdict.

## Exploration Scope

Use **2-3 explorations total** unless a kill condition fires early.

The work should rely first on the local Step-7 freeze and the branch sources it
already cites:

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-007/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-005/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN-HISTORY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-010.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/final-decider.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/winning-chain.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-002/judgments/chain-03.md`

Use older Step-1 through Step-3 material only as needed to anchor the exact
packet sheet, sign conventions, or witness-local ledger already frozen by Step
7.

Do **not** reopen broad mission planning. Do **not** run the dynamic stress
test. Do **not** launch a new witness search or packet-family comparison.

## Suggested Exploration Split

### Exploration A: Derive the raw exact closure ledger

Tasks:
- enumerate the exact modes and interactions forced by
  `F_SS(1/12)`
  on the frozen canonical ledger;
- include mandatory conjugates and distinguish closure-forced companions from
  already frozen witness content;
- identify where the closure process stabilizes or first shows unbounded
  growth.

Success standard:
- the exact closure burden is explicit and there is no hidden bookkeeping.

### Exploration B: Decide class retention and finiteness

Tasks:
- determine whether the closure ledger stays inside the audited one-bridge
  class and yields one finite exact closed subsystem;
- if it fails, locate the earliest decisive obstruction and write it as a
  constructive non-isolability memo;
- if it succeeds, identify the exact state variables and interactions that
  Chain Step 3 must inherit.

Success standard:
- mission control receives either one finite exact closed system or one sharp
  closure-stage failure atlas.

### Exploration C: Write the Step-8 handoff or stop memo

Only run this after the first two explorations settle the closure ledger.

Tasks:
- assemble the exact interaction sheet for later dynamics if the system closes;
- write the no-rescue audit and the no-overclaim boundary;
- decide whether Chain Step 3 can start or whether the branch stops at exact
  closure.

Success standard:
- mission control receives a clean
  `Step 3 can start`
  or
  `branch stops at exact closure`
  verdict.

## Kill Conditions

Trigger an early negative conclusion for this step if any of the following
happens:

- honest closure requires class-changing additions, arbitrary truncation, or
  uncontrolled packet growth;
- any apparent finite system omits forced conjugates, companions, or exact
  interaction terms that the same ledger requires;
- closure can be described only by changing packet semantics, spectator
  partition, sign / phase sheet, window, or bookkeeping currency;
- the exact closure picture remains too implicit to support a later dynamic
  audit on the same frozen ledger.

If any of those occur, report the sharpest earned constructive verdict and
recommend that the branch stop before Chain Step 3.

## Constraints

- Do **not** run exact dynamics or finite-window integration in this step.
- Do **not** evaluate dynamic pass/fail against repaired `G_tmpl` or repaired
  `G_leak` yet.
- Do **not** broaden the branch from `F_SS(1/12)` to the wider family or a new
  packet class.
- Do **not** retune thresholds, spectator classes, the `D_on` / `D_off` split,
  or the fixed window.
- Do **not** rescue class exit with optional bridges, shell-locked modes, post
  hoc companions, or rephasing.
- Do **not** package Step-4 dossier friendliness as proof of exact closure.

## Validation Requirements

- Tag each major conclusion as `[VERIFIED]`, `[INFERRED]`, or `[PROPOSED]`.
- Cite the exact local files supporting the Step-7 freeze and the Step-8
  closure bookkeeping.
- Make the final closure verdict explicit enough that Chain Step 3 can either
  start immediately or be cancelled immediately.
- If the step succeeds, end with one short section called
  `Frozen exact system for Chain Step 3`.
- If the step fails, end with one short section called
  `Why the branch stops at exact closure`.
