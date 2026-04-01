# Refined Chain 03 - Obstruction-First Geometry Route

## Central Premise

NS-specific vortex geometry is still a live axis after the De Giorgi route stalls, but the original chain bundled together three distinct ideas:

- local Beltrami alignment (`u` nearly parallel to `omega`)
- vorticity-direction coherence (`xi = omega / |omega|`)
- vortex-tube persistence under the dynamics

The refined chain separates them and asks a narrower question first: can any scale-appropriate local geometric observable on intense-vorticity regions control the full vortex-stretching mechanism, including nonlocal exterior contributions? If not, the right output is a rigorous fragility memo, not a recycled conditional criterion.

## Verifiable Result Target

Either:

- a genuinely new scale-appropriate bridge from one specific geometric observable to a known regularity mechanism, together with a plausible persistence route, or
- a sharp negative result showing that local near-Beltrami geometry on high-`|omega|` sets cannot by itself control the full stretching mechanism and therefore is not an operational regularity lever.

## Why This Chain Is Meaningfully Different

This version is not a broad "geometry might help" program. It is an obstruction-first test that:

- separates the candidate mechanisms instead of conflating them
- treats nonlocal strain as the main enemy
- demands scale-appropriate observables
- uses the Tao filter at the front rather than the back

## Ordered Steps

### Step 1 - Front-load the Tao/NS-specific filter

- Depends on: none.
- Action: identify the exact ingredient this route would need that the averaged model should destroy. Candidates include a genuinely NS-specific transport identity, an algebraic link from a geometric observable to `S omega`, or a rigorous persistence mechanism for coherent structures across scales.
- Expected output: a short memo stating which putative ingredient is NS-specific and which are only generic singular-integral facts.
- Kill condition: if the route uses only generic Calderon-Zygmund geometry and no clearly NS-specific feature, stop and mark the chain Tao-blocked.

### Step 2 - Separate the observables and enforce scaling discipline

- Depends on: Step 1.
- Action: define disjoint quantitative observables for:
  - local Beltrami deficit
  - vorticity-direction regularity
  - tube coherence or persistence
  Require each observable to be scale-invariant or explicitly scale-critical. Then test whether any route from Beltrami deficit to an existing criterion already passes through derivative control of `xi` or an equivalently stronger assumption.
- Expected output: a table of observables, their scaling, the regularity criteria they could feed, and the first obstruction for each proposed bridge.
- Kill condition: if every path from local Beltrami deficit to a known criterion requires `nabla xi`-type control or another stronger hypothesis, terminate with that obstruction.

### Step 3 - Attack the full stretching term, not the Lamb vector

- Depends on: Step 2.
- Action: decompose the stretching quantity `S omega . omega` into contributions from the intense-vorticity set and from the exterior field, or equivalently into local/self-induced and nonlocal remainder pieces. Test whether small Beltrami deficit on high-`|omega|` regions controls the full stretching term or only a local piece.
- Expected output: a lemma sheet or obstruction memo identifying exactly which portion of stretching is controlled and which portion remains free.
- Kill condition: if the only gain is on `u x omega` or on a local/self-induced part of stretching while the nonlocal remainder stays scale-critical, stop and record that local Beltrami depletion is insufficient.

### Step 4 - Test dynamic persistence near a singular scenario

- Depends on: Step 3.
- Action: if any plausible bridge survives, ask whether the needed observable can persist up to a hypothetical singular time. Demand an explicit transport identity, coercive quantity, or multiscale persistence mechanism. Also check whether geometry outside the intense-vorticity set still enters the critical integral quantities.
- Expected output: a persistence memo stating either a plausible propagation route or a precise impossibility point.
- Kill condition: if persistence requires stronger assumptions than existing geometric criteria, or if the complement of the intense set still dominates the relevant nonlocal term, terminate with that obstruction.

### Step 5 - Close with a strict outcome standard

- Depends on: Step 4, or directly on Step 3 if the chain dies there.
- Action: upgrade the chain to a conditional regularity statement only if there is:
  - a new implication from one clearly defined observable to a known regularity mechanism
  - a hypothesis that is scale-appropriate
  - a plausible persistence route under NS
  Otherwise produce a sharp fragility memo explaining why local near-Beltrami geometry is descriptive rather than operational.
- Expected output: either a genuinely new conditional proposition with exact missing ingredients, or a polished negative result for final comparison.
- Kill condition: if the final output is only a rephrased known criterion, a supercritical hypothesis, or an argument that does not control the nonlocal remainder, classify the chain as negative.
