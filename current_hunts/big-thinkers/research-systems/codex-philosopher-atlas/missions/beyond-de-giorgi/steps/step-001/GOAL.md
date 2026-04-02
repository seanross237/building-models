# Step 1 Goal: Exact Far-Field Obstruction Reconstruction and Tao Gate

## Mission Context

**Mission:** Beyond De Giorgi — What Structural Property Could Break the NS Regularity Barrier?

**Winning chain:** `Chain 01 - Harmonic Tail Obstruction Test with Early Tao Gate`

**Why this step exists:** The planning loop selected the pressure-side loophole as the best next branch, but only under strict gatekeeping. Before we spend exploration budget on harmonic-tail candidates, we need to pin down the exact surviving far-field pressure pairing from the earlier `vasseur-pressure` mission and decide which, if any, candidate NS-specific ingredients survive Tao's 2016 filter.

## This Step Covers

This strategizer execution covers **Chain Step 1 only**:

- rebuild the exact far-field obstruction
- identify the surviving harmonic modes or pairings after quotienting out what the test structure already kills
- state precisely what would count as a genuine gain on the bad coefficient
- front-load the Tao gate so we do not chase pressure-side ideas that averaged NS would also preserve

## Required Deliverables

By the end of this step, produce all of the following inside `RESULTS.md`:

1. **Formula sheet**
   - the exact far-field pressure pairing `I_p^far`
   - the role of the bad coefficient `C_far ~ ||u||_{L^2}^2 / r_k^3`
   - which pressure modes are already annihilated by the test structure
   - what quantity would actually need to become smaller for progress to occur

2. **Tao-gate memo**
   - a short list of candidate NS-specific ingredients that might matter for this pairing
   - for each one, whether Tao's averaged model plausibly destroys it
   - a verdict on whether the harmonic-tail branch survives the Tao filter in any nontrivial form

3. **Execution recommendation for Step 2**
   - either a narrow green-light for the remote-shell falsification model
   - or an immediate downgrade to the negative-result track if no real NS-specific ingredient survives

## Exploration Tasks

Use **2-3 explorations total** unless a kill condition fires early.

### Exploration A: Reconstruct the precise pressure obstruction

Tasks:
- Read the copied `vasseur-pressure` mission outputs and isolate the exact far-field pressure pairing that remains live.
- Identify which constant, affine, or other harmonic modes are already killed by the localization and test structure.
- Write the formula in a way that makes clear what the true operative coefficient is and where `O(E_0)` enters.

Success standard:
- We end with an explicit formula sheet, not a summary-level paraphrase.

### Exploration B: Tao filter on candidate structure

Tasks:
- Read Tao's 2016 averaged-NS obstruction at the level needed to distinguish preserved structure from destroyed structure.
- Test the most plausible pressure-relevant candidates only:
  - specific algebraic form of `u · ∇u`
  - pressure Hessian structure tied to `u_i u_j`
  - vorticity/strain geometry only if it directly touches the surviving far-field pairing
- Separate generic harmonic regularity facts from genuinely NS-specific ingredients.

Success standard:
- Each candidate gets a clear verdict: `survives Tao gate`, `fails Tao gate`, or `unclear but testable`.

### Exploration C: Optional synthesis or computation pass

Only run this if A and B leave a live candidate.

Tasks:
- Normalize notation across the prior pressure mission and the Tao filter.
- State exactly what Step 2's remote-shell falsification model must test.
- Rule out cosmetic gains that do not touch the actual coefficient.

Success standard:
- Step 2 begins from one sharply phrased test, not from a broad survey.

## Kill Conditions

Trigger an early negative conclusion for this step if either happens:

- no plausible NS-specific ingredient can be named for the surviving far-field pairing; or
- every apparent gain acts only on a mode or quantity the test structure already kills, or otherwise does not shrink the actual bad coefficient.

If either kill condition fires, count that as a successful obstruction result and write the strongest honest negative memo.

## Constraints

- Do **not** rerun broad De Giorgi or H^1-pressure searches; those are established background.
- Do **not** treat nicer harmonicity statements as progress unless they act on the surviving pairing itself.
- Do **not** move to the remote-shell model until the exact target quantity is pinned down and Tao-screened.
- Keep the work tightly tied to the existing `vasseur-pressure` mission and the copied mission files in this repository.

## Validation Requirements

- Every formula should be explicit enough that a later step can test it mechanically.
- Distinguish clearly between `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]` claims.
- Name the exact source files from the copied missions when pulling prior results.
- A sharp negative memo is a valid success state for this step.
