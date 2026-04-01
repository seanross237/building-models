# Exploration 001: GUE Pair Correlation and Nearest-Neighbor Spacing for Riemann Zeta Zeros

## Mission Context

We are investigating the spectral approach to the Riemann Hypothesis — the conjecture that the non-trivial zeros of the Riemann zeta function are eigenvalues of an undiscovered self-adjoint operator. A key piece of evidence for this is the Montgomery-Odlyzko law: the statistical properties of zeta zeros match those of eigenvalues of large random matrices from the Gaussian Unitary Ensemble (GUE).

This is the FIRST exploration in a systematic effort to build a catalog of computable constraints on this hypothetical operator. We start with the most fundamental statistical tests.

## Your Task

**This is a COMPUTATION task. Write Python code, execute it, and report the numerical results. Do NOT spend time on background research or web searches — all the information you need is below.**

Write and execute Python code to:

### Part 1: Compute Riemann Zeta Zeros
- Use `mpmath.zetazero(n)` to compute the first 10,000 non-trivial zeta zeros (the imaginary parts t_n where zeta(1/2 + i*t_n) = 0, t_n > 0).
- If 10,000 is too slow, use at least 2,000 zeros. Report how many you computed.
- Also compute zeros at HIGH height: use `mpmath.zetazero(n)` for n around 100,000 (e.g., zeros 99,001 to 100,000 or a subset). This tests whether GUE agreement changes at larger heights.

### Part 2: Pair Correlation Function R2
The pair correlation function measures the distribution of spacings between ALL pairs of zeros (not just nearest neighbors).

**Definition:** Given N zeros with imaginary parts t_1 < t_2 < ... < t_N, define the unfolded zeros as:
  x_n = (t_n / (2*pi)) * log(t_n / (2*pi*e))
(This is the smooth part of the zero-counting function N(T) ~ (T/(2*pi)) * log(T/(2*pi*e)).)

The pair correlation is the density of differences x_i - x_j for i != j.

**Montgomery's conjecture (1973):** The pair correlation function is:
  R2(r) = 1 - (sin(pi*r) / (pi*r))^2

This is identical to the GUE pair correlation (Dyson).

**What to compute:**
1. Unfold the zeros using the formula above.
2. Compute all pairwise differences of unfolded zeros.
3. Bin these differences into a histogram (use bins of width ~0.05 from r=0 to r=5).
4. Normalize to get the empirical pair correlation function.
5. Compare to Montgomery's prediction: R2(r) = 1 - (sin(pi*r)/(pi*r))^2.
6. Report the maximum absolute deviation, mean absolute deviation, and produce a comparison (print the empirical vs. predicted values at r = 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0).
7. **Do this separately for the low-height zeros and the high-height zeros.** Report whether agreement improves at larger height.

### Part 3: Nearest-Neighbor Spacing Distribution P(s)
The nearest-neighbor spacing distribution measures the gaps between consecutive zeros.

**Definition:** Given unfolded zeros x_1 < x_2 < ... < x_N, the spacings are s_n = x_{n+1} - x_n. The distribution of these spacings should match the GUE nearest-neighbor spacing distribution.

**GUE prediction (Wigner surmise approximation):**
  P_GUE(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)

(This is the Wigner surmise for GUE, which is an excellent approximation to the exact GUE spacing distribution.)

**What to compute:**
1. Compute the spacings s_n = x_{n+1} - x_n from unfolded zeros.
2. Normalize: the mean spacing should be 1 after unfolding. If it's not, rescale.
3. Bin into a histogram (bins of width ~0.05 from s=0 to s=4).
4. Compare to P_GUE(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi).
5. Report the maximum absolute deviation, mean absolute deviation.
6. **Key diagnostic:** Report the fraction of spacings with s < 0.1 (level repulsion). GUE predicts very few near-zero spacings. The exact fraction matters.
7. **Do this separately for low-height and high-height zeros.**

### Part 4: Constraint Extraction
Based on your computed results, answer:
1. How constraining are these statistics? If we were searching for the Riemann operator, what operators could we rule out based on pair correlation alone? (E.g., any operator with Poisson statistics is ruled out. Any operator with GOE statistics instead of GUE is ruled out.)
2. Are there ANY deviations from GUE predictions, even small ones? Report deviations with error estimates.
3. What is the precision of the GUE match? Express as: "The pair correlation matches GUE to within X% for the first N zeros."
4. Do the statistics change between low height and high height? Any trend?

## Success Criteria
- Code executes successfully and produces numerical results for at least 2,000 zeros.
- Pair correlation function is computed and compared to Montgomery's prediction with quantitative error measures.
- Nearest-neighbor spacing distribution is computed and compared to Wigner surmise with quantitative error measures.
- Results for both low-height and high-height zeros are reported.
- A clear statement of which operator types are ruled out by these constraints.

## Failure Criteria
- If computation takes too long (>10 minutes for zero computation), reduce N and report what N was achievable.
- If mpmath is not available, try to `pip install mpmath` first.
- If the computation cannot be completed, explain exactly what went wrong, what numerical precision or computational resources would be needed, and what the results SHOULD look like based on published work (cite Odlyzko 1987, Montgomery 1973).

## Output
Write your detailed findings to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-001/REPORT.md`

Write a concise summary (under 80 lines) to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-001/REPORT-SUMMARY.md`

Target report length: 300-500 lines including computed data tables.

## Classification Scheme for Results
For each statistic, classify the GUE match as:
- **EXACT MATCH**: deviation < 1% across all bins
- **STRONG MATCH**: deviation < 5% across all bins
- **MODERATE MATCH**: deviation < 10% or a few outlier bins
- **WEAK MATCH**: systematic deviations > 10%
- **DISCREPANCY**: qualitative disagreement with GUE prediction
