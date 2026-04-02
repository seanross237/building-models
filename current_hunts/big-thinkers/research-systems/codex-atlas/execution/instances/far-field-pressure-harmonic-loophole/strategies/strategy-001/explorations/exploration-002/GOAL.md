<!-- explorer-type: explorer -->

# Exploration 002: Tao Filter for the Harmonic Far-Field Pressure Loophole

## Goal

Decide whether the mission's surviving harmonic far-field pressure loophole is **Tao-compatible**, **Tao-incompatible**, or **still unclear**.

Use primary-source reasoning tied to Tao's averaged Navier-Stokes construction. This is a falsification-first exploration.

## Preloaded context from exploration 001

Exploration 001 established:

- In Vasseur's actual De Giorgi recurrence, the `beta = 4/3` bottleneck is the **local non-divergence pressure term `P_{k21}`**, not the harmonic nonlocal term `P_{k1}`.
- The mission's loophole is therefore **not** "Vasseur forgot a harmonic term." It is an **alternative near/far pressure decomposition** question: can one rewrite the dangerous pressure interaction so that a far-field harmonic component carries the relevant mass and yields a better pairing?
- The exact Vasseur bottleneck slot is

```text
I_k ≤ ||P_{k21}||_{L^q} ||d_k||_{L^2} ||1_{v_k>0}||_{L^{2q/(q-2)}}
    ≤ C_q C^k U_{k-1}^{4/3 - 5/(3q)}.
```

- The Tao-filter question is therefore: can a harmonic far-field decomposition survive averaged Navier-Stokes in a way that actually changes this bottleneck mechanism, rather than merely renaming already favorable pieces?

Read first:

- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/far-field-pressure-harmonic-loophole/strategies/strategy-001/explorations/exploration-001/REPORT.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/post-2007-beta-landscape.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/s2-adversarial-review-beta-four-thirds.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/agents/library/factual/navier-stokes/vasseur-de-giorgi/non-cz-pressure-routes-tool-independence.md`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/codex-atlas/execution/instances/vasseur-pressure/COMPUTATIONS-FOR-LATER.md`

## Required deliverables

Produce all of the following:

1. The exact averaged Navier-Stokes nonlinearity and pressure equation from Tao's construction, with explicit formulas from the primary source.
2. A sourced answer to: what replaces `-Δp = ∂i∂j(u_i u_j)` after averaging?
3. A sourced or carefully inferred answer to whether a local near/far pressure split with harmonic far-field component still exists in the averaged setting.
4. An explicit comparison table:
   - ordinary NS / Vasseur split
   - alternative harmonic far-field loophole picture
   - Tao averaged NS
   and for each row: what the pressure object is, whether it is harmonic on the local cylinder, and what the new bottleneck is.
5. A verdict table with exactly one of:
   - `Tao-compatible`
   - `Tao-incompatible`
   - `still unclear`
6. If the answer is not `Tao-compatible`, state precisely what exploration 003 should compute or model.

## Primary-source targets

Use primary sources, not secondary paraphrase, for Tao's construction:

- Tao's 2016 averaged Navier-Stokes blowup paper.
- Any directly cited companion definitions or appendices needed to state the averaged bilinear operator and the pressure law.

Secondary / local context is allowed only for orientation after the primary-source formulas are fixed.

## Null hypothesis

Assume by default that the loophole is **Tao-compatible** unless you can point to a specific algebraic feature of ordinary NS pressure that averaging destroys and that the harmonic far-field mechanism genuinely needs.

You must explicitly answer:

- What is the new bottleneck in the averaged setting?
- If you think the loophole survives, what specific NS structure is being used that Tao's averaging removes?

## Constraints

- Do not do a broad Tao literature survey.
- Do not re-derive the whole De Giorgi obstruction.
- Do not rely on vague statements like "averaging probably preserves harmonicity."
- Distinguish clearly between:
  - sourced formulas,
  - direct deductions from those formulas,
  - open uncertainties.

## Output format

Write:

1. `REPORT-SUMMARY.md`
2. `REPORT.md`

Structure `REPORT.md` as:

1. Executive verdict
2. Tao averaged equation and pressure law
3. Harmonic far-field comparison
4. Bottleneck replacement analysis
5. Verdict table
6. Recommended next move

Tag substantial statements as `[VERIFIED]`, `[CHECKED]`, or `[CONJECTURED]`.

## Failure mode to avoid

Do not stop at "Tao says generic harmonic-analysis methods fail." This exploration must decide whether the **specific harmonic far-field pressure mechanism** survives averaging at the equation level.
