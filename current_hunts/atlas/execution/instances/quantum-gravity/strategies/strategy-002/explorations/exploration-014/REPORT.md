# Exploration 014: Gravitational Wave and Non-CMB Experimental Signatures of QG+F

## Goal
Identify and assess experimental signatures of QG+F (quadratic gravity with fakeon prescription) beyond the CMB sector. Focus on: gravitational waves, table-top experiments, cosmological signatures beyond CMB, microcausality violation signatures, and experimental timeline/priority ranking.

## Context
From prior explorations:
- QG+F's CMB predictions are tightly defined (r < 0.005, n_s ≈ 0.964-0.967) but nearly indistinguishable from Starobinsky (Exp-010)
- BH predictions are unobservable — all corrections exp(-10⁵⁰) suppressed for astrophysical BHs (Exp-011)
- SM connections are primarily non-perturbative (Higgs mass from AS boundary condition) (Exp-012)
- Six-derivative extension shifts predictions slightly (n_s → 0.974, r → 0.0045) but adds no qualitatively new signatures (Exp-008)

**The question: Are there ANY testable signatures outside the CMB?**

---

## Task 1: Gravitational Wave Signatures

### 1.1 Scalar Mode (Spin-0 from R²)

The R² term in the QG+F action produces a massive scalar mode (the scalaron) with mass M₀. In the Stelle potential, this appears as a Yukawa attraction:

V(r) = -G·m₁·m₂/r · [1 + (1/3)·e^(-M₀·r) - (4/3)·e^(-M₂·r)]

The scalar mode is a **physical particle** in QG+F (unlike the spin-2 ghost, which is a fakeon). It can in principle source gravitational waves with scalar (breathing) polarization.

**Key issue for GW detection:** The scalaron mass M₀ is related to the inflation scale. From Starobinsky inflation, M₀ ~ 3×10¹³ GeV (the inflaton mass). At this mass, the Compton wavelength is λ₀ ~ 1/M₀ ~ 10⁻²⁷ m — far below any conceivable detection scale.

**However:** If M₀ were much lighter (as in some f(R) dark matter models where M₀ ~ 10⁻²² eV), it could produce observable effects. But in QG+F with the standard inflationary identification, M₀ is pinned to the inflation scale.

**Verdict: NOT DETECTABLE** with GW observatories. The scalar mode mass is too high for any astrophysical process to produce it in abundance, and its Compton wavelength is ~10⁻²⁷ m.

### 1.2 Modified Dispersion Relations

In quadratic gravity, the graviton propagator has poles at k² = 0 (massless graviton), k² = M₂² (massive spin-2), and k² = M₀² (massive scalar). For the massless graviton, the dispersion relation is **unchanged** from GR: ω = |k|·c.

The massive modes have the standard massive dispersion relation: ω² = k² + M². Since M₂, M₀ are near the Planck scale, these modes:
- Propagate subluminally (group velocity v_g = k/√(k²+M²) < c)
- Are only produced at Planck energies
- Cannot propagate macroscopic distances

**Massless-massive graviton oscillation:** In analogy with neutrino oscillations, there is a mixing between the massless graviton and the massive modes. In bigravity/quadratic gravity, this mixing would cause the GW amplitude to oscillate as a function of distance, with an oscillation length L_osc ~ E/M². For M ~ M_Planck and E ~ 100 Hz (LIGO), L_osc ~ 10⁻⁶⁰ m — unobservably tiny.

**LVK modified dispersion tests:** The LVK collaboration tests for modified dispersion relations parameterized as E² = p²c² + A·p^α·c^α. Current bounds constrain A at various values of α. For QG+F, the corrections would enter at the Planck scale, far beyond current sensitivity. Recent improvements (arXiv:2511.00497, 2025) extend these tests to group velocity parametrization and negative exponents, but still cannot reach Planck-scale effects.

**Verdict: NOT DETECTABLE.** The dispersion modification is at the Planck scale, suppressed by (E/M_Planck)² ~ 10⁻⁸⁰ for LIGO frequencies.

### 1.3 Scalar GW Polarization

