# Exploration 004 Summary: The n_s Tension — Working Backward from Data to Theory

## Goal
Assess the CMB spectral index tension (ACT DR6: n_s = 0.974 ± 0.003 vs. QG+F prediction n_s ≈ 0.967) and identify what modifications to QG+F could resolve it.

## What Was Tried
Comprehensive literature review including: (1) all major CMB experiments (ACT DR6, Planck PR4, SPT-3G D1) and BAO data (DESI DR1/DR2), (2) the March 2026 Ferreira et al. analysis arguing the n_s shift is a statistical artifact, (3) theoretical modifications to Starobinsky/QG+F inflation (R³ corrections, marginal deformations, radiative corrections, Weyl-squared contributions), (4) physical beta functions of quadratic gravity (Branchina et al. PRL 2024), (5) alternative inflationary models matching n_s ≈ 0.974.

## Outcome: SUCCEEDED — Nuanced picture with critical new finding

### Key Finding 1: The tension is real in the data but probably NOT physical
- CMB alone: n_s = 0.969 ± 0.003 → barely 1σ above Starobinsky
- CMB + DESI: n_s = 0.974 ± 0.003 → 2.3σ tension
- **Ferreira et al. (Phys. Rev. D, March 2026) argue the shift is a statistical artifact of BAO-CMB dataset tension**, not a signal of new primordial physics. They urge caution until the BAO-CMB tension is resolved.
- SPT-3G D1 gives n_s = 0.951 ± 0.011, pulling AGAINST the ACT-driven shift

### Key Finding 2: The fakeon doesn't help — confirmed definitively
- Self-consistent Weyl-squared analysis (arXiv: 2506.10081) proves the C² (fakeon) term modifies r but NOT n_s at leading order
- To shift n_s requires modifying the R² sector, not the C² sector

### Key Finding 3: Three viable gravitational-sector modifications exist
1. **R³ curvature correction** (δ₃ ≈ −10⁻⁴): Natural in six-derivative gravity; resolves tension exactly (arXiv: 2505.10305)
2. **RG running of R² coupling** (γ ≈ 0.007): Motivated by asymptotic safety and perturbative QG running (arXiv: 2509.23329)
3. **Logarithmic enhancement** (β ~ 0.1): Padé-regularized R²ln(R) modification giving n_s ≈ 0.970-0.975 (arXiv: 2603.14743, March 2026)

### Key Finding 4: The critical calculation remains UNDONE
Physical beta functions for quadratic gravity are now established (Branchina et al. PRL 2024). Percacci & Vacca (2025) embedded Starobinsky in the tachyon-free trajectory. But NOBODY has computed the resulting n_s shift. This well-defined, parameter-free calculation would either confirm QG+F predicts the right n_s or show that additional terms (R³) are needed.

### Key Finding 5: The tension will likely dissolve or be resolved by ~2028-2030
CMB-S4 (σ(n_s) ~ 0.002) + Simons Observatory + DESI DR3 will definitively determine whether the tension is real. The probability that the tension dissolves (due to BAO-CMB tension resolution) is estimated at 40-50%.

## Key Takeaway
**The n_s tension is the sharpest observational test for QG+F, but it is premature to modify the theory.** The March 2026 Ferreira et al. analysis strongly suggests the shift is a dataset artifact, not new physics. If the tension IS real, the most natural resolution is the RG running of QG+F's own R² coupling — a genuine loop-level prediction with no free parameters. The single most valuable next step is computing this n_s shift from the known physical beta functions.

## Leads Worth Pursuing
1. **Calculate n_s from QG+F physical beta functions** — highest-priority calculation, no free parameters, would be definitive
2. **Assess whether "physical" beta functions apply to in-in correlators** — flagged as an open question by Percacci & Vacca (2025)
3. **Six-derivative QG+F inflation** — does the R³ coefficient constrained by renormalizability naturally give δ₃ ≈ −10⁻⁴?
4. **Monitor DESI DR2/DR3 and SPT-3G updates** — watch whether the n_s shift persists or diminishes
5. **Early Dark Energy connection** — if EDE resolves H₀ tension, n_s shifts dramatically, changing the entire picture
