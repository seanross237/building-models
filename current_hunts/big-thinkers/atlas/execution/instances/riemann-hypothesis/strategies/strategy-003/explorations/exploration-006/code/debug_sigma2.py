#!/usr/bin/env python3
"""
Debug: Verify Sigma_2 and Delta_3 formulas against known GUE values.

Known GUE asymptotics (Mehta):
  Sigma_2(L) ~ (2/pi^2) [log(2*pi*L) + gamma + 1 - pi^2/8]  for large L
  Delta_3(L) ~ (1/pi^2) [log(L) - 0.0687]  for large L

gamma = Euler-Mascheroni constant = 0.5772...
"""

import numpy as np
from scipy import integrate

gamma_EM = 0.5772156649

def sigma2_asymptotic(L):
    """GUE asymptotic number variance"""
    return (2/np.pi**2) * (np.log(2*np.pi*L) + gamma_EM + 1 - np.pi**2/8)

def delta3_asymptotic(L):
    """GUE asymptotic Delta_3"""
    return (1/np.pi**2) * (np.log(L) - 0.0687)

# Method 1: Direct from GUE two-point cluster function
# Y_2(r) = (sin(pi*r)/(pi*r))^2  (cluster function / connected correlator)
# Sigma_2(L) = L - 2 * integral_0^L (L-r) * Y_2(r) dr

def sigma2_from_R2(L, n_pts=10000):
    """Compute Sigma_2 directly from GUE pair correlation"""
    r = np.linspace(1e-10, L, n_pts)
    Y2 = (np.sin(np.pi*r) / (np.pi*r))**2
    kernel = L - r
    integrand = kernel * Y2
    return L - 2 * np.trapezoid(integrand, r)

# Method 2: From form factor K(tau) = min(tau, 1)
# Formula: Sigma_2(L) = (2/pi^2) * integral_0^inf [1-K(tau)] * sin^2(pi*L*tau)/tau^2 dtau
# For K=min(tau,1): 1-K = 1-tau for tau<1, 0 for tau>1

def sigma2_from_K_v1(L, tau_max=10.0, n_pts=10000):
    """Original formula from goal"""
    eps = 1e-6
    tau = np.linspace(eps, tau_max, n_pts)
    K_gue = np.minimum(tau, 1.0)
    integrand = (1.0 - K_gue) * np.sin(np.pi*L*tau)**2 / tau**2
    return (2/np.pi**2) * np.trapezoid(integrand, tau)

# Method 3: The correct Fourier relation. Let me try with explicit integration range [0,1]:
def sigma2_from_K_v2(L, n_pts=10000):
    """Integral only over [0,1] where 1-K(tau) = 1-tau > 0"""
    eps = 1e-6
    tau = np.linspace(eps, 1.0, n_pts)
    integrand = (1.0 - tau) * np.sin(np.pi*L*tau)**2 / tau**2
    return (2/np.pi**2) * np.trapezoid(integrand, tau)

print("Comparing Sigma_2 methods:")
print(f"{'L':>5} {'asymptotic':>12} {'from R_2':>12} {'from K v1':>12} {'from K v2':>12}")
print("-" * 55)
for L in [2, 5, 10, 20, 30, 50]:
    s_a = sigma2_asymptotic(L)
    s_r = sigma2_from_R2(L)
    s_k1 = sigma2_from_K_v1(L)
    s_k2 = sigma2_from_K_v2(L)
    print(f"{L:5d} {s_a:12.6f} {s_r:12.6f} {s_k1:12.6f} {s_k2:12.6f}")

# Now compute Delta_3 via integral from Sigma_2 and compare to asymptotic
def delta3_from_sigma2(L, sigma2_func, n_pts=500):
    """Delta_3(L) = (2/L^4) integral_0^L (L^3 - 2*L^2*r + r^3) sigma2(r) dr"""
    r = np.linspace(0.01, L, n_pts)
    s2 = np.array([sigma2_func(ri) for ri in r])
    kernel = L**3 - 2*L**2*r + r**3
    integrand = kernel * s2
    return (2/L**4) * np.trapezoid(integrand, r)

print("\n\nComparing Delta_3 methods:")
print(f"{'L':>5} {'asymptotic':>12} {'from R_2->D3':>13} {'from K->D3':>12}")
print("-" * 45)
for L in [2, 5, 10, 15, 20, 30]:
    d_a = delta3_asymptotic(L)
    d_r = delta3_from_sigma2(L, sigma2_from_R2, n_pts=300)
    d_k = delta3_from_sigma2(L, sigma2_from_K_v2, n_pts=300)
    print(f"{L:5d} {d_a:12.6f} {d_r:13.6f} {d_k:12.6f}")

# Also check: is the issue that sin^2(pi*L*tau)/tau^2 needs different normalization?
# The Fourier transform pair: sinc^2(r) <-> max(1-|tau|, 0)
# integral sin^2(pi*L*tau)/(pi*tau)^2 dtau = L  (from -inf to inf)
# So integral sin^2(pi*L*tau)/(tau)^2 dtau = pi^2 * L
# And (2/pi^2) * integral 1 * sin^2(...)/tau^2 dtau = 2L
# While Sigma_2 for Poisson (K=0) should be L
# So maybe the normalization should be 1/pi^2 not 2/pi^2?

print("\n\nChecking normalization:")
eps = 1e-6
tau = np.linspace(eps, 100.0, 100000)
L = 10.0
val = np.trapezoid(np.sin(np.pi*L*tau)**2 / tau**2, tau)
print(f"integral sin^2(pi*L*tau)/tau^2 from 0 to 100: {val:.4f}")
print(f"pi^2 * L = {np.pi**2 * L:.4f}")
print(f"pi * L / 2 = {np.pi * L / 2:.4f}")
print(f"So (2/pi^2)*integral = {2/np.pi**2 * val:.4f}, should be L={L:.1f} for Poisson")
print(f"Or (1/pi^2)*integral = {1/np.pi**2 * val:.4f}")
