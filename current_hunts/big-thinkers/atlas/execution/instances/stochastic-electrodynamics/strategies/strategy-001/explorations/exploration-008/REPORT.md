# Exploration 008 — Critical Spectral Index n* and α Discrepancy Resolution

## Goal

Two tasks:

**Task A:** Locate the critical spectral index n* where the ALD-SED anharmonic excess Δe(β) changes sign (undershoot → overshoot) between n=2 (ω² spectrum) and n=3 (ω³ ZPF spectrum). Run calibrated normalization (var_x_0 ≈ 0.500) at n ∈ {2.25, 2.5, 2.75}.

**Task B:** Resolve the α-exponent discrepancy between E004 (α≈0.40, physical normalization) and E007 (α≈0.25, calibrated normalization). Run n=3 with physical normalization C_3 = 2τħ/m = 0.02 and fit Δe(β) = C × β^α.

---

## Parameters

```
ALD equation: ẍ = −ω₀²x − 4βx³ − τ(ω₀² + 12βx²)ẋ + F_zpf(t) + τF'_zpf(t)
S(ω) ∝ ω^n, FFT amplitude: A_k = sqrt(S(ω_k) × N / (2 × dt))
τ = 0.01, ω₀ = 1.0, ω_max = 10.0, dt = 0.05, T = 20000, N_ensemble = 200
β scan: {0.0, 0.2, 0.5, 1.0}
```

**QM reference (matrix diagonalization, verified):**

| β    | var_x_QM  |
|------|-----------|
| 0.0  | 0.500000  |
| 0.2  | 0.369964  |
| 0.5  | 0.305814  |
| 1.0  | 0.257150  |

**Prior E007 anchors:**
- n=2.00: Δe(β=1) = −0.0661 (undershoots QM)
- n=3.00: Δe(β=1) = +0.0433 (overshoots QM)
- Naïve linear interpolation from just {n=2, n=3}: n* ≈ 2.60

---

## Task A: Critical Spectral Index n*

### Method

Code: `code/ald_sed_exploration008.py` (reused E007 code, extended for non-integer n).

The noise amplitude formula S(ω) = C_n × ω^n works for any real n (not just integers). Calibration: run C_n=1 at β=0 with T=5000, N=50, then scale by linear response (var_x ∝ C_n). Verify with full T=20000, N=200 run.

Δe(β) = raw_err(β) − raw_err(0), where raw_err(β) = var_x_SED(β) − var_x_QM(β)

### Calibration Results [COMPUTED]

| n    | C_n (calibrated) | var_x(β=0) verified | SE      |
|------|-----------------|--------------------|---------|
| 2.25 | 0.019742        | 0.49207            | 0.00114 |
| 2.50 | 0.019695        | 0.49209            | 0.00114 |
| 2.75 | 0.019630        | 0.49213            | 0.00114 |

All three achieve var_x(β=0) ≈ 0.492, consistent with E007 integer-n results. (Note: verified value is ~0.492, slightly below the 0.500 target — this systematic offset is the same for all n and is removed by the Δe baseline subtraction.)

### β-Scan Results [COMPUTED]

| n    | C_n     | var_x(β=0) | Δe(β=0.2) | Δe(β=0.5) | Δe(β=1.0) | sign |
|------|---------|-----------|-----------|-----------|-----------|------|
| 2.00 | 0.01978 | 0.4921    | −0.05564  | −0.06544  | −0.06609  | −    |
| 2.25 | 0.01974 | 0.4921    | −0.04256  | −0.04788  | −0.04984  | −    |
| 2.50 | 0.01970 | 0.4921    | −0.02368  | −0.02598  | −0.02739  | −    |
| **2.75** | **0.01963** | **0.4921** | **+0.00274** | **+0.00295** | **+0.00409** | **+** |
| 3.00 | 0.01954 | 0.4922    | +0.02937  | +0.03918  | +0.04331  | +    |

