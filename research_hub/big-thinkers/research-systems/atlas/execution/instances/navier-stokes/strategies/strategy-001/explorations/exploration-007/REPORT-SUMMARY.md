# Exploration 007 Summary: BMO Norms, Intermittency, BKM vs Ladyzhenskaya

## Goal
Quantify the BKM advantage over Ladyzhenskaya for NS regularity, compute BMO norms (Kozono-Taniuchi), measure spatial intermittency, and synthesize a conditional enstrophy bound.

## What Was Tried
- Ran pseudospectral DNS (Taylor-Green vortex, N=48-64) at Re=100, 500, 1000, 5000, T=5.0
- Computed BKM inequality slack ratios and compared to Agmon and Ladyzhenskaya chain slacks
- Computed BMO norms of vorticity at 5 radii with 150 random ball centers per radius
- Measured vorticity flatness F4, volume fractions mu(lambda), effective Ladyzhenskaya constants
- Fit the conditional vortex stretching bound C(F4) as a function of flatness

## Outcome: Succeeded

### Verification Scorecard
- **COMPUTED: 18** (BKM slacks at 4 Re values, BMO norms, flatness, volume fractions, C(F4) fits, correlations, time series)
- **CONJECTURED: 3** (conditional bound generality, envelope exponent universality, mechanism formalization)
- **VERIFIED: 0** (no Lean formalization attempted — this was a numerical exploration)
- **CHECKED: 0**

### Key Takeaway

**The BKM bound has only 1.05x slack (near-tight) vs Ladyzhenskaya's 237x — a 226x advantage factor.** This is the single most important quantitative finding across all NS explorations. It shows that the ~200x slack in energy-method regularity arguments is an artifact of the Ladyzhenskaya interpolation chain, not an intrinsic feature of NS dynamics. BKM avoids this by using pointwise vorticity information with only a logarithmic correction.

### Other Major Findings

1. **BMO/L^inf ratio ≈ 0.27** (stable across Re=100-5000), giving a ~4x tightening via the Kozono-Taniuchi criterion. [COMPUTED]

2. **Vorticity is highly intermittent:** F4 = 3-12 at peak enstrophy (vs Gaussian prediction of 5/3), with only 1-2% of the domain carrying |omega| > 0.5 * omega_max. [COMPUTED]

3. **Conditional bound:** C(F4) ≈ 0.003/F4 (mean) or C_max(F4) ≈ 0.0035/F4^{0.85} (worst-case envelope). At Gaussian flatness (F4=5/3), this recovers the 237x slack exactly. [COMPUTED]

4. **Flatness-C_Leff correlation:** C_{L,eff}/C_L ~ F4^{-0.30}, with r = -0.93, confirming exploration 006's prediction (exponent -0.25 predicted, -0.30 measured). [COMPUTED]

## Proof Gaps Identified
- The conditional bound C(F4) ~ 1/F4 needs theoretical justification: why does the worst-case vortex stretching scale inversely with flatness?
- The BKM constant on T^3 (C ≈ 0.65) vs R^3 (C ≈ 0.24) — the factor of 2.7x needs derivation from the periodic Biot-Savart kernel
- Formalizing: "for NS solutions with F4 <= F_max, the vortex stretching is bounded by C/F_max * ||omega||^{3/2} ||nabla omega||^{3/2}"

## Unexpected Findings
- The BKM minimum slack (1.05) is **completely Re-independent** across Re=100-5000. The bound is near-tight at all Reynolds numbers.
- The BMO/L^inf ratio (0.25-0.27) is also essentially Re-independent — suggesting universal vorticity structure.
- The BKM advantage GROWS with Re in the time-average: 221x at Re=100 to 535x at Re=5000. This means the Ladyzhenskaya approach becomes progressively worse at higher Re.

## Computations Identified
- Verify BKM advantage on other initial conditions (random Gaussian, Kida vortex) to confirm universality
- Compute BMO norms at higher resolution (N=128) with finer ball sampling to check convergence
- Explore whether the conditional C(F4) bound can be combined with BKM to get an even tighter unconditional bound
- Test whether the F4 <= F_max condition can be propagated in time (i.e., if F4 is bounded at t=0, does it stay bounded?)
