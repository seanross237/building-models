# Exploration 006: Arithmetic Operator Construction — Von Mangoldt Toeplitz Matrix

## Goal
Construct operators directly from arithmetic functions (von Mangoldt, Möbius) as Toeplitz/Hankel matrices, compute their eigenvalues, and test whether their spectral statistics match GUE, GOE, or Poisson — particularly whether any arithmetic matrix produces zeta-zero-like statistics.

## Part 1: Von Mangoldt Toeplitz Matrix

### Construction
The von Mangoldt Toeplitz matrix T of size N×N is defined by:
- T_{ij} = Λ(|i-j|+1) for i ≠ j, where Λ is the von Mangoldt function
- T_{ii} = 0 (diagonal set to zero)

Λ(n) = ln(p) if n = p^k for some prime p, else 0. Its Dirichlet series is -ζ'(s)/ζ(s).

### Eigenvalue Results

| N | Range | Mean | Std | Near-zero (%) |
|---|-------|------|-----|---------------|
| 200 | [-45.22, 198.69] | 0.00 | 26.93 | 14.0% |
| 500 | [-110.57, 498.82] | 0.00 | 47.74 | 12.2% |
| 1000 | [-215.58, 997.74] | 0.00 | 72.59 | 12.6% |

### Key Observations — Part 1

1. **Enormous outlier eigenvalue**: The largest eigenvalue (~N) grows linearly with matrix size. This corresponds to the "DC component" — essentially the Chebyshev function ψ(N) ~ N by PNT. The eigenvector is approximately constant.

2. **Bulk spectrum**: The bulk eigenvalues form a roughly bell-shaped distribution centered near zero, with std growing as ~√N · C (std ≈ 2.3·√N).

3. **Density near zero**: About 12-14% of eigenvalues are near zero — smooth density passing through zero. No gap, no peak.

4. **Diagonal choice**: Setting T_{ii} = ln(2π) instead of 0 merely shifts all eigenvalues by ln(2π) ≈ 1.84. No qualitative change.

5. **Eigenvalue density shape**: Approximately Gaussian in the bulk, with a handful of isolated eigenvalues in the tail (the largest at ~N). This is characteristic of a structured low-rank perturbation.

---

## Part 2: Statistical Analysis of Eigenvalues (N=1000)

### Unfolding
After removing 18 outliers beyond ±2.5σ (leaving 982 bulk eigenvalues in [-145.6, 145.1]), eigenvalues were unfolded using cubic spline smoothing of the staircase function, then normalized to unit mean spacing.

### Nearest-Neighbor Spacing Distribution

| Statistic | Value |
|-----------|-------|
| **Chi² to Poisson** | **0.019** |
| Chi² to GOE | 0.838 |
| Chi² to GUE | 0.976 |
| **Best match** | **Poisson** |
| Spacing std | 0.895 (Poisson=1.0, GOE≈0.52, GUE≈0.42) |

The spacing distribution matches Poisson almost perfectly. The exponential decay exp(-s) describes the observed P(s) well, with large probability at s→0 and monotonic decay.

### Level Repulsion
**β = -0.31** (P(s) ~ s^β for s < 0.5)

This is *negative*, meaning eigenvalues actually *cluster* slightly more than Poisson at small spacings. This is the opposite of GUE (β=2) or GOE (β=1). There is zero level repulsion — eigenvalues are uncorrelated.

### Pair Correlation R₂(r)
The observed R₂(r) is approximately flat at ~0.3-0.4 for all r, bearing no resemblance to the GUE curve 1-(sin πr/πr)². The mean squared deviation from GUE pair correlation is 0.35 (enormous). This confirms complete absence of the correlations seen in zeta zeros.

### Number Variance Σ²(L)

| L | Σ²_obs | Σ²_Poisson | Σ²_GUE | obs/GUE |
|---|--------|------------|--------|---------|
| 0.5 | 0.492 | 0.500 | 0.674 | 0.73 |
| 1.0 | 0.886 | 1.000 | 0.814 | 1.09 |
| 2.0 | 1.351 | 2.000 | 0.955 | 1.42 |
| 5.0 | 1.361 | 5.000 | 1.141 | 1.19 |
| 10.0 | 1.053 | 10.000 | 1.281 | 0.82 |
| 20.0 | 1.204 | 20.000 | 1.422 | 0.85 |

