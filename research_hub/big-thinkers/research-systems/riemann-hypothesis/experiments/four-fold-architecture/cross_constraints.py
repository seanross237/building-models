"""
Cross-Constraint Analysis: What Does the CONJUNCTION of Four Properties Exclude?

Key finding from alpha_exponent.py: The alpha exponent is >> 2 at all sigma > 1/2.
This means the simple "Bohr-Jessen tail excludes zeros" argument FAILS.

So we need a more refined analysis. This script investigates:

1. The CORRELATION between small values at sigma and small values at 1-sigma
   (the functional equation forces them to coincide at the same t)

2. The "conditional alpha": given that |zeta(sigma+it)| is small, what is the
   conditional distribution of |zeta((1-sigma)+it)|?

3. The PF constraint: how does the spacing of on-line zeros constrain the
   possibility of off-line zeros?

4. The "dual" argument: instead of asking "can |zeta| be small at sigma > 1/2",
   ask "can the derivative zeta'(rho) be compatible with all four constraints?"

The key insight we are checking:
  The functional equation says zeta(s) = chi(s) * zeta(1-s).
  If zeta(sigma_0 + it_0) = 0, then zeta((1-sigma_0)+it_0) = 0.

  But the VALUE of zeta' at the paired zeros must satisfy:
  zeta'(sigma_0+it_0) = chi(sigma_0+it_0) * zeta'((1-sigma_0)+it_0) + chi'(sigma_0+it_0) * 0

  Wait, differentiating zeta(s) = chi(s)*zeta(1-s):
  zeta'(s) = chi'(s)*zeta(1-s) + chi(s)*(-zeta'(1-s))

  At s = sigma_0+it_0 where zeta(s) = zeta(1-s) = 0:
  zeta'(sigma_0+it_0) = chi'(sigma_0+it_0)*0 + chi(sigma_0+it_0)*(-zeta'((1-sigma_0)+it_0))
  zeta'(sigma_0+it_0) = -chi(sigma_0+it_0) * zeta'((1-sigma_0)+it_0)

  So: |zeta'(sigma_0+it_0)| = |chi(sigma_0+it_0)| * |zeta'((1-sigma_0)+it_0)|

  And |chi(sigma_0+it_0)| ~ (t_0/2pi)^{1/2-sigma_0} for large t_0.

  Since sigma_0 > 1/2, |chi| < 1, so:
  |zeta'(sigma_0+it_0)| < |zeta'((1-sigma_0)+it_0)|

  The derivative at the zero on the right side of the strip is SMALLER than
  the derivative at the paired zero on the left side. This means the zero
  at sigma_0 is "wider" (flatter) than the zero at 1-sigma_0.

  But the zero DENSITY at sigma_0 is supposed to be LOWER than at 1-sigma_0
  (by the zero density estimates). Having wider zeros at lower density and
  narrower zeros at higher density seems geometrically contradictory...
  unless the zeros on both sides are extremely rare.
"""

import numpy as np
from mpmath import mp, zeta, zetazero, diff, gamma as mpgamma, pi as mppi, log, fabs, power, sin
import time

mp.dps = 25

def chi_function(s):
    """chi(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s)"""
    return power(2, s) * power(mppi, s - 1) * sin(mppi * s / 2) * mpgamma(1 - s)

