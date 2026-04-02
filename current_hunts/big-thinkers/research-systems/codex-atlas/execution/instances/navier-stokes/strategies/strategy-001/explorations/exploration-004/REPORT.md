# Exploration 004: Vortex Stretching Slack Decomposition — Isolating the Geometric Factor

## Goal

Decompose the ~237× slack in the vortex stretching bound |∫S_{ij}ω_iω_j dx| ≤ C²_L × ||ω||^{3/2}_{L²} × ||∇ω||^{3/2}_{L²} into three constituent factors:
1. **Geometric alignment factor** α_geom: Hölder loss from ignoring strain-vorticity alignment
2. **Ladyzhenskaya factor** α_Lad: Constant loss from using C_L on T³
3. **Symmetric factor** α_sym: Loss from ||S||_{L²} ≤ ||∇u||_{L²}

Then characterize the geometric factor through strain-vorticity alignment statistics.

---

## Part A: Precise Decomposition of the 237× Slack

### Methodology

The bound chain is:
1. |∫ S_{ij}ω_iω_j dx| ≤ ||S||_{L²} × ||ω||²_{L⁴}  (Hölder/Cauchy-Schwarz)
2. ||ω||²_{L⁴} ≤ C²_L × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}  (Ladyzhenskaya²)
3. ||S||_{L²} ≤ ||∇u||_{L²} = ||ω||_{L²}  (symmetric part ≤ full gradient; Parseval for div-free)

Combining: ≤ C²_L × ||ω||^{3/2}_{L²} × ||∇ω||^{3/2}_{L²}

The three slack factors:
- **α_geom** = VS_Hölder / VS_actual = (||S||_{L²} × ||ω||²_{L⁴}) / |∫ Sωω dx|
- **α_Lad** = (C²_L × ||ω||^{1/2}_{L²} × ||∇ω||^{3/2}_{L²}) / ||ω||²_{L⁴}
- **α_sym** = ||∇u||_{L²} / ||S||_{L²}

**Decomposition check: α_geom × α_Lad × α_sym = Total slack at every timestep.** **[VERIFIED]** (code: `code/decomposition.py`)

Constants used:
- C_L (scalar, R³): C⁴_L = 8/(3√3 π²) ≈ 0.1561, C_L ≈ 0.6285
- C_L (vector, R³): C⁴_{L,vec} = 3 × C⁴_{L,scalar} ≈ 0.4684, C_{L,vec} ≈ 0.8271

### Identity: α_sym = √2 Exactly

**Theorem:** For divergence-free fields on T³, ||∇u||_{L²} = √2 ||S||_{L²}. **[VERIFIED]**

**Proof (verified computationally with 5 random div-free fields, code: `code/verify_sqrt2.py`):**
- ∇u = S + Ω where S is symmetric, Ω is antisymmetric
- ||∇u||² = ||S||² + ||Ω||² (cross term vanishes: ⟨S,Ω⟩ = 0)
- ||S||² = ||Ω||² (because ∫ ∂_j u_i ∂_i u_j dx = -∫ u_i ∂_i(∇·u) dx = 0 for div-free u)
- Therefore ||∇u||² = 2||S||², giving α_sym = √2 = 1.4142...

Also verified: ||∇u||_{L²} = ||ω||_{L²} for periodic div-free fields (Parseval identity). **[VERIFIED]**

### Results: Re=1000 (N=64)

