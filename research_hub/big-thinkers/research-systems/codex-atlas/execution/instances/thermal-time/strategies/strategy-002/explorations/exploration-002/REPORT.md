# Exploration 002 — Non-Equilibrium TTH Test (Post-Quench State)

## Goal

Test the Thermal Time Hypothesis for a non-Gibbs (post-quench) state of coupled harmonic oscillators. The state is the thermal state of the uncoupled system, which is NOT the Gibbs state of the coupled Hamiltonian. In this regime, global modular flow generates dynamics DIFFERENT from Hamiltonian evolution — TTH makes genuinely novel predictions.

## Setup

- Two coupled oscillators: H_AB(lambda) = 1/2(p_A^2 + w^2 q_A^2) + 1/2(p_B^2 + w^2 q_B^2) + lambda q_A q_B
- omega = 1.0, beta = 2.0, N = 20 Fock levels per mode (D = 400 total)
- Post-quench state: rho_0 = exp(-beta H_AB(0)) / Z_0 (thermal state of UNCOUPLED system)
- Three correlators compared:
  - **C_QM(tau)**: evolve x_A under coupled H_AB(lambda), state = rho_0
  - **C_global_TTH(tau)**: evolve x_A under uncoupled H_AB(0) = K_AB/beta (modular flow of rho_0)
  - **C_local_TTH(tau)**: evolve x_A under K_A/beta (local modular Hamiltonian)

## Control Checks

### 1. Gibbs State Control (C_global = C_QM for equilibrium states) `[VERIFIED]`

| lambda | max|C_QM - C_global| | Status |
|--------|----------------------|--------|
| 0.1    | 0.00e+00             | PASS   |
| 0.3    | 0.00e+00             | PASS   |
| 0.5    | 0.00e+00             | PASS   |

For the Gibbs state rho = exp(-beta H_AB(lambda))/Z, the modular Hamiltonian K = beta H + logZ I, so modular flow exactly equals Hamiltonian evolution. The global TTH correlator is identically equal to the QM correlator (not just to machine precision — the computation uses the same Hamiltonian). This validates the code infrastructure.

### 2. Uncoupled Control (lambda = 0) `[COMPUTED]`

At lambda = 0, the "post-quench" state IS the Gibbs state (since H_AB(0) = H_AB(0)). All three correlators agree:
- max|C_QM - C_global| = 0
- max|C_QM - C_local| = 9.85e-16 (machine epsilon)

### 3. State Properties `[COMPUTED]`

- Tr(rho_0) = 1.000000000000000
- Min eigenvalue of rho_0 = 7.37e-34 (positive to numerical precision)
- Product state verification: ||rho_A(trace) - rho_A(analytic)|| = 1.12e-16
- K_A = beta * omega * n_A + const: verified to ||delta|| = 6.24e-15

The post-quench state is a **product state** rho_0 = rho_A_thermal ⊗ rho_B_thermal, which has important consequences (see below).

## Main Results — Post-Quench State

### Discrepancy Table `[COMPUTED]`

| lambda | omega_+ | omega_- | ||dC_global||/||C_QM|| | ||dC_local||/||C_QM|| | max|dC_global| | max|dC_local| |
|--------|---------|---------|------------------------|-----------------------|----------------|---------------|
| 0.00   | 1.0000  | 1.0000  | 0.00000000             | 0.00000000            | 0.000000e+00   | 9.853e-16     |
| 0.10   | 1.0488  | 0.9487  | 0.09556749             | 0.09556749            | 1.258e-01      | 1.258e-01     |
| 0.20   | 1.0954  | 0.8944  | 0.42430829             | 0.42430829            | 4.580e-01      | 4.580e-01     |
| 0.30   | 1.1402  | 0.8367  | 1.01655006             | 1.01655006            | 8.708e-01      | 8.708e-01     |
| 0.50   | 1.2247  | 0.7071  | 1.74499299             | 1.74499299            | 1.250e+00      | 1.250e+00     |

