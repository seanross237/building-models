"""
02_correct_phi.py
=================
Establish the CORRECT form of the Polya kernel Phi(u).

The standard reference is Polya (1927) and de Bruijn (1950).

The Riemann xi function is:
    xi(s) = (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2)*zeta(s)

The function Xi(t) = xi(1/2 + it) is real and even for real t.

The Fourier representation is:
    Xi(t) = integral_{-inf}^{inf} Phi(u) e^{itu} du
          = 2 * integral_0^inf Phi(u) cos(tu) du     [since Phi is even]

The kernel Phi(u) is given by the Mellin-Barnes representation:

    Phi(u) = sum_{n=1}^inf (2*pi^2*n^4*exp(9u/2) - 3*pi*n^2*exp(5u/2)) * exp(-pi*n^2*exp(2u))

WAIT -- the issue is whether the formula uses (2*pi*n^4) or (2*pi^2*n^4).

Let me derive this from scratch.

The xi function:
    xi(s) = (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2)*zeta(s)

Using the Jacobi theta function theta(x) = sum_{n=-inf}^{inf} exp(-pi*n^2*x),
and psi(x) = sum_{n=1}^inf exp(-pi*n^2*x) = (theta(x)-1)/2,
we have:
    zeta(s) = pi^{s/2} / Gamma(s/2) * [1/(s(s-1)) + integral_1^inf (x^{s/2-1} + x^{(1-s)/2-1}) psi(x) dx]

The standard integral representation of xi(s):

    xi(s) = (1/2) - (s-1/2)^2 * integral_1^inf x^{-3/4} * psi'(sqrt(x)) * x^{???} dx

Let me use the KNOWN correct formula. From Edwards "Riemann's Zeta Function" or Titchmarsh:

    xi(s) = 4 * integral_1^inf d/dx[x^{3/2}*psi'(x)] * x^{-1/4} * cosh((s-1/2)/2 * log(x)) dx / x

Hmm, let me just compute Xi numerically from the zeta function and compare.

Author: Polya kernel log-concavity investigation
Date: 2026-04-04
"""

import mpmath
import json

mpmath.mp.dps = 50


def xi_from_zeta(s):
    """Compute xi(s) = (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2)*zeta(s)."""
    return mpmath.mpf(1)/2 * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)


def Xi_t(t):
    """Compute Xi(t) = xi(1/2 + it)."""
    s = mpmath.mpf(1)/2 + 1j * t
    val = xi_from_zeta(s)
    return mpmath.re(val)  # Should be real for real t


def phi_formula_v1(u, n_terms=50):
    """
    Version 1: Phi(u) = sum_{n=1}^inf (2*pi*n^4*exp(9u/2) - 3*pi*n^2*exp(5u/2)) * exp(-pi*n^2*exp(2u))

    This is the formula from the task description.
    """
    u = mpmath.mpf(u)
    pi = mpmath.pi
    total = mpmath.mpf(0)
    for n in range(1, n_terms + 1):
        n = mpmath.mpf(n)
        e2u = mpmath.exp(2*u)
        total += (2*pi*n**4*mpmath.exp(9*u/2) - 3*pi*n**2*mpmath.exp(5*u/2)) * mpmath.exp(-pi*n**2*e2u)
    return total


def phi_formula_v2(u, n_terms=50):
    """
    Version 2: The standard formula from de Bruijn / Edwards.

    Starting from:
    xi(s) = integral_0^inf [x^{s/2} + x^{(1-s)/2}] * f(x) dx/x

    where f(x) involves theta. After substitution x = e^{2u}:

    Xi(t) = 2 * integral_0^inf Phi(u) cos(tu) du

    Phi(u) = sum_{n=1}^inf (2*pi^2*n^4*exp(9u/2) - 3*pi*n^2*exp(5u/2)) * exp(-pi*n^2*exp(2u))

    Note the pi^2 in the first term!
    """
    u = mpmath.mpf(u)
    pi = mpmath.pi
    total = mpmath.mpf(0)
    for n in range(1, n_terms + 1):
        n = mpmath.mpf(n)
        e2u = mpmath.exp(2*u)
        total += (2*pi**2*n**4*mpmath.exp(9*u/2) - 3*pi*n**2*mpmath.exp(5*u/2)) * mpmath.exp(-pi*n**2*e2u)
    return total


