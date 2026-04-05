# Exploration 006 — Two-Point Formula Redo + Complex Dirichlet Characters

## Mission Context

We are investigating the Riemann Hypothesis through random matrix theory. Two open questions from previous explorations:

**Open Question 1 (from strategy-001, exploration-005 crashed):**
Does the two-point formula — Montgomery's prime pair sum — successfully reproduce the spectral form factor of zeta zeros? This is the critical question: do PRIMES determine spectral CORRELATIONS (not just spectral DENSITY)?

**Open Question 2 (from strategy-002, exploration-001):**
Can a Dirichlet character construction reach GUE statistics? Exploration-001's C2 construction failed because even Dirichlet characters mod 4 and 8 have χ(-1) = -1, causing antisymmetric cancellation → zero matrix. Complex characters with χ(-1) ≠ ±1 avoid this.

## Your Task

### Part A: Two-Point Formula — Definitive Computation

#### What to compute

1. The spectral form factor from actual zeta zeros: K_zeros(τ)
2. The spectral form factor from the prime sum formula (Berry's normalization): K_primes(τ)
3. The GUE theoretical form factor: K_GUE(τ) = min(|τ|, 1)

Compare all three and answer: **Do primes determine spectral correlations?**

#### The spectral form factor

For N unfolded zero positions x₁, ..., x_N:

K_zeros(τ) = (1/N) × |Σ_{n=1}^N exp(2πi τ x_n)|²

where x_n are unfolded: x_n = (t_n / 2π) × log(t_n / (2πe)) and then normalized to mean spacing 1.

Use N = 2000 zeros. Zeros are saved at:
`/Users/seanross/.../strategies/strategy-002/explorations/exploration-003/code/zeta_zeros_2000.npy`

If not available, compute with mpmath (~6 minutes).

This form factor should match min(τ, 1) to within 1-4% (confirmed by strategy-001).

#### The prime form factor (Berry's formula)

Berry (1985) showed that the form factor of the Riemann zeros is controlled by prime periodic orbits. The correct formula is:

For 0 < τ < 1 (the "ramp" region):

K_primes(τ) = (2/Σ) × Σ_{p^m : p^m ≤ T} (log p)² / p^m × cos(2πτ × m log p / log(T/2π))

where:
- T is the characteristic height of the zeros (T = geometric mean of {t_n})
- Σ = Σ_{p^m ≤ T} (log p)² / p^m (normalization)
- The sum is over prime powers p^m with p^m ≤ T

**CRITICAL:** The normalization factor Σ diverges as T → ∞ (logarithmically: Σ ~ log T / (2π)). This is why the previous exploration-003 got K_primes_100 = K_primes_1000 = K_primes_10000 — probably the normalization was wrong.

**Check:** For a fixed T and varying P_max, K_primes should converge as P_max increases toward T. At P_max = T, convergence is expected. The sum contribution diminishes for large p because (log p)²/p → 0.

**Alternative (simpler) formula:** For the diagonal approximation:

K_diag(τ) = (2π/T) × Σ_{p ≤ T} (log p)² / p × [cos(2πτ log p / log(T/2π))]²

But use: T = geometric mean height of the 2000 zeros ≈ exp(mean(log(t_n))).

**Suggested implementation:**

```python
import sympy
from sympy import primerange
import numpy as np

def form_factor_primes(tau_vals, zeros):
    """Compute prime sum form factor."""
    T = np.exp(np.mean(np.log(zeros)))  # geometric mean height
    log_T_over_2pi = np.log(T / (2 * np.pi))

    # Sum over prime powers p^m up to T
    K = np.zeros(len(tau_vals))
    norm = 0.0

    for p in primerange(2, int(T) + 1):
        pm = p
        m = 1
        while pm <= T:
            log_pm = m * np.log(p)
            weight = np.log(p)**2 / pm
            norm += weight
            for i, tau in enumerate(tau_vals):
                K[i] += weight * np.cos(2 * np.pi * tau * log_pm / log_T_over_2pi)
            m += 1
            pm *= p

    if norm > 0:
        K = K / norm  # Normalize so K(0) ≈ 1

    return K

# Test for tau in [0, 2]
tau_vals = np.linspace(0.01, 2.0, 100)
K_p = form_factor_primes(tau_vals, zeros)
# Compare to GUE: K_GUE = min(tau, 1)
K_GUE = np.minimum(tau_vals, 1.0)
```

**Expected:** K_primes should approximately match K_GUE for τ < 1, then plateau at 1 for τ > 1.

#### Diagnosis of previous failure

The previous exploration-003 got K_primes_100 = K_primes_1000 = K_primes_10000. This happened because the sum didn't change when more primes were added. Check:

1. Is the normalization correct? (K should be ~1 at τ=0 if normalized)
2. Does adding more primes (P_max 100 → 1000 → 10000) change the values? If not, the primes past 100 have negligible weight — which is plausible since (log 1000)²/1000 << (log 100)²/100.

Report: what fraction of the total norm Σ comes from primes up to 100, up to 1000, up to 10000?

#### Quantitative comparison

Report these metrics:
- Mean absolute deviation (MAD) between K_zeros and K_GUE in the ramp (τ < 1)
- Mean absolute deviation between K_primes and K_GUE in the ramp
- Mean absolute deviation between K_zeros and K_primes
- Does K_primes show a ramp-to-plateau transition at τ ≈ 1?

#### Answer the central question

At the end, state clearly: **"Do primes determine spectral correlations?"**

Answer options:
1. YES: K_primes ≈ K_zeros (primes determine the two-point statistics)
2. PARTIALLY: K_primes approximates the ramp but deviates beyond τ = 1
3. NO (convergence issue): K_primes doesn't converge to K_GUE/K_zeros even with many primes — correlations are not determined by prime sums alone
4. UNCLEAR: normalization issues prevent a definitive answer — specify what would resolve it

---

### Part B: Complex Dirichlet Character Construction

Build a new arithmetic matrix using **complex Dirichlet characters** that avoid the cancellation failure of exploration-001's C2.

#### Why C2 failed

Exploration-001 tested χ mod 4 (values: χ(1)=1, χ(-1)=-1, χ(2)=0, χ(3)=-1...) and χ mod 8. These are **even** or have χ(-1) = -1. When used as H_{jk} = Λ(j-k) × χ(j-k) with signed differences j-k, the condition χ(-n) = -χ(n) makes the matrix antisymmetric. Hermitianization (H+H†)/2 → all terms cancel → zero matrix.

#### Correct construction using χ mod 5

The Dirichlet character mod 5 with conductor 5:
- χ(1) = 1, χ(2) = i, χ(3) = -i, χ(4) = -1, χ(0) = 0

This is a **complex character** with χ(-1) = χ(4) = -1... hmm, that's still -1.

Try χ₁ mod 5 (the non-principal character with values {1, i, -1, -i, 0}):
Actually for mod 5 group (Z/5Z)*, generator = 2:
- χ(1) = 1
- χ(2) = i
- χ(4) = i² = -1
- χ(3) = i³ = -i
- χ(0) = 0

Note χ(4) = χ(-1 mod 5) = -1. So this still has χ(-1) = -1, making the construction antisymmetric.

**Better approach:** Use χ(j) × χ̄(k) (not χ(j-k)).

```python
def dirichlet_matrix_correct(N, q=5):
    """
    H_{jk} = Λ(|j-k|+1) × χ(j+1) × conj(χ(k+1))
    where χ is a character mod q.
    This is automatically Hermitian: H_{kj} = Λ(|j-k|+1) × χ(k+1) × conj(χ(j+1)) = H_{jk}†
    """
    # Dirichlet character mod 5
    # χ: 1→1, 2→i, 3→-i, 4→-1, 5→0, then repeats
    char_values = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}

    def chi(n):
        return char_values.get(n % q, 0)

    # Precompute Von Mangoldt
    Λ = np.zeros(2*N + 2)
    for pk in primerange(2, 2*N+2):
        pk_m = pk
        while pk_m <= 2*N+1:
            Λ[pk_m] = np.log(pk)
            pk_m *= pk

    # Build matrix H_{jk} = Λ(|j-k|+1) × χ(j+1) × conj(χ(k+1))
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(N):
            H[j, k] = Λ[abs(j-k)+1] * chi(j+1) * np.conj(chi(k+1))

    # This should already be Hermitian, but symmetrize to be safe
    H = (H + H.conj().T) / 2
    return H
```

This construction φ(j,k) = arg(χ(j+1)) - arg(χ(k+1)) = arg(χ(j+1)/χ(k+1)).

Note: The phase φ(j,k) = g(j) - g(k) where g(j) = arg(χ(j+1)). This is FACTORIZABLE! So H = D Λ D† where D = diag(χ(1), χ(2), ..., χ(N)) and Λ is the real Von Mangoldt Hankel matrix. Therefore H is UNITARILY EQUIVALENT to the real matrix Λ. This means β will be the same as for the real Hankel matrix (β = 0.44). This construction won't help.

**Truly complex construction:** Use a phase that depends on both j AND k jointly, not just j-k or g(j)-g(k):

```python
# Approach 1: χ(jk mod p) where the product jk is the argument
def dirichlet_product_matrix(N, q=5):
    """H_{jk} = Λ(|j-k|+1) × χ(jk mod q)"""
    char_values = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}
    # Note: χ(jk) = χ(j)×χ(k) multiplicatively
    # So H_{jk} = Λ(|j-k|+1) × χ(j) × χ(k)  (since χ is completely multiplicative)
    # This has phase arg(χ(j)) + arg(χ(k)) = g(j) + g(k)
    # NOT factorizable as g(j) - g(k), so this COULD break time-reversal

    def chi(n):
        return char_values.get(n % q, 0)

    Λ = # precompute as above

    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(j+1, N):
            H[j, k] = Λ[abs(j-k)+1] * chi((j+1) * (k+1))
            H[k, j] = np.conj(H[j, k])
    for j in range(N):
        H[j, j] = Λ[1]  # diagonal = Λ(1) = 0
    return H
```

The phase φ(j,k) = arg(χ(jk)) = arg(χ(j)) + arg(χ(k)) (multiplicativity). This is NOT of the form g(j) - g(k) but g(j) + g(k). This breaks time-reversal symmetry (T sends H → H* = D* Λ D which is not unitarily equivalent to H unless the character is real).

**Compute β for this construction** and compare to C3b (Gauss sums, β=1.09).

Also try: χ mod 13 (has 12 distinct phases, more phase diversity).

**Report scorecard** for the best Dirichlet construction using the same format as exploration-001.

## Verification Tags

- [COMPUTED]: numerical result from code
- [CHECKED]: cross-checked against published value
- [CONJECTURED]: reasoning-based claim

## Success Criteria

**Part A success:** K_primes converges to something close to K_GUE (within 30%), giving a definitive answer to the two-point formula question.

**Part B success:** Dirichlet character matrix achieves β > 1.0 (better than Hankel baseline of 0.44). β > 1.5 would be excellent.

**Failure:** K_primes diverges or stays flat (normalization issue), and Dirichlet construction gives β < 0.5.

## Exploration Directory

`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-006/`

Write scripts to `code/`, REPORT.md incrementally, REPORT-SUMMARY.md last.

Zeta zeros: `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-003/code/zeta_zeros_2000.npy`
