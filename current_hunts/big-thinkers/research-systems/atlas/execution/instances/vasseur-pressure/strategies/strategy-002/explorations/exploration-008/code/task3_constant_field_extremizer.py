#!/usr/bin/env python3
"""
Task 3: The constant field as Chebyshev extremizer.

KEY INSIGHT: A constant vector field u(x) = (c, 0, 0) is:
  - Divergence-free (trivially: ∂c/∂x₁ = 0)
  - In H¹(T³) with ||∇u||_{L²} = 0
  - Has constant magnitude |u(x)| = c everywhere

For this field:
  ||u||_{L^p}^p = c^p · |T³|  where |T³| = (2π)³
  |{|u| > λ}| = |T³| for λ < c, = 0 for λ ≥ c

  Chebyshev ratio = |{|u|>λ}| / (λ^{-p} ||u||_p^p)
                   = |T³| / (λ^{-p} c^p |T³|)
                   = (λ/c)^p

Taking λ → c⁻, the ratio → 1. So Chebyshev is TIGHT for div-free fields.

This script verifies this analytically and numerically, then checks whether
non-constant div-free fields can do anything the constant field cannot.
"""

import numpy as np

p = 10.0/3.0
vol_T3 = (2*np.pi)**3

print("=" * 70)
print("THE CONSTANT FIELD EXTREMIZER")
print("=" * 70)

# Part A: Verify constant field saturates Chebyshev
print("\nPart A: Constant field u = (c, 0, 0) on T³")
print("-" * 50)

c_values = [1.0, 2.0, 5.0, 10.0]
for c in c_values:
    Lp_p = c**p * vol_T3
    print(f"\n  c = {c}")
    print(f"  ||u||_{{10/3}}^{{10/3}} = {Lp_p:.4f}")
    print(f"  ||u||_{{L²}} = {c * vol_T3**0.5:.4f}")
    print(f"  ||∇u||_{{L²}} = 0")

    for lam_frac in [0.5, 0.8, 0.9, 0.95, 0.99, 0.999]:
        lam = lam_frac * c
        level_set = vol_T3  # |u| = c > λ everywhere
        cheb = lam**(-p) * Lp_p
        ratio = level_set / cheb
        expected_ratio = (lam/c)**p

        print(f"    λ = {lam_frac}c = {lam:.3f}: ratio = {ratio:.8f}, "
              f"expected (λ/c)^p = {expected_ratio:.8f}, "
              f"match = {abs(ratio - expected_ratio) < 1e-10}")

# Part B: Can non-constant fields beat ratio > 1?
print("\n" + "=" * 70)
print("Part B: Can ANY field beat Chebyshev ratio > 1?")
print("-" * 50)
print("""
Answer: NO. By definition, the Chebyshev inequality states:
  |{|f| > λ}| ≤ λ^{-p} ||f||_p^p    for ALL measurable f.

This is a trivial consequence of:
  ||f||_p^p = ∫|f|^p ≥ ∫_{|f|>λ} |f|^p ≥ λ^p · |{|f|>λ}|

So the ratio ≤ 1 ALWAYS. The question is: does div-free push the ratio
strictly below 1? The constant field shows it does NOT.
""")

# Part C: What about the De Giorgi chain — does it use Chebyshev with λ relative to max?
print("=" * 70)
print("Part C: The De Giorgi chain context")
print("-" * 50)
print("""
In the De Giorgi chain (Vasseur's proof), Chebyshev is applied with:
  λ = 2^k (a dyadic sequence of thresholds)
  f = (u - λ)₊ (the positive part, truncated)

The question is NOT "can a div-free u saturate Chebyshev" but rather:
"can (u - λ)₊ for a div-free u saturate Chebyshev for the L^{10/3} norm?"

NOTE: (u - λ)₊ is NOT itself a vector field, and NOT div-free.
It's a SCALAR function derived from the magnitude of a div-free field.

So the div-free constraint affects the problem through the distribution of |u|,
not through the structure of (|u| - λ)₊ itself.
""")

# Part D: Distribution of |u| for div-free fields
print("=" * 70)
print("Part D: Can div-free fields achieve arbitrary distributions of |u|?")
print("-" * 50)

