# Exploration 002 Summary - Comparator Dynamic Audit

- goal:
  audit `vorticity-direction coherence` and `tube coherence / persistence`
  against the fixed Step-3 package
  (`filament or tube concentration` / `sheet or pancake concentration`,
  Eulerian `B_r(x_*) x [t_* - r^2, t_*]`, threshold `|omega| >= r^{-2}`).
- what was checked:
  the best available transport identity or propagation heuristic for each
  comparator, the main diffusion loss, the main localization-evolution or
  commutator burden, dependence on the fixed package, Tao-discriminator status,
  and the first obvious failure mode, using the Step-2/3/4 record plus the
  geometry-screening library notes.
- outcome:
  `succeeded`
- one key takeaway:
  neither comparator beats the primary hybrid; direction-only loses the
  persistence bridge, and tube-only loses the stretching-facing quantity, so
  the fixed Step-3 package makes the hybrid look necessary rather than
  redundant.

- `vorticity-direction coherence`:
  - best transport / propagation story:
    [INFERRED] standard normalized-vorticity evolution from
    `(\partial_t + u . \nabla - \Delta)\omega = S\omega`;
    the route stays stretching-facing through `\xi . S\xi`, but direction is
    not passively transported once diffusion is present.
  - main diffusion loss:
    [INFERRED] diffusion acts directly on `\xi` and generates derivative costs;
    the accompanying amplitude identity penalizes rough directions through
    `-|omega||\nabla\xi|^2`.
  - main localization-evolution or commutator burden:
    [INFERRED] coherence must be measured on the moving intense set `E_r(t)`,
    so one pays both parabolic-cutoff commutators and threshold-boundary
    evolution without a repository-backed localized persistence bridge.
  - Tao discriminator status:
    [VERIFIED/INFERRED] only weakly live; criterion-level direction regularity
    is already prior-art and Tao-robust unless a new localized persistence
    bridge is supplied.
  - first obvious failure mode:
    [VERIFIED/INFERRED] collapse into prior-art direction criteria or hidden
    `nabla xi` control.
  - final rating:
    `informative but dynamically weak`

- `tube coherence / persistence`:
  - best transport / propagation story:
    [INFERRED] no direct transport law for connected components or tube axes;
    the best available heuristic is only that the superlevel set `E_r(t)` might
    remain populated across `[t_* - r^2, t_*]` according to the scalar
    `|omega|` evolution.
  - main diffusion loss:
    [INFERRED] diffusion acts on the thresholded superlevel geometry itself, so
    components can thicken, pinch off, merge, disappear, or cross the threshold
    on the same `r^2` time scale being audited.
  - main localization-evolution or commutator burden:
    [INFERRED] one must define "the same tube" inside a fixed Eulerian ball
    despite leakage across `\partial B_r`, threshold crossings, and
    births/deaths/mergers/splits of components; keeping the route alive would
    require the tube-adapted tracking the package was designed to forbid.
  - Tao discriminator status:
    [VERIFIED/INFERRED] dynamically dead under the fixed package; once reduced
    to one-time tube-shaped concentration, the route is Tao-robust and static.
  - first obvious failure mode:
    [VERIFIED/INFERRED] mistaking one-time tube concentration for persistence,
    then rescuing it with hidden tube-adapted relocalization.
  - final rating:
    `static-only`

- whether either comparator outperforms the primary hybrid:
  [INFERRED] no.

- what each comparator exposes about the hybrid:
  - [INFERRED] direction-only shows the hybrid needs the persistence half or it
    collapses back into prior-art direction criteria plus hidden derivative
    control.
  - [INFERRED] tube-only shows the hybrid needs the direction half or it
    collapses into vivid but estimate-free tube language.

- leads worth pursuing:
  - [INFERRED] if Step 4 still advances, the primary hybrid is the only route
    worth testing against a fixed stretching representation.
  - [INFERRED] the next stress test should keep the hidden-upgrade kill rule
    explicit: no tube-adapted relocalization, no tuned threshold/window rescue,
    and no imported `nabla xi` control.

- unexpected findings:
  - [VERIFIED] the local repository is consistent on the screening rule but
    does not contain formula-level localized transport laws for either
    comparator.
  - [INFERRED] once that gap is made explicit, tube-only downgrades more
    sharply than the Step-2 table alone suggested.

- computations worth doing later if outside scope:
  - [PROPOSED] if the mission advances, write one explicit localized coherence
    functional for the primary hybrid and compute its full cutoff/threshold
    commutator structure inside one fixed Step-4 stretching representation.
  - [PROPOSED] separately, compute whether the thresholded-set boundary motion
    can be quantified without tube-adapted relabeling; if not, that becomes a
    representation-stable obstruction rather than a loose heuristic.
