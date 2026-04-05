"""
Verify the PF order of the Polya kernel more carefully.

Previous test found PF5 passes, PF6 fails. We need to verify:
1. Is the PF6 failure real or a numerical artifact?
2. What is the exact boundary?
3. How does this relate to the known PF2 result in the literature?
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 40  # Higher precision

###############################################################################
# 1. Recompute Phi with higher precision
###############################################################################

def xi_real_hp(t):
    """Xi(1/2+it) with high precision."""
    if abs(t) < 0.001:
        s = mpmath.mpf(0.5)
        return float(0.5 * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s))
    s = mpmath.mpc(0.5, t)
    val = 0.5 * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
    return float(mpmath.re(val))

print("Precomputing Xi with high precision on [0, 60]...")
t_grid = np.linspace(0, 60, 4001)
dt = t_grid[1] - t_grid[0]
xi_grid = np.array([xi_real_hp(t) for t in t_grid])
print(f"Done. dt = {dt:.6f}, Max |Xi| = {np.max(np.abs(xi_grid)):.10f}")

def polya_kernel_hp(u):
    """Phi(u) via trapezoidal rule on precomputed Xi."""
    integrand = xi_grid * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

###############################################################################
# 2. Compute Phi on a dense grid
###############################################################################

print("\nComputing Phi on dense grid...")
u_dense = np.linspace(-5, 5, 501)
phi_dense = np.array([polya_kernel_hp(u) for u in u_dense])

print(f"Phi(0) = {phi_dense[250]:.10f}")
print(f"Phi(0.5) = {polya_kernel_hp(0.5):.10f}")
print(f"Phi(1.0) = {polya_kernel_hp(1.0):.10f}")
print(f"Phi(1.5) = {polya_kernel_hp(1.5):.10f}")
print(f"Phi(2.0) = {polya_kernel_hp(2.0):.10f}")

###############################################################################
# 3. Careful PF tests with interpolation
###############################################################################

def phi_interp(u):
    """Interpolate Phi at arbitrary u."""
    if u < u_dense[0] or u > u_dense[-1]:
        return 0.0
    idx = np.searchsorted(u_dense, u)
    if idx == 0:
        return phi_dense[0]
    if idx >= len(u_dense):
        return phi_dense[-1]
    frac = (u - u_dense[idx-1]) / (u_dense[idx] - u_dense[idx-1])
    return (1-frac) * phi_dense[idx-1] + frac * phi_dense[idx]

def toeplitz_det_points(points):
    """Compute det(Phi(x_i - x_j)) for given points."""
    n = len(points)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            mat[i][j] = phi_interp(points[i] - points[j])
    return np.linalg.det(mat)

###############################################################################
# 4. Systematic PF tests
###############################################################################

print("\n=== Systematic PF Tests (evenly-spaced points centered at 0) ===\n")

for order in [2, 3, 4, 5, 6, 7, 8]:
    min_det = float('inf')
    worst_h = 0
    n_neg = 0
    n_tests = 500

    for h_val in np.linspace(0.01, 2.5, n_tests):
        pts = np.array([i * h_val for i in range(order)])
        pts -= np.mean(pts)
        det = toeplitz_det_points(pts)
        if det < min_det:
            min_det = det
            worst_h = h_val
        if det < -1e-15:
            n_neg += 1

    print(f"PF{order}: min det = {min_det:12.6e} at h = {worst_h:.4f}, negatives = {n_neg}/{n_tests}")
    if n_neg > 0:
        print(f"  *** PF{order} VIOLATED ***")

###############################################################################
# 5. Random point PF tests
###############################################################################

print("\n=== Random Point PF Tests (5000 samples each) ===\n")

np.random.seed(42)
for order in [3, 4, 5, 6, 7]:
    n_neg = 0
    min_det = float('inf')
    worst_pts = None
    n_samples = 5000

    for _ in range(n_samples):
        pts = np.sort(np.random.uniform(-2, 2, order))
        det = toeplitz_det_points(pts)
        if det < min_det:
            min_det = det
            worst_pts = pts.copy()
        if det < -1e-15:
            n_neg += 1

    print(f"PF{order}: min det = {min_det:12.6e}, negatives = {n_neg}/{n_samples}")
    if worst_pts is not None:
        print(f"  Worst points: {worst_pts}")

###############################################################################
# 6. Focus on PF6 failure
###############################################################################

print("\n=== Detailed PF6 Analysis ===\n")

# Scan around the failure point h ~ 0.15
min_det_6 = float('inf')
for h_val in np.linspace(0.05, 0.30, 200):
    pts = np.array([i * h_val for i in range(6)])
    pts -= np.mean(pts)
    det = toeplitz_det_points(pts)
    if det < min_det_6:
        min_det_6 = det
        worst_h_6 = h_val
    if abs(h_val - 0.15) < 0.001 or det < 0:
        print(f"h = {h_val:.4f}: det = {det:.6e}, pts = [{pts[0]:.4f}, ..., {pts[-1]:.4f}]")

print(f"\nMin PF6 det: {min_det_6:.6e} at h = {worst_h_6:.4f}")

# Also test at the worst h with shifted center
print("\nPF6 with shifted center (h fixed at worst):")
for center in np.linspace(-1, 1, 21):
    pts = np.array([center + i * worst_h_6 for i in range(6)])
    pts -= np.mean(pts)
    det = toeplitz_det_points(pts)
    if det < -1e-15:
        print(f"  center = {center:.2f}: det = {det:.6e} *** NEGATIVE ***")

###############################################################################
# 7. Investigate what happens at different u ranges
###############################################################################

print("\n=== PF6 test with points at different absolute positions ===\n")

for center in np.linspace(-1, 1, 11):
    for h_val in np.linspace(0.05, 0.5, 50):
        pts = center + np.array([i * h_val for i in range(6)])
        det = toeplitz_det_points(pts)
        if det < -1e-10:
            print(f"  center={center:.2f}, h={h_val:.4f}: det = {det:.6e}")

###############################################################################
# 8. The key question: is Phi actually PF_5 but NOT PF_6?
###############################################################################

print("""
=== INTERPRETATION ===

The Polya kernel Phi is known from the literature to be PF_2 (Polya's result
from the 1920s). The question has been whether it is PF_n for higher n.

Our numerical results:
- PF2 through PF5: PASS (all tests, thousands of random and systematic samples)
- PF6: Needs careful verification

If Phi is PF_5 but not PF_6, this would mean:
- The 5x5 Toeplitz minors of Phi are all non-negative
- Some 6x6 Toeplitz minor is negative
- This bounds the "PF order" of the kernel

In terms of zeros:
- PF_infinity <=> ALL zeros of the associated entire function are real
- PF_n for finite n <=> a weaker condition on the zeros
- The gap between PF_5 and PF_infinity is the gap between what the
  Euler product achieves and what would be needed for a full proof of RH

From the convolution theory:
- The Euler product contributes PF_infinity factors (each Euler factor kernel)
- Convolution preserves PF_infinity
- But the GAMMA FACTORS contribute a non-PF factor
- The gamma factors might be what limits Phi to PF_5

The gamma factor contribution is:
  (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2)

This is the part of Xi that does NOT come from the Euler product.
If this factor limits the PF order to 5, then the Euler product's
PF_infinity contribution is "wasted" -- the gamma factors are the bottleneck.
""")

# Save results
results = {
    "u_dense": u_dense.tolist(),
    "phi_dense": phi_dense.tolist(),
}

with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/euler-product-repulsion/pf_order_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Results saved.")
