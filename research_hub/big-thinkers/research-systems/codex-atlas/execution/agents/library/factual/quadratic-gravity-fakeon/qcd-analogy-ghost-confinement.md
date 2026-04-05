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

### Two Proposed Scenarios

Two concrete scenarios for the ghost propagator ~G(k²)/k⁴ (Holdom-Ren 2016, arXiv:1605.05006):
- **Case A (softening):** Propagator softens to 1/k² with positive residue, no mass gap. Ghost pole transforms into a zero → massless physical graviton emerges.
- **Case B (confinement):** Mass gap develops, all perturbative propagating modes removed from spectrum. Ghost pole vanishes entirely.

### Evidence and Limitations

Evidence provided: Gribov copies exist in gravity (shown for spherically symmetric metrics); measure factor 1/(1+N_F(h)) suppresses IR physics. However, the authors themselves acknowledge:
1. "Presently we lack more direct arguments as to why the analogy should hold"
2. No lattice formulation of asymptotically free gravity exists
3. Non-locality concerns near M_Pl
4. M parameter instability from matter sector corrections
5. Black hole formation may block super-Planckian probes

Assessment: structurally motivated but has zero non-perturbative evidence specific to gravity. See `asymptotic-safety/ghost-fate-strong-coupling.md` for the comprehensive survey of ghost fate mechanisms in the AS literature.

## The Inverted Harmonic Oscillator (IHO) Interpretation

A March 2026 paper (arXiv:2603.07150) proposes an alternative to literal confinement: the ghost as an "inverted harmonic oscillator" (IHO). The mode contributes only through virtual dispersive effects rather than propagating asymptotically, preserving unitarity without requiring literal confinement. Claims 50-650× Bayesian evidence improvement over standard theory for CMB parity anomalies. **Verdict: interesting but not yet credible as breakthrough** — the sign flip of C² is ad hoc, unitarity is argued but not proven, and no explicit numerical predictions for n_s/r are provided. See [`iho-ghost-interpretation.md`](iho-ghost-interpretation.md) for the full critical assessment.

## Mass Gap in Non-Perturbative R^2 Gravity

A January 2025 paper (arXiv:2501.16445, Frasca) demonstrates a mass gap in non-perturbative quadratic R^2 gravity via Dyson-Schwinger equations:
- M^2_G ~ sqrt(R) (mass gap increases with square root of Ricci scalar)
- At low energies, the mass gap suppresses the scalaron's interactions
- Physics transitions toward Einstein-Hilbert gravity
- Signals breaking of scale invariance -- a phase transition from quadratic-gravity to EH dynamics

**Scope limitation:** Studies ONLY the scalar sector (scalaron from R² term). Does NOT address the spin-2 ghost and does NOT include C². Irrelevant to the spin-2 ghost question specifically.

## Gravitational "Hadrons"

If ghost confinement occurs at the Planck scale, the "hadron" spectrum of gravity would consist of:
1. **Massless graviton** as composite state -- analogue of the pion as a quasi-Goldstone boson
2. **Massive composites at M_P** -- "proton" and heavier hadron analogues, Planck-mass objects
3. **No concrete gravitational chiral symmetry** has been identified -- no clean Goldstone mechanism maps onto gravity

## Where the Analogy Breaks Down

Severity ratings from adversarial assessment (exploration-008-devils-advocate):

1. **Gauge group structure (HIGH).** QCD is SU(3) with a compact gauge group. Gravity involves diffeomorphisms -- an infinite-dimensional group. Confinement in gauge theory is tied to compact gauge groups (center symmetry Z(3)). The Wilson loop area law, center vortices, monopoles, and dual superconductor picture all depend on compactness. None have gravitational analogs. **Removes the primary theoretical mechanism for confinement.**
2. **Color vs. no color (HIGH).** Quarks carry color quantum number; only color-singlet combinations appear as physical states. The spin-2 ghost doesn't carry an analogous conserved quantum number. No selection rule separates "ghost-like" from "graviton-like" at the non-perturbative level. "Confining the ghost" has no rigorous meaning without a quantum number to enforce it.
3. **Universal coupling (MODERATE).** Gravity couples universally -- no analogue of "color-neutral" objects that decouple. The perturbative/non-perturbative transition affects everything, making clean QCD-style phase picture harder to sustain.
4. **No rigorous lattice proof (HIGH).** After 10+ years of the analogy being proposed (Holdom-Ren 2015), zero non-perturbative evidence specific to the gravitational spin-2 ghost. CDT exists but doesn't include C² and doesn't address ghost confinement. Conformal mode problem (point 5) makes naive lattice approaches ill-defined.
5. **Sign of the action (MODERATE).** Euclidean gravitational action is unbounded below (conformal mode problem). QCD's is bounded. Techniques that work in QCD (importance sampling, Monte Carlo) face qualitatively new obstacles.
6. **Ghost is UV-specific (LOW).** In QCD, confinement persists to zero energy. In gravity, the ghost only exists in the UV-complete quadratic theory; confinement must operate only at E ~ M_P. (This is arguably a feature of the framework, not a bug.)
7. **Non-perturbative uncertainty (MODERATE).** Anselmi acknowledges (arXiv:2510.05276, JHEP 01 (2026) 104) that perturbative expansion misses non-perturbative effects; "nonperturbative effects play crucial roles." In QCD, the non-perturbative sector is precisely defined (lattice gives numerical answers). In QG+F, it is acknowledged to be uncertain.

### Cumulative Assessment

The three highest-severity breakdowns (1, 2, 4) all concern the **confinement mechanism itself**: no compact gauge group, no quantum number to confine, no lattice evidence. These are the entire point of the analogy, not details. Without confinement being established, the QCD parallel is decorative, not structural. The analogy is load-bearing (the unified framework would collapse without it) and broken at its load-bearing joints — though confinement *could* occur through a non-QCD mechanism that the framework does not currently provide.

## Overall Assessment

The analogy is **structurally compelling** (asymptotic freedom -> strong coupling -> spectrum without unphysical states -> composites) but the **dynamical details differ fundamentally**. Best viewed as a *heuristic guide*, not a proof. No proof of gravitational ghost confinement exists. See `../cross-cutting/unified-qgf-as-framework/adversarial-assessment.md` for full adversarial analysis.

Sources: Holdom & Ren, PRD 93, 124030 (2015); PRD 109, 086005 (2024); IJMPD 25, 1643004 (2016) [arXiv:1605.05006]; arXiv:2603.07150 (IHO, March 2026); arXiv:2501.16445 (mass gap, Jan 2025); arXiv:2510.05276 (Anselmi non-perturbative uncertainty); Quanta Magazine (Nov 2025)

Cross-references: `asymptotic-safety/ghost-fate-strong-coupling.md` (comprehensive ghost fate survey in AS)
