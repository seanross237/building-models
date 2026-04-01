# Exploration 005: Two-Point Correlation from Prime Pairs — Montgomery's Formula

## Mission Context

Previous explorations established:
1. Zeta zeros match GUE with 10-point constraint catalog (explorations 001-002)
2. Simple xp regularizations fail (exploration 003)
3. **Critical insight (exploration 004)**: The one-point trace formula determines SPECTRAL DENSITY (via counting function N(T)) but NOT SPECTRAL CORRELATIONS (pair correlation, etc.). The Gibbs phenomenon makes individual zero reconstruction impossible.

But exploration 004 also identified a potential resolution: the **two-point trace formula** might encode correlations through PAIRS of primes. Montgomery (1973) proved that the pair correlation of zeta zeros is connected to prime pairs. This exploration tests whether that connection can be computed explicitly.

## Your Task

**This is a COMPUTATION + ANALYSIS task. Write Python code, execute it, and synthesize the results into a clear picture of how primes determine (or fail to determine) spectral correlations.**

**Computation budget: ~10 minutes total.**

### Part 1: Montgomery's Pair Correlation via Number Theory

Montgomery (1973) showed that for the pair correlation of zeta zeros:

R2(alpha) = 1 - (sin(pi*alpha)/(pi*alpha))^2 + delta(alpha)

This can be derived from the prime number theorem and the explicit formula as follows.

The two-point form factor (Fourier transform of pair correlation) is:

F(x) = |x|     for |x| < 1

Montgomery proved this by showing:

F(x) = sum over primes p of (ln(p))^2 / p * [p^{ix} + p^{-ix}] + lower order terms
     = 2 * sum_p (ln(p))^2 / p * cos(x * ln(p)) + ...

for x in the range where Montgomery could evaluate the sum.

**What to compute:**

1. Compute the prime sum: S(x) = sum_{p <= P_max} (ln(p))^2 / p * cos(x * ln(p))
   for x from 0 to 5 with step 0.01, and for P_max = 100, 1000, 10000, 100000.

2. Compare 2*S(x) to the theoretical prediction F(x) = |x| for |x| < 1 and F(x) = 1 for |x| > 1.

3. Report the convergence: does 2*S(x) approach |x| as P_max increases?

4. For the SAME x values, also compute the two-point form factor DIRECTLY from the zeta zeros:
   F_zeros(x) = (1/N) * |sum_{n=1}^{N} e^{2*pi*i*x*gamma_n/C}|^2
   where gamma_n are the (unfolded) zero positions and C is a normalization constant.
   Use N = 2000 zeros (compute via mpmath.zetazero).

5. Compare three things: F_primes(x) (from step 1), F_zeros(x) (from step 4), and F_GUE(x) = min(|x|, 1) (theory).

### Part 2: The Diagonal and Off-Diagonal Contributions

In random matrix theory and quantum chaos, the form factor has two parts:
- **Diagonal** contribution: sum over INDIVIDUAL prime orbits → gives the "ramp" (F = |x|)
- **Off-diagonal** contribution: sum over PAIRS of different prime orbits → gives corrections

Montgomery's result involves only the diagonal part (single prime terms). The off-diagonal terms (cross-terms between different primes) are what extend the result beyond |x| < 1.

**What to compute:**

1. Separate the prime sum into diagonal and off-diagonal parts:
   - Diagonal: S_diag(x) = sum_p (ln(p))^2/p * cos(x*ln(p))
   - Off-diagonal: include cross terms between different prime powers

2. Actually, the off-diagonal is more subtle. Instead, compute the FULL two-point correlation:
   C2(tau) = sum_{p,q primes, m,n >= 1} [ln(p)*ln(q) / (p^{m/2}*q^{n/2})] * cos(tau*(m*ln(p) - n*ln(q)))

   Split into:
   - (p,m) = (q,n) terms: diagonal
   - (p,m) != (q,n) terms: off-diagonal

3. Compare diagonal-only vs full sum to see if off-diagonal terms are significant.

### Part 3: Pair Correlation from Primes — Direct Computation

The explicit formula for the pair correlation density of zeta zeros at height T is (Bogomolny & Keating, 1996):

R2(s) = 1 - [sin(pi*s)/(pi*s)]^2 + sum_{p prime} sum_{m=1}^{M} [2*(ln p)^2 / (p^m * (2*pi)^2)] * [something involving cos(2*pi*s*m*ln(p)/ln(T/(2*pi)))]

The exact form involves the density of states and Fourier transforms. Rather than implementing this complicated formula:

**Alternative approach: Direct numerical comparison.**

1. Compute pair correlation from 2000 zeta zeros (as in exploration 001)
2. Compute the GUE prediction: R2_GUE(s) = 1 - (sin(pi*s)/(pi*s))^2
3. Compute the DIFFERENCE: delta_R2(s) = R2_zeros(s) - R2_GUE(s)
4. Compare this difference to what the prime sum predicts (should be small corrections)
5. Test if the prime corrections improve the GUE fit

### Part 4: Synthesis

Answer these key questions:
1. **Do primes determine correlations?** Can the pair correlation be reconstructed from prime sums, or is exploration 004's insight correct that correlations require the operator?
2. **What's the relationship between the one-point failure (exploration 004) and the two-point formula?** Why does the one-point trace formula fail to give individual zeros while the two-point formula can give pair correlation?
3. **What's the hierarchical structure?** One-point → density, two-point → pair correlation, three-point → ??? Do we need ALL n-point functions, or is there a finite set that determines the operator?
4. **Revised constraint catalog:** Based on these results, what additional constraints can we add to the catalog?

## Success Criteria
- Form factor computed from both primes and zeros, compared quantitatively
- Clear statement of whether primes determine pair correlation
- Synthesis of the one-point/two-point relationship
- At least one new constraint added to the catalog

## Failure Criteria
- If zero computation takes too long, use 1000 zeros
- If the prime sum doesn't converge, report at what P_max it stabilizes
- Focus on the questions, not the formulas — if a formula is wrong, explain the correct physics

## Output
Write detailed report to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-005/REPORT.md`

Write summary (under 80 lines) to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-005/REPORT-SUMMARY.md`
