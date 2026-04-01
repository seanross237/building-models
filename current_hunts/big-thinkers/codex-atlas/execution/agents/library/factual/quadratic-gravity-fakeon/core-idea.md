---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-24
source: exploration-002-spectral-dimension-constructive-axiom
---

# Quadratic Gravity with Fakeon Quantization

## The Action

The most general parity-preserving, torsion-free, diffeomorphism-invariant action quadratic in curvature (using the Gauss-Bonnet identity to eliminate one redundant term):

    S = integral d^4x sqrt(-g) [ (M_P^2/2)(R - 2 Lambda) - (1/(2 f_2^2)) C_{munurhosigma} C^{munurhosigma} + (1/(6 f_0^2)) R^2 ]

where M_P is the reduced Planck mass, Lambda is the cosmological constant, f_2 and f_0 are dimensionless couplings for the Weyl-squared and R-squared terms respectively. The dimensionlessness of f_2 and f_0 in 4D is precisely why the theory is renormalizable.

## Propagator Structure

Expanding around flat spacetime (g_muv = eta_muv + h_muv), the propagator decomposes into:

**Spin-2 sector:**

    G_2(p^2) = 1/p^2 - 1/(p^2 - M_2^2)

where M_2^2 = f_2^2 M_P^2 / 2. The second pole is the ghost (negative residue -1).

**Spin-0 sector:**

    G_0(p^2) = 1/p^2 - 1/(p^2 - M_0^2)

where M_0^2 = f_0^2 M_P^2 / 6. This mode has positive residue and can be quantized normally.

Both sectors go as ~1/p^4 for p >> M_2, M_0, giving d_s = 2 as required.

## The Fakeon Prescription (Anselmi-Piva 2018)

The massive spin-2 ghost is quantized as a **fakeon** -- a virtual particle that appears in loops but cannot appear as an asymptotic state:

    1/(p^2 - m_chi^2 + i epsilon) -> (p^2 - m_chi^2) / ((p^2 - m_chi^2 + i epsilon)^2 + E^4)

then E -> 0 after epsilon -> 0. This is not a minor technical modification -- it changes the physical content of the theory by removing the massive spin-2 particle from the physical spectrum entirely.

**Quantization choices:**
- h_muv (massless graviton): standard Feynman prescription
- chi_muv (massive spin-2, mass M_2): **fakeon prescription**
- phi (massive spin-0, mass M_0): standard Feynman or fakeon prescription

## Uniqueness from Constraint Stack

The constraint stack {d_s = 4 -> 2, Lorentz invariance, diffeomorphism invariance, renormalizability, unitarity} uniquely selects this theory through a chain of elimination:

1. **d_s = 2** -> propagator must go as 1/p^4 in UV -> exactly four-derivative terms in the action
2. **Diffeomorphism invariance** -> four-derivative terms must be quadratic curvature: R^2, R_muv R^muv, R_munurhosigma R^munurhosigma
3. **Gauss-Bonnet identity in d=4** -> eliminates one combination, leaving 2 independent terms: R^2 and C^2 (Weyl squared)
4. **Renormalizability** -> automatically satisfied since quadratic curvature couplings are dimensionless in 4D. Higher curvature terms (R^3 etc.) have negative mass dimension and are non-renormalizable.
5. **No higher-than-quadratic terms** -> R^3 ~ partial^6 g would give 1/p^6 propagator and d_s = 4/3, overshooting the target
6. **Fakeon** -> resolves the ghost forced by d_s = 2 (see no-go theorem in constraints/structural/)

## Parameters

Only **4 total parameters** (2 new beyond GR):

| Parameter | Physical meaning | Status |
|-----------|-----------------|--------|
| M_P | Planck mass | Known |
| Lambda | Cosmological constant | Known |
| f_2 (or M_2) | Weyl^2 coupling / spin-2 fakeon mass | **Free** |
| f_0 (or M_0) | R^2 coupling / scalar mass | **Free** |

## Established Properties

