# Exploration 007 — β^0.40 Mechanism: Does the ω³ ZPF Spectrum Drive the Scaling?

## Mission Context

You are working on the Stochastic Electrodynamics (SED) mission: quantifying where SED succeeds and fails compared to quantum mechanics.

**What has been established in prior explorations (E001–E006):**

1. The SED harmonic oscillator ground state works: var_x = 0.507 ± 0.05 vs QM 0.500 (1.4% error).

2. The **Langevin-approximated** SED fails at O(β) for V(x) = ½x² + βx⁴: var_x increases with β while QM decreases. At β=1: SED/QM = 9.38×. Mechanism: ω³ ZPF noise + constant damping → positive feedback loop.

3. The **full ALD (Landau-Lifshitz order reduction)** fixes the O(β) failure by making damping position-dependent: Γ_eff = τ(ω₀² + 12βx²). Residual:

| β    | var_x QM | var_x ALD     | err  | Δe (baseline-corrected) |
|------|----------|---------------|------|------------------------|
| 0.00 | 0.500    | 0.516 ± 0.007 | +3.1% | 0 (baseline)           |
| 0.10 | 0.413    | 0.426 ± 0.006 | +3.2% | +0.013 − 0.016 ≈ −0.003 |
| 1.00 | 0.257    | 0.303 ± 0.004 | +17.8% | **+0.030** |

Baseline-corrected fit from β ∈ {0.2, 0.5, 1.0}: **Δe(β) ≈ 0.030 × β^0.40**
This exponent was ruled out to be O(β) (ratio test: 1.40 vs predicted 2.50) and O(β²) (ratio test: 1.40 vs predicted 6.25). β^0.40 was the best fit (predicted ratio 1.44 vs observed 1.40).

4. β^0.40 is REAL, not a UV artifact. E005 showed: Δe ~ ω_max^(−0.18) (tripling ω_max reduces Δe by 18%) and Δe ~ τ^0.23 (quintupling 1/τ reduces Δe by 31%). The β^0.40 exponent persists across all parameter scans.

**The open question:** What CAUSES β^0.40? Three hypotheses:
- H1 (spectral): The ω³ ZPF spectrum specifically drives the scaling — changing to white or ω^n noise would change the β-exponent.
- H2 (dynamical): The ALD equation structure itself (Landau-Lifshitz memory truncation) drives the scaling regardless of noise color.
- H3 (finite-parameter artifact): β^0.40 is a transient exponent in the accessible (τ~0.01, ω_max~10) regime; it would approach β² in the P&C limit τ→0.

This exploration tests H1 by running the SAME ALD simulation with FOUR different noise spectra.

---

## Your Specific Goal

Run the ALD-SED anharmonic oscillator simulation with four noise spectra:
- **n=3**: Standard ZPF, S_F(ω) = C₃ × ω³ (this reproduces the standard SED result from E004)
- **n=2**: ω² noise, S_F(ω) = C₂ × ω²
- **n=1**: ω¹ noise (pink-ish), S_F(ω) = C₁ × ω
- **n=0**: White noise, S_F(ω) = C₀ (flat spectrum)

For each spectrum:
1. Find normalization constant C_n so that var_x(β=0) = 0.500 ± 0.01 (matching the QM harmonic ground state)
2. Run the β scan: β ∈ {0.0, 0.2, 0.5, 1.0}
3. Compute baseline-corrected Δe(β) = [var_x_SED(β) − var_x_QM(β)] − [var_x_SED(β=0) − 0.500]
4. Fit Δe(β) for β ∈ {0.2, 0.5, 1.0} to a power law β^α
5. Report α(n) and the β^0.40 ratio test (does the observed ratio Δe(0.5)/Δe(0.2) match β^α predictions?)

**IMPORTANT NOTE:** Runs with n=0, 1, 2 are DIAGNOSTIC TESTS, not SED results. You are manipulating the noise spectrum to identify which mathematical feature drives the scaling. Only n=3 is physically SED. Frame your results accordingly.

---

## Equations and Verified Formulas

**ALD equation (Landau-Lifshitz order reduction):**
```
ẍ = −ω₀²x − 4βx³ − τ(ω₀² + 12βx²)ẋ + F_zpf(t) + τF'_zpf(t)
```
Where F'_zpf is the time derivative of the ZPF force (finite-difference: (F[i+1]−F[i])/dt).

**Noise PSD for exponent n:**
```
S_n(ω) = C_n × ω^n   (one-sided, for ω > 0)
```

