# Exploration 004: Can the Inflationary Predictions (r, n_s) of QG+F and AS Be Reconciled?

## Goal
Pin down what Asymptotic Safety specifically predicts for the tensor-to-scalar ratio r under different truncations, compare with QG+F (Starobinsky) predictions, and determine whether the two frameworks' inflationary predictions are fundamentally compatible or irreconcilable.

## Summary of Pre-loaded Context
- **QG+F:** r ∈ [0.0004, 0.004], n_s ≈ 0.967 (Starobinsky mechanism via R²)
- **AS:** r "up to ~0.01" from Reuter FP effects, inflaton-free inflation
- **Discriminator:** r is the key observable separating the two

---

## 1. AS Inflationary Predictions — Detailed Breakdown

The pre-loaded context described AS inflation as "inflaton-free" with r "up to ~0.01." This turns out to be a significant oversimplification. There are actually **four distinct classes** of AS inflation models in the literature, with very different mechanisms and predictions. Critically, most of them ARE Starobinsky inflation, not alternatives to it.

### 1A. Bonanno-Reuter Inflaton-Free Inflation (2002)
- **Mechanism:** Running Λ(k) and G(k) near the NGFP drive quasi-de Sitter expansion. No inflaton field. Pure quantum gravity effect.
- **Paper:** Bonanno & Reuter, PRD 65, 043508 (2002)
- **Predictions for r:** The original model does NOT make sharp predictions for r — operates in Einstein-Hilbert truncation (only G, Λ running). Perturbation spectrum approximately scale-invariant, but detailed r predictions require going beyond this truncation.
- **Status:** Foundational but incomplete. The "r up to ~0.01" number commonly attributed to AS does NOT come from this model — it comes from the Bonanno-Platania refinements (1B below).

### 1B. Bonanno-Platania Refined Starobinsky Model (2015, 2018)
- **Mechanism:** RG improvement of R+R² gravity near NGFP generates logarithmic correction:
  `L_eff = M²_P R/2 + (a/2) R² / [1 + b ln(R/μ²)]`
  Parameter b encodes anomalous scaling from NGFP critical exponents.
- **Papers:** Bonanno & Platania, arXiv:1507.03375; Liu, Prokopec & Starobinsky, PRD 98, 043505 (2018)
- **KEY PREDICTIONS:**
  - **b = 0:** Reduces EXACTLY to standard Starobinsky. r ≈ 0.003, n_s ≈ 0.965
  - **b ~ 10⁻²** (maximal AS correction): r ≈ **0.01**, n_s ≈ 0.970–0.975
  - Running α ≈ −5 × 10⁻⁴ (same as Starobinsky) across all b
  - For N = 50–65 e-folds, r spans [0.003, 0.01] depending on b
- **CRITICAL INSIGHT:** This is NOT "inflaton-free." It IS Starobinsky inflation with a quantum gravity correction to the R² coefficient's running. The R² scalaron is still the inflaton.

### 1C. Codello-D'Odorico-Pagani "Asymptotically Safe Starobinsky Inflation" (2014)
- **Mechanism:** Non-perturbative RG for G and R² coupling. At the NGFP, the R² coupling VANISHES, explaining the smallness of primordial fluctuations.
- **Paper:** PRD 91, 103530 (2014), arXiv:1311.0881
- **Predictions for r:** Essentially identical to Starobinsky (r ≈ 0.003). The UV FP sets initial conditions but doesn't change inflationary dynamics at CMB scales.

### 1D. Gubitosi-Ooijer-Ripken-Saueressig (2018) — RG Flow to Starobinsky
- **Paper:** JCAP 1812, 004 (2018), arXiv:1806.10147
- **Key result:** f(R) truncation to second order: trans-Planckian dynamics **flows to Starobinsky inflation** at early times, standard Einstein + Λ at late times.
- **Predictions for r:** Same as Starobinsky. The paper's thesis is that AS naturally generates Starobinsky inflation.

### 1E. Bonanno et al. (2024) — Emergent Cosmology from Running G
- **Paper:** PRD 111, 103519 (2025), arXiv:2405.02636
- **Mechanism:** Running G(ε) = G_N/(1 + ε/ε_c) generates quasi-de Sitter phase.
- **Predictions for r:** Paper focuses on background evolution and transition scale to classical cosmology. Does not provide sharp r, n_s predictions from perturbation analysis.

