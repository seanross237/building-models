# Refined Chain 01 - Harmonic Tail Obstruction Test with Early Tao Gate

## Central Premise

The useful question is not whether harmonicity makes `p_far` smoother. That is already clear. The real question is whether any local quantity governing the surviving far-field pressure pairing can make the bad coefficient

`C_far ~ ||u||_{L^2}^2 / r_k^3`

smaller from admissible NS data, using an NS-specific ingredient that Tao's averaged model does not preserve.

If not, the chain should close quickly with a sharp obstruction memo.

## Verifiable Result Target

Either:

- a concrete NS-specific mechanism that converts local harmonic-tail structure into coefficient smallness or summable decay stronger than a fixed `O(E_0)` bound, or
- a negative result showing, by explicit shell-source model plus analytic argument, that local harmonicity alone cannot improve the bad coefficient in a Tao-relevant way.

## Why This Chain Is Still Worth Running

The prior pressure mission left the harmonic-tail loophole explicitly open. This refined chain treats that loophole as a falsifiable cleanup target, not as an open-ended search for a better pressure estimate.

## Gatekeeping Requirement

Before the chain is allowed to continue past the opening step, it must satisfy all three conditions below:

- the candidate quantity acts on the actual pressure pairing after removing any constant or affine modes already killed by the test structure;
- the hoped-for gain would reduce the bad coefficient itself, not just restate `O(E_0)` in smoother language;
- the route names an NS-specific ingredient beyond generic harmonic interior regularity.

If these conditions cannot be met, the chain downgrades immediately to a negative-result track.

## Ordered Steps

### Step 1 - Reconstruct the exact obstruction and apply the Tao gate

- Depends on: none.
- Action: rebuild the exact far-field pressure pairing from `vasseur-pressure`, identify which harmonic modes survive the test structure, isolate the precise quantity whose smallness matters, and state a candidate NS-specific ingredient if one exists.
- Expected output: a formula sheet containing `I_p^far`, the role of `C_far`, the surviving modes, and a one-page Tao-gate note.
- Kill condition: if no plausible NS-specific ingredient can be named by the end of this step, move directly onto the negative-result track.

### Step 2 - Run an explicit remote-shell falsification model

- Depends on: Step 1.
- Action: choose a remote shell source with admissible energy, compute the induced harmonic field or harmonic polynomial on the inner cylinder, and test the actual surviving quantity from Step 1.
- Expected output: a countermodel memo showing whether the interior quantity remains comparable to shell energy.
- Kill condition: if the model already forces the relevant local quantity to stay `O(E_0)`, close the positive route unless a clearly NS-specific cancellation survives the model.

### Step 3 - Test only a short list of pressure-relevant local quantities

- Depends on: Step 2 surviving.
- Action: examine only tightly justified candidates such as oscillation after quotienting out killed modes, derivative decay, harmonic polynomial remainder, or another explicitly motivated quantity. Do not run a broad norm survey, and do not rely on raw Harnack positivity.
- Expected output: a short estimate table recording exactly where annular or local data enters and whether any candidate beats fixed-coefficient control.
- Kill condition: if every candidate simply propagates boundary size as `O(E_0)`, stop and write the obstruction memo.

### Step 4 - Convert any surviving gain into a non-recursive quantitative criterion

- Depends on: Step 3.
- Action: if a candidate survives, translate it into a criterion that directly shrinks `C_far` or yields summable decay from admissible NS data, without silently rebuilding the exhausted De Giorgi architecture.
- Expected output: a conditional proposition with explicit quantitative gain, assumptions, and proof skeleton.
- Kill condition: if the gain does not reduce the bad coefficient, or only feeds back into the same missing `W^{1,3}`-type input or threshold recursion, record structural failure.

### Step 5 - Final NS-specificity check and chain closure

- Depends on: Step 4, or directly on an earlier kill.
- Action: test whether the surviving mechanism truly uses the NS-specific ingredient named in Step 1 rather than generic elliptic harmonicity.
- Expected output: a final route memo with one of two outcomes:
  - a narrowly specified NS-specific attack path, or
  - a negative result stating that the harmonic-tail loophole is Tao-compatible and therefore not a beyond-De-Giorgi escape.
- Kill condition: if the mechanism survives unchanged in Tao's averaged setting, close the chain negatively.

## Probability Assessment

Probability that this refined chain yields a presentable result: **0.78**

Most of that probability lies on a clean obstruction memo rather than a positive attack path.