**Key observations:**
1. **C_QM ≠ C_global_TTH for all lambda > 0** — confirming that TTH makes a genuinely different prediction for non-Gibbs states. The discrepancy grows dramatically with coupling strength.
2. **C_global_TTH = C_local_TTH to machine precision** — because the post-quench state is a product state (see explanation below).
3. At lambda = 0.3, the discrepancy exceeds 100% (||dC|| > ||C_QM||). At lambda = 0.5, it reaches 174%.

### Why C_global = C_local for Product States `[VERIFIED]`

The post-quench state is a product state: rho_0 = rho_A ⊗ rho_B.

**Global modular flow**: K_AB = beta(omega n_A + omega n_B) + const. Evolution of x_A under K_AB/beta:
```
e^{i(omega n_A + omega n_B)t} (x_A ⊗ I_B) e^{-i(omega n_A + omega n_B)t} = e^{i omega n_A t} x_A e^{-i omega n_A t} ⊗ I_B
```
The n_B part commutes with x_A ⊗ I_B and cancels.

**Local modular flow**: K_A = beta omega n_A + const (since rho_A is thermal for uncoupled H_A). Evolution of x_A under K_A/beta gives identically the same dynamics.

This is a **product-state identity**: for product states, global and local modular flows agree on local observables. For entangled states, they generically differ (confirmed by the squeezed state test below).

### Analytical Verification `[VERIFIED]`

The numerical correlators match exact analytical formulas to high precision:

**C_QM(t) = (2n_bar+1)/(4 omega) * [cos(omega_+ t) + cos(omega_- t)]** `[VERIFIED]`

Verification: ||C_QM(numerical) - C_QM(analytical)|| / ||C_QM|| for:
- lambda=0.1: 3.02e-13
- lambda=0.3: 7.89e-12
- lambda=0.5: 5.86e-09

**C_global(t) = (2n_bar+1)/(2 omega) * cos(omega t)** `[VERIFIED]`

Verification: ||C_global(numerical) - C_global(analytical)|| / ||C_global|| = 7.97e-16 for all lambda.

Where n_bar = 1/(e^{beta omega} - 1) = 0.1565 and omega_± = sqrt(omega^2 ± lambda).

### FFT Spectral Analysis `[COMPUTED]`

High-resolution FFT (N_tau=2000, T=16pi, zero-padded 8x, resolution 0.016 rad/s):

**lambda = 0.3** (representative case):

| Correlator | Dominant frequencies | Amplitudes | Physical origin |
|------------|---------------------|------------|-----------------|
| C_QM       | **1.1401**, **0.8433** | 341, 338   | Normal modes omega_+, omega_- |
| C_global   | **0.9995**           | 657        | Uncoupled frequency omega |
| C_local    | **0.9995**           | 657        | Same as C_global (product state) |

**lambda = 0.5** (strongest coupling):

| Correlator | Dominant frequencies | Amplitudes |
|------------|---------------------|------------|
| C_QM       | **0.7028**, **1.2338** | 344, 339   |
| C_global   | **0.9995**           | 657        |

**The discrepancy is STRUCTURAL, not quantitative:**
- C_QM contains the coupled normal mode frequencies omega_± = sqrt(omega^2 ± lambda)
- C_global_TTH contains only the uncoupled frequency omega = 1.0
- The frequency contents are completely disjoint — no shared spectral features

### Physical Interpretation: What Modular Time "Means" for Non-Equilibrium States `[CONJECTURED]`

Using sum-to-product identities:

```
C_QM(t) = A * cos(omega_avg * t) * cos(delta_omega * t / 2)
C_global(t) = A * cos(omega * t)
```

where omega_avg = (omega_+ + omega_-)/2, delta_omega = omega_+ - omega_-.

The modular flow "remembers" the pre-quench Hamiltonian and is completely blind to the post-quench coupling. Specifically:

1. **Modular time = pre-quench time**: The global modular flow generates evolution under H_AB(0), the pre-quench Hamiltonian. TTH's "thermal time" is the physical time of the system *before the quench happened*.

2. **Missing the beat**: C_QM shows characteristic beating with period T_beat = 4pi/delta_omega (ranging from 125.5 at lambda=0.1 to 24.3 at lambda=0.5). This beating is entirely absent from C_global, which oscillates at a single frequency.

