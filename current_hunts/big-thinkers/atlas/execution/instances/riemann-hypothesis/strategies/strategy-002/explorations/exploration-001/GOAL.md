# Exploration 001 — Tournament Entry A: Complex Arithmetic Matrices

## Mission Context

We are investigating the Riemann Hypothesis through the lens of random matrix theory. Previous work (strategy-001) established that:

1. **Zeta zeros are definitively GUE (β=2)**: pair correlation matches Montgomery to 9%, nearest-neighbor spacing matches Wigner surmise to 4%, spectral form factor matches GUE ramp-plateau within 1-4%.

2. **All tested arithmetic matrix operators fail** (score 0/10 against the 10-point constraint catalog):
   - Von Mangoldt Toeplitz → Poisson (β = -0.31)
   - Von Mangoldt Hankel → partial GOE (β = 0.44) — best real symmetric result
   - Real symmetric matrices are **mathematically capped at β ≤ 1**. This is not a quantitative limitation — it's structural. GOE (β=1) requires time-reversal symmetry. GUE (β=2) requires broken time-reversal symmetry. **You cannot reach GUE with real symmetric matrices.**

3. **The insight:** Complex Hermitian matrices CAN break time-reversal symmetry and reach β=2. The natural extension of the Hankel result is: take the same arithmetic content but add complex phases to the matrix entries.

## Your Task

**Build and test complex Hermitian arithmetic matrices.** Score each against the 10-point constraint catalog. The objective: push β from 0.44 (Hankel baseline) toward 2.0 (GUE target).

## The 10-Point Constraint Catalog

Every construction must be scored against these verified constraints on the true Riemann operator:

| # | Constraint | Target Value |
|---|-----------|-------------|
| 1 | Symmetry class | β=2 (GUE, not GOE or Poisson) |
| 2 | Pair correlation matches Montgomery | <10% mean relative deviation |
| 3 | NN spacing matches Wigner surmise | <5% mean absolute deviation |
| 4 | Poisson/GOE ruled out | GUE better than GOE AND Poisson |
| 5 | Quadratic level repulsion | β = 2.0 (P(s) ~ s²) |
| 6 | Number variance saturates | Σ²(L) ~ 0.3-0.5 for L>2 |
| 7 | Spectral rigidity saturates | Δ₃ = 0.156 for L>15 |
| 8 | Form factor ramp-plateau | ramp slope ~1.0, plateau ~1.0 |
| 9 | Super-rigidity | more rigid than finite GUE |
| 10 | Periodic orbit structure | saturation encodes prime sums |

For this exploration, focus primarily on **constraints 1, 3, 4, 5** (the symmetry class / level repulsion metrics that reveal β). Constraints 6-10 (long-range statistics) require more zeros to compute reliably and are lower priority for Phase 1 screening.

## Constructions to Test

Test these four matrix families in order (stop early if one clearly wins, spend more time on it):

### Construction 1: Complex Random Phase Baseline (Control)
```
H_{jk} = Λ(|j-k|+1) × exp(2πi × φ_{jk})
```
where φ_{jk} = φ_{kj}* (so H is Hermitian), and φ_{jk} are drawn from Uniform(0, 1).
This tests: does ANY complex phase push β toward 2? If no, complex structure alone isn't enough.

### Construction 2: Dirichlet Character Phases
```
H_{jk} = Λ(|j-k|+1) × χ(j-k) / |χ(j-k)|   (normalize phase)
```
where χ is a Dirichlet character mod q. Try q=4 (χ₄), q=8 (χ₈), q=12 (χ₁₂).
Note: for j=k (diagonal), use real values Λ(1) = 0.
Adjust for zero values of χ: if χ(j-k) = 0, use H_{jk} = 0.

### Construction 3: Gauss Sum Phases
```
H_{jk} = Λ(|j-k|+1) × exp(2πi × (j·k mod p) / p)
```
for p prime. Try p = 97, 101, 997 (primes near N/2 and N).

### Construction 4: Zeta-Value Phases
```
H_{jk} = Λ(|j-k|+1) × exp(2πi × Im(ζ(1/2 + i·(j-k))))
```
Use the imaginary part of zeta on the critical line as a phase.

## What to Compute for Each Construction

For each construction, use N = 300-500 (larger is better but time-limited):

1. **Level repulsion exponent β**: Fit P(s) to A × s^β × exp(-B × s²) for small s (s < 0.5). This is the primary discriminator.

2. **Spacing distribution**: Compute nearest-neighbor spacings after unfolding eigenvalues. Compare to:
   - GUE Wigner surmise: P_GUE(s) = (32/π²) s² exp(-4s²/π)
   - GOE: P_GOE(s) = (π/2) s exp(-πs²/4)
   - Report chi² ratio: chi²_GUE / chi²_GOE (should be <1 for GUE-like)

3. **Unfolding method**: Sort eigenvalues, fit smooth density (polynomial or kernel), unfold to mean spacing 1.

4. **GUE simulation control**: Also generate a true N×N GUE random matrix (H = (A + A†)/2 where A_{jk} ~ CN(0,1)) and run the same analysis. This gives the theoretical β=2.0 baseline.

## Deliverables

Produce a **scorecard table** with columns:

| Construction | N | β | chi²_GUE | chi²_GOE | GUE better? | Notes |
|---|---|---|---|---|---|---|
| Hankel (S001 baseline) | 500 | 0.44 | - | - | No | Real symmetric |
| GUE control | 500 | ~2.0 | ~1.0 | >1 | Yes | Random matrix |
| C1: Random phases | ... | | | | | |
| C2a: Dirichlet χ₄ | ... | | | | | |
| C2b: Dirichlet χ₈ | ... | | | | | |
| C3a: Gauss p=97 | ... | | | | | |
| C3b: Gauss p=997 | ... | | | | | |
| C4: Zeta phases | ... | | | | | |

**For the best-scoring construction**: compute the full 10-constraint scorecard.

## Key Questions to Answer

1. Does ANY complex phase choice push β above 1.0?
2. What is the best β achieved? How does it compare to GUE (β=2.0)?
3. Is there structure in which phase functions produce higher β?
4. What is the full constraint catalog score (X/10) for the best construction?
5. Does the eigenvector structure look interpretable (localized? extended? have arithmetic content)?

## Implementation Notes

- Use numpy for matrix construction and scipy.linalg.eigh for eigenvalues (much faster than scipy.linalg.eig for Hermitian matrices)
- For β fitting: use scipy.optimize.curve_fit on the small-s regime of the spacing distribution
- Computation: N=500 Hermitian eigenvalue decomposition takes ~0.1 seconds in numpy
- You can run multiple N=500 matrices and average (reduces noise in statistics)
- **Reuse strategy-001's code patterns** — the unfolding and spacing distribution analysis code from exploration-001 is the template

## Success Criteria

**Primary success:** β > 1.5 for at least one construction (significantly above GOE cap of 1.0, approaching GUE at 2.0)
**Secondary success:** β > 1.0 for at least one construction (any progress toward GUE)
**Failure:** All constructions have β ≤ 0.5 (no improvement over Hankel baseline of 0.44)

## Exploration Directory

Your exploration directory is:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-001/`

Write all scripts to `code/` subdirectory. Write REPORT.md incrementally as you compute each construction. Write REPORT-SUMMARY.md **last** — this signals you are finished.
