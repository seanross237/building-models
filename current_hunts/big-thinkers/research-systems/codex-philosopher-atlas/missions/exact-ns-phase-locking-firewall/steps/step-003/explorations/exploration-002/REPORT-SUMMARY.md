# Exploration 002 Summary

## Goal

- `[VERIFIED]` Audit recursive exact closure on each canonical second-budget
  shared-mode seed and determine whether any genuine finite fixed point
  survives inside the two-triad budget.

## What I Tried

- `[COMPUTED]` Replaced the placeholder spot-check script with
  `code/shared_mode_closure_audit.py`.
- `[COMPUTED]` Sampled radius-2 integer shared-mode seeds to recover the
  orbit-level seed patterns.
- `[COMPUTED]` Ran exhaustive raw orbit-sign closure on canonical
  representatives:
  `32` assignments for each five-orbit representative and
  `16` assignments for the four-orbit representative.

## Outcome

- `[CHECKED]` The honest second-budget catalog has exactly two seed families:
  five-orbit shared-vertex and four-orbit shared-edge.
- `[COMPUTED]` No assignment in either family reached an inside-budget fixed
  point.
- `[CHECKED]` The five-orbit family dies on pass 1 because at least one of the
  forward targets
  `a + 2b` or `a + 2c`
  must lie outside the seed support.
- `[CHECKED]` The four-orbit family dies on pass 1 because
  `(d, b) -> a + 2b`
  is always outside the seed support.

## Verification Scorecard

- `[COMPUTED]` Catalog sample:
  only `(support size 5, triad overlap 1)` and
  `(support size 4, triad overlap 2)` appeared.
- `[COMPUTED]` Five-orbit `generic` representative:
  `32/32` exact,
  `0/32` fixed,
  `32/32` spill on pass 1.
- `[COMPUTED]` Five-orbit `forward_collision` representative:
  `32/32` exact,
  `0/32` fixed,
  `32/32` spill on pass 1.
- `[COMPUTED]` Four-orbit `parallelogram` representative:
  `16/16` exact,
  `0/16` fixed,
  `16/16` spill on pass 1.

## Key Takeaway

- `[CHECKED]` The second budget already dies at the first honest closure pass:
  conjugate-completed ordered pairs force the missing opposite helicity sectors
  on the seed ledger and new off-budget wavevectors in the same pass.

## Proof Gaps Or Computation Gaps

- `[VERIFIED]` No enlargement audit was needed inside this exploration because
  closure left no apparent survivor to test.
- `[VERIFIED]` Projected ODEs were intentionally not derived; that remains a
  later-step task only if some future budget ever produces a survivor.

## Unexpected Findings

- `[COMPUTED]` The obstruction is stronger than a bare new-wavevector spill:
  every tested seed also saturates both helical sectors on the original seed
  orbits on pass 1.
- `[COMPUTED]` The five-orbit special subcase where
  `d + b = e`
  still dies immediately; the spill just moves to the other forward branch.
