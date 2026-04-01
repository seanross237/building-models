---
topic: cross-cutting
confidence: provisional
date: 2026-03-24
source: exploration-004-ns-tension-analysis (strategy-002)
---

# CMB Spectral Index Tension: Observational Status (2025)

## The Tension

The scalar spectral index n_s measured from the CMB is in growing tension with the Starobinsky/R² inflation prediction of n_s ≈ 0.967 (for N = 60 e-folds). The tension is primarily driven by DESI BAO data combined with CMB measurements.

## Key Measurements

### ACT DR6 (March 2025, arXiv: 2503.14452)

- **P-ACT + lensing + DESI DR1 BAO**: n_s = 0.974 ± 0.003
- Running of spectral index: dn_s/d ln k = 0.0062 ± 0.0052 (consistent with zero)
- H₀ = 68.22 ± 0.36 km/s/Mpc
- P-ACT + DESI DR2: ΛCDM parameters agree at 1.6σ

### Planck PR4 NPIPE Reanalysis (Tristram et al. 2024)

- **Planck PR4 alone**: n_s = 0.9638 ± 0.0040 (from arXiv: 2512.05108)
- Error bars reduced 10-20% vs. Planck 2018
- No major shifts in central values
- **Key**: Planck PR4 alone does NOT show the tension — its central value (~0.964) is even lower than Planck 2018

### SPT-3G D1 (June 2025, arXiv: 2506.20707)

- **SPT-3G D1 alone**: n_s = 0.951 ± 0.011
- Deepest CMB TT/TE/EE maps to date (4% of sky)
- Central value is LOWER than both Planck and ACT (larger error bars)

### DESI BAO (arXiv: 2404.03002)

- DESI BAO alone: Ωm = 0.295 ± 0.015
- **When combined with CMB, DESI systematically shifts n_s upward**: ACT shows Δn_s ≈ +0.010; Planck shows Δn_s ≈ +0.005
- Mechanism: n_s correlates with BAO parameters in CMB fit; DESI's distance measurements pull n_s higher

## Combined Analyses

From arXiv: 2512.05108 ("The spectrum of n_s constraints from DESI and CMB data"):

| Dataset | n_s (CMB alone) | n_s (CMB + DESI) |
|---|---|---|
| Planck PR4 | 0.9638 ± 0.0040 | 0.9690 ± 0.0035 |
| ACT alone | 0.9666 ± 0.0076 | 0.9767 ± 0.0068 |
| SPT-3G alone | 0.948 ± 0.012 | 0.955 ± 0.012 |
| CMB-SPA (combined) | 0.9693 ± 0.0029 | 0.9737 ± 0.0025 |

From arXiv: 2512.10613 ("Inflation at the End of 2025"):

| Dataset | n_s | r (95% CL) |
|---|---|---|
| CMB only (SPA+BK) | 0.9682 ± 0.0032 | < 0.034 |
| CMB + DESI (SPA+BK+DESI) | 0.9728 ± 0.0029 | < 0.035 |

## Critical Findings

1. The upward shift from ~0.969 → ~0.974 is driven primarily by DESI BAO data
2. **CMB alone (combined): n_s ≈ 0.969** — barely 1σ above Starobinsky
3. **CMB + DESI: n_s ≈ 0.974** — 2.3σ above Starobinsky
4. The "3.9σ tension" claim is the most extreme (ACT + DESI only)
5. **Inter-experiment tension**: ACT + DESI at 3.1σ internal tension, SPT + DESI at 2.5σ, Planck + DESI at 2.0σ

## Systematic Effects

1. **DESI-CMB parameter degeneracy**: If DESI BAO has unrecognized systematics, the n_s shift could be artificial
2. **CMB lensing anomaly**: Planck A_L > 1 at ~2σ correlates with n_s; PR4 reduces this
3. **Foreground contamination**: ACT/SPT higher multipoles more sensitive to foreground subtraction
4. **Inter-experiment tension**: SPT n_s = 0.951 vs. ACT n_s = 0.967 suggests potential systematics
5. **DESI dark energy hints**: If dark energy is dynamical (w₀wₐCDM), BAO distance inferences change, affecting derived n_s

## Early Dark Energy Wild Card

If Early Dark Energy (EDE) resolves the Hubble tension, the inferred n_s shifts dramatically (arXiv: 2509.11902):
- Axion-like EDE: Planck+SPT+ACT gives n_s = 0.979 ± 0.006
- AdS-EDE: gives n_s = 0.996 ± 0.005 (near Harrison-Zeldovich!)

If EDE is real, the "true" primordial n_s could be even higher than 0.974, making the Starobinsky tension WORSE. Alternatively, the observed tension could be an artifact of fitting ΛCDM to data that actually requires EDE.

## Future Experiments

| Experiment | Timeline | n_s Impact |
|---|---|---|
| Simons Observatory | First light ~2025 | Better small-scale measurements, delensing |
| ~~CMB-S4~~ | **CANCELLED July 2025** | ~~σ(n_s) ~ 0.002; a 0.007 shift would be >3σ~~ |
| LiteBIRD | 2032 launch | Full-sky polarization, combined with ground n_s |
| DESI DR2/DR3 | Partially available | Reduce BAO systematics |

**Resolution timeline**: With CMB-S4 cancelled (July 2025), the definitive timeline shifts to ~2034-2037 via SO enhanced (6 SATs) + LiteBIRD + DESI DR3. See [`cmb-experimental-timeline.md`](cmb-experimental-timeline.md).

## Assessment

The n_s tension is **real but not yet conclusive** (~2-3σ). It is primarily driven by the DESI-CMB combination, not by CMB alone. There is perhaps a 30-40% chance the tension shrinks as DESI systematics are better understood and SPT-3G's lower central value pulls combined constraints down. The next 3-5 years will be decisive.

Sources: arXiv: 2503.14452 (ACT DR6), arXiv: 2512.05108, arXiv: 2512.10613, arXiv: 2506.20707 (SPT-3G D1), arXiv: 2404.03002 (DESI DR1), arXiv: 2509.11902 (EDE)
