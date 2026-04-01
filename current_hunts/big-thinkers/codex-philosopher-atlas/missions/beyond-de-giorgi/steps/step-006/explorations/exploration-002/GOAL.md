# Exploration 002 Goal

## Objective

Run the Tao discriminator on the third frozen exact-rewrite candidate for
`step-006`:

- `vorticity transport / Biot-Savart form`

This candidate must be screened under the same already-fixed audit setup:

- architecture:
  `local-energy flux/localization`
- bad term:
  `I_flux[φ] = ∬_{Q_r} (|u|^2 + 2p) u · ∇φ`
- solution class:
  suitable weak solutions in the Leray-Hopf energy class with LEI
- localization protocol:
  one CKN-style parabolic cutoff, with all Biot-Savart, projection,
  Calderon-Zygmund, and commutator debt charged explicitly
- gain currency:
  `coefficient shrinkage in the fixed localized LEI balance`

## Required Questions

Answer all of the following from local repository sources:

1. What exact Navier-Stokes feature is this vorticity-side candidate claiming
   to exploit?
2. Is that feature genuinely absent from Tao's averaged setting, or does the
   repository only support it as a restatement of the same quadratic
   interaction?
3. Where could the distinction matter inside the fixed localized estimate on
   `I_flux[φ]`, if anywhere, before changing architecture?
4. Does keeping this candidate alive require silent architecture drift toward
   vorticity stretching or geometry work?
5. Does Biot-Savart reinsertion merely repay the same nonlocal cost, and if
   so, what does that imply for Step 2 classification?

## Working Hypothesis To Test, Not Assume

The strategizer's current hypothesis is:

- the candidate may look more Navier-Stokes-specific because it rewrites
  through `ω`, but the fixed local record likely supports only a negative
  verdict:
  either the same cost returns through Biot-Savart nonlocality, or the route
  becomes architecture-changing by drifting toward stretching/geometry
  localization.

Confirm, refine, or reject that hypothesis from the sources.

## Success Criteria

- The report states the claimed NS-specific feature precisely.
- The report gives a Tao-screen verdict
  (`destroys`, `weakens`, or `preserves`) and explains why.
- The report names the exact localized insertion point, or says plainly that
  there is none before Step 3.
- The report ends with one honest Step-2 classification:
  `admit to Step 3`,
  `reject as Tao-insufficient`,
  or `reject as architecture-changing`.

## Failure Criteria

- The candidate cannot be separated from a generic vorticity reformulation
  slogan.
- The only live effect depends on moving to a different bad term,
  different localization, or geometry-style stretching control.

If failure occurs, say so directly and classify the route accordingly.

## Source Priorities

Use the local repository only. High-priority anchors:

- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/steps/step-006/GOAL.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `library/factual/far-field-pressure-obstruction/generic-harmonic-regularity-fails-the-tao-gate.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-008.md`
- `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`

## Output Requirements

Write:

- `REPORT.md`
- `REPORT-SUMMARY.md`

Use source-based labels such as `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]`.
Keep the conclusion narrow and tied to the fixed LEI architecture.
