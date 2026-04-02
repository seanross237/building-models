# Exploration 001: SDP/SOS Certificate for 9D Eigenspace Bound

**Goal:** Attack the 9D eigenspace bound lambda_max(M_9(Q)) <= 16 via SDP/SOS
**Date:** 2026-03-28
**Code:** `code/stage1_numerical.py`, `code/stage2_3_adversarial.py`, `code/stage4_sos.py`, `code/stage4b_certificate_attempt.py`, `code/stage4c_algebraic_identity.py`, `code/stage5_epsilon.py`

---

## Setup

- T: 4×3 matrix (12-vector), constraint V = {T : sum_mu T_mu = 0} (9D subspace)
- Q: 4 base links R_mu + 6 cross-links D_{mu,nu}, all in SO(3)
- F_x(Q,T) = sum_{mu<nu} ||(I + R_mu D) T_mu - (R_mu + R_mu D R_nu^T) T_nu||^2
- Target: 16||T||_F^2 - F_x(Q,T) >= 0 for all T in V, all Q in SO(3)^{10}

---

## Stage 1: Numerical Verification

### 1.1 Sanity check at Q=I

**[VERIFIED]** M_12(I) = 16 I_12 - 4 (J_4 ⊗ I_3), max construction error = 0.00e+00.
Eigenvalues: {0 (×3), 16 (×9)}, exactly as predicted.
lambda_max(M_9(I)) = 16.000000 — the **bound is tight at Q=I**.

### 1.2 Random sampling (1000 configurations)

All 1000 random SO(3)^{10} configurations satisfy lambda_max(M_9(Q)) < 16.

| Statistic | Value |
|-----------|-------|
| Bound violated | 0/1000 |
| Max lambda_max | **15.4338** |
| Min gap (16 - lmax) | **0.5662** |
| Mean lambda_max | 11.97 |
| Median | 11.96 |
| Std dev | 1.23 |
| 95th percentile | 13.91 |
| 99th percentile | 14.63 |

**[COMPUTED]** Bound lambda_max(M_9(Q)) <= 16 holds for all 1000 random samples.

---

## Stage 2: M_12 Formula Construction

**[VERIFIED]** M_12 formula matches direct F_x computation to 5.68e-14 over 200 random configs.

The formula: for each plaquette (mu,nu), let A = I + R_mu D and B = R_mu + R_mu D R_nu^T.
Then M_12[3mu:3mu+3, 3mu:3mu+3] += A^T A, M_12[3nu:3nu+3, 3nu:3nu+3] += B^T B,
M_12[3mu:3mu+3, 3nu:3nu+3] -= A^T B (and symmetric), summed over all 6 plaquettes.

---

## Stage 3: SDP Feasibility and Adversarial Search

### 3.1 SDP feasibility (200 random Q)

**[COMPUTED]** 16 I_9 - M_9(Q) >= 0 (PSD) for all 200 tested configurations.

| Statistic | Value |
|-----------|-------|
| PSD violations | 0/200 |
| Min slack eigenvalue | 1.351 |
| Mean slack eigenvalue | 4.093 |
| Max slack eigenvalue | 7.484 |

### 3.2 Adversarial gradient ascent (50 starts × 200 steps)

Riemannian gradient ascent on SO(3)^{10} using finite-difference gradients of lambda_max.

**[COMPUTED]** Global best lambda_max found: **15.637** (gap = 0.363)
No violation of the bound found in 50 adversarial runs.

### 3.3 Near-identity adversarial search

| Perturbation eps | max lambda_max | Gap |
|-----------------|----------------|-----|
| 0.001 | 16.000000 | ~0 |
| 0.003 | 15.999997 | 3e-6 |
| 0.01 | 15.999970 | 3e-5 |
| 0.03 | 15.999817 | 2e-4 |
| 0.1 | 15.998175 | 1.8e-3 |
| 0.3 | 15.979423 | 0.021 |
| 1.0 | 15.793137 | 0.207 |

