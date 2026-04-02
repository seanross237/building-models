#!/usr/bin/env python3
"""
Task 1: Compute K_primes(tau) from Berry's diagonal approximation.

K_primes(tau) = sum over prime orbits (p,m) of:
   (log p)^2 * Gaussian(tau - tau_pm, sigma) / (2*pi*rho_bar)^2

where tau_pm = m * log(p) / log(T_geo/(2*pi))
"""

import numpy as np
from sympy import primerange

# Load parameters
d = np.load('../exploration-003/data_zeros.npz')
T_geo = float(d['T_geo'])
rho_bar = float(d['rho_bar'])
print(f"T_geo = {T_geo:.4f}")
print(f"rho_bar = {rho_bar:.6f}")

log_T = np.log(T_geo / (2 * np.pi))
print(f"log(T_geo/(2*pi)) = {log_T:.6f}")

# Primes up to 2000 (covers 96%+ of weight)
primes = list(primerange(2, 2000))
print(f"Number of primes: {len(primes)}")
print(f"Largest prime: {primes[-1]}")

# tau grid
tau_grid = np.linspace(0.01, 3.0, 300)
sigma = 0.05

# Compute K_primes(tau) via diagonal approximation
K_density = np.zeros(len(tau_grid))
norm = (2 * np.pi * rho_bar) ** 2
print(f"Normalization (2*pi*rho_bar)^2 = {norm:.6f}")

orbit_count = 0
for p in primes:
    log_p = np.log(p)
    for m in range(1, 6):
        tau_pm = m * log_p / log_T
        if tau_pm > tau_grid[-1] + 3 * sigma:
            break
        weight = log_p ** 2
        K_density += weight * np.exp(-0.5 * ((tau_grid - tau_pm) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
        orbit_count += 1

K_primes = K_density / norm
print(f"Total orbits included: {orbit_count}")

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

# Check: does K_primes exceed 1.0 for tau > 1?
mask_gt1 = tau_grid > 1.0
if np.any(mask_gt1):
    max_K_gt1 = K_primes[mask_gt1].max()
    mean_K_gt1 = K_primes[mask_gt1].mean()
    print(f"\nFor tau > 1: max(K_primes) = {max_K_gt1:.6f}, mean(K_primes) = {mean_K_gt1:.6f}")
    print(f"K_primes exceeds 1.0 for tau > 1? {max_K_gt1 > 1.0}")

# Save results
np.savez('k_primes.npz', tau=tau_grid, K_primes=K_primes)
print("\nSaved k_primes.npz")
