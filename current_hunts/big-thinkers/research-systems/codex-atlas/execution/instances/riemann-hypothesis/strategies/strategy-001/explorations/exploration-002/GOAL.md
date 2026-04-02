# Exploration 002: Number Variance, Spectral Rigidity, and Berry's Saturation

## Mission Context

We are investigating the spectral approach to the Riemann Hypothesis. In exploration 001, we established that zeta zeros match GUE statistics for pair correlation (9% mean relative deviation, noise-consistent) and nearest-neighbor spacing (4% mean absolute deviation). GUE was definitively the best-fitting ensemble.

Now we need long-range spectral statistics. These probe correlations between zeros that are far apart (not just nearest neighbors). The key prediction to test: **Berry (1985) predicted that the number variance of zeta zeros should saturate (deviate from the pure GUE prediction) at a scale related to the shortest periodic orbit.** This would be a deviation FROM GUE — one that constrains the operator's periodic orbit structure.

## Your Task

**This is a COMPUTATION task. Write Python code, execute it, and report numerical results. Do NOT spend time on web searches. All formulas are provided below.**

**Computation time budget: aim for ~5 minutes total. Use the first 2,000 zeta zeros computed via mpmath.zetazero(n). Do NOT attempt more than 2,000 zeros — mpmath is too slow for larger sets.**

### Step 0: Compute Zeros (reuse or recompute)

Use `mpmath.zetazero(n)` for n=1 to 2000. If this takes too long (>5 minutes), reduce to 1000. Store the imaginary parts t_n.

Unfold using: x_n = (t_n / (2*pi)) * log(t_n / (2*pi*e))

Verify mean spacing is approximately 1 after unfolding.

### Part 1: Number Variance Sigma^2(L)

**Definition:** For a window of length L in unfolded coordinates, count the number of zeros n(L, x) in the interval [x, x+L]. Slide the window across the zero sequence. The number variance is:

Sigma^2(L) = Var(n(L, x)) = <n(L,x)^2> - <n(L,x)>^2

where the average is over different window positions x.

**GUE prediction:**
Sigma^2_GUE(L) = (2/pi^2) * [log(2*pi*L) + gamma + 1 - pi^2/8]

where gamma = 0.5772... is the Euler-Mascheroni constant.

For large L this grows logarithmically.

**Berry's saturation prediction:**
For the zeta zeros specifically, Berry (1985, "Semiclassical theory of spectral rigidity") predicts that Sigma^2(L) deviates from GUE for L > L_max, where L_max is related to the Heisenberg time T_H. For zeros near height T:
L_max ~ T/(2*pi) * log(T/(2*pi))
Beyond L_max, the number variance saturates (stops growing) because the discrete prime spectrum cuts off the spectral form factor.

With 2000 zeros at heights T ~ 14 to 2500, we have L_max in the hundreds. The saturation may or may not be detectable — compute Sigma^2(L) for L from 0.1 to 100 (logarithmically spaced, ~50 points) and report whether saturation is visible.

**What to compute:**
1. For each L value, slide a window of length L across the unfolded zeros (step size = 0.5 or similar), count zeros in each window, compute variance.
2. Plot/print Sigma^2(L) vs L alongside the GUE prediction.
3. Report the maximum absolute deviation and the L value where deviation is largest.
4. Report whether there is any sign of saturation (Sigma^2 leveling off while GUE prediction continues to grow).

### Part 2: Spectral Rigidity Delta_3(L)

**Definition (Dyson-Mehta):** Delta_3(L) measures how well the staircase function N(x) (counting function of unfolded zeros) is approximated by a best-fit straight line over an interval of length L.

Delta_3(L) = min_{a,b} (1/L) * integral_0^L [N(x) - a - bx]^2 dx

where the minimum is over constants a, b.

In practice, for a discrete set of unfolded zeros {x_1, x_2, ...}:
- For each interval [x_start, x_start + L], find the best-fit line through the staircase and compute the mean-squared deviation
- Average over positions x_start

**GUE prediction:**
Delta_3_GUE(L) = (1/pi^2) * [log(2*pi*L) + gamma - 5/4 - pi^2/12]

**What to compute:**
1. Compute Delta_3(L) for L from 0.5 to 100 (logarithmically spaced, ~30 points)
2. Compare to GUE prediction
3. Report deviations — especially at large L where Berry's saturation should appear

### Part 3: Spectral Form Factor K(tau)

**Definition:** The spectral form factor is the Fourier transform of the pair correlation function. For discrete data:

K(tau) = (1/N) * |sum_{n=1}^{N} exp(2*pi*i*tau*x_n)|^2

**GUE prediction:**
K_GUE(tau) = 2*tau     for tau < 1
K_GUE(tau) = 2 - 1/tau  for tau > 1  (but this is the connected part approximation)

Actually, simpler: for the connected two-point correlator (subtracting the disconnected part):
K_GUE(tau) = tau       for 0 < tau < 1
K_GUE(tau) = 1         for tau > 1

The "ramp" (linear growth) for tau < 1 and "plateau" (constant) for tau > 1 is characteristic of GUE.

**What to compute:**
1. Compute K(tau) for tau from 0.01 to 3 (~50 points)
2. Check whether the ramp-plateau structure is visible
3. Report the transition point (should be near tau = 1)
4. Report deviations from GUE prediction

### Part 4: Constraint Extraction and Synthesis

Based on your computed results, answer:
1. **Is Berry's saturation detected?** If yes, at what scale L? If no, what is the upper bound on the saturation scale (the largest L where GUE is still consistent)?
2. **What do the long-range statistics tell us about the Riemann operator that short-range statistics don't?** Specifically:
   - Does the number variance constrain the periodic orbit spectrum of the operator?
   - Does the spectral form factor show the "ramp-plateau" structure predicted by GUE?
3. **Combined constraint summary:** Combine with exploration 001's results. What is the total constraint catalog so far?

## Success Criteria
- Number variance computed for at least 20 values of L and compared to GUE prediction
- Spectral rigidity computed for at least 15 values of L and compared to GUE prediction
- Spectral form factor computed and ramp-plateau structure checked
- Clear statement of whether Berry's saturation is detected or not
- Combined constraint catalog with exploration 001

## Failure Criteria
- If computation takes too long, reduce to 1000 zeros and/or fewer L values
- If the sliding window computation is too slow, use larger step sizes
- If any part fails, complete the other parts and explain what failed

## Output
Write detailed findings to:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-002/REPORT.md`

Write concise summary (under 80 lines) to:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-002/REPORT-SUMMARY.md`

Target report length: 300-500 lines.

## Classification Scheme
- **GUE CONFIRMED**: matches GUE prediction within statistical noise
- **SATURATION DETECTED**: clear deviation from GUE consistent with Berry's prediction
- **ANOMALOUS DEVIATION**: deviation from GUE NOT consistent with Berry's prediction (this would be very interesting)
- **INCONCLUSIVE**: insufficient data to distinguish GUE from saturation

## Context from Exploration 001
- First 2000 zeros range: t in [14.13, 2515.29]
- Unfolding formula: x_n = (t_n/(2*pi)) * log(t_n/(2*pi*e))
- Mean unfolded spacing: 0.999965 (excellent)
- mpmath.zetazero rate: ~5-18 zeros/s for n < 2000
- pip install mpmath numpy scipy first if needed
