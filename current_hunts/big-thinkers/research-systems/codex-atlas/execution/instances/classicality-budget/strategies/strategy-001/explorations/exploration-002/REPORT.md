# Exploration 002: Numerical Computation of the Classicality Budget

## Goal

Compute the classicality budget R_δ ≤ (S_max / S_T) − 1 numerically for 6 physical systems using Python with numpy/scipy. Produce exact numbers, verify physical sense, and flag any systems where the budget gives absurd results.

## Formula

The classicality budget inequality: **R_δ ≤ (S_max / S_T) − 1**

where:
- **R_δ** = redundancy number (how many independent observers can verify the same classical fact)
- **S_max** = maximum entropy of the bounded region (tighter of Bekenstein or holographic bounds)
- **S_T** = information content of one classical fact (in bits)

**Entropy bounds used:**
- Bekenstein bound: S_Bek = 2πRE / (ℏc ln 2) bits
- Holographic (spherical) bound: S_holo = πR² / (l_P² ln 2) bits
- S_max = min(S_Bek, S_holo)

**Generalized form for multiple facts:** For N_facts distinct classical facts, each with redundancy R_δ:

> N_facts × (R_δ + 1) × S_T ≤ S_max

This gives the fundamental trade-off: **more facts = less redundancy per fact**, and vice versa.

## Physical Constants Used

All SI values: [COMPUTED]

| Constant | Value | Unit |
|----------|-------|------|
| ℏ | 1.054572 × 10⁻³⁴ | J·s |
| c | 2.997925 × 10⁸ | m/s |
| G | 6.674300 × 10⁻¹¹ | m³/(kg·s²) |
| l_P | 1.616255 × 10⁻³⁵ | m |
| E_P | 1.956 × 10⁹ | J |
| m_P | 2.176434 × 10⁻⁸ | kg |
| M_☉ | 1.989 × 10³⁰ | kg |

---

## Summary Table

[COMPUTED]

| System | S_max (bits) | Tighter Bound | R_δ (S_T=1) | R_δ (S_T=10⁶) | log₁₀(S_max) |
|--------|-------------|---------------|-------------|----------------|---------------|
| Lab (1m sphere, 1 kg) | 1.29 × 10⁴³ | Bekenstein | 1.29 × 10⁴³ | 1.29 × 10³⁷ | 43.1 |
| Human brain (1.4 kg) | 2.50 × 10⁴² | Bekenstein | 2.50 × 10⁴² | 2.50 × 10³⁶ | 42.4 |
| Near BH (1 kg at 2r_s) | 7.61 × 10⁴⁶ | Bekenstein | 7.61 × 10⁴⁶ | 7.61 × 10⁴⁰ | 46.9 |
| Solar-mass BH (full) | 1.51 × 10⁷⁷ | Both (equal) | 1.51 × 10⁷⁷ | 1.51 × 10⁷¹ | 77.2 |
| Observable universe | 1.13 × 10¹²³ | Bekenstein | 1.13 × 10¹²³ | 1.13 × 10¹¹⁷ | 123.1 |
| Planck-scale region | 4.53 | Holographic | 3.53 | < 0 | 0.66 |
| QC (1000 qubits) | 2.58 × 10¹⁹ | Bekenstein | 2.58 × 10¹⁹ | 2.58 × 10¹³ | 19.4 |

---

## Detailed Results by System

### System 1: Lab-scale Region (1-meter sphere, 1 kg)

**Parameters:**
- R = 0.5 m (radius of 1-meter diameter sphere)
- M = 1.0 kg (ordinary matter, e.g. air at ~1 atm)
- E = mc² = 8.988 × 10¹⁶ J

**Entropy bounds:** [COMPUTED]

| Bound | Value (bits) | log₁₀ |
|-------|-------------|-------|
| Bekenstein | 1.288 × 10⁴³ | 43.11 |
| Holographic | 4.338 × 10⁶⁹ | 69.64 |
| **Effective** | **1.288 × 10⁴³** | **43.11** |

Tighter bound: Bekenstein (by 26 orders of magnitude).

**Classicality budget:** [COMPUTED]

