#!/usr/bin/env python3
"""
Task 1: Pointwise dual of the Chebyshev optimization.

We want to solve:
  maximize |{|u| > λ}|
  subject to ||u||_{L^p}^p ≤ S^p

The Chebyshev inequality gives: |{|u| > λ}| ≤ λ^{-p} S^p.

DUAL FORMULATION:
The dual of the level-set measure optimization is the pointwise problem:
  minimize ρ S^p
  subject to ρ |v|^p ≥ 1 for all |v| > λ
  ρ ≥ 0

The constraint ρ|v|^p ≥ 1 for |v| > λ requires ρ ≥ 1/|v|^p for all |v| > λ.
The tightest constraint is at |v| = λ (the minimum of |v|^p for |v| > λ):
  ρ ≥ 1/λ^p

So the dual optimal is: ρ* = 1/λ^p, giving dual value = S^p / λ^p.
This IS the Chebyshev bound.

Now with two norms (L^2 and L^{10/3}):
  minimize μ E^2 + ρ S^{10/3}
  subject to μ r^2 + ρ r^{10/3} ≥ 1 for all r > λ
  μ, ρ ≥ 0

This is a semi-infinite LP in (μ, ρ). We discretize r ∈ (λ, R_max] and solve.
"""

import numpy as np
from scipy.optimize import linprog, minimize
import sys

# Parameters
p = 10/3  # Exponent for L^{10/3}
lam = 1.0  # Threshold λ (we normalize)

# ============================================================
# Part A: Single-norm Chebyshev (p = 10/3 only)
# ============================================================
print("=" * 60)
print("PART A: Single-norm pointwise dual (L^{10/3} only)")
print("=" * 60)

# Dual: min ρ S^p s.t. ρ r^p ≥ 1 for r > λ
# Optimal: ρ* = 1/λ^p, value = S^p / λ^p
S_values = [1.0, 2.0, 5.0]
for S in S_values:
    cheb_bound = S**p / lam**p
    rho_opt = 1.0 / lam**p
    dual_val = rho_opt * S**p
    print(f"  S={S:.1f}, λ={lam:.1f}: Chebyshev bound = {cheb_bound:.6f}, dual value = {dual_val:.6f}, match = {abs(cheb_bound - dual_val) < 1e-10}")

# ============================================================
# Part B: Two-norm dual (L^2 and L^{10/3})
# ============================================================
print("\n" + "=" * 60)
print("PART B: Two-norm pointwise dual (L^2 + L^{10/3})")
print("=" * 60)

def solve_two_norm_dual(E, S, lam, R_max=100.0, n_grid=10000):
    """
    Solve: minimize μ E² + ρ S^{10/3}
           subject to μ r² + ρ r^{10/3} ≥ 1 for all r > λ
           μ, ρ ≥ 0

    Discretize r ∈ (λ, R_max] on a grid.
    This is a linear program in (μ, ρ).
    """
    p = 10/3
    # Grid of r values
    r_grid = np.linspace(lam + 1e-8, R_max, n_grid)

    # LP: min c^T x s.t. A x ≥ b, x ≥ 0
    # x = [μ, ρ]
    # c = [E², S^{10/3}]
    c = np.array([E**2, S**p])

    # Constraints: μ r_i² + ρ r_i^{10/3} ≥ 1 for each r_i
    # In scipy linprog: A_ub x ≤ b_ub, so we negate:
    # -μ r_i² - ρ r_i^{10/3} ≤ -1
    A_ub = np.column_stack([-r_grid**2, -r_grid**p])
    b_ub = -np.ones(n_grid)

    # Bounds: μ ≥ 0, ρ ≥ 0
    bounds = [(0, None), (0, None)]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if result.success:
        mu_opt, rho_opt = result.x
        dual_val = result.fun
        # Chebyshev-only bound (ρ only, μ=0)
        cheb_only = S**p / lam**p
        return {
            'mu': mu_opt, 'rho': rho_opt,
            'dual_value': dual_val,
            'chebyshev_only': cheb_only,
            'improvement_ratio': dual_val / cheb_only if cheb_only > 0 else float('inf')
        }
    else:
        return {'error': result.message}

# Test with various parameters
print("\nTwo-norm dual: does adding L^2 constraint tighten the Chebyshev bound?")
print(f"{'E':>6} {'S':>6} {'λ':>6} | {'Dual value':>12} {'Cheb only':>12} {'Ratio':>8}")
print("-" * 65)

test_cases = [
    (1.0, 2.0, 1.0),
    (1.0, 5.0, 1.0),
    (2.0, 5.0, 1.0),
    (1.0, 2.0, 0.5),
    (0.5, 2.0, 1.0),
    (10.0, 10.0, 1.0),
    (1.0, 10.0, 5.0),
]

