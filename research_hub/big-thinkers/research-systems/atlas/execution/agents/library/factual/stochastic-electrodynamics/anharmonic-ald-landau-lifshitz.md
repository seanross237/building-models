---
topic: SED anharmonic oscillator — ALD with Landau-Lifshitz order reduction
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-004"
---

## Key Result

The Landau-Lifshitz (LL) order-reduced Abraham-Lorentz-Dirac equation **eliminates the O(β) failure** found in the Langevin approximation, confirming that the Langevin failure was an artifact of the approximation, not a fundamental SED limitation. This is consistent with the Pesquera & Claverie (1982) prediction that full ALD should fail only at O(β²).

For **β ≤ 0.10**: ALD error is statistically indistinguishable from the β=0 baseline — no O(β) excess.
For **β > 0.20**: A residual sublinear (β^0.40) failure emerges, conjectured to be a UV cutoff artifact.

## The LL Equation

For V(x) = ½ω₀²x² + βx⁴ (natural units m=ħ=ω₀=1), the LL-reduced equation is:

    ẍ = −ω₀²x − 4βx³ − τ(ω₀² + 12βx²)ẋ + F_zpf(t) + τF'_zpf(t)

Key: position-dependent damping **Γ_eff(x) = τ(ω₀² + 12βx²) increases at large x**.
τF'_zpf(t) is computed in frequency domain (iω multiplication); PSD ~ 2τ³ω⁵ (~1% of primary noise at ω_max=10).

Parameters: τ=0.01, ω₀=1, ω_max=10, dt=0.05, T=20000, N_ensemble=200.

## 3-Way Comparison Table (ALD vs QM vs Langevin)

| β    | var_x QM | var_x ALD     | ALD err  | ALD σ  | var_x Langevin | Lang err  |
|------|----------|---------------|----------|--------|----------------|-----------|
| 0.00 | 0.5000   | 0.5157±0.0074 | +3.1%    | +2.1σ  | 0.515±0.007    | +3.0%     |
| 0.01 | 0.4862   | 0.5027±0.0068 | +3.4%    | +2.4σ  | 0.529±0.008    | +8.8%     |
| 0.05 | 0.4458   | 0.4654±0.0069 | +4.4%    | +2.8σ  | —              | —         |
| 0.10 | 0.4125   | 0.4256±0.0061 | +3.2%    | +2.1σ  | 0.735±0.014    | +78.2%    |
| 0.20 | 0.3700   | 0.4014±0.0050 | +8.5%    | +6.3σ  | —              | —         |
| 0.50 | 0.3058   | 0.3435±0.0040 | +12.3%   | +9.4σ  | —              | —         |
| 1.00 | 0.2571   | 0.3028±0.0038 | +17.8%   | +12.2σ | 2.411±0.043    | +837.8%   |

**Improvement**: ALD reduces error by **11x** at β=0.10 and **47x** at β=1.0 compared to Langevin.

## Order-of-Failure Analysis

β-dependent excess above baseline: Δe(β) = [ALD error(β)] − [ALD error(β=0)]:

| β    | Δe(β)   | Significance    |
|------|---------|-----------------|
| 0.01 | +0.0008 | 0.1σ (noise)    |
| 0.05 | +0.0039 | 0.6σ (noise)    |
| 0.10 | −0.0026 | −0.4σ (noise)   |
| 0.20 | +0.0158 | 3.2σ ★          |
| 0.50 | +0.0220 | 5.5σ ★★         |
| 1.00 | +0.0300 | 8.0σ ★★★        |

**Power-law fit (β = 0.2, 0.5, 1.0):** Δe(β) ≈ 0.030 × β^0.40

- O(β¹) would predict ratio Δe(0.5)/Δe(0.2) = 2.50 → **observed 1.40** (rules out O(β))
- O(β²) would predict ratio = 6.25 → **observed 1.40** (rules out O(β²))
- O(β^0.40) predicts ratio = 1.44 → **1.40 ✓**

## Physical Mechanism: Why Position-Dependent Damping Fixes the O(β) Failure

**Langevin failure:** Constant damping Γ = τω₀² = 0.01 cannot compensate for the ω³ ZPF noise pumping. As β increases the oscillator amplitude, higher-frequency modes are excited, which have larger ZPF density → positive feedback → runaway.

**ALD fix:** Γ_eff(x) = τ(ω₀² + 12βx²). Equilibrium values:

| β    | ⟨Γ_eff⟩ | vs constant Γ=0.01 | Ratio |
|------|---------|---------------------|-------|
| 0.00 | 0.0100  | 0.0100              | 1.00  |
| 0.10 | 0.0151  | 0.0100              | 1.51  |
| 0.50 | 0.0306  | 0.0100              | 3.06  |
| 1.00 | 0.0463  | 0.0100              | 4.63  |

