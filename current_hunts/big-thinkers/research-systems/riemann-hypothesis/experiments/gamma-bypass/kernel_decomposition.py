"""
Investigation 1 & 5: Kernel decomposition and numerical comparison.

We decompose Xi(1/2+it) = G(1/2+it) * zeta(1/2+it) and compute:
(a) The full Xi kernel (Polya kernel Phi)
(b) The gamma factor kernel Phi_G
(c) The "zeta kernel" Phi_zeta
(d) The Hardy Z-function kernel
(e) Alternative completions

Then test PF properties of each.
"""

import mpmath
import numpy as np
import json

mpmath.mp.dps = 50

###############################################################################
# 1. The building blocks on the critical line
###############################################################################

def xi_on_line(t):
    """Xi(1/2+it) -- real-valued on the critical line."""
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    val = mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
    return float(mpmath.re(val))

def gamma_factor_on_line(t):
    """G(1/2+it) = (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2), s = 1/2+it."""
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    val = mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2)
    return complex(val)

def zeta_on_line(t):
    """zeta(1/2+it) -- complex-valued."""
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    return complex(mpmath.zeta(s))

def stripped_gamma_on_line(t):
    """G_stripped(1/2+it) = pi^{-s/2}*Gamma(s/2), without s(s-1)/2 factor."""
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    val = mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2)
    return complex(val)

def hardy_Z(t):
    """
    Hardy's Z-function: Z(t) = e^{i*theta(t)} * zeta(1/2+it)
    where theta(t) = arg(pi^{-it/2} * Gamma(1/4+it/2)) (Riemann-Siegel theta).
    Z(t) is REAL for real t.
    """
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    # theta = Im(log(pi^{-it/2} * Gamma(1/4+it/2)))
    # = -t/2 * log(pi) + Im(log(Gamma(1/4+it/2)))
    theta = mpmath.im(mpmath.loggamma(mpmath.mpc('0.25', t/2))) - t/2 * mpmath.log(mpmath.pi)
    z_val = mpmath.exp(mpmath.mpc(0, theta)) * mpmath.zeta(s)
    return float(mpmath.re(z_val))

def s_factor_on_line(t):
    """The s(s-1)/2 factor on the critical line: (1/2)*(1/2+it)*(-1/2+it) = -(1/4+t^2)/2."""
    t = mpmath.mpf(t)
    return float(-(mpmath.mpf('0.25') + t**2) / 2)

###############################################################################
# 2. Compute the kernels via Fourier cosine transform
###############################################################################

print("Computing function values on the critical line...")
t_max = 60.0
N_pts = 4001
t_grid = np.linspace(0, t_max, N_pts)
dt = t_grid[1] - t_grid[0]

# Compute all functions
xi_vals = np.array([xi_on_line(t) for t in t_grid])
print("  Xi computed.")

G_complex = np.array([gamma_factor_on_line(t) for t in t_grid])
G_real = np.real(G_complex)
G_imag = np.imag(G_complex)
print("  Gamma factor computed.")

zeta_complex = np.array([zeta_on_line(t) for t in t_grid])
zeta_real = np.real(zeta_complex)
zeta_imag = np.imag(zeta_complex)
print("  Zeta computed.")

Z_vals = np.array([hardy_Z(t) for t in t_grid])
print("  Hardy Z computed.")

s_factor_vals = np.array([s_factor_on_line(t) for t in t_grid])
print("  s(s-1)/2 factor computed.")

stripped_G_complex = np.array([stripped_gamma_on_line(t) for t in t_grid])
stripped_G_real = np.real(stripped_G_complex)
stripped_G_imag = np.imag(stripped_G_complex)
print("  Stripped gamma (no s(s-1)) computed.")

###############################################################################
# 3. Kernel computation via Fourier cosine transform
###############################################################################

def kernel_from_real_func(f_vals, u):
    """Compute kernel K(u) = 2 * int_0^inf f(t) cos(ut) dt."""
    integrand = f_vals * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

def kernel_from_complex_func_modulus(f_complex, u):
    """Kernel of |f(t)|."""
    integrand = np.abs(f_complex) * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

