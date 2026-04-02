---
topic: Classicality budget in experimentally accessible systems — regime survey
confidence: verified
date: 2026-03-27
source: classicality-budget strategy-002 exploration-003
---

## Summary

Systematic computation of R_max = S_eff/S_T − 1 across 8 experimental systems (using actual thermodynamic entropy S_eff, not the Bekenstein bound). Three systems fall in the "tight" regime (R_max < 10): a short BEC sonic horizon, a sideband-cooled ion trap, and a GaAs nanodot at 4 K. All macroscopic non-gravitational systems are non-constraining. The inflationary Hubble patch is a de Sitter analog of the BH horizon with R_max ≈ −0.979.

**Formula:** R_δ ≤ (S_eff/S_T − 1)/(1−δ)
All results below use δ=0, S_T=1 bit.

---

## 8-System Master Table

| System | S_eff (bits) | R_max | Budget Status |
|--------|-------------|-------|---------------|
| BH horizon (solar mass, Hawking) | 2.67×10⁻³ | −0.997 | FORBIDDEN — inaccessible |
| Inflation (H=10¹³ GeV Hubble patch) | 2.14×10⁻² | −0.979 | FORBIDDEN — inaccessible |
| BEC sonic horizon (L=1 μm, T_eff=50 nK) | 2.98 | **1.98** | TIGHT |
| 20-ion trap (n̄=0.01, 60 modes) | 4.86 | **3.86** | TIGHT |
| GaAs nanodot 10 nm (T=4 K) | 10.25 | **9.25** | TIGHT |
| BEC sonic horizon (L=100 μm, T_eff=50 nK) | 474.9 | 473.9 | CONSTRAINED |
| 50-ion trap (n̄=0.1, 150 modes) | 72.5 | 71.5 | CONSTRAINED |
| Optical fiber soliton (T_eff~10⁴ K, L=1 cm) | 3.03×10⁵ | 3.03×10⁵ | INTERESTING |
| 53-qubit Sycamore QC (15 mK, 25 mm³ Si) | 5.30×10⁹ | 5.30×10⁹ | NOT constraining |
| NEMS resonator (20 mK, 10 MHz, 1 mm³ Si) | 5.02×10⁸ | 7.36×10⁷ | NOT constraining |

**Legend:**
- FORBIDDEN: R_max < 0 (no classical copies possible)
- TIGHT: R_max < 10 (at most ~10 independent copies; experimentally meaningful)
- CONSTRAINED: R_max < 10³ (non-trivially constraining)
- INTERESTING: R_max < 10⁶ (weaker but notable)
- NOT constraining: R_max ≥ 10⁶

---

## Physical Calculations

### BEC Sonic Horizon (Steinhauer 2016/2020)
- Physical setup: Rb-87 BEC with acoustic Hawking temperature T_eff = 50 nK, healing length ξ = 0.5 μm
- 1D phonon modes: N_modes = L/ξ; all 200 modes thermally occupied (λ_th = 0.2 μm < ξ)
- **L = 1 μm: N_modes = 2, S_eff = 2.98 bits, R_max = 1.98 → TIGHT**
- L = 100 μm: N_modes = 200, S_eff = 474.9 bits → CONSTRAINED
- BEC at preparation temperature T_prep = 2 nK: S_eff = 23.1 bits, R_max = 22.1

### 20-Ion Trap
- 20 Ca⁺/Yb⁺ ions, 3N = 60 motional modes, sideband-cooled to n̄
- Entropy per mode = (n̄+1)log₂(n̄+1) − n̄·log₂(n̄)
- **n̄ = 0.01: 0.081 bits/mode, S_eff = 4.86 bits, R_max = 3.86 → TIGHT**
- n̄ = 0.1: 0.483 bits/mode, S_eff = 72.5 bits → CONSTRAINED
- n̄ = 0.001: S_eff = 0.685 bits, R_max = −0.315 → FORBIDDEN

### GaAs Nanodot (10 nm, Debye phonons)
- ~22,000 atoms, V = (10 nm)³, θ_D(GaAs) ≈ 345 K
- **T = 4 K: S_phonon = 10.25 bits, R_max = 9.25 → TIGHT**
- T = 300 K: S_phonon = 4.32×10⁶ bits (not constraining)
- T = 0.1 K: S_phonon = 1.60×10⁻⁴ bits, R_max = −0.9998 → FORBIDDEN

### Google Sycamore (53 qubits, 15 mK)
- Si chip: Debye solid, V = 25 mm³, θ_D(Si) = 645 K
- S_eff = 5.30×10⁹ bits; for 53-bit state: R_max ≈ 10⁸ → NOT constraining
- Substrate has too many phonon modes; would need to restrict to qubits' local coupling volume

### NEMS Resonator (20 mK, 10 MHz)
- n̄ = 41.2 at 20 mK (far from ground state); 1 mm³ Si substrate: S_eff = 5.02×10⁸ bits
- NOT constraining because far from ground state AND large substrate

### Inflationary Hubble Patch (H_inf = 10¹³ GeV)
- R_H = c/H_inf = 1.97×10⁻²⁹ m (sub-nuclear scale); T_dS = 1.85×10²⁵ K
- S_eff(radiation) = 0.0214 bits → R_max = −0.979 **≈ BH result**
- Both BH and inflation are de Sitter-like geometries with Hawking/Unruh radiation; T×r = const applies in both
- Physical interpretation: During GUT-scale inflation, QD redundancy is forbidden. The quantum-to-classical transition of inflaton perturbations must occur via decoherence with superhorizon modes, not QD redundancy. Not directly testable.

---

## The Tight-Budget Bottleneck

**Why macroscopic systems are never tight:** The classicality budget is non-constraining for all macroscopic systems because S_eff >> 1 bit. The budget only becomes tight when the environment has < ~1000 accessible modes. This requires either:
- (a) Engineered cryogenic quantum systems with <100 accessible thermal modes
- (b) Analog BH systems at nanokelvin temperatures with ξ-scale coherence lengths

**Minimum entropy for any classicality:** A classical fact (S_T = 1 bit) requires R_δ ≥ 2 (two independent observers confirming). This requires S_eff ≥ 3 bits (R_max ≥ 2). Achievable with:
- ~10 motional modes with n̄ = 0.1 (3–4 sideband-cooled ions)
- BEC of length L ~ 2 μm at T_H = 50 nK
- 10 nm GaAs dot at T ~ 6 K

These are all experimentally accessible thresholds today.

---

## Status

All values [COMPUTED] from code: `code/experimental_test.py`.
BH horizon value [CHECKED] against prior exploration-005.
Inflation/NEMS/fiber assessments [COMPUTED]; inflation inaccessibility [VERIFIED by geometry].
