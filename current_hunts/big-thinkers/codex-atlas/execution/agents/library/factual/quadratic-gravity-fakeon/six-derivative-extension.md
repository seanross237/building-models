---
topic: quadratic-gravity-fakeon
confidence: verified
date: 2026-03-25
source: exploration-005-ns-beta-functions-six-derivative (strategy-002), exploration-004-ns-tension-analysis (strategy-002), exploration-008-six-derivative-validation (strategy-002)
---

# Six-Derivative Super-Renormalizable Gravity: QG+F Extension

## Motivation

The RG running of the R^2 coupling within QG+F is definitively insufficient to resolve the n_s tension (Delta_n_s ~ 10^{-14}; see `ns-tension-resolution-paths.md`). The most natural next step is extending QG+F to six derivatives, which naturally includes the R^3 correction that resolves the tension.

## The Six-Derivative Action

### Complete Inventory of Six-Derivative Terms in 4D

There are **17 independent scalar invariants of mass dimension six** in the gravitational action:

**Pure cubic curvature terms (8):**
1. R^3
2. R R_{mu nu}R^{mu nu}
3. R_{mu nu}R^{nu rho}R_{rho}^{mu}
4. R_{alpha beta}R_{mu nu}R^{alpha mu beta nu}
5. R R_{alpha mu beta nu}R^{alpha mu beta nu}
6. R_{alpha rho}R_{mu beta nu rho}R^{alpha mu beta nu}
7. R_{alpha mu beta nu}R^{rho sigma alpha mu}R_{rho sigma}^{beta nu}
8. R_{alpha mu beta nu}R^{alpha rho beta sigma}R^{mu}_{rho}^{nu}_{sigma}

**Terms with derivatives on curvature (9):**
9-17: nabla_lambda R nabla^lambda R, nabla_lambda R_{mu nu} nabla^lambda R^{mu nu}, nabla_lambda R_{mu nu} nabla^mu R^{lambda nu}, nabla_lambda R_{alpha mu beta nu} nabla^lambda R^{alpha mu beta nu}, R box R, R^{mu nu} nabla_mu nabla_nu R, R_{mu nu} box R^{mu nu}, R^{alpha mu beta nu} nabla_mu nabla_nu R_{alpha beta}, box^2 R

### Reduction to Independent Terms

After integration by parts, Xu's geometric identity (4D), and the 4D Lovelock constraint (6D Euler density is topological), the 17 terms reduce to **10 independent terms** in the action integral.

### Minimal Propagator-Relevant Form

Following Rachwal, Modesto, Pinzul, Shapiro (arXiv:2104.13980, PRD 104, 085018, 2021):

    S_6 = integral d^4x sqrt(-g) [ (1/kappa^2)R + theta_{0,R} R^2 + theta_{0,C} C^2
                                   + theta_{1,R} R box R + theta_{1,C} C box C ]

where theta_{0,R} = 1/(6f_0^2), theta_{0,C} = -1/(2f_2^2). This has **5 propagator-relevant parameters**: kappa^2, theta_{0,R}, theta_{0,C}, theta_{1,R}, theta_{1,C}.

### For Cosmological Backgrounds: Only 3 Matter

On FLRW backgrounds, isotropy and homogeneity drastically reduce independent contributions (arXiv:2509.09167). Only **3 effectively contribute**:
1. **R^3** -- the most important for inflation; shifts n_s
2. **R box R** -- introduces new dynamical degrees of freedom
3. **R R_{mu nu}R^{mu nu}** -- mixes with scalar and tensor sectors

The inflation-relevant action reduces to an f(R) theory (Weyl tensor vanishes on FLRW):

    f(R) = R/(2 kappa^2) + R^2/(6m^2) + delta_3 R^3/(36m^4) + ...

## Propagator Structure and Particle Content

### Spin-2 Sector

