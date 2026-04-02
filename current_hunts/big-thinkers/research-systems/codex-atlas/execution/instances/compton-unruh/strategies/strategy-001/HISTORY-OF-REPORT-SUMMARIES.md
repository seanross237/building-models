# Exploration History

## Exploration 001 — Dimensional Analysis and Scale Identification (Math Explorer)

**Outcome: DECISIVE NEGATIVE RESULT**

The Compton-Unruh resonance at a ~ cH₀ is dimensionally inconsistent by 43 orders of magnitude.

- The matching acceleration for a proton is a* = 2.69 × 10³³ m/s², while the target is cH₀ = 6.6 × 10⁻¹⁰ m/s²
- The matching is mass-dependent (a* = 2πmc³/ℏ) — no universal a₀
- The cosmological scale H₀ doesn't appear in the matching condition
- The Boltzmann suppression at a ~ cH₀ is exp(-10⁴²) — effectively zero
- The Unruh-DeWitt detector response has no resonance structure; the Compton frequency enters only as a mass threshold
- The de Sitter modification T_dS = (ℏ/2πck_B)√(a² + c²H²) introduces a floor at T_GH but doesn't help

**Interesting finding**: There IS a crossover at a ~ cH₀ where de Sitter horizon effects dominate over acceleration effects. This crossover does NOT involve the Compton frequency but may deserve separate investigation.

**Leads**: (1) de Sitter thermal crossover as distinct mechanism, (2) McCulloch's IR cutoff approach, (3) proton mass entering through a different channel

---

## Exploration 002 — Survey of Unruh-Inertia Proposals (Standard Explorer)

**Outcome: FAILED** — Explorer worked on wrong mission (classicality-budget). Produced no output for this exploration. Will retry as exploration-003.

---

## Exploration 003 — Survey of Unruh-Inertia Proposals and No-Go Theorem Search (Standard Explorer)

**Outcome: NO UNIVERSAL NO-GO, BUT SEVERE CONSTRAINTS**

Surveyed 5 proposals (McCulloch QI, Haisch-Rueda SED, MOND, Verlinde, Jacobson/Padmanabhan).

**DEAD mechanisms:**
- Direct Compton-Unruh resonance (43 orders of magnitude, Expl. 001)
- Haisch-Rueda-Puthoff SED inertia (Levin 2009: relevant force = zero relativistically)
- McCulloch's QI as literally formulated (negative inertial mass at a₀; Renda 2019 derivation errors)
- Any thermal-detection-based mechanism (T_U = 10⁻³¹ K drowned by CMB at 2.7 K; energy density ratio 10¹²³)

**SURVIVING mechanisms:**
- Vacuum structure / mode counting (Casimir analogy)
- Verlinde's entropic gravity (derives a₀ = cH₀/6 ≈ 1.1×10⁻¹⁰ m/s², matches MOND to ~10%)
- De Sitter crossover at a ~ cH₀ (area vs volume entropy competition)

**Critical objection**: Stars in galaxies are in free fall (zero proper acceleration), so standard Unruh effect should not apply. Any mechanism must specify what "acceleration" enters the formula.

**Unexpected**: McCulloch's core equation gives NEGATIVE inertial mass at MOND-relevant accelerations.

---

## Exploration 004 — De Sitter Crossover Mechanism (Math Explorer)

**Outcome: MIXED — Tantalizing mathematical identity, but no rigorous derivation**

**KEY FINDING**: The ratio T_U(a)/T_dS(a) = a/√(a² + c²H₀²) is ALGEBRAICALLY IDENTICAL to the standard MOND interpolation function μ(x) = x/√(1+x²) with a₀ = cH₀.

If m_i = m × T_U/T_dS, the model reproduces:
- MOND rotation curves (correct shape)
- Baryonic Tully-Fisher relation (correct slope)
- Solar system constraints (deviation < 10⁻¹⁴ at Earth orbit)

