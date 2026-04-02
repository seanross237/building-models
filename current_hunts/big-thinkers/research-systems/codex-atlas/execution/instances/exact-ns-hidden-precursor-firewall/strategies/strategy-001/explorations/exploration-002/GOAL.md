<!-- explorer-type: explorer -->

# Exploration 002: Phase 1 Precursor-and-Fidelity Gate for `E_flux`

## Goal

Choose exactly one precursor observable and one earlier region for the preferred exact-NS event `E_flux` from exploration 001, or conclude sharply that every natural candidate is either a tautological restatement of the event, a closed pressure / De Giorgi / epsilon-regularity route in disguise, or too generic / fragile to support the hidden-precursor question.

This is a Phase 1 gate exploration. It is not allowed to drift into proving the firewall or surveying many observables. Its job is to decide whether one precursor-and-region pair survives as a theorem-facing object.

Create `REPORT.md` and fill it section by section as you finish each section. Do not wait to write everything at the end. Create `REPORT-SUMMARY.md` as soon as the verdict is stable.

## Decision Target

State one decision target first and organize the report around it:

```text
Either there exists one preferred precursor observable P and one earlier region R_- for the
exact-NS event E_flux such that P is dynamically tied to the delayed-transfer burst without
merely restating the event earlier in time and without collapsing into a closed route, or no
such precursor pair survives and the strategy should stop with the correct failure category.
```

## Preloaded Context

Read first:

- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-hidden-precursor-firewall/strategies/strategy-001/STRATEGY.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-hidden-precursor-firewall/MISSION.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-hidden-precursor-firewall/MISSION-VALIDATION-GUIDE.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-hidden-precursor-firewall/strategies/strategy-001/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/exact-ns-hidden-precursor-firewall/strategies/strategy-001/explorations/exploration-001/REPORT-SUMMARY.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/runtime/results/codex-atlas-exact-ns-hidden-precursor-firewall-strategy-001-receptionist-e001.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/beltrami-pressure-analytical.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/near-beltrami-pressure-perturbation.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/near-beltrami-negative-result.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/strategy-001-adversarial-synthesis.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vortex-stretching-structural-slack.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vorticity-intermittency-measures.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/missionary/strategy-001-exact-ns-no-near-closed-tao-circuit-learnings.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/require-mechanism-layer-maps.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/specify-failure-paths.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/one-task-per-exploration.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/meta/goal-design/check-faithful-support-shrinkage-before-narrowing.md`

Strategizer-side local-library read already established:

1. Lamb-vector / Beltrami-deficit geometry is the strongest non-flux physical-space candidate in the library, but it is already known to be fragile under tiny perturbations and pressure-route-adjacent.
2. Vortex-stretching / enstrophy-production quantities are available locally, but they look generic and may not be delayed-transfer-specific.
3. The local library does not appear to contain a canonical predecessor region for the preferred exact event `E_flux`; no ready-made backward-cone or predecessor-cylinder recipe is already fixed locally.
4. The biggest live Phase 1 risk is tautology: choosing a "precursor" that is really just the event quantity `Pi_ell` or `W` restated earlier in time.

Use primary sources immediately for any missing region design, exact formula, or observability convention. Prefer primary-source PDE literature over secondary summaries.

## Required Deliverables

Your `REPORT.md` and `REPORT-SUMMARY.md` must provide:

1. One preferred precursor observable and at most one backup precursor.
2. One preferred earlier region and at most one backup region.
3. For the preferred pair:
   - the exact formula,
   - the exact spacetime measurement set,
   - the smallness condition representing "no earlier warning,"
   - why the observable is dynamically tied to `E_flux`,
   - why it is not just `E_flux` restated earlier in time,
   - why it is not a disguised closed pressure / De Giorgi / epsilon-regularity quantity.
4. A fidelity ledger stating whether the pair is measured on:
   - exact NS itself,
   - or an exact-NS-derived observation formalism with no dynamical model change.
5. A direct answer to what would count as:
   - a precursor lower bound theorem,
   - a no-hidden-transfer statement,
   - a counterexample,
   - or a failure of the precursor gate.
6. An explicit gate verdict:
   - `pass`: proceed to quantitative testing,
   - `fail`: stop with the right failure category.

## Required Discipline

- Keep one preferred precursor and at most one backup. Do not return a menu.
- If you propose earlier-region flux as the precursor, explain exactly why the choice is not tautological. "Use the same event quantity earlier" is not enough.
- If you propose Duchon-Robert activity, explain why it is a precursor to `E_flux` rather than a second event definition.
- If you propose Lamb-vector / Beltrami-deficit geometry, confront the near-Beltrami negative result directly and explain why the candidate is not already killed.
- If you propose vortex-stretching / enstrophy-production, explain why it is about delayed transfer specifically rather than generic amplification.
- Do not widen the task into proving the quantitative theorem. The job here is to choose or kill the pair.
- If the local library lacks a canonical earlier region, say so and use primary sources to defend one explicit earlier region choice.

## Helpful Questions

Use these as a checklist:

1. Which candidate precursor is closest to the event while still non-tautological?
2. What earlier region is canonical enough to avoid choosing the precursor region after the fact?
3. If the precursor uses the same scale interface `ell`, what makes it a precursor rather than just an earlier event slice?
4. If the precursor changes the quantity family, what is the exact dynamical tie to the delayed-transfer burst?
5. Does any candidate secretly collapse into the closed pressure / De Giorgi branch under a new name?
6. Does any candidate secretly collapse into generic "activity gets large" language with no Tao-specific content?
7. If all candidates fail, is the right verdict definition-level failure or model-level negative?

## Output Format

Write:

1. `REPORT.md`
2. `REPORT-SUMMARY.md`

Structure `REPORT.md` as:

1. Executive verdict
2. Candidate precursor audit
3. Preferred precursor-and-region pair
4. Backup pair or rejection of alternatives
5. Fidelity ledger and tautology/closed-route screen
6. Gate analysis and pass/fail verdict

Tag substantial claims as `[VERIFIED]`, `[CHECKED]`, `[CONJECTURED]`, or `[COMPUTED]`.

## Failure Mode To Avoid

Do not answer with "some earlier activity metric should work." The report must either choose one theorem-facing precursor pair for `E_flux` or explain exactly why no such pair survives.