| S_T (bits) | Description | R_δ (max) | log₁₀(R_δ) |
|-----------|-------------|-----------|------------|
| 1 | Minimal binary fact | 1.29 × 10⁴³ | 43.1 |
| 10 | A letter of text | 1.29 × 10⁴² | 42.1 |
| 29 | Position to 1mm in 3D [ESTIMATED] | 4.45 × 10⁴¹ | 41.6 |
| 100 | A sentence | 1.29 × 10⁴¹ | 41.1 |
| 10⁶ | A photograph | 1.29 × 10³⁷ | 37.1 |

**Physical interpretation:** A 1-meter lab region has an enormous classicality budget. Even for photograph-resolution classical facts (10⁶ bits each), the region can support 10³⁷ independent observers each verifying the same fact. The budget is so large that for any real-world lab experiment, the classicality constraint is trivially satisfied.

**Cross-check:** [CHECKED] S_Bek ≈ 10⁴³ bits for 1 kg at 0.5 m matches standard textbook Bekenstein bound calculations.

---

### System 2: Human Brain (1.4 kg)

**Parameters:**
- V_brain = 1400 cm³ → R = (3V/(4π))^(1/3) = 0.0694 m (equivalent sphere radius)
- M = 1.4 kg
- E = mc² = 1.258 × 10¹⁷ J

**Entropy bounds:** [COMPUTED]

| Bound | Value (bits) | log₁₀ |
|-------|-------------|-------|
| Bekenstein | 2.504 × 10⁴² | 42.40 |
| Holographic | 8.356 × 10⁶⁷ | 67.92 |
| **Effective** | **2.504 × 10⁴²** | **42.40** |

Tighter bound: Bekenstein (by 25 orders of magnitude).

**Classicality budget for brain-specific S_T values:** [COMPUTED, S_T values ESTIMATED]

| S_T (bits) | Description | R_δ (max) | log₁₀(R_δ) |
|-----------|-------------|-----------|------------|
| 1 | Single neuron state (fire/not) | 2.50 × 10⁴² | 42.4 |
| 8 | Single synapse weight | 3.13 × 10⁴¹ | 41.5 |
| 10³ | Conscious percept (low estimate) | 2.50 × 10³⁹ | 39.4 |
| 10⁶ | Conscious percept (high estimate) | 2.50 × 10³⁶ | 36.4 |

**The multi-fact trade-off (S_T = 1 bit):** [COMPUTED]

| N_facts | R_δ (max) | Interpretation |
|---------|-----------|----------------|
| 1 | 2.50 × 10⁴² | Single fact, max redundancy |
| 10⁶ | 2.50 × 10³⁶ | Million distinct facts |
| 10¹¹ | 2.50 × 10³¹ | ~ number of neurons |
| 10²⁰ | 2.50 × 10²² | ~ number of synapses |
| 10³⁰ | 2.50 × 10¹² | Rich inner world |
| 10⁴² | 1.5 | Maximum facts, near-zero redundancy |

**Physical interpretation:** The brain's Bekenstein bound (~10⁴² bits) dwarfs its neural complexity (~10¹¹ neurons, ~10¹⁴ synapses) by roughly 28 orders of magnitude. The classicality budget is **absolutely not** the limiting factor for brain function or conscious experience. Even with 10¹¹ distinct neural facts, each can have redundancy R_δ ~ 10³¹ — billions of billions of independent verifications per fact.

**Important caveat:** The Bekenstein bound counts ALL physical degrees of freedom (subatomic, nuclear, electronic, molecular, etc.), not just computationally relevant ones. The actual information processed by the brain uses a tiny fraction of its Bekenstein capacity. A more operationally relevant bound might use the thermally accessible entropy (~10²⁵ bits for 1.4 kg at 310 K), which is still enormously above neural complexity but 17 orders of magnitude below the Bekenstein bound.

---

### System 3: Near a Black Hole Horizon

**System 3a: 1 kg of matter at r = 2r_s from a solar-mass BH**

**Parameters:**
- r_s = 2GM_☉/c² = 2954 m (Schwarzschild radius for M_☉)
- R = r_s = 2954 m (region size)
- M_test = 1 kg, E = mc² = 8.988 × 10¹⁶ J (local energy)

**Entropy bounds:** [COMPUTED]

| Bound | Value (bits) | log₁₀ |
|-------|-------------|-------|
| Bekenstein | 7.613 × 10⁴⁶ | 46.88 |
| Holographic | 1.514 × 10⁷⁷ | 77.18 |
| **Effective** | **7.613 × 10⁴⁶** | **46.88** |

