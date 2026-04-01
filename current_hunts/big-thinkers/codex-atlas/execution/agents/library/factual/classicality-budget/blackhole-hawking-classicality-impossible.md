---
topic: Black hole Hawking radiation makes classicality impossible near the horizon
confidence: verified
date: 2026-03-27
source: classicality-budget strategy-001 exploration-005
---

## Core Result

Near any black hole horizon — regardless of mass — the Hawking radiation environment has **S_eff = 1/(540 ln2) ≈ 0.003 bits** — effectively zero. The classicality budget via quantum Darwinism is **R_δ < 0 for all fact sizes**. Classical reality (in the QD sense) is impossible near any BH horizon, using Hawking radiation as the environment.

This is the one physical system where the operational classicality budget is genuinely constraining.

**Mass-independence** (from E006): The 0.003-bit result is UNIVERSAL — it holds for any BH mass
from sub-gram to supermassive. This follows from T_H × r_s = ℏc/(4πk_B) = constant, which causes
all mass dependence to cancel. See `blackhole-universal-constants.md` for the full derivation.

---

## Why Hawking Radiation Has Essentially Zero Entropy

**Hawking temperature** for a solar-mass BH (M = M_☉ = 1.99 × 10³⁰ kg):
- T_H = ħc³/(8πGMk_B) = 6.168 × 10⁻⁸ K

**Schwarzschild radius:** r_s = 2.954 × 10³ m = 2.95 km

**Photon wavelength** at temperature T_H:
- λ ~ ħc/(k_BT_H) ≈ 4.2 × 10¹⁰ m = **0.3 AU**

The Hawking photon wavelength (0.3 AU) exceeds the Schwarzschild radius (2.95 km) by **7 orders of magnitude** (λ/r_s ≈ 10^7). There is typically < 10^{-3} of one Hawking photon present in the near-horizon volume (sphere of radius r_s) at any moment.

**Computed:** S_Hawking(V = (4/3)π r_s³) = 2.67 × 10⁻³ bits, average photon count = 5.14 × 10⁻⁴.

---

## The Gap: Accessible vs. Total Entropy

| Quantity | Value |
|----------|-------|
| Bekenstein-Hawking entropy S_BH | 1.514 × 10⁷⁷ bits |
| Hawking photon entropy in near-horizon sphere | 2.67 × 10⁻³ bits |
| Ratio S_Hawking / S_BH | **1.76 × 10⁻⁸⁰** |

The BH has 10⁷⁷ bits of Bekenstein-Hawking entropy, but this is hidden behind the horizon. The only accessible environment is the Hawking radiation — with 80 orders of magnitude less entropy than the BH's total capacity.

---

## Physical Meaning

An observer near a solar-mass BH who relies only on Hawking photons as the QD environment would find the classicality budget is **zero**: there are not enough Hawking photons in the environment to carry even one redundant copy of any classical fact. The Hawking environment cannot support classicalization.

This connects to:
1. **Black hole information paradox**: The Hawking radiation doesn't carry enough information about what fell in. The classicality budget quantifies exactly how far the Hawking environment is from being able to create objective classical facts.
2. **Information scrambling**: The BH interior has 10⁷⁷ bits of encoding capacity, but this is accessible only through Hawking radiation over the BH's entire lifetime (Hawking evaporation time ~2 × 10⁷⁴ years for solar-mass BH). At any given moment, the accessible environment entropy is essentially zero.

---

## Planck-Mass BH: Prior Conjecture DISPROVED (E006)

A prior conjecture in this file suggested that for a Planck-mass BH (M ~ 2 × 10⁻⁸ kg), the
Hawking photon wavelength "becomes comparable to r_s" and the Hawking environment "might have
significant entropy." This conjecture was INCORRECT.

Exploration 006 proved: λ_Hawking = 4π r_s ≈ 12.57 r_s for ALL BH masses, including Planck mass.
The mass independence of T_H × r_s means the photon wavelength is ALWAYS 12.57 times the
Schwarzschild radius — never "comparable" in the sense of fitting inside the near-horizon sphere.

Consequently, S_Hawking = 1/(540 ln2) ≈ 0.003 bits at Planck mass, exactly as for solar-mass BHs.
The Hawking environment NEVER has significant entropy in the near-horizon sphere, regardless of mass.

Note: Quantum gravity effects DO dominate at Planck scale (the budget derivation's axioms do break
down), but this is a separate issue from the entropy — the entropy result is simply universal.

---

## Connection to the Catch-22 (Exploration 004)

Exploration 004 established a catch-22 via the tensor product route: the budget gives interesting predictions (R_δ ~ few) in regimes where the derivation's axioms fail. Exploration 005 provides independent convergent confirmation via operational entropy:

- For macroscopic non-BH systems: operational budget is enormous (10¹⁵ to 10²⁶ bits). Not constraining.
- For BH horizon: operational budget is essentially zero (0.003 bits). Maximally constraining.

These two paths — one through the tensor product failure argument, one through operational entropy computation — independently converge on the same conclusion: the classicality budget is non-trivial only where standard QM fails.
