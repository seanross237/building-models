#!/usr/bin/env python3
"""
Debug Sigma_2 formula carefully.

Method 1 (gold standard): Direct from GUE cluster function
  Sigma_2(L) = L - 2 * integral_0^L (L-r) * [sin(pi*r)/(pi*r)]^2 dr

Method 2: From form factor via Fourier
  Sigma_2(L) = L - (2/pi^2) * integral_0^inf sin^2(pi*L*tau)/tau^2 * (1-K(tau)) dtau

For GUE: K(tau) = min(tau, 1), so 1-K = max(1-tau, 0), nonzero only for tau < 1:
  Sigma_2(L) = L - (2/pi^2) * integral_0^1 (1-tau) * sin^2(pi*L*tau)/tau^2 dtau

Known GUE asymptotic:
  Sigma_2(L) ~ (2/pi^2) * [ln(2*pi*L) + gamma + 1 - pi^2/8]
"""

import numpy as np
from scipy import integrate

gamma_EM = 0.5772156649

def sigma2_gue_asymptotic(L):
    return (2/np.pi**2) * (np.log(2*np.pi*L) + gamma_EM + 1 - np.pi**2/8)

# Method 1: Direct from cluster function with scipy quad
def sigma2_from_cluster(L):
    """Sigma_2(L) = L - 2 integral_0^L (L-r) sinc^2(r) dr"""
    def integrand(r):
        if r < 1e-15:
            return L * 1.0  # sinc(0)=1, kernel=L
        return (L - r) * (np.sin(np.pi*r) / (np.pi*r))**2
    result, err = integrate.quad(integrand, 0, L, limit=200)
    return L - 2 * result

# Method 2: From form factor with scipy quad
def sigma2_from_ff(L):
    """Sigma_2(L) = L - (2/pi^2) integral_0^1 (1-tau) sin^2(pi*L*tau)/tau^2 dtau"""
    def integrand(tau):
        if tau < 1e-15:
            return (1.0) * (np.pi*L)**2  # limit as tau->0
        return (1 - tau) * np.sin(np.pi*L*tau)**2 / tau**2
    result, err = integrate.quad(integrand, 0, 1, limit=200)
    return L - (2/np.pi**2) * result

# Compare all three
print(f"{'L':>5} {'asymptotic':>12} {'cluster':>12} {'form_factor':>12}")
print("-" * 45)
for L in [1, 2, 5, 10, 15, 20, 30, 50, 100]:
    s_a = sigma2_gue_asymptotic(L)
    s_c = sigma2_from_cluster(L)
    s_f = sigma2_from_ff(L)
    print(f"{L:5d} {s_a:12.6f} {s_c:12.6f} {s_f:12.6f}")

# Now compute Delta_3 from both Sigma_2 methods
def delta3_from_sigma2_func(L, sigma2_func):
    """Delta_3(L) = (2/L^4) integral_0^L (L^3-2L^2*r+r^3) sigma2(r) dr"""
    def integrand(r):
        kernel = L**3 - 2*L**2*r + r**3
        return kernel * sigma2_func(r)
    result, err = integrate.quad(integrand, 0.001, L, limit=200)
    return (2/L**4) * result

def delta3_asymptotic(L):
    return (1/np.pi**2) * (np.log(L) - 0.0687)

print(f"\n{'L':>5} {'D3_asymptotic':>14} {'D3_cluster':>12} {'D3_formfact':>13}")
print("-" * 48)
for L in [2, 5, 10, 15, 20, 25, 30]:
    d_a = delta3_asymptotic(L)
    d_c = delta3_from_sigma2_func(L, sigma2_from_cluster)
    d_f = delta3_from_sigma2_func(L, sigma2_from_ff)
    print(f"{L:5d} {d_a:14.6f} {d_c:12.6f} {d_f:13.6f}")

# Double check: what if there's a factor of 2 issue in K?
# Maybe K_GUE(tau) should be 2*min(tau,1) - some correction?
# Or maybe the formula involves 2*tau for GUE?
# Let's test K(tau) = 2*tau - tau*log(1+2*tau) (Haake COE formula, sometimes confused with GUE)
print("\n--- Testing alternative form factors ---")

