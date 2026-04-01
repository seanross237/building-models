# Exploration 001 Summary: Gaussian Caveat Resolution

## Goal
Resolve the Gaussian approximation caveat on Claim 3 by testing modular flow for coherent and squeezed states (Gaussian-exact modular Hamiltonian) on the Rindler lattice.

## Outcome: SUCCESS — Caveat resolved, Claim 3 confirmed

**Part A (Coherent state):** delta_C_local = mu_k^2 = constant to machine precision (std < 10^{-17}). delta_C_full oscillates at omega_m. Analytical predictions verified exactly. This validates the computational pipeline. [VERIFIED]

**Part B (Squeezed state — the critical test):** For the squeezed vacuum (Gaussian, exact modular Hamiltonian), delta_C_local oscillates at modular frequencies epsilon_k/(2*pi), NOT at the physical frequency omega_m. The discrepancy ||delta_C_local - delta_C_full||/||delta_C_full|| = 5.7 (N=50), 7.4 (N=100), 7.9 (N=200). The amplitude of delta_C_local is 10-16x larger than delta_C_full, dominated by wrong-frequency oscillations. [COMPUTED]

**Part C (Convergence):** At fixed physical frequency omega ≈ 0.3, the discrepancy grows as N^{0.44} from N=50 to N=400. The amplitude ratio grows as N^{0.41}. The mismatch worsens in the continuum limit, consistent with the N^{0.33} scaling from the one-particle case. [COMPUTED]

**Part D (Squeeze sweep):** Discrepancy is large (13-66x) for all squeezing parameters r = 0.1 to 1.0. Not a small-perturbation artifact. [COMPUTED]

## Verification Scorecard
- **VERIFIED:** 6 (coherent state analytics, vacuum controls, C_full formulas)
- **COMPUTED:** 12 (all squeezed state results, convergence scaling, parameter sweep)
- **CONJECTURED:** 0

## Key Takeaway
The structural mismatch between modular flow and physical time evolution persists for Gaussian-exact states. The Gaussian approximation caveat is NOT the issue. Claim 3 stands without qualification: modular flow produces wrong frequencies for non-vacuum states, with discrepancy growing in the continuum limit.

## Unexpected Findings
- The convergence exponent (~0.44) is slightly larger than the one-particle case (~0.33), suggesting the mismatch may be even stronger for squeezed states.
- The modular flow response amplitude is roughly constant (~0.1) regardless of squeezing strength, while the physical response scales with (e^{-2r}-1). This means the relative discrepancy diverges as r → 0.

## Proof Gaps
None — this was a computational exploration. All results are numerical, reproducible from code in `code/`.

## Computations for Future Work
- Test thermal (mixed) Gaussian states to check if temperature affects the mismatch
- Extend to massive scalar field to see if the mass gap changes the scaling exponent
- Compare the squeezed-state modular spectrum shift to the one-particle Gaussian-approximation shift quantitatively
