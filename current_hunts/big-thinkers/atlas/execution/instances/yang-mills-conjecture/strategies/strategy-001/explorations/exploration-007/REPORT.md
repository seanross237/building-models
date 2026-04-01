# Exploration 007: ADVERSARIAL REVIEW — Independent Verification of Conjecture 1 Proof

## Verdict: CONDITIONAL PASS

The core algebraic proof (Steps 1-5) for the per-vertex bound lambda_max(M_total) <= 64 on L=2 is **correct**. All algebraic identities, the Combined Bound Lemma, and the expansion are verified numerically with high precision. However, the chain from this per-vertex bound to the full Conjecture 1 (lambda_max(M(Q)) <= 16 for all Q on all L) has **two gaps** that are not addressed by the proof:

1. **Full matrix vs staggered mode**: The proof only bounds the staggered mode Rayleigh quotient, not the full operator norm.
2. **Odd L sign structures**: The proof formula is specific to even L. On odd L (e.g., L=3), some vertices have different sign structures that the proof doesn't handle.

Both gaps are supported numerically (no violations found in extensive testing), but the analytical proof does not close them.

---

## Task 1: Independent Re-implementation

### 1a. Lattice construction (L=2, d=4)

**[COMPUTED]** Built the d=4 hypercubic torus with L=2 independently. Verified:
- 16 vertices, 64 edges, 96 plaquettes ✓
- Each plaquette has a unique base vertex (96 unique assignments) ✓
- Code: `code/task1_lattice_and_Bsq.py`

### 1b. B_square formula and staggered mode

**[COMPUTED]** Implemented B_sq(Q,v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4}) from scratch.

At identity: M_stag has eigenvalues (1024, 1024, 1024). Since |v|^2 = 64, the Rayleigh quotient is 1024/64 = 16. ✓

### 1c. Per-vertex bound F_x <= 64|n|^2

**[COMPUTED]** Over 200 random configs × 16 vertices = 3200 tests on L=2: max F_x/(64|n|^2) = **0.735**. Zero violations.

### 1d. Sum identity

**[COMPUTED]** |Sum_x F_x - n^T M_stag n| < 2.3e-13 over 100 tests. The partition by base vertex is exact.

### 1e. Full 192×192 matrix M(Q)

**[COMPUTED]** Built the FULL M(Q) matrix independently (code: `code/task1b_full_matrix.py`).

**At identity:**
- Eigenvalues: {0, 4, 8, 12, 16} with multiplicities {57, 36, 54, 36, 9}
- lambda_max = 16.000000 exactly
- Top eigenspace is 9-dimensional; staggered modes are a 3-dimensional subspace
- Singular values of staggered-vs-top-eigenspace overlap: (1.0, 1.0, 1.0) — staggered is fully contained in the top eigenspace ✓

**200 random configs:**
- Max lambda_max(full M) = **14.41** (all below 16)
- Full matrix violations (> 16): **0**
- Staggered Rayleigh quotient always ≤ full lambda_max (as expected) ✓

---

## Task 2: Check the Cube-Face Reduction (Step 0)

**[COMPUTED]** Each plaquette has a unique base vertex. The 96 plaquettes on L=2 partition into 16 vertices × 6 plaquettes each. Verified: Sum_x F_x = n^T M_stag n to precision 2.3e-13.

**[CHECKED]** The reduction argument is:
- If F_x <= 64|n|^2 for all x, Q, then Sum_x F_x <= 64 × L^d × |n|^2 = 4d × |v|^2
- This gives: staggered Rayleigh quotient <= 4d = 16

This reduction is **valid** for the staggered mode. However, it only bounds v^T M v / |v|^2 for staggered v. The full conjecture lambda_max(M(Q)) <= 16 requires bounding ALL eigenvectors, not just staggered modes. See Task 7 for analysis.

---

## Task 3: Check the Sign Structure (Step 1)

### 3a. Sign enumeration

**[VERIFIED]** For each plaquette (mu,nu), the 6 cross-term signs are determined by ab = (-1)^{mu+nu+1}:
- If ab = +1 (active plane): all 6 signs positive
- If ab = -1 (inactive plane): 2 positive, 4 negative

