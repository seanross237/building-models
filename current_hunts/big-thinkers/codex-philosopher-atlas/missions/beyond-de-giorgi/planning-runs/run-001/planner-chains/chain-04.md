# Chain 04 - Critical Element / Concentration-Compactness

## Central Premise

If regularity fails, the right object may be a minimal blowup profile rather than a sharper local estimate. Kenig-Merle style arguments succeed when one can extract a critical element and then rule it out by rigidity. This chain tests how far current NS profile-decomposition machinery can be pushed and whether any rigidity ingredient survives Tao's averaged-model obstruction.

## Verifiable Result Target

Either:

- a concrete critical-element program for NS with one viable rigidity lever, or
- an obstruction map explaining exactly why the supercritical gap still prevents a Kenig-Merle route here.

## Why This Chain Is Meaningfully Different

This is the only chain that starts from the blowup hypothesis and works globally through compactness and rigidity. It is not based on local estimates, geometry of a chosen region, or algebraic reformulation of the nonlinear term.

## Ordered Steps

### Step 1 - Audit the compactness machinery

- Depends on: none.
- Action: map the existing NS profile-decomposition and critical-space literature, with emphasis on Gallagher-Koch-Planchon type partial results and the exact function spaces where compactness modulo symmetries is available.
- Expected output: a landscape note naming the best candidate phase space and the precise theorem stack already in hand.
- Kill condition: if no phase space offers both the needed profile decomposition and a plausible blowup extraction setup, terminate with a compactness obstruction memo.

### Step 2 - Build the minimal-counterexample package

- Depends on: Step 1.
- Action: formulate the hypothetical minimal blowup object, normalize the symmetries, and list the candidate NS-specific rigidity quantities that could distinguish real NS from Tao's averaged model.
- Expected output: a critical-element dossier spelling out assumptions, invariances, compactness claims, and candidate rigidity handles.
- Kill condition: if the setup itself already fails because the minimal element cannot be extracted in the chosen space, stop and record that failure precisely.

### Step 3 - Stress-test one rigidity route

- Depends on: Step 2.
- Action: choose one route, such as backward uniqueness, a Liouville theorem, exclusion of self-similar concentration, or a Lamb-vector concentration law, and test whether it uses more than energy plus harmonic analysis.
- Expected output: a route memo with the required lemmas, known precedents, and the first genuinely missing ingredient.
- Kill condition: if every available rigidity route reduces to Tao-preserved structure, stop and write that as the core obstruction.

### Step 4 - Apply the Tao filter and close the chain

- Depends on: Step 3, or directly on Step 2 if the chain dies there.
- Action: compare the extracted critical-element story with Tao's averaged equation and identify whether any surviving rigidity ingredient is truly NS-specific.
- Expected output: a final memo with either a viable compactness program or a negative result explaining why concentration-compactness cannot currently escape the averaged-model barrier.
- Kill condition: if no NS-specific rigidity survives the comparison, close the chain as Tao-blocked.