def analyze_derivative_constraint():
    """
    At each known zero rho_n = 1/2 + i*gamma_n on the critical line,
    compute |zeta'(rho_n)| and |chi(sigma+i*gamma_n)| for various sigma.

    If an off-line zero existed at sigma_0 + i*t_0, the derivative relation
    |zeta'(sigma_0+it_0)| = |chi(sigma_0+it_0)| * |zeta'((1-sigma_0)+it_0)|
    must hold. We check what this implies.
    """
    print("=" * 70)
    print("DERIVATIVE CONSTRAINT AT HYPOTHETICAL OFF-LINE ZEROS")
    print("=" * 70)

    # Get first several zeros
    n_zeros = 20
    zeros = []
    for n in range(1, n_zeros + 1):
        z = zetazero(n)
        zeros.append(float(z.imag))

    print(f"\n  Analysis at the first {n_zeros} zeta zeros:")
    print(f"  Each zero rho_n = 1/2 + i*gamma_n is on the critical line.")
    print(f"  We compute |zeta'(rho_n)| and check the chi-factor at sigma != 1/2.\n")

    print(f"  {'n':<4} {'gamma_n':<10} {'|zeta_prime|':<14} "
          f"{'|chi(0.6+ig)|':<14} {'|chi(0.7+ig)|':<14} {'|chi(0.8+ig)|':<14}")

    for n, gamma_n in enumerate(zeros, 1):
        s = 0.5 + 1j * gamma_n
        # Compute zeta'(rho_n) numerically
        zp = diff(zeta, s)
        abs_zp = float(fabs(zp))

        # Compute |chi| at various sigma
        chi_vals = {}
        for sigma in [0.6, 0.7, 0.8]:
            try:
                c = chi_function(sigma + 1j * gamma_n)
                chi_vals[sigma] = float(fabs(c))
            except:
                # Use asymptotic formula
                chi_vals[sigma] = (gamma_n / (2 * np.pi)) ** (0.5 - sigma)

        print(f"  {n:<4} {gamma_n:<10.4f} {abs_zp:<14.6f} "
              f"{chi_vals[0.6]:<14.6f} {chi_vals[0.7]:<14.6f} {chi_vals[0.8]:<14.6f}")

    # Now analyze: for a hypothetical off-line zero at sigma_0 + it_0,
    # what would the derivative need to be?
    print(f"\n\n  IMPLICATION FOR HYPOTHETICAL OFF-LINE ZEROS:")
    print(f"  If rho = sigma_0 + it_0 is a zero with sigma_0 > 1/2:")
    print(f"  |zeta'(sigma_0+it_0)| = |chi(sigma_0+it_0)| * |zeta'((1-sigma_0)+it_0)|")
    print(f"  Since |chi(sigma+it)| ~ (t/2pi)^{{1/2-sigma}}, we need:")
    print(f"")

    for t_0 in [100, 1000, 10000, 100000]:
        print(f"  t_0 = {t_0}:")
        for sigma_0 in [0.6, 0.7, 0.8]:
            chi_abs = (t_0 / (2 * np.pi)) ** (0.5 - sigma_0)
            print(f"    sigma_0={sigma_0}: |chi| = {chi_abs:.6f}, "
                  f"so |zeta'(sig_0)| = {chi_abs:.6f} * |zeta'(1-sig_0)|")
            print(f"                     The right-half zero has derivative "
                  f"{1/chi_abs:.2f}x SMALLER than the left-half zero")
        print()

