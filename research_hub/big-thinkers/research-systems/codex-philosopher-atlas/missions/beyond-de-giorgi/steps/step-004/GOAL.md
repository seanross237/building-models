# Step 4 Goal: Chain Step 3 Run The Dynamic Plausibility Screen Early

## Mission Context

**Mission:** Beyond De Giorgi — What Structural Property Could Break the NS
Regularity Barrier?

**Active chain:** `Winning Chain - Calibrated Geometry Route with Explicit Tao
Discriminator and Narrow Claim Discipline`

**Why this step exists now:** `step-003` completed Chain Step 2 and kept the
geometry branch alive only in a tightly bounded form. The branch now has one
honest primary survivor, `direction coherence + tube persistence`, but only on
an explicit Step-3 package:

- primary scenario: `filament or tube concentration`
- comparator scenario: `sheet or pancake concentration`
- localization: Eulerian parabolic package on `B_r(x_*) x [t_* - r^2, t_*]`
  with threshold `|omega| >= r^{-2}`

The chain should not move into kernel-level stretching analysis until it first
asks the dynamic question: under this fixed package, what is actually
transported, approximately propagated, or rapidly lost?

## This Step Covers

This strategizer execution covers **Chain Step 3 only**:

- run the dynamic plausibility screen on the bounded candidate table inherited
  from `step-003`;
- identify, for each candidate, the best available transport identity,
  propagation heuristic, commutator burden, diffusion loss, and
  localization-evolution cost;
- rank candidates as `dynamically plausible`, `informative but dynamically
  weak`, or `static-only`;
- and decide whether any route is still honest enough to justify the later
  fixed-representation stretching analysis.

Do **not** treat this step as permission to run Chain Step 4 or Chain Step 5.
Do not choose the final Biot-Savart decomposition yet. Do not claim full
stretching control here. This step is about persistence credibility, not
kernel-level control.

## Required Deliverables

Produce all of the following inside `RESULTS.md`:

1. **Dynamic-screen memo**
   - restate the fixed Step-3 package inherited from `step-003`;
   - explain why dynamic plausibility is now the right gate before any
     stretching representation is fixed;
   - state the exact candidate set being screened:
     - primary:
       `direction coherence + tube persistence`
     - secondary comparators:
       `vorticity-direction coherence`,
       `tube coherence / persistence`
     - fragility screens only:
       `local Beltrami / alignment`,
       `Beltrami deficit + concentration`,
       `Beltrami deficit + anisotropy`

2. **Candidate-by-candidate transport table**
   - for each candidate, record:
     - the best available transport identity or propagation heuristic;
     - the main diffusion loss;
     - the main commutator or localization-evolution burden;
     - what part of the scenario/localization package it depends on most;
     - whether its Tao discriminator still looks live dynamically rather than
       only statically;
     - and the first obvious dynamic failure mode.

3. **Dynamic ranking and kill memo**
   - classify each candidate as:
     - `dynamically plausible`
     - `informative but dynamically weak`
     - `static-only`
   - say whether the primary hybrid remains worth carrying into Chain Step 4;
   - if not, recommend branch invalidation or replanning rather than allowing
     the mission to drift into representation work anyway.

4. **Step-4 readiness recommendation**
   - if a route survives, state exactly what the next step should fix when it
     chooses one primary kernel-level representation of `S omega . omega`;
   - if no route survives honestly, say that the current chain should stop and
     why.

## Exploration Tasks

Use **2-4 explorations total** unless a kill condition fires early.

### Exploration A: Dynamic screen for the primary hybrid

Tasks:
- test `direction coherence + tube persistence` against the fixed Eulerian
  package from `step-003`;
- identify the best available transport or approximate propagation story for
  coherence along a coherent intense tube family;
- record the diffusion burden, relocalization burden, and any dependence on
  hidden tube adaptation;
- decide whether the Tao discriminator remains live once persistence is stated
  dynamically rather than descriptively.

Success standard:
- the primary hybrid receives a concrete dynamic verdict rather than generic
  optimism.

### Exploration B: Comparator audit

Tasks:
- screen `vorticity-direction coherence` and `tube coherence / persistence`
  under the same package;
- determine whether either comparator is dynamically stronger, dynamically
  weaker, or merely exposes why the primary hybrid is necessary;
- check whether the comparators collapse into prior-art direction criteria or
  static tube language once propagation costs are named explicitly.

Success standard:
- the comparator audit materially sharpens the ranking rather than duplicating
  Step 3's static table.

### Exploration C: Fragility-screen audit

Only run this after A and B, or earlier if the primary route already looks
weak.

Tasks:
- confirm that Beltrami-family quantities remain fragility screens even after
  dynamic considerations are included;
- test whether any apparent persistence story depends on hidden normalization,
  stronger derivative control, or tube-adapted relocalization;
- use these screens to state the earliest honest branch-kill condition if the
  primary hybrid fails.

Success standard:
- dynamic failure modes are explicit enough that the next evaluator can decide
  branch invalidation or continuation without ambiguity.

## Kill Conditions

Trigger an early negative conclusion for this step if any of the following
happens:

- the primary hybrid `direction coherence + tube persistence` has no credible
  propagation or persistence story even heuristically under the fixed Eulerian
  package;
- the route survives only after reintroducing tube-adapted localization, tuned
  threshold or time-window choices, or stronger derivative control than the
  bounded Step-3 package contains;
- every surviving candidate is dynamically weak or static-only, so that moving
  to kernel-level stretching analysis would be blind momentum rather than an
  earned next step.

If a kill condition fires, count that as a successful obstruction result for
this step and recommend branch invalidation or replanning rather than
continuing.

## Constraints

- Do **not** reopen the exhausted harmonic-tail pressure branch except as
  established background.
- Do **not** change the scenario classes or localization protocol fixed in
  `step-003`; this step tests persistence under that package rather than
  redesigning it.
- Do **not** move into kernel-level `S omega . omega` decomposition yet.
- Do **not** treat descriptive tube language as a dynamic mechanism.
- Use source-based labels such as `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]`.

## Validation Requirements

- Name the exact source files used for each major transport or propagation
  claim.
- Keep the Tao discriminator explicit for any candidate still ranked
  `dynamically plausible`.
- Make the localization-evolution cost and hidden-normalization risks explicit,
  not implicit.
- Keep final claims bounded to the fixed Step-3 package actually inherited from
  `step-003`.
