---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-24
source: exploration-003-quadratic-gravity-fakeon-validation
---

# IR Recovery: Newton's Law, Propagator, and Validation Against GR

## Propagator Decomposition

The quadratic gravity propagator around flat spacetime decomposes into three sectors:

    G(p²) = G_massless(p²) + G_spin2(p²) + G_scalar(p²)

| Sector | Expression | Pole | Nature |
|--------|-----------|------|--------|
| Massless graviton | P²/p² | p² = 0 | Standard GR graviton |
| Massive spin-2 | -P²/(p² - M₂²) | p² = M₂² | Fakeon (purely virtual) |
| Massive scalar | P⁰/(p² - M₀²) | p² = M₀² | Physical or fakeon |

At low momenta (p² ≪ M₂², M₀²), the massive propagators contribute only constant (contact) corrections: G(p²) → P²/p² + O(1/M²). The theory recovers GR in the IR by construction.

## Stelle Potential (Newton's Law with Corrections)

The static Newtonian potential between two masses (Stelle 1978, Gen. Rel. Grav. 9, 353-371):

    V(r) = -GM/r × [1 + (1/3) e^{-M₀ r} - (4/3) e^{-M₂ r}]

where M₀ = f₀ M_P/√6 (scalar mass from R² term) and M₂ = f₂ M_P/√2 (fakeon mass from C² term).

**Physical interpretation of each term:**
- +1: standard Newtonian gravity
- +(1/3) e^{-M₀ r}: attractive scalar exchange correction
- -(4/3) e^{-M₂ r}: repulsive spin-2 fakeon exchange correction

**Key regimes:**
- r ≫ 1/M₀, 1/M₂: V(r) → -GM/r (standard Newton)
- r ~ 1/M₂: repulsive correction weakens gravity by up to factor 4/3
- r ~ 1/M₀: attractive correction strengthens gravity by factor 1/3
- r → 0: V(r) → -GM/r × [1 + 1/3 - 4/3] = 0 — **gravity vanishes at the origin**

The r → 0 regularization implies singularity resolution inside black holes — a prediction shared with many QG approaches but here derived from a specific mechanism.

**Note on fakeon prescription:** The Stelle potential above was derived with the ghost as a normal particle. With the fakeon prescription, the static potential is modified — the fakeon contributes an oscillating/damped correction rather than a pure exponential. The leading Yukawa form persists in the non-relativistic limit. The detailed classicized potential is given in Anselmi 18A4. Newton's law is recovered at large distances regardless.

## Experimental Constraints on Yukawa Corrections

For M₂, M₀ ~ M_P (~10¹⁹ GeV), the Compton wavelengths are ~10⁻³⁵ m — far below experimental resolution:
- **Eöt-Wash** constrains Yukawa corrections down to ~50 μm (masses ~10⁻³ eV), which is **22 orders of magnitude** below the Planck scale
- Even in the Salvio-Strumia "agravity" scenario (M₂ ~ 10¹¹ GeV), corrections at r ~ 10⁻²⁷ m are still far below current reach (~10⁻⁵ m)

## Validation Summary Against GR Constraints

| Test | Result | Detail |
|------|--------|--------|
| Graviton propagator IR limit | ✅ Pass | Massless graviton pole dominates; massive modes decouple exponentially |
| Newton's law V(r) = -GM/r | ✅ Pass | + exponentially suppressed Yukawa corrections (above) |
| PPN γ = 1, β = 1 | ✅ Pass | Corrections ~ e^{-M₂ r_solar} ≈ e^{-10^{38}} for Planck-scale masses |
| GW speed c_gw = c | ✅ Pass | Exact, by Lorentz invariance (no preferred frame effects) |
| Graviton mass m_g = 0 | ✅ Pass | Massless by construction; fakeon never appears as asymptotic state |
| Lorentz invariance | ✅ Pass | Exact by construction; advantage over Hořava-Lifshitz, CDT, some LQG variants |
| Bekenstein-Hawking entropy | ✅ Pass | Wald entropy gives S = A/(4G) + O(l_P²/r_H²); negligible for astrophysical BHs; see `black-hole-predictions.md` |

**Overall: 7/7 passed** (BH entropy resolved — Wald formula gives correct leading term with tiny corrections)

Sources: Stelle (1978), Gen. Rel. Grav. 9, 353-371; Anselmi & Piva (2018), JHEP 11, 021; LIGO GW170817; Cassini mission (2003)
