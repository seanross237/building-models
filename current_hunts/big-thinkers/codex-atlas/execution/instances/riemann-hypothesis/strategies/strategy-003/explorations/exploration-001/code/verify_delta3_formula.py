"""
Step 1: Verify the correct formula for Delta_3(L) in terms of the form factor K(tau).

The standard result (Mehta, Haake):

  Sigma_2(L) = (2/pi^2) int_0^inf K(tau)/tau^2 sin^2(pi*L*tau) dtau   ... (*)

  Delta_3(L) = L/15 + (2/L^4) int_0^L (L-r)^2 (2Lr - r^2) [R2(r)-1] dr  ... (**)

where R2(r) - 1 = 2 int_0^inf (K(tau)-1) cos(2*pi*tau*r) dtau

Combining: Delta_3(L) via form factor directly.

Verification: for K_GUE(tau) = min(|tau|, 1), Delta_3_GUE(L=20) should be ~0.28.
"""

import numpy as np
from scipy.integrate import quad as scipy_quad

# =============================================================================
# GUE form factor and pair correlation
# =============================================================================
def K_GUE(tau):
    """GUE form factor: K = |tau| for |tau|<1, 1 for |tau|>=1"""
    tau = abs(tau)
    return min(tau, 1.0)

def R2_GUE(r):
    """GUE pair correlation: R2(r) = 1 - (sin(pi*r)/(pi*r))^2"""
    if abs(r) < 1e-15:
        return 0.0
    sinc = np.sin(np.pi * r) / (np.pi * r)
    return 1.0 - sinc**2

# =============================================================================
# Test 1: Compute Sigma_2 from K(tau)
# =============================================================================
print("=" * 60)
print("Test 1: Sigma_2 from K(tau)")
print("=" * 60)

def sigma2_from_K(L, K_func, tau_max=50.0, n_points=10000):
    """Sigma_2(L) = (2/pi^2) int_0^inf K(tau)/tau^2 sin^2(pi*L*tau) dtau"""
    # Numerical integration with fine grid
    tau_vals = np.linspace(1e-10, tau_max, n_points)
    dtau = tau_vals[1] - tau_vals[0]
    K_vals = np.array([K_func(t) for t in tau_vals])
    integrand = K_vals / tau_vals**2 * np.sin(np.pi * L * tau_vals)**2
    return (2.0 / np.pi**2) * np.trapezoid(integrand, tau_vals)

def sigma2_from_R2(L, R2_func, n_points=5000):
    """Sigma_2(L) = L + 2 int_0^L (L-r)(R2(r)-1) dr"""
    r_vals = np.linspace(1e-10, L, n_points)
    dr = r_vals[1] - r_vals[0]
    R2_vals = np.array([R2_func(r) for r in r_vals])
    integrand = (L - r_vals) * (R2_vals - 1.0)
    return L + 2.0 * np.trapezoid(integrand, r_vals)

# Known GUE asymptotic: Sigma_2(L) ~ (2/pi^2)(log(2*pi*L) + gamma + 1 - pi^2/8)
gamma_E = 0.5772156649
print(f"\n{'L':>5s} {'Sigma2_K':>12s} {'Sigma2_R2':>12s} {'Asymptotic':>12s}")
print("-" * 50)
for L in [1, 2, 5, 10, 20, 50]:
    s2_K = sigma2_from_K(L, K_GUE, tau_max=100, n_points=20000)
    s2_R2 = sigma2_from_R2(L, R2_GUE, n_points=10000)
    s2_asymp = (2.0 / np.pi**2) * (np.log(2*np.pi*L) + gamma_E + 1 - np.pi**2/8)
    print(f"{L:5d} {s2_K:12.6f} {s2_R2:12.6f} {s2_asymp:12.6f}")

# =============================================================================
# Test 2: Compute Delta_3 from R2 using CORRECT formula
# =============================================================================
print("\n" + "=" * 60)
print("Test 2: Delta_3 from R2")
print("=" * 60)

def delta3_from_R2(L, R2_func, n_points=5000):
    """Delta_3(L) = L/15 + (2/L^4) int_0^L (L-r)^2 (2Lr-r^2) (R2(r)-1) dr"""
    r_vals = np.linspace(1e-10, L, n_points)
    R2_vals = np.array([R2_func(r) for r in r_vals])
    kernel = (L - r_vals)**2 * (2*L*r_vals - r_vals**2)
    integrand = kernel * (R2_vals - 1.0)
    integral = np.trapezoid(integrand, r_vals)
    return L/15.0 + (2.0 / L**4) * integral

