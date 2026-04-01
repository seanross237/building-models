# Exploration 003: B-square Formula and Convention Verification

**Date:** 2026-03-28
**Mode:** CONVENTION VERIFICATION
**Verdict:** LEFT formula (corrected) is CORRECT. RIGHT formula (E001's) gives WRONG eigenvalues at Q ≠ I.

---

## Executive Summary

The single most critical computation of this validation strategy: comparing the LEFT (corrected) and RIGHT (E001's) B_□ formulas at the configuration U_all = iσ₃.

**Result:** The two formulas give DIFFERENT eigenvalues at Q ≠ I:
- LEFT (corrected): λ_max = 4β at U_all = iσ₃ (same as Q=I) → H_norm = 1/12 → Conjecture 1 SURVIVES
- RIGHT (E001's): λ_max = 6β at U_all = iσ₃ → H_norm = 1/8 → This is WRONG

The LEFT formula is verified by finite differences (both diagonal and off-diagonal elements) using left perturbation Q → exp(εv)·Q. The RIGHT formula is NOT the correct covariant Hessian for the SZZ Bakry-Émery framework.

---

## The Two Formulas

### LEFT formula (corrected, prior mission's):
```
P1 = I
P2 = Q1
P3 = Q1·Q2·Q3^{-1}           (includes Q3's inverse)
P4 = Q1·Q2·Q3^{-1}·Q4^{-1}   (= U_plaq, full holonomy)
```
B_□ = v₁ + Ad_{P2}(v₂) − Ad_{P3}(v₃) − Ad_{P4}(v₄)

### RIGHT formula (E001's):
```
P1 = I
P2 = Q1
P3 = Q1·Q2                    (NO Q3^{-1})
P4 = Q1·Q2·Q3^{-1}            (NO Q4^{-1})
```
B_□ = v₁ + Ad_{P2}(v₂) − Ad_{P3}(v₃) − Ad_{P4}(v₄)

### Why they differ
At Q=I: both P3 = I and P4 = I → formulas are IDENTICAL → same eigenvalues (4β).
At Q ≠ I: different partial holonomies → different Ad transport → different off-diagonal Hessian elements → different eigenvalues.

---

## Test Results

### Test 1: Q=I Sanity Check
- LEFT formula: λ_max = 4.000000β ✓
- RIGHT formula: λ_max = 4.000000β ✓
- Both agree at Q=I (expected, since P3=P4=I for both)

### Test 2: U_all = iσ₃ (THE CRITICAL TEST)
- Plaquette holonomy: Re Tr(U_□) = 2.0 (flat connection, action at minimum)
- **LEFT formula: λ_max = 4.000000β** → H_norm = 1/12 exactly
- **RIGHT formula: λ_max = 6.000000β** → H_norm = 1/8
- **Difference: 2.000000** (not a numerical error — a genuine formula difference)

The LEFT formula gives λ_max = 4β at U=iσ₃, which EQUALS the Q=I value. The top 9 eigenvalues are all 4β (same 9-fold degeneracy as at Q=I, which is expected since U=iσ₃ is a flat connection with trivial plaquette holonomies).

### Test 3: Finite Difference Verification (LEFT convention)
```
Diagonal:    H[0,0]:   formula=1.500000, FD=1.500098, diff=9.78e-05 ✓
Off-diagonal: H[0,3]:  formula=-0.250000, FD=-0.249969, diff=3.11e-05 ✓
Off-diagonal: H[0,6]:  formula=-0.250000, FD=-0.249969, diff=3.11e-05 ✓
Off-diagonal: H[1,4]:  formula=-0.250000, FD=-0.249969, diff=3.11e-05 ✓
Off-diagonal: H[3,9]:  formula=-0.250000, FD=-0.249969, diff=3.11e-05 ✓
Off-diagonal: H[5,8]:  formula=-0.250000, FD=-0.249969, diff=3.11e-05 ✓
```
All discrepancies < 10⁻⁴ (consistent with O(h²) finite difference truncation error for h=10⁻⁵).

### Test 4: Random Q (LEFT formula)
5 random Haar-distributed Q: all H_norm < 1/12 ✓
Maximum H_norm observed: 0.073525 (well below 1/12)

---

## Implications for the Validation

1. **E001's claim of CS saturation at U=iσ₃ is WRONG.** E001 used the RIGHT formula and got λ_max = 6β. The correct LEFT formula gives λ_max = 4β.

2. **Conjecture 1 SURVIVES.** U_all = iσ₃ gives H_norm = 1/12 exactly (same as Q=I), NOT 1/8. This is because U=iσ₃ is a flat connection, and flat connections are isospectral with Q=I in the LEFT formula.

3. **β < 1/6 is CORRECT but NOT necessarily tight.** The CS bound HessS ≤ 6β|v|² is NOT saturated by any tested Q. The actual maximum HessS/|v|² over all tested Q is 4β (at Q=I and flat connections), well below the 6β bound.

4. **The 8× improvement over SZZ is confirmed.** β < 1/6 (from the CS bound H_norm ≤ 1/8) is correct. Whether the tighter β < 1/4 (from Conjecture 1, H_norm ≤ 1/12) holds depends on Conjecture 1, which remains open but unrefuted.

---

## Convention Chain Verification

The proof chain with explicit conventions:

1. SZZ convention: S(Q) = −(β/N) Σ Re Tr(U_□), |A|² = −2Tr(A²)
2. HessS(v,v) = (β/(2N)) v^T M(Q) v where M(Q) = Σ_□ B_□^T B_□
3. For the LEFT formula: B_□ = v₁ + Ad_{Q₁}(v₂) − Ad_{Q₁Q₂Q₃⁻¹}(v₃) − Ad_{U_□}(v₄)
4. Bakry-Émery: K_S > 0 iff HessS(v,v) < (N/2)|v|² for all v
5. CS bound: |B_□|² ≤ 4 Σ_{e∈□} |v_e|², since |Ad_P(v)| = |v| (isometry)
6. Summing: Σ_□ |B_□|² ≤ 4 × 2(d−1) × |v|² = 24|v|² (each link in 2(d−1) plaquettes)
7. Therefore: HessS ≤ (β/(2N)) × 24 × |v|² = 6β|v|² (for N=2)
8. K_S > 0 iff 6β < 1 → **β < 1/6** ✓

The factor 48 in "H_norm = λ_max/(48β)" comes from: 8(d−1)N = 8×3×2 = 48. This is the SZZ Lemma 4.1 constant.

---

## Code
- `code/critical_test.py` — the definitive test comparing LEFT and RIGHT formulas