| t | VS_actual | VS_Hölder | VS_bound | α_geom | α_Lad | α_sym | Product = Total |
|---|---|---|---|---|---|---|---|
| 0.157 | 3.05e+00 | 1.56e+02 | 3.99e+03 | 51.04 | 18.11 | 1.414 | 1307 |
| 0.433 | 8.59e+00 | 1.55e+02 | 4.22e+03 | 18.07 | 19.24 | 1.414 | 492 |
| 0.673 | 1.38e+01 | 1.56e+02 | 4.64e+03 | 11.29 | 21.10 | 1.414 | 337 |
| 0.956 | 2.07e+01 | 1.59e+02 | 5.48e+03 | 7.69 | 24.40 | 1.414 | 265 |
| 1.202 | 2.75e+01 | 1.66e+02 | 6.65e+03 | 6.04 | 28.29 | 1.414 | 242 |
| **1.369** | **3.27e+01** | **1.75e+02** | **7.77e+03** | **5.34** | **31.47** | **1.414** | **237.5** |
| 1.494 | 3.69e+01 | 1.83e+02 | 8.85e+03 | 4.96 | 34.19 | 1.414 | 240 |
| 1.747 | 4.64e+01 | 2.07e+02 | 1.19e+04 | 4.46 | 40.63 | 1.414 | 257 |
| 2.000 | 5.73e+01 | 2.43e+02 | 1.67e+04 | 4.24 | 48.63 | 1.414 | 292 |

### Results: Re=100 (N=48)

| t | VS_actual | VS_Hölder | VS_bound | α_geom | α_Lad | α_sym | Product = Total |
|---|---|---|---|---|---|---|---|
| 0.210 | 3.99e+00 | 1.53e+02 | 3.94e+03 | 38.36 | 18.23 | 1.414 | 989 |
| 0.638 | 1.20e+01 | 1.47e+02 | 4.30e+03 | 12.28 | 20.64 | 1.414 | 358 |
| 1.023 | 1.96e+01 | 1.46e+02 | 5.12e+03 | 7.45 | 24.78 | 1.414 | 261 |
| **1.423** | **2.80e+01** | **1.53e+02** | **6.65e+03** | **5.45** | **30.79** | **1.414** | **237.1** |
| 1.835 | 3.70e+01 | 1.70e+02 | 9.19e+03 | 4.58 | 38.29 | 1.414 | 248 |
| 2.444 | 4.93e+01 | 2.13e+02 | 1.50e+04 | 4.32 | 49.71 | 1.414 | 304 |
| 3.000 | 5.79e+01 | 2.65e+02 | 2.16e+04 | 4.57 | 57.69 | 1.414 | 373 |

### Key Finding: Corrected Decomposition at the 237× Point

At the time when total slack = 237× (the value from exploration-002): **[COMPUTED]**

| Factor | Re=100 (t≈1.42) | Re=1000 (t≈1.37) | Goal estimate | Corrected |
|---|---|---|---|---|
| α_geom (geometric/Hölder) | 5.45 | 5.34 | ~9 | **~5.4** |
| α_Lad (Ladyzhenskaya) | 30.79 | 31.47 | ~18.6 | **~31** |
| α_sym (symmetric) | 1.414 | 1.414 | ~1.4 | **√2** |
| **Total** | **237.1** | **237.5** | **~237** | **237** |

**The original estimates were significantly wrong.** The Ladyzhenskaya factor is ~31×, not ~18.6×, and the geometric factor is only ~5.3×, not ~9×.

### Time Dynamics of the Slack Factors

**[COMPUTED]**

- **α_geom** starts very large (>50) in the nearly-symmetric initial flow and drops to a minimum of ~4.2-4.6 at late times. The flow develops alignment structure over time, making the Hölder bound relatively tighter.
- **α_Lad** starts at ~18 (near the theoretical minimum for low-frequency flows) and grows monotonically as the flow develops multiscale structure. More small-scale structure means ∇ω grows faster than ω, making the L⁴ interpolation inequality relatively looser.
- **α_sym = √2 exactly** at all times — this is a mathematical identity, not a dynamical quantity.

The total slack has a **minimum around 237** at an intermediate time and grows both early (dominated by α_geom) and late (dominated by α_Lad).

### Log-Slack Budget at the 237× Point

Total log-slack = ln(237) = 5.47

