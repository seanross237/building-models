<!-- explorer-type: explorer -->

# Exploration 001: Reconstruct the Exact Far-Field Pressure Obstruction

## Goal

Produce an equation-level reconstruction of the exact pressure obstruction behind the mission's surviving "far-field pressure harmonicity" loophole. The output must be precise enough to feed directly into the next exploration, which will test Tao-compatibility against averaged Navier-Stokes.

This is a reconstruction task, not a broad literature survey.

## Required deliverables

Deliver all of the following:

1. The exact pressure decomposition and pairing under discussion, with notation, domains/cylinders, and the specific integral that is supposed to be improved by exploiting harmonicity.
2. A clear verdict on what object the loophole is actually about:
   - the nonlocal / far-field pressure term,
   - the local pressure term `P_k^{21}`,
   - or some reinterpretation linking the two.
3. The recurrence slot where the problematic coefficient enters Vasseur's De Giorgi recurrence.
4. The exponent arithmetic showing how that slot connects to the `beta = 4/3` barrier.
5. An explicit explanation of why the coefficient is fixed `O(E_0)` rather than `U_k`-dependent in the baseline argument.
6. A compact equation-level statement, suitable for the Tao-filter follow-up, of exactly what would need to survive under averaged Navier-Stokes for the loophole to remain alive.
7. A short source table listing which formulas came from which source.

## Background to preload

Use these local sources first:

- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/proposition-3-sharpness-audit.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/beta-current-value-four-thirds.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/h1-pressure-dead-end.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/instances/vasseur-pressure/strategies/strategy-002/FINAL-REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/instances/vasseur-pressure/strategies/strategy-001/FINAL-REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/instances/vasseur-pressure/MISSION-COMPLETE.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/MISSION.md`
- `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/MISSION-VALIDATION-GUIDE.md`

Primary-source targets:

- Vasseur (2007), especially Proposition 3 / Section 4.
- Choi-Vasseur (2014) only if needed for decomposition comparison.
- Vasseur-Yang (2021) only if useful as a contrast showing where the same `4/3` arithmetic reappears without pressure.

## Known context

The local library already says:

- the De Giorgi bottleneck is the non-divergence-form pressure interaction in Proposition 3,
- the `1/2 + 5/6 = 4/3` arithmetic is the load-bearing exponent decomposition,
- the `H^1` pressure route failed because pressure control stayed at fixed energy scale,
- an untested lead remained: the far-field pressure may be harmonic on the local cylinder, with oscillation decay via Harnack.

Your job is to reconcile these statements exactly. In particular:

- If the "far-field harmonic loophole" is really a reformulation of an already-closed `P_k^{21}` obstruction, say so explicitly.
- If it instead concerns a different pressure split than the one used in the De Giorgi recurrence, identify that split cleanly and explain how it would have to plug back into the recurrence.
- If the prior mission language conflates distinct pressure decompositions, untangle that carefully.

## Constraints

- Do not spend effort on a broad Navier-Stokes survey.
- Do not re-prove the full `beta = 4/3` sharpness theorem.
- Do not drift into speculative constructive models.
- Stay equation-first: exact formulas, exact recurrence slot, exact exponent bookkeeping.
- Distinguish paper-sourced statements from your own synthesis.

## Output format

Write:

1. `REPORT-SUMMARY.md`
2. `REPORT.md`

Structure `REPORT.md` as:

1. Executive verdict
2. Exact formulas and pressure decomposition
3. Recurrence-slot reconstruction
4. Why the coefficient is fixed rather than `U_k`-dependent
5. Compact Tao-filter statement
6. Source table

Tag substantial statements as `[VERIFIED]`, `[CHECKED]`, or `[CONJECTURED]`.

## Failure mode to avoid

Do not answer with only prose like "the far-field term is harmonic and therefore maybe smaller." The mission needs the exact integral, the exact place it enters the recurrence, and the exact coefficient logic.
