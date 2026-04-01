# Task 001: DNS Solver Setup and Taylor-Green Vortex Validation

## Mission Context

We are investigating the Vasseur pressure exponent gap in Navier-Stokes regularity theory. Vasseur (2007) showed that De Giorgi iteration achieves a pressure exponent beta = 4/3, but beta > 3/2 would imply full regularity of 3D Navier-Stokes. The entire Millennium Prize Problem compresses to improving one exponent by 1/6.

Our mission is to measure the *effective* pressure exponent in DNS (direct numerical simulation) to determine whether the theoretical bound beta = 4/3 is tight or whether real NS solutions achieve higher exponents. Before measuring anything, we need a validated DNS solver.

## Objective

Set up a working pseudospectral DNS solver for 3D incompressible Navier-Stokes on the periodic torus T^3 = [0, 2π]^3, and validate it against published Taylor-Green vortex benchmarks. The solver must compute and output the pressure field (not just velocity), as pressure is central to all subsequent measurements.

## Success Criteria

1. **Solver runs correctly**: Taylor-Green vortex at Re=100, N=64 produces physically reasonable energy decay and enstrophy evolution.
2. **Quantitative validation**: Compare enstrophy evolution against published Taylor-Green results (Brachet et al. 1983, or equivalent). Enstrophy peak timing and magnitude should agree within 5% at adequate resolution.
3. **Energy conservation**: The energy equation E(t) + 2ν ∫₀ᵗ ||∇u||² ds = E(0) holds to relative error < 1e-6 at Re=100, N=64.
4. **Divergence-free**: max|∇·u| < 1e-10 at all times.
5. **Pressure field output**: The solver computes and outputs the full pressure field p(x,t) in physical space at diagnostic timesteps.
6. **Resolution convergence**: Run Taylor-Green at Re=100 for both N=64 and N=128. Show that enstrophy evolution converges (difference < 2%).
7. **Higher Re test**: Run at Re=1000, N=64 and N=128. Report whether N=64 is adequate or underresolved.

## Failure Criteria

- If the solver produces energy growth (E(t) > E(0) by more than roundoff), something is fundamentally wrong — debug.
- If energy conservation error exceeds 1e-4 at Re=100, N=64, the time-stepping or dealiasing is broken.
- If you cannot get a working solver within reasonable effort, report what failed and why.

## Relevant Context

### Prior Atlas Code

There is an existing pseudospectral NS solver from a prior Atlas mission at:
```
/Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/atlas/execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-002/code/
```

Files:
- `ns_solver.py` — NavierStokesSolver class: FFT-based pseudospectral, 2/3 dealiasing, RK4, CFL-adaptive dt, Leray-Helmholtz pressure projection. Also contains `taylor_green_ic()`.
- `run_simulations.py` — Runs simulations and collects slack measurements.
- `slack_measurements.py` — 8 bound/actual inequality pairs with sharp constants on T^3.

**Evaluation**: This code is already quite good. It handles the core NS numerics correctly. What it's MISSING for our purposes:
1. **Pressure field computation**: The solver projects out divergent modes (pressure projection) but does not store/output the actual pressure field p. We need p(x,t) explicitly — it's the key quantity for Vasseur's De Giorgi analysis.
2. **Pressure computation**: From the NS momentum equation, p is recovered from the Poisson equation: Δp = -∂ᵢ∂ⱼ(uᵢuⱼ). In Fourier space: p̂(k) = -kᵢkⱼ (ûᵢ*ûⱼ)^(k) / |k|². This is closely related to the existing pressure projection code but needs to be extracted as an explicit field.
3. **L^p norms of pressure**: We need ||p||_{L^q} for various q, especially q = 3/2 (the Calderón-Zygmund exponent).

**Recommendation**: Copy the Atlas code into your `code/` directory, adapt it, and extend it.

### Taylor-Green Vortex Benchmarks

The Taylor-Green vortex (TGV) is the standard DNS validation test:
- IC: u = (sin x cos y cos z, -cos x sin y cos z, 0) on [0, 2π]^3
- At Re = 100: enstrophy peaks around t ≈ 5-6, then decays
- At Re = 1600: transition to turbulence, enstrophy peak sharper and later
- Brachet et al. (1983) and more recently van Rees et al. (2011) provide reference enstrophy evolution data

Key benchmark numbers for Re=100:
- Enstrophy peak should occur around t ≈ 5-6
- Energy decay should be smooth and monotonic
- For N=64 at Re=100, the flow should be well-resolved (spectrum drops off before 2N/3)

### Pressure Computation (Technical Detail)

In a pseudospectral code, the pressure p solves:
  Δp = -∇·(u·∇u) = -∂ᵢ∂ⱼ(uᵢuⱼ)

In Fourier space:
  p̂(k) = kᵢkⱼ/(|k|²) * (uᵢuⱼ)^(k)  [for k ≠ 0; p̂(0) = 0]

This can be computed from the nonlinear term that the solver already computes. The existing `project()` method in ns_solver.py does exactly this projection — it computes k·F/|k|² and subtracts it. The pressure field IS this k·F/|k|² component (up to a factor of -1 and the 1j factors from differentiation).

Specifically, if NL is the nonlinear term (u·∇u) in Fourier space:
  p̂(k) = kᵢ NLᵢ^(k) / |k|²

Then project() removes this from the RHS. So pressure is already implicitly computed — it just needs to be extracted and saved.

## Approach Guidance

1. **Start by copying the Atlas code** into your `code/` directory and getting it running as-is. Verify it imports and runs.
2. **Add pressure field extraction**: Modify the solver to compute and return p(x,t) alongside velocity diagnostics. Add a `compute_pressure()` method.
3. **Add pressure diagnostics**: Compute ||p||_{L^q} for q = 1, 3/2, 2, 3, ∞ at each diagnostic timestep.
4. **Validate**: Run Taylor-Green at Re=100, N=64. Check energy conservation, divergence-free, enstrophy evolution.
5. **Resolution test**: Run at both N=64 and N=128 for Re=100. Compare enstrophy.
6. **Higher Re**: Run at Re=1000, both resolutions. Report resolution adequacy.
7. **Save results**: Output a JSON file with all diagnostic time series.

Pitfalls to avoid:
- The pressure computation MUST use the dealiased nonlinear term, same as the RHS computation. Don't compute pressure from un-dealiased products.
- The 2/3 dealiasing is essential — without it, aliasing errors corrupt the pressure field.
- At high Re and low N, the flow may be underresolved. This is expected — just report it clearly.

## Output Requirements

The worker MUST produce:

1. **`code/`** directory containing:
   - `ns_solver.py` — adapted solver with pressure computation
   - `run_validation.py` — validation script that runs all the tests described above
   - `validation_results.json` — output data
   - Any other support files needed

2. **RESULT.md** — detailed account of what was done, including:
   - What was changed in the solver
   - Validation results with numbers
   - Enstrophy evolution data at key timesteps
   - Energy conservation errors
   - Pressure field statistics
   - Resolution convergence comparison

3. **RESULT-SUMMARY.md** — concise summary (see required sections below). Write this LAST.

Write to RESULT.md incrementally as you work. RESULT-SUMMARY.md signals completion.
