# Mission Complete — Stochastic Electrodynamics

**Date:** 2026-03-27
**Strategies executed:** 3
**Total explorations:** 16 (6 + 6 + 4)
**Highest tier achieved:** Tier 4 (partial), with Tier 3 fully satisfied across 5 systems

---

## Central Answer

**Is field quantization necessary?** Yes.

SED (classical electrodynamics + a real Lorentz-invariant zero-point radiation field) reproduces quantum mechanics exactly for all linear (quadratic Hamiltonian) systems. This is not approximate — Santos (2022) proved that SED is mathematically equivalent to the O(ℏ) term of QED in the Weyl-Wigner representation. For linear systems, all higher-order terms vanish, so SED is exact.

For nonlinear systems, SED fails. The O(ℏ²) Moyal bracket corrections are structurally absent from SED, and no simple modification can recover them without importing quantum structure. We verified this computationally across five independent systems:

| System | SED Result | QM/QED Result | Discrepancy |
|--------|-----------|---------------|-------------|
| Harmonic oscillator | var_x = 0.507 | 0.500 | 1.4% (numerical noise) |
| Quartic anharmonic (β=1) | var_x = 0.303 | 0.257 | **+17.8%** |
| Double-well tunneling | Γ_SED/Γ_exact = exp(0.072 + 1.049·x) | exact QM rate | **1.3× to 18× overestimate** |
| Hydrogen (L=1.0 Bohr orbit) | T_ion = 19,223 periods | stable | **self-ionizes** |
| Two coupled oscillators | C_xx(d) = j₀(q) − j₂(q)/2 | C_xx = 0 | **nonzero at all d** |

The root cause across all failures is the ω³ spectral density of the zero-point field. In nonlinear systems, anharmonicity shifts effective frequencies, and the ω³ dependence creates a positive feedback loop (higher frequency → more ZPF power → more energy injection). The harmonic oscillator is immune because its frequency is fixed. This mechanism was identified in Strategy-001, confirmed in Strategy-002 across three additional systems, and connected to the Santos O(ℏ²) framework in Strategy-003.

Three proposed SED modifications were evaluated and all fail: local fluctuation-dissipation theorem (worsens failures), non-cubic spectral index (breaks Lorentz invariance), and dressed-particle renormalization (Nieuwenhuizen 2015/2020 — does not prevent hydrogen ionization).

**Prior art:** Santos (2022) proves this mathematically. Nieuwenhuizen (2020) states it explicitly for hydrogen. de la Peña & Cetto (2014) dispute it. The debate is live. Our contribution is systematic quantitative evidence across five systems under one investigation, with specific numbers that make the argument concrete.

---

## Mission Targets — Status

| Target | Status | Key Result |
|--------|--------|------------|
| Hydrogen spectrum | ✅ Addressed | No spectrum — self-ionizes. T_ion(L) ≈ 37,527 × L^6.44. L=1.0 median: 19,223 periods |
| Bell inequality violations | ✅ Addressed | S ≤ 2 always (trivially local realistic). No Bell violation possible in SED |
| Anomalous magnetic moment (g-2) | ⚠️ Not attempted | SED has no spin — intractable without fundamental extension. Ruled out in Strategy-001 survey |
| Multi-particle entanglement | ✅ Addressed | ZPF creates correlations (C_xx ≠ 0) but they are classical — never violate Bell. Correlations decay as 1/d in 3D |
| Minimal modification | ✅ Addressed | All three tested modifications fail. The needed modification IS the O(ℏ²) Moyal bracket — i.e., quantum mechanics itself |

---

## Consolidated Novel Claims

### Claim 1 — Convergence Law for ALD-SED Quartic Oscillator [STRONGEST]

**Claim:** The ALD-SED position variance for the quartic anharmonic oscillator (V = ½ω₀²x² + ¼βx⁴) overshoots the QM result by 17.8% at β=1, and the residual converges as Δ(⟨x²⟩)/⟨x²⟩_QM ∝ τ^{0.23} × ω_max^{-0.18}. Extrapolation: reducing the residual to 1% requires τ/τ_phys ~ 10^{-100} — physically inaccessible.

**Evidence:**
- ALD simulation at 7 β values, 200 trajectories each. var_x = 0.303 ± 0.004 vs QM 0.257 at β=1.0
- Convergence study across multiple (τ, ω_max) pairs; power-law fit to residual
- Connected to Santos O(ℏ²): the O(ℏ²) Moyal correction is negative (QM more localized than SED), consistent with the sign of the excess
- First numerical SED simulation of the anharmonic oscillator — Pesquera & Claverie (1982) were analytic only

**Novelty search:** Pesquera & Claverie (1982) proved analytically that SED fails for the quartic oscillator at O(β²). They gave no convergence exponents. The specific exponents (0.23 in τ, −0.18 in ω_max) and the "physically inaccessible" extrapolation appear in no prior paper. Santos (2022) implies the failure but gives no quantitative convergence law.

