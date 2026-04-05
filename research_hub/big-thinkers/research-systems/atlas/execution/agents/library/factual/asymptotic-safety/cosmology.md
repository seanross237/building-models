---
topic: asymptotic-safety
confidence: verified
date: 2026-03-25
source: https://cerncourier.com/a/a-safe-approach-to-quantum-gravity/, exploration-007-nonperturbative-QGF (strategy-002)
---

# Asymptotic Safety: Cosmological and Physical Applications

## AS Inflation: Four Distinct Classes

There are **four distinct classes** of AS inflation models in the literature, with different mechanisms and predictions. Critically, most of them produce Starobinsky inflation, not alternatives to it. The characterization of AS inflation as purely "inflaton-free" applies only to the most primitive model.

### Class 1: Bonanno-Reuter Inflaton-Free Inflation (2002)

The original AS inflation model. Running Λ(k) and G(k) near the NGFP drive quasi-de Sitter expansion without an inflaton field — a pure quantum gravity effect.

- **Paper:** Bonanno & Reuter, PRD 65, 043508 (2002)
- **Mechanism:** Near the Reuter fixed point, the effective cosmological constant is large (~M_P^4), driving exponential expansion. As the RG flow moves away from the fixed point, inflation ends naturally.
- **Predictions for r:** NOT sharply predicted — operates in Einstein-Hilbert truncation (only G, Λ running). Perturbation spectrum approximately scale-invariant.
- **Status:** Foundational but incomplete. The "r up to ~0.01" number commonly attributed to AS does NOT come from this model.

### Class 2: Bonanno-Platania Modified Starobinsky (2015, 2018)

RG improvement of R+R² gravity near NGFP generates a logarithmic correction:

    L_eff = M²_P R/2 + (a/2) R² / [1 + b ln(R/μ²)]

Parameter b encodes anomalous scaling from NGFP critical exponents.

- **Papers:** Bonanno & Platania, arXiv:1507.03375; Liu, Prokopec & Starobinsky, PRD 98, 043505 (2018)
- **Key predictions:**
  - b = 0: Reduces EXACTLY to standard Starobinsky. r ≈ 0.003, n_s ≈ 0.965
  - b ~ 10⁻² (maximal AS correction): r ≈ 0.01, n_s ≈ 0.970–0.975
  - Running α ≈ −5 × 10⁻⁴ (same as Starobinsky) across all b
  - For N = 50–65 e-folds, r spans [0.003, 0.01] depending on b
- **CRITICAL:** This is NOT inflaton-free. It IS Starobinsky inflation with a quantum gravity correction to the R² coefficient's running. The R² scalaron is still the inflaton.
- **Note:** b is NOT uniquely determined by AS — it depends on truncation-dependent critical exponents at the NGFP.

### Class 3: Starobinsky from AS RG Flow (Codello 2014, Gubitosi 2018)

Multiple groups show the NGFP naturally generates Starobinsky inflation:

- **Codello, D'Odorico, Pagani (2014):** Non-perturbative RG for G and R² coupling. At the NGFP, the R² coupling VANISHES, explaining the smallness of primordial fluctuations. Predictions identical to Starobinsky: r ≈ 0.003, n_s ≈ 0.965. Paper: PRD 91, 103530; arXiv:1311.0881
- **Gubitosi, Ooijer, Ripken, Saueressig (2018):** f(R) truncation to second order shows trans-Planckian dynamics **flows to Starobinsky inflation** at early times, standard Einstein + Λ at late times. Same predictions as Starobinsky. Paper: JCAP 1812, 004; arXiv:1806.10147

### Class 4: Emergent Inflaton Potential / Running G Cosmology (2024)

- **Bonanno et al. (2024/2025):** PRD 111, 103519; arXiv:2405.02636. Running G(ε) = G_N/(1 + ε/ε_c) generates quasi-de Sitter phase. ε_c encodes g* = 540π/833. Focuses on background evolution; sharp r, n_s predictions not yet published.
- **Pawlowski et al. (2024):** arXiv:2406.10170. Scalar-tensor AS inflation. Inflaton potential emerges from integration of RG flow equations starting at NGFP. Approximate plateau potential (not exactly R²). Predictions: n_s ≈ 0.965, r ≈ 0.005, N_ef ≈ 66 — compatible with observations and slightly above pure Starobinsky.

### Summary Table: AS Inflation Predictions for r

