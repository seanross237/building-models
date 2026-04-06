"""
Davenport-Heilbronn kernel vs Zeta kernel: PF property comparison.

The DH function is: L(s) = (1-i*kappa)/2 * L(s, chi1) + (1+i*kappa)/2 * L(s, chi1_bar)
where chi1 is a character mod 5 and kappa = (sqrt(10-2*sqrt(5)) - 2)/(sqrt(5) - 1).

This satisfies the same functional equation as zeta but has zeros off the critical line.
We compute the Polya-type kernel for both and compare PF properties.
"""

import mpmath
import numpy as np
import json

mpmath.mp.dps = 50  # high precision

###############################################################################
# 1. Define the Davenport-Heilbronn function
###############################################################################

def chi1_mod5(n):
    """Non-principal character mod 5 (the one with chi(2)=i)."""
    n = n % 5
    if n == 0:
        return mpmath.mpc(0, 0)
    elif n == 1:
        return mpmath.mpc(1, 0)
    elif n == 2:
        return mpmath.mpc(0, 1)  # chi(2) = i
    elif n == 3:
        return mpmath.mpc(0, -1)  # chi(3) = -i
    elif n == 4:
        return mpmath.mpc(-1, 0)  # chi(4) = -1

def chi1_bar_mod5(n):
    """Conjugate character."""
    return mpmath.conj(chi1_mod5(n))

def dirichlet_L(s, chi_func, N_terms=5000):
    """Compute L(s, chi) = sum_{n=1}^{N} chi(n)/n^s."""
    result = mpmath.mpc(0, 0)
    for n in range(1, N_terms + 1):
        result += chi_func(n) * mpmath.power(n, -s)
    return result

# kappa parameter
sqrt5 = mpmath.sqrt(5)
kappa = (mpmath.sqrt(10 - 2*sqrt5) - 2) / (sqrt5 - 1)
print(f"kappa = {float(kappa):.10f}")

def davenport_heilbronn(s, N_terms=5000):
    """
    The Davenport-Heilbronn function.
    L_DH(s) = (1 - i*kappa)/2 * L(s, chi1) + (1 + i*kappa)/2 * L(s, chi1_bar)
    """
    c1 = (1 - mpmath.mpc(0, 1)*kappa) / 2
    c2 = (1 + mpmath.mpc(0, 1)*kappa) / 2
    L1 = dirichlet_L(s, chi1_mod5, N_terms)
    L2 = dirichlet_L(s, chi1_bar_mod5, N_terms)
    return c1 * L1 + c2 * L2

###############################################################################
# 2. Verify DH has zeros off the critical line
###############################################################################

print("\n=== Verification: DH function values ===")
# On the critical line
for t in [10, 20, 30]:
    s = mpmath.mpc(0.5, t)
    val = davenport_heilbronn(s, 3000)
    print(f"DH(0.5 + {t}i) = {float(val.real):.6f} + {float(val.imag):.6f}i, |DH| = {float(abs(val)):.6f}")

# Off the critical line (known to have zeros near sigma ~ 0.808)
print("\nSearching for DH values off the critical line (sigma=0.7 to 0.9):")
for sigma in [0.6, 0.7, 0.8, 0.85, 0.9]:
    for t in range(10, 50, 5):
        s = mpmath.mpc(sigma, t)
        val = davenport_heilbronn(s, 3000)
        if abs(val) < 0.5:
            print(f"  Small: |DH({sigma}+{t}i)| = {float(abs(val)):.6f}")

###############################################################################
# 3. Compute the "kernel" for both functions
###############################################################################

def zeta_xi(s):
    """Xi function: Xi(s) = (1/2)s(s-1)pi^{-s/2}Gamma(s/2)zeta(s)"""
    return 0.5 * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)

def dh_xi(s, N_terms=3000):
    """
    Completed DH function. For a Dirichlet L-function with conductor 5:
    Xi_DH(s) = (5/pi)^{(s+a)/2} * Gamma((s+a)/2) * L_DH(s)
    where a depends on the parity. For chi1 mod 5 (odd character), a=1.

    Actually, for the DH function we need the completed form.
    Since DH = linear combination of L(s,chi1) and L(s,chi1_bar),
    and these have conductor 5, the completed form involves the Gauss sum.

    For simplicity, we'll use: Xi_DH(s) = (5/pi)^{s/2} * Gamma((s+1)/2) * L_DH(s)
    (using a=1 for odd character -- chi1(-1) = chi1(4) = -1, so it's even, a=0)
    """
    # chi1(4) = -1, chi1(-1) = chi1(4) = -1 for mod 5, so chi1 is odd, a=1
    # Wait: chi1(-1) = chi1(4) since -1 ≡ 4 mod 5, and chi1(4) = -1, so chi1 is odd, a=1.
    a = 1
    factor = mpmath.power(5/mpmath.pi, (s + a)/2) * mpmath.gamma((s + a)/2)
    return factor * davenport_heilbronn(s, N_terms)

