# Exploration 004: Full Abraham-Lorentz Dynamics — Landau-Lifshitz Order Reduction

## Goal

Test whether the Landau-Lifshitz (LL) order-reduced Abraham-Lorentz dynamics —
with **position-dependent damping** Γ_eff = τ(ω₀² + 12βx²) — fixes the O(β)
failure found in exploration 003 (constant-damping Langevin approximation).

Compare against:
- QM reference (matrix diagonalization, E003, exact)
- E003 Langevin results (constant damping Γ = τω₀² = 0.01)

**Physical question:** Does Pesquera & Claverie (1982) hold? SED should agree
with QM at O(β) and fail only at O(β²).

---

## Physics: The Landau-Lifshitz Equation

The Abraham-Lorentz equation for V(x) = ½ω₀²x² + βx⁴ (natural units: m=ħ=ω₀=1):

    ẍ = F(x) + τẍ_dot + F_zpf(t)       [AL equation]

where F(x) = −ω₀²x − 4βx³ and the τẍ_dot term (radiation reaction) causes runaways.

**LL order reduction:** Replace ẍ_dot with its zeroth-order approximation:

    τẍ_dot ≈ τF'(x)·ẋ + τF'_zpf(t)

where F'(x) = ∂F/∂x = −ω₀² − 12βx².

This gives the final LL equation:

    ẍ = −ω₀²x − 4βx³ − τ(ω₀² + 12βx²)ẋ + F_zpf(t) + τF'_zpf(t)

**Key difference from E003:** Γ_eff(x) = τ(ω₀² + 12βx²) INCREASES at large x.
When β > 0 and x is large, damping grows as 12βτx², counteracting the ω³ noise
pumping that caused runaway in the Langevin approximation.

**Parameters:** τ=0.01, ω₀=1, ω_max=10, dt=0.05, T=20000 per trajectory.

---

## Implementation

### Noise generation (verified in E003)
F_zpf(t) with PSD S_F(ω) = 2τω³ (one-sided) via FFT.
Amplitude: A_k = sqrt(S_F(ω_k) × N_t / (2·dt)).

### Noise derivative (new in E004)
τ·F'_zpf(t) computed in frequency domain by multiplying coefficients by iωτ before IFFT.
Nyquist component zeroed to preserve real output.
PSD of τF'_zpf: S_{τF'}(ω) = 2τ³ω⁵ — at ω_max=10, this is ~1% of S_F(ω_max).

### Integration
Euler-Cromer (symplectic Euler). Position-dependent Γ_eff(x) recomputed each step.

**Code:** `code/ald_simulate.py` (complete implementation)
**Analysis:** `code/analyze_ald.py` (order-of-failure analysis)

---

## Results: All β Values

All simulations used N_ensemble=200, T=20000, dt=0.05, seed=42 (same as E003 for fair comparison).

### β = 0.0 (Harmonic Oscillator Baseline)

```
var_x_ALD  = 0.5157 ± 0.0074
var_x_QM   = 0.5000
Frac_diff  = +3.14%  (2.1σ)
```

**[COMPUTED]** β=0 ALD matches E003 Langevin (0.515) exactly because at β=0,
Γ_eff = τω₀² = constant, and τF'_zpf adds negligible variance (its PSD is
τ²ω² × S_F, giving RMS ≈ 0.23 vs 2.82 for F_zpf — 8% correction at ω_max,
below statistical noise). Passes 5% threshold.

### β = 0.01

```
var_x_ALD  = 0.5027 ± 0.0068    var_x_QM = 0.4862
Frac_diff  = +3.40%  (2.4σ)
E003 Langevin: 0.529 ± 0.008 (+8.8%, 5.4σ)
```

**[COMPUTED]** ALD reduces error from 5.4σ to 2.4σ. β-dependent excess over
baseline: +0.0008 (0.12σ) — **statistically indistinguishable from zero**.

### β = 0.05

```
var_x_ALD  = 0.4654 ± 0.0069    var_x_QM = 0.4458
Frac_diff  = +4.39%  (2.8σ)
```

**[COMPUTED]** β-dependent excess: +0.0039 (0.57σ) — marginally distinguishable
from baseline, within noise.

### β = 0.10

```
var_x_ALD  = 0.4256 ± 0.0061    var_x_QM = 0.4125
Frac_diff  = +3.17%  (2.1σ)
E003 Langevin: 0.735 ± 0.014 (+78.2%, 23.6σ)
```

**[COMPUTED]** ALD reduces error from 23.6σ to 2.1σ — an 11x improvement.
β-dependent excess: −0.0026 (−0.43σ) — within noise. ALD agrees with QM
within the β=0 baseline systematic.

### β = 0.20

```
var_x_ALD  = 0.4014 ± 0.0050    var_x_QM = 0.3700
Frac_diff  = +8.50%  (6.3σ)
```

**[COMPUTED]** β-dependent excess: +0.0158 (3.2σ) — first **statistically
significant** β-dependent failure. Exceeds baseline systematic.

