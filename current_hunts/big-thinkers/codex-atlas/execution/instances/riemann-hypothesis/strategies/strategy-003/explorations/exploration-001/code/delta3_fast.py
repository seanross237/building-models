"""
FAST computation: Delta_3 with Berry-Keating corrections.

Strategy: Pre-compute R1_c and R2_c on a grid once, then interpolate for all integrals.
This reduces mpmath calls from millions to ~2000.
"""

import numpy as np
from mpmath import mp, mpf, zeta as mp_zeta, log as mp_log, pi as mp_pi
import time

mp.dps = 20

T = 1682.0
d_bar = float(mp_log(T / (2 * mp_pi)) / (2 * mp_pi))
print(f"T = {T}, d_bar = {d_bar:.6f}")

from sympy import primerange
primes = list(primerange(2, 2000))
print(f"Primes: {len(primes)}")

# =============================================================================
# Pre-compute R1_c and R2_c on a grid
# =============================================================================
print("\n=== Pre-computing corrections on grid ===")
t0 = time.time()

x_grid = np.concatenate([
    np.linspace(0.01, 1.0, 100),
    np.linspace(1.0, 5.0, 100),
    np.linspace(5.0, 20.0, 100),
    np.linspace(20.0, 60.0, 80),
])
x_grid = np.unique(x_grid)
print(f"Grid points: {len(x_grid)}")

# --- R1_c ---
def compute_R1_c(x):
    """Eq (4.23) of Berry-Keating 1999"""
    if abs(x) < 1e-12:
        return 0.0
    xi = x / d_bar
    prefactor = 1.0 / (2.0 * (np.pi * d_bar)**2)

    term1 = 1.0 / xi**2

    # Numerical second derivative of Re log zeta(1-i*xi)
    h = max(abs(xi) * 1e-4, 1e-5)
    def lzr(xi_val):
        s = mpf(1) - mpf(xi_val) * mpf(1j)
        z = complex(mp_zeta(s))
        return np.log(abs(z)) if abs(z) > 1e-300 else 0.0
    try:
        d2 = (lzr(xi+h) + lzr(xi-h) - 2*lzr(xi)) / h**2
    except:
        d2 = 0.0

    # Sum over primes
    term3 = 0.0
    for p in primes[:200]:
        logp = np.log(p)
        denom = p * np.exp(1j * xi * logp) - 1.0
        if abs(denom) > 1e-15:
            term3 -= (logp**2 / denom**2).real

    return prefactor * (term1 - d2 + term3)

# --- R2_c ---
def compute_R2_c(x):
    """Eq (4.27)-(4.28) of Berry-Keating 1999"""
    if abs(x) < 1e-12:
        return 0.0
    xi = x / d_bar
    prefactor = 1.0 / (2.0 * (np.pi * d_bar)**2)

    term1 = -np.cos(2 * np.pi * x) / xi**2

    try:
        z = complex(mp_zeta(mpf(1) + mpf(xi) * mpf(1j)))
        zeta_abs_sq = abs(z)**2
    except:
        zeta_abs_sq = 1.0 / xi**2

    # Product b(xi)
    b_val = 1.0 + 0j
    for p in primes[:150]:
        p_ixi = p**(1j * xi)
        b_val *= (1.0 - (p_ixi - 1.0)**2 / (p - 1.0)**2)

    exp_2pix = np.exp(2j * np.pi * x)
    term2 = zeta_abs_sq * (exp_2pix * b_val).real

    return prefactor * (term1 + term2)

# Compute on grid
R1c_grid = np.zeros(len(x_grid))
R2c_grid = np.zeros(len(x_grid))

for i, x in enumerate(x_grid):
    R1c_grid[i] = compute_R1_c(x)
    R2c_grid[i] = compute_R2_c(x)
    if (i+1) % 50 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{len(x_grid)} done ({elapsed:.0f}s)")

elapsed = time.time() - t0
print(f"Grid computation done in {elapsed:.0f}s")

# Save grid
np.savez('code/correction_grid.npz', x_grid=x_grid, R1c=R1c_grid, R2c=R2c_grid, T=T, d_bar=d_bar)

# =============================================================================
# Interpolation functions
# =============================================================================
def R_GUE(x):
    if abs(x) < 1e-15:
        return 0.0
    return 1.0 - (np.sin(np.pi * x) / (np.pi * x))**2

def R1c_interp(x):
    if x < x_grid[0] or x > x_grid[-1]:
        return 0.0
    return np.interp(x, x_grid, R1c_grid)

def R2c_interp(x):
    if x < x_grid[0] or x > x_grid[-1]:
        return 0.0
    return np.interp(x, x_grid, R2c_grid)

