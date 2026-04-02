# Exploration 003 — Tournament Entry C: Two-Point Formula + Kernel Operator

## Mission Context

We are investigating the Riemann Hypothesis through the lens of random matrix theory. A previous exploration (strategy-001, exploration-004) established that the **one-point trace formula** (explicit formula for N(T)) fails for individual zero reconstruction because the prime sum converges to the Gibbs midpoint ±0.5 at every zero, and adding more primes makes reconstruction worse (variance explained goes from +80% at P_max=10 to -6% at P_max=10,000).

However, this exploration asks a different question: does the **two-point formula** (pair correlation) succeed where the one-point failed?

**Montgomery (1973) proved:** The pair correlation of zeta zeros is connected to prime pairs. Specifically, the two-point form factor has a prime sum representation. If this prime sum successfully reproduces the numerically-computed pair correlation from actual zeros, it would mean that primes encode spectral CORRELATIONS (not just spectral density).

**Strategy-001 attempted this computation** (exploration-005) but the explorer crashed before completing it. Partial code exists at:
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-005/code/part1_form_factor_primes.py`
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-005/code/part2_form_factor_zeros.py`

**Read those scripts before starting** — they contain working implementations that you can extend.

## Your Task

This is a computation + construction task:

**Part 1:** Compute and compare three versions of the spectral form factor:
- F_primes(x): from prime sums
- F_zeros(x): from actual zeta zeros
- F_GUE(x): theoretical GUE prediction = min(|x|, 1)

**Part 2:** If the two-point formula works, construct a kernel operator from R₂ and score it against the constraint catalog.

**Part 3:** Answer the central question: do primes determine spectral correlations?

## Key Formulas

### Montgomery's Pair Correlation
R₂(r) = 1 - (sin(πr)/(πr))²

This is the GUE prediction. Montgomery proved this is the CORRECT asymptotic pair correlation for zeta zeros (unconditionally for r in the range where he could compute).

### Spectral Form Factor (Fourier transform of R₂)
F(x) = min(|x|, 1)    (GUE theoretical)

F_primes(x) = (1/Z) × Σ_p (ln p)² / p × cos(x · ln p)

**CRITICAL WARNING:** The raw prime sum S(x) = Σ_p (ln p)²/p × cos(x·ln p) DIVERGES as more primes are added (S(0) ~ (1/2)·ln(P_max)²). You must normalize properly:

Berry's normalization (see Berry 1985):
```
F_primes(τ) ≈ (2π/T) × Σ_{p^m ≤ T} (ln p)² / p^m × cos(2πτ · ln(p^m) / ln(T/(2π)))
```
where T is the height of zeros being analyzed, τ is the dimensionless form factor argument (time), and the sum is over prime powers p^m ≤ T (or P_max).

The correct normalization uses:
- ρ_bar = log(T/(2π)) / (2π) — mean zero density at height T
- For 2000 zeros near T≈10⁴: ρ_bar ≈ log(10⁴/(2π))/(2π) ≈ 1.32

### Form Factor from Zeros
F_zeros(τ) = (1/N) × |Σ_{n=1}^{N} exp(2πi·τ·x_n)|²

where x_n are the UNFOLDED zero positions (mean spacing = 1):
x_n = (t_n / 2π) × log(t_n / (2πe))     [standard unfolding formula]

## Part 1: Form Factor Computation

### Step 1: Load zeta zeros
```python
import mpmath
mpmath.mp.dps = 25
N = 2000
zeros = [float(mpmath.zetazero(n).imag) for n in range(1, N+1)]
zeros = np.array(zeros)
```
**This will take ~6 minutes** (2000 zeros at ~5.6/s). Save to file and reload:
```python
np.save('code/zeta_zeros_2000.npy', zeros)
```
Check if the file already exists first:
```python
import os
if os.path.exists('code/zeta_zeros_2000.npy'):
    zeros = np.load('code/zeta_zeros_2000.npy')
else:
    # compute and save
```

Note: Strategy-001's exploration-005 may have already computed these. Check:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-005/part1_results.npz`

### Step 2: Unfold
```python
def unfold(zeros):
    t = np.array(zeros)
    return (t / (2*np.pi)) * np.log(t / (2*np.pi*np.e))

unfolded = unfold(zeros)
# Normalize to mean spacing 1
unfolded = unfolded / np.mean(np.diff(unfolded))
```

### Step 3: Form factor from zeros
```python
def form_factor_zeros(tau_vals, unfolded):
    N = len(unfolded)
    K = np.zeros(len(tau_vals))
    for i, tau in enumerate(tau_vals):
        phases = np.exp(2j * np.pi * tau * unfolded)
        K[i] = np.abs(np.sum(phases))**2 / N
    return K
```
Compute for τ ∈ [0.01, 2.0] with 100 points.

### Step 4: Form factor from primes (normalized)
```python
import sympy
from sympy import primerange

def form_factor_primes_normalized(tau_vals, T, P_max):
    """Berry's normalization of prime form factor."""
    rho_bar = np.log(T / (2*np.pi)) / (2*np.pi)
    primes = list(primerange(2, P_max))

    K = np.zeros(len(tau_vals))
    for i, tau in enumerate(tau_vals):
        s = 0.0
        for p in primes:
            pm = p
            m = 1
            while pm <= P_max:
                ln_pm = m * np.log(p)
                s += (np.log(p)**2) / pm * np.cos(2*np.pi*tau * ln_pm / np.log(T/(2*np.pi)))
                m += 1
                pm *= p
        K[i] = (2 * np.pi / T) * s
    return K

# Try P_max = 100, 1000, 10000
T = zeros.mean()  # characteristic height
```

