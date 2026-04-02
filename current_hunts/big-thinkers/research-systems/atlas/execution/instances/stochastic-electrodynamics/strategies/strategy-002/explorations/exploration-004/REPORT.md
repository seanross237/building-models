# Exploration 004 — Phase 2: Root Cause Diagnosis and Minimal Modification Survey

## Goal Summary

Synthesize results from Strategy-002 Phase 1 (double-well tunneling E001, coupled oscillators E002, hydrogen E003) and evaluate the "ω³ feedback mechanism" as a unifying root cause hypothesis. Survey SED literature for prior modifications (Boyer, de la Peña-Cetto, Pesquera-Claverie, Santos, Nieuwenhuizen, Claverie-Diner). Assess three proposed fixes (Local FDT, spectral index modification, dressed particle). Identify which novel claims from E001-E003 survive scrutiny.

**Method:** Web literature search + paper fetches from arXiv, Springer, Frontiers, Semantic Scholar, SciELO.

---

## Section 1: Literature Survey — SED Modifications and Prior Work

### 1.1 Boyer (1975–2019)

**Boyer 1976 (Phys. Rev. D 13, 2832)** — This is the foundational nonlinear failure paper. Boyer computed the scattering of ZPF by a nonlinear electric dipole oscillator and showed: **the Rayleigh-Jeans spectrum is an equilibrium distribution in the presence of a nonlinear oscillator, while the Lorentz-invariant ω³ ZPF is NOT**. The nonlinear oscillator acts to "push" the ZPF toward the Rayleigh-Jeans law. Boyer noted this would constitute a perpetual-motion machine of the second kind if taken seriously — the nonlinear oscillator can extract energy from the ZPF indefinitely.

**Boyer 2019 (Atoms 7(1):29, arXiv:1903.00996)** — "Stochastic Electrodynamics: The Closest Classical Approximation to Quantum Theory." Boyer surveys successes and failures. He acknowledges failures with nonlinear systems but takes the position that SED "might still work" for physically realized atomic systems (like hydrogen) as opposed to artificial nonlinear binding potentials. He does NOT propose any modification to the ω³ spectrum or to the ALD radiation reaction. His position is essentially: SED is the best classical approximation to QM; the failures are the cost of using a classical framework.

**Boyer's proposed modifications:** None. Boyer consistently maintains the standard ω³ ZPF and the Abraham-Lorentz-Dirac (ALD) radiation reaction as the defining features of SED. He is arguably SED's most prominent defender but offers no mechanism to fix nonlinear failures.

**Boyer's statement on non-locality:** Boyer (2018) explicitly states that SED is a globally non-local theory because the ZPF has global phase correlations. This is relevant to E002's C_xx(d) result.

### 1.2 Claverie, de la Peña-Auerbach & Diner (1977)

**Paper: "Stochastic Electrodynamics of non-Linear systems. II. Derivation of a reduced Fokker-Planck equation in terms of relevant constants of motion"**

This is the most important early diagnosis paper. Claverie, de la Peña & Diner attempted to derive a Fokker-Planck equation for nonlinear SED systems and encountered a fundamental obstacle: **the ω³ ZPF is highly colored noise, making the process strongly non-Markovian**. The Fokker-Planck equation (which assumes white noise or weakly colored noise) cannot be straightforwardly derived for systems driven by ω³ noise. They showed that:
- The reduced Fokker-Planck equation involves radiation balance conditions
- For linear oscillators, radiation balance is automatically satisfied
- For nonlinear systems, radiation balance fails, and the Fokker-Planck approach breaks down

A companion paper by Claverie & Diner (1977) examined "Some Remarks about the LAX Approximation" in SED, identifying the Markov approximation failure as central.

**Significance:** This is the earliest explicit identification that ω³ colored noise (not merely nonlinearity per se) is the root of the Fokker-Planck failure. The mechanism is intimately related to the ω³ feedback hypothesis.

### 1.3 Pesquera & Claverie (1982)

**Paper: "The quartic anharmonic oscillator in stochastic electrodynamics," J. Math. Phys. 23, 1315-1322**

Using Kubo's linear response theory on the slightly anharmonic oscillator with perturbation βx⁴:
- Computed stationary probability density and mean energy
- **Key result:** Mean energy differs from QM prediction at **order β** (not β² — this is first order in anharmonicity)
- The maximum absorption frequencies do NOT coincide with quantum transition frequencies
- **"Radiation balance" is not exactly satisfied as soon as β ≠ 0** — this is the most damning result

The radiation balance failure at first order in β is crucial: it means even infinitesimally small anharmonicity breaks SED's ability to reach the quantum ground state. This is not a perturbative correction that becomes small — it's a qualitative failure.

**No modification proposed.** Pesquera & Claverie treated this as a definitive negative result for SED with nonlinear systems.