def analyze_zero_spacing_constraint():
    """
    PF_4 constrains zero spacing. Compute the actual spacing of critical-line
    zeros and check what constraints PF_4 would impose on off-line zeros.

    For a PF_2 function, zeros are real and simple. PF_4 adds interlacing
    constraints between zeros. Specifically, for the Xi function:
    Xi(z) = product over zeros: (1 - z/rho_n)

    The zeros must satisfy the total positivity conditions encoded in
    the Toeplitz minors of the Fourier transform.
    """
    print("\n" + "=" * 70)
    print("ZERO SPACING AND PF CONSTRAINTS")
    print("=" * 70)

    # Get the first 50 zeros and compute their spacing
    n_zeros = 50
    gammas = []
    for n in range(1, n_zeros + 1):
        z = zetazero(n)
        gammas.append(float(z.imag))

    gammas = np.array(gammas)
    spacings = np.diff(gammas)

    # Normalize spacings by the mean density: d_n ~ 2*pi/log(gamma_n/(2pi))
    mean_spacings = 2 * np.pi / np.log(gammas[:-1] / (2 * np.pi))
    normalized_spacings = spacings / mean_spacings

    print(f"\n  Critical line zero spacings (first {n_zeros} zeros):")
    print(f"  Mean spacing: {np.mean(spacings):.4f}")
    print(f"  Std spacing:  {np.std(spacings):.4f}")
    print(f"  Min spacing:  {np.min(spacings):.4f}")
    print(f"  Max spacing:  {np.max(spacings):.4f}")
    print(f"\n  Normalized spacings (by local mean density):")
    print(f"  Mean: {np.mean(normalized_spacings):.4f}")
    print(f"  Std:  {np.std(normalized_spacings):.4f}")
    print(f"  Min:  {np.min(normalized_spacings):.4f}")
    print(f"  Max:  {np.max(normalized_spacings):.4f}")

    # GUE prediction for the nearest-neighbor spacing distribution
    # p(s) = (32/pi^2) * s^2 * exp(-4s^2/pi)
    s_vals = normalized_spacings
    print(f"\n  GUE level repulsion check:")
    print(f"  P(normalized spacing < 0.5) = {np.mean(s_vals < 0.5):.4f} "
          f"(GUE prediction: ~0.11)")
    print(f"  P(normalized spacing < 0.3) = {np.mean(s_vals < 0.3):.4f} "
          f"(GUE prediction: ~0.02)")
    print(f"  P(normalized spacing < 0.1) = {np.mean(s_vals < 0.1):.4f} "
          f"(GUE prediction: ~0.0003)")

    # Key PF constraint: if Xi has PF_2k properties, then the zeros
    # satisfy certain interlacing conditions. For PF_2, zeros are real and simple.
    # For PF_4, additionally, the zeros of Xi and Xi'' interlace.

    # Compute Xi'' zeros (approximately) by numerical differentiation
    print(f"\n  PF_4 interlacing check: zeros of Xi and Xi'' should interlace")
    print(f"  (This means between any two consecutive Xi-zeros, there is exactly one Xi''-zero)")

    # We'll check this by evaluating Xi'' at the midpoints between zeros
    # Xi(z) relates to zeta: Xi(z) = (1/2) * s(s-1) * pi^{-s/2} * Gamma(s/2) * zeta(s)
    # where s = 1/2 + iz

    def xi_func(z_val):
        """Compute Xi(z) = (1/2) * s*(s-1) * pi^(-s/2) * Gamma(s/2) * zeta(s)
        where s = 1/2 + i*z"""
        s = 0.5 + 1j * z_val
        return float((0.5 * s * (s - 1) * power(mppi, -s/2) * mpgamma(s/2) * zeta(s)).real)

    midpoints = (gammas[:-1] + gammas[1:]) / 2

    xi_double_prime_signs = []
    for mid in midpoints[:20]:  # check first 20 gaps
        # Evaluate Xi'' at the midpoint (z = mid on real axis -> s = 1/2 + i*mid)
        z_val = float(mid)
        # Use central difference for Xi''(z)
        h = 0.001
        xi_plus = xi_func(z_val + h)
        xi_mid = xi_func(z_val)
        xi_minus = xi_func(z_val - h)
        xi_pp = (xi_plus - 2*xi_mid + xi_minus) / h**2
        xi_double_prime_signs.append(np.sign(xi_pp))

    sign_changes = sum(1 for i in range(len(xi_double_prime_signs)-1)
                       if xi_double_prime_signs[i] != xi_double_prime_signs[i+1])

    print(f"  Xi'' signs at midpoints: {['+'if s>0 else '-' for s in xi_double_prime_signs]}")
    print(f"  Sign changes: {sign_changes} (should be ~{len(xi_double_prime_signs)-1} for interlacing)")

    if sign_changes == len(xi_double_prime_signs) - 1:
        print(f"  >>> PERFECT interlacing: consistent with PF_4")
    else:
        print(f"  >>> {sign_changes}/{len(xi_double_prime_signs)-1} interlacing pairs")

