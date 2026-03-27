---
topic: cross-cutting
confidence: verified
date: 2026-03-26
source: exploration-010-IHO-CMB-predictions (strategy-002), exploration-004-inflation-prediction-reconciliation (strategy-003)
---

# QG+F vs. Asymptotic Safety: CMB Discrimination

## The Key Distinction — Corrected

**QG+F** drives inflation via the R² Starobinsky mechanism. The C² (Weyl-squared) term modifies tensor perturbations, pushing r slightly below pure Starobinsky. The scalar spectral index n_s is determined by R² alone.

**Asymptotic Safety** — contrary to the common characterization as "inflaton-free" — **also produces Starobinsky inflation** in its most developed models:
- Codello et al. (2014) and Gubitosi et al. (2018) show the NGFP naturally generates Starobinsky inflation via RG flow
- Bonanno-Platania (2015/18) gives a logarithmic deformation OF Starobinsky from NGFP effects
- Only the original Bonanno-Reuter (2002) model is truly "inflaton-free," and it is the most primitive truncation with the least sharp predictions

See `asymptotic-safety/cosmology.md` for the full AS inflation taxonomy (6 models across 4 classes).

## Reconciliation Status: SUPPORTS (MODERATE)

**Both theories predict Starobinsky inflation.** The apparent tension between QG+F (r ~ 0.003) and AS ("r up to 0.01") dissolves upon close examination: the "r up to 0.01" comes from one specific model (Bonanno-Platania with maximal b ~ 10⁻²). Most AS inflation papers predict r ≈ 0.003, identical to QG+F. No published paper directly compares the two frameworks' inflationary predictions — this is a literature gap.

### Compatibility Scenario (if QG+F and AS are the same theory)
- The NGFP determines UV initial conditions for the R² coupling
- The R² coupling flows to values consistent with Starobinsky inflation
- The C² term constrains the tensor sector, pushing r slightly below pure Starobinsky
- The Bonanno-Platania b parameter represents residual NGFP correction; including C² may constrain b to be small

### The Missing Calculation
Nobody has done AS inflation with the **full fourth-order truncation** (R² + C²) simultaneously. AS calculations typically use f(R) truncations that exclude C². QG+F calculations include C² but don't incorporate non-perturbative RG running. This is exactly where the two frameworks need to meet.

### Strength of Reconciliation: MODERATE
The predictions are reconcilable by convergence-of-approximations rather than by explicit calculation. The key missing calculation is AS inflation in the fourth-order (R² + C²) truncation.

## The Discrimination Table

| Observable | QG+F (4-deriv) | QG+F (6-deriv) | AS (Reuter FP) | Discriminating? |
|-----------|----------------|----------------|----------------|-----------------|
| **n_s** | 0.964-0.967 | ~0.974 | 0.964-0.97 | WEAK — overlapping ranges |
| **r** | **0.0004-0.004** | ~0.0045 | **~0.003 (most models); up to 0.01 (Bonanno-Platania max b only)** | **YES — SHARPEST** (but overlap substantial) |
| **α_s** | ~-6.5×10⁻⁴ | ~-8×10⁻⁴ | ~-5×10⁻⁴ | NO — below measurement precision |
| **β_s** | ~2.4×10⁻⁵ | ~10⁻⁵ | ~10⁻⁵ | NO — unmeasurable |
| **n_T** | -r/8 | -r/8 | -r/8 (likely) | NO — both satisfy consistency relation |
| **f_NL** | ~10⁻⁴ | ~10⁻⁴ | ~10⁻⁴ | NO — both negligible |
| **Inflaton needed?** | Yes (R² scalaron) | Yes | **Most models: Yes (R² scalaron from NGFP flow). Only Bonanno-Reuter 2002: No** | WEAK — most AS models also use R² scalaron |
| **Running G (cosmic)** | Logarithmic, tiny (~10⁻¹⁴) | Same | **Power-law, potentially observable** | YES — via precision cosmology |
| **BH remnants** | No prediction | No prediction | **Planck-mass remnants** | YES — via PBH dark matter |
| **Higgs mass** | No prediction | No prediction | **~126 GeV (Shaposhnikov-Wetterich)** | YES — but already observed |
| **d_s (UV)** | d_s = 2 | d_s = 4/3 | d_s ~ 2 | WEAK — not directly observable |
| **Consistency violation** | r + 8n_T ~ 10⁻⁴ | Similar | Unknown | NO — too small to measure |

