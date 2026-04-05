# Exploration 002 Summary — Non-Equilibrium TTH Test

## Goal
Test TTH for a post-quench state (thermal state of uncoupled system, not Gibbs of coupled H) and determine whether modular time makes physically meaningful predictions for non-equilibrium states.

## What Was Tried
- Computed C_QM, C_global_TTH, and C_local_TTH for post-quench state at lambda = 0.0, 0.1, 0.2, 0.3, 0.5
- Validated with Gibbs-state control checks, uncoupled control, convergence checks (N=15/20/25)
- High-resolution FFT spectral analysis (N=2000 pts, 16pi window, 8x zero-padding)
- Verified results against exact analytical formulas
- Tested a second non-equilibrium state: squeezed thermal state (r=0.3)

## Outcome: SUCCESS

**TTH makes genuinely different predictions for non-Gibbs states**, with large, growing, *structural* discrepancies:

| lambda | ||C_QM - C_global|| / ||C_QM|| | Nature of discrepancy |
|--------|--------------------------------|-----------------------|
| 0.1    | 9.6%                           | Structural (different frequencies) |
| 0.3    | 102%                           | Structural |
| 0.5    | 175%                           | Structural |

The discrepancy is **structural, not quantitative**: C_QM has normal-mode frequencies omega_± = sqrt(omega^2 ± lambda), while C_global_TTH has only the uncoupled frequency omega = 1.0. The spectral contents are completely disjoint.

## Verification Scorecard
- **[VERIFIED]**: 4 claims (Gibbs control, analytical formula match, product-state identity, C_QM ≠ C_global for lambda>0)
- **[COMPUTED]**: 8 claims (discrepancy table, FFT analysis, convergence, squeezed state, comparison tables, beat periods, asymptotic limit)
- **[CONJECTURED]**: 1 claim (physical interpretation of modular time as "preparation-history time")

## Key Takeaway
**Modular time = pre-quench time.** The TTH modular flow for the post-quench state generates evolution under the *pre-quench* Hamiltonian H_AB(0), completely ignoring the post-quench coupling. The correlator has the wrong frequencies (uncoupled omega instead of normal modes omega_±), misses the characteristic beating pattern, and the discrepancy grows to sqrt(3) ≈ 1.73 asymptotically. This is not a subtle quantitative disagreement — it is a qualitative failure of modular time to track physical time after a quench.

## Unexpected Findings
1. **C_global = C_local exactly for the post-quench state** (product-state identity). Because rho_0 = rho_A ⊗ rho_B, the B-mode part of the modular Hamiltonian commutes with x_A and drops out. For entangled non-Gibbs states (squeezed test), this identity breaks.

2. **Squeezed state has much smaller global TTH discrepancy** (7.8% vs 102% at same lambda=0.3). The squeezed state's modular flow has the *correct normal-mode frequencies* but slightly wrong amplitudes — a quantitative discrepancy, not structural. The local TTH discrepancy is much worse (180%), showing entanglement information matters.

## Leads Worth Pursuing
- The squeezed state result suggests a hierarchy: non-equilibrium states that are "close" to Gibbs (like S rho_Gibbs S†) have near-correct modular dynamics, while states that are "far" from Gibbs (like post-quench) have qualitatively wrong modular dynamics. Quantifying this hierarchy could be informative.
- The asymptotic limit sqrt(3) for the discrepancy is a universal number (independent of lambda) — worth understanding why.
- A time-dependent coupling lambda(t) that interpolates from 0 to lambda_final would show how the modular Hamiltonian "tracks" (or fails to track) the changing dynamics in real time.

## Computations Identified
- Quantify the "distance from Gibbs" metric that predicts whether global TTH discrepancy is structural vs quantitative
- Test with time-dependent coupling (adiabatic vs sudden quench interpolation)
- Test with multi-mode systems (>2 oscillators) to see if structural discrepancy persists or washes out
