# Exploration 003 Summary: Berry-Keating xp Operator — Spectrum Computation

## Goal
Numerically compute spectra of three Hilbert-Pólya candidate operators and score each against the 10-point constraint catalog from Phase 1.

## What Was Tried
Three approaches implemented and tested:
- **A: Sierra-Townsend regularization** — equally spaced eigenvalues E_n = n (2000 eigenvalues)
- **B: BBM PT-symmetric operator** — H = (1-e^{-ip})(xp+px)(1-e^{ip}) in N=120 harmonic oscillator basis
- **C: Connes-inspired zeta zero matrix** — 200 zeta zeros embedded in Hermitian matrix, compared to GUE ensemble

## Outcome

**Approach A: 0/10 PASS.** Equally spaced spectrum fails every constraint. It's crystalline, not chaotic — the "mean field" contribution with no prime number information.

**Approach B: 0/10 PASS (1 PARTIAL).** The BBM operator in truncated HO basis produces a doublet spectrum with negative level repulsion (β = -0.57, should be +2), wrong scaling (eigenvalues O(1) vs zeros O(10-400)), and unbounded number variance. The harmonic oscillator basis is fundamentally unsuited to the xp operator — truncation artifacts dominate.

**Approach C: 5/10 PASS, 4 PARTIAL.** The actual zeta zeros (trivially) match GUE local statistics: NN spacing consistent with Wigner surmise (KS p=0.23), quadratic repulsion β=2.34, Poisson decisively rejected (p=5×10⁻²³). Confirmed super-rigidity: zeta zeros are 45-56% more rigid than finite GUE at L=5-15. Partial matches on number variance (saturates but at slightly low values) and form factor (plateau ≈ 1.11, ramp slope degraded by finite-size effects).

## Key Takeaway

**The prime number input is the entire ball game.** The xp operator provides only the smooth (Weyl) part of the spectral staircase. All the interesting structure — GUE statistics, super-rigidity, form factor — comes from the fluctuations, which are entirely determined by the primes via the explicit formula. No simple regularization of xp captures this. A successful Hilbert-Pólya operator must have primes encoded in its very structure (boundary conditions, potential, or arithmetic geometry of the domain).

## Unexpected Findings

- **GUE vs GSE indistinguishable at N=200**: The zeta zero spacing distribution has L1 distance 0.068 from both GUE and GSE Wigner surmises. With only 200 zeros, these symmetry classes cannot be discriminated via spacing alone — one needs number variance or higher-order correlations.
- **BBM Hermiticity**: The BBM operator, despite being designed as PT-symmetric, is effectively Hermitian in the truncated HO basis (max|H-H†| = 4×10⁻¹³). The truncation completely destroys the intended PT-symmetric structure.
- **Super-rigidity confirmed with independent computation**: At L=10, zeta zeros are 56% more rigid than the 200×200 GUE ensemble, consistent with Phase 1's finding (30-50%) and suggesting the effect is robust.

## Computations Identified

1. **BBM in position-space basis**: Discretize x ∈ [ε, L] on a grid and represent p = -id/dx with finite differences. This avoids the HO basis truncation problem. Moderate difficulty (~100 lines, standard FD eigenvalue problem). Would determine whether the BBM operator's failure is intrinsic or an artifact of the basis choice.

2. **Trace formula reconstruction**: Starting from the equally-spaced Sierra-Townsend spectrum, add the oscillatory corrections from the explicit formula: δN(E) = -(1/π) Σ_p Σ_m (ln p / p^{m/2}) cos(mE ln p). Compute the resulting perturbed spectrum and check how many constraints it satisfies. This directly tests whether xp + prime corrections = zeta zeros. Moderate difficulty (~80 lines with mpmath).

3. **N=2000 zero statistics for Approach C**: Rerun the zeta zero analysis with 2000 zeros (as in Phase 1) to get reliable number variance, spectral rigidity, and form factor. The N=200 limitation degraded several measurements. Easy (~30 min compute for zeros, same analysis code).