For 1 kg of test mass, the Bekenstein bound is the limiting factor. The holographic bound (which equals the BH entropy) is 30 orders of magnitude larger.

**System 3b: Full solar-mass black hole**

**Parameters:**
- R = r_s = 2954 m
- M = M_☉ = 1.989 × 10³⁰ kg
- E = M_☉c² = 1.788 × 10⁴⁷ J

**Entropy bounds:** [COMPUTED] [CHECKED]

| Bound | Value (bits) | log₁₀ |
|-------|-------------|-------|
| Bekenstein | 1.514 × 10⁷⁷ | 77.18 |
| Holographic | 1.514 × 10⁷⁷ | 77.18 |
| **Effective** | **1.514 × 10⁷⁷** | **77.18** |

**The two bounds are exactly equal!** Computed ratio: 1.000000.

This is a fundamental result, verified analytically:
- S_Bek = 2π(2GM/c²)(Mc²)/(ℏc) = 4πGM²/(ℏc)
- S_holo = π(2GM/c²)²/l_P² = 4πG²M²/(c⁴l_P²) = 4πGM²/(ℏc) [since l_P² = Gℏ/c³]
- → They are identical when R = r_s. ✓

**Cross-check:** [CHECKED] Bekenstein-Hawking entropy S_BH ≈ 10⁷⁷ nats for solar-mass BH. Our value: 1.050 × 10⁷⁷ nats. ✓

**Classicality budget (full BH):** [COMPUTED]

| S_T (bits) | R_δ (max) | log₁₀(R_δ) |
|-----------|-----------|------------|
| 1 | 1.51 × 10⁷⁷ | 77.2 |
| 10⁶ | 1.51 × 10⁷¹ | 71.2 |

**Physical interpretation:** The BH saturates both entropy bounds — this is the maximum entropy configuration for a given radius. A solar-mass BH has a classicality budget of ~10⁷⁷ bits. This is the regime where the budget is most physically meaningful: the total information capacity is exactly at the bound. The budget constrains classical facts accessible to external observers, connecting to black hole complementarity questions.

---

### System 4: Observable Universe

**Parameters:**
- R = 4.4 × 10²⁶ m (comoving radius of observable universe)
- M ~ 10⁵³ kg (total mass-energy, rough estimate)
- E = Mc² ~ 8.988 × 10⁶⁹ J

**Entropy bounds:** [COMPUTED]

| Bound | Value (bits) | log₁₀ |
|-------|-------------|-------|
| Bekenstein | 1.134 × 10¹²³ | 123.05 |
| Holographic | 3.359 × 10¹²³ | 123.53 |
| **Effective** | **1.134 × 10¹²³** | **123.05** |

Tighter bound: Bekenstein (by a factor of ~3 — the bounds are remarkably close).

⚠️ **CAVEAT:** The cosmological application of the Bekenstein bound is contested. The bound was derived for isolated, weakly-gravitating systems in asymptotically flat spacetime. The observable universe is expanding, has no sharp boundary, and exists in curved spacetime. The Bousso covariant entropy bound is more appropriate for cosmological applications. However, the order of magnitude (~10¹²³) is consistent across formulations and with published estimates (e.g., Egan & Lineweaver 2010 give the cosmic event horizon entropy as ~2.6 × 10¹²² k_B ≈ 3.75 × 10¹²² bits).

**Classicality budget:** [COMPUTED]

| S_T (bits) | Description | R_δ (max) | log₁₀(R_δ) |
|-----------|-------------|-----------|------------|
| 1 | Minimal fact | 1.13 × 10¹²³ | 123.1 |
| 156 [ESTIMATED] | Star position to 1 AU | 7.26 × 10¹²⁰ | 120.9 |
| 10⁶ | A photograph | 1.13 × 10¹¹⁷ | 117.1 |

**Physical interpretation:** The universe has an absurdly large classicality budget. The total number of observable classical facts (~10²⁴ stars × ~100 bits = ~10²⁶ bits) is negligible compared to S_max ~ 10¹²³. The universe is deep in the "cheap classicality" regime. The near-equality of the two bounds (factor ~3) is notable — it reflects the cosmic coincidence that the Schwarzschild radius of the universe's mass is comparable to the Hubble radius.

---

### System 5: Planck-Scale Region

**Parameters:**
- R = l_P = 1.616 × 10⁻³⁵ m
- E = E_P = 1.956 × 10⁹ J (Planck energy)
- M = m_P = 2.176 × 10⁻⁸ kg

