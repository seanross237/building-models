"""
contraction_optimize.py
========================
Optimize the master loop contraction estimate from CNS arXiv:2505.16585.

The key contraction condition (Proposition 3.23) is:
    β · B(N,d) < C_d

This gives threshold:
    β_max = C_d / B(N,d)

From the paper's analysis:
- Conservative: C_eff = 10^40 * 4  (giving β₀(4) = 10^{-40}/4)
- Structural: C_eff = 10^3 * d   (giving β < 1/(4000) in d=4)
- Optimized: C_eff = 8*d*e       (giving β ~ 1/87 in d=4)
- Target: Bakry-Émery β < 1/24

Key formula: β_max(C, d=4) = 1/(C * d) where C is the effective constant multiplier.

We also model the curvature-enhanced bound:
    β_max(κ, δ) = (C_d + δ * κ) / B(N,d)
"""

import numpy as np
import math

print("=" * 70)
print("MASTER LOOP CONTRACTION ESTIMATE OPTIMIZATION")
print("CNS arXiv:2505.16585 — Proposition 3.23 Analysis")
print("=" * 70)
print()

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Basic threshold formula
# ─────────────────────────────────────────────────────────────────────────────
print("─" * 70)
print("PART 1: Threshold Formula Analysis")
print("─" * 70)
print()

d = 4  # spacetime dimension
e = math.e  # Euler's number ≈ 2.718

print(f"Dimension: d = {d}")
print(f"Euler's number: e = {e:.6f}")
print()

# Known thresholds
print("Known thresholds:")
print()

# Conservative (from paper eq 2.2)
beta_conservative = 1e-40 / 4
print(f"  Conservative (paper eq 2.2):  β₀(4) = 10^{{-40}}/4 = {beta_conservative:.3e}")

# Structural from Thm 3.2
beta_structural = 1.0 / (1e3 * d)
print(f"  Structural (Thm 3.2):         β₀(4) = 1/(10³·d) = 1/{int(1e3*d)} = {beta_structural:.6f}")

# Optimized with C ~ 8de
C_opt = 8 * d * e  # Note: paper says C ~ 8de, treating 'd' as the value d=4
# Actually re-reading: "C ~ 8de" — this likely means C_d ≈ 8*d*e as a pure number
# So β_max = 1/(8de) ≈ 1/87 means the denominator is 8*d*e itself
beta_opt_87 = 1.0 / (8 * d * e)
print(f"  Optimized (C ~ 8de):          β₀(4) = 1/(8·4·e) = 1/{8*d*e:.2f} ≈ {beta_opt_87:.6f}")

# Bakry-Émery target
beta_BE = 1.0 / 24
print(f"  Bakry-Émery target:           β < 1/24 = {beta_BE:.6f}")

print()
print(f"Ratio (optimized / Bakry-Émery): {beta_opt_87 / beta_BE:.3f}x")
print(f"Gap factor: {beta_BE / beta_opt_87:.3f}x (master loop needs this much improvement)")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: β_max as a function of C
# ─────────────────────────────────────────────────────────────────────────────
print()
print("─" * 70)
print("PART 2: β_max(C, d=4) = 1/(C·d)")
print("─" * 70)
print()
print("Interpretation: the threshold formula in the paper is β_max = 1/(C_eff)")
print("where C_eff incorporates all the dimensional factors.")
print()
print("Two models:")
print("  Model A: β_max = 1/(C * d)  [C is multiplicative constant, d=4 separate]")
print("  Model B: β_max = 1/C_eff    [C_eff is the total denominator]")
print()

# Model A: β_max = 1/(C * d)
# For threshold = 1/87 ≈ 0.01149, with d=4:
# 1/(C * 4) = 1/87  =>  C = 87/4 = 21.75
C_at_87 = (8 * d * e)  # = 87.07 ≈ 87, this is the full denominator C_eff
C_model_A_at_87 = C_at_87 / d  # = ~21.77 (C in model A form)
print(f"Model A: β_max = 1/(C*4)")
print(f"  At β=1/87:  C_eff = {C_at_87:.4f}, so C_A = {C_model_A_at_87:.4f}")
print(f"  At β=1/24:  need C_eff = 24, so C_A = {24/d:.4f}")
print()

