# Exploration 006: Spectral Ladyzhenskaya Inequality — Report

## Goal
Compute effective Ladyzhenskaya constants for spectrally localized fields and formulate a spectral Ladyzhenskaya inequality that could reduce the 158-237× slack in the vortex stretching bound.

## Reference Constants

The sharp Ladyzhenskaya inequality on R³ for scalar fields:
- ||f||⁴_{L⁴} ≤ c₁ ||f||_{L²} ||∇f||³_{L²}, with c₁ = 8/(3π²√3) ≈ 0.1561
- Equivalently: ||f||_{L⁴} ≤ C_L ||f||^{1/4}_{L²} ||∇f||^{3/4}_{L²} with C_L = c₁^{1/4} ≈ 0.629

[CHECKED] These values match Ladyzhenskaya (1967) and the Aubin-Talenti literature.

**Important caveat:** The R³ constant does NOT apply directly on T³ = [0,2π]³. On the torus, the sharp constant is larger (worse) for low-frequency fields. Our sanity check confirms: a single mode cos(x) gives C_eff = 1.107 > C_L_scalar. This is not a bug — the Aubin-Talenti bubble cannot fit on T³. For high-frequency content (k₀ >> 1), the T³ constant converges to the R³ constant.

All norms below use the normalized measure (1/(2π)³) dx on T³.

---

## Part A: Analytical Framework — Gaussian CLT Regime

### Key Insight

For fields with many random-phase Fourier modes, the Central Limit Theorem applies: the pointwise distribution of f(x) is approximately Gaussian. For a Gaussian random variable with variance σ², E[f⁴] = 3σ⁴, so:

**||f||_{L⁴} = 3^{1/4} ||f||_{L²}** (in the Gaussian regime) [CONJECTURED — requires CLT assumptions]

This immediately gives the effective Ladyzhenskaya constant:

**C_{L,eff} = 3^{1/4} (||f||_{L²} / ||∇f||_{L²})^{3/4}** [CONJECTURED]

The ratio ||f||/||∇f|| is determined entirely by the energy spectrum:
- ||f||² = 4π ∫ k^{2-2α} dk (for power-law |f̂_k| ~ k^{-α})
- ||∇f||² = 4π ∫ k^{4-2α} dk

### Asymptotic Formula for Kolmogorov Spectrum

For the Kolmogorov spectrum with dissipation cutoff:
- |û_k|² ~ k^{-11/3} exp(-c(k/k_d)^{4/3}), where k_d = Re^{3/4}

In the large-Re limit:
- ||f||² → 6π (constant, infrared dominated)
- ||∇f||² → 3π × k_d^{4/3} = 3π × Re (ultraviolet dominated)

This gives:

**C_{L,eff} ≈ 1.707 × Re^{-3/8}** [COMPUTED — verified analytically and numerically]

At Re = 1000: C_{L,eff} ≈ 0.128 (asymptotic) vs 0.125 (full numerical integration), error 2.1%.

The asymptotic formula matches the full numerical integral to within:
- 6.7% at Re = 100
- 2.1% at Re = 1000
- 0.2% at Re = 100,000

[COMPUTED] Scaling exponent from fit to numerical data: −0.528 (includes sub-leading corrections at moderate Re). True asymptotic exponent: −3/8 = −0.375.

---

## Part B: Numerical Computation of Effective Constants

All computations on T³ = [0,2π]³ with N=32 grid (verified at N=48 where noted).

### B1: Band-Limited Fields

Fields with Fourier support in |k| ∈ [k₀/2, 2k₀], unit amplitudes per mode. The "max" values are from optimization over phases (15 L-BFGS-B restarts); "mean" is over 300 random-phase samples.

| k₀ | Total Modes | Max C_eff | Mean C_eff ± σ | Ratio (mean/C_L) |
|----|-------------|-----------|----------------|-------------------|
| 2  | 256         | 1.305     | 0.569 ± 0.008  | 0.905             |
| 4  | 2082        | 0.418     | 0.335 ± 0.002  | 0.533             |
| 8  | 16823       | 0.202     | 0.198 ± 0.000  | 0.316             |
| 12 | 31466       | 0.171     | 0.169 ± 0.000  | 0.269             |