def kernel_from_complex_func_real(f_complex, u):
    """Kernel of Re(f(t))."""
    integrand = np.real(f_complex) * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

# High-precision kernel using mpmath quadrature
def phi_hp(u):
    """Phi(u) via mpmath quadrature of Xi."""
    u_mp = mpmath.mpf(u)
    def integrand(t):
        t = mpmath.mpf(t)
        s = mpmath.mpc('0.5', t)
        xi = mpmath.mpf('0.5') * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
        return mpmath.re(xi) * mpmath.cos(u_mp * t)
    val = mpmath.quad(integrand, [0, 20, 40, 60], maxdegree=8)
    return float(2 * val)

print("\n=== Computing kernels at key u values ===\n")

u_vals = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

kernel_data = {}
print(f"{'u':>6s}  {'Phi_Xi(hp)':>14s}  {'Phi_Xi(trap)':>14s}  {'Phi_G(Re)':>14s}  {'Phi_zeta(Re)':>14s}  {'Phi_Z':>14s}  {'s_factor_K':>14s}  {'stripped_G_K':>14s}")
print("-" * 120)

for u in u_vals:
    phi_xi_hp = phi_hp(u) if u <= 0.5 else phi_hp(u)
    phi_xi_trap = kernel_from_real_func(xi_vals, u)
    phi_G = kernel_from_complex_func_real(G_complex, u)
    phi_zeta = kernel_from_complex_func_real(zeta_complex, u)
    phi_Z = kernel_from_real_func(Z_vals, u)
    phi_sfactor = kernel_from_real_func(s_factor_vals, u)
    phi_stripped = kernel_from_complex_func_real(stripped_G_complex, u)

    print(f"{u:6.2f}  {phi_xi_hp:14.6e}  {phi_xi_trap:14.6e}  {phi_G:14.6e}  {phi_zeta:14.6e}  {phi_Z:14.6e}  {phi_sfactor:14.6e}  {phi_stripped:14.6e}")

    kernel_data[str(u)] = {
        'phi_xi_hp': phi_xi_hp,
        'phi_xi_trap': phi_xi_trap,
        'phi_G_real': phi_G,
        'phi_zeta_real': phi_zeta,
        'phi_Z': phi_Z,
        'phi_s_factor': phi_sfactor,
        'phi_stripped_G': phi_stripped,
    }

###############################################################################
# 4. PF tests for each kernel
###############################################################################

print("\n\n=== PF Tests for Each Kernel ===\n")

def toeplitz_det_from_values(kernel_func, h, order):
    """Compute the Toeplitz determinant of order 'order' at spacing h.
    Uses evenly-spaced points: kernel evaluated at 0, h, 2h, ..., (order-1)*h."""
    vals = [kernel_func(k*h) for k in range(order)]
    mat = np.zeros((order, order))
    for i in range(order):
        for j in range(order):
            mat[i][j] = vals[abs(i-j)]
    return np.linalg.det(mat)

def toeplitz_det_shifted(kernel_func, u0, h, order):
    """Toeplitz determinant shifted to center at u0."""
    vals = [kernel_func(u0 + k*h) for k in range(-(order-1), order)]
    # Index mapping: val[k + (order-1)] = kernel(u0 + k*h)
    mat = np.zeros((order, order))
    for i in range(order):
        for j in range(order):
            mat[i][j] = vals[(i - j) + (order - 1)]
    return np.linalg.det(mat)

# Test each kernel's PF order
kernels_to_test = {
    'Xi (hp)': phi_hp,
    'Hardy Z': lambda u: kernel_from_real_func(Z_vals, u),
    'Gamma Re': lambda u: kernel_from_complex_func_real(G_complex, u),
    'Zeta Re': lambda u: kernel_from_complex_func_real(zeta_complex, u),
    's(s-1)/2': lambda u: kernel_from_real_func(s_factor_vals, u),
    'Stripped G': lambda u: kernel_from_complex_func_real(stripped_G_complex, u),
}

h_test_values = [0.05, 0.08, 0.1, 0.12, 0.15]