3. **Carrier frequency shift**: Even the central oscillation frequency differs: omega_avg = omega - lambda^2/(8 omega^3) + ... shifts away from omega for finite coupling.

4. **Not "wrong" but "different physics"**: The modular flow isn't producing random noise — it's producing a coherent physical prediction (evolution under the old Hamiltonian). This is analogous to how a thermometer stuck at the pre-quench temperature gives a consistent but incorrect reading.

5. **State-preparation encoding**: The modular Hamiltonian K = -log(rho) encodes the state's preparation history. For a thermal state prepared at temperature T under Hamiltonian H, the modular Hamiltonian is beta*H — it "knows" both the temperature and the Hamiltonian. After a quench, the modular Hamiltonian still "remembers" the old Hamiltonian, even though the dynamics are now governed by the new one.

**Asymptotic discrepancy**: For any lambda > 0, the relative discrepancy ||C_QM - C_global|| / ||C_QM|| → sqrt(3) ≈ 1.732 as T → infinity (since the frequency contents are disjoint, the cross-correlation averages to zero). `[COMPUTED]`

### Beat Period vs. Observation Window `[COMPUTED]`

| lambda | Beat period T_beat | T_beat / T_window(4pi) | Discrepancy at T=4pi | Discrepancy at T=16pi |
|--------|-------------------|------------------------|----------------------|-----------------------|
| 0.1    | 125.5             | 9.99                   | 0.0956               | 1.522                 |
| 0.2    | 62.5              | 4.97                   | 0.4243               | 1.977                 |
| 0.3    | 41.4              | 3.29                   | 1.017                | 1.593                 |
| 0.5    | 24.3              | 1.93                   | 1.745                | 1.737                 |

For small lambda (long beat period), the discrepancy is small over short observation windows because the beating envelope hasn't deviated significantly from 1. The discrepancy manifests over timescales comparable to or longer than the beat period.

## Squeezed State Test `[COMPUTED]`

Applied squeezing S(r=0.3) to mode A of the Gibbs state at lambda=0.3:
rho_squeezed = S_AB rho_gibbs S_AB†

### Results

| Metric | Value |
|--------|-------|
| ||C_QM - C_global_TTH|| / ||C_QM|| | **0.0777** |
| ||C_QM - C_local_TTH|| / ||C_QM|| | **1.801** |
| ||C_global - C_local|| / ||C_global|| | **1.823** |
| ||K_squeezed - K_gibbs|| / ||K_gibbs|| | 3.47 |

**Striking contrast with post-quench case:**

| Property | Post-quench (lam=0.3) | Squeezed (lam=0.3, r=0.3) |
|----------|-----------------------|---------------------------|
| Global TTH discrepancy | 1.017 (102%) | **0.078 (7.8%)** |
| Local TTH discrepancy | 1.017 (102%) | 1.801 (180%) |
| C_global = C_local? | Yes (product state) | **No** (entangled state) |
| State entangled? | No | Yes |

**Key findings:**

1. **Global TTH is much closer for squeezed state** (7.8% vs 102%): The squeezed state's modular Hamiltonian K_sq = S(beta H)S† ≈ beta H + O(r), so the modular flow is a perturbation of the actual dynamics. Unlike the post-quench case, the squeezing doesn't change the Hamiltonian's eigenstates drastically.

2. **Local TTH is much worse for squeezed state** (180%): The squeezed state has non-trivial entanglement between A and B, so the partial trace destroys important information. The local modular Hamiltonian K_A has a very different spectral structure.

3. **C_global ≠ C_local for entangled states**: This confirms the product-state identity from above. For entangled states, global and local modular flows generically differ.

### Spectral Content (Squeezed State)

| Correlator | Top frequencies | Interpretation |
|------------|----------------|----------------|
| C_QM       | 0.843 (260), 1.140 (142) | Normal modes omega_-, omega_+ |
| C_global   | 0.843 (244), 1.140 (157) | Same modes! (small perturbation) |
| C_local    | 0.937 (388) | Single shifted frequency |

The squeezed state's global TTH shares the correct normal-mode frequencies with C_QM — only the amplitudes differ slightly. This is a **quantitative** discrepancy (same frequencies, different amplitudes), not a structural one. In contrast, the post-quench global TTH has completely wrong frequencies.

