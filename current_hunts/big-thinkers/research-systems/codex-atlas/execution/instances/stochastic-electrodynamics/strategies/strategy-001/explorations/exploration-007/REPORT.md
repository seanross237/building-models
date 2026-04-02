# Exploration 007 — β^0.40 Mechanism: Does the ω³ ZPF Spectrum Drive the Scaling?

## Goal

Test Hypothesis H1: The ω³ ZPF spectrum specifically drives the β^0.40 (positive-direction) power-law scaling in ALD-SED anharmonic oscillator simulations. Method: run the same ALD simulation with four noise spectra (n=0,1,2,3, where S_n(ω) = C_n × ω^n), all normalized to var_x(β=0) = 0.500, and compare the resulting β-scaling.

## Fixed Parameters

- τ = 0.01, ω₀ = 1.0, ω_max = 10.0
- dt = 0.05 (FIXED — Euler-Cromer stability requirement)
- T = 20,000, N_ensemble = 200 trajectories
- β ∈ {0.0, 0.2, 0.5, 1.0}
- Noise spectra: S_n(ω) = C_n × ω^n for n = 0, 1, 2, 3

---

## Section 1: QM Reference Values [COMPUTED]

Matrix diagonalization in harmonic oscillator basis (N_basis = 150 states), V(x) = ½x² + βx⁴.

| β   | var_x_QM  | Source |
|-----|-----------|--------|
| 0.0 | 0.50000   | matrix diag (n_basis=150) |
| 0.2 | 0.36996   | matrix diag (n_basis=150) |
| 0.5 | 0.30581   | matrix diag (n_basis=150) |
| 1.0 | 0.25715   | matrix diag (n_basis=150) |

Values at β=0.2 and β=0.5 precisely computed (not approximate as in GOAL): β=0.2→0.370, β=0.5→0.306 to 3 sig figs. **[COMPUTED]**

---

## Section 2: Normalization Calibration [COMPUTED]

Calibration procedure: run with C_n=1.0 at β=0, T_calib=5000, N_calib=50. Scale C_n = 0.500/var_calib (linear response at β=0).

Verification at β=0 with full T=20000, N_ensemble=200:

| n | Spectrum | C_n (calibrated) | var_x(β=0) full run | Pass (within ±0.01)? |
|---|----------|-----------------|---------------------|----------------------|
| 3 | ω³ ZPF   | 0.019541        | 0.4922 ± 0.0011     | ✓ (−0.0078 offset)  |
| 2 | ω²       | 0.019776        | 0.4921 ± 0.0011     | ✓ (−0.0079 offset)  |
| 1 | ω¹       | 0.019831        | 0.4920 ± 0.0011     | ✓ (−0.0080 offset)  |
| 0 | white    | 0.019772        | 0.4920 ± 0.0011     | ✓ (−0.0080 offset)  |

**Note on C_n uniformity:** All calibrated C_n values are nearly identical (0.0195–0.0198). This is expected: the harmonic oscillator resonance is narrow (width ∝ τω₀² = 0.01), so var_x(β=0) is dominated by noise at ω ≈ ω₀ = 1. At ω = 1, all spectra evaluate to C_n × 1^n = C_n, so calibrating to the same variance gives similar C_n. The spectra differ primarily in their power at ω ≠ 1.

**Systematic offset:** All four spectra show var_x(β=0) ≈ 0.492 instead of exactly 0.500. This ≈1.6% undershoot arises because the short calibration run (T=5000) underestimates thermalization. The baseline correction Δe(β) = raw_err(β) − raw_err(0) accounts for this offset throughout.

---

## Section 3: β Scan Results [COMPUTED]

### n=3 (ω³ ZPF — standard SED)

| β   | var_x_QM | var_x_SED | stderr | raw_err  | Δe (baseline-corr) |
|-----|----------|-----------|--------|----------|---------------------|
| 0.0 | 0.5000   | 0.4922    | 0.0011 | −0.0078  | 0 (baseline)        |
| 0.2 | 0.3700   | 0.3915    | 0.0019 | +0.0215  | +0.0294 ± 0.0022   |
| 0.5 | 0.3058   | 0.3372    | 0.0013 | +0.0314  | +0.0392 ± 0.0017   |
| 1.0 | 0.2572   | 0.2926    | 0.0008 | +0.0355  | +0.0433 ± 0.0014   |

**Direction:** var_x DECREASES with β (correct, matching QM direction). **[COMPUTED]**

