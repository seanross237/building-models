# Curation Receipt — Meta Exploration 001

Date: 2026-03-31
Mission: `far-field-pressure-harmonic-loophole`
Strategy: `strategy-001`
Exploration: `exploration-001`

## Added

- `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/exact-far-field-pressure-obstruction.md`
- `execution/agents/library/meta/methodology/reconcile-notation-before-falsification.md`

## Updated

- `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/h1-pressure-dead-end.md`
- `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md`
- `execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/INDEX.md`
- `execution/agents/library/factual/navier-stokes/INDEX.md`
- `execution/agents/library/factual/INDEX.md`
- `execution/agents/library/meta/methodology/INDEX.md`
- `execution/agents/library/meta/INDEX.md`
- `execution/agents/library/curator-log.md`

## Duplicates Skipped

- Meta execution note about the explorer exiting after a report skeleton. This was not filed as a new entry because the lesson is already covered by:
  - `execution/agents/library/meta/goal-design/preload-context-from-prior-work.md`
  - `execution/agents/library/meta/system-behavior/explorer-crashes-and-path-confusion.md`

## Conflicts Resolved

- Resolved a factual notation conflict in the existing library:
  - prior shorthand implied "far-field term `P_{k21}`"
  - curated result: in literal Vasseur notation, `P_{k21}` is the bad **local** term and `P_{k1}` is the already-favorable harmonic/nonlocal term
  - surviving loophole now stored as a decomposition-mismatch question involving an alternative near/far split

## Outcome

The factual library now records the exact obstruction correctly, and the meta library now records the process lesson: reconcile notation across predecessor vocabularies before falsification work.
