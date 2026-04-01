#!/usr/bin/env python3
"""
Analytical computation of effective Ladyzhenskaya constant C_{L,eff}
in the Gaussian (many-mode) regime.

Key insight: for a field f = Σ_k a_k e^{iφ_k + ik·x} with many random-phase modes,
the CLT gives f(x) → Gaussian. For Gaussian f with variance σ²:
  <f²> = σ², <f⁴> = 3σ⁴

So ||f||_{L⁴} = 3^{1/4} ||f||_{L²}.

Then C_{L,eff} = ||f||_{L⁴} / (||f||^{1/4}_{L²} ||∇f||^{3/4}_{L²})
              = 3^{1/4} ||f||_{L²} / (||f||^{1/4}_{L²} ||∇f||^{3/4}_{L²})
              = 3^{1/4} (||f||_{L²} / ||∇f||_{L²})^{3/4}

This depends only on the ratio ||f||/||∇f||, which is determined by the spectrum.
"""

import numpy as np
from scipy.integrate import quad
from scipy.special import gamma as gamma_func

# Ladyzhenskaya constant
C_lady4_scalar = 8.0 / (3.0 * np.pi**2 * np.sqrt(3.0))
C_L_SCALAR = C_lady4_scalar**0.25  # ≈ 0.629

print(f"C_L_scalar = {C_L_SCALAR:.6f}")
print(f"3^{{1/4}} = {3**0.25:.6f}")
print()

# ============================================================================
# Analytical C_eff for power-law spectra
# ============================================================================

def ceff_powerlaw_analytical(alpha, k_min=1, k_max=1e6):
    """
    For |f̂_k| = k^{-α} for k in [k_min, k_max], compute:

    ||f||² = 4π ∫_{k_min}^{k_max} k² × k^{-2α} dk = 4π ∫ k^{2-2α} dk
    ||∇f||² = 4π ∫_{k_min}^{k_max} k² × k² × k^{-2α} dk = 4π ∫ k^{4-2α} dk

    (The k² in each integral comes from the shell counting: # modes at radius k ∝ k²)

    C_eff = 3^{1/4} (||f||/||∇f||)^{3/4}
    """
    def integrand_L2(k):
        return k**2 * k**(-2*alpha)  # = k^{2-2α}

    def integrand_H1(k):
        return k**4 * k**(-2*alpha)  # = k^{4-2α}

    I_L2, _ = quad(integrand_L2, k_min, k_max)
    I_H1, _ = quad(integrand_H1, k_min, k_max)

    L2 = np.sqrt(4 * np.pi * I_L2)
    H1 = np.sqrt(4 * np.pi * I_H1)

    C_eff = 3**0.25 * (L2/H1)**0.75
    return C_eff, L2, H1


def ceff_kolmogorov_analytical(Re, c_diss=1.0, k_min=1):
    """
    For Kolmogorov spectrum with dissipation:
    |û_k|² ∝ k^{-11/3} exp(-c(k/k_d)^{4/3})
    where k_d = Re^{3/4}.

    ||f||² = 4π ∫ k^{-5/3} exp(-c(k/k_d)^{4/3}) dk
    ||∇f||² = 4π ∫ k^{1/3} exp(-c(k/k_d)^{4/3}) dk
    """
    k_d = Re**0.75

    def integrand_L2(k):
        return k**(-5.0/3.0) * np.exp(-c_diss * (k/k_d)**(4.0/3.0))

    def integrand_H1(k):
        return k**(1.0/3.0) * np.exp(-c_diss * (k/k_d)**(4.0/3.0))

    I_L2, _ = quad(integrand_L2, k_min, 10*k_d)
    I_H1, _ = quad(integrand_H1, k_min, 10*k_d)

    L2 = np.sqrt(4 * np.pi * I_L2)
    H1 = np.sqrt(4 * np.pi * I_H1)

    C_eff = 3**0.25 * (L2/H1)**0.75
    return C_eff, L2, H1


