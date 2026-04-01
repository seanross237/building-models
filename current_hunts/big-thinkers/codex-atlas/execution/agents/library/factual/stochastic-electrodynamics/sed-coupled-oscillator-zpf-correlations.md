---
topic: SED two-oscillator ZPF correlations — C_xx(d) = cos(ω₀d/c) and comparison to QM
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-002"
---

## Key Result

Two harmonic oscillators sharing a common 1D plane-wave ZPF realization develop position-position correlations **C_xx(d) = cos(ω₀d/c)**, while QM predicts **C_xx = 0** for uncoupled oscillators in a product ground state. This is a clean, analytically derived, numerically confirmed SED-QM discrepancy for a two-oscillator system.

The individual oscillator statistics (var_x ≈ ℏ/(2mω₀) = 0.5) agree with QM — this is the established SED success for linear oscillators. The failure is specifically in the two-point correlation.

## Analytical Derivation

For oscillator 2 at separation d from oscillator 1, the ZPF force is phase-shifted in the frequency domain:
F₂(ω) = F₁(ω) × e^{iωd/c}

The normalized position-position correlation is:

```
C_xx(d) = ∫₀^∞ |χ(ω)|² cos(ωd/c) S_F(ω) dω
          ─────────────────────────────────────────
          ∫₀^∞ |χ(ω)|² S_F(ω) dω
```

where χ(ω) = 1/(m(ω₀² − ω² − iγω)) is the susceptibility and γ = τω₀². For narrow linewidth (γ/ω₀ = τω₀ ≪ 1), spectral weight concentrates at ω ≈ ω₀:

**C_xx(d) ≈ cos(ω₀d/c) × exp(−τω₀²d/(2c)) ≈ cos(ω₀d/c)**

The exponential damping is negligible for τ = 0.001 at all separations tested.

## Numerical Confirmation

Parameters: ω₀=1.0, τ=0.001, ω_max=10.0, dt=0.05, N=100,000 steps, N_traj=200, c=1.0.

| d (c/ω₀) | C_xx (sim) | C_xx (analytic) | cos(ω₀d/c) | QM |
|----------|------------|-----------------|------------|-----|
| 0.0      | 1.0000     | 1.0000          | 1.000      | 0   |
| 0.1      | 0.9948     | 0.9949          | 0.9950     | 0   |
| 1.0      | 0.5384     | 0.5386          | 0.5400     | 0   |
| 10.0     | −0.8328    | −0.8334         | −0.8391    | 0   |

**Simulation vs. analytical: < 0.2% relative error at all separations.** [CHECKED]

Individual variances: var_x ≈ 0.485–0.507 across all d, consistent with QM prediction 0.500. ✓

## Momentum-Momentum Correlation

C_pp(d) mirrors C_xx(d): C_pp ≈ 0.99 (d=0.1), 0.52 (d=1.0), −0.80 (d=10.0). The same phase-shift argument applies to momenta.

**Caveat:** var_p is UV-cutoff dependent (∫ω² dω diverges without cutoff). C_pp values should not be directly compared to QM.

## SED vs QM Comparison

| Observable       | QM (vacuum, uncoupled) | SED (shared 1D ZPF)      |
|------------------|------------------------|--------------------------|
| var_x            | ℏ/(2mω₀) = 0.5        | ≈ 0.5 ✓                  |
| ⟨x₁x₂⟩         | 0                      | 0.5 cos(ω₀d/c) ≠ 0      |
| C_xx(d)          | 0                      | cos(ω₀d/c)               |
| Bell S (CHSH)    | ≤ 2 (separable state)  | ≤ 2 ✓ (see entanglement-bell-contested.md) |

## Caveats and Scope

**1D vs 3D:** This is a 1D plane-wave ZPF model. The 3D result is now computed in `sed-3d-zpf-correlator.md` (strategy-003 E003): C_xx(d) = j₀(q) − (1/2)j₂(q), which decays as ~(3/2)sin(q)/q for large d (1/d envelope, oscillating but never zero for finite d). The 3D orientational average reduces but does not eliminate the SED-QM discrepancy.

**Not van der Waals:** C_xx(d) from shared ZPF (zeroth order in inter-oscillator coupling) is distinct from van der Waals correlations (second order in Coulomb coupling, ~r⁻⁶ falloff). Boyer (1972) showed SED reproduces van der Waals exactly; that is a different mechanism.

**Boyer (2018) non-locality:** Boyer explicitly states that SED is a non-local hidden-variable theory — "random radiation phases distributed throughout space act as non-local hidden variables." The correlations C_xx are a consequence of this non-locality, not a violation of it.

## Testable Prediction

If C_xx were measurable for two oscillators sharing a vacuum ZPF, SED would predict non-zero oscillating correlation C_xx(d) = cos(ω₀d/c); QM predicts zero for uncoupled oscillators in a product state. This is in principle a discriminating experiment, though no practical realization has been proposed.
