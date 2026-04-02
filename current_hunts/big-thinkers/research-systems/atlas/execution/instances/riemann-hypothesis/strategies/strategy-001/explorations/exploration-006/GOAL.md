# Exploration 006: Arithmetic Operator Construction — Von Mangoldt Toeplitz Matrix

## Mission Context

We are investigating the spectral approach to the Riemann Hypothesis. Key findings so far:
1. Zeta zeros match GUE statistics (10-point constraint catalog, explorations 001-002)
2. Simple xp regularizations produce 0/10 matching constraints (exploration 003)
3. The trace formula determines spectral DENSITY but not CORRELATIONS (exploration 004)
4. The key missing ingredient: an operator that has prime numbers encoded in its structure

This exploration takes a different approach: instead of regularizing xp, construct an operator directly from arithmetic functions and test whether its spectrum has any connection to zeta zeros or GUE statistics.

## Your Task

**This is a COMPUTATION task. Write Python code, execute it, report numerical results. Do NOT do web research.**

**Computation budget: ~5 minutes total. NO zero computation needed — focus on matrix construction and eigenvalue analysis.**

### Part 1: Von Mangoldt Toeplitz Matrix

The von Mangoldt function Lambda(n) is:
- Lambda(n) = ln(p) if n = p^k for some prime p and integer k >= 1
- Lambda(n) = 0 otherwise

It's the natural function encoding primes. Its Dirichlet series is -zeta'(s)/zeta(s) = sum Lambda(n)/n^s.

**Construct the Toeplitz matrix T of size N x N:**
T_{ij} = Lambda(|i-j|+1) for i != j
T_{ii} = 0 (or = ln(2*pi), a normalization constant)

This is a real symmetric matrix whose off-diagonal entries encode the prime structure.

**What to compute:**
1. Construct T for N = 200, 500, 1000
2. Compute ALL eigenvalues using numpy.linalg.eigvalsh
3. Report: eigenvalue range, mean, std, density of states shape
4. **Key test:** Does the eigenvalue density have any connection to the zeta function? Specifically, look at the eigenvalue density near zero — is there a gap, a peak, or a smooth density?

### Part 2: Statistical Analysis of Eigenvalues

For the N=1000 matrix:
1. **Unfold the eigenvalues** — compute the smooth eigenvalue density (e.g., using a histogram or kernel density estimate), then rescale to unit mean spacing
2. **Compute NN spacing distribution P(s)** and compare to GUE, GOE, and Poisson
3. **Compute pair correlation R2** and compare to Montgomery's conjecture
4. **Score against the constraint catalog:**
   - Constraint 2 (Pair correlation): compute and compare
   - Constraint 3 (NN spacing): compute and compare
   - Constraint 4 (Poisson/GOE ruled out): test
   - Constraint 5 (Level repulsion): check P(s→0) ~ s^beta, report beta

### Part 3: Variants

Try at least TWO of these variants and compare:

**Variant A: Normalized von Mangoldt**
- a(n) = Lambda(n) / sqrt(n) (decaying entries — more convergent)
- Same Toeplitz construction

**Variant B: Mobius Toeplitz**
- a(n) = mu(n) (the Mobius function: +1 if n is squarefree with even number of prime factors, -1 if odd, 0 if has a square factor)
- This is connected to 1/zeta(s)

**Variant C: Log-zeta Hankel matrix**
- H_{ij} = Lambda(i+j) (Hankel structure instead of Toeplitz)
- Different spectral properties from Toeplitz

For each variant, compute eigenvalues (N=500) and report spacing distribution.

### Part 4: Assessment

1. **Which matrix (if any) has GUE-like eigenvalue statistics?** Report the closest match and quantify.
2. **Does ANY arithmetic matrix produce the super-rigidity seen in zeta zeros?** (Constraint 9: 30-50% more rigid than finite-size GUE)
3. **What universality class do arithmetic Toeplitz matrices fall into?** (GUE, GOE, Poisson, or none?)
4. **Novel observation:** Is there ANYTHING unexpected in the spectral properties of these matrices? A feature that hasn't been studied?

## Success Criteria
- At least 2 matrix variants computed at N >= 500
- Spacing distribution compared to GOE, GUE, Poisson for each variant
- Clear classification of universality class for each variant
- A statement about whether arithmetic operators can produce zeta-zero-like spectra

## Failure Criteria
- If N=1000 is too slow, use N=500
- If unfolding is problematic, use the empirical CDF method

## Output
Write detailed report to:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-006/REPORT.md`

Write summary (under 80 lines) to:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-006/REPORT-SUMMARY.md`
