#!/usr/bin/env python3
"""
Task 1: Compute K_primes(tau) from Berry's diagonal approximation (corrected).

The trace formula for zeta zeros:
  d(E) = rho_bar + (1/pi) Re sum_p sum_m (log p / p^{m/2}) e^{i m E log p}

The diagonal approximation for the spectral form factor:
  K_diag(tau) = (1/T_H^2) sum_p sum_m (log p)^2 / p^m * delta(tau - tau_{p,m})

where T_H = 2*pi*rho_bar = log(T/(2*pi)) is the Heisenberg time,
      tau_{p,m} = m * log(p) / T_H is the scaled orbit period.

CRITICAL: The weight is (log p)^2 / p^m, NOT just (log p)^2.
The 1/p^m comes from |A_{p,m}|^2 where A is the semiclassical amplitude.
"""

import numpy as np
from sympy import primerange

# Load parameters
d = np.load('../exploration-003/data_zeros.npz')
T_geo = float(d['T_geo'])
rho_bar = float(d['rho_bar'])
print(f"T_geo = {T_geo:.4f}")
print(f"rho_bar = {rho_bar:.6f}")

T_H = 2 * np.pi * rho_bar  # Heisenberg time = log(T/(2pi))
log_T = np.log(T_geo / (2 * np.pi))
print(f"T_H = 2*pi*rho_bar = {T_H:.6f}")
print(f"log(T_geo/(2*pi)) = {log_T:.6f}")
print(f"These should be equal: diff = {abs(T_H - log_T):.2e}")

# Primes
primes = list(primerange(2, 2000))
print(f"Number of primes: {len(primes)}")

# tau grid
tau_grid = np.linspace(0.01, 3.0, 300)
sigma = 0.05

# Compute K_primes(tau) with CORRECT weight = (log p)^2 / p^m
K_density = np.zeros(len(tau_grid))
norm = T_H ** 2  # = (2*pi*rho_bar)^2

orbit_count = 0
total_weight = 0.0
for p in primes:
    log_p = np.log(p)
    for m in range(1, 20):  # more repetitions since weight decays as 1/p^m
        tau_pm = m * log_p / T_H
        if tau_pm > tau_grid[-1] + 3 * sigma:
            break
        weight = log_p ** 2 / (p ** m)  # CORRECTED: include 1/p^m
        total_weight += weight
        K_density += weight * np.exp(-0.5 * ((tau_grid - tau_pm) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
        orbit_count += 1

K_primes = K_density / norm
print(f"Total orbits included: {orbit_count}")
print(f"Total weight: {total_weight:.6f}")

# Report key values
key_taus = [0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]
print(f"\n{'tau':>6} {'K_primes':>12} {'K_GUE':>8} {'ratio':>10}")
print("-" * 40)
for t in key_taus:
    idx = np.argmin(np.abs(tau_grid - t))
    k_p = K_primes[idx]
    k_gue = min(t, 1.0)
    ratio = k_p / k_gue if k_gue > 0 else float('inf')
    print(f"{t:6.1f} {k_p:12.6f} {k_gue:8.3f} {ratio:10.4f}")

# Does K_primes exceed 1.0 for tau > 1?
mask_gt1 = tau_grid > 1.0
if np.any(mask_gt1):
    max_K_gt1 = K_primes[mask_gt1].max()
    mean_K_gt1 = K_primes[mask_gt1].mean()
    print(f"\nFor tau > 1: max(K_primes) = {max_K_gt1:.6f}, mean(K_primes) = {mean_K_gt1:.6f}")
    print(f"K_primes exceeds 1.0 for tau > 1? {max_K_gt1 > 1.0}")

# Also check behavior near tau=1
mask_near1 = (tau_grid > 0.8) & (tau_grid < 1.2)
print(f"\nK_primes near tau=1:")
for i in np.where(mask_near1)[0][::2]:
    print(f"  tau={tau_grid[i]:.3f}: K_primes={K_primes[i]:.6f}")

# Check: does K_primes ~ tau for small tau? (Berry's prediction)
mask_small = tau_grid < 0.3
small_taus = tau_grid[mask_small]
small_K = K_primes[mask_small]
if len(small_taus) > 2:
    slope = np.polyfit(small_taus, small_K, 1)[0]
    print(f"\nLinear fit K_primes ~ slope*tau for tau<0.3: slope = {slope:.4f}")
    print(f"  (should be ~1.0 if Berry's diag approx gives K=tau)")

# Save
np.savez('k_primes.npz', tau=tau_grid, K_primes=K_primes)
print("\nSaved k_primes.npz")

# Also save a version with finer grid for integration
tau_fine = np.linspace(0.001, 3.0, 3000)
K_density_fine = np.zeros(len(tau_fine))
for p in primes:
    log_p = np.log(p)
    for m in range(1, 20):
        tau_pm = m * log_p / T_H
        if tau_pm > tau_fine[-1] + 3 * sigma:
            break
        weight = log_p ** 2 / (p ** m)
        K_density_fine += weight * np.exp(-0.5 * ((tau_fine - tau_pm) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
K_primes_fine = K_density_fine / norm
np.savez('k_primes_fine.npz', tau=tau_fine, K_primes=K_primes_fine)
print("Saved k_primes_fine.npz (3000 points for integration)")