General metric theories allow up to 6 GW polarization modes:
- 2 tensor (+ and ×) — standard GR
- 2 vector (x and y)
- 2 scalar (breathing and longitudinal)

QG+F predicts **additional modes** from the massive scalar (breathing mode) and the massive spin-2 (all 5 helicities). However, under the fakeon prescription, the massive spin-2 is **purely virtual** — it does not propagate as an asymptotic state.

**What survives:**
- The 2 standard tensor modes ✓
- The massive scalar breathing mode (but only if M₀ is light enough to be produced)
- The spin-2 fakeon does NOT produce a real GW polarization mode

Since M₀ ~ 10¹³ GeV in QG+F, the scalar mode is far too heavy to be sourced by any astrophysical process. No additional polarization modes are expected at LIGO/LISA frequencies.

**Detection prospects for extra polarizations (from recent literature):**
- Current LIGO+Virgo+KAGRA network can distinguish tensor from scalar modes
- Einstein Telescope excels for vector modes; LIGO for scalar modes (arXiv:2506.02909, 2025)
- Space-based LISA, TianQin, Taiji being studied for polarization tests
- But all require the extra modes to actually be present at observable frequencies — in QG+F they are not

**Verdict: NOT DETECTABLE.** No extra GW polarization modes at observable frequencies.

### 1.4 BH Merger Ringdown and QNM Spectrum

This is the **most studied** GW signature for quadratic gravity.

**Key result (arXiv:2412.15037, March 2025):** Gravitational QNMs of BHs in quadratic gravity have been computed. The Schwarzschild solution admits:
1. All standard GR QNMs (unchanged)
2. **New classes of QNM modes from the massive spin-2 field** with mass μ = 1/√(2α)

These massive spin-2 QNMs exist even when the BH solution is the same as in GR (Schwarzschild). The dimensionless parameter is p = r_h · μ. Hairy (non-GR) BH solutions exist for 0.876 ≲ p ≲ 1.143.

**Energy partitioning:** The massive spin-2 mode carries more energy than the spin-0 mode in gravitational wave emission (Nature Scientific Reports, 2023). This means if detectable, the spin-2 signature would dominate.

**First ringdown constraints from LVK data (arXiv:2506.14695, June 2025):**
- First GW ringdown constraints on quadratic-gravity theories
- Analyzed GW150914, GW190521, GW200129
- 90% C.I. bounds on coupling length scales: ℓ < 34-49 km (depending on variant)
- Signal-to-noise in ringdown only: ≲7

**The fakeon complication:** Under the fakeon prescription, the massive spin-2 is purely virtual. Whether it contributes to QNM ringdown is subtle:
- QNMs are quasi-bound modes that decay — they are NOT asymptotic states
- The fakeon modifies the propagator in the complex plane
- In principle, the ghost could contribute to the Green's function determining ringdown
- But practically: from Exp-011, all QG+F corrections are suppressed by exp(-M₂·r_h) ~ exp(-10⁵⁰) for astrophysical BHs when M₂ ~ M_Planck

**Verdict: NOT DETECTABLE in QG+F** with M₂ ~ M_Planck. The massive spin-2 QNMs would have frequencies ω ~ M₂ ~ M_Planck, entirely outside any detection band. The existing LVK ringdown constraints (ℓ < 40 km → M₂ > 5×10⁻¹² eV) are ~40 orders of magnitude weaker than QG+F's expected M₂.

### 1.5 Six-Derivative Extension GW Signatures

The six-derivative extension adds Lee-Wick complex-mass pairs: two massive spin-2 and two massive spin-0 modes (14 DOF total vs 8 in QG+F). The complex masses mean the modes both oscillate and decay.

**New features relative to four-derivative QG+F:**
- Lee-Wick particles may form composite bound states (explored in scalar toy models)
- Additional QNM families from the extra massive modes
- Complex-mass poles produce interference patterns in amplitudes
- But again, all masses are near the Planck scale

**Verdict: NOT DETECTABLE.** Same Planck-scale suppression applies.

### Task 1 Summary

