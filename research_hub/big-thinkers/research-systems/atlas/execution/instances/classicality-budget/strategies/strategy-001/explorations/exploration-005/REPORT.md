# Exploration 005: Operationally Relevant Classicality Budget

**Date:** 2026-03-27
**Code:** `code/classicality_budget_thermal.py`

---

## Goal

Replace the Bekenstein bound in the classicality budget formula with operationally
relevant thermodynamic entropy, compute for 6 physical systems, and determine
whether the budget becomes physically constraining.

**Framework:**  R_δ ≤ S_eff / S_T − 1

- S_eff = actual thermal/statistical mechanical entropy of the environment
- S_T = entropy per classical fact being observed
- Exploration 002 established Bekenstein-based budgets ranging from 10^43 (lab) to 10^123 (universe)
- This exploration asks: if we use real entropy instead, does the budget tighten enough to matter?

---

## Section 1: Methods and Physical Formulas

### 1.1 Operationally Relevant Entropy

The "operationally relevant" environment entropy for quantum Darwinism is the actual number
of distinguishable states the environment can occupy — not the theoretical Bekenstein maximum.
This is the standard thermodynamic entropy, which determines (via the Holevo bound) the
maximum classical information extractable from the environment.

**Key formulas:**

**Thermal photon entropy** (Planck distribution / Stefan-Boltzmann thermodynamics):

  s_photon = (16 σ T³) / (3 c)      [J K⁻¹ m⁻³]

  This follows from:
    - Energy density of photon gas: u = (4σ/c) T⁴
    - Thermodynamic relation: s = (4/3) × u/T = 16σT³/(3c)

  Two independent derivations (Stefan-Boltzmann + explicit Planck sum) agree to
  10⁻⁹ relative error. [VERIFIED]

**Ideal gas entropy** (Sackur-Tetrode formula + rotational):

  S_trans/Nk_B = 5/2 + ln[(V/N) × (2πmk_BT/h²)^(3/2)]
  S_rot/Nk_B   = 1 + ln(T/θ_rot)   [high-T limit, valid when T >> θ_rot]

**Liquid water molar entropy**: S_molar(298K) = 69.91 J/mol/K (NIST tabulated value)
  With temperature correction: S_molar(310K) = 69.91 + Cp × ln(310/298) ≈ 72.88 J/mol/K

**Si phonon entropy** (Debye T³ law, T << θ_D):

  S_phonon = (4π⁴/5) × N × (T/θ_D)³ × k_B       [valid for T << θ_D = 645K]

**Hawking temperature:**

  T_H = ħc³ / (8πGMk_B)

**Bekenstein bound** (for comparison):

  S_Bek = 2πREk_B / (ħc)   where E = Mc²

### 1.2 Verification Cross-Checks Performed

1. Photon entropy formula: two independent derivations agree to 10⁻⁹ — [VERIFIED]
2. Photon entropy at 300K: independent calculation gives S = 2.84×10¹⁵ bits — [CHECKED]
3. CMB photon density at 2.725K: code gives 411/cm³ matching Fixsen (2009) — [CHECKED]
4. BH entropy S_BH = A/(4G) gives 1.51×10⁷⁷ bits for solar mass — [CHECKED vs Exploration 002]

---

## Section 2: System-by-System Results

### System 1: Photon Field in a 1m³ Room (T = 300K)

