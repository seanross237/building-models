# Exploration 008: Prove max lambda[P^T R(Q) P] <= -W(Q)/12

## Goal

Verify and attempt to prove the inequality max lambda[P^T R(Q) P] <= -W(Q)/12 where W(Q) = sum_plaq (1 - Re Tr(U_plaq)/N) >= 0 is the Wilson action density. If this holds for all Q in SU(2)^E, it immediately implies P^T R(Q) P is negative semidefinite (since W >= 0), closing the main spectral gap theorem.

## Setup

- Lattice: L=2, d=4, SU(2) gauge group
- M(Q) = sum_plaq B_plaq^T B_plaq (192x192 PSD Hessian)
- M(I) = K_curl with lambda_max = 4d = 16, multiplicity 9
- P = 192x9 matrix of top eigenspace of M(I)
- R(Q) = M(Q) - M(I) (difference operator, Tr = 0)
- Target: all eigenvalues of 9x9 matrix P^T R(Q) P are <= 0
- B_plaq B_plaq^T = 4*I_3 per plaquette (structural invariant, all Q)

## Section 1: Numerical Verification (201 configs)

### 1.1 Main Result

**[COMPUTED] P^T R(Q) P is negative semidefinite for ALL 201 tested configurations.** Zero violations out of 201. The maximum eigenvalue of P^T R(Q) P is ≤ 0 for every config class: random Haar, Gibbs samples, near-identity, pure gauge, abelian, and adversarial gradient ascent.

### 1.2 The -W/12 Formula is WRONG

**[COMPUTED] The formula max lambda[R(Q)|_P] = -W(Q)/12 does NOT hold in general.** It fails dramatically for:

1. **Abelian configs**: max_eig = 0 exactly (tau_3 invariant direction preserved), but W > 0 (typically 77-109), so -W/12 < 0. The ratio max_eig/(-W/12) = 0, but the bound max_eig ≤ -W/12 is VIOLATED (0 > -W/12).

2. **Some Haar and near-identity configs**: The ratio max_eig/(-W/12) can be < 1, meaning max_eig is LESS negative than -W/12, violating the upper bound.

3. **Pure gauge configs**: max_eig is significantly negative (-6 to -8) but W = 0, so the formula is undefined.

### 1.3 Detailed Results by Config Class

| Group | Count | max_eig range | W range | ratio range | Violations (max_eig > -W/12) |
|-------|-------|--------------|---------|-------------|------------------------------|
| Haar | 50 | [-9.06, -7.50] | [85.9, 105.8] | [0.90, 1.18] | 5 |
| Gibbs | 50 | [-9.29, -6.61] | [19.1, 93.9] | [1.04, 4.84] | 0 |
| NearI | 21 | [-9.01, -0.001] | [0.01, 106.7] | [0.88, 1.63] | 5 |
| PureGauge | 20 | [-8.35, -5.83] | [0, 0] | N/A | 0 |
| Abelian | 20 | [0, 0] | [76.8, 108.5] | [0, 0] | 20 |
| Adversarial | 40 | [-9.16, -8.07] | [83.4, 102.4] | [1.02, 1.23] | 0 |

### 1.4 Key Observations

1. **max_eig ≤ 0 universally** — the fundamental inequality P^T R(Q) P ≼ 0 holds without exception. [COMPUTED]

2. **Abelian configs saturate the bound** at max_eig = 0, achieved by the tau_3 staggered mode which is invariant under abelian gauge transformations. The eigenvalue structure shows three zero eigenvalues (from preserved tau_3 modes) and six strictly negative eigenvalues. [COMPUTED]

3. **Pure gauge configs give max_eig ≪ 0 despite W = 0** — the gauge transformation "rotates" the top eigenspace away from the reference P, making all eigenvalues of P^T R(Q) P strictly negative. [COMPUTED]

4. **Adversarial gradient ascent** (40 configs, 20 steps each trying to maximize the ratio max_eig/(-W/12)) never pushed max_eig above 0. The adversarial configs cluster at ratio ≈ 1.0-1.2, far from violation. [COMPUTED]

5. **Eigenvalue structure**: For generic (non-abelian, non-pure-gauge) configs, all 9 eigenvalues of P^T R(Q) P are distinct and negative. For abelian configs, the structure is {0 (x3), negative (x2), negative (x2), negative (x2)} reflecting the abelian decomposition into tau_3 invariant and tau_{1,2} rotating sectors. [COMPUTED]

### 1.5 Corrected Understanding

The correct statement is:

- **max lambda[P^T R(Q) P] ≤ 0** for all Q (the spectral gap inequality) — VERIFIED for 201 configs
- **max lambda[P^T R(Q) P] = 0** iff Q has a globally invariant color direction (abelian configs, Q=I) — VERIFIED
- The formula max lambda = -W/12 is NOT valid in general — DISPROVED by abelian counterexamples

The proof target should be **max lambda[P^T R(Q) P] ≤ 0 directly**, not via the Wilson action formula.

## Section 2: Analytical Proof — Per-Plaquette Triangle Inequality

### 2.1 Structure of the Top Eigenspace

*In progress...*

## Section 3: Single-Plaquette Exact Analysis

*Pending...*

## Section 4: Connection to Jiang (2022)

*Pending...*

## Section 5: Summary

*Pending...*
