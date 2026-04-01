#!/usr/bin/env python3
"""
Task 2: Compute Delta_3 from K_primes via the Wiener-Khinchin route.

Step 1: K(tau) -> Sigma_2(L) via:
  Sigma_2(L) = 2*L - (2/pi^2) * integral_0^tau_max K(tau)/tau^2 * sin^2(pi*L*tau) dtau

Step 2: Sigma_2(L) -> Delta_3(L) via:
  Delta_3(L) = (2/L^4) * integral_0^L (L^3 - 2*L^2*r + r^3) * Sigma_2(r) dr

Three versions of K(tau):
1. K_nocap: K_primes(tau) raw (decays past tau=1)
2. K_cap: min(K_primes(tau), 1.0) for all tau, then hard cap K=1 for tau > 1
3. K_GUE: min(tau, 1.0) for reference
"""

import numpy as np

# Load fine-grid K_primes
d = np.load('k_primes_fine.npz')
tau_fine = d['tau']
K_primes_fine = d['K_primes']
print(f"tau grid: {len(tau_fine)} points, [{tau_fine[0]:.4f}, {tau_fine[-1]:.4f}]")

# Load parameters
setup = np.load('setup.npz')
T_geo = float(setup['T_geo'])
rho_bar = float(setup['rho_bar'])

# Define three K(tau) versions
def K_nocap(tau):
    """Raw K_primes - interpolated from computed values"""
    return np.interp(tau, tau_fine, K_primes_fine)

def K_cap(tau):
    """K_primes with hard saturation cap: min(K_primes, 1) for tau <= 1, K=1 for tau > 1"""
    k = np.interp(tau, tau_fine, K_primes_fine)
    # For tau > 1, set K = 1 (GUE saturation)
    k = np.where(tau > 1.0, 1.0, k)
    # Also cap below at K = min(K_primes, 1) for tau < 1
    k = np.minimum(k, np.where(tau <= 1.0, tau_fine[-1]*10, 1.0))  # no cap needed for tau<1
    return k

def K_cap_v2(tau):
    """K_primes for tau <= 1, then K=1 for tau > 1"""
    k = np.interp(tau, tau_fine, K_primes_fine)
    k = np.where(tau > 1.0, 1.0, k)
    return k

def K_gue(tau):
    """GUE form factor: min(tau, 1)"""
    return np.minimum(tau, 1.0)

# Step 1: Compute Sigma_2(L) from K(tau)
# Sigma_2(L) = 2*L - (2/pi^2) * integral K(tau)/tau^2 * sin^2(pi*L*tau) dtau
# For unfolded eigenvalues, the number variance is:
# Sigma_2(L) = 2*L - 2*L^2 + (2*L^2/pi^2) * integral_0^inf (sin(pi*L*tau)/(pi*L*tau))^2 * (1-K(tau)) dtau
# Actually, the standard relation is:
# Sigma_2(L) = L - 2 integral_0^L (L-r) * (1-R2(r)) dr  where R2 is two-point correlation
#
# Or via form factor:
# Sigma_2(L) = integral_0^inf (sin(pi*L*tau)/(pi*tau))^2 * (1-K(tau)) dtau / (pi^2/2)
#
# Let me use the careful formula. For the form factor relation:
# Y_2(r) = 1 - R_2(r)/rho_bar^2  (cluster function, scaled)
# K(tau) = 1 - integral Y_2(r) e^{2*pi*i*r*tau} dr  (Fourier transform)
#
# The number variance:
# Sigma_2(L) = L - 2 integral_0^L (L-r) * [delta(r) - R_2(r)] dr
#            = L + 2 integral_0^L (L-r) * Y_2(r) dr  (subtracting Poisson term)
#
# Via Fourier (see Mehta Ch. 5):
# Sigma_2(L) = (2/pi^2) * integral_0^inf [1 - K(tau)] * sin^2(pi*L*tau) / tau^2 dtau
#
# This is the key formula. Note: for K(tau)=1, Sigma_2=0 (rigid).
# For K(tau)=0, Sigma_2 = 2*L*(1/pi^2)*integral sin^2/tau^2 = L (Poisson).

def compute_sigma2(L, K_func, tau_max=10.0, n_pts=10000):
    """
    Sigma_2(L) = (2/pi^2) * integral_0^tau_max [1 - K(tau)] * sin^2(pi*L*tau) / tau^2 dtau
    """
    # Use integration on [epsilon, tau_max] to avoid tau=0 singularity
    # Near tau=0: [1-K(tau)] ~ 1 - tau (for GUE-like) so integrand ~ (1-tau)*L^2*pi^2 which is finite
    eps = 1e-4
    tau = np.linspace(eps, tau_max, n_pts)
    dt = tau[1] - tau[0]

    K_vals = K_func(tau)
    integrand = (1.0 - K_vals) * np.sin(np.pi * L * tau)**2 / tau**2

    result = (2.0 / np.pi**2) * np.trapezoid(integrand, tau)
    return result

# Step 2: Compute Delta_3(L) from Sigma_2
# Delta_3(L) = (2/L^4) * integral_0^L (L^3 - 2*L^2*r + r^3) * Sigma_2(r) dr

def compute_delta3(L, K_func, n_r=200, tau_max=10.0):
    """Compute Delta_3(L) via exact formula."""
    r_grid = np.linspace(0.01, L, n_r)
    dr = r_grid[1] - r_grid[0]

    sigma2_vals = np.array([compute_sigma2(r, K_func, tau_max=tau_max) for r in r_grid])
    kernel = L**3 - 2*L**2*r_grid + r_grid**3

    integrand = kernel * sigma2_vals
    delta3 = (2.0 / L**4) * np.trapezoid(integrand, r_grid)
    return delta3

# Compute for L values
L_values = np.array([2, 5, 8, 10, 12, 15, 18, 20, 22, 25, 27, 30], dtype=float)

print("Computing Delta_3 for three K(tau) models...")
print("This will take a while...\n")

results = {}
for label, K_func in [('nocap', K_nocap), ('cap', K_cap_v2), ('GUE', K_gue)]:
    print(f"\n--- {label} ---")
    delta3_vals = []
    for L in L_values:
        d3 = compute_delta3(L, K_func, n_r=150, tau_max=8.0)
        delta3_vals.append(d3)
        print(f"  L={L:5.1f}: Delta_3 = {d3:.6f}")
    results[label] = np.array(delta3_vals)

# Print comparison table
print(f"\n{'L':>5} {'nocap':>12} {'cap':>12} {'GUE':>12} {'E003 measured':>14}")
print("-" * 58)
# E003 measured values (approximate from E003 report)
e003_L = {5: 0.075, 10: 0.117, 15: 0.135, 20: 0.148, 25: 0.155, 30: 0.160}
for i, L in enumerate(L_values):
    e003 = e003_L.get(int(L), float('nan'))
    print(f"{L:5.1f} {results['nocap'][i]:12.6f} {results['cap'][i]:12.6f} {results['GUE'][i]:12.6f} {e003:14.3f}")

# Saturation values (average over L=20-30)
mask_sat = L_values >= 20
for label in ['nocap', 'cap', 'GUE']:
    sat_val = results[label][mask_sat].mean()
    print(f"\nDelta_3_sat (avg L=20-30) for {label}: {sat_val:.6f}")

# Save
np.savez('delta3_primes.npz', L_values=L_values,
         delta3_nocap=results['nocap'],
         delta3_cap=results['cap'],
         delta3_gue=results['GUE'])
print("\nSaved delta3_primes.npz")
