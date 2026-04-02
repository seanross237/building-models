"""
Full analysis of the formula verification.
Tests: ln(Γ_SED/Γ_exact) = ln(A) + slope × (S_WKB - Vb/Ezpf)
"""
import numpy as np

# ============================================================
# Full dataset: E001 + E005
# ============================================================
# E001 data (verified from E001 REPORT.md)
# Note: E001 Gamma_SED for lam=0.25 was 0.0663, for lam=0.10 was 0.00790
data = [
    # (lam, S_WKB, Vb_Ezpf, Gamma_SED, Gamma_SED_sem, Gamma_exact, source)
    (0.25, 1.4076, 1.4142, 0.0663,    0.0035,   5.780326e-02, "E001"),
    (0.10, 6.2894, 3.5355, 0.00790,   0.00137,  4.278771e-04, "E001"),
    # E005 new data
    (0.30, 0.9865, 1.1785, 1.1142e-01, 4.1404e-03, 8.964654e-02, "E005"),
    (0.20, 2.1059, 1.7678, 6.3476e-02, 3.4270e-03, 2.810832e-02, "E005"),
    (0.15, 3.4170, 2.3570, 3.8711e-02, 2.9409e-03, 7.468192e-03, "E005"),
    (0.075, 9.2679, 4.7140, 4.1350e-03, 6.4414e-04, 2.206057e-05, "E005"),
    (0.05, 15.3328, 7.0711, 4.3250e-04, 8.5151e-05, 5.194501e-08, "E005"),
]

lams     = np.array([d[0] for d in data])
S_WKBs   = np.array([d[1] for d in data])
Vb_Ezpfs = np.array([d[2] for d in data])
Gamma_SEDs = np.array([d[3] for d in data])
Gamma_SEMs = np.array([d[4] for d in data])
Gamma_exacts = np.array([d[5] for d in data])
sources  = [d[6] for d in data]

exponents = S_WKBs - Vb_Ezpfs
ratios    = Gamma_SEDs / Gamma_exacts
ln_ratios = np.log(ratios)
implied_A = np.exp(ln_ratios - exponents)

print("=" * 90)
print("FULL DATASET: E001 + E005")
print("=" * 90)
print(f"{'λ':>8} {'S_WKB':>8} {'Vb/Ez':>8} {'exponent':>10} {'Γ_SED':>12} "
      f"{'Γ_exact':>12} {'ratio':>10} {'ln(ratio)':>10} {'A_impl':>8}")
print("-" * 90)
for i, (lam, src) in enumerate(zip(lams, sources)):
    print(f"{lam:>8.4f} {S_WKBs[i]:>8.4f} {Vb_Ezpfs[i]:>8.4f} {exponents[i]:>10.4f} "
          f"{Gamma_SEDs[i]:>12.4e} {Gamma_exacts[i]:>12.4e} {ratios[i]:>10.4f} "
          f"{ln_ratios[i]:>10.4f} {implied_A[i]:>8.4f}  [{src}]")

# ============================================================
# Linear fits
# ============================================================
print("\n" + "=" * 90)
print("LINEAR FIT: ln(Γ_SED/Γ_exact) = ln(A) + slope × (S_WKB - Vb/Ezpf)")
print("=" * 90)

def linear_fit_stats(x, y, label):
    n = len(x)
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    residuals = y - y_pred
    SS_res = np.sum(residuals**2)
    SS_tot = np.sum((y - y.mean())**2)
    R2 = 1 - SS_res / SS_tot
    RMSE = np.sqrt(SS_res / n)

    print(f"\n  {label} (n={n}):")
    print(f"    slope     = {slope:.4f}  (expected: 1.0)")
    print(f"    intercept = {intercept:.4f}")
    print(f"    A = exp(intercept) = {np.exp(intercept):.4f}  (expected: ~1.15)")
    print(f"    R² = {R2:.6f}")
    print(f"    RMSE = {RMSE:.4f}")
    print(f"    Residuals: mean={residuals.mean():.4f}, max_abs={np.abs(residuals).max():.4f}")

    return slope, intercept, R2, RMSE, residuals

# All 7 points
slope_all, int_all, R2_all, RMSE_all, resid_all = linear_fit_stats(
    exponents, ln_ratios, "All 7 data points (E001 + E005)")