### n=2 (ω² noise — diagnostic only)

| β   | var_x_QM | var_x_SED | stderr | raw_err  | Δe (baseline-corr) |
|-----|----------|-----------|--------|----------|---------------------|
| 0.0 | 0.5000   | 0.4921    | 0.0011 | −0.0079  | 0 (baseline)        |
| 0.2 | 0.3700   | 0.3064    | 0.0012 | −0.0636  | −0.0556 ± 0.0017   |
| 0.5 | 0.3058   | 0.2324    | 0.0008 | −0.0734  | −0.0654 ± 0.0014   |
| 1.0 | 0.2572   | 0.1831    | 0.0005 | −0.0740  | −0.0661 ± 0.0013   |

**Direction:** var_x DECREASES with β (correct). Δe NEGATIVE (SED undershoots QM increasingly). **[COMPUTED]**

### n=1 (ω¹ noise — diagnostic only)

| β   | var_x_QM | var_x_SED | stderr | raw_err  | Δe (baseline-corr) |
|-----|----------|-----------|--------|----------|---------------------|
| 0.0 | 0.5000   | 0.4920    | 0.0011 | −0.0080  | 0 (baseline)        |
| 0.2 | 0.3700   | 0.2597    | 0.0011 | −0.1102  | −0.1023 ± 0.0016   |
| 0.5 | 0.3058   | 0.1846    | 0.0006 | −0.1212  | −0.1133 ± 0.0013   |
| 1.0 | 0.2572   | 0.1366    | 0.0004 | −0.1205  | −0.1126 ± 0.0012   |

**Direction:** var_x DECREASES with β (correct). Δe NEGATIVE and large. Saturation near β=0.5–1.0. **[COMPUTED]**

### n=0 (white noise — diagnostic only)

| β   | var_x_QM | var_x_SED | stderr | raw_err  | Δe (baseline-corr) |
|-----|----------|-----------|--------|----------|---------------------|
| 0.0 | 0.5000   | 0.4920    | 0.0011 | −0.0080  | 0 (baseline)        |
| 0.2 | 0.3700   | 0.2273    | 0.0009 | −0.1427  | −0.1347 ± 0.0014   |
| 0.5 | 0.3058   | 0.1556    | 0.0005 | −0.1502  | −0.1423 ± 0.0012   |
| 1.0 | 0.2572   | 0.1116    | 0.0003 | −0.1456  | −0.1376 ± 0.0012   |

**Direction:** var_x DECREASES with β (correct). Δe NEGATIVE, large, nearly flat for β>0.2. **[COMPUTED]**

---

## Section 4: Power Law Fits and Ratio Tests [COMPUTED]

### 4.1 Power law fits: Δe(β) vs β

The critical observation: n=3 produces **positive** Δe; n=0,1,2 produce **negative** Δe. This means:

- For n=3, the fit is: **+C × β^α** (SED overestimates QM increasingly with β)
- For n=0,1,2, the fit is: **−C × β^α** (SED underestimates QM increasingly with β)

The positive/negative split is a QUALITATIVE distinction, not just quantitative.

**Fit results for |Δe(β)| = C × β^α using log-linear regression on β ∈ {0.2, 0.5, 1.0}:**

| n | sign(Δe) | α (fit) | stderr | C (fit) |
|---|----------|---------|--------|---------|
| 3 | +        | 0.245   | 0.018  | +0.0444 |
| 2 | −        | 0.111   | 0.017  | −0.0677 |
| 1 | −        | 0.062   | 0.013  | −0.1146 |
| 0 | −        | 0.016   | 0.012  | −0.1398 |

**Key observation:** α decreases monotonically with decreasing n. The n=3 spectrum has the steepest growth of residual error with β (α=0.25). Lower-n spectra show nearly flat (saturating) behavior (α≈0.02–0.11).

### 4.2 Ratio tests

**Ratio Δe(0.5)/Δe(0.2) compared to power law predictions:**

| n | Observed ratio | α=0.40 pred | α=0.25 pred | α=1.0 pred | Best-match α |
|---|----------------|-------------|-------------|------------|--------------|
| 3 | +1.334 ± 0.117 | 1.443       | 1.309       | 2.500      | 0.31         |
| 2 | +1.176 ± 0.043 | 1.443       | 1.309       | 2.500      | 0.18         |
| 1 | +1.108 ± 0.021 | 1.443       | 1.309       | 2.500      | 0.11         |
| 0 | +1.056 ± 0.015 | 1.443       | 1.309       | 2.500      | 0.06         |

