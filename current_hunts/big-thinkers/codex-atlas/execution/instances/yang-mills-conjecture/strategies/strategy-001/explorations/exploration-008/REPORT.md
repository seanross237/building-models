# Exploration 008: Close Gap 1 — Full 9D Eigenspace Bound

## Goal

Prove that lambda_max(M(Q)) <= 16 for ALL directions in the 9-dimensional top eigenspace P of M(I), not just the 3D uniform-color staggered subspace covered by the E006 proof.

## Summary of Results

**The bound holds with overwhelming numerical evidence. No algebraic proof found, but the proof structure is fully characterized.**

- **0 violations** across 110K+ random configs and 350+ adversarial gradient ascent trials
- Best adversarial eigenvalue: 15.997 (Task 2C, 100 trials); 15.77 (Task 4D, 200 trials)
- Gap structure identified: gap = f_same + cross, where f_same >= 0 always and the harmful cross term is at most ~8% of f_same
- Key identities verified: budget identity, per-plaquette expansion, combined bound lemma

## The Mathematical Setup

### The 9D eigenspace P

At Q = I, M(I) has eigenvalue 16 with multiplicity 9. The eigenspace P is spanned by:

  v^{(s,a)}_{x,mu} = (-1)^{|x|} s_mu e_a

where s is perpendicular to (1,1,1,1) in R^4 (3 spatial DOF) and e_a is a color basis vector in R^3 (3 color DOF).

A general element w of P has w_{x,mu} = (-1)^{|x|} T_mu where T = (T_0, T_1, T_2, T_3) is a 4x3 matrix with **constraint Sum_mu T_mu = 0** (a 3-vector equation giving 9 DOF).

### Per-vertex formulation

**Key reduction** [VERIFIED]: The bound v^T M(Q) v <= 16|v|^2 for v in P is EQUIVALENT to the per-vertex bound:

  **F_x(T, Q_local) <= 16 ||T||_F^2   for all T with Sum_mu T_mu = 0**

where F_x = Sum_{mu<nu} |(I + R_mu D_{mu,nu}) T_mu - (R_mu + R_mu D_{mu,nu} R_nu^T) T_nu|^2 is the per-vertex B-field squared, and ||T||_F^2 = Sum_mu |T_mu|^2.

This is a 12x12 eigenvalue problem: lambda_max(M_12|_V) <= 16 where M_12 is the per-vertex Hessian restricted to the 9D constraint space V = {T : Sum_mu T_mu = 0}.

## Task 1: Eigenspace Structure [COMPUTED]

(Full 192x192 computation was too expensive to complete; per-vertex approach used instead.)

## Task 2: Per-Vertex Analysis

### M_12 at Q=I [VERIFIED]
- M_12(I) = 16 I_12 - 4 (J_4 tensor I_3) where J_4 is the 4x4 all-ones matrix
- Eigenvalues: {0 (multiplicity 3), 16 (multiplicity 9)}
- On V: all eigenvalues equal 16 (maximum, tight)
- On complement (1,1,1,1)xR^3: eigenvalue 0
- Code: `code/task2_pervertex_general.py` Part A

### Random configs (10,000 tests) [COMPUTED]
- Max constrained eigenvalue: **15.525** (well below 16)
- Max UNCONSTRAINED eigenvalue: **20.885** (exceeds 16!)
- **The constraint Sum_mu T_mu = 0 is ESSENTIAL** — without it, eigenvalue can reach ~21
- Code: `code/task2_pervertex_general.py` Part B

### Adversarial gradient ascent (100 trials x 300 iterations) [COMPUTED]
- Best constrained eigenvalue: **15.997** (approaches 16 from below, never exceeds)
- Best unconstrained eigenvalue: 17.878
- **BOUND HOLDS in all 100 adversarial trials**
- Code: `code/task2_pervertex_general.py` Part C

### Structure of maximizer [COMPUTED]
- The constrained maximizer is **NOT always rank-1** (uniform-color)
- Rank-1 fraction ranges from 0.56 to 0.99, mean 0.90
- **Implication: Cannot reduce to uniform-color case. Need full 9D proof.**
- Code: `code/task2_pervertex_general.py` Part D

### Trace identity for general s [COMPUTED]
- For uniform-color modes with general spatial pattern s perp (1,1,1,1):
  - Tr(M_total(s)) is NOT constant over Q (varies by factor ~3)
  - The E006 trace identity (c + Tr(P) = 64) does NOT hold for general s
  - However, max(lambda_max / |s|^2) stays below 16 in all tests
