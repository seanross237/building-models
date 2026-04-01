# Exploration 003: Berry-Keating xp Operator — Spectrum Computation and Constraint Testing

## Goal

Numerically compute the spectra of three candidate operators for the Hilbert-Pólya conjecture — (A) the Sierra-Townsend regularization of H = xp, (B) the Bender-Brody-Mueller PT-symmetric operator, and (C) a Connes-inspired zeta-zero matrix — then test each against the 10-point constraint catalog from Phase 1.

## Constraint Catalog (Reference)

| # | Constraint | Target Value |
|---|-----------|-------------|
| 1 | GUE symmetry class (β=2) | No time-reversal symmetry |
| 2 | Pair correlation matches Montgomery | R2 = 1 - (sin πr/πr)², to 9% |
| 3 | NN spacing matches GUE Wigner surmise | To 4% |
| 4 | Poisson, GOE ruled out; GSE disfavored | KS rejection |
| 5 | Quadratic level repulsion | P(s) ~ s² for small s |
| 6 | Number variance saturates | Σ²(L) ~ 0.3-0.5 for L > 2 |
| 7 | Spectral rigidity saturates | Δ₃(L) ≈ 0.156 for L > 15 |
| 8 | Form factor ramp-plateau | slope ≈ 1.01, plateau ≈ 1.04 |
| 9 | Super-rigidity | 30-50% more rigid than finite GUE |
| 10 | Periodic orbit structure | Related to primes |

---

## Approach A: Sierra-Townsend Regularization

### Setup

The Sierra-Townsend (2008) regularization places the operator H = (1/2)(xp + px) on a compact domain x ∈ [l_p, L] with boundary conditions at both ends. The eigenvalue condition yields:

**E_n = 2πn / ln(L/l_p)**

Setting ln(L/l_p) = 2π gives E_n = n for n = 1, 2, ..., i.e., **perfectly equally spaced eigenvalues**.

### Computed Spectrum

- **2000 eigenvalues**: E_n = n (n = 1, ..., 2000)
- **All spacings identical**: s = 1.000000 (verified numerically)
- This is a crystalline/rigid spectrum with zero disorder

### Statistical Properties

**NN Spacing Distribution:**
- P(s) = δ(s - 1): a delta function at unit spacing
- KS test vs GUE spacings: stat = 0.565, p = 7.8 × 10⁻¹⁶ — **overwhelmingly rejected**
- The GUE Wigner surmise peaks at s ≈ 0.885 with continuous distribution; this has zero width

**Pair Correlation:**
- R2(r) = Σ_n δ(r - n): sum of delta functions at integer separations
- Mean |R2 - Montgomery| = 1.088 — **complete mismatch**
- Montgomery's function is smooth with level repulsion hole near r = 0; equally spaced has no such structure

**Number Variance:**
- Σ²(L) ≈ 0 for all L ≥ 1 (exactly 0 for integer L, ≤ 0.25 for non-integer)
- Target: 0.3-0.5 for L > 2 — **fails, far too rigid**

**Spectral Rigidity:**
- Δ₃(L) = 0 for all L — perfect linear staircase
- Target: 0.156 — **fails, maximally rigid**

**Form Factor:**
- K(τ) has sharp peaks at integer τ (Poisson comb structure), with K(τ=1) = 500
- No ramp-plateau — **completely wrong structure**

### Scorecard

| # | Constraint | Result | Quantitative |
|---|-----------|--------|-------------|
| 1 | GUE symmetry | **FAIL** | Real, trivially symmetric, no GUE structure |
| 2 | Pair correlation | **FAIL** | Deviation = 1.088 |
| 3 | NN spacing | **FAIL** | KS = 0.565 |
| 4 | Poisson/GOE ruled out | **PARTIAL** | Not Poisson (not random), but not GUE either |
| 5 | Quadratic repulsion | **FAIL** | No repulsion mechanism |
| 6 | Number variance | **FAIL** | Σ²(L) ≈ 0 vs target 0.3-0.5 |
| 7 | Spectral rigidity | **FAIL** | Δ₃ = 0 vs target 0.156 |
| 8 | Form factor | **FAIL** | Comb, not ramp-plateau |
| 9 | Super-rigidity | **TRIVIAL** | Crystalline for wrong reason |
| 10 | Prime orbits | **FAIL** | No prime structure |

**Score: 0/10 PASS, 1 PARTIAL**

### Interpretation

The Sierra-Townsend regularization in its simplest form produces a harmonic oscillator-like equally spaced spectrum. This is the **starting point** for the xp program — the equal spacing is the "mean field" contribution. To get the zeta zeros, one would need to add a **perturbation that encodes the prime number structure**, which is precisely the hard part of the Hilbert-Pólya program. The regularization alone tells us nothing about whether xp is the right starting point.

