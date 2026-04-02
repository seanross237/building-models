# Chain 03 - Critical-Element Audit with Decoupled Formulation and Explicit Rigidity Tests

## Central Premise

Concentration-compactness should stay in play only if it can first produce a
non-circular Navier-Stokes minimal-element framework in some candidate critical
space. The refined chain therefore separates threshold formulation from rigidity
and treats the Tao barrier as an operational screen rather than a rhetorical
warning.

## Verifiable Result Target

Either:

- a narrowly scoped critical-element program in one candidate space with one
  rigidity route whose missing input is materially smaller than a renamed global
  regularity statement; or
- a calibrated obstruction map showing exactly where the program fails:
  threshold functional, compactness modulo symmetries, coercive backbone, or
  NS-specific rigidity.

## Why This Chain Is Still Worth Keeping

This is not a novel mathematical template, but it is still a useful planning
branch because it audits the global compactness-and-rigidity route directly. Its
value is not originality. Its value is disciplined calibration.

## Ordered Steps

### Step 1 - Rank candidate spaces by minimal-element feasibility, not by premature rigidity

- Depends on: none.
- Action: compare `L^3`, `\dot H^{1/2}`, and at most one weaker candidate such
  as `BMO^{-1}` only if a replacement compactness structure is stated
  explicitly.
- Action: for each space, specify the threshold quantity, solution class,
  perturbation theory, relevant symmetry group, and whether compactness modulo
  scaling and spatial translation can be formulated cleanly.
- Action: state separately whether time translation is part of the compactness
  picture and what maximal-lifespan notion is being used.
- Expected output: a candidate-space memo ranking spaces by non-circular
  threshold-formulation feasibility, with a separate note on later rigidity
  prospects.
- Kill condition: terminate only if no candidate space supports a clean
  threshold formulation with plausible compactness modulo the relevant
  symmetries.

### Step 2 - Build the threshold framework explicitly

- Depends on: Step 1.
- Action: in the top-ranked space, define the minimization quantity, maximal-
  lifespan solution class, symmetry normalization, pressure handling, and the
  exact meaning of "almost periodic modulo symmetries."
- Action: distinguish clearly between formal formulation, known perturbative
  input, and the compactness statement that would actually be needed.
- Expected output: a threshold dossier listing what is available, what is
  missing, and which missing piece is first-order rather than cosmetic.
- Kill condition: if the needed compactness or perturbation statement is absent
  in a way that is effectively as hard as solving the regularity problem in the
  chosen framework, stop and record that as a foundational obstruction.

### Step 3 - Audit the coercive backbone and the supercritical gap

- Depends on: Step 2.
- Action: identify what scale-invariant coercive quantity, monotonicity
  principle, or substitute structure would control a threshold object in the
  chosen space.
- Action: test whether current Navier-Stokes tools provide any backbone
  stronger than generic energy bounds plus harmonic analysis.
- Expected output: a coercive-structure memo naming the first indispensable
  missing control and why it matters for a critical-element program.
- Kill condition: if no credible backbone exists even for a hypothetical
  threshold element, conclude that concentration-compactness lacks the analogue
  that powers successful critical-element arguments elsewhere.

### Step 4 - Run an operational Tao screen on representative rigidity routes

- Depends on: Steps 2 and 3.
- Action: test at least two representative rigidity routes, not just one. One
  should be analytic, such as backward uniqueness or ancient-solution
  exclusion. One should be geometric or self-similar.
- Action: for each route, name the exact NS-specific input claimed to do work,
  explain why Tao-style averaged or toy models would or would not preserve it,
  and record the regularity or decay assumptions the route actually needs.
- Expected output: a rigidity audit table with route, NS-specific ingredient,
  dependence on stronger hypotheses, and first missing theorem.
- Kill condition: if every route either needs assumptions stronger than a
  generic critical element supplies or relies only on structure that Tao-style
  obstruction models plausibly preserve, stop with a route-specific obstruction
  memo.

### Step 5 - Promote only a non-circular survivor into a contradiction blueprint

- Depends on: Step 4.
- Action: only if one route genuinely survives, write the contradiction program
  from threshold element to exclusion in one chosen space.
- Action: benchmark the key missing theorem against known literature and ask
  explicitly whether it is materially narrower than a disguised global-
  regularity claim.
- Expected output: a contradiction blueprint with one phase space, one rigidity
  route, one bottleneck, and one explicit next theorem target.
- Kill condition: if the bottleneck is equivalent in difficulty to proving the
  original regularity problem or critical-space exclusion outright, downgrade
  the result back to obstruction.

### Step 6 - Close with a calibrated claim

- Depends on: Step 5, or directly on Step 4 or Step 3 if the chain dies
  earlier.
- Action: make the final claim no broader than the audited coverage.
- Expected output: either a limited positive program in one space and one route,
  or an obstruction map specifying whether failure came from threshold
  formulation, compactness, missing coercive structure, or rigidity.
- Kill condition: if the conclusion generalizes beyond the spaces and routes
  actually tested without a representative meta-argument, narrow it.

## Probability Assessment

- Probability this refined chain yields a presentable result: **0.74**
- Most likely presentable result: a calibrated obstruction map.
- Less likely presentable result: a genuinely actionable contradiction program.
