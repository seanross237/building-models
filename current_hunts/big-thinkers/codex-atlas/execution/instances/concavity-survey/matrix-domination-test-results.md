# Matrix Domination Test: H(I) >= H(Q) as PSD Ordering

**Date:** 2026-03-29
**System:** L=2 hypercubic torus, SU(2) Wilson action, beta=1.0
**Test:** Is H(I) - H(Q) positive semidefinite for random Q in SU(2)^E?

---

## Executive Summary

**Matrix domination H(I) >= H(Q) is FALSE.** It fails for 100% of random configurations in all dimensions tested. The violation is large (min eigenvalue of H(I)-H(Q) approximately -1 to -1.6) and universal.

However, two weaker orderings DO hold:

1. **Weak majorization** (partial sums of sorted eigenvalues): HOLDS in 0 violations across 2300+ samples across d=2,3,4. Margins are comfortable (tightest margin ~0.25 in d=2, growing to ~1.5 in d=4).

2. **Eigenvalue-by-eigenvalue ordering** (sorted descending): HOLDS perfectly in d=4 (0/200 violations) and d=3 (only 5/500 violations, all at the zero-eigenvalue boundary). Fails more frequently in d=2 (457/500).

**This closes the matrix domination path (Approach 1 from the concavity survey) but opens majorization as the next proof target.**

---

## 1. Sanity Checks (PASSED)

All sanity checks passed before running the main test.

### Eigenvalue verification at Q=I

| d | DOF | Plaquettes | lambda_max(H(I)) | Expected | Match | H_norm(I) | Expected |
|---|-----|------------|-------------------|----------|-------|-----------|----------|
| 2 | 24  | 4          | 2.000000          | 2.0      | YES   | 0.125000  | 1/8      |
| 3 | 72  | 24         | 3.000000          | 3.0      | YES   | 0.093750  | 3/32     |
| 4 | 192 | 96         | 4.000000          | 4.0      | YES   | 0.083333  | 1/12     |

The formula lambda_max(H(I)) = d*beta is confirmed exactly, matching the Fourier analysis proof in `fourier-hessian-proof-q-identity.md`.

### Finite-difference verification (d=2)

| Config | |H_analytical - H_FD| |
|--------|----------------------|
| Q = I  | 4.14e-08             |
| Q = random | 1.05e-07         |

The analytical Hessian formula is verified against finite differences to machine precision.

---

## 2. Matrix Domination Test: H(I) - H(Q) >= 0

### Result: FAILS UNIVERSALLY

| d | Samples | PSD violations | Violation rate | min(min_eig) | mean(min_eig) | max(min_eig) |
|---|---------|---------------|----------------|--------------|---------------|--------------|
| 2 | 1000    | **1000**      | **100%**       | -1.529       | -0.856        | -0.206       |
| 3 | 1000    | **1000**      | **100%**       | -1.648       | -1.160        | -0.766       |
| 4 | 500     | **500**       | **100%**       | -1.631       | -1.314        | -1.000       |

Every single random configuration produces a negative eigenvalue in H(I) - H(Q). The violations are O(1), not numerical noise.

### Distribution of min eigenvalue of H(I) - H(Q)

**d=2:**
| Percentile | Value |
|-----------|-------|
| 0th       | -1.529 |
| 5th       | -1.192 |
| 25th      | -0.996 |
| 50th      | -0.867 |
| 75th      | -0.715 |
| 95th      | -0.510 |
| 100th     | -0.206 |

**d=3:**
| Percentile | Value |
|-----------|-------|
| 0th       | -1.648 |
| 5th       | -1.389 |
| 25th      | -1.257 |
| 50th      | -1.161 |
| 75th      | -1.062 |
| 95th      | -0.911 |
| 100th     | -0.766 |

**d=4:**
| Percentile | Value |
|-----------|-------|
| 0th       | -1.631 |
| 5th       | -1.491 |
| 25th      | -1.383 |
| 50th      | -1.314 |
| 75th      | -1.246 |
| 95th      | -1.151 |
| 100th     | -1.000 |

Note: the distribution narrows and shifts toward -1 as d increases. In d=4, even the mildest violation has min_eig = -1.000.

### Anti-Instanton Configurations (d=4)

| Axes assignment | lambda_max(H(Q)) | min_eig(H(I)-H(Q)) | PSD? |
|-----------------|-------------------|---------------------|------|
| (0,0,2,1)       | 2.000             | -1.000              | NO   |
| (1,1,0,2)       | 2.000             | -1.000              | NO   |
| (0,0,1,2)       | 2.000             | -1.000              | NO   |
| (0,1,2,0)       | 2.000             | -1.000              | NO   |

