# Decision Memo - beyond-de-giorgi / decision-005

## Decision

`proceed`

## Mission-Control Verdict

This is a post-step review of `step-003`, which executed Chain Step 2 on the
active geometry branch. The step did what the chain required before any
transport or stretching claims were allowed: it fixed a concrete
scenario-and-localization package, bounded the observable family, and tested
whether the branch survived honest formulation.

The result keeps the chain alive, but only narrowly. `step-003` did not
discover a broad geometric route. It preserved one primary hybrid survivor,
`direction coherence + tube persistence`, only on a specific Step-3 package:
primary scenario `filament or tube concentration`, comparator scenario
`sheet or pancake concentration`, and an Eulerian parabolic localization on
`B_r(x_*) x [t_* - r^2, t_*]` with threshold `|omega| >= r^{-2}`.

That is not a reason to replan yet. Replanning would be correct if the latest
step had shown that no honest scenario/localization package kept the branch
concrete, or if only prior-art or static descriptors remained. The step found
the opposite: one bounded hybrid remains live enough to justify the chain's
next test, and the comparators are still useful for detecting collapse in the
next pass.

`terminate` is also wrong. The mission-level question is still open, and the
latest result is neither a terminal positive route nor a terminal negative map.

## Chain Assessment

The current chain remains active, but under a sharply constrained package.

What `step-003` settled:

- the branch may proceed only on the fixed primary scenario
  `filament or tube concentration`, with `sheet or pancake concentration` kept
  as a comparator rather than a coequal live route;
- the localization protocol is now fixed enough for controller purposes:
  Eulerian, parabolic, dyadic-ball based, and thresholded by `|omega| >= r^{-2}`;
- `direction coherence + tube persistence` remains the only primary candidate;
- `vorticity-direction coherence` and `tube coherence / persistence` remain
  only as secondary comparators;
- Beltrami-family objects remain fragility screens, not promoted routes;
- the next step should invalidate the branch immediately if the primary hybrid
  needs tube-adapted relocalization, tuned threshold/window choices, or
  stronger derivative control than the fixed package contains.

This is fully compatible with the active chain. Chain Step 3 is supposed to
ask what quantity is actually propagated, approximately preserved, or rapidly
lost under the chosen localization. `step-003` produced exactly the package
needed for that screen and did not yet answer it.

## Required Next Move

Proceed to `step-004` and execute **Chain Step 3 only**:

- run the early dynamic plausibility screen on the fixed Step-3 package;
- record, for the primary hybrid and bounded comparators, the best available
  transport identity, commutator burden, diffusion loss, and
  localization-evolution cost;
- classify candidates as `dynamically plausible`, `informative but dynamically
  weak`, or `static-only`;
- kill the branch early if the primary hybrid has no credible persistence story
  even heuristically under the fixed Eulerian package.

The strategizer should not move into kernel-level `S omega . omega`
representation work yet. If dynamic plausibility collapses, the next evaluator
pass can replan or invalidate the branch. At this stage, the correct
controller move is to proceed.