At β=1, the effective damping is 4.6× larger than constant Γ, counteracting the ω³ noise pumping.

**Sign correctness:** ALD gets the direction right:

```
Δvar_x (β=0 → β=1):
  QM:       −0.243  (quartic confinement wins — correct)
  ALD:      −0.213  (88% of slope, correct sign)
  Langevin: +1.896  (wrong sign — noise pumping dominates)
```

## Residual Failure at β > 0.2: NOT a UV Cutoff Artifact [CONFIRMED by E005]

The β^0.40 residual is inconsistent with P&C's O(β²τ) = 0.01 prediction (our observed excess ~0.030 at β=1 is larger). Initial hypothesis was that the finite UV cutoff ω_max=10 was responsible.

**E005 tested this directly (ω_max ∈ {10,20,30}; τ ∈ {0.01,0.005,0.002}):**

- Tripling ω_max (10→30) reduces Δe by only **18%** — power law Δe ~ ω_max^(-0.18), far from the p≥1 expected for a UV artifact
- Quintupling 1/τ (τ: 0.01→0.002) reduces Δe by only **31%** — power law Δe ~ τ^0.23, far from the τ^1 P&C τ-dependence
- The UV cutoff conjecture is **REFUTED**. The error is real in the accessible parameter regime.
- P&C's O(β²) prediction is asymptotically correct, but requires τ < 10^-4 and ω_max > 10^6 — not numerically accessible.

The combined dependence is Δe ~ τ^0.23 × ω_max^(-0.18): extremely slow approach to zero. At τ=0.002 (5× smaller than E004), ALD still overpredicts var_x(β=1) by +15.1%.

## Implications for SED Viability

- The O(β) Langevin failure was an approximation artifact, **not** a fundamental SED failure
- Full ALD agrees with QM for β ≤ 0.1 within statistical noise
- P&C's Pesquera-Claverie claim (SED = QM at O(β)) is approximately supported
- The β^0.40 residual at β > 0.2 is NOT a UV artifact (E005 confirmed) but may require the extreme double limit τ<10^-4, ω_max>10^6 to converge to zero — whether this constitutes an intrinsic SED failure or an asymptotically-correct result in an inaccessible regime remains open

## Normalization Sensitivity of the β-Exponent [E007]

E007 (SED strategy-001, 2026-03-27) tested the same ALD-SED setup with calibrated normalization (var_x(β=0) = 0.500, vs. E004's natural SED normalization var_x(β=0) ≈ 0.516):

- **E004 (natural normalization):** α ≈ 0.40, ratio Δe(0.5)/Δe(0.2) = 1.40
- **E007 (calibrated to 0.500):** α ≈ 0.245, ratio Δe(0.5)/Δe(0.2) = 1.334 ± 0.117

The ratio tests are statistically consistent (within ~0.6σ). The fitted exponents differ by ~60%, primarily because lower baseline energy in E007 changes the absolute Δe magnitudes and shifts the fitted slope. **Both agree that α is well below 1.0 and far below 2.0.**

**Conclusion:** The exact value of α (in the range 0.25–0.40) is normalization-sensitive. When comparing α across explorations, the normalization target must be specified and matched. The qualitative finding (sub-linear power-law residual, positive direction, magnitude ~0.03–0.04 at β=1) is robust.

See `ald-sed-zpf-spectral-sign-reversal.md` for E007's main finding: the ω³ spectrum uniquely produces positive Δe; lower spectral indices produce negative Δe.

## Future Work

1. ~~ω_max = 20 test to diagnose UV cutoff vs. intrinsic failure~~ **DONE (E005): UV cutoff NOT the cause**
2. ~~Test whether the ω³ spectrum specifically drives the positive-direction scaling~~ **DONE (E007): H1 STRONGLY SUPPORTED — sign reversal confirmed, n*≈2.61**
3. τ-dependence: reduce τ to 0.001 or lower (E005 reached τ=0.002; P&C regime requires τ<10^-4)
4. Fine β scan [0.001, 0.01] to measure true O(β) vs O(β²) crossover
5. Compare LL with full Abraham-Lorentz equation (3rd-order ODE, runaway suppression)
6. Full position distribution P(x) comparison and KS statistics
7. Repeat E007 with natural SED normalization (0.516) to determine whether α converges to 0.40

## References

- Pesquera, L. & Claverie, P. (1982). "The quartic anharmonic oscillator in SED." J. Math. Phys. 23(7), 1315-1322.
- SED strategy-001 exploration-004 (2026-03-27): direct numerical verification with LL order reduction.
- See `anharmonic-langevin-o-beta-failure.md` for why constant-damping Langevin fails at O(β).
- See `anharmonic-oscillator-failure.md` for QM reference values and full Langevin failure data.
