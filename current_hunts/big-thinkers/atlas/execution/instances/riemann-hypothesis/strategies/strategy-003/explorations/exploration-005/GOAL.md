# Exploration 005: K(τ) from Prime Orbit Sums → Does It Predict Δ₃_sat = 0.155?

## Mission Context

We are investigating the spectral rigidity gap: Δ₃_sat(zeta) = 0.155 vs GUE analytic prediction 0.294 (~47% more rigid). The gap has been confirmed by direct computation (E003). The central UNSOLVED question is: **what explains this gap?**

Berry (1985) derived the formula Δ₃_sat = (1/π²) log(log(T/2π)) using the prime orbit structure of the Riemann zeros. At T≈600, this gives 0.155 — matching perfectly. The formula comes from the periodic orbit/prime sum theory.

**E003 confirmed 0.155 from zeros but SKIPPED the prime orbit computation (Tasks 3 and 5).** This exploration does exactly those tasks: compute K(τ) from prime orbit sums and determine whether the prime structure predicts Δ₃_sat = 0.155.

## Core Question

When you compute K(τ) from prime periodic orbits (not from zero pairs), does the resulting Δ₃ prediction match 0.155 or 0.294?

- If K_primes → Δ₃ ≈ 0.155: **prime orbit structure EXPLAINS the gap**
- If K_primes → Δ₃ ≈ 0.294 (same as GUE): **off-diagonal corrections are essential (needed beyond diagonal approx)**
- If K_primes → Δ₃ somewhere between: **partial explanation, off-diagonal adds the rest**

## Working Directory

Your working directory is `explorations/exploration-005/` (relative to the strategy directory). All code, data, and reports go here.

---

## Background

### K(τ) — Three Components

1. **K_GUE(τ) = min(τ, 1)** for τ ∈ [0,2] — pure GUE (no primes)
2. **K_diag(τ)** — diagonal prime approximation (Berry 1985): sums over prime periodic orbits p^m
3. **K_empirical(τ)** — Fourier transform of empirical R₂(r) from actual zeros (computed in E003)

### K(τ) from Prime Orbit Sums (Berry Diagonal Approximation)

The spectral form factor from periodic orbit theory (diagonal approximation):

```python
# K_diag(τ) computation — key formula
# τ in [0, τ_max], σ = smoothing width

from sympy import primerange
import numpy as np

primes = list(primerange(2, 2000))  # primes up to 2000

def compute_K_primes(tau_grid, T_geo, rho_bar, sigma=0.05):
    """
    Berry diagonal approximation for K(τ).
    τ_pm = m * log(p) / log(T_geo/(2π)) is the dimensionless time for orbit (p,m)
    Weight = (log p)² / (2π ρ̄)²
    """
    K_density = np.zeros(len(tau_grid))
    for p in primes:
        for m in range(1, 6):  # m=1..5 (higher powers negligible)
            tau_pm = m * np.log(p) / np.log(T_geo / (2*np.pi))
            if tau_pm > tau_grid[-1] + 5*sigma:
                break
            weight = (np.log(p))**2
            # Gaussian smoothing
            K_density += weight * np.exp(-0.5*((tau_grid - tau_pm)/sigma)**2) / (sigma * np.sqrt(2*np.pi))

    K_primes = K_density / (2*np.pi*rho_bar)**2
    return K_primes
```

**CRITICAL normalization (3 wrong versions burned prior explorations):**
- WRONG: K_cosine = Re[Z(τ)] — can be negative
- WRONG: K_density / (2πρ̄) — off by factor of 2πρ̄
- **CORRECT: K_density / (2πρ̄)²** ✓

### Parameters from E003 (reuse these)

```python
T_geo = 1127.1201   # geometric mean height of 2000 zeros
rho_bar = 0.825942  # mean zero density = log(T_geo/(2π))/(2π)
```

Or reload zeros from `../exploration-003/code/` (zeros_cache.pkl or data_zeros.npz).

### K(τ) Saturation

