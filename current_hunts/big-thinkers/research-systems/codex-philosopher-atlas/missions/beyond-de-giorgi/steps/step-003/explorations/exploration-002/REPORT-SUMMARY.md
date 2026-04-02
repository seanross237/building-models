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
- Perturbation checks:
  - threshold constant changed from `1` to `1/2` or `2`
  - spatial scale changed from `r` to `(1/2)r` or `2r`
  - time window changed from `r^2` to `(1/2)r^2` or `2r^2`
- Why this package is preferred over the main alternatives:
  - `tube-adapted` localization would put tube coherence into the definition
  - fully `Lagrangian` localization would hide too much localization-evolution
    cost before the dynamic screen
  - local-max or quantile thresholds would add extra hidden normalization
- Main reason the protocol is not secretly overfitted:
  it avoids preselecting a tube axis, avoids local-maximum or quantile
  normalization, and keeps the comparator scenario usable under the same basic
  localization package.
- First residual hidden-normalization risk:
  the choice of center `(x_*, t_*)` and dyadic scale `r` could still be tuned
  after seeing favorable filament geometry, so later steps must keep that
  choice rule fixed when comparing candidates or scenarios.