### β = 0.50

```
var_x_ALD  = 0.3435 ± 0.0040    var_x_QM = 0.3058
Frac_diff  = +12.34%  (9.4σ)
```

**[COMPUTED]** β-dependent excess: +0.0220 (5.5σ). Clear signal.

### β = 1.00

```
var_x_ALD  = 0.3028 ± 0.0038    var_x_QM = 0.2571
Frac_diff  = +17.79%  (12.2σ)
E003 Langevin: 2.411 ± 0.043 (+837.8%, 50.5σ)
```

**[COMPUTED]** ALD reduces error from 50.5σ to 12.2σ — a 4x improvement in
statistical significance, and an improvement from 838% fractional error to 18%.

---

## 3-Way Comparison Table

| β    | var_x QM | var_x ALD     | ALD err | ALD σ | var_x Langevin | Lang err |
|------|----------|---------------|---------|-------|----------------|----------|
| 0.00 | 0.5000   | 0.5157±0.0074 | +3.1%   | +2.1σ | 0.515±0.007    | +3.0%    |
| 0.01 | 0.4862   | 0.5027±0.0068 | +3.4%   | +2.4σ | 0.529±0.008    | +8.8%    |
| 0.05 | 0.4458   | 0.4654±0.0069 | +4.4%   | +2.8σ | ---            | ---      |
| 0.10 | 0.4125   | 0.4256±0.0061 | +3.2%   | +2.1σ | 0.735±0.014    | +78.2%   |
| 0.20 | 0.3700   | 0.4014±0.0050 | +8.5%   | +6.3σ | ---            | ---      |
| 0.50 | 0.3058   | 0.3435±0.0040 | +12.3%  | +9.4σ | ---            | ---      |
| 1.00 | 0.2571   | 0.3028±0.0038 | +17.8%  | +12.2σ| 2.411±0.043    | +837.8%  |

**Key:** ALD reduces error by 11x at β=0.1 and 47x at β=1.0 compared to Langevin.

---

## Order-of-Failure Analysis

**[COMPUTED]** using `code/analyze_ald.py`.

### β-dependent excess above baseline

Defining Δe(β) = [var_x_ALD(β) − var_x_QM(β)] − [var_x_ALD(0) − var_x_QM(0)]:

| β    | Δe(β)   | Significance |
|------|---------|--------------|
| 0.01 | +0.0008 | 0.1σ (noise) |
| 0.05 | +0.0039 | 0.6σ (noise) |
| 0.10 | −0.0026 | −0.4σ (noise)|
| 0.20 | +0.0158 | 3.2σ ★       |
| 0.50 | +0.0220 | 5.5σ ★★      |
| 1.00 | +0.0300 | 8.0σ ★★★     |

### Power-law fit (β = 0.2, 0.5, 1.0)

```
Δe(β) ≈ 0.030 × β^0.40
```

Ratios:
- O(β¹) prediction: Δe(0.5)/Δe(0.2) = 2.50 expected, **1.40 observed**
- O(β²) prediction: Δe(0.5)/Δe(0.2) = 6.25 expected, **1.40 observed**
- O(β^0.4): Δe(0.5)/Δe(0.2) = 1.44 expected, **1.40 observed** ✓

**Conclusion [COMPUTED]:** The β-dependent ALD failure grows as β^0.40 (sublinear),
which is:
- Much slower than the Langevin O(β) failure
- Also slower than the Pesquera-Claverie O(β²) prediction

For β ≤ 0.1: ALD failure is **statistically indistinguishable** from the β=0
systematic (within noise). The O(β) positive feedback loop is ELIMINATED.

For β > 0.2: A residual β-dependent failure emerges, growing as β^0.40.

---

## Does ALD Fix the O(β) Failure? Yes — with Caveats

### Main claim: O(β) failure is eliminated [COMPUTED]

For β ≤ 0.1 (the "linear SED regime" from E003), the ALD error is consistent
with JUST the β=0 baseline:
- β=0.10: Δe = −0.0026 ± 0.0061 (within noise)
- Contrast with Langevin: +0.322 ± 0.014 at β=0.1 (23σ excess)

The position-dependent damping Γ_eff = τ(ω₀² + 12βx²) successfully prevents
the ω³ noise pumping that drove the Langevin oscillator to large amplitude.

### Residual failure at large β: not O(β²) as P&C predict [CONJECTURED]

P&C (1982) predicted failure only at O(β²τ). For our parameters (τ=0.01,β=1):
P&C would predict ΔE_P&C ∝ τβ² = 0.01. Our observed excess is ~0.030 — larger.

Possible explanations:
1. **UV cutoff effect**: ω_max=10 truncates the ZPF spectrum. At finite ω_max,
   the FDT balance is imperfect. The anharmonic term β·x⁴ drives higher-frequency
   components, and the UV truncation creates a β-dependent systematic. This effect
   is not included in P&C's τ→0 analysis.
