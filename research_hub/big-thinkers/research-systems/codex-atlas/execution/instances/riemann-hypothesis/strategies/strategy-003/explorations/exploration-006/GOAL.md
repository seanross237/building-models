# Exploration 006: K(τ) from Prime Orbit Sums — Does the Diagonal Approximation Predict Δ₃ = 0.155?

## CRITICAL: Confirm Working Directory First

**BEFORE ANYTHING ELSE:** Run `pwd` and `ls`.

Your working directory MUST be:
`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-003/explorations/exploration-006/`

If you see files like `REPORT.md` already present, or if `ls` shows files NOT listed below, you are in the wrong directory. Run `cd` to the correct path above before proceeding.

Expected initial contents: `GOAL.md` (this file) only.

---

## Mission Context

We are investigating the **spectral rigidity gap**: Δ₃_sat(zeta) = 0.155 vs GUE analytic ≈ 0.294 (47% more rigid). This gap has been confirmed by direct computation (E003). The central unanswered question: **does the prime periodic orbit structure explain this gap?**

Berry (1985) derived Δ₃_sat = (1/π²)log(log(T/2π)) using periodic orbit/prime sum theory. At T≈600, this gives ~0.155. The formula predicts the right answer — but does a direct computation of K(τ) from prime orbit sums also give 0.155 when you feed it through the Σ₂ → Δ₃ chain?

This exploration attempts to answer: **Is K_primes(τ) with a hard saturation cap at τ=1 consistent with Δ₃_sat = 0.155?**

---

## Key Parameters (from E003)

```python
T_geo = 1127.1201   # geometric mean height of 2000 zeros
rho_bar = 0.825942  # mean zero density = log(T_geo/(2π))/(2π)
```

Data available at: `../exploration-003/code/data_zeros.npz`

---

## Background: K(τ) from Prime Orbit Sums

### Berry's Diagonal Approximation

```python
# K_primes(τ) = smoothed sum over prime periodic orbits
# τ_pm = m * log(p) / log(T_geo/(2π))  [dimensionless time for orbit (p,m)]
# weight = (log p)²
# Normalize by (2π ρ̄)²

from sympy import primerange
import numpy as np

primes = list(primerange(2, 2000))  # covers 96%+ of prime orbit weight

def compute_K_primes(tau_grid, T_geo, rho_bar, sigma=0.05):
    log_T = np.log(T_geo / (2*np.pi))
    K_density = np.zeros(len(tau_grid))
    for p in primes:
        log_p = np.log(p)
        for m in range(1, 6):
            tau_pm = m * log_p / log_T
            if tau_pm > tau_grid[-1] + 3*sigma:
                break
            weight = log_p**2
            K_density += weight * np.exp(-0.5*((tau_grid - tau_pm)/sigma)**2) \
                         / (sigma * np.sqrt(2*np.pi))
    return K_density / (2*np.pi*rho_bar)**2
```

**CRITICAL normalization:** Divide by `(2π ρ̄)²` — NOT by `(2π ρ̄)` or by raw density.

### Predicting Δ₃ from K(τ)

Once you have K_primes(τ), use the Wiener-Khinchin route to get Δ₃:

```python
# Step 1: K(τ) → Σ₂(L)
# Σ₂(L) = (2/π²) ∫₀^τ_max K(τ)/τ² × sin²(πLτ) dτ

# Step 2: Σ₂(L) → Δ₃(L) via:
# Δ₃(L) = (2/L⁴) ∫₀^L (L³-2L²r+r³) Σ₂(r) dr
```

Test two versions of K(τ):
1. **K_nocap**: K_primes(τ) with no modification (continues past τ=1)
2. **K_cap**: K_primes(τ) for τ≤1, then K(τ)=1 for τ>1 (hard saturation cap)

### Berry's Formula Cross-Check

Berry (1985): Δ₃_sat = (1/π²) × log(log(T/(2π)))

Compute this at T values and compare:
- T=383, 600, 1127 (T_geo), 2245

---

## Tasks (Write to REPORT.md after EACH task — before starting the next)

### Task 0: Confirm Directory + Load Data

1. Run `pwd` and confirm you are in `exploration-006/`. If not, cd there NOW.
2. Run `ls ../exploration-003/code/` to check if `data_zeros.npz` exists.
3. Load zeros: `np.load('../exploration-003/code/data_zeros.npz')`, extract T_geo and rho_bar.
4. If zeros not available, compute via mpmath: `from mpmath import zetazero; t = [float(zetazero(n).imag) for n in range(1, 2001)]`
5. Confirm: T_geo ≈ 1127, rho_bar ≈ 0.826.
6. Save: `np.savez('setup.npz', T_geo=T_geo, rho_bar=rho_bar)`

**Write Task 0 results to REPORT.md NOW. Then proceed.**

### Task 1: Compute K_primes(τ)

Compute K_primes(τ) for τ ∈ [0.01, 3.0] (300 points) with σ=0.05.