**All gravitational wave signatures of QG+F are undetectable.** The fundamental problem is that all new degrees of freedom (massive spin-2, massive spin-0) have masses at or near the Planck/inflation scale. No astrophysical process produces these modes, and their effects on GW propagation are suppressed by factors of (E/M_Planck)² ~ 10⁻⁸⁰.

---

## Task 2: GQuEST and Table-Top Experiments

### 2.1 GQuEST Experiment

**What GQuEST measures:** GQuEST (Gravity from the Quantum Entanglement of Space-Time) is a tabletop Michelson interferometer at Fermilab, designed to detect "geontropic spacetime fluctuations." Published in Phys. Rev. X 15, 011034 (Feb 2025).

**The geontropic model (Verlinde-Zurek):** Proposes that quantum gravity produces fluctuations in spacetime geometry from entanglement entropy. A scalar field (the "pixellon" ϕ) represents these fluctuations, modifying the metric as:

ds² = -dt² + (1-ϕ)(dr² + r²dΩ²)

Predicted RMS fluctuations: ⟨δL²⟩ ≈ α · (5.7×10⁻¹⁸ m)² · (L/5m), where α ~ O(1).

**Detection method:** Novel photon-counting readout that bypasses the standard quantum limit, enabling measurement times 100× shorter than conventional interferometers. For α=1: 5σ detection in ~10⁵ s (~1-2 days). Extends beyond the Fermilab Holometer (which constrained α ≲ 0.1).

**Can GQuEST test QG+F? NO.**

GQuEST tests holographic spacetime fluctuations — a qualitatively different prediction from QG+F:
- QG+F is a perturbative QFT on a classical background — no pixellon field, no spacetime "fuzziness"
- QG+F's modifications are at the Planck scale (~10⁻³⁵ m), 17 orders of magnitude below GQuEST's sensitivity (~10⁻¹⁸ m)
- The geontropic model is closer to holographic/entropic gravity approaches (Verlinde), conceptually distinct from QG+F

**A null result from GQuEST would be consistent with QG+F** (which predicts no such fluctuations). A positive result would be evidence AGAINST QG+F.

**Verdict: NOT RELEVANT to QG+F.**

### 2.2 Gravity-Induced Entanglement (BMV)

**The BMV proposal (Bose 2017, Marletto-Vedral 2017):** Two massive particles in spatial superposition interact gravitationally. If gravity mediates entanglement, it implies gravity is quantum.

**Recent developments (2024-2025):**
- Nanodiamond interferometers with NV centers as implementation (arXiv:2410.19601, Oct 2024)
- Theoretical debate: some semi-classical theories may also produce entanglement (arXiv:2510.20991, Oct 2025)
- New proposal without requiring observable spacetime superpositions (arXiv:2506.21122, June 2025)

**Can BMV distinguish QG+F from other QG theories? NO.**

BMV tests whether gravity is quantum at all — a binary yes/no question. QG+F predicts YES (it is a quantum field theory of gravity), but so do ALL quantum gravity theories (string theory, LQG, etc.). At BMV experimental energies (E ≪ M₂), only the massless graviton mediates the interaction. The fakeon and scalaron do not contribute. The BMV result is identical in QG+F and standard quantum GR.

**Verdict: NOT DISCRIMINATING.** BMV tests quantum gravity vs classical gravity, not QG+F vs alternatives.

### 2.3 Short-Range Gravity Tests (Yukawa Bounds)

**The Stelle potential** predicts Yukawa corrections to Newton's law:

V(r) = -G·m₁·m₂/r · [1 + (1/3)·e^(-M₀·r) - (4/3)·e^(-M₂·r)]

**Current experimental bounds:**
- Eöt-Wash torsion pendulum: |α| ≤ 1 down to λ = 48 μm (95% C.L.) [PRL 124, 051301 (2020)]
- No deviation from 1/r² at submillimeter scales
- New Josephson effect proposal for mm-scale quantum gravity tests (Nature Scientific Reports, 2024)

**What this means for QG+F:**
- The Yukawa ranges are 1/M₀ ~ 7×10⁻²⁸ m and 1/M₂ ~ 10⁻³⁵ m
- Both are **~25 orders of magnitude** below the best submillimeter experiments
- Current bounds constrain M₂ > ℏc/(48 μm) ~ 4×10⁻³ eV — 31 orders of magnitude weaker than QG+F's M₂