| Source | Factor | ln(factor) | % of log-slack |
|---|---|---|---|
| Geometric alignment | 5.34 | 1.68 | **30.6%** |
| Ladyzhenskaya constant | 31.47 | 3.45 | **63.1%** |
| Symmetric factor | 1.414 | 0.35 | **6.3%** |
| **Total** | **237.5** | **5.47** | **100%** |

**The Ladyzhenskaya inequality is the dominant source of slack**, contributing 63% of the log-slack. The geometric alignment contributes 31%. The symmetric factor is negligible.

---

## Part B: Strain-Vorticity Alignment Statistics

### B1: Enstrophy-Weighted Alignment Evolution (Re=1000)

**[COMPUTED]** (code: `code/decomposition.py`, analysis: `code/alignment_analysis.py`)

| t | ⟨cos²θ₁⟩_ω | ⟨cos²θ₂⟩_ω | ⟨cos²θ₃⟩_ω | Depletion |
|---|---|---|---|---|
| 0.157 | 0.264 | 0.428 | 0.308 | 0.059 |
| 0.433 | 0.316 | 0.375 | 0.310 | 0.158 |
| 0.673 | 0.364 | 0.349 | 0.288 | 0.238 |
| 0.956 | 0.415 | 0.330 | 0.255 | 0.326 |
| **1.369** | **0.479** | **0.309** | **0.213** | **0.438** |
| 1.620 | 0.508 | 0.300 | 0.192 | 0.496 |
| 2.000 | 0.534 | 0.296 | 0.170 | 0.561 |

Isotropic expectation: ⟨cos²θ_i⟩ = 1/3 ≈ 0.333 for each.

**Key observations:** **[COMPUTED]**

1. **Vorticity preferentially aligns with the extensional strain eigenvector** (e₁, the direction of maximum stretching). At the 237× point: ⟨cos²θ₁⟩_ω = 0.479, which is 44% above the isotropic value.

2. **Vorticity avoids the compressive eigenvector** (e₃). At the 237× point: ⟨cos²θ₃⟩_ω = 0.213, which is 36% below isotropic.

3. **Intermediate alignment is near isotropic**: ⟨cos²θ₂⟩_ω ≈ 0.31 at the 237× point, only 7% below isotropic.

4. **The alignment evolves monotonically**: as the flow develops, vorticity becomes increasingly aligned with the extensional strain direction. At early times the alignment is actually anti-correlated (cos²θ₁ < 1/3).

5. **This is consistent with, but distinct from, fully-developed turbulence.** In homogeneous isotropic turbulence at high Re (Ashurst et al. 1987, Tsinober et al. 1992), vorticity preferentially aligns with the **intermediate** eigenvector e₂. Our Taylor-Green flow at moderate Re shows dominant alignment with e₁ instead, which is characteristic of transitional flows with organized vortex structures. **[CHECKED]** (against published DNS results)

### B2: Eigenvalue Structure (Re=1000)

**[COMPUTED]**

| t | ⟨λ₁⟩_ω | ⟨λ₂⟩_ω | ⟨λ₃⟩_ω | λ₂/λ₁ | λ₃/λ₁ | trace |
|---|---|---|---|---|---|---|
| 0.157 | +0.276 | +0.002 | -0.278 | 0.008 | -1.008 | ~0 |
| 0.673 | +0.298 | +0.026 | -0.323 | 0.086 | -1.086 | ~0 |
| **1.369** | **+0.332** | **+0.062** | **-0.394** | **0.186** | **-1.186** | **~0** |
| 2.000 | +0.367 | +0.106 | -0.472 | 0.288 | -1.288 | ~0 |

Trace check: λ₁ + λ₂ + λ₃ = 0 to machine precision (~10⁻¹⁶) at all times, confirming incompressibility. **[VERIFIED]**

The eigenvalue structure shows |λ₃| > λ₁ > λ₂ > 0 (the compressive eigenvalue is the strongest), with the intermediate eigenvalue λ₂ positive and growing over time. The ratio λ₂/λ₁ grows from 0.008 to 0.288, meaning the strain becomes less axisymmetric over time.

