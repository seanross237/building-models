# Exploration 006: Adversarial Review of Complete Proof Chain

## Verdict: CONDITIONAL PASS — LOGICAL GAP IN PART C

The per-vertex proof (Parts A+B, Steps B1-B9) is **correct and independently verified**. Every identity holds to < 3e-12, every claimed inequality holds with 0 violations across thousands of tests.

**However, the upstream connection (Part C) contains a genuine logical gap:** the proof bounds the staggered Rayleigh quotient v^T M(Q) v ≤ 16|v|^2 for v in the 9D staggered subspace, but claims this implies lambda_max(M(Q)) ≤ 16 over the full 192D space. This step is invalid — for random Q, the top eigenvector of M(Q) is almost entirely NON-staggered (staggered projection < 0.5), and the non-staggered eigenvalue (up to 14.6) is NOT constrained by the proof.

The final bound lambda_max(M(Q)) ≤ 16 **appears numerically true** (0 violations in 700+ tests including gradient ascent), but the proof chain does not establish it.

---

## Stage 1: Independent Verification of Identities B1-B9 [ALL VERIFIED]

Fresh code written from scratch. See `code/verify_all_identities.py`, `code/verify_B6_fixed.py`.

| Step | Claim | Trials | Max Error | Min Value | Status |
|------|-------|--------|-----------|-----------|--------|
| B1 | 16\|\|T\|\|² = 4Σ\|T_mu-T_nu\|² | 1000 | 1.1e-13 | — | **[VERIFIED]** |
| B2 | Per-plaquette identity | 1000 | 6.3e-13 | — | **[VERIFIED]** |
| B3 | 16\|\|T\|\|² - F_x = 2Σf + sum_S | 500 | 2.2e-12 | — | **[VERIFIED]** |
| B4 | sum_S(D=I) = 6Σf+\|Σa\|² ≥ 0 | 500 | 0 | 0.60 | **[VERIFIED]** |
| B5 | sum_S = baseline + Σ 2u^T(I-D)v | 500 | 3.2e-12 | — | **[VERIFIED]** |
| B6 | \|B\|² = \|p\|²+\|v\|²+2p^TRDv | 2000 | 1.6e-12 | — | **[VERIFIED]** |
| B7 | u^T Dv ≤ \|\|u\|\|·\|\|v\|\| (SO(3)) | 6000 | 0 | — | **[VERIFIED]** |
| B8 | Σ\|\|u-v\|\|² = 4Σf+\|Σa\|² | 1000 | 3.4e-13 | — | **[VERIFIED]** |
| B9 | F = 2Σf + Σ(·)² ≥ 0 | 1000 | 3.5e-13 | 0.21 | **[VERIFIED]** |
| — | Full gap F_x ≤ 16\|\|T\|\|² | 500 | — | 2.65 | **[VERIFIED]** |
| — | sum_S ≥ 0 | 1000 | — | 1.29 | **[VERIFIED]** |

**B6 subtlety:** F_x is affine in D only for orthogonal D (where D^TD=I makes the quadratic term |Dv|²=|v|² constant). Tested correctly via the identity |B|²=|p|²+|v|²+2p^TRDv. [VERIFIED]

---

## Stage 2: Adversarial Attack on Per-Vertex Bound [NO VIOLATIONS]

`code/adversarial_gradient_ascent.py`:

- **Extreme configs** (all-180°, all-(-I), ±90°): lambda_max = 16.000 (all gauge-equivalent to Q=I)
- **Near-identity** (eps=0.01-2.0): lambda_max smoothly decreases from 16 to 14.25
- **Gradient ascent** (20 starts × 80 steps): best lambda_max = **14.36**, gap 1.64 from bound
- **Per-vertex** (50 Q × 16 vertices): max F_x/(16||T||²) = 0.32

**Per-vertex bound is correct and has large safety margin.** [VERIFIED]

---

## Stage 3: Upstream Connection (Part C) — CRITICAL GAP FOUND

### 3a. Double Counting: NO ISSUE [VERIFIED]

|sum_x F_x - v^T M(Q) v| < 4.6e-13 over 100 tests. Each plaquette counted once at its base vertex. No double counting. `code/upstream_and_full_matrix.py`.

### 3b. Full Matrix Eigenvalues at Q=I [VERIFIED]

L=2, d=4: M(I) eigenvalues = {0(×57), 4(×36), 8(×54), 12(×36), 16(×9)}.
- Top eigenspace (eigenvalue 16) IS the 9D staggered subspace ✓
- Next eigenvalue is 12 (gap = 4) ✓
- Total dimension: 192 ✓

### 3c. THE GAP: Staggered Bound Does Not Imply Full lambda_max Bound [FOUND]

**The proof establishes:** v^T M(Q)v ≤ 16|v|² for all v in the 9D staggered subspace P.