Active planes: (0,1), (0,3), (1,2), (2,3) — 4 planes with 24 positive terms
Inactive planes: (0,2), (1,3) — 2 planes with 4 positive, 8 negative terms

**Total: 28 positive, 8 negative. Net Σ σ_k = 20.** ✓

c + Tr(P) = 24 + 2×20 = 64 ✓

### 3b. Sign structure consistency across vertices

**[VERIFIED]** On L=2, the sign structure is the SAME for all 16 vertices (up to an overall sign that cancels in |B|^2). This is because on L=2, adding 1 to any coordinate always flips its parity.

**[COMPUTED]** On L=3, there are **8 distinct sign structures** across the 81 vertices. Some vertices have 3 or 4 inactive planes instead of 2. See Task 6 for details.

Code: `code/task345_core_proof.py`

---

## Task 4: Check the Expansion (Step 3)

### 4a. Expansion verification

**[VERIFIED]** Independently derived and verified:

64 - n^T M_total n = 2 × [group_02 + group_13 + group_active]

where:
- group_02 = f(R0) + f(R2) + f(R0 D02) + f(D02 R2^T) - f(D02) - f(R0 D02 R2^T)
- group_13 = f(R1) + f(R3) + f(R1 D13) + f(D13 R3^T) - f(D13) - f(R1 D13 R3^T)
- group_active = Σ_{active} [f(R_mu D) + f(D) + f(R_mu D R_nu^T) + f(D R_nu^T)]

**Max |LHS - RHS| over 100,000 tests: 4.26e-14** ✓

### 4b. Group non-negativity

**[COMPUTED]** Over 100,000 random configs:
- Min group_02 = 0.000731 ≥ 0 ✓
- Min group_13 = 0.000089 ≥ 0 ✓
- Min group_active = 4.675 ≥ 0 ✓ (trivially, since all 16 terms are f(rotation, n) ≥ 0)

### 4c. Algebraic verification of grouping

**[VERIFIED]** The grouping works because:
1. Each active plaquette contributes f(R_mu) + f(R_nu) base-link terms (sign +1)
2. Each inactive plaquette needs f(R_mu) + f(R_nu) to complete the Combined Bound
3. Active plaquettes provide 2×f(R_mu) for each base link (budget), while inactive plaquettes need 1×f(R_mu) each (demand)
4. Budget ≥ demand for all base links on the standard (4+/2-) sign structure ✓

Code: `code/task345_core_proof.py`

---

## Task 5: Check the Combined Bound Lemma (Step 4)

### 5a. Algebraic identity

**[VERIFIED]** f(A) + f(B) + f(AD) + f(DB^T) - f(D) - f(ADB^T) = n^T(I-A)D(I-B^T)n + f(A) + f(B)

Both sides expand to: 2 - n^T A n - n^T B n + n^T D n - n^T AD n - n^T DB^T n + n^T ADB^T n

**Max error over 100,000 tests: 2.66e-15** ✓

### 5b. Cauchy-Schwarz step

**[VERIFIED]** |n^T(I-A)D(I-B^T)n| ≤ |(I-A^T)n| · |D(I-B^T)n| = √(2f(A)) · √(2f(B)) = 2√(f(A)f(B))

Key sub-steps:
- n^T R n = n^T R^T n (trivially true: a scalar equals its transpose) ✓
- |(I-R^T)n|^2 = 2f(R,n): max error 3.55e-15 over 100k tests ✓
- |D w| = |w| since D is orthogonal ✓

**Max ratio |cross|/bound over 200,000 tests: 0.9999964** (Cauchy-Schwarz tight but not violated) ✓

### 5c. AM-GM step

**[VERIFIED]** f(A) + f(B) - 2√(f(A)f(B)) = (√f(A) - √f(B))^2 ≥ 0. Trivially true.

### 5d. f(R,n) ≥ 0

**[VERIFIED]** Min f(R,n) = 0.0000057 over 500,000 tests. Analytically: f(R,n) = 1 - n^T R n where n^T R n = n^T((R+R^T)/2)n and symmetric part has eigenvalues {1, cos θ, cos θ} ∈ [-1, 1]. So f(R,n) ∈ [0, 2]. ✓

### 5e. Adversarial search

**[COMPUTED]** Gradient descent adversarial search (200 random starts, 3000 steps each): minimum combined bound value found > 0. No violations.

---