print("\n=== Xi function values ===")
for t in [5, 10, 15, 20]:
    s = mpmath.mpc(0.5, t)
    xi_z = zeta_xi(s)
    xi_dh = dh_xi(s)
    print(f"t={t}: Xi_zeta = {float(abs(xi_z)):.6f}, Xi_DH = {float(abs(xi_dh)):.6f}")

###############################################################################
# 4. Compute the Polya-type kernels via inverse Fourier transform
###############################################################################

def compute_polya_kernel_zeta(u_values, num_quad_points=200):
    """
    Phi(u) = integral Xi(1/2 + it) * exp(iut) dt  (Fourier transform of Xi on the critical line)

    More precisely, we use the real version:
    Phi(u) = 2 * Re[integral_0^infty Xi(1/2+it) * cos(ut) dt]

    Since Xi(1/2+it) is real for real t (by the functional equation), this simplifies.
    """
    results = []
    for u in u_values:
        # Numerical integration using mpmath.quad
        def integrand(t):
            s = mpmath.mpc(0.5, t)
            xi_val = zeta_xi(s)
            return mpmath.re(xi_val) * mpmath.cos(u * t)

        # Xi(1/2+it) is real-valued, so this integral is real
        val = 2 * mpmath.quad(integrand, [0, 50], maxdegree=7)
        results.append(float(val))
    return results

def compute_polya_kernel_dh(u_values, num_quad_points=200):
    """
    Same but for DH: Phi_DH(u) = 2 * Re[integral_0^infty Xi_DH(1/2+it) * exp(iut) dt]

    Note: Xi_DH(1/2+it) is NOT necessarily real for real t (unlike zeta's Xi).
    """
    results_re = []
    results_im = []
    for u in u_values:
        def integrand_re(t):
            s = mpmath.mpc(0.5, t)
            xi_val = dh_xi(s, 2000)
            return float(mpmath.re(xi_val * mpmath.exp(mpmath.mpc(0, u*t))))

        def integrand_im(t):
            s = mpmath.mpc(0.5, t)
            xi_val = dh_xi(s, 2000)
            return float(mpmath.im(xi_val * mpmath.exp(mpmath.mpc(0, u*t))))

        val_re = mpmath.quad(integrand_re, [0, 50], maxdegree=6)
        val_im = mpmath.quad(integrand_im, [0, 50], maxdegree=6)
        results_re.append(2 * float(val_re))
        results_im.append(2 * float(val_im))
    return results_re, results_im

print("\n=== Computing Polya kernel for zeta (this may take a while) ===")
u_vals = np.linspace(-3, 3, 31)
phi_zeta = compute_polya_kernel_zeta(u_vals)
print("Zeta kernel computed.")
print("Sample values:")
for i in range(0, len(u_vals), 5):
    print(f"  Phi_zeta({u_vals[i]:.2f}) = {phi_zeta[i]:.6f}")

print("\n=== Computing Polya kernel for DH ===")
phi_dh_re, phi_dh_im = compute_polya_kernel_dh(u_vals)
print("DH kernel computed.")
print("Sample values:")
for i in range(0, len(u_vals), 5):
    print(f"  Phi_DH({u_vals[i]:.2f}) = {phi_dh_re[i]:.6f} + {phi_dh_im[i]:.6f}i")

###############################################################################
# 5. Test PF2 (log-concavity) for both kernels
###############################################################################

