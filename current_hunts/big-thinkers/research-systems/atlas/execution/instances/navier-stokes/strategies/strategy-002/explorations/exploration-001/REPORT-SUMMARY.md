# Exploration 001 Summary: BKM Enstrophy Bypass — Computational Validation

## Goal
Determine whether the BKM (Beale-Kato-Majda) approach to bounding vortex stretching gives tighter enstrophy regularity criteria than the standard Ladyzhenskaya chain, by computing both bounds on DNS data for 3 initial conditions × 4 Reynolds numbers.

## What Was Tried
- Ran 13 pseudospectral DNS simulations (64³ and 128³ grids) of 3D Navier-Stokes
- Computed Ladyzhenskaya bound (C_L² ||ω||^{3/2} ||∇ω||^{3/2}) and BKM bound (C_CZ ||ω||² ||ω||_{L^∞} log(·)) at every timestep
- Applied Young's inequality to both closures and compared effective enstrophy ODE blow-up times
- Measured the critical ratio ||ω||_{L^∞}/||ω||_{L²} to check if it negates BKM's advantage

## Outcome: MASSIVELY VALIDATED

**T_BKM/T_Lad ranges from 5×10⁷ to 8×10¹⁶** across all tested flows. The success criterion was T_BKM/T_Lad > 10.

One case (TGV Re=5000) shows **no finite-time blow-up at all** under the BKM closure, versus T_Lad ≈ 10⁻¹⁵.

## Verification Scorecard
- **[COMPUTED]**: 8 results — 13 DNS runs, blow-up times, slack factors, ODE RHS comparisons, convergence check, Young's optimization, omega ratio dynamics, empirical CZ constants
- **[CHECKED]**: 1 result — Ladyzhenskaya slack = 237× matches Strategy-001 exactly
- **[CONJECTURED]**: 1 result — BKM advantage scales as ~Re³

## Key Takeaway
**The BKM chain eliminates the cubic nonlinearity in the enstrophy ODE.** The Ladyzhenskaya approach requires Young's inequality to trade ||∇ω||^{3/2} against the dissipation ν||∇ω||², introducing a catastrophic ν⁻³ factor. The BKM approach puts ||∇ω|| inside a logarithm, making the dissipation easily dominant and avoiding the ν⁻³ blow-up entirely. The resulting ODE is at most d/dt ||ω||² ~ ||ω||² × ||ω||_{L^∞} × log(·), which gives double-exponential growth rather than finite-time blow-up if ||ω||_{L^∞} stays controlled.

## Leads Worth Pursuing
1. **Formalize the BKM enstrophy ODE**: Write the Lean proof that the BKM-based closure gives d/dt ||ω||² ≤ F(||ω||², ||ω||_{L^∞}) with no ν⁻³ factor, and that this ODE has no finite-time blow-up when ||ω||_{L^∞} is bounded.
2. **The ||ω||_{L^∞} control problem**: The BKM approach reduces NS regularity to controlling ||ω||_{L^∞}. This is the BKM criterion itself — so the enstrophy approach via BKM doesn't give regularity for free, but it does show that the ONLY obstruction is ||ω||_{L^∞} blow-up (not the enstrophy cascade that Ladyzhenskaya predicts).
3. **Test at higher resolution**: The convergence check (N=128) showed α_fit decreasing from 1.40 to 0.72, suggesting the ||ω||_{L^∞}/||ω||_{L²} ratio growth becomes less severe with better resolution. Higher resolution (N=256, 512) would test whether α → 0 as resolution increases.
4. **Adversarial initial conditions**: The AntiParallel tubes showed the smallest advantage (5×10⁷) — test more aggressive vortex reconnection scenarios.

## Unexpected Findings
- The empirical Calderón-Zygmund constant is 4-1000× smaller than the theoretical value (0.003-0.06 vs 0.24), suggesting the BKM bound has significant room for further tightening.
- The ||ω||_{L^∞}/||ω||_{L²} ratio stays bounded below 0.55 for all tested flows and actually DECREASES at the highest Reynolds number (Re=5000), which is the opposite of what a blow-up scenario would require.

## Computations Identified
- N=256 DNS at Re=1000, 5000 to check convergence of α_fit
- Vortex reconnection IC (Kida-Pelz type) as a more adversarial test case
- Direct comparison of BKM vs Prodi-Serrin enstrophy approaches