def analyze_off_line_density_constraint():
    """
    THE KEY CROSS-CONSTRAINT:

    At sigma_0 > 1/2, the density of zeros is N(sigma_0, T) = O(T^{A(sigma_0)}).
    At 1-sigma_0 < 1/2, the paired zeros have the SAME density.

    But at 1-sigma_0, the "natural" zero density from the functional equation
    transform of the on-line zeros is N(1/2, T) ~ (T/2pi)*log(T/2pi).

    An off-line zero at sigma_0 is "extra" -- it's not part of the critical-line count.
    It must be paired with a zero at 1-sigma_0 that is ALSO "extra" (not on the line).

    The question: in the vicinity of the critical line, how "crowded" are the
    zeros? Is there room for extra zeros off the line without violating the
    PF/GUE spacing constraints?

    We investigate the local zero structure near the critical line.
    """
    print("\n" + "=" * 70)
    print("OFF-LINE ZERO DENSITY: ROOM FOR EXTRA ZEROS?")
    print("=" * 70)

    # The argument from GUE repulsion:
    # On the critical line, zeros have GUE-type level repulsion: p(s) ~ s^2 for small s.
    # This means very close zeros are extremely rare.
    #
    # An off-line zero at sigma_0 + it_0 would affect the critical-line zeros
    # in its vicinity (by the argument principle, a zero near the line
    # "perturbs" nearby on-line zeros).

    # Compute the local zero density and check how an off-line zero would
    # affect it.

    # Get zeros near a specific height
    T_target = 1000
    n_zeros_to_get = 200

    print(f"\n  Computing zeros near T = {T_target}...")

    # Get zeros near T_target
    gammas = []
    for n in range(1, n_zeros_to_get + 1):
        z = zetazero(n)
        g = float(z.imag)
        gammas.append(g)
        if g > T_target + 50:
            break

    gammas = np.array(gammas)

    # Focus on zeros near T_target
    near_mask = np.abs(gammas - T_target) < 50
    gammas_near = gammas[near_mask]

    print(f"  Found {len(gammas_near)} zeros within 50 of T={T_target}")

    if len(gammas_near) > 1:
        spacings = np.diff(gammas_near)
        local_density = 1.0 / np.mean(spacings)
        predicted_density = np.log(T_target / (2*np.pi)) / (2*np.pi)

        print(f"  Local density: {local_density:.4f} zeros/unit")
        print(f"  Predicted density: {predicted_density:.4f} zeros/unit")
        print(f"  Ratio: {local_density/predicted_density:.3f}")
        print(f"  Mean spacing: {np.mean(spacings):.4f}")
        print(f"  Min spacing:  {np.min(spacings):.4f}")

        # The "room" for an off-line zero:
        # An off-line zero at sigma_0 + i*t_0 would, by the argument principle,
        # be counted in the zero-counting function. The on-line zeros near t_0
        # would need to "make room" for the extra zero.

        # The average spacing is ~ 2*pi/log(T/(2pi)). For an extra zero to
        # fit, it would need to "compress" nearby spacings by a factor of
        # N/(N+1) where N is the number of on-line zeros in the vicinity.

        # But GUE repulsion means the spacing distribution has p(0) = 0
        # (level repulsion). This means there's a "minimum effective spacing"
        # that makes it hard to add extra zeros.

        print(f"\n  GUE REPULSION ARGUMENT:")
        print(f"  The mean spacing at T=1000 is {np.mean(spacings):.4f}")
        print(f"  If an extra zero were at sigma_0 + i*t_0, with t_0 near one of")
        print(f"  the critical line zeros, the argument principle would require")
        print(f"  the nearby on-line zeros to shift to accommodate it.")
        print(f"  But GUE repulsion constrains how close zeros can get.")
        print(f"  The probability of two zeros being within delta is ~ delta^2")
        print(f"  (quadratic level repulsion).")

