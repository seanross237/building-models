# History of Report Summaries

Exploration summaries will be appended here as they land.

---

## Exploration 001

# Exploration 001 Summary

- Goal: choose one primary singular-scenario class, and at most one comparator,
  for Step 3 of the geometry route after Step 2 narrowed the live branch to
  `direction coherence + tube persistence`.
- What was checked:
  - the Step 3 goal/reasoning files
  - the chain and run-002 refined/attack/judgment materials
  - the Step 2 results and both Step 2 exploration reports
  - the geometry-route screening notes and the Tao-screen obstruction note
- Outcome: succeeded
- One key takeaway:
  the live Step 2 hybrid is concrete only in a filament/tube concentration
  scenario, because the repository's actual stretching-facing test question is
  whether direction coherence persists along a coherent tube family strongly
  enough to reduce full stretching, including exterior/inter-scale effects.
- Primary scenario choice:
  `filament or tube concentration`
- Optional comparator:
  `sheet or pancake concentration`
- Why the rejected scenario class was not preferred:
  sheet/pancake concentration is present in the local record mainly as a
  discipline-enforcing comparator, not as the repository's favored natural home
  for the hybrid; more specific variants such as axial tube collapse or
  reconnection-type concentration are too sparsely supported to retain.
- Leads worth pursuing:
  - choose a localization package that can test tube-family persistence without
    baking in a tube-adapted advantage by definition
  - use the sheet/pancake comparator to check whether the next-step observable
    table collapses into generic direction regularity or bare concentration
- Unexpected findings:
  - the local record is stronger on why tube/filament should be primary than on
    any positive sheet/pancake mechanism
  - sheet/pancake survives mainly because chain discipline demands a concrete
    comparator, not because the Step 2 survivor is naturally sheet-based
- Computations worth doing later if outside scope:
  - once localization is chosen, test whether the candidate observable can even
    state a meaningful exterior/inter-scale stretching gain in both the primary
    and comparator scenarios before investing in any larger proof route
- Failure mode for each chosen scenario:
  - filament/tube concentration:
    the hybrid only improves tube-core or self-induced geometry while the
    exterior/inter-scale stretching contribution or localization-evolution cost
    stays large, so the scenario collapses into descriptive tube language.
- sheet/pancake concentration:
    the hybrid ceases to function as tube persistence and degrades into generic
    direction regularity or bare concentration, showing misfit rather than new
    stretching leverage.

---

## Exploration 002

# Exploration 002 Summary

- Goal: fix one explicit localization protocol for Step 3, for the primary
  `filament or tube concentration` scenario with `sheet or pancake
  concentration` retained as a comparator.
- What was checked:
  - `missions/beyond-de-giorgi/steps/step-003/GOAL.md`
  - `missions/beyond-de-giorgi/steps/step-003/REASONING.md`
  - `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-001/REPORT.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/refined/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/attacks/chain-02.md`
  - `missions/beyond-de-giorgi/planning-runs/run-002/judgments/chain-02.md`
  - `missions/beyond-de-giorgi/steps/step-002/RESULTS.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/factual/geometry-route-screening/tube-persistence-remains-live-only-as-a-dynamic-or-hybrid-route.md`
  - `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
  - `library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
  - `library/meta/exploration-goal-design/normalize-notation-and-name-the-operative-bound-up-front.md`
  - `library/meta/exploration-goal-design/state-nonlocal-moment-dependence-in-the-goal.md`
- Outcome: `succeeded`
- One key takeaway:
  the least overfitted Step-3 protocol is a neutral Eulerian parabolic package,
  not a tube-adapted one: define the intense set by a scale-matched vorticity
  threshold inside `B_r(x_*) x [t_* - r^2, t_*]` and force any tube coherence
  to emerge from that data rather than from the localization itself.
- Fixed threshold/scale/window/type package:
  - threshold: `[PROPOSED] |omega| >= r^{-2}`
  - scale: `[PROPOSED]` one dyadic ball `B_r(x_*)`
  - time window: `[PROPOSED] [t_* - r^2, t_*]`
  - type: `[INFERRED] Eulerian`
- Two perturbation checks:
  - threshold constant changed from `1` to `1/2` or `2`
  - time window changed from `r^2` to `(1/2)r^2` or `2r^2`
- Main reason the protocol is not secretly overfitted:
  it avoids preselecting a tube axis, avoids local-maximum or quantile
  normalization, and keeps the comparator scenario usable under the same basic
  localization package.
- First residual hidden-normalization risk:
  the choice of center `(x_*, t_*)` and dyadic scale `r` could still be tuned
  after seeing favorable filament geometry, so later steps must keep that
  choice rule fixed when comparing candidates or scenarios.

---

## Exploration 003

# Exploration 003 Summary

- Goal: define the bounded observable table for Step 3 using the fixed
  scenario and localization package.
- What was checked:
  - the Step 3 goal and reasoning files
  - Exploration 001 report on scenario class
  - Exploration 002 report on localization
  - Step 2 results and both Step 2 exploration reports
  - the geometry-route screening notes and the Tao-screen obstruction notes
- Outcome: `succeeded`
- One key takeaway:
  after fixing both scenario and localization, only one candidate still merits
  primary status:
  `direction coherence + tube persistence`. The direction-only and tube-only
  routes survive only as secondary comparators, while all Beltrami-family
  objects remain fragility screens.
- Compact candidate ranking:
  - primary:
    `direction coherence + tube persistence`
  - secondary:
    `vorticity-direction coherence`,
    `tube coherence / persistence`
  - effectively dead as promoted routes:
    `local Beltrami / alignment`,
    `Beltrami deficit + concentration`,
    `Beltrami deficit + anisotropy`
- Whether the branch should advance to the dynamic plausibility screen:
  yes, but only narrowly and only on the fixed Step-3 package. The next step
  should kill the route immediately if the primary hybrid needs tube-adapted
  relocalization, tuned threshold/window choices, or stronger derivative
  control than the bounded package contains.