**Companion paper:** "The harmonic and anharmonic oscillator in classical stochastic electrodynamics" (Il Nuovo Cimento B) — showed qualitative QM agreement but with quantitative discrepancies.

### 1.4 de la Peña & Cetto — LSED (Linear Stochastic Electrodynamics)

**Papers:** "The Foundations of Linear Stochastic Electrodynamics," Found. Phys. 35 (2005); also books "The Quantum Dice" (1996) and "The Emerging Quantum" (2015)

LSED is the most systematic attempt to salvage SED's quantum mechanical interpretation. The central idea:
- Standard SED couples the particle to ALL modes of the ZPF
- LSED restricts attention to modes of the ZPF that are **resonant with atomic transition frequencies**
- This is a "mode selection" approach, invoking linear response theory: only resonant modes drive the particle dynamics significantly
- LSED derives quantum matrix mechanics from the vacuum field by selecting resonant modes

**Critical limitation:** LSED is explicitly a **linear response theory**. It works for systems where transitions are well-defined (harmonic oscillator). The "linear" in LSED refers to linear response of the particle to the field — not to a linear potential.

**Does LSED fix nonlinear failures?** No. For the anharmonic oscillator and hydrogen, LSED has the same fundamental problem: the resonant mode selection is well-defined only for harmonic systems where transition frequencies are sharply defined. For nonlinear systems, the transition frequencies are energy-dependent, mode selection becomes ambiguous, and LSED reduces to standard SED.

De la Peña's 2022 paper (arXiv:2207.06549) claims that "recent numerical experiments have shown that a statistical analysis of an atomic electron interacting with the ZPF furnishes the quantum distribution for the ground state of the H atom" — this is the optimistic Cole & Zou (2003) short-run result that E003 subsequently refuted by running longer simulations.

**Is LSED a "position-dependent noise"?** No. LSED modifies the coupling by selecting resonant modes (a frequency-domain modification), not by making noise power position-dependent.

### 1.5 Santos (2022) — Weyl-Wigner Representation

**Paper: "On the analogy between stochastic electrodynamics and nonrelativistic quantum electrodynamics," EPJ Plus (arXiv:2212.03077)**

Santos proves using the Weyl-Wigner (phase space) representation of QED:
- **An approximation to first order in Planck's constant has formal analogy with SED**
- For quadratic Hamiltonians: the first-order-in-ħ approximation is **exact** (all higher-order Wigner distribution corrections vanish for quadratic H)
- For nonlinear Hamiltonians: second-order and higher ħ corrections are non-zero, and SED misses them entirely

This provides the most precise characterization of SED's domain: **SED = first-order-ħ approximation to QED**, exact for quadratic H, inexact otherwise. This explains the successes (harmonic oscillator, van der Waals, Casimir — all involve quadratic H) and the failures (anharmonic, hydrogen — nonlinear H).

**No modification proposed.** Santos treats this as a diagnostic result.

**Santos earlier work (1974):** Early contributions to SED foundations. Santos also proposed SEDS (SED with Spin) as a modification:

**Santos SEDS — SED with Spin:**
- Adds spin degrees of freedom to the SED particle
- Partially addresses some failures (explains Bohr magneton, spin-statistics connection)
- Does NOT resolve the fundamental nonlinear failure for spinless systems (anharmonic oscillator, hydrogen orbital dynamics)

### 1.6 Nieuwenhuizen (2020) — Five Renormalization Schemes

**Paper: "Stochastic Electrodynamics: Renormalized Noise in the Hydrogen Ground-State Problem," Frontiers in Physics 8:335**

Nieuwenhuizen systematically tested 5 renormalization schemes for the ZPF coupling to hydrogen:

1. **Short-Time Regularization (Scheme 1):** High-frequency cutoff; ω̃ = ω₀²/ω for components above resonance. Well-behaved but doesn't prevent ionization.
2. **Absolute Value (Scheme 2):** |W| with positive eigenvalues. "Does not eliminate divergence; if anything, it becomes worse."
3. **Broken Power (Scheme 3):** |W|^(1/2) — softens short-time behavior. Produces cutoff-dependent energy asymmetries near pericenters.
4. **Mixed Cross-Terms (Scheme 4):** Combined AE and EA cross-term contributions. Yields smaller critical L but ionization still occurs.
5. **Cubic Root Decomposition (Scheme 5):** W^(1/3) and W^(2/3) with complex correlation functions.

**Result: In no situation did any renormalization scheme escape the previously signaled self-ionization.** The conclusion is unambiguous: "SED is not a basis for quantum mechanics" — the instability is fundamental.

**Mechanism:** At orbital angular momentum κ < 0.588, energy absorbed from ZPF exceeds energy radiated. The radiation loss goes as k⁴ → 0 at low k, while ZPF absorption remains finite. At near-zero energy + low L, runaway ionization is unavoidable.