**Entropy bounds:** [COMPUTED] [CHECKED]

| Bound | Value (nats) | Value (bits) | log₁₀(bits) |
|-------|-------------|-------------|-------------|
| Bekenstein | 2π = 6.283 | 9.064 | 0.96 |
| Holographic | π = 3.142 | **4.532** | 0.66 |

**Analytic verification:** [CHECKED]
- S_Bek = 2π l_P E_P / (ℏc) = 2π(Gℏ/c³)^{1/2}(ℏc⁵/G)^{1/2}/(ℏc) = **2π nats** exactly ✓
- S_holo = πl_P²/l_P² = **π nats** exactly ✓
- Ratio S_Bek/S_holo = 2 exactly ✓

**This is the only system where the holographic bound is tighter.** The Bekenstein bound is exactly 2× the holographic bound at Planck scale.

**Classicality budget:** [COMPUTED]

| S_T (bits) | Description | R_δ (max) | Classical? |
|-----------|-------------|-----------|------------|
| 1 | Minimal fact | **3.53** | Barely — ~3 observers max |
| 2.27 | Critical fact size | **1.0** | Boundary — exactly 1 observer |
| 4.53 | Max fact size | **0** | No redundancy at all |
| 10 | A letter | **−0.55** | **Impossible** — S_T > S_max |

**Physical interpretation — THE KEY RESULT:**

At the Planck scale, the classicality budget is **almost zero**. With S_max ≈ 4.5 bits:

1. **A single bit of classical information** can be verified by at most ~3 independent observers. In quantum Darwinism terms, R_δ ≈ 3.5 — barely above the threshold for classical objectivity (which typically requires R_δ ≫ 1).

2. **The critical S_T = 2.27 bits.** A classical fact requiring more than ~2 bits can only be verified by a single observer — there's no room for independent confirmation.

3. **Facts requiring ≥ 5 bits cannot exist as classical facts at all.** R_δ < 0 means the information budget is exhausted before even a single redundant copy can be made.

4. **Classical reality in the quantum Darwinism sense cannot exist at the Planck scale** for any fact more complex than a few bits. This is consistent with the expectation that spacetime itself loses classical character at the Planck scale.

5. **The holographic bound gives exactly π nats per Planck area.** The informal statement "1 bit per Planck area" is approximate — the exact value is π/ln(2) ≈ 4.53 bits.

---

### System 6: Quantum Computer (1000 Trapped-Ion Qubits)

**Parameters:**
- R = 0.01 m (1 cm, trapped-ion register)
- M = 10⁻²² kg (1000 ions at ~10⁻²⁵ kg each, register only)
- E = mc² = 8.988 × 10⁻⁶ J
- Hilbert space dimension = 2¹⁰⁰⁰

**Entropy bounds:** [COMPUTED]

| Bound | Value (bits) | log₁₀ |
|-------|-------------|-------|
| Bekenstein | 2.577 × 10¹⁹ | 19.41 |
| Holographic | 1.735 × 10⁶⁶ | 66.24 |
| **Effective** | **2.577 × 10¹⁹** | **19.41** |

Tighter bound: Bekenstein (by 47 orders of magnitude).

**Critical comparison — Bekenstein vs. Hilbert space:** [COMPUTED]

| Quantity | Value |
|----------|-------|
| Bekenstein bound | 2.577 × 10¹⁹ bits |
| log₂(Hilbert dim) | 1000 bits |
| Ratio S_Bek / log₂(dim_H) | **2.577 × 10¹⁶** |

**The Bekenstein bound is ~10¹⁶ times larger than the Hilbert space log-dimension.** The qubit register uses only ~10⁻¹⁷ of its Bekenstein-allowed information capacity.

**Classicality budget:** [COMPUTED]

| S_T (bits) | Description | R_δ (max) | log₁₀(R_δ) |
|-----------|-------------|-----------|------------|
| 1 | Single output bit | 2.58 × 10¹⁹ | 19.4 |
| 100 | 100-bit output | 2.58 × 10¹⁷ | 17.4 |
| 10⁶ | Photograph-sized output | 2.58 × 10¹³ | 13.4 |

**Physical interpretation:**

1. **The classicality budget does not constrain quantum computation.** The register has room for 10¹⁹ bits of classical information, while quantum computation uses only 1000 qubits.