def phi_formula_v3(u, n_terms=50):
    """
    Version 3: Derive from scratch using the standard representation.

    From Titchmarsh, "The Theory of the Riemann Zeta-Function":

    xi(s) = 1/2 + integral_1^inf psi(x) * (x^{s/2 - 1} + x^{-s/2 - 1/2}) dx
            + 1/(s-1) - 1/s   ... actually let me use a cleaner route.

    The standard representation is:

    2*xi(s) = 1 + s*(s-1) * integral_1^inf psi(x) * (x^{s/2-1} + x^{(1-s)/2-1}) dx

    where psi(x) = sum_{n=1}^inf exp(-pi*n^2*x).

    But the cleanest derivation uses:

    xi(1/2+it) = 4 * integral_1^inf d/dx[x^{3/2}*psi'(x)] * x^{-1/4} * cos(t/2 * log x) dx

    Let x = e^{2v}, dx = 2*e^{2v}*dv, v ranges from 0 to inf:

    xi(1/2+it) = 4 * integral_0^inf d/dv[e^{3v}*psi'(e^{2v})] * (1/(2*e^{2v})) * e^{-v/2} * cos(tv) * 2*e^{2v} dv

    Hmm, this is getting messy. Let me just check numerically which formula matches.
    """
    pass


def phi_formula_v4(u, n_terms=50):
    """
    Version 4: The formula from the Wikipedia article on Xi function.

    Phi(t) = 2 * sum_{n=1}^inf (2*pi^2*n^4*e^{9t} - 3*pi*n^2*e^{5t}) * exp(-pi*n^2*e^{4t})

    With Xi(z) = integral_{-inf}^{inf} Phi(t) e^{izt} dt

    Here Phi(t) = Phi(-t), and t is the integration variable (not the argument of Xi).
    """
    t = mpmath.mpf(u)
    pi = mpmath.pi
    total = mpmath.mpf(0)
    for n in range(1, n_terms + 1):
        n = mpmath.mpf(n)
        total += (2*pi**2*n**4*mpmath.exp(9*t) - 3*pi*n**2*mpmath.exp(5*t)) * mpmath.exp(-pi*n**2*mpmath.exp(4*t))
    return total


def phi_formula_v5(u, n_terms=50):
    """
    Version 5: The most standard form.

    Following Csordas-Norfolk-Varga (1986) and Ki-Kim-Lee (2009):

    Phi(t) = sum_{n=1}^inf a_n(t)

    where a_n(t) = (2*pi*n^2*cosh(9t/2) - 3*cosh(5t/2)) * (2*pi*n^2) * exp(-pi*n^2*cosh(2t))

    Wait, that doesn't look right either. Let me look at the formulation more carefully.

    Actually, the standard form starting from:
    xi(s) = integral_0^inf Phi(x) x^{s-1} dx

    where the Fourier representation uses Phi(u) as an even function of u.

    The key formula (from Ki-Kim-Lee 2009, equation (1.2)):

    Phi(t) = 2*sum_{n=1}^inf (2*pi^2*n^4*e^{9t/2} - 3*pi*n^2*e^{5t/2}) * exp(-pi*n^2*e^{2t})

    for the representation Xi(z) = integral_0^inf Phi(t)*cos(zt) dt

    So the only difference from V1 is pi^2 instead of pi in the first coefficient.
    Let me test both.
    """
    t = mpmath.mpf(u)
    pi = mpmath.pi
    total = mpmath.mpf(0)
    for n in range(1, n_terms + 1):
        n = mpmath.mpf(n)
        e2t = mpmath.exp(2*t)
        total += 2*(2*pi**2*n**4*mpmath.exp(9*t/2) - 3*pi*n**2*mpmath.exp(5*t/2)) * mpmath.exp(-pi*n**2*e2t)
    return total