**Note:** Nieuwenhuizen does NOT propose modifying the ω³ spectral density itself. None of his 5 schemes change the spectral form; they all modify the coupling operators.

### 1.7 Faria, França & Sponchiado (2006) — Tunneling as Escape Rate

**Paper: "Tunneling as a Classical Escape Rate Induced by the Vacuum Zero-point Radiation," Foundations of Physics 36, 307-320 (arXiv:quant-ph/0409119)**

This is the prior art for E001's double-well exploration. Key results:
- Extended Kramers escape rate theory to include ZPF
- Escape rate formula (Eq. 17): **k ∝ exp(−ΔU/D(T))** where D(T) = (ħωₐ/2)coth(ħωₐ/2k_BT)
- At T → 0: **k ∝ exp(−ΔU/(ħωₐ/2)) = exp(−2ΔU/E_zpf)** where E_zpf = ħωₐ/2
- Demonstrated non-null escape rate at T=0 — "tunneling" via ZPF kicks
- Validated against CO-hemoglobin recombination data (qualitative match)
- No explicit WKB tunneling rate comparison — no Γ_SED/Γ_QM ratio derived
- Analytical approach only; no numerical simulation of actual double-well trajectory

**Critical difference from E001:** Faria & França have k ∝ exp(−2ΔU/E_zpf); E001 claims Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf). These are different formulas. E001's formula involves the WKB action S_WKB explicitly, and is a ratio to the QM tunneling rate. The Faria & França formula is an absolute rate.

### 1.8 Other Relevant Modifications

**Cavalleri & Rueda (1983):** "Zitterbewegung in stochastic electrodynamics and implications on a zero-point field acceleration mechanism." Extended electron model where ZPF-induced relativistic oscillations of the center of charge modify effective mass. The "dressed particle" idea — but not developed as a fix for nonlinear failures generally.

**Nelson's Stochastic Mechanics (2512.16168, 2024):** Recent paper on tunneling in double-well potentials uses Nelson's stochastic mechanics (NOT SED). Derives τ_QM = (π/2)τ̄ connecting stochastic-mechanical and QM tunneling times. Important: Nelson's SM is DIFFERENT from SED — it uses ħ explicitly and enforces quantum distributions by construction (osmotic velocity). This paper is NOT SED tunneling.

**Position-Dependent Noise / Local FDT:** Literature search found NO paper proposing this modification. The concept of making noise power depend on position (proportional to |V''(x)| or ω_local(x)³) is absent from the SED literature.

**Spectral Index Modification (ω^n, n < 3):** Literature search found NO paper proposing this modification. The ω³ spectrum is treated as sacrosanct (required by Lorentz invariance). No author has proposed modifying n below 3 as a systematic fix.

---

## Section 2: Assessment of Root Cause Hypothesis (ω³ Feedback)

### 2.1 The Hypothesis

The proposed mechanism: when a system's **local oscillation frequency ω_local(x) deviates from the equilibrium frequency ω₀**, the ω³ ZPF delivers power proportional to ω_local³ while the ALD damping calibrated to ω₀ cannot compensate, creating energy imbalance.

### 2.2 Support from Literature

**Strong support:**
1. **Boyer 1976** directly established: nonlinear oscillators push ZPF toward Rayleigh-Jeans. The ω³ ZPF is NOT an equilibrium spectrum for nonlinear oscillators. This is precisely the energy imbalance the hypothesis predicts.
2. **Claverie-Diner 1977** showed: ω³ colored noise makes Fokker-Planck inapplicable to nonlinear systems. The technical failure is the non-Markovian nature of ω³-driven dynamics. This is the mechanism by which the imbalance manifests.
3. **Pesquera-Claverie 1982** showed: radiation balance fails at **first order** in anharmonicity β. Even infinitesimally small ω_local deviation from ω₀ breaks the balance — consistent with ω³ feedback being a continuous, not threshold, effect.
4. **Santos 2022** provided the deepest explanation: SED misses second-order-in-ħ corrections. In the Weyl-Wigner language, the ω³ feedback is the classical signal of these missing quantum corrections.

**Partial support for specific systems:**

*Anharmonic oscillator:* The anharmonic term shifts ω_local(x) upward → more ZPF power → ALD compensates incompletely (15-18% residual in Strategy-001). ✓ Consistent.

*Double-well (E001):* At barrier top, V''(x) < 0 → ω²_local < 0 → imaginary frequency → ALD becomes an anti-damper. The ZPF kicks the particle over the barrier faster than quantum tunneling (18× overestimate at λ=0.10). The ω³ feedback explains why SED tunneling is "over-tunneling" — the ZPF sees the anti-restoring force and cooperates in pushing particles over. ✓ Consistent.

