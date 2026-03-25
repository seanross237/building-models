---
topic: quadratic-gravity-fakeon
confidence: provisional
date: 2026-03-25
source: exploration-007-nonperturbative-QGF (strategy-002)
---

# QCD-Gravity Analogy and Ghost Confinement

## The Analogy

The structural analogy between quadratic gravity (QG+F) and QCD was first explicitly articulated by **Holdom and Ren (2015, PRD 93, 124030; arXiv:1512.05305)**. Their central thesis: the Planck mass is the gravitational analogue of Lambda_QCD -- a dynamically generated scale where the coupling becomes strong and non-perturbative physics takes over.

Extended to matter in **Holdom & Ren (PRD 109, 086005, 2024)**: in the UV (trans-Planckian), the spectrum contains gravitons, the massive spin-2 ghost, and the massive scalar. Below M_P, the theory enters a strongly coupled phase where (conjecturally) the ghost is confined and GR emerges as the low-energy effective theory.

### Structural Mapping

| Feature | QCD | Quadratic Gravity (QG+F) |
|---------|-----|--------------------------|
| UV behavior | Asymptotically free (g_s -> 0) | Asymptotically free in f_2 (Weyl^2 coupling) |
| Running coupling | alpha_s(mu) runs logarithmically | f_2(mu) runs logarithmically |
| Dynamical scale | Lambda_QCD ~ 200 MeV | M_P ~ 10^19 GeV (conjectured) |
| Perturbative regime | E >> Lambda_QCD | E >> M_P |
| Non-perturbative regime | E ~ Lambda_QCD (confinement) | E ~ M_P (strong gravity) |
| Unphysical degrees of freedom | Gluons (colored, confined) | Spin-2 ghost (fakeon/confined) |
| Physical spectrum | Hadrons (colorless bound states) | Massless graviton + ? |
| Non-perturbative completion | Lattice QCD | Asymptotic safety (Reuter FP) / CDT |

## Ghost Confinement Conjecture

In QCD, quarks and gluons carry color charge and are confined -- they cannot appear as asymptotic states. Only color-singlet bound states (hadrons) appear in the physical spectrum.

**In quadratic gravity, the "confined" degree of freedom is the massive spin-2 ghost.** The Holdom-Ren conjecture: just as gluons are absent from the QCD physical spectrum due to confinement, the spin-2 ghost is absent from the gravitational physical spectrum due to non-perturbative effects.

**The fakeon prescription as perturbative shadow of confinement:** Anselmi's fakeon prescription removes the ghost from the perturbative spectrum by a specific integration contour choice. But this is a kinematic prescription, not a dynamical mechanism. The Holdom-Ren conjecture suggests the *dynamical* mechanism is confinement -- the ghost is removed by non-perturbative strong-coupling effects, just as gluons are removed in QCD.

## The Inverted Harmonic Oscillator (IHO) Interpretation

A March 2026 paper (arXiv:2603.07150) proposes an alternative to literal confinement: the ghost as an "inverted harmonic oscillator" (IHO). The mode contributes only through virtual dispersive effects rather than propagating asymptotically, preserving unitarity without requiring literal confinement. Claims 50-650× Bayesian evidence improvement over standard theory for CMB parity anomalies. **Verdict: interesting but not yet credible as breakthrough** — the sign flip of C² is ad hoc, unitarity is argued but not proven, and no explicit numerical predictions for n_s/r are provided. See [`iho-ghost-interpretation.md`](iho-ghost-interpretation.md) for the full critical assessment.

## Mass Gap in Non-Perturbative R^2 Gravity

A January 2025 paper (arXiv:2501.16445) demonstrates a mass gap in non-perturbative quadratic R^2 gravity via Dyson-Schwinger equations:
- M^2_G ~ sqrt(R) (mass gap increases with square root of Ricci scalar)
- At low energies, the mass gap suppresses the scalaron's interactions
- Physics transitions toward Einstein-Hilbert gravity
- Signals breaking of scale invariance -- a phase transition from quadratic-gravity to EH dynamics

## Gravitational "Hadrons"

If ghost confinement occurs at the Planck scale, the "hadron" spectrum of gravity would consist of:
1. **Massless graviton** as composite state -- analogue of the pion as a quasi-Goldstone boson
2. **Massive composites at M_P** -- "proton" and heavier hadron analogues, Planck-mass objects
3. **No concrete gravitational chiral symmetry** has been identified -- no clean Goldstone mechanism maps onto gravity

## Where the Analogy Breaks Down

1. **Gauge group structure:** QCD is SU(3) with a compact gauge group. Gravity involves diffeomorphisms -- an infinite-dimensional group. Confinement in gauge theory is tied to compact gauge groups (center symmetry).
2. **Color vs. no color:** Quarks carry color quantum number. The spin-2 ghost doesn't carry an analogous conserved quantum number.
3. **Universal coupling:** Gravity couples universally -- no analogue of "color-neutral" objects that decouple.
4. **No rigorous lattice proof:** CDT and Hamber's Regge calculus provide non-perturbative formulations but do not yet demonstrate "ghost confinement."
5. **Sign of the action:** Euclidean gravitational action is unbounded below (conformal mode problem). QCD's is bounded.
6. **Ghost is UV-specific:** In QCD, confinement is a property of the fundamental theory. In gravity, the ghost only exists in the UV-complete quadratic theory.
7. **Non-perturbative uncertainty in fakeons:** Anselmi acknowledges (arXiv:2510.05276, JHEP 01 (2026) 104) that perturbative expansion misses non-perturbative effects; "nonperturbative effects play crucial roles."

## Overall Assessment

The analogy is **structurally compelling** (asymptotic freedom -> strong coupling -> spectrum without unphysical states -> composites) but the **dynamical details differ fundamentally**. Best viewed as a *heuristic guide*, not a proof. No proof of gravitational ghost confinement exists.

Sources: Holdom & Ren, PRD 93, 124030 (2015); PRD 109, 086005 (2024); arXiv:2603.07150 (IHO, March 2026); arXiv:2501.16445 (mass gap, Jan 2025); arXiv:2510.05276 (Anselmi non-perturbative uncertainty); Quanta Magazine (Nov 2025)