**CRITICAL GAPS**:
1. No first-principles derivation of m_i = m × T_U/T_dS
2. The naive entropic approach (F ~ T_dS) gives WRONG SIGN (anti-MOND)
3. Direct self-force (ALD) vanishes for constant acceleration
4. Predicted a₀ = cH₀ is 5.5× too large (Verlinde's factor fixes this to within 8%)

**Three routes to explore**: DeWitt-Brehme self-force in dS, Verlinde's entropic argument, fluctuation-dissipation theorem in dS.

---

## Exploration 005 — Literature Search: T_U/T_dS = μ_MOND Novelty, Verlinde Comparison, Free-Fall Objection (Standard Explorer)

**Outcome: MOSTLY SUCCEEDED — Identity appears novel, distinct from Verlinde, free-fall unresolved**

**Novelty verdict**: The specific identity T_U/T_dS = μ_standard_MOND appears genuinely novel. Zero papers found with this identity. Closest prior: Milgrom 1999 (astro-ph/9805346) used EXCESS temperature T_dS − T_GH — different formula, different interpolation function, a₀ = 2cH₀.

**Verlinde comparison**: T_U/T_dS and Verlinde 2016 are genuinely distinct:
- Verlinde: elastic entropy displacement (modified gravity), gets only deep-MOND limit, a₀_eff = cH₀/6 ≈ 1.1×10⁻¹⁰ (8% from observed)
- T_U/T_dS: temperature ratio (modified inertia), gets EXACT standard interpolation function, but a₀ = cH₀ (5.5× too large)
- T_U/T_dS predicts RAR exactly; Verlinde fails RAR observationally

**Free-fall objection**: UNRESOLVED. Sciama-Candelas 1981 confirms freely-falling observers see cold vacuum, not T_GH. Milgrom (1999) himself flagged this — 25 years unresolved. Potential resolution: replace proper acceleration with de Sitter-relative acceleration = g_B (= Newtonian gravitational acceleration for orbital stars). Not rigorously developed.

**Key leads**: (1) Compute de Sitter-relative acceleration for orbital stars, (2) Jacobson local Rindler temperature connection, (3) Factor of 5.5 may come from 3D spatial entropy

---

## Exploration 006 — Fluctuation-Dissipation Mechanism and SPARC Galaxy Fits (Math Explorer)

**Outcome: NEGATIVE on FDT, POSITIVE on Verlinde-scale model**

**FDT result (CLOSED)**: χ''_dS/χ''_flat = 1.000000 exactly. Enhanced de Sitter noise canceled by higher temperature in FDT denominator. Quantum mass renormalization is T-independent. Damping goes the WRONG WAY: γ_dS > γ_flat. Only route to ratio formula is ad hoc "thermodynamic inertia" definition — the ansatz in disguise, not a derivation.

**Galaxy rotation curves**:
- NGC 3198: MOND χ²/dof=1.34, Verlinde(cH₀/6) χ²/dof=1.21, cH₀ χ²/dof=132
- NGC 2403: MOND χ²/dof=0.88, Verlinde(cH₀/6) χ²/dof=0.52, cH₀ χ²/dof=140
- Best-fit a₀: 0.74–0.93 × a₀_MOND for both galaxies
- cH₀ decisively ruled out; cH₀/6 matches MOND

**Remaining leads**: (1) Verlinde-FDT connection (entropy elasticity as dissipation kernel), (2) Quantum information route (T_U/T_dS = purity of Rindler reduced density matrix?), (3) DeWitt-Brehme self-force in dS

---

## Exploration 007 — Free-Fall Objection: De Sitter-Relative Acceleration and Factor of 1/6 (Math Explorer)

**Outcome: FREE-FALL RESOLVED, factor 1/(2π) NOT derivable**

**Free-fall resolution**: a_dS_rel = g_N EXACTLY for all test cases. Stars in circular orbits have de Sitter-relative acceleration = Newtonian gravitational acceleration (Λ cancels identically in a_star − a_Hubble). Jacobson local Rindler independently gives a_Rindler = g_N. Both approaches are equivalent. The 25-year-old objection (Milgrom 1999) is cleanly resolved.

**Factor of 1/(2π)**: CANNOT be derived from T_U/T_dS. 2π factors in T_U and T_dS cancel in the ratio. Four independent approaches all fail. Requires Verlinde's area-volume entropy competition as external input. This is the primary remaining gap.

**NGC 3198 fits**: cH₀ model χ²/dof = 557 (ruled out). Verlinde cH₀/(2π) χ²/dof = 29.1, same as MOND (28.5). Best-fit a₀ = 0.98 × a₀_MOND.

---

## Exploration 008 — Adversarial Stress Test (Standard Explorer)

**Outcome: DECISIVE NEGATIVE — Model falsified by gravitational lensing**

**Fatal failures**:
1. **Bullet Cluster (CRITICAL)**: Modified inertia leaves gravitational potential unchanged. Predicted lensing mass = 3.5×10¹³ M_sun, observed = 2×10¹⁴ M_sun (5.7× discrepancy). Lensing morphology wrong.
2. **Cluster lensing (CRITICAL)**: 5-10× mass deficit for any cluster. Einstein radius underestimated by √10.
3. **CMB 3rd peak (SEVERE)**: 3rd/1st peak ratio suppressed ~2× without dark matter. Planck matches ΛCDM to 1%.

**New internal inconsistency**: Which "a" enters μ? Case A (proper accel = 0) kills model. Case B (centripetal v²/r) gives MOND but is ad hoc. Case C (g_N, as stated) gives v ∝ r^{1/2}, NOT flat rotation curves.

**Model viability**: Theoretical 2/10, Observational 3/10 (galaxy scales only).

**Key takeaway**: T_U/T_dS = μ_MOND identity is real, but as modified inertia it's falsified. Must be reformulated as modified gravity or understood as emergent property within a framework that also modifies the potential.

---