### Step 5: GUE theoretical
```python
tau_vals = np.linspace(0.01, 2.0, 100)
F_GUE = np.minimum(tau_vals, 1.0)
```

### Step 6: Compare and quantify
- Plot F_zeros, F_GUE, F_primes at P_max = 100, 1000, 10000
- Report: mean absolute deviation between F_zeros and F_GUE
- Report: mean absolute deviation between F_primes and F_GUE
- Does F_primes converge toward F_zeros as P_max increases?
- Report: at what τ values does the agreement break down?

## Part 2: Pair Correlation from Zeros

Also compute the pair correlation R₂ directly (in the spacing domain, not Fourier domain):

```python
# Pair correlation from 2000 zeros
from itertools import combinations

def pair_correlation(unfolded, r_bins):
    """R₂(r) = density of pairs with separation r (normalized)."""
    N = len(unfolded)
    r_max = max(r_bins)

    counts = np.zeros(len(r_bins) - 1)
    for i in range(N):
        diffs = unfolded[i+1:] - unfolded[i]
        diffs = diffs[diffs < r_max]
        hist, _ = np.histogram(diffs, bins=r_bins)
        counts += hist

    # Normalize: divide by N and by bin width
    dr = r_bins[1] - r_bins[0]
    R2 = counts / (N * dr * (N-1) / (max(r_bins)))  # rough normalization
    return R2

r_bins = np.linspace(0, 5, 51)
R2_zeros = pair_correlation(unfolded, r_bins)
r_centers = (r_bins[:-1] + r_bins[1:]) / 2
R2_montgomery = 1 - (np.sin(np.pi * r_centers) / (np.pi * r_centers))**2
```

Report: deviation of R₂_zeros from Montgomery formula. This was 9% in strategy-001 — confirm or update this number.

## Part 3: Kernel Operator Construction (if time permits)

If the two-point formula shows good agreement (F_primes approaches F_GUE), construct the corresponding kernel operator:

The Montgomery pair correlation R₂(x, y) = 1 - (sin(π(x-y))/(π(x-y)))² defines an integral operator:

```
(T f)(x) = ∫₀^L R₂(x, y) f(y) dy
```

Discretize this as a finite N×N matrix:
```python
def kernel_matrix(N, R2_func=None):
    """N×N matrix H_{jk} = R₂(j-k) / N"""
    H = np.zeros((N, N))
    for j in range(N):
        for k in range(N):
            r = abs(j - k)
            if r > 0:
                H[j, k] = 1 - (np.sin(np.pi * r) / (np.pi * r))**2
            else:
                H[j, k] = 1  # R₂(0) = 1 (diagonal)
    return H

H_kernel = kernel_matrix(500)
eigenvalues = np.linalg.eigvalsh(H_kernel)
```

Score this kernel operator against the 10-constraint catalog (at minimum: β, spacing distribution, GUE vs GOE comparison).

**If R₂_zeros deviates from Montgomery, use the NUMERICAL R₂ as the kernel instead of the formula.**

## Key Questions to Answer

1. **Does the prime form factor F_primes converge to F_GUE = min(|τ|, 1)?** Quantitatively — report the convergence as a function of P_max.

2. **Does F_primes agree with F_zeros (the direct computation from zeta zeros)?** This is the key test: do primes encode correlations or just density?

3. **What is R₂ from actual zeros?** Confirm or update the 9% deviation from Montgomery.

4. **If we construct the kernel operator from R₂, what symmetry class does it have?** Score against constraints 1, 3, 4, 5.

5. **One-point vs two-point:** The one-point formula (prime counting) failed spectacularly for zero reconstruction. Does the two-point formula succeed for pair correlation? Why or why not?

## Success Criteria

**Primary success:** F_primes(τ) converges toward F_GUE(τ) as P_max increases, AND F_zeros agrees with F_GUE to within the 9% previously measured. This would mean primes DO encode spectral correlations.

**Secondary success:** The kernel operator H_{jk} = R₂(j-k) scores β > 1.5 against the constraint catalog.

**Interesting failure:** F_primes fails to converge to F_GUE, analogous to the one-point Gibbs failure — this would mean CORRELATIONS also fail to emerge from prime sums, and the operator must be found by different means.

## Output Format

Score the kernel operator (if constructed) against the 10-constraint catalog:
| # | Constraint | Target | Achieved | PASS/PARTIAL/FAIL |
|---|-----------|--------|----------|-------------------|
| 1 | GUE β=2 | β=2.0 | β=? | |
| 3 | Spacing distribution | 4% MAD | ?% | |
...

## Exploration Directory

Your exploration directory is:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-003/`

Write all scripts to `code/` subdirectory. Write REPORT.md incrementally as you complete each part. Write REPORT-SUMMARY.md **last** — this signals you are finished.

**Previous code to check first:**
- `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-005/code/` (crashed explorer's partial work)
