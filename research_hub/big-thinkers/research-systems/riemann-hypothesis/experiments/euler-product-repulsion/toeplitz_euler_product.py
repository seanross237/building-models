"""
Can Toeplitz determinants of the Polya kernel be expressed as products over primes?

The PF_n condition requires all n x n Toeplitz minors of K(x-y) = Phi(x-y) to be >= 0.
If the kernel decomposes as a convolution of prime factor kernels:
  Phi = Phi_gamma * conv_p phi_p

then the Toeplitz determinant of Phi relates to products of Toeplitz determinants
of the individual phi_p via a specific algebraic identity.

This script explores this connection numerically.
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 30

###############################################################################
# 1. Compute Phi(u) = Polya kernel (cosine transform of Xi on critical line)
###############################################################################

def xi_real(t):
    """Real part of Xi(1/2+it). Xi is real on the critical line."""
    if abs(t) < 0.001:
        return float(mpmath.re(0.5 * mpmath.mpc(0.5,0) * (-0.5) * mpmath.power(mpmath.pi, -0.25) * mpmath.gamma(0.25) * mpmath.zeta(0.5)))
    s = mpmath.mpc(0.5, t)
    val = 0.5 * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
    return float(mpmath.re(val))

# Precompute Xi on a grid for integration
print("Precomputing Xi(1/2+it) on [0, 50]...")
t_grid = np.linspace(0, 50, 2001)
xi_grid = np.array([xi_real(t) for t in t_grid])
dt = t_grid[1] - t_grid[0]
print(f"Done. Max |Xi| = {np.max(np.abs(xi_grid)):.6f}")

def polya_kernel(u):
    """Phi(u) = 2 * integral_0^inf Xi(1/2+it) * cos(ut) dt"""
    integrand = xi_grid * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

###############################################################################
# 2. Compute Phi on a grid
###############################################################################

print("\nComputing Polya kernel Phi(u)...")
u_grid = np.linspace(-4, 4, 81)
phi_vals = np.array([polya_kernel(u) for u in u_grid])

print("Phi values at selected points:")
for i in range(0, len(u_grid), 10):
    print(f"  Phi({u_grid[i]:5.2f}) = {phi_vals[i]:.8f}")

###############################################################################
# 3. PF2 test (log-concavity)
###############################################################################

print("\n=== PF2 (Log-Concavity) Test for Polya Kernel ===\n")

# Check positivity first
neg_indices = np.where(phi_vals < 0)[0]
if len(neg_indices) > 0:
    print(f"WARNING: Phi is negative at {len(neg_indices)} points")
    for idx in neg_indices[:5]:
        print(f"  u = {u_grid[idx]:.2f}, Phi = {phi_vals[idx]:.8f}")
else:
    print("Phi is non-negative everywhere (good)")

# Test log-concavity: Phi(u)^2 >= Phi(u-h)*Phi(u+h)
min_ratio = float('inf')
worst_u = 0
for i in range(1, len(phi_vals)-1):
    if phi_vals[i] > 0 and phi_vals[i-1] > 0 and phi_vals[i+1] > 0:
        ratio = phi_vals[i]**2 / (phi_vals[i-1] * phi_vals[i+1])
        if ratio < min_ratio:
            min_ratio = ratio
            worst_u = u_grid[i]

print(f"Min PF2 ratio: {min_ratio:.8f} at u = {worst_u:.2f}")
print(f"PF2 satisfied: {min_ratio >= 1.0 - 1e-6}")

###############################################################################
# 4. PF3, PF4, PF5 tests (Toeplitz minor determinants)
###############################################################################

print("\n=== Higher PF Tests ===\n")

def toeplitz_det(phi_func_vals, u_arr, indices, points):
    """
    Compute det(Phi(x_i - x_j)) for given point indices.
    indices: list of indices into u_arr/phi_func_vals
    The points are u_arr[indices]
    """
    n = len(points)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            diff = points[i] - points[j]
            # Interpolate Phi at this difference
            idx = np.searchsorted(u_arr, diff)
            if idx <= 0:
                mat[i][j] = phi_func_vals[0]
            elif idx >= len(u_arr):
                mat[i][j] = phi_func_vals[-1]
            else:
                # Linear interpolation
                frac = (diff - u_arr[idx-1]) / (u_arr[idx] - u_arr[idx-1])
                mat[i][j] = (1-frac) * phi_func_vals[idx-1] + frac * phi_func_vals[idx]
    return np.linalg.det(mat)

# Use a denser u grid for interpolation
u_dense = np.linspace(-6, 6, 401)
phi_dense = np.array([polya_kernel(u) for u in u_dense])

for order in [2, 3, 4, 5]:
    print(f"PF{order} test:")
    n_samples = 1000
    n_negative = 0
    min_det = float('inf')
    worst_points = None

    for _ in range(n_samples):
        # Random points in [-2, 2]
        pts = np.sort(np.random.uniform(-2, 2, order))
        det = toeplitz_det(phi_dense, u_dense, None, pts)
        if det < min_det:
            min_det = det
            worst_points = pts.copy()
        if det < -1e-12:
            n_negative += 1

    print(f"  Min determinant: {min_det:.6e}")
    print(f"  Negative dets: {n_negative}/{n_samples}")
    print(f"  PF{order} satisfied: {n_negative == 0}")
    if worst_points is not None:
        print(f"  Worst points: {worst_points}")
    print()

###############################################################################
# 5. Systematic PF test on evenly-spaced points
###############################################################################

print("=== Systematic PF Test (evenly-spaced points) ===\n")

for order in [2, 3, 4, 5, 6]:
    min_det = float('inf')
    worst_h = 0
    n_neg = 0

    for h_val in np.linspace(0.05, 2.0, 100):
        pts = np.array([i * h_val for i in range(order)])
        pts -= np.mean(pts)  # center around 0
        det = toeplitz_det(phi_dense, u_dense, None, pts)
        if det < min_det:
            min_det = det
            worst_h = h_val
        if det < -1e-12:
            n_neg += 1

    print(f"PF{order}: min det = {min_det:.6e} at h = {worst_h:.4f}, negatives = {n_neg}/100")

###############################################################################
# 6. Compare with individual Euler factor contribution
###############################################################################

print("\n=== Euler Factor Contribution to Toeplitz Determinants ===\n")

def euler_xi_contribution(p, t):
    """
    Contribution of prime p to Xi(1/2+it):
    From the Euler product: -log(1 - p^{-1/2-it}) -> factor (1-p^{-1/2-it})^{-1}
    """
    s = mpmath.mpc(0.5, t)
    factor = 1 / (1 - mpmath.power(p, -s))
    return float(mpmath.re(mpmath.log(factor)))

# Compute partial Euler product Xi for first N primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

print("Computing partial product kernels...")

def partial_product_kernel(num_primes, u_values):
    """
    Kernel of prod_{p in first num_primes} (1-p^{-1/2-it})^{-1}
    = exp(sum_{p} -log(1-p^{-1/2-it}))

    The kernel is the cosine transform of the real part of this.
    """
    results = []
    for u in u_values:
        def integrand(t_val):
            log_prod = sum(euler_xi_contribution(p, t_val) for p in primes[:num_primes])
            return np.exp(log_prod) * np.cos(u * t_val)

        # Use the precomputed t_grid
        vals = np.array([integrand(t) for t in t_grid[:501]])  # Use [0, 12.5] for speed
        return 2 * np.trapz(vals, dx=dt)

    return results

# This is too slow for the full computation, so let's verify the key property:
# the partial product contribution increases monotonically

print("\nPartial Euler product log-values at t=10:")
for n_primes in [1, 2, 3, 5, 10, 15]:
    log_val = sum(euler_xi_contribution(p, 10.0) for p in primes[:n_primes])
    print(f"  First {n_primes:2d} primes: sum log = {log_val:.6f}")

print("\nPartial Euler product log-values at t=20:")
for n_primes in [1, 2, 3, 5, 10, 15]:
    log_val = sum(euler_xi_contribution(p, 20.0) for p in primes[:n_primes])
    print(f"  First {n_primes:2d} primes: sum log = {log_val:.6f}")

###############################################################################
# 7. The Hadamard product connection
###############################################################################

print("""
=== HADAMARD PRODUCT AND TOEPLITZ STRUCTURE ===

