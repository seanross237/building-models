---
topic: Pair correlation MRD test — discriminating power limits at N=500
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-002 exploration-007"
---

## Summary

The standard pair correlation mean relative deviation (MRD) test, applied at N=500 with 5-realization curve averaging, is not a discriminating test for Riemann-specific structure. Any GUE-class Hermitian matrix achieves ≤10% MRD against Montgomery's formula. Even GOE-class matrices can pass. The Von Mangoldt amplitude structure contributes nothing over a random GUE baseline. Meaningful discrimination requires larger N or more realizations.

## Null Matrix Comparison

All four matrix types pass the 10% MRD threshold when pair correlation is computed as a 5-realization pooled average:

| Matrix | MRD | β_Wigner | Class | Notes |
|---|---|---|---|---|
| C1 (Von Mangoldt Hankel + random phases) | 7.9% | 1.18 ± 0.22 | GUE | Baseline claim |
| GUE control (random complex Gaussian) | 7.8% | 1.50 | GUE | No arithmetic content |
| Flat-amplitude random phase | 6.8% | 1.45 | GUE | BETTER than C1 |
| Flat-amplitude Toeplitz (random per-lag phase) | 9.0% | 0.45 | **GOE** | Passes despite being GOE |

Setup: N=500 Hermitian matrices, 5 realizations each, degree-5 polynomial unfolding, dr=0.05 bins, MRD over r∈[0.5, 4.0] against R₂(r) = 1 − (sin(πr)/πr)².

## Key Conclusions

**1. Von Mangoldt amplitude is unnecessary.** Flat-amplitude random phases (6.8% MRD) outperform C1 (7.9%). Pure random GUE (7.8%) matches C1. The arithmetic content of the Von Mangoldt function provides no pair correlation improvement over a random baseline.

**2. The test cannot distinguish GOE from GUE.** The Toeplitz random-phase matrix is GOE-class (β=0.45 — factorizable phases → unitarily real) yet passes pair correlation at 9.0% MRD with 5-realization averaging. A test that cannot separate GOE from GUE provides no evidence for Riemann-specific structure.

**3. The 7.9% MRD is a 5-realization averaging artifact.** C1 individual realizations have mean MRD = 15.5% ± 1.9%; 0 of 20 individual realizations pass the ≤10% threshold. The "PASS" verdict required pooling 5 R₂(r) curves (noise reduction by ~√5) before computing MRD. At 20-realization pooling (10,000 eigenvalues), MRD = 3.7% — but this reflects the GUE universality class, not arithmetic structure.

**4. Comparison to actual Riemann zeros.** The first 2,000 Riemann zeros (S001) achieve 9.1% MRD — worse than C1's 5-realization average (7.9%). The C1 matrix with 20-realization pooling (3.7%, from ~10,000 eigenvalues) significantly outperforms the actual zeros dataset-for-dataset only because it uses 5× more eigenvalues. Neither comparison isolates arithmetic structure.

## What a Meaningful Test Would Require

To discriminate GUE from GOE (or Riemann-specific from generic GUE) via pair correlation:
- **Large N:** Single-matrix MRD noise is ~15% at N=500; reducing to ~3–5% requires N > 2,000
- **More realizations:** At N=500, need ≥20 realizations pooled to see MRD < 10% per-realization
- **Or: statistics that distinguish GUE from GOE more sharply** — β_Wigner and Δ₃ are better discriminators than pair correlation MRD at this sample size

## Context

This finding arose from adversarial attack on the C1 pair correlation claim (S002-E007). See also: `c1-constraint-scorecard.md` for the full C1 scorecard update including the revised status of constraint #2 (pair correlation).