Record K_primes vs K_GUE at key τ values:

| τ | K_primes | K_GUE=min(τ,1) | K_primes/K_GUE |
|---|---------|----------------|----------------|
| 0.1 | ? | 0.1 | ? |
| 0.3 | ? | 0.3 | ? |
| 0.5 | ? | 0.5 | ? |
| 0.8 | ? | 0.8 | ? |
| 1.0 | ? | 1.0 | ? |
| 1.5 | ? | 1.0 | ? |
| 2.0 | ? | 1.0 | ? |

Note: Does K_primes exceed 1.0 for τ > 1?

Save: `np.savez('k_primes.npz', tau=tau_grid, K_primes=K_primes)`

**Write Task 1 results to REPORT.md NOW. Then proceed.**

### Task 2: Predict Δ₃ from K_primes

Compute Δ₃(L) for L ∈ [1, 30] using both K_nocap and K_cap:

```python
L_values = np.linspace(2, 30, 57)
delta3_nocap = []
delta3_cap = []

for L in L_values:
    tau = tau_grid[tau_grid > 0.001]  # avoid τ=0 singularity
    K_nocap_vals = K_primes[tau_grid > 0.001]
    K_cap_vals = np.minimum(K_primes[tau_grid > 0.001], 1.0)

    integrand_nocap = K_nocap_vals / tau**2 * np.sin(np.pi*L*tau)**2
    integrand_cap = K_cap_vals / tau**2 * np.sin(np.pi*L*tau)**2

    sigma2_nocap = (2/np.pi**2) * np.trapz(integrand_nocap, tau)
    sigma2_cap = (2/np.pi**2) * np.trapz(integrand_cap, tau)

    delta3_nocap.append(sigma2_nocap / L)  # approximate: Δ₃ ≈ Σ₂/L for saturation
    delta3_cap.append(sigma2_cap / L)
```

Actually use the EXACT Δ₃ formula (verified in E001 and E003):
```
Δ₃(L) = (2/L⁴) ∫₀ᴸ (L³-2L²r+r³) Σ₂(r) dr
```

Record at L = 5, 10, 15, 20, 25, 30.

**Report Δ₃_sat (average over L=20-30) for both no-cap and cap versions.**

Target: Does either version give Δ₃_sat ≈ 0.155?

Save: `np.savez('delta3_primes.npz', L_values=L_values, delta3_nocap=..., delta3_cap=...)`

**Write Task 2 results to REPORT.md NOW. Then proceed.**

### Task 3: Berry Formula Comparison

Compute (1/π²) × log(log(T/(2π))) for T ∈ {383, 600, 1127, 2245} and compare to measured values from E003:

| T | Berry formula | Measured Δ₃_sat |
|---|--------------|----------------|
| 383 | ? | 0.1435 |
| 600 | ? | ~0.155 |
| 1127 (T_geo) | ? | 0.1545 |
| 2245 | ? | 0.1595 |

Does Berry formula track the measured values? What's the percent error at each T?

**Write Task 3 results to REPORT.md NOW. Then proceed.**

### Task 4: Central Verdict

Fill in this comparison table:

| Approach | Δ₃_sat | Matches 0.155? |
|----------|--------|----------------|
| Direct from zeros (E003) | 0.1545 | YES |
| K_primes, no cap | ? | ? |
| K_primes, cap at τ=1 | ? | ? |
| Berry formula at T=1127 | ? | ? |
| GUE analytic | 0.294 | NO |
| C1 matrix (E005) | 0.285 | NO |

**Answer the core question:** Does the prime orbit diagonal approximation predict Δ₃_sat ≈ 0.155, or does it predict GUE-like ~0.294?

**Write Task 4 results to REPORT.md. Then write REPORT-SUMMARY.md.**

---

## Success Criteria

**Success:** K_primes with saturation cap predicts Δ₃_sat within 20% of 0.155 (0.124–0.186). Prime structure explains the gap.

**Partial:** K_primes without cap gives Δ₃ growing unboundedly, but with cap gives 0.155 → saturation mechanism is the key ingredient.

**Failure:** K_primes with cap predicts Δ₃ ≈ 0.294 regardless → prime diagonal approximation cannot explain the gap; off-diagonal is essential.

---

## Key Reference Values

- Δ₃_sat(zeta) = 0.1545 [COMPUTED in E003]
- K_GUE(τ) = min(τ,1) for τ∈[0,2]
- GUE analytic Δ₃_sat = 0.294 [E003]
- 96% of prime orbit weight from p ≤ 1000

## Warnings

- **Write to REPORT.md after EACH task. Do NOT batch.**
- **Save .npz after each computation.**
- **Prime sum computation with 500 primes × 300 τ values = 150,000 evaluations ≈ 2-5 min. Use timeout 15m.**
- **scipy.optimize BROKEN** — use manual fits.
- **CWD CHECK**: If at any point `pwd` shows a directory that is NOT exploration-006, STOP and cd to the correct path.