def ceff_bandlimited_analytical(k0):
    """
    For uniform spectrum in [k0/2, 2k0]:
    |f̂_k| = const for |k| ∈ [k0/2, 2k0]

    ||f||² ∝ ∫_{k0/2}^{2k0} k² dk = (1/3)[(2k0)³ - (k0/2)³] = (1/3)(8k0³ - k0³/8)
    ||∇f||² ∝ ∫_{k0/2}^{2k0} k⁴ dk = (1/5)[(2k0)⁵ - (k0/2)⁵]
    """
    a, b = k0/2, 2*k0
    I_L2 = (b**3 - a**3) / 3
    I_H1 = (b**5 - a**5) / 5

    L2 = np.sqrt(4 * np.pi * I_L2)
    H1 = np.sqrt(4 * np.pi * I_H1)

    C_eff = 3**0.25 * (L2/H1)**0.75
    return C_eff, L2, H1


# ============================================================================
# Compute and display results
# ============================================================================

print("="*70)
print("ANALYTICAL C_eff IN GAUSSIAN (RANDOM PHASE) REGIME")
print("="*70)

# Band-limited
print("\n--- Band-limited (uniform in [k0/2, 2k0]) ---")
for k0 in [2, 4, 8, 12, 16, 32, 64, 128]:
    C, L2, H1 = ceff_bandlimited_analytical(k0)
    print(f"  k0={k0:4d}: C_eff = {C:.6f}, ratio = {C/C_L_SCALAR:.4f}, "
          f"||f||/||∇f|| = {L2/H1:.6f}")

# Power-law with varying K_max
print("\n--- Power-law α=11/6 (Kolmogorov) with varying K_max ---")
for k_max in [10, 30, 100, 300, 1000, 3000, 10000]:
    C, L2, H1 = ceff_powerlaw_analytical(11.0/6.0, k_min=1, k_max=k_max)
    print(f"  K_max={k_max:6d}: C_eff = {C:.6f}, ratio = {C/C_L_SCALAR:.4f}")

# NS spectrum with varying Re
print("\n--- Kolmogorov spectrum with dissipation, varying Re ---")
for Re in [100, 300, 1000, 3000, 10000, 30000, 100000, 1e6, 1e9]:
    C, L2, H1 = ceff_kolmogorov_analytical(Re)
    print(f"  Re={Re:>10.0f}: C_eff = {C:.6f}, ratio = {C/C_L_SCALAR:.4f}, "
          f"k_d = {Re**0.75:.1f}")

# Fit the Re scaling
print("\n--- Scaling analysis: C_eff vs Re ---")
Re_vals = np.logspace(2, 9, 50)
C_vals = np.array([ceff_kolmogorov_analytical(Re)[0] for Re in Re_vals])

# Log-log fit
log_Re = np.log(Re_vals)
log_C = np.log(C_vals)
coeffs = np.polyfit(log_Re, log_C, 1)
exponent = coeffs[0]
prefactor = np.exp(coeffs[1])

print(f"  Power-law fit: C_eff ≈ {prefactor:.4f} × Re^{{{exponent:.4f}}}")
print(f"  Theoretical prediction: C_eff ~ Re^{{-3/8}} = Re^{{-0.3750}}")

# Compare with theoretical prediction
# C_eff = 3^{1/4} (||f||/||∇f||)^{3/4}
# For Kolmogorov: ||f||² ~ const, ||∇f||² ~ k_d^{4/3} ~ Re
# So C_eff ~ (1/Re^{1/2})^{3/4} = Re^{-3/8}
print(f"\n  For Re=1000: C_eff_analytical = {ceff_kolmogorov_analytical(1000)[0]:.6f}")
print(f"  For Re=1000: C_eff_formula = {3**0.25 * 2**0.375 * 1000**(-0.375):.6f}")