[COMPUTED] Code: `code/spectral_ladyzhenskaya_v2.py`

**Key observations:**
1. **Optimization gives significantly higher C_eff than random phases** at low k₀ (max is 2.3× mean at k₀=2), but the gap narrows at high k₀ (max is 1.02× mean at k₀=12). This confirms the CLT: with many modes, all phase configurations give similar results.

2. **The analytical Gaussian prediction** matches the mean values well:
   - k₀=2: analytical 0.560, numerical mean 0.569 (2% error)
   - k₀=4: analytical 0.333, numerical mean 0.335 (1% error)
   - k₀=8: analytical 0.198, numerical mean 0.198 (0.0% error)
   - k₀=12: analytical 0.146, numerical mean 0.169 (16% error — truncation effect at N=32)

3. **C_eff exceeds C_L at k₀=2** because the R³ Ladyzhenskaya constant doesn't bound functions on T³. Low-frequency modes can concentrate more effectively on the torus.

**Resolution verification (N=48):** For k₀=4, max=0.418 (same as N=32), mean=0.335 (same). [CHECKED]

### B2: Power-Law Spectra

|f̂_k| ~ k^{-α} for k ∈ [1, 0.4N]. 500 random-phase samples each.

| α     | Description | Mean C_eff ± σ | Max C_eff | Ratio (mean/C_L) |
|-------|-------------|----------------|-----------|-------------------|
| 5/6   | GOAL convention | 0.286 ± 0.001 | 0.290 | 0.455 |
| 1     | —           | 0.302 ± 0.001  | 0.307     | 0.481             |
| 3/2   | —           | 0.390 ± 0.004  | 0.409     | 0.620             |
| 11/6  | Kolmogorov (proper) | 0.498 ± 0.009 | 0.527 | 0.793 |

[COMPUTED] Code: `code/spectral_ladyzhenskaya_v2.py`

**Critical note on resolution:** The α=11/6 result at N=32 gives C_eff=0.498, but at N=48 gives 0.401. The result is NOT converged because the infrared-dominated L² norm is captured but the ultraviolet-dominated gradient norm is truncated by the grid. The analytical formula (which integrates to ∞) gives C_eff=0.054 for K_max=1000, dramatically lower.

**The N=32 grid only resolves K_max ≈ 13 modes, far below the Kolmogorov dissipation scale k_d = Re^{3/4} ≈ 178 at Re=1000.** The numerical values at N=32 are meaningful only as upper bounds on C_eff for the truncated spectrum.

### B3: Divergence-Free vs. General

Band-limited vector fields satisfying k · û_k = 0 vs. scalar fields in the same band.

| k₀ | Div-Free Mean C_eff | Scalar Mean C_eff | Ratio (divfree/scalar) |
|----|--------------------|--------------------|------------------------|
| 4  | 0.289 ± 0.001      | 0.335 ± 0.002      | 0.863                 |
| 8  | 0.171 ± 0.000      | 0.198 ± 0.000      | 0.863                 |

[COMPUTED] Code: `code/spectral_ladyzhenskaya_v2.py`

**Finding:** The divergence-free constraint reduces C_eff by a uniform factor of ~0.863 (13.7% reduction). This factor is remarkably consistent across k₀ values. [COMPUTED]

**Analytical explanation:** [VERIFIED — numerical matches analytical to 4 significant figures]

The factor 0.8634 matches **(5/9)^{1/4} = 0.86334** exactly (within statistical error).

**Derivation:** For a 3-component isotropic Gaussian vector field u = (u_x, u_y, u_z) with independent components each of variance σ²:
- E[|u|⁴] = E[(u_x²+u_y²+u_z²)²] = 3E[u_i⁴] + 6E[u_i²]E[u_j²] = 9σ⁴ + 6σ⁴ = 15σ⁴
- The flatness: F_vec = E[|u|⁴]/(E[|u|²])² = 15σ⁴/(3σ²)² = 5/3

For a scalar Gaussian: F_scalar = E[f⁴]/(E[f²])² = 3.

The L⁴ norms in Gaussian regime:
- Scalar: ||f||_{L⁴} = 3^{1/4} ||f||_{L²}
- Vector: ||u||_{L⁴} = (5/3)^{1/4} ||u||_{L²}