# Known GUE asymptotic: Delta_3(L) ~ (1/2pi^2)(log(2*pi*L) + gamma + 1 - pi^2/8) + 1/(4*pi^2)
# More precisely: Delta_3(L) ~ (1/pi^2)[log(L) + gamma - 5/4 - pi^2/8 + log(2*pi)] ... various forms
# The simplest: Delta_3 ~ Sigma_2 / 2 approximately
# Actually: Delta_3(L) ~ (1/pi^2)(log(L) - 0.0687) for large L

print(f"\n{'L':>5s} {'Delta3_R2':>12s} {'(1/pi^2)logL':>12s} {'Sigma2/4':>12s}")
print("-" * 50)
for L in [1, 2, 5, 10, 20, 30, 50]:
    d3 = delta3_from_R2(L, R2_GUE, n_points=10000)
    d3_approx = (1.0/np.pi**2) * np.log(L)
    s2 = sigma2_from_R2(L, R2_GUE)
    print(f"{L:5d} {d3:12.6f} {d3_approx:12.6f} {s2/4:12.6f}")

# =============================================================================
# Test 3: Compute Delta_3 directly from form factor K(tau)
# =============================================================================
print("\n" + "=" * 60)
print("Test 3: Delta_3 from K(tau) via double integral")
print("=" * 60)

def delta3_from_K(L, K_func, tau_max=50.0, n_tau=5000, n_r=2000):
    """
    Delta_3(L) = L/15 + (4/L^4) int_0^inf (K(tau)-1) I(tau,L) dtau
    where I(tau,L) = int_0^L (L-r)^2 (2Lr-r^2) cos(2*pi*tau*r) dr
    """
    tau_vals = np.linspace(1e-10, tau_max, n_tau)
    K_minus_1 = np.array([K_func(t) - 1.0 for t in tau_vals])

    # Compute the inner integral I(tau, L) for each tau
    r_vals = np.linspace(1e-10, L, n_r)
    kernel_r = (L - r_vals)**2 * (2*L*r_vals - r_vals**2)

    I_vals = np.zeros(len(tau_vals))
    for i, tau in enumerate(tau_vals):
        cos_vals = np.cos(2*np.pi*tau*r_vals)
        I_vals[i] = np.trapezoid(kernel_r * cos_vals, r_vals)

    # Outer integral
    integrand = K_minus_1 * I_vals
    integral = np.trapezoid(integrand, tau_vals)

    return L/15.0 + (4.0 / L**4) * integral

print(f"\n{'L':>5s} {'D3_fromR2':>12s} {'D3_fromK':>12s} {'Ratio':>8s}")
print("-" * 40)
for L in [1, 2, 5, 10, 20, 30, 50]:
    d3_r2 = delta3_from_R2(L, R2_GUE, n_points=10000)
    d3_k = delta3_from_K(L, K_GUE, tau_max=100, n_tau=10000, n_r=5000)
    ratio = d3_k / d3_r2 if abs(d3_r2) > 1e-10 else float('nan')
    print(f"{L:5d} {d3_r2:12.6f} {d3_k:12.6f} {ratio:8.4f}")

# =============================================================================
# Test 4: Alternative direct formula from form factor
# =============================================================================
print("\n" + "=" * 60)
print("Test 4: Delta_3 via Sigma_2 -> Dyson-Mehta integral")
print("=" * 60)

def delta3_via_sigma2(L, K_func, n_points_r=500, tau_max=50, n_tau=10000):
    """
    Step 1: Compute Sigma_2(r) for r in [0, L]
    Step 2: Delta_3(L) = (2/L^4) int_0^L (L^3 - 2L^2 r + r^3) Sigma_2(r) dr

    Note: This is the claimed formula from strategy notes. Need to verify.
    """
    r_vals = np.linspace(1e-10, L, n_points_r)

    # Compute Sigma_2 at each r
    s2_vals = np.array([sigma2_from_K(r, K_func, tau_max=tau_max, n_points=n_tau) for r in r_vals])

    # Dyson-Mehta kernel
    kernel = L**3 - 2*L**2*r_vals + r_vals**3
    integrand = kernel * s2_vals
    integral = np.trapezoid(integrand, r_vals)

    return (2.0 / L**4) * integral

# Check this formula too
print(f"\n{'L':>5s} {'D3_fromR2':>12s} {'D3_viaSig2':>12s}")
print("-" * 30)
for L in [5, 10, 20]:
    d3_r2 = delta3_from_R2(L, R2_GUE, n_points=10000)
    d3_s2 = delta3_via_sigma2(L, K_GUE, n_points_r=200, tau_max=50, n_tau=5000)
    print(f"{L:5d} {d3_r2:12.6f} {d3_s2:12.6f}")

print("\nDone.")