for name, kfunc in kernels_to_test.items():
    print(f"\n--- Kernel: {name} ---")
    print(f"{'h':>6s}  {'D2':>14s}  {'D3':>14s}  {'D4':>14s}  {'D5':>14s}  {'D6':>14s}  PF order")
    for h in h_test_values:
        dets = []
        for r in range(2, 7):
            try:
                d = toeplitz_det_from_values(kfunc, h, r)
                dets.append(d)
            except:
                dets.append(float('nan'))
        pf_order = 1
        for d in dets:
            if d > 0:
                pf_order += 1
            else:
                break
        sign_str = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
        print(f"{h:6.3f}  {dets[0]:14.6e}  {dets[1]:14.6e}  {dets[2]:14.6e}  {dets[3]:14.6e}  {dets[4]:14.6e}  PF_{pf_order} [{sign_str}]")

###############################################################################
# 5. Hardy Z-function: detailed analysis
###############################################################################

print("\n\n=== Hardy Z-Function Deep Dive ===\n")

# Z(t) is real for real t, and Z(t) = 0 iff zeta(1/2+it) = 0.
# Can we represent Z(t) = integral psi(u) cos(tu) du?
# If so, what are the PF properties of psi?

# Z(t) = e^{i*theta(t)} * zeta(1/2+it)
# Xi(1/2+it) = G(1/2+it) * zeta(1/2+it) where G includes gamma factors
# So zeta(1/2+it) = Xi(1/2+it) / G(1/2+it)
# Z(t) = e^{i*theta(t)} * Xi(1/2+it) / G(1/2+it)
# Z(t) = e^{i*theta(t)} / G(1/2+it) * Xi(1/2+it)

# The "correction factor" is e^{i*theta(t)} / G(1/2+it). Let's compute this.
print("Correction factor Z(t)/Xi(1/2+it) = e^{i*theta}/G:")
for t in [1, 5, 10, 14.13, 20, 30, 50]:
    xi_val = xi_on_line(t)
    z_val = hardy_Z(t)
    if abs(xi_val) > 1e-10:
        ratio = z_val / xi_val
        print(f"  t={t:6.2f}: Z = {z_val:12.6f}, Xi = {xi_val:12.6f}, Z/Xi = {ratio:12.6f}")
    else:
        print(f"  t={t:6.2f}: Z = {z_val:12.6f}, Xi = {xi_val:12.6f} (near zero)")

# The Z-function kernel: psi(u) = (1/pi) * integral_0^inf Z(t) cos(ut) dt
print("\nHardy Z kernel values:")
Z_kernel_vals = {}
for u in u_vals:
    val = kernel_from_real_func(Z_vals, u)
    Z_kernel_vals[str(u)] = val
    print(f"  psi({u:.2f}) = {val:14.6e}")

# Check if Z kernel goes negative
print("\nDoes Z kernel go negative?")
u_fine = np.linspace(0, 2, 201)
Z_kernel_fine = [kernel_from_real_func(Z_vals, u) for u in u_fine]
for i, (u, v) in enumerate(zip(u_fine, Z_kernel_fine)):
    if v < 0 and i > 0 and Z_kernel_fine[i-1] >= 0:
        print(f"  Z kernel first negative at u ~ {u:.3f}, value = {v:.6e}")
        break
else:
    min_val = min(Z_kernel_fine)
    min_u = u_fine[Z_kernel_fine.index(min_val)] if isinstance(Z_kernel_fine, list) else u_fine[np.argmin(Z_kernel_fine)]
    print(f"  Z kernel minimum: {min_val:.6e} at u = {min_u:.3f}")
    if min_val >= 0:
        print(f"  Z kernel appears NON-NEGATIVE on [0, 2]!")

###############################################################################
# 6. The Riemann-Siegel theta function analysis
###############################################################################

print("\n\n=== Riemann-Siegel Theta Analysis ===\n")

def theta_RS(t):
    """Riemann-Siegel theta function."""
    t = mpmath.mpf(t)
    return float(mpmath.im(mpmath.loggamma(mpmath.mpc('0.25', t/2))) - t/2 * mpmath.log(mpmath.pi))

