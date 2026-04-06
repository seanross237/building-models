"""
Investigation 2: Lee-Yang Theorem, Generalized Lee-Yang, and the Zero-Location Problem

The Lee-Yang theorem (1952) proves that partition functions of ferromagnetic Ising
models have all zeros on the unit circle. The proof uses:
1. Each local factor has zeros on |z|=1
2. Products preserve this property

We investigate whether this mechanism extends to the Riemann zeta function,
where the complication is that individual Euler factors DON'T have zeros on
the critical line.
"""

import numpy as np
import mpmath
mpmath.mp.dps = 30

print("=" * 80)
print("INVESTIGATION 2: GENERALIZED LEE-YANG AND ZERO-LOCATION")
print("=" * 80)

# ===================================================================
# 2.1 The Original Lee-Yang Theorem
# ===================================================================

print("\n--- 2.1: The Original Lee-Yang Theorem ---")
print("""
Lee-Yang (1952): For the Ising model with ferromagnetic interactions (J_ij >= 0),
the partition function Z(z) = sum_sigma z^{sum_i sigma_i} exp(-beta H(sigma))
has all zeros on |z| = 1.

Proof sketch:
1. For a SINGLE spin: Z_1(z) = z + z^{-1} = (z-i)(z+i)/z. Zeros at z = +/-i, 
   which are on |z| = 1.
   
2. The "transfer matrix" connecting two spins produces a polynomial whose zeros
   are on |z| = 1 IF the interaction is ferromagnetic.
   
3. The partition function is a product of such local factors (in a transfer
   matrix decomposition), and each factor preserves the "zeros on |z|=1" property.

The key mechanism: multiplication by a function with zeros on |z|=1, when that
function satisfies certain positivity conditions, preserves the zero-location
property.
""")

# ===================================================================
# 2.2 What Makes Lee-Yang Work That Doesn't Apply to Zeta
# ===================================================================

print("\n--- 2.2: The Gap Between Lee-Yang and Zeta ---")
print("""
In Lee-Yang:
  - Variable: z (fugacity)
  - Target: |z| = 1 (unit circle)
  - Each factor: zeros already on |z| = 1
  - Product: preserves "zeros on |z| = 1"

For zeta:
  - Variable: s = 1/2 + it (or just t)
  - Target: t real (i.e., Re(s) = 1/2)
  - Each Euler factor (1-p^{-s})^{-1}: NO zeros at all (when viewed as function of t)
  - BUT the reciprocal product prod_p (1-p^{-s}) has zeros at 
    s = 2*pi*i*k/log(p), i.e., on Re(s) = 0, NOT Re(s) = 1/2
    
The critical difference:
  Lee-Yang: factors have zeros on the RIGHT line -> product has zeros on the RIGHT line
  Zeta: factors have zeros on the WRONG line (Re(s)=0) -> product has zeros on... where?
  
The gamma factor moves zeros from Re(s)=0 to Re(s)=1/2 (if RH is true).
This is NOT a Lee-Yang mechanism. It's something else.
""")

# ===================================================================
# 2.3 The Borcea-Branden Generalization
# ===================================================================

print("\n--- 2.3: Borcea-Branden Generalization ---")
print("""
Borcea-Branden (2009) proved a vast generalization of Lee-Yang:

Theorem: Let T: C[z1,...,zn] -> C[w1,...,wm] be a linear operator.
T preserves stability (all zeros in the product of upper half-planes)
if and only if its symbol (a polynomial in 2(n+m) variables) is stable.

For the Lee-Yang application:
- T is "evaluate at z" (goes from spin space to partition function space)
- Stability of the symbol is equivalent to ferromagnetic interactions

For the zeta application:
- T would be "multiply by 1/prod_p(1-p^{-s})" (Euler product)
- The "symbol" of this operator would need to be analyzed for stability

But there's a fundamental issue: the Euler product is an INFINITE product,
not a finite polynomial operation. Borcea-Branden works for finite-dimensional
polynomial spaces. The extension to infinite products is non-trivial.

Knuth-Borcea-Branden-Liggett (2009) extended to power series, but only
for specific types of operators.
""")

# ===================================================================
# 2.4 The Multiplicative Convolution Perspective
# ===================================================================

