# Exploration 003: Non-Perturbative K(τ) from Prime Pair Sums

## Mission Context

We are investigating the **spectral rigidity gap** in the Riemann zeta zeros: the spectral statistic Δ₃_sat(zeta) = 0.155 is ~40% smaller than what GUE random matrices produce (Δ₃_sat(GUE, N=500) = 0.23–0.26). Previous strategies built a 10-constraint catalog confirming this gap; no matrix class can close it.

**Why this exploration:** Strategy-003 Exploration-001 showed that the Berry-Keating PERTURBATIVE off-diagonal corrections (R¹_c, R²_c) give only 1.6% gap closure and blow up at T=1682 because the expansion requires ⟨d⟩ >> 1 (T >> 10^{10}). At T=1682, ⟨d⟩ = 0.89, making the 1/⟨d⟩² perturbative expansion INVALID.

The goal of this exploration is to bypass the perturbative expansion entirely: compute K(τ) DIRECTLY from the prime pair correlation sum, no asymptotic approximations. Then propagate through the verified Σ₂ → Δ₃ route.

## Specific Goal

Compute the spectral form factor K(τ) non-perturbatively from prime pair sums and determine whether it predicts Δ₃_sat close to 0.155.

## Working Directory

Your working directory is `explorations/exploration-003/` (relative to the strategy directory). All code, data, and reports go here.

---

## Background Formulas (Use These Exactly)

### K(τ) from Berry (1985) Diagonal Approximation

The simplest non-perturbative prime sum is the diagonal approximation:
```
K_diag(τ) = (1/(2πρ̄)²) × Σ_{p,m} (log p)² × δ(τ - m·log(p)/log(T/2π))
```
In practice, this is computed as a smoothed sum:
```
K_density(τ) = Σ_{p prime, m≥1} (log p)² × gaussian(τ - m·log(p)/log(T/2π), σ)
K_primes(τ) = K_density(τ) / (2πρ̄)²
```
where ρ̄ = log(T/2π) / (2π) is the mean zero density, T is the geometric mean height of the zeros, σ ≈ 0.1 is the smoothing width.

**CRITICAL NORMALIZATION — 3 wrong versions have burned prior explorations:**
- WRONG: K_cosine = Re[Σ exp(2πiτ·t_n)] — can be negative, is NOT K(τ)
- WRONG: K_density / (2πρ̄) — off by a factor of (2πρ̄)
- CORRECT: K_density / (2πρ̄)²  ✓

### Off-Diagonal Enhancement: Hardy-Littlewood Correlation

The full non-perturbative K(τ) includes pair contributions:
```
K(τ) = K_diag(τ) + K_off-diag(τ)
```

The off-diagonal part from Berry-Keating (1999) SIAM Rev 41:236-266, eq 4.18:
```
K(τ) = |τ| + 2|τ| × Re[ Σ_{p≠p'} (log p)(log p') × b(ξ) × exp(2πiτ·ξ) ]
```
where ξ is the frequency variable and b(ξ) = Π_p (1 − (p^{iξ}−1)²/(p−1)²) is the Hardy-Littlewood twin prime constant product.

**Key approach for this exploration:** Instead of expanding b(ξ) perturbatively in 1/⟨d⟩², compute it DIRECTLY as an Euler product:
```python
def b_euler(xi, primes_list):
    """Hardy-Littlewood factor, direct product (no perturbative expansion)"""
    result = 1.0 + 0j
    for p in primes_list:
        factor = 1.0 - (p**(1j*xi) - 1)**2 / (p - 1)**2
        result *= factor
    return result
```

### Pair Correlation → K(τ) Route

An alternative: compute K(τ) from the pair correlation function R₂(r):
```
K(τ) = 1 + ∫_{-∞}^{∞} (R₂(r) - 1) × exp(2πiτr) dr
```
This is the Fourier transform of the pair correlation. K(τ) for τ∈[0,1] is the ramp region; K(τ≥1) should saturate to 1.

You can estimate R₂(r) empirically from the 2000 zeta zeros (already precomputed in prior explorations), compute its Fourier transform, and get K(τ) non-perturbatively.

### Σ₂ → Δ₃ Route (VERIFIED, use this exactly)

Once you have K(τ), compute:

**Step 1: K(τ) → R₂(r)**
```
R₂(r) = ∫₋∞^∞ K(τ) × exp(-2πiτr) dτ   (inverse Fourier of K)
```
Or work directly with R₂(r) from the empirical zero pair correlation.

**Step 2: R₂ → Σ₂**
```
Σ₂(L) = L + 2∫₀ᴸ (L−r)(R₂(r)−1) dr
```

**Step 3: Σ₂ → Δ₃**
```
Δ₃(L) = (2/L⁴) ∫₀ᴸ (L³−2L²r+r³) Σ₂(r) dr
```