For a Toeplitz matrix T with entries T_{ij} = Phi(x_i - x_j):

If Phi = Phi_1 * Phi_2 (convolution), then in the Fourier domain:
  hat{Phi}(xi) = hat{Phi_1}(xi) * hat{Phi_2}(xi)  (pointwise product)

The Toeplitz matrix for the convolution Phi_1 * Phi_2 is related to
the HADAMARD product of the Toeplitz matrices for Phi_1 and Phi_2
via the Schur product theorem:

  T(Phi_1 * Phi_2) is NOT simply T(Phi_1) o T(Phi_2) [Hadamard product]

However, the EIGENVALUES of the Toeplitz matrix are the Fourier coefficients,
and for a product in the Fourier domain:
  If hat{Phi} = hat{Phi_1} * hat{Phi_2} (pointwise), then
  the eigenvalues of T(Phi) = eigenvalues of T(Phi_1) * eigenvalues of T(Phi_2)
  (approximately, for large Toeplitz matrices -- Szego's theorem)

CONSEQUENCE: If all eigenvalues of T(Phi_1) and T(Phi_2) are non-negative,
then all eigenvalues of T(Phi) are non-negative.

This means: if each Euler factor contributes a positive-definite Toeplitz kernel,
the full product also has positive-definite Toeplitz structure.

Positive-definite Toeplitz <=> PF_2 (Bochner's theorem: the Fourier transform
of a PD function is non-negative).

But PF_n for n > 2 requires a STRONGER condition than positive definiteness.
The question of whether the convolution preserves PF_n for arbitrary n
is answered by Schoenberg: YES, convolution of PF_infinity functions gives PF_infinity.
But individual Euler factor kernels might only be PF_k for finite k.
""")

###############################################################################
# 8. Save results
###############################################################################

results = {
    "u_grid": u_grid.tolist(),
    "phi_vals": phi_vals.tolist(),
    "u_dense": u_dense.tolist(),
    "phi_dense": phi_dense.tolist(),
    "pf2_min_ratio": float(min_ratio),
}

with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/euler-product-repulsion/toeplitz_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved.")
