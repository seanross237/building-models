---
topic: Excited-state modular flow — state-dependent time with structural frequency mismatch
confidence: verified
date: 2026-03-28
source: thermal-time/strategies/strategy-002/explorations/exploration-003/REPORT.md, thermal-time/strategies/strategy-003/explorations/exploration-001/REPORT.md
---

## Summary

Tests TTH for a one-particle excitation |1_m> = b_m^+ |0> of a free scalar field on an N-site lattice. Uses Gaussian approximation for the modular Hamiltonian (exact two-point functions, quadratic K_R). **The modular "clock" ticks at entanglement spectrum frequencies, not physical mode frequencies.** The target physical frequency is ABSENT from the modular flow response. The discrepancy GROWS in the continuum limit (delta_disc ~ N^{+0.33} for fixed physical frequency).

## Setup

- Free massless scalar field on N-site lattice, Dirichlet BC
- Right half-lattice (n_R = N/2) as subsystem (lattice Rindler analogue)
- Williamson decomposition for bosonic modular Hamiltonian
- Exact two-point corrections: X^(1) = X^(0) + u_m u_m^T / omega_m (from Wick's theorem)
- Gaussian approximation: constructs quadratic K_R from modified covariance matrices
- N = 20, 30, 50, 80, 100, 150, 200

## Key Result: Structural Spectral Mismatch

FFT analysis at N=100, mode 0:
- **delta_C_full**: clean peak at physical frequency f = omega_m/(2pi) = 0.005, amplitude 0.632
- **delta_C_local**: amplitude at target frequency = 0.00005 (ratio 0.0001!)
- **delta_C_local dominant peaks**: f = 0.021, 0.041, 0.157 — at MODULAR frequencies, not physical

The modular flow oscillates at modular energies eps_k/(2pi), which are determined by the entanglement spectrum. The physical mode frequency omega_m is simply absent from the modular response. This parallels the E002 post-quench finding: modular time tracks entanglement structure, not physical dynamics.

## Convergence: Discrepancy GROWS in Continuum Limit

Fixed physical frequency (omega ~ 0.3) convergence:

| N   | mode | omega | delta_disc | max|dC_loc| | max|dC_full| |
|-----|------|-------|------------|-------------|---------------|
| 30  | 2    | 0.303 | 4.17       | 0.701       | 0.112         |
| 50  | 4    | 0.307 | 5.44       | 0.682       | 0.066         |
| 100 | 9    | 0.310 | 9.96       | 0.498       | 0.032         |
| 150 | 13   | 0.290 | 12.60      | 0.392       | 0.020         |

**Power-law: delta_disc ~ N^{+0.33}.** Physical correction shrinks as max|dC_full| ~ 1/N (mode function at probe decays), while modular flow response shrinks SLOWER, so the relative discrepancy grows without bound.

### Mode-0 Convergence is an ARTIFACT

Mode 0 shows apparent convergence delta_disc ~ N^{-0.46}, but this is misleading: omega_0 = pi/(N+1) -> 0 as N -> infinity, making delta_C_full -> constant (no oscillation). The L2 metric then measures only the DC offset, not the frequency content. The correct test uses fixed physical frequency, which shows growing discrepancy.

## Modular Hamiltonian Perturbation

| N   | ||delta h_phi|| / ||h_phi|| | ||delta h_pi|| / ||h_pi|| |
|-----|---------------------------|-------------------------|
| 50  | 3.1%                      | 29.3%                   |
| 100 | 1.6%                      | 30.4%                   |
| 200 | 0.8%                      | 30.2%                   |

The phi-coupling perturbation vanishes as ~1/N; the pi-coupling perturbation persists at ~30% — a large, persistent effect from the excitation on the momentum sector.

## Multi-Mode Comparison (N=50)

Low-frequency modes give smallest delta_disc; high-frequency modes give largest — consistent with the IR artifact: low omega_m -> nearly constant delta_C_full -> artificially small relative discrepancy.

## Gaussian Approximation Caveat — RESOLVED

The one-particle state is non-Gaussian. The Gaussian approximation constructs a QUADRATIC modular Hamiltonian (true K_R is non-quadratic), with linear (symplectic) modular flow. Non-Gaussian corrections (cubic+ terms in K_R) could in principle modify the spectral content.

**RESOLVED (s003-E001):** A squeezed vacuum state — which IS Gaussian, giving an EXACT modular Hamiltonian — shows the identical structural mismatch: modular flow at modular frequencies, physical frequency absent, discrepancy growing as N^{0.44} in the continuum limit (vs. N^{0.33} for one-particle). The mismatch is a genuine feature, not a Gaussian approximation artifact. See `gaussian-caveat-resolution.md` for full details.

## Comparison with E002 (Non-Equilibrium TTH)

| Feature | E002 (post-quench) | E003 (excited state) |
|---------|-------------------|---------------------|
| Physical freqs | omega_+/- (normal modes) | omega_m (excited mode) |
| Modular freqs | omega (uncoupled) | eps_k/(2pi) (entanglement) |
| Spectral match | NO (structural) | NO (structural) |
| Grows with N? | N/A (fixed system) | YES (~N^{+0.33}) |
| Nature | "Modular time = pre-quench time" | "Modular clock ticks at entanglement frequencies" |

Both show the same pattern: modular time tracks entanglement structure, not physical dynamics. For the vacuum (BW theorem), K_R happens to be the boost generator — this is SPECIAL to the vacuum. For excited states, K_R is no longer geometric.

## Adversarial Review (s003-E002)

**Novelty rating: 4/5 — strongest claim.** Closest prior art: **Lashkari-Liu-Rajagopal 2021** (arXiv:1811.05052) — computes modular flow operators for excited states (coherent/squeezed in GFF) but does NOT compare correlator dynamics to physical time evolution. The zero spectral weight quantification, N^{0.33–0.44} continuum divergence, and TTH test framing are genuinely new. All three conceptual attacks fail or are weakened for this claim: (1) TTH IS defined for all faithful states; (2) in the Rindler test case, the observer is fixed and TTH gives the wrong answer; (3) growing discrepancy with N makes the lattice type-I objection worse, not better. See `tth-adversarial-claims-assessment.md` for full adversarial review.

## Verification Status

- [VERIFIED]: Two-point corrections (analytical + numerical), equal-time check to machine precision, Williamson reconstruction < 4e-15
- [COMPUTED]: All convergence tables, spectral analysis, modular Hamiltonian perturbation, multi-mode comparison
- [VERIFIED]: Gaussian caveat RESOLVED — squeezed vacuum (exact K_R) reproduces same mismatch (s003-E001)
- [VERIFIED]: Adversarial review (s003-E002) — survives all three attacks, novelty 4/5
- [CONJECTURED]: Physical interpretation (modular clock = entanglement frequencies)