Propagator decomposes via Barnes-Rivers projectors. The six-derivative spin-2 form factor gives a cubic equation in k^2, yielding **three spin-2 poles**:
- k^2 = 0: massless graviton (healthy, 2 DOF)
- k^2 = -mu^2_+ and k^2 = -mu^2_-: two massive spin-2 modes (5 DOF each)

Mass eigenvalues:

    mu^2_pm = [1/(2 lambda theta_{1,C})] x [1 +/- sqrt(1 - 4 lambda^2 theta_{1,C}/kappa^2)]

where lambda = -1/theta_{0,C} = 2f_2^2.

### Spin-0 Sector

Three spin-0 poles: k^2 = 0 decouples (Bianchi identity), plus two massive spin-0 modes (1 DOF each).

### Total Particle Content

- 1 massless graviton (2 DOF) -- healthy
- 2 massive spin-2 modes (5 DOF each) -- at least one is a ghost
- 2 massive spin-0 modes (1 DOF each) -- one may be ghostly
- **Total: 14 DOF** (vs. 8 DOF in four-derivative QG+F)

### Alternating Residues (Ghost Theorem)

The spin-2 propagator partial fraction decomposition has alternating signs -- a theorem for polynomial propagators with N poles. For three poles, at least one massive mode has wrong-sign residue (ghost).

## Ghost Resolution: Two Approaches

### Approach 1: Fakeon Prescription (Anselmi)

Ghost-pole modes declared "fakeons." Modified cutting rules (spectral optical identities) ensure S-matrix unitarity. Extends to any number of ghost poles.

### Approach 2: Lee-Wick Complex Mass Pairs (PREFERRED)

When 4 lambda^2 theta_{1,C}/kappa^2 > 1, the two massive spin-2 poles become **complex conjugate pairs**:
- Complex-mass particles are inherently unstable; never go on-shell
- No modification of cutting rules needed -- standard QFT
- Complex poles are gauge-independent and "sedentary"
- Ghost-like states may form physical bound states (arXiv:2511.15283)
- Preserves super-renormalizability

A 2025 paper (Anselmi, Briscese, Calcagni et al., JHEP May 2025) compared four inequivalent amplitude prescriptions and concluded **only the fakeon prescription is physically viable** (CLOP/LWN fails).

Unitarity proof extended to general higher-derivative theories with fakeons by Piva (arXiv:2305.12549, EPJP 2023).

## Key Properties

| Property | QG+F (4-derivative) | Six-derivative extension |
|---|---|---|
| Renormalizability | Renormalizable | **Super-renormalizable** |
| UV finiteness | All loop orders diverge | **One-loop divergences only** |
| Propagator (high p) | ~1/p^4 | ~1/p^6 |
| Unitarity | Via fakeon for spin-2 ghost | Via fakeon/Lee-Wick for all massive modes |
| Spectral dimension | d_s = 4 -> 2 | **d_s = 4 -> 4/3** |
| Lorentz invariance | Yes | Yes |
| Diffeomorphism invariance | Yes | Yes |
| Propagating DOF | 8 | **14** |
| Free parameters | 2 beyond GR (M_2, M_0) | +10 new (cubic coefficients) |
| Cosmologically relevant params | 2 | +3 (of which delta_3 dominates) |
| R^3 term | Absent at tree level | **Naturally present** |

## Super-Renormalizability (Stronger Than Power Counting)

Naive power counting for 2N-derivative theory in D=4: omega(L) = 4 - 2(N-2)(L-1). For N=3: omega(L) = 6 - 2L, divergent at L = 1,2,3.

However, the actual situation is **better** (Rachwal et al. arXiv:2104.13980): "divergences show up only at the first loop. Only four-, second- and zero-derivative terms in the action get renormalized."

- **One-loop:** Divergences in R^2, C^2, Gauss-Bonnet, R (Newton constant), and Lambda (cosmological constant)
- **Two-loop and higher:** FINITE -- no divergences
- **The six-derivative couplings theta_{1,R}, theta_{1,C} do NOT run** (exactly marginal at one loop)

