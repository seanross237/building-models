# Exploration History

## Exploration 001: Ghost Propagator Specification

**Goal:** Derive the specific quantitative prediction for the spin-2 ghost propagator in C²-extended FRG.

**Outcome: PARTIAL SUCCESS**

The prediction was sharpened significantly beyond "the ghost should dissolve somehow," but a fully discriminating numerical prediction remains blocked by one uncomputed quantity.

**Key Results:**
- Ghost mass at NGFP: m₂/k = √(g₁*/g₃*) ≈ 1.42 (from Benedetti et al. fixed-point values). Physical mass: m₂ ~ 0.5–2 M̄_P.
- BH instability threshold: r_H ≈ 0.876/m₂ ≈ 0.6 l_P (sub-Planckian).
- Predicted mechanism: Complex conjugate pole tower (Draper et al. type). Mass divergence RULED OUT for spin-2 (g₃* ≠ 0 at NGFP).
- Computational specification: Compute spin-2 TT propagator in (R + R² + C²) FRG truncation with momentum-dependent form factors.
- Classification: Partially discriminating, novel, numerically specific to factor ~4 for m₂.
- The prediction is a well-specified falsifiable consistency check rather than a sharp discriminating prediction. The deepest discriminating content is the amplitude equivalence test: do scattering amplitudes from the complex pole tower equal fakeon-prescription amplitudes?

**Leads:** Has anyone computed C²-extended FRG propagator? Can amplitude equivalence (fakeon ↔ pole tower) be tested in a toy model? Can c_C be constrained by NGFP critical exponents?

---

## Exploration 002: BH Evaporation Phase Transition — Quantitative Predictions

**Goal:** Derive all quantitative predictions from the BH evaporation phase transition with numbers and classifications.

**Outcome: SUCCEEDED (with caveats)**

12 predictions derived and classified:
- 6 NOVEL (M_crit = 0.31 M_P, T_crit = 0.13 M_P, three-phase picture, transition order, latent heat estimate)
- 4 INHERITED from AS (remnant mass/temperature, heat capacity sign change, PBH DM)
- 1 CONSISTENCY CHECK (M_rem > M_crit ordering)
- 1 DISCRIMINATING (ghost confinement trigger mechanism)

**Critical finding:** Most BH predictions are INHERITED from AS alone. The unified framework's genuine contribution is narrow: a ghost confinement trigger mechanism and specific numerical values (M_crit, T_crit) that are completely unobservable. The endpoint (Planck remnant, T → 0) is entirely from AS. The trigger (Schwarzschild instability) is entirely from QG+F.

**Convention dependence:** m₂ = 1.42 M_P vs m₂ = 1.42 M̄_P changes whether ghost confinement instability is preempted by AS transition or actively drives it. Single largest systematic uncertainty.

---

## Exploration 003: NGFP Predictions for Inflationary Parameters b and δ₃

**Goal:** Determine whether NGFP predicts b and/or δ₃, and whether these resolve the n_s tension.

**Outcome: PARTIALLY SUCCESSFUL**

**Parameter b (logarithmic R² correction): NOT discriminating.**
- Naive estimate b ~ θ/(16π²) ~ 0.01 is not rigorous
- Perturbative FRG formula gives b ~ 10⁻¹⁴, effectively zero
- Suppressed by enormous RG running from Planck to inflationary scales
- Cannot resolve n_s tension (needs b ~ 0.02-0.05)

**Parameter δ₃ (R³ coupling): POTENTIALLY discriminating but incomplete.**
- NGFP R³ fixed-point value: g̃₃* ≈ -(0.86-1.10) × 10⁻² (negative, converged n=3 to n=8)
- R³ direction IS irrelevant (ϑ₃ ≈ -4.17), meaning it IS predicted, not free
- Sign matches phenomenological requirement (both negative)
- BUT: mapping g̃₃* → physical δ₃ has NOT been computed (requires full RG trajectory)
- Needed value: δ₃ ≈ -1.19 × 10⁻⁴ for n_s ≈ 0.974

**Key takeaway:** The correct sign of δ₃ from the NGFP is a promising lead. The full RG flow computation (NGFP → inflationary scales in ≥6-derivative truncation) would be definitive. If it yields δ₃ ≈ -10⁻⁴, the framework has a strong discriminating prediction.

---

## Exploration 004: Higgs Mass Consistency Under Unification

**Goal:** Does the fakeon prescription change the Shaposhnikov-Wetterich Higgs mass prediction?

**Outcome: SUCCEEDED — Classification: CONSISTENCY CHECK**

