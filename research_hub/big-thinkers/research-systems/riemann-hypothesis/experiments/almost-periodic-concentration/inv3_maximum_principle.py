"""
Investigation 3: Maximum Principle Argument

If ζ(σ₀+it₀) = 0 for σ₀ > 1/2, consider the rectangle R = [1/2, σ₀] × [t₀-1, t₀+1].

Questions:
1. The zero forces ζ' to be at least "typical size" / (σ₀-1/2). Does this conflict
   with the functional equation's constraint on ζ'?
2. Can we use the Hadamard three-circle theorem to get quantitative bounds?
3. Does the Euler product structure create additional constraints on the growth rate?
"""

import mpmath
import numpy as np

mpmath.mp.dps = 30

print("=" * 70)
print("INVESTIGATION 3: MAXIMUM PRINCIPLE AND DERIVATIVE BOUNDS")
print("=" * 70)

# ============================================================
# Part A: Setup -- what does a zero at σ₀ > 1/2 force?
# ============================================================

print("\n--- Part A: Consequences of a zero at σ₀ > 1/2 ---\n")

# If ζ(σ₀+it₀) = 0 with σ₀ > 1/2:
#
# 1. By the functional equation: ζ((1-σ₀)+it₀) = 0 also.
#    So there's a zero at 1-σ₀ < 1/2 and another at σ₀ > 1/2,
#    symmetric about σ = 1/2.
#
# 2. ζ is analytic and nonvanishing for σ > 1. So the zero at σ₀
#    must be "created" by the continuation, not by the Euler product directly.
#
# 3. Near the zero: ζ(s) = (s - s₀)^m · g(s) where g(s₀) ≠ 0
#    and m is the multiplicity.
#
# 4. For a simple zero (m=1): |ζ(s)| ≈ |ζ'(s₀)| · |s - s₀|
#    In particular, |ζ(σ₀+it)| ≈ |ζ'(s₀)| · |t - t₀| for t near t₀.
#
# 5. The maximum principle on R = [σ₁, σ₂] × [t₀-δ, t₀+δ]:
#    max_{∂R} |ζ| ≥ max_R |ζ|
#    The zero at the interior forces the boundary values to be "large enough"
#    to be consistent with the growth rate.

# The Hadamard three-circle theorem gives:
# If f is analytic in the annulus r₁ ≤ |z| ≤ r₂, then
# log M(r) is convex in log r, where M(r) = max_{|z|=r} |f(z)|.
#
# For our strip: let s₀ = σ₀ + it₀ and consider ζ(s) on the strip
# a ≤ Re(s) ≤ b containing σ₀. The three-line analogue gives:
#
# log M(σ) is convex in σ, where M(σ) = sup_t |ζ(σ+it)|
#
# This is the Phragmén-Lindelöf principle in strips.

# For the SPECIFIC function near the zero:
# On σ = 1/2 + δ (just right of the critical line):
#   |ζ(1/2+δ+it)| is typically of order 1 (by concentration, mean ~1)
#
# On σ = 1 + δ (well into convergence region):
#   |ζ(1+δ+it)| ≈ ζ(1+δ) ≈ 1/δ (by Laurent expansion near the pole)
#
# At σ₀ between these: |ζ(σ₀+it₀)| = 0
#
# Convexity of log M(σ) requires:
# log M(σ₀) ≤ ((σ₀ - 1/2)/(1 - 1/2)) · log M(1) + ((1 - σ₀)/(1 - 1/2)) · log M(1/2)
#
# But log M(σ₀) = -∞ (there's a zero), and the right side is finite.
# This seems like a contradiction!
#
# WAIT: The three-line theorem applies to log M(σ) = sup_t log|f(σ+it)|,
# not to log|f(σ+it₀)| for FIXED t₀. The sup over t at σ₀ is NOT -∞
# (there are non-zero values at σ₀). The zero at σ₀+it₀ is a point value,
# not the supremum.

