---
topic: Li coefficients — GUE comparison and super-rigidity connection
confidence: provisional
date: 2026-03-28
source: "riemann-hypothesis strategy-003 exploration-002, strategy-003 exploration-007 (novelty review), strategy-003 exploration-008 (truncation validation), strategy-003 exploration-009 (convergence test — artifact confirmed)"
---

## Finding

Zeta and GUE Li coefficients are remarkably similar (97.1% Coffey residual correlation for n >= 50) but diverge systematically at K=N=2000: GUE overshoots zeta for large n, with crossover around n ~= 300. `[COMPUTED]` **RESOLVED (E009): The crossover is a TRUNCATION ARTIFACT.** The matched K=N convergence test (K=N=500, 1000, 2000, 3000, 5000) shows the ratio at n=500 monotonically increases from 0.888 to 1.090, crossing 1.0 between K=N=2000 and 3000. At K=N≥3000, zeta EXCEEDS GUE at all tested n. Root cause: linear scaling of GUE eigenvalues creates a density mismatch that worsens with K (semicircle vs. logarithmic density). The 97.1% correlation and residual analysis remain valid findings; the crossover-specific claim does not.

## GUE Comparison Data (E008: 100 Realizations)

GUE(2000) random matrices (**100 realizations** — 20× more than E002's 5), eigenvalues scaled to match zeta zero range [t₁, t₂₀₀₀]:

| n | lambda_n^zeta | lambda_n^GUE (mean +/- std) | Ratio | Significance |
|---|---------------|------------------------------|-------|-------------|
| 1 | 0.0227 | 0.0203 +/- 0.0019 | 1.114 | +1.2σ |
| 10 | 2.235 | 2.004 +/- 0.184 | 1.115 | +1.3σ |
| 50 | 42.43 | 37.50 +/- 2.82 | 1.131 | +1.7σ |
| 100 | 114.18 | 103.02 +/- 3.47 | 1.108 | +3.2σ |
| 200 | 288.97 | 277.55 +/- 4.81 | 1.041 | +2.4σ |
| 300 | 479.91 | 480.10 +/- 5.57 | 1.000 | −0.03σ |
| 400 | 677.59 | 699.67 +/- 5.73 | 0.968 | −3.9σ |
| 500 | 881.43 | 925.62 +/- 6.09 | **0.952** | **−7.3σ** |

**Crossover at n ≈ 300 confirmed** (ratio = 0.9996 at n=300, essentially unity). For small n (n < 200), zeta EXCEEDS GUE by ~10-13%. At n=500, 7.3σ below GUE — highly significant at matched K=N=2000.

**NOTE:** E002 used N_GUE=2000 matrices with 5 realizations (not N=100 as some strategy summaries stated). E008 corrected this and replicated with 100 realizations for much better statistics.

## Residual Analysis `[COMPUTED]`

- **Coffey residual correlation (n >= 50):** rho = 0.971 (extremely high; partly truncation artifact but far exceeds what truncation alone would produce)
- **Residual magnitude:** Mean |delta^zeta| = 40.35 vs. Mean |delta^GUE| = 34.16 (zeta 18% larger)
- **Residual variability:** delta/log(n) std: zeta = 0.76, GUE = 0.15 (zeta 5x more variable)

## Spectral Rigidity Connection

| L | Delta_3^GUE | Delta_3^zeta | GUE theory |
|---|-------------|-------------|------------|
| 20 | 0.237 | 0.157 | 0.148 |
| 50 | 0.288 | 0.161 | 0.195 |
| 100 | 0.309 | 0.163 | 0.230 |

Zeta zeros saturate at Delta_3 ~= 0.155-0.163 for L > 20 (super-rigid), confirming prior berry-saturation-confirmed.md. GUE eigenvalues from finite N=2000 matrix continue growing to 0.309.

## Mechanism `[CONJECTURED]`

Super-rigid spacing (as in zeta) → more evenly distributed phases theta_k → more efficient cancellation in Sum cos(n*theta_k) → smaller lambda_n at large n. The GUE model captures 97% of Li coefficient structure but misses a correction that grows with n, reflecting arithmetic structure beyond random matrix universality.

The 70% larger zeta residual and 5x larger standard deviation suggest the zeta zeros encode structure beyond GUE statistics in the Li coefficients. The GUE residual is smoother (lower std), consistent with randomness, while the zeta residual has more variation, consistent with arithmetic structure.

## Novelty Assessment (E007 Adversarial Review) `[LITERATURE CONFIRMED]`

**Novelty rating: 4/5 — no prior paper compares λ_n^zeta to λ_n^GUE.**

Literature search covered: Li (1997, J. Number Theory 65:325), Keiper (1992, Math. Comp. 58:765), Bombieri & Lagarias (1999, J. Number Theory 77:274), Schumayer & Hutchinson (2011, Rev. Mod. Phys. 83:307), plus general searches for "Li coefficients GUE," "Keiper-Li spectral statistics random matrix," "lambda_n crossover." **Zero papers found** that:
- Compute λ_n for GUE random matrices
- Compare λ_n^zeta to λ_n^GUE point-by-point
- Identify a crossover at n≈300 where zeta falls below GUE
- Connect Li coefficient growth rate to spectral rigidity (Δ₃) or phase cancellation efficiency

**Key asymptotic (Bombieri-Lagarias 1999):** λ_n ~ (1/2) n log n + C₁ n + O(√n log n) for the Riemann zeta function under RH. This gives leading growth but NOT the ratio λ_n^zeta / λ_n^GUE or its evolution with n.

The standard literature treats Li coefficients as a number-theoretic object (positivity criterion for RH). The RMT community studies zeta zeros via pair correlations, spacings, form factors, and Δ₃ — but not via Li coefficients. These two streams are non-overlapping.

**E009 UPDATE:** The specific crossover finding (ratio < 1 for n > 300, 7.3σ at n=500) is a **truncation artifact** of the linear scaling method (see "Truncation Artifact — RESOLVED" section below). The comparison methodology (computing λ_n for both zeta and GUE) remains novel (4/5), but the specific quantitative crossover claim is **RETRACTED**. The 97.1% correlation, residual analysis, and super-rigidity connection remain valid observations.

## Truncation Analysis — CRITICAL (E008)

**The Li coefficient sum converges SLOWLY for large n.** E008 computed λ_n with 5000 zeros (vs E002's 2000):

| n | λ_n (2k zeros) | λ_n (5k zeros) | Change |
|---|---------------|---------------|--------|
| 100 | 114.18 | 116.34 | +1.9% |
| 200 | 288.97 | 297.58 | +3.0% |
| 300 | 479.91 | 499.29 | +4.0% |
| 400 | 677.59 | 712.03 | +5.1% |
| 500 | 881.43 | 935.20 | **+6.1%** |
| 750 | 1388.94 | 1509.67 | +8.7% |
| 1000 | 1885.47 | 2099.41 | +11.4% |

Each additional block of ~1000 zeros adds ~2% to λ_500. At n=1000, convergence is worse (+11% from 2k→5k). **The sum is NOT converged at 2000 zeros for n ≥ 300.**

### N-Dependence of GUE λ_n

GUE λ_n scales roughly linearly with matrix dimension N (50 trials each, all scaled to [t₁, t₂₀₀₀]):

| N | λ_100^GUE | λ_500^GUE | ζ/GUE ratio at n=500 |
|---|----------|----------|----------------------|
| 500 | 26.96 | 235.23 | 3.75 |
| 1000 | 52.67 | 465.43 | 1.89 |
| 2000 | 103.32 | 925.78 | 0.952 |
| 3000 | 153.28 | 1385.16 | 0.636 |

**The comparison is only meaningful when N_GUE = K_zeros.** Both the zeta sum and GUE eigenvalue count must match for the ratio to be well-defined.

**E009 update:** With MATCHED K=N (each GUE N×N matrix scaled to [t₁, t_K]), the GUE λ_n behavior is anomalous — λ_100^GUE DECREASES from 117.5 (N=500) to 86.7 (N=5000) while zeta λ_100 INCREASES (107.1 to 116.3). This divergent K-dependence is the root cause of the crossover artifact. See "Truncation Artifact — RESOLVED" section below.

### Truncation Artifact — RESOLVED (E009)

**The crossover is a truncation artifact.** E009 completed the matched K=N test at all levels:

| K=N | λ_500^zeta | λ_500^GUE (mean ± std) | Ratio | Significance |
|-----|-----------|------------------------|-------|-------------|
| 500 | 707.36 | 796.25 ± 3.99 | **0.888** | −22.3σ |
| 1000 | 812.56 | 904.72 ± 5.47 | **0.898** | −16.9σ |
| 2000 | 881.43 | 925.62 ± 6.09 | **0.952** | −7.3σ |
| 3000 | 909.39 | 906.08 ± 6.39 | **1.004** | +0.5σ |
| 5000 | 935.20 | 858.19 ± 7.92 | **1.090** | +9.7σ |

The ratio at n=500 monotonically increases: 0.888 → 0.898 → 0.952 → 1.004 → 1.090. It crosses 1.0 between K=N=2000 and 3000, and reaches 1.09 (9.7σ ABOVE 1) at K=N=5000. At K=N≥3000, zeta EXCEEDS GUE at ALL tested n values (n=100 through 500).

Full ratio table (zeta/GUE) across all n:

| K=N | n=100 | n=200 | n=300 | n=400 | n=500 |
|-----|-------|-------|-------|-------|-------|
| 500 | 0.911 | 0.891 | 0.881 | 0.880 | 0.888 |
| 1000 | 0.990 | 0.946 | 0.919 | 0.904 | 0.898 |
| 2000 | 1.108 | 1.041 | 1.000 | 0.968 | 0.952 |
| 3000 | 1.197 | 1.118 | 1.063 | 1.027 | 1.004 |
| 5000 | 1.342 | 1.239 | 1.171 | 1.122 | 1.090 |

**Root cause: broken GUE scaling.** Linear rescaling (map N GUE eigenvalues to [t₁, t_K]) creates a density mismatch:
- GUE eigenvalues follow a semicircle distribution concentrated near the center
- Zeta zeros have logarithmically growing density
- As K=N grows, GUE λ_n at small n DECREASES (117.5 → 86.7 for λ_100) while zeta λ_n INCREASES (107.1 → 116.3)
- The ratio is a smooth function of K that crosses 1.0 at some K-dependent point — not a structural property

**The correct comparison would require unfolding both zero sets to unit mean spacing before computing Li coefficients.** This was not performed in E002–E009 and remains open as a future direction.

## Verification Status (Updated E009)

- **RESOLVED: Matched K=N scaling test.** E009 computed the ratio at K=N=500, 1000, 2000, 3000, 5000. The ratio at n=500 increases monotonically and crosses 1.0 — confirming the crossover is a truncation artifact, not a structural property.
- **RESOLVED: GUE ensemble matching.** E009 computed GUE at N=500 (50 trials), N=1000 (50 trials), N=2000 (100 trials, cached from E008), N=3000 (30 trials), N=5000 (15 trials). Matched at each K=N level.
- **OPEN: Correct comparison method.** The linear scaling comparison is invalidated. A proper test would require unfolding both zeta zeros and GUE eigenvalues to unit mean spacing before computing Li coefficients. This was not attempted.
- **OPEN: Super-rigidity mechanism.** The conjectured mechanism (super-rigidity → phase cancellation → smaller λ_n) was predicated on the crossover being real. With the crossover shown to be an artifact, the mechanism remains unconfirmed. However, the 97.1% correlation and the general similarity of zeta and GUE Li coefficients remain valid observations.

## Cross-References

- See `li-coefficients-verified-n500.md` for the primary Li coefficient computation
- See `li-phase-cancellation-structure.md` for the phase cancellation interpretation
- See `berry-saturation-confirmed.md` for the Delta_3 saturation measurement
- See `riemann-operator-constraints.md` for the super-rigidity constraint on the Riemann operator