for E, S, lam_test in test_cases:
    res = solve_two_norm_dual(E, S, lam_test)
    if 'error' in res:
        print(f"{E:6.1f} {S:6.1f} {lam_test:6.1f} | ERROR: {res['error']}")
    else:
        print(f"{E:6.1f} {S:6.1f} {lam_test:6.1f} | {res['dual_value']:12.6f} {res['chebyshev_only']:12.6f} {res['improvement_ratio']:8.4f}")
        if res['improvement_ratio'] < 0.999:
            print(f"  ** L^2 constraint helps! μ={res['mu']:.6e}, ρ={res['rho']:.6e}")

# ============================================================
# Part C: Three-norm dual (L^2 + H^1 + L^{10/3})
# ============================================================
print("\n" + "=" * 60)
print("PART C: Three-norm dual (L^2 + H^1 + L^{10/3})")
print("=" * 60)

def solve_three_norm_dual(E, D, S, lam, R_max=100.0, n_grid=10000):
    """
    Solve: minimize μ E² + ν D² + ρ S^{10/3}
           subject to μ r² + ν k²r² + ρ r^{10/3} ≥ 1 for all r > λ, all k
           μ, ν, ρ ≥ 0

    NOTE: The |∇u|² term depends on spatial structure, not just pointwise |u|.
    In Fourier: ||∇u||² = Σ |k|² |û_k|². This is NOT a pointwise function of |u|.

    So the pointwise dual with the gradient norm is:
    minimize μ E² + ν D² + ρ S^{10/3}
    subject to μ |u(x)|² + ρ |u(x)|^{10/3} ≥ 1 for |u(x)| > λ
    and ν D² is "free" (doesn't appear in the constraint)

    UNLESS we use the Sobolev embedding: ||u||_{L^6}³ ≤ C ||∇u||_{L^2}³
    Then: ||u||_{L^6} ≤ C_S D, adding an L^6 norm constraint.

    So effectively: minimize μ E² + ν D² + ρ S^{10/3}
    subject to μ r² + ρ r^{10/3} ≥ 1 for r > λ (pointwise)
    and ν is chosen to absorb the L^6 constraint through Sobolev.

    Actually, the gradient constraint enters through Gagliardo-Nirenberg:
    ||u||_{L^{10/3}} ≤ C ||u||_{L^2}^{1-θ} ||∇u||_{L^2}^θ where θ = 3(1/2 - 3/10)/(1) = 3/5

    This means S ≤ C E^{2/5} D^{3/5}, which constrains S.
    But in the dual, we take E, D, S as given (they satisfy this).

    The key insight: in the pointwise dual, ||∇u||_{L^2} ≤ D does NOT
    add a pointwise constraint on |u(x)|. It constrains the SPATIAL STRUCTURE.
    The pointwise dual ignores spatial structure — it only sees the distribution
    of values. So the gradient constraint is invisible at the pointwise level.
    """
    p = 10/3
    r_grid = np.linspace(lam + 1e-8, R_max, n_grid)

    # The gradient norm doesn't give a pointwise constraint.
    # But we can add an L^6 constraint via Sobolev:
    # ||u||_{L^6} ≤ C_S ||∇u||_{L^2}, C_S = (6π²)^{-1/3} ≈ for 3D torus
    # C_S for T^3: we'll use a typical value
    C_S = 1.0 / (2 * np.pi)  # rough constant for T^3
    L6_bound = C_S * D  # ||u||_{L^6} ≤ L6_bound

    # Now we have three norms: L^2, L^6, L^{10/3}
    # Dual: min μ E² + σ L6_bound^6 + ρ S^{10/3}
    # s.t. μ r² + σ r^6 + ρ r^{10/3} ≥ 1 for r > λ

    c = np.array([E**2, L6_bound**6, S**p])
    A_ub = np.column_stack([-r_grid**2, -r_grid**6, -r_grid**p])
    b_ub = -np.ones(n_grid)
    bounds = [(0, None), (0, None), (0, None)]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if result.success:
        mu_opt, sigma_opt, rho_opt = result.x
        dual_val = result.fun
        cheb_only = S**p / lam**p
        return {
            'mu': mu_opt, 'sigma': sigma_opt, 'rho': rho_opt,
            'dual_value': dual_val,
            'chebyshev_only': cheb_only,
            'improvement_ratio': dual_val / cheb_only if cheb_only > 0 else float('inf'),
            'L6_bound': L6_bound
        }
    else:
        return {'error': result.message}

