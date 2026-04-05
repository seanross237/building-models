# Step 1 Goal: Chain Step 1 Fix the Intrinsic Object, Equivalence Test, Search Class, and Metrics

## Mission Context

**Mission:** Exact NS Phase-Locking Firewall

**Active chain:**
`Chain 01 - Intrinsic Exact Closed-Support Delayed-Transfer Stress Test`

**Why this step exists now:** this is a bootstrap step after planning run
`run-001`. Mission control selected the current chain because it keeps the
mission's highest-upside branch alive, but only after importing hard guardrails
from the losing branches. Before any support enumeration, exact dynamics
ledger, or delayed-transfer test can count, the mission must first freeze the
intrinsic object layer:
what exact phase/coherence object is even admissible,
what representation changes preserve it,
what exact support class the search is allowed to use,
and what delayed-transfer metrics later steps must satisfy.

## This Step Covers

This strategizer execution covers **Chain Step 1 only**.

You must do all of the following, and only the following:

- define one very small candidate family of exact phase/coherence objects built
  from exact Fourier or helical interaction data, with no desired-channel
  labels, packet sheets, or frozen transfer annotations in the raw definition;
- state the formal equivalence and admissibility test for those objects,
  covering exact symmetries, conjugate completion, helical-sign relabeling,
  gauge conventions, and normalization changes;
- classify each candidate with exactly one status:
  `intrinsic`,
  `canonically representable but non-intrinsic`,
  or `inadmissible`;
- choose the initial exact search objects and support class for this branch,
  defaulting to finite Fourier or helical mode supports unless a sharper
  alternative is justified;
- declare closure conventions, admissible enlargements, smallest-first
  ordering, and an explicit escalation ladder;
- define the quantitative success metrics up front:
  what counts as delayed transfer relative to turnover and viscous times,
  what spectator burden threshold is allowed during the same window,
  and what robustness standard later steps must meet;
- state whether Chain Step 2 is now well-posed and list the frozen commitments
  it must inherit.

Do **not** enumerate actual support survivors yet. That belongs to Chain Step
2. Do **not** derive full projected ODEs or compatibility equations yet. That
belongs to Chain Step 3. Do **not** drift into generic turbulence language
about phase mixing. Everything in this step must stay tied to exact
Fourier/helical interaction structure.

## Required Deliverables

Produce all of the following inside `RESULTS.md`:

1. **Intrinsic-object memo**
   - propose a very small candidate family, preferably no more than three
     candidates;
   - state the raw definition of each candidate;
   - explain why each candidate is supposed to capture delayed-transfer-facing
     phase/coherence structure rather than generic bookkeeping.

2. **Equivalence and admissibility sheet**
   - define the exact transformations under which the object must be tested:
     conjugation, phase gauge changes, sign relabeling, normalization changes,
     and representation changes forced by real-valuedness;
   - assign each candidate one of the three admissibility statuses;
   - explain the decisive reason for each status.

3. **Exact search-class memo**
   - state what the branch will count as an exact search object;
   - state the closure convention, including recursive closure and spectator
     inclusion rules;
   - state at least one admissible enlargement rule;
   - state the smallest-first ordering and escalation ladder the next step must
     follow.

4. **Quantitative metric sheet**
   - define delayed-transfer timing relative to intrinsic turnover and viscous
     clocks;
   - define the spectator-burden threshold for the same window;
   - define the robustness standard:
     single trajectory only,
     open parameter regime,
     or another explicitly justified level.

5. **Step verdict**
   - state whether Chain Step 2 is now well-posed;
   - if yes, list the exact frozen commitments Step 2 must inherit;
   - if no, state plainly that the branch should stop with a
     definition-level or methodology-failure verdict.

## Exploration Scope

Use **2-3 explorations total** unless a kill condition fires early.

Rely first on the local mission basis already named in `MISSION.md`:

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-006/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-009.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-of-averaged-ns-blowup-firewall-FINAL-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/CHAIN.md`
- `library/factual/tao-circuit-feature-ledger/INDEX.md`
- `library/factual/navier-stokes/INDEX.md`
- the current `CHAIN.md`
- the planning artifacts in `planning-runs/run-001/`

Do **not** spend this step re-running broad literature surveys or generic exact
NS screening. Start from the inherited Atlas context and move directly to the
intrinsic-object, admissibility, search-class, and metrics freeze.

## Suggested Exploration Split

### Exploration A: Candidate object and intrinsicity screen

Tasks:
- identify a very small candidate family of exact phase/coherence objects;
- test whether each candidate survives without desired-channel labels or packet
  annotation;
- decide which candidate, if any, remains alive as an intrinsic object.

Success standard:
- the branch can name at least one candidate that survives an honest
  admissibility screen, or else it earns a sharp definition-level failure.

### Exploration B: Exact search class and canonicalization discipline

Tasks:
- choose the exact search objects and support semantics for the branch;
- freeze closure conventions, admissible enlargements, and smallest-first
  ordering;
- make clear what later steps may treat as symmetry, canonicalization, or
  substantive model change.

Success standard:
- Step 2 can enumerate supports without representation cherry-picking or
  hidden pruning.

### Exploration C: Metric sheet and readiness verdict

Only run this after the object screen and search class are explicit.

Tasks:
- define delayed-transfer timing, spectator burden, and robustness thresholds;
- decide whether those metrics are sharp enough for later steps to test exact
  candidates honestly;
- issue a clean `Step 2 can start` or `branch stops here` verdict.

Success standard:
- mission control receives a concrete frozen handoff, not narrative optimism.

## Kill Conditions

Trigger an early negative conclusion for this step if any of the following
happens:

- every candidate phase/coherence object depends essentially on desired-channel
  labels, packet sheets, or other non-intrinsic annotation;
- the equivalence and admissibility statuses cannot be stated sharply enough to
  distinguish intrinsic from merely canonically encoded objects;
- the exact search class, closure rule, or admissible enlargement policy
  remains too noncanonical for later support enumeration to mean anything;
- delayed-transfer, spectator-burden, or robustness metrics can only be stated
  narratively rather than quantitatively.

If any of those occur, report the sharpest earned definition-level or
methodology-failure verdict and recommend that the branch stop before Chain
Step 2.

## Constraints

- Do **not** enumerate recursively closed support survivors yet.
- Do **not** derive full exact dynamics, compatibility equations, or transfer
  windows yet.
- Do **not** smuggle Tao's five-role template or desired subgraph labels into
  the raw object definition.
- Do **not** accept an object that is only meaningful after hand-selecting a
  hoped-for transfer direction.
- Do **not** treat polished rhetoric about phase mixing as success unless the
  object and metrics are explicit enough for later exact testing.

## Validation Requirements

- Tag each major conclusion as `[VERIFIED]`, `[INFERRED]`, or `[PROPOSED]`.
- Name the exact local source files supporting each mission-context claim.
- Make the admissibility test explicit enough that Step 2 can reject
  non-intrinsic candidates immediately.
- Make the search-class memo explicit enough that Step 2 can enumerate supports
  without inventing new closure rules on the fly.
- If the step succeeds, end with one short section called
  `Frozen commitments for Chain Step 2`.
- If the step fails, end with one short section called
  `Why the branch stops at intrinsic object definition`.