def main():
    print("=" * 80)
    print("DETERMINING THE CORRECT POLYA KERNEL FORMULA")
    print("=" * 80)
    print(f"Precision: {mpmath.mp.dps} decimal digits\n")

    # First, compute Xi(0) from zeta directly
    Xi_0 = Xi_t(mpmath.mpf(0))
    print(f"Xi(0) = xi(1/2) = {float(Xi_0):.15e}")

    # Now, Xi(0) = 2*integral_0^inf Phi(u) du  (from the Fourier representation)
    # So integral_0^inf Phi(u) du = Xi(0)/2

    # Compute integral_0^inf Phi(u) du for each formula version using quadrature
    print("\nTesting formula versions:")
    print("Xi(0)/2 should equal integral_0^inf Phi(u) du")
    print(f"Target: Xi(0)/2 = {float(Xi_0/2):.15e}")
    print(f"Target: Xi(0)   = {float(Xi_0):.15e}")
    print()

    # For the integral, Phi decays super-exponentially, so [0, 5] is more than enough
    # Actually [0, 2] suffices as we saw Phi ~ 10^{-70} at u=2.

    # Version 1
    integral_v1 = mpmath.quad(lambda u: phi_formula_v1(u, 30), [0, 3])
    print(f"V1 (2*pi*n^4):     integral_0^inf Phi du = {float(integral_v1):.15e}")
    print(f"   2*integral = {float(2*integral_v1):.15e}")

    # Version 2
    integral_v2 = mpmath.quad(lambda u: phi_formula_v2(u, 30), [0, 3])
    print(f"V2 (2*pi^2*n^4):   integral_0^inf Phi du = {float(integral_v2):.15e}")
    print(f"   2*integral = {float(2*integral_v2):.15e}")

    # Version 4
    integral_v4 = mpmath.quad(lambda u: phi_formula_v4(u, 30), [0, 3])
    print(f"V4 (exp(4t)):      integral_0^inf Phi du = {float(integral_v4):.15e}")
    print(f"   2*integral = {float(2*integral_v4):.15e}")

    # Version 5
    integral_v5 = mpmath.quad(lambda u: phi_formula_v5(u, 30), [0, 3])
    print(f"V5 (2x, pi^2):    integral_0^inf Phi du = {float(integral_v5):.15e}")
    print(f"   2*integral = {float(2*integral_v5):.15e}")

    # Also check: Xi(t) = 2*integral_0^inf Phi(u)*cos(tu) du
    # Check at t = 14.1347... (first zero of Xi)
    t_zero = mpmath.im(mpmath.zetazero(1))
    Xi_at_zero = Xi_t(t_zero)
    print(f"\nXi at first zero: Xi({float(t_zero):.6f}) = {float(Xi_at_zero):.15e}")

    # Check the Fourier integral at a non-zero point
    t_test = mpmath.mpf(5)
    Xi_at_5 = Xi_t(t_test)
    print(f"Xi(5) from zeta: {float(Xi_at_5):.15e}")

    for name, phi_func in [("V1", phi_formula_v1), ("V2", phi_formula_v2),
                           ("V5", phi_formula_v5)]:
        fourier_5 = 2 * mpmath.quad(lambda u: phi_func(u, 30) * mpmath.cos(t_test * u), [0, 3])
        print(f"  {name}: 2*int Phi*cos(5u) du = {float(fourier_5):.15e}  "
              f"ratio = {float(fourier_5/Xi_at_5):.8f}")

    # =========================================================
    # Derive the correct formula from first principles
    # =========================================================
    print("\n" + "=" * 70)
    print("DERIVATION FROM FIRST PRINCIPLES")
    print("=" * 70)

    print("""
    Starting from the completed zeta function:

    xi(s) = (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2)*zeta(s)

    The Riemann-Siegel representation:

    xi(s) = 1/2 + (s^2 - s/4) * integral_1^inf psi(x) * x^{-3/4} *
            [x^{s/2} + x^{(1-s)/2}] dx/x

    ...this is getting complicated. Let me use the simplest derivation.

    We know: zeta(s) * Gamma(s/2) * pi^{-s/2} = integral_0^inf x^{s/2-1} psi(x) dx +
             integral_0^inf x^{(1-s)/2-1} psi(x) dx + 1/(s-1) - 1/s

    (using the Mellin transform of psi and the functional equation of theta).

    Multiplying by s*(s-1)/2:
    xi(s) = 1/2 + s*(s-1)/2 * integral_0^inf psi(x) [x^{s/2-1} + x^{(1-s)/2-1}] dx

    Now substitute x = exp(2u):
    dx = 2*exp(2u) du
    x^{s/2-1} = exp((s-2)*u)
    x^{(1-s)/2-1} = exp((1-s-2)*u/1) = exp((-1-s)*u)  ...

    Hmm, let me try a different, cleaner approach.
    """)

    # Let me just numerically determine the correct formula by testing
    # multiple coefficient choices

    print("\nNumerical determination of correct coefficients:")
    print("Testing: Phi(u) = sum_n [A*n^4*exp(au) + B*n^2*exp(bu)] * exp(-pi*n^2*exp(cu))")
    print()

    # We know:
    # - The gaussian part involves exp(-pi*n^2*exp(2u)) (standard)
    # - The polynomial prefactor involves n^4 and n^2 terms
    # - The exponentials in u are exp(9u/2) and exp(5u/2) (standard)
    # - The coefficients A, B are to be determined

    # Let me try: Phi(u) = 4 * sum_n (2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}) * e^{-pi*n^2*e^{2u}}
    def phi_test(u, A_coeff, B_coeff, n_terms=30):
        u = mpmath.mpf(u)
        pi = mpmath.pi
        total = mpmath.mpf(0)
        for n in range(1, n_terms + 1):
            n = mpmath.mpf(n)
            e2u = mpmath.exp(2*u)
            total += (A_coeff*n**4*mpmath.exp(9*u/2) + B_coeff*n**2*mpmath.exp(5*u/2)) * mpmath.exp(-pi*n**2*e2u)
        return total

    # Grid of (A, B) values to test
    pi = mpmath.pi
    candidates = [
        ("2pi, -3pi", 2*pi, -3*pi),
        ("2pi^2, -3pi", 2*pi**2, -3*pi),
        ("4pi^2, -6pi", 4*pi**2, -6*pi),
        ("8pi^2, -6pi", 8*pi**2, -6*pi),
        ("4pi, -6pi", 4*pi, -6*pi),
    ]

    for name, A, B in candidates:
        integral = mpmath.quad(lambda u: phi_test(u, A, B, 30), [0, 3])
        fourier_0 = 2 * integral  # should = Xi(0)
        fourier_5 = 2 * mpmath.quad(lambda u: phi_test(u, A, B, 30) * mpmath.cos(5*u), [0, 3])

        ratio_0 = float(fourier_0 / Xi_0) if Xi_0 != 0 else float('inf')
        ratio_5 = float(fourier_5 / Xi_at_5) if Xi_at_5 != 0 else float('inf')

        print(f"  A={name:20s}: Xi(0) ratio = {ratio_0:.8f}, Xi(5) ratio = {ratio_5:.8f}")

    # =========================================================
    # The definitive approach: numerical integration of the Mellin transform
    # =========================================================
    print("\n" + "=" * 70)
    print("DEFINITIVE: Compute Phi from xi by inverse Fourier")
    print("=" * 70)

    # Phi(u) = (1/(2*pi)) * integral_{-inf}^{inf} Xi(t) * exp(-itu) dt
    # Since Xi is real and even:
    # Phi(u) = (1/pi) * integral_0^inf Xi(t) * cos(tu) dt

    # This integral converges because Xi(t) decays like exp(-pi*|t|/4) for large |t|.

    for u_test in [0.0, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
        u_test = mpmath.mpf(u_test)

        # Compute Phi(u) from the inverse Fourier transform
        Phi_from_inverse = (1/mpmath.pi) * mpmath.quad(
            lambda t: Xi_t(t) * mpmath.cos(t * u_test),
            [0, 50],  # Xi decays rapidly
            maxdegree=8
        )

        # Compare with formula versions
        v1 = phi_formula_v1(u_test, 30)
        v2 = phi_formula_v2(u_test, 30)
        v5 = phi_formula_v5(u_test, 30)

        print(f"u = {float(u_test):.2f}:")
        print(f"  Phi (inverse FT) = {float(Phi_from_inverse):.12e}")
        print(f"  V1 (2*pi*n^4)    = {float(v1):.12e}  ratio = {float(v1/Phi_from_inverse) if Phi_from_inverse != 0 else 'N/A'}")
        print(f"  V2 (2*pi^2*n^4)  = {float(v2):.12e}  ratio = {float(v2/Phi_from_inverse) if Phi_from_inverse != 0 else 'N/A'}")
        print(f"  V5 (2x V2)       = {float(v5):.12e}  ratio = {float(v5/Phi_from_inverse) if Phi_from_inverse != 0 else 'N/A'}")
        print()

    print("\nThe version whose ratio is consistently 1.0 is the correct formula.")


if __name__ == '__main__':
    main()