- Code: `code/task2_pervertex_general.py` Part E

### Direct F_x/||T||^2 bound for general T [COMPUTED]
- Max F_x / ||T||_F^2 = 12.46 over 5,000 random (T, Q) pairs
- Bound is 16; substantial margin
- Code: `code/task2_pervertex_general.py` Part F

## Task 3: Per-Plaquette Budget Analysis

### Budget identity [VERIFIED]

**For T with Sum_mu T_mu = 0: 16 ||T||^2 = 4 Sum_{mu<nu} |T_mu - T_nu|^2**

**Proof:** Sum_{mu<nu} |T_mu - T_nu|^2 = (d-1)||T||^2 - 2 Sum_{mu<nu} T_mu . T_nu = (d-1)||T||^2 + ||T||^2 = d||T||^2 = 4||T||^2 (using |Sum T_mu|^2 = 0). So 4 * 4||T||^2 = 16||T||^2. QED.

Verified numerically: error < 5e-13. Code: `code/task3_budget_decomposition.py` Part A.

### Per-plaquette budget fails [COMPUTED]
- Max |B|^2 / (4|T_mu - T_nu|^2) = **195.6** — individual plaquettes can vastly overspend
- About 5-21% of plaquettes exceed their budget
- ALL 6 plaquette types can have negative gap
- **Cross-plaquette cancellation is needed** (same situation as E006)
- Code: `code/task3_budget_decomposition.py` Part B

### Total gap decomposition [VERIFIED]

**Per-plaquette expansion identity:**

  4|T_mu - T_nu|^2 - |B_{mu,nu}|^2 = 2 f(U_{mu,nu}, T_mu) + 2 f(W_{mu,nu}, T_nu) - 2 T_mu^T C_{mu,nu} T_nu

where:
- f(R, p) = p^T(I - R)p >= 0 for R in SO(3), p in R^3
- U_{mu,nu} = R_mu D_{mu,nu}, W_{mu,nu} = D_{mu,nu} R_nu^T
- C_{mu,nu} = (I-R_mu) + (I-R_nu^T) + (I-D_{mu,nu}^T) + (I-R_mu D_{mu,nu} R_nu^T)

Summing over plaquettes: **gap = f_same + cross** where:
- **f_same = 2 Sum [f(U, T_mu) + f(W, T_nu)] >= 0** (always non-negative)
- **cross = -2 Sum T_mu^T C_{mu,nu} T_nu** (can be positive or negative)

Verified: identity holds to < 2e-13. Code: `code/task7_key_identity.py`.

### Cross term is dominated by f_same [COMPUTED]
- When cross term HURTS (is negative, reducing gap): max |cross|/f_same = **0.082**
- When cross term HELPS (is positive, increasing gap): can be much larger (up to 3.7x f_same)
- The cross is strongly ASYMMETRIC — it mostly helps the gap
- **Gap >= 0.918 * f_same >= 0** in all tested configurations
- Code: `code/task3_budget_decomposition.py` Part H

## Task 4: Proof Attempt

### Adversarial tests (200 trials x 1000 iterations each) [COMPUTED]
- Best constrained eigenvalue: **15.769**
- Mean converged value: 12.05, Std: 1.34
- **0% above 15.99, 0% above 16.00**
- Code: `code/task4_proof_attempt.py` Part D

### Gap structure at adversarial maxima [COMPUTED]
- At adversarial maxima: gap ranges from 2.2 to 6.4 (always positive)
- f_same > 0 always; cross term is typically small (|cross| < 2 in most cases)
- Rank-1 fraction of maximizer: 0.61 to 0.94 (mixed rank)
- Distance from identity: 22-26 (well away from Q=I)
- Code: `code/task4_proof_attempt.py` Part E

### Uniform-color bound for general s [COMPUTED]
- Min gap over 50,000 random tests: 0.034 (positive)
- Max F_x / (16|s|^2) = 0.901 (well below 1.0)
- Base-link budget alone is insufficient for general s (only 17.7% of configs)
- BUT the total gap (including f_same from cross-links) is always positive
- Code: `code/task4_proof_attempt.py` Part C

