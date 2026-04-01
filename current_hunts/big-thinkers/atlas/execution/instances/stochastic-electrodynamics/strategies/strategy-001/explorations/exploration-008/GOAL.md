# Exploration 008 — Critical Spectral Index n* and α Discrepancy Resolution

## Mission Context

You are continuing the Stochastic Electrodynamics (SED) mission. Prior explorations established:

**E004 (ALD-SED anharmonic oscillator):**
- Physical SED (ZPF spectral density S_F = 2τħω³/m) with Landau-Lifshitz ALD damping
- At β=0: var_x ≈ 0.516 (baseline, slightly above QM 0.500)
- Baseline-corrected excess Δe(β) ≈ 0.030×β^0.40 (E004 fit, physical normalization)
- At β=1: Δe ≈ 0.030 (positive, SED overshoots QM)

**E007 (spectral noise comparison):**
- Ran ALD-SED with 4 noise spectra S(ω) ∝ ω^n for n ∈ {0,1,2,3}
- Normalization: calibrated so var_x(β=0)=0.500 for all n
- **Key finding: Only n=3 overshoots QM; n=0,1,2 all undershoot.**

| n | Δe at β=0.2 | Δe at β=1.0 | α  |
|---|------------|------------|-----|
| 3 | +0.029     | +0.043     | 0.25 |
| 2 | −0.056     | −0.066     | 0.11 |
| 1 | −0.102     | −0.113     | 0.06 |
| 0 | −0.135     | −0.138     | 0.02 |

**Two open questions this exploration answers:**

1. **Where is n*?** The sign of Δe flips between n=2 (undershoot) and n=3 (overshoot). By linear interpolation at β=1: n* ≈ 2 + 0.066/(0.066+0.043) = 2.61. But this is just linear interpolation. The actual n* needs to be measured.

2. **What is the true α for physical SED?** E004 found α≈0.40 (physical normalization, var_x_0=0.516). E007 found α≈0.25 (calibrated normalization, var_x_0=0.500). The discrepancy is due to different noise amplitudes. The physical SED α is what matters scientifically.

---

## Your Two Tasks

### Task A: Locate n* (the critical spectral index where Δe changes sign)

Run ALD-SED at n = {2.25, 2.5, 2.75, 3.0} using the CALIBRATED normalization (calibrate each to give var_x(β=0) ≈ 0.500). Measure Δe at β=1.0 for each n. Find where Δe=0.

You already have the n=3 result from E007: Δe(n=3) = +0.043 at β=1.
You already have the n=2 result from E007: Δe(n=2) = −0.066 at β=1.

Add n=2.25, 2.5, 2.75 to pin down n*.

**Expected:** Δe changes sign somewhere between n=2 and n=3. Fit a linear or quadratic interpolation to find n* exactly.

**If n* is close to 3.0:** The physical ZPF is at (or near) the stability boundary — very significant.
**If n* ≈ 2.5-2.7:** The ZPF is safely past the stability boundary, and the ALD cannot fully compensate. This quantifies the "spectral mismatch."

### Task B: Resolve the α discrepancy (physical vs. calibrated normalization)

Run n=3 with the PHYSICAL SED normalization. In the physical normalization, the noise amplitude is set by S_F(ω) = 2τħω³/m (not calibrated to hit 0.500). For the harmonic oscillator, this gives var_x ≈ 0.516 at β=0 (as seen in E004).

**To set the physical normalization:** Use C_3 = 2τħ/m = 2×0.01×1.0 = 0.02 (in natural units where ħ=m=1). But check: E004 got var_x_0 = 0.516 with the physical normalization. The physical C_3 should give that.

Alternative approach: run the simulation at β=0, measure var_x, and report it. Then run the full β scan with this normalization. The absolute value of C_3 matters.

For reference: E007's calibrated C₃ = 0.01954 (to give var_x_0 = 0.492). The physical C₃ should be slightly larger to give var_x_0 = 0.516.

Measure: Δe(β) at β ∈ {0.2, 0.5, 1.0} with physical normalization. Fit β^α. Does α→0.40 (matching E004)?

---

## Equations and Verified Parameters

**ALD equation (Landau-Lifshitz, verified from E004/E007):**
```
ẍ = −ω₀²x − 4βx³ − τ(ω₀² + 12βx²)ẋ + F_zpf(t) + τF'_zpf(t)
```

**FFT noise amplitude formula (VERIFIED — do not re-derive):**
```
A_k = sqrt(S(ω_k) × N / (2 × dt))
```

**For non-integer n:** S(ω) = C_n × ω^n for ω ∈ (0, ω_max]. Same formula applies.

**⚠️ dt = 0.05 ALWAYS. Do NOT use dt = π/ω_max (instability at β=1).**

**Fixed parameters:**
```
τ = 0.01, ω₀ = 1.0, ω_max = 10.0, dt = 0.05, T = 20000, N_ensemble = 200
β scan: {0.0, 0.2, 0.5, 1.0}
```

**QM reference values (matrix diagonalization, verified):**
```
β=0.0: 0.500, β=0.2: 0.370, β=0.5: 0.306, β=1.0: 0.257
```

**E007 code location:**
```
explorations/exploration-007/code/ald_sed_optimized.py
```
You should REUSE this code — it's already debugged and fast.

---

## Expected Analysis

**Task A output:**

| n     | C_n (calibrated) | var_x_0 | Δe(β=1) | sign |
|-------|-----------------|---------|---------|------|
| 2.00  | ~0.0198         | ~0.492  | −0.066  | −    |
| 2.25  | ?               | ~0.492  | ?       | ?    |
| 2.50  | ?               | ~0.492  | ?       | ?    |
| 2.75  | ?               | ~0.492  | ?       | ?    |
| 3.00  | ~0.0195         | ~0.492  | +0.043  | +    |

Fit: linear interpolation or quadratic fit to find n* where Δe(β=1) = 0.

**Task B output:**

| normalization | C₃      | var_x_0 | Δe(β=0.2) | Δe(β=0.5) | Δe(β=1.0) | α   |
|--------------|---------|---------|-----------|-----------|-----------|-----|
| Calibrated   | 0.01954 | 0.492   | 0.029     | 0.039     | 0.043     | 0.25|
| Physical     | ?       | ~0.516  | ?         | ?         | ?         | ?   |

Does α → 0.40 with physical normalization? If so, the E004 result is confirmed and α depends on normalization. If not, there's something else going on.

---

## Success Criteria

**Success:** n* located to ±0.1 precision (requires Δe to change sign between two adjacent n values among the 5 tested). α for physical normalization measured with ≥3 β points.

**Partial success:** n* bracketed but not precisely located; OR only Task B completed.

**Failure:** Simulation instability for non-integer n; normalization calibration fails.

---

## Prior Art Note

Do a quick literature search: "stochastic electrodynamics critical spectral index", "colored noise detailed balance Brownian oscillator", "ZPF spectral density anharmonic stability." We want to know if the n*≈2.6 crossover has been noted analytically.

---

## Output

Write your report to:
`explorations/exploration-008/REPORT.md`

Write your summary to:
`explorations/exploration-008/REPORT-SUMMARY.md`

Save code to:
`explorations/exploration-008/code/`

Working directory:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-001/`