Asymptotically free: all running couplings -> 0 in the UV.

## Spectral Dimension: d_s = 4/3 (NOT 2)

The six-derivative propagator scales as ~1/k^6 at high momenta, corresponding to dynamical critical exponent z = 3. Therefore:

    d_s(UV) = D/z = 4/3 ~ 1.33

| Theory | d_s(IR) | d_s(UV) |
|--------|---------|---------|
| GR | 4 | 4 |
| QG+F (4-derivative) | 4 | 2 |
| Six-derivative QG+F | 4 | **4/3** |

This is **stronger UV dimensional reduction** than QG+F, and crosses below the d_s = 2 critical boundary for renormalizability -- consistent with super-renormalizability. Note: this overshoots the d_s = 2 "target" from the constructive axiom program (see `core-idea.md`), which is why the six-derivative theory is not uniquely selected by that derivation.

## Inflationary Predictions with R^3

### Modified Action (f(R) sector)

    f(R) = 1/2 (R + R^2/(6m^2) + delta_3 R^3/(36m^4))

where m is the scalaron mass and delta_3 is a dimensionless coupling.

### Modified Slow-Roll Parameters

For y = e^{-sqrt(2/3) phi/M_P} << 1:

    epsilon_V ~ (4/3) y^2 - (2/3) delta_3
    eta_V ~ -(4/3) y - (1/3) delta_3 y^{-1}

### Numerical Results

| Parameter | Pure Starobinsky | With R^3 (delta_3 = -1.19 x 10^{-4}) |
|-----------|-----------------|---------------------------------------|
| n_s | ~ 0.967 (N=55) | **~ 0.974** |
| r | ~ 0.003 | **~ 0.0045** |
| alpha_s | ~ -0.0006 | **~ -0.0008** |

Source: arXiv:2505.10305. Matches ACT+DESI data at 1 sigma.

### Mechanism

Negative delta_3 makes the potential plateau slightly flatter at large field values, reducing |eta_V| and increasing n_s: Delta_n_s ~ +(2/3)|delta_3|/y ~ +0.005 to +0.008.

### Tachyonic Instability

For delta_3 < 0, the R^3 term eventually causes f'(R) < 0 at very large R -> tachyonic instability. Occurs at **trans-Planckian** curvatures irrelevant for inflation.

## Naturalness of delta_3 ~ 10^{-4}

| Perspective | Expected delta_3 | Assessment |
|-------------|-----------------|------------|
| EFT (derivative expansion) | (m/Lambda)^2 with Lambda ~ 100m ~ 3 x 10^{15} GeV | **Natural** (near GUT scale) |
| Loop-generated in QG+F | f_0^2/(16 pi^2) ~ 10^{-10} | 6 orders too small -> must be tree-level |
| Six-derivative theory | Free parameter | Smallness reflects mass hierarchy |

The new mass scale Lambda_6 ~ m/sqrt(|delta_3|) ~ 3 x 10^{15} GeV sits between inflation (~10^{13} GeV) and Planck (~10^{18} GeV), close to the GUT scale.

**Key conclusion**: If delta_3 ~ 10^{-4}, the R^3 term must be a **fundamental tree-level coupling**, not loop-generated. Points to six-derivative theory as fundamental, with QG+F as its leading-order truncation.

## Validation Summary (Full Tier 1-4)

### Tier 1 (Structural Sanity): PASS

| Check | Status | Notes |
|-------|--------|-------|
| Ghost analysis | Conditional PASS | Ghosts present but resolvable |
| Fakeon/Lee-Wick | PASS | Both approaches work; Lee-Wick preferred |
| Unitarity | PASS | Proven via spectral optical identities |
| Super-renormalizability | PASS | One-loop divergences only |
| Asymptotic freedom | PASS | All couplings -> 0 in UV |