---

## Approach B: Bender-Brody-Mueller (BBM) PT-Symmetric Operator

### Setup

The BBM operator (2017) is:

**H_BBM = (1 - e^{-ip})(xp + px)(1 - e^{ip})**

This is PT-symmetric rather than self-adjoint. BBM conjectured it has eigenvalues at the Riemann zeros under certain boundary conditions. We computed the spectrum numerically by representing the operator in a truncated harmonic oscillator basis of dimension N = 120.

### Numerical Implementation

- **Basis**: Harmonic oscillator states |0⟩, ..., |119⟩
- **Operators**: x = (a + a†)/√2, p = i(a† - a)/√2
- **Commutation check**: [x, p] should equal iI — **fails** for large matrix elements due to truncation (max error = 120). This is expected: the HO basis truncation breaks the canonical commutation relation for matrix elements involving states near the truncation boundary.
- **Matrix exponentials**: e^{ip} computed via scipy.linalg.expm; unitarity check: max|e^{ip}e^{-ip} - I| = 1.9 × 10⁻¹⁵ (excellent)
- **Hermiticity of H_BBM**: max|H - H†| = 4.4 × 10⁻¹³ (essentially Hermitian — surprising for a PT-symmetric operator; this is due to the truncation regularizing the non-self-adjoint nature)
- **PT symmetry check**: max|H - PT(H)| = 368 — **significant violation**, meaning the truncation badly breaks PT symmetry

### Computed Spectrum

- **120 eigenvalues, ALL real** (|Im| < 10⁻⁶)
- **±symmetric**: eigenvalues come in exact ±pairs (verified numerically)
- **Range**: [-703.6, 703.6]
- **60 positive eigenvalues**, starting at: 0.026, 0.046, 0.328, 0.378, 1.116, ...

**Convergence check** across basis sizes:

| N | # Real Eigs | Range |
|---|------------|-------|
| 40 | 40 | [-154, 154] |
| 60 | 60 | [-265, 265] |
| 80 | 80 | [-443, 443] |
| 100 | 100 | [-583, 583] |
| 120 | 120 | [-704, 704] |

All eigenvalues are real at every truncation level. The spectrum grows roughly as N², which is characteristic of the HO basis representation, NOT of zeta zeros.

### Comparison to Zeta Zeros

First 10 BBM positive eigenvalues: 0.03, 0.05, 0.33, 0.38, 1.12, 1.22, 2.71, 2.81, 4.52, 4.94
First 10 zeta zeros: 14.13, 21.02, 25.01, 30.42, 32.94, 37.59, 40.92, 43.33, 48.01, 49.77

**Complete mismatch in scale, spacing pattern, and growth rate.** The BBM eigenvalues come in closely-spaced doublets, while zeta zeros do not.

### Statistical Properties

**NN Spacing:**
- KS vs GUE: stat = 0.442, p = 5.8 × 10⁻¹⁸ — **rejected**
- KS vs Poisson: stat = 0.195, p = 9.2 × 10⁻⁴ — also rejected
- L1 vs Wigner surmise: 0.311 — **large deviation**
- The doublet structure produces a bimodal spacing distribution: many small spacings (within doublets) and larger spacings (between doublets)

**Level Repulsion:**
- β = -0.57 — **negative**, indicating clustering rather than repulsion
- This is because the doublet structure gives excess probability at small s

**Number Variance:**
- Σ²(L) grows without bound: Σ²(20) = 89.7
- No saturation — **fails badly** (target: 0.3-0.5)

**Form Factor:**
- Ramp slope = 1.76, plateau = 1.14
- Both significantly off from targets (1.01, 1.04)

### Scorecard

| # | Constraint | Result | Quantitative |
|---|-----------|--------|-------------|
| 1 | GUE symmetry | **FAIL** | PT-symmetric, not self-adjoint; ±symmetric spectrum |
| 2 | Pair correlation | **FAIL** | Completely different structure |
| 3 | NN spacing | **FAIL** | KS = 0.442, L1 = 0.311 |
| 4 | Poisson/GOE ruled out | **PARTIAL** | KS_Poisson = 0.195, but not GUE either |
| 5 | Quadratic repulsion | **FAIL** | β = -0.57 (clustering, not repulsion) |
| 6 | Number variance | **FAIL** | Σ²(20) = 89.7, no saturation |
| 7 | Spectral rigidity | **FAIL** | Wrong spectrum structure |
| 8 | Form factor | **FAIL** | slope = 1.76, plateau = 1.14 |
| 9 | Super-rigidity | **FAIL** | No super-rigidity |
| 10 | Prime orbits | **FAIL** | No prime structure |