**Strongest counterargument:** The exponents are measured at specific simulation parameters and may depend on the UV cutoff scheme and β value. A referee could argue they are not universal. Three data points per exponent is thin.

**Verdict: PARTIALLY VERIFIED.** The qualitative conclusion (physically irreducible failure) is robust. The specific exponents are empirical observations, not analytically derived.

**Novelty: 3/5.** Quantitative extension of a known qualitative result.

---

### Claim 2 — Physical-τ T_ion(L) Power Law for SED Hydrogen

**Claim:** With physical τ = 2.591×10⁻⁷ a.u., the SED hydrogen ionization time for circular orbits follows T_ion ≈ 37,527 × L^{6.44} (R²=0.996), and the L=1.0 circular Bohr orbit ionizes with median time 19,223 orbital periods.

**Evidence:**
- 140 trajectories total: 20 per L value × 7 L values (0.4–1.0)
- ⟨r⟩ = 1.509 a₀ ≈ QM 1s value (1.500 a₀) confirming physical setup
- Power law R² = 0.996 for L = 0.4–0.8
- Non-linear τ-scaling (26–89× vs prior wrong-τ data) suggests richer physics than simple diffusion

**Novelty search:** Nieuwenhuizen & Liska (2015) established qualitative self-ionization. They did not provide: correct physical τ, a statistical sample (20 trajectories per L), a quantitative T_ion(L) table, or the power law exponent. Nieuwenhuizen (2020) confirmed the result persists through renormalization but gives no quantitative data at physical τ.

**Strongest counterargument:** The power law L^{6.44} is an empirical fit to 5 points. The exponent is not theoretically predicted. UV cutoff ω_max = 100 a.u. introduces dependence.

**Verdict: PARTIALLY VERIFIED.** First quantitative T_ion table at correct physical parameters. The qualitative phenomenon is prior art; the specific numbers are new.

**Novelty: 3/5.** Quantitative extension of a known qualitative result.

---

### Claim 3 — Classical < QM < ALD Hierarchy with Negative Moyal Correction

**Claim:** For the quartic oscillator at β=1, the ordering classical(0.183) < QM(0.257) < ALD/SED(0.303) shows that the O(ℏ²) Moyal correction is negative — QM is MORE localized than SED. This is consistent with Santos (2022) and verifiable from the Moyal bracket structure.

**Evidence:**
- Three independent calculations: classical Boltzmann at T=ℏω/2, QM exact, ALD simulation
- Santos O(ℏ²) correction term: −(ℏ²β²/8)∂²⟨x²⟩/∂p² has negative sign, consistent with QM < SED
- O(ℏ²) correction is zero at O(β) by symmetry (Moyal source term odd in x), consistent with Pesquera-Claverie (1982)

**Novelty search:** Santos (2022) proves the framework but doesn't give the sign for this specific system. No prior paper gives all three values in this comparison for the quartic oscillator.

**Strongest counterargument:** The classical Boltzmann baseline at T=ℏω/2 is not a well-defined SED limit for the quartic oscillator. The "hierarchy" conflates different physical pictures.

**Verdict: PARTIALLY VERIFIED.** The three numbers are correct and the Moyal connection is valid. The baseline objection is fair but doesn't invalidate the main finding.

**Novelty: 3/5.** New specific comparison, known general framework.

---

### Claim 4 — SED Tunneling Rate Formula

**Claim:** SED barrier-crossing rates follow ln(Γ_SED/Γ_exact) = 0.072 + 1.049(S_WKB − √2/(4λ)) with R²=0.9998 across 4 decades.

**Evidence:**
- Computed at 7 λ values from Langevin SED simulation of double-well potential
- Verified in Strategy-002 E005 (independent recomputation at 4 λ values)
- Slope=1.049 is 7σ from 1.0; confirmed to be a finite-τ/ω_max artifact (NOT O(ℏ²))
- ω_local = √2 universality for all symmetric double wells (analytic derivation)

**Novelty search:** Faria-França (2004) derived the exponential structure of SED tunneling (Kramers-like Boltzmann form). The ratio-to-QM formulation and the numerical verification across 4 decades are new. The S_WKB crossover condition is new.

**Strongest counterargument:** The exponential structure is prior art (Faria-França 2004). The R² and specific coefficients are from Langevin approximation, which Strategy-001 proved fails at O(β) — the true ALD result may differ.

**Verdict: PARTIALLY VERIFIED.** Novel as a precise numerical verification; partially prior art in structure.

**Novelty: 2/5.** Numerical confirmation of known functional form.

---

### Claim 5 — 3D ZPF Spatial Correlator as SED–QM Discriminant

