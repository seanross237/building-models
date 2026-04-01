# Exploration 007 — Adversarial Review of C1 Pair Correlation Claim

## Goal

Attack the claim: **"The C1 random-phase Von Mangoldt Hankel matrix satisfies Montgomery's pair correlation formula at the 7.9% MRD level."**

Three tests:
1. **Null matrix comparison** — Does Von Mangoldt amplitude structure matter, or does any GUE-class matrix achieve ≤10% MRD?
2. **Realization stability** — Is 7.9% a stable estimate from 5 realizations, or was it lucky?
3. **Severity table** — Systematic adversarial assessment of all attack vectors.

## Setup / Method

- N=500 Hermitian matrices
- 5 realizations for null matrices (Tests 1a-1c), 20 realizations for C1 stability (Test 2)
- Pair correlation: degree-5 polynomial unfolding, dr=0.05 bins from r=0 to r=6, MRD over r∈[0.5,4.0]
- β_Wigner: Brody distribution fit via manual grid search (scipy fallback for numpy.Inf issue)
- Code: `code/adversarial_test.py`, results in `code/results.npz`

---

## Test 1: Null Matrix Comparison [COMPUTED]

### Results Summary Table

| Matrix | MRD (5 realizations pooled) | β_Wigner | Passes ≤10% threshold |
|---|---|---|---|
| C1 (Von Mangoldt Hankel + random phases) | **7.9%** (from S002-E005) | 1.18 ± 0.22 | YES |
| GUE control (random complex Gaussian) | **7.8%** | 1.50 | YES |
| Flat-amplitude random phase | **6.8%** | 1.45 | YES |
| Flat-amplitude Toeplitz (random per-lag phase) | **9.0%** | 0.45 | YES (barely) |

All four matrix types pass the 10% MRD threshold for pair correlation (when computed as 5-realization pooled averages, as in S002-E005).

### 1a. GUE Control [COMPUTED]

A fully random N×N complex Hermitian matrix (GUE ensemble) achieves:
- **MRD = 7.8%** vs Montgomery's formula R₂(r) = 1 - (sin(πr)/πr)²
- β_Wigner = 1.50 (Brody fit; expected theoretical β=2.0 — finite-size effect at N=500)

**Interpretation:** A matrix with NO arithmetic content whatsoever achieves essentially the same pair correlation score (7.8%) as C1 (7.9%). The pair correlation pass is a generic feature of GUE-class matrices, not specific to the Von Mangoldt construction.

### 1b. Flat-Amplitude Random Phase [COMPUTED]

H_{jk} = exp(2πi φ_{jk}) for j<k, with φ_{jk} iid Uniform[0,1], H_{kj} = H^*_{jk}, H_{jj} = 0:
- **MRD = 6.8%** — BETTER than C1 (7.9%)
- β_Wigner = 1.45

**Interpretation:** Flat amplitudes with random phases achieve BETTER pair correlation than C1. The Von Mangoldt amplitude profile actually makes C1's pair correlation slightly WORSE (or at best equal), not better. The arithmetic content of the Von Mangoldt function is not helping.

### 1c. Flat-Amplitude Toeplitz Random Phase [COMPUTED]

H_{jk} = exp(2πi ψ_{|j-k|}) — one random phase per lag (Hermitian Toeplitz):
- **MRD = 9.0%** — close to threshold, still passes
- β_Wigner = 0.45 (near GOE class — factorizable phases → GOE, as expected)

**Interpretation:** Even a GOE-class matrix (Toeplitz → real-equivalent via phase factorizability) passes the pair correlation threshold. This suggests pair correlation MRD at N=500 with 5-realization averaging is an insufficiently discriminating test.

---

## Test 2: Realization Stability (20 C1 Realizations) [COMPUTED]

### C1 MRD across 20 independent N=500 realizations:

| Realization | MRD | Pass (≤10%)? |
|---|---|---|
| 1 | 12.1% | FAIL |
| 2 | 18.8% | FAIL |
| 3 | 18.2% | FAIL |
| 4 | 19.1% | FAIL |
| 5 | 13.4% | FAIL |
| 6 | 15.4% | FAIL |
| 7 | 17.0% | FAIL |
| 8 | 12.2% | FAIL |
| 9 | 15.0% | FAIL |
| 10 | 14.5% | FAIL |
| 11 | 15.0% | FAIL |
| 12 | 16.6% | FAIL |
| 13 | 15.7% | FAIL |
| 14 | 16.1% | FAIL |
| 15 | 15.9% | FAIL |
| 16 | 16.5% | FAIL |
| 17 | 15.3% | FAIL |
| 18 | 13.7% | FAIL |
| 19 | 13.5% | FAIL |
| 20 | 15.4% | FAIL |

**Summary:**
- Mean MRD = **15.5% ± 1.9%**
- Min = 12.1%, Max = 19.1%, 90th percentile = 18.3%
- **Pass rate: 0/20 (0%)** — no individual realization achieves MRD ≤ 10%

