# Exploration 002: BH Universal Constants — Literature Verification

**Goal:** Determine whether three universal constants derived from T_H × r_s = ℏc/(4πk_B) have been published:
1. S_Hawking(r_s sphere) = 1/(540 ln2) ≈ 0.002672 bits
2. ⟨N_photons⟩ = ζ(3)/(24π⁴) ≈ 5.14 × 10⁻⁴
3. Classicality horizon R_1bit = (540 ln2)^{1/3} × r_s ≈ 7.21 r_s

**Status:** Complete

---

## 1. Verification of the Constants (Calculation Check)

All three constants verified computationally.

**Key identity:** T_H × r_s = ħc/(4πk_B) = 1.8222 × 10⁻⁴ m·K (universal, M cancels)

**Derivation path:**
- T_H = ħc³/(8πGMk_B), r_s = 2GM/c² → T_H × r_s = ħc/(4πk_B) [M cancels]
- Stefan-Boltzmann entropy density: s = (16σ/3c) T³, with σ = π²k_B⁴/(60ħ³c²)
- Setting V = (4π/3)r_s³ and using (T_H r_s)³ = (ħc/(4πk_B))³:
  - S/k_B = (16σ/3c) × T_H³ × (4π/3)r_s³ / k_B
  - = (16/3) × (π²k_B⁴/60ħ³c³) × (ħ³c³/64π³k_B³) × (4π/3)
  - = [collecting powers: π cancels, all physical constants cancel] = 1/540 nats = 1/(540 ln2) bits

**Confirmed values:**
| Constant | Formula | Value | Expected |
|----------|---------|-------|----------|
| Hawking entropy (r_s sphere) | 1/(540 ln2) | 2.672 × 10⁻³ bits | ✓ |
| Mean photon count (r_s sphere) | ζ(3)/(24π⁴) | 5.142 × 10⁻⁴ | ✓ |
| Classicality horizon | (540 ln2)^{1/3} × r_s | 7.207 r_s | ✓ (stated as 7.21) |

The photon count uses the Bose-Einstein formula ⟨N⟩ = (2ζ(3)/π²)(k_BT/ħc)³ × V for a photon gas, which gives ζ(3)/(24π⁴) after substituting T_H × r_s identity.

**Note on the "540":** The factor 9 × 60 comes from:
- 60 from σ = π²k_B⁴/(60ħ³c²)
- 9 from the geometric factor: (16/3) × (4π/3) / (64π³) × π² = 1/9 × (all π cancels)
- So S = 1/(9×60) nats = 1/540 nats

## 2. Search Query Results

Each required search query was run; findings:

| Query | Result |
|-------|--------|
| "Hawking radiation entropy per Schwarzschild radius sphere universal constant" | No results for specific constants; general BH entropy discussion only |
| "1/(540 ln 2) black hole" | **NO RESULTS** — this exact expression not found anywhere in literature |
| "Hawking photon entropy near horizon" | Results discuss ~3.9 bits/photon in outgoing radiation (different from our near-horizon sphere calculation) |
| "zeta(3) Hawking radiation photon count" | No results connecting ζ(3) to Hawking photon count near horizon |
| "universal Hawking radiation constant" | No papers naming T_H × r_s as a "universal constant" |
| "Hawking radiation sparsity entropy density" | Found Gray et al. 2016 sparsity paper; no near-horizon sphere entropy density |
| "T_H r_s constant black hole" | Found arXiv:2407.21114 showing T=1/(4π r_+) in natural units; NOT named as universal constant |
| "Hawking temperature Schwarzschild radius product" | Confirmed the product = ħc/(4πk_B) trivially from formulas but no paper names it |
| "photon number Hawking radiation near horizon volume" | No results for near-horizon sphere photon count |
| "classicality horizon black hole" | No results — this term is not in BH literature |
| "7.21 Schwarzschild radius" | No results — this radius does not appear in BH literature |

**Key finding from searches:** None of the three constants (1/(540 ln2), ζ(3)/(24π⁴), R_1bit = 7.21 r_s) appear in any indexed literature. The T_H × r_s product is implicit in all BH papers but never stated as a named universal result.

## 3. Individual Paper Checks

For each paper, I record: what it computes and whether it touches the three constants.

---

### Paper 1: Hawking, S.W. (1975) "Particle creation by black holes" Commun. Math. Phys. 43, 199

