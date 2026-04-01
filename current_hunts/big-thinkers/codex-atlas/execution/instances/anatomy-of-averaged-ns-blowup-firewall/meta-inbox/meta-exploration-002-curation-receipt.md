# Curation Receipt: anatomy-of-averaged-ns-blowup-firewall exploration-002

## Added

- `execution/agents/library/factual/navier-stokes/exact-ns-triadic-coefficient-rigidity.md`
- `execution/agents/library/factual/navier-stokes/exact-ns-unavoidable-spectator-couplings.md`
- `execution/agents/library/meta/methodology/toy-subsystem-isolation-inside-exact-network.md`

## Updated

- `execution/agents/library/factual/navier-stokes/tao-averaged-ns-delayed-transfer-circuit.md`
- `execution/agents/library/factual/navier-stokes/INDEX.md`
- `execution/agents/library/factual/INDEX.md`
- `execution/agents/library/meta/goal-design/require-mechanism-layer-maps.md`
- `execution/agents/library/meta/goal-design/preload-context-from-prior-work.md`
- `execution/agents/library/meta/goal-design/INDEX.md`
- `execution/agents/library/meta/methodology/INDEX.md`
- `execution/agents/library/meta/INDEX.md`
- `execution/agents/library/curator-log.md`

## Skipped As Duplicates Or Already Covered

- Generic pressure/nonlocality, LP cleanup, commutator/CLMS, div-free level-set, and near-Beltrami routes were already filed in the Navier-Stokes library and were not duplicated.
- The meta lesson "pressure/Leray is enforcement, not the main candidate" was merged into `meta/methodology/toy-subsystem-isolation-inside-exact-network.md` instead of filed separately.
- The meta lesson about tying the comparison to Tao's literal gate chain was merged into `meta/goal-design/require-mechanism-layer-maps.md`.
- The meta lesson about preloading closed routes was merged into `meta/goal-design/preload-context-from-prior-work.md`.
- The explorer-drift execution note was skipped as not distinct enough from existing scoping/task-discipline guidance.

## Conflicts Resolved

- Pressure/Leray was classified as the enforcement mechanism for coefficient rigidity and spectator leakage, not filed as a third standalone firewall candidate.
- Literal-gate-chain guidance was treated as an update to the existing mechanism-layer-map entry rather than as a duplicate new meta entry.
- Closure-stack preload was treated as a variant of the existing preload rule rather than as a separate preload entry.

## Outcome

Exploration-002 is now curated as an exact-NS intervention map centered on two surviving firewall candidates:

1. exact triadic coefficient rigidity;
2. unavoidable spectator couplings in the full projected triad network.

The recommended next diagnostic is a minimal exact-support realization problem that writes all forced projected amplitude equations and tests whether Tao's desired hierarchy can dominate every spectator channel by a genuine small parameter.
