# Exploration 002 Report

## Goal

Fix one explicit localization protocol for Step 3 of the geometry route, using
`filament or tube concentration` as the primary scenario and `sheet or pancake
concentration` as the comparator, with explicit threshold, spatial scale, time
window, and localization type stated before any bounded observable table is
defined.

## Method

- Read the required Step 3 and Step 2 repository anchors.
- Extract repository-verified constraints on acceptable localization.
- Propose one auditable protocol only where the repository does not already
  force a unique choice.
- Stress-test the protocol against the primary and comparator scenarios and
  against reasonable perturbations.

## Findings Log

### Initial setup

- [VERIFIED] Report scaffold created before analysis.

### Repository-supported constraints

- [VERIFIED] Step 3 requires the localization protocol to be fixed before any
  observables are defined, and it must explicitly name:
  - intensity threshold
  - spatial scale
  - time window
  - localization type
  Sources:
  - `missions/beyond-de-giorgi/steps/step-003/GOAL.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] The protocol is not allowed to win by hidden normalization. A
  candidate should be killed if its apparent strength comes from localization
  choices tailored to manufacture coherence. Sources:
  - `missions/beyond-de-giorgi/steps/step-003/GOAL.md`
  - `missions/beyond-de-giorgi/CHAIN.md`
  - `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- [VERIFIED] The live full-stretching-facing burdens already named in the local
  record are:
  - smaller exterior/inter-scale stretching contribution
  - smaller localization-evolution cost
  - possibly smaller local/self-induced stretching term
  Sources:
  - `library/factual/geometry-route-screening/geometry-candidates-must-act-on-full-stretching.md`
  - `library/meta/exploration-goal-design/fix-a-provisional-stretching-representation-early-in-geometry-screens.md`
  - `missions/beyond-de-giorgi/steps/step-002/explorations/exploration-002/REPORT.md`
- [VERIFIED] Exploration 001 fixed the primary scenario as
  `filament or tube concentration` and retained `sheet or pancake
  concentration` only as a comparator. Source:
  - `missions/beyond-de-giorgi/steps/step-003/explorations/exploration-001/REPORT.md`
- [VERIFIED] The local repository does not provide a pre-existing numeric
  localization recipe. Any explicit threshold constant or exact scale rule used
  here must therefore be marked `[PROPOSED]`. Source:
  - receptionist result summarized in `missions/beyond-de-giorgi/steps/step-003/REASONING.md`

### Localization-type choice

- [INFERRED] The primary localization type should be `Eulerian`, not
  `tube-adapted` and not fully `Lagrangian`.
- [INFERRED] Why not `tube-adapted` as primary:
  the main hidden-normalization danger in this step is defining the region in a
  way that already follows the hoped-for coherent tube family. That would make
  later success ambiguous because the localization itself would have installed
  the geometry being tested.
- [INFERRED] Why not `Lagrangian` as primary:
  Step 3 is still before the explicit dynamic plausibility screen. A fully
  transported localization would import stronger propagation structure too
  early and blur whether persistence is being observed or assumed.
- [INFERRED] Why `Eulerian` is preferred:
  it is auditable, scenario-compatible for both filament/tube and
  sheet/pancake comparators, and it lets tube-family persistence show up as a
  later property of the intense set rather than as a definition.

### Fixed protocol proposal

- [PROPOSED] Intensity threshold:
  use the superlevel condition
  `|omega(x,t)| >= K_* r^{-2}` with one fixed dimensionless constant `K_* = 1`.
- [PROPOSED] Spatial scale:
  work on one dyadic ball `B_r(x_*)` at a time, centered at a candidate intense
  point `(x_*, t_*)`, with `r` chosen from the dyadic step scale under audit
  rather than from a tube-fitted axis.
- [PROPOSED] Time window:
  use the backward parabolic interval `[t_* - r^2, t_*]`.
- [INFERRED] Localization type:
  `Eulerian`.

Combined protocol:

- [PROPOSED] Audit the intense set
  `E_r(t) = { x in B_r(x_*) : |omega(x,t)| >= r^{-2} }`
  on the parabolic cylinder
  `Q_r(x_*, t_*) = B_r(x_*) x [t_* - r^2, t_*]`,
  with all candidate observables computed from this Eulerian data package first.

### Why this protocol is the right fit

- [INFERRED] The amplitude threshold `r^{-2}` is the simplest scale-matched
  vorticity threshold available on the local record. It ties intensity to the
  chosen spatial scale without importing a tube-specific geometry or a
  data-dependent normalization like "top quantile" or "fraction of the local
  maximum."
- [INFERRED] The dyadic ball `B_r(x_*)` is preferable to a tube-adapted region
  because it keeps the geometry neutral at the definition stage. Tube
  persistence has to emerge from the structure of the intense set inside the
  ball, not from the coordinate choice.
- [INFERRED] The backward parabolic window `[t_* - r^2, t_*]` is the natural
  minimal persistence window for a Navier-Stokes-scale audit. It is long enough
  to ask whether coherence survives over one diffusion-scale interval, but not
  so long that persistence is being demanded as a theorem before the dynamic
  screen.