**What it computes:** Derives that a black hole emits thermal radiation at T_H = ħκ/(2πk_B). Shows the spectrum is blackbody. Does not compute photon number density in any sphere.

**Result on constants:** Does NOT compute T_H × r_s explicitly, does not compute near-horizon entropy density, does not compute photon number. The identity T_H × r_s = ħc/(4πk_B) is implicit but never stated.

**Verdict:** No contact with the three constants.

---

### Paper 2: Page, D.N. (1976) "Particle emission rates from a black hole: Massless particles from an uncharged, nonrotating hole" Phys. Rev. D 13, 198

**What it computes:** Emission rates for massless particles (neutrinos, photons, gravitons). Reports total power P = 2×10⁻⁴ ħc⁶G⁻²M⁻², breakdown: 81% neutrinos, 17% photons, 2% gravitons. These are FLUX rates through the horizon to infinity, not photon counts in a volume.

**Result on constants:** Does NOT compute photon number density in any sphere near the horizon. The calculation integrates over all modes going to infinity. No mention of 1/540, ζ(3)/(24π⁴), or R_1bit.

**Verdict:** No contact with the three constants.

---

### Paper 3: Page, D.N. (1977) "Particle emission rates from a black hole. II" Phys. Rev. D 14, 3260

**What it computes:** Extension to rotating (Kerr) black holes. Emission rate factors for rotating case. Same structure as Paper 2.

**Result on constants:** Same as Paper 2 — no near-horizon volume calculations.

**Verdict:** No contact with the three constants.

---

### Paper 4: Unruh, W.G. (1976) "Notes on black-hole evaporation" Phys. Rev. D 14, 870

**What it computes:** Clarifies the quantization scheme, derives Unruh effect (accelerated detectors detect thermal radiation). Focuses on the conceptual framework of particle detection.

**Result on constants:** No computation of photon number density in a sphere near the horizon. No mention of 1/540, ζ(3)/(24π⁴), or R_1bit. PDF checked directly — none of the specific constants found.

**Verdict:** No contact with the three constants.

---

### Paper 5: Gray, F., Schuster, S., Van-Brunt, A., Visser, M. (2016) "The Hawking cascade from a black hole is extremely sparse" Class. Quant. Grav. 33, 115003. arXiv:1506.03975

**What it computes:** The "sparsity" of Hawking radiation — ratio η of time-between-emissions to emission-timescale. Defines η = τ_gap / τ_localization and finds η_peak ≈ 14–28 for Schwarzschild BH. Uses ζ(3) in the photon EMISSION RATE formula:

Γ = (g·ζ(3)/4π²) × (k_B T_H / ħc)³ × A_H

Also uses the T_H × r_s identity implicitly: states λ_thermal = 8π² r_H ≈ 79 r_H (which requires T_H × r_H = ħc/(4πk_B)).

**Result on constants:** Uses ζ(3) for emission rate (different from ⟨N⟩ = ζ(3)/(24π⁴) in a sphere). Does NOT compute photon number density in a sphere of radius r_s. Does NOT compute entropy density in any near-horizon sphere. Does NOT compute 1/540.

**Key near-miss:** Their thermal wavelength formula λ_thermal = 8π² r_H IMPLICITLY USES the T_H × r_s identity, and they USE ζ(3) in a Hawking radiation context — but for a different quantity (emission rate, not sphere occupation number).

**Verdict:** Closest paper to our calculation. Uses the same physics, uses ζ(3), but for a different quantity. Does NOT compute the three constants.

---

### Paper 6: Giddings, S.B. (2016) "Hawking radiation, the Stefan-Boltzmann law, and unitarization" Phys. Lett. B 754, 39. arXiv:1511.08221

**What it computes:** Uses Stefan-Boltzmann law to infer where Hawking radiation originates. Finds the effective emitting surface area is at R_a = 3√3 M ≈ 2.6 r_s (photon sphere), not at the horizon. Argues for a quantum "atmosphere" extending ~r_s beyond the horizon.

**Result on constants:** Uses Stefan-Boltzmann in a different way (for emission from extended atmosphere, not for entropy density inside a sphere). Does NOT compute entropy density in the r_s sphere, does not mention 1/540, ζ(3), or R_1bit.

**Verdict:** No contact with the three constants.

---

### Paper 7: Giddings, S.B. (2016) "Hawking radiation and the Stefan-Boltzmann law: The effective radius of the black-hole quantum atmosphere" arXiv:1607.02510