### B3: Constantin-Fefferman Depletion Factor

**[COMPUTED]**

The actual vortex stretching integral can be written as:

VS = ∫ (λ₁ cos²θ₁ + λ₂ cos²θ₂ + λ₃ cos²θ₃) |ω|² dx

The worst case would have all vorticity aligned with λ₁:

VS_worst = ∫ λ₁ |ω|² dx

The **depletion factor** = VS / VS_worst measures what fraction of maximum stretching is realized.

| t | Depletion Factor | Interpretation |
|---|---|---|
| 0.157 | 0.059 | Only 6% of max stretching — nearly isotropic |
| 0.673 | 0.238 | 24% |
| **1.369** | **0.438** | **44% of max stretching** |
| 2.000 | 0.561 | 56% |

The depletion factor increases monotonically from ~0.06 to ~0.56, meaning the flow goes from nearly isotropic alignment to significant (but not extreme) preferential alignment.

**Physical explanation of depletion:** Three mechanisms reduce the stretching below worst-case:
1. **Sign cancellation (53%):** The compressive term λ₃ cos²θ₃ |ω|² is negative, partially cancelling the extensional term. At the 237× point: λ₃⟨cos²θ₃⟩_ω = -0.084, which cancels 53% of λ₁⟨cos²θ₁⟩_ω = +0.159.
2. **Imperfect alignment:** Only 48% of the enstrophy-weighted alignment is with the extensional direction (vs. 100% in worst case).
3. **Intermediate contribution:** The intermediate eigenvalue λ₂ is positive but small, contributing a small positive term.

### B4: Alignment PDFs at Peak Enstrophy

**[COMPUTED]**

At peak enstrophy (t=2.0, Re=1000):
- **cos²θ₁ (extensional):** Bimodal distribution. Peak at cos²θ₁ ≈ 0 (many points with orthogonal vorticity) and at cos²θ₁ ≈ 1 (strongly aligned). Median = 0.59, P(cos²θ₁ > 0.5) = 0.53.
- **cos²θ₂ (intermediate):** Concentrated near cos²θ₂ ≈ 0 with a long tail. Median = 0.09, P(cos²θ₂ > 0.5) = 0.27.
- **cos²θ₃ (compressive):** Strongly concentrated near cos²θ₃ ≈ 0. Median = 0.01, P(cos²θ₃ > 0.5) = 0.17. Vorticity strongly avoids aligning with the compressive direction.

### B5: Vorticity Direction Gradient (Constantin-Fefferman Quantity)

**[COMPUTED]**

||∇ξ||_{L²} where ξ = ω/|ω| (computed via finite differences, restricted to regions where |ω| > threshold):

| t (Re=1000) | ||∇ξ||_{L²} |
|---|---|
| 0.157 | 38.1 |
| 0.673 | 41.8 |
| 1.369 | 48.2 |
| 2.000 | 56.1 |

The vorticity direction gradient grows monotonically, indicating that the vorticity direction field becomes more complex over time. This is the quantity in the Constantin-Fefferman regularity criterion: regularity holds as long as ||∇ξ|| remains bounded.

### B6: Physical Interpretation of α_geom ≈ 5.3

**[CONJECTURED]**

The geometric factor α_geom = ||S||_{L²} × ||ω||²_{L⁴} / |∫ Sωω dx| ≈ 5.3 at the 237× slack point. This means the Hölder/Cauchy-Schwarz inequality overestimates the actual vortex stretching by a factor of 5.3. Three physical mechanisms contribute:

1. **Spatial decorrelation between |S| and |ω|²:** The Cauchy-Schwarz bound assumes S and ωω are maximally correlated in space. In reality, regions of high strain and high enstrophy are correlated but not identical. This contributes roughly a factor of 2.