**WRONG Δ₃ kernel (documented pitfall — DO NOT USE):**
```
# WRONG: Δ₃ ≠ L/15 - (1/L⁴)∫(L−r)³(2L²+rL−r²)(R₂−1)dr
```

**Alternative Δ₃ (direct from zeros, for verification):**
Dyson-Mehta staircase statistic — analytically:
```python
# yₖ = k-th unfolded zero position, sorted
I0 = n*L - sum(yk for yk in window)
I1 = n*L**2/2 - 0.5*sum(yk**2 for yk in window)
I2 = n**2*L - sum((2*k-1)*yk for k,yk in enumerate(sorted_window, 1))
F_min = I2 - I0**2/L - 12*(I1 - I0*L/2)**2/L**3
delta3 = F_min / L
```

---

## Tasks (Complete in Order)

### Task 0: Setup and Data Loading [SECTION COMPLETE when done]

1. Load the first 2000 zeta zeros (mpmath's `zetazero(n)` for n=1..2000, or reuse cached data from exploration-002 if `code/zeros_cache.pkl` is accessible — check path `../exploration-002/code/zeros_cache.pkl`).
2. Unfold the zeros: x_n = (t_n / (2π)) × log(t_n / (2π)) to get mean spacing = 1.
3. Compute geometric mean height T_geo from {t_n} (use t_n raw values).
4. Compute ρ̄ = log(T_geo / (2π)) / (2π).
5. Save: `np.savez('data_zeros.npz', zeros=t_array, unfolded=x_array, T_geo=T_geo, rho_bar=rho_bar)`

**Write Task 0 results to REPORT.md before proceeding.**

### Task 1: Empirical R₂(r) from Zero Pairs [SECTION COMPLETE when done]

Compute R₂(r) empirically:
```python
# For each pair of unfolded zeros (x_i, x_j), accumulate |x_i - x_j| in bins
r_grid = np.linspace(0, 30, 600)  # dr = 0.05
counts = histogram of |x_i - x_j| for i≠j, i<j
R2_empirical = counts / (N * dr)   # normalize to mean density = 1
```
Verify: R₂(r) → 1 as r → ∞ (sanity check). R₂(0) → 0 (level repulsion). R₂(r ≈ 1) should dip (anti-bunching).

Save: `np.savez('r2_empirical.npz', r_grid=r_grid, R2=R2_values)`

**Write Task 1 results to REPORT.md before proceeding.**

### Task 2: K(τ) from Empirical R₂ (Non-Perturbative) [SECTION COMPLETE when done]

Compute K(τ) = FT[R₂-1] + 1:
```python
tau_grid = np.linspace(0, 3, 300)
# Use numerical integration: K(τ) = 1 + ∫₀^R_max (R₂(r)-1) × 2cos(2πτr) dr
# (symmetrize: R₂(r) = R₂(-r) for real systems)
K_empirical = 1 + 2 * np.trapz((R2 - 1) * np.cos(2*np.pi*tau_grid[:,None]*r_grid[None,:]), r_grid, axis=1)
```
Also compute K_GUE(τ) = min(τ, 1) for τ∈[0,2] as reference.

Tabulate K_empirical vs K_GUE at τ = 0.1, 0.5, 1.0, 1.5, 2.0.

Save: `np.savez('k_tau_empirical.npz', tau_grid=tau_grid, K_empirical=K_empirical, K_GUE=K_GUE)`

**Write Task 2 results to REPORT.md before proceeding.**

### Task 3: K(τ) from Prime Orbit Sums (Diagonal Approx) [SECTION COMPLETE when done]

Compute K_primes(τ) from prime periodic orbits:
```python
from sympy import primerange
primes = list(primerange(2, 1500))  # primes up to 1500 (covers 96% of weight)

tau_grid = np.linspace(0.01, 2.0, 200)
K_density = np.zeros(len(tau_grid))

for p in primes:
    for m in range(1, 5):  # m=1,2,3,4 (higher powers negligible)
        tau_pm = m * np.log(p) / np.log(T_geo / (2*np.pi))
        weight = (np.log(p))**2
        # Gaussian smoothing, σ=0.1
        K_density += weight * np.exp(-0.5*((tau_grid - tau_pm)/0.1)**2) / (0.1 * np.sqrt(2*np.pi))

K_primes = K_density / (2*np.pi*rho_bar)**2
```

Tabulate K_primes vs K_empirical vs K_GUE.

Save: `np.savez('k_tau_primes.npz', tau_grid=tau_grid, K_primes=K_primes)`

**Write Task 3 results to REPORT.md before proceeding.**

### Task 4: Δ₃ from Non-Perturbative K(τ) [SECTION COMPLETE when done]

From K_empirical (Task 2), compute Δ₃:

**Route A (via R₂):** Use the R₂ already computed in Task 1 with the verified Σ₂ → Δ₃ route:
```python
L_values = np.linspace(1, 30, 60)
delta3_empirical = []
for L in L_values:
    # Σ₂(L) = L + 2∫₀ᴸ (L-r)(R₂(r)-1) dr
    mask = r_grid <= L
    sigma2 = L + 2*np.trapz((L - r_grid[mask]) * (R2[mask] - 1), r_grid[mask])
    delta3_empirical.append(sigma2)  # save Σ₂ for next integral

# Δ₃(L) = (2/L⁴) ∫₀ᴸ (L³-2L²r+r³) Σ₂(r) dr
delta3_values = []
for i, L in enumerate(L_values):
    mask = L_values[:i+1] <= L
    r_vals = L_values[:i+1][mask]
    sigma2_vals = np.array(delta3_empirical)[:i+1][mask]
    integrand = (L**3 - 2*L**2*r_vals + r_vals**3) * sigma2_vals
    delta3_values.append((2/L**4) * np.trapz(integrand, r_vals))
```

**Route B (direct from zeros):** Compute Δ₃ directly from unfolded zeros using the Dyson-Mehta staircase method (windowed integral). This is the most reliable ground truth.

Compare Route A vs Route B at L=10, 15, 20, 25.

Target: Δ₃_sat = 0.155 ± 0.008. Report whether K_empirical predicts this value.

Save: `np.savez('delta3_results.npz', L_values=L_values, delta3_routeA=routeA, delta3_routeB=routeB)`

**Write Task 4 results to REPORT.md before proceeding.**

### Task 5: Hardy-Littlewood K(τ) Enhancement [SECTION COMPLETE when done]

Attempt to compute the off-diagonal K enhancement using the b(ξ) Euler product:
```python
def b_euler(xi, primes_list, n_primes=100):
    """Hardy-Littlewood factor as direct Euler product"""
    result = np.ones(len(xi), dtype=complex)
    for p in primes_list[:n_primes]:
        factor = 1.0 - (p**(1j*xi) - 1)**2 / (p - 1)**2
        result *= factor
    return result
```

Compute |b(ξ)|² for ξ ∈ [0, 30] and plot against 1 (the GUE baseline). If |b(ξ)|² deviates from 1 significantly, this contributes to K_off-diag.

Note: This is exploratory — quantify the magnitude of |b(ξ)|² − 1 and whether it's large enough to shift Δ₃ meaningfully.

Save: `np.savez('hardy_littlewood.npz', xi_grid=xi, b_squared=b_sq)`

**Write Task 5 results to REPORT.md before proceeding.**

---

## Success Criteria

**Success:** At least one of the following:
- K_empirical (from R₂ Fourier transform) predicts Δ₃_sat within 10% of 0.155 via the Σ₂ route (i.e., 0.140–0.170)
- The Hardy-Littlewood b(ξ) Euler product shows |b(ξ)|² meaningfully ≠ 1 in a way that explains gap closure
- A clear quantitative explanation of WHERE in K(τ) the super-rigidity information is encoded (e.g., plateau height, ramp slope, transition point)

**Partial success:** K_empirical from zero pair correlation exactly reproduces Δ₃_sat = 0.155 (expected — this is circular), plus clear identification of what K_primes is missing.

**Failure:** K_empirical and K_primes both give Δ₃ ≈ 0.24 (same as GUE), and b(ξ) ≈ 1 everywhere. This would mean the super-rigidity gap is NOT explained by the prime orbit structure.

---

## Key Reference Values

- Δ₃_sat(zeta zeros) = 0.1550 ± 0.0008 (L > 15)
- Δ₃_sat(GUE, N=500 sim) = 0.23–0.26 (NOT the infinite-N theory ~0.566)
- K_GUE(τ) = min(τ,1) for τ ∈ [0,2], then = 1
- K_zeros at τ=0.5: empirically ≈ 0.549, K_primes ≈ 0.453, K_GUE = 0.500
- Berry closed-form: Δ₃_sat = (1/π²)log(log(T/2π)) — gives 0.155 at T=600, 0.174 at T=1682
- T_geo (2000 zeros) ≈ 1127
- GUE Δ₃ at L=20: 0.217 ± 0.002 (not 0.566 — that's infinite-N theory)

## Warnings

- **scipy.optimize is BROKEN** (numpy.Inf removed). Use manual Brody fit: minimize χ² manually with scipy.optimize.minimize(method='Nelder-Mead') OR just use np.polyfit for linear fits.
- **Prime sum timeout**: Loops over 1000+ primes × many τ values can take 10-15 min. Use timeout 30m on the heavy computations.
- **Intermediate saves**: After each Task, save `.npz` results. A session death at Task 4 without saves loses everything.

## Output Required

Write `REPORT.md` incrementally — after EACH section completes, write that section's results before starting the next section.

At the end, write `REPORT-SUMMARY.md` (200–400 words): outcome, key numbers, what was explained, what wasn't, best leads.
