# Exploration 002 Report - Comparator Dynamic Audit

## Goal

Audit the Step-3 comparators `vorticity-direction coherence` and
`tube coherence / persistence` against the fixed Step-3 package:

- primary scenario: `filament or tube concentration`
- comparator scenario: `sheet or pancake concentration`
- localization: Eulerian parabolic package on
  `B_r(x_*) x [t_* - r^2, t_*]`
- threshold: `|omega| >= r^{-2}`

Required outputs:

- best available transport identity or propagation heuristic
- main diffusion loss
- main localization-evolution or commutator burden
- dependence on the fixed package
- Tao discriminator status
- first obvious failure mode
- final dynamic rating for each comparator

## Method

- Read the required Step-2, Step-3, Step-4, chain, and library source anchors.
- Extract the strongest repository-backed dynamic story available for each
  comparator.
- Use standard Navier-Stokes identities only as `[INFERRED]` schematic
  scaffolding where the local corpus does not state the formula explicitly.
- Keep the mission-level conclusions tied to the local screening record rather
  than to any imported theorem.

## Running Notes

### Initial scaffold

- [VERIFIED] Report skeleton created before analysis.

### Operational note

- [VERIFIED] The launched explorer produced an initial draft but did not finish
  the audit. The final report below completes the task directly from the
  anchored local materials.

## Findings

### 1. Fixed package inherited from Step 3

- [VERIFIED] The audit is constrained to the Step-3 package that left only one
  honest primary survivor:
  `direction coherence + tube persistence`, with the comparators
  `vorticity-direction coherence` and `tube coherence / persistence`.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] The package is fixed to the neutral Eulerian parabolic audit
  region
  `Q_r(x_*, t_*) = B_r(x_*) x [t_* - r^2, t_*]`
  with intense set
  `E_r(t) = {x in B_r(x_*) : |omega(x,t)| >= r^{-2}}`.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-002/REPORT.md`
  - `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`
  - `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