*Hydrogen (E003):* Near the nucleus, V(r) = -e²/r, V''(r) = -2e²/r³ → |V''| → ∞ as r → 0. For eccentric orbits, the electron makes close approaches to the nucleus where ω_local → ∞. The ω³ ZPF then delivers enormous power on the near-nucleus pass. Nieuwenhuizen showed the critical threshold is L < 0.588ħ — exactly the angular momentum below which orbits become eccentric enough for near-nucleus passes to dominate. ✓ Strongly consistent.

*Coupled linear oscillators (E002):* Linear → ω_local = ω₀ everywhere → no feedback → exact balance (no failure). ✓ Consistent. C_xx(d) = cos(ω₀d/c) is a success, not a failure.

### 2.3 What the Hypothesis Does NOT Unify

**The detailed mechanism differs between systems:**
- Anharmonic: continuous first-order departure from balance (ω_local slightly above ω₀)
- Double-well: sign reversal (ω_local imaginary at barrier top)
- Hydrogen: singularity (ω_local → ∞ near nucleus + orbital instability from low-k runaway)

The ω³ feedback is a necessary condition for all failures, but it's not sufficient as a complete explanation: for hydrogen, the ALSO-necessary condition is that orbits can reach eccentricities where the near-nucleus passes dominate (L < 0.588ħ). The Coulomb potential's 1/r singularity creates a qualitatively different failure mode from the polynomial nonlinearity in anharmonic/double-well.

**The crossover condition in E001:** S_WKB = V_barrier/E_zpf — is this equivalent to ω_local = ω₀?

No. The crossover occurs when the WKB action integral (a global quantity over the barrier) equals the ratio V_barrier/E_zpf (a global energy ratio). The condition ω_local = ω₀ is a local condition at the barrier top. These are related (both involve energy/frequency scales) but are not identical. At the crossover, the SED quasi-thermal process with energy scale E_zpf produces the same rate as quantum tunneling with action S_WKB — a coincidence in energy scales, not a local frequency matching.

### 2.4 Verdict on Root Cause Hypothesis

**The ω³ feedback mechanism is a correct and previously unnamed unifying concept**, but it needs to be stated more precisely:

> SED fails whenever a system's dynamical evolution causes the particle to experience ZPF frequencies significantly different from the equilibrium frequency ω₀. The ω³ spectral density is the equilibrium distribution ONLY for the harmonic oscillator (ω_local = ω₀ everywhere). For nonlinear systems, the ω³ spectrum delivers either too much power (when ω_local > ω₀, as in anharmonic oscillator and near-nucleus hydrogen) or provides anti-damped amplification (when ω_local is imaginary, as at the double-well barrier top). Neither the ALD damping term (calibrated to emit at ω₀³) nor the linear response machinery (LSED) can compensate for this mismatch.

This framing is consistent with Boyer 1976, Claverie-Diner 1977, Pesquera-Claverie 1982, and Santos 2022. **None of these papers state the ω³ feedback as a unified mechanism across anharmonic, double-well, and hydrogen** — that synthesis is the novel contribution of this Strategy-002 analysis.

---

## Section 3: Evaluation of Three Proposed Fixes

### Fix A: Local FDT (Position-Dependent Noise)

**Proposed formula:** Replace S_F(ω) = 2τω³/m with S_F(ω, x) = 2τ|V''(x)|^(3/2)/m × δ(ω − ω_local(x))

**Literature precedent:** NONE FOUND. This modification is absent from the SED literature. No paper was found proposing position-dependent ZPF power or a local fluctuation-dissipation theorem approach in SED.

**Analysis:**

For the harmonic oscillator: V''(x) = ω₀² everywhere → ω_local = ω₀ everywhere → Local FDT reduces to standard SED. ✓ Preserves harmonic success.

For the anharmonic oscillator V(x) = ½ω₀²x² + λx⁴: V''(x) = ω₀² + 12λx² → ω_local(x) = √(ω₀² + 12λx²) > ω₀ for x ≠ 0. The local noise would scale as ω_local³(x) > ω₀³ everywhere except x = 0. This is the OPPOSITE of what's needed to fix the problem — Local FDT would deliver EVEN MORE power to the anharmonic oscillator, worsening the energy imbalance. ✗ Would not fix anharmonic oscillator.

For the double-well V(x) = -½ω₀²x² + ¼λx⁴: At the barrier top, V''(x_top) = -ω₀² < 0 → ω²_local < 0. The local noise power would be |V''|^(3/2) = ω₀³, which is finite — but the ALD term becomes anti-damping. This partially compensates (finite noise vs. anti-damping), but the fundamental issue remains. ✗ Partial, not a fix.

For hydrogen V(r) = -e²/r: V''(r) = -2e²/r³ → |V''(r)| → ∞ as r → 0. Local FDT noise → ∞ near nucleus, even faster than standard ω³ ZPF. ✗ Dramatically worsens hydrogen failure.