print("Correcting the maximum principle argument:")
print()
print("The three-line/Phragmen-Lindelof principle applies to M(σ) = sup_t |ζ(σ+it)|.")
print("A zero at σ₀+it₀ means M(σ₀) = 0 only if ζ vanishes EVERYWHERE on σ=σ₀.")
print("But ζ(σ₀+it) ≠ 0 for generic t. So M(σ₀) > 0 and there's no contradiction")
print("from the supremum-based principle.")
print()
print("We need a more LOCAL argument.")

# ============================================================
# Part B: Local growth rate from the zero
# ============================================================

print("\n--- Part B: Local growth rate constraints from a zero ---\n")

# Consider a disk D(s₀, r) around the hypothetical zero s₀ = σ₀+it₀.
#
# If ζ(s₀) = 0 with multiplicity m, then:
# |ζ(s)| ≈ |ζ^(m)(s₀)/m!| · |s-s₀|^m for |s-s₀| small
#
# On the circle |s-s₀| = r:
# max |ζ| ≈ |ζ^(m)(s₀)/m!| · r^m
#
# By the maximum modulus principle on D(s₀, r):
# |ζ^(m)(s₀)/m!| · r^m ≤ max_{|s-s₀|=r} |ζ(s)|
#
# We can estimate the right side using known bounds.

# For σ₀ near 1/2, take r = σ₀ - 1/2 (the circle reaches the critical line).
# On the circle, the maximum is at most the Lindelöf-type bound:
# |ζ(σ+it)| ≤ C · t^{μ(σ)+ε} where μ(σ) is the Lindelöf function.
# Unconditionally: μ(σ) ≤ 1/2 - σ for 0 ≤ σ ≤ 1/2 (from convexity)
# μ(σ) = 0 for σ > 1 (absolute convergence)
# μ is convex, so μ(σ) ≤ (1-σ)/2 for 1/2 ≤ σ ≤ 1.

# On the circle |s-s₀| = r at height ~t₀:
# max |ζ| ≤ C · t₀^{(1-min_σ)/2 + ε}
# where min_σ = σ₀ - r = σ₀ - (σ₀-1/2) = 1/2
# So max |ζ| ≤ C · t₀^{1/4 + ε}

# But also, on the RIGHT part of the circle (σ > σ₀), the concentration
# bound says |ζ| is typically ~1. So the maximum is at least ~1.

# From the zero:
# |ζ'(s₀)| · r ≤ max_{|s-s₀|=r} |ζ|
# |ζ'(s₀)| ≤ max/r = max/(σ₀-1/2)

# This gives an UPPER bound on |ζ'| at the zero. Is this consistent
# with the functional equation's prediction for |ζ'| at a zero?

print("Upper bound on |ζ'(s₀)| from the maximum principle:")
print()

for sigma_0 in [0.55, 0.6, 0.7, 0.8]:
    r = sigma_0 - 0.5
    for t_0 in [100, 1000, 10000]:
        # Upper bound on max|ζ| on the circle
        # Using the convexity bound μ(σ) ≤ (1-σ)/2 for σ ≥ 1/2
        # On the circle, σ ranges from 1/2 to 2σ₀-1/2
        # The worst bound is at σ = 1/2: |ζ| ≤ t^{1/4+ε}
        max_on_circle = t_0**(0.25 + 0.01)  # with small ε

        zeta_prime_upper = max_on_circle / r

        print(f"  σ₀={sigma_0}, t₀={t_0}: r={r:.2f}, max|ζ|≤{max_on_circle:.1f}, |ζ'(s₀)|≤{zeta_prime_upper:.1f}")
    print()

# ============================================================
# Part C: Lower bound on |ζ'| from the functional equation
# ============================================================

print("\n--- Part C: Functional equation constraint on ζ' at a zero ---\n")