2. **Why the gap?** The Bekenstein bound counts ALL physical degrees of freedom — positions, momenta, internal electronic states, nuclear states, etc. — not just the computational qubit register. The 1000 qubits occupy a tiny subspace of the full Hilbert space.

3. **The budget constrains classical output, not quantum processing.** With R_δ ~ 10¹⁹ for a 1-bit output, ~10¹⁹ independent observers could each read out the same result. This is far more than sufficient.

4. **To make the budget constraining for QC**, you would need to encode information at near-Planck density — no foreseeable technology comes close.

---

## Sanity Checks

**All 7 checks passed.** ✓

| # | Check | Result |
|---|-------|--------|
| 1 | (R_δ + 1) × S_T = S_max for all systems | **PASS** — verified for all 28 (system, S_T) pairs |
| 2 | Planck scale gives R_δ ≈ 0 | **PASS** — S_max = 4.53 bits, R_δ = 3.53 for S_T=1, R_δ < 0 for S_T ≥ 10 |
| 3 | Observable universe R_δ astronomically large | **PASS** — R_δ = 1.13 × 10¹²³, log₁₀ ≈ 123 |
| 4 | Brain budget ≫ N_neurons | **PASS** — R_δ/N_neurons = 2.50 × 10³¹ |
| 5 | QC: S_Bek > Hilbert log-dim | **PASS** — S_Bek = 2.58 × 10¹⁹ ≫ 1000 bits |
| 6 | BH: Bekenstein = Holographic | **PASS** — ratio = 1.000000 (exact to machine precision) |
| 7 | BH entropy matches Bekenstein-Hawking | **PASS** — S_BH = 1.05 × 10⁷⁷ nats ≈ 10⁷⁷ (published value) |

---

## Key Physical Insights

### 1. The Bekenstein bound is tighter for ALL non-gravitational systems

For every system except the Planck-scale region, the Bekenstein bound determines S_max. The holographic bound is typically 25–50 orders of magnitude larger. The two bounds coincide *only* for black holes. This means the classicality budget for ordinary matter is determined by **energy content**, not **surface area**.

### 2. When Bekenstein = Holographic: the black hole condition

The bounds are equal when E = Rc⁴/(2G), i.e., R = 2GM/c² — the system is a black hole. This is the maximum entropy configuration for a given radius. Below this energy density, Bekenstein < Holographic.

### 3. The classicality budget spans ~122 orders of magnitude

From Planck scale (S_max ≈ 4.5 bits) to observable universe (S_max ≈ 10¹²³ bits). This is essentially the full dynamic range of physical scales.

### 4. Truly empty space has zero classicality budget

If E = 0, then S_Bek = 0, so R_δ = −1 for any S_T > 0. **No classical reality is possible in truly empty space.** Even a single photon (E ≈ 1 eV) in a 1 m³ region gives S_Bek ≈ 2.3 × 10⁷ bits — enough for millions of classical facts with high redundancy. But vacuum (E = 0) permits nothing. This is physically sensible: classical facts require matter/energy to encode and transmit them.

### 5. The multi-fact trade-off is the real constraint

R_δ ≤ (S_max / S_T) − 1 gives the budget for a *single* fact. For N_facts distinct facts:

> **N_facts × (R_δ + 1) × S_T ≤ S_max**
>
> → **R_δ ≤ S_max / (N_facts × S_T) − 1**

This is the generalized classicality budget. For the brain with N_facts = 10¹¹ (one per neuron) and S_T = 1 bit, R_δ ≤ 2.50 × 10³¹. Still enormous.

### 6. The critical S_T where R_δ = 1 (minimum objectivity)

| System | S_T_crit (bits) | Interpretation |
|--------|----------------|----------------|
| Lab | 6.44 × 10⁴² | No practical fact this large |
| Brain | 1.25 × 10⁴² | No practical fact this large |
| Solar BH | 7.57 × 10⁷⁶ | No practical fact this large |
| Universe | 5.67 × 10¹²² | No practical fact this large |
| **Planck** | **2.27** | **A ~2-bit fact hits the wall!** |
| QC | 1.29 × 10¹⁹ | No practical fact this large |

---

## Surprising or Problematic Results

### 1. ⚠️ The numbers are too large to be physically interesting for most systems