Anti-instantons have exactly min_eig = -1.000, with lambda_max(H(Q)) = 2.0 (half of H(I)'s 4.0). Despite having much lower top eigenvalue, they still violate PSD domination.

---

## 3. Violation Mechanism

### What the violating direction looks like

For representative violations at d=4:

| Trial | min_eig(H(I)-H(Q)) | v^T H(I) v | v^T H(Q) v | Excess | Avg plaq trace |
|-------|--------------------:|------------:|------------:|-------:|---------------:|
| 0     | -1.409              | 0.267       | 1.677       | 1.409  | -0.068         |
| 1     | -1.263              | 0.189       | 1.453       | 1.263  | 0.021          |
| 9     | -1.557              | 0.260       | 1.817       | 1.557  | 0.090          |

**Key insight:** The violating eigenvector v has v^T H(I) v close to 0 (it lies in or near the kernel of H(I)), but v^T H(Q) v is O(1.5). The Hessian at random Q activates directions that are flat at Q=I.

**Physical interpretation:** At flat connection Q=I, the kernel of the Hessian corresponds to pure gauge directions. At non-flat Q, the gauge symmetry is broken, and the Hessian has nonzero curvature in those formerly-flat directions. The "commutator cross terms" (documented in `hessian-analytical-formula-c-decomposition.md`) generate this curvature.

---

## 4. Eigenvalue-by-Eigenvalue Ordering

### Result: MIXED — holds strongly in d=4, weakly in d=3, fails in d=2

| d | Samples | Violations | Violation rate | Violated ranks |
|---|---------|-----------|----------------|---------------|
| 2 | 500     | 457       | 91.4%          | 9 out of 24 (ranks 3,4,9-15) |
| 3 | 500     | 5         | 1.0%           | 2 out of 72 (ranks 42,43) |
| 4 | 200     | 0         | 0%             | None |

**d=2 details:** Violations are concentrated at ranks where eig_I = 0 (the kernel). The kernel dimension of H(I) is large relative to total DOF (24), so H(Q) easily exceeds H(I) at those ranks.

**d=3 details:** Only 5 violations, all at ranks 42-43 (again at the zero eigenvalue boundary). Worst violation magnitude: -0.034.

**d=4 details:** Zero violations in 200 random configs. Eigenvalue-by-eigenvalue ordering appears to hold perfectly in d=4.

---

## 5. Weak Majorization

### Result: HOLDS in all dimensions

| d | Samples | Violations | Tightest margin | At index |
|---|---------|-----------|-----------------|----------|
| 2 | 1000    | 0         | 0.253           | m=0      |
| 3 | 1000    | 0         | 1.060           | m=0      |
| 4 | 300     | 0         | 1.543           | m=0      |

Weak majorization: for all m = 1, ..., Ndof,

    sum_{k=1}^m lambda_k(H(Q)) <= sum_{k=1}^m lambda_k(H(I))

where eigenvalues are sorted in descending order.

The tightest margin occurs at m=0 (just the top eigenvalue), which is exactly the statement lambda_max(H(Q)) <= lambda_max(H(I)). The margin grows with dimension, suggesting the result becomes MORE robust in higher d.

Anti-instanton configs also satisfy majorization with comfortable margin (2.0 at m=0 in d=4).

---

## 6. Implications

### For the concavity survey proof strategy

1. **Matrix domination (Approach 1): CLOSED.** H(I) >= H(Q) as a matrix inequality is false. This path cannot produce a proof.

2. **Majorization (Approach 2): OPEN and promising.** Weak majorization holds in 2300+ samples with zero violations and comfortable margins. This is strictly weaker than PSD domination but still implies lambda_max(H(Q)) <= lambda_max(H(I)) directly.

3. **Eigenvalue-by-eigenvalue ordering:** An intermediate result. Holds strongly in d=4 (the target dimension) but the proof may not need it — majorization suffices.

### For the Hessian bound proof

The failure of matrix domination means:
- A proof via "H(I) - H(Q) = sum of PSD terms" is impossible
- The D + C decomposition cannot be used to show PSD domination directly
- Any proof of lambda_max(H(Q)) <= lambda_max(H(I)) must work at the level of eigenvalues (Weyl inequalities, trace inequalities, or majorization theory), NOT at the matrix level

The success of majorization means:
- The eigenvalue spectrum of H(Q) is "dominated" by H(I) in a cumulative sense
- This is consistent with the "plaquette destructive interference" picture: away from flat, contributions partially cancel, reducing ALL eigenvalues cumulatively (though not all individually)
- A proof via Schur convexity or trace/moment inequalities may be possible

### Recommended next step

**Numerical Step A2:** Investigate why majorization holds. Compute the moments Tr(H(Q)^k) for k=1,2,3,... and compare to Tr(H(I)^k). If H(I) dominates all moments, this gives a proof path via the moment characterization of majorization.

**Analytical Step A3:** Check whether the Schur-Horn theorem, combined with gauge orbit analysis, can prove majorization. The fact that PSD fails but majorization holds suggests the majorization comes from a trace-level identity (like Tr(H(Q)) <= Tr(H(I))), not from a matrix-level one.

---

## 7. Technical Details

### Code

- `matrix_domination_test.py`: Main test (1000 random configs per dimension)
- `matrix_domination_followup.py`: Eigenvalue-by-eigenvalue, majorization, anti-instanton, violation characterization

### Hessian formula

The Hessian is computed using the product-of-exponentials formula, verified against finite differences (error < 1e-7). Under left perturbation Q_k -> exp(t*v_k) Q_k:

    d^2 S/dt^2 = -(beta/2) sum_P [sum_k Re Tr(w_k^2 U_P) + 2 sum_{k<l} Re Tr(w_k w_l U_P)]

where w_k = s_k Ad_{P_k}(v_{e_k}) are the parallel-transported tangent vectors. This formula includes both the B^2 (diagonal) and commutator (cross) terms.

### Verification chain

1. SU(2) generators verified anti-Hermitian
2. Hessian at Q=I matches exact formula: lambda_max = d*beta, H_norm = d/(4(d-1)N^2)
3. Analytical Hessian matches finite-difference Hessian to O(1e-7)
4. Random Q check: lambda_max(H(Q)) < lambda_max(H(I)) confirmed before running sweep