When all 20 realizations are pooled (totaling 10,000 eigenvalues), the pooled MRD = **3.7%** — excellent, because pooling 20 matrices dramatically reduces statistical noise in the pair correlation estimate.

### Interpretation

The "7.9% MRD" from S002-E005 was computed as follows:
1. Generate 5 independent C1 matrices
2. Compute R₂(r) for EACH matrix
3. **Average the 5 R₂(r) curves together** (reducing noise by ~√5)
4. Compute MRD between averaged R₂ and Montgomery formula

This is different from computing MRD per realization. The 5-realization averaging trick reduces the MRD from ~15.5% (individual) to ~7.9% (5-realization average). With 20-realization pooling, the MRD reaches 3.7%.

**The "PASS" verdict depends on sample size:** A single N=500 matrix has pair correlation noise of ~15.5% MRD on average. Only with averaging over multiple realizations does the MRD drop below 10%.

**Comparison:** The actual Riemann zeros (2000 zeros, S001) achieve 9.1% MRD. This is for the ENTIRE 2000-zero dataset treated as one set. An equivalent comparison for C1 at N=500 would use many more eigenvalues. The 20-realization pooled C1 (3.7% MRD, 10,000 eigenvalues) significantly OUTPERFORMS the actual zeros.

---

## Test 3: Severity Table

| Attack | Evidence | Severity | Verdict |
|---|---|---|---|
| **Von Mangoldt amplitude unnecessary** | Flat-amplitude (6.8%) ≤ C1 (7.9%). GUE (7.8%) ≈ C1. Amplitude removes nothing. | **SERIOUS** | ESTABLISHED |
| **7.9% MRD not stable at single-realization level** | Individual MRD mean = 15.5% ± 1.9%; 0/20 pass ≤10% threshold. | **SERIOUS** | ESTABLISHED |
| **Pair correlation insensitive to matrix type** | Even Toeplitz GOE-class matrix passes (9.0%). Test is insufficiently discriminating. | **SERIOUS** | ESTABLISHED |
| **GUE class ≠ Riemann-like** | β=1.18 (target 2.0); Δ₃=0.285 (target 0.156). Off from zeta statistics. | **MODERATE** | ESTABLISHED |
| **3/10 PASS scorecard is not strong evidence** | 3 PASS, 4 PARTIAL. Partials have significant gaps (β 1.18 vs 2.0, Δ₃ 0.285 vs 0.156). | **MODERATE** | ESTABLISHED |
| **Random phases drive the GUE class, not arithmetic** | All evidence: (i) C1 GUE-class only after switching to complex phases; (ii) arithmetic (Gauss, Dirichlet) → GOE regardless of amplitude; (iii) flat phases also GUE. | **SERIOUS** | ESTABLISHED |

### Overall Claim Assessment

The original claim: *"C1 random-phase Von Mangoldt Hankel matrix satisfies Montgomery's pair correlation formula at the 7.9% MRD level."*

**What is actually established:** The C1 construction is in the GUE universality class (confirmed by multiple statistics: spacing distribution KS=0.042, form factor shape). Matrices in the GUE class generically satisfy pair correlation at approximately 7-9% MRD when averaged over several realizations.

**What is NOT established:**
1. That the Von Mangoldt amplitude is necessary — it isn't (flat amplitudes do equally well)
2. That 7.9% is a stable, per-realization property — it's a 5-realization averaging artifact
3. That C1 "encodes" GUE statistics in an arithmetic sense — random complex phases alone are sufficient

**Restated, honest version of the claim:**
*"The C1 construction is in the GUE universality class. When pair correlation is averaged over 5+ realizations (or ~2500+ eigenvalues), it satisfies Montgomery's formula at the ~8-10% level. This is generic to any GUE-class Hermitian matrix and does not require the Von Mangoldt amplitude structure."*

**Status: SUPPORTED (not ESTABLISHED)** — The claim is true but not novel; any GUE-class matrix makes it true.

---

## Unexpected Finding

The Toeplitz random phase matrix (factorizable phases → GOE class) ALSO passes pair correlation at 9.0% MRD. This means pair correlation at N=500 with 5-realization averaging is not capable of distinguishing GOE from GUE (Toeplitz has β=0.45 but passes the pair correlation test). This further undermines the discriminating power of the MRD test.

**Implication:** The 10% MRD criterion for pair correlation is not a strong discriminator at this matrix size/sample size. A meaningful pair correlation test would require either larger N or more realizations.

---

## Verification Scorecard

- 0 VERIFIED (Lean)
- 4 COMPUTED (mrd_gue=7.8%, mrd_flat=6.8%, mrd_toep=9.0%, c1_mrds mean=15.5%)
- 1 CHECKED (compared against E005 result of 7.9% — consistent)
- 0 CONJECTURED