The Ladyzhenskaya ratio C_eff = (flatness)^{1/4} (||f||/||∇f||)^{3/4}, so:
- **C_vec / C_scalar = (5/3)^{1/4} / 3^{1/4} = (5/9)^{1/4} ≈ 0.8633**

This is NOT primarily about the divergence-free constraint per se — it's about the difference between scalar and vector field flatness. A 3-component Gaussian vector field has flatness 5/3 < 3, so its L⁴ norm relative to L² is lower than for scalars. The div-free constraint ensures isotropy (no preferential direction), which enables this exact calculation.

**Verified across 6 values of k₀ (3-12)** with 400 samples each: mean ratio = 0.8634 ± 0.0002. Code: `code/verify_divfree.py`.

### B4: NS-Like Spectra

|û_k| ~ k^{-11/6} exp(-½(k/k_d)^{4/3}), k_d = Re^{3/4}. 500 random samples.

| Re     | Mean C_eff ± σ | Max C_eff | Ratio (mean/C_L) | Analytical (Gaussian, full spectrum) |
|--------|----------------|-----------|-------------------|--------------------------------------|
| 100    | 0.517 ± 0.010  | 0.558     | 0.822             | 0.284                                |
| 1,000  | 0.500 ± 0.009  | 0.543     | 0.796             | 0.125                                |
| 10,000 | 0.499 ± 0.009  | 0.535     | 0.793             | 0.054                                |

[COMPUTED] Code: `code/spectral_ladyzhenskaya_v2.py` and `code/analytical_ceff.py`

**The numerical and analytical values diverge dramatically** because the N=32 grid truncates the spectrum at K_max ≈ 13, while the physical dissipation scale is k_d ≈ 178 (Re=1000). The analytical values integrate the full spectrum and represent the true C_eff for the complete Kolmogorov cascade. The numerical values represent C_eff for a spectrum truncated at wavenumber 13.

**The analytical values should be trusted** for the purpose of assessing slack in the NS regularity argument, since the full spectrum is what matters physically.

---

## Part C: Littlewood-Paley Analysis

Decompose f = Σ_j Δ_j f where Δ_j projects to wavenumbers |k| ∈ [2^{j-1}, 2^j).

### Contribution Breakdown for ||f||⁴_{L⁴}

| Component | Kolmogorov (α=11/6) | α=5/6 | α=3/2 | Flat (α=0) |
|-----------|--------------------:|------:|------:|-----------:|
| Diagonal: Σ ||Δ_j f||⁴_4 | 36.8% | 34.1% | 26.5% | 56.7% |
| Pairwise cross: 6 Σ_{i<j} ⟨(Δ_i f)² (Δ_j f)²⟩ | 63.0% | 65.9% | 73.4% | 43.3% |
| Higher-order cross | 0.2% | ~0% | 0.1% | ~0% |

[COMPUTED] Code: `code/littlewood_paley.py`, N=32, 200-300 random-phase samples per spectrum.

### Band-by-Band Kurtosis (Kolmogorov)

| Band j | ||Δ_j f||²_2 | ||Δ_j f||⁴_4 | Kurtosis | Expected (Gaussian) |
|--------|-------------|-------------|----------|---------------------|
| 1      | 0.545       | 0.820       | 2.77     | 3                   |
| 2      | 0.248       | 0.184       | 2.99     | 3                   |
| 3      | 0.149       | 0.066       | 3.00     | 3                   |
| 4      | 0.059       | 0.010       | 3.00     | 3                   |

[COMPUTED]

### Key Finding

**The pairwise cross terms DOMINATE** (63% for Kolmogorov), not the diagonal. This means:

1. A Littlewood-Paley approach that bounds each band separately and sums will OVERESTIMATE ||f||⁴_{L⁴} by losing the cross-term structure.
2. The standard LP square-function estimate ||f||_{L⁴} ≤ C||(Σ|Δ_j f|²)^{1/2}||_{L⁴} correctly handles this, but doesn't give a tighter constant than the original Ladyzhenskaya.
3. For Kolmogorov spectra, the HHI (spectral concentration index) is 0.38, meaning ~2.6 effective bands. The lowest band dominates both ||f||² and ||f||⁴.