2. **Alignment structure:** At each point, Sωω = |ω|² Σ λ_i cos²θ_i. The Hölder bound replaces this signed sum with |S|×|ω|² (the Frobenius norm of S times enstrophy density). The actual sum has partial cancellation between extensional (positive) and compressive (negative) contributions. The enstrophy-weighted effective stretching rate is Σ λ_i ⟨cos²θ_i⟩_ω = 0.094, while the worst case is λ₁ = 0.332, giving a factor of ~3.5 from alignment alone.

3. **Combined effect:** The two factors interact nonlinearly, giving α_geom ≈ 5.3 rather than the simple product 2 × 3.5.

**Why α_geom is robust across Re:** At the 237× slack point, Re=100 gives α_geom = 5.45 and Re=1000 gives α_geom = 5.34. This is because the alignment statistics are remarkably similar at matching slack levels, suggesting the geometric factor is determined by the flow topology rather than the Reynolds number.

### B7: Cross-Re Comparison

**[COMPUTED]**

At the 237× total slack point:

| Quantity | Re=100 (t=1.42) | Re=1000 (t=1.37) |
|---|---|---|
| ⟨cos²θ₁⟩_ω | 0.474 | 0.479 |
| ⟨cos²θ₂⟩_ω | 0.312 | 0.309 |
| ⟨cos²θ₃⟩_ω | 0.214 | 0.213 |
| Depletion | 0.431 | 0.438 |
| ||∇ξ||_{L²} | 43.8 | 48.2 |
| α_geom | 5.45 | 5.34 |
| α_Lad | 30.79 | 31.47 |

The alignment statistics are nearly identical across Reynolds numbers at the same total slack level. This confirms that the geometric factor is a structural property of the Taylor-Green vortex topology.

---

## Part C: Sharp Ladyzhenskaya Constant on T³ for Div-Free Fields

### C1: Known Maximizer Survey

**[COMPUTED]** (code: `code/sharp_lad_focused.py`)

| Field | C_L = ||u||_{L⁴} / (||u||^{1/4}_{L²} ||∇u||^{3/4}_{L²}) | Div-free? |
|---|---|---|
| sin(x) e_y (single mode, |k|=1) | 0.2789 | Yes |
| ABC flow (A=B=C=1) | 0.2708 | Yes |
| Gaussian bump σ=0.5 (projected) | 0.2613 | Yes |
| Taylor-Green vortex | 0.1953 | Yes |
| R³ scalar sharp C_L | 0.6285 | — |
| R³ vector sharp C_L | 0.8271 | — |

### C2: Single-Mode Analytical Formula

**[VERIFIED]** (confirmed numerically to 6 digits)

For a single Fourier mode f = sin(k·x) on T³ = [0,2π]³:

C_L(|k|) = (3/8)^{1/4} × √2 / ((2π)^{3/4} × |k|^{3/4})

For |k| = 1: C_L = 0.2789. As |k| → ∞: C_L → 0 as |k|^{-3/4}.

Single modes cannot approach the R³ constant because they are spread uniformly in space. The R³ optimizer is a concentrated Gaussian — representing it on T³ requires superpositions of many high-frequency modes.

### C3: Effective Ladyzhenskaya Constant for the Taylor-Green Vortex

**[COMPUTED]**

The effective constant C_{L,eff} = ||ω||_{L⁴} / (||ω||^{1/4}_{L²} × ||∇ω||^{3/4}_{L²}) measures how close the flow's vorticity is to the Ladyzhenskaya optimizer:

| t (Re=1000) | C_{L,eff} | C²_{L,eff} | C²_L(R³) | α_Lad = C²_L/C²_{L,eff} |
|---|---|---|---|---|
| 0.157 | 0.194 | 0.0378 | 0.684 | 18.1 |
| 0.673 | 0.180 | 0.0324 | 0.684 | 21.1 |
| **1.369** | **0.147** | **0.0217** | **0.684** | **31.5** |
| 2.000 | 0.119 | 0.0141 | 0.684 | 48.6 |