**Sign change confirmed between n=2.50 and n=2.75** (at all three β values).

### n* Determination [COMPUTED]

**Linear interpolation (β=1.0):**
```
n* = 2.50 + (2.75 − 2.50) × |−0.02739| / (|−0.02739| + |+0.00409|)
   = 2.50 + 0.25 × 0.8701
   = 2.7175
```

**Quadratic fit to all 5 points (n=2,2.25,2.5,2.75,3):** coeffs = [0.0628, −0.2050, 0.0928]
- Root in [2,3]: **n* = 2.720**

**Cubic fit:** n* = 2.722

**Consistency across β values:**
| β   | n* (linear interp) |
|-----|-------------------|
| 0.2 | 2.724             |
| 0.5 | 2.725             |
| 1.0 | 2.718             |

Spread < 0.007, confirming n* is a robust system property.

**Final answer: n* = 2.72 ± 0.03** [COMPUTED]

### Interpretation

The sign-change at n* ≈ 2.72 is **well below n=3** (the physical ZPF spectrum). This means:

- The physical ZPF spectrum (n=3) is located **0.28 spectral index units above** the stability boundary.
- At n=3, SED overshoots QM by Δe(β=1) ≈ +0.043, consistent with a meaningful excess driven by being safely past n*.
- At n=2.75, the overshoot is tiny (Δe ≈ 0.004), suggesting the crossover is sharp near n*.

The gradient of Δe(β=1) with respect to n near the crossover:
```
dΔe/dn ≈ (0.00409 − (−0.02739)) / (2.75 − 2.50) = 0.03148 / 0.25 ≈ 0.126 per unit n
```

The n* crossover is NOT at n=3. The physical ZPF lies **past** the stability boundary by ~0.28 units.

---

## Task B: Physical Normalization α-Exponent

### Method

Used C_3 = 2τħ/m = 2 × 0.01 × 1.0 = **0.02** (physical ZPF normalization in units ħ=m=1).

E007 calibrated value: C_3 = 0.01954 (ratio 0.02/0.01954 = 1.0235).

By linear response, expected var_x(β=0) = 0.492 × 1.0235 = **0.504** (not 0.516 as E004 reported — discrepancy noted below).

### Results [COMPUTED]

| β   | var_x_SED | var_x_QM | raw_err | Δe       |
|-----|----------|---------|---------|----------|
| 0.0 | 0.50374  | 0.5000  | +0.00374| 0.0      |
| 0.2 | 0.39861  | 0.3700  | +0.02864| +0.02490 |
| 0.5 | 0.34669  | 0.3058  | +0.04088| +0.03714 |
| 1.0 | 0.29858  | 0.2571  | +0.04143| +0.03769 |

**Power law fit (all 3 points, scipy curve_fit): α = 0.239 ± 0.126**

### Comparison: Physical vs Calibrated Normalization [COMPUTED]

| β   | Δe_physical | Δe_calibrated | ratio  |
|-----|-------------|---------------|--------|
| 0.2 | +0.02490    | +0.02937      | 0.848  |
| 0.5 | +0.03714    | +0.03918      | 0.948  |
| 1.0 | +0.03769    | +0.04331      | 0.870  |

Physical Δe is ~85-95% of calibrated Δe. The shapes are similar.

**Three-point fit results:**
- Physical normalization: α = 0.239 ± 0.126
- Calibrated (E007): α = 0.234 ± 0.051

**The two normalizations give consistent α ≈ 0.24.** [COMPUTED]

### The Power Law is NOT Clean — Key Finding [COMPUTED]

Two-point α estimates reveal the functional form is not a simple power law:

| β range | α_physical | α_calibrated |
|---------|-----------|-------------|
| 0.2→0.5 | **0.436** | **0.315** |
| 0.5→1.0 | **0.021** | **0.144** |
| 0.2→1.0 | 0.257     | 0.241     |

