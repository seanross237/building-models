# Exploration 002 Summary — Two SED Oscillators: ZPF Correlations and Bell S

## Goal
Simulate two harmonic oscillators sharing the same ZPF realization (phase-shifted at separation d) and compute: position-position correlation C_xx(d), momentum-momentum correlation C_pp(d), and Bell-CHSH parameter S.

## What Was Tried
Ran N_traj=200 trajectories × N=100,000 steps each via Euler-Cromer integration of the ALD equation. ZPF generated in frequency domain; oscillator 2 receives phase shift e^{iωd/c}. Separations d = 0.0, 0.1, 1.0, 10.0 (in units c/ω₀). Analytical computation of C_xx(d) via numerical integration verified simulation. Bell-CHSH computed by threshold measurements on position samples with swept threshold settings.

## Outcome: Success

**Quantitative findings:**

| d | C_xx (sim) | C_xx = cos(ω₀d/c) | S_max | S > 2? |
|---|------------|---------------------|-------|--------|
| 0.0 | 1.0000 | 1.0000 | 2.000 | NO |
| 0.1 | 0.9948 | 0.9950 | 1.949 | NO |
| 1.0 | 0.5384 | 0.5400 | 1.092 | NO |
| 10.0 | -0.8328 | -0.8391 | 1.613 | NO |

Individual variances var_x ≈ 0.49–0.51, QM prediction = 0.500. Agreement within 2%.

## Verification Scorecard
- 2 VERIFIED (analytic formula confirmed by both computation and numerical integration)
- 4 COMPUTED (simulation results with code in `code/`)
- 2 CHECKED (C_xx formula confirmed analytically; prior art assessed)
- 1 CONJECTURED (novel claim about being first CHSH computation)

## Key Takeaway
**The shared ZPF creates position correlations C_xx(d) = cos(ω₀d/c) — oscillating with separation, not decaying — that are completely absent in QM for uncoupled oscillators.** These are classical common-cause correlations. The Bell-CHSH S ≤ 2 always: SED never violates the Bell bound. SED is a classical (non-quantum-nonlocal) theory for this system.

This appears to be the **first direct computation of Bell-CHSH from two SED oscillators sharing a ZPF realization.** Prior literature (de la Pena et al. 2010) claims structural entanglement in LSED but never computed Bell S.

## Leads Worth Pursuing
1. **3D ZPF model**: In 1D, C_xx oscillates without decay. In 3D with all k-vectors, would the correlation average to zero (recovering QM) or to the r⁻⁶ van der Waals term? This is the key gap.
2. **Optimal CHSH threshold search**: The d=10 case shows |C_xx| = 0.83 but S_max only 1.61 — could better threshold settings (beyond our 3-point grid) push S closer to 2?
3. **LSED entanglement claim**: De la Pena (2010) claims non-factorizable states for resonant oscillators. A direct Bell-CHSH computation in LSED formalism would test this claim.

## Proof Gaps
None (no formalization attempted).

## Unexpected Findings
- The negative correlation at d=10: C_xx = -0.83 ≈ cos(10). The correlation *anti-correlates* at large separation due to half-wavelength phase flip — NOT decay to zero as the GOAL description suggested.
- At d=0 (trivially correlated), CHSH saturates exactly at S=2.000 via degenerate settings (A'=B always), confirming the classical bound is tight.
- Boyer (2018) explicitly acknowledges SED is non-local (global ZPF phases) — undermining naive "local hidden variable" framing of SED.

## Computations Identified for Later
- 3D multi-mode ZPF model with all k-directions to check if C_xx decays as r⁻⁶
- Comparison of our classical C_xx with the LSED non-factorizable state formulation
