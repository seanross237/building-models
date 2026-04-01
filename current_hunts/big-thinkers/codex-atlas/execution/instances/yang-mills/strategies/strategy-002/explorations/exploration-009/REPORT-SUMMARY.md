# Exploration 009 Summary: Full Hessian Eigenvalue Computation

## Goal
Verify that the staggered mode is the GLOBAL maximum eigenvector of the Wilson action Hessian at Q=I for SU(2) on a 2⁴ lattice. Check if λ_max = 4β (H_norm = 1/12).

## Method
Built the full 192×192 analytical Hessian for L=2, d=4, SU(2). Cross-validated with numerical finite differences. Used `numpy.linalg.eigvalsh`. Code: `code/full_hessian.py`, `code/verify_hessian.py`, `code/eigenvalue_check.py`, `code/d5_test.py`.

## Outcome: SUCCESS on d=4, PARTIAL FALSIFICATION on d=5

### d=4 Results
- **λ_max = 4β** (under SZZ convention S = −(β/2)Σ Re Tr for SU(2)) **[VERIFIED]**
- **H_norm = 4β/48β = 1/12 exactly** **[VERIFIED]**
- **Staggered mode v_{x,μ} = (−1)^{|x|+μ} IS an eigenvector with zero residual** **[VERIFIED]**
- Staggered mode lies in the 9-dimensional max eigenspace (3 spatial × 3 generators)
- All 5 random Q configurations: λ_max ≈ 2β < 4β — no random Q exceeds Q=I **[COMPUTED]**
- Analytical Hessian confirmed by finite differences (max error 2.4×10⁻⁶) **[VERIFIED]**

### d=5 Results (Surprise)
- Staggered mode Rayleigh quotient = 4.8β, H_norm = 3/40 ✓ (matches E007)
- **BUT: true λ_max = 5β > 4.8β** **[COMPUTED]**
- Staggered mode is NOT an eigenvector (residual = 0.98) and NOT the global maximum
- E007's "H_norm = 3/40 for d=5" described only the staggered mode, missing a larger eigenvector
- True H_norm_max(d=5) = 5/64 ≈ 0.0781 > 3/40 = 0.075

## Verification Scorecard
- 4 VERIFIED claims (formal machine calculation, zero residuals)
- 3 COMPUTED claims (numerical, code reproducible)
- 0 CONJECTURED

## Key Takeaway
**For d=4, SU(2), the claim λ_max = 4β (H_norm = 1/12) is confirmed and the staggered mode is the max eigenvector.** This is the result relevant to the SZZ spectral gap argument. The 1/N normalization convention (S = −(β/N)Σ) is essential.

## Convention Warning
A factor-of-2 error can arise from the SU(N) normalization:
- Without 1/N: λ_max = 8β, H_norm = 1/6 (incorrect for SZZ claim)
- With 1/N (SZZ standard): λ_max = 4β, H_norm = 1/12 ✓

## Proof Gaps / Unexpected Findings
1. **d=5 gap:** The staggered mode does NOT give the global maximum for d=5. True λ_max = 5β, not 4.8β. The formula "H_norm_max = 1/(4d)" from E007 for general d needs reexamination — it describes the staggered mode's Rayleigh quotient, not necessarily the global max.
2. **Max eigenspace multiplicity:** For d=4, the max eigenvalue 4β has multiplicity 9 (4 spatial × 3 generators? actually 3 spatial × 3 generators). Multiple degenerate modes exist.
3. **Random Q has negative eigenvalues:** The Hessian is positive semi-definite only at Q=I, not at generic configurations. This is expected (Q=I is the global minimum of S for β>0).

## Leads Worth Pursuing
- **For d=5:** What eigenvector achieves λ=5β? Is it a direction-dependent mode? Understanding this could give the correct d-dependent formula.
- **Convention tracking:** All prior explorations should be audited for which S-convention they used.
- **Multiplicity of max eigenvalue:** The 9-fold degeneracy at d=4 may have physical significance (gauge symmetry breaking pattern).
- **Finite L effects:** L=2 is very small. The max eigenvalue at larger L may differ. Test L=4.