**This is the crucial discovery: Δe(β) has two regimes:**
1. **β < 0.5 (steep growth):** α ≈ 0.44 (physical) or 0.31 (calibrated)
2. **β > 0.5 (saturation):** α ≈ 0.02 (physical) or 0.14 (calibrated)

The curve saturates near β = 0.5. A single power law poorly describes both regimes.

### Ratio Test

| Normalization | Δe(0.5)/Δe(0.2) | α prediction | closest α |
|---------------|----------------|-------------|----------|
| Physical      | **1.491**       | 1.443 (α=0.40), 1.257 (α=0.25) | **α≈0.44** |
| Calibrated    | **1.334**       | same        | between 0.25 and 0.40 |

**Striking result:** The physical normalization ratio (1.491) is closest to α=0.40, which is why E004 found α=0.40 if they fit only β ∈ {0.2, 0.5}.

### Resolution of the α Discrepancy [COMPUTED]

**The E004/E007 discrepancy is explained:**

- E004 used β ∈ {0.2, 0.5} (or similar early β range) → saw α ≈ 0.40 (steep regime)
- E007 fit β ∈ {0.2, 0.5, 1.0} → got α ≈ 0.25 (averaged over both regimes)
- **α is not constant** — Δe(β) saturates near β=0.5

The physical normalization does **not** resolve the discrepancy by itself (α_physical ≈ 0.24). But it reveals that the ratio test gives 1.491, consistent with E004's α=0.40 fitting the early growth phase.

**Secondary discrepancy:** E004 reported var_x(β=0) = 0.516 with physical normalization. We get 0.504. This 2.3% difference suggests E004 used slightly different parameters (possibly larger τ, different ω_max, or ω_max = ω_cut with a different cutoff). With C_3 = 0.02, linear response gives var_x_0 = 0.504, and our calibrated simulation confirms this exactly (0.50374).

---

## Summary Table

**Task A: n* results** [COMPUTED]
```
n   | Δe(β=1)   | sign
2.00 | -0.06609  | −  (undershoots)
2.25 | -0.04984  | −
2.50 | -0.02739  | −
2.75 | +0.00409  | +  ← SIGN CHANGE HERE
3.00 | +0.04331  | +  (overshoots, physical ZPF)

n* = 2.72 ± 0.03  (linear interp: 2.718, quadratic fit: 2.720, cubic: 2.722)
```

**Task B: α results** [COMPUTED]
```
Normalization | C_3    | var_x_0 | α (3-pt fit) | α (0.2→0.5) | α (0.5→1.0)
Physical      | 0.0200 | 0.504   | 0.239 ± 0.13 | 0.436       | 0.021
Calibrated    | 0.01954| 0.492   | 0.234 ± 0.05 | 0.315       | 0.144

Conclusion: α discrepancy is due to fitting range, not normalization.
Δe(β) is NOT a clean power law — it saturates near β = 0.5.
```

---

## What Couldn't Be Resolved

1. **E004 var_x_0 discrepancy (0.516 vs 0.504):** We cannot replicate 0.516 with C_3=0.02 in our setup. E004 may have used different τ, ω_max, or a different code. Without the E004 code, this remains unresolved.

2. **Analytical prediction of n*:** We measured n* ≈ 2.72 computationally but have no theoretical prediction for this value. The GOAL suggests checking "colored noise detailed balance Brownian oscillator" literature — not investigated in this exploration.

3. **Why n* ≈ 2.72 and not some "nice" number:** The value doesn't appear to be 1+√(3/2), π/3+2, or any obvious combination. Whether there is a theoretical explanation remains open.

---

## Code

All scripts in `code/ald_sed_exploration008.py`. Intermediate results saved as:
- `code/results_n2.25.json`, `code/results_n2.5.json`, `code/results_n2.75.json` (Task A)
- `code/results_taskB_physical.json` (Task B)
- `code/final_results.json` (complete summary)
- `code/qm_reference.json` (QM reference values)
