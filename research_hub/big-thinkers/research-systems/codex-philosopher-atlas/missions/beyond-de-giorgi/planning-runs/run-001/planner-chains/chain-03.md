# Chain 03 - Geometric Vorticity Alignment and Local Beltrami Tubes

## Central Premise

Tao's averaged equation preserves energy and harmonic analysis but should destroy fine vortex geometry. Exact Beltrami alignment kills the Lamb-vector loss entirely, while Constantin-Fefferman type criteria show that vorticity geometry can control regularity without using De Giorgi. This chain tests whether local near-Beltrami structure on high-vorticity sets can be turned into a quantitative geometric criterion.

## Verifiable Result Target

Either:

- a conditional regularity statement or conjecture tying blowup exclusion to vorticity-direction regularity or local Beltrami deficit on intense-vorticity regions, or
- a sharp negative result showing that local Beltrami geometry is too fragile to buy any real depletion.

## Why This Chain Is Meaningfully Different

This is the only chain built around coherent structures and high-vorticity geometry. It does not seek a new norm inequality or a new compactness theorem.

## Ordered Steps

### Step 1 - Fix the geometric observables

- Depends on: none.
- Action: synthesize Constantin-Fefferman style criteria and define the quantitative observables this mission cares about: vorticity-direction modulus, local Beltrami deficit, and concentration of the high-`|omega|` set.
- Expected output: a geometry memo with precise candidate observables and the known threshold statements they would need to feed.
- Kill condition: if the known geometric criteria are too nonlocal or too strong to connect to any local Beltrami quantity, stop and write that mismatch down explicitly.

### Step 2 - Quantify depletion from local Beltrami structure

- Depends on: Step 1.
- Action: derive how small local Beltrami deficit on high-vorticity regions affects vortex stretching or pressure-loss terms, using the established exact-Beltrami cancellation as the anchor case.
- Expected output: a lemma sheet translating local alignment assumptions into quantitative depletion estimates.
- Kill condition: if any useful gain requires essentially global alignment, or if the local deficit does not control the stretching term in a scalable way, terminate with a fragility result.

### Step 3 - Bridge the geometry to a regularity statement

- Depends on: Step 2.
- Action: formulate a conditional criterion of the form "if alignment or deficit stays controlled on the intense-vorticity set, blowup is excluded," and identify the exact missing lemma required to prove it.
- Expected output: a draft conditional proposition or a sharply stated conjecture with proof skeleton.
- Kill condition: if the bridge still demands an unproved global tube-persistence statement or a norm assumption stronger than current criteria, write that as the obstruction and stop.

### Step 4 - Apply the Tao filter and close the chain

- Depends on: Step 3, or directly on Step 2 if the chain dies there.
- Action: determine which part of the argument genuinely uses NS-specific geometry that averaging destroys: tube coherence, alignment transport, or exact `S omega` coupling.
- Expected output: a final memo with either a geometry-first attack path or a negative result showing that local Beltrami geometry is too fragile or too non-distinguishing.
- Kill condition: if the same criterion can hold verbatim for the averaged model, close the chain as Tao-blocked.
