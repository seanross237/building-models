# Exploration 001: BKM Enstrophy Bypass — Computational Validation

## Mission Context

We are studying the 3D Navier-Stokes regularity problem. Strategy-001 established that the vortex stretching bound — the key inequality in the enstrophy approach to regularity — has **237x slack** on Taylor-Green vortex flows (158x adversarial minimum). The slack decomposes as 63% from the Ladyzhenskaya interpolation constant + 31% from geometric alignment + 6% from the symmetric factor.

Strategy-001 also found that the BKM/Calderon-Zygmund approach gives **near-tight bounds** (~3x slack with theoretical constant) on the same flows where Ladyzhenskaya has 237x slack.

**The central question of this exploration:** Does translating the BKM advantage into the enstrophy ODE actually produce a tighter regularity criterion? The BKM bound uses ||omega||_{L^infty} instead of interpolating through L^2 norms, which trades the Ladyzhenskaya constant looseness for a need to control ||omega||_{L^infty}/||omega||_{L^2}. If this ratio grows too fast, BKM could be WORSE for enstrophy control.

## Goal

Compute and compare two enstrophy ODE closures for 3D Navier-Stokes:

**Closure 1 (Ladyzhenskaya chain — the standard approach):**
Starting from the enstrophy equation:
  (1/2) d/dt ||omega||^2_{L^2} = integral(omega_i S_{ij} omega_j) dx - nu ||nabla omega||^2_{L^2}

Bound the vortex stretching using Ladyzhenskaya + Holder:
  |VS| <= C_L ||omega||^{3/2}_{L^2} ||nabla omega||^{3/2}_{L^2}

After Young's inequality to absorb the dissipation term:
  d/dt ||omega||^2_{L^2} <= C ||omega||^6_{L^2} / nu^3

This gives FINITE-TIME blow-up: y(t) = y_0/(1 - C*y_0^2*t/nu^3)^{1/2}

**Closure 2 (BKM-based):**
Bound the vortex stretching using the Calderon-Zygmund bound on the strain:
  |VS| = |integral(omega_i S_{ij} omega_j)| <= ||omega||^2_{L^2} ||S||_{L^infty}

Then use the BKM-type estimate:
  ||S||_{L^infty} <= C_{CZ} ||omega||_{L^infty} (1 + log^+(||nabla omega||_{L^2}/||omega||_{L^2}))

So:
  |VS| <= C_{CZ} ||omega||^2_{L^2} ||omega||_{L^infty} (1 + log^+(||nabla omega||_{L^2}/||omega||_{L^2}))

After absorbing the dissipation term with Young's inequality, the resulting ODE structure depends on how ||omega||_{L^infty} relates to ||omega||_{L^2}.

## Specific Computations Required

### Step 1: Set up the DNS solver
Use the validated pseudospectral solver from Strategy-001 at:
  `../../strategy-001/explorations/exploration-002/code/ns_solver.py`
  `../../strategy-001/explorations/exploration-002/code/slack_measurements.py`

Copy and adapt this code. Run at N=64 resolution (N=128 convergence check for key results).

### Step 2: Compute both bounds at every timestep
For each initial condition and Reynolds number, at every saved timestep, compute:

a) **Actual vortex stretching**: VS_actual = integral(omega_i S_{ij} omega_j) dx (the actual value, can be positive or negative)

b) **Ladyzhenskaya bound**: VS_Lad = C_L ||omega||^{3/2}_{L^2} ||nabla omega||^{3/2}_{L^2}
   Use the sharp constant C_L = 0.827 (on R^3).

c) **BKM bound**: VS_BKM = C_{CZ} ||omega||^2_{L^2} ||omega||_{L^infty} (1 + log^+(||nabla omega||_{L^2}/||omega||_{L^2}))
   Use the theoretical Calderon-Zygmund constant C_{CZ}. Strategy-001 used C_{CZ} = 0.24 (theoretical). Use this value and also report the empirical C_{CZ} that makes the bound tight at each timestep.

d) **BKM slack** = VS_BKM / |VS_actual|
e) **Ladyzhenskaya slack** = VS_Lad / |VS_actual|
f) **Advantage factor** = VS_Lad / VS_BKM (how many times tighter BKM is)

### Step 3: Compute the ODE RHS comparison
For each closure, compute the right-hand side of the enstrophy ODE:

