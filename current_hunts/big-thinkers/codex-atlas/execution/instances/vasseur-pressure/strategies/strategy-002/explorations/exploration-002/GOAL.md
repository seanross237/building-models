<!-- explorer-type: math -->

# Exploration 002: DNS Measurement of Level-Set Distribution vs Chebyshev Bound

## Goal

Compute the actual level-set distribution function μ(λ) = |{x : |u(x,t)| > λ}| for 3D Navier-Stokes DNS solutions and compare it against the Chebyshev prediction μ(λ) ~ λ^{-10/3}. Determine whether NS solutions have faster tail decay than Chebyshev predicts — if so, quantify the gap.

## Background

Strategy-002 exploration-001 performed a line-by-line decomposition audit of Vasseur (2007) Proposition 3 and identified the Chebyshev inequality at the truncation level set as the **SINGLE potentially improvable step** in the entire De Giorgi chain. Specifically:

The De Giorgi recurrence exponent β = 4/3 = 1/2 + 5/6 arises from 5 inequality steps. Four are provably sharp. The fifth — the Chebyshev estimate:

|{v_{k-1} > 2^{-k}}| ≤ 2^{10k/3} · ||v_{k-1}||_{L^{10/3}}^{10/3} ≤ C^k · U_{k-1}^{5/3}

is sharp for ARBITRARY L^{10/3} functions but may not be tight for NS solutions, which have additional structure (divergence-free, energy inequality, NS dynamics).

**Improving this to U_{k-1}^{5/3+δ} with δ > 1/3 would break the 4/3 barrier.**

This exploration directly tests whether the Chebyshev step has exploitable numerical slack.

## Specific Computation

### Setup
Use the spectral NS solver from Strategy-001 (located at `../strategy-001/explorations/exploration-002/code/`). Run 3D periodic Navier-Stokes DNS for these cases:
- **Taylor-Green vortex** at Re = 100, 500, 1600
- **Random IC** at Re = 100, 500
- **ABC flow** at Re = 100, 500 (Beltrami control — known to have favorable structure)

Resolution: N = 128 (128³ grid). This matches Strategy-001's convergence-checked resolution.

### Level-set distribution measurement

For each DNS case, at several time snapshots (t = 0.5, 1.0, 2.0, or whenever the flow is most turbulent):

1. **Compute μ(λ) = |{x : |u(x,t)| > λ}| / |Ω|** for 50 logarithmically spaced values of λ from 0.1 × max(|u|) to 0.99 × max(|u|).

2. **Fit the power-law tail:** In the region where μ(λ) is well-behaved (say μ(λ) ∈ [10^{-4}, 0.3]), fit μ(λ) ~ A · λ^{-p}. Extract the exponent p.

3. **Compare with Chebyshev:** The Chebyshev prediction is p = 10/3 ≈ 3.333. If the measured p > 10/3, there is slack. Quantify: p_measured - 10/3 = ?

4. **Also compute the De Giorgi level-set version:** For the truncated velocity v_k = [|u| - (1-2^{-k})]_+, compute:
   - A_k = |{v_{k-1} > 2^{-k}}| (the level-set measure appearing in the De Giorgi iteration)
   - Compare A_k with the Chebyshev bound: 2^{10k/3} · ||v_{k-1}||_{L^{10/3}}^{10/3}
   - Compute the tightness ratio: (Chebyshev bound) / A_k for k = 1, ..., 10
   This directly measures the slack in the specific Chebyshev application used in Vasseur's proof.

### Key checks
- Verify that ||v_{k-1}||_{L^{10/3}} is computed correctly (parabolic norm: (∫_0^T ∫ |v_{k-1}|^{10/3} dx dt)^{3/10})
- Compare the L^{10/3} parabolic norm with the simpler L^{10/3}_x norm at fixed t (the parabolic version integrates over time — make sure you're computing the right one)
- Report raw numbers, not just fits

## Success Criteria

The exploration succeeds if it produces:
1. μ(λ) curves for at least 5 DNS cases with clear power-law fits in the tail region
2. Measured exponents p for each case, with confidence intervals
3. Tightness ratios (Chebyshev bound / actual A_k) for k = 1..10 across at least 3 cases
4. A clear verdict: is p > 10/3 for turbulent NS flows? By how much?

## Failure Criteria

The exploration fails if:
- The solver doesn't produce converged DNS solutions
- The level-set distribution has no clear power-law regime
- The computation is done but without proper comparison to the Chebyshev exponent 10/3

## Important Notes

- **Tag all results:** Use [COMPUTED], [VERIFIED], [CHECKED] tags for machine-verified claims.
- **Worst-case caveat:** DNS solutions are smooth. The Chebyshev bound is most important for near-singular solutions. If you find p > 10/3 on smooth DNS, note explicitly that this does NOT prove the improvement extends to near-singular solutions. The measurement tells us the slack exists for smooth flows — whether it persists is a separate (analytical) question.
- **Reuse code.** The Strategy-001 DNS solver and De Giorgi measurement infrastructure exist. Extend them; don't rewrite from scratch. Key code: `../strategy-001/explorations/exploration-002/code/` contains the spectral solver, level-set truncation, and U_k computation.
- **If the solver code is not accessible**, write a minimal 3D spectral NS solver (periodic box, pseudo-spectral, 2/3 dealiasing, RK4 time stepping). This is standard infrastructure.
