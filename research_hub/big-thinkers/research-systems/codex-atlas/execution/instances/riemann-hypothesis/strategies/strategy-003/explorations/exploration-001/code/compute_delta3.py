"""
Off-diagonal form factor and predicted Delta_3 for Riemann zeta zeros.

Based on Berry-Keating (1999) SIAM Rev. 41:236-266, equations:
- (4.4): Sigma_2(x) = (2/pi^2) int_0^inf K(tau)/tau^2 sin^2(pi*x*tau) dtau
- (4.10): K_GUE(tau) = |tau| Theta(1-|tau|) + Theta(|tau|-1)
- (4.18): K(tau) with short orbit corrections
- (4.23): R1_c diagonal pair correlation correction
- (4.27)-(4.28): R2_c off-diagonal pair correlation correction

Delta_3 formula:
  Delta_3(L) = L/15 - (1/L^4) int_0^L (L-s)^3 (2L^2+sL-s^2) [R2(s)-1] ds
"""

import numpy as np
from mpmath import mp, mpf, zeta, log, pi, gamma as euler_gamma, exp, cos, sin, re, im, fabs, quad, inf
from sympy import primerange
import warnings
warnings.filterwarnings('ignore')

mp.dps = 30  # 30 decimal places

# =============================================================================
# Parameters
# =============================================================================
T = 1682.0  # Height of ~1000th zero
d_bar = float(log(T / (2 * pi)) / (2 * pi))  # Mean density at height T
print(f"T = {T}")
print(f"d_bar = {d_bar:.6f}")
print(f"T_H = 2*pi*d_bar = {2*np.pi*d_bar:.6f}")
print(f"log(T/(2pi)) = {float(log(T/(2*pi))):.6f}")

# Primes up to a reasonable limit
primes = list(primerange(2, 10000))
print(f"Number of primes loaded: {len(primes)}")

# =============================================================================
# Section 1: GUE pair correlation and form factor
# =============================================================================
print("\n" + "="*70)
print("Section 1: GUE Baseline")
print("="*70)

def R_GUE(x):
    """GUE pair correlation function. R_GUE(x) = 1 - (sin(pi*x)/(pi*x))^2"""
    if abs(x) < 1e-15:
        return 0.0  # delta function contribution excluded; R(0)=0
    return 1.0 - (np.sin(np.pi * x) / (np.pi * x))**2

def K_GUE(tau):
    """GUE form factor. K(tau) = |tau| for |tau|<1, 1 for |tau|>=1"""
    tau = abs(tau)
    if tau < 1.0:
        return tau
    else:
        return 1.0

# Delta_3 from pair correlation:
# Delta_3(L) = L/15 - (1/L^4) int_0^L (L-s)^3 (2L^2+sL-s^2) [R2(s)-1] ds
def compute_delta3_from_R2(L, R2_func, n_quad=2000, upper_limit=None):
    """Compute Delta_3(L) from the pair correlation function R2.

    Uses: Delta_3(L) = L/15 - (1/L^4) int_0^L (L-s)^3 (2L^2+sL-s^2) (R2(s)-1) ds
    """
    if upper_limit is None:
        upper_limit = L

    # Integration grid
    s_vals = np.linspace(1e-10, upper_limit, n_quad)
    ds = s_vals[1] - s_vals[0]

    # Kernel function
    kernel = (L - s_vals)**3 * (2*L**2 + s_vals*L - s_vals**2)

    # R2(s) - 1 values
    R2_minus_1 = np.array([R2_func(s) - 1.0 for s in s_vals])

    # Integral using trapezoidal rule
    integrand = kernel * R2_minus_1
    integral = np.trapezoid(integrand, s_vals)

    delta3 = L/15.0 - integral / L**4
    return delta3

# Test with GUE
print("\nGUE Delta_3 values:")
L_values = [1, 2, 5, 10, 15, 20, 25, 30, 40, 50]
delta3_GUE = []
for L in L_values:
    d3 = compute_delta3_from_R2(L, R_GUE, n_quad=5000)
    delta3_GUE.append(d3)
    # Compare with analytical GUE formula
    # Delta_3_GUE(L) = (1/pi^2)[log(L) + gamma_E - 5/4 - pi^2/8 + ...]
    # More precisely: (1/pi^2)[log(2*pi*L) - 1 - gamma_E + pi^2/8] ... various forms
    print(f"  L={L:3d}: Delta_3 = {d3:.6f}")

