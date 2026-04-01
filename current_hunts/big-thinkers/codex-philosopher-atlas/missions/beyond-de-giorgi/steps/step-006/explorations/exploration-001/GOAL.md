# Exploration 001 Goal

## Objective

Run the Tao discriminator on the first two frozen exact-rewrite candidates for
`step-006` of the chain
`Fixed-Protocol Obstruction Audit for Exact NS Reformulations`:

- `divergence / stress form`
- `Lamb-vector / Helmholtz-projected form`

The audit setup is already frozen and must not be changed:

- architecture:
  `local-energy flux/localization`
- bad term:
  `I_flux[φ] = ∬_{Q_r} (|u|^2 + 2p) u · ∇φ`
- solution class:
  suitable weak solutions in the Leray-Hopf energy class with LEI
- localization protocol:
  one CKN-style parabolic cutoff, with projection, Calderon-Zygmund,
  commutator, and Biot-Savart debt charged explicitly
- gain currency:
  `coefficient shrinkage in the fixed localized LEI balance`

## Required Questions

Answer all of the following from local repository sources:

1. For `divergence / stress form`, what exact Navier-Stokes feature is
   supposed to matter beyond a bare identity?
2. For `Lamb-vector / Helmholtz-projected form`, what exact Navier-Stokes
   feature is supposed to matter beyond a bare identity?
3. For each candidate, does Tao-style averaging destroy, weaken, or preserve
   that feature once the claim is stated precisely?
4. For each candidate, where in the fixed localized balance on `I_flux[φ]`
   could the distinction matter, if anywhere, before changing architecture or
   hypotheses?
5. Which candidate-specific claims are only identity-level, only verbal, or
   only available by silently changing architecture or hypotheses?
6. What is the honest Step-2 classification for each candidate:
   `admit to Step 3`,
   `reject as Tao-insufficient`,
   or `reject as architecture-changing`?

## Working Hypotheses To Test, Not Assume

- `divergence / stress form` likely relocates derivatives onto the cutoff but
  recreates the same stress-against-`∇φ` burden after integration by parts.
- `Lamb-vector / Helmholtz-projected form` likely exposes a cleaner first-order
  identity, but the gain may wash out once projection / pressure / commutator
  debt is restored after localization.

You should confirm, refine, or reject those hypotheses from the source record.

## Success Criteria

- Each of the two candidates receives:
  - one explicit claimed NS-specific feature,
  - one Tao-screen verdict
    (`destroys`, `weakens`, or `preserves`),
  - one localized insertion-point note,
  - and one admission/rejection classification.
- Every major claim is labeled `[VERIFIED]`, `[INFERRED]`, or `[PROPOSED]`.
- The report states clearly whether either candidate reaches Step 3.

## Failure Criteria

- The candidate's alleged specialness cannot be stated more precisely than
  "it is a nicer rewrite."
- The only way to keep a candidate alive is to change architecture, switch the
  bad term, or smuggle in stronger hypotheses.

If failure occurs, say so directly and recommend rejection rather than
continuation by rhetoric.

## Source Priorities

Use the local repository only. High-priority anchors:

- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/steps/step-006/GOAL.md`
- `missions/beyond-de-giorgi/steps/step-005/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-005/explorations/exploration-003/REPORT.md`
- `library/factual/exact-rewrite-obstruction-audit/projected-and-vorticity-rewrites-must-pay-localization-debt.md`
- `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- `library/factual/far-field-pressure-obstruction/algebraic-rewrites-and-local-geometry-fail-the-tao-gate.md`
- `missions/beyond-de-giorgi/controller/decisions/decision-008.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `runtime/results/codex-patlas-standalone-20260331T130634Z-receptionist-94037.md`

## Output Requirements

Write:

- `REPORT.md`
- `REPORT-SUMMARY.md`

Use source-based labels such as `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]`.
Keep the conclusion narrow and tied to the fixed LEI architecture.
