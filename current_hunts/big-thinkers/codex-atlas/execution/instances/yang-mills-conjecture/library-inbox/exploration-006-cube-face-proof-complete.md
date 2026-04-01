# Exploration 006: Prove lambda_max(M_total) <= 64

## Goal

Prove that for all SO(3) rotations R_0, R_1, R_2, R_3 (base links) and D_{mu,nu} (cross-links), the largest eigenvalue of the 3×3 PSD matrix M_total satisfies lambda_max(M_total) <= 64.

This bound is equivalent to the Cube-Face Inequality F_x <= 64|n|^2, which is the single remaining gap in the proof of Conjecture 1 (lambda_max(M(Q)) <= 16 for Yang-Mills on the d=4 torus).

## Result: PROOF COMPLETE

**[VERIFIED]** We prove lambda_max(M_total) <= 64 via a five-step argument combining a trace identity, algebraic factorization, Cauchy-Schwarz, and AM-GM. All steps are verified numerically (>100,000 configs each, 0 violations, errors < 1e-10).

---

## Background: The Matrix M_total

M_total is defined on a d=4 torus with lattice size L=2. For each of 6 plaquette orientations (mu,nu) with 0 <= mu < nu <= 3, a 3×3 matrix A_{mu,nu} is given by:

A_{mu,nu} = a(I + R_mu D_{mu,nu}) + b(R_mu + R_mu D_{mu,nu} R_nu^T)

where a = (-1)^mu, b = (-1)^{nu+1}, and R_mu ∈ SO(3) are base-link rotations, D_{mu,nu} ∈ SO(3) are cross-link rotations.

M_total = Σ_{mu<nu} A_{mu,nu}^T A_{mu,nu}   (a 3×3 positive semidefinite matrix)

The 6 plaquettes split into:
- **Active** (|a+b| = 2, mu+nu odd): (0,1), (0,3), (1,2), (2,3) — 4 plaquettes
- **Inactive** (a+b = 0, mu+nu even): (0,2), (1,3) — 2 plaquettes

At Q = I (all rotations identity): M_total = 64·I, with active planes contributing 16I each and inactive planes contributing 0.

---

## Stage 1: Numerical Verification

### 1.1 Identity configuration

**[VERIFIED]** M_total(I) = 64·I₃. Code: `code/stage1_compute_mtotal.py`.

### 1.2 Random sampling (10,000 configs)

**[COMPUTED]** lambda_max ranges from 14.8 to 54.1 (mean 33.3). **0 violations** of the bound 64.

### 1.3 Adversarial gradient ascent (30 trials)

**[COMPUTED]** ALL 30 trials converge to lambda_max = 64.000000 exactly. The bound is tight.

### 1.4 Saturation manifold

**[COMPUTED]** lambda_max = 64 is achieved if and only if there exists a unit vector n such that R_mu n = n for all mu = 0,...,3 and D_{mu,nu} n = n for all active (mu,nu). Inactive cross-links are unconstrained. At saturation, active planes each contribute 16 and inactive planes contribute 0.

---

## Stage 2: Key Algebraic Identity

### 2.1 Cross-term decomposition

**[VERIFIED]** Expanding each |B_p|² = |Σ_i s_{p,i} Q_{p,i} n|² gives 4 diagonal terms (each = 1) and 6 cross terms per plaquette:

F_x(n) = n^T M_total n = 24 + 2 Σ_{k=1}^{36} σ_k · n^T O_k n

where O_k ∈ SO(3) are composed rotations and σ_k ∈ {+1, -1} are fixed signs.

Sign counts: 28 positive, 8 negative. Net: Σ σ_k = 20.

### 2.2 The trace identity: c + Tr(P) = 64

**[VERIFIED]** Decompose M_total = c·I + P where:
- c = 24 + 2 Σ_k σ_k cos θ_k (isotropic part)
- P = 2 Σ_k σ_k (1-cos θ_k) u_k u_k^T (anisotropy matrix)
- θ_k = rotation angle of O_k, u_k = rotation axis

Then **c + Tr(P) = 24 + 2 Σ_k σ_k = 24 + 40 = 64** identically, since the cos θ_k terms cancel. This is independent of all rotation parameters.

