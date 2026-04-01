# Chain 05 - Strain-Pressure Eigenstructure

## Central Premise

The exact tensor identities of NS may contain information that averaged quadratic models do not retain at the same level. The key objects are the strain tensor, the pressure Hessian, and the vorticity-stretching identity `omega . grad u = S omega`. This chain tests whether eigenframe dynamics or sign structure in these tensors yields a usable rigidity or conditional criterion.

## Verifiable Result Target

Either:

- a conditional criterion or falsifiable conjecture phrased in strain-pressure eigenstructure, or
- a clear obstruction note showing that the exact tensor identities are still too nonlocal to beat Tao's filter.

## Why This Chain Is Meaningfully Different

This chain is tensorial rather than geometric or compactness-based. It does not assume vortex tubes and does not hunt for a new commutator; it asks whether the exact NS tensor algebra itself is the missing structural property.

## Ordered Steps

### Step 1 - Compile the exact tensor identities

- Depends on: none.
- Action: assemble the pointwise and transport identities linking strain, pressure Hessian, and vorticity stretching, and separate what is exact NS structure from what is merely Calderon-Zygmund repackaging.
- Expected output: a tensor-identity sheet marking which formulas are exact, which are nonlocal, and which appear specific to the true NS nonlinearity.
- Kill condition: if all candidate identities immediately collapse to generic harmonic-analysis statements with no sharper content, stop and record that collapse.

### Step 2 - Search for eigenframe-level control

- Depends on: Step 1.
- Action: examine eigenvalue and eigenvector dynamics for the strain tensor and pressure Hessian, looking for sign patterns, depletion scenarios, or monotone quantities on regions of strong strain.
- Expected output: a shortlist of candidate tensor inequalities or invariants, each with a note on whether it is conditionally plausible.
- Kill condition: if pressure-Hessian nonlocality prevents even conditional sign control in every natural formulation, terminate with a nonlocality obstruction memo.

### Step 3 - Build one concrete criterion

- Depends on: Step 2.
- Action: choose the strongest surviving tensor statement and turn it into a conditional regularity criterion, reduced ODE model, or falsifiable conjecture about blowup geometry.
- Expected output: a draft proposition or conjecture with proof skeleton and a list of the exact missing lemmas.
- Kill condition: if the criterion is just a restatement of a known open condition with no new leverage, stop and write that as the failure mode.

### Step 4 - Apply the Tao filter and close the chain

- Depends on: Step 3, or directly on Step 2 if the chain dies there.
- Action: check whether the surviving tensor mechanism uses exact NS identities that Tao's averaged bilinear operator destroys, rather than norms and estimates it preserves.
- Expected output: a final memo with either a tensor-structure attack path or a negative result explaining why strain-pressure eigenstructure still does not separate NS from averaged NS.
- Kill condition: if the same mechanism survives in the averaged model, close the chain as Tao-blocked.