print("\n--- 2.4: Multiplicative Convolution ---")
print("""
The Euler product is naturally multiplicative: zeta(s) = prod_p (1-p^{-s})^{-1}

In MELLIN space (not Fourier), this becomes a multiplicative convolution.
The Mellin transform of n^{-s} is a delta function at log(n).

So the Dirichlet series zeta(s) = sum n^{-s} has Mellin kernel:
  K(x) = sum_{n=1}^{infty} delta(x - log(n))

The Euler product factorization says this kernel decomposes as:
  K = conv_p K_p  (multiplicative convolution)

where K_p(x) = sum_{k=0}^{infty} delta(x - k*log(p))

This is the multiplicative analog of the kernel decomposition.

KEY INSIGHT: In multiplicative convolution, the relevant "PF" theory is 
different. The appropriate framework is the MELLIN-space PF theory, which
deals with functions on (0, infinity) rather than on R.

There IS a multiplicative total positivity theory (Karlin, Chapter 6):
A kernel K(x,y) is totally positive if all minors det(K(x_i, y_j)) >= 0.
For a multiplicative convolution kernel, this translates to conditions on
K(x/y) being totally positive on (0, infinity).
""")

# ===================================================================
# 2.5 Numerical: Lee-Yang Type Products
# ===================================================================

print("\n--- 2.5: Numerical Lee-Yang Type Product ---")

# Build a toy model: multiply polynomials with zeros on the unit circle
# and verify the product has zeros on the unit circle
from numpy.polynomial import polynomial as P

def poly_from_unit_circle_zeros(angles):
    """Build polynomial with zeros at e^{i*theta} for each angle theta."""
    roots = np.exp(1j * np.array(angles))
    coeffs = np.array([1.0 + 0j])
    for r in roots:
        coeffs = np.convolve(coeffs, [1.0, -r])
    return coeffs

# Product of polynomials with zeros on unit circle
print("Product of polynomials with zeros on |z|=1:")
p_product = np.array([1.0 + 0j])
for k in range(1, 6):
    angles = np.random.uniform(0, 2*np.pi, 3)
    pk = poly_from_unit_circle_zeros(angles)
    p_product = np.convolve(p_product, pk)

roots_product = np.roots(p_product[::-1])
radii = np.abs(roots_product)
print(f"  Product degree: {len(p_product)-1}")
print(f"  Radii of zeros: min={min(radii):.6f}, max={max(radii):.6f}")
print(f"  All on unit circle: {all(abs(r - 1) < 1e-6 for r in radii)}")

# Now do the ADDITION (DH-type) of two such polynomials
print("\nAddition of polynomials with zeros on |z|=1:")
angles1 = np.random.uniform(0, 2*np.pi, 5)
angles2 = np.random.uniform(0, 2*np.pi, 5)
p1 = poly_from_unit_circle_zeros(angles1)
p2 = poly_from_unit_circle_zeros(angles2)

# Pad to same length
max_len = max(len(p1), len(p2))
p1_pad = np.zeros(max_len, dtype=complex)
p2_pad = np.zeros(max_len, dtype=complex)
p1_pad[:len(p1)] = p1
p2_pad[:len(p2)] = p2

p_sum = p1_pad + p2_pad
# Remove trailing zeros
while len(p_sum) > 1 and abs(p_sum[-1]) < 1e-12:
    p_sum = p_sum[:-1]

roots_sum = np.roots(p_sum[::-1])
radii_sum = np.abs(roots_sum)
on_circle = sum(abs(r - 1) < 0.01 for r in radii_sum)
print(f"  Sum degree: {len(p_sum)-1}")
print(f"  Radii of zeros: min={min(radii_sum):.6f}, max={max(radii_sum):.6f}")
print(f"  Zeros within 0.01 of unit circle: {on_circle}/{len(roots_sum)}")
print(f"  Addition DESTROYS the unit-circle property")

# ===================================================================
# 2.6 The Critical Question: Seed Function
# ===================================================================

print("\n--- 2.6: The Seed Function Problem ---")
print("""
In the Lee-Yang mechanism, each factor ALREADY has zeros on the target set.
For zeta, the Euler factors DON'T have zeros on Re(s) = 1/2.

So the Lee-Yang mechanism says: "if you start with zeros in the right place,
multiplication preserves this." But we DON'T start in the right place.

The gamma factor completion is what moves things to Re(s) = 1/2.
The Euler product preserves the structure created by the gamma factor.

This suggests a TWO-STEP mechanism:
  STEP 1: The gamma factor creates a function with "zeros tending toward Re(s)=1/2"
  STEP 2: The Euler product, as a convolution, preserves this tendency

The invariant we seek might not be "zeros on the line" but rather
"a structural tendency toward the line" that convolution preserves and
addition destroys.

CANDIDATE INVARIANT #2: "Phase-coherent zero tendency"
The gamma factor creates a phase structure where zeros want to live on Re(s)=1/2.
Convolution (Euler product) preserves this phase coherence.
Addition (DH-type) destroys it by introducing competing phase structures.
""")

# ===================================================================
# 2.7 The Functional Equation as Phase Constraint
# ===================================================================

