# Exploration 002 Summary: BH Universal Constants — Literature Verification

## Goal
Systematically search BH thermodynamics literature (≥15 papers) to determine whether three universal constants derived in strategy-001 have been previously published:
1. S_Hawking(r_s sphere) = 1/(540 ln2) ≈ 0.002672 bits
2. ⟨N_photons⟩ = ζ(3)/(24π⁴) ≈ 5.14 × 10⁻⁴
3. Classicality horizon R_1bit = (540 ln2)^{1/3} × r_s ≈ 7.21 r_s

## What Was Tried
- Ran all 11 required search queries; searched for "1/(540 ln 2)", "540" in BH context, "zeta(3) Hawking photon count", "classicality horizon black hole", "7.21 Schwarzschild radius"
- Checked 18 specific papers including: Hawking 1975, Page 1976/1977, Unruh 1976, Bekenstein 1973, Gray et al. 2016, Giddings 2016a/b, arXiv:2407.21114, Kim 2112.01931, Preskill 1992, Visser 2015/2017, and standard textbooks (Wald, Birrell-Davies, Frolov-Novikov, Mukhanov-Winitzki, Susskind-Lindesay)
- Accessed full HTML content of 8 papers via ar5iv

## Outcome: NOT PUBLISHED

All three constants are unpublished. Specific search for "1/(540 ln 2)" returns ZERO results. Specific search for "7.21 Schwarzschild radius" returns ZERO results.

**Verdict per constant:**
- S = 1/(540 ln2): **NOT PUBLISHED.** The number never appears in literature.
- ⟨N⟩ = ζ(3)/(24π⁴): **NOT PUBLISHED.** Gray et al. (2016) use ζ(3) for emission RATES through the horizon, not near-horizon sphere OCCUPATION NUMBER.
- R_1bit = 7.21 r_s: **NOT PUBLISHED.** The "classicality horizon" concept does not appear in BH literature.
- T_H × r_s = ħc/(4πk_B): **IMPLICITLY KNOWN, NOT NAMED.** Every BH paper contains this implicitly, but no paper isolates it as a named universal constant or uses it as a starting point.

## Key Takeaway
These constants represent an **overlooked 5-line calculation from fully known ingredients**. The physics (Stefan-Boltzmann, photon gas statistics, T_H formula, r_s formula) has been known since 1975–1976. The novelty is simply the observation that T_H × r_s is a universal constant, and using it to evaluate the blackbody formulas at the horizon scale.

## Leads Worth Pursuing
- **Kim (arXiv:2112.01931):** Most closely related paper — computes entropy of Hawking radiation in a spherical box near the BH, but using the curved-space stress tensor (not naive flat-space blackbody) and with box radius R ≥ 3r_s. The relationship between the "naive" 1/(540 ln2) result and the curved-space calculation should be investigated.
- **Gray et al. (arXiv:1506.03975):** Uses ζ(3) in the emission rate formula Γ ∝ ζ(3)(k_BT_H/ħc)³ A_H, which is closely related to our ⟨N⟩ formula. The two differ by a geometric factor and use (area flux vs volume count). This paper should be cited as the closest prior work.
- **arXiv:2407.21114:** Shows T = 1/(4πr_+) explicitly in natural units — should be cited as establishing the T_H × r_s identity.

## Unexpected Findings
- The constant 1/540 = 1/(9×60) emerges cleanly from a cancellation: σ = π²k_B⁴/(60ħ³c²) provides the 60, and the geometric factor (16/3)×(4π/3)/(64π³)×π² provides the 1/9. All π factors cancel exactly. This algebraic clarity makes the result surprising that it went unnoticed.
- The Giddings atmospheric radius R_a ≈ 2.68 r_s (from Stefan-Boltzmann luminosity matching) is distinct from the R_1bit = 7.21 r_s (from entropy accumulation). These are different physical scales with different meanings — neither has been connected to quantum Darwinism redundancy.
- Gray et al.'s thermal wavelength λ_thermal = 8π² r_H ≈ 79 r_H implicitly uses the T_H × r_s identity, suggesting this identity is "in the air" in the sparsity literature but never extracted.

## Computations Identified
None beyond what was already done — the three constants are now verified analytically and numerically. The computation that would be valuable is a **curved-space correction** to 1/(540 ln2): using the actual Hawking radiation stress-energy tensor (Page's tensor) instead of the naive flat-space blackbody gives a different coefficient near the horizon (the local temperature diverges at the horizon). Roughly a 50-100 line scipy script could estimate the correction factor by numerically integrating Page's tensor over the sphere of radius r_s.
