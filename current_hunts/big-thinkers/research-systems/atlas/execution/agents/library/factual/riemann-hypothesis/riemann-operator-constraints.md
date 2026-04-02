---
topic: Constraints on the hypothetical Riemann operator from GUE statistics
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-001, exploration-002, exploration-004"
---

## Finding

The confirmed GUE statistics of Riemann zeta zeros place definitive constraints on the properties of any hypothetical self-adjoint operator whose eigenvalues are the zeta zeros (the "Riemann operator" or Hilbert-Polya operator).

## Definitively Ruled Out

1. **Any operator with Poisson statistics** — mean deviation 5x worse than GUE. Eliminates:
   - Generic integrable systems
   - Diagonal operators
   - Number-theoretic operators with statistically independent eigenvalues
   - Any system where eigenvalues behave like uncorrelated random variables

2. **Any operator with GOE statistics (beta=1)** — mean deviation 2x worse than GUE. Eliminates:
   - Real symmetric operators on real Hilbert spaces
   - Hamiltonians with time-reversal symmetry and integer spin (T^2 = +1)
   - Any operator with purely real matrix elements

## Disfavored

3. **Operators with GSE statistics (beta=4)** — mean deviation ~25% worse than GUE with N=2,000. Discrimination would sharpen with more zeros. Formally, the Riemann operator must not have the Kramers degeneracy structure characteristic of GSE.

## Required Properties

The Riemann operator must:
- Act on a **complex** Hilbert space
- Break time-reversal symmetry (or have half-integer spin symmetry)
- Have generically **complex** matrix elements
- Exhibit **quadratic level repulsion** (P(s) ~ s^2 for small s)

## Periodic Orbit Constraints (from long-range statistics)

Berry's saturation (confirmed in exploration-002) adds structural constraints on the classical dynamics of H:

- **Classical limit must be chaotic** — GUE statistics require classically chaotic dynamics (not integrable, not mixed)
- **Shortest periodic orbits have periods ~ log p** for primes p — the prime periodic orbit contributions produce the observed spectral saturation
- **Orbit structure is strong enough to cause saturation at L ~ 2–5** — the sum Σ_p (ln p)²/p over periodic orbits is large enough to suppress long-range correlations well below the GUE level
- **Super-rigidity** — the zeta zeros are MORE ordered than any random matrix at large scales (number variance slope 12× smaller than GUE, spectral rigidity saturates at 0.156). The spectrum is "crystalline" at large scales while maintaining GUE-level fluctuations at small scales.
- **No missing structure detected** — all statistics measured so far (pair correlation, spacing distribution, number variance, spectral rigidity, form factor) are consistent with GUE + prime orbit picture. No anomalous deviations found.

## Precision of Constraints

At the level of 2,000 zeros:
- No systematic deviations from GUE are detected in short-range statistics
- Pair correlation deviations are statistically consistent with zero (68% within 1-sigma)
- Long-range deviations from GUE are all consistent with Berry's saturation mechanism
- The true match to GUE is better than the measurement precision
- Odlyzko's computations with millions of zeros at t ~ 10^20 confirm and sharpen these constraints

## Operator Encodes More Than Trace Formula (from exploration-004)

The Berry-Keating decomposition (xp smooth spectrum + prime oscillatory corrections) determines the **spectral density** via the counting function N(T) but NOT the **spectral correlations** that produce GUE statistics. Specifically:

- The trace formula Tr(f(H)) gives the explicit formula for any test function f, but the **operator itself** contains additional structure — eigenvectors, matrix elements — that the trace formula does not capture.
- This additional structure determines individual eigenvalue positions and GUE statistics.
- Computational verification: prime corrections improve number variance by 75% (a density statistic) but destroy level repulsion (β: 2.32 → 0.03, a correlation statistic).

**Implication for the Hilbert-Pólya program**: Finding the operator requires going **beyond** spectral density to spectral correlations. The trace formula alone is insufficient; one needs either a spectral determinant approach (det(H - E) = 0), a resolvent approach (poles of Tr(H - E)^{-1}), or something that encodes level positions rather than just counting.

**Important nuance (E006):** Berry's *diagonal* approximation — using prime orbit weights to construct K_primes(τ) *directly* without perturbing zero positions — DOES reproduce the two-point spectral form factor ramp with 14.5% accuracy (comparable to K_zeros accuracy of 12.8%). This is different from the prime corrections finding above:

- **Prime corrections to zero positions** (E004): modifies individual zero positions using N_osc → destroys level repulsion (β: 2.32 → 0.03). Primes cannot reconstruct zero positions.
- **Berry diagonal approximation for K(τ)** (E006): uses prime orbit weights to predict K(τ) ramp *as a statistical pattern*, independent of zero positions → succeeds for τ < 1 (MAD=14.5%), fails for τ > 1 (no plateau mechanism).

The corrected statement is: *prime corrections to individual zero positions* do not determine spectral correlations; but *prime orbit weights via Berry's diagonal formula* do determine the two-point form factor ramp. See `prime-sum-form-factor-ramp.md` for the full calculation.
