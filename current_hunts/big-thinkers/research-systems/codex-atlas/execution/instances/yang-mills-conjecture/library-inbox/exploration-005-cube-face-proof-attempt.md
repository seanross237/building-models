# Exploration 005: Proof of Cube-Face Inequality F_x <= 64 for General Q

## Goal

Prove (or make maximal progress toward) Lemma 5: For all Q in SU(2)^E, all vertices x, and staggered mode v_stag = (-1)^{|x|+mu} n:

F_x(Q) := Sum_{mu<nu} |B_{(x,mu,nu)}(Q, v_stag)|^2 <= 64 |n|^2

This is the single remaining gap in the proof of Conjecture 1 (lambda_max(M(Q)) <= 16).

---

## Stage 1: Setup and Numerical Verification

### 1.1 Implementation

Implemented full F_x computation on L=2, d=4 torus using quaternion → SO(3) conversion.
Code: `code/stage1_verify.py`

B formula used:
```
B = s1*n + s2*R1*n - s3*R2*n - s4*R3*n
```
where R1 = Ad(Q_{e1}), R2 = Ad(Q_{e1}Q_{e2}Q_{e3}^{-1}), R3 = Ad(U_sq).

### 1.2 Verification: F_x(I) = 64

**[COMPUTED]** F_x(I) = 64.000000 for all 16 vertices. Max error: 0.00e+00.
Total sum = 1024.000000 = 4d|v|^2. PASS.

### 1.3 Random Q Tests

**[COMPUTED]** 1000 random Haar configs × 16 vertices = 16,000 F_x evaluations.
- Max F_x observed: 48.927 (well below 64)
- Violations (F_x > 64): 0
- Also verified with 4 different n vectors; all pass.

### 1.4 Single-Link Perturbation

**[COMPUTED]** Q_{(0,0,0,0),0} = exp(ε·τ₁) for ε ∈ {0.01, 0.1, 0.5, 1.0, π/2, π}:
F_x = 64.000000 for ALL 16 vertices, ALL epsilon values.

**Explanation:** This rotation preserves n = (1,0,0) since it rotates about the x-axis. Hence Ad(Q)·n = n for all ε, making B identical to the Q=I case. This test is not informative for cross-link effects.

---

## Stage 2: Algebraic Decomposition and Structure

### 2.1 Key Reformulation: F_x = n^T M_total n

**[VERIFIED]** F_x is a quadratic form in the direction vector n:

F_x = n^T M_total(R, D) n

where M_total is a 3×3 PSD matrix independent of n, given by:
M_total = sum_{mu<nu} A_{mu,nu}^T A_{mu,nu},  A = a*S + b*T

with S = I + R_mu D, T = R_mu + R_mu D R_nu^T.

At Q = I: M_total = 64·I (all eigenvalues equal 64). Verified to machine precision.

The bound F_x <= 64 for all unit n is EQUIVALENT to lambda_max(M_total) <= 64.

### 2.2 Cross-Link Monotonicity FAILS

**[COMPUTED]** Tested 50,000 random (R_base, D_cross) pairs: F_x(R, D) > F_x(R, I) in 33% of cases. Max Delta = +27.3. Adversarial gradient ascent finds Delta up to +28.

**Cross-link monotonicity is FALSE.** Cross-links can INCREASE F_x for fixed base links. Approach A from the goal is DEAD.

Inactive plaquettes are the main source: single inactive cross-link adds up to +12 to F_x, vs +3 for active.

### 2.3 lambda_max Analysis — THE KEY RESULT

**[COMPUTED]** Over 10,000 random configs: max lambda_max = 56.9 (below 64). Zero violations.

**[COMPUTED]** Adversarial gradient ascent on lambda_max: ALL 30 trials converge to lambda_max = 64.000000 EXACTLY. The maximum is always achieved by a rich manifold of configurations (not just Q=I).

At all adversarial maxima: eigs = [small, medium, 64.0000]. The top eigenvalue saturates at 64 while lower eigenvalues vary.

From Q=I, gradient ascent on lambda_max cannot increase past 64 (max at step 0).

### 2.4 Trace Analysis

**[COMPUTED]** Tr(M_total) ranges from ~40 to ~128 (random) with max 192 at Q=I. Trace bound Tr <= 192 holds but is far too weak (192/3 = 64 works only if M ∝ I, which it isn't generically). Anisotropy ratio lambda_max/(Tr/3) up to 2.14.

---

## Stage 3: Proof Attempts

### 3.1 Approach A: Cross-Link Monotonicity

*Pending...*

### 3.2 Approach B: General Formula Extension

*Pending...*

### 3.3 Approach C: Gauge Fixing

*Pending...*

---

## Stage 4: Summary and Tightest Bound

*Pending...*
