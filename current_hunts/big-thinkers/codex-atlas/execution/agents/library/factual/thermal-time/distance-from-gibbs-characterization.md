---
topic: Distance-from-Gibbs characterization — relative entropy vs. TTH discrepancy
confidence: verified
date: 2026-03-28
source: thermal-time/strategies/strategy-003/explorations/exploration-003/REPORT.md
---

## Summary

Systematic mapping of TTH discrepancy vs. relative entropy S(rho || rho_Gibbs) for two state families on coupled harmonic oscillators (lambda=0.3, beta=2.0, omega=1.0, N=20 Fock truncation). **Central finding: relative entropy does NOT determine TTH discrepancy.** At comparable S_rel (~0.05), squeezed states have 0% discrepancy while quench states have ~140%. The discriminant is whether the deformation preserves the Hamiltonian's eigenvalue spectrum.

## Setup

H_AB = (1/2)(p_A² + omega² q_A²) + (1/2)(p_B² + omega² q_B²) + lambda q_A q_B
Normal modes: omega_+ = sqrt(1.3) ~ 1.140, omega_- = sqrt(0.7) ~ 0.837

- **Family 1: Squeezed states** — Two-mode squeezing S(r) applied to Gibbs state, r in [0, 1.0] (11 points)
- **Family 2: Post-quench states** — Thermal state of H(lambda - delta_lambda), delta_lambda in [0, 0.5] (11 points)

Control check: Gibbs state (r=0 / delta_lambda=0) gives S_rel = 5.7e-14, discrepancy = 6.7e-13. **PASS.**

## Central Result: Two Families Do NOT Fall on the Same Curve

| Family   | Parameter             | S_rel  | Discrepancy |
|----------|-----------------------|--------|-------------|
| Quench   | delta_lambda = 0.05   | 0.0016 | 67.9%       |
| Quench   | delta_lambda = 0.10   | 0.0060 | 125.2%      |
| Squeezed | r = 0.1               | 0.0526 | 0.0%        |
| Quench   | delta_lambda = 0.50   | 0.1332 | 123.3%      |
| Squeezed | r = 0.2               | 0.2127 | 0.0%        |

At S_rel ~ 0.05, the squeezed state has 0.0% discrepancy while the quench state has ~144%. The quench family produces 100x larger discrepancy at 30x smaller relative entropy.

## Family 1: Squeezed States — Always Quantitative

All 11 points are QUANTITATIVE (correct frequencies, amplitude differences only). Maximum discrepancy 6.8% at r=1.0 (S_rel = 8.15). Disc ~ S_rel^0.70 (Pearson r = 0.93).

**Physics:** K_sq = S(beta H + logZ)S† has the same eigenvalue spectrum as beta H (unitarily equivalent). Modular flow under the rotated Hamiltonian: same frequencies, different amplitudes. The small discrepancy at large r is conjectured to be a Fock truncation artifact (N=20); should converge to zero in the continuum.

## Family 2: Post-Quench States — Immediate Structural Failure

Step-function transition: the smallest quench (delta_lambda = 0.05, S_rel = 0.0016) already produces 68% discrepancy. Saturates in the range 120-160% for all nonzero delta_lambda with no monotonic trend (Pearson r = 0.43 linear). The automated FFT classifier incorrectly labeled these as "QUANTITATIVE" due to coarse frequency tolerance (0.08); the correct physical classification is **STRUCTURAL** — modular flow generates dynamics under H', not H.

**Physics:** K_q = beta H' has a genuinely different spectrum from H. The frequency mismatch delta_omega * tau_max ~ 1 is satisfied even at the smallest quench for tau_max = 16pi, producing O(1) discrepancy regardless of how small delta_lambda is.

## The Discriminant: Spectrum Preservation

**[CONJECTURED]** TTH discrepancy is controlled not by distance-from-Gibbs but by the spectral distance between the modular Hamiltonian and the true Hamiltonian:

- **Unitary deformations** (squeezed): rho = S rho_Gibbs S†. Modular Hamiltonian K = S(beta H)S† has same spectrum as H. Modular flow generates dynamics under a rotated copy of H. Same frequencies, different amplitudes → **quantitative** discrepancy only, bounded by truncation, converges to zero in continuum.

- **Non-unitary deformations** (quench): rho = exp(-beta H')/Z with H' != H. Modular Hamiltonian K = beta H' has genuinely different spectrum. Modular flow generates dynamics under the wrong Hamiltonian. Different frequencies → **structural** discrepancy, O(1) immediately, step-function onset.

## Relative Entropy Ranges

The two families span very different S_rel ranges: squeezed [0, 8.15], quench [0, 0.13]. Quench S_rel scales as beta² delta_lambda² (second-order); squeezed S_rel scales as sinh²(r) (exponential growth).

## Significance

Extends the squeezed state contrast from nonequilibrium-tth-post-quench.md (single data point r=0.3, 7.8%) to a systematic 22-point survey establishing the discriminant as spectrum preservation, not relative entropy. This provides a clean theoretical prediction for when TTH fails structurally vs. quantitatively.