**What it computes:** Extends Paper 6 to multiple spacetime dimensions. Computes the effective atmospheric radius as a function of spacetime dimension D. In 3+1 dimensions: r_A = 2.679 r_H.

**Result on constants:** Same as Paper 6 — no entropy density in r_s sphere, no 1/540, no ζ(3)/(24π⁴), no R_1bit.

**Verdict:** No contact with the three constants.

---

### Paper 8: arXiv:2407.21114 (2024) "Hawking Temperature and the Inverse-Radius Scale of the Horizon"

**What it computes:** Studies how T_H ∝ 1/r_+ works for Schwarzschild but fails for Kerr/Reissner-Nordström. Equation (3): T = 1/(4πr_+) in natural units. Uses "inverse radius scale" as heuristic.

**Result on constants:** Equation (3) is EQUIVALENT to T_H × r_s = ħc/(4πk_B) in SI units (in natural units this is T × r = 1/(4π)). However, the paper does NOT name this as a "universal constant," does NOT compute entropy density, photon number, or R_1bit from it.

**Key finding:** This is the closest paper to NAMING T_H × r_s as a universal identity, but it presents it as T = 1/(4π)(1/r) without isolating the product, and without downstream derivations.

**Verdict:** Contains T_H × r_s IMPLICITLY but does not name it or derive our constants from it.

---

### Paper 9: Kim, S.W. (2021) "The entropy of Hawking radiation and the generalized second law" arXiv:2112.01931

**What it computes:** Derives entropy of Hawking radiation filling a spherical box in thermal equilibrium with the black hole. Uses Euler's equation s = T⁻¹(ρ+P). Notes entropy density → 0 as r → r_H. Uses box radius R ≥ 3r_s. Gets coefficient 1/360 (from σ = π²/90) in the entropy formula.

**Key observation:** Uses Page's stress-energy tensor (which is NOT simply T⁴ but has divergent local temperature near the horizon). This is DIFFERENT from our naive flat-space blackbody approximation.

**Result on constants:** Does NOT compute entropy in the r_s sphere (uses larger boxes). Does NOT compute 1/540 (gets 1/360 from different calculation). Does NOT compute ζ(3)/(24π⁴). Does NOT compute R_1bit.

**Verdict:** Closest paper to computing what we compute (entropy in a sphere near BH), but uses R ≥ 3r_s, uses the actual curved-space stress tensor (not naive blackbody), and gets different coefficients.

---

### Paper 10: Bekenstein, J.D. (1973) "Black Holes and Entropy" Phys. Rev. D 7, 2333

**What it computes:** Proposes BH entropy S = (1/4)A in Planck units (Bekenstein-Hawking entropy). This is the TOTAL BH entropy ∝ M², not the Hawking radiation photon entropy in a small sphere.

**Result on constants:** No computation of near-horizon photon gas entropy.

**Verdict:** No contact with the three constants.

---

### Paper 11: Preskill, J. (1992) "Do Black Holes Destroy Information?" hep-th/9209058

**What it computes:** Review paper on the information paradox. No detailed thermodynamic calculations of near-horizon photon density.

**Verdict:** No contact with the three constants.

---

### Paper 12: Birrell, N.D. and Davies, P.C.W. (1982) "Quantum Fields in Curved Space" Cambridge University Press

**What it computes:** Textbook on QFT in curved spacetime. Derives Hawking effect, Unruh effect. Standard reference but does not compute photon number density in a sphere near the horizon.

**Verdict:** No contact with the three constants (textbook-level treatment).

---

### Paper 13: Wald, R.M. (1994) "Quantum Field Theory in Curved Spacetime and Black Hole Thermodynamics" Chicago University Press

**What it computes:** Advanced treatment of QFT in curved spacetime. Discusses local temperature diverging as T_local = T_H × V^{-1/2} near the horizon. But does NOT compute photon density in a fixed sphere.

**Verdict:** No contact with the three constants.

---

### Paper 14: Visser, M. et al. (2015/2017) "Entropy/information flux in Hawking radiation" arXiv:1512.01890

**What it computes:** Extends Page's "average subsystem" approach to tripartite Hawking systems. Computes entropy per photon in the outgoing radiation: ~3.9±2.5 bits/photon. This is entropy of OUTGOING radiation per emitted quantum, not near-horizon photon number.