# Analytical GUE for large L: (1/pi^2)(log(L) - 0.0687...)
# Let me compute more precisely
print(f"\n  GUE analytical (1/pi^2)(log(L)): ", end="")
for L in [10, 20, 30, 50]:
    val = (1/np.pi**2) * np.log(L)
    print(f"L={L}:{val:.4f} ", end="")
print()

# =============================================================================
# Section 2: Diagonal pair correlation correction R1_c (eq 4.23)
# =============================================================================
print("\n" + "="*70)
print("Section 2: Diagonal Correction R1_c")
print("="*70)

def R1_c(x, d_bar_val, T_val, n_primes=500):
    """Diagonal pair correlation correction.

    R1_c(x) = 1/(2*(pi*d_bar)^2) * [1/xi^2 - d^2/dxi^2 Re log zeta(1-i*xi)
               - Re sum_p log^2(p)/(p*exp(i*xi*log(p))-1)^2]

    where xi = x/d_bar
    """
    if abs(x) < 1e-12:
        return 0.0

    xi = x / d_bar_val
    prefactor = 1.0 / (2.0 * (np.pi * d_bar_val)**2)

    # Term 1: 1/xi^2
    term1 = 1.0 / xi**2

    # Term 2: -d^2/dxi^2 Re log zeta(1-i*xi)
    # Use numerical second derivative
    h = 1e-5
    xi_mp = mpf(xi)
    h_mp = mpf(h)

    def log_zeta_re(xi_val):
        s = 1 - 1j * float(xi_val)
        try:
            z = complex(zeta(mpf(s.real) + mpf(s.imag) * 1j))
            return np.log(abs(z))  # Re(log(zeta)) = log|zeta|
        except:
            return 0.0

    # Wait - Re log zeta(1-i*xi) = Re[log(zeta(1-i*xi))]
    # For xi near 0, zeta(1-i*xi) has a pole, so log has a singularity
    # But the 1/xi^2 term cancels this
    # Let me compute the COMBINATION (1/xi^2 - d^2/dxi^2 Re log zeta(1-i*xi))
    # which should be finite

    # Actually, near xi=0: zeta(1-i*xi) ~ 1/(−i*xi) = i/xi, so log zeta ~ log(i/xi) = i*pi/2 - log(xi)
    # Re log zeta ~ -log|xi|, d/dxi Re log zeta ~ -1/xi, d^2/dxi^2 ~ 1/xi^2
    # So 1/xi^2 - d^2/dxi^2 Re log zeta = 1/xi^2 - 1/xi^2 + O(1) → finite

    # Compute log zeta at three points for second derivative
    def log_zeta_complex(xi_val):
        """Compute log(zeta(1 - i*xi)) as complex number"""
        s_real = mpf(1)
        s_imag = mpf(-xi_val)
        z = zeta(s_real + s_imag * mpf(1j))
        return complex(z)

    try:
        z0 = log_zeta_complex(xi)
        z_plus = log_zeta_complex(xi + h)
        z_minus = log_zeta_complex(xi - h)

        log_z0 = np.log(z0)  # complex log
        log_zp = np.log(z_plus)
        log_zm = np.log(z_minus)

        # Second derivative of Re part
        d2_re_log_zeta = (log_zp.real + log_zm.real - 2*log_z0.real) / h**2
    except:
        d2_re_log_zeta = 0.0

    # Term 3: -Re sum_p log^2(p) / (p*exp(i*xi*log(p))-1)^2
    term3 = 0.0
    for p in primes[:n_primes]:
        logp = np.log(p)
        phase = 1j * xi * logp
        denom = p * np.exp(phase) - 1.0
        if abs(denom) > 1e-15:
            term3 -= (logp**2 / denom**2).real

    result = prefactor * (term1 - d2_re_log_zeta - term3)
    return result

