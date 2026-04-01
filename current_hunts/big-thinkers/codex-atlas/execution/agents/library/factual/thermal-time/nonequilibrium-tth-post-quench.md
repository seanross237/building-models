---
topic: Non-equilibrium TTH test — post-quench and squeezed states
confidence: verified
date: 2026-03-28
source: thermal-time/strategies/strategy-002/explorations/exploration-002/REPORT.md
---

## Summary

Tests TTH for non-Gibbs states where modular flow genuinely differs from Hamiltonian evolution. Two coupled oscillators (omega=1.0, beta=2.0, N=20 Fock levels); post-quench state rho_0 = exp(-beta H_AB(0))/Z_0 (thermal state of UNCOUPLED system) used as initial state under COUPLED dynamics H_AB(lambda). **TTH generates the pre-quench dynamics, not the post-quench dynamics.** The discrepancy is structural (completely disjoint frequency content), not quantitative.

## Main Result: Post-Quench TTH Discrepancy

| lambda | ||dC_global||/||C_QM|| | ||dC_local||/||C_QM|| | Character |
|--------|------------------------|-----------------------|-----------|
| 0.00   | 0.000                  | 0.000                 | Control   |
| 0.10   | 0.096                  | 0.096                 | 9.6%      |
| 0.30   | 1.017                  | 1.017                 | 102%      |
| 0.50   | 1.745                  | 1.745                 | 174%      |

C_QM != C_global_TTH for all lambda > 0: TTH makes genuinely different predictions for non-Gibbs states.

## Structural Spectral Mismatch

FFT analysis (N_tau=2000, T=16pi, 8x zero-padding):

| Correlator | Frequencies (lambda=0.3)   | Physical origin              |
|------------|----------------------------|------------------------------|
| C_QM       | omega_+ = 1.140, omega_- = 0.843 | Coupled normal modes    |
| C_global   | omega = 1.000 (single)     | Uncoupled frequency          |
| C_local    | omega = 1.000 (single)     | Same (product state identity)|

**The frequency contents are completely disjoint.** C_QM oscillates at the coupled normal-mode frequencies; C_global oscillates at the uncoupled frequency. No parameter tuning can reconcile them — the spectral structures are topologically different. Asymptotic discrepancy -> sqrt(3) ~ 1.732 as T -> infinity. `[VERIFIED against exact analytical formulas to 3e-13 relative error]`

## Physical Interpretation: Modular Time = Pre-Quench Time

The modular Hamiltonian K = -log(rho_0) = beta*H_AB(0) encodes the state's PREPARATION history. Modular flow generates evolution under H_AB(0) — the pre-quench Hamiltonian. TTH's "thermal time" for this state IS the physical time of the system before the quench happened. The modular flow "remembers" the old Hamiltonian and is completely blind to the post-quench coupling.

## Product-State Identity: C_global = C_local (exactly)

**C_global_TTH = C_local_TTH to machine precision for the post-quench state.** This is because rho_0 = rho_A_thermal x rho_B_thermal is a product state. For product states, the B-sector of the global modular Hamiltonian (n_B terms) commutes with local A observables and cancels. This is a general identity: for ANY product state, global and local modular flows agree on local observables. For entangled states, they generically differ. `[VERIFIED]`

## Squeezed State Contrast

Squeezed state (S(r=0.3) applied to mode A of Gibbs state at lambda=0.3):

| Property | Post-quench (lambda=0.3) | Squeezed (lambda=0.3, r=0.3) |
|----------|--------------------------|-------------------------------|
| Global TTH discrepancy | 102% (structural)   | **7.8%** (quantitative)       |
| Local TTH discrepancy  | 102% (structural)   | **180%** (structural)         |
| C_global = C_local?    | Yes (product state)  | **No** (entangled state)      |
| Spectral character     | Wrong frequencies    | Correct frequencies, wrong amplitudes |

**Key contrast:** The squeezed state's global TTH shares the correct normal-mode frequencies with C_QM — only amplitudes differ (quantitative). The post-quench global TTH has completely wrong frequencies (structural). For entangled states, local TTH is WORSE (180%) because partial trace destroys entanglement information.

## Analytical Formulas (exact, verified)

- C_QM(t) = (2n_bar+1)/(4*omega) * [cos(omega_+ t) + cos(omega_- t)]
- C_global(t) = (2n_bar+1)/(2*omega) * cos(omega*t)
- n_bar = 1/(exp(beta*omega) - 1) = 0.1565; omega_+/- = sqrt(omega^2 +/- lambda)

Numerical-analytical agreement: < 3e-13 (lambda=0.1), < 8e-12 (lambda=0.3), < 6e-9 (lambda=0.5). Convergence: N=20 vs N=25 difference at machine precision for C_global; 3e-12 for C_QM.

## Adversarial Review (s003-E002)

**Novelty ratings:** Claim 1 (post-quench = pre-quench dynamics): 2.5/5 — algebraically expected (K = βH₀ is textbook), but explicit spectral computation, √3 asymptotic, and TTH framing are new. Closest prior art: Cardy-Tonni 2016/2018 compute K_A form after quenches but NOT correlator dynamics. Claim 2 (product-state identity): **1/5 — known result** (Takesaki Vol. II Theorem IX.4.2). Claim 4 (squeezed state contrast): 3/5 — novel taxonomy, single data point. Central interpretation ("preparation-history time"): **4/5 — novel**, not found in Connes-Rovelli, Rovelli later papers, Swanson 2020, Chua 2024, or Paetz thesis. See `tth-adversarial-claims-assessment.md` for full adversarial review.

## Extended: Distance-from-Gibbs Characterization (S003-E003)

The single squeezed data point above (r=0.3, 7.8%) has been extended to a systematic 22-point survey in `distance-from-gibbs-characterization.md`. Key extension: relative entropy does NOT determine TTH discrepancy — at comparable S_rel (~0.05), squeezed states have 0% while quench states have ~140%. The discriminant is spectrum preservation (unitary vs. non-unitary deformation of the Gibbs state).

## Significance

This is the first direct test of TTH for a non-equilibrium state with exact analytical verification. The result reveals a fundamental asymmetry in TTH: for equilibrium (Gibbs) states, K = beta*H so TTH = QM trivially. For non-equilibrium states, K encodes the preparation Hamiltonian, and TTH generates dynamics corresponding to the state's history — not the actual post-quench dynamics. Whether this is a bug or a feature depends on TTH interpretation: if TTH claims modular time IS physical time, this is a failure; if TTH claims modular time is state-determined time (which may differ from Hamiltonian time), the result precisely characterizes the nature of that difference.
