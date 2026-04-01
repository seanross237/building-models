# Strategy 001 Final Report: Computational Constraint Cartography

## Executive Summary

Over 6 explorations (5 successful, 1 failed), this strategy built a **10-point quantitative constraint catalog** for the hypothetical Riemann operator, tested it against the leading operator candidates, and discovered a fundamental limitation of the trace formula approach. The key findings are:

1. **GUE is definitively confirmed** as the correct universality class for zeta zeros, with quantitative precision: pair correlation matches Montgomery to 9% (noise-consistent), nearest-neighbor spacing matches Wigner surmise to 4%, and the spectral form factor shows the GUE ramp-plateau structure to 1-4%.

2. **Berry's spectral rigidity saturation is clearly detected.** Zeta zeros are 30-50% MORE rigid than finite-size GUE random matrices at large scales. The spectral rigidity Delta_3 saturates at 0.156 for L > 15, while GUE theory predicts 0.50. This "super-rigidity" encodes prime number information.

3. **All Berry-Keating xp regularizations fail the constraint catalog** (0/10). The xp operator provides only the smooth (Weyl) spectral density. The fluctuations that produce GUE statistics come entirely from primes.

4. **Individual zero reconstruction from the explicit formula fundamentally fails** due to the Gibbs phenomenon. The trace formula determines spectral DENSITY but not spectral CORRELATIONS. The Berry-Keating operator, if it exists, contains more information than the trace formula.

5. **Simply encoding primes into a matrix does not produce GUE statistics.** Arithmetic Toeplitz matrices are Poisson; Hankel matrices reach partial GOE at best. Real symmetric matrices are structurally limited to GOE (beta=1), never GUE (beta=2).

## What We Accomplished

### Phase 1: Constraint Extraction (Explorations 001-002)

Built a 10-point quantitative constraint catalog from computation on the first 2000 zeta zeros:

| # | Constraint | Value | Source |
|---|-----------|-------|--------|
| 1 | GUE symmetry class (beta=2) | No time-reversal symmetry | E001 |
| 2 | Pair correlation matches Montgomery | 9% mean relative deviation | E001 |
| 3 | NN spacing matches GUE Wigner surmise | 4% mean absolute deviation | E001 |
| 4 | Poisson/GOE definitively ruled out | GOE 2x worse, Poisson 5x worse | E001 |
| 5 | Quadratic level repulsion | P(s) ~ s^2 for small s | E001 |
| 6 | Number variance saturates beyond GUE | Sigma^2(L) ~ 0.3-0.5 for L > 2 | E002 |
| 7 | Spectral rigidity saturates | Delta_3 = 0.156 for L > 15 | E002 |
| 8 | Form factor ramp-plateau | slope = 1.010, plateau = 1.043 | E002 |
| 9 | Super-rigidity | 30-50% more rigid than finite GUE | E002 |
| 10 | Periodic orbit structure | Saturation encodes sum(ln(p)^2/p) | E002 |

Every constraint is backed by reproducible Python code using mpmath, numpy, and scipy.

### Phase 2: Operator Testing (Explorations 003-006)

Tested five operator candidates/approaches:

| Candidate | Score | Key Failure |
|-----------|-------|-------------|
| Sierra-Townsend (xp regularized) | 0/10 | Equally spaced (crystalline) |
| BBM PT-symmetric (HO basis) | 0/10 | Doublets, negative beta |
| Trace formula reconstruction | N/A | Gibbs phenomenon (fundamental) |
| Von Mangoldt Toeplitz | 0/4 | Poisson statistics |
| Von Mangoldt Hankel | 1/4 partial | beta=0.44 (partial GOE, not GUE) |

### Key Insight Chain

The explorations build on each other to form a coherent narrative:

1. **Zeta zeros are GUE** (E001) → the operator breaks time-reversal symmetry
2. **Plus super-rigid** (E002) → prime orbits impose additional structure beyond GUE
3. **xp alone fails** (E003) → the smooth (Weyl) part is necessary but insufficient
4. **xp + primes fails for individual zeros** (E004) → the trace formula gives density, not correlations; the operator encodes MORE than the trace formula
5. **Arithmetic matrices fail** (E006) → simply putting primes into a matrix doesn't work; matrix STRUCTURE matters as much as arithmetic CONTENT; real symmetric matrices can't even reach GUE

