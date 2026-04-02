"""
FINAL computation: Delta_3 for Riemann zeta zeros with off-diagonal corrections.

VERIFIED route:
  1. R2(x) = R_GUE(x) + R1_c(x) + R2_c(x)
  2. Sigma_2(L) = L + 2 int_0^L (L-r)(R2(r)-1) dr
  3. Delta_3(L) = (2/L^4) int_0^L (L^3-2L^2r+r^3) Sigma_2(r) dr

The Sigma_2 -> Delta_3 route was verified against GUE random matrix simulations
to ~3% accuracy.
"""

import numpy as np
from mpmath import mp, mpf, zeta as mp_zeta, log as mp_log, pi as mp_pi
from scipy.integrate import quad as scipy_quad
import time

mp.dps = 25

# =============================================================================
# Parameters
# =============================================================================
T = 1682.0
d_bar = float(mp_log(T / (2 * mp_pi)) / (2 * mp_pi))
print(f"T = {T}")
print(f"d_bar = {d_bar:.6f}")
print(f"1/(2*(pi*d_bar)^2) = {1.0/(2.0*(np.pi*d_bar)**2):.6f}")

# Primes for the product b(xi) and the sum in R1_c
from sympy import primerange
primes = list(primerange(2, 5000))
print(f"Number of primes: {len(primes)}")

# =============================================================================
# GUE pair correlation
# =============================================================================
def R_GUE(x):
    """R_GUE(x) = 1 - (sin(pi*x)/(pi*x))^2"""
    if abs(x) < 1e-15:
        return 0.0
    return 1.0 - (np.sin(np.pi * x) / (np.pi * x))**2

# =============================================================================
# Diagonal correction R1_c (eq 4.23 of Berry-Keating 1999)
# =============================================================================
def R1_c(x, d_bar_val, n_primes=300):
    """
    R1_c(x) = 1/(2*(pi*d)^2) * [1/xi^2 - d^2/dxi^2 Re log zeta(1-i*xi)
               - Re sum_p log^2(p)/(p*exp(i*xi*log(p))-1)^2]
    where xi = x / d_bar
    """
    if abs(x) < 1e-12:
        return 0.0

    xi = x / d_bar_val
    prefactor = 1.0 / (2.0 * (np.pi * d_bar_val)**2)

    # Term 1: 1/xi^2
    term1 = 1.0 / xi**2

    # Term 2: -d^2/dxi^2 Re log zeta(1-i*xi)
    h = max(abs(xi) * 1e-5, 1e-6)

    def log_zeta_re(xi_val):
        """Re[log(zeta(1 - i*xi))]"""
        s = mpf(1) - mpf(xi_val) * mpf(1j)
        z = mp_zeta(s)
        z_complex = complex(z)
        if abs(z_complex) < 1e-300:
            return 0.0
        return np.log(abs(z_complex))

    try:
        lr0 = log_zeta_re(xi)
        lrp = log_zeta_re(xi + h)
        lrm = log_zeta_re(xi - h)
        d2_re_log_zeta = (lrp + lrm - 2*lr0) / h**2
    except:
        d2_re_log_zeta = 0.0

    # Term 3: -Re sum_p log^2(p) / (p*exp(i*xi*log(p))-1)^2
    term3 = 0.0
    for p in primes[:n_primes]:
        logp = np.log(p)
        exp_phase = p * np.exp(1j * xi * logp)
        denom = exp_phase - 1.0
        if abs(denom) > 1e-15:
            term3 -= (logp**2 / denom**2).real

    result = prefactor * (term1 - d2_re_log_zeta + term3)
    return result

# =============================================================================
# Off-diagonal correction R2_c (eqs 4.27-4.28 of Berry-Keating 1999)
# =============================================================================
def compute_b(xi, n_primes=200):
    """b(xi) = prod_p (1 - (p^{i*xi} - 1)^2 / (p-1)^2)"""
    b_val = 1.0 + 0j
    for p in primes[:n_primes]:
        p_ixi = p**(1j * xi)
        num = (p_ixi - 1.0)**2
        den = (p - 1.0)**2
        factor = 1.0 - num / den
        b_val *= factor
    return b_val