**FFT noise amplitude formula (VERIFIED — do not re-derive):**
```
A_k = sqrt(S_n(ω_k) × N / (2 × dt))
```
where N is the number of timesteps, dt the timestep, ω_k = 2πk/(N×dt).

**⚠️ CRITICAL dt WARNING from E005:** ALWAYS use dt=0.05. Do NOT use dt = π/ω_max (Nyquist formula) — this causes Euler-Cromer instability at β=1 because ω_eff ≈ 7 → stability requires dt < 0.29, but π/10 ≈ 0.314 exceeds the limit.

**Normalization approach:** For each n, run a short calibration at β=0 (e.g., 50 trajectories × T=5000) to find var_x_calibration. Scale C_n by (0.500/var_x_calibration)^... Wait: scale S_n by the ratio (0.500/var_x_calibration), since var_x ∝ C_n. Then verify on a longer run that var_x(β=0) is within ±0.01 of 0.500 before proceeding.

---

## Fixed Parameters (hold constant across all n)

```
τ = 0.01
ω₀ = 1.0
ω_max = 10.0
dt = 0.05          # FIXED — do NOT change this
T = 20000          # integration time per trajectory
N_ensemble = 200   # trajectories per β value
β values = [0.0, 0.2, 0.5, 1.0]
```

---

## QM Reference Values

```python
var_x_QM = {
    0.0:  0.500,
    0.1:  0.413,   # from matrix diagonalization (E003)
    0.2:  0.370,   # approximate (from perturbation + extrapolation)
    0.5:  0.306,
    1.0:  0.257
}
```

The exact values at β=0.2 and β=0.5 should be verified by matrix diagonalization in your code. V(x) = ½x² + βx⁴, truncate at reasonable basis size (e.g., 150 harmonic oscillator states).

---

## Expected Analysis

For each exponent n, you should produce:

1. **Normalization check**: C_n value and var_x at β=0 after calibration.

2. **β scan table**:
```
| β   | var_x_QM | var_x_n=X | raw_err | Δe_corrected |
|-----|----------|-----------|---------|--------------|
| 0.0 | 0.500    | ...       | ...     | 0 (baseline) |
| 0.2 | 0.370    | ...       | ...     | ...          |
| 0.5 | 0.306    | ...       | ...     | ...          |
| 1.0 | 0.257    | ...       | ...     | ...          |
```

3. **Power law fit**: fit Δe(β) for β ∈ {0.2, 0.5, 1.0} to C×β^α. Report α with uncertainty.

4. **Ratio test**: Δe(0.5)/Δe(0.2) vs predictions for α = 0.40, 1.0, 2.0.

5. **Direction test**: Does var_x increase or decrease with β for this n? (QM: decreases.)

**Summary table across all n:**
```
| n | Spectrum | C_n    | α (β^α fit) | direction (↑/↓) | β^0.40? |
|---|----------|--------|-------------|-----------------|---------|
| 3 | ω³ ZPF   | ...    | ...         | ↓ (correct)     | YES     |
| 2 | ω²       | ...    | ...         | ...             | ...     |
| 1 | ω¹       | ...    | ...         | ...             | ...     |
| 0 | white    | ...    | ...         | ...             | ...     |
```

---

## Success Criteria

**Success:** For each of the 4 spectra, a β^α power law is measured with enough precision to discriminate among α = 0.40, 1.0, 2.0 (requires at least 3 β points). A clear verdict is reached: does β^0.40 scale with n or is it n-independent?

**Partial success:** 2-3 spectra completed with clear α values; 1 spectrum hits numerical issues (e.g., white noise normalization near zero or UV instability).

**Failure:** Unable to normalize spectra consistently; β^α fit is degenerate (all four show α ≈ 0 or α → ∞); simulation is unstable for white noise.

---

## Prior Art Note

You should check the SED literature for any prior work on:
1. Anharmonic oscillators driven by noise with non-ω³ spectra
2. The Landau-Lifshitz reduction applied to colored noise
3. Any analytical predictions for the β-scaling exponent in ALD-SED

Use web search. Search terms: "stochastic electrodynamics anharmonic colored noise", "Abraham-Lorentz dynamics quartic oscillator noise spectrum", "Pesquera Claverie SED spectral density anharmonic".

---

## Output Location

Write your report to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-001/explorations/exploration-007/REPORT.md`

Write your summary to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-001/explorations/exploration-007/REPORT-SUMMARY.md`

Save all code to:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-001/explorations/exploration-007/code/`