# For GOE (beta=1): K(tau) = 2*tau - tau*log(1+2*tau) for tau<1
# For GUE (beta=2): K(tau) = min(2*tau, 2*tau - tau + 1) ... no
# Actually for GUE: b_2(tau) = 1 - max(1-tau, 0) = min(tau, 1). This IS K for GUE.
# But some refs define K differently.

# Dyson's b function for GUE:
# b_2(k) where k is in "natural" units such that mean spacing = 1
# b_2(k) = min(|k|, 1)
# Then Sigma_2(L) = 2*integral_0^inf |chi(k)|^2 (1-b_2(k)) dk   ... with what chi?

# Actually, I wonder if the conventional formula uses a different Fourier pair.
# The standard RMT formula (e.g., Guhr et al 1998, eq 3.62) is:
# Sigma_2(L) = integral_{-inf}^{inf} (sin(kL/2)/(k/2))^2 * [1 - Y(k)] dk / (2*pi)
# where Y(k) is the Fourier transform of Y_2(r) = sinc^2(r):
# Y(k) = max(1-|k|/(2*pi), 0)

# Then 1-Y(k) = min(|k|/(2*pi), 1)

# And Sigma_2(L) = (1/2*pi) integral (sin(kL/2)/(k/2))^2 * min(|k|/(2*pi), 1) dk
# = (1/pi) integral_0^inf (sin(kL/2)/(k/2))^2 * min(k/(2*pi), 1) dk

# Let tau = k/(2*pi):
# k = 2*pi*tau, dk = 2*pi*dtau
# sin(kL/2) = sin(pi*tau*L)
# k/2 = pi*tau
# min(k/(2*pi), 1) = min(tau, 1) = K_GUE(tau)

# Sigma_2(L) = (1/pi) integral_0^inf (sin(pi*tau*L)/(pi*tau))^2 * K_GUE(tau) * 2*pi dtau
# = 2 integral_0^inf sin^2(pi*tau*L)/(pi^2*tau^2) * K_GUE(tau) dtau
# = (2/pi^2) integral_0^inf sin^2(pi*L*tau)/tau^2 * K_GUE(tau) dtau

# But that has K, not (1-K)! Let me recheck.

# Guhr et al eq 3.62:
# Sigma^2(L) = (1/pi) integral_{-inf}^{inf} (sin^2(kL/2)/(k/2)^2) * (1 - b(k)) dk
# where b(k) = b_beta(k) is the spectral form factor

# With k = 2*pi*tau:
# = (1/pi) * 2*pi integral_0^inf sin^2(pi*L*tau)/(pi*tau)^2 * (1 - b(2*pi*tau)) dtau
# = 2 integral_0^inf sin^2(pi*L*tau)/(pi^2*tau^2) * (1 - b(2*pi*tau)) dtau
# = (2/pi^2) integral_0^inf sin^2(pi*L*tau)/tau^2 * (1 - b(2*pi*tau)) dtau

# Hmm but what is b(2*pi*tau)?
# Guhr et al define b(k) as the Fourier transform of (1-Y_2(r)):
# b(k) = integral (1-Y_2(r)) e^{ikr} dr
# For GUE: b(k) = delta(k) - integral Y_2(r) e^{ikr} dr

# No, Guhr et al eq 3.59:
# b_beta(k) = integral Y_2,beta(r) e^{ikr} dr  (Fourier transform of Y_2 with angular freq convention)

# For GUE: Y_2(r) = sinc^2(r) = (sin(pi*r)/(pi*r))^2
# b_2(k) = integral sinc^2(r) e^{ikr} dr
# With the angular frequency convention: this is the Fourier transform of sinc^2 at angular freq k.

# FT of sinc^2(r) = (sin(pi*r)/(pi*r))^2:
# Using the standard pair: sinc^2(r) <-> triangle(k/(2*pi))
# where triangle(x) = max(1-|x|, 0)
# In angular frequency: FT(sinc^2)(omega) = (1/(2*pi)) * triangle(omega/(2*pi))...

# Actually, let me be really careful. The standard Fourier pair with convention F(omega) = integral f(x) e^{-i*omega*x} dx:
# f(x) = sinc(x) = sin(pi*x)/(pi*x) -> F(omega) = rect(omega/(2*pi)) = 1 for |omega|<pi, 0 for |omega|>pi
# f(x) = sinc^2(x) -> F(omega) = triangle(omega/(2*pi)) = max(1-|omega|/(2*pi), 0) for |omega|<2*pi

