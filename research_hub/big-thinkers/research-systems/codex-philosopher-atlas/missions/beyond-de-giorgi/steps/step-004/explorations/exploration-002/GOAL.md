# Exploration 002 Goal — Comparator Dynamic Audit

## Objective

Run the dynamic plausibility screen on the Step-3 comparators:

- `vorticity-direction coherence`
- `tube coherence / persistence`

using the same fixed Step-3 package:

- primary scenario: `filament or tube concentration`
- comparator scenario: `sheet or pancake concentration`
- localization: Eulerian parabolic package on
  `B_r(x_*) x [t_* - r^2, t_*]`
- threshold: `|omega| >= r^{-2}`

This exploration must determine whether either comparator is dynamically
stronger than the primary hybrid, dynamically weaker, or useful only because it
reveals why the primary hybrid needs both pieces.

For each comparator, the report must record:

- the best available transport identity or propagation heuristic;
- the main diffusion loss;
- the main localization-evolution or commutator burden;
- what part of the fixed package it depends on most;
- whether its Tao discriminator remains live dynamically;
- and the first obvious failure mode.

The report should also say whether the comparator collapses into prior-art
direction criteria, static tube language, or hidden derivative control once the
dynamic burden is named explicitly.

## Success Criteria

- Produces a source-based comparator memo that sharpens the ranking.
- Uses `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]` labels consistently.
- Names exact source files for every major transport, diffusion, and burden
  claim.
- Distinguishes clearly between the direction-only and tube-only routes.
- Ends with:
  - a verdict for each comparator:
    `dynamically plausible`, `informative but dynamically weak`, or
    `static-only`
  - whether either comparator outperforms the primary hybrid
  - and what each comparator exposes about the hybrid's necessity or weakness

## Failure Criteria

- Treats prior-art direction coherence as automatically live without naming a
  new localized persistence bridge.
- Treats one-time tube concentration as persistence.
- Imports hidden `nabla xi` control or tube-adapted relocalization without
  naming them as new assumptions.
- Reaches only descriptive comparisons rather than dynamic ones.

## Required Source Anchors

- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-004/GOAL.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-004/REASONING.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/runtime/results/codex-patlas-standalone-20260331T113910Z-receptionist-79670.md`

## Constraints

- Use local repository materials only.
- Do not promote either comparator beyond what the fixed Step-3 package earns.
- If you use a standard Navier-Stokes identity not explicit in the local
  repository, mark it `[INFERRED]` and keep the mission-level conclusion tied
  to the local record.
- Do not move into kernel-level stretching decomposition.

## Deliverables

Write:

1. `REPORT.md` with the comparator dynamic audit.
2. `REPORT-SUMMARY.md` with:
   - goal
   - what was checked
   - outcome
   - one key takeaway
   - best transport / propagation story for each comparator
   - main diffusion loss for each comparator
   - main localization-evolution or commutator burden for each comparator
   - Tao discriminator status for each comparator
   - first obvious failure mode for each comparator
   - final rating for each comparator