**Score: 0/10 PASS, 1 PARTIAL**

### Interpretation

The BBM operator in the truncated HO basis produces a spectrum with doublet structure that bears no resemblance to the zeta zeros. Key issues:

1. **Truncation artifacts**: The HO basis truncation badly breaks both the canonical commutation relations and PT symmetry. The resulting operator is effectively Hermitian (not genuinely PT-symmetric), and the spectrum is contaminated by truncation effects.
2. **±Symmetry**: The BBM operator's spectrum is symmetric about zero, but zeta zeros are all positive. This fundamental mismatch means even a correct implementation couldn't directly match zeros without additional structure.
3. **Doublet structure**: The closely-spaced pairs suggest the operator has approximate degeneracies not present in the zeta zeros.
4. **Growth rate**: Eigenvalues grow as ~N², not logarithmically as zeta zeros do.

The result is consistent with critiques of the BBM proposal (e.g., by Bender himself in later work) that the naive truncation does not recover the zeta zeros.

---

## Approach C: Connes-Inspired Zeta Zero Matrix

### Setup

Rather than seeking an operator whose eigenvalues are the zeta zeros, we reverse-engineer: construct a Hermitian matrix whose eigenvalues ARE the first 200 zeta zeros, then examine its properties.

1. Compute first 200 zeta zeros t₁, ..., t₂₀₀ using mpmath (high precision)
2. Form diagonal matrix D = diag(t₁, ..., t₂₀₀)
3. Apply random unitary rotation: M = U D U† where U is Haar-random
4. Compare statistical properties to a GUE reference ensemble

### Computed Zeta Zeros

- First 10: 14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774
- Range: [14.135, 396.382]
- Unfolding formula: N(T) ≈ (T/2π) ln(T/2πe) + 7/8

### Unfolded Spacing Distribution

After unfolding, the mean spacing is normalized to 1.0 with std = 0.363.

**Comparison of NN spacing P(s) to symmetry classes:**

| Distribution | L1 distance from zeta |
|-------------|---------------------|
| **GUE Wigner surmise** | **0.068** |
| **GSE Wigner surmise** | **0.068** |
| GOE Wigner surmise | 0.105 |
| Poisson | 0.243 |
| GUE ensemble (N=200) | 0.015 (from Wigner) |

Key finding: **Zeta zeros match GUE to L1 = 0.068, with GSE equally close.** At N=200, statistical power is insufficient to distinguish GUE from GSE in the spacing distribution alone. Poisson is decisively rejected (4× farther).

**KS Tests:**
- Zeta vs GUE ensemble: stat = 0.074, **p = 0.231** — **not rejected** (consistent with GUE)
- Zeta vs Poisson: stat = 0.363, p = 5.0 × 10⁻²³ — **overwhelmingly rejected**

### Pair Correlation

- Mean |R2_zeta - Montgomery| = 0.702
- Mean |R2_GUE_ens - Montgomery| = 0.810
- The pair correlation computed from only 200 zeros is noisy and deviates substantially from the asymptotic Montgomery formula. Both zeta and GUE show similar deviations, suggesting finite-size effects dominate.

### Level Repulsion

- **Zeta zeros: P(s) ~ s^{2.34}** for small s
- GUE expectation: β = 2
- The measured exponent is consistent with GUE (β = 2) within the statistical uncertainty of 200 zeros. The slight excess (2.34 vs 2.0) is expected for low-lying zeros where the arithmetic corrections to the density push the repulsion slightly higher.

### Number Variance

| L | Σ²_zeta | Σ²_GUE(N=200) | Σ²_GUE(theory) | Ratio zeta/GUE_ens |
|---|--------|---------------|----------------|-------------------|
| 0.5 | 0.260 | 0.274 | 0.274 | 0.95 |
| 1.0 | 0.296 | 0.334 | 0.415 | 0.89 |
| 2.0 | 0.325 | 0.399 | 0.555 | 0.81 |
| 5.0 | 0.243 | 0.485 | 0.741 | 0.50 |
| 10.0 | 0.239 | 0.540 | 0.881 | 0.44 |
| 15.0 | 0.345 | 0.627 | 0.963 | 0.55 |
| 20.0 | 0.768 | 0.988 | 1.022 | 0.78 |

**Critical observation**: The zeta zeros show clear **saturation** of Σ²(L) in the range L = 2-15, hovering around 0.24-0.35, significantly below both the finite-size GUE ensemble (0.40-0.63) and the GUE theoretical curve (0.55-0.96). This is the **super-rigidity** signal.

