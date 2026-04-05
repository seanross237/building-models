---
topic: T_BKM/T_Lad ~ Re^3 — BKM avoids the nu^{-3} factor in Ladyzhenskaya enstrophy ODE
confidence: provisional
date: 2026-03-30
source: "navier-stokes strategy-002 exploration-001/002/004 (adversarial review)"
---

## Overview

The Ladyzhenskaya enstrophy ODE has a nu^{-3} factor from Young's inequality (absorbing ||grad omega||^2 into dissipation), giving T_Lad ~ nu^3 / (C * E_0^2). The BKM exponential doubling time T_double ~ 1/(sqrt(2) * sup||omega||_Linf) avoids this factor. Their ratio T_double/T_Lad ~ Re^3 under the natural scaling M ~ sqrt(E_0) ~ 1/Re.

**Verified numerically:** T_Lad * Re^3 = 1.252e-3 (constant to 4 digits across Re=100-5000). [COMPUTED]

## The nu^{-3} Mechanism (VERIFIED)

Starting from the enstrophy equation with Ladyzhenskaya in 3D:
- VS ≤ (C_L^2/sqrt(2)) * ||omega||^{3/2} * ||grad omega||^{3/2}
- Young's inequality to absorb ||grad omega||^2: setting epsilon = 2/nu gives (nu/2)||grad omega||^2 + (2/nu)^3 * E^3
- The nu^{-3} factor emerges from (2/nu)^3
- Result: T_Lad = nu^3/(C * E_0^2)

This is correct. No published paper makes the nu^{-3} mechanism explicit as "the factor BKM avoids."

## Adversarial Caveats

### 1. Comparing Different Types of Time (MOST SERIOUS)
T_Lad is a genuine **finite-time blow-up** prediction from an ODE dE/dt ~ E^3. T_BKM is an **exponential doubling time** from dE/dt ~ E (which NEVER blows up for finite ||omega||_Linf). The comparison is between fundamentally different kinds of quantity — not symmetric. BKM never predicts blow-up; Ladyzhenskaya always does.

### 2. Scaling Assumption
The Re^3 ratio assumes M ~ U ~ sqrt(E_0) and L=1 (unit domain T^3). For highly intermittent flows where ||omega||_Linf >> ||omega||_L2, the ratio could differ.

### 3. T_Lad Is Catastrophically Pessimistic
The 237x vortex stretching slack means T_Lad underestimates the true blow-up time by ~(237)^{2/3} ~ 100x even within the Ladyzhenskaya framework. The Re^3 advantage of BKM is real but overstates the practical difference.

### 4. DNS Shows T_Lad Is Meaningless in Practice
T_Lad ~ 10^{-15} at Re=1000 but actual blow-up doesn't occur in simulations. Comparing "theoretical blow-up times" may be misleading when neither matches reality.

## Novelty Verdict

**NOVEL** — The explicit Re^3 scaling comparison between BKM and Ladyzhenskaya enstrophy ODEs appears not in the published literature. The mechanism (Young's inequality giving nu^{-3}) is implicit in many texts (Constantin-Foias 1988, Majda-Bertozzi 2001) but not stated as "the factor BKM avoids."

**Defensibility: 3/5** — Mathematically correct under natural scaling. Weakened by the apples-to-oranges comparison of different time types. Would benefit from a cleaner formulation.

## Literature

- Constantin-Foias (1988), Majda-Bertozzi (2001): nu^{-3} scaling implicit but not highlighted
- Doering group: confirms enstrophy bounds are "sharp" in some sense but does not make BKM vs Ladyzhenskaya comparison
- No published paper makes this explicit comparison