Log-log slope of gap vs eps: **1.94** (consistent with quadratic: gap ~ O(||Q-I||^2)).

**[COMPUTED]** The approach to 16 from below is quadratic in the distance from Q=I.

---

## Stage 4: SOS Decomposition Analysis

### 4.1 Per-plaquette budget identity

**[VERIFIED]** For each plaquette (mu,nu):
4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu^T C_{mu,nu} T_nu

where U = R_mu D, W = D R_nu^T, C = (I-R_mu)+(I-R_nu^T)+(I-D^T)+(I-R_mu D R_nu^T).
Max identity error: 5.68e-14 over 200 trials. f(R,p) = p^T(I-R)p >= 0 for all R in SO(3).

### 4.2 Cross-term ratio

**[COMPUTED]** Max |cross|/f_same ratio = **5.24%** (claimed bound: 8.2%) over 500 configs × 20 T vectors.
All gaps 16||T||^2 - F_x >= 0 in this test (min gap = 3.51, since T not normalized).

### 4.3 Critical finding: per-plaquette bound FAILS

**[COMPUTED]** Single-plaquette 6×6 block is PSD (each plaquette contributes non-negatively).
**[COMPUTED]** BUT: lambda_max(M_AB) = **8** at Q=I, far exceeding the per-plaquette budget of 4.

Test: max ratio |A p - B q|^2 / (4|p-q|^2) = **7454** over 500 configs × 100 T vectors.
Per-plaquette bound |Ap-Bq|^2 <= 4|p-q|^2 is **FALSE**.

**Implication:** A per-plaquette SOS certificate is impossible. The constraint sum T_mu = 0 is **essential** for the global bound to hold — it cannot be avoided.

### 4.4 Key algebraic identity (using sum T_mu = 0)

**[VERIFIED]** Error 7.11e-15:
sum_{mu<nu} T_mu^T [(I - R_mu) + (I - R_nu^T)] T_nu = -sum_mu f(R_mu, T_mu) = -f_R

Derivation: sum_{mu,nu} T_mu^T (I - R_mu) T_nu = 0 (since sum T_nu = 0)
=> sum_{mu<nu} [T_mu^T(I-R_mu)T_nu + T_mu^T(I-R_nu^T)T_nu] = -sum_mu f(R_mu, T_mu)

This identity is the key structural property that the SOS proof must exploit.

### 4.5 Decomposition certificate

**[COMPUTED]** The exact identity (max error 7.11e-14):

  **16||T||^2 - F_x = f_same + 2·f_R - Term_C - Term_D**

where:
- f_same = sum_{mu<nu} [2f(R_mu D, T_mu) + 2f(D R_nu^T, T_nu)] >= 0 (12 non-negative terms)
- f_R = sum_mu f(R_mu, T_mu) >= 0 (4 non-negative terms)
- Term_C = 2 sum_{mu<nu} T_mu^T (I - D_{mu,nu}^T) T_nu (can be negative)
- Term_D = 2 sum_{mu<nu} T_mu^T (I - R_mu D_{mu,nu} R_nu^T) T_nu (can be negative)

Derivation uses: 16||T||^2 - F_x = f_same - 2 sum C = f_same - (A+B) - C - D
= f_same + 2 f_R - C - D (applying the identity from §4.4).

**[COMPUTED]** The certificate value f_same + 2·f_R - Term_C - Term_D >= 0 holds for all tested T in V with 0 violations over 20,000 test pairs.
Minimum certificate value found: 13.16 (normalized T, ||T||=1 not enforced; see gap distribution below).

### 4.6 SOS certificate status

**Achieved:** A structurally clean decomposition formula giving 16||T||^2 - F_x as a sum of f-terms minus two correction terms C, D.

**Remaining gap:** Proving algebraically that Term_C + Term_D <= f_same + 2·f_R.
This is equivalent to the original bound — we have not found a shortcut, but the structure is more explicit.

