# Task 002: Vasseur De Giorgi Framework — Mathematical Analysis and Computation Spec

## Mission Context

We are investigating the Vasseur pressure exponent gap in Navier-Stokes regularity theory. Vasseur (2007) proved partial regularity of 3D NS solutions using De Giorgi iteration — a PDE technique that controls the size of super-level sets of |u|. The key obstruction to full regularity is a pressure term in the energy inequality at each De Giorgi level. Vasseur showed this term achieves exponent beta = 4/3 using standard Calderón-Zygmund (CZ) theory, but beta > 3/2 would imply full regularity. The gap 4/3 → 3/2 is the entire obstruction.

We have a validated pseudospectral DNS solver producing velocity and pressure fields on T³. **Before we can measure beta_effective from DNS data, we need to know exactly WHAT to compute.** That is the purpose of this task.

## Objective

Analyze Vasseur (2007) to extract the precise mathematical formulas needed to compute De Giorgi iteration quantities from DNS data, and specify how to measure the effective pressure exponent beta_effective. Produce a complete computational specification that a code worker can implement.

## Success Criteria

1. **Identify the De Giorgi truncation scheme**: What are the truncation levels {C_k}? What is the truncation function? How are the super-level sets A_k defined?

2. **Write the energy inequality at level k**: The De Giorgi method derives a recursive energy inequality. Write it explicitly, identifying:
   - The "energy" at level k: E_k = ∫ |u_k|² φ² dx (or whatever Vasseur uses)
   - The viscous/dissipation term
   - The pressure term (THE critical one)
   - The nonlinear/transport term
   - Any cut-off function φ and how it enters

3. **Identify the pressure term precisely**: This is the most important deliverable. The pressure term in the De Giorgi energy inequality has a specific form. Write it as an explicit integral involving p, u, and the truncation. Show exactly where the CZ estimate is applied and where the exponent beta = 4/3 comes from.

4. **Derive the formula for beta_effective**: Given DNS data (velocity field u(x,t), pressure field p(x,t)), specify:
   - How to choose the truncation levels C_k
   - How to compute the super-level set measure |A_k|
   - How to compute the pressure contribution at level k
   - How to fit/extract beta_effective from the scaling of these quantities

5. **Explain where beta > 3/2 would be sufficient**: Why does Vasseur need beta > 3/2 specifically? What fails at beta = 4/3? Write the recursive inequality and show how the iteration converges/fails.

6. **Check Vasseur's Conjecture 14 / Appendix**: This is reportedly where Vasseur states that beta > 3/2 would suffice. Verify this claim and explain the logic.

7. **Survey how the CZ bound gives beta = 4/3**: The Calderón-Zygmund inequality gives ||p||_{L^{3/2}} ≤ C ||u ⊗ u||_{L^{3/2}}. Show how this gets used and why it limits beta to 4/3.

## Failure Criteria

- If you cannot access or find Vasseur (2007), try to reconstruct the argument from the De Giorgi iteration technique applied to NS. Clearly label reconstructed vs. cited material.
- If the De Giorgi scheme is fundamentally different from what the mission assumes, explain the actual structure.

## Relevant Context

### Vasseur (2007)
- Title: "A new proof of partial regularity of solutions to Navier-Stokes equations"
- arXiv: 0607.xxxx (search for it — may be 0607.5964 or similar)
- Key result: Alternative proof of Caffarelli-Kohn-Nirenberg partial regularity using De Giorgi iteration instead of the classical blow-up method
- The critical section: where the pressure term is estimated using CZ theory
- Conjecture 14 / Appendix: states that improved pressure estimate (beta > 3/2) would yield full regularity

### De Giorgi Iteration (General)
The De Giorgi technique works as follows:
1. Define truncation levels C_k → some limit C_∞ as k → ∞
2. Define truncated functions u_k = (|u| - C_k)_+ (or similar)
3. Derive an energy inequality for u_k that has the form:
   Y_k ≤ b^k Y_{k-1}^{1+δ}
   where Y_k measures the "energy" at level k
4. If the base growth rate and initial Y_0 satisfy a threshold condition, then Y_k → 0, which means |u| ≤ C_∞ a.e. (boundedness)
5. The exponent δ > 0 is where the pressure term's regularity enters
6. If β = 4/3, the De Giorgi exponent δ is not large enough for the iteration to close
7. If β > 3/2, the exponent δ becomes large enough

### CZ Inequality for Pressure
From Δp = -∂_i∂_j(u_i u_j), the CZ inequality gives:
||p||_{L^q} ≤ C_q ||u ⊗ u||_{L^q} for 1 < q < ∞

For NS, the natural choice is q = 3/2 (matching the Sobolev embedding H^1 → L^6 and L^2 data).
This gives β = 4/3 in Vasseur's scheme (the exact relationship between q and β should be determined).

### Tran-Yu (2014, AIHP)
- Claims that Galilean invariance improves the pressure estimate
- Uses De Giorgi iteration with frame-dependent quantities
- Should be checked for whether it actually achieves β > 4/3

### Prior DNS Results (Task 001)
Working solver at: `../task-001/code/ns_solver.py`
- Computes velocity u(x,t) and pressure p(x,t) on T³
- Outputs L^q pressure norms for q = 1, 3/2, 2, 3, ∞
- At Re=100 N=64: enstrophy peaks at t=5, energy conservation 1e-5
- At Re=1000: pressure L^{3/2} ≈ 3.0-3.5 (roughly constant) while enstrophy grows

## Approach Guidance

1. **Start with Vasseur (2007)**: Search for the paper online (arXiv or journal). Read the De Giorgi iteration sections carefully. Look for the energy inequality derivation and where CZ is applied.

2. **Focus on the pressure term**: Don't try to reconstruct the entire proof — focus on:
   - The energy inequality at each level
   - Where pressure appears
   - What estimate is used on the pressure term
   - What exponent β means in context

3. **Be precise about formulas**: The code worker who receives your output needs to know EXACTLY what integrals to compute. Use explicit notation: ∫_{A_k} p · ψ_k dx where A_k = {x : |u(x)| > C_k} and ψ_k = ..., etc.

4. **Tag everything**: Mark each claim as [VERIFIED] (checked against source), [COMPUTED] (derived by calculation), [CHECKED] (cross-checked against multiple sources), or [CONJECTURED] (reasonable inference but not directly confirmed).

5. **Don't spend more than 40% of your time on literature search**. If you can't find the exact paper, work from what you know about De Giorgi iteration applied to NS and be explicit about which parts are reconstructed.

## Output Requirements

The worker MUST produce:

1. **RESULT.md** — Detailed mathematical analysis with:
   - The De Giorgi truncation scheme (levels, truncation function, super-level sets)
   - The energy inequality at level k with all terms identified
   - The pressure term in explicit integral form
   - How β = 4/3 arises from CZ
   - What β_effective means and how to compute it from DNS
   - The computational specification: a numbered list of formulas to implement
   - Assessment of Tran-Yu claim (if accessible)

2. **RESULT-SUMMARY.md** — Concise summary

Write to RESULT.md incrementally. RESULT-SUMMARY.md signals completion.