### 1F. Scalar-Tensor AS Inflation — Emergence of Inflaton Potential (2024)
- **Paper:** arXiv:2406.10170 (Pawlowski et al.)
- **Mechanism:** Inflaton potential emerges from integration of RG flow equations starting at NGFP. Approximate plateau potential (not exactly R²).
- **Predictions:** n_s ≈ 0.965, r ≈ 0.005, N_ef ≈ 66. Compatible with observations.
- **Note:** The r ≈ 0.005 is slightly higher than pure Starobinsky but within the QG+F window.

### Summary Table: AS Inflation Predictions for r

| Model | Truncation | Mechanism | r prediction | n_s |
|-------|-----------|-----------|-------------|-----|
| Bonanno-Reuter 2002 | Einstein-Hilbert | Λ(k) running, inflaton-free | Not sharply predicted | ~scale-inv. |
| Bonanno-Platania 2015/18 | R+R²+log | Modified Starobinsky | 0.003–0.01 (b-dependent) | 0.965–0.975 |
| Codello et al. 2014 | R+R²+R³ | Starobinsky from NGFP | ~0.003 | ~0.965 |
| Gubitosi et al. 2018 | f(R) to O(R²) | RG flow → Starobinsky | ~0.003 | ~0.965 |
| Bonanno et al. 2024 | Einstein-Hilbert+matter | Running G cosmology | Not computed | — |
| Pawlowski et al. 2024 | Scalar-tensor | Emergent potential from RG | ~0.005 | ~0.965 |

---

## 2. QG+F Inflationary Predictions — Cross-check

### Anselmi-Piva: Weyl-Squared Effects on Starobinsky Inflation
The QG+F Lagrangian is R + R²/(6m²_φ) + C²/(2m²_χ), where C² is the Weyl-squared term and the spin-2 ghost (mass m_χ) is quantized as a fakeon.

Key results from Anselmi & Piva, JHEP 07 (2020) 211 (arXiv:2005.10293):
- **r prediction:** 0.4 ≲ 1000r ≲ 3.5, i.e., **r ∈ [0.0004, 0.0035]**
- Equivalently: 4/3 < N²r < 12 at leading order in e-folds N
- **Fakeon mass bound:** m_χ > m_φ/4 (consistency requirement)
- The Weyl-squared term modifies tensor perturbations but the standard relation r ≈ −8n_T is preserved
- The C² term does NOT affect the background FRW evolution (conformally invariant), only perturbations

### Bianchi-Gamonal: Precision Predictions with Self-Consistent W² Corrections (2025)
Paper: arXiv:2506.10081 (June 2025). Treats W² perturbatively via reduction of order:
- **r ≈ 3(1 − β/6α)(n_s − 1)²** where α is the R² coupling and β is the W² coupling
- For β > 0, r is **systematically reduced** below pure Starobinsky
- Tensor and scalar sound speeds differ: c_t/c_s ≈ 1 + β/(6α)
- Results computed to N³LO (next-to-next-to-next-to-leading order)
- **Key point:** Including W² (as QG+F requires) pushes r DOWN from Starobinsky, not up

### Anselmi 2023 Causality Bound
PRD 108, 083526 (2023): "Causality bounds in quadratic inflation from purely virtual particles"
- Pure quadratic inflation (V = m²φ²) with R+C² fakeon gravity is ruled out by causality constraints.
- Starobinsky inflation (R² inflaton) remains viable.
- This constrains the inflationary model within QG+F to be specifically Starobinsky-type.

### QG+F Summary
- **r ∈ [0.0004, 0.0035]** from the full R+R²+C² theory with fakeon
- The C² term reduces r below pure Starobinsky (r ≈ 0.003 for N ≈ 55)
- n_s ≈ 0.967 (standard Starobinsky)
- The six-derivative extension can push r up to ~0.0045 and n_s to ~0.974

---

## 3. Direct Comparisons in the Literature

### Has anyone explicitly compared AS and QG+F inflation predictions?
**No.** I found no paper that directly compares the two frameworks' inflationary predictions side by side. This is a gap in the literature.

### The closest comparison: AS Starobinsky papers vs. QG+F Starobinsky papers
- Codello et al. (2014) and Gubitosi et al. (2018) show AS naturally produces Starobinsky inflation → r ≈ 0.003
- Anselmi & Piva (2020) show QG+F naturally produces Starobinsky inflation → r ∈ [0.0004, 0.0035]
- These are **compatible predictions**. Both derive from the same R² inflaton mechanism.

### The "r up to 0.01" claim is misleading
The pre-loaded context stated AS predicts "r up to ~0.01." This comes specifically from Bonanno-Platania's logarithmic correction model with b ~ 10⁻², which represents the maximum AS departure from pure Starobinsky. But:
1. This model reduces to Starobinsky when b = 0
2. The parameter b is NOT uniquely determined by AS — it depends on critical exponents at the NGFP which are truncation-dependent
3. The majority of AS inflation papers (Codello 2014, Gubitosi 2018) predict r ≈ 0.003, indistinguishable from QG+F
4. Only the Bonanno-Platania model with maximal b gives r ≈ 0.01, and even they acknowledge this is the upper end