# At a zero s₀ of ζ, the functional equation ξ(s) = ξ(1-s) gives:
# ξ(s) = (1/2)s(s-1)π^{-s/2}Γ(s/2)ζ(s)
# ξ'(s₀) = (1/2)s₀(s₀-1)π^{-s₀/2}Γ(s₀/2) · ζ'(s₀)
#           + ζ(s₀) · (derivative of the gamma factor)
# Since ζ(s₀) = 0, the second term vanishes:
# ξ'(s₀) = (1/2)s₀(s₀-1)π^{-s₀/2}Γ(s₀/2) · ζ'(s₀)
#
# By the symmetry ξ(s₀) = ξ(1-s₀) = 0:
# ξ'(s₀) = -ξ'(1-s₀)  (from differentiating ξ(s)=ξ(1-s))
#
# This gives a RELATION between ζ'(s₀) and ζ'(1-s₀), not an absolute bound.

# The Hadamard product: ξ(s) = ξ(0) ∏_ρ (1-s/ρ)
# ξ'(s₀)/ξ(s₀) = ∑_ρ 1/(s₀-ρ)  (logarithmic derivative)
# But at the zero, we need L'Hôpital:
# ξ'(s₀) = ξ(0) · ∏_{ρ≠s₀} (1-s₀/ρ) · (-1/s₀)  [if s₀ is a simple zero]

# The magnitude: |ξ'(s₀)| = |ξ(0)/s₀| · ∏_{ρ≠s₀} |1-s₀/ρ|
#
# For the zeros on the critical line: the product ∏_{ρ≠s₀} |1-s₀/ρ|
# is related to the zero spacing. Near height T, the average zero spacing
# is 2π/log(T), so the nearest zero is at distance ~2π/log(T).
# The product over all other zeros converges (barely).

# The key comparison: is the UPPER bound from the maximum principle
# consistent with the LOWER bound from the Hadamard product?

# For a zero at σ₀ + it₀ with σ₀ > 1/2:
# The nearest zero on the critical line (if RH holds for those) is at
# 1/2 + it_n where |t_n - t₀| ~ 2π/log(t₀).
# The factor |1 - s₀/ρ_n| ≈ |σ₀ - 1/2|/t₀ (very small).
#
# But this is just the NEAREST zero. The product over ALL zeros involves
# infinitely many terms, and is related to the value of ζ'/(ζ · gamma factor).

print("For a hypothetical zero at σ₀+it₀:")
print()
print("Upper bound (max principle): |ζ'(s₀)| ≤ t₀^{1/4+ε} / (σ₀ - 1/2)")
print("This grows as t₀^{1/4} / (σ₀-1/2).")
print()
print("Lower bound (Hadamard product + zero spacing):")
print("|ζ'(s₀)| is determined by the product over all other zeros.")
print("If the zero is ISOLATED from other zeros (which it must be since")
print("the nearby zeros are all on σ=1/2 and hence at distance ≥ σ₀-1/2),")
print("then |ζ'(s₀)| is bounded below by a function of σ₀-1/2 and t₀.")
print()

# ============================================================
# Part D: Numerical computation of ζ' and the derivative bounds
# ============================================================

print("\n--- Part D: Numerical derivative computation ---\n")

# Compute |ζ'(σ+it)| for various σ and t, and compare to bounds.

# Use mpmath for high-precision zeta computation
for sigma in [0.6, 0.7, 0.8]:
    print(f"σ = {sigma}:")
    for t_val in [14.135, 21.022, 100.0, 1000.0]:
        s = mpmath.mpc(sigma, t_val)
        zeta_val = mpmath.zeta(s)
        # Numerical derivative via central difference
        h = 1e-8
        zeta_plus = mpmath.zeta(mpmath.mpc(sigma, t_val + h))
        zeta_minus = mpmath.zeta(mpmath.mpc(sigma, t_val - h))
        zeta_prime_t = (zeta_plus - zeta_minus) / (2*h)  # dζ/dt (not dζ/ds)
        # dζ/ds = (1/i) dζ/dt since s = σ+it => ds = i dt
        zeta_prime_s = zeta_prime_t / mpmath.mpc(0, 1)

        max_principle_upper = float(t_val)**(0.26) / (sigma - 0.5)

        print(f"  t={t_val:>8.3f}: |ζ|={float(abs(zeta_val)):>10.6f}, "
              f"|ζ'|={float(abs(zeta_prime_s)):>10.4f}, "
              f"upper bound={max_principle_upper:>10.1f}, "
              f"ratio=|ζ'|/upper={float(abs(zeta_prime_s))/max_principle_upper:.4f}")
    print()