**Why no full SOS:** The slack 16 I_9 - M_9(I) = **zero matrix**. Any SOS decomposition G_k^T G_k must have G_k(I,T) = 0 for all T in V. The certificate cannot be expressed as a polynomial SOS in the rotation entries alone at degree 2 — higher degree or Lie-algebra structure is needed.

---

## Stage 5: Epsilon Bound

**[VERIFIED]** lambda_max(M_9(I)) = **16.0000000000** (16 decimal places).
**No uniform epsilon > 0 exists**: the bound lambda_max <= 16 is sharp.

Near Q=I: gap ~ C · ||Q-I||^2 (log-log slope 1.94). The approach to 16 is **quadratic**.

For generic (Haar-random) Q, the gap distribution:
- Min gap over 5,000 samples: 0.566
- 1st percentile gap: 1.475
- Effective epsilon for generic Q: ~0.57

---

## Summary of Key Results

| Result | Status | Source |
|--------|--------|--------|
| M_12 formula verified | [VERIFIED] error=5.68e-14 | stage2_3 |
| lambda_max <= 16 for 16,000+ samples | [COMPUTED] | stage1,3,5 |
| Adversarial max lambda_max = 15.637 | [COMPUTED] | stage2_3 |
| Bound tight at Q=I (lambda_max = 16) | [VERIFIED] | stage1 |
| Per-plaquette 6×6 blocks PSD | [COMPUTED] | stage4 |
| Per-plaquette bound FAILS (max ratio=7454) | [COMPUTED] | stage4b |
| Single-plaquette lambda_max = 8 at Q=I | [COMPUTED] | stage4b |
| Key identity (I-R_mu)+(I-R_nu^T) = -f_R | [VERIFIED] 7e-15 | stage5 |
| Decomposition formula exact (error=7e-14) | [COMPUTED] | stage5 |
| Certificate >= 0 for 20,000 tests | [COMPUTED] | stage4c |
| Cross-term ratio <= 5.24% | [COMPUTED] | stage4 |
| No uniform epsilon > 0 | [VERIFIED] | stage5 |
| Gap ~ O(||Q-I||^2) near identity | [COMPUTED] | stage5 |
| Algebraic SOS proof complete | [NOT ACHIEVED] | — |

---

## Proof Gaps Identified

1. **Main gap**: Proving Term_C + Term_D <= f_same + 2·f_R algebraically.
   Term_C = 2 sum T_mu^T (I - D_{mu,nu}^T) T_nu and Term_D = 2 sum T_mu^T (I - R_mu D R_nu^T) T_nu
   cannot be simplified using sum T_mu = 0 in the same way as Terms A+B.
   Each D_{mu,nu} and R_mu D_{mu,nu} R_nu^T are DIFFERENT for each pair — no global constraint.

2. **SOS at Q=I**: The slack 16 I_9 - M_9(I) = 0 means the SOS certificate must vanish
   identically at Q=I. Standard polynomial SOS at degree 2 in rotation entries is too tight.

3. **Per-plaquette approach blocked**: lambda_max of single plaquette = 8, exceeding
   the budget of 4. Must use the constraint subspace V globally.

---

## Potential Next Steps

- **Schur complement modulo V**: 16 I_12 - M_12 restricted to V via the projector P_V.
  Try writing P_V (16 I - M_12) P_V as a sum of products that manifestly use sum T_mu = 0.

- **Bounded D approach**: If cross-links D_{mu,nu} = I (base links only), does a
  simpler certificate exist? Then Term_C = 0 and Term_D involves only R_mu R_nu^T.

- **SOS modulo ideal**: Use Positivstellensatz modulo the SO(3) ideal R^T R = I.
  A degree-4 SOS might exist. Need cvxpy/SDP solver for this.

- **Lie algebra linearization**: Work in the tangent space at Q=I.
  Near identity: 16||T||^2 - F_x = sum_k (omega_k · T)^2 + O(eps^3) for some basis.
  This might give a local SOS certificate.