1. **Renormalizable** -- proven by Stelle (1977). Finite number of counterterms.
2. **Unitary** -- proven by Anselmi and Piva (2018) via fakeon prescription. Optical theorem satisfied at all loop orders.
3. **d_s = 2 in UV** -- propagator falls as 1/p^4 at high momenta.
4. **Recovers GR in IR** -- at E << M_2, quadratic terms are negligible.
5. **Asymptotically free in f_2** -- the Weyl-squared coupling runs to zero in the UV.
6. **Incorporates both Carlip mechanisms** -- the bare 1/p^4 propagator gives d_s = 2 from the action structure (scale invariance); asymptotic freedom in f_2 provides a UV fixed point; and the strong-coupling Wheeler-DeWitt regime produces asymptotic silence.

## Costs and Open Questions

1. **Microcausality violation** at the scale tau ~ 1/M_2 (possibly ~10^{-43} s if M_2 ~ M_P). Survives the classical limit. See `microcausality-and-novel-signatures.md`.
2. **No classical limit for the fakeon** -- the massive spin-2 mode does not correspond to any classical field. Classical equations use averaged (retarded + advanced) Green's functions.
3. **f_0^2 not asymptotically free** in pure gravity -- may become so with appropriate matter content (possibly the Standard Model).
4. **Black hole entropy** -- The Wald entropy formula gives S = A/(4G) + O(l_P²/r_H²) corrections for Schwarzschild BHs in quadratic gravity. For astrophysical BHs, corrections are negligible (10⁻⁷⁶ for solar mass, 10⁻⁹⁰ for SMBH). The fakeon prescription selects Schwarzschild at the classical level — non-Schwarzschild branches are excluded. For Planck-scale BHs, corrections are O(1) and the perturbative expansion breaks down. See `black-hole-predictions.md` for the full BH catalog.
5. **Relationship to asymptotic safety** -- the two may describe the same physics from different perspectives (bare vs. dressed propagator achieving 1/p^4). Quadratic gravity is asymptotically free in f_0 and f_2 (Fradkin & Tseytlin 1982); AS posits a non-trivial UV fixed point with non-zero G_N. Salvio's work hints at connections but this remains unresolved.
6. **Predicting M_2 and M_0** -- from BH entropy, spectral dimension matching, inflation, or cosmological constant constraints. Any combination that fixes one or both of the 2 free parameters would be a major result.
7. **Spectral dimension** -- remarkably, Anselmi's group has never computed the spectral dimension of their theory. Computing d_s for quadratic gravity + fakeon and confirming d_s = 4 -> 2 would close the loop on the constructive axiom derivation.
8. **Non-perturbative completion** -- the theory is perturbatively renormalizable and asymptotically free, but the non-perturbative completion (analogous to confinement in QCD) is unknown. The QCD analogy (Holdom-Ren 2015, 2024) is structurally tight but unproven dynamically; a mass gap in R^2 gravity has been demonstrated via Dyson-Schwinger equations (arXiv:2501.16445, Jan 2025); the IHO interpretation (arXiv:2603.07150, March 2026) offers an alternative to literal ghost confinement. See `qcd-analogy-ghost-confinement.md` for full details.
9. **Unimodular extension** -- Salvio (2024, arXiv:2406.12958) showed that unimodular quadratic gravity addresses the old cosmological constant problem by making Lambda an integration constant. The fakeon prescription has not been combined with the unimodular constraint.
10. **Phenomenological predictions** at accessible energies remain to be worked out. See `inflationary-predictions.md` and `microcausality-and-novel-signatures.md`.

## Distinction from "Stelle Gravity"

While the action is identical to Stelle's 1977 theory, the physics differs fundamentally:
- **Stelle gravity** has a ghost -> violates unitarity above the ghost mass
- **Fakeon gravity** has no ghost -> unitary at all energies

The fakeon prescription makes different predictions for scattering cross sections above M_2.

Sources: Stelle, Phys. Rev. D 16, 953 (1977); Anselmi & Piva, JHEP 11, 021 (2018), arXiv:1806.03605; Salvio, Front. Phys. 6:77 (2018), arXiv:1804.09944; Donoghue & Menezes, arXiv:2112.01974
