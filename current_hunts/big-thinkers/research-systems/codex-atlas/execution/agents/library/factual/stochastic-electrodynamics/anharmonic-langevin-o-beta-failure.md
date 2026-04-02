---
topic: Langevin approximation fails at O(beta) for anharmonic SED — one order worse than full ALD
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-003"
---

## Key Finding

The Langevin approximation (constant damping Γ = tau*omega_0^2) fails at **O(beta)** for the SED anharmonic oscillator. This is **one order earlier** than Pesquera & Claverie (1982) proved for the full Abraham-Lorentz-Dirac (ALD) equation, which fails at O(beta^2).

**Practical implication:** Most SED calculations in the literature use the Langevin approximation. These calculations are wrong at O(beta) for any anharmonic potential — not merely at O(beta^2).

## Physical Mechanism

The O(beta) failure arises from a positive feedback loop that the Langevin approximation cannot track:

1. Beta > 0 shifts the effective resonance frequency: omega_eff = sqrt(1 + 12*beta*var_x) > omega_0
2. ZPF input power scales as omega_eff^3: S_F(omega_eff) ∝ omega_eff^3 > S_F(omega_0)
3. The Langevin damping is held constant: Γ = tau*omega_0^2 (doesn't increase with omega_eff)
4. Net: input power grows as omega_eff^3, dissipation is fixed → oscillator is pumped to larger amplitude
5. Larger var_x → higher omega_eff → back to step 1

QM does not exhibit this feedback because energy quantization controls level populations; the ω³ ZPF density does not drive the wavefunction to larger amplitudes.

## Quantitative Evidence

Adjusted discrepancy / beta is approximately constant at small beta, indicating O(beta) dependence:

| beta  | Adjusted excess (above beta=0 baseline) | Adj/beta |
|-------|------------------------------------------|----------|
| 0.010 | +5.8%                                    | 5.80     |
| 0.050 | +33.7%                                   | 6.74     |
| 0.100 | +75.2%                                   | 7.51     |
| 0.200 | +177.0%                                  | 8.85     |

Ratio Adj/beta ≈ 6–9 (roughly constant). This is the O(beta) scaling signature.

## Why P-C Got O(beta^2) for Full ALD

In the full ALD equation, the radiation reaction force is frequency-dependent: Γ(omega) = tau*omega^2. When the effective resonance shifts to omega_eff, the damping also adjusts upward. This partially cancels the input power increase, moving the leading failure to O(beta^2). The Langevin approximation freezes the damping at omega_0, so no cancellation occurs, and failure manifests at O(beta).

## Framing Note (E006 adversarial review)

This is an **approximation failure**, NOT a fundamental SED failure. The Langevin approximation (constant Γ = τω₀²) is a simplification of the exact Abraham-Lorentz-Dirac equation. Using a constant-Γ approximation for a system with nonlinear forces and discovering it fails is — in retrospect — expected for a careful physicist: P&C (1982) used full ALD from the start precisely because they knew the constant-Γ Langevin couldn't track position-dependent damping.

**Correct framing:** "The Langevin approximation of SED fails at O(β) for the anharmonic oscillator; full ALD (Landau-Lifshitz order reduction) eliminates this O(β) failure." Do NOT frame as "SED fails at O(β)."

The discovery value is in the quantitative demonstration and the positive-feedback mechanism (ω³ noise × fixed Γ → pumping) — which makes the failure mode concrete and warns practitioners who use Langevin for nonlinear SED systems.

## Context

- Full anharmonic failure data: see `anharmonic-oscillator-failure.md`
- The O(beta) failure means the linearity boundary is at beta > ~0.005 in practice (not the P-C O(beta^2) boundary that would be ~0.005^(1/2) ~ 0.07)
- **UPDATE (exploration-004):** This O(beta) failure is an **approximation artifact**. Full ALD with Landau-Lifshitz order reduction eliminates the O(beta) excess for beta ≤ 0.1. ALD reduces the beta=1 error from 838% (Langevin) to 18%, and gets the sign of var_x change correct. See `anharmonic-ald-landau-lifshitz.md`.
