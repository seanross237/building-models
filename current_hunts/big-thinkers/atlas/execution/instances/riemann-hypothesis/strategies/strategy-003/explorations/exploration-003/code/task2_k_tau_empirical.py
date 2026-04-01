"""Task 2: K(τ) from Empirical R₂ (Non-Perturbative Fourier Transform)."""
import numpy as np

# Load R₂ data
r2_data = np.load('r2_empirical.npz')
r_grid = r2_data['r_grid']
R2 = r2_data['R2']
R2_GUE = r2_data['R2_GUE']
dr = r_grid[1] - r_grid[0]
r_max = r_grid[-1]

print(f"Loaded R₂: {len(R2)} points, r ∈ [{r_grid[0]:.3f}, {r_grid[-1]:.3f}], dr={dr:.4f}")

# Compute K(τ) = 1 + ∫₀^R_max (R₂(r)-1) × 2cos(2πτr) dr
# Using the symmetric relation: FT of R₂(r)-1 gives K(τ)-1
# Factor of 2 because we integrate only positive r and R₂(r) = R₂(-r)
tau_grid = np.linspace(0, 3, 301)

# Method: vectorized numerical integration
# K(τ) = 1 + 2 × ∫₀^r_max (R₂(r) - 1) × cos(2πτr) dr
K_empirical = np.zeros(len(tau_grid))
for i, tau in enumerate(tau_grid):
    integrand = (R2 - 1.0) * np.cos(2 * np.pi * tau * r_grid)
    K_empirical[i] = 1.0 + 2.0 * np.trapz(integrand, r_grid)

# Also compute K from GUE R₂ as a cross-check
K_from_GUE_R2 = np.zeros(len(tau_grid))
for i, tau in enumerate(tau_grid):
    integrand = (R2_GUE - 1.0) * np.cos(2 * np.pi * tau * r_grid)
    K_from_GUE_R2[i] = 1.0 + 2.0 * np.trapz(integrand, r_grid)

# K_GUE analytic: min(|τ|, 1)
K_GUE_analytic = np.minimum(np.abs(tau_grid), 1.0)

print(f"\nK(τ) comparison:")
print(f"{'τ':>5} {'K_empirical':>12} {'K_from_GUE_R2':>14} {'K_GUE_analytic':>15}")
for tau_val in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
    idx = int(tau_val / (tau_grid[1] - tau_grid[0]))
    if idx < len(tau_grid):
        print(f"{tau_val:5.1f} {K_empirical[idx]:12.6f} {K_from_GUE_R2[idx]:14.6f} {K_GUE_analytic[idx]:15.6f}")

print(f"\n--- Key reference values from GOAL.md ---")
print(f"K_zeros at τ=0.5: {K_empirical[50]:8.4f}  (expected ≈ 0.549)")
print(f"K_GUE at τ=0.5:   {K_GUE_analytic[50]:8.4f}  (expected = 0.500)")

# Check K(τ) features:
# 1. Is K(0) ≈ 0? (should be for a repulsive point process)
print(f"\nK(0) = {K_empirical[0]:.6f} (should be ~0)")
# 2. K(τ→∞) ≈ 1? (saturation)
print(f"K(3.0) = {K_empirical[-1]:.6f} (should be ~1)")
# 3. Is the ramp steeper than GUE?
# Compare slopes in τ ∈ [0.1, 0.8]
mask_ramp = (tau_grid >= 0.1) & (tau_grid <= 0.8)
slope_emp = np.polyfit(tau_grid[mask_ramp], K_empirical[mask_ramp], 1)[0]
slope_gue = 1.0  # K_GUE = τ for τ<1
print(f"\nRamp slope (τ ∈ [0.1, 0.8]):")
print(f"  Empirical: {slope_emp:.4f}")
print(f"  GUE: {slope_gue:.4f}")

# Save
np.savez('k_tau_empirical.npz', tau_grid=tau_grid, K_empirical=K_empirical,
         K_from_GUE_R2=K_from_GUE_R2, K_GUE=K_GUE_analytic)
print(f"\nSaved k_tau_empirical.npz")