# So b_2(k) = max(1 - |k|/(2*pi), 0)

# Then 1 - b_2(k) = min(|k|/(2*pi), 1)

# Sigma_2(L) = (1/pi) integral sin^2(kL/2)/(k/2)^2 * (1-b_2(k)) dk
# = (2/pi) integral_0^inf 4*sin^2(kL/2)/k^2 * min(k/(2*pi), 1) dk
# = (8/pi) integral_0^inf sin^2(kL/2)/k^2 * min(k/(2*pi), 1) dk

# Substituting u = k/(2*pi):
# k = 2*pi*u, dk = 2*pi*du, sin^2(kL/2) = sin^2(pi*u*L), k^2 = 4*pi^2*u^2
# min(k/(2*pi),1) = min(u,1)

# = (8/pi) * 2*pi integral_0^inf sin^2(pi*u*L)/(4*pi^2*u^2) * min(u,1) du
# = 16 integral_0^inf sin^2(pi*u*L)/(4*pi^2*u^2) * min(u,1) du
# = (4/pi^2) integral_0^inf sin^2(pi*L*u)/u^2 * min(u,1) du

# Hmm that doesn't look right either. Let me re-read Guhr et al.

# Actually, I think the issue is that Guhr eq 3.62 might use a specific normalization.

# Let me try a completely different approach. Just numerically verify:
print("\n=== Direct verification via integral ===")

# Compute Sigma_2(L=10) from cluster function (known correct)
L = 10.0
sigma2_exact = sigma2_from_cluster(L)
print(f"Sigma_2(L=10) from cluster function = {sigma2_exact:.6f}")

# Now try: (2/pi^2) integral_0^inf sin^2(pi*L*tau)/tau^2 * min(tau,1) dtau
def test_formula_A(L):
    """(2/pi^2) integral sin^2/tau^2 * K_GUE dtau"""
    def integrand(tau):
        return np.sin(np.pi*L*tau)**2 / tau**2 * min(tau, 1.0)
    r, e = integrate.quad(integrand, 1e-10, 50, limit=300)
    return (2/np.pi**2) * r

# (2/pi^2) integral sin^2/tau^2 * (1-K_GUE) dtau
def test_formula_B(L):
    def integrand(tau):
        return np.sin(np.pi*L*tau)**2 / tau**2 * max(1-tau, 0.0)
    r, e = integrate.quad(integrand, 1e-10, 1, limit=300)
    return (2/np.pi**2) * r

# L - (2/pi^2) integral sin^2/tau^2 * (1-K_GUE) dtau
def test_formula_C(L):
    return L - test_formula_B(L)

# (2/pi^2) integral (sin(pi*L*tau)/(pi*tau))^2 * (1-K_GUE) dtau
# This uses sinc^2 instead of sin^2/tau^2
def test_formula_D(L):
    def integrand(tau):
        if tau < 1e-15:
            return L**2 * max(1, 0.0)
        return (np.sin(np.pi*L*tau)/(np.pi*tau))**2 * max(1-tau, 0.0)
    r, e = integrate.quad(integrand, 0, 1, limit=300)
    return r

for L in [5, 10, 20, 30]:
    s_exact = sigma2_from_cluster(L)
    fA = test_formula_A(L)
    fB = test_formula_B(L)
    fC = test_formula_C(L) # = L - fB
    fD = test_formula_D(L)
    print(f"\nL={L}:")
    print(f"  Sigma_2 exact (cluster)  = {s_exact:.6f}")
    print(f"  (2/pi^2)*int K*sin2/tau2 = {fA:.6f}")
    print(f"  (2/pi^2)*int(1-K)*sin2/t2= {fB:.6f}")
    print(f"  L - above                = {fC:.6f}")
    print(f"  int sinc^2 * (1-K) dtau  = {fD:.6f}")
    print(f"  L - 2*(2/pi^2)*int(1-K)  = {L - 2*fB:.6f}")
    print(f"  asymptotic               = {sigma2_gue_asymptotic(L):.6f}")
