<!-- explorer-type: explorer -->

# Exploration 001 Goal

## Goal

Reconstruct Tao's 2016 averaged Navier-Stokes blowup mechanism at equation level, sharply enough to support later real-NS intervention mapping. This exploration is Phase 0 only. It must separate:

1. the averaged bilinear operator itself,
2. the finite-dimensional cascade / transfer architecture extracted from it,
3. the final blowup mechanism.

## Why This Matters

This strategy cannot propose a firewall candidate unless Tao's actual mechanism is recovered precisely. Prior Atlas work already closes generic estimate-level refinements, generic pressure rewrites, standard compactness hosts, and BKM/enstrophy bypasses. The live question is mechanism-level: what exact structure of real NS blocks Tao's cascade, if any?

## Preloaded Context

- The local Atlas barrier context says Tao (2016) is the benchmark showing that energy identity + generic harmonic-analysis estimates are insufficient.
- The strongest local Tao-filter notes are:
  - `execution/instances/navier-stokes/library-inbox/exploration-005-literature-vortex-stretching.md`
  - `execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-002/REPORT.md`
- Those notes already recover:
  - the ordinary NS bilinear form `B(u,v) = -(1/2) P[(u·∇)v + (v·∇)u]`,
  - Tao's averaged operator as an average over rotations, dilations, and order-zero Fourier multipliers,
  - the averaged primitive-variable pressure law `-Δp = div T(u,u)`,
  - the strategic point that Tao preserves generic harmonic-analysis structure while removing finer NS structure.
- What the local library does **not** already provide is the actual finite-dimensional cascade architecture in enough detail to use directly. So this exploration must be paper-first on the cascade internals.

## Required Deliverables

Your `REPORT.md` and `REPORT-SUMMARY.md` must provide:

1. The explicit form of Tao's averaged operator and the averaging ingredients.
2. A clear notation map distinguishing:
   - the averaged PDE,
   - any shell/model reduction or circuit/cascade system,
   - the final blowup argument.
3. The specific modal packets, amplitudes, or variables that carry energy across scales.
4. A step-by-step schematic of the cascade:
   - which scale talks to which,
   - what transfer is amplified or delayed,
   - what stability / timing mechanism matters.
5. The exact load-bearing identities, cancellations, sign constraints, or symmetries Tao uses.
6. A short list of mechanism steps that can later be compared directly to exact NS triadic interactions.
7. An explicit verdict:
   - `succeeded`: mechanism reconstructed sharply enough for Phase 1,
   - `failed`: reconstruction not sharp enough, with the precise missing pieces.

## Constraints

- Do not drift into a broad regularity survey.
- Do not spend budget re-closing estimate-level routes.
- Distinguish rigorously between what is literally in Tao's construction and what you infer from it.
- Prefer equations, named variables, and causal mechanism statements over prose slogans.
- If the paper forces a reconstruction gap, say so bluntly instead of inventing a firewall candidate.

## Helpful Questions

Use these as a checklist:

1. What is the exact averaged operator and which structural NS features does it preserve?
2. How does Tao pass from that operator to a controllable finite-dimensional cascade?
3. What are the gate variables or modal amplitudes at one scale, and how do they trigger the next scale?
4. Which parts of the mechanism depend on averaging to isolate interactions or suppress unwanted couplings?
5. At what exact steps would one later ask whether real NS triadic geometry, pressure coupling, or incompressibility would interfere?

## Output Discipline

- Start `REPORT.md` with a skeleton and fill it incrementally.
- End `REPORT-SUMMARY.md` with:
  - outcome,
  - one key takeaway,
  - leads worth pursuing,
  - unexpected findings,
  - computations worth doing later.
