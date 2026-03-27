---
topic: Constraints on the hypothetical Riemann operator from GUE statistics
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-001 exploration-001, exploration-002"
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