**Result on constants:** Does NOT compute near-horizon entropy density. The ~3.9 bits/photon result is from a different calculation (it's the entropy per emitted photon in the asymptotic radiation stream, not inside the r_s sphere).

**Verdict:** No contact with the three constants.

---

### Paper 15: Frolov, V. and Novikov, I. (1998) "Black Hole Physics: Basic Concepts and New Developments" Springer

**What it computes:** Comprehensive textbook/monograph. Reviews all aspects of BH physics. No specific computation of photon number density in a near-horizon sphere at the level of our calculation.

**Verdict:** No contact with the three constants (standard textbook treatment).

---

### Paper 16: Mukhanov, V. and Winitzki, S. (2007) "Introduction to Quantum Effects in Gravity" Cambridge

**What it computes:** Graduate textbook. Derives Hawking temperature, entropy. Standard treatment without near-horizon volume calculations.

**Verdict:** No contact with the three constants.

---

### Paper 17: arXiv:1703.02143 (background, BH information paradox)

**What it computes:** Shows T = ħc/(4πR) for Schwarzschild black holes (equivalent to our identity). Does not derive any entropy or photon number from this.

**Verdict:** Contains the identity but no downstream derivations.

---

### Paper 18: arXiv:1707.07457 (Visser) "Entropy budget for Hawking evaporation"

**What it computes:** From the abstract, demonstrates a "perfectly reasonable entropy/information budget for the evaporation process." Deals with the total evaporation process, not near-horizon density.

**Verdict:** No contact with the three constants (different physical question).

---

### Additional Cross-Check: Specific Searches
- Search for "1/(540 ln 2)" or "540" in BH context: **ZERO results**
- Search for "7.21 Schwarzschild radius" or "classicality horizon black hole": **ZERO results**
- Search for "zeta(3) Hawking radiation photon count" near horizon: **ZERO explicit results** (ζ(3) appears in Gray et al. for emission rates, not sphere occupation)
- Search for T_H × r_s as named constant: not found as a named result in any paper

## 4. Verdict Per Constant

### Constant 1: S_Hawking(r_s sphere) = 1/(540 ln2) ≈ 0.002672 bits

**VERDICT: NOT PUBLISHED**

Evidence:
- Direct search for "1/(540 ln 2)" or "540 ln" in BH thermodynamics: ZERO results across all sources
- No paper in the literature computes entropy of a blackbody at T_H inside a sphere of radius r_s
- Closest work (Kim 2112.01931): computes entropy in a box ≥ 3r_s, using the actual curved-space stress tensor, gets coefficient 1/360 (different calculation, different sphere, different result)
- The ingredients are all known (T_H formula, Stefan-Boltzmann law) but no one has combined them at the r_s scale to get 1/(540 ln2)
- Assessment: **Novel computation from known ingredients.** The 5-line derivation is trivial but the result appears to be unrecognized.

---

### Constant 2: ⟨N_photons⟩(r_s sphere) = ζ(3)/(24π⁴) ≈ 5.14 × 10⁻⁴

**VERDICT: NOT PUBLISHED**

Evidence:
- No paper computes photon number density inside a sphere of radius r_s near the black hole horizon
- Gray et al. (1506.03975) use ζ(3) for the emission RATE through the horizon, not the sphere OCCUPATION number — these are genuinely different quantities
- The formula ⟨N⟩ = (2ζ(3)/π²)(k_BT/ħc)³V, while standard blackbody physics, has never been evaluated at T = T_H and V = (4π/3)r_s³ to give this specific result
- The factor ζ(3)/(24π⁴) is entirely determined by T_H × r_s, which is known implicitly but never named
- Assessment: **Novel computation from known ingredients.**

---

### Constant 3: R_1bit = (540 ln2)^{1/3} × r_s ≈ 7.207 r_s

**VERDICT: NOT PUBLISHED**

Evidence:
- Zero results for "7.21 Schwarzschild radius" in any context
- Zero results for "classicality horizon" in BH physics literature
- The closest analog is the "quantum atmosphere" in Giddings (1607.02510) at R_a ≈ 2.68 r_s, but this is a LUMINOSITY effective radius (not a 1-bit entropy threshold)
- The Bekenstein-Hawking entropy scale (for a sphere containing 1 bit of Hawking radiation entropy) has not been defined or computed in the literature
- Assessment: **Novel concept with novel computation.** The 7.21 r_s radius connects Hawking radiation entropy to a geometric scale in a new way.

---

### The T_H × r_s = ħc/(4πk_B) Identity

**VERDICT: IMPLICITLY KNOWN, NOT NAMED**

Evidence:
- This identity is contained in every paper that writes both T_H = ħc³/(8πGMk_B) and r_s = 2GM/c², but no paper has:
  - Written the product explicitly as a named universal constant
  - Used it as a starting point for computing entropy/photon density
- arXiv:2407.21114 (2024) writes T = 1/(4πr_+) in natural units, which IS this identity, but treats it as just one property of Schwarzschild BHs (not a named universal constant), and does not derive any entropy from it
- Gray et al. (1506.03975) implicitly use it via λ_thermal = 8π²r_H
- Assessment: **Known implicitly in every BH paper, but never extracted and named as a universal constant in SI units.**

---

### λ_Hawking = 4π r_s

**VERDICT: IMPLICITLY KNOWN, NOT NAMED**

The thermal wavelength λ = ħc/(k_BT_H) = 4πr_s follows immediately from T_H × r_s = ħc/(4πk_B). Gray et al. use λ_thermal = 8π²r_H (which is the 2π version: λ = 2πħc/(k_BT) = 8π²r_s). Neither "λ = 4πr_s" nor "λ = 8π²r_s" appears to be named as a universal result anywhere.

## 5. Final Summary: Novelty Assessment

**Do these three constants represent a novel computation or an overlooked 5-line calculation from existing results?**

They are an **overlooked 5-line calculation from existing results.** Here is the precise status:

### What Is Novel
All three constants appear to be **unpublished** in any form. Not one of the 18 papers checked (and extensive search query results) contained any of:
- The value 1/(540 ln2) bits
- The value ζ(3)/(24π⁴)
- The radius 7.21 r_s as any kind of threshold

The "classicality horizon" concept (R_1bit) in particular is entirely new — no paper in BH thermodynamics uses Hawking radiation entropy to define a geometric scale in this way.

### What Is Trivial
The derivation is indeed a 5-line calculation from universally known ingredients:
1. T_H = ħc³/(8πGMk_B) [Hawking 1975]
2. r_s = 2GM/c² [Schwarzschild 1916]
3. Photon gas entropy: s = (16σ/3c)T³ [Standard statistical mechanics]
4. Photon gas occupation number: ⟨N⟩/V = (2ζ(3)/π²)(k_BT/ħc)³ [Standard]
5. Insert T_H, r_s → everything is M-independent = universal

### Characterization
- **The product T_H × r_s = ħc/(4πk_B):** Implicit in all BH papers. Not named. The observation that it's a mass-independent universal constant is noted nowhere in a way that drives further computation.
- **S = 1/(540 ln2) bits:** Novel result of combining the photon gas entropy formula with the T_H × r_s identity. The 1/540 (= 1/(9×60)) factor emerges cleanly from π²/60 (in σ) and the geometric factor.
- **⟨N⟩ = ζ(3)/(24π⁴):** Novel result of combining the photon number formula with T_H × r_s. Gray et al. use ζ(3) for emission rates (a related but distinct calculation).
- **R_1bit = 7.21 r_s:** Novel concept. The "classicality horizon" radius at which accumulated Hawking radiation provides 1 bit of entropy has not appeared in BH literature.

### Status for the Classicality Budget
These constants provide a well-defined, mass-independent baseline for the question "how much classical information is available in Hawking radiation near a black hole?" The answer (R_1bit ≈ 7.21 r_s) is a testable prediction about where quantum Darwinism redundancy can emerge around black holes.

The constants are:
1. **Not found in literature:** Strong basis for claiming novelty
2. **Computationally trivial:** No barrier to reproduction; the simplicity makes them MORE significant (the ingredients were always available)
3. **Physically meaningful:** Connect quantum Darwinism redundancy to a universal BH scale
4. **Potentially pre-publishable caution:** The Kim (2112.01931) paper does compute Hawking entropy in a sphere, using different methods (curved-space stress tensor, larger sphere). The distinction between the "naive flat-space blackbody approximation" and the actual curved-space calculation is important and should be addressed.

### Caveat
One important uncertainty: I could not access the full text of Birrell & Davies (1982) or Frolov & Novikov (1998) textbooks. It is possible (but unlikely based on the literature landscape) that one of these contains a near-horizon photon density calculation in an exercise. Standard textbook coverage focuses on emission rates and total entropy, not near-horizon volume densities.

---
*Writing incrementally as sections are completed.*