- [VERIFIED] The branch-wide screen remains estimate-level: a comparator only
  stays live if it points toward a smaller full-stretching contribution, not
  just cleaner geometry. Before Step 4 fixes one representation, the admissible
  targets are a smaller local/self-induced stretching piece, a smaller
  exterior/nonlocal stretching piece, or a smaller
  localization/inter-scale interaction term.
  Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`

### 2. Formula sheet used for the dynamic audit

- [VERIFIED] The local repository requires each candidate to have a best
  transport identity or propagation heuristic, a diffusion loss, and a
  localization-evolution burden, but the required local sources do not give a
  formula-level evolution law for either comparator.
  Sources:
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
  - `runtime/results/codex-patlas-standalone-20260331T113910Z-receptionist-79670.md`
- [INFERRED] Standard vorticity identity used as schematic scaffolding:
  `(\partial_t + u . \nabla - \Delta)\omega = S\omega`.
  This is not explicit in the local corpus, so the formula is used only to
  instantiate the dynamic-screen slots the repository asks for.
- [INFERRED] Standard amplitude identity on `{omega != 0}`:
  `(\partial_t + u . \nabla - \Delta)|omega|
   = (\xi . S\xi)|omega| - |omega||\nabla\xi|^2`,
  where `\xi = omega / |omega|`.
  This is the cleanest available propagation heuristic for anything defined by
  the thresholded intense set `|omega| >= r^{-2}`.
- [INFERRED] Standard schematic direction evolution on `{omega != 0}`:
  `(\partial_t + u . \nabla - \Delta)\xi`
  equals a projected stretching term plus diffusion-generated gradient terms
  involving `\nabla log|omega|` and `\nabla\xi`.
  The exact lower-order form is not needed here; the key point is that
  direction is not passively transported once diffusion is present.

### 3. Comparator audit table

| Comparator | Best transport identity or propagation heuristic | Main diffusion loss | Main localization-evolution or commutator burden | What part of the fixed package it depends on most | Tao discriminator status | First obvious failure mode | Dynamic rating |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `vorticity-direction coherence` | [INFERRED] Use the standard direction evolution obtained from `(\partial_t + u . \nabla - \Delta)\omega = S\omega`: the stretching-facing part is the projected `S\xi` term, but diffusion also generates gradient terms involving `\nabla\xi` and `\nabla log|omega|`. Sources for why this is the right slot to fill: `missions/beyond-de-giorgi/CHAIN.md`, `missions/beyond-de-giorgi/steps/step-004/GOAL.md`. | [INFERRED] Diffusion acts directly on `\xi`; keeping coherence costs derivative control. The scalar amplitude identity also shows the penalty `-|omega||\nabla\xi|^2`, so rough direction fields dissipate the very intense region where the comparator is supposed to live. This is precisely the hidden `nabla xi` burden the local record warns against. Sources for the warning and benchmark boundary: `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`, `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`. | [INFERRED] Under the fixed Eulerian package, coherence must be measured on the moving intense set `E_r(t)`, not on a transported tube. Any localized coherence functional therefore picks up ball-cutoff commutators and boundary-motion terms from the threshold surface `|omega| = r^{-2}`. The real burden is that the comparator has no repository-backed bridge showing how localized coherence survives on the same intense region across `[t_* - r^2, t_*]`. Sources: `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`, `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-003/REPORT.md`, `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`. | [VERIFIED/INFERRED] It depends most on the Eulerian intense-set package rather than on the filament/tube scenario itself. The same comparator can be stated on both the filament/tube and sheet/pancake scenarios, which is exactly why Step 3 kept it as a cross-scenario benchmark. Sources: `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`, `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-003/REPORT.md`. | [VERIFIED/INFERRED] Only weakly live. The repository already classifies criterion-level direction regularity as prior art and Tao-robust benchmark material. The discriminator would revive only if one had a new localized persistence bridge under the fixed package. No such bridge appears in the local record. Sources: `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`, `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`, `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`. | [VERIFIED/INFERRED] It first fails by collapsing into prior-art direction criteria or by smuggling in hidden `nabla xi` control once one tries to keep the coherence localized and persistent on `E_r(t)`. Sources: `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`, `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`, `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`. | `informative but dynamically weak` |
| `tube coherence / persistence` | [INFERRED] There is no direct transport identity in the local corpus for connected components, tube axes, or thresholded-set topology. The best available heuristic is therefore the amplitude equation for `|omega|`: intense components can persist only insofar as the superlevel set `E_r(t)` stays populated over the diffusion-scale interval `[t_* - r^2, t_*]`. Sources for why this is the only honest dynamic reading: `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`, `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`. | [INFERRED] Diffusion immediately acts on the thresholded superlevel geometry: components can thicken, pinch off, merge, disappear, or cross the threshold on the same `r^2` time scale used by the audit. Unlike direction coherence, there is no comparator-specific PDE quantity whose diffusion loss stays inside the route; the object itself is a moving level-set geometry. Sources for the repository-side consequence: `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`, `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`. | [INFERRED] This is the heavier burden of the two comparators. In the fixed Eulerian ball one must decide what counts as "the same tube" across time while allowing leakage across `\partial B_r`, threshold crossings at `|omega| = r^{-2}`, and component births/deaths/mergers/splits. Keeping the route alive would require tube-adapted relabeling or stronger Lagrangian tracking, which the Step-3 package explicitly forbids as primary localization. Sources: `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`, `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-002/REPORT.md`, `library/factual/geometry-route-screening/step-3-should-start-with-a-neutral-eulerian-parabolic-localization-package.md`, `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`. | [VERIFIED/INFERRED] It depends most on the filament/tube scenario and on the thresholded Eulerian localization. Without the primary tube-like scenario there is no comparator object; without the fixed threshold/window there is no auditable persistence claim. Sources: `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`, `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-003/REPORT.md`. | [VERIFIED/INFERRED] Nominally live only if genuine persistence across scales and times is shown, but under the fixed package that discriminator does not cash out dynamically. Once the route is reduced to one-time tube-shaped concentration, it is Tao-robust and static. Sources: `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`, `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`, `library/meta/obstruction-screening/for-geometry-branches-only-dynamic-coherence-or-persistence-clears-the-tao-screen.md`. | [VERIFIED/INFERRED] The first failure is mistaking one-time tube concentration for persistence. The next is hidden tube-adapted relocalization: once the "same tube" is tracked by hand, the localization has installed the desired geometry instead of auditing it. Sources: `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`, `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`, `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`. | `static-only` |

### 4. Direction-only route: detailed read

- [VERIFIED] The local record already classifies standalone direction
  regularity as prior-art calibrated and requires any new route to add a
  localized NS-specific bridge from coherence to full stretching or to a new
  persistence mechanism.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
- [INFERRED] The best dynamic story available is still real but too weak:
  direction is stretching-facing because `\xi . S\xi` is exactly the scalar
  factor that appears in the amplitude equation, but the diffusion-generated
  terms mean coherence is not a passively transported Eulerian observable.
- [INFERRED] Under the fixed package, the main burden is not merely "diffusion
  is bad." It is that any localized coherence quantity on `E_r(t)` naturally
  asks for derivative control of `\xi`, threshold-boundary control, or both.
  That is exactly the hidden upgrade the Step-2 and Step-3 records tell us not
  to smuggle in.
- [INFERRED] This makes the comparator dynamically weaker than the primary
  hybrid. It keeps the stretching-facing part, but it loses the only locally
  credible Tao-sensitive persistence story, namely coherent tube persistence
  across time and scale.
- [INFERRED] So the direction-only route does not outperform the hybrid. It is
  still useful because it isolates one failure mode sharply:
  the hybrid really does need the persistence half; otherwise the route
  collapses back into prior-art direction criteria plus hidden derivative
  control.

### 5. Tube-only route: detailed read

- [VERIFIED] The repository kept tube persistence alive only as a dynamic or
  hybrid route and explicitly ruled out descriptive tube language or coherent
  snapshots as sufficient.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
- [INFERRED] The dynamic trouble is stronger here than for direction-only:
  there is no direct transport law for "tube coherence" in the fixed Eulerian
  package, only a heuristic that intense superlevel components of `|omega|`
  might remain tube-like for a short time.
- [INFERRED] Once the burden is stated honestly, the route nearly empties out.
  The object that must persist is a connected-component geometry of the moving
  superlevel set `E_r(t)`, but the fixed package purposely avoids the
  tube-adapted relocalization that would make such tracking cheap.
- [INFERRED] That means the tube-only comparator is not just weaker than the
  hybrid; as a promoted dynamic route it collapses into static tube language.
  Its only remaining value is diagnostic:
  it exposes why the hybrid needs the direction half to stay pointed at full
  stretching rather than at vivid but estimate-free geometry.

### 6. Collapse checks required by the task

- [VERIFIED/INFERRED] `vorticity-direction coherence` collapses toward prior-art
  direction criteria once the dynamic burden is named, unless one introduces a
  new localized persistence bridge. The first hidden upgrade is stronger
  `nabla xi` control.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `library/factual/geometry-route-screening/direction-regularity-is-prior-art-not-a-standalone-novelty-claim.md`
- [VERIFIED/INFERRED] `tube coherence / persistence` collapses toward static
  tube language once the fixed Eulerian localization is enforced, unless one
  introduces tube-adapted relocalization or a new component-tracking law.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
  - `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