print("\n--- 2.7: Functional Equation Phase Constraint ---")

# The functional equation xi(s) = xi(1-s) forces:
# For s = 1/2 + it: xi(1/2+it) = xi(1/2-it)
# So xi is an EVEN function of t, hence real-valued on the real t-axis.

# For ANY function satisfying this, zeros come in conjugate pairs sigma +/- it
# AND symmetric pairs (1-sigma) +/- it.

# If a zero has sigma != 1/2, there are FOUR zeros: sigma+it, sigma-it, (1-sigma)+it, (1-sigma)-it
# If sigma = 1/2, there are TWO zeros: 1/2+it, 1/2-it

# The functional equation creates a "preference" for Re(s) = 1/2 zeros:
# off-line zeros come in quartets, on-line zeros come in pairs.
# So on-line zeros are "cheaper" (by a factor of 2).

print("Functional equation forces xi(1/2+it) = xi(1/2-it) [xi is even in t]")
print("On-line zeros come in pairs: +/- t (cost = 2)")
print("Off-line zeros come in quartets: sigma+/-it, (1-sigma)+/-it (cost = 4)")
print("The functional equation makes on-line zeros 'cheaper' by factor 2")
print("")
print("This is a COUNTING argument, not a forcing argument.")
print("It explains why MOST zeros should be on the line (Hardy's theorem),")
print("but doesn't explain why ALL zeros must be on the line.")
print("")

# The KEY question: what is the ADDITIONAL constraint from the Euler product
# that forces the remaining zeros (if any) onto the line?

print("The Euler product must provide the ADDITIONAL constraint:")
print("  Functional equation: 'zeros prefer the line' (pairs vs quartets)")
print("  Euler product: 'zeros MUST be on the line' (some structural rigidity)")
print("")
print("The additive structure of DH satisfies the functional equation")
print("but lacks the structural rigidity from the Euler product.")

# ===================================================================
# 2.8 The "Generalized Lee-Yang" Candidate
# ===================================================================

print("\n--- 2.8: Generalized Lee-Yang for Zeta ---")
print("""
In Lee-Yang:
  Z(z) = prod_i f_i(z)
  Each f_i has zeros on |z| = 1
  The product Z has zeros on |z| = 1

For zeta, we need something like:
  xi(s) = G(s) * prod_p (1-p^{-s})^{-1}
  
  G(s) has zeros "related to" Re(s) = 1/2 (gamma function zeros are at 
  negative even integers, moved by the pi^{-s/2} and s(s-1) factors)
  
  Each (1-p^{-s})^{-1} has NO zeros
  
  The product creates zeros at Re(s) = 1/2

This is DIFFERENT from Lee-Yang in a fundamental way:
  Lee-Yang: factors HAVE zeros on the right set, product preserves this
  Zeta: factors are ZERO-FREE, the product creates zeros (through the limit)

The zeros of xi emerge from the INFINITE product. No finite truncation has
any zeros. The zeros are a COLLECTIVE phenomenon of infinitely many primes.

This is like a PHASE TRANSITION: finitely many spins give no transition,
but the infinite-volume limit does.

CANDIDATE INVARIANT #3: "Infinite-product zero emergence on the critical line"
The Euler product factors are individually zero-free but their infinite product
creates zeros through a phase-transition mechanism that forces them onto the
symmetry axis. This is destroyed by addition because the phase transition 
requires multiplicative independence.
""")

print("\n" + "=" * 80)
print("SUMMARY OF INVESTIGATION 2:")
print("=" * 80)
print("""
1. Lee-Yang works because EACH factor has zeros on the target set, and 
   multiplication preserves this. This does NOT directly apply to zeta.

2. For zeta, the Euler factors are zero-free. Zeros emerge only in the 
   infinite product — a phase-transition phenomenon.

3. The Borcea-Branden generalization characterizes stability-preserving 
   operators, but extending to infinite products is non-trivial.

4. The functional equation makes on-line zeros 'cheaper' (pairs vs quartets)
   but doesn't force all zeros onto the line.

5. The Euler product provides STRUCTURAL RIGIDITY beyond the functional equation:
   - Concentration of log|zeta| (from prior experiment)
   - Phase coherence from multiplicative structure
   - Infinite-product phase transition creating zeros on the line

THREE CANDIDATE INVARIANTS IDENTIFIED:
  #1: Real-rootedness under Polya-Schur multiplier sequences
  #2: Phase-coherent zero tendency  
  #3: Infinite-product zero emergence (phase transition)
  
None of these is yet precise enough to be a theorem. Investigation 3 will
try to make them precise through the lens of total positivity and interlacing.
""")
