# Exploration 003: Vortex Stretching Slack Across Multiple Initial Conditions + Adversarial Search

## Mission Context

We are building a "slack atlas" for 3D Navier-Stokes regularity theory. Exploration 002 measured the slack in 8 key inequalities on the Taylor-Green vortex, finding that the **vortex stretching bound has 237× minimum slack** — by far the loosest inequality (55× more than the next). The slack grows as Re^0.28.

Critically, exploration 002 found that the minimum slack for functional inequalities is **determined by initial condition geometry**, not dynamics. This means different initial conditions could produce very different slack ratios. Your job is to test this.

## Your Goal

Run the measurement infrastructure from exploration 002 on **at least 5 different initial conditions**, including adversarial ones designed to minimize the vortex stretching slack ratio. The question is: **how low can the vortex stretching slack go?**

## Initial Conditions to Test

### 1. ABC Flow (Arnold-Beltrami-Childress)
```python
A, B, C = 1, 1, 1  # equal coefficients
u_x = A*sin(z) + C*cos(y)
u_y = B*sin(x) + A*cos(z)
u_z = C*sin(y) + B*cos(x)
```
This is a Beltrami flow (ω = u), so vorticity is perfectly aligned with velocity. The vortex stretching term has a specific structure.

### 2. Random-Phase Gaussian
Initialize Fourier modes with random phases and energy spectrum E(k) ~ k⁴ exp(-2(k/k_peak)²) with k_peak = 4. This represents "generic" turbulent initial data.

### 3. Concentrated Vortex Tube
A thin vortex tube along the z-axis:
```
ω_z = Γ/(πσ²) × exp(-(x² + y²)/σ²),  ω_x = ω_y = 0
```
Recover u from ω via Biot-Savart. Use σ = 0.1 (thin tube). This stresses the Sobolev embeddings due to localized gradient.

### 4. Anti-Parallel Vortex Tubes
Two counter-rotating vortex tubes separated by distance d, known to produce strong vortex stretching during reconnection:
```
ω₁ at (0, +d/2) pointing in +z direction
ω₂ at (0, -d/2) pointing in -z direction
```
Use d = π/2, σ = 0.2. This is the canonical setup for studying vortex reconnection, which produces the most intense vortex stretching in known flows.

### 5. Adversarial Gradient Search
Starting from the anti-parallel vortex tube configuration, use numerical optimization to MINIMIZE the vortex stretching slack ratio at the time of peak enstrophy. Parameterize the initial condition as:
- Vortex tube positions (x₁, y₁, x₂, y₂)
- Tube radii (σ₁, σ₂)
- Tube circulations (Γ₁, Γ₂)
- Optional: tube tilt angles (θ₁, φ₁, θ₂, φ₂)

Use scipy.optimize or gradient descent on the min slack ratio. Even a parametric sweep over (d, σ, Γ) would be valuable if full optimization is too expensive.

### 6. (Optional) Kida Vortex
High-symmetry flow — computationally cheap, useful as another data point.

## Measurement Protocol

For each initial condition:
- Use **N=64³** primary, **N=128³** convergence check for the condition with lowest slack
- Run at **Re = 100, 500, 1000** (skip Re=5000 for speed unless results are surprising)
- Use the existing measurement infrastructure from exploration 002 (code at `../exploration-002/code/`)
- Report the **vortex stretching slack ratio** at each timestep
- Record: min slack, time of min slack, Re-dependence, and comparison to Taylor-Green (237×)

## Existing Code

The measurement infrastructure is at `../exploration-002/code/`:
- `ns_solver.py` — pseudospectral DNS solver
- `slack_measurements.py` — 8 bound/actual pairs and diagnostics
- `run_simulations.py` — simulation runner

Copy what you need into your own `code/` directory and extend it for the new initial conditions. Do NOT modify the original files.

## Output Format

### Slack Comparison Table
| Initial Condition | Re=100 min | Re=500 min | Re=1000 min | TGV ratio | Notes |
|---|---|---|---|---|---|

### Adversarial Search Results
- Best parameters found
- Minimum slack achieved
- How it compares to the theoretical lower bound (which is 1, i.e., equality)
- Whether the optimal IC has physical interpretation (e.g., a known vortex configuration)

## Success Criteria
- At least 5 initial conditions tested with vortex stretching slack measured
- At least one adversarial optimization attempted (parametric sweep minimum)
- A comparison table showing slack across all ICs
- Identification of whether ANY initial condition achieves slack < 50× (would be a significant finding)
- N=128 convergence check on the tightest IC

## Failure Criteria
- Fewer than 3 initial conditions tested
- No adversarial search attempted
- Results reported without convergence checks
- No comparison to the Taylor-Green baseline (237×)

## Critical Instructions
- **Tag all numerical claims** with [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- **The anti-parallel vortex tube is the highest priority adversarial IC** — it produces the strongest known vortex stretching. If you run out of time, make sure this one is complete.
- **If any IC achieves slack < 10×**, this is a major finding. Report it prominently and run convergence checks at N=128 AND N=256 if possible.
- **Write results incrementally** — after each IC, write the results to the report before moving to the next.

## File Paths
- Existing code: ../exploration-002/code/
- Your code: code/ (create this directory)
- Report: REPORT.md (in this directory)
- Summary: REPORT-SUMMARY.md (in this directory)