The effective constant **decreases** over time as the flow develops more small-scale structure but remains smooth. At the 237× point, C_{L,eff} = 0.147, which is only 18% of the R³ constant.

### C4: Why the Ladyzhenskaya Slack is Large

**[CONJECTURED]**

The Ladyzhenskaya inequality on R³ has its optimizer at a concentrated, spike-like function (the Aubin-Talenti bubble). The Taylor-Green vortex is a smooth, spatially-extended flow — its vorticity field is spectrally concentrated at low wavenumbers, the opposite of the optimizer.

The sharp constant on T³ equals the R³ value C_L ≈ 0.827 (for vectors), achievable in the limit by concentrating a function at a point — this requires arbitrarily many Fourier modes. But for any smooth NS solution, the effective constant will be much smaller because:

1. NS solutions are analytic in space (Fourier coefficients decay exponentially)
2. The vorticity field is spatially extended, not concentrated
3. The ||ω||_{L⁴}/||ω||_{L²} ratio reflects the spatial distribution of enstrophy

This suggests that **the Ladyzhenskaya bound is structurally suboptimal for NS regularity** — it's designed for arbitrary Sobolev functions, not for the specific class of functions that arise as NS solutions.

---

## Summary of All Results

### Part A Verification Scorecard

| Claim | Tag | Evidence |
|---|---|---|
| α_geom × α_Lad × α_sym = total slack | **[VERIFIED]** | Exact match at all 30 timesteps, two Re values |
| α_sym = √2 for div-free fields | **[VERIFIED]** | Analytical proof + numerical check (5 random fields) |
| ||∇u|| = ||ω|| for periodic div-free | **[VERIFIED]** | Parseval identity + numerical check |
| α_geom ≈ 5.3 at 237× point | **[COMPUTED]** | Re=100: 5.45, Re=1000: 5.34 |
| α_Lad ≈ 31 at 237× point | **[COMPUTED]** | Re=100: 30.79, Re=1000: 31.47 |
| Ladyzhenskaya dominates (63% of log-slack) | **[COMPUTED]** | ln(31.47)/ln(237.5) = 0.631 |

### Part B Verification Scorecard

| Claim | Tag | Evidence |
|---|---|---|
| Vorticity aligns with extensional strain | **[COMPUTED]** | ⟨cos²θ₁⟩_ω = 0.479 vs isotropic 0.333 |
| Vorticity avoids compressive strain | **[COMPUTED]** | ⟨cos²θ₃⟩_ω = 0.213 vs isotropic 0.333 |
| Depletion factor ≈ 0.44 at 237× point | **[COMPUTED]** | Re=100: 0.431, Re=1000: 0.438 |
| Trace-free eigenvalues (incompressibility) | **[VERIFIED]** | λ₁+λ₂+λ₃ = O(10⁻¹⁶) at all points |
| Sign cancellation ≈ 53% | **[COMPUTED]** | |λ₃⟨cos²θ₃⟩|/(λ₁⟨cos²θ₁⟩) = 0.53 |
| Alignment consistent across Re | **[COMPUTED]** | Re=100 vs Re=1000 differ by <2% at matched slack |
| TGV shows extensional alignment (not intermediate) | **[CHECKED]** | Consistent with moderate-Re published results |

### Part C Verification Scorecard

| Claim | Tag | Evidence |
|---|---|---|
| Single-mode C_L = (3/8)^{1/4}√2/((2π)^{3/4}|k|^{3/4}) | **[VERIFIED]** | Analytical + numerical match to 6 digits |
| Best T³ div-free C found: 0.279 | **[COMPUTED]** | Single mode sin(x)e_y achieves this |
| C_{L,eff} ≈ 0.147 at 237× point | **[COMPUTED]** | Derived from simulation norms |
| T³ sharp constant = R³ constant | **[CONJECTURED]** | By approximation argument (periodized Gaussians) |
| Ladyzhenskaya structurally suboptimal for NS | **[CONJECTURED]** | NS solutions are smooth, optimizer is spike-like |
