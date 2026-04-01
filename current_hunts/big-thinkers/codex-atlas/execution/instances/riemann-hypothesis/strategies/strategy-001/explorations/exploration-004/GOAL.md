# Exploration 004: Trace Formula Reconstruction — xp + Primes = Zeta Zeros?

## Mission Context

We are investigating the spectral approach to the Riemann Hypothesis. Previous explorations established:
1. A 10-point constraint catalog from GUE statistics of zeta zeros (explorations 001-002)
2. All simple regularizations of Berry-Keating xp fail the catalog (exploration 003)
3. The key insight: "The prime number input is the entire ball game" — xp gives only the smooth (Weyl) density; fluctuations come from primes

This exploration tests the core Berry-Keating hypothesis computationally: can we reconstruct the zeta zero spectrum by starting from the smooth xp spectrum and adding oscillatory corrections from the explicit formula?

## Your Task

**This is a COMPUTATION task. Write Python code, execute it, report numerical results. Do NOT do web research.**

**Computation budget: ~8 minutes total. Use 2000 zeta zeros computed via mpmath.**

### Background: The Explicit Formula

The Riemann-von Mangoldt formula gives the zero-counting function:

N(T) = N_smooth(T) + N_osc(T)

where:
- N_smooth(T) = (T/(2*pi)) * ln(T/(2*pi*e)) + 7/8  (the Weyl term — from xp)
- N_osc(T) = -(1/pi) * arg(zeta(1/2 + iT))  (the oscillatory part — from primes)

The **explicit formula** connects N_osc to primes:

N_osc(T) ≈ -(1/pi) * sum_p sum_{m=1}^{inf} (ln(p) / (m * p^{m/2})) * sin(m * T * ln(p))

where the sum runs over primes p and their powers m.

### Part 1: Compute Zeta Zeros and the Smooth Spectrum

1. Compute the first 2000 zeta zeros t_1, ..., t_2000 using mpmath.zetazero(n) (this takes ~5-6 minutes)
2. Also compute the "smooth spectrum" — the equally-spaced approximation. For each n = 1, 2, ..., 2000, find t_n^{smooth} such that N_smooth(t_n^{smooth}) = n - 1/2 (i.e., invert the smooth counting function). This can be done via Newton's method:
   - Start with t_0 = 2*pi*(n-1/2)/W(something), or just use a root finder
   - Solve: (t/(2*pi)) * ln(t/(2*pi*e)) + 7/8 = n - 1/2
3. Report the first 20 values: t_n (actual), t_n^{smooth} (smooth), and the difference delta_n = t_n - t_n^{smooth}

### Part 2: Prime Corrections

The oscillatory correction to the nth zero is approximately:

delta_n ≈ -(1/pi) * sum_p sum_{m=1}^{M} (ln(p) / (m * p^{m/2})) * sin(m * t_n^{smooth} * ln(p)) / N_smooth'(t_n^{smooth})

where N_smooth'(T) = (1/(2*pi)) * ln(T/(2*pi)) is the derivative of the smooth counting function, and we divide by it to convert from a correction to N into a correction to t.

Compute the prime-corrected spectrum:

t_n^{corrected} = t_n^{smooth} + delta_n^{prime}

where delta_n^{prime} uses:
- All primes p up to some cutoff P_max (try P_max = 100, 1000, 10000)
- m up to M = 5 (higher powers of primes contribute less)

**What to compute for each P_max:**
1. The corrected spectrum t_n^{corrected}
2. The residual: r_n = t_n - t_n^{corrected} (how much the prime corrections DON'T explain)
3. Statistics of the residual: mean, std, max

### Part 3: Statistical Testing of the Corrected Spectrum

For the BEST prime correction (whichever P_max gives smallest residuals):

1. **Unfold the corrected spectrum** using the standard formula
2. **Compute pair correlation R2** and compare to Montgomery's conjecture
3. **Compute NN spacing P(s)** and compare to GUE Wigner surmise
4. **Score against the constraint catalog:**
   - Constraint 1 (GUE symmetry): Can't test directly (no matrix)
   - Constraint 2 (Pair correlation): Compute and compare
   - Constraint 3 (NN spacing): Compute and compare
   - Constraint 4 (Poisson/GOE ruled out): Test
   - Constraint 5 (Level repulsion): Check P(s→0) ~ s^beta, report beta
   - Constraint 6 (Number variance saturation): Compute Sigma^2(L)
   - Constraint 7 (Spectral rigidity): Compute Delta_3(L)
   - Constraints 8-10: As feasible

### Part 4: Convergence and Residual Analysis

The key questions:
1. **Does the corrected spectrum converge to the actual zeros as P_max increases?** Plot mean|residual| vs P_max.
2. **What does the residual look like?** After subtracting the prime corrections, is the remaining error:
   - Random (noise-like, decreasing with P_max)?
   - Systematic (a pattern that persists regardless of P_max)?
   - Related to higher-order terms in the explicit formula?
3. **How many primes are needed to match the constraint catalog?** Find the MINIMUM P_max where the corrected spectrum passes constraints 2-7.
4. **Is there a "prime gap" — a residual that no number of primes can explain?** This would suggest the Berry-Keating decomposition is incomplete and something beyond xp + primes is needed.

## Success Criteria
- The smooth spectrum t_n^{smooth} and at least two P_max levels computed
- Residual analysis showing convergence (or not) with P_max
- At least 3 constraints tested on the corrected spectrum
- A clear answer to: "Does xp + primes = zeta zeros, within computational precision?"

## Failure Criteria
- If zero computation takes >6 minutes, reduce to 1000 zeros
- If the prime correction sum converges too slowly, note this as a finding
- If any part fails, complete the other parts

## Output
Write detailed report to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-004/REPORT.md`

Write summary (under 80 lines) to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-004/REPORT-SUMMARY.md`

Target report length: 300-500 lines.