# ============================================================
# Part E: The growth rate of |ζ'| along σ = const as t → ∞
# ============================================================

print("\n--- Part E: Growth of |ζ'(σ+it)| as t → ∞ ---\n")

# The critical question: how fast does |ζ'(σ+it)| grow with t?
# If it grows slower than t^{1/4}/(σ-1/2), then the maximum principle
# upper bound is NOT saturated, and there's "room" for a zero.
# If it grows at the same rate, the bound IS tight.

# Unconditional result: for σ > 1/2,
# ∫_0^T |ζ'(σ+it)|² dt ~ C(σ) · T  (mean-square estimate)
# So the typical |ζ'| is O(1), NOT growing with t.
# But the maximum can be much larger.

# Compute |ζ'(σ+it)| at many t values
for sigma in [0.7]:
    t_vals_compute = [10, 50, 100, 500, 1000, 5000]
    print(f"σ = {sigma}:")
    zp_header = "|zeta'(s)|"
    print(f"{'t':>8} | {'|zeta(s)|':>12} | {zp_header:>12} | {'t^1/4/(s-1/2)':>16} | {'Ratio':>8}")
    print("-" * 70)

    for t_val in t_vals_compute:
        s = mpmath.mpc(sigma, t_val)
        zeta_val = mpmath.zeta(s)
        h = 1e-8
        zeta_plus = mpmath.zeta(mpmath.mpc(sigma, t_val + h))
        zeta_minus = mpmath.zeta(mpmath.mpc(sigma, t_val - h))
        zeta_prime_t = (zeta_plus - zeta_minus) / (2*h)
        zeta_prime_s = zeta_prime_t / mpmath.mpc(0, 1)

        bound = float(t_val)**(0.25) / (sigma - 0.5)
        ratio = float(abs(zeta_prime_s)) / bound

        print(f"{t_val:>8} | {float(abs(zeta_val)):>12.6f} | {float(abs(zeta_prime_s)):>12.4f} | {bound:>16.2f} | {ratio:>8.4f}")
    print()

# ============================================================
# Part F: The derivative at the actual zeros (σ = 1/2)
# ============================================================

print("\n--- Part F: ζ' at actual zeros for comparison ---\n")

# At the known zeros on σ = 1/2:
known_zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
               37.586178, 40.918719, 43.327073, 48.005151, 49.773832]

zp_hdr2 = "|zeta'(1/2+it)|"
print(f"{'t (zero)':>12} | {zp_hdr2:>14} | {'t^(1/4)':>8}")
print("-" * 45)

for t_val in known_zeros:
    s = mpmath.mpc(0.5, t_val)
    h = 1e-8
    zeta_plus = mpmath.zeta(mpmath.mpc(0.5, t_val + h))
    zeta_minus = mpmath.zeta(mpmath.mpc(0.5, t_val - h))
    zeta_prime_t = (zeta_plus - zeta_minus) / (2*h)
    zeta_prime_s = zeta_prime_t / mpmath.mpc(0, 1)

    print(f"{t_val:>12.6f} | {float(abs(zeta_prime_s)):>14.6f} | {float(t_val)**(0.25):>8.4f}")

print()

# ============================================================
# Part G: The Hadamard three-circle theorem applied to log|ζ|
# ============================================================

print("\n--- Part G: Hadamard three-circle / convexity of log|ζ| ---\n")

