# Exploration 008: Validate λ_n^zeta / λ_n^GUE Crossover — Novel Claim Confirmation

## CRITICAL: Confirm Working Directory First

**BEFORE ANYTHING ELSE:** Run `pwd` and `ls`.

Your working directory MUST be:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-008/`

If you are NOT in this exact directory, run:
```bash
cd /Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-008/
```
Then verify with `pwd`. Do not proceed until you confirm you are in `exploration-008/`.

---

## Mission Context

We have identified what appears to be a **novel finding**: Li coefficients λ_n for the Riemann zeta zeros grow SLOWER than λ_n for GUE random matrices for large n (crossover at n≈300, ratio λ_n^zeta/λ_n^GUE ≈ 0.95 at n=500).

This was found in E002 using:
- 2,000 zeta zeros (via mpmath zetazero)
- GUE matrices of dimension N=100, 1,000 realizations

**E007 literature search confirmed: NO prior paper compares λ_n^zeta to λ_n^GUE.** This is a novel cross-community connection between Li's criterion (number theory) and random matrix theory.

**The central question for E008:** Is the ratio λ_n^zeta/λ_n^GUE < 1 for n>300 a **genuine signal**, or an artifact of:
(A) Too few zeros (truncation artifact)
(B) Too small GUE matrix dimension N
(C) Statistical noise in the GUE ensemble

---

## Li Coefficient Definition

```python
# For the Riemann zeta function:
# λ_n(zeta) = Σ_{ρ} [1 - (1 - 1/ρ)^n]
# where ρ runs over nontrivial zeros ρ = 1/2 + i*t_k
#
# For GUE: replace nontrivial zeros with GUE eigenvalues e_k (scaled to unit mean spacing)
# λ_n(GUE) = Σ_k [1 - (1 - 1/z_k)^n]
# where z_k are the GUE "zeros" placed at appropriate positions

# From E002 (VERIFIED):
# lambda_n(zeta) approximation using 2*n_zeros terms:
# lambda_n = sum over zeros t_k:
#   rho = 0.5 + 1j*t_k
#   term = 1 - (1 - 1/rho)**n + 1 - (1 - 1/rho.conjugate())**n  [for each conjugate pair]

from mpmath import mp, zetazero, mpc, power
import numpy as np

mp.dps = 25  # 25 decimal places sufficient

def compute_lambda_zeta(n, zeros_imag):
    """Compute λ_n using zeros with imaginary parts in zeros_imag."""
    total = 0.0
    for t in zeros_imag:
        rho = mpc('0.5', t)
        rho_bar = mpc('0.5', -t)
        term = 2.0 - float((1 - 1/rho)**n + (1 - 1/rho_bar)**n).real
        # Note: for ρ = 1/2 + it, the conjugate pair contributes 2*Re[1-(1-1/ρ)^n]
        total += float(term.real)
    return total
```

---

## Tasks (Write to REPORT.md after EACH task before starting the next)

### Task 0: CWD Check + Load Prior Data

1. Run `pwd` — confirm exploration-008
2. Check if `../exploration-002/code/` exists and contains zero data
3. Load or recompute 2000 zeros: `t_array = [float(zetazero(n).imag) for n in range(1, 2001)]`
4. Save: `np.save('t_zeros_2k.npy', t_array)`
5. Confirm: t_array[0] ≈ 14.135, t_array[1999] ≈ 2515

**Write Task 0 to REPORT.md NOW. Then proceed.**

### Task 1: Recompute λ_n^zeta with 2,000 zeros (baseline replication)

Compute λ_n for n=1, 10, 50, 100, 200, 300, 400, 500 using 2,000 zeros.

**USE THE CORRECT FORMULA** from E002 (above). At 25-digit precision.

Record:
| n | λ_n^zeta (2k zeros) | λ_n^zeta (E002 value) | Match? |
|---|---------------------|----------------------|--------|
| 100 | ? | 59.72 | ? |
| 200 | ? | 288.97 | ? |
| 500 | ? | 881.43 | ? |

If values match E002 within 0.1%, proceed. If not, debug before continuing.

**Write Task 1 to REPORT.md NOW. Then proceed.**

### Task 2: Compute λ_n^zeta with 5,000 zeros

```python
# Get zeros 1..5000 (takes ~25 min — use timeout carefully)
# Option A: Use mpmath directly (slow but exact)
# t_5k = [float(zetazero(n).imag) for n in range(1, 5001)]
# Option B: Use known Odlyzko data if available
# For this exploration, use mpmath with a 30-min timeout

import subprocess
# Save in batches to avoid losing progress:
# Batch 1: zeros 1-1000
# Batch 2: zeros 1001-2000 (already have)
# Batch 3: zeros 2001-3000
# Batch 4: zeros 3001-4000
# Batch 5: zeros 4001-5000
```

Compute λ_n for n = 100, 200, 300, 400, 500, 750, 1000 using 5,000 zeros.

**Expected:** λ_n should be more accurate (less truncation error) with 5,000 vs 2,000 zeros.

Key comparison: does λ_500(zeta, 5k zeros) / λ_500(zeta, 2k zeros) ≈ 1.0? If very different, truncation is important.

**Write Task 2 to REPORT.md NOW. Then proceed.**

### Task 3: Compute λ_n^GUE with N=300 matrices, 500 realizations

```python
# For GUE: compute eigenvalues, "unfold" them, then compute Li coefficients
# The Li coefficient for a matrix spectrum requires defining the "zeros" of the
# characteristic polynomial on the critical line analog

