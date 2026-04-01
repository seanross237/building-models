<!-- explorer-type: standard -->

# Exploration 001: Line-by-Line Decomposition Audit of the β = 4/3 Barrier

## Goal

Perform a line-by-line reading of Vasseur (2007), "A new proof of partial regularity of solutions to 3-D incompressible Navier-Stokes equations" (arXiv:0607017), specifically **Proposition 3** (the De Giorgi recurrence inequality). Extract the precise chain of inequalities that produces the recurrence exponent β < 4/3, identifying exactly where each sub-exponent (1/2 and 5/6) originates and which steps have potential slack.

## Background

The De Giorgi iteration for 3D Navier-Stokes produces a recurrence:

U_k ≤ C^k · U_{k-1}^β

where β < 4/3 is the critical exponent. Strategy-001 (10 explorations) established that:
- β = 4/3 = 1/2 + 5/6 (conceptually)
- 1/2 comes from the energy/derivative definition: ||∇(β_k v)||_{L²} ≤ U_{k-1}^{1/2}
- 5/6 comes from Sobolev embedding H¹ → L⁶ in 3D + Chebyshev on nonlinear velocity factors at the truncation level
- The same 4/3 appears in the vorticity formulation (Vasseur-Yang 2021) via different mechanism
- No paper since 2007 has improved β
- CZ slack improvement, Galilean invariance, Choi-Vasseur alternative decomposition, and global Beltrami conditioning are all closed

BUT: we do not yet have the line-by-line detail needed to identify which specific steps in the proof have slack and which are provably sharp. That is what this exploration provides.

## Specific Tasks

### Task 1: Extract the complete chain of inequalities in Proposition 3

For each step in the proof of Proposition 3, record:
1. The inequality being used (verbatim or paraphrased with equation reference)
2. What mathematical tool is invoked (Hölder, Sobolev, Young, CZ, interpolation, Chebyshev, etc.)
3. What exponents appear and how they are chosen
4. What structural property of NS is used (if any): divergence-free, pressure equation, energy inequality, etc.
5. Whether the step is SHARP (the inequality is known to be tight for the relevant function class) or POTENTIALLY LOOSE (tightness unknown or known to be non-tight for restricted classes)

### Task 2: Produce a sensitivity table

For each step that contributes to the final exponent β, compute:
- If this step's exponent improved by δ (e.g., replacing p with p+δ in an Lp bound), what would β become?
- Which steps are "bottleneck" (small improvement → large β change) vs "insensitive" (large improvement → small β change)?
- Are there trade-offs (improving step X worsens step Y)?

The sensitivity table should look like:
```
| Step | Tool | Exponent contribution to β | Sensitivity dβ/dδ | Sharp? | Notes |
```

### Task 3: Identify free parameters

The proof makes choices:
- Truncation function shape: β_k(s) = s · min(1, λ_k/s) — is this optimal?
- Sobolev exponent: which Lp space is the interpolation target?
- Hölder conjugate pairs: how are they chosen?
- Pressure decomposition: how is the pressure split?

For each choice, note whether it was OPTIMIZED (the author chose the best option) or CONVENTIONAL (a standard choice that could potentially be improved).

### Task 4: Cross-check with the vorticity formulation

Vasseur-Yang (2021), "Second derivatives estimate of suitable solutions to the 3D Navier-Stokes equations," applies De Giorgi to the vorticity equation. Strategy-001's exploration-008 found that the same 4/3 reappears from:
- ∇ costs U^{1/2} (same origin as velocity)
- Quadratic nonlinearity costs U^{5/6} (from trilinear structure)

For the vorticity version: do the SAME steps appear, or are different inequalities used to reach the same final number? If different, which steps have different sharpness?

## Success Criteria

The exploration succeeds if it produces:
1. A complete step-by-step decomposition of Proposition 3 with ≥ 6 distinct inequality steps identified and classified (sharp vs potentially loose)
2. A sensitivity table showing how β depends on each step's exponent
3. Identification of ≥ 2 free parameters with assessment of whether they were optimized
4. A cross-comparison with the vorticity formulation showing whether the improvable steps are the SAME or DIFFERENT

## Failure Criteria

The exploration fails if:
- It only reproduces the high-level "1/2 + 5/6" without the step-by-step detail
- It cannot access or read the Vasseur (2007) paper sufficiently to extract the proof structure
- The sensitivity table is missing or does not distinguish bottleneck from insensitive steps

## Key References

- Vasseur (2007): arXiv:0607017, specifically Proposition 3 and its proof
- Vasseur-Yang (2021): "Second derivatives estimate of suitable solutions to the 3D Navier-Stokes equations"
- Strategy-001 exploration-001 REPORT (framework extraction): established the high-level structure
- Strategy-001 exploration-008 REPORT (vorticity De Giorgi): established universality of 4/3

## Notes

- This is a READING and ANALYSIS task. No computation or DNS is needed.
- Be precise about equation numbers and line references. "Step 3 in the proof of Proposition 3, going from (3.14) to (3.15)" is the required citation level.
- If you cannot access the paper directly, reconstruct the proof from the arXiv version and standard PDE references. The key mathematical content is: De Giorgi iteration with truncated velocity, local energy inequality, pressure decomposition, Calderón-Zygmund theory, Sobolev embedding in 3D.
- The 5/6 is the MORE PROMISING target for improvement. Pay special attention to the chain of inequalities that produces the 5/6 contribution. Is there a single step where 5/6 appears, or is it a combination of several steps?