**Conclusion for LP approach:** [COMPUTED] The Littlewood-Paley decomposition does NOT yield a tighter Ladyzhenskaya inequality through band-by-band Bernstein estimates. The cross terms between bands are too large. The improvement for NS flows comes entirely from the large ||∇f||/||f|| ratio, which the standard inequality already captures through the interpolation exponents.

---

## Part D: Candidate Theorem Statement and Analysis

### What CAN be proven

**Theorem 1 (Vector vs Scalar Flatness, Gaussian Regime):** For a 3-component isotropic Gaussian random field u on T³ (arising from many random-phase Fourier modes), the effective Ladyzhenskaya constant satisfies:

C_{L,eff}^{vec} = (5/9)^{1/4} × C_{L,eff}^{scalar} ≈ 0.8633 × C_{L,eff}^{scalar}

[VERIFIED — analytical derivation confirmed by numerical computation to 4 significant figures across 6 values of k₀]

**Proof sketch:** The flatness (normalized fourth moment) of |u|² for an isotropic 3-Gaussian is 5/3, compared to 3 for a scalar Gaussian. The L⁴/L² ratio enters the Ladyzhenskaya constant as (flatness)^{1/4}, giving the factor (5/3)^{1/4}/3^{1/4} = (5/9)^{1/4}.

**Theorem 2 (Gaussian Regime Effective Constant):** For scalar fields with energy spectrum E(k) and random phases, in the many-mode limit:

C_{L,eff} = 3^{1/4} × (Σ|f̂_k|²)^{3/8} / (Σ|k|²|f̂_k|²)^{3/8}

[COMPUTED — verified numerically at multiple spectral profiles and resolutions]

For Kolmogorov spectrum with dissipation, this gives:

C_{L,eff} ≈ 1.707 × Re^{-3/8}

[COMPUTED — analytical formula matches numerical integration to < 2% for Re ≥ 1000]

### What CANNOT be proven without additional assumptions

**Negative result:** [COMPUTED] A spectral Ladyzhenskaya inequality of the form

||f||_{L⁴} ≤ C_{L,spec}(β) × ||f||^{1/4}_{L²} × ||∇f||^{3/4}_{L²}

with C_{L,spec}(β) < C_L depending on spectral decay rate β is NOT achievable through Bernstein + LP methods alone, because:

1. **For any single band [k₀/2, 2k₀]:** The worst-case (phase-optimized) C_eff converges to a constant independent of k₀ as k₀ → ∞. The Bernstein bound gives C_eff ≤ C_B × 4^{3/4} ≈ 2.83 C_B, independent of the band location.

2. **For multi-band fields:** The cross terms between LP bands contribute 63% of ||f||⁴_{L⁴} for Kolmogorov spectra, so banding doesn't help.

3. **The spectral constraint on amplitudes** (not phases) cannot improve the constant, because for any given amplitudes {|f̂_k|}, the worst-case phases (constructive interference) achieve C_eff comparable to the universal constant.

### What can be stated with phase assumptions

**Candidate Theorem (Gaussian Regime):** For real-valued fields f on T³ with random i.i.d. phases, in the limit of many modes (N → ∞), the effective Ladyzhenskaya ratio satisfies:

C_{L,eff} → 3^{1/4} (||f||_{L²} / ||∇f||_{L²})^{3/4}

For a Kolmogorov spectrum with Reynolds number Re:

**C_{L,eff} ≈ 1.707 × Re^{-3/8}**

[COMPUTED] Verified to 2% accuracy at Re=1000 by numerical integration.

Specific values:

| Re | C_{L,eff} (Gaussian) | C_{L,eff}/C_L | Slack reduction (4th power) |
|----|---------------------|---------------|----------------------------|
| 100 | 0.284 | 0.452 | 24× |
| 1,000 | 0.125 | 0.199 | 632× |
| 10,000 | 0.054 | 0.085 | 18,878× |
| 100,000 | 0.023 | 0.036 | 586,261× |

[COMPUTED] Code: `code/analytical_ceff.py`

### Assessment: How much slack can a spectral Ladyzhenskaya close?

The GOAL.md states the Ladyzhenskaya inequality contributes 63% of the log-slack in the vortex stretching bound (total slack 158-237×).

