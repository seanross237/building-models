# Chain 02 - SQG-Type Cancellation via Lamb Vector Reformulation

## Central Premise

SQG succeeds because the nonlinear coupling can be rewritten into a first-order commutator structure. NS fails in the usual formulation because truncation breaks divergence-free structure and the quadratic pressure term only gives Calderon-Zygmund consolidation. This chain asks whether a reformulation around the Lamb vector, vorticity transport, or Helmholtz projection reveals a hidden NS cancellation that is invisible in velocity-pressure form.

## Verifiable Result Target

Either:

- a concrete reformulation in which the nonlinear interaction behaves like a first-order cancellation rather than a second-order CZ loss, or
- a clean obstruction note proving that no SQG-style commutator analogue survives the NS vector geometry.

## Why This Chain Is Meaningfully Different

This is the only chain whose core question is "can the nonlinear interaction itself be reformulated into a better mechanism?" It is not a localization chain, not a geometry chain, and not a compactness chain.

## Ordered Steps

### Step 1 - Audit the SQG mechanism against NS formulations

- Depends on: none.
- Action: write a side-by-side comparison of the SQG regularity mechanism and the NS nonlinearity in velocity, vorticity, Lamb-vector, and Helmholtz-projected forms.
- Expected output: a comparison matrix identifying which exact SQG advantages are missing in NS and listing candidate substitute identities.
- Kill condition: if no candidate identity survives truncation or localization even formally, stop and record that the SQG blueprint has no transferable NS slot.

### Step 2 - Test candidate reformulations algebraically

- Depends on: Step 1.
- Action: compute the best candidate rewrites, such as `u . grad u = grad(|u|^2 / 2) - u x omega`, projected transport forms, or commutators involving the Lamb vector, and check whether any one turns the quadratic interaction into a gain-bearing bilinear object.
- Expected output: an algebraic memo with explicit formulas, scale counting, and a verdict on whether any first-order cancellation actually appears.
- Kill condition: if every reformulation still collapses to second-order CZ structure or immediately reintroduces the vector-divergence obstruction, terminate with an obstruction memo.

### Step 3 - Build a pilot inequality on the best candidate

- Depends on: Step 2.
- Action: derive one test energy inequality for the surviving object, then stress-test it on exact Beltrami flows and on small perturbations away from Beltrami alignment.
- Expected output: a pilot inequality plus a perturbation verdict showing whether the gain is robust or infinitely fragile.
- Kill condition: if the gain disappears under arbitrarily small non-Beltrami perturbations, record that the candidate is structurally nongeneric and stop.

### Step 4 - Apply the Tao filter and close the chain

- Depends on: Step 3, or directly on Step 2 if the chain dies there.
- Action: decide whether the surviving cancellation uses the exact algebraic form of the NS nonlinearity in a way Tao's averaged operator destroys.
- Expected output: a final memo with either a concrete reformulation target for future work or a negative result stating that NS has no SQG-type first-order cancellation in any natural formulation tested here.
- Kill condition: if the mechanism is preserved by the averaged model at the same level of strength, close the chain as Tao-blocked.
