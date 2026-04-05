---
topic: Standard FDT gives no inertia modification in de Sitter — sign problem confirmed in damping
confidence: provisional
date: 2026-03-27
source: "compton-unruh strategy-001 exploration-006"
---

## Finding

The standard (classical and quantum) Fluctuation-Dissipation Theorem (FDT) gives **NO modification
to inertial mass** when a particle moves in de Sitter spacetime. The dissipative susceptibility χ'' is
temperature-independent for an Ohmic bath, giving χ''_dS = χ''_flat exactly. The sign problem from
exploration-004 (naive entropic gives anti-MOND) is confirmed in the FDT: de Sitter adds MORE damping,
not less. The only route to the ratio formula via Langevin dynamics is non-equilibrium and self-referential.

## Classical FDT Result [COMPUTED]

Kubo FDT for a Brownian particle in a thermal bath at temperature T:

    χ''(ω) = ω × S(ω) / (2k_BT)

For a KMS thermal state, S(ω) ~ k_BT/ℏ in the classical (low-frequency) limit.

**In flat Rindler (T = T_U):**

    S_flat(ω) ~ k_BT_U/ℏ
    χ''_flat(ω) = ω × S_flat / (2k_BT_U) = ω/(2ℏ)   [T-independent]

**In de Sitter (T = T_dS):**

    S_dS(ω) = (T_dS/T_U) × S_flat(ω)    [enhanced noise from higher T]
    χ''_dS(ω) = ω × S_dS / (2k_BT_dS) = ω/(2ℏ)   [SAME as flat]

**Result:** χ''_dS / χ''_flat = 1.000000. The enhanced noise from T_dS > T_U is exactly canceled by
the higher temperature in the FDT denominator. **Standard FDT gives no modification to inertia.**

## Quantum FDT [CONJECTURED]

Full quantum FDT: χ''(ω) = (S(ω)/2ℏ) × tanh(ℏω/(2k_BT)). For an Ohmic spectral density J(ω) = ηω,
mass renormalization δm = (q²/π) ∫ J(ω)/ω² dω is T-independent (UV-divergent, requires
renormalization). **Temperature affects only the noise, not the mass.** [CONJECTURED based on
Caldeira-Leggett theory]

## Sign Problem Confirmed in Damping [COMPUTED]

The effective damping coefficient γ ∝ T:

    γ_flat ~ T_U
    γ_dS   ~ T_dS
    γ_dS / γ_flat = T_dS/T_U = 1/μ > 1

De Sitter has **MORE damping** than flat space (γ_dS > γ_flat). The ratio formula requires LESS
effective resistance (m_i = m × T_U/T_dS < m). This is the **WRONG direction**. The sign problem from
exploration-004 (naive entropic force gives anti-MOND) is independently confirmed in the FDT context:
both approaches show de Sitter adds more fluctuations and more damping, not less inertia.

## The Non-Equilibrium Route [CONJECTURED — Self-Circular]

The only plausible Langevin route to the ratio formula requires a non-equilibrium setup:
- Dissipation γ set by T_U (acceleration horizon coupling)
- Noise from the full de Sitter vacuum at T_dS (not T_U)

This system is NOT in thermal equilibrium (violates standard FDT). The steady-state:

    ⟨v²⟩_dS = k_B T_dS / m   [equipartition at T_dS]

Define "thermodynamic inertia" via Unruh energy (E_U = ½k_BT_U) vs. kinetic energy (½k_BT_dS):

    m_i = m × T_U/T_dS = m × μ_MOND(a/cH₀)

**However:** This amounts to DEFINING inertia via the Unruh energy scale, which is precisely the ratio
ansatz in disguise. There is no derivation establishing that γ ~ T_U (rather than T_dS) in de Sitter.
The assumption requires privileging the Rindler-horizon coupling over the full de Sitter ambient bath,
which is physically motivated but unproven. [CONJECTURED]

## Updated Status: Path to Rigor

The standard FDT route (option 3 in `desitter-force-mechanisms-assessment.md`) is now **tested negative**.
The non-equilibrium Langevin approach is self-referential. The most promising remaining routes are:

1. **Non-equilibrium horizon coupling**: Prove from first principles that the Rindler horizon
   specifically controls dissipation (γ ~ T_U) while the full de Sitter bath controls noise. Requires
   distinguishing horizon coupling from ambient bath coupling — a calculation not yet done.

2. **Verlinde elastic entropy → FDT connection**: If Verlinde's 2016 derivation (which does give
   a₀ = cH₀/6) can be connected to a fluctuation-dissipation relation via entropy elasticity = damping,
   this would provide the missing factor and a physical mechanism.

3. **Quantum information**: T_U/T_dS as the quantum purity of the Rindler-wedge reduced state in the
   de Sitter vacuum; if inertia connects to entanglement structure, this could provide a derivation.