**From other graviton mass bounds:**
- S-star orbits (S2 around SgrA*): m_g < 1.5×10⁻²² eV
- GW propagation (LIGO O3): m_g < 1.8×10⁻²³ eV
- These constrain the massless graviton mass (QG+F predicts m_g = 0 exactly)

**Verdict: NOT CONSTRAINING.** The Yukawa ranges are 25+ orders of magnitude below experimental reach.

---

## Task 3: Cosmological Signatures Beyond CMB

### 3.1 21-cm Cosmology

The 21-cm hydrogen line probes the dark ages and cosmic dawn (z ~ 6-200). Modified gravity theories can affect the 21-cm signal through:
- Modified growth rate of density perturbations
- Altered thermal history
- Modified Jeans mass and structure formation

**QG+F's impact on 21-cm:** In QG+F, all modifications to the Friedmann equations and growth equations are suppressed by (H/M₂)² and (H/M₀)². Since H ~ 10⁻⁴² GeV (today) and M₂, M₀ > 10¹³ GeV, the suppression is (H/M)² ~ 10⁻¹¹⁰. This is identically zero for all practical purposes.

The scalaron's influence on structure formation in f(R) gravity (where M₀ could be light, ~10⁻²² eV, producing observable effects) does NOT apply to QG+F, where the scalaron mass is fixed to the inflation scale.

**Verdict: NOT DETECTABLE.** Modifications to 21-cm signal suppressed by ~10⁻¹¹⁰.

### 3.2 Large-Scale Structure and Matter Power Spectrum

**f(R) gravity modifications to the matter power spectrum** are well-studied (e-MANTIS emulator, DESI 2024 constraints). In f(R) models with light scalaron (M₀ ~ 10⁻²² eV), the fifth force enhances structure formation, affecting:
- Growth factor f(z)·σ₈(z)
- Matter power spectrum P(k) at k ~ 0.01-1 h/Mpc
- σ₈ tension (potentially)

**QG+F's impact:** However, in QG+F:
- The scalaron mass M₀ ~ 3×10¹³ GeV makes the fifth force range ~10⁻²⁷ m — irrelevant for cosmology
- All modifications to the Friedmann equations enter at O(H²/M²) ~ 10⁻¹¹⁰
- The theory reduces to ΛCDM + GR at all cosmologically accessible scales
- DESI and Euclid constraints on f(R) models are not relevant to QG+F

**Gravitational lensing:** Same suppression. QG+F corrections to the lensing potential are (E/M)² ~ 10⁻¹¹⁰.

**Verdict: NOT DETECTABLE.** QG+F is indistinguishable from GR at all cosmological scales below the inflation energy.

### 3.3 Stochastic GW Background

**Phase transitions in the early universe** can produce a stochastic GW background (SGWB) detectable by LISA, ET, and pulsar timing arrays. Recent work (arXiv:2603.21762, March 2026; JHEP 2025) studies GW spectra from both weak and strong first-order phase transitions.

**Does QG+F predict a GW-producing phase transition?**

QG+F does NOT predict any first-order phase transition beyond those in the Standard Model. The relevant question is whether the Planck-scale physics of QG+F could produce a SGWB during:
1. **Inflation exit/reheating:** The scalaron oscillation reheats the universe (identical to Starobinsky). GW production during reheating is at frequencies f ~ 10⁸-10¹⁰ Hz — far above any detector bandwidth.
2. **Ghost confinement phase transition:** If the non-perturbative completion involves a QCD-like ghost confinement transition (Holdom-Ren conjecture, Exp-007), this could produce a SGWB. But: (a) no calculation of this exists, (b) the transition would be at T ~ M_Planck, producing GWs at f ~ 10¹⁰ Hz.
3. **CDT phase transitions:** The B-C phase transition in CDT lattice gravity is a candidate UV critical point. Again, at Planck energies, producing ultra-high-frequency GWs.