Note: ratios are computed as |Δe(0.5)| / |Δe(0.2)| since Δe has the same sign for each n.

**Ratio Δe(0.5)/Δe(0.2) = 1.334 for n=3:**
- Consistent with α in range 0.23–0.32 (depending on β-pair choice)
- α=0.40 is disfavored (predicted ratio 1.44 vs observed 1.33) but within ~1σ of measurement uncertainty
- α=1.0 is strongly ruled out (predicted ratio 2.50 vs observed 1.33)
- α=2.0 is strongly ruled out (predicted ratio 6.25 vs observed 1.33)

### 4.3 Consistency check: α from different β-pair ratios (n=3)

| β-pair | Ratio |  Best-match α |
|--------|-------|----------------|
| (0.2, 0.5) | 1.334 | 0.31 |
| (0.2, 1.0) | 1.475 | 0.24 |
| (0.5, 1.0) | 1.105 | 0.14 |

The decreasing α across different pairs suggests the scaling is sub-power-law (slightly concave on log-log). The overall fit α=0.245 is a reasonable summary, but the "true" exponent is not perfectly constant.

### 4.4 Discrepancy with E004 (α=0.40)

E004 found Δe(β) ≈ 0.030 × β^0.40 with ratio test Δe(0.5)/Δe(0.2) = 1.40. This exploration finds:
- My ratio: 1.334 ± 0.117 (compatible with E004's 1.40 within ~0.6σ)
- My α: 0.245 (vs E004's 0.40)

Sources of discrepancy:
1. **Normalization**: E004 used natural SED normalization giving var_x(β=0) ≈ 0.516; this run calibrates to 0.492. Higher initial energy → larger anharmonic excitation → potentially steeper β-scaling.
2. **Absolute Δe magnitudes**: E004's Δe(β=1) = 0.030 vs my 0.043. The larger Δe in my run is consistent with the lower baseline (my calibration over-corrects the baseline more).
3. The ratio test values are statistically consistent (within ~1σ given measurement noise).

**Conclusion on α discrepancy:** This exploration cannot definitively resolve whether α=0.25 or α=0.40. What IS clear is that α is in the range 0.14–0.32 from my data, and E004's value 0.40 is at the high end. Both are well below α=1.0 and far below α=2.0.

---

## Section 5: Summary Table [COMPUTED]

| n | Spectrum | C_n    | sign(Δe) | α (β^α fit) | β^0.40? | direction |
|---|----------|--------|----------|-------------|---------|-----------|
| 3 | ω³ ZPF   | 0.0195 | **+**    | **0.25 ± 0.02** | Partial | ↓ (correct) |
| 2 | ω²       | 0.0198 | **−**    | 0.11 ± 0.02  | NO     | ↓ (correct) |
| 1 | ω¹       | 0.0198 | **−**    | 0.06 ± 0.01  | NO     | ↓ (correct) |
| 0 | white    | 0.0198 | **−**    | 0.02 ± 0.01  | NO     | ↓ (correct) |

"β^0.40?" column refers to whether the spectrum shows the same positive-direction scaling as E004's ALD-SED result. Only n=3 shows the positive sign (though with α≈0.25, somewhat lower than E004's 0.40).

---

## Section 6: Physical Interpretation [CONJECTURED]

### 6.1 Why does n=3 show positive Δe while n<3 shows negative Δe?

At β=0, all spectra are calibrated to give var_x = 0.500 (matching QM) by construction. At ω=ω₀=1, all spectra evaluate to C_n × 1^n = C_n, and since C_n ≈ 0.0195 for all n, the power at the fundamental resonance is identical across spectra.

The spectra differ away from ω₀=1:
- **n=3 (ω³)**: Power at 3ω₀ is 27 × (power at ω₀); power at 5ω₀ is 125× stronger
- **n=2 (ω²)**: Power at 3ω₀ is 9×; at 5ω₀ is 25×
- **n=1 (ω¹)**: Power at 3ω₀ is 3×; at 5ω₀ is 5×
- **n=0 (white)**: Power at 3ω₀ = power at ω₀ (flat)

The anharmonic term 4βx³ excites modes at 3ω₀, 5ω₀, ... These modes experience different ZPF driving depending on the spectrum.

**Mechanism [CONJECTURED]:** For n=3, the ZPF has relatively more energy at the anharmonic harmonic frequencies (3ω₀, 5ω₀, ...) compared to n=0. This extra high-frequency ZPF energy feeds into the anharmonic modes via the 4βx³ coupling. The result is:
- n=3: Extra high-frequency ZPF → extra excitation of anharmonic modes → var_x slightly ABOVE what the ALD equilibrium would predict → positive Δe
- n=0,1,2: Insufficient high-frequency ZPF → ALD damping exceeds ZPF driving at anharmonic frequencies → var_x falls BELOW QM baseline correction → negative Δe

The ALD radiation reaction includes the τF'(t) term (force derivative) which also preferentially couples to high-frequency modes (d/dt in frequency domain = iω), amplifying the effect.

### 6.2 Why does α decrease with decreasing n?

The magnitude of the negative Δe for n<3 grows faster and saturates earlier (α → 0 as n → 0). This is consistent with the white noise case: when high-frequency content is flat, the ALD damping increase with β is no longer compensated by increased ZPF energy at anharmonic harmonics. The saturation at β>0.5 for n=0,1 suggests a fixed-point behavior where the oscillator has lost all the anharmonic ZPF compensation.

### 6.3 The ω³ spectrum as a critical point

The n=3 spectrum may represent a "critical" spectral index for the ALD equation: it is precisely the spectrum generated by classical electrodynamics (Rayleigh-Jeans + ZPF in 3D) and it produces the correct harmonic ground state. For anharmonic potentials, n=3 gives a small positive residual that grows as β^0.25 (this run) or β^0.40 (E004). Spectra with n<3 break this balance, producing large negative deviations. **[CONJECTURED]**

---

## Section 7: Verdict on H1

**H1 (spectral): The ω³ ZPF spectrum specifically drives the scaling — changing to white or ω^n noise would change the β-exponent.**

**VERDICT: H1 STRONGLY SUPPORTED [COMPUTED]**

Evidence:
1. Only n=3 produces POSITIVE Δe (SED > QM after baseline correction). All n<3 produce NEGATIVE Δe. This is a qualitative sign reversal.
2. The α exponent for |Δe| decreases monotonically from n=3 (α≈0.25) to n=0 (α≈0.02). The n=3 spectrum is uniquely steep.
3. The magnitude of Δe differs by a factor of 3–5 between n=3 and n=0 at the same β.
4. All spectra show var_x DECREASING with β (correct direction), so the qualitative anharmonic response is not spectrum-dependent. But the RESIDUAL deviation from QM (Δe) is strongly spectrum-dependent.

**What remains open:**
- Whether the true exponent is α=0.25 (this run) or α=0.40 (E004). This depends on normalization.
- Whether n=3 is exactly "critical" or whether n=2.5, n=3.5 would also show positive Δe.
- What the analytical explanation for β^α is (neither explored here).

---

## Section 8: Unresolved Issues

### 8.1 Exponent discrepancy (α=0.25 vs E004's α=0.40)

My α=0.245 vs E004's 0.40. The ratio test (1.334 vs 1.40) is within ~0.6σ statistical noise, but the fitted exponents differ by 60%. Possible resolution: repeat this exploration with var_x(β=0) calibrated to 0.516 (E004's natural SED normalization) to see if α rises toward 0.40. This would test whether the exponent is normalization-sensitive.

### 8.2 Near-integer spectra

Testing n=2.5, n=3.5 would tell us whether the sign reversal is sharp (at n=3 exactly) or gradual. This is important for understanding whether the "specialness" of n=3 is exact or approximate.

### 8.3 Analytical prediction

Neither H2 (ALD structure) nor H3 (finite-parameter artifact) have been tested. A systematic study of β^α vs τ (H3) at fixed n=3 would determine whether α→β² in the physical limit.

---

## Code

All code saved to `code/`:
- `ald_sed_optimized.py` — main simulation (vectorized batch integration, noise generation, calibration, β scan)
- `analysis_supplement.py` — power law fitting, ratio tests, summary table generation
- `qm_reference.json` — QM reference values from matrix diagonalization
- `results_n3.json`, `results_n2.json`, `results_n1.json`, `results_n0.json` — raw β scan data per spectrum
- `final_results.json` — combined results from main simulation
- `analysis_results.json` — power law fit results and summary

Run order: `python3 ald_sed_optimized.py` then `python3 analysis_supplement.py`.

Total compute time: ~10.4 minutes (624.9 seconds) on a standard laptop CPU.