# Test R1_c at a few points
print("\nTesting R1_c at select x values:")
for x_test in [0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0]:
    val = R1_c(x_test, d_bar, T)
    print(f"  x={x_test:5.1f}: R1_c = {val:+.8f}")

# =============================================================================
# Section 3: Off-diagonal correction R2_c (eqs 4.27-4.28)
# =============================================================================
print("\n" + "="*70)
print("Section 3: Off-Diagonal Correction R2_c")
print("="*70)

def compute_b(xi, n_primes=200):
    """Compute b(xi) = prod_p (1 - (p^{i*xi} - 1)^2 / (p-1)^2)

    This is the convergent product over primes from eq (4.28).
    """
    b_val = 1.0 + 0j
    for p in primes[:n_primes]:
        p_ixi = p**(1j * xi)  # p^{i*xi}
        num = (p_ixi - 1.0)**2
        den = (p - 1.0)**2
        factor = 1.0 - num / den
        b_val *= factor
    return b_val

def R2_c(x, d_bar_val, T_val, n_primes=200):
    """Off-diagonal pair correlation correction.

    R2_c(x) = 1/(2*(pi*d_bar)^2) * [-cos(2*pi*x)/xi^2
               + |zeta(1+i*xi)|^2 * Re{exp(2*pi*i*x) * b(xi)}]

    where xi = x/d_bar
    """
    if abs(x) < 1e-12:
        return 0.0

    xi = x / d_bar_val
    prefactor = 1.0 / (2.0 * (np.pi * d_bar_val)**2)

    # Term 1: -cos(2*pi*x)/xi^2
    term1 = -np.cos(2 * np.pi * x) / xi**2

    # Term 2: |zeta(1+i*xi)|^2 * Re{exp(2*pi*i*x) * b(xi)}
    try:
        z = complex(zeta(mpf(1) + mpf(xi) * mpf(1j)))
        zeta_abs_sq = abs(z)**2
    except:
        zeta_abs_sq = 1.0 / xi**2  # leading approximation near pole

    b_val = compute_b(xi, n_primes)
    exp_2pix = np.exp(2j * np.pi * x)

    term2 = zeta_abs_sq * (exp_2pix * b_val).real

    result = prefactor * (term1 + term2)
    return result

# Test R2_c
print("\nTesting R2_c at select x values:")
for x_test in [0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0]:
    val = R2_c(x_test, d_bar, T)
    print(f"  x={x_test:5.1f}: R2_c = {val:+.8f}")

# =============================================================================
# Section 4: Full R2 and Delta_3 computation
# =============================================================================
print("\n" + "="*70)
print("Section 4: Full R2 and Delta_3")
print("="*70)

def R2_full(x, d_bar_val, T_val, include_diag=True, include_offdiag=True):
    """Full pair correlation for Riemann zeros.
    R2(x) = R_GUE(x) + R1_c(x) + R2_c(x)
    """
    r = R_GUE(x)
    if include_diag:
        r += R1_c(x, d_bar_val, T_val)
    if include_offdiag:
        r += R2_c(x, d_bar_val, T_val)
    return r

# Compute Delta_3 for several scenarios
print("\nComputing Delta_3 for L=20 (saturation regime):")
print("(This may take a few minutes...)\n")

L_test = 20.0
n_quad = 3000

# Scenario 1: GUE only
d3_GUE = compute_delta3_from_R2(L_test, R_GUE, n_quad=n_quad)
print(f"  GUE only:              Delta_3({L_test:.0f}) = {d3_GUE:.6f}")

# Scenario 2: GUE + diagonal correction R1_c
d3_diag = compute_delta3_from_R2(L_test,
    lambda s: R2_full(s, d_bar, T, include_diag=True, include_offdiag=False),
    n_quad=n_quad)
print(f"  GUE + R1_c (diag):     Delta_3({L_test:.0f}) = {d3_diag:.6f}")

# Scenario 3: GUE + off-diagonal correction R2_c only
d3_offdiag = compute_delta3_from_R2(L_test,
    lambda s: R2_full(s, d_bar, T, include_diag=False, include_offdiag=True),
    n_quad=n_quad)
print(f"  GUE + R2_c (off-diag): Delta_3({L_test:.0f}) = {d3_offdiag:.6f}")