2. **Finite-τ effects**: P&C's analysis holds for τ→0. At τ=0.01, there are
   higher-order τ corrections. For β=1: ΔE ~ τ²β² corrections ~ 0.0001 (too small).
3. **LL approximation error**: The LL reduction itself introduces O(τ²) errors,
   independently of β. For τ=0.01, O(τ²) ~ 0.0001 (too small to explain 0.030).

The most likely explanation is the UV cutoff effect. This is not a failure of SED
per se but a numerical artifact of the finite spectrum. The P&C prediction
(O(β²τ) → essentially zero for τ=0.01) would apply in the ω_max→∞ limit.

**Bottom line:** The β^0.40 growth is likely a UV-cutoff artifact, not an
intrinsic SED failure. Testing with ω_max = 20 would confirm or refute this.

---

## Physical Interpretation

### Why does position-dependent damping fix the O(β) failure?

**E003 failure mechanism:** Constant damping Γ = τω₀² = 0.01 does not increase
with amplitude. The ω³ ZPF noise spectrum pumps the oscillator at all frequencies
equally. For the anharmonic oscillator, larger x means larger restoring force, but
the NOISE force also scales up via the ω³ spectrum. With constant damping, there's
a net positive feedback: the noise pumps the oscillator to larger x, which couples
to higher-frequency modes, which have larger noise → runaway.

**ALD fix:** Γ_eff(x) = τ(ω₀² + 12βx²). At equilibrium:

| β    | ⟨Γ_eff⟩ = τ(ω₀²+12β⟨x²⟩) | vs constant Γ=0.01 | Ratio |
|------|---------------------------|---------------------|-------|
| 0.00 | 0.0100                    | 0.0100              | 1.00  |
| 0.01 | 0.0106                    | 0.0100              | 1.06  |
| 0.05 | 0.0128                    | 0.0100              | 1.28  |
| 0.10 | 0.0151                    | 0.0100              | 1.51  |
| 0.20 | 0.0196                    | 0.0100              | 1.96  |
| 0.50 | 0.0306                    | 0.0100              | 3.06  |
| 1.00 | 0.0463                    | 0.0100              | 4.63  |

At β=1, the position-dependent damping is 4.6× larger than the constant-damping
case. This additional dissipation counteracts the ω³ noise pumping, stabilizing
the oscillator near its correct QM amplitude.

**The slope comparison [COMPUTED]:**
```
Δvar_x (β=0 → β=1):
  QM:       −0.243  (var_x decreases — quartic confinement wins)
  ALD:      −0.213  (ALD correctly tracks QM direction, 88% of slope)
  Langevin: +1.896  (wrong sign — noise pumping dominates)
```

The ALD gets the SIGN correct (QM direction) and the MAGNITUDE to within 12%.
The Langevin was wrong by over 800%.

---

## Verification Status Summary

All computation results are from executed code in `code/ald_simulate.py` and
`code/analyze_ald.py`, saved to `code/ald_results.json`.

- **7 β values simulated** [COMPUTED] — each with N=10,000 samples, no runaways
- **3-way comparison** [COMPUTED] — ALD vs QM vs Langevin
- **Order-of-failure fit** [COMPUTED] — Δe(β) ∝ β^0.40
- **Physical mechanism** [COMPUTED] — Γ_eff increases 1.0×–4.6× over β range
- **P&C discrepancy interpretation** [CONJECTURED] — UV cutoff explanation

---

## What This Means for SED vs QM

The central question from E003 was: does the O(β) Langevin failure reflect a
fundamental SED limitation or just the crude approximation of constant damping?

**E004 answer:** It was the approximation. With position-dependent damping:
- For β ≤ 0.1: ALD matches QM within statistical noise (no O(β) failure)
- For β > 0.2: A residual sublinear (β^0.40) failure emerges, likely UV cutoff

**What Pesquera & Claverie predicted is approximately supported:**
The O(β) failure is gone; only a small, slowly-growing discrepancy remains.
Whether this residual grows as O(β²) as P&C predict, or as β^0.40 due to UV
artifacts, cannot be definitively determined with ω_max=10 alone.

**Verdict:** SED with full ALD is a qualitatively different theory from the
Langevin approximation. It correctly tracks the QM ground state direction, and
its residual errors are much smaller and more slowly growing. This is consistent
with the Pesquera-Claverie claim, though full verification requires testing with
larger ω_max and smaller τ.

---

## Limitations and Future Work

1. **UV cutoff test**: Run with ω_max = 20 to check if β^0.40 growth is a UV artifact
2. **τ-dependence**: Reduce τ to 0.001 to approach P&C's τ→0 regime
3. **Small-β precision**: Fine scan β = [0.001, 0.01] to measure the true O(β) vs O(β²) crossover
4. **Exact AL vs LL**: Compare LL with the exact Abraham-Lorentz equation (e.g., Runge-Kutta on the 3rd-order ODE with runaway suppression via asymptotic matching)
5. **P(x) shape**: Compute the full position distribution and compare KS statistics with QM and E003 Langevin