def analyze_moment_constraint():
    """
    From the Keating-Snaith conjecture:
    E[|zeta(1/2+it)|^{2k}] ~ C(k) * (log T)^{k^2}

    At sigma > 1/2:
    E[|zeta(sigma+it)|^{2k}] ~ D(k, sigma) (bounded)

    The NEGATIVE moments are also important:
    E[|zeta(sigma+it)|^{-2k}] controls the zero density.

    If E[|zeta|^{-2k}] is finite for some k, then the zero density is bounded
    by the moment method.

    Specifically: by Markov inequality,
    P(|zeta(sigma+it)| < epsilon) <= epsilon^{2k} * E[|zeta(sigma+it)|^{-2k}]

    If E[|zeta|^{-2k}] < infinity for sigma > 1/2, then:
    P(|zeta| < epsilon) = O(epsilon^{2k}) for any k

    This would give alpha = infinity (faster than any power), which is much
    stronger than alpha < 2.

    The question: what is E[|zeta(sigma+it)|^{-2k}] for sigma > 1/2?
    """
    print("\n" + "=" * 70)
    print("NEGATIVE MOMENTS AND ZERO DENSITY")
    print("=" * 70)

    print("\n  Computing E[|zeta(sigma+it)|^{-2k}] for sigma > 1/2\n")

    np.random.seed(42)
    T_center = 5000
    n_samples = 500

    t_values = T_center + np.random.uniform(-T_center/4, T_center/4, n_samples)
    t_values = t_values[t_values > 14.5]

    sigmas = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 1.00]
    ks = [0.5, 1.0, 1.5, 2.0, 3.0]

    print(f"  {'sigma':<8}", end="")
    for k in ks:
        print(f"{'E[|z|^-'+str(2*k)+']':<16}", end="")
    print()

    for sigma in sigmas:
        abs_vals = []
        for t in t_values:
            z = zeta(sigma + 1j * float(t))
            abs_vals.append(float(fabs(z)))
        abs_vals = np.array(abs_vals)

        print(f"  {sigma:<8.2f}", end="")
        for k in ks:
            neg_moment = np.mean(abs_vals ** (-2*k))
            print(f"{neg_moment:<16.4f}", end="")
        print()

    print(f"\n  INTERPRETATION:")
    print(f"  If E[|zeta|^{{-2k}}] is FINITE for sigma > 1/2 and all k,")
    print(f"  then P(|zeta| < eps) decays faster than any power of eps.")
    print(f"  This means the alpha exponent is effectively INFINITY,")
    print(f"  which is much stronger than our direct estimates.")
    print(f"\n  However, the negative moments from sampling are unreliable")
    print(f"  because they are dominated by the SMALLEST sampled values.")
    print(f"  The true negative moments may be infinite if the Bohr-Jessen")
    print(f"  distribution has P(|zeta| = 0) > 0 for sigma > 1/2.")
    print(f"  (But meromorphy forces isolated zeros, so P = 0.)")