**Verdict: NOT DETECTABLE.** Any QG+F-specific GW background would be at frequencies ~10⁸-10¹⁰ Hz, far above LISA (10⁻⁴-10⁻¹ Hz), LIGO (10-10³ Hz), and PTA (10⁻⁹-10⁻⁷ Hz) bands.

### 3.4 Dark Matter Candidates

**Three potential DM candidates from QG+F/AS:**

**1. The scalaron as DM:**
- Recent work (arXiv:2506.06436, June 2025): freeze-in production of scalaron DM in f(R) gravity
- Viable mass range: m_Φ ≲ 0.17 GeV (upper bound from lifetime) and m_Φ ≥ 2.7×10⁻³ eV (lower bound from fifth force tests)
- Requires reheating temperature T_rh ~ 10¹⁴-10¹⁶ GeV
- **BUT:** In QG+F, the scalaron mass is M₀ ~ 3×10¹³ GeV (far above the viable DM window of MeV scale)
- At M₀ ~ 10¹³ GeV, the scalaron decays rapidly (τ ≪ τ_universe) via all SM channels
- **NOT VIABLE** as DM in standard QG+F

**2. Planck-mass BH remnants (from AS):**
- AS predicts Planck-mass remnants from Hawking evaporation (T → 0, evaporation halts)
- Recent review: Rovelli & Vidotto (arXiv:2407.09584, July 2024) on Planck stars, white holes, remnants
- Could constitute cold dark matter (no EM interaction, correct behavior as CDM)
- Requires primordial BHs with initial mass < 10⁹ g
- **This is a non-perturbative AS prediction, NOT accessible to perturbative QG+F**
- No quantitative abundance prediction exists — depends on primordial BH formation rate

**3. Agravity DM candidate (Salvio 2016):**
- In agravity (= QG+F + classical scale invariance + SM), adding 3 right-handed neutrinos addresses DM
- Heaviest right-handed neutrino (M ~ 10⁸-10¹⁰ GeV) as DM via freeze-in
- This is a specific particle physics model BUILT ON QG+F, not a generic QG+F prediction
- Testable through leptogenesis constraints and neutrino oscillation parameters

**Verdict: WEAKLY RELEVANT.** The agravity DM candidate is the most concrete, but it's a specific model choice, not a generic QG+F prediction. The scalaron is too heavy; Planck remnants are non-perturbative.

---

## Task 4: Microcausality Violation Signature

### 4.1 The Physics of Fakeon Microcausality Violation

QG+F violates microcausality at the scale Δx ~ 1/M₂. The key papers are:
- Anselmi & Piva, JHEP 2018: "Quantum gravity, fakeons and microcausality"
- Anselmi, CQG 2019: "Fakeons, microcausality and the classical limit of quantum gravity"
- Anselmi & Marino, CQG 2020: "Fakeons and microcausality: light cones, gravitational waves and the Hubble constant"

**The violation mechanism:**
- The fakeon prescription modifies the retarded/advanced propagator at distances ~1/M₂
- The causal Green's function acquires acausal components — effects before causes at Δt ~ 1/M₂ ~ 10⁻⁴³ s
- This violation **survives the classical limit** (Anselmi 2019) — it's not just a quantum artifact

**Range of violation:**
- The violation extends up to **six orders of magnitude above the Planck length** — i.e., up to ~10⁻²⁹ m (compared to ℓ_P ~ 10⁻³⁵ m)
- This is because M₂ could be lower than M_Planck; the violation range is 1/M₂, and the consistency bound from inflation gives M₂ > M₀/4 ~ 10¹² GeV → 1/M₂ < 10⁻²⁸ m

**Can it be amplified?**
- Anselmi & Marino (2020) explicitly investigated amplification/detection
- **Result: NO.** The violation is "short range for all practical purposes"
- It does NOT propagate along light cones
- It does NOT propagate via gravitational waves
- "The universe even conspires to make the effect disappear" — the expansion (positive Hubble constant) suppresses the propagation of acausal effects

### 4.2 Scattering Cross Sections and the "Missing Resonance"

