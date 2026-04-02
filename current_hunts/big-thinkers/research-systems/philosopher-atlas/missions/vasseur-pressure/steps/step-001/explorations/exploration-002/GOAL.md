# Exploration 002: Pressure Term Dissection in De Giorgi Energy Inequality

## Goal

Perform a detailed dissection of the De Giorgi energy inequality in the Vasseur/Caffarelli-Vasseur framework for Navier-Stokes equations. Identify exactly where the pressure exponent beta = 4/3 arises, trace the chain of inequalities that produce it, and compare with the pressure-free drift-diffusion case where De Giorgi succeeds fully.

## Context

The incompressible Navier-Stokes equations in R^3 (or T^3):
  partial_t u + (u cdot nabla) u + nabla p = Delta u
  div u = 0

**Vasseur (2007)** applied De Giorgi iteration to NS, obtaining partial regularity. The method works by:
1. Defining super-level set energies U_k = integral (|u| - C_k)_+^2 phi_k^2 dx
2. Deriving an energy inequality relating U_{k+1} to U_k
3. Attempting to close a recursive estimate U_{k+1} <= C * 2^{k*alpha} * U_k^{1+delta} for some delta > 0
4. If closed, U_k -> 0 and |u| is bounded

The pressure term in the energy inequality requires p in L^beta for the iteration to close. Currently beta = 4/3 is achieved. Full regularity needs beta > 3/2.

**Caffarelli-Vasseur (2010)** applied the same De Giorgi framework to drift-diffusion (no pressure term) and reached criticality. This is the comparison case.

## Specific Tasks

### Task 1: Write Out the Full De Giorgi Energy Inequality

Starting from the NS equations, derive the energy inequality for the truncated quantities. Show ALL terms:

1. **Dissipation term:** -integral |nabla (u - C_k)_+|^2 phi_k^2 dx  (favorable, absorbed)
2. **Nonlinear transport term:** integral from (u cdot nabla u) paired with test function — trace how div-free condition helps
3. **Pressure term:** integral p * div(test function) — this is the problematic term. The test function involves the cutoff phi_k, so div(phi_k * ...) != 0.
4. **Commutator/cutoff corrections:** Terms involving nabla phi_k from product rule

For each term, state:
- The exact expression
- Which function space estimate is used (Holder, Sobolev, CZ, interpolation)
- What exponent it contributes to the final recursion

### Task 2: Trace the Chain Producing beta = 4/3

For the pressure term specifically:
1. p = (-Delta)^{-1} div div (u otimes u) by Leray projection. Since u in L^{3,infinity} (critical), Calderon-Zygmund gives p in L^{3/2, infinity}.
2. But the De Giorgi iteration needs p localized on the support of phi_k. Write the localized pressure estimate.
3. The pairing integral p * (term involving phi_k) is estimated via Holder: ||p||_{L^beta} * ||other||_{L^{beta'}}.
4. Trace which value of beta makes the recursion close. Show that beta = 4/3 works but beta < 4/3 does not.
5. Show that beta > 3/2 would be sufficient for the full recursion to close (U_k -> 0).

**Annotated inequality chain required:** Write it as:
  A --[inequality name, exponents]--> B --[inequality name, exponents]--> C --> ... --> beta = 4/3

### Task 3: Caffarelli-Vasseur Comparison

In the drift-diffusion equation (theta_t + u cdot nabla theta = -(-Delta)^alpha theta with div u = 0):
- There is no pressure term
- De Giorgi iteration closes at criticality (alpha = 1/2 in 2D, or the appropriate critical exponent)

Map term by term:
| Term | Drift-diffusion estimate | NS estimate | Difference |
|------|------------------------|-------------|------------|
| Dissipation | ... | ... | Same? |
| Transport | ... | ... | Same? |
| Pressure | ABSENT | ... | THIS IS THE GAP |
| Cutoff corrections | ... | ... | Worse? |

For the transport term in drift-diffusion, the div-free condition allows integration by parts that eliminates a derivative. In NS, the same trick partially works but leaves the pressure behind. Document this precisely.

### Task 4: Bogovskii Corrector Scaling

When localizing the pressure via cutoff phi_k, one approach is the Bogovskii operator: find a corrector w_k such that div(phi_k u - w_k) = 0. Then the test function is divergence-free and the pressure term vanishes.

But the corrector w_k costs something. Compute:
1. w_k is supported on the annulus A_k = {x : dist(x, supp nabla phi_k) <= epsilon_k}
2. ||w_k||_{L^q} in terms of ||u cdot nabla phi_k||_{L^p} on A_k
3. The annulus A_k corresponds to {C_k <= |u| <= C_{k+1}} by the De Giorgi level sets. Use the measure estimate |{|u| > lambda}| <= C lambda^{-3} (from u in L^{3,infinity}) to estimate the measure of A_k.
4. Does ||w_k||_{L^q} grow faster than the De Giorgi energy U_k as k -> infinity? If yes, the corrector destroys the recursion. If no, it's manageable.

Compute this scaling explicitly. Use Python/Sympy if helpful for tracking exponents.

## Output Format

Your report should contain:

1. **The full De Giorgi energy inequality** with all terms labeled and estimates specified
2. **The annotated inequality chain** for the pressure term: ... --> beta = 4/3
3. **The comparison table** (drift-diffusion vs. NS, term by term)
4. **Bogovskii corrector scaling computation**
5. **Assessment:** Is the beta = 4/3 bottleneck from a single sharp inequality, or distributed across multiple estimates? Where should the H^1 route focus?

## Validation Requirements

- Every function space specified precisely (e.g., L^{4/3}(R^3), not just "L^p")
- Domain stated for every estimate (T^3 vs R^3 vs bounded)
- Tag every claim: [VERIFIED] (checked against published source), [COMPUTED] (you derived it), [CHECKED] (verified by computation), or [CONJECTURED]
- Partial results are valuable. If you can resolve 3 of 4 tasks, report what you have.

## Success Criteria

- Annotated inequality chain showing exactly which estimate forces beta = 4/3
- Clear identification of whether the bottleneck is a single sharp inequality or distributed
- Comparison table showing what pressure costs in the De Giorgi framework
- Bogovskii corrector scaling computed

## Failure Criteria

- Unable to reconstruct the De Giorgi energy inequality from Vasseur's framework
- Exponent tracking is inconsistent or dimensionally wrong