**The proof claims:** Therefore lambda_max(M(Q)) ≤ 16.

**This is INVALID.** lambda_max = max over ALL 192D vectors, not just P.

**Quantitative evidence (`code/analyze_gap_and_normalization.py`):**

| Quantity | Q=I | Random Q (200 tests) |
|----------|-----|---------------------|
| Staggered eigenvalue | 16.0 | max 9.5, mean 8.4 |
| Non-staggered max eigenvalue | 12.0 | max 14.6, mean 14.1 |
| Full lambda_max | 16.0 | max 14.5, mean 14.1 |
| Top eigenvector staggered projection | 1.0 | 0.19–0.48 |
| Non-stag > stag? | No | **100% of trials** |

**Key finding:** For ALL 200 random Q, the top eigenvector is predominantly NON-staggered. The non-staggered eigenvalue (14.6 max) is the binding constraint, not the staggered one (9.5 max). The per-vertex proof is bounding the WRONG subspace for non-trivial Q.

### 3d. Momentum Decomposition at Q=I [VERIFIED]

L=2 momenta k ∈ {0,π}^4 with eigenvalue = 4·(# of π-components):

| Momentum class | Eigenvalue | Count | Multiplicity |
|---------------|------------|-------|-------------|
| k = (0,0,0,0) | 0 | 1 | 12 |
| 1 component = π | 4 | 4 | 36 |
| 2 components = π | 8 | 6 | 54 |
| 3 components = π | 12 | 4 | 36 |
| k = (π,π,π,π) | 16 | 1 | 9+3 |

The non-staggered eigenvalue 12 (from k with 3 π-components) grows to 14.6 as Q deviates from I. This is NOT constrained by the proof.

### 3e. Lattice Formula Consistency [VERIFIED]

Per-vertex formula exactly matches lattice B-field computation. Cross-link mapping D_{mu,nu} = Q_{x+mu,nu} · Q_{x+nu,mu}^T verified to 5.7e-14. Sign structure for even-parity vertices verified. `code/verify_per_vertex_on_lattice.py`.

---

## Stage 4: Odd L Check

### L=3, d=4 [COMPUTED]

`code/focused_adversarial.py`:

- **Q=I eigenvalues:** {0(×252), 3(×72), 6(×216), 9(×288), 12(×144)}. lambda_max = **12.0** (not 16!)
- **Eigenvalue formula:** 4d·sin²(π/L) = 16·(3/4) = 12 for L=3 (max at k=2π/3)
- **Random Q (30 tests):** max lambda_max = **14.1**, 0 violations of 16
- **Staggered vector at L=3:** NOT a single momentum mode (period-2 pattern doesn't divide L=3)

The per-vertex bound F_x ≤ 16||T||² still holds at L=3 (proved for any Q, independent of L). But the staggered Rayleigh quotient at Q=I is NOT 16 — it's some average over momentum modes. The bound 16 is even more slack than at L=2.

---

## Stage 5: Full Matrix Stress Test

**L=2 (192×192): 500+ configurations, 0 violations.** [COMPUTED]

- Random: max lambda_max = 14.66 (200 tests)
- Adversarial gradient ascent: best = 14.36 (20 starts × 80 steps)
- Extreme configs: 16.00 (flat connections only)
- Near-identity: smooth decrease from 16.0

**L=3 (972×972): 30 configurations, 0 violations.** [COMPUTED]
- Max lambda_max = 14.10

---

## Normalization Check [CONJECTURED]

The exact SZZ Hessian norm formula requires specifying the gauge group:
- SU(2), N=2: H_norm = beta·lambda_max/(2N) = 4·beta. SZZ needs H < 1, so beta < 1/4.
- SO(3) adjoint, N=3: H_norm = 8·beta/3. Needs beta < 3/8.
- The GOAL mentions both H_norm = 1/3 (N=3 convention) and beta < 1/4 (N=2 convention).

This should be pinned down against the exact SZZ theorem statement.

---

## Summary Table

| Component | Verdict | Evidence |
|-----------|---------|----------|
| B1-B9 identities | **VERIFIED** | 500-6000 trials each, errors < 3e-12 |
| Per-vertex F_x ≤ 16\|\|T\|\|² | **VERIFIED** | 1800+ tests, 0 violations |
| No double counting | **VERIFIED** | 100 tests, error < 5e-13 |
| Lattice formula consistency | **VERIFIED** | 200 tests, error < 6e-14 |
| Staggered ⟹ full lambda_max | **FAILED** | Logical gap; non-stag eigs dominate for Q≠I |
| lambda_max(M(Q)) ≤ 16 | **[COMPUTED]** | 700+ tests (L=2,3), 0 violations |
| Odd L validity | **[COMPUTED]** | L=3 holds numerically, proof coverage unclear |
| SZZ normalization | **[CONJECTURED]** | Group convention must be specified |
