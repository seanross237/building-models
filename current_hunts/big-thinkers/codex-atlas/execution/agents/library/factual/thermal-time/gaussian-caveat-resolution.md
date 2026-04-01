---
topic: Gaussian caveat resolved — squeezed vacuum confirms structural frequency mismatch
confidence: verified
date: 2026-03-28
source: thermal-time/strategies/strategy-003/explorations/exploration-001/REPORT.md
---

## Summary

Resolves the critical Gaussian approximation caveat on the excited-state modular flow finding (see `excited-state-modular-flow.md`). Tests two Gaussian states — coherent and squeezed vacuum — where the Williamson decomposition gives the EXACT modular Hamiltonian with no approximation. **The squeezed vacuum reproduces the same structural mismatch: modular flow oscillates at modular frequencies, NOT the physical mode frequency.** Discrepancy grows as N^{0.44} in the continuum limit. The Gaussian caveat does NOT matter.

## Coherent State Control [VERIFIED]

Coherent state |alpha> = D_m(alpha)|0> has covariance matrix identical to vacuum (X_R^{(alpha)} = X_R^{(0)}, P_R^{(alpha)} = P_R^{(0)}). Therefore:

- **delta_C_local(tau) = mu_k^2 = constant** (no tau-dependence) — confirmed to machine precision (std < 10^{-17})
- **delta_C_full(tau) = mu_k^2 * cos(omega_m * tau)** — FFT peak correctly at omega_m
- All errors at 10^{-16} to 10^{-17} across N = 50, 100, 200

Validates the computational pipeline: modular flow correctly "ignores" the coherent displacement.

## Squeezed Vacuum Test — Main Result [COMPUTED]

Single-mode squeezed vacuum S_m(r)|0> modifies covariance matrices by a rank-1 correction. **Crucially, this state IS Gaussian** — the Williamson decomposition gives the EXACT modular Hamiltonian.

Parameters: r = 0.5, mode m = N//4, optimal probe site (max |U[k,m]| in right sublattice).

| N   | omega_m | Discrepancy (L2 rel.) | Amp ratio | Recon err |
|-----|---------|----------------------|-----------|-----------|
| 50  | 0.780   | 5.74                 | 10.4x     | 2.50e-15  |
| 100 | 0.787   | 7.38                 | 11.7x     | 1.31e-14  |
| 200 | 0.776   | 7.94                 | 15.9x     | 5.05e-15  |

FFT analysis: delta_C_local dominant peaks at modular frequencies (5.6, 0.5, 4.9, 3.2 at N=50) — **no significant weight at omega_m**. Physical response delta_C_full verified analytically to machine precision at all N.

## Convergence: Discrepancy Grows in Continuum Limit [COMPUTED]

Fixed physical frequency omega_m ~ 0.3, r = 0.5, optimal probe:

| N   | omega_m  | Discrepancy | Amp ratio |
|-----|----------|------------|-----------|
| 50  | 0.307    | 5.49       | 8.63x     |
| 100 | 0.310    | 7.29       | 12.5x     |
| 200 | 0.296    | 8.38       | 16.5x     |
| 400 | 0.297    | 14.39      | 20.2x     |

**Power-law: Discrepancy ~ N^{0.44}, Amplitude ratio ~ N^{0.41}.** Consistent with the N^{0.33} scaling for the one-particle state. Different exponent (~0.4 vs ~0.3) likely reflects squeezed vs. one-particle excitation nature; qualitative behavior identical.

## Squeezing Parameter Sweep [COMPUTED]

N = 100, mode = 25, r from 0.1 to 1.0: Discrepancy ranges from 13 (r=1.0) to 66 (r=0.1). Larger at small r because delta_C_local retains modular-frequency oscillations of constant amplitude (~0.1) while delta_C_full shrinks as (e^{-2r}-1) → 0. The mismatch is structural, independent of squeezing strength.

## Modular Energy Shifts [COMPUTED]

Squeezing modifies modular energies by up to |delta_eps| ~ 5.9 (L2 shift / L2 vac ~ 3–8%). The perturbation affects intermediate modes most, but the modular flow still oscillates at these shifted modular frequencies, not the physical frequency.

## Physical Interpretation

The modular Hamiltonian K_R of the half-lattice vacuum is the Lorentz boost generator (BW theorem). For non-vacuum states, K_R changes (different Williamson normal form), generating a "generalized boost" — structurally different from time translation. No state-dependent perturbation within the Gaussian family can reconcile modular flow with physical evolution. The modular and physical Hamiltonians generate fundamentally different symmetries (boost vs. translation).

## Verdict

**Claim 3 (excited-state modular flow mismatch) is CONFIRMED with no Gaussian approximation caveat.** The structural mismatch between modular flow and physical time evolution is a genuine feature of non-vacuum states on a half-lattice partition, not an artifact of approximating the modular Hamiltonian.