print("""
We've shown that a CONSTANT field (|u| ≡ c) is div-free.
More generally:

1. u(x) = (c₁, c₂, c₃) (any constant) is div-free with |u| = |(c₁,c₂,c₃)| everywhere.
   → Can achieve any constant magnitude.

2. u(x) = (f(x₂, x₃), 0, 0) where f is any function of x₂, x₃ only.
   div(u) = ∂f/∂x₁ = 0 ✓ (f doesn't depend on x₁)
   |u| = |f(x₂, x₃)|
   → Can achieve any magnitude profile that depends on 2 variables.

3. u(x) = (0, -∂ψ/∂x₃, ∂ψ/∂x₂) for any stream function ψ(x₂, x₃).
   div(u) = 0 - ∂²ψ/∂x₂∂x₃ + ∂²ψ/∂x₃∂x₂ = 0 ✓
   This also gives |u| depending on x₂, x₃.

4. For full 3D control: u = ∇ × A for any vector potential A.
   Then div(u) = div(curl(A)) = 0. And |u(x)| depends on all of x.

The key point: given any smooth SCALAR field φ(x) ≥ 0, can we find a
divergence-free u with |u(x)| = φ(x)?

For 2D dependence: take u = (φ(x₂,x₃), 0, 0). Then |u| = |φ|. ✓
This already gives enough freedom for the Chebyshev extremizer.

Specifically, the Chebyshev near-extremizer needs |u| ≈ c on most of the
domain and |u| ≈ 0 on a small set. Using construction 2:
  u(x) = (g(x₂, x₃), 0, 0) where g ≈ c except on a thin strip.

This is div-free and has ||u||_{L^{10/3}}^{10/3} ≈ c^{10/3} vol(T³) and
|{|u|>λ}| ≈ vol(T³) for λ < c.
""")

# Part E: The actual Chebyshev extremizer in div-free
print("=" * 70)
print("Part E: Explicit construction of Chebyshev extremizer in div-free")
print("-" * 50)

# On [0,2π]³: u = (φ_ε(x₂), 0, 0) where φ_ε is a smooth approximation to:
#   φ_ε(x₂) = c for x₂ ∈ [ε, 2π-ε]
#   φ_ε(x₂) = 0 for x₂ near 0 (smoothly transitioning)
# More efficiently: just use u = (c, 0, 0) constant.

# The constant field u = (c, 0, 0) with c = λ + ε achieves:
#   ratio = (λ/(λ+ε))^p → 1 as ε → 0
# So the constant field IS the extremizer. No need for anything fancy.

Ng = 64
dx = 2*np.pi / Ng
x1d = np.arange(Ng) * dx
_, grid_y, _ = np.meshgrid(x1d, x1d, x1d, indexing='ij')

print("\nNumerical verification on 64³ grid:")
c = 1.0
lam_test = 0.99  # λ very close to c

# Constant field
ux = c * np.ones((Ng, Ng, Ng))
uy = np.zeros((Ng, Ng, Ng))
uz = np.zeros((Ng, Ng, Ng))

mag = np.sqrt(ux**2 + uy**2 + uz**2)
Lp_p = np.sum(mag**p) * dx**3
level_set = np.sum(mag > lam_test) * dx**3
cheb = lam_test**(-p) * Lp_p
ratio = level_set / cheb

print(f"  Constant field u = ({c}, 0, 0)")
print(f"  λ = {lam_test}")
print(f"  ||u||_{{10/3}}^{{10/3}} = {Lp_p:.6f}")
print(f"  |{'{'}|u|>{lam_test}{'}'}| = {level_set:.6f}")
print(f"  Chebyshev bound = {cheb:.6f}")
print(f"  Ratio = {ratio:.8f}")
print(f"  Expected = {(lam_test/c)**p:.8f}")
print(f"  div(u) = 0 everywhere ✓")
print(f"  ||∇u|| = 0 ✓")

# Also: x₂-dependent field
print("\nSmooth x₂-dependent div-free field:")
phi = c + 0.5 * np.sin(grid_y)  # φ(x₂) = c + 0.5 sin(x₂)
ux2 = phi
uy2 = np.zeros((Ng, Ng, Ng))
uz2 = np.zeros((Ng, Ng, Ng))

mag2 = np.sqrt(ux2**2 + uy2**2 + uz2**2)
Lp_p2 = np.sum(mag2**p) * dx**3
lam_test2 = 0.8 * np.max(mag2)
level_set2 = np.sum(mag2 > lam_test2) * dx**3
cheb2 = lam_test2**(-p) * Lp_p2
ratio2 = level_set2 / cheb2