**The bottom line:** The Riemann operator must be:
- **Complex** (not real symmetric) — to produce GUE, not GOE
- **Arithmetically structured** — to have prime periodic orbits
- **Non-trivially organized** — the relationship between arithmetic content and matrix structure must be specific
- **More than a trace formula** — its eigenvectors and matrix elements carry information beyond what the counting function encodes

## What Directions We Tried

1. **Short-range RMT statistics** — Completed successfully. Foundation for everything else.
2. **Long-range RMT statistics** — Completed successfully. Produced the super-rigidity finding.
3. **Berry-Keating xp variants** — Completed. All fail. Definitively shows xp is insufficient alone.
4. **Trace formula reconstruction** — Completed. Deep negative result (Gibbs phenomenon).
5. **Two-point correlation from primes** — Failed (explorer crashed). Question remains open.
6. **Arithmetic matrix operators** — Completed. Shows structure matters more than content.

## Most Promising Findings

### Finding 1: Super-Rigidity Quantification
The zeta zeros are 30-50% more rigid than finite-size GUE random matrices at scales L = 5-15. Specifically:
- Sigma^2(zeta)/Sigma^2(GUE sim) = 0.50-0.73 at L = 5-100
- Delta_3(zeta) saturates at 0.156 while Delta_3(GUE sim) continues growing to 0.288
- Logarithmic growth rate of Sigma^2 is 12x smaller than finite-size GUE

This is Berry's saturation, computationally verified. The saturation level encodes information about the prime orbit sum.

### Finding 2: Gibbs Phenomenon in Zero Reconstruction
The one-point trace formula cannot reconstruct individual zero positions because N_osc is a step function at the zeros. Key quantitative results:
- N_osc at smooth zeros is ALWAYS exactly ±0.5 (mathematical identity)
- Residual convergence: P_max^{-0.13} (far slower than random P_max^{-0.5})
- More primes = worse reconstruction (variance explained: 80% at P_max=10, -6% at P_max=10000)
- But sign prediction is 100% accurate

### Finding 3: Toeplitz-Hankel Dichotomy
Same arithmetic function (von Mangoldt), same matrix size, but:
- Toeplitz structure → Poisson (beta = -0.3)
- Hankel structure → partial GOE (beta = 0.44)

This demonstrates that the relationship between arithmetic data and spectral statistics depends critically on how the data is organized into the operator, not just what data is used.

## What We'd Recommend for the Next Strategy

1. **The two-point trace formula (exploration 005, failed) should be retried.** Montgomery proved that pair correlation IS determined by prime pairs. Computing this explicitly would either confirm or refine the conclusion from exploration 004 that "primes determine density not correlations."

2. **Use precomputed zero tables** (LMFDB, Odlyzko tables) instead of mpmath for large-scale statistics. mpmath's zetazero() tops out practically at ~2000 zeros. Millions of zeros would sharpen all measurements by 10-30x.

3. **Explore complex arithmetic matrices.** Real symmetric matrices can only reach GOE. To get GUE (beta=2), complex entries are needed. Possible: H_{ij} = Lambda(|i-j|+1) * exp(i * theta_{ij}) where theta involves zeta values or Dirichlet characters.

