---
topic: Fernandez-Dalgo (2025) dynamic pressure decomposition in paraboloid geometry
confidence: provisional
date: 2026-03-30
source: "vasseur-pressure exploration-005"
---

## Finding

Pedro Gabriel Fernandez-Dalgo (BCAM, Bilbao), "Dynamic Refinement of Pressure Decomposition in Navier-Stokes Equations," arXiv:2501.18402v2, April 2025.

### What It Does

The paper proves that critical energy of a Leray-type solution inside a backward paraboloid is controlled by behavior near the paraboloid's boundary, excluding the interior near the vertex. Uses a **time-dependent pressure decomposition** with three pieces (p_1, p_2, p_3) where the cutoff regions MOVE in time (depending on the parabolic scaling factor theta_a(tau) = sqrt(-a*tau)).

### Technical Approach

- Uses Gronwall-type energy methods, NOT De Giorgi iteration
- Paraboloid geometry replaces nested balls
- Three-way split similar to CV14 but adapted to time-dependent domains
- Key result: relaxes L^3 hypothesis from exterior regions to intermediate scales (L^{3,infinity})

### What It Does NOT Do

- Does NOT address the De Giorgi recurrence exponent beta
- Does NOT use iterative recurrence (U_k <= C^k * U_{k-1}^beta)
- Represents progress in epsilon-regularity criteria, a DIFFERENT direction from the beta problem

### Relationship to CV14

Structurally similar three-way pressure decomposition, but the "dynamic" aspect (cutoff regions moving in time) is genuinely new. The innovation is optimal localization of pressure in a paraboloid geometry, not improvement of De Giorgi iteration.