print("Model B: β_max = 1/C_eff (C_eff is the full denominator)")
print(f"  At β=1/87:  C_eff = {1/beta_opt_87:.4f}")
print(f"  At β=1/24:  C_eff = {1/beta_BE:.4f}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: Full optimization table
# ─────────────────────────────────────────────────────────────────────────────
print()
print("─" * 70)
print("PART 3: β_max vs C_eff  (d=4)")
print("─" * 70)
print()

C_values = np.array([
    4.0,   # minimum sensible (β_max = 1/4)
    6.0,   # Bakry-Émery target: 1/24
    8*e,   # ≈ 21.7 (C~8e, single d factor)
    8*d*e, # ≈ 87.1 (C~8de, full expression)
    24*d,  # = 96 (β_max = 1/96)
    1e3,   # structural (β_max = 1/1000)
    4e3,   # structural * d (β_max = 1/4000)
    1e40,  # conservative paper bound
])

labels = [
    "C_eff=4",
    "C_eff=6 (for 1/24)",
    "C_eff=8e ≈ 21.7",
    "C_eff=8de ≈ 87.1",
    "C_eff=24d = 96",
    "C_eff=10³",
    "C_eff=10³d",
    "C_eff=10^40",
]

print(f"{'Label':<25} {'C_eff':>12} {'β_max':>14} {'β_max frac':>16} {'vs 1/24':>8}")
print("-" * 80)
for C_val, lab in zip(C_values, labels):
    beta = 1.0 / C_val if C_val > 0 else float('inf')
    # Format as fraction approximation
    if beta > 0 and beta < 1:
        approx_denom = round(1/beta)
        frac_str = f"~1/{approx_denom}"
    else:
        frac_str = f"{beta:.3e}"
    ratio = beta / beta_BE
    print(f"{lab:<25} {C_val:>12.4g} {beta:>14.6f} {frac_str:>16} {ratio:>8.4f}")

print()

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Minimum C to reach Bakry-Émery threshold
# ─────────────────────────────────────────────────────────────────────────────
print()
print("─" * 70)
print("PART 4: Minimum C needed to reach β_max = 1/24")
print("─" * 70)
print()

# β_max = C_d / B(N,d) = 1/24
# If β_max = 1/(C_eff) and C_eff is reduced by factor f from current value of 87:
C_required_for_BE = 24  # β_max = 1/C_eff = 1/24
C_current = 8 * d * e   # ≈ 87.07
improvement_needed = C_current / C_required_for_BE

print(f"Current best C_eff: {C_current:.4f} (gives β_max ≈ 1/87)")
print(f"Required C_eff for 1/24: {C_required_for_BE}")
print(f"Improvement factor needed: {improvement_needed:.3f}x reduction in C_eff")
print()

# In terms of the constant C in β < 1/(Cd):
C_A_required = C_required_for_BE / d  # = 24/4 = 6
C_A_current = C_current / d           # ≈ 21.77
print(f"In formula β < 1/(C·d):")
print(f"  Current C:   {C_A_current:.4f}")
print(f"  Required C:  {C_A_required:.4f}")
print(f"  Ratio:       {C_A_current / C_A_required:.3f}x")
print()

print("Can the constant C_A = 8e ≈ 21.77 be reduced to C_A = 6?")
print(f"  8e = {8*e:.4f}")
print(f"  6  = 6.0000")
print(f"  This requires C_A to drop by {8*e/6:.3f}x from 8e to 6")
print(f"  8e/6 = {8*e/6:.4f} — this is NOT just a factor of e or π")
print()
print("Physical interpretation: The constant 8e comes from the")
print("'deformation term' in the master loop analysis. To get from")
print("8e to 6, one would need to remove a factor of ~3.62 from the")
print("combinatorial/algebraic bound.")
print()
print("Note: 8e / (4π/3) ≈ {:.4f}  (4π/3 ≈ {:.4f})".format(8*e/(4*math.pi/3), 4*math.pi/3))
print("Note: 8e / (2π) ≈ {:.4f}  (2π ≈ {:.4f})".format(8*e/(2*math.pi), 2*math.pi))
print("Note: 8e / e² = {:.4f}  (e² ≈ {:.4f})".format(8*e/e**2, e**2))

# ─────────────────────────────────────────────────────────────────────────────
# PART 5: Curvature-enhanced bound
# ─────────────────────────────────────────────────────────────────────────────
print()
print("─" * 70)
print("PART 5: Curvature-Enhanced Bound Analysis")
print("─" * 70)
print()

print("Conjectured curvature-enhanced master loop bound:")
print("  β_max(κ, δ) = (C_d + δ·κ) / B(N,d)")
print()
print("Where:")
print("  C_d = current contraction constant (≈ 1 in normalized units)")
print("  κ = N/2 = Ricci curvature of U(N) or SU(N)")
print("  δ = curvature coupling strength (unknown, conjectured > 0)")
print("  B(N,d) = combinatorial factor from master loop")
print()

# Normalize: current β_max = 1/87 from C_d/B(N,d)
# So B(N,d)/C_d = 87 (the effective denominator)
# β_max(C_d, δ=0) = 1/87

B_over_Cd = 1.0 / beta_opt_87  # ≈ 87
print(f"Normalization: B(N,d)/C_d ≈ {B_over_Cd:.4f}")
print()

# For the curvature-enhanced version:
# β_max(κ, δ) = (C_d + δ·κ) / B(N,d) = (1 + δ·κ/C_d) / (B/C_d)
#             = (1 + δ·κ/C_d) · β_max(0)
#
# In normalized units where β_max(0) = 1/87:
# β_max(κ) = (1 + δ_norm * κ) * (1/87)
# where δ_norm = δ/C_d

print("Table: β_max vs κ (for various δ_norm values)")
print()

# κ = N/2 for U(N)
kappa_values = [0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
N_equiv = [2*k for k in kappa_values]

delta_norm_values = [0.0, 0.01, 0.05, 0.1, 0.5, 1.0]

# Print header
print(f"{'κ':>6} {'N≈':>6} ", end="")
for d_n in delta_norm_values:
    print(f" δ_n={d_n:4.2f}", end="")
print()
print("-" * (14 + 11*len(delta_norm_values)))

for kappa, N_v in zip(kappa_values, N_equiv):
    print(f"{kappa:>6.1f} {N_v:>6.0f} ", end="")
    for d_n in delta_norm_values:
        beta_enh = (1 + d_n * kappa) * beta_opt_87
        print(f" {beta_enh:>9.5f}", end="")
    print()

print()

# What δ_norm is needed to reach 1/24?
target = beta_BE  # 1/24
kappa_test_values = [1.0, 2.0, 5.0, 10.0, 20.0, 100.0]
print("Required δ_norm to reach β_max = 1/24 = {:.6f}:".format(target))
print()
print(f"  {'κ':>6}  {'N≈':>6}  {'δ_norm_required':>18}  {'Physical interpretation':>30}")
print("  " + "-" * 70)
for kappa in kappa_test_values:
    if kappa > 0:
        # β_max = (1 + δ_norm * κ) * (1/87) = 1/24
        # 1 + δ_norm * κ = 87/24
        # δ_norm = (87/24 - 1) / κ = (87 - 24)/(24 * κ) = 63/(24 * κ)
        d_n_req = (B_over_Cd * target - 1) / kappa  # = (87/24 - 1) / κ
        N_v = 2 * kappa
        d_n_req_phys = d_n_req  # normalized
        interp = f"needs δ/C_d = {d_n_req:.4f} per unit κ"
        print(f"  {kappa:>6.1f}  {N_v:>6.1f}  {d_n_req:>18.6f}  {interp}")

print()
# Special analysis for large N
print("Large N analysis:")
print("  At N → ∞: κ = N/2 → ∞")
print("  β_max(N) = (1 + δ_norm * N/2) * (1/87)")
print("  For any δ_norm > 0, β_max → ∞ as N → ∞")
print("  But we need fixed N (typically N=2 or N=3 for SU(2), SU(3))")
print()

# For N=2 (SU(2)): κ = 1
kappa_SU2 = 1.0
d_n_for_SU2 = (B_over_Cd * target - 1) / kappa_SU2
print(f"  SU(2) (N=2, κ=1): need δ_norm = {d_n_for_SU2:.4f} ≈ {d_n_for_SU2:.2f}")
print(f"    This means: δ/C_d = {d_n_for_SU2:.4f}")
print(f"    Physically: curvature term δ·κ must be {d_n_for_SU2:.4f} × C_d")

# For N=3 (SU(3)): κ = 3/2
kappa_SU3 = 3/2
d_n_for_SU3 = (B_over_Cd * target - 1) / kappa_SU3
print()
print(f"  SU(3) (N=3, κ=3/2): need δ_norm = {d_n_for_SU3:.4f}")
print(f"    This means: δ/C_d = {d_n_for_SU3:.4f}")

# For large N
print()
print("  As N increases, required δ_norm decreases (easier to satisfy):")
for N_val in [2, 3, 4, 10, 100]:
    kappa_v = N_val / 2.0
    d_n = (B_over_Cd * target - 1) / kappa_v
    print(f"    N={N_val:3d} (κ={kappa_v:5.1f}): δ_norm = {d_n:.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 6: Physical Summary
# ─────────────────────────────────────────────────────────────────────────────
print()
print("─" * 70)
print("PART 6: Physical Summary and Key Numbers")
print("─" * 70)
print()

print("MAXIMUM ACHIEVABLE β₀(4) IN MASTER LOOP FRAMEWORK:")
print()
print(f"  1. Conservative bound (paper):      {beta_conservative:.3e} = 10^-40/4")
print(f"  2. Structural bound (Thm 3.2):      {beta_structural:.6f} ≈ 1/4000")
print(f"  3. Optimized bound (tightest, 1/87): {beta_opt_87:.6f} ≈ 1/87")
print(f"  4. Bakry-Émery target:              {beta_BE:.6f} = 1/24")
print()
print(f"  Gap factor 3→4: {beta_BE/beta_opt_87:.3f}x improvement needed")
print()
print("  The master loop framework (without curvature input) appears to be")
print(f"  bounded above by β_max ≈ 1/87 ≈ {beta_opt_87:.4f}, which is {beta_BE/beta_opt_87:.2f}x")
print("  below the Bakry-Émery threshold.")
print()

print("CAN CURVATURE INPUT (δ > 0) BRIDGE THE GAP?")
print()
print("  YES, in principle, but requires a positive coupling δ of the")
print("  Ricci curvature κ = N/2 of U(N) into the master loop estimate.")
print()
print("  For SU(2): δ/C_d ≈ 2.63 needed (large — hard to realize)")
print("  For SU(3): δ/C_d ≈ 1.75 needed (still large)")
print("  For SU(10): δ/C_d ≈ 0.53 needed (more feasible)")
print()
print("  At large N: the required δ_norm → 0 (easier)")
print("  This suggests the curvature enhancement is most promising")
print("  for large-N gauge theories (planar limit).")
print()

print("CONCLUSION:")
print()
print("  β₀(4)_max (without curvature) ≈ 1/87 ≈ 0.0115")
print(f"  β₀(4)_target (Bakry-Émery) = 1/24 ≈ 0.0417")
print()
print("  The curvature input mechanism could in principle bridge the gap,")
print("  but requires a new term in the master loop contraction estimate")
print("  that couples the Lie group curvature to the loop weights.")
print("  This is the key open problem stated in CNS Remark 1.4.")

# ─────────────────────────────────────────────────────────────────────────────
# PART 7: Precise formula extraction
# ─────────────────────────────────────────────────────────────────────────────
print()
print("─" * 70)
print("PART 7: Precise Formula for β_max(C, d=4)")
print("─" * 70)
print()

print("β_max formula (Model A: general dimension):")
print("  β_max(C_A, d) = 1 / (C_A · d)")
print()
print("  where C_A comes from the contraction constant in Prop 3.23")
print()
print("  Current best: C_A = 8e ≈ 21.77 (from 'C ~ 8de' expression)")
print("  This gives: β_max(d=4) = 1/(8e · 4) = 1/(32e) ≈ 1/86.97")
print()
print(f"  1/(32e) = {1/(32*e):.8f}")
print(f"  1/87    = {1/87:.8f}")
print(f"  Match:    {abs(1/(32*e) - 1/87) < 0.001}")
print()

print("β_max formula (Model B: C_eff as single denominator):")
print("  β_max(C_eff, d=4) = 1 / C_eff")
print()

# Minimum achievable C_eff
# The paper says with the deformation analysis, C_eff = 8de = 32e ≈ 87
# Can this be reduced below 24?
print("Minimum C_eff for 1/24 threshold: C_eff = 24")
print(f"Current C_eff: 8de = 8·4·e = 32e ≈ {32*e:.4f}")
print(f"Ratio: C_current/C_required = {32*e/24:.4f}")
print()
print(f"The contraction constant C_A would need to decrease from 8e to 6.")
print(f"Equivalently, the β · B(N,d) < C_d condition needs C_d/B(N,d) ≥ 1/24.")

# Summary of key numbers for report
print()
print("═" * 70)
print("KEY NUMBERS FOR REPORT:")
print("═" * 70)
print(f"  β₀(4) conservative:  {beta_conservative:.3e}")
print(f"  β₀(4) structural:    {beta_structural:.6f} = 1/{int(1/beta_structural)}")
print(f"  β₀(4) optimized:     {beta_opt_87:.6f} ≈ 1/{round(1/beta_opt_87)}")
print(f"  β₀(4) BE target:     {beta_BE:.6f} = 1/24")
print(f"  Gap factor:          {beta_BE/beta_opt_87:.4f}x")
print(f"  C_eff (optimized):   32e = {32*e:.4f}")
print(f"  C_eff (for 1/24):    24")
print(f"  C_reduction needed:  {32*e/24:.4f}x")
print(f"  δ_norm for SU(2):    {(B_over_Cd * target - 1) / 1.0:.4f}")
print(f"  δ_norm for SU(3):    {(B_over_Cd * target - 1) / 1.5:.4f}")
