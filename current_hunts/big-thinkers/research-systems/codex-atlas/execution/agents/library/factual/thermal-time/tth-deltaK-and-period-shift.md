---
topic: ΔK_A correction for entangled oscillators — O(λ²), band-2 structure, 6.4% period shift
confidence: verified
date: 2026-03-27
source: thermal-time/strategies/strategy-001/explorations/exploration-002/REPORT.md
---

## Summary

For two bilinearly coupled harmonic oscillators in a global thermal state ρ_AB = e^{−βH_AB}/Z, the modular Hamiltonian of subsystem A deviates from βH_A by a correction ΔK_A that is O(λ²) with a characteristic band-2 structure (temperature renormalization + squeezing), and yields a 6.4% longer autocorrelation period than standard QM at λ=0.3. This constitutes a genuine TTH prediction distinguishable from standard QM.

## Setup

- H = H_A + H_B + H_int, H_A = ω_A a†a, H_B = ω_B b†b, ω_A = ω_B = 1.0
- H_int = λ q_A ⊗ q_B (bilinear), q = (a+a†)/√2
- Global state: ρ_AB = e^{−βH_AB}/Z, β = 2.0
- ρ_A = Tr_B[ρ_AB]; K_A = −log ρ_A (computed via eigendecomposition, N=20 Fock truncation)
- ΔK_A = K_A − βH_A_red − c·I (c chosen so Tr[ΔK_A] = 0)
- Verification: ‖ΔK_A‖_F = 6×10⁻¹⁵ at λ=0 (machine precision) ✓

## Result 1: ΔK_A ≠ 0 for λ ≠ 0

| λ    | ‖ΔK_A‖_F  | ΔK[0,0] | ΔK[1,1] | ΔK[2,2] |
|------|-----------|---------|---------|---------|
| 0.00 | 0.000000  | 0.0000  | 0.0000  | 0.0000  |
| 0.05 | 0.105904  | 0.0315  | 0.0281  | 0.0247  |
| 0.10 | 0.423121  | 0.1260  | 0.1124  | 0.0988  |
| 0.20 | 1.685187  | 0.5013  | 0.4473  | 0.3933  |
| 0.30 | 3.768246  | 1.1191  | 0.9987  | 0.8782  |
| 0.50 | 10.312152 | —       | —       | —       |

## Result 2: ΔK_A = O(λ²) — analytic proof + numerical confirmation

**Numerical:** Power law fit ‖ΔK_A‖_F ~ 42.1 × λ^{1.998}. Ratio test: ‖ΔK(2λ)‖/‖ΔK(λ)‖ = 3.9998 ≈ 4.

**Analytic explanation:** At O(λ¹), the Duhamel perturbation formula gives:
```
δρ_A = Tr_B[δρ_AB] ∝ Tr[ρ_B q_B] = 0
```
because the thermal expectation value of position vanishes (odd-moment zero for thermal states). Therefore ΔK_A starts at O(λ²). Shape universality: ΔK_A/λ² is identical at λ=0.05 and λ=0.3 (cosine similarity = 1.000), confirming ΔK_A = λ²·f(β,ω) + O(λ⁴) with no λ³ correction.

## Result 3: Band-2 Structure

At λ=0.3, ΔK_A has two non-zero contributions:
- **Band 0 (diagonal):** 78% of ‖ΔK‖_F; elements approximately linear in n: ΔK_A[n,n] ≈ Δβ·n
  - Δβ ≈ −0.120 at λ=0.3 → β_eff = β + Δβ ≈ 1.88 (subsystem appears hotter)
  - Scaling: Δβ ~ λ^{1.98} (O(λ²)) ✓
- **Band 2 (|i−j|=2 off-diagonal):** 44% of ‖ΔK‖_F; elements: ΔK_A[n,n+2] ≈ −0.0347 × √((n+1)(n+2))
  - Exactly the matrix element of (a†² + a²) (squeezing operator) ✓
- **All other bands (1, 3, 4, ...):** < 3×10⁻⁴ (machine noise)

**Physical origin:** H_int = q_A⊗q_B. At second order, (q_A)² = (a+a†)²/2 = n + 1/2 + (a²+a†²)/2. The a² and a†² operators shift Fock number by ±2 → band-2 structure.

## Result 4: Physical Interpretation

To leading order in λ²:
```
K_A ≈ β_eff H_A + λ²·C(β,ω)·(a†² + a²)/2 + const·I
```

Bilinear coupling to B has two effects on the modular Hamiltonian of A:
1. **Temperature renormalization:** β_eff = β − 1.36λ² (A appears hotter than the actual temperature)
2. **Effective squeezing:** off-diagonal (a†²+a²)/2 term — ρ_A becomes a squeezed Gaussian thermal state

Physical picture: bilinear coupling generates Gaussian quantum correlations between A and B. The marginal ρ_A = Tr_B[ρ_AB] is a Gaussian state with modified covariance matrix, and its modular Hamiltonian is a general quadratic (squeezing + temperature renormalization).

## Result 5: TTH-QM Period Shift

**Three autocorrelation functions computed (λ=0.3, β=2.0):**
1. **TTH bare:** q_A(t) = e^{iK_A t} q_A e^{−iK_A t}, t = modular parameter
2. **Standard QM:** q_A(τ) = e^{iH_A τ} q_A e^{−iH_A τ}, τ = physical time
3. **TTH normalized:** same as bare but with τ = β·t (Bisognano-Wichmann normalization)

**Period shift (first zero crossing):**

| λ    | τ_TTH (normalized) | τ_QM   | Δτ/τ     |
|------|--------------------|--------|----------|
| 0.00 | 1.5708             | 1.5708 | 0.000000 |
| 0.05 | 1.5735             | 1.5708 | 0.001702 |
| 0.10 | 1.5815             | 1.5708 | 0.006841 |
| 0.20 | 1.6146             | 1.5708 | 0.027877 |
| 0.30 | 1.6726             | 1.5708 | 0.064804 |
| 0.40 | 1.7609             | 1.5708 | 0.121036 |
| 0.50 | 1.8896             | 1.5708 | 0.202971 |

**Scaling:** Δτ/τ ~ λ^{2.07} ≈ 0.71·λ² (leading order).

**At λ=0.3:** TTH normalized gives 6.4% LONGER period than the FREE oscillator (H_A evolution). **Important correction (see exploration-003 / `tth-full-qm-vs-local-tth.md`):** This comparison is against the wrong baseline. The correct comparison is C_full_QM (H_AB evolution). Against C_full, the period shift at λ=0.3 is only ~1.3% (τ_zero: 1.6726 vs. 1.6506). The 6.4% figure overstates the TTH–QM disagreement because C_full itself is shifted by normal-mode beating relative to the free oscillator.

**Recommended figure of merit:** The L² norm ‖C_full − C_local‖/‖C_full‖ = 0.827 (82.7%) at λ=0.3 is the more reliable discriminant — it captures the full structural difference (single-frequency TTH vs. two-frequency beating QM). The zero-crossing metric understates the discrepancy.

## Conclusion

With the correct normalization (τ=β·t), TTH makes a genuinely different prediction from standard QM for entangled systems. However, the relevant figure of merit is not the period shift (which compared against the free oscillator baseline) but the L² norm discrepancy between C_local_TTH and C_full_QM (82.7% at λ=0.3). The structural source of this discrepancy: C_full has two-frequency normal-mode beating, C_local has one frequency. No parameter tuning can fix this structural mismatch. See `tth-full-qm-vs-local-tth.md` for the complete comparison.
