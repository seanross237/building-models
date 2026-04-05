# Exploration 002 Summary: Computational Slack Measurement

## Goal
Build measurement infrastructure for 8 key NS regularity inequalities and run first measurements on the Taylor-Green vortex at Re = 100, 500, 1000, 5000.

## Outcome: SUCCESS

All 8 inequality pairs implemented, validated, and measured at 4 Reynolds numbers with N=128 convergence check.

## Verification Scorecard
- **VERIFIED**: 4 claims (norm accuracy, div-free identity, energy conservation, ||S||=||ω||/√2 identity)
- **COMPUTED**: 9 claims (all slack ratios at 4 Re values, vortex stretching 3-factor decomposition)
- **CHECKED**: 8 claims (N=128 convergence confirmed all min slacks to < 0.7%)
- **CONJECTURED**: 0 claims (former conjecture on √2 factor now verified)

## Key Takeaway

**The vortex stretching bound (E2/E3) has 237× minimum slack — it's the bottleneck by a factor of 55×.** The actual vortex stretching integral is less than 0.5% of what the bound permits. This massive gap decomposes exactly into three multiplicative factors: **Ladyzhenskaya applied to vorticity (~31×)**, Hölder alignment loss (~5.4×), and the strain/vorticity norm √2 factor (1.414×). The dominant factor is NOT the geometric alignment but the **Ladyzhenskaya constant on ω** — vorticity is more spread in Fourier space than velocity, making the interpolation 7× looser for ω than for u.

## Slack Atlas (Min Slack Across All Re)

| Rank | Inequality | Min Slack | Status |
|---|---|---|---|
| 1 (loosest) | E2/E3: Vortex Stretching | **237×** | Grows ∝ Re^{0.28} |
| 2 | R1/F2: Prodi-Serrin | 31× | Stable |
| 3 | E4: Kato-Ponce | 25× | Grows ∝ Re^{0.16} |
| 4 | F4+G1: Agmon | 12× | Grows ∝ Re^{0.14} |
| 5 | F5: CZ Pressure | 7.8× | Stable |
| 6 | F3: Sobolev H¹→L⁶ | 4.5× | Stable |
| 7 | F1: Ladyzhenskaya | 4.3× | Stable |
| 8 (tightest) | E1: Energy | 1.0× | Exact |

## Leads Worth Pursuing

1. **Tighten Ladyzhenskaya for vorticity** (most impactful): The 31× loss from applying Ladyzhenskaya to ω (vs 4.3× for u) is the dominant bottleneck factor. Computing the sharp Ladyzhenskaya constant for fields of the form ω = ∇×u with div-free u would exploit NS-specific structure. Even a 3× improvement would cut total slack from 237× to ~23×.

2. **Geometric vortex stretching bound**: The 5.4× Hölder alignment loss comes from ignoring ω-strain alignment. A bound using the Constantin-Fefferman vorticity direction regularity could reduce this.

3. **Higher Re turbulent regime**: All current measurements are in the laminar-transitional regime (enstrophy still growing at T=5). Running to the turbulent cascade phase (T=10-20 at Re=1000-5000 with N=256+) would test whether the slack structure changes qualitatively in fully developed turbulence.

## Unexpected Findings

- **Min slack is Re-independent for all functional inequalities** (F1, F3, F5): The minimum occurs at early time (t ≈ 0-1.4) when the flow retains TGV symmetry. This suggests the minimum slack is determined by the initial condition geometry, not the dynamics.

- **Ladyzhenskaya is 7× looser for ω than for u**: The Ladyzhenskaya constant applied to vorticity gives 31× slack vs 4.3× for velocity. This is because vorticity has significant energy at higher wavenumbers (it's a derivative of velocity), making the L⁴ interpolation between L² and H¹ much less efficient. This is the dominant bottleneck factor — not the Hölder alignment loss as previously estimated.

- **The Prodi-Serrin bound's exponents** (||u||_{L²}^{1/4} ||u||_{H¹}^{7/4}) may not be derivable from a standard Hölder + GNS chain in 3D — the standard derivation gives different Sobolev regularity requirements. The 31× slack may partly reflect using a non-optimal interpolation.

## Computations for Later

- **Sharp Ladyzhenskaya constant for vorticity fields ω = ∇×u** — this is the most impactful computation: what is the best C in ||ω||_{L⁴} ≤ C||ω||_{L²}^{1/4}||∇ω||_{L²}^{3/4} when ω is constrained to be a curl of a div-free field?
- N=256, Re=1000-5000 simulations to T=15 (turbulent regime)
- Test whether ABC flows or Kida vortex produce tighter slack ratios
- Compute ||ω||_{L⁴} empirical constant for each wavenumber shell to identify which scales contribute most to the Ladyzhenskaya gap