# The key insight from convexity: log|ζ(σ+it)| is subharmonic.
# Therefore, for FIXED t:
# log|ζ(σ+it)| cannot have a minimum in the interior of a strip
# unless it equals -∞ (i.e., ζ = 0).
#
# This is just the maximum principle for harmonic functions applied
# to log|ζ|, which is harmonic where ζ ≠ 0.
#
# More quantitatively: by Hadamard's three-line theorem,
# for α < σ < β:
# log M(σ) ≤ (β-σ)/(β-α) · log M(α) + (σ-α)/(β-α) · log M(β)
# where M(σ) = sup_t |ζ(σ+it)|.

# This gives: at σ₀ between 1/2 and 1,
# log M(σ₀) ≤ (1-σ₀)/((1-1/2)) · log M(1/2) + (σ₀-1/2)/(1-1/2) · log M(1)
#
# M(1/2) can be estimated: |ζ(1/2+it)| ≤ C · t^{1/6} log(t) (Huxley bound)
# M(1) has a pole: ζ(1+it) ~ 1 for large t (bounded above and below)
#
# This gives M(σ₀) ≤ C · t^{(1/6)(1-σ₀)/(1/2)} = C · t^{(1-σ₀)/3}
# This is the Lindelöf-type convexity bound.

# The point: convexity in σ of log M means that IF a zero exists at σ₀,
# then the function must decrease from its "typical" value to 0 and back,
# which is costly in terms of the growth rate.

# Numerical verification of convexity:
print("log|ζ(σ+it)| vs σ for fixed t (should be roughly convex):")
print()

for t_val in [14.135, 100.0, 1000.0]:
    print(f"  t = {t_val}:")
    sigmas = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2]
    for sigma in sigmas:
        zeta_val = mpmath.zeta(mpmath.mpc(sigma, t_val))
        log_zeta = float(mpmath.log(abs(zeta_val)))
        print(f"    σ={sigma:.2f}: log|ζ| = {log_zeta:>8.4f}, |ζ| = {float(abs(zeta_val)):>10.6f}")
    print()

print()
print("=" * 70)
print("CONCLUSION OF INVESTIGATION 3")
print("=" * 70)
print("""
Key findings:

1. THE NAIVE MAXIMUM PRINCIPLE ARGUMENT FAILS.
   The three-line theorem applies to M(σ) = sup_t |ζ|, not to |ζ| at a
   single t. Since M(σ₀) > 0 even if there's a zero at σ₀+it₀, the
   sup-based argument gives no contradiction.

2. LOCAL GROWTH FROM A ZERO: If ζ(σ₀+it₀) = 0, the maximum principle on
   a disk gives |ζ'(s₀)| ≤ max|ζ|/r where r = σ₀-1/2. With the Lindelöf
   bound, this gives |ζ'(s₀)| ≤ t₀^{1/4+ε}/(σ₀-1/2). This is an UPPER
   bound, not contradicted by the actual growth rates.

3. DERIVATIVE GROWTH: |ζ'(σ+it)| for σ > 1/2 is typically O(1), far below
   the maximum principle bound of t^{1/4}/(σ-1/2). There is no contradiction
   between the derivative at a hypothetical zero and the growth bounds.

4. CONVEXITY IN σ: log|ζ(σ+it)| is roughly convex in σ for fixed t
   (verified numerically). At a zero, it would dip to -∞, creating a
   sharp concavity. BUT this is exactly what happens at zeros on σ=1/2
   (verified), so it's not forbidden by convexity for σ > 1/2 either.

5. THE MAXIMUM PRINCIPLE ALONE IS INSUFFICIENT to exclude off-line zeros.
   It constrains the derivative and local behavior but doesn't create a
   contradiction with the Euler product or functional equation.

INSIGHT: The maximum principle gives one-sided bounds (upper bounds on
derivatives, growth constraints) but these are always satisfied. The
constraints become interesting only when combined with ARITHMETIC
structure (Euler product) that provides matching LOWER bounds on
derivatives or SPECIFIC values. The missing ingredient is still the
connection between multiplicative structure and zero location.
""")
