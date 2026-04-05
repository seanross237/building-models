#!/usr/bin/env python3
"""
Scaling analysis: C_{L,eff} vs Re for Kolmogorov spectrum.
Fix NaN issue by using better integration bounds.
Verify Re^{-3/8} scaling.
"""
import numpy as np
from scipy.integrate import quad

C_lady4_scalar = 8.0 / (3.0 * np.pi**2 * np.sqrt(3.0))
C_L_SCALAR = C_lady4_scalar**0.25

def ceff_kolmogorov(Re, c_diss=1.0, k_min=1):
    """C_eff for Kolmogorov spectrum with dissipation cutoff."""
    k_d = Re**0.75
    k_upper = min(10*k_d, 1e8)  # cap to avoid overflow

    def integrand_L2(k):
        return k**(-5.0/3.0) * np.exp(-c_diss * (k/k_d)**(4.0/3.0))

    def integrand_H1(k):
        return k**(1.0/3.0) * np.exp(-c_diss * (k/k_d)**(4.0/3.0))

    I_L2, _ = quad(integrand_L2, k_min, k_upper, limit=200)
    I_H1, _ = quad(integrand_H1, k_min, k_upper, limit=200)

    L2 = np.sqrt(4 * np.pi * abs(I_L2))
    H1 = np.sqrt(4 * np.pi * abs(I_H1))

    if L2 < 1e-30 or H1 < 1e-30:
        return np.nan
    return 3**0.25 * (L2/H1)**0.75


# Compute over wide Re range
print("="*70)
print("C_eff vs Re SCALING")
print("="*70)

Re_vals = np.logspace(1.5, 8, 40)
C_vals = []
for Re in Re_vals:
    C = ceff_kolmogorov(Re)
    C_vals.append(C)
    if Re in [100, 1000, 10000, 100000, 1e6]:
        print(f"  Re = {Re:.0f}: C_eff = {C:.6f}, ratio = {C/C_L_SCALAR:.4f}")

C_vals = np.array(C_vals)
valid = ~np.isnan(C_vals) & (C_vals > 0)

# Fit scaling
log_Re = np.log10(Re_vals[valid])
log_C = np.log10(C_vals[valid])
coeffs = np.polyfit(log_Re, log_C, 1)
exponent = coeffs[0]
prefactor = 10**coeffs[1]

print(f"\n  Power-law fit: C_eff ≈ {prefactor:.4f} × Re^{{{exponent:.4f}}}")
print(f"  Theoretical: ~Re^{{-3/8}} = ~Re^{{-0.375}}")

# Verify with exact formula
# For large Re: ||f||² → const, ||∇f||² → A × k_d^{4/3} = A × Re
# where A = 4π × ∫₀^∞ u^{1/3} e^{-u^{4/3}} du × 3/(4) (from substitution)
# Actually let me compute the asymptotic integrals

# For large k_d (i.e., large Re):
# I_L2 = ∫₁^∞ k^{-5/3} e^{-c(k/k_d)^{4/3}} dk → ∫₁^∞ k^{-5/3} dk = 3/2 (for c→0, k_d→∞)
# But the exponential cutoff makes it converge at k~k_d.
# For the leading behavior: I_L2 ≈ ∫₁^∞ k^{-5/3} dk = 3/2 + O(e^{-c})
# (since k^{-5/3} is integrable at ∞ and the exponential is ≈1 for k << k_d)

# I_H1 = ∫₁^∞ k^{1/3} e^{-c(k/k_d)^{4/3}} dk
# Change u = k/k_d: = k_d^{4/3} ∫_{1/k_d}^∞ u^{1/3} e^{-cu^{4/3}} du
# For large k_d: ≈ k_d^{4/3} ∫₀^∞ u^{1/3} e^{-cu^{4/3}} du
# With t = cu^{4/3}: u = (t/c)^{3/4}, du = (3/4)(t/c)^{-1/4}/c dt
# ∫₀^∞ u^{1/3} e^{-t} (3/(4c)) (t/c)^{-1/4} dt/...
# Actually: substitution v = u^{4/3}: dv = (4/3) u^{1/3} du, so u^{1/3} du = (3/4) dv
# ∫₀^∞ u^{1/3} e^{-cv} (3/4) dv... wait that's not right either.
# Let v = c u^{4/3}: dv = (4c/3) u^{1/3} du, so u^{1/3} du = (3/(4c)) dv
# ∫₀^∞ e^{-v} (3/(4c)) dv = 3/(4c)