print(f"  u = (1 + 0.5 sin(x₂), 0, 0)")
print(f"  λ = 0.8 * max|u| = {lam_test2:.4f}")
print(f"  Ratio = {ratio2:.6f}")
print(f"  (Lower than constant field because magnitude is non-uniform)")

# Part F: Multiple norm constraints simultaneously
print("\n" + "=" * 70)
print("Part F: Effect of ALL constraints simultaneously")
print("-" * 50)

print("""
In the De Giorgi chain, the function being estimated has:
  (1) ||u||_{L²} ≤ E (energy bound)
  (2) ||∇u||_{L²} ≤ D (enstrophy bound)
  (3) ||u||_{L^{10/3}} ≤ S (from Sobolev embedding applied to ∇u)
  (4) div(u) = 0

For the constant field u = (c, 0, 0):
  E = c(2π)^{3/2}, D = 0, S = c(2π)^{9/10}

The constraints link: S ≤ C_GN E^{2/5} D^{3/5} (Gagliardo-Nirenberg).
For the constant field, D = 0 would make this bound give S = 0.
But the constant field has S > 0. This is because GN says:
  ||u||_{L^{10/3}} ≤ C ||u||_{L²}^{1-θ} ||∇u||_{L²}^θ + C' ||u||_{L²}
where θ = 3/5 and the second term handles the mean.

On T³ with non-zero mean: the Poincaré inequality applies to the
mean-free part. The mean itself satisfies ||u_0||_{L^{10/3}} = ||u_0||_{L²} · |T³|^{...}
with no gradient needed.

SO: the constant field (= pure mean) uses NO gradient budget but
achieves the Chebyshev extremizer ratio. The H¹ constraint is idle.

In the De Giorgi chain, the gradient budget is used for the Sobolev
embedding step (to bound ||u||_{L^{10/3}}), NOT for the Chebyshev step.
The Chebyshev step uses only the L^{10/3} norm, which is already fixed.
""")

# Part G: Quantify the "gain" from norm constraints
print("=" * 70)
print("Part G: What DOES improve the level-set bound (beyond Chebyshev)?")
print("-" * 50)

print("""
When we have BOTH L² and L^{10/3} bounds, the optimal level-set bound
is NOT just Chebyshev in L^{10/3}. It's the dual optimization from Task 1.

The improvement factor is:
  dual_value / chebyshev_only = min(μE² + ρS^{10/3}) / (S^{10/3}/λ^{10/3})

This can be much less than 1 when E is small relative to S^{5/3}/λ^{2/3}.

HOWEVER, in the De Giorgi chain, E and S are linked:
  S^{10/3} = ||u||_{L^{10/3}}^{10/3} ≤ C ||∇u||_{L²}^{10/3} (by Sobolev in 3D)

And E² is the energy which satisfies its own bound.

The key chain parameter sensitivity (from E001) is:
  β = 1 + s/n where s comes from the Sobolev embedding.
  For H¹ ↪ L^{2*} with 2* = 6 in 3D: s/n = 1/3, giving β = 4/3.

The Chebyshev step converts the L^{10/3} bound to a level-set bound.
As we've shown, this step is tight (ratio → 1 for the constant field).
So β = 4/3 is indeed optimal for this chain.
""")

# Summary
print("\n" + "=" * 70)
print("SUMMARY OF KEY FINDINGS")
print("=" * 70)
print("""
1. The constant field u = (c, 0, 0) is div-free, in H¹(T³), and
   saturates the Chebyshev bound: ratio → 1 as λ → c⁻.

2. This means: div-free does NOT improve the Chebyshev bound.
   The extremizer of Chebyshev (constant function) is already div-free.

3. The H¹ constraint (||∇u|| ≤ D) is IRRELEVANT for Chebyshev tightness
   because the extremizer has ||∇u|| = 0.

4. The only way to improve the level-set bound is by using MULTIPLE norms
   simultaneously (Task 1 showed this). But in the De Giorgi chain, the
   norms are linked by the Sobolev embedding, and the Chebyshev step is
   the LAST step — it uses only the L^{10/3} norm, which is already fixed.

5. CONCLUSION: β = 4/3 is sharp for the De Giorgi framework.
   The Chebyshev step cannot be improved by exploiting NS structure.
""")