**Claim:** C_xx(d) = j₀(ω₀d/c) − ½j₂(ω₀d/c) in 3D. QM predicts 0 for uncoupled oscillators. Testable experimental discriminant.

**Evidence:**
- Analytic derivation from first principles
- Verified by 4 independent methods (integration by parts, quadrature, Bessel identity, Monte Carlo N=500k) — all machine precision
- Near field: C_xx ≈ 1 − q²/5; Far field: C_xx ≈ (3/2)sin(q)/q ∼ 1/d

**Novelty search:** The formula is the xx-component of the standard transverse EM propagator at equal times. Derivable from Boyer (1975) in 1-2 lines. The framing as an experimental SED–QM discriminant is the contribution, not the formula itself.

**Strongest counterargument:** Any physicist reading Boyer (1975) would notice this immediately. The "discriminant" framing requires identifying a specific experiment, which we haven't done.

**Verdict: VERIFIED (formula correct) but NOVELTY LOW.** Value is as a precise experimental target, not as a derivation.

**Novelty: 2/5.** Standard result, new framing.

---

### Claim 6 — ω³ Feedback as Unified Root Cause

**Claim:** All SED failures (anharmonic oscillator, tunneling, hydrogen, coupled oscillators) share a common root cause: the ω³ spectral density of the ZPF creates a positive feedback loop in nonlinear systems.

**Evidence:**
- Anharmonic: frequency shift up → ω³ delivers more power → excess variance
- Tunneling: excess energy injection → higher escape rate
- Hydrogen: angular momentum loss → higher orbital frequency → more noise power → self-ionization
- Coupled oscillators: ω³ spectral coupling creates correlations absent in QM

**Novelty search:** The ω³ spectral density is a known feature of SED. Boyer, de la Peña, and others discuss it. The specific statement that it unifies ALL failures through a single positive feedback mechanism is our synthesis, not in any single prior paper. But any SED practitioner would immediately see this.

**Strongest counterargument:** This is an explanatory narrative, not a theorem. Each system fails for somewhat different detailed reasons. "ω³ feedback" is a shared theme but not a rigorous unification.

**Verdict: CONJECTURED.** Physically reasonable synthesis, not a proven mechanism.

**Novelty: 2/5.** Synthesis of known elements.

---

## Strategy Arc Summary

| Strategy | Focus | Explorations | Key Achievement |
|----------|-------|-------------|-----------------|
| 001 | Depth: reproduce + extend anharmonic | 6/10 | First numerical quartic SED, convergence law τ^{0.23} |
| 002 | Breadth: tunneling + hydrogen + coupled | 6/10 | Tunneling formula R²=0.9998, T_ion data, ω³ unification |
| 003 | Finish: Santos connection + cleanup + synthesis | 4/4 | 3D correlator, physical-τ hydrogen, honest novelty assessment |

**Total exploration budget:** 16 explorations across 3 strategies.

---

## Tier Assessment

| Tier | Criterion | Status |
|------|-----------|--------|
| 1 | Reproduction | ✅ Harmonic oscillator reproduced (var_x = 0.507 vs QM 0.500) |
| 2 | Extension | ✅ Five systems computed with quantitative QM comparison |
| 3 | Boundary | ✅ ω³ feedback identified as root cause across 5 systems |
| 4 | Novel Insight | ⚠️ Partial — convergence law exponents and T_ion table are new, but novelty is incremental (quantitative extension of known qualitative results). Grand conclusion is prior art (Santos 2022, Nieuwenhuizen 2020) |
| 5 | Implications | ⚠️ Partial — "field quantization is necessary for nonlinear systems" is clearly stated but is a known conclusion. Our contribution is the quantitative evidence, not the conclusion itself |

**Honest summary:** This mission produced a comprehensive quantitative case for the necessity of field quantization, grounded in computation across 5 independent systems. The individual novel claims are incremental (quantitative extensions of known qualitative results), not breakthrough insights. The most novel output is the convergence law (τ^{0.23} × ω_max^{-0.18}), which demonstrates that SED's failure for nonlinear systems is not merely difficult to fix — it is physically irreducible. The mission's strength is its breadth and computational rigor, not the depth of any single finding.

---

## Open Questions for Future Work

1. **Analytically derive the convergence exponents** (τ^{0.23} × ω_max^{-0.18}) from Fokker-Planck perturbation theory. Would upgrade the convergence law from empirical to derived.
2. **Experimental proposal for C_xx(d) discriminant.** Identify a quantum optics or photonic crystal experiment that could test SED's nonzero C_xx vs QM's zero.
3. **Test de la Peña/Cetto LSED** against our specific quantitative predictions. Their "Emerging Quantum" framework claims to extend SED — do they predict var_x ≠ 0.303?
4. **ALD tunneling rates.** Our tunneling formula uses Langevin, which Strategy-001 proved fails at O(β). The true ALD tunneling rate has not been computed.
