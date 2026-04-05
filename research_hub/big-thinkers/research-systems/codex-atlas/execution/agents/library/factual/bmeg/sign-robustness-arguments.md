---
topic: bmeg
confidence: provisional
date: 2026-03-24
source: exploration-007-BMEG-self-consistency
---

# Three Independent Arguments for eta_h > 0

The positivity of the fluctuation graviton anomalous dimension eta_h rests on three independent, background-independent arguments. This is what gives BMEG its self-consistency: even on the d_s = 2 background, these arguments hold.

## 1. Antiscreening (Spin-2 Self-Interaction)

The graviton self-interaction is *antiscreening*: the effective Newton's constant increases at short distances, producing a positive anomalous dimension for the fluctuation graviton.

- Analogous to gluon self-interaction in QCD producing asymptotic freedom
- In QCD the sign is determined by gauge group structure (colors vs flavors); in gravity it is determined by spin-2 self-coupling structure
- Verified perturbatively (Marunovic & Prokopec, PRD 87, 104027, 2013) and nonperturbatively (Bonanno et al. 2022)
- **This is a property of the graviton's spin-2 self-interaction, NOT of the background geometry.** Changing the background modifies the *magnitude* but not the *sign*.

## 2. Spectral Function Positivity

Fehre, Litim, Pawlowski, Reichert (PRL 130, 081501, 2023) computed the graviton spectral function in Lorentzian quantum gravity:

- The fluctuation graviton spectral function is **positive** (rho_h(lambda) >= 0 for all lambda)
- It has a massless pole and multi-graviton continuum
- It satisfies the spectral sum rule of an asymptotic state
- Negative eta_h would require negative spectral weight at some scales (incompatible with total spectral weight integrating to finite value)

A 2025 self-consistent computation (arXiv:2507.22169) confirms positivity even when the full non-perturbative spectral function feeds back into loop diagrams. The authors state structural properties "rely only on the asymptotic behaviour of the Newton coupling, and changes of fixed-point value only lead to quantitative changes."

## 3. Unitarity

- eta_h > 0 gives propagator ~ 1/p^{2-eta_h}, softer than 1/p^2; combined with massless pole, requires positive spectral function
- eta_h < 0 would give 1/p^{2+|eta_h|}, generically requiring negative spectral weight (negative norm states)
- Negative spectral weight violates unitarity (optical theorem)
- **Unitarity of the fluctuation graviton requires eta_h >= 0, regardless of background geometry**

## Dimensional Cross-Check

The 2+epsilon expansion (Gastmans, Kallosh, Truffin 1978; Kawai, Ninomiya 1990) provides additional support:

- In d = 2 + epsilon: perturbative fixed point at G_* = epsilon/B with eta_h ~ O(epsilon) > 0
- eta_h is a continuous function of dimension: vanishes at d = 2, positive for d > 2
- On the d_s = 2 background (effectively 2D only at highest energies), the graviton sees d_eff > 2 at all finite momentum scales, so eta_h > 0

## Summary

These three arguments are mutually independent and none depends on the background geometry. This is the core reason BMEG's self-consistency holds: the sign of eta_h is structurally protected.
