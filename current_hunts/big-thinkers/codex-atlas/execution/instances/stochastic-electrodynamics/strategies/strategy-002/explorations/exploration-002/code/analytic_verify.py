"""
Analytical verification of C_xx(d) for two SED oscillators sharing a ZPF.

Theory:
<x1(t) x2(t)> = (1/pi) * integral_0^{omega_max} |chi(omega)|^2 * cos(omega*d/c) * S_F(omega) d_omega

where chi(omega) = 1 / (m * (-omega^2 + omega0^2 - i*gamma*omega))
and gamma = tau * omega0^2

For near-resonance approximation:
C_xx(d) ≈ cos(omega0 * d / c) * exp(-gamma * d / (2*c))
"""
import numpy as np
from scipy.integrate import quad

omega0 = 1.0
m      = 1.0
hbar   = 1.0
tau    = 0.001
c      = 1.0
omega_max = 10.0

gamma = tau * omega0**2  # = 0.001

def S_F(omega):
    """One-sided ZPF force PSD"""
    if omega <= 0 or omega > omega_max:
        return 0.0
    return 2 * tau * hbar * omega**3 / m

def chi_sq(omega):
    """Squared magnitude of susceptibility"""
    denom = m**2 * ((omega0**2 - omega**2)**2 + (gamma * omega)**2)
    return 1.0 / denom

def integrand_var(omega):
    """Integrand for variance: |chi|^2 * S_F(omega)"""
    return chi_sq(omega) * S_F(omega) / np.pi

def integrand_corr(omega, d):
    """Integrand for cross-correlation: |chi|^2 * cos(omega*d/c) * S_F(omega)"""
    return chi_sq(omega) * S_F(omega) * np.cos(omega * d / c) / np.pi

# Compute var_x analytically
var_x, var_err = quad(integrand_var, 0, omega_max, limit=500)
print(f"Analytical var_x = {var_x:.6f}  (QM: {hbar/(2*m*omega0):.6f})")

# Compute C_xx(d) analytically for each separation
separations = [0.0, 0.1, 1.0, 10.0]
print("\nAnalytical C_xx(d):")
print(f"{'d':>6} | {'<x1x2>_analytic':>16} | {'C_xx_analytic':>13} | {'cos(w0*d/c)':>12}")
print("-" * 60)
for d in separations:
    corr, corr_err = quad(integrand_corr, 0, omega_max, args=(d,), limit=500)
    C_xx = corr / var_x  # Normalized by var_x (= var_x1 = var_x2)
    cos_pred = np.cos(omega0 * d / c) * np.exp(-gamma * d / (2 * c))
    print(f"{d:>6.1f} | {corr:>16.6f} | {C_xx:>13.6f} | {cos_pred:>12.6f}")

# More separations to see the oscillation
print("\nFiner d sweep (analytical):")
d_values = np.linspace(0, 20, 41)
print(f"{'d':>6} | {'C_xx_analytic':>13} | {'cos(w0*d/c)':>12}")
print("-" * 40)
for d in d_values:
    corr, _ = quad(integrand_corr, 0, omega_max, args=(d,), limit=200)
    C_xx = corr / var_x
    cos_pred = np.cos(omega0 * d / c) * np.exp(-gamma * d / (2 * c))
    print(f"{d:>6.2f} | {C_xx:>13.6f} | {cos_pred:>12.6f}")