**Setup:** Thermal photon gas in 1 m³ at room temperature.
The photon field is the primary decoherence medium for macroscopic objects ("things are
seen by light").

**Results:** [COMPUTED]

  S_photon = 2.846 × 10¹⁵ bits
  S_Bek    = 1.598 × 10⁴³ bits   (1 kg mass, 0.62m radius)
  Ratio    = 1.78 × 10⁻²⁸         (photons use < 10⁻²⁷ of Bekenstein capacity)

  Number of thermal photons in 1m³: 5.48 × 10¹⁴
  Entropy per photon: 5.20 bits  (consistent with Bose-Einstein thermal distribution)

**Classicality budget (S_eff = S_photon):**

  | S_T (fact size) | R_δ_max (photon) | R_δ_max (Bekenstein) | Factor reduction |
  |-----------------|------------------|----------------------|------------------|
  | 1 bit           | 2.85 × 10¹⁵      | 1.60 × 10⁴³          | 10⁻²⁸            |
  | 10 bits         | 2.85 × 10¹⁴      | 1.60 × 10⁴²          | 10⁻²⁸            |
  | 100 bits        | 2.85 × 10¹³      | 1.60 × 10⁴¹          | 10⁻²⁸            |
  | 10⁶ bits        | 2.85 × 10⁹       | 1.60 × 10³⁷          | 10⁻²⁸            |

**Verdict:** Budget NOT constraining. Even for megabit facts, the room photon field
supports ~2.85 billion independent verifications. The budget is reduced 28 orders
of magnitude from Bekenstein, but remains astronomically generous.

---

### System 2: Air Molecules at STP (1m³)

**Setup:** 1 m³ of air at T = 293K, P = 101325 Pa.
N ≈ 2.503 × 10²⁵ molecules (mostly N₂, m ≈ 4.81 × 10⁻²⁶ kg).
Each air molecule that scatters off an object carries information about its state.

**Results:** [COMPUTED]

  S_air_trans  = 6.532 × 10²⁶ bits  (translational only, Sackur-Tetrode)
  S_air_full   = 8.584 × 10²⁶ bits  (translational + rotational, diatomic gas)
  S_Bek        = 1.924 × 10⁴³ bits  (1.2 kg mass, 0.62m radius)
  Ratio        = 4.46 × 10⁻¹⁷

  Entropy per molecule: 34.29 bits/molecule (trans + rot at 293K)

  Note: Air molecules have FAR more entropy than room photons:
    S_air / S_photon ≈ 300,000×
  Because N_molecules ~ 2.5×10²⁵ >> N_photons ~ 5.5×10¹⁴, each with ~34 bits.

**Classicality budget:**

  | S_T          | R_δ_max (air)  | R_δ_max (Bekenstein) |
  |--------------|----------------|----------------------|
  | 1 bit        | 8.58 × 10²⁶    | 1.92 × 10⁴³           |
  | 10 bits      | 8.58 × 10²⁵    | 1.92 × 10⁴²           |
  | 100 bits     | 8.58 × 10²⁴    | 1.92 × 10⁴¹           |
  | 10⁶ bits     | 8.58 × 10²⁰    | 1.92 × 10³⁷           |

**Verdict:** Budget NOT constraining. Air molecules provide an enormous encoding
capacity — 10²⁶ bits for a 1m³ room. The budget is reduced 17 orders of magnitude
from Bekenstein but remains extremely generous.

---

### System 3: CMB in the Observable Universe

**Setup:** CMB photon gas at T_CMB = 2.725K throughout the observable universe
(comoving radius R = 4.4 × 10²⁶ m, V = 3.57 × 10⁸⁰ m³).

**Results:** [COMPUTED]

  N_CMB          = 1.465 × 10⁸⁹ photons
  CMB density    = 411 photons/cm³  [CHECKED — matches Fixsen (2009)]
  S_CMB          = 7.611 × 10⁸⁹ bits  =  5.275 × 10⁸⁹ k_B
  S_Bek (univ)   = 3.402 × 10¹²⁴ bits  (M_univ ≈ 3×10⁵⁴ kg)
  Ratio          = 2.24 × 10⁻³⁵

**Cross-check against literature:** [CHECKED]

  Penrose quotes S_CMB ≈ 10⁸⁸ k_B; this refers to the Hubble sphere (R_H = c/H₀ ≈ 1.32×10²⁶ m)
  not the full observable universe. Recomputing with Hubble sphere gives:
  S_CMB (Hubble) ≈ 1.43 × 10⁸⁸ k_B ≈ 2.06 × 10⁸⁸ bits  [COMPUTED]
  This is consistent with Penrose's 10⁸⁸ figure. The factor of ~37 difference is
  exactly (R_obs / R_Hubble)³ ≈ (46/14)³ ≈ 36. My 7.6×10⁸⁹ bits is for the larger
  comoving observable universe volume. Both are correct for their respective volumes.

**Classicality budget:**

  | S_T           | R_δ_max (CMB)  | R_δ_max (Bekenstein) |
  |---------------|----------------|----------------------|
  | 1 bit         | 7.61 × 10⁸⁹    | 3.40 × 10¹²⁴         |
  | 10 bits       | 7.61 × 10⁸⁸    | 3.40 × 10¹²³         |
  | 10⁶ bits      | 7.61 × 10⁸³    | 3.40 × 10¹¹⁸         |

**Verdict:** Budget NOT constraining. The CMB budget is reduced 35 orders of magnitude
from Bekenstein, but 10⁸⁹ bits is still immense. Even for 10⁶-bit facts, R_δ ~ 10⁸³.

---

### System 4: Brain Thermal Environment (37°C, 1.4 kg)

**Setup:** Human brain at T = 310K, M = 1.4 kg, volume ≈ 1.35 L, 80% water by mass.
The decoherence environment is the thermal medium (water + ions + proteins).
Two sub-cases: (a) liquid water entropy (primary thermal environment),
(b) thermal photon EM field in brain volume.

**Results:** [COMPUTED]

  Water: 62.2 mol at 310K
  S_molar(water, 310K) = 72.88 J/mol/K
  S_brain_thermal = 4531 J/K = 4.735 × 10²⁶ bits   [liquid water entropy]
  S_brain_photon  = 4.233 × 10¹² bits               [EM photon field at 310K in 1.35L]
  S_Bek           = 2.471 × 10⁴² bits               (1.4kg, 0.068m radius)
  Ratio (water/Bek)  = 1.92 × 10⁻¹⁶
  Ratio (photon/Bek) = 1.71 × 10⁻³⁰

  Note: Water entropy >> photon entropy by 14 orders of magnitude
  (liquid water has vastly more accessible degrees of freedom than the photon field
  inside the same volume at the same temperature)

**Classicality budget (using liquid water entropy):**

  | S_T                | R_δ_max (water) | R_δ_max (Bekenstein) |
  |--------------------|-----------------|----------------------|
  | 1 bit              | 4.74 × 10²⁶     | 2.47 × 10⁴²           |
  | 10⁶ bits (percept) | 4.74 × 10²⁰     | 2.47 × 10³⁶           |
  | 10¹¹ bits (brain)  | 4.74 × 10¹⁵     | 2.47 × 10³¹           |

**Classicality budget (using photon EM field only):**

  | S_T                | R_δ_max (photon) |
  |--------------------|------------------|
  | 1 bit              | 4.23 × 10¹²      |
  | 10⁶ bits (percept) | 4.23 × 10⁶       |
  | 10¹¹ bits (brain)  | 41.3             |

**Notable result:** If the relevant decoherence environment is restricted to the
photon EM field inside the brain (which is actually the primary decoherence
medium for quantum superpositions in biology, via electromagnetic coupling), then
for a full brain state (S_T ~ 10¹¹ bits), R_δ_max ≈ 41.

This means: the EM photon environment inside the brain can support at most ~41
independent verifications of the full neural state. This is still generous for
practical purposes, but it's a real number, not 10³¹.

**Verdict:** Using molecular entropy — NOT constraining. Using photon EM field
only — marginally interesting for full-brain-state facts (~41-fold redundancy).

---

### System 5: Near a Black Hole Horizon (Solar-Mass BH, Hawking Radiation)

**Setup:** Solar-mass BH (M = M_☉ = 1.99 × 10³⁰ kg).
The only thermal radiation available for encoding environmental records is the
Hawking photons. We compute the entropy of the Hawking photon gas in the
volume V ~ r_s³ near the horizon.

**Results:** [COMPUTED]

  Hawking temperature:    T_H = 6.168 × 10⁻⁸ K
  Schwarzschild radius:   r_s = 2.954 × 10³ m = 2.95 km
  BH entropy (Bekenstein-Hawking): S_BH = 1.514 × 10⁷⁷ bits

  Volume of sphere V₁ = (4/3)π r_s³ = 1.080 × 10¹¹ m³
  S_Hawking(V₁) = 2.672 × 10⁻³ bits
  Average number of photons in V₁ = 5.14 × 10⁻⁴

  Ratio S_Hawking / S_BH = 1.76 × 10⁻⁸⁰   [80-order-of-magnitude gap!]

**Why is S_Hawking so small?**

  Hawking photons have de Broglie wavelength λ ~ ħc/(k_BT_H) ≈ 4.2 × 10¹⁰ m = 0.3 AU.
  This is vastly larger than r_s = 2.95 km.
  The photon wavelength exceeds the entire "near-horizon region" by 7 orders of magnitude.
  As a result, there is typically << 1 Hawking photon present in the near-horizon volume
  at any given time. This is not a small correction — it means the Hawking environment
  is essentially vacuum for purposes of information encoding.

**Classicality budget (S_eff = Hawking photons in r_s sphere):**

  | S_T       | R_δ_max          |
  |-----------|------------------|
  | 1 bit     | -9.97 × 10⁻¹     |
  | 10 bits   | -1.000           |
  | 100 bits  | -1.000           |
  | 10⁶ bits  | -1.000           |

  For comparison, Bekenstein-based budget (S_BH = 1.51×10⁷⁷ bits):
  | S_T = 1 bit: R_δ = 1.51 × 10⁷⁷ |

**Verdict: CONSTRAINING. The Hawking photon environment for a solar-mass BH
  has S_eff < 1 bit. R_δ ≈ -1 for all fact sizes. Classical reality via quantum
  Darwinism is IMPOSSIBLE based on Hawking radiation alone.**

  Physical interpretation: An observer near a solar-mass BH trying to verify classical
  facts through the Hawking radiation environment would find the budget is zero —
  there are not enough Hawking photons in the environment to carry even one redundant copy
  of any classical fact. The environment cannot support classicalization.

  Note: The BH's own Bekenstein-Hawking entropy is 10⁷⁷ bits — the budget would be
  enormous if one could access the BH's internal degrees of freedom. But those are
  hidden behind the horizon. The only accessible environment is the Hawking radiation,
  which has S_eff ~ 10⁻³ bits. This is the starkest possible illustration of the
  difference between Bekenstein capacity and operational capacity.

---

### System 6: Quantum Computer Register (1000 Qubits, T = 10 mK)

**Setup:** Superconducting quantum computer (e.g., transmon qubits) operating at T = 10 mK
in a dilution refrigerator. 1000 qubits, chip area ≈ 1 cm² in V ≈ 1 cm³.
Qubit frequency ω/(2π) = 5 GHz → E_q = k_B × 0.24 K, so k_BT/E_q = 0.042 (deep quantum regime).

**Environment entropy contributions:**

  1. Thermal photons (blackbody at 10mK in 1 cm³):
     S_photon = 1.054 × 10⁻⁴ bits   [COMPUTED]
     (Essentially zero — photons at 10mK have wavelengths >> cm scale)

  2. Si substrate phonons (Debye T³ law, θ_D = 645K, V = 1 cm³):
     N_phonon modes = 1.249 × 10²²
     S_phonon = 5.234 × 10⁹ bits    [COMPUTED]
     (T³ law: S ∝ (T/θ_D)³ = (0.01/645)³ ≈ 3.7 × 10⁻¹⁵)

  Total: S_env = 5.234 × 10⁹ bits  (dominated by phonons)

  S_Bekenstein (1g chip, 1cm): 2.577 × 10³⁸ bits
  Ratio S_env / S_Bek = 2.03 × 10⁻²⁹

**Classicality budget:**

  | S_T              | R_δ_max (realistic) | R_δ_max (Bekenstein) |
  |------------------|---------------------|----------------------|
  | 1 bit            | 5.23 × 10⁹          | 2.58 × 10³⁸           |
  | 10 bits          | 5.23 × 10⁸          | 2.58 × 10³⁷           |
  | 100 bits         | 5.23 × 10⁷          | 2.58 × 10³⁶           |
  | 1000 bits (reg.) | 5.23 × 10⁶          | 2.58 × 10³⁵           |
  | 10⁶ bits         | 5.23 × 10³          | 2.58 × 10³²           |

**Notable result:** For 10⁶-bit facts, R_δ = 5.23 × 10³ — the budget is still not
truly constraining (many thousands of possible verifications), but 29 orders of
magnitude tighter than Bekenstein. For the full 1000-qubit register (S_T = 1000 bits),
R_δ ≈ 5 × 10⁶.

**Temperature sensitivity analysis:** [COMPUTED]

  At what temperature does S_photon(T, 1cm³) = 1000 bits (barely enough for one copy)?
    → T_cross_photon = 2.12 K = 2117 mK   (211× the operating temperature)

  At what temperature does S_phonon(T, 1cm³, Si) = 1000 bits?
    → T_cross_phonon = 5.76 × 10⁻⁵ K   (175× BELOW operating temperature)

  This is remarkable: the Si phonon bath at 10mK already has 5 × 10⁹ bits of entropy.
  The cryogenic temperature would need to be lowered by 175× to get the phonon
  environment below the 1000-bit encoding threshold for the register.

**Verdict:** SOMEWHAT constraining. At 10mK, S_env = 5.23×10⁹ bits (dominated by
phonons). Budget is reduced 29 orders from Bekenstein. For the qubit register itself
(S_T = 1000 bits), R_δ = 5×10⁶ — generous. For very large facts (10⁶ bits), R_δ ≈ 5000.
The environment has enough entropy to classicalize the quantum computer in principle,
but much less capacity than Bekenstein implied.

---

## Section 3: Master Comparison Table

### 3.1 Entropy Values

  | System                          | S_eff (bits)  | S_Bek (bits)  | S_eff/S_Bek  |
  |---------------------------------|---------------|---------------|--------------|
  | Photon field (room, 300K, 1m³) | 2.85 × 10¹⁵  | 1.60 × 10⁴³  | 1.78 × 10⁻²⁸ |
  | Air molecules (STP, 1m³)        | 8.58 × 10²⁶  | 1.92 × 10⁴³  | 4.46 × 10⁻¹⁷ |
  | CMB (observable universe)       | 7.61 × 10⁸⁹  | 3.40 × 10¹²⁴ | 2.24 × 10⁻³⁵ |
  | Brain thermal (310K, 1.4kg)     | 4.74 × 10²⁶  | 2.47 × 10⁴²  | 1.92 × 10⁻¹⁶ |
  | BH horizon (solar, Hawking)     | 2.67 × 10⁻³  | 1.51 × 10⁷⁷  | 1.76 × 10⁻⁸⁰ |
  | QC (10mK, 1000 qubits)         | 5.23 × 10⁹   | 2.58 × 10³⁸  | 2.03 × 10⁻²⁹ |

### 3.2 Classicality Budgets

  (R_δ_max = S_eff/S_T − 1 for S_T = 1 bit and S_T = 10⁶ bits)

  | System                          | R_δ (S_T=1)  | R_δ (S_T=10⁶) | Constraining? |
  |---------------------------------|--------------|----------------|---------------|
  | Photon field (room, 300K, 1m³) | 2.85 × 10¹⁵ | 2.85 × 10⁹     | NO            |
  | Air molecules (STP, 1m³)        | 8.58 × 10²⁶ | 8.58 × 10²⁰    | NO            |
  | CMB (observable universe)       | 7.61 × 10⁸⁹ | 7.61 × 10⁸³    | NO            |
  | Brain thermal (310K, 1.4kg)     | 4.74 × 10²⁶ | 4.74 × 10²⁰    | NO            |
  | BH horizon (solar, Hawking)     | −0.997       | −1.000         | YES — zero    |
  | QC (10mK, 1000 qubits)         | 5.23 × 10⁹  | 5.23 × 10³     | SOMEWHAT      |

### 3.3 Key Takeaways from the Table

1. **The Bekenstein bound overestimates actual encoding capacity by 17–80 orders of magnitude.**
   Real thermodynamic entropy occupies an incredibly small fraction of the Bekenstein maximum.

2. **Only ONE system becomes genuinely constraining: the black hole horizon.**
   The Hawking photon environment near a solar-mass BH has S_eff = 0.003 bits —
   effectively ZERO. No classical facts can be verified through Hawking radiation alone.

3. **All non-gravitational systems remain non-constraining**, even with realistic entropy.
   The smallest realistic budget for non-BH systems is the QC photon environment
   (10⁻⁴ bits), but the phonon bath dominates (5×10⁹ bits), making it non-constraining.

4. **The range of realistic S_eff values is enormous:**
   From 10⁻⁴ bits (photons at 10mK) to 10⁸⁹ bits (CMB in observable universe).
   Bekenstein covers 10⁻⁸⁰ to 10⁻¹⁶ of these actual values.

---

## Section 4: Physical Interpretation

### 4.1 Why Is the Bekenstein Bound So Loose?

The Bekenstein bound S_max ≤ 2πRE/(ħc) assumes a system is a black hole or at the
verge of gravitational collapse. For a 1kg room-temperature object with R = 0.6m and
E = Mc² = 9×10¹⁶ J, the Bekenstein bound is 1.6×10⁴³ bits — but the actual entropy
uses only 10⁻²⁸ of this capacity. The reason: non-gravitational systems are nowhere
near their density limits. Real matter stores information in molecular and atomic states,
not quantum gravitational degrees of freedom.

### 4.2 The Black Hole Case is Special and Physically Profound [COMPUTED + CONJECTURED]

The solar-mass BH result is striking. The BH has S_BH = 1.51×10⁷⁷ bits of Bekenstein-
Hawking entropy, but the Hawking photon bath near the horizon carries S_eff ≈ 0.003 bits.
The ratio is 10⁻⁸⁰.

**Physically, this occurs because:**
- The Hawking photons have wavelength λ ~ ħc/(k_BT_H) ≈ 4×10¹⁰ m = ~0.3 AU
- The Schwarzschild radius is r_s = 2.95 km
- λ/r_s ≈ 10⁷ — the photon wavelength exceeds the system scale by 7 orders of magnitude
- Therefore, there is less than 1 Hawking photon in the entire near-horizon volume at any time

This means: an observer near a solar-mass BH, relying only on Hawking photons as the
environment for quantum Darwinism, would find ZERO classicality budget. Classical facts
about objects near the horizon cannot be made "objective" through Hawking radiation.

This connects to several deep results:
1. **Black hole complementarity**: The BH information paradox arises partly because the
   Hawking radiation doesn't carry enough information about what fell in. The classicality
   budget quantifies exactly how far this is from being objective.
2. **Information scrambling**: The BH interior has 10⁷⁷ bits of encoding capacity, but
   this is inaccessible to outside observers except through Hawking radiation over the
   BH lifetime. The accessible environment entropy is essentially zero at any given moment.

**Caveat [CONJECTURED]:** For a Planck-mass BH (M ~ 2×10⁻⁸ kg), T_H ~ 10³¹ K and
r_s ~ 10⁻³⁵ m (Planck length). The photon wavelength becomes λ ~ ħc/(k_BT_H) ~ r_s,
so photons fit in the near-horizon volume. At the Planck scale, the Hawking environment
might actually have significant entropy. This is unexplored territory.

### 4.3 The Quantum Computer Case: Near-Interesting [COMPUTED]

At 10mK, the phonon bath in 1cm³ of Si has S_phonon = 5.23×10⁹ bits. This is notable:

- For the 1000-qubit register (S_T = 1000 bits), R_δ = 5×10⁶ — the environment
  COULD support 5 million independent verifications of the full qubit state.
- This means: from a classicality budget perspective, the cryogenic environment has
  enough entropy to make the quantum register "objective" in the quantum Darwinism
  sense. The qubits' classical state could in principle be encoded into 5×10⁶
  copies in the phonon bath.

But quantum computers are engineered to PREVENT this. The coupling to the phonon bath
is minimized. The actual redundancy achieved is far less than the maximum budget.
This illustrates an important distinction:

  **The classicality budget is a CEILING on redundancy, not a floor.**
  The budget says how many copies COULD exist; the dynamics determine how many DO exist.

For the QC environment, the phonon bath has enough entropy to classicalize the qubits
if decoherence were maximized, but the engineering goal is to keep actual redundancy near 0.

### 4.4 The Room vs. the Lab: Photons vs. Molecules

A surprising finding: air molecules (S = 8.6×10²⁶ bits in 1m³) carry 11 orders of
magnitude more entropy than the photon field (S = 2.8×10¹⁵ bits) in the same volume.

This seems counterintuitive — but it makes sense:
- N_molecules ~ 10²⁵ each with ~34 bits (translational + rotational phase space)
- N_photons ~ 10¹⁵ each with ~5.2 bits

For quantum Darwinism, the air molecules are actually a more powerful encoding medium
than the photon field, per unit volume. This has implications for which environmental
degrees of freedom are more "responsible" for classicality in everyday experience.
Photons may be more experimentally accessible and the primary decoherence agent for
interference experiments, but the molecular bath has a larger total encoding capacity.

---

## Section 5: Conclusions

### 5.1 Main Answer: Is the Budget Constraining with Realistic Entropy?

**Yes, but only for one system: the black hole horizon environment.**

For the 5 non-BH systems, the realistic classicality budget is reduced by 16–35 orders
of magnitude compared to Bekenstein, but remains astronomically non-constraining.
Even the smallest non-BH budget (QC at 10mK, photon-only: 10⁻⁴ bits) becomes
non-constraining when the full environment (phonons included) is considered.

The black hole Hawking radiation case is uniquely constraining: S_eff ≈ 10⁻³ bits
in the near-horizon region, making R_δ < 0 for all fact sizes. This is physically
meaningful and connects to the BH information paradox.

### 5.2 Verification Status of Key Claims

- S_photon(300K, 1m³) = 2.85×10¹⁵ bits [COMPUTED] — code in `code/classicality_budget_thermal.py`
- S_air(STP, 1m³) = 8.58×10²⁶ bits [COMPUTED] — Sackur-Tetrode + rotational
- S_CMB(full obs. universe) = 7.6×10⁸⁹ bits [COMPUTED, CHECKED vs Penrose (Hubble sphere)]
- S_brain_water(310K, 1.4kg) = 4.7×10²⁶ bits [COMPUTED] — tabulated molar entropy
- S_Hawking(solar BH, r_s sphere) = 2.7×10⁻³ bits [COMPUTED]
- S_QC(10mK, Si phonons, 1cm³) = 5.23×10⁹ bits [COMPUTED] — Debye T³ law
- BH horizon budget R_δ < 0: CONSTRAINING [COMPUTED]
- All other systems non-constraining [COMPUTED]
- Hawking photon interpretation (BH information paradox connection) [CONJECTURED]

### 5.3 What Would Make the Budget Constraining for Non-BH Systems?

For the photon field in a room (S_eff = 2.85×10¹⁵ bits), the budget would become
constraining (R_δ < 1000) only for facts with S_T > 2.8×10¹² bits. No ordinary
physical system has such large per-fact entropy.

For air molecules (S_eff = 8.58×10²⁶ bits), one would need S_T > 8×10²³ bits per fact
to get R_δ < 1000. That exceeds the total entropy of the air itself — impossible by definition.

**Conclusion [COMPUTED]:** For all non-gravitational systems studied, the operationally
relevant classicality budget is non-constraining for any physically realizable fact.
The only scenario where the budget becomes tight is near a strong gravity source, where
the accessible Hawking radiation is sparse while the Bekenstein-Hawking entropy is large.

### 5.4 Why This Matters

The key insight from this exploration: **the Bekenstein bound is extremely loose for
non-gravitational systems, being overestimated by 16–35 orders of magnitude.**
This means that for any terrestrial quantum Darwinism experiment, the classicality
budget cannot be saturated even in principle — the environment has orders of magnitude
less entropy than would be needed to hit the Bekenstein ceiling.

This validates the practical irrelevance of the classicality budget for laboratory physics,
while identifying the BH horizon as the one physical system where the realistic entropy
(Hawking radiation) creates a genuine constraint — a constraint that connects directly
to the black hole information paradox.

---

## References / Physical Constants Used

All computations in SI units. Key constants:
- k_B = 1.380649 × 10⁻²³ J/K (exact, SI)
- ħ = 1.054571817 × 10⁻³⁴ J·s
- c = 2.99792458 × 10⁸ m/s (exact)
- G = 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²
- σ = 5.670374419 × 10⁻⁸ W m⁻² K⁻⁴ (Stefan-Boltzmann)
- S_molar(H₂O, 298K) = 69.91 J/mol/K (NIST)
- θ_D(Si) = 645 K (Debye temperature, standard reference)
- θ_rot(N₂) = 2.88 K (rotational temperature)

Formulas sourced from: statistical mechanics textbooks (Pathria & Beale, Kittel & Kroemer),
NIST thermochemistry data, Bekenstein (1973), Hawking (1975).
