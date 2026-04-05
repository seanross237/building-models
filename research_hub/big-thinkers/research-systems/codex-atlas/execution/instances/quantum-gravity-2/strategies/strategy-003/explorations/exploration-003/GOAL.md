# Exploration 003: Ghost Fate at Strong Coupling — Does AS Produce Ghost Confinement?

## Mission Context

We are testing the conjecture that QG+F (quadratic gravity with fakeon) and Asymptotic Safety (AS) are the same UV-complete theory. Previous exploration (002) found the fixed-point connection INCONCLUSIVE. Now we test the second key implication.

## Your Specific Goal

**ONE QUESTION:** What does the non-perturbative / AS literature say about the fate of the massive spin-2 ghost at strong coupling? Does ghost confinement, ghost mass running to infinity, or ghost spectral weight suppression naturally emerge from AS?

This is the bridge question: The fakeon is QG+F's defining innovation — it removes the ghost from the physical spectrum via a specific propagator prescription. If QG+F = AS, the non-perturbative sector must produce an equivalent effect dynamically. The question is: does it?

Specifically investigate:

1. **Ghost propagator in non-perturbative AS:** Has anyone computed the ghost (massive spin-2) propagator using functional RG or lattice methods? Does the spectral function show confinement signatures (violation of positivity, absence of asymptotic states)?

2. **Graviton spectral function reconstruction:** Bonanno et al. (2022) reconstructed the momentum-dependent graviton propagator from AS. Does this reconstruction show anything about the ghost pole? Does the spectral function have negative-norm contributions that get suppressed non-perturbatively?

3. **Running of the ghost mass:** In AS, all couplings run. Does M_2 (the ghost mass) run to infinity at the NGFP, effectively decoupling the ghost? Or does it run to some finite value? Has anyone computed the running of the Weyl-squared coupling f_2 at the NGFP?

4. **CDT evidence:** Causal Dynamical Triangulations is the lattice version of AS. Has CDT seen any evidence of ghost-like modes being present or absent in the non-perturbative spectrum?

5. **Phase transition / mass gap:** A Jan 2025 paper (arXiv:2501.16445) shows a mass gap in non-perturbative R^2 gravity via Dyson-Schwinger equations. Does this mass gap affect the ghost?

**Give a verdict:** SUPPORTS / FALSIFIES / INCONCLUSIVE for the conjecture.

## Pre-loaded Context

**Holdom-Ren ghost confinement conjecture:** The ghost is confined at strong coupling, analogous to gluon confinement in QCD. The fakeon prescription is the perturbative shadow of this dynamical mechanism. However, the analogy has 7 known breakdown points: no compact gauge group, no color charge, universal coupling, no lattice proof, conformal mode problem, ghost is UV-specific, non-perturbative uncertainty.

**QCD structural mapping:**
| QCD | QG+F |
|-----|------|
| Gluons (colored, confined) | Spin-2 ghost (fakeon/confined) |
| Lambda_QCD ~ 200 MeV | M_P ~ 10^19 GeV (conjectured) |
| Lattice QCD confirms confinement | CDT / AS: no confirmation yet |

**Bonanno et al. (2022):** Reconstructed momentum-dependent graviton propagator from AS. Library entry at asymptotic-safety/graviton-propagator.md.

**Key authors to search:** Bonanno, Reuter, Saueressig, Platania, Knorr, Percacci, Holdom, Ren, Becker, Pagani, Dona, Eichhorn, Ohta, Buoninfante, Hamber (lattice gravity), Ambjorn, Loll, Jurkiewicz (CDT).

**What the library already knows:** The ghost confinement conjecture is "structurally compelling but dynamical details differ fundamentally. Best viewed as a heuristic guide, not a proof." The mass gap result (arXiv:2501.16445) shows M^2_G ~ sqrt(R) for the scalaron. The IHO interpretation (March 2026) is an alternative but "not yet credible."

## Success Criteria
- Survey of what the non-perturbative literature says about the ghost's fate
- Identify whether ANY mechanism (confinement, mass running, spectral suppression) naturally emerges
- Clear verdict with specific evidence
- 150-300 lines

## Failure Criteria
- If the non-perturbative literature simply doesn't address the ghost at all, say so clearly — that IS the finding

## Output
- `explorations/exploration-003/REPORT.md` (150-300 lines, write incrementally)
- `explorations/exploration-003/REPORT-SUMMARY.md` (write LAST)