For all macroscopic systems, the classicality budget is so enormous (10⁴²–10¹²³) that it provides no useful constraint. The budget only becomes tight at the Planck scale. **Is the classicality budget physically meaningful for anything other than Planck-scale physics?**

Possible answers:
- The budget might become interesting near black hole horizons where actual entropy approaches S_max
- A more operationally relevant version might use thermally accessible entropy rather than the Bekenstein bound
- The budget tells us that classical reality is "cheap" — nature has an enormous surplus of information capacity relative to what's used for classicality

### 2. ⚠️ The Bekenstein bound may be too generous for quantum Darwinism

The Bekenstein bound counts ALL information capacity. But quantum Darwinism requires redundant encoding in the *accessible environment* — photons, air molecules, etc. The *operationally relevant* S_max might be the thermal/environmental entropy, not the Bekenstein bound. For the brain: Bekenstein gives ~10⁴² bits, but thermal entropy is ~10²⁵ bits. The qualitative picture doesn't change (both are ≫ neural complexity), but the quantitative picture would shift significantly for systems closer to their limits.

### 3. ✓ The Planck-scale result is physically elegant

S_max ≈ 4.5 bits at Planck scale, with R_δ ≈ 3.5 for minimal facts, naturally explains why classicality fails at the Planck scale without any ad hoc assumptions. This is the most physically meaningful prediction of the classicality budget.

### 4. ✓ Holographic bound gives π nats, not "1 bit," per Planck area

The informal "1 bit per Planck area" is often quoted but the exact holographic result at R = l_P is π/ln(2) ≈ 4.53 bits. The factor of ~4.5 doesn't change the qualitative picture but matters for precise statements.

### 5. ⚠️ Observable universe bounds are close (factor ~3)

S_Bek/S_holo ≈ 0.34 for the observable universe — the bounds are within a factor of 3. This reflects the cosmic coincidence that the Schwarzschild radius of the universe's total mass (~10²⁶ m) is comparable to the Hubble radius (~10²⁶ m). The observable universe is "information-theoretically close" to being a black hole. However, applying entropy bounds cosmologically is fraught with assumptions.

### 6. ✓ No absurd results found — the budget is internally consistent

All numbers are physically sensible. The budget gracefully interpolates from "impossibly tight" (Planck) through "irrelevantly generous" (everyday) to "astronomically generous" (cosmological). This consistency suggests the formula R_δ ≤ S_max/S_T − 1 is at least dimensionally and physically correct, even if its derivation needs further scrutiny.

---

## S_T Reference Table

For calibration, S_T estimates for common classical facts: [ESTIMATED]

| Classical Fact | S_T (bits) |
|---------------|-----------|
| Binary choice (yes/no) | 1 |
| Element identity (118 elements) | 6.9 |
| ASCII character | 7 |
| Temperature (300K range, ±1K) | 8.2 |
| Human face (~10⁴ faces) | 13.3 |
| Position in 1m³ to 1mm | 29.0 |
| Position in 1m³ to 1μm | 58.9 |
| Position in 1m³ to 1nm | 88.8 |
| Star position to 1 AU in observable universe | 156 |
| Book (~500 pages) | ~10⁷ |
| Photograph (1 Mpix, 24-bit color) | ~2.4 × 10⁷ |

---

## Plots

Two plots generated and saved to `code/`:

1. **`classicality_budget_plot.png`** — R_δ vs S_T on a log-log plot for all 7 system variants. Shows budget curves as parallel lines (slope −1 in log-log), offset by each system's S_max. The R_δ = 1 threshold is marked as a red dashed line. The Planck-scale curve crosses this threshold at S_T ≈ 2.3 bits.

2. **`entropy_bounds_comparison.png`** — Bar chart comparing Bekenstein, holographic, and effective bounds across all systems. Highlights how Bekenstein dominates for ordinary matter while both bounds converge at the black hole.

---

## Code and Reproducibility

All scripts saved to `code/`:

- **`classicality_budget.py`** — Main computation. Computes all entropy bounds, classicality budgets, and sanity checks. Outputs `results.json`.
- **`verification.py`** — Cross-checks against published values, computes multi-fact trade-offs, and derives additional physical insights.
- **`plot_budget.py`** — Generates log-log and bar chart plots.
- **`results.json`** — Raw numerical results for downstream use.

To reproduce: `cd code/ && python3 classicality_budget.py && python3 verification.py && python3 plot_budget.py`
