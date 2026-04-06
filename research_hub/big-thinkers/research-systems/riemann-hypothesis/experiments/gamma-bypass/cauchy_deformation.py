"""
Deep investigation of the Cauchy deformation and its implications.

Major discovery from hardy_z_and_alternatives.py:
- Multiplying Xi(t) by (1+lambda*t^2)^{-1} restores PF_5 at lambda ~ 0.005
- The sech deformation Xi(t)/cosh(lambda*t) even achieves PF_6 at lambda ~ 0.5

BUT: the fundamental theorem says convolution with PF_m gives min(old, m).
So how can these deformations INCREASE PF order??

Resolution: The fundamental theorem applies to CONVOLUTION IN KERNEL DOMAIN.
Multiplying Xi(t) by f(t) gives kernel = CONVOLUTION of old kernel with FT[f].
If FT[f] is PF_infinity, then min(PF_4, PF_inf) = PF_4. Can't increase.

BUT WAIT: the Cauchy kernel FT[1/(1+lambda*t^2)] = (pi/lambda) * exp(-|u|/sqrt(lambda))
This is NOT PF_infinity! It has a cusp at u=0 (not smooth).
Actually... exp(-a|u|) IS PF_infinity (it's the Laplace distribution kernel).

So the Cauchy deformation should give min(PF_4, PF_inf) = PF_4.
But we're seeing PF_5! This means either:
(a) Our numerical PF test is wrong, or
(b) The "fundamental theorem" doesn't apply as stated, or
(c) Something subtle about the deformation

Let's investigate carefully.
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 50

###############################################################################
# 1. Setup
###############################################################################

t_max = 60.0
N_pts = 4001
t_grid = np.linspace(0, t_max, N_pts)
dt = t_grid[1] - t_grid[0]

# Precompute Xi
print("Computing Xi...")
xi_vals = np.array([float(mpmath.re(mpmath.mpf('0.5') * mpmath.mpc('0.5', mpmath.mpf(t)) * (mpmath.mpc('0.5', mpmath.mpf(t)) - 1) * mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.zeta(mpmath.mpc('0.5', mpmath.mpf(t))))) for t in t_grid])
print("Done.")

def kernel(f_vals, u):
    integrand = f_vals * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

def toeplitz_det(kernel_func, h, order):
    vals = [kernel_func(k*h) for k in range(order)]
    mat = np.zeros((order, order))
    for i in range(order):
        for j in range(order):
            mat[i][j] = vals[abs(i-j)]
    return np.linalg.det(mat)

###############################################################################
# 2. The paradox: how does Cauchy deformation increase PF?
###############################################################################

print("\n=== The Cauchy Deformation Paradox ===\n")

# Xi_lambda(t) = Xi(t) / (1 + lambda*t^2)
# Kernel: K_lambda(u) = integral Xi(t)/(1+lambda*t^2) * cos(ut) dt
#
# This is NOT simply the convolution of Phi with FT[1/(1+lambda*t^2)].
# The reason: FT[f*g] = FT[f] * FT[g] only when f and g are both in L^1
# and we use the same transform convention. Here Xi decays super-exponentially,
# and 1/(1+lambda*t^2) decays only polynomially. The product is fine.
#
# Actually, FT[f*g](u) = (FT[f] conv FT[g])(u) (convolution theorem).
# This IS correct for our case: both functions are in L^1.
#
# FT[1/(1+lambda*t^2)](u) = (pi/sqrt(lambda)) * exp(-|u|/sqrt(lambda))
# = C * exp(-a|u|) for a = 1/sqrt(lambda)
#
# This kernel IS PF_infinity (Laplace distribution).
# So convolution with it should give min(PF_4, PF_inf) = PF_4.
#
# Yet numerically we see PF_5. Let's check more carefully.

# The issue might be: the PF test using evenly-spaced Toeplitz matrices
# at specific h values might miss the PF_5 failure at small h.

print("Careful PF5 test for Cauchy-deformed Xi at lambda=0.01:")
print("Testing many h values from 0.01 to 0.5")
print(f"{'h':>8s}  {'D4':>14s}  {'D5':>14s}  {'D6':>14s}  Signs")

xi_cauchy = xi_vals / (1 + 0.01 * t_grid**2)
K_cauchy = lambda u: kernel(xi_cauchy, u)

pf5_fails = 0
for h in np.arange(0.01, 0.51, 0.01):
    d4 = toeplitz_det(K_cauchy, h, 4)
    d5 = toeplitz_det(K_cauchy, h, 5)
    d6 = toeplitz_det(K_cauchy, h, 6)
    s4 = '+' if d4 > 0 else '-'
    s5 = '+' if d5 > 0 else '-'
    s6 = '+' if d6 > 0 else '-'
    if d5 < 0:
        pf5_fails += 1
        print(f"{h:8.3f}  {d4:14.6e}  {d5:14.6e}  {d6:14.6e}  {s4}{s5}{s6}  <-- PF5 FAIL")
    elif h < 0.12 or abs(h - 0.2) < 0.01 or abs(h - 0.3) < 0.01:
        print(f"{h:8.3f}  {d4:14.6e}  {d5:14.6e}  {d6:14.6e}  {s4}{s5}{s6}")

print(f"\nTotal PF5 failures out of 50 h values: {pf5_fails}")

###############################################################################
# 3. Very fine h scan near h = 0 for the deformed kernel
###############################################################################

print("\n\nVery fine h scan for Cauchy lambda=0.01:")
print(f"{'h':>10s}  {'D5':>14s}")

for h in [0.001, 0.002, 0.005, 0.008, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]:
    d5 = toeplitz_det(K_cauchy, h, 5)
    s = '+' if d5 > 0 else '-'
    print(f"{h:10.4f}  {d5:14.6e}  [{s}]")

###############################################################################
# 4. Use mpmath for high-precision PF5 test of the Cauchy-deformed kernel
###############################################################################

print("\n\n=== High-Precision PF5 Test (mpmath) ===\n")

def xi_mp(t):
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    return mpmath.re(mpmath.mpf('0.5') * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s))

def phi_cauchy_hp(u, lam):
    """High-precision kernel of Xi(t)/(1+lambda*t^2)."""
    u_mp = mpmath.mpf(u)
    lam_mp = mpmath.mpf(lam)
    def integrand(t):
        return xi_mp(t) / (1 + lam_mp * t**2) * mpmath.cos(u_mp * t)
    val = mpmath.quad(integrand, [0, 20, 40, 60], maxdegree=8)
    return float(2 * val)

def phi_hp(u):
    """High-precision kernel of Xi(t) (original)."""
    u_mp = mpmath.mpf(u)
    def integrand(t):
        return xi_mp(t) * mpmath.cos(u_mp * t)
    val = mpmath.quad(integrand, [0, 20, 40, 60], maxdegree=8)
    return float(2 * val)

print("High-precision D5 for original Xi at h=0.08:")
phi_orig = [phi_hp(k*0.08) for k in range(5)]
mat_orig = np.zeros((5,5))
for i in range(5):
    for j in range(5):
        mat_orig[i,j] = phi_orig[abs(i-j)]
print(f"  D5(Xi, h=0.08) = {np.linalg.det(mat_orig):.10e}")

print("\nHigh-precision D5 for Cauchy-deformed Xi (lambda=0.01) at h=0.08:")
phi_cauchy_vals = [phi_cauchy_hp(k*0.08, 0.01) for k in range(5)]
mat_cauchy = np.zeros((5,5))
for i in range(5):
    for j in range(5):
        mat_cauchy[i,j] = phi_cauchy_vals[abs(i-j)]
print(f"  D5(Xi_cauchy, h=0.08) = {np.linalg.det(mat_cauchy):.10e}")

# Also test at the critical h range
print("\nHigh-precision D5 scan (Cauchy lambda=0.01):")
for h in [0.05, 0.08, 0.1, 0.12]:
    vals = [phi_cauchy_hp(k*h, 0.01) for k in range(5)]
    mat = np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            mat[i,j] = vals[abs(i-j)]
    d5 = np.linalg.det(mat)
    print(f"  h={h}: D5 = {d5:.10e}  [{'PF5 OK' if d5 > 0 else 'PF5 FAIL'}]")

###############################################################################
# 5. Resolution of the paradox
###############################################################################

print("\n\n=== Resolution of the Paradox ===\n")

# Let's check: is the Cauchy-deformed kernel the convolution of Phi with
# the exponential kernel?
#
# If yes, then Schoenberg's theorem applies, and PF can't increase.
# If the numerical PF_5 holds at high precision, then either:
# (a) Schoenberg's theorem doesn't apply (conditions not met), or
# (b) The original kernel was actually PF_5 at these h values
#     (i.e., we were testing the wrong configurations)
#
# Wait: the PF test uses EVENLY-SPACED TOEPLITZ matrices.
# The PF_4/PF_5 status depends on the POINT CONFIGURATION.
# The Cauchy deformation changes the kernel shape, which changes
# WHICH h values produce positive/negative determinants.
#
# The original Xi has PF_5 failure at h ~ 0.05-0.11.
# The Cauchy deformation might shift this failure region.
# Let's check PF_5 of the original at h > 0.12:

print("Original Xi PF_5 at larger h values:")
for h in [0.12, 0.15, 0.2, 0.3, 0.4, 0.5]:
    vals = [phi_hp(k*h) for k in range(5)]
    mat = np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            mat[i,j] = vals[abs(i-j)]
    d5 = np.linalg.det(mat)
    print(f"  h={h}: D5 = {d5:.10e}")

print("\nOriginal Xi PF_5 at very small h:")
for h in [0.01, 0.02, 0.03, 0.04]:
    vals = [phi_hp(k*h) for k in range(5)]
    mat = np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            mat[i,j] = vals[abs(i-j)]
    d5 = np.linalg.det(mat)
    print(f"  h={h}: D5 = {d5:.10e}")

###############################################################################
# 6. The general Toeplitz PF test at shifted points
###############################################################################

print("\n\n=== PF_5 with shifted center (u0 != 0) for Cauchy-deformed ===\n")

# The prior experiment (pf4-modular) showed PF_5 fails only for u0 < 0.031.
# Does the Cauchy deformation fix this?

def toeplitz_det_shifted_hp(kfunc, u0, h, order):
    """Toeplitz determinant centered at u0."""
    vals = []
    for k in range(-(order-1), order):
        vals.append(kfunc(u0 + k*h))
    mat = np.zeros((order, order))
    for i in range(order):
        for j in range(order):
            idx = (i - j) + (order - 1)
            mat[i,j] = vals[idx]
    return np.linalg.det(mat)

print("Cauchy lambda=0.01, D5 at (u0, h) configurations:")
print(f"{'u0':>8s}  {'h':>8s}  {'D5':>14s}")

for u0 in [0.001, 0.01, 0.02, 0.03, 0.05]:
    for h in [0.01, 0.03, 0.05]:
        kfunc_c = lambda u: phi_cauchy_hp(u, 0.01)
        d5 = toeplitz_det_shifted_hp(kfunc_c, u0, h, 5)
        s = '+' if d5 > 0 else '-'
        print(f"{u0:8.3f}  {h:8.3f}  {d5:14.6e}  [{s}]")

print("\nOriginal Xi, same configurations:")
for u0 in [0.001, 0.01, 0.02, 0.03, 0.05]:
    for h in [0.01, 0.03, 0.05]:
        kfunc_o = lambda u: phi_hp(u)
        d5 = toeplitz_det_shifted_hp(kfunc_o, u0, h, 5)
        s = '+' if d5 > 0 else '-'
        print(f"{u0:8.3f}  {h:8.3f}  {d5:14.6e}  [{s}]")

###############################################################################
# 7. The de Bruijn-Newman BACKWARD direction
###############################################################################

print("\n\n=== De Bruijn-Newman: NEGATIVE Lambda ===\n")

# For NEGATIVE lambda, Xi_lambda(t) = Xi(t) * exp(lambda*t^2) with lambda < 0.
# This DAMPS the function (thinner tails), making the kernel BROADER.
# The kernel becomes more Gaussian, hence more PF.
#
# We saw: at lambda = -0.01, PF becomes 6+!
# But lambda < 0 means we're going in the direction AWAY from the known
# Lambda >= 0. However, PF_infinity at large negative lambda just means
# the Gaussian dominates and the function has no finite zeros.
#
# The interesting question: what is the CRITICAL lambda where PF jumps?

print("Finding critical lambda for PF_5 transition (at h=0.08):")
print(f"{'lambda':>12s}  {'D5':>14s}")

# Binary search for the transition
for lam in np.arange(-0.01, 0.001, 0.0005):
    xi_lam = xi_vals * np.exp(lam * t_grid**2)
    K_lam = lambda u, xv=xi_lam: kernel(xv, u)
    d5 = toeplitz_det(K_lam, 0.08, 5)
    s = '+' if d5 > 0 else '-'
    print(f"{lam:12.5f}  {d5:14.6e}  [{s}]")

###############################################################################
# 8. The "squared function" approach
###############################################################################

print("\n\n=== Xi^2 Investigation ===\n")

# Xi^2 was PF_6+ in all tests! Why?
# Xi^2(t) = Xi(t)^2 >= 0 for all real t.
# Its zeros are exactly the zeta zeros (with multiplicity 2).
# But Xi^2 doesn't have the functional equation in the usual sense.
#
# The kernel of Xi^2: K_{Xi^2}(u) = FT[Xi^2](u) = (Phi * Phi)(u) (autoconvolution).
# Schoenberg: autoconvolution of PF_k is PF_k. So Xi^2 should be PF_4.
# But we see PF_6+! What's going on?

# Actually, let's think more carefully:
# FT[Xi^2](u) = (Phi * Phi)(u) where * is convolution.
# This is the autoconvolution of Phi.
# Schoenberg says: convolution of PF_k with PF_m gives PF_{min(k,m)}.
# So autoconvolution of PF_4 gives PF_4.
#
# BUT: maybe the test just hasn't found the failure yet.
# Let me test more h values and shifted configurations.

print("Xi^2: exhaustive PF search at h = 0.01 to 0.5:")
K_sq = lambda u: kernel(xi_vals**2, u)

found_fail = False
for h in np.arange(0.01, 0.51, 0.005):
    dets = []
    for r in [4, 5, 6]:
        d = toeplitz_det(K_sq, h, r)
        dets.append(d)
    if dets[1] < 0:  # D5 fails
        print(f"  h={h:.3f}: D4={dets[0]:.2e} D5={dets[1]:.2e} D6={dets[2]:.2e}  <-- PF5 FAIL!")
        found_fail = True
    if dets[2] < 0:  # D6 fails
        print(f"  h={h:.3f}: D4={dets[0]:.2e} D5={dets[1]:.2e} D6={dets[2]:.2e}  <-- PF6 FAIL!")
        found_fail = True

if not found_fail:
    print("  No PF5 or PF6 failures found in 100 tests.")
    print("  Xi^2 appears to be PF_6+ or higher.")
    print("  But by Schoenberg, autoconvolution of PF_4 should be PF_4.")
    print()
    print("  RESOLUTION: The PF_4 status of Phi uses SHIFTED Toeplitz matrices")
    print("  (centered at u0 > 0). The unshifted test (centered at u0 = 0)")
    print("  might not capture the failure because Phi is even and the")
    print("  autoconvolution Phi*Phi is smoother (non-negative, broader).")
    print()
    print("  The PF_5 failure of Phi occurs at u0 < 0.031, h < 0.056.")
    print("  After autoconvolution, the failure region might shift or shrink.")

# Test with shifted center
print("\nXi^2: PF test with shifted center:")
for u0 in [0.001, 0.01, 0.02, 0.03]:
    for h in [0.01, 0.03, 0.05]:
        kfunc_sq = lambda u: kernel(xi_vals**2, u)
        d5 = toeplitz_det_shifted_hp(kfunc_sq, u0, h, 5)
        s = '+' if d5 > 0 else '-'
        marker = " <-- FAIL" if d5 < 0 else ""
        print(f"  u0={u0}, h={h}: D5 = {d5:.6e} [{s}]{marker}")

###############################################################################
# Save
###############################################################################

print("\n\nDone.")