**The dressed propagator (Anselmi, JHEP 2022):**
- For a physical particle: self-energy resummation → Breit-Wigner peak at E = m with width Γ → visible resonance
- For a ghost: Breit-Wigner peak with negative width → instability
- For a fakeon: **no peak at all** — the cross section is smooth near E = m_f
- The "peak uncertainty" ΔE ≳ Γ_f/2 expresses a fundamental limit on probing the fakeon
- The peak region is "outside the convergence domain" and "can only be reached for physical particles, thanks to analyticity"

**The distinctive scattering signature:**
- A physical massive particle at mass M would show a resonance bump in the cross section
- The fakeon shows the **absence of a resonance** — a smooth cross section with at most a gentle shoulder or dip
- This is the "missing resonance" signature: the theory predicts a massive degree of freedom that does NOT produce a peak

**In the six-derivative extension (Lee-Wick):**
- Complex-mass poles produce interference patterns
- "Pair of bumps" from constructive/destructive interference at E ~ Re(M)
- This is a more complex signature than the simple missing resonance of four-derivative QG+F

### 4.3 Detectability Assessment

**The energy scale problem:**
- All these signatures occur at E ~ M₂ ~ M_Planck ~ 10¹⁹ GeV
- The LHC reaches ~10⁴ GeV — a gap of 10¹⁵
- No foreseeable collider can probe these energies
- Cosmic ray energies reach ~10¹¹ GeV (Ultra-High-Energy Cosmic Rays) — still 10⁸ below M₂

**Indirect channels investigated:**
1. **Cosmological correlations:** The microcausality violation during inflation affects the inflationary correlators — but these effects are already captured in the CMB predictions (n_s, r). No additional independent signature.
2. **BH information leakage:** The acausal Green's function could allow information to escape a BH at rate ~exp(-M₂·r_h). For astrophysical BHs, this is exp(-10⁵⁰) — zero.
3. **Gravitational wave propagation:** Anselmi & Marino (2020) showed explicitly that microcausality violation does NOT propagate via GWs.
4. **Direction of time:** The positivity of H₀ (Hubble constant) appears connected to the arrow of time in the fakeon framework. But this is a philosophical/interpretive connection, not a testable prediction distinct from standard cosmology.

**Verdict: NOT DETECTABLE.** The microcausality violation is confined to scales ~10⁻²⁸ to 10⁻³⁵ m and does not amplify or propagate to observable scales. Anselmi himself has shown this.

---

## Task 5: Experimental Timeline and Priority Ranking

### Complete Signature Catalog

| # | Signature | Sector | Detectable? | Experiment | Timeline |
|---|-----------|--------|-------------|------------|----------|
| 1 | Tensor-to-scalar ratio r < 0.005 | CMB | **YES** | LiteBIRD, SO | 2030-2037 |
| 2 | Spectral index n_s ≈ 0.964-0.967 | CMB | **YES** (already) | Planck, LiteBIRD | Done/2037 |
| 3 | Running α_s ≈ -6.5×10⁻⁴ | CMB | Marginal | CMB-S4 (cancelled) | >2040 |
| 4 | Massive spin-2 QNMs in ringdown | GW | **No** (Planck suppressed) | LIGO/ET | — |
| 5 | Scalar GW polarization | GW | **No** (M₀ too high) | LIGO/ET/LISA | — |
| 6 | Modified GW dispersion | GW | **No** (Planck suppressed) | LIGO/ET | — |
| 7 | Graviton-fakeon oscillation | GW | **No** (L_osc ~ 10⁻⁶⁰ m) | — | — |
| 8 | Stochastic GW background | GW | **No** (f ~ 10⁸ Hz) | — | — |
| 9 | GQuEST spacetime fluctuations | Table-top | **Not relevant** to QG+F | GQuEST | ~2027 |
| 10 | BMV entanglement | Table-top | **Not discriminating** | BMV labs | ~2030+ |
| 11 | Yukawa short-range | Table-top | **No** (25 orders gap) | Eöt-Wash | — |
| 12 | 21-cm signal | Cosmology | **No** (10⁻¹¹⁰ suppressed) | HERA, SKA | — |
| 13 | Matter power spectrum | Cosmology | **No** (identical to GR) | DESI, Euclid | — |
| 14 | Missing resonance at M₂ | Collider | **No** (10¹⁵× beyond LHC) | — | — |
| 15 | Microcausality violation | Various | **No** (short-range, non-propagating) | — | — |
| 16 | Scalaron DM | Cosmology | **No** (M₀ too high for DM) | — | — |
| 17 | Planck remnant DM (AS) | Cosmology | Maybe (non-perturbative) | Indirect DM searches | >2040 |
| 18 | Agravity DM (right-handed ν) | Particle | Possible (model-dependent) | Neutrino exp. | >2030 |
| 19 | Higgs mass from AS boundary | Particle | **CONFIRMED** (m_H = 126 GeV) | Done | Done |

