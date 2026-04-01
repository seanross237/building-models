---
topic: Flat-amplitude test — Von Mangoldt amplitude does not cause Δ₃ anomaly; finite-size GUE correction
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-002 exploration-009"
---

## Summary

A controlled experiment (E009) tested whether C1's intermediate spectral rigidity is caused by Von Mangoldt arithmetic amplitude structure or is generic GUE-class behavior at N=500.

**Result: Von Mangoldt arithmetic does NOT contribute to Δ₃.** H_flat (flat amplitude, random phases), C1 (Von Mangoldt × random phases), and a GUE control give statistically indistinguishable Δ₃_sat values. The "anomalous intermediate rigidity" claim for C1 is retracted.

**Critical finite-size correction:** The correct Δ₃_sat for N=500 GUE matrices is ~0.23–0.26, far below the infinite-N GUE theory value (~0.566 at L≈37). Prior explorations that compared C1's Δ₃_sat = 0.285 against the infinite-N prediction were using the wrong baseline.

## Construction Details

- N = 500, 3 realizations per ensemble
- **Formula:** Exact staircase integration (Dyson-Mehta integral). Each Δ₃(L) = minimum-variance linear fit to piecewise-constant staircase, integrated analytically over all flat segments between eigenvalues. Implementations that sample only at eigenvalue positions (residuals/L) underestimate Δ₃ by ~50×.
- **Δ₃_sat** = mean of Δ₃(L) for L ∈ [25, 50]

| Ensemble | Construction | Δ₃_sat | ±std |
|---|---|---|---|
| H_flat | H_{jk} = exp(2πiφ_{jk}), φ~U[0,2π] | **0.256** | ±0.010 |
| C1 | H_{jk} = Λ(\|j-k\|+1) × exp(2πiφ_{jk}) | **0.243** | ±0.017 |
| GUE_control | H = (A+A†)/√(2N), A_{jk}~CN(0,1)/√2 | **0.227** | ±0.010 |
| GUE theory (N→∞) | (1/2π²)(ln(2πL)+γ−5/4) at L≈37 | 0.242 | — |
| Riemann zeta zeros | Measured target | 0.155 | — |

## Overlap Test

H_flat vs. C1: difference = 0.013, combined uncertainty = 0.020. **Difference < 1σ. Not distinguishable.**

All three N=500 ensembles span 0.227–0.256 — consistent with each other within sampling noise.

## What This Resolves

**C1 anomalous rigidity claim RETRACTED.** Δ₃_sat ≈ 0.243 is the expected finite-size GUE value at N=500. It is not caused by Von Mangoldt amplitude structure. The claim is downgraded from WEAK (E008) to NOT NOVEL.

**Prior Δ₃_sat = 0.285 (E005) was sampling variation.** The E005 value (5 realizations) is within 2.5σ of the E009 C1 mean (0.243 ± 0.017). Realization-to-realization variability is substantial at N=500.

**Finite-size vs. infinite-N GUE:** The infinite-N GUE theory gives Δ₃_sat ≈ 0.566 at L≈37. At N=500, finite-size effects reduce this to ~0.22–0.26 — a factor of ~2.3× lower. Prior comparisons that called C1 "50% of GUE" were comparing to infinite-N theory; against the correct finite-size GUE baseline, C1 is unremarkable.

## Formula Bug: Residuals vs. Staircase Integration

The GOAL.md specified a Δ₃ formula that samples only at eigenvalue positions: Δ₃ ≈ mean(residuals²)/L. This is incorrect. The Dyson-Mehta integral integrates the piecewise-constant staircase N(E) over ALL values of E — not just the eigenvalue positions. The flat segments between eigenvalues contribute substantially.

The wrong formula underestimates Δ₃ by ~50×. The explorer independently diagnosed this bug by observing that the GUE control gave Δ₃_sat ≈ 0.01 (impossible — should be ~0.22–0.26). Correct implementation uses `compute_delta3_exact_staircase` — analytical integration of the piecewise flat staircase.

## Central Gap Confirmed

**No construction in S001–S002 achieves Δ₃_sat < 0.2.** All N=500 ensembles give Δ₃_sat ≈ 0.23–0.26; Riemann zeta zeros give Δ₃_sat ≈ 0.155. The gap is ~40%. This gap is confirmed by E009 and remains the defining unsolved problem for Strategy 003.

Surviving novel claims from E008 (N²/p scaling law, Dirichlet character algebraic impossibility) are unchanged and independent of the C1 rigidity claim.