# =============================================================================
# Sigma_2 and Delta_3
# =============================================================================
def sigma2(L, R2_func, n_points=3000):
    """Sigma_2(L) = L + 2 int_0^L (L-r)(R2(r)-1) dr"""
    if L < 1e-10: return 0.0
    r = np.linspace(1e-10, L, n_points)
    R2 = np.array([R2_func(ri) for ri in r])
    return L + 2.0 * np.trapezoid((L - r) * (R2 - 1.0), r)

def delta3(L, sigma2_func, n_points=300):
    """Delta_3(L) = (2/L^4) int_0^L (L^3-2L^2r+r^3) Sigma_2(r) dr"""
    if L < 0.5: return L / 15.0
    r = np.linspace(0.01, L, n_points)
    s2 = np.array([sigma2_func(ri) for ri in r])
    kernel = L**3 - 2*L**2*r + r**3
    return (2.0 / L**4) * np.trapezoid(kernel * s2, r)

# =============================================================================
# MAIN: Compute Delta_3 for all scenarios
# =============================================================================
print("\n" + "="*70)
print("COMPUTING DELTA_3")
print("="*70)

# Define R2 variants
def R2_gue(x): return R_GUE(x)
def R2_diag(x): return R_GUE(x) + R1c_interp(x)
def R2_offdiag(x): return R_GUE(x) + R2c_interp(x)
def R2_full(x): return R_GUE(x) + R1c_interp(x) + R2c_interp(x)

# Define Sigma_2 variants
def s2_gue(r): return sigma2(r, R2_gue)
def s2_diag(r): return sigma2(r, R2_diag)
def s2_offdiag(r): return sigma2(r, R2_offdiag)
def s2_full(r): return sigma2(r, R2_full)

# First: Sigma_2 comparison
print("\n--- Sigma_2 values ---")
print(f"{'L':>5s} {'GUE':>10s} {'+R1c':>10s} {'+R2c':>10s} {'Full':>10s}")
print("-"*50)
for L in [1, 2, 5, 10, 15, 20, 30, 50]:
    sg = s2_gue(L)
    sd = s2_diag(L)
    so = s2_offdiag(L)
    sf = s2_full(L)
    print(f"{L:5d} {sg:10.6f} {sd:10.6f} {so:10.6f} {sf:10.6f}")

# Delta_3 computation
print("\n--- Delta_3 values ---")
L_values = [2, 5, 10, 15, 20, 25, 30, 40, 50]

berry_pred = (1.0/np.pi**2) * np.log(np.log(T/(2*np.pi)))
print(f"\nBerry prediction (T={T}): {berry_pred:.6f}")
print(f"Target (zeta zeros): 0.155\n")

print(f"{'L':>5s} {'GUE':>10s} {'GUE+R1c':>10s} {'GUE+R2c':>10s} {'Full':>10s}")
print("-"*50)

results = {'L': [], 'GUE': [], 'diag': [], 'offdiag': [], 'full': []}
t0 = time.time()

for L in L_values:
    d3_g = delta3(L, s2_gue)
    d3_d = delta3(L, s2_diag)
    d3_o = delta3(L, s2_offdiag)
    d3_f = delta3(L, s2_full)

    results['L'].append(L)
    results['GUE'].append(d3_g)
    results['diag'].append(d3_d)
    results['offdiag'].append(d3_o)
    results['full'].append(d3_f)

    elapsed = time.time() - t0
    print(f"{L:5d} {d3_g:10.6f} {d3_d:10.6f} {d3_o:10.6f} {d3_f:10.6f}  [{elapsed:.0f}s]")

# Save
np.savez('code/delta3_fast_results.npz',
         L=np.array(results['L']),
         d3_GUE=np.array(results['GUE']),
         d3_diag=np.array(results['diag']),
         d3_offdiag=np.array(results['offdiag']),
         d3_full=np.array(results['full']),
         T=T, d_bar=d_bar, berry_pred=berry_pred)

# =============================================================================
# ANALYSIS
# =============================================================================
print("\n" + "="*70)
print("ANALYSIS")
print("="*70)

target = 0.155
idx20 = results['L'].index(20)

d3g = results['GUE'][idx20]
d3d = results['diag'][idx20]
d3o = results['offdiag'][idx20]
d3f = results['full'][idx20]

print(f"\nAt L=20:")
print(f"  Target:         {target}")
print(f"  GUE only:       {d3g:.6f}  (error: {abs(d3g-target)/target*100:.1f}%)")
print(f"  GUE + R1_c:     {d3d:.6f}  (error: {abs(d3d-target)/target*100:.1f}%)")
print(f"  GUE + R2_c:     {d3o:.6f}  (error: {abs(d3o-target)/target*100:.1f}%)")
print(f"  Full:           {d3f:.6f}  (error: {abs(d3f-target)/target*100:.1f}%)")
print(f"  Berry formula:  {berry_pred:.6f}  (error: {abs(berry_pred-target)/target*100:.1f}%)")

