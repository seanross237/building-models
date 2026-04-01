# Mission: Vasseur Pressure Exponent Gap

## Goal

Determine whether the Vasseur pressure exponent gap (beta = 4/3, need beta > 3/2) can be closed using H^1 structure of the pressure from compensated compactness.

## Background

The De Giorgi method for Navier-Stokes regularity, developed by Caffarelli, Kohn, Nirenberg and extended by Vasseur (2007), requires controlling the pressure term in the energy inequality. The current best pressure exponent is beta = 4/3 (from Calderon-Zygmund bounds on the Newtonian potential of div(u x u)). The De Giorgi iteration needs beta > 3/2 to close. This gap of 1/6 is the single bottleneck — the entire Millennium Prize Problem compresses to improving this one exponent.

The pressure p = (-Delta)^{-1} div div (u x u) lives in H^1(R^3) (Hardy space) by the div-curl lemma / compensated compactness theory of Coifman-Lions-Meyer-Semmes. The question is whether this H^1 structure — which is strictly stronger than L^1 — can be leveraged within the De Giorgi framework to improve the exponent beyond 4/3.

## Key Context

- beta = 4/3 has been unchanged since Vasseur 2007 (19 years)
- The Leray-Hopf energy class provides u in L^2_t H^1_x, hence Du in L^2
- The pressure satisfies -Delta p = div div (u x u), giving p in H^1 by CZ theory
- The gap between W^{1,2} (what NS provides) and W^{1,3} (what many routes need) is a known structural barrier
- Three main H^1 exploitation routes exist: interpolation, H^1-BMO duality, atomic decomposition
