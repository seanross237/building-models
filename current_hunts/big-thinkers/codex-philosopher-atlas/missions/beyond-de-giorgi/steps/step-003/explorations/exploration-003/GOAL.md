# Exploration 003 Goal — Define The Bounded Observable Table

## Objective

Using the fixed Step-3 package from Explorations 001 and 002:

- primary scenario: `filament or tube concentration`
- comparator scenario: `sheet or pancake concentration`
- localization protocol:
  - threshold: `|omega| >= r^{-2}`
  - scale: one dyadic ball `B_r(x_*)`
  - time window: `[t_* - r^2, t_*]`
  - type: `Eulerian`

define the bounded observable table for Step 3 and rank which candidates remain
honest inputs for the later dynamic plausibility screen.

The table must include exactly these items:

- primary candidate: `direction coherence + tube persistence`
- secondary comparators:
  - `vorticity-direction coherence`
  - `tube coherence / persistence`
- fragility screens only:
  - `local Beltrami / alignment`
  - `Beltrami deficit + concentration`
  - `Beltrami deficit + anisotropy`

For each item, record:

- scaling or normalization status
- what localization data it depends on
- what scenario it is meant to address
- its intended leverage point on the future full-stretching target
- its Tao discriminator
- and its first obvious instability or hidden-normalization risk

The report must end with a Step-3 readiness recommendation:

- which candidates remain primary
- which are secondary
- which are effectively dead
- and whether the branch should advance to the dynamic plausibility screen

If the primary hybrid collapses under this honest formulation, say so directly
and recommend invalidation or replanning rather than drift.

## Success Criteria

- Produces one bounded table, not open-ended brainstorming.
- Uses `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]` labels consistently.
- Keeps primary, comparator, and fragility-screen roles distinct.
- States a Tao discriminator for every candidate still treated as primary or
  secondary.
- Makes explicit when a candidate depends on the fixed Eulerian localization
  package rather than on a new hidden normalization choice.
- Ends with a decisive readiness recommendation for the next chain step.

## Failure Criteria

- Re-promotes Beltrami/alignment to primary status.
- Lets a candidate inherit a more favorable scenario or localization than the
  fixed Step-3 package.
- Uses vague geometry prose instead of a bounded table.
- Keeps a candidate alive without naming a full-stretching-facing leverage
  point.
- Avoids saying when a candidate is effectively dead.

## Required Source Anchors

- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/GOAL.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/REASONING.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/explorations/exploration-002/REPORT.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/direction-coherence-plus-tube-persistence-is-the-primary-step-2-survivor.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/standalone-beltrami-alignment-collapses-to-a-fragility-screen.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`

## Constraints

- Use local repository materials only.
- Do not move into the full dynamic plausibility screen itself.
- Do not fix a new kernel-level representation beyond the schematic leverage
  points already allowed by the local record.
- Keep the table bounded to the fixed Step-3 package above.

## Deliverables

Write:

1. `REPORT.md` with the bounded observable table and ranking.
2. `REPORT-SUMMARY.md` with:
   - goal
   - what was checked
   - outcome
   - one key takeaway
   - a compact candidate ranking
   - whether the branch should advance to the dynamic plausibility screen
