# Chain 02 - Obstruction-First Geometry Route

## Central Premise

NS-specific vortex geometry is still a live axis after the pressure-side loophole closed, but "geometry" is too broad to be a plan. This chain separates three different ideas:

- local Beltrami alignment (`u` nearly parallel to `omega`)
- vorticity-direction coherence (`xi = omega / |omega|`)
- vortex-tube persistence under the dynamics

It then asks the narrower question first: can any scale-appropriate local geometric observable on intense-vorticity regions control the full vortex-stretching mechanism, including the nonlocal remainder that usually survives?

## Verifiable Result Target

Either:

- a new scale-appropriate bridge from one specific geometric observable to a known regularity mechanism, together with a plausible persistence route; or
- a sharp negative result showing that local near-Beltrami or alignment observables do not by themselves control the full stretching mechanism and therefore are not operational regularity levers.

## Why This Chain Is Meaningfully Different

This is the only chain built around coherent structures and intense-vorticity geometry. It does not search for a better algebraic rewrite, a compactness theorem, or an eigenframe criterion.

## Ordered Steps

### Step 1 - Front-load the Tao and NS-specificity filter

- Depends on: none.
- Action: identify the exact ingredient this route would need that Tao's averaged model should destroy. Candidates include a true transport law for a geometric observable, an exact algebraic link from the observable to `S omega`, or a multiscale coherence mechanism for vortex structures.
- Expected output: a short memo stating which candidate ingredient is genuinely NS-specific and which are only generic singular-integral facts.
- Kill condition: if the route uses only Calderon-Zygmund geometry with no clearly NS-specific feature, stop immediately and mark the chain Tao-blocked.

### Step 2 - Separate the observables and enforce scaling discipline

- Depends on: Step 1.
- Action: define disjoint quantitative observables for:
  - local Beltrami deficit,
  - vorticity-direction regularity,
  - tube coherence or persistence.
- Action: require each observable to be scale-invariant or explicitly scale-critical, then test whether any route from Beltrami deficit to an existing criterion already passes through `nabla xi` control or another strictly stronger assumption.
- Expected output: a table of observables, their scaling, the criteria they could feed, and the first obstruction for each proposed bridge.
- Kill condition: if every path from local Beltrami deficit to a known criterion requires stronger derivative control than the observable itself provides, terminate with that obstruction.

### Step 3 - Attack the full stretching term, not just the local-looking piece

- Depends on: Step 2.
- Action: decompose the stretching quantity `S omega . omega` into self-induced and nonlocal remainder pieces, or into intense-set and exterior contributions, and test whether the chosen observable controls the full expression or only a local fragment.
- Expected output: a lemma sheet or obstruction memo identifying exactly which portion of stretching is controlled and which portion remains free.
- Kill condition: if the only gain is on `u x omega` or another local/self-induced piece while the decisive nonlocal remainder stays scale-critical, stop and record that local geometric depletion is insufficient.

### Step 4 - Test dynamic persistence near a singular scenario

- Depends on: Step 3.
- Action: if a plausible bridge survives, ask whether the required observable can persist up to a hypothetical singular time. Demand an explicit transport identity, coercive quantity, or multiscale persistence mechanism.
- Expected output: a persistence memo stating either a plausible propagation route or a precise impossibility point.
- Kill condition: if persistence requires assumptions stronger than the known geometric criteria, or if the complement of the intense-vorticity set still dominates the critical nonlocal term, terminate with that obstruction.

### Step 5 - Close with a strict outcome standard

- Depends on: Step 4, or directly on Step 3 if the chain dies there.
- Action: upgrade the chain to a conditional regularity statement only if there is:
  - a new implication from one clearly defined observable to a known regularity mechanism,
  - a scale-appropriate hypothesis,
  - and a plausible persistence route under NS.
- Expected output: either a new conditional proposition with exact missing ingredients or a polished fragility memo explaining why local near-Beltrami geometry is descriptive rather than operational.
- Kill condition: if the final output is only a rephrased known criterion, a supercritical hypothesis, or an argument that never controls the nonlocal remainder, classify the chain as negative.