The diagonal approximation gives K_primes(τ) that keeps growing past τ=1 (no saturation mechanism). Two options:
1. **Hard cap**: Set K(τ) = 1 for τ > 1 (theoretical GUE saturation)
2. **No cap**: Let K_primes grow past τ=1 (diagonal only)

Test both and compare the resulting Δ₃ predictions.

### Σ₂ → Δ₃ Route (VERIFIED — use this, not the integral chain)

**IMPORTANT: The R₂ → Σ₂ → Δ₃ integral chain fails with N=2000 zeros (43% overestimate — E003 finding). Use the DIRECT sliding-window method for final Δ₃ verification from zeros.**

For the PRIME ORBIT prediction route, you can use the K(τ) → R₂ → Δ₃ chain because K_primes is smooth (no noise):

1. K_primes(τ) → R₂_predicted(r) via inverse Fourier transform
2. Σ₂(L) = L + 2∫₀ᴸ (L−r)(R₂_predicted(r)−1) dr
3. Δ₃(L) = (2/L⁴) ∫₀ᴸ (L³−2L²r+r³) Σ₂(r) dr

**WRONG Δ₃ kernel (documented pitfall):** DO NOT USE `(L-r)³(2L²+rL-r²)` kernel.

Alternatively, use the Wiener-Khinchin route:
```
Σ₂(L) = (2/π²) ∫₀^∞ K(τ)/τ² × sin²(πLτ) dτ
```

---

## Tasks (Complete in Order — Write to REPORT.md AFTER EACH TASK)

### Task 1: Setup — Load Zeros and Parameters [Write to REPORT.md immediately after]

1. Load 2000 zeta zeros from `../exploration-003/code/data_zeros.npz` (or recompute using mpmath if missing). Get `t_array` (raw heights), `x_array` (unfolded), `T_geo`, `rho_bar`.
2. Confirm: T_geo ≈ 1127, rho_bar ≈ 0.826, mean spacing ≈ 1.0.
3. Save as `setup.npz`.

**Write results to REPORT.md now. Then proceed.**

### Task 2: K(τ) from Prime Orbits [Write to REPORT.md immediately after]

Compute K_primes(τ) for τ ∈ [0.01, 3.0] (300 points) using primes up to 2000.

Use **two smoothing widths**: σ=0.05 and σ=0.10. The narrower σ reveals individual orbit peaks; wider σ gives the smooth envelope.

Record at key τ values:

| τ | K_primes(σ=0.05) | K_primes(σ=0.10) | K_GUE |
|---|-----------------|-----------------|-------|
| 0.10 | ? | ? | 0.10 |
| 0.25 | ? | ? | 0.25 |
| 0.50 | ? | ? | 0.50 |
| 0.75 | ? | ? | 0.75 |
| 1.00 | ? | ? | 1.00 |
| 1.50 | ? | ? | 1.00 |
| 2.00 | ? | ? | 1.00 |

Also record: **Does K_primes exceed 1.0 for τ > 1?** (Yes means no natural saturation in diagonal approx.)

Save: `k_primes.npz`

**Write results to REPORT.md now. Then proceed.**

### Task 3: Predicted Δ₃ from K_primes [Write to REPORT.md immediately after]

**Compute Δ₃ predicted by prime orbit K(τ) via the Wiener-Khinchin route:**

```python
L_values = np.linspace(1, 30, 60)
delta3_primes_nocap = []
delta3_primes_cap = []

for L in L_values:
    # Σ₂(L) = (2/π²) ∫₀^τmax K(τ)/τ² sin²(πLτ) dτ
    tau = tau_grid
    K_nocap = K_primes  # no saturation cap
    K_cap = np.minimum(K_primes, 1.0)  # hard cap at τ>1

    integrand_nocap = K_nocap / tau**2 * np.sin(np.pi*L*tau)**2
    integrand_cap = K_cap / tau**2 * np.sin(np.pi*L*tau)**2

    sigma2_nocap = (2/np.pi**2) * np.trapz(integrand_nocap, tau)
    sigma2_cap = (2/np.pi**2) * np.trapz(integrand_cap, tau)

    # Δ₃ from Σ₂:
    # For simplicity, use Σ₂ directly: Δ₃ ≈ Σ₂(L)/(L^2) × scaling_factor
    # Better: compute Δ₃ from Σ₂ using the double integral
    delta3_primes_nocap.append(sigma2_nocap)  # placeholder
    ...
```

