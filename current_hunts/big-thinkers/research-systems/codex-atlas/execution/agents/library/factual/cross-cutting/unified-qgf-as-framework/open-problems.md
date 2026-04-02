---
topic: unified-qgf-as-framework
confidence: provisional
date: 2026-03-26
source: exploration-007-unified-framework (quantum-gravity-2 strategy-003)
---

# Open Problems in the Unified QG+F--AS Framework

Prioritized catalog of unresolved issues, with specific calculations that would resolve each.

## #1: The AF -> NGFP Trajectory (UNRESOLVED -- Most Important)

The unified framework requires an RG trajectory that:
1. Starts at the AF (Gaussian) fixed point in the UV
2. Passes through (or near) the NGFP at the Planck scale
3. Flows to the Einstein-Hilbert fixed point in the IR

Under SWY (2022), the AF and NGFP are clearly distinct with different critical exponents. A connecting trajectory **may** exist but has not been computed. SWY (2023) showed AF can flow to GR in the IR via scaling solutions, but the NGFP's role was not established.

Under Codello-Percacci (2006), the two fixed points are the same, and no connecting trajectory is needed.

**Resolving calculation:** Full FRG computation in the (R + R^2 + C^2 + E) truncation that:
- Identifies both fixed points (AF and NGFP)
- Maps the phase space of RG trajectories
- Determines whether a trajectory AF -> NGFP -> GR exists
- Computes critical exponents at both fixed points

Technically demanding but well-defined. Beta functions for all 4 couplings are partially available (Falls et al. 2023; SWY 2022, 2023).

See `../../asymptotic-safety/af-ngfp-fixed-point-connection.md` for full literature analysis.

## #2: Spin-2 Ghost Confinement (UNRESOLVED -- Second Most Important)

No existing calculation has demonstrated ghost confinement for the gravitational spin-2 ghost specifically:

- Becker et al. (2017): Ghost mass diverges at NGFP. **Scalar ghosts only.**
- Draper et al. (2020): Complex pole tower. **General truncation, not Stelle ghost specifically.**
- Holdom & Ren (2015, 2016, 2024): QCD analogy. **Heuristic, not derived.**
- Frasca (2025): Mass gap via Dyson-Schwinger. **Scalar sector only, no C^2.**

### Where the QCD Analogy Breaks Down

1. QCD has a compact gauge group (SU(3)); gravity has diffeomorphisms (non-compact)
2. Quarks carry color charge; the ghost has no analogous confined quantum number
3. Euclidean gravitational action is unbounded below, complicating lattice approaches
4. No non-perturbative uncertainty in QCD (unlike the fakeon's inherent uncertainty)

**Resolving calculation:** Reconstruct the full graviton propagator (transverse-traceless spin-2 sector) within the (R + R^2 + C^2) FRG truncation and determine:
- Whether the ghost pole persists, migrates, or dissolves
- Whether the spectral function is positive (unitarity)
- Whether the result matches the Draper et al. complex pole tower structure

This is **the key open calculation** of the unified framework — and the single most genuinely discriminating test. Only the unified theory predicts ghost dissolution; the "compatible-but-separate" interpretation has no mechanism for AS dynamics to affect the ghost's pole structure. Estimated difficulty: PhD-thesis-level, 1–2 years for an expert group. No fundamental obstruction.

See `../../asymptotic-safety/ghost-fate-strong-coupling.md` for the comprehensive ghost fate survey; `./discriminating-predictions.md` for the full discrimination analysis including the null hypothesis and ranking of all discriminators.

## #3: Non-Perturbative Uncertainty

Anselmi (arXiv:2601.06346, Jan 2026) acknowledged non-perturbative effects introduce "a new type of uncertainty" -- predictions become "delayed prepostdictions." In the unified framework, this uncertainty is localized to the Planck-scale transition region. But its quantitative implications (how much uncertainty? in which observables?) have not been worked out.

## #4: n_s Tension Resolution

Current CMB + DESI BAO: n_s = 0.9737 +/- 0.0025, which is 2.3-sigma above standard Starobinsky (0.964-0.967). If this tension strengthens:
- NGFP correction (b ~ 10^{-2}) shifts n_s upward to 0.970-0.975 (possible but requires computation)
- Six-derivative terms from NGFP truncation hierarchy (natural but uncomputed)
- Rethinking of inflationary sector (would undermine framework)

See `../cmb-spectral-index-tension.md` and `../../quadratic-gravity-fakeon/ns-tension-resolution-paths.md`.

## #5: Matter Sector Coupling

The framework is developed primarily for pure gravity. Including SM matter raises:
- How does the fakeon prescription interact with matter loops?
- Are NGFP boundary conditions for matter (Shaposhnikov-Wetterich) compatible with fakeon quantization?
- Does the ghost couple to matter, and if so, how does confinement affect matter physics?

## #6: Cosmological Constant Problem

Both QG+F and AS treat Lambda as a running coupling, but neither resolves the CC problem (Lambda_obs ~ 10^{-122} M_P^4). The unified framework inherits this. AS's cosmological running (G(r) at cosmic scales) might provide partial resolution, but remains speculative.

See `../cosmological-constant-problem.md` for full analysis.

## #7: Experimental Falsification Conditions

The unified theory is falsifiable via:

| Test | Falsification Condition | Timeline |
|------|------------------------|----------|
| CMB tensor-to-scalar ratio | r outside [0.0004, 0.01] | LiteBIRD ~2036-2037 |
| UV spectral dimension | Lattice gravity finds d_s != 2 | Ongoing (CDT) |
| PBH remnants | Complete evaporation (no remnants) | LISA era (2030s) |
| BH information paradox | Requires radically different physics | Theory-dependent |

Sources: Sen-Wetterich-Yamada (2022, 2023); Falls-Kluth-Litim (2023); Becker et al. (2017); Draper et al. (2020); Holdom & Ren (2015, 2016, 2024); Frasca (2025); Anselmi (2026); exploration-007-unified-framework