**Verdict:** Fix A is novel (not in literature), but does NOT fix any of the three failures examined. In fact it worsens the anharmonic and hydrogen problems. The concept is interesting as a diagnostic tool (it makes the energy imbalance more explicit) but is not a viable physical modification.

### Fix B: Spectral Index Modification (ω^n, n < 3)

**Proposed formula:** Replace the standard ω³ ZPF spectral density with ω^n for n < 3.

**Literature precedent:** NONE FOUND. No paper in the SED literature proposes changing the spectral exponent as a fix for nonlinear failures. The ω³ form is treated as sacrosanct because it is the unique Lorentz-invariant spectrum.

**Analysis:**

**Physical meaning:** The ω³ spectral density is the ONLY Lorentz-invariant spectrum (required by Lorentz covariance of the zero-point field). Changing to ω^n for n ≠ 3 breaks Lorentz invariance of the ZPF. This would be a fundamental modification to the theory, not just a "fix."

**For n = 2 (Rayleigh-Jeans):** Boyer 1976 showed this is what nonlinear oscillators PUSH the ω³ ZPF toward. So the system itself "wants" n = 2. But n = 2 corresponds to thermal equilibrium — it would destroy the zero-point energy and make the harmonic oscillator collapse classically. ✗ Catastrophic.

