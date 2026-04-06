"""
Careful verification of the PF5 boundary.

The previous test showed PF5 with evenly-spaced points has ONE failure at h=0.0998
with det = -2e-4. This could be numerical noise. We verify with:
1. Higher precision Phi computation
2. Finer h scan
3. Richardson extrapolation for the integral
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 50  # Very high precision

###############################################################################
# 1. Compute Phi with very high precision using mpmath quadrature
###############################################################################

def xi_mp(t):
    """Xi(1/2+it) using full mpmath precision."""
    t = mpmath.mpf(t)
    if abs(t) < mpmath.mpf('0.001'):
        s = mpmath.mpf('0.5')
    else:
        s = mpmath.mpc('0.5', t)
    val = mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
    return mpmath.re(val)

def phi_hp(u):
    """
    Phi(u) = 2 * integral_0^inf Xi(1/2+it) * cos(ut) dt
    Using mpmath's adaptive quadrature.
    """
    u_mp = mpmath.mpf(u)
    def integrand(t):
        return xi_mp(t) * mpmath.cos(u_mp * t)
    # Use multiple ranges to help convergence
    val = mpmath.quad(integrand, [0, 20, 40, 60], maxdegree=8)
    return 2 * float(val)

# Compute at key points
print("Computing Phi with high precision (mpmath quad)...")
phi_at = {}
for u in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    val = phi_hp(u)
    phi_at[u] = val
    print(f"  Phi({u:.2f}) = {val:.12f}")

###############################################################################
# 2. PF5 test at the critical h values
###############################################################################

print("\n=== PF5 Test with High-Precision Phi ===\n")

# For evenly-spaced points at spacing h, centered at 0:
# points = [-2h, -h, 0, h, 2h]
# Toeplitz matrix T_{ij} = Phi((i-j)*h) for i,j in {0,...,4}

# Actually for 5 points: pts[k] = (k-2)*h for k=0..4
# T_{ij} = Phi((i-j)*h) where i-j ranges from -4 to 4

# We need Phi at 0, h, 2h, 3h, 4h (and Phi is even)
def toeplitz_5_evenly(h):
    """5x5 Toeplitz determinant at spacing h."""
    phi_vals = [phi_hp(k*h) for k in range(5)]  # Phi(0), Phi(h), ..., Phi(4h)

    # T_{ij} = Phi(|i-j|*h)
    mat = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            mat[i][j] = phi_vals[abs(i-j)]
    return np.linalg.det(mat), mat, phi_vals

def toeplitz_6_evenly(h):
    """6x6 Toeplitz determinant at spacing h."""
    phi_vals = [phi_hp(k*h) for k in range(6)]

    mat = np.zeros((6, 6))
    for i in range(6):
        for j in range(6):
            mat[i][j] = phi_vals[abs(i-j)]
    return np.linalg.det(mat), mat, phi_vals

# Scan h values around the failure point h ~ 0.1
print("PF5 determinant scan (evenly-spaced, 5 points):")
print(f"{'h':>8s}  {'det':>14s}  {'Phi(h)':>12s}  {'Phi(2h)':>12s}  {'Phi(3h)':>12s}  {'Phi(4h)':>12s}")
print("-" * 75)

for h in np.arange(0.05, 0.15, 0.01):
    det, mat, pv = toeplitz_5_evenly(h)
    print(f"{h:8.4f}  {det:14.6e}  {pv[1]:12.6e}  {pv[2]:12.6e}  {pv[3]:12.6e}  {pv[4]:12.6e}")

print("\nFiner scan around h=0.10:")
for h in np.arange(0.08, 0.12, 0.002):
    det, mat, pv = toeplitz_5_evenly(h)
    sign = "NEG!" if det < 0 else "pos"
    print(f"  h={h:.4f}: det = {det:14.6e}  [{sign}]")

###############################################################################
# 3. PF6 determinant for verification
###############################################################################

print("\n\nPF6 determinant scan:")
print(f"{'h':>8s}  {'det':>14s}")
print("-" * 25)

for h in np.arange(0.05, 0.20, 0.01):
    det, mat, pv = toeplitz_6_evenly(h)
    sign = "NEG!" if det < 0 else "pos"
    print(f"{h:8.4f}  {det:14.6e}  [{sign}]")

###############################################################################
# 4. Eigenvalue analysis of the Toeplitz matrices
###############################################################################

print("\n\n=== Eigenvalue Analysis of Toeplitz Matrices ===")

for h in [0.1, 0.14, 0.2]:
    print(f"\nh = {h}:")

    for order in [5, 6]:
        phi_vals = [phi_hp(k*h) for k in range(order)]
        mat = np.zeros((order, order))
        for i in range(order):
            for j in range(order):
                mat[i][j] = phi_vals[abs(i-j)]

        eigvals = np.sort(np.linalg.eigvalsh(mat))
        det = np.prod(eigvals)
        print(f"  Order {order}: eigenvalues = {eigvals}")
        print(f"    det = {det:.6e}, min eigenvalue = {eigvals[0]:.6e}")

###############################################################################
# 5. The gamma factor's role
###############################################################################

print("\n\n=== Gamma Factor Contribution ===")
print("Testing: is the gamma factor the bottleneck?")
print()

# The gamma factor in Xi is: G(s) = (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2)
# On the critical line: G(1/2+it) = (1/2)*(1/2+it)*(-1/2+it)*pi^{-(1/4+it/2)}*Gamma(1/4+it/2)

def gamma_factor(t):
    """G(1/2+it)"""
    s = mpmath.mpc(0.5, t)
    return float(mpmath.re(0.5 * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2)))

# Compare: Xi = G * zeta, so in kernel terms:
# Phi_Xi = Phi_G * Phi_zeta (convolution... approximately)

# Actually this is wrong. Xi(s) = G(s) * zeta(s) means the kernel of Xi
# is the convolution of the kernels of G and zeta ONLY if both are
# "Fourier-compatible" in the right sense.

# More precisely: Xi(1/2+it) = G(1/2+it) * zeta(1/2+it)
# so the Fourier transform of Xi is the CONVOLUTION of the FT of G and FT of zeta.

# The FT of G:
print("Gamma factor kernel (FT of G(1/2+it)):")
t_grid_fine = np.linspace(0, 60, 4001)
dt_fine = t_grid_fine[1] - t_grid_fine[0]

G_vals = np.array([gamma_factor(t) for t in t_grid_fine])
print(f"G(1/2+i*0) = {G_vals[0]:.10f}")
print(f"Max |G| = {np.max(np.abs(G_vals)):.10f}")

# FT of G
def G_kernel(u):
    integrand = G_vals * np.cos(u * t_grid_fine)
    return 2 * np.trapz(integrand, dx=dt_fine)

# FT of zeta on the critical line
zeta_vals = np.array([float(mpmath.re(mpmath.zeta(mpmath.mpc(0.5, t)))) for t in t_grid_fine])

def zeta_kernel(u):
    integrand = zeta_vals * np.cos(u * t_grid_fine)
    return 2 * np.trapz(integrand, dx=dt_fine)

print("\nGamma kernel vs Zeta kernel:")
for u in [0, 0.1, 0.2, 0.5, 1.0]:
    gk = G_kernel(u)
    zk = zeta_kernel(u)
    pk = phi_hp(u)
    print(f"u={u:.1f}: Phi_G = {gk:.6e}, Phi_zeta = {zk:.6e}, Phi_Xi = {pk:.6e}")

# Test PF for gamma kernel alone
print("\nPF tests for gamma factor kernel alone:")
u_test = np.linspace(-2, 2, 101)
G_kernel_vals = np.array([G_kernel(u) for u in u_test])

# PF2 for G kernel
min_r = float('inf')
for i in range(1, len(G_kernel_vals)-1):
    if G_kernel_vals[i] > 0 and G_kernel_vals[i-1] > 0 and G_kernel_vals[i+1] > 0:
        r = G_kernel_vals[i]**2 / (G_kernel_vals[i-1] * G_kernel_vals[i+1])
        min_r = min(min_r, r)

print(f"  Gamma kernel PF2 min ratio: {min_r:.6f}")
print(f"  Gamma kernel PF2: {'PASS' if min_r >= 1-1e-6 else 'FAIL'}")

print("\n\nDone.")