# Power-law spectra at various α
print("\n--- Power-law spectra, α varies, K_max = 1000 ---")
for alpha in [0.5, 5.0/6.0, 1.0, 1.5, 11.0/6.0, 2.0, 2.5, 3.0]:
    C, L2, H1 = ceff_powerlaw_analytical(alpha, k_min=1, k_max=1000)
    print(f"  α={alpha:.4f}: C_eff = {C:.6f}, ratio = {C/C_L_SCALAR:.4f}")

# The Bernstein bound for band-limited fields
print("\n--- Bernstein-type bound comparison ---")
print("  For a single band [k0/2, 2k0], Bernstein gives:")
print("  ||f||_{L⁴} ≤ C_B k0^{3/4} ||f||_{L²}")
print("  So C_{L,eff} = ||f||_{L⁴}/(||f||^{1/4}||∇f||^{3/4})")
print("  ≤ C_B k0^{3/4} ||f||^{3/4} / ||∇f||^{3/4}")
print("  ~ C_B (since ||∇f|| ~ k0 ||f|| for band-limited)")
print()
print("  But the Gaussian regime gives a TIGHTER bound because of phase cancellation:")
print("  ||f||_{L⁴} = 3^{1/4} ||f||_{L²} (not k0^{3/4} ||f||_{L²})")
print("  The k0^{3/4} in Bernstein is the worst case (constructive interference).")
print("  Random phases give 3^{1/4} instead.")

# Critical analysis: when does the Gaussian regime apply?
print("\n--- When does Gaussian regime apply? ---")
print("  By CLT: need N_modes >> 1 for each frequency band.")
print("  Shell at |k| = k has ~ 4πk² modes.")
print("  Gaussian for k ≥ 1: 4π×1² ≈ 13 modes (marginal)")
print("  Gaussian for k ≥ 3: 4π×9 ≈ 113 modes (good)")
print()
print("  Deviation from Gaussianity: O(1/sqrt(N_modes))")
print("  For the L⁴ moment: <f⁴>/<f²>² = 3 ± O(1/sqrt(N_modes))")

# Slack reduction analysis
print("\n" + "="*70)
print("SLACK REDUCTION ANALYSIS")
print("="*70)
print()
print("Original slack from GOAL.md: 158-237× total, Ladyzhenskaya contributes 63%")
print("of log-slack.")
print()
print("If we can replace C_L with C_{L,eff} = C_eff(Re), then:")
print("  Slack_new/Slack_old = (C_eff/C_L)^4 (since slack is in L⁴ norm, 4th power)")
print()

for Re in [1000, 10000, 100000]:
    C_eff = ceff_kolmogorov_analytical(Re)[0]
    ratio = C_eff / C_L_SCALAR
    slack_factor = ratio**4  # Fourth power because Ladyzhenskaya is an L⁴ bound
    # Actually the slack in the original is C_L⁴ × (other terms)
    # If we replace C_L with C_eff, the Ladyzhenskaya slack reduces by (C_eff/C_L)⁴
    print(f"  Re={Re:>7d}: C_eff={C_eff:.6f}, C_eff/C_L={ratio:.4f}, "
          f"slack reduction (C_eff/C_L)⁴ = {slack_factor:.6f} ({1/slack_factor:.1f}×)")

print()
print("The Ladyzhenskaya-dominated fraction of total slack:")
print("  If Ladyzhenskaya accounts for 63% of log(slack),")
print("  then log(slack_new) = log(slack_old) - 0.63×|log(C_eff/C_L)×4|")
print()

for Re in [1000, 10000, 100000]:
    C_eff = ceff_kolmogorov_analytical(Re)[0]
    ratio = C_eff / C_L_SCALAR
    old_slack = 200  # approximate midpoint of 158-237
    log_old = np.log(old_slack)
    log_reduction = 4 * np.log(1/ratio) * 0.63  # Ladyzhenskaya's share of log-slack
    new_slack = np.exp(log_old - log_reduction)
    print(f"  Re={Re:>7d}: Old slack ~ {old_slack}×, New slack ~ {new_slack:.1f}× "
          f"(reduction {old_slack/new_slack:.1f}×)")
