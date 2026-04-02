---
topic: ABC (Beltrami) flow has highest beta_eff and most stable bottleneck exponent
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-002"
---

## Finding

The Arnold-Beltrami-Childress (ABC) flow — u = (B sin y + C cos z, C sin z + A cos x, A sin x + B cos y) with A=B=C=1 — shows dramatically better De Giorgi iteration behavior than all other tested ICs. The Beltrami property (curl(u) = u, so u is an eigenfunction of curl) provides structural advantages for the De Giorgi analysis.

### ABC vs Other ICs

| Property | ABC | Next best | Worst |
|---|---|---|---|
| beta_eff at Re=1000 | **1.009** | 0.730 (VT) | 0.386 (RG) |
| R^2 at Re=1000 | **0.999** | 0.965 (VT) | 0.961 (RG) |
| gamma at Re=1000 | **1.103** | 1.154 (VT) | 0.459 (KV) |
| U_0 | ~270 | ~100 (VT) | ~5000 (KV) |

### Why ABC Is Special

1. **beta_eff increases toward 1.0 with Re:** 0.90 (Re=100) → 0.98 (Re=500) → 1.01 (Re=1000). Other ICs either decrease or stay flat.

2. **Best fit quality:** R^2 = 0.983 → 0.996 → 0.999. The De Giorgi recurrence model fits ABC data almost exactly.

3. **Smallest U_0 (~270):** Less intermittent velocity field compared to other ICs (500-5000).

4. **Most stable bottleneck exponent:** gamma ~ 1.10-1.22 across all Re (other ICs vary by 2-3x).

### Physical Mechanism (Confirmed Analytically — E006)

The Beltrami property (curl u = u) preserves velocity field structure and maintains well-populated level sets. **E006 derivation:** The Lamb vector L = omega x u = lambda(u x u) = 0 identically, so u . nabla u = nabla(|u|^2/2) — the entire nonlinear advection is a pure gradient. The pressure is p = -|u|^2/2 + const (Bernoulli), requiring NO Calderon-Zygmund inversion. The CZ "loss" is exactly zero because the pressure Poisson source is a pure Hessian. Solution decays as u(t) = u_0 exp(-nu lambda^2 t), trivially regular. See `../../beltrami-pressure-analytical.md` for full derivation.

### Truncation Survival (Confirmed — E007)

The De Giorgi truncation u_below = u min(1, lambda_k/|u|) preserves Beltrami structure: Beltrami deficit B_k = O(2^{-k}), pressure remainder R_frac = O(2^{-k}), bottleneck remainder I_r/I_t = O(2^{-k}). The CZ-lossy piece of the pressure contributes < 5% of the bottleneck at k=4 and < 0.2% at k=8. All quantities are Re-independent. See `beltrami-deficit-truncation-survival.md` and `pressure-bernoulli-dominance-truncated.md`.

### Actionable Insight

The ABC flow's favorable scaling suggests investigating conditional regularity: "if the velocity field is sufficiently Beltrami-like, then beta > 3/2." This connects to known results on geometric regularity criteria (Beirao da Veiga & Berselli on the alignment of velocity and vorticity). The d_k^2 second term in the De Giorgi functional (threshold-dependent) also behaves better for Beltrami flows. **E007 resolves the key obstacle** (truncation breaking Beltrami): the mechanism survives truncation.

### Convergence

ABC results are well-converged: N=64 to N=128 changes are < 2% for beta_eff and < 1% for gamma. This is the most robust finding in the DNS measurement campaign.

## E009 Adversarial Assessment

The beta_eff ~ 1.0 for ABC is consistent with the Beltrami mechanism but is NOT causal verification — ABC flows are globally smooth and far from singular, so their beta_eff reflects their specific velocity distribution, not the analytical structure of the pressure bound. However, the ABC beta_eff -> 1.0 trend with increasing Re IS interesting as corroborative evidence for the geometric story. See `beltrami-deficit-truncation-survival.md` for the E009 assessment of the truncation survival claim (the weakest claim in Strategy-001). **The strongest surviving finding from Strategy-001 is the structural story: Lamb vector -> CZ loss, Beltrami -> L=0 -> no loss, connecting flow geometry to the De Giorgi bottleneck in a way no published paper appears to have done.**

## E010 Update — Advantage Is Measure-Zero Specific

E010 tested perturbed-ABC flows (u = (1-eps) u_ABC + eps u_random) and found that the beta_eff advantage degrades continuously: 1.01 (eps=0) -> 1.07 (eps=0.01) -> 0.89 (eps=0.05) -> 0.28 (eps=0.50). beta > 1 is maintained only for eps < ~0.02. The "ABC is special" result is real but specific to exact or near-exact Beltrami flows — a measure-zero set in the space of all initial conditions. See `../../near-beltrami-negative-result.md`.