| Model | Truncation | Mechanism | r prediction | n_s |
|-------|-----------|-----------|-------------|-----|
| Bonanno-Reuter 2002 | Einstein-Hilbert | Λ(k) running, inflaton-free | Not sharply predicted | ~scale-inv. |
| Bonanno-Platania 2015/18 | R+R²+log | Modified Starobinsky | 0.003–0.01 (b-dependent) | 0.965–0.975 |
| Codello et al. 2014 | R+R²+R³ | Starobinsky from NGFP | ~0.003 | ~0.965 |
| Gubitosi et al. 2018 | f(R) to O(R²) | RG flow → Starobinsky | ~0.003 | ~0.965 |
| Bonanno et al. 2024 | Einstein-Hilbert+matter | Running G cosmology | Not computed | — |
| Pawlowski et al. 2024 | Scalar-tensor | Emergent potential from RG | ~0.005 | ~0.965 |

### Key Insight: Most AS Inflation IS Starobinsky Inflation

The truly "inflaton-free" model is only the original Bonanno-Reuter (2002), which is the most primitive (Einstein-Hilbert truncation) and has the least sharp predictions. All refinements converge toward Starobinsky or Starobinsky-like inflation. The "r up to ~0.01" comes specifically from Bonanno-Platania's maximal b correction; the majority of AS inflation papers predict r ≈ 0.003, indistinguishable from QG+F.

### Discriminating Test: Tensor-to-Scalar Ratio

See `cross-cutting/qgf-vs-as-cmb-discrimination.md` for full discrimination analysis. Summary: r > 0.005 favors Bonanno-Platania AS (large b) over QG+F; r < 0.003 favors QG+F; r ≈ 0.003 cannot distinguish them.

## Gravitational Vacuum Condensate and Running G at Cosmological Scales

### Hamber's Lattice Gravity Results

The Regge-Wheeler lattice path integral formulation reveals a nontrivial gravitational vacuum condensate (Hamber, arXiv:1707.08188; Symmetry 11(1), 87, 2019) -- analogous to the gluon and chiral condensates in QCD:
- Critical exponent nu ~ 1/3 (conjectured universal)
- A nonperturbative scale xi, directly analogous to Lambda_QCD

### Running of Newton's Constant at Large Distances

    G(r) = G_0[1 + c_0(l_P/xi)^{1/nu} + c_1(r/xi)^{1/nu} + ...]

where xi ~ 1/sqrt(Lambda) is the gravitational correlation length. This predicts deviations from GR at distances comparable to the Hubble radius.

The running is **power-law** (not logarithmic), which is qualitatively different from perturbative QG+F. Perturbative running (Exploration 005) gives Delta_theta/theta ~ 10^{-14}; the non-perturbative condensate running could be potentially observable.

### Testability

- Precision tests of gravity at cosmological scales (modified expansion history)
- Deviations from LCDM in large-scale structure
- Running of effective Newton constant measurable via CMB + BAO + type Ia supernovae
- Future high-precision satellite experiments

## What Perturbative QG+F Cannot Reproduce

The non-perturbative sector makes at least 4 predictions invisible to perturbative QG+F:

| Prediction | Non-Perturbative Source | Testable? | Timescale |
|-----------|----------------------|-----------|-----------|
| Planck remnants | BR black holes from RG improvement | Via PBH dark matter, GW | 2030s (LISA) |
| Running G at cosmic scales | Vacuum condensate (Hamber) | Precision cosmology | 2030s |
| Inflation without inflaton | Reuter fixed point (Bonanno-Reuter 2002 only; most AS models predict Starobinsky) | r ~ 0.003–0.01 vs r ~ 0.0004–0.0035 | 2030s (LiteBIRD) |
| Higgs mass prediction | SM at the fixed point | Already confirmed (125 GeV) | Done |

## Connections to Particle Physics

The Reuter fixed point may provide a unified description of all forces:
- Profound consequences for physics inside black holes
- Predictions for SM parameters (Higgs mass, top quark mass; see `standard-model.md`)
- Constraints on BSM physics
- Specific relations between coupling constants testable via particle physics

Research has progressed from theoretical foundations toward empirical testing, becoming "an observationally guided endeavour."

## Textbook Reference

Martin Reuter and Frank Saueressig: "Quantum Gravity and the Functional Renormalization Group: The Road towards Asymptotic Safety" (Cambridge Monographs on Mathematical Physics).

Sources: CERN Courier; Bonanno & Reuter (2002, PRD 65, 043508); Bonanno & Platania (arXiv:1507.03375); Liu, Prokopec & Starobinsky (2018, PRD 98, 043505); Codello, D'Odorico, Pagani (2014, PRD 91, 103530; arXiv:1311.0881); Gubitosi et al. (2018, JCAP 1812, 004; arXiv:1806.10147); Bonanno et al. (2024/2025, PRD 111, 103519; arXiv:2405.02636); Pawlowski et al. (2024, arXiv:2406.10170); Hamber (arXiv:1707.08188; Symmetry 11(1), 87, 2019); Shaposhnikov & Wetterich (2010); exploration-004-inflation-prediction-reconciliation