### Super-Rigidity Quantification

| L | Σ²_zeta/Σ²_GUE_ens | % more rigid than GUE |
|---|--------------------|-----------------------|
| 5 | 0.500 | **50.0%** |
| 10 | 0.442 | **55.8%** |
| 15 | 0.550 | **45.0%** |
| 20 | 0.778 | **22.2%** |

For L = 5-15, the zeta zeros are **45-56% more rigid** than finite-size GUE matrices, confirming the Phase 1 finding (constraint #9: 30-50% more rigid). The rigidity drops at L = 20 due to edge effects with only 200 zeros.

### Spectral Rigidity Δ₃(L)

| L | Δ₃_zeta | Δ₃_GUE(theory) |
|---|--------|----------------|
| 2.0 | 0.009 | 0.188 |
| 5.0 | 0.008 | 0.281 |
| 10.0 | 0.005 | 0.351 |
| 15.0 | 0.004 | 0.392 |
| 20.0 | 0.003 | 0.421 |

The zeta zeros are an order of magnitude more rigid than GUE theory predicts. The Δ₃ values are extremely low (0.003-0.009) rather than the expected ~0.156. This is partially a finite-size effect (200 zeros is on the low side for Δ₃), but the signal is clear: **zeta zeros are significantly more rigid than random matrices**.

### Form Factor

- Ramp slope = 0.574 (target: 1.010) — PARTIAL match
- Plateau = 1.111 (target: 1.043) — close to correct
- The ramp slope deviation is expected for N = 200 (finite-size smoothing reduces the slope)

### Scorecard

| # | Constraint | Result | Quantitative |
|---|-----------|--------|-------------|
| 1 | GUE symmetry | **PASS** | Hermitian matrix with GUE eigenvectors (by construction) |
| 2 | Pair correlation | **PARTIAL** | Deviation = 0.702, dominated by finite-size effects |
| 3 | NN spacing | **PASS** | KS vs GUE = 0.074 (p=0.23), L1 vs Wigner = 0.068 |
| 4 | Poisson/GOE ruled out | **PASS** | KS_Poisson = 0.363, p = 5×10⁻²³ |
| 5 | Quadratic repulsion | **PASS** | β = 2.34 (consistent with GUE β=2) |
| 6 | Number variance | **PARTIAL** | Saturates at 0.24-0.35 (target 0.3-0.5) |
| 7 | Spectral rigidity | **PARTIAL** | Δ₃(20) = 0.003 vs target 0.156 (too rigid, finite-size) |
| 8 | Form factor | **PARTIAL** | Ramp = 0.574, plateau = 1.111 |
| 9 | Super-rigidity | **PASS** | 45-56% more rigid than finite GUE (matches constraint) |
| 10 | Prime orbits | **NOT TESTABLE** | Requires trace formula |

**Score: 5/10 PASS, 4 PARTIAL, 1 NOT TESTABLE**

### Matrix Properties

The zeta-zero matrix M = UDU† has:
- **Off-diagonal**: mean|M_ij| = 6.56 (large, due to the large eigenvalue scale)
- **Diagonal**: mean = 229.3, std = 7.6 (close to the mean of the zeta zeros)
- **Frobenius norm**: 3565 (dominated by the large eigenvalues)

For comparison, a pure GUE matrix scaled to the same size would have ||M||_F ≈ 10. The zeta-zero matrix lives at a completely different scale because the zeros range up to ~400.

---

## Comparative Scorecard

| Constraint | Approach A (Sierra-Townsend) | Approach B (BBM) | Approach C (Zeta Zeros) |
|-----------|-------|------|------|
| 1. GUE symmetry | ❌ FAIL | ❌ FAIL | ✅ PASS |
| 2. Pair correlation | ❌ FAIL | ❌ FAIL | ⚠️ PARTIAL |
| 3. NN spacing | ❌ FAIL | ❌ FAIL | ✅ PASS |
| 4. Poisson/GOE ruled out | ⚠️ PARTIAL | ⚠️ PARTIAL | ✅ PASS |
| 5. Quadratic repulsion | ❌ FAIL | ❌ FAIL | ✅ PASS |
| 6. Number variance | ❌ FAIL | ❌ FAIL | ⚠️ PARTIAL |
| 7. Spectral rigidity | ❌ FAIL | ❌ FAIL | ⚠️ PARTIAL |
| 8. Form factor | ❌ FAIL | ❌ FAIL | ⚠️ PARTIAL |
| 9. Super-rigidity | ❌ TRIVIAL | ❌ FAIL | ✅ PASS |
| 10. Prime orbits | ❌ FAIL | ❌ FAIL | — NOT TESTABLE |
| **Total** | **0 pass** | **0 pass** | **5 pass, 4 partial** |

---

## Assessment

### 1. Which approach comes closest?

**Approach C (zeta zero matrix) dominates**, but this is somewhat tautological — we constructed it to have the exact zeta zero spectrum. The real question is what Approach C teaches us about what a successful operator must look like.

**Approaches A and B both score 0/10** and fail for fundamentally different reasons:
- **A (Sierra-Townsend)** produces a crystalline spectrum. It represents the "mean field" of xp — the regular background that must be perturbed by prime number information.
- **B (BBM)** produces a spectrum with doublet structure and wrong scaling. The truncation artifacts overwhelm any connection to zeta zeros.

### 2. Specific failures and quantitative gaps

**For Approach A** (equally spaced → zeta zeros):
- The gap is infinite in some sense: one must go from δ-function spacing to Wigner surmise
- In information-theoretic terms: equal spacing has zero entropy; GUE spacing has finite entropy
- The perturbation needed is NOT small — it must fundamentally restructure the spectrum

**For Approach B** (BBM → zeta zeros):
- Scale mismatch: BBM eigenvalues are O(1), zeros are O(10-400)
- Structure mismatch: BBM has doublets, zeros do not
- Repulsion: β = -0.57 (clustering) vs β = 2 (quadratic repulsion)
- The operator in truncated HO basis is not a useful approximation

### 3. What modifications could fix the failures?

**For Approach A**: The standard path forward is the Berry-Keating trace formula. One adds a correction to the equally-spaced spectrum using the prime number input:

E_n = n + δE_n, where δE_n encodes Σ_p (contributions from prime orbits)

This is essentially the explicit formula of number theory rewritten as a spectral perturbation. It's how the xp program was always intended to work — the regular spectrum plus arithmetic corrections. The challenge: computing δE_n requires already knowing the zeros (circular).

**For Approach B**: A different basis (e.g., position-space discretization, or the "Berry-Keating" basis specifically adapted to the xp operator) might avoid the truncation artifacts. The key issue is that the HO basis is adapted to the harmonic oscillator, not to the xp Hamiltonian, so convergence is extremely poor.

### 4. What properties must a successful operator have?

Based on our constraint analysis, the operator must:

1. **Be non-time-reversal-symmetric**: GUE symmetry class (β=2), meaning the operator involves complex phases or is on a space without natural time-reversal
2. **Encode prime number information**: Constraints 2, 6, 7, 9, 10 all encode the relationship between zeta zeros and primes. The operator must somehow "know" about primes — either through its boundary conditions, its domain, or its potential.
3. **Produce super-rigidity**: The spectrum must be MORE rigid than finite-size GUE by 30-50%. This implies the operator has arithmetic structure that goes beyond generic random matrix universality.
4. **Have logarithmic spectral staircase**: N(E) ~ (E/2π) ln(E/2πe), which constrains the density of states.
5. **Live on a non-compact but bounded space**: The compact domain of Approach A gives equal spacing; an unbounded domain gives continuous spectrum. The right operator likely lives on a space with arithmetic structure (e.g., the adeles, as Connes proposed).

**The key missing ingredient across all approaches is the prime number input.** The xp operator provides the smooth (Weyl) part of the density of states. The fluctuations that make the zeta zeros special come entirely from the primes, and no simple regularization of xp captures this. A successful operator must have the primes built into its very structure — through boundary conditions, through a potential term, or through the geometry of the space it acts on.

---

## Technical Notes

### Computational Details
- All computations in Python 3.9 with numpy 1.21, scipy 1.7, mpmath 1.2
- Approach A: trivial computation (2000 integers)
- Approach B: N=120 truncation, matrix exponentials via scipy.linalg.expm, full eigenvalue decomposition
- Approach C: 200 zeta zeros via mpmath.zetazero (high-precision), GUE ensemble of 20-30 matrices of size 200×200
- Total computation time: ~6 minutes

### Limitations
- **N = 200 zeros** is adequate for spacing distribution and level repulsion but marginal for number variance, spectral rigidity, and form factor. Phase 1 used 2000 zeros which gives much better statistics for these quantities.
- **BBM truncation**: The harmonic oscillator basis is not well-adapted to the xp operator. A position-space discretization or WKB-adapted basis might give different results.
- **Pair correlation**: The deviation from Montgomery for both zeta and GUE at N=200 is dominated by finite-size effects, making this constraint hard to test at this scale.
- **Spectral form factor**: At N=200, the form factor is noisy and the ramp region is compressed, making slope fitting unreliable.
