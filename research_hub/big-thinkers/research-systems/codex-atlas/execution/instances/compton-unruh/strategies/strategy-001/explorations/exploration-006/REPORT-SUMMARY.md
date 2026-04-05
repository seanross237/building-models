# Exploration 006 — Summary

## Goal
Two tasks: (1) Investigate whether the FDT in de Sitter provides a first-principles derivation of m_i = m × T_U/T_dS. (2) Test the ratio model against NGC 3198 and NGC 2403 rotation curves.

## What Was Tried

**Part 1 (FDT):**
- Computed the classical FDT dissipative susceptibility χ''(ω) in both Rindler and de Sitter
- Analyzed the quantum FDT (mass renormalization)
- Explored the effective damping coefficient ratio γ_dS/γ_flat
- Considered the temperature-mismatch Langevin scenario (non-equilibrium)
- Scripts: `code/fdt_analysis.py`

**Part 2 (Rotation Curves):**
- NGC 3198: stellar+gas disk fit (total baryonic 3.2×10¹⁰ Msun, BTFR-consistent)
- NGC 2403: corrected to include HI gas (total baryonic ~1.85×10¹⁰ Msun)
- Chi-squared scans over a₀ for both galaxies
- Compared: Newton, MOND (a₀=1.2e-10), Verlinde (cH₀/6=1.13e-10), cH₀ (6.8e-10), best-fit
- Scripts: `code/rotation_curves_corrected.py`, `code/ngc2403_masscheck.py`

## Outcome: NEGATIVE on FDT, POSITIVE on Verlinde model

**FDT result (negative):** The standard classical FDT gives χ''_dS/χ''_flat = 1.000000 exactly. The enhanced de Sitter noise (S_dS > S_flat) is canceled by the higher temperature in the FDT denominator. Quantum FDT: mass renormalization is T-independent. Neither classical nor quantum FDT gives m_i = m×T_U/T_dS. The damping coefficient goes the wrong way: γ_dS > γ_flat (more damping, not less effective inertia). The only route to the ratio formula is an ad hoc "thermodynamic inertia" definition that reinterprets kinetic energy using T_U rather than T_dS — this IS the ratio ansatz in disguise, not a derivation.

**Galaxy fits (positive for Verlinde):**
- NGC 3198: MOND χ²/dof=1.34, Verlinde χ²/dof=1.21, cH₀ χ²/dof=132
- NGC 2403: MOND χ²/dof=0.88, Verlinde χ²/dof=0.52, cH₀ χ²/dof=140
- Best-fit a₀: 0.74–0.93 × a₀_MOND for both galaxies
- cH₀ model decisively ruled out; Verlinde (cH₀/6) fits as well as MOND

## Verification Scorecard
- **VERIFIED**: 0
- **COMPUTED**: 11 (temperature formulas, χ''/ratio=1, damping sign, rotation curves×2 galaxies×4 models, BTFR, chi2/dof, best-fit a₀, MOND-regime fractions)
- **CHECKED**: 0
- **CONJECTURED**: 3 (quantum mass renormalization T-independence, non-equilibrium Langevin interpretation, connection to Verlinde derivation)

## Key Takeaway
The FDT route to m_i = m×T_U/T_dS is CLOSED by a robust negative result: χ''_dS = χ''_flat exactly, so the FDT produces no modification to inertia. The sign problem (de Sitter adds more damping, not less) is confirmed. Galaxy fits confirm the predicted a₀ = cH₀ is 5.7× too large; cH₀/6 (Verlinde's elastic entropy factor) fits both galaxies at χ²/dof ~ 1. The ratio model with Verlinde's correction is observationally indistinguishable from MOND.

## Proof Gaps Identified
- The non-equilibrium Langevin scenario gives the ratio formula, but requires γ ~ T_U (not T_dS). No calculation establishes this hierarchy — it would need to show that the Rindler horizon couples to a DIFFERENT mode of the vacuum than the de Sitter ambient bath.
- The Verlinde "elastic entropy" derivation gets a₀ = cH₀/(2π) ≈ cH₀/6.3, but the physical connection between entropy elasticity and the ratio formula T_U/T_dS has not been established.

## Leads Worth Pursuing
1. **Verlinde-FDT connection**: Does Verlinde's elastic entropy play the role of the dissipation kernel in the FDT? If S_elastic ~ γ, and S_elastic scales with T_U (not T_dS), this could provide the missing link.
2. **Quantum information route**: T_U/T_dS might equal the quantum purity of the Rindler reduced density matrix in the de Sitter vacuum. If inertia is tied to purity, the ratio formula follows.
3. **DeWitt-Brehme self-force in de Sitter**: The scalar radiation reaction force in de Sitter space has curvature corrections. Computing the full ALD force for constant acceleration might give a mass correction that scales differently than T_dS.

## Unexpected Findings
- The NGC 2403 initial fit (stellar disk only) accidentally gave chi2/dof(cH₀) = 0.56 while MOND got 65 — a cautionary result showing that mass modeling is crucial and that the ratio model should NOT be compared without consistent baryonic mass accounting.
- With proper baryonic masses (BTFR-consistent), BOTH galaxies show the same pattern: cH₀ fails by factor ~100 in χ², Verlinde matches MOND.
