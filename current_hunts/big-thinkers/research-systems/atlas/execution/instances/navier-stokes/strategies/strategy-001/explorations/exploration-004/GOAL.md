# Exploration 004: Vortex Stretching Slack Decomposition — Isolating the Geometric Factor

## Mission Context

The vortex stretching bound |∫S_{ij}ω_iω_j dx| ≤ C²_L × ||ω||^{3/2}_{L²} × ||∇ω||^{3/2}_{L²} has 237× slack on the Taylor-Green vortex (exploration 002). This slack decomposes into three sources:

1. **Hölder loss (~9×):** |∫S_{ij}ω_iω_j dx| ≤ ||S||_{L²} × ||ω||²_{L⁴} discards geometric alignment
2. **Constant loss (~18.6×):** Using C_L from ℝ³ on T³ (the Ladyzhenskaya constant squared, since it appears twice in the chain)
3. **Symmetric/antisymmetric factor (~1.4×):** ||S||_{L²} ≤ ||∇u||_{L²} loses the √2 from only taking the symmetric part

Your job is to **precisely quantify each factor** and, most importantly, **characterize the geometric factor** — the 9× from Hölder. This is the most interesting and potentially exploitable source of slack.

## Your Goal

### Part A: Precise Decomposition of the 237× Slack

Compute the following intermediate quantities at each timestep for the Taylor-Green vortex at Re=100 and Re=1000:

1. **Actual VS:** VS_actual = |∫ S_{ij} ω_i ω_j dx|
2. **Hölder product:** VS_Hölder = ||S||_{L²} × ||ω||²_{L⁴}
3. **Full bound:** VS_bound = C²_L × ||ω||^{3/2}_{L²} × ||∇ω||^{3/2}_{L²}

Then the decomposition is:
- **Geometric alignment factor:** α_geom = VS_Hölder / VS_actual (measures how much Hölder loses by ignoring alignment)
- **Ladyzhenskaya factor:** α_Lad = (C_L × ||ω||^{1/4}_{L²} × ||∇ω||^{3/4}_{L²})² / ||ω||²_{L⁴} = (Lad bound on ||ω||_{L⁴})² / ||ω||²_{L⁴}
- **Symmetric factor:** α_sym = ||∇u||_{L²} / ||S||_{L²} (should be √2 for div-free fields)
- **Check:** α_geom × α_Lad × α_sym should equal the total slack VS_bound / VS_actual = 237

### Part B: Characterize the Geometric Factor

The geometric factor α_geom measures how much the actual vortex stretching differs from the Hölder bound. Physically, this depends on the alignment between vorticity ω and the strain eigenvectors.

Compute the following at each timestep:

1. **Strain eigenvalues:** At each grid point, compute the eigenvalues λ₁ ≥ λ₂ ≥ λ₃ of the strain rate tensor S_{ij}. (By incompressibility, λ₁ + λ₂ + λ₃ = 0, so λ₁ > 0 > λ₃.)

2. **Vorticity-strain alignment:** At each grid point, compute:
   - cos²(θ₁) = (ω̂ · e₁)² where e₁ is the eigenvector of λ₁ (extensional strain)
   - cos²(θ₂) = (ω̂ · e₂)² where e₂ is the eigenvector of λ₂ (intermediate)
   - cos²(θ₃) = (ω̂ · e₃)² where e₃ is the eigenvector of λ₃ (compressive)

   Report the volume-averaged (or enstrophy-weighted) alignment statistics.

3. **Constantin-Fefferman depletion factor:** The actual VS can be written as:
   VS = ∫ (λ₁ cos²θ₁ + λ₂ cos²θ₂ + λ₃ cos²θ₃) |ω|² dx

   The Hölder bound corresponds to replacing all cos²θ with their worst-case values. The depletion factor is the ratio of the actual alignment integral to the worst-case.

4. **Vorticity direction gradient:** Compute ||∇ξ||_{L²} where ξ = ω/|ω| (the vorticity direction field). This is the quantity in the Constantin-Fefferman regularity criterion.

### Part C: Sharp Ladyzhenskaya Constant on T³ for Div-Free Fields

As a secondary computation, attempt to compute the **sharp Ladyzhenskaya constant** restricted to divergence-free vector fields on T³:

C_{L,div-free} = sup{ ||u||_{L⁴} / (||u||^{1/4}_{L²} × ||∇u||^{3/4}_{L²}) : u ∈ H¹(T³), ∇·u = 0, u ≠ 0 }

Approach: parameterize div-free fields in Fourier space as û(k) = a(k) × k̂ + b(k) × (k̂ × ê) for arbitrary coefficients a(k), b(k), and optimize the ratio using scipy. Start with low-frequency modes (|k| ≤ 5) and increase resolution.

Compare to the general (non-div-free) constant C_L = 0.827. If C_{L,div-free} < C_L, this improves the vortex stretching bound by (C_{L,div-free}/C_L)².

## Existing Code

Use the infrastructure from exploration 002: `../exploration-002/code/ns_solver.py` and `../exploration-002/code/slack_measurements.py`. Copy what you need into your `code/` directory.

## Output Format

### Part A Table: Slack Decomposition Over Time (Re=1000)
| t | VS_actual | VS_Hölder | VS_bound | α_geom | α_Lad | α_sym | Total (check) |
|---|---|---|---|---|---|---|---|

### Part B: Alignment Statistics
- PDF (histogram) of cos²(θ₁,₂,₃) weighted by |ω|² at time of peak enstrophy
- Enstrophy-weighted mean alignment: ⟨cos²θ_i⟩_ω for i=1,2,3 vs. time
- Comparison to isotropic expectation (⟨cos²θ_i⟩ = 1/3 for each)
- The depletion factor vs. time

### Part C: Sharp Constant
- C_{L,div-free} vs. number of Fourier modes included
- Convergence behavior
- The optimizer (which div-free field achieves the highest ratio)

## Success Criteria
- Complete decomposition α_geom × α_Lad × α_sym = total slack verified to < 5% at all timesteps
- Alignment statistics computed and reported (at least the enstrophy-weighted means)
- At least a preliminary estimate of C_{L,div-free}
- Physical interpretation of why the geometric factor is ~9× (what about the flow structure causes this?)

## Failure Criteria
- Decomposition doesn't multiply to the total (indicates a bug)
- No eigenvalue/alignment computation attempted
- Only Part A completed without Part B

## Critical Instructions
- Tag all numerical claims with [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- **Part B is the highest priority** — the alignment statistics are the most scientifically interesting output
- Part C (sharp constant) is secondary — attempt it only if Parts A and B are complete
- Write incrementally: Part A results first, then Part B, then Part C

## File Paths
- Existing code: ../exploration-002/code/
- Your code: code/ (create this directory)
- Report: REPORT.md
- Summary: REPORT-SUMMARY.md
