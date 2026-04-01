# Exploration 001 Goal

## Objective

Choose exactly one inherited architecture and exactly one named bad term for
`step-005` of the chain
`Fixed-Protocol Obstruction Audit for Exact NS Reformulations`.

The exploration must compare the leading candidate architectures named in the
chain and then justify one final choice that is concrete enough for later
estimate testing:

- `De Giorgi truncation`
- `local-energy flux/localization`
- `vorticity stretching localization`

## Required Questions

Answer all of the following from local repository sources:

1. Which architecture is best supported for a fixed-protocol exact-rewrite
   audit, given the already-established mission negatives?
2. Which rival architectures are already exhausted, already strongly prefigured
   by prior negatives, or too mismatched to the natural rewrite shortlist?
3. Inside the chosen architecture, what is the single mission-central bad term
   that later rewrites must target?
4. Why is this the right target for the current chain rather than a disguised
   rerun of:
   - the killed far-field pressure branch,
   - the killed geometry branch,
   - or the already-known vorticity / Beltrami fragility story?
5. What would later success mean in this exact setup?

## Working Hypothesis To Test, Not Assume

The strategizer's current working hypothesis is:

- chosen architecture:
  `local-energy flux/localization`
- provisional bad term:
  the localized cutoff-flux bundle in the local energy inequality,
  schematically
  `∬ (|u|^2 + 2p) u · ∇φ`,
  or the exact subterm inside that bundle that should be frozen as the unique
  audit target.

You should confirm, refine, or reject this hypothesis based on the source
record. Do not inherit it uncritically.

## Success Criteria

- One architecture is selected and source-justified.
- One named bad term is selected and written explicitly enough that later steps
  cannot quietly change it.
- Rejected architectures are explained concretely, not by vibe.
- The memo states what a real later gain would mean in this fixed setup.

## Failure Criteria

- No source-supported architecture can be fixed without collapsing into an
  already-settled negative.
- The candidate bad term remains too vague to support a later loss ledger.

If failure occurs, say so directly and explain whether the step should trigger
an early under-specification kill.

## Source Priorities

Use the local repository only. High-priority anchors:

- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/CHAIN.md`
- `missions/beyond-de-giorgi/CHAIN-HISTORY.md`
- `missions/beyond-de-giorgi/planning-runs/run-003/selected/chain-01.md`
- `missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md`
- `missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md`
- `missions/beyond-de-giorgi/planning-runs/run-003/attacks/chain-01.md`
- `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
- `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/vasseur-pressure/steps/step-002/RESULTS.md`

## Output Requirements

Write:

- `REPORT.md`
- `REPORT-SUMMARY.md`

Use source-based labels such as `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]`.
Keep the conclusion narrow and auditable.