### 2.3 Equivalence to eigenvalue condition

**[VERIFIED]** Since lambda_max(M) = c + lambda_max(P):

lambda_max(M) ≤ 64 ⟺ lambda_max(P) ≤ Tr(P) ⟺ lambda_mid(P) + lambda_min(P) ≥ 0

---

## Stage 3: The Proof

### 3.1 Step 1 — Trace Identity (algebraic)

**[VERIFIED]** Per-plaquette σ sums: active plaquettes contribute +6 each (4 × 6 = 24), inactive contribute -2 each (2 × (-2) = -4). Total Σ σ_k = 20.

Therefore c + Tr(P) = 24 + 2 × 20 = 64.

### 3.2 Step 2 — Equivalence (linear algebra)

**[VERIFIED]** Standard: lambda_max(cI + P) ≤ 64 iff lambda_max(P) ≤ 64 - c = Tr(P).

### 3.3 Step 3 — Expansion of 64I - M

**[VERIFIED]** Define f(R) = I - sym(R) for R ∈ SO(3), a positive semidefinite matrix. As a quadratic form: f(R, n) = 1 - n^T R n ≥ 0.

By enumerating all 36 cross-term rotations O_k and their signs σ_k, and grouping by plaquette:

**64I - M = 2 × [group_02 + group_13 + group_active]**

where:

**group_02** = f(R_0) + f(R_2) + f(R_0 D_{02}) + f(D_{02} R_2^T) - f(D_{02}) - f(R_0 D_{02} R_2^T)

**group_13** = f(R_1) + f(R_3) + f(R_1 D_{13}) + f(D_{13} R_3^T) - f(D_{13}) - f(R_1 D_{13} R_3^T)

**group_active** = Σ_{active (mu,nu)} [f(R_mu D_{mu,nu}) + f(D_{mu,nu}) + f(R_mu D_{mu,nu} R_nu^T) + f(D_{mu,nu} R_nu^T)]

This decomposition is verified numerically: max |direct - expansion| < 4 × 10^{-14} over 100,000 random configs. Code: `code/stage4_complete_proof.py`.

### 3.4 Step 4 — Combined Bound Lemma

**LEMMA (Combined Bound):** For any A, B, D ∈ SO(3) and unit n ∈ R³:

f(A,n) + f(B,n) + f(AD,n) + f(DB^T,n) - f(D,n) - f(ADB^T,n) ≥ 0

**Proof of Lemma:**

**(a) Algebraic factorization.** Direct computation gives the identity:

f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) = **n^T(I-A)D(I-B^T)n + f(A) + f(B)**

Verification: expand both sides using f(R,n) = 1 - n^T R n:

LHS = 2 + n^T D n + n^T ADB^T n - n^T A n - n^T B n - n^T AD n - n^T DB^T n

n^T(I-A)D(I-B^T)n = n^T D n - n^T DB^T n - n^T AD n + n^T ADB^T n

Adding f(A) + f(B) = 2 - n^T A n - n^T B n gives the same expression. ✓

**[VERIFIED]** Maximum discrepancy < 3 × 10^{-15} over 100,000 tests.

**(b) Cauchy-Schwarz inequality.**

|n^T(I-A)D(I-B^T)n| ≤ |(I-A)n| · |D(I-B^T)n|

Since D is orthogonal: |D(I-B^T)n| = |(I-B^T)n|.

And |(I-R)n|² = n^T(I-R)^T(I-R)n = n^T(2I - R - R^T)n = 2(1 - n^T R n) = 2f(R,n).

Therefore: |n^T(I-A)D(I-B^T)n| ≤ √(2f(A)) · √(2f(B)) = 2√(f(A)f(B))

**[VERIFIED]** Maximum ratio |cross|/bound = 1.000000 over 500,000 tests (Cauchy-Schwarz is tight).

**(c) AM-GM.**

Expression ≥ f(A) + f(B) - 2√(f(A)f(B)) = (√f(A) - √f(B))² ≥ 0. **∎**

### 3.5 Step 5 — Assembly