- [INFERRED] The same package keeps the comparator honest: a dyadic Eulerian
  ball can contain either a tube segment or a sheet patch at the same audited
  scale, so any later advantage for the filament/tube scenario has to come from
  the observable's behavior, not from a tube-fitted localization.
- [INFERRED] This protocol targets the right full-stretching-facing burden:
  whether coherence/persistence on the intense set can later make the
  exterior/inter-scale contribution or the localization-evolution cost smaller,
  rather than merely making the core geometry look more filamentary.

### Stability checks

#### Perturbation 1: threshold constant

- [INFERRED] Replace `K_* = 1` by `K_* = 1/2` or `K_* = 2`.
- [INFERRED] Expected effect:
  the intense set thickens or thins, but the protocol remains honest as long as
  any promoted observable is not critically dependent on one tuned threshold.
- [INFERRED] Diagnostic:
  if `direction coherence + tube persistence` looks viable only at one narrow
  threshold constant, then the branch is probably living on hidden
  normalization rather than a stable mechanism.

#### Perturbation 2: spatial scale

- [INFERRED] Replace `r` by `(1/2)r` or `2r`, keeping the same Eulerian type
  and scale-matched threshold rule `|omega| >= r^{-2}` relative to the audited
  radius.
- [INFERRED] Expected effect:
  a smaller ball isolates the most intense core while making boundary leakage
  more visible; a larger ball includes more exterior contribution and makes the
  comparator sheet geometry more competitive.
- [INFERRED] Diagnostic:
  if the candidate only looks viable at one hand-picked radius, then the
  protocol has not removed hidden scale tuning.

#### Perturbation 3: time-window length

- [INFERRED] Replace `[t_* - r^2, t_*]` by `[t_* - (1/2)r^2, t_*]` or
  `[t_* - 2r^2, t_*]`.
- [INFERRED] Expected effect:
  shorter windows reduce diffusion and transport burden; longer windows
  increase it. An honest persistence signal should degrade gradually, not
  disappear instantly when the window is modestly rescaled.
- [INFERRED] Diagnostic:
  if the hybrid survives only on an extremely short window, then the protocol
  is probably extracting a static snapshot rather than a persistence mechanism.

#### Perturbation 4: localization type

- [INFERRED] Compare the Eulerian protocol against a mild Lagrangian follow-up
  on a shorter subwindow, but do not replace the primary protocol.
- [INFERRED] Expected effect:
  a genuinely live mechanism may look somewhat cleaner under limited advection,
  but it should not require full tube-adapted tracking from the start.
- [INFERRED] Diagnostic:
  if the candidate only becomes coherent once the localization is explicitly
  made tube-adapted, that is strong evidence that the protocol was secretly
  installing the hoped-for geometry.

## Dead Ends / Failed Attempts

- [INFERRED] Fully tube-adapted localization was considered and rejected as the
  primary protocol because it would bias the test toward preserving the very
  tube-family coherence the branch wants to discover.
- [INFERRED] A threshold normalized by local maximum or quantile was also
  rejected as the primary protocol because the local record repeatedly warns
  against hidden normalization, and such choices would make the intense set too
  data-adaptive before the candidate table is even fixed.

## Kill-Condition Assessment

- [VERIFIED] The repository does not hand us a fully verified numeric package,
  so the threshold, scale, and window chosen here remain `[PROPOSED]`.
- [INFERRED] That does not by itself trigger the Step-3 kill condition. The
  kill condition in this exploration is about whether any honest explicit
  protocol can be fixed without quietly installing the hoped-for conclusion.
- [INFERRED] The present package is honest enough to keep the branch alive for
  the next screen because it is geometry-neutral at definition time, it keeps
  the comparator usable, and it names the burdens it is meant to expose.
- [INFERRED] A later kill should occur if the observable table turns out to be
  viable only after replacing this package by a more adaptive Lagrangian or
  tube-adapted one, or only at a sharply tuned threshold/scale choice.

## Conclusion

- Outcome: `succeeded`
- Fixed protocol:
  - threshold: `[PROPOSED] |omega| >= r^{-2}`
  - spatial scale: `[PROPOSED]` one dyadic ball `B_r(x_*)`
  - time window: `[PROPOSED] [t_* - r^2, t_*]`
  - localization type: `[INFERRED] Eulerian`
- Preferred over the main alternatives:
  - `tube-adapted` localization would install tube coherence too directly.
  - fully `Lagrangian` localization would discount localization-evolution cost
    too early.
  - local-max or quantile thresholds would normalize away part of the intended
    persistence burden.
- Main reason it is not secretly overfitted:
  the protocol does not follow a preselected tube axis or normalize by a
  data-dependent local maximum; it uses a neutral Eulerian parabolic package
  and forces tube persistence to emerge from the data rather than from the
  definition.
- First residual hidden-normalization risk:
  the choice of center `(x_*, t_*)` and dyadic scale `r` could still be tuned
  after seeing favorable filament geometry. Later steps must therefore keep the
  same scale/center discipline when comparing the primary and comparator
  scenarios.