## The r Discriminator — Detailed Analysis

The tensor-to-scalar ratio is the cleanest discriminator:

**QG+F prediction:**
- r ∈ [0.0004, 0.004] (4-derivative)
- r ≈ 0.0045 (6-derivative)
- Upper bound: r < 0.005 in all variants

**AS prediction (Bonanno-Platania 2018, PRD 98, 043505):**
- For b → 0 (pure Starobinsky): r → 0.003-0.004
- For b ~ 10⁻³ (maximal AS corrections): r ≈ 0.01
- r ∈ [0.003, 0.01] depending on AS correction parameter b

**Discrimination windows:**
- r > 0.005: **Favors AS** over QG+F
- 0.003 < r < 0.005: **Ambiguous** — both allowed
- r < 0.003: **Favors QG+F** over simplest AS models
- r < 0.0004: Only QG+F with heavy fakeon consistent

**Required precision:** σ(r) < 0.002, ideally σ(r) ~ 0.001

## Other Potential Discriminators

### Speed of Sound During Inflation
QG+F predicts modified tensor perturbation speed: c_t/c_s ≃ 1 + β/(6α). Unique C² signature, but correction is tiny (proportional to slow-roll parameters). Likely unmeasurable.

### Blue-Tilted Tensor Spectrum
A December 2024 paper (JHEP 12, 024) proposes that UV-complete theories with Weyl invariance predict blue-tilted tensors (n_T > 0) with r₀.₀₅ ≈ 0.01. Dramatically different from both QG+F and AS (both predict n_T < 0). Different framework.

### Stochastic GW Background
Future space-based detectors (DECIGO) could measure n_T with enough precision to distinguish models. Decades away.

## AS Inflation: Full Landscape (Corrected)

The AS inflation literature contains **four classes** of models. See `asymptotic-safety/cosmology.md` for full taxonomy.

**Key correction:** The "r up to 0.01" for AS is misleading. It comes specifically from Bonanno-Platania's logarithmic correction model with maximal b ~ 10⁻² — one model out of six. The majority of developed AS models (Codello 2014, Gubitosi 2018, Pawlowski 2024) predict r ≈ 0.003–0.005, squarely within the QG+F window.

### Bonanno-Platania (the model that gives r ~ 0.01)

    L_eff = M_P² R/2 + (a/2) R²/[1 + b ln(R/μ²)]

where b parameterizes AS correction strength. For b → 0: reduces to Starobinsky. For b ~ 10⁻²: n_s increases toward ~0.975, r increases to ~0.01. But b is NOT uniquely determined by AS — it depends on truncation-dependent critical exponents.

### Other AS models (all predict r ≈ 0.003)
- Codello et al. (2014): NGFP sets R² initial conditions → pure Starobinsky
- Gubitosi et al. (2018): f(R) RG flow → Starobinsky explicitly
- Pawlowski et al. (2024): Emergent inflaton potential from scalar-tensor RG → r ≈ 0.005
- Bonanno et al. (2024/2025): Running G cosmology, sharp r not yet published

## Experimental Timeline for Discrimination

See `cmb-experimental-timeline.md` for full details. Summary:
- **2027-2028:** BICEP Array σ(r) ~ 0.003 — can detect r > 0.01 (strong AS)
- **2030-2032:** SO enhanced σ(r) ~ 0.001-0.002 — earliest definitive discrimination
- **2036-2037:** LiteBIRD σ(r) < 0.001 — most reliable discrimination

Sources: Bonanno & Platania (2018, PRD 98, 043505); Bonanno et al. (2025, PRD 111, 103519; arXiv:2405.02636); Anselmi (2020, JHEP 07, 211; 2021, JCAP 01, 048); Codello, D'Odorico, Pagani (2014, PRD 91, 103530); Gubitosi et al. (2018, JCAP 1812, 004); Pawlowski et al. (2024, arXiv:2406.10170); Bianchi & Gamonal (2025, arXiv:2506.10081); JHEP 12 (2024) 024; exploration-004-inflation-prediction-reconciliation