a) **Ladyzhenskaya ODE RHS**: RHS_Lad = C_L ||omega||^{3/2} ||nabla omega||^{3/2} - nu ||nabla omega||^2
   After Young's inequality: RHS_Lad_Young = C_Lad^4 ||omega||^6 / (27 nu^3)

b) **BKM ODE RHS**: RHS_BKM = C_{CZ} ||omega||^2 ||omega||_{L^infty} (1 + log^+(...)) - nu ||nabla omega||^2
   Apply Young's inequality here too. The key: what power of ||omega||_{L^2} appears after absorption?

c) **Actual RHS**: d/dt ||omega||^2_{L^2} computed directly from the simulation

Report: actual RHS, Lad bound on RHS, BKM bound on RHS, at every timestep.

### Step 4: Effective blow-up time comparison
Starting from the measured ||omega(0)||_{L^2}, integrate BOTH ODE closures forward analytically (or numerically if the BKM version doesn't have closed-form):

a) Ladyzhenskaya-based ODE: what is the blow-up time T_Lad?
b) BKM-based ODE: what is the blow-up time T_BKM? (Does it blow up at all? If the log correction gives double-exponential growth instead of finite-time blow-up, that's the headline result.)
c) Actual enstrophy at the end of simulation.

Report T_BKM/T_Lad for each IC and Re.

### Step 5: The critical check — ||omega||_{L^infty}/||omega||_{L^2} dynamics
This is the make-or-break measurement:

a) Compute ||omega||_{L^infty}/||omega||_{L^2} at every timestep.
b) How does this ratio scale with Re?
c) How does it change in time (early vs. late)?
d) If this ratio grows proportionally to ||omega||_{L^2}^alpha for some alpha > 0, the BKM approach may lose its advantage. Measure alpha.

### Step 6: Young's inequality optimization
For the BKM closure, when you apply Young's inequality to separate the vortex stretching from the dissipation term, there is freedom in how you do it. Try multiple strategies:
a) Standard Young with epsilon: absorb ||nabla omega||^2 into the dissipation
b) Optimize epsilon at each timestep (what epsilon minimizes the resulting bound?)
c) Report the best-case BKM ODE after Young's inequality optimization

## Initial Conditions and Parameters

**Reynolds numbers:** Re = 100, 500, 1000, 5000 (nu = 1/Re)
**Resolution:** N = 64 primary; N = 128 convergence check for Re=1000 (TGV only)
**Time integration:** Run to T = 5.0 or until enstrophy starts decaying, whichever is later
**Save interval:** Every 0.05 time units (100 snapshots per run)

**Initial conditions:**
1. **Taylor-Green vortex** (the baseline from Strategy-001):
   u = (sin(x)cos(y)cos(z), -cos(x)sin(y)cos(z), 0)

2. **Random-phase Gaussian** with Kolmogorov spectrum:
   E(k) ~ k^{-5/3} for k in [1, N/3], random phases, divergence-free projected

3. **Adversarial anti-parallel tubes** (the 158x IC from Strategy-001):
   sigma = 2.5, d = pi/4, delta = 1.2 (parameters from exploration-003)
   If you can't reconstruct the exact IC, use a reasonable anti-parallel tube setup.

## Success Criteria

**The exploration succeeds if:**
- Both bounds are computed for all 4 Re values and all 3 ICs (12 runs minimum)
- The effective blow-up time ratio T_BKM/T_Lad is reported for all runs
- The ||omega||_{L^infty}/||omega||_{L^2} dynamics are characterized

**The BKM direction is validated if:**
- T_BKM/T_Lad > 10 for all tested flows (BKM gives ≥10x later blow-up)
- OR the BKM-based ODE gives double-exponential growth (no finite-time blow-up)

**The BKM direction fails if:**
- T_BKM/T_Lad < 2 for most flows (BKM isn't significantly better)
- OR ||omega||_{L^infty}/||omega||_{L^2} grows fast enough to negate the log advantage

## Failure Criteria

If the DNS solver fails to converge or the computations can't complete in time, at minimum deliver:
- TGV at Re=100 and Re=1000 with both closures
- The ||omega||_{L^infty}/||omega||_{L^2} ratio dynamics for TGV

## Output Format

Write your findings as REPORT.md and REPORT-SUMMARY.md in your exploration directory (the current directory). Include:
1. Summary table: IC × Re → T_BKM/T_Lad, min BKM slack, min Lad slack, advantage factor
2. Time series plots or tables of key quantities
3. Clear verdict: does the BKM enstrophy bypass work?
4. All code in a `code/` subdirectory with a README
