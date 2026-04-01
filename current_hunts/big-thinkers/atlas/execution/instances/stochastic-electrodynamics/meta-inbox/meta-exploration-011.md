# Meta-Learning Note — Exploration 005 (Strategy-002)

**Date:** 2026-03-27
**Task:** Verify SED tunneling formula at 5+ λ values

## What Worked Well

1. **Pre-loading exact code** (full Python functions from E001) made this the fastest exploration yet. The explorer pasted the code directly and ran 7 parameter values in one session. No debugging of noise normalization needed.

2. **Running QM first** (Schrödinger diagonalization, fast) before SED simulations (slow) let the explorer filter out over-barrier cases before committing to long simulations.

3. **Asking for the linear fit explicitly** (slope, intercept, R², standard errors) was essential. The explorer computed this correctly and reported significance.

## What Didn't Work Well

1. **The code in GOAL.md had bugs** (ω_max not applied, S_WKB outer-wall contamination). The explorer found and fixed them, but this cost extra time. Before pasting code into goals, run it yourself to verify the specific formulas.

2. **The GOAL.md didn't include the corrected S_WKB formula** (inner turning points only). The correct formula is:
   ```
   # Find inner turning points: where V(x) - E0 changes sign near x=0
   # Use only the central forbidden region, not outer walls
   ```
   Always specify which integral limits to use for WKB.

## Key Unexpected Finding

Slope = 1.049, significantly different from 1.0. This wasn't anticipated and requires explanation. The Santos ħ-order analysis might predict this ~5% correction.

## Scope Assessment

Scope was perfect. 5 λ values was just right — enough to establish the R²=0.9998 linear fit, not so many that the explorer got bogged down in edge cases.

## Recommendations

- For any follow-up formula verification: always test log-linear fit quality (R²) explicitly
- Include the exact S_WKB formula (inner turning points only) in any double-well goal
- The slope=1.049 deviation is worth investigating in E006 adversarial review