# Just E005 (5 new points)
mask_e005 = np.array([s == "E005" for s in sources])
slope_e5, int_e5, R2_e5, RMSE_e5, resid_e5 = linear_fit_stats(
    exponents[mask_e005], ln_ratios[mask_e005], "E005 only (5 new points)")

# Check: constrained slope=1 fit
print("\n  Constrained slope=1 fit (all 7 points):")
# With slope=1: ln(ratio) - exponent = ln(A) = constant
ln_A_vals = ln_ratios - exponents
print(f"    ln(A) values: {ln_A_vals}")
print(f"    A values: {np.exp(ln_A_vals)}")
print(f"    Mean ln(A) = {ln_A_vals.mean():.4f}, std = {ln_A_vals.std():.4f}")
print(f"    Mean A = {np.exp(ln_A_vals.mean()):.4f}")
print(f"    A range: [{np.exp(ln_A_vals.min()):.4f}, {np.exp(ln_A_vals.max()):.4f}]")

# ============================================================
# Check if A depends on anything systematically
# ============================================================
print("\n" + "=" * 90)
print("DOES A DEPEND ON λ? (checking for secondary corrections)")
print("=" * 90)

print(f"\nCorrelation of ln(A_implied) with:")
print(f"  λ:          r = {np.corrcoef(lams, np.log(implied_A))[0,1]:.4f}")
print(f"  S_WKB:      r = {np.corrcoef(S_WKBs, np.log(implied_A))[0,1]:.4f}")
print(f"  Vb/Ezpf:    r = {np.corrcoef(Vb_Ezpfs, np.log(implied_A))[0,1]:.4f}")
print(f"  exponent:   r = {np.corrcoef(exponents, np.log(implied_A))[0,1]:.4f}")
print(f"  ln(Vb/Ez):  r = {np.corrcoef(np.log(Vb_Ezpfs), np.log(implied_A))[0,1]:.4f}")

# Try 2-parameter fit: ln(ratio) = a + b*(S_WKB - Vb/Ez) + c*ln(Vb/Ez)
X = np.column_stack([np.ones(len(lams)), exponents, np.log(Vb_Ezpfs)])
coeffs, residuals_2, rank, sv = np.linalg.lstsq(X, ln_ratios, rcond=None)
y_pred_2 = X @ coeffs
SS_res_2 = np.sum((ln_ratios - y_pred_2)**2)
SS_tot = np.sum((ln_ratios - ln_ratios.mean())**2)
R2_2 = 1 - SS_res_2 / SS_tot
print(f"\nTwo-parameter fit: ln(ratio) = a + b*(S_WKB - Vb/Ez) + c*ln(Vb/Ez)")
print(f"  a = {coeffs[0]:.4f}, b = {coeffs[1]:.4f}, c = {coeffs[2]:.4f}")
print(f"  R² = {R2_2:.6f} (vs {R2_all:.6f} for 1-param)")

# ============================================================
# Formula summary
# ============================================================
print("\n" + "=" * 90)
print("VERDICT ON FORMULA")
print("=" * 90)
print(f"""
Formula: ln(Γ_SED/Γ_exact) = ln(A) + (S_WKB - Vb/Ezpf)

Best-fit slope: {slope_all:.4f} (expected 1.0)  → {'PASSES' if abs(slope_all-1.0) < 0.15 else 'FAILS'} within 15% tolerance
R²: {R2_all:.4f}  → {'STRONG' if R2_all > 0.99 else 'MODERATE' if R2_all > 0.95 else 'WEAK'} linear relationship
Best-fit A: {np.exp(int_all):.4f}  (expected ~1.15)

Key findings:
- Slope ≈ 1.05 (close to 1): CONFIRMED
- But A is NOT constant: ranges from {implied_A.min():.3f} to {implied_A.max():.3f}
- A shows a systematic trend with barrier depth (Pearson r={np.corrcoef(S_WKBs, np.log(implied_A))[0,1]:.4f} with S_WKB)
- The formula holds approximately but with a slowly-varying prefactor

Interpretation:
- For shallow barriers (S_WKB ≈ Vb/Ezpf): A ≈ 1.15 (E001 result)
- For deep barriers (S_WKB >> Vb/Ezpf): A grows toward ~2.15
- This suggests a logarithmic correction: ln(A) = 0.14 + 0.06 × (S_WKB - Vb/Ezpf) approximately
- OR: A ~ (Vb/Ezpf)^0.3 approximately
""")
