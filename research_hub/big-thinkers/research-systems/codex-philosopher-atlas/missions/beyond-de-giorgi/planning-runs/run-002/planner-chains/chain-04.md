# Chain 04 - Strain-Pressure Eigenstructure

## Central Premise

The exact tensor identities of NS may carry information that scalar norm estimates erase. The key objects are the strain tensor `S`, the pressure Hessian `nabla^2 p`, and the stretching identity `omega . nabla u = S omega`. This chain tests whether eigenframe dynamics, sign structure, or tensor-level depletion yields a usable rigidity or conditional regularity lever that Tao's averaged operator would not preserve.

## Verifiable Result Target

Either:

- a conditional criterion, reduced dynamical model, or falsifiable conjecture phrased in strain-pressure eigenstructure; or
- a clear obstruction note showing that the exact tensor identities remain too nonlocal or too weak to separate NS from averaged NS in an operational way.

## Why This Chain Is Meaningfully Different

This chain is tensorial rather than geometric or compactness-based. It does not assume vortex tubes, and it does not search for a better nonlinear rewrite of the whole equation. It asks whether the exact local tensor algebra is itself the missing structural property.

## Ordered Steps

### Step 1 - Compile the exact tensor identities and front-load the Tao screen

- Depends on: none.
- Action: assemble the pointwise and transport identities linking `S`, `nabla^2 p`, and `omega`, and separate formulas that are exact NS structure from formulas that are only Calderon-Zygmund repackaging.
- Expected output: a tensor-identity sheet marking which statements are exact, which are nonlocal, and which appear genuinely tied to the true NS bilinear form.
- Kill condition: if all candidate identities immediately collapse to generic singular-integral statements with no sharper structural content, stop and record that collapse.

### Step 2 - Search for eigenframe-level control with scaling discipline

- Depends on: Step 1.
- Action: examine eigenvalue and eigenvector dynamics for `S` and `nabla^2 p`, looking for scale-appropriate sign patterns, eigenvalue gaps, alignment scenarios, or monotone quantities on regions of strong strain.
- Expected output: a shortlist of candidate tensor statements or invariants, each with a note on scaling, plausibility, and how it would feed a regularity mechanism.
- Kill condition: if pressure-Hessian nonlocality prevents even conditional sign or eigenframe control in every natural formulation, terminate with a nonlocality obstruction memo.

### Step 3 - Test whether any candidate controls the full stretching mechanism

- Depends on: Step 2.
- Action: pick the strongest candidate and check whether it controls the full `S omega . omega` term or only a local or self-induced piece. Treat the nonlocal pressure contribution as the main adversary.
- Expected output: a lemma sheet or obstruction memo identifying exactly what part of stretching is controlled and what remains free.
- Kill condition: if the candidate only repackages a known open condition or leaves the decisive nonlocal remainder untouched, stop and record that failure.

### Step 4 - Build one concrete criterion or reduced model

- Depends on: Step 3.
- Action: turn the best surviving tensor statement into a conditional regularity criterion, a reduced eigenframe ODE model, or a falsifiable conjecture about blowup geometry.
- Expected output: a draft proposition or conjecture with explicit assumptions, the exact missing lemma, and the reason the claim is not just a restatement of a known criterion.
- Kill condition: if the resulting statement is merely a renamed version of an existing open condition with no new leverage, narrow the output to an obstruction memo.

### Step 5 - Close with a strict NS-specificity check

- Depends on: Step 4, or directly on Step 3 if the chain dies there.
- Action: test whether the surviving mechanism uses exact NS tensor structure that Tao's averaged bilinear operator destroys, rather than only norm bounds and generic elliptic facts.
- Expected output: either a tensor-structure attack path with a named next theorem target or a negative result explaining why strain-pressure eigenstructure still does not operationally separate NS from averaged NS.
- Kill condition: if the same mechanism survives in the averaged model at the same level of strength, close the chain as Tao-blocked.