# Scenario 4: Full (GUE + R1_c + R2_c)
d3_full = compute_delta3_from_R2(L_test,
    lambda s: R2_full(s, d_bar, T, include_diag=True, include_offdiag=True),
    n_quad=n_quad)
print(f"  Full (GUE + R1_c + R2_c): Delta_3({L_test:.0f}) = {d3_full:.6f}")

# Target
target = 0.155
print(f"\n  Target (zeta zeros):   Delta_3_sat = {target}")
print(f"\n  Percentage errors:")
print(f"    GUE only:     |{d3_GUE:.6f} - {target}| / {target} = {abs(d3_GUE - target)/target*100:.1f}%")
print(f"    With R1_c:    |{d3_diag:.6f} - {target}| / {target} = {abs(d3_diag - target)/target*100:.1f}%")
print(f"    With R2_c:    |{d3_offdiag:.6f} - {target}| / {target} = {abs(d3_offdiag - target)/target*100:.1f}%")
print(f"    Full:         |{d3_full:.6f} - {target}| / {target} = {abs(d3_full - target)/target*100:.1f}%")

# Gap fraction closed
if d3_GUE > target:
    gap_GUE = d3_GUE - target
    print(f"\n  Gap analysis:")
    print(f"    GUE gap:      {d3_GUE:.6f} - {target} = {gap_GUE:.6f}")
    if d3_diag < d3_GUE:
        print(f"    R1_c reduces: {d3_GUE:.6f} -> {d3_diag:.6f} (closes {(d3_GUE-d3_diag)/gap_GUE*100:.1f}% of gap)")
    if d3_full < d3_GUE:
        print(f"    Full reduces: {d3_GUE:.6f} -> {d3_full:.6f} (closes {(d3_GUE-d3_full)/gap_GUE*100:.1f}% of gap)")

# =============================================================================
# Section 5: Scan over L values
# =============================================================================
print("\n" + "="*70)
print("Section 5: Delta_3 vs L scan")
print("="*70)

L_scan = [1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50]
results = {'L': [], 'GUE': [], 'diag': [], 'full': []}

print(f"\n{'L':>5s} {'GUE':>10s} {'GUE+R1c':>10s} {'Full':>10s} {'Berry_pred':>10s}")
print("-" * 50)

for L in L_scan:
    d3_g = compute_delta3_from_R2(L, R_GUE, n_quad=max(2000, 100*L))
    d3_d = compute_delta3_from_R2(L,
        lambda s: R2_full(s, d_bar, T, include_diag=True, include_offdiag=False),
        n_quad=max(2000, 100*L))
    d3_f = compute_delta3_from_R2(L,
        lambda s: R2_full(s, d_bar, T, include_diag=True, include_offdiag=True),
        n_quad=max(2000, 100*L))

    # Berry prediction: (1/pi^2) log(log(T/(2pi)))
    berry_pred = (1/np.pi**2) * np.log(np.log(T/(2*np.pi)))

    results['L'].append(L)
    results['GUE'].append(d3_g)
    results['diag'].append(d3_d)
    results['full'].append(d3_f)

    print(f"{L:5d} {d3_g:10.6f} {d3_d:10.6f} {d3_f:10.6f} {berry_pred:10.6f}")

# Save results
np.savez('code/delta3_results.npz',
         L_scan=np.array(results['L']),
         delta3_GUE=np.array(results['GUE']),
         delta3_diag=np.array(results['diag']),
         delta3_full=np.array(results['full']),
         T=T, d_bar=d_bar)
print("\nResults saved to code/delta3_results.npz")

# =============================================================================
# Section 6: Berry's saturation formula
# =============================================================================
print("\n" + "="*70)
print("Section 6: Berry's Saturation Formula")
print("="*70)

for T_test in [600, 1000, 1682, 3000, 5000, 10000]:
    d_test = float(log(T_test / (2*pi)) / (2*pi))
    berry_sat = (1/np.pi**2) * np.log(np.log(T_test / (2*np.pi)))
    print(f"  T = {T_test:6.0f}: d_bar = {d_test:.4f}, Berry Delta_3_sat = {berry_sat:.6f}")

print("\n" + "="*70)
print("DONE")
print("="*70)