### Why a clean algebraic proof is hard [CONJECTURED]
1. **Trace identity fails for general s**: Unlike E006 where Tr(M_total) = 64 independently of Q, for general s the trace varies
2. **Active/inactive classification depends on s**: The sign pattern s_mu s_nu determines which plaquettes are "hard", and this varies with s
3. **Base-link budget is insufficient for some s patterns**: For balanced patterns like (1,1,-1,-1), each direction participates in multiple "hard" plaquettes and can't dedicate full budget to any one
4. **Cross-color coupling**: For rank > 1 modes, the B-field mixes different color directions, introducing cross terms that don't appear in uniform-color analysis
5. **Constraint is essential**: The unconstrained M_12 has eigenvalue up to ~21, so the proof MUST use Sum_mu T_mu = 0

## Task 5: Uniform-Color Extension

### Adversarial test for all s patterns [COMPUTED]
- 100 adversarial trials jointly optimizing R, D, and s: best lambda_max/|s|^2 = **14.86**
- Sweep over s directions (13 x 25 grid, 500 Q per s): worst ratio = **15.08**
- The uniform-color bound holds with significant margin for all s patterns
- Code: `code/task5_uniform_color_proof.py`

## Verified Identities for Future Proof

1. **Budget Identity** [VERIFIED]: 16||T||^2 = 4 Sum |T_mu - T_nu|^2 for T with Sum T_mu = 0. Algebraic proof provided.

2. **Per-Plaquette Expansion** [VERIFIED]: 4|T_mu-T_nu|^2 - |B|^2 = 2f(U,T_mu) + 2f(W,T_nu) - 2 T_mu^T C T_nu. Verified to machine precision.

3. **E006 Combined Bound Lemma** [VERIFIED]: f(A)+f(B)+f(AD)+f(DB^T)-f(D)-f(ADB^T) = n^T(I-A)D(I-B^T)n + f(A)+f(B) >= 0. Proven in E006.

4. **f_same Domination** [COMPUTED]: max(harmful_cross / f_same) < 0.1 over all tested configs. This is the KEY structural fact enabling the proof, but NOT yet proven algebraically.

## Conclusions

### What is established

1. **[COMPUTED] The full 9D bound lambda_max(M_12|_V) <= 16 holds** with 0 violations across:
   - 10,000 random configs (max = 15.53)
   - 100 adversarial trials with 300 iterations (max = 15.997)
   - 200 adversarial trials with 1000 iterations (max = 15.77)
   - 50,000 uniform-color random tests (max ratio = 0.90)
   - 10,000 extreme-rotation configs

2. **[VERIFIED] The per-vertex formulation** reduces the problem to a 12x12 constrained eigenvalue bound, with the constraint Sum_mu T_mu = 0 being ESSENTIAL (without it, eigenvalue reaches ~21).

3. **[VERIFIED] The gap decomposition** gap = f_same + cross where f_same >= 0 and the harmful cross is at most ~8% of f_same. This identifies the precise algebraic structure that a proof must exploit.

### What remains unproven

The algebraic proof that f_same + cross >= 0 for all SO(3) rotations and all constrained T. The difficulty stems from:
- The cross term involving products T_mu^T (I-R) T_nu of DIFFERENT vectors (no same-vector Cauchy-Schwarz)
- The constraint space being lower-dimensional (9D vs 12D)
- The base-link budget being shared across multiple "hard" plaquettes

### Proof strategy for future work

**Most promising approach:** Prove that the harmful part of the cross term is bounded by f_same. Specifically:

  max over all (R, D, T): [2 Sum T_mu^T C_{mu,nu} T_nu]_+ / f_same < 1

where [x]_+ = max(x, 0) and C, f_same are as defined in the gap decomposition. Numerical evidence: this ratio never exceeds 0.082 (enormous safety margin).

**Alternative approaches:**
- Direct SDP/SOS proof that M_12 - 16I is negative semidefinite on V
- Concavity argument showing Q=I maximizes the restricted Rayleigh quotient
- Extension of E006 combined bound to matrix-valued settings (T_mu as vectors, not scalar s_mu)

### Verification Scorecard
- **VERIFIED:** 3 (budget identity, per-plaquette expansion, M_12 at Q=I)
- **COMPUTED:** 8 (random tests, adversarial tests, gap structure, uniform-color tests, extreme rotations, maximizer structure, cross-term ratio, trace identity failure)
- **CONJECTURED:** 2 (algebraic proof difficulty, f_same domination proof)
