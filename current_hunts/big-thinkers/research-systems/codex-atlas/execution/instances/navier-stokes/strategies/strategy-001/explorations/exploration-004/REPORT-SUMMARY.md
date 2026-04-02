# Exploration 004 Summary: Vortex Stretching Slack Decomposition

## Goal
Decompose the ~237× slack in the vortex stretching bound into three factors (geometric alignment, Ladyzhenskaya constant, symmetric factor) and characterize the geometric factor through strain-vorticity alignment statistics.

## What Was Tried
- Ran pseudospectral DNS at Re=100 (N=48) and Re=1000 (N=64) for the Taylor-Green vortex
- Computed the full 3-factor slack decomposition at 15+ timesteps per simulation
- Eigendecomposed the strain tensor at every grid point to extract alignment statistics
- Computed enstrophy-weighted alignment PDFs, depletion factor, and vorticity direction gradient
- Surveyed known maximizers and computed effective Ladyzhenskaya constants for the flow

## Outcome: Succeeded

### Verification Scorecard
- **6 VERIFIED** (machine-checked identities and exact matches)
- **12 COMPUTED** (numerical results from reproducible code)
- **1 CHECKED** (cross-referenced with published DNS results)
- **3 CONJECTURED** (physical interpretations)

### Key Findings

1. **The decomposition is exact: α_geom × α_Lad × α_sym = total slack at all timesteps.** The product matches to machine precision.

2. **The original factor estimates were significantly wrong.** At the 237× slack point:
   - α_geom ≈ **5.3** (not ~9 as estimated): geometric alignment/Hölder loss
   - α_Lad ≈ **31** (not ~18.6): Ladyzhenskaya constant loss
   - α_sym = **√2** (not ~1.4): exact identity for div-free fields

3. **Ladyzhenskaya is the dominant source of slack** — 63% of log-slack vs 31% for geometric alignment. This is the opposite of what was expected.

4. **Why Ladyzhenskaya dominates:** The effective Ladyzhenskaya constant for the flow's vorticity is C_{L,eff} ≈ 0.147, only 18% of the R³ sharp constant C_L = 0.827. The Ladyzhenskaya optimizer is a spike-like concentrated function; smooth NS solutions are spectrally extended and inherently far from this optimizer.

5. **Alignment statistics:** Vorticity preferentially aligns with the extensional strain eigenvector (⟨cos²θ₁⟩_ω = 0.479 vs isotropic 0.333). The depletion factor is 0.44 — actual stretching is 44% of worst-case. The compressive strain provides 53% cancellation against extensional stretching.

6. **Alignment is robust across Re:** At matched slack levels, Re=100 and Re=1000 show nearly identical alignment statistics (<2% difference), suggesting the geometric factor is topological rather than Reynolds-number-dependent.

## Proof Gaps Identified
- The claim that C_L(T³) = C_L(R³) for the sharp constant needs formal proof (approximation by periodized Gaussians)
- Whether the geometric factor α_geom has a flow-independent lower bound is unknown

## Unexpected Findings
- **The Ladyzhenskaya bound, not Hölder, is the weakest link.** This suggests improving regularity theory should focus on better interpolation inequalities for NS-like fields rather than geometric alignment estimates.
- **The total slack has a minimum in time** (~237×) — it's not monotonic. The minimum corresponds to a balance point where the growing α_Lad and shrinking α_geom cross.
- **The Taylor-Green vortex at Re=100-1000 shows extensional alignment** (cos²θ₁ dominant), unlike fully-developed turbulence which shows intermediate alignment (cos²θ₂ dominant per Ashurst et al. 1987). The transition from extensional to intermediate alignment likely occurs at higher Re.

## Computations Identified
- Run at Re=5000-10000 to check if alignment shifts toward intermediate eigenvector (turbulent regime)
- Compute the effective Ladyzhenskaya constant for random-phase initial conditions (broadband spectrum)
- Investigate whether constrained interpolation inequalities (restricting to div-free, Navier-Stokes-like fields) can yield tighter bounds than the general Ladyzhenskaya inequality
- The 63% log-slack from Ladyzhenskaya suggests exploring Beale-Kato-Majda type bounds that avoid interpolation entirely
