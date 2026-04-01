# Exploration 003 Summary — Excited-State Modular Flow

## Goal
Test TTH's state-dependent time prediction: for a one-particle excitation |1_m> = b_m^+ |0> on a lattice scalar field, does the modular flow correlator C_local^(1) match the physical Hamiltonian correlator C_full^(1)?

## What Was Tried
- Computed vacuum and excited-state modular Hamiltonians via Williamson decomposition (Gaussian approximation) for N = 20-200 sites
- Compared modular flow correlators vs physical correlators for multiple probe sites and modes
- High-resolution spectral analysis (FFT) of the response delta_C = C^(1) - C^(0)
- Convergence study with both mode 0 (omega → 0) and fixed frequency (omega ≈ 0.3)

## Outcome: STRONG SUCCESS

**TTH predicts structural state-dependent time for excited states.** The modular flow response to a one-particle excitation has **completely wrong frequency content** compared to the physical response:

1. **delta_C_full** is a clean cosine at the physical frequency omega_m — a single spectral peak `[VERIFIED]`
2. **delta_C_local** has NO power at omega_m. Its dominant frequencies are modular frequencies eps_k/(2pi), completely unrelated to the physical mode frequency `[COMPUTED]`
3. At N=100, the amplitude of delta_C_local at the target physical frequency is **0.01% of delta_C_full** — effectively zero
4. The discrepancy **GROWS in the continuum limit** (delta_disc ~ N^{+0.33} for fixed physical frequency), not shrinks

## Verification Scorecard
- **[VERIFIED]**: 3 claims (two-point corrections, equal-time check, reconstruction error)
- **[COMPUTED]**: 12 claims (all convergence data, spectral analysis, amplitude ratios, multi-mode comparison)
- **[CONJECTURED]**: 2 claims (non-Gaussian corrections, physical interpretation)

## Key Takeaway
**The modular "clock" ticks at entanglement frequencies, not physical frequencies.** The modular Hamiltonian encodes the entanglement structure of the reduced state, which has its own spectrum unrelated to the physical Hamiltonian spectrum. When the state changes, the entanglement spectrum shifts, producing modular flow dynamics at modular frequencies — not at the physical mode frequency that characterizes the excitation. This is a structural, not quantitative, failure of TTH to match physical dynamics for non-vacuum states.

This directly parallels Exploration 002's finding: modular time tracks the entanglement structure (or the preparation history), not the physical dynamics.

## Proof Gaps Identified
- **Gaussian approximation**: The one-particle state is non-Gaussian. The true modular Hamiltonian is non-quadratic. The non-Gaussian corrections would add nonlinear terms to the modular flow. However, the structural mismatch (wrong frequencies entirely) makes it very unlikely that these corrections would restore the correct physical frequency.
- **Continuum limit**: All computations are on a finite lattice. The BW theorem only applies in the continuum. A rigorous continuum treatment (using Araki's perturbation theory for modular operators) would be needed to make definitive statements.

## Unexpected Findings
1. **Mode-0 convergence is an illusion**: The apparent N^{-0.47} convergence of delta_disc for mode 0 is entirely due to the physical frequency omega_0 → 0 making delta_C_full → constant. For fixed physical frequency, the discrepancy GROWS with N.
2. **Momentum sector amplification**: The perturbation to the pi-coupling of the modular Hamiltonian persists at ~30% even as N → ∞, while the phi-coupling perturbation vanishes as 1/N. The entanglement structure is strongly sensitive to excitations through the momentum sector.
3. **Modular flow overreaction**: max|delta_C_local| is 1.5-14× larger than max|delta_C_full|. The modular Hamiltonian amplifies the effect of the excitation.

## Computations Identified
- Verify the Gaussian approximation with direct Fock-space computation at small N (N=8-10)
- Use Araki's perturbation formula for the exact first-order correction to the modular Hamiltonian (bypassing the Gaussian approximation)
- Test with COHERENT state excitations (Gaussian states!) where the Gaussian modular Hamiltonian is exact, to isolate the effect of the Gaussian approximation
- Test higher-particle excitations (|2_m>, etc.) to see if the structural mismatch persists