4. **The spectral determinant approach** (from exploration 004's suggestions) bypasses the counting function entirely and might avoid the Gibbs obstruction.

5. **Quantitative comparison to Berry's saturation formula.** We confirmed saturation qualitatively but didn't compare the measured saturation LEVEL to Berry's explicit prediction (which involves specific prime sums). This would be a clean, high-value computation.

## Novel Claims

### Claim 1: Gibbs Phenomenon as Fundamental Obstruction
**Claim:** Individual zero reconstruction from the explicit formula is fundamentally impossible (not just computationally hard) because the prime sum converges to the Gibbs midpoint at the step discontinuities of N(T). The convergence rate is P_max^{-0.13}, requiring ~30 million primes for 1% accuracy at individual zeros.

**Evidence:** Exploration 004, computed for 2000 zeros with P_max from 10 to 10000. Variance explained decreases from 80% to -6% as P_max increases. The ±0.5 identity for N_osc at smooth zeros is derived mathematically.

**Novelty search:** The Gibbs phenomenon in the context of the explicit formula is well-known in analytic number theory (it's essentially the reason the prime counting function pi(x) is harder to work with than the Chebyshev function psi(x)). However, the specific application to ZERO RECONSTRUCTION — showing that it gets WORSE with more primes — may not be widely appreciated. The quantitative convergence rate P_max^{-0.13} and the "negative variance explained" result may be new.

**Strongest counterargument:** This is essentially a well-known mathematical fact (conditional convergence of Fourier series at discontinuities) applied to a specific context. The novelty is in the quantitative characterization and the implication for the Hilbert-Polya program, not in the mathematics itself.

**Status:** Partially verified. The mathematics is solid but the novelty claim is modest.

### Claim 2: Toeplitz-Hankel Dichotomy for Arithmetic Matrices
**Claim:** Von Mangoldt Toeplitz matrices have Poisson spectral statistics (beta ≈ -0.3) while Von Mangoldt Hankel matrices have partial GOE statistics (beta ≈ 0.44), demonstrating that operator STRUCTURE determines universality class independently of arithmetic CONTENT.

**Evidence:** Exploration 006, computed at N = 200-1000 for Toeplitz, N = 500 for Hankel. Spacing distributions, level repulsion exponents, and number variance all classified.

**Novelty search:** Toeplitz matrix spectral theory is well-studied (Szego's theorem, etc.) and the Poisson result for Toeplitz is expected from the asymptotic eigenvalue distribution theorem. Hankel matrices from arithmetic functions are less studied. The specific comparison using the same arithmetic function in both structures may be novel as a computational demonstration.

**Strongest counterargument:** The Toeplitz result is expected from Szego's theorem. The Hankel result may be a finite-size effect (beta may approach 0 at larger N). Neither result is surprising to someone who knows random matrix theory and Toeplitz spectral theory.

**Status:** Speculative. The computation is correct but the novelty is limited.

### Claim 3: Super-Rigidity Quantification
**Claim:** At scales L = 5-100, zeta zeros are 30-50% more rigid than eigenvalues of finite-size GUE random matrices (not just the asymptotic GUE formula). The spectral rigidity Delta_3 saturates at 0.156 ± 0.001 for L > 15, and the logarithmic growth rate of Sigma^2 is 12x smaller than finite-size GUE and 34x smaller than asymptotic GUE.

**Evidence:** Exploration 002, using 2000 zeros and direct comparison with a 2000x2000 GUE simulation. Independently confirmed in exploration 003 with 200 zeros (45-56% more rigid at L = 5-15).

**Novelty search:** Berry's saturation prediction (1985) is well-known. Odlyzko computed similar statistics with millions of zeros. The specific quantification "30-50% more rigid than finite-size GUE" and the comparison against actual GUE simulation (not just the asymptotic formula) may add precision to existing results, but is not fundamentally new.

**Strongest counterargument:** This is a computational verification of a well-known prediction, done with fewer zeros than published computations (Odlyzko used millions).

**Status:** Verified but not novel. The computation is correct and the quantification is useful as a constraint, but Berry, Odlyzko, and others have done this more precisely.

## Summary

This strategy successfully built a computational constraint catalog for the Riemann operator and used it to systematically test candidates. The most valuable outcome is not any single finding but the **chain of reasoning**: GUE confirmation → super-rigidity from primes → xp alone fails → trace formula gives density not correlations → arithmetic matrices need complex structure. Each step constrained the search space further.

No genuinely novel claims emerged that would survive expert scrutiny. The novelty is in the systematic computational approach and the chain of insights connecting the findings, not in any individual result. The strategy achieved its goal of mapping the constraint landscape, even if no new territory was discovered within it.