The number variance is far below Poisson for large L (as expected for a structured matrix — it's not truly random). At small L, it tracks Poisson well. At large L, it actually shows some rigidity (Σ² saturates rather than growing linearly), but this rigidity is from the Toeplitz structure constraining the density, not from eigenvalue repulsion.

### Constraint Catalog Scorecard (Von Mangoldt Toeplitz)

| Constraint | Required | Observed | Pass? |
|-----------|----------|----------|-------|
| C2: Pair correlation = 1-(sinπr/πr)² | GUE | Flat ~0.35 | **FAIL** |
| C3: NN spacing = GUE Wigner surmise | s²e^(-4s²/π) | e^(-s) | **FAIL** |
| C4: Poisson/GOE ruled out | Not Poisson | **Is Poisson** | **FAIL** |
| C5: Level repulsion β=2 | β=2 | β=-0.31 | **FAIL** |
| C9: Super-rigidity | <GUE variance | ~GUE variance | Ambiguous |

**Score: 0/4 definite passes (possibly 0.5/5 with the ambiguous rigidity)**

---

## Part 3: Variants

### Variant A: Normalized von Mangoldt — a(n) = Λ(n)/√n (N=500)

The 1/√n decay makes entries more convergent but doesn't change the fundamental structure.

| Statistic | Value |
|-----------|-------|
| Eigenvalue range | [-9.00, 12.13] |
| **Best match** | **Poisson** (Chi²=0.034) |
| Chi² to GOE | 1.061 |
| Chi² to GUE | 0.573 |
| β (repulsion) | -0.34 |
| Spacing std | 0.920 |

**Result: Poisson.** Normalizing by √n does not introduce level repulsion. The spectrum is still uncorrelated.

### Variant B: Möbius Toeplitz — a(n) = μ(n) (N=500)

μ(n) is connected to 1/ζ(s). It takes values in {-1, 0, 1} — essentially a random-sign matrix with zeros at non-squarefree positions.

| Statistic | Value |
|-----------|-------|
| Eigenvalue range | [-42.27, 39.25] |
| **Best match** | **Poisson** (Chi²=0.034) |
| Chi² to GOE | 0.900 |
| Chi² to GUE | 0.686 |
| β (repulsion) | -0.36 |
| Spacing std | 0.922 |

**Result: Poisson.** Despite μ(n) being a very different arithmetic function from Λ(n), the Toeplitz matrix with μ(n) entries also produces Poisson statistics. The universality class appears to be determined by the Toeplitz structure, not the specific arithmetic function.

### Variant C: Log-zeta Hankel — H_{ij} = Λ(i+j) (N=500)

This uses Hankel structure instead of Toeplitz: H_{ij} = Λ(i+j). The key structural difference is that Hankel matrices have constant anti-diagonals, while Toeplitz matrices have constant diagonals.

| Statistic | Value |
|-----------|-------|
| Eigenvalue range | [-125.49, 125.30] |
| **Best match** | **Poisson** (barely; Chi²=0.056) |
| Chi² to GOE | **0.065** (very close!) |
| Chi² to GUE | 0.327 |
| β (repulsion) | **0.44** |
| Spacing std | **0.72** |

**Result: INTERMEDIATE between Poisson and GOE — much closer to GOE than any Toeplitz variant.**

This is the most interesting finding. The Hankel matrix shows:
- **Partial level repulsion** (β=0.44, between Poisson=0 and GOE=1)
- **Reduced spacing fluctuation** (std=0.72, between Poisson=1.0 and GOE≈0.52)
- **Nearly equal chi² to Poisson and GOE** (0.056 vs 0.065)
- **Number variance at L=10 matches GUE almost perfectly** (ratio = 1.005!)

Number variance for Variant C:

| L | Σ²_obs | Σ²_GUE | Ratio |
|---|--------|--------|-------|
| 1 | 0.617 | 0.814 | 0.76 |
| 5 | 1.346 | 1.141 | 1.18 |
| 10 | 1.287 | 1.281 | **1.00** |

---

## Part 4: Assessment

### 1. Which matrix has GUE-like statistics?

**None match GUE.** All three Toeplitz variants (original, normalized, Möbius) are firmly Poisson. The Hankel variant is the closest to any random matrix ensemble, sitting between Poisson and GOE — but not GUE.

### 2. Does any arithmetic matrix produce super-rigidity?

**No.** The Toeplitz variants have number variance comparable to GUE at some scales (by coincidence, not mechanism). The Hankel variant's L=10 match is striking but appears coincidental — it doesn't hold across all L values, and the spacing distribution is not GUE.

### 3. Universality class of each variant

| Matrix | Universality Class |
|--------|-------------------|
| Von Mangoldt Toeplitz | **Poisson** (β=-0.31, std=0.90) |
| Normalized von Mangoldt Toeplitz | **Poisson** (β=-0.34, std=0.92) |
| Möbius Toeplitz | **Poisson** (β=-0.36, std=0.92) |
| Von Mangoldt Hankel | **Intermediate Poisson-GOE** (β=0.44, std=0.72) |

### 4. Novel observations

**The Toeplitz vs. Hankel dichotomy is the key finding.**

Both use the same arithmetic function Λ(n) and the same matrix size. The only difference is the index structure:
- **Toeplitz**: T_{ij} = Λ(|i-j|+1) — entries depend on the *difference* of indices → **Poisson**
- **Hankel**: H_{ij} = Λ(i+j) — entries depend on the *sum* of indices → **Partial GOE**

This suggests that for arithmetic matrices:
- The **convolution structure** (Toeplitz = diagonal in Fourier space) kills correlations. Toeplitz matrices are diagonalized by the DFT, so eigenvalues are essentially samples of a Fourier transform — and Fourier transforms of arithmetic functions oscillate independently → Poisson.
- The **Hankel structure** introduces coupling between different "frequencies" that creates partial eigenvalue repulsion.

**Why this matters for the Riemann Hypothesis spectral program:**
1. Simply encoding prime structure into a matrix is NOT sufficient to get GUE statistics.
2. The matrix structure (how indices map to function arguments) matters more than the arithmetic content.
3. The Hankel structure moves toward GOE but not GUE — suggesting that getting β=2 requires something beyond simple arithmetic encoding.
4. The trace formula argument (exploration 004) said density is determined but correlations are not. This computation confirms it empirically: we have the right spectral density (determined by Λ(n)) but wrong correlations (Poisson instead of GUE).

### 5. Theoretical explanation for Poisson statistics of Toeplitz matrices

For a real symmetric Toeplitz matrix with first row [c₀, c₁, ..., c_{N-1}], the eigenvalues are approximately given by sampling the spectral function f(θ) = c₀ + 2Σ cₖ cos(kθ) at N quasi-equally-spaced points. For arithmetic functions, f(θ) is highly irregular (it's essentially a trigonometric polynomial with prime-structured coefficients), and the sampling points are deterministic → Poisson statistics are expected.

This is a known result in random matrix theory: **deterministic Toeplitz matrices generically have Poisson statistics** unless the generating sequence has very specific correlation structure (e.g., i.i.d. random entries, which would give GOE).

### 6. Path forward

To get GUE from arithmetic data, one likely needs:
- **Non-trivial mixing**: The matrix should not be diagonalizable by a simple transform like DFT
- **Time-reversal symmetry breaking**: GUE requires complex-valued matrices (β=2). All matrices here are real symmetric → at best GOE (β=1)
- **The Hilbert-Pólya operator** likely cannot be a simple Toeplitz or Hankel matrix with arithmetic entries. It must have a more sophisticated structure that produces the specific eigenvalue repulsion seen in zeta zeros.

The most promising direction is the Hankel matrix with complex-valued entries (e.g., using Λ(n)·e^{iθ(n)} for some phase function θ), which could potentially break time-reversal symmetry and push from GOE toward GUE.
