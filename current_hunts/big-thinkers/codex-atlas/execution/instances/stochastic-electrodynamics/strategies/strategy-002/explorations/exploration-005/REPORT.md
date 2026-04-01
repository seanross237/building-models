# Exploration 005 — SED Tunneling: Verify Γ Formula at 5+ λ Values

**Date:** 2026-03-27
**Explorer:** Math Explorer
**Goal:** Verify the formula Γ_SED/Γ_exact ≈ A × exp(S_WKB − V_barrier/E_zpf) at 5 new λ values
(0.30, 0.20, 0.15, 0.075, 0.05) using ALD equation SED simulations and exact QM diagonalization.

---

## 1. Setup

### Potential and Parameters

Double-well: `V(x) = −½ω₀²x² + ¼λx⁴`, with ω₀ = m = ħ = 1.

Universal facts (from E004):
- Local oscillation frequency at well bottom: ω_local = √2 (independent of λ)
- ZPF energy: E_zpf = ω_local/2 = √2/2 ≈ 0.7071
- Barrier height: V_barrier = 1/(4λ)
- V_barrier/E_zpf = √2/(4λ)

### Code Used

The ALD equation simulations use `code/sed_sim_corrected.py` which applies the UV cutoff `ω ≤ ω_max = 10` to the ZPF noise PSD (matching E001's actual code, not the simplified GOAL.md snippet which accidentally dropped this cutoff). Concretely:

```python
S_F = np.where((omegas > 0) & (omegas <= omega_max),
               2.0 * tau * hbar * omegas**3 / m,
               0.0)
```

Without this cutoff (as in the GOAL.md snippet), Gamma_SED is ~1.5× higher for all λ, shifting A from ~1.1 to ~1.6. Both versions give slope ≈ 1.05 and R² > 0.999 for the linear formula. The omega_max=10 version is used here for consistency with E001.

**Sanity check** (before running new λ values): at λ=0.10 with seed=42, my code gives Γ_SED = 0.00746 vs E001's 0.00790. Difference is ~5%, within E001's reported SEM of 0.00137. ✓

---

## 2. QM Tunneling Rates (All λ)

**Script:** `code/qm_rates_corrected.py`
**Method:** Finite-difference Schrödinger equation (3000-point grid, ±7 units), exact eigenvalues via `scipy.linalg.eigh_tridiagonal`. S_WKB computed over central barrier only (between inner turning points).

`[COMPUTED]` All values verified against E001 (λ=0.25: S_WKB=1.4076 ≈ 1.408 ✓; λ=0.10: S_WKB=6.2894 ≈ 6.290 ✓).

| λ | V_barrier | E₀ | E₁ | Γ_exact | S_WKB | V_b/E_zpf | exponent |
|---|-----------|-----|-----|---------|-------|-----------|----------|
| 0.30 | 0.8333 | −0.3021 | −0.1228 | 8.965×10⁻² | 0.9865 | 1.1785 | −0.1920 |
| 0.20 | 1.2500 | −0.6327 | −0.5765 | 2.811×10⁻² | 2.1059 | 1.7678 | +0.3381 |
| 0.15 | 1.6667 | −1.0110 | −0.9960 | 7.468×10⁻³ | 3.4170 | 2.3570 | +1.0600 |
| 0.075 | 3.3333 | −2.6462 | −2.6462 | 2.206×10⁻⁵ | 9.2679 | 4.7140 | +4.5539 |
| 0.05 | 5.0000 | −4.3059 | −4.3059 | 5.194×10⁻⁸ | 15.3328 | 7.0711 | +8.2617 |

All are in the tunneling regime (E₀ < 0 = V(0) = barrier top). The splitting E₁−E₀ is extremely small for deep barriers (λ=0.05: splitting ~ 10⁻⁷ ħω₀).

---

## 3. SED Simulations

**Script:** `code/sed_sim_corrected.py`
**ALD equation:** ẍ = −V'(x)/m − τ·V''(x)·ẋ + F_zpf + τ·Ḟ_zpf
**Parameters:** τ=0.001, ω_max=10, dt=0.05
**Crossing detection:** sign changes of x(t) after 1000 time units burn-in

### 3.1 λ = 0.30 `[COMPUTED]`

V_barrier = 0.833, x_min = ±1.826, ω_local = √2

**Params:** N=200,000, T=10,000, T_measure=9,000, N_traj=100, seed=456

| Quantity | Value |
|----------|-------|
| Γ_SED | 0.07484 ± 0.00309 |
| Γ_exact | 0.08965 |
| **Γ_SED/Γ_exact** | **0.835** |
| ln(ratio) | −0.181 |
| exponent (S_WKB − V_b/E_zpf) | −0.192 |
| Implied A | 1.012 |
| Zero-crossing trajectories | 0/100 |
| Mean crossings/traj | 673.6 |

**Observation:** All 100 trajectories cross the barrier, mean 674 crossings in T=9000 units. The SED rate is 17% **below** Γ_exact — the SED mechanism slightly underestimates quantum tunneling for this near-threshold barrier.

### 3.2 λ = 0.20 `[COMPUTED]`

V_barrier = 1.25, x_min = ±2.236

**Params:** N=200,000, N_traj=100, seed=457

| Quantity | Value |
|----------|-------|
| Γ_SED | 0.04123 ± 0.00226 |
| Γ_exact | 0.02811 |
| **Γ_SED/Γ_exact** | **1.467** |
| ln(ratio) | 0.383 |
| exponent | 0.338 |
| Implied A | 1.046 |
| Zero-crossing trajectories | 0/100 |
| Mean crossings/traj | 371.1 |

**Observation:** All 100 trajectories active. SED now overestimates QM by 47%.

### 3.3 λ = 0.15 `[COMPUTED]`

V_barrier = 1.667, x_min = ±2.582

**Params:** N=200,000, N_traj=100, seed=458

| Quantity | Value |
|----------|-------|
| Γ_SED | 0.02576 ± 0.00234 |
| Γ_exact | 7.468×10⁻³ |
| **Γ_SED/Γ_exact** | **3.449** |
| ln(ratio) | 1.238 |
| exponent | 1.060 |
| Implied A | 1.195 |
| Zero-crossing trajectories | 4/100 |
| Mean crossings/traj | 231.9 |

**Observation:** 4 trajectories get stuck for the full measurement window. SED overestimates by 3.4×.

### 3.4 λ = 0.075 `[COMPUTED]`

V_barrier = 3.333, x_min = ±3.651 (deep barrier)

**Params:** N=200,000, N_traj=200 (doubled for deeper barrier), seed=459

| Quantity | Value |
|----------|-------|
| Γ_SED | 2.848×10⁻³ ± 4.1×10⁻⁴ |
| Γ_exact | 2.206×10⁻⁵ |
| **Γ_SED/Γ_exact** | **129.1** |
| ln(ratio) | 4.861 |
| exponent | 4.554 |
| Implied A | 1.359 |
| Zero-crossing trajectories | 109/200 |
| Mean crossings/traj | 25.6 |

**Observation:** 109/200 (55%) trajectories make zero crossings in T=9000. The distribution is highly non-uniform — a few trajectories make many crossings while the majority make none. This is the "burst" regime (rare ZPF fluctuations push the particle over the barrier, followed by rapid multiple crossings before damping quenches it). SED overestimates by 129×.

### 3.5 λ = 0.05 `[COMPUTED]`

V_barrier = 5.000, x_min = ±4.472 (very deep barrier)

**Params:** N=500,000, T=25,000, T_measure=24,000, N_traj=200, seed=460

| Quantity | Value |
|----------|-------|
| Γ_SED | 3.253×10⁻⁴ ± 7.9×10⁻⁵ |
| Γ_exact | 5.194×10⁻⁸ |
| **Γ_SED/Γ_exact** | **6263** |
| ln(ratio) | 8.742 |
| exponent | 8.262 |
| Implied A | 1.617 |
| Zero-crossing trajectories | 159/200 |
| Mean crossings/traj | 7.3 |

**Observation:** 159/200 (80%) trajectories make zero crossings even in T=24,000. SED overestimates QM by 6263×. The crossing events are extremely rare and highly non-uniform (max crossings = 232 for one trajectory vs 0 for the majority). Despite these statistics, the signal is measurable and sits on the predicted trend line.

---

## 4. Formula Verification

### 4.1 Complete Data Table

Combining E001 (2 points) + E005 (5 new points):

| λ | src | exponent | Γ_SED | Γ_exact | ratio | ln(ratio) |
|---|-----|----------|-------|---------|-------|-----------|
| 0.30 | E005 | −0.192 | 7.484×10⁻² | 8.965×10⁻² | 0.835 | −0.181 |
| 0.25 | E001 | −0.007 | 6.630×10⁻² | 5.780×10⁻² | 1.147 | 0.137 |
| 0.20 | E005 | +0.338 | 4.123×10⁻² | 2.811×10⁻² | 1.467 | 0.383 |
| 0.15 | E005 | +1.060 | 2.576×10⁻² | 7.468×10⁻³ | 3.449 | 1.238 |
| 0.10 | E001 | +2.754 | 7.900×10⁻³ | 4.279×10⁻⁴ | 18.46 | 2.916 |
| 0.075 | E005 | +4.554 | 2.848×10⁻³ | 2.206×10⁻⁵ | 129.1 | 4.861 |
| 0.05 | E005 | +8.262 | 3.253×10⁻⁴ | 5.194×10⁻⁸ | 6263 | 8.742 |

The ratio spans 4 decades (0.84 to 6263) and the exponent spans 8.5 units (−0.19 to +8.26).

### 4.2 Linear Fit Results

`[COMPUTED]` — code: `code/final_analysis.py`

**Fit: ln(Γ_SED/Γ_exact) = intercept + slope × (S_WKB − V_b/E_zpf)**

| Dataset | slope | ±se | intercept | A=exp(int) | R² | RMSE |
|---------|-------|-----|-----------|------------|-----|------|
| All 7 points | 1.0491 | 0.0072 | 0.0720 | 1.075 | 0.99977 | 0.046 |
| E005 only (5 new) | 1.0531 | 0.0066 | 0.0556 | 1.057 | 0.99988 | 0.036 |

The maximum residual across all 7 points is 0.072 in ln-space, corresponding to a factor of e^0.072 = 1.075 in ratio space. All predictions match measurements to within 8%.

### 4.3 Predicted vs Measured Ratios

Using the best-fit formula (slope=1.049, A=1.075):

| λ | ratio_measured | ratio_predicted | factor off |
|---|---------------|-----------------|------------|
| 0.25 | 1.147 | 1.067 | 1.07× |
| 0.10 | 18.46 | 19.32 | 0.96× |
| 0.30 | 0.835 | 0.879 | 0.95× |
| 0.20 | 1.467 | 1.532 | 0.96× |
| 0.15 | 3.449 | 3.268 | 1.06× |
| 0.075 | 129.1 | 127.7 | 1.01× |
| 0.05 | 6263 | 6244 | 1.00× |

**All predictions accurate to within 7%.** `[COMPUTED]`

### 4.4 Verdict on the Formula

`[COMPUTED]`

**Is ln(Γ_SED/Γ_exact) linear in (S_WKB − V_b/E_zpf)?**
→ **YES.** R² = 0.99977 across 4 decades in ratio.

**Is the slope ≈ 1?**
→ **YES, approximately.** Slope = 1.049 ± 0.007. Statistically significantly > 1 (t=6.82, df=5, p < 0.002), but physically close: a 4.9% deviation.

**Is A universal at ≈ 1.15?**
→ **APPROXIMATELY.** With slope=1.05, the best-fit A = 1.075 (close to 1.15). The implied A (from slope=1 assumption) grows from 1.01 to 1.62 as λ decreases. This growth is largely explained by the slope not being exactly 1: with slope=1.05 and exponent range 8.5, the apparent variation in A spans exp(0.05 × 8.5) = 1.5×, matching observations.

**Refined formula:**
```
ln(Γ_SED/Γ_exact) = 0.072 + 1.049 × (S_WKB − √2/(4λ))
```
Or equivalently: `Γ_SED/Γ_exact ≈ 1.075 × exp(1.049 × (S_WKB − √2/(4λ)))`

This works to within 7% across λ ∈ [0.05, 0.30] and ratio ∈ [0.84, 6263].

---

## 5. When Does the Formula Break Down?

**Answer:** The SED rate is measurable at all 5 tested λ values, including λ=0.05 (V_barrier=5, Γ_exact=5×10⁻⁸). `[COMPUTED]`

**Practical limit of SED measurability:**
- λ=0.075: 55% zero-crossing trajectories, need N_traj=200
- λ=0.05: 80% zero-crossing trajectories, need N=500,000 + N_traj=200
- λ < 0.05 would likely need N>1,000,000 or N_traj>500 to see even a few crossings

**Formula accuracy limit:**
The formula never catastrophically breaks. The slope remains ~1.05 even at the deepest barrier tested. The formula is not observed to break down within the tested range. `[COMPUTED]`

**Physical interpretation of why the formula holds:**
- Γ_SED ~ Γ₀ × exp(−V_barrier/E_zpf): classical Boltzmann factor with ZPF energy scale
- Γ_exact ~ Γ₀ × exp(−S_WKB): quantum WKB suppression
- The ratio Γ_SED/Γ_exact ~ exp(S_WKB − V_barrier/E_zpf) follows because both rates share the same attempt frequency Γ₀ (≈ ω_local/2π for motion confined to one well)
- The slope being 1.05 rather than exactly 1 suggests a small correction to either the classical Boltzmann approximation or the WKB formula

---

## 6. Code Discrepancy vs GOAL.md

`[COMPUTED]`

**Important technical finding:** The GOAL.md code snippet includes `omega_max=10.0` as a parameter but does NOT apply it in the PSD formula body. The actual E001 code (double_well_lam010.py) correctly applies:
```python
S_F = np.where((omegas > 0) & (omegas <= omega_max), 2*tau*hbar*omegas**3/m, 0.0)
```

Without the cutoff (GOAL.md as-written): Γ_SED is ~1.5× higher at λ=0.10, shifting A to ~1.6 and intercept to ~0.35.

With the cutoff (E001-style): A ~ 1.07, intercept = 0.072, consistent with E001's reported A ~ 1.15.

Both versions give slope ≈ 1.05 and R² > 0.999. The cutoff affects the absolute scale (A) but not the exponent relationship (slope).

---

## 7. Prior Art Search

`[CONJECTURED]` — Based on prior survey in E001.

The papers identified in E001 (Faria et al. 2005; Schafaschek et al. 2025; Drummond 1989) do not derive or test the specific formula Γ_SED/Γ_exact = A × exp(S_WKB − V_b/E_zpf). The exponential relationship spanning multiple decades is new to this exploration series.

---

## 8. Overall Conclusions

`[COMPUTED]` — All rates computed from reproducible code in `code/`.

**Primary finding:** The formula
```
ln(Γ_SED/Γ_exact) = 0.072 + 1.049 × (S_WKB − V_barrier/E_zpf)
```
is verified across 7 data points spanning λ ∈ [0.05, 0.30], with R² = 0.9998 and maximum prediction error of 7%.

**Slope ≈ 1 confirmed:** [COMPUTED] Best-fit slope = 1.049 ± 0.007.

**Universal prefactor A:** [COMPUTED] Best-fit A = 1.075. Under the exact slope=1 assumption, A ranges from 1.01 to 1.62, with systematic growth for deeper barriers.

**SED measurability:** [COMPUTED] SED crossing rates are measurable down to λ=0.05 (V_barrier=5, Γ_SED = 3.3×10⁻⁴ vs Γ_exact = 5.2×10⁻⁸). The formula does not break down within the tested range.

**Verification scorecard:**
- [VERIFIED]: 0 (no Lean formalization)
- [COMPUTED]: 7 SED rates, 5 QM rates, 1 linear fit — all reproducible
- [CHECKED]: QM rates cross-checked against E001
- [CONJECTURED]: Prior art novelty claim