I_asymptotic = 3.0 / 4.0  # for c=1

print(f"\n  Asymptotic I_H1 / k_d^(4/3) → {I_asymptotic:.4f}")
print(f"  So ||∇f||² → 4π × {I_asymptotic:.4f} × k_d^(4/3) = {4*np.pi*I_asymptotic:.4f} × Re")
print(f"  And ||f||² → 4π × 3/2 = {4*np.pi*1.5:.4f} (constant)")

C_asymp_formula = 3**0.25 * (4*np.pi*1.5)**0.375 / (4*np.pi*0.75)**0.375
print(f"\n  Asymptotic C_eff = 3^(1/4) × (||f||²)^(3/8) / (||∇f||²)^(3/8)")
print(f"  = 3^(1/4) × (6π)^(3/8) / (3π)^(3/8) × Re^(-3/8)")
print(f"  = 3^(1/4) × 2^(3/8) × Re^(-3/8)")
C_prefactor = 3**0.25 * 2**0.375
print(f"  = {C_prefactor:.6f} × Re^(-3/8)")
print(f"\n  At Re=1000: {C_prefactor:.6f} × {1000**(-0.375):.6f} = {C_prefactor * 1000**(-0.375):.6f}")
print(f"  Numerical:  {ceff_kolmogorov(1000):.6f}")

# Accuracy of asymptotic vs numerical
print("\n  Asymptotic vs numerical comparison:")
for Re in [100, 300, 1000, 3000, 10000, 100000]:
    C_num = ceff_kolmogorov(Re)
    C_asymp = C_prefactor * Re**(-0.375)
    print(f"  Re={Re:>7d}: numerical={C_num:.6f}, asymptotic={C_asymp:.6f}, "
          f"error={abs(C_num-C_asymp)/C_num*100:.1f}%")

# Now: what's the theoretical bound that can actually be PROVEN?
print("\n" + "="*70)
print("PROVABLE BOUND ANALYSIS")
print("="*70)
print()
print("The Gaussian regime C_eff = 3^{1/4}(||f||/||∇f||)^{3/4} is the TYPICAL value.")
print("But for a BOUND, we need the WORST case over all phases.")
print()
print("Bernstein inequality: For f with support in |k| ≤ K,")
print("  ||f||_{L⁴(T³)} ≤ C_B × K^{3/4} × ||f||_{L²(T³)}")
print("  where C_B depends on dimension (d=3).")
print()
print("For band-limited [k₀/2, 2k₀]:")
print("  ||f||_{L⁴} ≤ C_B × (2k₀)^{3/4} × ||f||_{L²}")
print("  ||∇f|| ≥ (k₀/2) ||f||  (lower bound for band-limited)")
print("  So C_{L,eff} ≤ C_B × (2k₀)^{3/4} / (k₀/2)^{3/4} = C_B × 4^{3/4}")
print("  = C_B × 2^{3/2} = C_B × 2.828")
print()
print("This gives a constant independent of k₀! Not useful for reducing slack.")
print()
print("The REAL improvement comes from having energy spread across MANY bands.")
print("For f = Σ_j Δ_j f (Littlewood-Paley), we need to account for")
print("CROSS-BAND CANCELLATION.")
print()
print("For a Kolmogorov spectrum, the key is that low-k modes dominate ||f||_{L²}")
print("while high-k modes dominate ||∇f||_{L²}, creating a large ||∇f||/||f|| ratio.")
print("This ratio, not any band-specific improvement, drives the slack reduction.")
print()

# What CAN be proven?
print("What can be proven (without random phase assumption):")
print("  For f with energy spectrum E(k) ≤ A k^{-β}, the Sobolev interpolation gives:")
print("  ||f||_{L⁴} ≤ C ||f||^{1-θ}_{L²} ||∇f||^θ_{L²} with θ = 3/4")
print("  And the SAME C as the sharp constant, regardless of spectrum.")
print()
print("  The spectral constraint helps only when combined with PHASE information.")
print("  Without phase information, the worst case is always constructive interference.")
print()
print("  However, for DIVERGENCE-FREE fields (NS), there's an additional constraint:")
print("  The Helmholtz projection eliminates certain phase alignments.")
print("  Our numerical finding: div-free reduces C_eff by ~14%.")
