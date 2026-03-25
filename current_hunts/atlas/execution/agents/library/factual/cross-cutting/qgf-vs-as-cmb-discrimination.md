---
topic: cross-cutting
confidence: verified
date: 2026-03-25
source: exploration-010-IHO-CMB-predictions (strategy-002)
---

# QG+F vs. Asymptotic Safety: CMB Discrimination

## The Key Distinction

**QG+F** drives inflation via the R² Starobinsky mechanism. The C² term provides perturbatively small quantum gravity corrections (suppressed by α = 1/(4πN) ~ 1/115).

**Asymptotic Safety** drives inflation via the Reuter non-Gaussian fixed point — a non-perturbative mechanism where the running cosmological constant provides the effective inflaton. No explicit inflaton field needed.

## The Discrimination Table

| Observable | QG+F (4-deriv) | QG+F (6-deriv) | AS (Reuter FP) | Discriminating? |
|-----------|----------------|----------------|----------------|-----------------|
| **n_s** | 0.964-0.967 | ~0.974 | 0.964-0.97 | WEAK — overlapping ranges |
| **r** | **0.0004-0.004** | ~0.0045 | **up to 0.01** | **YES — SHARPEST** |
| **α_s** | ~-6.5×10⁻⁴ | ~-8×10⁻⁴ | ~-5×10⁻⁴ | NO — below measurement precision |
| **β_s** | ~2.4×10⁻⁵ | ~10⁻⁵ | ~10⁻⁵ | NO — unmeasurable |
| **n_T** | -r/8 | -r/8 | -r/8 (likely) | NO — both satisfy consistency relation |
| **f_NL** | ~10⁻⁴ | ~10⁻⁴ | ~10⁻⁴ | NO — both negligible |
| **Inflaton needed?** | Yes (R² scalaron) | Yes | **No** | YES — conceptual, not directly observable |
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

## AS Inflation: The Bonanno-Platania Framework

The AS effective Lagrangian:

    L_eff = M_P² R/2 + (a/2) R²/[1 + b ln(R/μ²)]

where b parameterizes AS correction strength. For b → 0: reduces to Starobinsky. For b ~ 10⁻³: n_s increases toward ~0.97, r increases to ~0.01.

Also: Emergent cosmology model (Bonanno et al. PRD 111, 103519, 2025):

    G(ε) = G_N / (1 + ε/ε_c)

with ε_c determined by g* = 540π/833. Produces quasi-de Sitter without inflaton. Explicit n_s, r predictions not yet published.

## Experimental Timeline for Discrimination

See `cmb-experimental-timeline.md` for full details. Summary:
- **2027-2028:** BICEP Array σ(r) ~ 0.003 — can detect r > 0.01 (strong AS)
- **2030-2032:** SO enhanced σ(r) ~ 0.001-0.002 — earliest definitive discrimination
- **2036-2037:** LiteBIRD σ(r) < 0.001 — most reliable discrimination

Sources: Bonanno & Platania (2018, PRD 98, 043505); Bonanno et al. (2025, PRD 111, 103519; arXiv:2405.02636); Anselmi (2020, JHEP 07, 211; 2021, JCAP 01, 048); JHEP 12 (2024) 024
