---
topic: Empirical beta_eff from DNS via De Giorgi iteration — 5 ICs x 4 Re
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-002"
---

## Finding

The De Giorgi recurrence exponent beta_eff was measured from 3D periodic Navier-Stokes DNS across 5 initial conditions, 4 Reynolds numbers, and 2 grid resolutions (N=64, N=128 for convergence). All 21 cases use L^inf normalization (critical: L^2 normalization makes level sets trivially empty for smooth flows), K_max=10 De Giorgi levels, fit via log(U_k) = a*k + beta*log(U_{k-1}) for k=2,...,K_max.

### Key Result

**All measured beta_eff < 4/3 = 1.333.** The maximum is 1.01 (ABC at Re=1000), far below both the analytical bound (4/3) and the regularity threshold (3/2).

### Primary Data Table (N=64)

| IC | Re | beta_eff | std_err | R^2 | U_0 | Monotone |
|---|---|---|---|---|---|---|
| ABC | 100 | 0.905 | 0.048 | 0.983 | 264 | N |
| ABC | 500 | 0.983 | 0.021 | 0.996 | 270 | N |
| ABC | 1000 | **1.009** | 0.008 | **0.999** | 271 | N |
| VortexTubes | 100 | 0.662 | 0.141 | 0.954 | 79 | Y |
| VortexTubes | 500 | 0.715 | 0.127 | 0.958 | 99 | Y |
| VortexTubes | 1000 | 0.730 | 0.115 | 0.965 | 103 | Y |
| TaylorGreen | 100 | 0.737 | 0.108 | 0.965 | 468 | Y |
| TaylorGreen | 500 | 0.558 | 0.062 | 0.945 | 685 | N |
| TaylorGreen | 1000 | 0.591 | 0.054 | 0.953 | 696 | N |
| KidaVortex | 100 | 0.550 | 0.059 | 0.971 | 925 | N |
| KidaVortex | 500 | 0.459 | 0.038 | 0.972 | 2889 | N |
| KidaVortex | 1000 | 0.490 | 0.053 | 0.954 | 5358 | N |
| RandomGauss | 100 | 0.347 | 0.164 | 0.783 | 557 | N |
| RandomGauss | 500 | 0.374 | 0.126 | 0.864 | 2412 | N |
| RandomGauss | 1000 | 0.386 | 0.072 | 0.961 | 4732 | N |

Extended (Re=2000): TG beta=0.648, RG beta=0.370.

### IC Ranking by beta_eff

1. **ABC (Beltrami):** 0.90–1.01 — highest, cleanest fits (R^2 > 0.98)
2. **Vortex Tubes:** 0.66–0.73 — moderate, monotone U_k sequences
3. **Taylor-Green:** 0.56–0.87 — moderate, resolution-dependent at low Re
4. **Kida Vortex:** 0.46–0.55 — low-moderate
5. **Random Gaussian:** 0.35–0.39 — lowest, poor fit quality at low Re

### Re Dependence Is IC-Specific

- ABC: beta INCREASES with Re (0.90 → 0.98 → 1.01), approaching 1 from below
- VortexTubes: weak increase
- TaylorGreen: DECREASES from Re=100 to Re>=500 (flow develops intermittency)
- RandomGauss: flat (~0.37 across all Re)
- KidaVortex: slight increase at Re=1000

### Convergence (N=64 vs N=128)

| IC | Re | N=64 beta | N=128 beta | Diff |
|---|---|---|---|---|
| ABC | 100 | 0.905 ± 0.048 | 0.922 ± 0.036 | 0.017 (**excellent**) |
| ABC | 500 | 0.983 ± 0.021 | 0.989 ± 0.019 | 0.006 (**excellent**) |
| TaylorGreen | 100 | 0.737 ± 0.108 | 0.873 ± 0.171 | 0.136 (marginal, within 2sigma) |
| TaylorGreen | 500 | 0.558 ± 0.062 | 0.614 ± 0.050 | 0.055 (within error) |

ABC results well-converged (<2% change). TG has modest resolution dependence at Re=100 but qualitative picture unchanged.

### Non-Monotonicity of U_k

Most cases show U_1 > U_0 (non-monotone at first step). Cause: the d_k^2 dissipation functional has a threshold-dependent term proportional to lambda_k * |grad u|^2 / |u| on the active set. As lambda_k increases from 0 to 0.5, this term INCREASES even as the active set shrinks. Does NOT invalidate the De Giorgi iteration — the recurrence U_k <= C^k * U_{k-1}^beta is about consecutive-level relationships, not monotonicity.

### Critical Caveat: beta_eff != beta_p

**Vasseur's beta_p** is the WORST-CASE exponent in a proved inequality for ALL suitable weak solutions, including potential singular ones. **Empirical beta_eff** is the best-fit exponent from specific smooth DNS solutions. For smooth solutions, the De Giorgi iteration converges rapidly regardless, so the recurrence holds with many possible (a, beta) pairs. Therefore: beta_eff < 4/3 does NOT mean the analytical bound is tight. The bottleneck exponent gamma is more directly comparable — see `bottleneck-exponent-dns.md`.

### Resolution Effects at High k

At k >= 7-8 with N=64, only a handful of grid points lie above threshold (lambda_k >= 0.992), producing quantized U_k ratios (artifacts). Convergence checks confirm beta_eff values stabilize for the lower k range (k=2-6) that dominates the fit.

## E009 Adversarial Assessment

**The measurement proves smooth solutions are smooth — a tautology.** For smooth solutions, U_k = 0 exactly for k > k_max (where lambda_k exceeds ||u||_infty). The fitted beta_eff reflects the transient decay over the first few k-levels, which depends on the specific flow's velocity distribution, NOT on the analytical structure of the De Giorgi proof. beta_eff < 4/3 is EXPECTED for smooth solutions and proves nothing about whether the analytical bound is tight for near-singular solutions. The non-monotonicity of U_k further undermines the measurement — the recurrence model U_k ~ C^k U_{k-1}^beta doesn't even fit well for some flows, making the extracted "beta_eff" a poor description of the data.

**The measurement survives as an empirical fact; the interpretation does NOT survive.** The data table is valid computational output, but the conclusion "this suggests the 4/3 analytical bound is close to sharp for general turbulent flows" is not supported. The data is equally consistent with the 4/3 bound being arbitrarily loose, because smooth DNS solutions don't probe the regime where the bound matters.

**Corrected framing:** "DNS measurements of the De Giorgi recurrence on smooth solutions yield beta_eff = 0.35-1.01, confirming that smooth flows decay much faster than the De Giorgi geometric rate. ABC/Beltrami flows show the highest beta_eff (~1.0), consistent with the Beltrami mechanism. The data characterizes pressure-velocity coupling structure on smooth flows but cannot diagnose whether the analytical 4/3 bound is tight for near-singular solutions." Grade: C (measurement done, interpretation problematic). **Novel** — no prior work extracts De Giorgi recurrence exponents from DNS.

**One salvageable result:** ABC beta_eff -> 1.0 with increasing Re IS interesting because it corroborates the Beltrami mechanism (Claim 4), providing corroborative evidence for the geometric story.
