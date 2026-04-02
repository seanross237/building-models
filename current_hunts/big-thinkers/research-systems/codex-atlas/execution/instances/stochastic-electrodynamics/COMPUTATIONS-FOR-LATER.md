# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## 1. ~~Anharmonic SED Oscillator Simulation~~ DONE (Exploration 003)
- **Result:** SED fails qualitatively — var_x increases with β (opposite to QM). O(β) failure in Langevin approximation. SED/QM ratio = 9.4x at β=1.

## 2. ~~Full Abraham-Lorentz Dynamics Anharmonic Oscillator~~ DONE (Exploration 004)
- **Result:** ALD eliminates O(β) failure. Residual β^0.40 error persists at ~15-18% at β=1. Mechanism: ω³ ZPF feedback confirmed in E007.

## 2a. Critical Spectral Index n* — Find Where Δe Changes Sign (HIGH PRIORITY)
- **What:** Run ALD-SED with n=2.5, 2.75, 3.0 to locate the exact spectral exponent where the Δe error changes sign from negative (undershoot) to positive (overshoot). E007 showed n=2→undershoot, n=3→overshoot, crossover at n*≈2.61.
- **Why it matters:** If n*=3 exactly, the physical ZPF is at the stability boundary — a profound result. If n*≈2.6, the ZPF is safely above the boundary. Either way, quantifying n* gives a precise characterization of WHY SED fails.
- **Source:** Exploration 007; n*≈2.61 from linear interpolation.
- **Difficulty:** Low (reuse E007 code, add n=2.5, 2.75).
- **Specific equation:** Same ALD code, change S(ω) ∝ ω^n for non-integer n.

## 2b. α Discrepancy Resolution — Physical Normalization for n=3 (MEDIUM PRIORITY)
- **What:** E004 found α≈0.40 for ALD residual; E007 found α≈0.25 for n=3. Difference is normalization: E004 used physical SED (var_x_0=0.516); E007 calibrated to var_x_0=0.500. Need to run E007 n=3 with E004's physical normalization to resolve.
- **Source:** Explorations 004, 007.
- **Difficulty:** Very low (one re-run with different normalization).


## 3. ~~SED Tunneling Rate~~ DONE (Strategy-002 Exploration 001)
- **Result:** First numerical SED double-well simulation. Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf). At λ=0.25 (S_WKB≈1.41≈V_barrier/E_zpf): ratio=1.15 (15% agreement). At λ=0.10 (S_WKB=6.29, V_barrier/E_zpf=3.52): ratio=18.5 (18× overestimate).
- **New formula identified:** Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf) [CONJECTURED from 2 data points]

## 5. SED Tunneling Crossover — Verify Formula with More λ Values (HIGH PRIORITY)
- **What:** The formula Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf) was measured at only 2 λ values (0.25 and 0.10). Extend to λ=0.05, 0.15, 0.50 to verify the formula and determine if it's exact or approximate.
- **Why it matters:** If confirmed, this is a novel quantitative prediction for when SED accidentally mimics quantum tunneling.
- **Source:** Strategy-002 Exploration 001; Faria & Franca (2005) (analytical, no numerical comparison).
- **Difficulty:** Low (reuse E001 code, change λ).

## 6. ~~SED Coupled Oscillators — 3D Multi-Mode ZPF~~ DONE (Strategy-003 Exploration 003)
- **Result:** C_xx(d) = j₀(q) − j₂(q)/2 = (3/2q³)[(q²−1)sin(q) + q cos(q)] where q = ω₀d/c. Non-zero at all finite d; decays as ~(3/2)sin(q)/q for large q. NOT van der Waals r⁻⁶. SED-QM discrepancy persists in 3D but weakens from constant-amplitude to 1/d decay. Verified analytically + Monte Carlo (N=500k modes) to machine precision.

## 7. ~~SED Hydrogen — Physical τ and Extended Runs~~ DONE (Strategy-003 Exploration 002)
- **Result:** Physical τ = 2.591×10⁻⁷ a.u. T_ion(L) table: L=0.5 → 448 periods, L=1.0 → 19,223 periods (18/20 ionized in 50k). Power law T_ion ≈ 37,527 × L^6.44. ⟨r⟩(L=1.0) = 1.509 a₀ ≈ QM 1s. Scaling is non-linear in τ (26-89× longer, not 60×).

## 8. Fokker-Planck Perturbation Theory for SED at O(β) (MEDIUM PRIORITY)
- **What:** Compute d⟨x²⟩_SED/dβ at β=0 analytically from the classical Fokker-Planck equation with ω³ noise spectrum. If this gives −3/2 (same as QM first-order perturbation theory result), it independently confirms SED = O(ħ) QED at O(β), and makes the Santos framework prediction testable without simulation.
- **Why it matters:** Would provide the first purely analytic prediction from Santos' framework, establishing it as more than a classification scheme.
- **Source:** Strategy-003 Exploration 001. See Section 6 of that report.
- **Difficulty:** Medium (~20-line calculation solving linear Fokker-Planck in frequency domain).
- **Specific equations:** FP equation for ω³ Langevin; Schrödinger perturbation theory: d⟨x²⟩_QM/dβ|_{β=0} = −3/2.

## 9. Slope Convergence Test — Confirm slope=1.049 is Finite-ω_max Artifact (MEDIUM PRIORITY)
- **What:** Run ALD tunneling simulation at λ=0.1 (deep barrier) for ω_max = 10, 20, 50, 100 (4 values). Plot slope vs 1/ω_max. If slope → 1.000 linearly, confirms the artifact hypothesis from E001.
- **Why it matters:** Would close the open question of whether slope=1.049 is fundamental physics or a UV artifact. Current evidence points to artifact, but a convergence test would confirm definitively.
- **Source:** Strategy-003 Exploration 001, Section 3.5.
- **Difficulty:** Low (reuse existing Strategy-002 tunneling code; change ω_max).
- **Specific equations:** ALD with ZPF spectrum S(ω) = 2τω³, ω_max varied.

## 4. ~~Full Anharmonic Probability Distribution~~ DONE (Exploration 003)
- **Result:** SED is super-Gaussian, QM is sub-Gaussian. KS p=0.000 at β=0.1. Shapes differ qualitatively.