# theta(t) grows like (t/2)*log(t/(2*pi*e)) + pi/8
# The correction factor between Z and Xi is:
# Z(t) = e^{i*theta(t)} * zeta(1/2+it)
# Xi(1/2+it) = G(1/2+it) * zeta(1/2+it)
# So Z(t) = e^{i*theta(t)} / G(1/2+it) * Xi(1/2+it)
# The factor F(t) = e^{i*theta(t)} / G(1/2+it) is a "rotation" factor.

print("Theta function values:")
for t in [1, 5, 10, 20, 50, 100]:
    th = theta_RS(t)
    print(f"  theta({t:5.0f}) = {th:12.6f}")

# |G(1/2+it)| growth rate
print("\n|G(1/2+it)| growth (should be ~ |t|^{1/2}):")
for t in [1, 5, 10, 20, 50, 100]:
    G_val = gamma_factor_on_line(t)
    print(f"  |G(1/2+i*{t:5.0f})| = {abs(G_val):14.6e}, |t|^{0.5} = {t**0.5:14.6e}, ratio = {abs(G_val)/t**0.5:14.6e}")

###############################################################################
# 7. Alternative completion: xi without s(s-1)
###############################################################################

print("\n\n=== Alternative Completion: Without s(s-1) Factor ===\n")

# xi_alt(s) = pi^{-s/2} * Gamma(s/2) * zeta(s) (no s(s-1)/2 factor)
# This has poles at s=0 and s=1 (from zeta), and the gamma function has poles at s = 0, -2, -4, ...
# But: Gamma(s/2)*zeta(s) is well-defined for Re(s) > 0, s != 1

def xi_alt_on_line(t):
    """pi^{-s/2} * Gamma(s/2) * zeta(s), s = 1/2+it. Complex in general."""
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    val = mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
    return complex(val)

xi_alt_vals = np.array([xi_alt_on_line(t) for t in t_grid])
xi_alt_real = np.real(xi_alt_vals)
xi_alt_imag = np.imag(xi_alt_vals)

print("Alternative Xi (no s(s-1)) on critical line:")
for t_idx in [0, 100, 200, 500, 1000, 2000]:
    t = t_grid[t_idx]
    v = xi_alt_vals[t_idx]
    print(f"  t={t:6.2f}: Re = {v.real:14.6e}, Im = {v.imag:14.6e}, |val| = {abs(v):14.6e}")

# The Re part of xi_alt on the critical line:
# xi_alt(1/2+it) = pi^{-1/4-it/2} * Gamma(1/4+it/2) * zeta(1/2+it)
# The s(s-1)/2 = -(1+4t^2)/8 factor is REAL and NEGATIVE for t > 0.
# So Xi(1/2+it) = s(s-1)/2 * xi_alt(1/2+it)
# and Xi is real => Re(s(s-1)/2 * xi_alt) = s(s-1)/2 * Re(xi_alt) is real
# But s(s-1)/2 is real, so Re(xi_alt) = Xi / s(s-1)/2.

print("\nRelationship between Xi and xi_alt:")
for t_idx in [100, 500, 1000, 2000]:
    t = t_grid[t_idx]
    xi_val = xi_vals[t_idx]
    s_val = s_factor_vals[t_idx]
    if abs(s_val) > 1e-10:
        ratio = xi_val / s_val
        alt_real = xi_alt_real[t_idx]
        print(f"  t={t:6.2f}: Xi/s_factor = {ratio:14.6e}, Re(xi_alt) = {alt_real:14.6e}, match: {abs(ratio - alt_real) < 1e-4}")

# Kernel of xi_alt (real part)
print("\nKernel of xi_alt (real part):")
for u in [0, 0.1, 0.2, 0.3, 0.5, 1.0]:
    val = kernel_from_complex_func_real(xi_alt_vals, u)
    print(f"  K_alt({u:.1f}) = {val:14.6e}")

###############################################################################
# 8. Save results
###############################################################################

results = {
    'kernel_data': kernel_data,
    'Z_kernel': Z_kernel_vals,
    'description': 'Kernel decomposition: Xi = G * zeta, Hardy Z, alternative completions'
}

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/gamma-bypass/kernel_decomposition_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\n\nDone. Results saved.")
