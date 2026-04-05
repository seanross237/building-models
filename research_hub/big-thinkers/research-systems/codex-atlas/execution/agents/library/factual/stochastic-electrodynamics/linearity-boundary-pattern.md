---
topic: SED linearity boundary
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-002 (synthesis of full landscape survey)"
---

## The Pattern

SED succeeds when and only when:
1. The system is **linear** (harmonic oscillator or free field)
2. The calculation involves only **equilibrium properties** (ground state, not excited states)
3. No **quantum coherence** or **interference** is involved

Every extension to nonlinear potentials, excited states, or interference phenomena has failed.

## Complete Scorecard

| System | Status | Reference |
|--------|--------|-----------|
| Harmonic oscillator ground state | SED = QM | Marshall 1963, Boyer 1975 |
| Casimir effect | SED = QM | Boyer 1973 |
| Van der Waals forces | SED = QM | Boyer 1973 |
| Blackbody spectrum | SED = QM | Boyer 1969, Marshall 1965 |
| Diamagnetism | SED = QM | (follows from HO) |
| Specific heats | SED = QM | (follows from HO) |
| **Anharmonic oscillator** | SED != QM at O(beta^2) full ALD; O(beta) with Langevin approx | Pesquera & Claverie 1982; E003-E004 |
| **Hydrogen atom** | Self-ionizes | Nieuwenhuizen & Liska 2015, Nieuwenhuizen 2020 |
| **Quantum coherence** | No interference | Huang & Batelaan 2019 |
| **Excited states** | No discrete spectrum | Boyer 2019 review |
| Bell inequality violation | Contested | Marshall & Santos, Santos 2020 |
| g-2 anomalous moment | SEDS claims (non-standard) | Cavalleri et al. 2010 |
| Lamb shift | Partial results | Boyer 1988, Cavalleri et al. |
| Tunneling | Not computed | -- |

## No Discrete Excited States

The SED harmonic oscillator has only one equilibrium state (the ground state). It has no discrete excited states -- the QM levels E_n = (n + 1/2) hbar omega have no natural SED counterpart. Boyer (2019) notes that after pulse excitation, the energy distribution shows peaks near QM levels, but these are transient non-equilibrium features, not true eigenstates.

## Novelty Assessment (E006 adversarial review)

The **concept** of this boundary is NOT novel. It has been well-known since Boyer (1975) and is explicitly stated in Boyer (2019), Atoms 7(1):29: "SED gives predictions agreeing with QM for linear systems (Hamiltonians quadratic in positions and momenta), but not for nonlinear systems." Claverie, Diner, and others noted this in the 1970s-1980s.

**What IS new in E002-E004's treatment:**
- The label "linearity boundary" (new terminology)
- The systematic enumeration (4+3 successes + 6 failure categories by type)
- The specific numerical quantification (threshold β > 0.005 for Langevin approximation)
- The first time-domain numerical confirmation of the anharmonic failure

**Present as:** "confirming and quantifying a well-known pattern" — not a new discovery.

## Santos (2022) Theoretical Grounding

**Santos, E. (2022), Eur. Phys. J. Plus. arXiv:2212.03077** provides the most precise characterization of this linearity boundary in the Weyl-Wigner representation:

> **SED = first-order-in-ħ approximation to QED.**

- For **quadratic Hamiltonians** (harmonic oscillator, Casimir, van der Waals): the first-order-ħ approximation is exact — all higher Wigner distribution corrections vanish. SED = QM.
- For **nonlinear Hamiltonians**: second-order and higher ħ corrections are non-zero, and SED misses them entirely. SED ≠ QM.

This provides the exact mathematical reason for the linearity boundary: it is the boundary between the O(ħ¹) and O(ħ²) regimes of QED. The failures cannot be corrected within a classical framework because fixing them would require including ħ² corrections. See `sed-omega3-feedback-mechanism.md` for the dynamical consequences.

## Open Computations Status (as of March 2026)

- **Numerical anharmonic oscillator:** CONFIRMED (strategy-001 E003/E004/E005). Failure is O(β) for Langevin; ALD/LL eliminates O(β) for β ≤ 0.1; residual β^0.40 NOT a UV artifact. See `anharmonic-ald-landau-lifshitz.md` and `uv-cutoff-parameter-scan.md`.
- **Tunneling / barrier penetration:** COMPUTED (strategy-002 E001). **SED matches QM to 15% for moderate barriers (S_WKB ≈ 1.4, λ=0.25) but overestimates by 18× for deep barriers (S_WKB ≈ 6.3, λ=0.1).** Mechanism: ZPF-driven over-barrier crossings, NOT quantum tunneling. See `sed-double-well-tunneling.md`.
- **Compton scattering:** Requires fully relativistic SED, extremely challenging. Not tractable.
