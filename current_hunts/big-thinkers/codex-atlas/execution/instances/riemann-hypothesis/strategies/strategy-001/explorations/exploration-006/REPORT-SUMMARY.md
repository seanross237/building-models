# Exploration 006 Summary: Arithmetic Operator Construction

## Goal
Construct matrices from arithmetic functions (von Mangoldt Λ, Möbius μ) as Toeplitz and Hankel matrices, compute eigenvalues at N=200-1000, and classify their spectral statistics against GUE/GOE/Poisson.

## What Was Tried
- **Von Mangoldt Toeplitz** T_{ij}=Λ(|i-j|+1) at N=200,500,1000 — full statistical workup including unfolding, NN spacing, pair correlation, number variance, level repulsion exponent
- **Normalized von Mangoldt Toeplitz** a(n)=Λ(n)/√n at N=500
- **Möbius Toeplitz** a(n)=μ(n) at N=500
- **Von Mangoldt Hankel** H_{ij}=Λ(i+j) at N=500

## Outcome: SUCCEEDED — Clear Classification

**All three Toeplitz variants are Poisson.** Chi² to Poisson: 0.019-0.034, vs GOE: 0.84-1.06, vs GUE: 0.57-0.98. Level repulsion β ≈ -0.3 (negative — clustering, not repulsion). Spacing std ≈ 0.92 (Poisson = 1.0). Pair correlation is flat, not the GUE sine-kernel. Score: 0/4 on the constraint catalog.

**The Hankel variant is intermediate Poisson-GOE.** Chi² to Poisson: 0.056, to GOE: 0.065 (nearly equal). β = 0.44, spacing std = 0.72. Partial level repulsion, reduced fluctuations. Number variance at L=10 accidentally matches GUE (ratio 1.005), but this doesn't hold across all L.

## Key Takeaway
**Simply encoding primes into a matrix does NOT produce GUE statistics. The matrix structure (Toeplitz vs Hankel) matters more than the arithmetic content.** Toeplitz matrices are diagonalized by the DFT, so their eigenvalues are samples of a spectral function → Poisson is generic and expected. Hankel structure introduces inter-frequency coupling that creates partial repulsion but only reaches GOE, not GUE. Getting β=2 (GUE) from a real symmetric matrix is impossible — complex-valued entries are needed.

## Unexpected Findings
- The **Toeplitz vs. Hankel dichotomy** is striking: same arithmetic function Λ(n), same size, but Toeplitz → Poisson while Hankel → partial GOE. The index mapping (|i-j| vs i+j) determines the universality class.
- All Toeplitz variants have β < 0 (eigenvalue clustering), which is unusual and suggests the arithmetic structure actively anti-correlates certain eigenvalue separations.
- The Hankel number variance at L=10 matching GUE with ratio 1.005 is a curious coincidence worth checking at larger N.

## Computations Identified
1. **Complex Hankel matrix**: H_{ij} = Λ(i+j)·e^{i·arg(ζ(1/2+i·(i+j)))} — adding phases from zeta itself could break time-reversal symmetry and push toward GUE. ~50-line scipy script, would need zeta evaluations from mpmath.
2. **Hankel at larger N** (N=2000-5000): Check whether β increases toward 1 (GOE) or stays at ~0.44 as N grows. Would confirm whether the partial repulsion is a finite-size effect. ~30-line numpy script, ~minutes of compute.
3. **Asymmetric arithmetic matrix**: Instead of real symmetric, try T_{ij} = Λ(i·j mod N) — multiplicative rather than additive index structure, connected to Dirichlet characters. Could produce non-trivial spectral properties. ~40-line script.