**For n = n* ≈ 2.61 (Strategy-001 result):** This minimizes the 15-18% residual for the anharmonic oscillator. But:
- Breaks Lorentz invariance
- Would change the harmonic oscillator ground state (since ⟨x²⟩ ∝ ∫ ω^n/ω₀² × δ(ω−ω₀) = ω₀^(n-2), which equals ω₀⁰ = 1 (correct) only for n = 2... wait, actually for the harmonic oscillator, ⟨x²⟩ is determined by the spectrum at ω = ω₀ only, so ⟨x²⟩ ∝ ω₀^n/ω₀² = ω₀^(n-2). For this to match QM, need ω₀^(n-2) = 1, which requires n = 2, not n = 3. But we know n = 3 works for the harmonic oscillator because ⟨x²⟩ = ħ/(2mω₀) is reproduced by ρ(ω₀) = ħω₀³/(πc³) × V/(... more carefully, it's not just the frequency but the full mode density). Actually, this is more subtle — the n* crossover for the anharmonic oscillator found in Strategy-001 isn't saying n = 2.61 gives the right QM ground state, it's saying n* minimizes the RESIDUAL between SED and QM for the anharmonic case specifically. For the harmonic oscillator, any n gives the right ground state when properly calibrated.

- Would NOT fix hydrogen (the Coulomb singularity creates a qualitatively different failure)
- No physical motivation

**Verdict:** Fix B is novel (not in literature) but physically unmotivated (breaks Lorentz invariance) and cannot universally fix all failures. The n* ≈ 2.61 result from Strategy-001 is an interesting empirical finding but not a viable physical modification.

### Fix C: Effective Mass / Dressed Particle

**Proposed idea:** Use a dressed particle with modified (renormalized) mass, as in Cavalleri's extended electron model or Santos' SEDS.

**Literature precedent:** Partially yes. Cavalleri & Rueda (1983) proposed an extended electron model where ZPF-induced zitterbewegung modifies the effective inertial mass. Santos proposed SEDS (SED with Spin) as a more systematic modification.

**Cavalleri Extended Electron Analysis:**
- ZPF-driven relativistic oscillations of the center of charge relative to center of mass
- Gives rise to modified effective mass m* = m + δm(E_zpf)
- Primarily addresses questions about inertia and zitterbewegung
- Does NOT address the energy balance problem in nonlinear systems
- The hydrogen ionization and anharmonic oscillator radiation balance failure are not fixed by mass renormalization

**Santos SEDS (SED with Spin):**
- Adds spin degree of freedom to SED particle
- Partially explains Bohr magneton, spin-statistics, and some magnetic phenomena
- Does NOT resolve the nonlinear binding force failures
- Santos himself acknowledges (2022) that the fundamental quadratic Hamiltonian constraint is the core issue

**Nieuwenhuizen 5-Scheme Renormalization:**
- This is the most systematic "dressed particle" approach tried for hydrogen
- Results: ALL 5 schemes fail, self-ionization persists
- This exhausts the space of "coupling renormalization" approaches

**Verdict:** Fix C is in the literature (partially), but none of the dressed-particle modifications fix the core nonlinear energy balance problem. Nieuwenhuizen's exhaustive 5-scheme analysis for hydrogen is essentially a proof that renormalization of the noise coupling cannot rescue hydrogen SED.

### Summary Table of Three Fixes

| Fix | In literature? | Fixes anharmonic? | Fixes H? | Fixes double-well? | Notes |
|-----|----------------|-------------------|----------|-------------------|-------|
| A: Local FDT | No (NEW) | No (worsens) | No (worsens) | No | Novel concept, wrong direction |
| B: Spectral index n<3 | No (NEW) | Partially (n*≈2.61 reduces residual) | No | Unknown | Breaks Lorentz invariance |
| C: Dressed particle | Partially (Cavalleri, Santos SEDS, Nieuwenhuizen) | No | No (Nieuwenhuizen exhaustive) | Unknown | Exhaustively tested for H, all fail |

---

## Section 4: Novel Claim Assessment

### Claim A: The Formula Γ_SED/Γ_WKB ≈ exp(S_WKB − V_barrier/E_zpf)

**Prior art found:**
- Faria, França & Sponchiado (2006, Found. Phys. 36, 307-320) derived k ∝ exp(−ΔU/(ħωₐ/2)) using Kramers theory extended with ZPF
- At T=0: k ∝ exp(−2ΔU/E_zpf) — an absolute escape rate, NOT a ratio to WKB

**Is E001's formula different?** Yes, in three important ways:
1. E001 expresses a RATIO to the WKB quantum tunneling rate (Γ_SED/Γ_WKB), not an absolute rate
2. E001's formula contains S_WKB explicitly, while Faria & França have only ΔU/E_zpf
3. E001 identified the CROSSOVER condition S_WKB = V_barrier/E_zpf at a specific λ value

**Computational check of the formula:** Independent computation confirms:
- E001 uses E_zpf = ħω_local/2 where ω_local = √(V''(x_min)) = **√2** (the local well frequency — always √2 for this double-well regardless of λ, when ω₀=1)
- This gives E_zpf = √2/2 ≈ 0.707 (not ħω₀/2 = 0.5)
- V_barrier/E_zpf: at λ=0.25, = 1.0/(√2/2) = √2 ≈ 1.414 ✓ (matches GOAL.md's 1.41)
- V_barrier/E_zpf: at λ=0.10, = 2.5/(√2/2) = 5√2/2 ≈ 3.536 ✓ (matches GOAL.md's 3.52)

**Formula accuracy assessment:**
- λ=0.25: formula predicts exp(1.41−1.41) = 1.00, actual ratio = 1.15 → **15% underestimate**
- λ=0.10: formula predicts exp(6.29−3.52) = exp(2.77) ≈ 15.9, actual ratio = 18.5 → **14% underestimate**

The formula has a **consistent ~15% systematic underestimate** at both data points. This suggests the formula has the correct functional form (exponential of S−V/E) but may need a prefactor ≈ 1.15. For an exponential formula spanning a ratio of 1 to 18, agreement within 15% is actually reasonable.

**Novelty verdict:** The ratio formulation and the crossover condition are genuinely new and not in Faria & França. The formula should be treated as a well-motivated conjecture with 2-point support and ~15% precision. The exact prefactor and the universality of the crossover condition need testing at more λ values.

**Risk:** The two-λ verification is thin. The formula should be tested at 4-5 λ values spanning at least one decade. The interesting prediction: at λ where S_WKB < V_barrier/E_zpf, the formula would give Γ_SED < Γ_QM — quantum mechanics tunnels FASTER than SED. Is this realized?

### Claim B: C_xx(d) = cos(ω₀d/c) for Two SED Oscillators

**Prior art found:**
- Boyer (1969-1973) derived van der Waals forces between coupled oscillators using ZPF correlations
- The ZPF spatial correlation function ⟨E_i(r₁,t)E_j(r₂,t)⟩ is known analytically (it involves the electromagnetic Green's function)
- In 1D, the two-point ZPF electric field correlation at equal times has the form ∝ cos(k|r₁-r₂|)k²dk integrated, which for a single mode ω₀ gives cos(ω₀d/c)

**Is E002's formula different from Boyer?** The issue is context:
- Boyer (1972, Phys. Rev. A 5, 1799) derived van der Waals forces — the FORCE, not the displacement correlation
- The displacement correlation C_xx(d) = ⟨x₁(t)x₂(t)⟩ for two driven oscillators is different from the ZPF field correlation
- For two identical oscillators at separation d sharing a 1D single-mode ZPF, the equal-time displacement correlation C_xx(d) = cos(ω₀d/c) because each oscillator is driven by the same ZPF mode (phase-coherent across the separation)
- This derivation would be analytically straightforward from Boyer's ZPF correlation functions, but the EXPLICIT CHSH computation and the Bell-CHSH ≤ 2 demonstration appears genuinely new

**Novelty verdict:** The formula C_xx(d) = cos(ω₀d/c) is likely derivable from Boyer's ZPF two-point correlations (1969-1973) and thus NOT fundamentally new as a correlation formula. However, the CHSH computation from SED, the explicit Bell-CHSH ≤ 2 result, and the comparison to quantum correlations (which can exceed 2) is genuinely new. The correlation formula may be known; the CHSH analysis is new.

**Caveat:** The 1D result may be an artifact of using a single-mode 1D ZPF. In 3D multi-mode ZPF, the correlation averages over all polarizations and k-directions, likely giving a different (weaker, possibly zero) result. E002 flagged this as a "key gap."

### Claim C: T_ion(L) Measurements for SED Hydrogen

**Prior art found:**
- Cole & Zou (2003, Found. Phys. 33, 1071-1577) — Short-run simulations appeared to show hydrogen stability
- Nieuwenhuizen (2015, Found. Phys. 45, 1501) — Showed L < 0.588ħ leads to ionization, theoretical analysis
- Nieuwenhuizen (2020, Front. Phys. 8, 335) — 5-scheme renormalization study, all fail

**Does any paper have explicit T_ion(L) quantitative data?** No paper found with systematic T_ion vs. L measurements. Nieuwenhuizen (2015, 2020) shows that L < 0.588 leads to ionization but doesn't provide time-to-ionization as a function of L. Cole & Zou don't provide T_ion data.

**Novelty verdict:** The explicit T_ion(L) data from E003 (e.g., at L=1.0, 10% ionize in 200 periods; at L=0.5, 95% ionize, median T_ion=17 periods) appears genuinely new. The reconciliation of Cole (short-run optimism) with Nieuwenhuizen (pessimism) is a new synthesis.

**Important caveat from E003 itself:** E003 acknowledges a τ discrepancy — the simulation uses τ ≈ 1.57×10⁻⁵ while the physical ALD value is τ_phys = 2α³/3 ≈ 2.6×10⁻⁷ (factor ~60 off). This means the E003 T_ion values are ~60× shorter than the physical hydrogen atom would give. The 17-period median T_ion at L=0.5 corresponds to ~1020 physical periods in real hydrogen units. The 200-period cap for L=1.0 corresponds to ~12,000 physical periods. Nieuwenhuizen's "tens of thousands of orbits" stabilization claim falls within this range. The physical T_ion values need to be stated with this calibration factor applied.

### Claim D: ω³ Feedback Unifies All SED Failures

**Prior art found:**
- Boyer (1976): ZPF is not equilibrium for nonlinear oscillators — established the non-equilibrium nature
- Claverie-Diner (1977): ω³ colored noise breaks Fokker-Planck for nonlinear systems — established the technical mechanism
- Santos (2022): SED fails for non-quadratic H — established the quantum-mechanical framing
- NO paper found that explicitly states "the ω³ feedback mechanism unifies the failures in anharmonic oscillator, double-well tunneling, and hydrogen"

**Novelty verdict:** The explicit unification narrative — tracing all three failures to ω³ × ω_local mismatch — is genuinely new as a stated claim. Each component (Boyer's non-equilibrium, Claverie's Fokker-Planck failure, Santos' ℏ-order analysis) was known separately, but the unified ω³ feedback narrative tying together double-well, anharmonic, and hydrogen is new.

**Qualifier:** "Unifies" may be too strong a word. The precise mechanism differs between systems (sign reversal at barrier top, divergence at nucleus, continuous bias for anharmonic). A more careful statement: "the ω³ energy balance mismatch is the common enabling condition for all SED nonlinear failures, manifesting differently in each system."

---

## Section 5: Overall Recommendation for Phase 3

### What Has Been Established

**Solid ground:**
1. The three SED failures (anharmonic, double-well, hydrogen) share a common enabling condition: ω³ ZPF non-equilibrium with nonlinear oscillators. This is new as a unified narrative, supported by Boyer 1976, Claverie-Diner 1977, and Santos 2022.
2. All three proposed fixes (Local FDT, spectral index n<3, dressed particle) either fail (Fix C, exhaustively tested by Nieuwenhuizen) or are novel but wrong direction (Fix A, Fix B). The fix space is genuinely bleak.
3. T_ion(L) data (Claim C) is genuinely new and the reconciliation of Cole vs. Nieuwenhuizen is valuable.

**Needs more work:**
1. The Γ_SED/Γ_WKB formula (Claim A) has only 2 data points and a ~15% discrepancy at the better-sampled point. Should be tested at 4-5 λ values.
2. The C_xx(d) = cos(ω₀d/c) correlation (Claim B) needs a 3D calculation to assess whether the 1D result survives in the physical ZPF.
3. The crossover condition S_WKB = V_barrier/E_zpf needs clearer physical interpretation.

### Recommended Phase 3 Explorations

**Phase 3A (Priority 1) — Adversarial Review of Claim A:**
Run systematic numerical tests of the Γ_SED/Γ_WKB formula at 5 values of λ (spanning 3 orders of magnitude). Check whether the formula exp(S_WKB − V_barrier/E_zpf) holds or needs modification. Compare carefully to Faria & França's exp(−ΔU/E_zpf) — these are different formulas and one or both could be wrong.

**Phase 3B (Priority 2) — 3D ZPF Correlation:**
Compute C_xx(d) for two oscillators in the full 3D multi-mode ZPF. Does the cos(ω₀d/c) result survive? If it averages to near-zero in 3D, the E002 result is a 1D artifact with no physical relevance.

**Phase 3C (Priority 3) — Santos ħ-order Analysis:**
Do the missing second-order-in-ħ corrections from Santos' analysis qualitatively predict the 15-18% residual in the anharmonic oscillator, the 18× tunneling overestimate in the double-well, and the L < 0.588 ionization threshold in hydrogen? If the quantitative predictions match, this would be a strong test of the unified narrative.

**Phase 3D (Phase 3 Final) — Synthesis Report:**
After 3A, 3B, 3C: write a synthesis paper structure with:
- Introduction: Standard SED and its domain of validity
- Section 2: Three new numerical results (E001-E003 verified)
- Section 3: Root cause — ω³ feedback unified narrative
- Section 4: Why no simple fix exists (Nieuwenhuizen exhaustive + Fix A/B analysis)
- Section 5: Santos' ħ-order framing as the exact mathematical statement

### Assessment of the Overall SED Strategy

After Phase 1 (Strategy-001: harmonic/anharmonic) and Phase 2 (Strategy-002: double-well, coupled oscillators, hydrogen), the picture is:

**SED as a research program:** The strongest finding is NEGATIVE — the ω³ energy balance mismatch is fundamental, and there is no known fix that preserves SED's successes while correcting its failures. This is consistent with Santos' finding that SED = first-order-in-ħ QED, which is a fixed approximation, not a complete theory.

**SED as a generator of novel results:** Despite the theoretical failures, the numerical explorations have produced:
1. The first quantitative T_ion(L) data for hydrogen in SED (E003)
2. The first CHSH computation from SED (E002)
3. A new barrier-crossing rate formula with an explicit crossover condition (E001, needs verification)
4. A unified ω³ feedback narrative connecting all failures

These are worth reporting even in the context of SED's known failures — they clarify WHERE and HOW SED fails, which is useful for anyone building modified theories.

---

## References

1. Boyer, T.H. (1976). Equilibrium of random classical electromagnetic radiation in the presence of a nonrelativistic nonlinear electric dipole oscillator. *Phys. Rev. D* 13, 2832.

2. Boyer, T.H. (2019). Stochastic Electrodynamics: The Closest Classical Approximation to Quantum Theory. *Atoms* 7(1):29. arXiv:1903.00996.

3. Claverie, P., de la Peña-Auerbach, L. & Diner, S. (1977). Stochastic Electrodynamics of non-Linear systems. II. Derivation of a reduced Fokker-Planck equation in terms of relevant constants of motion.

4. Claverie, P. & Diner, S. (1977). Some Remarks about the LAX Approximation in Stochastic Electrodynamics. Technical Report.

5. Pesquera, L. & Claverie, P. (1982). The quartic anharmonic oscillator in stochastic electrodynamics. *J. Math. Phys.* 23, 1315-1322.

6. de la Peña, L. & Cetto, A.M. (2005). The Foundations of Linear Stochastic Electrodynamics. *Found. Phys.* 35, 1675.

7. de la Peña, L., Cetto, A.M. & Valdés Hernández, A. (2015). *The Emerging Quantum: The Physics Behind Quantum Mechanics*. Springer.

8. Santos, E. (2022). On the analogy between stochastic electrodynamics and nonrelativistic quantum electrodynamics. *Eur. Phys. J. Plus.* arXiv:2212.03077.

9. Nieuwenhuizen, T.M. (2020). Stochastic Electrodynamics: Renormalized Noise in the Hydrogen Ground-State Problem. *Frontiers in Physics* 8:335.

10. Nieuwenhuizen, T.M. & Liska, M.T.P. (2015). Simulation of the Hydrogen Ground State in Stochastic Electrodynamics-2: Inclusion of Relativistic Corrections. *Found. Phys.* 45, 1501.

11. Faria, A.J., França, H.M. & Sponchiado, R.C. (2006). Tunneling as a Classical Escape Rate Induced by the Vacuum Zero-point Radiation. *Found. Phys.* 36, 307-320. arXiv:quant-ph/0409119.

12. Cavalleri, G. & Rueda, A. (1983). Zitterbewegung in stochastic electrodynamics and implications on a zero-point field acceleration mechanism. *Lett. Nuovo Cimento* 38.

13. Cole, D.C. & Zou, Y. (2003). Simulation Study of Aspects of the Classical Hydrogen Atom Interacting with Electromagnetic Radiation: Circular Orbits. *Found. Phys.* 33, 1071-1577.

14. Boström, M. et al. (2022). arXiv:2512.16168 — Tunneling in double-well potentials within stochastic quantization (Nelson's SM — NOT SED).
