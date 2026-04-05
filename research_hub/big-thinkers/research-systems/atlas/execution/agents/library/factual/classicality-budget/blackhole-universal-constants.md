---
topic: Universal dimensionless constants for Hawking radiation near any black hole
confidence: verified
date: 2026-03-27
source: classicality-budget strategy-001 exploration-006; strategy-002 exploration-002
---

## Core Result

The Hawking radiation properties inside the near-horizon sphere (radius r_s) are **universal
dimensionless constants** — independent of black hole mass. All fundamental constants (ℏ, c, G, k_B)
cancel completely. This follows from the universal identity T_H × r_s = ℏc/(4πk_B).

---

## The Key Identity

**T_H × r_s = ℏc/(4πk_B) ≈ 1.822 × 10⁻⁴ m·K   [universal, for any BH mass]**

Proof:
- T_H = ℏc³/(8πGMk_B)
- r_s = 2GM/c²
- T_H × r_s = [ℏc³/(8πGMk_B)] × [2GM/c²] = ℏc/(4πk_B)   ✓ (M cancels)

Since T_H ∝ 1/M and r_s ∝ M, hotter BHs are smaller BHs, and the two effects cancel exactly.

**Consequence**: The Hawking photon wavelength λ = ħc/(k_BT_H) satisfies:

  **λ_Hawking = 4π r_s ≈ 12.57 r_s   [always, for any BH]**

---

## The Three Universal Constants

### 1. Hawking Photon Entropy in the Near-Horizon Sphere

Using photon blackbody entropy density s = (16σ/3c) T_H³ and volume V = (4π/3) r_s³:

  T_H³ × V = constant × M⁰   (M cancels via T_H × r_s = const)

Substituting σ = π²k_B⁴/(60ħ³c²):

  **S_Hawking(r_s sphere) = 1/(540 ln2) ≈ 0.002672 bits**

where 540 = 9 × 60 (the 60 from Stefan-Boltzmann; the 9 from spherical geometry + (4π)³ factor).

Verified numerically at: M_sun, 10⁶ M_sun, 10⁹ M_sun, 10¹⁰ kg, 1 kg, M_Planck — all give
exactly 1/(540 ln2) bits.

### 2. Mean Hawking Photon Count in the Near-Horizon Sphere

  **⟨N⟩ = ζ(3)/(24π⁴) ≈ 5.14 × 10⁻⁴**

where ζ(3) = 1.20206... is Apéry's constant. Verified numerically at all masses.

### 3. Classicality Budget Redundancy

For S_T = 1 bit:

  **R_δ = 1/(540 ln2) − 1 ≈ −0.9973   [universal, for any BH mass]**

There is no BH mass for which Hawking radiation provides sufficient entropy for QD-classical
objectivity of any 1-bit fact.

---

## No Classicality Onset Mass

A natural question: is there a BH mass M_onset at which S_Hawking first exceeds 1 bit,
enabling QD-classical objectivity?

**Answer: No such mass exists.**

Since S_Hawking = 1/(540 ln2) ≈ 0.003 bits is CONSTANT, it is always less than 1 bit,
for any BH mass from sub-gram to supermassive. The classicality budget is universally
R_δ ≈ −0.997 near any BH horizon in the universe.

For the budget to equal zero (marginal single-copy classicality), one would need S_T exactly
equal to 1/(540 ln2) ≈ 0.003 bits — a sub-millibit fact with no physically meaningful interpretation.

---

## Novelty Assessment

**Verdict (strategy-002 E002, thorough literature verification): NOT PUBLISHED — CONFIRMED**

Exhaustive search across 18 specific papers + 11 targeted queries (including literal string searches
for "1/(540 ln2)" and "7.21 Schwarzschild radius"). Zero results found for any of the three constants.

- S_Hawking = 1/(540 ln2) bits: **ZERO results** in any indexed source; literal string "1/(540 ln2)" not found anywhere
- ⟨N⟩ = ζ(3)/(24π⁴): **ZERO results**; ζ(3) appears in related BH context (Gray et al. 2016) for
  emission *rates*, not sphere occupation number — genuinely different quantity
- R_1bit = 7.21 r_s: **ZERO results**; "classicality horizon" concept does not exist in BH literature
- T_H × r_s identity: **IMPLICITLY KNOWN but never named** — implicit in all BH papers, explicit
  as T = 1/(4πr_+) in arXiv:2407.21114 (natural units), but never stated as a named universal
  constant or used to derive entropy/photon density

**Algebraic clarity**: The factor 1/540 = 1/(9×60) has a clean structure — 60 comes from
Stefan-Boltzmann (σ = π²k_B⁴/60ħ³c²); the factor 9 comes from the spherical geometric factor.
All π-factors cancel completely. This clean cancellation makes it surprising the result went unnoticed.

**Closest prior work**:
- Kim (2021, arXiv:2112.01931) — closest paper: computes Hawking entropy in a spherical box near BH,
  but uses box radius ≥ 3r_s (not the r_s sphere), uses the actual curved-space stress tensor (not
  naive flat-space blackbody), and gets coefficient 1/360 (different calculation, different geometry).
- Gray et al. (2016, arXiv:1506.03975) — closest ζ(3) usage: uses ζ(3) in Hawking emission *rate*
  through horizon (different quantity from sphere occupation number ⟨N⟩); also implicitly uses
  T_H × r_s via λ_thermal = 8π²r_H.
- arXiv:2407.21114 (2024) — writes T = 1/(4πr_+) in natural units (equivalent to our identity)
  but doesn't name it, doesn't derive entropy/photon density from it.

**Character of novelty**: An "overlooked 5-line calculation from existing results." The ingredients
(T_H formula, r_s formula, Stefan-Boltzmann, photon gas occupation number) were always available.
The barrier was absence of motivation: no one had asked "how much Hawking entropy is inside the
near-horizon sphere?" in the QD-classicality language.

**Caveat**: Full text of Birrell & Davies (1982) and Frolov & Novikov (1998) textbooks not directly
accessible. Unlikely (but not impossible) that a textbook exercise contains the near-horizon sphere
calculation. Standard textbook treatment focuses on emission rates and total entropy.