Actually use the full route:
1. From K_primes, compute R₂_predicted via IFT: `R2_pred(r) = ∫ K(τ) exp(-2πiτr) dτ`
2. Then Σ₂ → Δ₃ as in E003 Task 4 Method A (but now with smooth K_primes, no noise)

Report:
- Δ₃_sat(primes, no cap) at L=20: ?
- Δ₃_sat(primes, with cap) at L=20: ?
- Compare to: Δ₃_sat(zeros) = 0.1545, Δ₃_sat(GUE analytic) = 0.294

Save: `delta3_primes.npz`

**Write results to REPORT.md now. Then proceed.**

### Task 4: Berry's Formula Check [Write to REPORT.md immediately after]

Berry (1985) gives Δ₃_sat = (1/π²) log(log(T/2π)) from prime orbit theory.

Compute this at multiple T values and compare to the height-resolved measurements:
- T=383 (bin 1 from S001): Berry predicts ?, measured 0.1435
- T=600: Berry predicts ?, measured ≈0.155
- T=1127 (T_geo): Berry predicts ?, measured 0.1545
- T=2245 (bin 4): Berry predicts ?, measured 0.1595

Also compute: for what T does Berry formula predict EXACTLY 0.155?

**Write results to REPORT.md now. Then proceed.**

### Task 5: Comparison Summary [Write to REPORT.md immediately after]

Fill in this comparison table:

| Method | Δ₃_sat predicted | Matches 0.155? |
|--------|-----------------|----------------|
| K_primes diagonal (no cap) | ? | ? |
| K_primes diagonal (with cap) | ? | ? |
| K_empirical (E003, from zeros) | 0.1545 | YES |
| GUE analytic | 0.294 | NO |
| Berry formula at T=T_geo | ? | ? |

Answer the central question: **Does the prime orbit diagonal approximation explain the Δ₃ gap, or is an off-diagonal correction essential?**

**Write results to REPORT.md now. Then write REPORT-SUMMARY.md.**

---

## Success Criteria

**Success:** K_primes with saturation cap predicts Δ₃_sat within 20% of 0.155 (i.e., 0.124–0.186). This would mean the diagonal approximation captures most of the gap.

**Partial success:** K_primes without cap gives Δ₃ growing without bound (confirming saturation is needed), but K_primes up to τ=1 contains the signal that, when saturated, predicts ~0.155.

**Failure:** K_primes (with or without cap) predicts Δ₃ ≈ 0.294 regardless — the prime diagonal approximation gives GUE-like rigidity and cannot explain the gap.

---

## Key Reference Values

- Δ₃_sat(zeta zeros) = 0.1545 (direct, E003)
- GUE analytic = 0.294
- Berry formula at T=600: (1/π²)log(log(600/2π)) = 0.155
- Berry formula at T=1127: (1/π²)log(log(1127/2π)) = ?
- K_primes at τ=0.5: expected ~0.45 (from S002 explorations — K_primes underestimates at low τ)
- 96.1% of prime orbit weight from primes p ≤ 1000
- σ=0.05 for tight smoothing, σ=0.10 for envelope

## Warnings

- **Write to REPORT.md after EACH task. Do not batch at the end.**
- **Save .npz after each computation block.**
- **DO NOT rerun K(τ) computation with different parameters — too slow. Run once with σ=0.05 and σ=0.10, save both, use saved data.**
- scipy.optimize is BROKEN (numpy.Inf removed). Use manual fits if needed.
- Prime sum loops: use `timeout 20m` for the K_primes computation.

## Output Required

Write `REPORT.md` incrementally after EACH task. At the end, write `REPORT-SUMMARY.md` (150-300 words): the central verdict (does prime diagonal explain the gap?), key numbers, best leads for E006+.
