# Exploration 004 — Summary

## Goal
Test whether N²/p_opt ≈ 275 is a universal scaling constant for the peak Brody β of Gauss sum matrices H_{jk} = Λ(|j-k|+1) × exp(2πijk/p), across N ∈ {250, 500, 1000}.

## What Was Done
1. **Baseline replication (N=500):** Tested 6 fitting methods against S002 targets. Discovered S002 used Wigner interpolated distribution (not Brody). Reproduced S002 values to <0.04 error with histogram-based Wigner fit.
2. **N=250 sweep:** 26 primes tested (N²/p from 25 to 2717). Peak β_W=1.318 at p=277 (N²/p=225.6).
3. **N=1000 sweep:** 19 primes tested (N²/p from 100 to 500). Peak β_W=1.019 at p=4999 (N²/p=200.0).
4. **Universality assessment:** Compared peak positions and heights across all three N values.

## Outcome: HYPOTHESIS REJECTED

The N²/p ≈ 275 universal scaling is **not supported**. Peak N²/p values are 225.6 (N=250), 309.0 (N=500), 200.0 (N=1000) — a factor 1.5× spread with no convergence. Peak β_max *decreases* with N (1.32 → 1.15 → 1.02), opposite to what a convergent scaling law predicts.

## Verification Scorecard
- **[CHECKED]:** 2 (baseline replication matches S002 targets; methodology identification)
- **[COMPUTED]:** 5 (N=250 peak, N=1000 peak, universality comparison, β_max trend, rejection verdict)
- **[CONJECTURED]:** 0

## Key Takeaway
The Gauss sum matrix β peak is not governed by a simple N²/p scaling law. The signal is noise-dominated at these matrix sizes (~250–1000 spacings per point), and the apparent S002 "peak at N²/p≈275" was likely a favorable fluctuation at a single matrix size. The fitting method (Wigner histogram vs Brody MLE) significantly affects both peak location and height, further undermining claims of universality.

## Unexpected Findings
- **S002 used Wigner interpolated distribution**, not Brody. The "β=1.154" target is a Wigner β, not a Brody β. The corresponding Brody β is ~1.010.
- **Peak β_max decreases with N** — this is the strongest evidence against universality and suggests the observed spectral repulsion at intermediate N²/p is a finite-size effect.
- **The p≈N resonance** creates a dramatic β→0 collapse at p=251, N=250, contaminating the entire 240–260 region.

## Computations Identified for Follow-up
1. Large-N test (N=5000) at N²/p ∈ {200, 250, 275, 300, 350} to check if peaks converge
2. Bootstrap confidence intervals on β fits to quantify noise vs signal
3. Investigate whether Brody MLE peaks (N²/p≈290–310 for N=500,1000) are more robust than Wigner peaks
