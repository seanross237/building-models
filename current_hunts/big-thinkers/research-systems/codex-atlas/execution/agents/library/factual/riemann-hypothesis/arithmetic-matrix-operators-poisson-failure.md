---
topic: Arithmetic matrix operators (Toeplitz/Hankel) fail to produce GUE statistics
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-006"
---

## Finding

Numerical experiments with Toeplitz and Hankel matrices constructed from arithmetic functions (von Mangoldt Λ(n), Möbius μ(n)) all fail to produce GUE statistics. Three Toeplitz variants yield Poisson statistics; the Hankel variant reaches only an intermediate Poisson-GOE regime. None approach the GUE statistics of actual Riemann zeta zeros.

## Matrices Tested

### Von Mangoldt Toeplitz (N=200, 500, 1000)

T_{ij} = Λ(|i-j|+1) for i≠j, diagonal set to zero. The largest eigenvalue (~N) is the "DC component" from the Prime Number Theorem (ψ(N) ~ N). Bulk eigenvalues have std growing as ~2.3·√N.

After removing outliers (18 of 1000 eigenvalues beyond ±2.5σ) and unfolding 982 bulk eigenvalues:

| Statistic | Value |
|-----------|-------|
| Chi² to **Poisson** | **0.019** (best match) |
| Chi² to GOE | 0.838 |
| Chi² to GUE | 0.976 |
| Level repulsion β | **-0.31** (negative — clusters MORE than Poisson) |
| Spacing std | 0.895 (Poisson=1.0, GOE≈0.52, GUE≈0.42) |
| Pair correlation R₂(r) | Flat at ~0.3–0.4 (GUE: 1-(sinπr/πr)²) |
| Deviation from GUE pair corr | 0.35 (enormous) |

**Constraint Scorecard:** 0/4 definite passes (C2 pair corr, C3 spacing, C4 not-Poisson, C5 level repulsion β=2 all FAIL).

### Variants (N=500)

| Matrix | Best Match | β | Spacing std | Chi² best |
|--------|------------|---|-------------|-----------|
| Normalized von Mangoldt Toeplitz [Λ(n)/√n] | **Poisson** | -0.34 | 0.920 | 0.034 |
| Möbius Toeplitz [μ(n)] | **Poisson** | -0.36 | 0.922 | 0.034 |
| Von Mangoldt Hankel H_{ij} = Λ(i+j) | **Intermediate (Poisson-GOE)** | **0.44** | **0.72** | 0.056 (Poisson), 0.065 (GOE) |

The Möbius function (connected to 1/ζ(s)) gives identical Poisson behavior as von Mangoldt. The arithmetic content does not matter — the universality class is fixed by the matrix structure.

## The Toeplitz vs. Hankel Dichotomy

The most important finding: using the identical arithmetic function Λ(n) and identical matrix size, changing only the index rule from "difference" (Toeplitz) to "sum" (Hankel) shifts from firmly Poisson to intermediate Poisson-GOE:

- **Toeplitz**: T_{ij} = Λ(|i-j|+1) — entries depend on **|i-j|** → **Poisson** (β = -0.31)
- **Hankel**: H_{ij} = Λ(i+j) — entries depend on **i+j** → **Partial GOE** (β = 0.44)

The Hankel matrix also achieves a remarkable coincidence: number variance at L=10 matches GUE with ratio 1.005. But the spacing distribution is not GUE (it's between Poisson and GOE), so this is structure-induced rigidity, not genuine GUE correlations.

## Theoretical Explanation: Why Toeplitz → Poisson

A real symmetric Toeplitz matrix with first row [c₀, c₁, ..., c_{N-1}] has eigenvalues approximately given by sampling the spectral function f(θ) = c₀ + 2Σ cₖ cos(kθ) at N quasi-equally-spaced points. For arithmetic functions like Λ(n), f(θ) is a trigonometric polynomial with prime-structured (highly irregular) coefficients, and the sampling points are deterministic. **Deterministic Toeplitz matrices generically have Poisson statistics** — this is a known result in random matrix theory. Eigenvalues are essentially independent samples of an irregular Fourier transform.

The Hankel structure couples different "frequencies" in a way the DFT cannot diagonalize, introducing partial eigenvalue repulsion, but still remains real symmetric.

## Key Implications for the Hilbert-Pólya Program

1. **Prime encoding alone is NOT sufficient for GUE.** Simply writing down a matrix whose entries are arithmetic functions does not produce zeta-zero-like statistics — not even close.

2. **Matrix structure dominates arithmetic content.** The universality class (Poisson vs. GOE vs. intermediate) is determined by whether the index rule is additive or difference-based, not by whether the function is Λ, μ, or any other arithmetic function. All Toeplitz variants regardless of arithmetic function → Poisson.

3. **Real symmetric matrices are fundamentally limited to GOE (β=1) at best** — getting GUE (β=2) requires complex-valued matrices. Time-reversal symmetry breaking requires complex entries; all matrices tested here are real symmetric.

4. **Confirms the trace formula constraint** (see riemann-operator-constraints.md): the trace formula determines spectral density but NOT spectral correlations. Here we see it empirically — the Toeplitz matrix correctly encodes the PNT (largest eigenvalue ~ N = ψ(N)) but produces completely wrong correlations (Poisson instead of GUE).

## Most Promising Direction

The von Mangoldt Hankel matrix with **complex-valued entries** — e.g., H_{ij} = Λ(i+j)·e^{iθ(i+j)} for some phase function θ — could potentially break time-reversal symmetry and push from β=0.44 (partial GOE) toward β=2 (GUE). This is the natural extension: the Hankel structure already introduces partial repulsion; adding complex phases removes the real-symmetric constraint that caps β at 1.

**Update (2026-03-27, strategy-002 exploration-001):** This prediction was confirmed. Complex Hermitian matrices with random phases achieve β=1.675 (approaching GUE); Gauss sum phases achieve β=1.092 (GOE). The key constraint: phases must depend jointly on (j,k), not just |j-k|. See `complex-phase-matrices-gue-approach.md` for full results and `c1-constraint-scorecard.md` for the 10-constraint evaluation.
