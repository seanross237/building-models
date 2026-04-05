# Exploration 002: Computational Slack Measurement — Infrastructure + Taylor-Green Vortex

## Mission Context

We are building a "slack atlas" for 3D Navier-Stokes regularity theory — measuring how loose the key analytical estimates are compared to what actually happens in computed flows. Exploration 001 produced a comprehensive catalog of 17 load-bearing inequalities, ranked by expected slack. Your job is to make these inequalities computable and run the first measurements.

## Your Goal

**Part A: Build the Measurement Infrastructure**

For each of the following 8 key inequalities from the catalog, write a pair of Python functions:
- `bound_XX(u_hat, solver) → float` — computes the RIGHT-HAND side of the inequality (the proven upper bound)
- `actual_XX(u_hat, solver) → float` — computes the LEFT-HAND side (what the inequality bounds)
- The slack ratio is then `bound / actual` (should be ≥ 1 if the inequality holds)

The 8 inequalities to implement (IDs from the catalog):

### F1: Ladyzhenskaya (3D)
- **Bound:** C_L × ||u||_{L²}^{1/4} × ||∇u||_{L²}^{3/4}
- **Actual:** ||u||_{L⁴}
- Use C_L from the general GNS sharp constant. Compute it numerically if needed — the sharp constant for ||u||_{L⁴} ≤ C||u||_{L²}^{1/4}||∇u||_{L²}^{3/4} on T³ is known via Fourier analysis.

### F3: Sobolev H¹ ↪ L⁶
- **Bound:** S₃ × ||∇u||_{L²}
- **Actual:** ||u||_{L⁶}
- S₃ is the sharp Aubin-Talenti constant.

### E2/E3: Vortex Stretching
- **Bound:** C × ||ω||_{L²}^{3/2} × ||∇ω||_{L²}^{3/2} (from Ladyzhenskaya applied to ω)
- **Actual:** |∫ S_{ij} ω_i ω_j dx| (the actual vortex stretching integral)
- For C, use the Ladyzhenskaya constant from F1 (since the bound chains through it).
- This is the **highest priority** measurement. The vortex stretching bound is the #1 bottleneck.

### E1: Energy Inequality
- **Bound:** ||u₀||²_{L²} (initial energy, for unforced case)
- **Actual:** ||u(t)||²_{L²} + 2ν ∫₀ᵗ ||∇u||² ds (accumulated energy + dissipation)
- Slack = bound/actual should be ≈ 1 for smooth solutions (equality expected). Any deviation indicates energy conservation issues in the numerics.

### R1/F2: Prodi-Serrin Supporting GNS
- **Bound:** C × ||u||_{L²}^{1/4} × ||u||_{H¹}^{7/4} (from GNS applied to nonlinear term ||u·∇u||_{L²})
- **Actual:** ||u·∇u||_{L²}
- This bounds the nonlinear term that appears in regularity arguments.

### F4+G1: Agmon + Gronwall Chain
- **Bound:** C × ||u||_{H¹}^{1/2} × ||u||_{H²}^{1/2} (Agmon for ||∇u||_{L^∞})
- **Actual:** ||∇u||_{L^∞}
- This is the second-highest priority.

### F5: Calderón-Zygmund Pressure
- **Bound:** C_{CZ} × ||u||²_{L³} (CZ for pressure L^{3/2} norm)
- **Actual:** ||p||_{L^{3/2}}
- Compute pressure via p = -Δ⁻¹(∂_i u^j ∂_j u^i) in Fourier space.

### E4: H^s Energy (Transport Cancellation Check)
- **Bound:** C × ||∇u||_{L^∞} × ||u||²_{H²} (Kato-Ponce based)
- **Actual:** |d/dt ||u||²_{H²}| + 2ν||u||²_{H³} (actual H² energy change rate)
- This checks how much the transport cancellation (div u = 0) helps.

## Part B: Run First Measurements — Taylor-Green Vortex

### Simulation Setup
- **Solver:** Use the existing pseudospectral solver at `code/ns_solver.py` as a starting point. Modify or extend as needed. If it has bugs or missing features, fix them.
- **Initial condition:** Taylor-Green vortex:
  ```
  u_x = sin(x) cos(y) cos(z)
  u_y = -cos(x) sin(y) cos(z)
  u_z = 0
  ```
- **Domain:** T³ = [0, 2π]³ (periodic)
- **Resolution:** N = 64³ primary, N = 128³ convergence check for vortex stretching
- **Reynolds numbers:** Re = 100, 500, 1000, 5000 (set ν = 1/Re with appropriate scaling)
- **Time evolution:** Run to t = 5 (Taylor-Green develops maximum enstrophy around t ≈ 1-3 depending on Re). Sample slack ratios at 50+ timesteps.

### Measurement Protocol
For each Re, at each timestep, compute all 8 slack ratios. Record:
1. Time-averaged slack ratio (mean over all timesteps after t = 0.5)
2. Minimum slack ratio (worst case = tightest approach to bound)
3. Time of minimum slack (when does the bound come closest to being tight?)
4. Trend with Re (does slack grow, shrink, or stay constant?)

### Output Requirements
Produce a **Slack Atlas Table**:

| Inequality | Re=100 (mean±std) | Re=500 | Re=1000 | Re=5000 | Trend | Min Slack (worst Re) |
|---|---|---|---|---|---|---|

Also produce time-series plots (as described data, not images) showing slack ratio vs. time for each inequality at Re=1000.

## Scaffolding Available

The file `code/ns_solver.py` contains a pseudospectral DNS solver with:
- FFT-based spectral method on T³
- 2/3 dealiasing rule
- RK4 time stepping with adaptive CFL
- Pressure projection for incompressibility

You should USE this solver, extending it as needed. Don't rewrite from scratch.

## Success Criteria
- All 8 bound/actual function pairs are implemented and tested on at least one flow
- Slack ratios computed for Taylor-Green at 4 Reynolds numbers (Re = 100, 500, 1000, 5000)
- Energy conservation (E1) verified to ≤ 1% error (validates the numerics)
- A ranked slack table produced with quantified ratios
- N=128³ convergence check for the vortex stretching slack ratio at one Re value
- All numerical results tagged with [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]

## Failure Criteria
- Fewer than 5 inequality pairs implemented
- No simulation results (only code, no data)
- Energy conservation fails (>5% error) without explanation
- Slack ratios reported without error bars or convergence checks

## Critical Instructions
- **Tag every numerical claim.** [VERIFIED] = independently checked by two methods. [COMPUTED] = result of a single computation. [CHECKED] = sanity-checked against known results. [CONJECTURED] = based on extrapolation or estimation.
- **If Re=5000 at N=64³ is under-resolved** (energy spectrum not decaying by Nyquist), report it and use the highest Re that IS resolved. Don't report garbage data.
- **Write code incrementally.** Test each bound/actual pair on a simple known flow (e.g., single Fourier mode) before running the full simulation.
- **The vortex stretching measurement is highest priority.** If you run out of time/context, make sure E2/E3 is complete.

## File Paths
- Solver code: code/ns_solver.py (already exists — read and extend)
- New measurement code: code/slack_measurements.py (create this)
- Write your report to: REPORT.md (in this exploration directory)
- Write a concise summary to: REPORT-SUMMARY.md (in this exploration directory)