gap = d3g - target
if abs(gap) > 1e-6:
    print(f"\n  Gap = {gap:.6f}")
    print(f"  R1_c direction: {'closes' if d3d < d3g else 'OPENS'} gap by {abs(d3g-d3d):.6f} ({abs(d3g-d3d)/abs(gap)*100:.1f}%)")
    print(f"  R2_c direction: {'closes' if d3o < d3g else 'OPENS'} gap by {abs(d3g-d3o):.6f} ({abs(d3g-d3o)/abs(gap)*100:.1f}%)")
    print(f"  Full direction: {'closes' if d3f < d3g else 'OPENS'} gap by {abs(d3g-d3f):.6f} ({abs(d3g-d3f)/abs(gap)*100:.1f}%)")

# =============================================================================
# HEIGHT DEPENDENCE
# =============================================================================
print("\n" + "="*70)
print("HEIGHT DEPENDENCE")
print("="*70)

for T_test in [600, 1682, 3000]:
    d_test = float(mp_log(T_test / (2*mp_pi)) / (2*mp_pi))
    berry_sat = (1.0/np.pi**2) * np.log(np.log(T_test/(2*np.pi)))

    # Recompute corrections for this T
    # Scale the corrections by (d_bar/d_test)^2 since prefactor ~ 1/d^2
    # Actually, need to recompute xi = x/d_test too
    # For a quick estimate, recompute at just L=20
    print(f"\n  T = {T_test}, d_bar = {d_test:.4f}, Berry = {berry_sat:.6f}")

    # Quick recompute with new d_bar
    def R1c_T(x, d_val=d_test):
        if abs(x) < 1e-12: return 0.0
        xi = x / d_val
        prefactor = 1.0 / (2.0 * (np.pi * d_val)**2)

        term1 = 1.0 / xi**2
        h = max(abs(xi) * 1e-4, 1e-5)
        def lzr(xi_val):
            z = complex(mp_zeta(mpf(1) - mpf(xi_val) * mpf(1j)))
            return np.log(abs(z)) if abs(z) > 1e-300 else 0.0
        try:
            d2 = (lzr(xi+h) + lzr(xi-h) - 2*lzr(xi)) / h**2
        except:
            d2 = 0.0

        term3 = 0.0
        for p in primes[:100]:
            logp = np.log(p)
            denom = p * np.exp(1j * xi * logp) - 1.0
            if abs(denom) > 1e-15:
                term3 -= (logp**2 / denom**2).real

        return prefactor * (term1 - d2 + term3)

    def R2c_T(x, d_val=d_test):
        if abs(x) < 1e-12: return 0.0
        xi = x / d_val
        prefactor = 1.0 / (2.0 * (np.pi * d_val)**2)
        term1 = -np.cos(2 * np.pi * x) / xi**2
        try:
            z = complex(mp_zeta(mpf(1) + mpf(xi) * mpf(1j)))
            zeta_abs_sq = abs(z)**2
        except:
            zeta_abs_sq = 1.0 / xi**2
        b_val = 1.0 + 0j
        for p in primes[:100]:
            b_val *= (1.0 - (p**(1j * xi) - 1.0)**2 / (p - 1.0)**2)
        term2 = zeta_abs_sq * (np.exp(2j * np.pi * x) * b_val).real
        return prefactor * (term1 + term2)

    # Compute on sparse grid for this T
    x_sp = np.concatenate([np.linspace(0.1, 2, 30), np.linspace(2, 10, 30), np.linspace(10, 25, 20)])
    x_sp = np.unique(x_sp)
    R1c_sp = np.array([R1c_T(x) for x in x_sp])
    R2c_sp = np.array([R2c_T(x) for x in x_sp])

    def R2_full_T(x):
        r1 = np.interp(x, x_sp, R1c_sp) if x_sp[0] <= x <= x_sp[-1] else 0.0
        r2 = np.interp(x, x_sp, R2c_sp) if x_sp[0] <= x <= x_sp[-1] else 0.0
        return R_GUE(x) + r1 + r2

    def s2_T(r):
        return sigma2(r, R2_full_T, n_points=1500)

    d3_T = delta3(20.0, s2_T, n_points=150)
    d3_T_gue = delta3(20.0, s2_gue, n_points=150)

    print(f"    Delta_3(20) GUE:  {d3_T_gue:.6f}")
    print(f"    Delta_3(20) Full: {d3_T:.6f}")
    print(f"    Direction: {'toward 0.155' if d3_T < d3_T_gue else 'AWAY from 0.155'}")

print("\n" + "="*70)
print("DONE")
print("="*70)