**[VERIFIED]** Apply the Combined Bound Lemma to each group:

- **group_02**: Apply with A = R_0, B = R_2, D = D_{02}. Result: ≥ 0.
- **group_13**: Apply with A = R_1, B = R_3, D = D_{13}. Result: ≥ 0.
- **group_active**: Sum of 16 non-negative f-terms. Result: ≥ 0.

Therefore: 64I - M = 2 × (≥0 + ≥0 + ≥0) ≥ 0, i.e., **lambda_max(M_total) ≤ 64. ∎**

Verified over 100,000 random configs: min(group_02) = 0.000220, min(group_13) = 0.000628, min(group_active) = 2.741. **0 violations.**

---

## Stage 4: Additional Results

### 4.1 Three Unit Vectors Lemma (proved for completeness)

**[VERIFIED]** For unit vectors n, p, q ∈ R³: p·q ≥ 4(n·p) + 4(n·q) - 7.

This gives f(AB) ≤ 4f(A) + 4f(B), which alone proves the D=I case but is insufficient for general D.

**Proof:** Let u = 1 - n·p, v = 1 - n·q ∈ [0,2]. Need: 3u + 3v + uv ≥ √(u(2-u)v(2-v)). Squaring: LHS² - RHS = 9u² + 14uv + 9v² + 8u²v + 8uv² ≥ 0 (sum of non-negative terms).

### 4.2 Subadditivity and inactive-net conditions FAIL individually

**[COMPUTED]** f(AB) ≤ f(A) + f(B) fails: max ratio f(AB)/(f(A)+f(B)) ≈ 1.97.

**[COMPUTED]** f(AD) + f(DB^T) ≥ f(D) + f(ADB^T) fails: deficit up to 3.9.

But the COMBINED bound (with base-link f(A) + f(B) included) holds. The key insight is that the base-link deficiency terms provide exactly enough slack to absorb the negative inactive cross-link contributions.

### 4.3 D=I case proof (alternative, simpler)

**[VERIFIED]** For D = I: 64I - M = 2[4Σ_μ f(R_μ) + Σ_active f(R_μR_ν^T) - Σ_inactive f(R_μR_ν^T)]. By the Three Vectors Lemma, f(R_μR_ν^T) ≤ 4f(R_μ) + 4f(R_ν), so the inactive composites are absorbed by the base links, leaving 2Σ_active f(R_μR_ν^T) ≥ 0.

---

## Verification Scorecard

| Claim | Tag | Method |
|-------|-----|--------|
| M_total(I) = 64I | [VERIFIED] | Direct computation |
| lambda_max ≤ 64 (random) | [COMPUTED] | 10,000 + 100,000 random configs, 0 violations |
| lambda_max ≤ 64 (adversarial) | [COMPUTED] | 30 + 20 adversarial trials, all converge to 64.0 |
| Trace identity c + Tr(P) = 64 | [VERIFIED] | Algebraic proof + numerical check |
| Step 3 expansion | [VERIFIED] | Numerical identity check (error < 4e-14) |
| Combined Bound Lemma factorization | [VERIFIED] | Numerical identity check (error < 3e-15) |
| Cauchy-Schwarz step | [VERIFIED] | 500,000 tests, ratio ≤ 1.000 |
| AM-GM step | [VERIFIED] | Trivially true: (√a - √b)² ≥ 0 |
| Full proof assembly | [VERIFIED] | 100,000 configs, 0 violations, all 3 groups ≥ 0 |
| Three Vectors Lemma | [VERIFIED] | Algebraic proof + 1,000,000 numerical tests |

---

## Code

- `code/stage1_compute_mtotal.py` — Basic computation and verification of M_total
- `code/stage2_saturation_analysis.py` — Saturation manifold and c+Tr(P)=64 identity
- `code/stage3_proof_attempt.py` — D=I formula and coefficient structure
- `code/stage3b_proof_lemma.py` — Three Vectors Lemma and subadditivity tests
- `code/stage3c_combined_bound.py` — Combined bound discovery and budget analysis
- `code/stage4_complete_proof.py` — **Complete proof: factorization, C-S, AM-GM, assembly**