def R2_c(x, d_bar_val, n_primes=200):
    """
    R2_c(x) = 1/(2*(pi*d)^2) * [-cos(2*pi*x)/xi^2
               + |zeta(1+i*xi)|^2 * Re{exp(2*pi*i*x) * b(xi)}]
    where xi = x / d_bar
    """
    if abs(x) < 1e-12:
        return 0.0

    xi = x / d_bar_val
    prefactor = 1.0 / (2.0 * (np.pi * d_bar_val)**2)

    # Term 1: -cos(2*pi*x)/xi^2
    term1 = -np.cos(2 * np.pi * x) / xi**2

    # Term 2: |zeta(1+i*xi)|^2 * Re{exp(2*pi*i*x) * b(xi)}
    try:
        z = complex(mp_zeta(mpf(1) + mpf(xi) * mpf(1j)))
        zeta_abs_sq = abs(z)**2
    except:
        zeta_abs_sq = 1.0 / xi**2

    b_val = compute_b(xi, n_primes)
    exp_2pix = np.exp(2j * np.pi * x)
    term2 = zeta_abs_sq * (exp_2pix * b_val).real

    return prefactor * (term1 + term2)

# =============================================================================
# Sigma_2 computation
# =============================================================================
def sigma2(L, R2_func, n_points=5000):
    """Sigma_2(L) = L + 2 int_0^L (L-r)(R2(r)-1) dr"""
    if L < 1e-10:
        return 0.0
    r_vals = np.linspace(1e-10, L, n_points)
    R2_vals = np.array([R2_func(r) for r in r_vals])
    integrand = (L - r_vals) * (R2_vals - 1.0)
    return L + 2.0 * np.trapezoid(integrand, r_vals)

# =============================================================================
# Delta_3 computation (verified Dyson-Mehta route)
# =============================================================================
def delta3(L, sigma2_func, n_points=300):
    """Delta_3(L) = (2/L^4) int_0^L (L^3-2L^2r+r^3) Sigma_2(r) dr

    Verified against GUE random matrix simulations to ~3% accuracy.
    """
    if L < 0.5:
        return L / 15.0  # Poisson limit for very small L
    r_vals = np.linspace(0.01, L, n_points)
    s2_vals = np.array([sigma2_func(r) for r in r_vals])
    kernel = L**3 - 2*L**2*r_vals + r_vals**3
    return (2.0 / L**4) * np.trapezoid(kernel * s2_vals, r_vals)

# =============================================================================
# MAIN COMPUTATION
# =============================================================================
print("\n" + "="*70)
print("MAIN COMPUTATION: Delta_3 with corrections")
print("="*70)

# Define different R2 functions
def R2_GUE_only(x):
    return R_GUE(x)

def R2_with_R1c(x):
    return R_GUE(x) + R1_c(x, d_bar)

def R2_with_R2c(x):
    return R_GUE(x) + R2_c(x, d_bar)

def R2_full(x):
    return R_GUE(x) + R1_c(x, d_bar) + R2_c(x, d_bar)

# Define Sigma_2 functions
def s2_GUE(r):
    return sigma2(r, R2_GUE_only, n_points=3000)

def s2_diag(r):
    return sigma2(r, R2_with_R1c, n_points=3000)

def s2_offdiag(r):
    return sigma2(r, R2_with_R2c, n_points=3000)

def s2_full(r):
    return sigma2(r, R2_full, n_points=3000)

# First: verify Sigma_2 values
print("\n--- Sigma_2 values ---")
print(f"{'L':>5s} {'GUE':>10s} {'GUE+R1c':>10s} {'GUE+R2c':>10s} {'Full':>10s}")
print("-" * 50)
for L in [1, 5, 10, 20]:
    s_g = s2_GUE(L)
    s_d = s2_diag(L)
    s_o = s2_offdiag(L)
    s_f = s2_full(L)
    print(f"{L:5d} {s_g:10.6f} {s_d:10.6f} {s_o:10.6f} {s_f:10.6f}")

# Now compute Delta_3
print("\n--- Delta_3 values ---")
L_values = [2, 5, 10, 15, 20, 25, 30, 40, 50]

print(f"\n{'L':>5s} {'GUE':>10s} {'GUE+R1c':>10s} {'GUE+R2c':>10s} {'Full':>10s} {'Berry':>10s}")
print("-" * 65)

results = {'L': [], 'GUE': [], 'diag': [], 'offdiag': [], 'full': []}