### Tier 2 (Known Physics): PASS

All corrections Planck-suppressed. GR recovery, Newtonian potential (Yukawa corrections exponentially suppressed at r >> 10^{-29} cm), PPN parameters (gamma = beta = 1 to absurd precision), GW speed = c for massless graviton.

### Tier 3 (Precision Tests): PASS

Massless graviton preserved, Wald entropy formula well-defined (corrections negligible for astrophysical BH), spectral dimension d_s = 4/3 in UV, modified Stelle potential with oscillatory Yukawa corrections (Lee-Wick regime).

### Tier 4 (Novel Predictions): PASS with caveats

| Prediction | Value | Testable? | Timeline |
|-----------|-------|-----------|----------|
| n_s | 0.974 | YES | CMB-S4 (~2030), Simons Observatory |
| r | 0.0045 | YES | LiteBIRD (~2032) |
| alpha_s (running) | -0.0008 | Marginal | CMB-S4 + DESI |
| d_s (UV) | 4/3 | No | Conceptual only |
| Microcausality violation | E > M_2 | No | Planck-scale energies |
| New massive modes | ~10^{13}-10^{18} GeV | No | Far beyond colliders |

## Comparison Table: GR vs QG+F vs Six-Derivative

| Property | GR | QG+F (4-deriv) | Six-Derivative QG+F |
|----------|:--:|:--------------:|:-------------------:|
| Free params beyond GR | 0 | 2 (M_0, M_2) | 4 (propagator) or 3 (inflation) |
| Propagating DOF | 2 | 8 | 14 |
| n_s | N/A | ~0.967 | **~0.974** |
| r | N/A | [0.0004, 0.0035] | **~0.0045** |
| d_s (UV) | 4 | 2 | **4/3** |
| Renormalizability | No | Renormalizable | **Super-renormalizable** |
| Divergent loops | All | All | **One-loop only** |
| Ghost treatment | N/A | Fakeon (1 spin-2) | Lee-Wick complex pairs preferred |
| BH entropy | A/4 | A/4 + small corr. | A/4 + slightly different corr. |

## Novelty Assessment

**Not a truly "novel theory"** but a legitimate, observationally distinguishable extension of QG+F:
- The next term in the EFT expansion of QG+F
- A UV improvement: renormalizable -> super-renormalizable
- A one-parameter extension for inflation: delta_3 shifts n_s

Best described as **"six-derivative QG+F"** or **"super-renormalizable QG+F"**.

### Research Status

~20-30 papers directly on six-derivative quantum gravity (2017-2025), ~100+ on broader super-renormalizable/higher-derivative gravity with fakeons/Lee-Wick.

**Computed:** One-loop beta functions, propagator structure, super-renormalizability proof, asymptotic freedom, inflationary predictions, unitarity, exact BH solutions (2025), amplitude prescriptions comparison (2025).

**Open:** Full two-loop finiteness verification, Newtonian potential with six-derivative corrections + fakeon, whether delta_3 is constrained by RG flow, Lee-Wick bound state spectrum in gravity, spectral dimension from diffusion equation.

## Active Research Groups

- **Anselmi and collaborators** (Pisa): QG+F and fakeon framework
- **Rachwal, Modesto, Shapiro**: six-derivative QG beta functions
- **Salvio** (Rome): quadratic gravity phenomenology
- **Branchina, Donoghue, Percacci**: physical beta functions
- **Ferrara, Ferraro et al.**: cubic curvature inflation (arXiv:2509.09167, arXiv:2505.10305)
- Various cosmology groups: R^3 corrections motivated by ACT/DESI (~20+ papers 2024-2025)

Sources: arXiv:2104.13980, arXiv:2505.10305, arXiv:2509.09167, arXiv:2508.07508, arXiv:2305.12549, arXiv:2511.15283, arXiv:2511.06640, arXiv:2504.20757, arXiv:1004.0737