def analyze_the_key_obstruction():
    """
    THE FUNDAMENTAL OBSTRUCTION TO THE FOUR-FOLD ARCHITECTURE

    The deepest issue is:

    1. Each of the four properties constrains zeta STATISTICALLY or LOCALLY.
    2. RH is a GLOBAL, DETERMINISTIC statement.
    3. The gap between statistical/local and global/deterministic is
       precisely the gap that every existing approach fails to close.

    The four-fold conjunction narrows the gap but does not close it because:

    - The functional equation is a global analytic identity -> but it just
      pairs zeros, doesn't exclude them
    - The Bohr-Jessen phase boundary is a statistical statement about the
      VALUE DISTRIBUTION -> it says zeros are "rare" not "impossible"
    - The GMC structure is a distributional statement -> it describes
      typical behavior, not specific points
    - The PF property is a constraint on the kernel/spectral structure ->
      it constrains but doesn't determine the zero set

    THE HONEST ASSESSMENT: The conjunction of four properties makes off-line
    zeros IMPLAUSIBLE (they would need to satisfy multiple conflicting
    constraints simultaneously) but does not make them IMPOSSIBLE.

    WHAT WOULD CLOSE THE GAP:

    Option 1: A RIGIDITY theorem. Show that the functional equation +
    PF_4 + Euler product jointly determine the zero set uniquely. This
    is essentially the inverse spectral problem: given these three constraints,
    is the zero set uniquely determined?

    Option 2: A QUANTITATIVE exclusion. Show that the probability of
    an off-line zero, as constrained by all four properties, is literally
    zero (not just very small). This requires an EXACT statement, not
    an asymptotic one.

    Option 3: A CONTRAPOSITIVE. Assume an off-line zero exists, and derive
    a contradiction with one of the PROVEN properties (not conjectured ones).
    This is the classical approach, but we need to use ALL four properties
    in the derivation.
    """
    print("\n" + "=" * 70)
    print("THE FUNDAMENTAL OBSTRUCTION AND PATH FORWARD")
    print("=" * 70)

    print("""
  SUMMARY OF CROSS-CONSTRAINTS ON A HYPOTHETICAL OFF-LINE ZERO:

  Suppose rho = sigma_0 + it_0 is a zero with sigma_0 > 1/2.

  CONSTRAINT                     | WHAT IT REQUIRES                | STATUS
  ============================================================================
  C1. Functional eqn pairing     | Zero also at (1-sigma_0)+it_0  | Proven
  C2. Bohr-Jessen at sigma_0     | log|zeta| has finite variance  | Proven
     -> alpha exponent            | alpha ~ 3-10 (> 2)             | COMPUTED: does NOT exclude
  C3. Supercritical GMC at 1-sig | Variance diverges, measure = 0 | Proven (qualitative)
  C4. PF_4 of kernel             | Zeros satisfy interlacing       | Likely (PF_4 not fully proved)
  C5. Derivative relation        | |zeta'(sig)| = |chi|*|zeta'(1-sig)| | Proven
     -> chi factor                | (t/2pi)^{1/2-sigma} < 1       | COMPUTED
  C6. Meromorphy                 | Zeros are isolated              | Proven
  C7. GUE repulsion              | On-line zeros have s^2 repulsion | Numerical (proven for GUE)

  THE CONJUNCTION:
  C1 + C5: The derivative at sigma_0 is SMALLER by factor (t/2pi)^{sigma_0-1/2}
           than at the paired zero. This means the zero at sigma_0 is "wide"
           and the zero at 1-sigma_0 is "narrow".

  C1 + C3: The paired zero at 1-sigma_0 lives in the supercritical regime.
           The GMC measure degenerates there. But this doesn't mean zeros
           can't exist -- it means the TYPICAL value of |zeta| grows to infinity.
           A zero is an exceptional event in an already exceptional landscape.

  C2 + C6: At sigma_0, the Bohr-Jessen distribution has finite variance and
           sub-Gaussian tails. But alpha > 2, so the zero-density argument
           alone does not exclude zeros.

  THE GAP:
  We cannot show the constraints are JOINTLY unsatisfiable. Each constraint
  restricts the class of possible off-line zeros, but we cannot prove the
  intersection of all constraint sets is empty.

  THE NEAREST APPROACH TO A PROOF:
  If we could establish that for sigma > 1/2:
  (a) The Bohr-Jessen distribution at sigma has density f(z) near z=0 with
      f(0) = 0 (the density vanishes at the origin), AND
  (b) The rate at which f(z) -> 0 as z -> 0 is fast enough that the
      "effective alpha" is > some threshold that conflicts with the
      functional equation derivative constraint (C5)...

  Then the conjunction would yield a proof. But (a) is unproven.
  The Bohr-Jessen density is known to be smooth (Jessen-Wintner), and
  its behavior near zero is NOT fully characterized.

  NOVEL REDUCTION:
  RH is equivalent to: "The Bohr-Jessen density function at every
  sigma > 1/2 vanishes at the origin faster than |z|^{A(sigma)-2},
  where A(sigma) is the Ingham-Huxley zero-density exponent."

  This is a WEAKER statement than RH but implies it. It translates RH
  into a purely probabilistic number theory question about the value
  distribution of the Euler product.
""")

def main():
    t0 = time.time()

    analyze_derivative_constraint()
    analyze_zero_spacing_constraint()
    analyze_moment_constraint()
    analyze_off_line_density_constraint()
    analyze_the_key_obstruction()

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")

if __name__ == "__main__":
    main()