## Task 6: Check L-dependence

### 6a. Even L

**[VERIFIED]** For L=2 and L=4, all vertices have the SAME sign structure (4 positive, 2 negative planes). The proof formula A = a(I + R_mu D) + b(R_mu + R_mu D R_nu^T) matches the actual lattice computation to machine precision (error < 1.42e-14). The proof is **valid for all even L**.

Code: `code/task6c_correct_pervertex.py`

### 6b. Odd L (L=3): PROOF FORMULA MISMATCH

**[COMPUTED]** On L=3, vertices are classified into 8 distinct sign structures based on which coordinates equal L-1 = 2. The proof's formula A = a(I + R_mu D) + b(R_mu + R_mu D R_nu^T) does NOT match the actual lattice computation for vertices where some coordinate = 2.

**Max discrepancy: 31.8** (not a rounding error — a genuine formula mismatch)

Root cause: On L=2, (x_mu + 1) mod L always changes parity, giving -s3 = s1 and -s4 = s2 (the pairing that enables the proof's A-matrix formula). On L=3, when x_mu = 2, (2+1) mod 3 = 0 does NOT change parity, breaking the pairing.

For even L, (x_mu + 1) mod L always changes parity (since L is even), so the pairing holds for all vertices. **The proof is specific to even L.**

### 6c. Per-vertex bound on L=3 (actual lattice)

**[COMPUTED]** Despite the formula mismatch, the per-vertex bound F_x <= 64 DOES hold numerically on L=3:
- Interior vertices (all coords < 2): max lambda = 52.60 ✓
- Boundary vertices (some coord = 2): max lambda = 56.68 ✓

All values well below 64. But the proof doesn't cover boundary vertices on odd L.

### 6d. Full matrix on L=3

**[COMPUTED]** L=3, d=4 (972×972 matrix):
- Identity: lambda_max = 12.0 (spectrum {0, 3, 6, 9, 12})
- Random configs: lambda_max ≤ 14.13
- No violations of bound 16

Code: `code/task6_L_dependence.py`, `code/task6b_sign_structures.py`

---

## Task 7: Check the Full Chain

### 7a. Per-vertex bound → staggered mode bound

**[VERIFIED]** If lambda_max(M_total) <= 64 for all vertices and all Q, then:
- Sum_x F_x <= 64 × L^d × |n|^2
- = 4d × (d × L^d × |n|^2) = 4d × |v|^2
- So staggered Rayleigh quotient = Sum F_x / |v|^2 <= 4d = 16

This step is logically correct. ✓

### 7b. Staggered mode bound → full operator bound (GAP)

**[CONJECTURED]** The proof claims lambda_max(M(Q)) <= 16 follows from the staggered mode bound. This requires that non-staggered modes also have Rayleigh quotient ≤ 16.

Evidence:
- At Q=I: top eigenspace is 9-dimensional, containing the 3-dimensional staggered subspace. All 9 modes have eigenvalue 16. ✓
- Near identity (epsilon perturbation): lambda_max decreases monotonically from 16 as epsilon increases ✓
- For random Q: max lambda_max(full M) = 14.41 (well below 16) over 200 tests ✓
- The staggered Rayleigh quotient is always ≤ the full lambda_max ✓

The full operator bound holds numerically, but the proof does not establish it analytically. The proof would need either:
(a) A separate bound on non-staggered modes, or
(b) A proof that Q=I is the global maximizer of lambda_max(M(Q)), or
(c) A matrix inequality showing M(Q) ≤ 16I as an operator (which is stronger than the per-vertex bound)

### 7c. Nature of the top eigenspace at identity

**[COMPUTED]** The 9-dimensional eigenvalue-16 subspace at Q=I contains:
- 3 staggered modes (overlap singular values: 1.0, 1.0, 1.0)
- 6 non-staggered modes (NOT constant modes, NOT single-direction Fourier modes)

The non-staggered modes are more complex lattice modes that achieve the same Rayleigh quotient 16 at identity but are not addressed by the per-vertex bound argument.

Code: `code/task7_full_chain.py`

---

## Errors Found

### GAP 1 (Moderate): Full matrix vs staggered mode reduction

**Severity: MODERATE.** The proof establishes the staggered mode Rayleigh quotient ≤ 16 but does not prove lambda_max(M(Q)) ≤ 16 for the full operator. The 9-dimensional top eigenspace at identity includes 6 non-staggered modes not covered by the per-vertex argument. Numerically, all modes are bounded by 16 (0 violations in 200+ tests).

**Impact:** The proof proves a weaker statement than Conjecture 1. It would be sufficient if the conjecture only concerns staggered modes, but Conjecture 1 as stated is about the full operator.

### GAP 2 (Minor for physical applications): Odd L sign structures

**Severity: MINOR (for even L) / MODERATE (for odd L).** The proof's M_total formula is specific to even L. On odd L (e.g., L=3), vertices where some coordinate = L-1 have a different sign structure and the formula fails (max error ~32). The proof is valid for all even L.

**Impact:** For the physically relevant limit L → ∞ (typically taken through even L), this gap is irrelevant. For a proof valid on all lattice sizes, additional work is needed.

### NO ERRORS in core proof steps

The algebraic content of Steps 1-5 is correct:
- Sign structure: correct
- Trace identity: correct
- Expansion: correct
- Combined Bound Lemma: correct (algebraic identity, Cauchy-Schwarz, AM-GM all verified)
- Assembly: correct

---

## Verification Scorecard

| Claim | Tag | Method | Confidence |
|-------|-----|--------|------------|
| Lattice construction (16V, 64E, 96P) | [VERIFIED] | Direct computation | 100% |
| M_stag(I) = 1024 I | [VERIFIED] | Direct computation | 100% |
| Per-vertex F_x ≤ 64 on L=2 | [COMPUTED] | 3200 tests, 0 violations | 99%+ |
| Sum_x F_x = n^T M n | [VERIFIED] | Identity to 2.3e-13 | 100% |
| Full M(Q) has lambda_max ≤ 16 on L=2 | [COMPUTED] | 200 tests, 0 violations | 95%+ |
| Sign count: 28 pos, 8 neg, net 20 | [VERIFIED] | Enumeration | 100% |
| c + Tr(P) = 64 | [VERIFIED] | Algebraic proof + numerical | 100% |
| Expansion of 64I - M | [VERIFIED] | 100k tests, error < 4.3e-14 | 100% |
| Combined Bound Lemma factorization | [VERIFIED] | 100k tests, error < 2.7e-15 | 100% |
| Cauchy-Schwarz step | [VERIFIED] | 200k tests, ratio < 1.0 | 100% |
| AM-GM step | [VERIFIED] | Trivially true | 100% |
| All 3 groups ≥ 0 | [COMPUTED] | 100k tests, 0 violations | 99%+ |
| Proof formula matches L=2 lattice | [VERIFIED] | 1600 tests, error < 1.4e-14 | 100% |
| Proof formula FAILS for L=3 boundary verts | [VERIFIED] | Error up to 31.8 | 100% |
| Proof formula matches L=4 lattice | [VERIFIED] | 1600 tests, error < 1.4e-14 | 100% |
| Per-vertex bound holds on L=3 | [COMPUTED] | 500 × 81 tests, max lambda < 57 | 95%+ |
| Full M has lambda_max ≤ 16 on L=3 | [COMPUTED] | 5 tests, max 14.13 | 90% |
| Staggered modes ⊂ top eigenspace at Q=I | [VERIFIED] | SVD overlap = (1,1,1) | 100% |
| Full M → staggered reduction | [CONJECTURED] | Not proven; numerically supported | — |

**Totals: 13 VERIFIED, 5 COMPUTED, 1 CONJECTURED**

---

## Code

- `code/task1_lattice_and_Bsq.py` — Independent lattice construction and B_sq verification
- `code/task1b_full_matrix.py` — Full 192×192 M(Q) matrix construction and eigenvalue analysis
- `code/task345_core_proof.py` — Sign structure, expansion, and Combined Bound Lemma verification
- `code/task5b_adversarial_short.py` — Adversarial gradient descent search for lemma violations
- `code/task6_L_dependence.py` — L=2 and L=3 lattice comparison
- `code/task6b_sign_structures.py` — Sign structure classification across L values
- `code/task6c_correct_pervertex.py` — Verification that proof formula matches lattice for even/odd L
- `code/task7_full_chain.py` — Full eigenspace analysis and chain verification