### Priority Ranking (Likelihood of Detection in Next 20 Years)

**Tier 1: Realistic (>50% chance by 2046)**
1. **r measurement by LiteBIRD** (2036-2037) — the ONLY test that can discriminate QG+F from AS. If r < 0.003: favors QG+F. If r > 0.005: disfavors QG+F. **This remains the single most important test.**

**Tier 2: Possible but not discriminating (test quantum gravity generically)**
2. **BMV gravity-induced entanglement** (~2030+) — confirms gravity is quantum, consistent with QG+F but not specific to it
3. **GQuEST null result** (~2027) — consistent with QG+F, but a positive result would disfavor QG+F

**Tier 3: Long-shot or model-dependent**
4. **Agravity DM detection** — depends on the specific agravity model being correct
5. **AS grand unification predictions** — Eichhorn-Held program to predict gauge couplings from UV fixed point

**Tier 4: Not detectable with foreseeable technology**
6-19. Everything else — all suppressed by (E/M_Planck)² or confined to Planck-scale distances

### The Single Most Promising Non-CMB Test

**There is no promising non-CMB test specific to QG+F.**

The most promising non-CMB test that is at least *consistent* with QG+F is the **BMV gravity-induced entanglement experiment** — but it only tests whether gravity is quantum, not whether it's specifically QG+F. Any quantum gravity theory passes this test.

The most promising test that could *rule out* QG+F is **GQuEST** — if it detects holographic spacetime fluctuations, this would be evidence against QG+F's perturbative QFT framework. But a null result (which QG+F predicts) is uninformative.

**The honest conclusion: QG+F is a one-prediction theory (r).** All other signatures are suppressed by the enormous gap between observable energies and the Planck/inflation scale. This is not a weakness unique to QG+F — it affects ALL perturbative quantum gravity theories. The reason the CMB is special is that inflation amplified quantum fluctuations from Planck-scale physics to cosmological scales — a unique amplification mechanism that does not apply to any other sector.

---

## Key Findings Summary

1. **Every non-CMB signature of QG+F is undetectable with current or foreseeable technology.** The fundamental barrier is the ~15 orders of magnitude gap between the highest energies we can probe (~10⁴ GeV at LHC, ~10² Hz at LIGO) and the QG+F mass scales (M₂, M₀ ~ 10¹³-10¹⁹ GeV).

2. **The fakeon's defining signature — the missing resonance — is the most distinctive prediction but the least detectable.** It requires collider energies of ~10¹⁹ GeV.

3. **Microcausality violation does not propagate.** Anselmi himself showed (2019, 2020) that the violation is confined to scales ~1/M₂ and does not propagate via light cones or GWs. "The universe conspires to make the effect disappear."

4. **GW ringdown QNMs are the most studied but still hopeless.** While massive spin-2 QNMs exist in quadratic gravity (and are now being computed in detail), in QG+F with M₂ ~ M_Planck they are at completely inaccessible frequencies.

5. **GQuEST and BMV test different physics.** GQuEST tests holographic fluctuations (not QG+F). BMV tests quantum gravity generically (not specifically QG+F).

6. **The r measurement from CMB remains the only game in town.** LiteBIRD (2036-2037) is the definitive test. This was already known from Exp-010, and nothing in the non-CMB sector changes this picture.

7. **The most interesting non-CMB direction is the agravity DM candidate** (right-handed neutrinos in the Salvio framework) — but this is model-dependent and not a generic QG+F prediction.

---