- [VERIFIED/INFERRED] Neither comparator earns hidden derivative control or
  hidden relocalization under the fixed package. If either route needs those
  additions, that is a negative finding rather than a rescue.
  Sources:
  - `missions/beyond-de-giorgi/steps/step-004/GOAL.md`
  - `missions/beyond-de-giorgi/steps/step-003/RESULTS.md`
  - `runtime/results/codex-patlas-standalone-20260331T113910Z-receptionist-79670.md`

### 7. Comparative verdict

- [INFERRED] `vorticity-direction coherence` is dynamically weaker than the
  primary hybrid, not dynamically stronger.
- [INFERRED] `tube coherence / persistence` is also dynamically weaker than the
  primary hybrid and, under the fixed package, is useful mainly because it
  reveals why the hybrid needs both pieces.
- [INFERRED] Neither comparator outperforms the primary hybrid.
- [INFERRED] The hybrid's necessity is now sharper:
  the direction half keeps the route tied to full stretching, and the tube
  half is the only locally supported source of a Tao-sensitive persistence
  story. Remove either part and the route collapses into prior-art direction
  criteria, static tube language, or hidden extra control.

## Dead Ends / Failed Attempts

- [VERIFIED] I searched the required local corpus for an explicit localized
  transport formula for `xi` or for Eulerian tube-component persistence and did
  not find one. The repository supplies screening rules and candidate
  boundaries, not formula-level comparator evolution laws.
- [INFERRED] Because of that gap, all transport identities above are standard
  Navier-Stokes scaffolding rather than repository-verified formulas.
- [INFERRED] I did not promote either comparator using tube-adapted
  relocalization, tuned threshold/window choices, or hidden `nabla xi` control,
  because the Step-3 package and the Step-4 task explicitly forbid treating
  those as free inputs.

## Conclusion

- Outcome: `succeeded`
- Comparator verdicts:
  - `vorticity-direction coherence`: `informative but dynamically weak`
  - `tube coherence / persistence`: `static-only`
- Outperformance check:
  neither comparator outperforms the primary hybrid
- One-line takeaway:
  the direction-only route loses the persistence bridge, while the tube-only
  route loses the stretching-facing quantity, so the fixed Step-3 package makes
  the hybrid look necessary rather than redundant.