# SIMPLEST VALID APPROACH (from E002):
# Use GUE eigenvalues scaled to unit mean spacing
# Map them to "zeros" using ρ_k = 1/2 + i * x_k  (same as for zeta)
# where x_k are unfolded GUE eigenvalues

def lambda_n_from_eigenvalues(eigenvalues_scaled, n, mp_precision=25):
    """
    eigenvalues_scaled: array of GUE eigenvalues, unfolded to mean spacing 1
    """
    total = 0.0
    for x in eigenvalues_scaled:
        rho = mpc('0.5', float(x))
        rho_bar = mpc('0.5', -float(x))
        term = 2.0 - float(((1 - 1/rho)**n + (1 - 1/rho_bar)**n).real)
        total += term
    return total

# GUE ensemble: N=300, 500 realizations
import numpy as np

N = 300
n_realizations = 500
lambda_n_gue = {n_val: [] for n_val in [100, 200, 300, 400, 500]}

for _ in range(n_realizations):
    # Generate GUE matrix
    A = (np.random.randn(N,N) + 1j*np.random.randn(N,N)) / np.sqrt(2)
    H = (A + A.conj().T) / np.sqrt(2*N)
    evals = np.linalg.eigvalsh(H)
    # Unfold to unit mean spacing
    evals_sorted = np.sort(evals)
    # Simple linear unfolding using Wigner semicircle mean density
    # rho_sc(x) = (2/pi) * sqrt(1 - x^2/4) for x in [-2,2]
    N_vals = N * np.cumsum(np.ones(N)/N)  # CDF approximation
    # Better: use empirical CDF for unfolding
    from scipy.stats import rankdata
    ranks = rankdata(evals_sorted)
    evals_unfolded = ranks / N * N  # scale so mean spacing = 1

    for n_val in [100, 200, 300, 400, 500]:
        lam = lambda_n_from_eigenvalues(evals_unfolded, n_val)
        lambda_n_gue[n_val].append(lam)

# Compute mean and std for each n
gue_stats = {}
for n_val in [100, 200, 300, 400, 500]:
    gue_stats[n_val] = (np.mean(lambda_n_gue[n_val]), np.std(lambda_n_gue[n_val]))
```

**IMPORTANT SCOPE WARNING:** Computing λ_n at n=500 for 300 eigenvalues × 500 matrices at 25-digit precision is SLOW. If this times out, reduce to:
- N=200 matrices, 200 realizations
- n values: 100, 200, 300, 400, 500 only
- 15-digit precision (mp.dps=15)

Check: does GUE λ_500 ≈ 929 (E002 reference value at N=100)?

**Write Task 3 to REPORT.md NOW. Then proceed.**

### Task 4: Ratio Analysis and Verdict

Compute the crossover:

| n | λ_n^zeta (5k zeros) | λ_n^GUE (mean ± std, N=300) | Ratio | Is ratio < 1? | n_sigma below 1 |
|---|---------------------|------------------------------|-------|---------------|----------------|
| 100 | ? | ? ± ? | ? | ? | ? |
| 200 | ? | ? ± ? | ? | ? | ? |
| 300 | ? | ? ± ? | ? | ? | ? |
| 400 | ? | ? ± ? | ? | ? | ? |
| 500 | ? | ? ± ? | ? | ? | ? |

**E002 reference (to compare):** ratio ≈ 0.95 at n=500, crossover at n≈300.

Answer:
1. Is the crossover still at n≈300 with 5k zeros and N=300 GUE?
2. Does the ratio at n=500 stay ≈ 0.95, or change significantly?
3. Is the ratio statistically significant (>3σ below 1)?
4. **Verdict:** Is the λ_n^zeta/λ_n^GUE crossover a real signal (robust to changing zeros/N) or an artifact?

**Write Task 4 to REPORT.md NOW. Then write REPORT-SUMMARY.md.**

---

## Success Criteria

**SUCCESS:** Crossover at n≈300 persists with 5k zeros and N=300 GUE. Ratio at n=500 still ≈ 0.90-0.95 and statistically significant. **Novel claim CONFIRMED.**

**PARTIAL:** Crossover exists but ratio changes significantly (e.g., 0.95 → 0.98) → signal present but weaker than E002 suggested.

**FAILURE:** Ratio ≈ 1.0 at n=500 with 5k zeros or N=300 → E002 result was a truncation/finite-N artifact. **Novel claim refuted.**

---

## Key Reference Values (from E002)

- λ_100^zeta = 59.72, λ_100^GUE = 57.82 ± 0.83 (ratio = 1.03, slightly above 1)
- λ_200^zeta = 288.97, λ_200^GUE = 279.39 ± 2.13 (ratio = 1.03)
- λ_500^zeta = 881.43, λ_500^GUE = 929.10 ± 2.68 (ratio = 0.949)
- Crossover at n ≈ 300 (transition from ratio > 1 to ratio < 1)

## Warnings

- **CWD CHECK**: Verify `pwd` = exploration-008 before ANY other action
- **Write to REPORT.md after EACH task. Do NOT batch.**
- **Save intermediate data after each task** (zeros, GUE eigenvalues, λ_n arrays)
- **scipy.optimize BROKEN** — use manual fits if needed
- **mpmath precision**: Use mp.dps=25 for λ_n computation (lower is inaccurate)
- **Zero computation timeout**: If 5000 zeros takes too long, use 3000 zeros as fallback
- **GUE timeout**: If N=300 × 500 realizations times out, use N=200 × 200 realizations
