---
topic: Classicality budget with operationally relevant thermodynamic entropy (6 systems)
confidence: verified
date: 2026-03-27
source: classicality-budget strategy-001 exploration-005
---

## Summary

Replacing the Bekenstein bound with actual thermodynamic (operational) entropy for 6 physical systems, the classicality budget remains non-constraining for all non-gravitational systems. The Bekenstein bound overestimates actual entropy by **16–80 orders of magnitude** across all systems studied. Only near a black hole horizon does the operational budget become genuinely constraining.

**Framework:** R_δ ≤ S_eff / S_T − 1, where S_eff = actual thermodynamic entropy of the accessible environment.

---

## Master Comparison Table

| System | S_eff (bits) | S_Bek (bits) | S_eff/S_Bek | Constraining? |
|--------|--------------|--------------|-------------|---------------|
| Photon field (room, 300K, 1m³) | 2.85 × 10¹⁵ | 1.60 × 10⁴³ | 1.78 × 10⁻²⁸ | NO |
| Air molecules (STP, 1m³) | 8.58 × 10²⁶ | 1.92 × 10⁴³ | 4.46 × 10⁻¹⁷ | NO |
| CMB (observable universe) | 7.61 × 10⁸⁹ | 3.40 × 10¹²⁴ | 2.24 × 10⁻³⁵ | NO |
| Brain thermal (310K, 1.4kg) | 4.74 × 10²⁶ | 2.47 × 10⁴² | 1.92 × 10⁻¹⁶ | NO |
| BH horizon (solar, Hawking) | 2.67 × 10⁻³ | 1.51 × 10⁷⁷ | 1.76 × 10⁻⁸⁰ | **YES — R_δ < 0** |
| QC (10mK, 1000 qubits) | 5.23 × 10⁹ | 2.58 × 10³⁸ | 2.03 × 10⁻²⁹ | SOMEWHAT |

---

## System-by-System Key Results

### Photon field (300K, 1m³)
- N_photons = 5.48 × 10¹⁴, entropy per photon = 5.20 bits (Bose-Einstein thermal distribution)
- Formula: s_photon = 16σT³/(3c) [two independent derivations agree to 10⁻⁹]
- R_δ_max = 2.85 × 10¹⁵ for 1-bit facts; 2.85 × 10⁹ for 10⁶-bit facts — NOT constraining

### Air molecules (STP, 1m³)
- N_molecules ≈ 2.5 × 10²⁵ (N₂), entropy per molecule = 34.29 bits (Sackur-Tetrode + rotational)
- Air has 300,000× more entropy than room photons per unit volume (more molecules, each with more phase space)
- R_δ_max = 8.58 × 10²⁶ for 1-bit facts — NOT constraining

### CMB (observable universe, 2.725K)
- N_CMB = 1.465 × 10⁸⁹ photons; density = 411/cm³ [matches Fixsen (2009)]
- S_CMB = 7.61 × 10⁸⁹ bits [Hubble sphere gives 2.06 × 10⁸⁸ bits, consistent with Penrose's 10⁸⁸ k_B]
- R_δ_max = 7.61 × 10⁸⁹ — NOT constraining even at cosmological scales

### Brain thermal (310K, 1.4kg)
- Liquid water entropy dominates: S_brain = 4.74 × 10²⁶ bits (NOT constraining)
- EM photon field only: S_brain_photon = 4.23 × 10¹² bits → R_δ_max ≈ 41 for full brain state (S_T ~ 10¹¹ bits)
- Note: photon-only result is marginal but may not reflect the dominant decoherence medium (see below)

### Quantum computer (10mK, 1000 qubits, 1cm³ Si)
- Photon environment: S_photon = 1.054 × 10⁻⁴ bits (essentially zero — wavelengths >> cm scale)
- Si phonon bath (Debye T³ law): S_phonon = 5.23 × 10⁹ bits (dominates)
- For 1000-qubit register (S_T = 1000 bits): R_δ = 5 × 10⁶ — generous
- For megabit facts (S_T = 10⁶ bits): R_δ ≈ 5000 — SOMEWHAT constraining
- Temperature sensitivity: phonon bath would need 175× reduction (to 5.76 × 10⁻⁵ K) to reach below 1000-bit threshold

---

## Key Physical Insights

### Why Bekenstein is so loose
Non-gravitational systems store information in molecular/atomic states, nowhere near quantum gravitational degrees of freedom. A 1kg room-temperature object uses only 10⁻²⁸ of its Bekenstein capacity.

### Air vs. photons: molecular entropy dominates
Air molecules (10²⁵ molecules × 34 bits each) contain 11 orders of magnitude more entropy than the photon field in the same volume. For QD purposes, air molecules are a more powerful encoding medium than photons per unit volume, though photons are more experimentally accessible.

### Classicality budget is a ceiling, not a floor
The QC case illustrates this: the phonon bath has enough entropy to classicalize the register (budget = 5 × 10⁶), but the qubits are engineered to suppress decoherence, keeping actual redundancy near zero. The budget bounds how many copies COULD exist; dynamics determine how many DO exist.

### Conditions for budget to become constraining for non-BH systems
For photon field (S_eff = 2.85 × 10¹⁵ bits), constraining budget (R_δ < 1000) would require S_T > 2.8 × 10¹² bits per fact. For air (S_eff = 8.58 × 10²⁶ bits), would need S_T > 8 × 10²³ bits — exceeding the total entropy of the air itself (impossible by definition).

---

## Verification Status

- S_photon(300K, 1m³) = 2.85 × 10¹⁵ bits [COMPUTED, independently verified × 2]
- S_air(STP, 1m³) = 8.58 × 10²⁶ bits [COMPUTED — Sackur-Tetrode + rotational]
- S_CMB(full obs. universe) = 7.61 × 10⁸⁹ bits [COMPUTED, CHECKED vs Penrose]
- S_brain_water(310K, 1.4kg) = 4.74 × 10²⁶ bits [COMPUTED — NIST molar entropy]
- S_Hawking(solar BH, r_s sphere) = 2.67 × 10⁻³ bits [COMPUTED — see blackhole-hawking-classicality-impossible.md]
- S_QC(10mK, Si phonons, 1cm³) = 5.23 × 10⁹ bits [COMPUTED — Debye T³ law]
- All non-BH systems non-constraining [COMPUTED]
- Hawking radiation BH information paradox connection [CONJECTURED]

---

## Caveat: Brain Photon Result

The EM photon-only budget for the brain (R_δ ≈ 41 for full neural state) may be an artifact. The dominant decoherence medium for neurons is likely the molecular phonon bath (thermal fluctuations in water/protein structure), not the EM photon field. With molecular entropy, the budget is ~ 10²⁶ bits (not constraining). The photon-only result is potentially interesting but requires a specific physical claim that photons (not phonons) are the relevant QD environment for neural processes.