## Convergence Check `[COMPUTED]`

At lambda=0.3, comparing N=15, N=20, N=25:

| Correlator | ||N=15 - N=20|| / ||N=20|| | ||N=25 - N=20|| / ||N=20|| |
|------------|---------------------------|---------------------------|
| C_QM       | 3.63e-09                  | 2.87e-12                  |
| C_global   | 8.97e-12                  | 4.42e-16                  |

Results are converged to at least 9 significant digits at N=20. The N=25 vs N=20 difference is at or below machine precision for C_global. All reported results are trustworthy.

## Comparison: Gibbs vs Post-Quench (Side by Side) `[COMPUTED]`

| lambda | Gibbs: ||dC_global||/||C_QM|| | Quench: ||dC_global||/||C_QM|| | Quench: ||dC_local||/||C_QM|| |
|--------|-------------------------------|-------------------------------|------------------------------|
| 0.00   | 0                             | 0                             | 0                            |
| 0.10   | 0                             | 0.0956                        | 0.0956                       |
| 0.20   | 0                             | 0.4243                        | 0.4243                       |
| 0.30   | 0                             | 1.0166                        | 1.0166                       |
| 0.50   | 0                             | 1.7450                        | 1.7450                       |

For Gibbs states, global TTH = QM always (by construction — modular flow equals Hamiltonian flow). The non-trivial content of TTH for non-equilibrium states is that the modular flow generates *different* dynamics — dynamics that correspond to the state's preparation history.

## Conclusions

### Summary of Findings

1. **TTH makes genuinely different predictions for non-Gibbs states** — confirmed with large discrepancies. `[VERIFIED]`

2. **The discrepancy is structural**: C_QM has normal-mode frequencies omega_± = sqrt(omega^2 ± lambda); C_global has only uncoupled frequency omega = 1.0. Completely disjoint spectral content. `[COMPUTED]`

3. **Modular time = pre-quench time**: The TTH modular flow evolves under the pre-quench Hamiltonian, encoding the state's preparation history rather than the actual post-quench dynamics. `[COMPUTED]`

4. **Product-state identity**: For product states, C_global_TTH = C_local_TTH exactly, because n_B commutes with x_A ⊗ I_B. `[VERIFIED]`

5. **Squeezed state contrast**: For a squeezed (non-product) state, the global TTH discrepancy is only 7.8% (quantitative, same frequencies) vs 102% for the post-quench state (structural, different frequencies). Local TTH is worse (180%) because entanglement information is lost. `[COMPUTED]`

6. **Exact analytical formulas verified**: C_QM(t) = A/2[cos(omega_+ t) + cos(omega_- t)], C_global(t) = A cos(omega t), with A = (2n_bar+1)/(2 omega). `[VERIFIED]`

### What This Means for TTH

The results show that TTH's thermal time has a clear physical meaning for non-equilibrium states: **it corresponds to the dynamics of the Hamiltonian that prepared the state**. This is not wrong — it's a legitimate physical prediction — but it's different from the actual dynamics.

This reveals a fundamental asymmetry in TTH: for equilibrium states, the modular Hamiltonian encodes the actual Hamiltonian (up to rescaling), so TTH "gets it right." For non-equilibrium states, the modular Hamiltonian encodes the preparation Hamiltonian, and TTH generates "the wrong dynamics" from the perspective of an observer who knows the actual Hamiltonian has changed.

Whether this is a bug or a feature depends on one's interpretation of TTH. If TTH claims that modular time IS physical time, then this is a failure — modular time and physical time demonstrably diverge after a quench. If TTH claims that modular time is one possible notion of time determined by the state (and may differ from Hamiltonian time), then the post-quench case reveals the extent and nature of this difference.

## Code

All scripts in `code/`:
- `compute_nonequilibrium.py` — Main computation: control checks, post-quench correlators, convergence
- `spectral_analysis.py` — High-resolution FFT with zero-padding, analytical verification
- `analytical_comparison.py` — Exact formulas, asymptotic analysis, comparison tables
- `squeezed_state_test.py` — Squeezed thermal state test