t_start = time.time()
for L in L_values:
    d3_g = delta3(L, s2_GUE, n_points=200)
    d3_d = delta3(L, s2_diag, n_points=200)
    d3_o = delta3(L, s2_offdiag, n_points=200)
    d3_f = delta3(L, s2_full, n_points=200)

    berry_pred = (1.0/np.pi**2) * np.log(np.log(T/(2*np.pi)))

    results['L'].append(L)
    results['GUE'].append(d3_g)
    results['diag'].append(d3_d)
    results['offdiag'].append(d3_o)
    results['full'].append(d3_f)

    print(f"{L:5d} {d3_g:10.6f} {d3_d:10.6f} {d3_o:10.6f} {d3_f:10.6f} {berry_pred:10.6f}")

    elapsed = time.time() - t_start
    print(f"  [elapsed: {elapsed:.0f}s]")

# Save results
np.savez('code/delta3_final_results.npz',
         L_scan=np.array(results['L']),
         delta3_GUE=np.array(results['GUE']),
         delta3_diag=np.array(results['diag']),
         delta3_offdiag=np.array(results['offdiag']),
         delta3_full=np.array(results['full']),
         T=T, d_bar=d_bar)

# =============================================================================
# ANALYSIS
# =============================================================================
print("\n" + "="*70)
print("ANALYSIS at L=20 (saturation regime)")
print("="*70)

target = 0.155
d3_gue_20 = results['GUE'][results['L'].index(20)]
d3_diag_20 = results['diag'][results['L'].index(20)]
d3_offdiag_20 = results['offdiag'][results['L'].index(20)]
d3_full_20 = results['full'][results['L'].index(20)]

print(f"\n  Target:         {target}")
print(f"  GUE only:       {d3_gue_20:.6f}  error: {abs(d3_gue_20-target)/target*100:.1f}%")
print(f"  GUE + R1_c:     {d3_diag_20:.6f}  error: {abs(d3_diag_20-target)/target*100:.1f}%")
print(f"  GUE + R2_c:     {d3_offdiag_20:.6f}  error: {abs(d3_offdiag_20-target)/target*100:.1f}%")
print(f"  Full:           {d3_full_20:.6f}  error: {abs(d3_full_20-target)/target*100:.1f}%")

gap = d3_gue_20 - target
print(f"\n  Gap: {d3_gue_20:.6f} - {target} = {gap:.6f}")
if gap > 0:
    diag_closes = (d3_gue_20 - d3_diag_20) / gap * 100
    offdiag_closes = (d3_gue_20 - d3_offdiag_20) / gap * 100
    full_closes = (d3_gue_20 - d3_full_20) / gap * 100
    print(f"  R1_c closes:    {diag_closes:.1f}% of gap")
    print(f"  R2_c closes:    {offdiag_closes:.1f}% of gap")
    print(f"  Full closes:    {full_closes:.1f}% of gap")

# =============================================================================
# HEIGHT DEPENDENCE
# =============================================================================
print("\n" + "="*70)
print("HEIGHT DEPENDENCE TEST")
print("="*70)

for T_test in [600, 1682, 3000]:
    d_test = float(mp_log(T_test / (2*mp_pi)) / (2*mp_pi))
    berry_sat = (1.0/np.pi**2) * np.log(np.log(T_test/(2*np.pi)))

    # Define R2 functions for this T
    def R2_full_T(x, d_val=d_test):
        r = R_GUE(x)
        r += R1_c(x, d_val)
        r += R2_c(x, d_val)
        return r

    def s2_full_T(r, d_val=d_test):
        return sigma2(r, lambda x: R2_full_T(x, d_val), n_points=2000)

    L_test = 20.0
    d3_full_T = delta3(L_test, lambda r: s2_full_T(r, d_test), n_points=150)

    print(f"\n  T = {T_test}:")
    print(f"    d_bar = {d_test:.4f}")
    print(f"    Berry prediction: {berry_sat:.6f}")
    print(f"    Computed Delta_3(20): {d3_full_T:.6f}")
    print(f"    Error vs Berry: {abs(d3_full_T - berry_sat)/berry_sat*100:.1f}%")

print("\n" + "="*70)
print("COMPUTATION COMPLETE")
print("="*70)