print("\nThree-norm dual: does adding H^1 (via Sobolev→L^6) tighten the bound?")
print(f"{'E':>6} {'D':>6} {'S':>6} {'λ':>6} | {'Dual':>10} {'Cheb':>10} {'Ratio':>8} {'L6bnd':>8}")
print("-" * 75)

test_cases_3 = [
    (1.0, 5.0, 2.0, 1.0),
    (1.0, 10.0, 2.0, 1.0),
    (2.0, 10.0, 5.0, 1.0),
    (1.0, 20.0, 3.0, 1.0),
    (5.0, 50.0, 10.0, 2.0),
]

for E, D, S, lam_test in test_cases_3:
    res = solve_three_norm_dual(E, D, S, lam_test)
    if 'error' in res:
        print(f"{E:6.1f} {D:6.1f} {S:6.1f} {lam_test:6.1f} | ERROR: {res['error']}")
    else:
        print(f"{E:6.1f} {D:6.1f} {S:6.1f} {lam_test:6.1f} | {res['dual_value']:10.4f} {res['chebyshev_only']:10.4f} {res['improvement_ratio']:8.4f} {res['L6_bound']:8.4f}")

# ============================================================
# Part D: Analytical verification of dual optimality
# ============================================================
print("\n" + "=" * 60)
print("PART D: Analytical verification — when is Chebyshev tight?")
print("=" * 60)

print("""
ANALYSIS: In the single-norm case (L^p only), the Chebyshev bound is:
  |{|f| > λ}| ≤ λ^{-p} ||f||_p^p

This is TIGHT: take f = (λ+ε) · 1_A where |A| = ||f||_p^p / (λ+ε)^p → ||f||_p^p / λ^p.

The dual confirms: ρ* = λ^{-p}, dual value = λ^{-p} S^p.

In the TWO-norm case (L^2 + L^{10/3}), the dual can potentially do better.
The question is: does the L^2 constraint (or equivalently, the energy bound)
provide additional information beyond L^{10/3}?

For the EXTREMIZER of Chebyshev, f = c · 1_A:
  ||f||_{L^2}² = c² |A|
  ||f||_{L^{10/3}}^{10/3} = c^{10/3} |A|
  |{|f|>λ}| = |A| (when c > λ)

If we set c = λ, |A| = S^{10/3}/λ^{10/3}:
  ||f||_{L^2}² = λ² · S^{10/3}/λ^{10/3} = S^{10/3}/λ^{4/3}

So the L^2 norm of the Chebyshev extremizer is S^{5/3}/λ^{2/3}.
If E < S^{5/3}/λ^{2/3}, the L^2 constraint is ACTIVE and the bound can be tightened.
If E ≥ S^{5/3}/λ^{2/3}, the L^2 constraint is slack and Chebyshev is optimal.
""")

# Verify this critical threshold
print("Verification of the L^2 threshold:")
for E, S, lam_test in [(1.0, 2.0, 1.0), (0.5, 2.0, 1.0), (1.0, 5.0, 1.0)]:
    threshold = S**(5/3) / lam_test**(2/3)
    res = solve_two_norm_dual(E, S, lam_test)
    if 'error' not in res:
        active = "ACTIVE (L^2 helps)" if E < threshold else "SLACK (Chebyshev optimal)"
        print(f"  E={E}, S={S}, λ={lam_test}: threshold={threshold:.4f}, E vs threshold: {active}")
        print(f"    Dual ratio = {res['improvement_ratio']:.6f}")

print("\n" + "=" * 60)
print("PART E: Key insight — does div-free affect the distribution of values?")
print("=" * 60)
print("""
CRITICAL OBSERVATION:

The pointwise dual does NOT see the div-free constraint at all.
The constraint div(u) = 0 is a SPATIAL constraint — it constrains how
values are arranged in space, not what the distribution of values is.

The Chebyshev inequality depends ONLY on the distribution of |u(x)|.
For any distribution d(r) of radial values satisfying:
  ∫ r^2 d(r) dr = E²  and  ∫ r^{10/3} d(r) dr = S^{10/3}
the level set measure is:
  |{|u| > λ}| = ∫_{r>λ} d(r) dr

The question is: does div-free constrain which distributions d(r) are realizable?

Answer: NO, for any smooth distribution of positive values, there exists a
div-free vector field on T³ achieving it (by appropriate choice of direction field).
This is because the div-free constraint constrains the DIRECTION of u, not its magnitude.

EXCEPTION: The ∇u constraint (H¹ norm) DOES constrain the distribution indirectly,
because rapid oscillation in |u| requires large |∇u|. But this is captured by
the Sobolev embedding, which adds an L^6 constraint — already included in Part C.
""")
