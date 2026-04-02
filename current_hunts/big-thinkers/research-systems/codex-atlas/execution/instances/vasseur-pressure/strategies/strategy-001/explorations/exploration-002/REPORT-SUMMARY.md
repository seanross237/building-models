# Exploration 002 Summary: Empirical Beta from De Giorgi Iteration

## Goal
Measure the De Giorgi recurrence exponent beta_effective on 3D Navier-Stokes DNS across 5 initial conditions and multiple Reynolds numbers. The analytical bound is beta < 4/3; regularity requires beta > 3/2.

## What Was Tried
Ran 21 DNS cases: 5 ICs (Taylor-Green, vortex tubes, random Gaussian, Kida, ABC) x 3-4 Re values (100-2000) at N=64, plus 4 convergence checks at N=128. For each case: computed De Giorgi level-set energies U_k for k=0,...,10, fit the recurrence log(U_k) = a*k + beta*log(U_{k-1}), and measured the bottleneck pressure integral separately.

## Outcome: Inconclusive-to-Negative

**All beta_eff < 4/3**, ranging from 0.35 (random Gaussian) to 1.01 (ABC at Re=1000). However, empirical beta on smooth DNS solutions is not directly comparable to Vasseur's worst-case analytical beta.

The more informative **bottleneck exponent** (measuring the pressure integral's scaling that limits beta_p) shows:
- gamma > 4/3 only for the smoothest flows (laminar, Re=100)
- gamma DECREASES with Re for all ICs
- At Re >= 500, gamma drops to 0.5-0.6 for turbulent ICs

This suggests the 4/3 bound is close to sharp for general turbulent flows — the gap to 3/2 appears genuine, not analytical looseness.

## Verification Scorecard
- [COMPUTED]: 21 cases with reproducible code (15 primary + 4 convergence + 2 high-Re)
- [CONJECTURED]: 2 claims (gap is genuine; Beltrami structure helps)

## Key Takeaway
The bottleneck pressure integral's exponent worsens (moves away from 4/3) as flows become more turbulent. This is the **opposite** of what the regularity program needs. The gap between beta < 4/3 and beta > 3/2 likely reflects genuine mathematical difficulty in controlling the pressure term, not analytical slack.

## Unexpected Findings
- **ABC (Beltrami) flow is dramatically better**: beta_eff ~ 1.0, bottleneck gamma ~ 1.1-1.2, both the highest among all ICs. The Beltrami property (u = eigenfunction of curl) provides genuine analytical leverage.
- **Non-monotonicity of U_k** is real for most cases (due to threshold-dependent term in d_k^2), not a numerical artifact.

## Leads Worth Pursuing
1. **Conditional regularity via Beltrami-near structure**: the ABC finding suggests a conditional result exploiting velocity-vorticity alignment
2. **Refined De Giorgi functional**: modifying d_k^2 to remove the non-monotone threshold term might improve bounds
3. **Pressure decomposition at turbulent scales**: understanding why gamma saturates at Re ~ 500-1000

## Computations Identified
- Measure beta_eff for ABC at Re = 5000-10000 (does the trend beta → 1 continue?)
- Test the velocity-vorticity alignment angle on cases where beta is highest
- Compute conditional bottleneck exponent restricted to regions of high strain
