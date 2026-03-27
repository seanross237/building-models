# Meta-Learning: Exploration 001

## What worked well
- **Providing explicit formulas** (Montgomery pair correlation, Wigner surmise) enabled the explorer to go straight to code rather than spending time researching.
- **Explicit instruction "this is a COMPUTATION task, write Python code"** worked — the explorer wrote ~450 lines of Python and executed it.
- **Classification scheme** (EXACT/STRONG/MODERATE/WEAK/DISCREPANCY) was used correctly in the output.
- **Failure criteria with fallback plan** was critical: the explorer's first attempt (5000 zeros) timed out at 10 minutes, so it killed the process and rewrote with 2000 zeros. This adaptive behavior saved the exploration.

## What didn't work well
- **10,000 zeros was way too ambitious for mpmath.** The initial attempt tried to compute 5000 zeros and timed out. Even 2000 zeros took ~6 minutes. Future explorations requiring many zeros should either use fewer zeros or implement faster algorithms (Riemann-Siegel).
- **High-height zeros at n=100,000 were infeasible.** The explorer adapted to n~10,000 but could only get 500 zeros in ~6 minutes. Goal was overambitious for mpmath's capabilities.
- **Report writing started with a skeleton (22 lines) that wasn't updated until all computation was done.** This made it look like the explorer was stuck when it was actually computing.

## Lessons for future explorations
1. **For computational tasks, budget computation time explicitly.** Say "you have ~10 minutes total for all computations" or similar. mpmath.zetazero(n) runs at roughly 5-18 zeros/s for n < 2000 and ~1.5 zeros/s for n ~ 10,000.
2. **When requesting computations at different parameter ranges, prioritize.** Say "if you can only do one range, do the low-height zeros first" rather than leaving the explorer to figure out time allocation.
3. **The Wigner surmise is approximate enough to be detected at N=2000.** Future spacing distribution comparisons should use the exact GUE distribution (Fredholm determinant) or at least acknowledge the Wigner approximation error upfront.