---

## 4. Are the Mechanisms Compatible or Distinct?

### The key realization: Both theories predict Starobinsky inflation

This is the central finding of this exploration. The pre-loaded framing — "AS inflation is inflaton-free, QG+F inflation is Starobinsky" — is **incorrect** for the most developed AS models:

1. **Codello et al. (2014):** AS Starobinsky inflation — the NGFP explains WHY R² is small enough
2. **Gubitosi et al. (2018):** AS RG flow produces Starobinsky inflation explicitly
3. **Bonanno-Platania (2015/18):** A logarithmic deformation OF Starobinsky from NGFP effects
4. **Pawlowski et al. (2024):** Emergent inflaton potential from AS, r ≈ 0.005

The truly "inflaton-free" Bonanno-Reuter (2002) model is the original one, but it's also the most primitive (Einstein-Hilbert truncation) and the one with the least sharp predictions. All refinements have converged toward Starobinsky or Starobinsky-like inflation.

### Compatibility scenario
If QG+F and AS are the same theory, the natural picture is:
- The NGFP (AS) determines the UV initial conditions for the R² coupling
- The R² coupling flows to values consistent with Starobinsky inflation
- The C² term (Weyl-squared, containing the spin-2 mode) modifies tensor perturbations, pushing r slightly below pure Starobinsky
- The parameter b in the Bonanno-Platania model represents the residual NGFP correction at inflationary scales; if the C² sector is included (as QG+F requires), b may be constrained to be small

### The missing calculation
Nobody has done AS inflation with the **full fourth-order truncation** (R² + C²) simultaneously. AS calculations typically use f(R) truncations that exclude C². QG+F calculations include C² but don't incorporate non-perturbative RG running. The gap is exactly where the two frameworks need to meet.

### What would distinguish them observationally?
Given that both theories' most developed predictions overlap around r ≈ 0.003:
- If r ≈ 0.003 is measured: **Cannot distinguish** QG+F from AS
- If r > 0.005: Favors Bonanno-Platania AS model (large b) over QG+F
- If r < 0.001: Favors QG+F with large fakeon corrections
- The tensor spectral index n_T and the sound speed ratio c_t/c_s (from the W² term) could provide additional discrimination

---

## 5. Verdict

### **SUPPORTS** — The inflationary predictions are reconcilable

The apparent tension between QG+F and AS inflationary predictions dissolves upon close examination:

1. **The "r up to 0.01" for AS is misleading.** The number comes from one specific model (Bonanno-Platania with maximal b). Most AS inflation papers predict r ≈ 0.003, identical to Starobinsky.

2. **Both theories predict Starobinsky inflation.** QG+F: the R² term IS the inflaton, with C² corrections reducing r slightly. AS: multiple independent groups (Codello 2014, Gubitosi 2018) show the NGFP naturally generates Starobinsky inflation via RG flow.

3. **The predictions overlap.** QG+F: r ∈ [0.0004, 0.0035]. AS (most models): r ≈ 0.003. The intersection is substantial.

4. **The Bonanno-Platania b parameter is not fixed by AS.** It depends on truncation-dependent critical exponents. If b is small (which lower-truncation AS results suggest), the model gives r ≈ 0.003, right in the QG+F window.

5. **The missing piece:** A full AS calculation using the R² + C² truncation (not just f(R)) would likely reproduce the QG+F result more closely, since including the C² term constrains the tensor sector.

### Strength of verdict: MODERATE
The predictions are reconcilable, but the reconciliation is by convergence-of-approximations rather than by explicit calculation. No one has demonstrated the full bridge. The key missing calculation is AS inflation in the fourth-order (R² + C²) truncation.

### Key references
- Anselmi & Piva, JHEP 07 (2020) 211 — QG+F inflation predictions
- Bonanno & Platania, arXiv:1507.03375 — AS modified Starobinsky
- Liu, Prokopec & Starobinsky, PRD 98, 043505 — Corrected analysis of Bonanno-Platania
- Codello, D'Odorico, Pagani, PRD 91, 103530 — AS Starobinsky inflation
- Gubitosi et al., JCAP 1812, 004 — RG flow to Starobinsky
- Bianchi & Gamonal, arXiv:2506.10081 — Precision W² corrections to Starobinsky
- Pawlowski et al., arXiv:2406.10170 — Emergent inflaton potential from AS