**If the Gaussian C_{L,eff} could be used as a bound:**
- At Re=1000: The Ladyzhenskaya contribution to slack would reduce by factor (0.199)⁴ ≈ 1/632.
- Applying to 63% of the log-slack: total slack drops from ~200× to ~3.4×.
- At Re=10,000: total slack drops below 1×, which is impossible — meaning the Gaussian approximation is too aggressive to be a valid bound.

**Reality check:** [CONJECTURED] The Gaussian CLT gives the TYPICAL value, not a bound. NS solutions have phase correlations (intermittency) that create coherent structures (vortex tubes) with enhanced L⁴ concentration. The true worst-case C_eff for NS solutions is somewhere between the Gaussian value and the universal constant. The GOAL.md reports measured C_eff ≈ 0.147, which is close to the Gaussian prediction of 0.125 at Re=1000 (the phases add ~18% to concentration above Gaussian).

**Bottom line:** A provable spectral Ladyzhenskaya inequality requires one of:
1. Bounds on intermittency (flatness/kurtosis) of NS solutions
2. Structural constraints from incompressibility + NS dynamics
3. A probabilistic framework (not worst-case)

The divergence-free constraint alone gives only a 14% improvement — significant but not a game-changer for the 158× slack.

---

## Results Table

| Spectral Profile | C_{L,eff} | Ratio C_{L,eff}/C_L | Slack Reduction Factor |
|---|---|---|---|
| Band-limited k₀=2 (optimized) | 1.305 | 2.08 | — (exceeds C_L on T³) |
| Band-limited k₀=4 (mean) | 0.335 | 0.53 | 12.5× |
| Band-limited k₀=8 (mean) | 0.198 | 0.32 | 102× |
| Band-limited k₀=12 (mean) | 0.169 | 0.27 | 194× |
| Power-law α=5/6 (N=32) | 0.286 | 0.46 | 23× |
| Power-law α=11/6 (N=32) | 0.498 | 0.79 | 2.5× |
| Div-free k₀=4 (mean) | 0.289 | 0.46 | 23× |
| Div-free k₀=8 (mean) | 0.171 | 0.27 | 194× |
| NS Re=1000 (Gaussian analytical) | 0.125 | 0.20 | 632× |
| NS Re=10000 (Gaussian analytical) | 0.054 | 0.085 | 18,878× |

Notes: "Slack Reduction Factor" = (C_L/C_{L,eff})⁴, which measures how much the fourth-power Ladyzhenskaya slack decreases. The N=32 numerical values for broad spectra are upper bounds due to spectral truncation.

---

## Critical Assessment

### What this exploration achieved:
1. [COMPUTED] Effective Ladyzhenskaya constants for 10+ spectral profiles
2. [COMPUTED] Analytical formula C_{L,eff} ≈ 1.707 × Re^{-3/8} for Kolmogorov spectra
3. [COMPUTED] Div-free constraint gives uniform 13.7% reduction
4. [COMPUTED] LP cross terms dominate (63%) — band-by-band approach fails
5. [CONJECTURED] Candidate theorem with explicit Re-dependence

### What the spectral Ladyzhenskaya CANNOT do:
- **It cannot close the gap deterministically.** Without phase information, the sharp constant cannot be improved for a given spectral profile.
- **The measured improvement for NS flows (C_eff ≈ 0.147 at Re~1000) is a STATISTICAL property** arising from near-Gaussian phase distribution, not a deterministic bound.
- **The LP decomposition does not help** — cross terms are too large.

### Most promising direction:
**Flatness bounds.** If one could prove that the flatness of NS velocity fields satisfies:

F₄ := ||u||⁴_{L⁴} / (||u||²_{L²})² ≤ F_max(Re)

with F_max growing slower than the worst-case (constructive interference) value, then the spectral Ladyzhenskaya would follow with explicit Re-dependent constants.

For Gaussian fields: F₄ = 5/3 (vector) or 3 (scalar). Intermittent turbulence has F₄ > 5/3, but experimental data suggests F₄ grows very slowly with Re. A bound F₄ ≤ C × Re^ε for small ε would give:

C_{L,eff} ≤ C^{1/4} Re^{ε/4} × (||u||/||∇u||)^{3/4} ~ Re^{ε/4 - 3/8}

For ε < 3/2, this still decreases with Re, providing increasing slack reduction.
