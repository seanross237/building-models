# Exploration 002 Goal — Fix And Stress-Test The Localization Protocol

## Objective

Fix one explicit localization protocol for Step 3 of the geometry route, using
the scenario choice from Exploration 001 as the primary test bed:

- primary scenario: `filament or tube concentration`
- comparator scenario: `sheet or pancake concentration`

The protocol must specify all of the following before any bounded observable
table is defined:

- intensity threshold
- spatial scale
- time window
- localization type: Eulerian, Lagrangian, or tube-adapted

The report must also explain:

- why this protocol is the right fit for the primary scenario
- why it does not quietly bake in the hoped-for conclusion
- what full-stretching-facing burden it is intended to expose
  (for example: exterior/inter-scale contribution or localization-evolution
  cost)
- and whether the protocol is stable under reasonable perturbations of
  threshold, scale, time window, or localization type

If the local repository does not support any honest explicit protocol without
arbitrary normalization, say so clearly and assess whether that should trigger
the Step-3 kill condition.

## Success Criteria

- Produces one explicit protocol, not a menu of vague options.
- Uses `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]` labels consistently.
- Distinguishes repository-supported constraints from newly proposed protocol
  choices.
- States what estimate-level burden the protocol is meant to test, not merely
  what region it isolates.
- Includes a short stability check under at least two reasonable perturbations.
- Ends with:
  - the fixed protocol
  - why it is preferred over the main alternatives
  - and the first obvious hidden-normalization risk that remains

## Failure Criteria

- Chooses a localization package that simply follows whatever tube geometry the
  hybrid hopes to preserve.
- Leaves threshold, scale, window, or localization type implicit.
- Treats a proposal as if it were already repository-verified.
- Ignores the comparator role of `sheet or pancake concentration`.
- Talks only about local core geometry while leaving the exterior/inter-scale
  or localization-evolution burden unnamed.

## Required Source Anchors

- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/GOAL.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/REASONING.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-003/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/meta/exploration-goal-design/normalize-notation-and-name-the-operative-bound-up-front.md`
- `/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library/meta/exploration-goal-design/state-nonlocal-moment-dependence-in-the-goal.md`

## Constraints

- Use local repository materials only.
- Do not define the bounded observable table yet.
- Be explicit if any part of the final protocol is only `[PROPOSED]`.
- Keep the protocol simple enough that later dynamic and stretching screens can
  actually audit it.
- Treat `tube-adapted` localization as suspect unless the report can explain
  why it is not merely installing the hoped-for coherence into the definition.

## Deliverables

Write:

1. `REPORT.md` with the localization protocol memo and stability check.
2. `REPORT-SUMMARY.md` with:
   - goal
   - what was checked
   - outcome
   - one key takeaway
   - the fixed threshold/scale/window/type package
   - two perturbation checks
   - the main reason the protocol is not secretly overfitted
   - the first residual hidden-normalization risk
