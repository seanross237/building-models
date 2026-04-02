# Meta-Learning Note — Strategy-001 Exploration 007

**Date:** 2026-03-27
**Exploration:** 007 — β^0.40 Mechanism: Spectral Noise Comparison (4 noise spectra × 4 β values)

## What Worked

**Multi-ansatz sweep is highly efficient for mechanism investigations.** Four variants ran in ~10 minutes total with a single script. The goal design (one script, four noise exponents, same parameters) was correct — the explorer executed exactly what was asked.

**Pre-loading QM reference values and the FFT normalization formula** saved time. The explorer immediately ran matrix diagonalization to get precise QM values rather than searching for them.

**The normalization calibration approach** (run β=0, scale C_n to hit var_x=0.500) worked cleanly. Unexpected finding: all C_n values are nearly equal (~0.0198) — because at resonance ω=ω₀=1, S_n(1)=C_n for all n, so the β=0 calibration is spectrum-independent.

**The "sign reversal" result was immediately obvious** from the raw data — no ambiguity. When a result is this clean (n=3 positive, n<3 negative), the explorer focused on interpretation rather than disambiguation.

## What Didn't Work / Cautions

**Normalization choice matters for the α exponent.** E007 found α≈0.25 (calibrated to 0.500), while E004 found α≈0.40 (physical SED normalization 0.516). This discrepancy is important. Always specify whether normalization should match prior explorations or use calibration.

**α fit from negative Δe values was not computed** — the explorer set α=null for n=0,1,2 because Δe was negative. A better design would ask for |Δe| ~ β^α for ALL variants regardless of sign.

## Lesson for Goal Design

When the diagnostic involves comparing signs of errors, ask explicitly for:
1. The SIGN of the error for each variant
2. The MAGNITUDE power law |Δe| ~ β^α for each variant (even if Δe < 0)
3. The normalization target (calibrated or physical) — must match prior explorations if comparing α exponents

## Science Lesson

The "sign flip" diagnostic is powerful for finding critical thresholds. n=2 undershoots, n=3 overshoots → crossover n*≈2.61. This pattern is reusable: whenever you have two variants bracketing a threshold, the crossover gives a direct measurement of the critical parameter.