def test_log_concavity(kernel_values, u_values):
    """
    Test PF2: Phi is PF2 iff Phi(u) >= 0 and log(Phi(u)) is concave.
    Equivalently: Phi(u)^2 >= Phi(u-h) * Phi(u+h) for all u, h > 0.

    Returns the min ratio Phi(u)^2 / (Phi(u-h)*Phi(u+h)).
    PF2 requires ratio >= 1 everywhere.
    """
    violations = []
    min_ratio = float('inf')
    n = len(kernel_values)

    for i in range(1, n-1):
        if kernel_values[i] <= 0:
            violations.append((u_values[i], kernel_values[i], "non-positive"))
            continue
        if kernel_values[i-1] <= 0 or kernel_values[i+1] <= 0:
            continue

        ratio = kernel_values[i]**2 / (kernel_values[i-1] * kernel_values[i+1])
        if ratio < min_ratio:
            min_ratio = ratio
        if ratio < 1.0:
            violations.append((u_values[i], ratio, "log-concavity violation"))

    return min_ratio, violations

print("\n=== PF2 (Log-Concavity) Test ===")

# For zeta kernel
min_r_z, viol_z = test_log_concavity(phi_zeta, u_vals)
print(f"\nZeta kernel:")
print(f"  Min ratio Phi^2/(Phi_left * Phi_right) = {min_r_z:.6f}")
print(f"  PF2 satisfied: {min_r_z >= 1.0 - 1e-6}")
if viol_z:
    print(f"  Violations: {viol_z[:5]}")

# For DH kernel (use absolute value since it may be complex)
phi_dh_abs = [np.sqrt(r**2 + im**2) for r, im in zip(phi_dh_re, phi_dh_im)]
min_r_dh, viol_dh = test_log_concavity(phi_dh_abs, u_vals)
print(f"\nDH kernel (|Phi|):")
print(f"  Min ratio |Phi|^2/(|Phi_left| * |Phi_right|) = {min_r_dh:.6f}")
print(f"  PF2 satisfied: {min_r_dh >= 1.0 - 1e-6}")
if viol_dh:
    print(f"  Violations: {viol_dh[:5]}")

# Also test the real part alone for DH
min_r_dh_re, viol_dh_re = test_log_concavity(phi_dh_re, u_vals)
print(f"\nDH kernel (Re(Phi)):")
print(f"  Min ratio = {min_r_dh_re:.6f}")
print(f"  PF2 satisfied: {min_r_dh_re >= 1.0 - 1e-6}")
if viol_dh_re:
    print(f"  Violations: {viol_dh_re[:5]}")

###############################################################################
# 6. Higher PF tests (PF3, PF4, PF5) via Toeplitz minors
###############################################################################

def toeplitz_minor(kernel_values, u_values, center_idx, size, step=1):
    """
    Compute the size x size Toeplitz determinant based on kernel values.
    T_{ij} = Phi(u_{center + (i-j)*step}) for the Toeplitz matrix.

    For PF_n, all n x n minors of the Toeplitz matrix [Phi(u_i - u_j)] must be non-negative.
    """
    matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            idx = center_idx + (i - j) * step
            if 0 <= idx < len(kernel_values):
                matrix[i][j] = kernel_values[idx]
            else:
                matrix[i][j] = 0  # Phi(u) -> 0 for large |u|
    return np.linalg.det(matrix)

print("\n=== Higher PF Tests (Toeplitz minors) ===")

# Use denser grid for higher PF tests
u_dense = np.linspace(-2, 2, 41)
print("Computing dense zeta kernel...")
phi_z_dense = compute_polya_kernel_zeta(u_dense)

print("\nZeta kernel Toeplitz minors:")
center = len(u_dense) // 2  # u=0

for size in [2, 3, 4, 5]:
    dets = []
    min_det = float('inf')
    for c in range(size, len(u_dense) - size):
        for step in [1, 2, 3]:
            det = toeplitz_minor(phi_z_dense, u_dense, c, size, step)
            dets.append(det)
            if det < min_det:
                min_det = det

    n_neg = sum(1 for d in dets if d < -1e-10)
    print(f"  PF{size}: min det = {min_det:.6e}, #negative = {n_neg}/{len(dets)}")
    print(f"    PF{size} satisfied: {n_neg == 0}")

###############################################################################
# 7. Save results
###############################################################################

results = {
    "kappa": float(kappa),
    "u_values": u_vals.tolist(),
    "phi_zeta": phi_zeta,
    "phi_dh_re": phi_dh_re,
    "phi_dh_im": phi_dh_im,
    "phi_dh_abs": phi_dh_abs,
    "pf2_zeta_min_ratio": float(min_r_z),
    "pf2_dh_abs_min_ratio": float(min_r_dh),
    "pf2_dh_re_min_ratio": float(min_r_dh_re),
}

with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/euler-product-repulsion/kernel_comparison_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved.")