The fakeon does NOT change the SW prediction. Three independent arguments:
1. Beta functions are prescription-independent (UV divergences unaffected)
2. NGFP is Euclidean (fakeon is a Lorentzian concept)
3. Threshold absorptive parts vanish (ghost too heavy for EW physics)

Upper bound: |Δm_H| < 10⁻⁷ GeV — six orders below experimental uncertainty.

The unified framework inherits the SW Higgs mass prediction unchanged. Dominant uncertainties remain m_top and α_s.

---

## Exploration 005: Three-Domain Prediction Assessment (Spectral Dimension, CC, GW)

**Goal:** Assess predictions in spectral dimension, cosmological constant, and gravitational wave domains.

**Outcome: SUCCEEDED**

- **Spectral Dimension — CONSISTENCY CHECK.** d_s → 2 in UV is universal across ALL QG approaches (Carlip 2019). Framework adds nothing new. Six-derivative extension gives two-step flow (4 → 2 → 4/3) but at trans-Planckian scales — unobservable.
- **Cosmological Constant — INHERITED (nothing new).** Complete blank. No mechanism, no prediction, no novel reformulation. δΛ ~ M₂⁴/(16π²) is 95-111 orders too large.
- **Gravitational Waves — DISCRIMINATING.** Bounded r ∈ [4×10⁻⁴, 4×10⁻³] from fakeon mass constraint M₂ > M₀/4. Lower bound is genuinely unique to QG+F. Testable by LiteBIRD (~2032). r = −8n_T preserved (Bianchi & Gamonal 2025). No blue-tilted stochastic background (that's nonlocal gravity, not QG+F).

**Key takeaway:** Framework's predictive power narrowly concentrated in CMB/inflationary sector. Claims of broad predictive reach should be tempered.

---

## Exploration 006: Devil's Advocate — Adversarial Assessment of All Predictions

**Goal:** Mount 6 specific attacks against all predictions from E001-E005.

**Outcome: SUCCEEDED — devastating**

**Zero genuinely discriminating predictions survive adversarial scrutiny.**

- D1 (ghost pole tower): SERIOUS. Circular — assumes unification to predict unification. Downgraded to CONSISTENCY CHECK.
- D2 (BH phase transition trigger): FATAL. Forever inaccessible. M_rem > M_crit may eliminate the trigger. Reclassified as UNTESTABLE NARRATIVE.
- D3 (bounded r): SERIOUS. Pure QG+F prediction, not unified. Reclassified as INHERITED from QG+F.
- P1 (δ₃ correct sign): SERIOUS. Correct sign insufficient; magnitude unknown and may be orders too small (b parameter precedent). Remains a LEAD, not a prediction.
- C1-C4 (consistency checks): Survive but add no discriminating power.

**Null hypothesis test:** H₀ (compatible-but-separate) explains every claimed prediction equally well. No prediction requires unification.

**Predictive tier: REMAINS FAIL.** The framework is a well-structured research program that identifies important computations, but a research program is not a predictive framework.

**Three computations could upgrade the assessment:** C²-extended FRG propagator, g̃₃* → δ₃ mapping, AF → NGFP trajectory. None have been started.

---

## Exploration 007: Complete Theory Document

**Goal:** Write the definitive theory document — final deliverable of the research program.

**Outcome: SUCCEEDED**

513-line document incorporating:
- Full theory statement (action, two descriptions, QCD analogy, regime structure, five bridges)
- Evidence for/against (prosecution-defense scorecard with adversarial attacks)
- Post-adversarial prediction catalog (11 predictions across 4 tiers)
- Three critical computations
- Comparison to alternatives
- Open problems

**Key takeaway:** The framework is internally consistent, organizationally valuable, and empirically vacuous. Zero novel discriminating predictions survive. It's a research program, not a finished theory. The contribution is organizational: it identifies what computations would resolve the open questions.

---

## Exploration 008: Mission Validation — Formal Assessment

**Goal:** Score the theory against the 5-tier Mission Validation Guide.

**Outcome: SUCCEEDED**

| Tier | Score |
|------|-------|
| 1. Novelty | MARGINAL — Novel synthesis, not a new theory |
| 2. Logical Consistency | PASS — Clean internal logic; survived adversarial testing |
| 3. Explanatory Power | MARGINAL — Explains theory relationships, not nature |
| 4. Compatibility with Reality | PASS — No contradictions; testable (inherited) predictions |
| 5. Depth | PASS — Rich structure; honest edge-cases; valuable questions |

Overall: 3 PASS, 2 MARGINAL, 0 FAIL.

The program reached the boundary of what can be achieved by reasoning about existing theories without performing original calculations. The framework's most valuable contribution is specifying exactly what computations would resolve the open questions.

---

