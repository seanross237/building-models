"""
04_analytic_proof_attempt.py
============================
Attempting an analytic proof of log-concavity of the Polya kernel.

STRATEGY:
=========

We have F(u) = f_1(u) + R(u), where:
  f_1(u) = (2*pi^2*e^{9u/2} - 3*pi*e^{5u/2}) * exp(-pi*e^{2u})   [n=1 term]
  R(u) = sum_{n=2}^inf f_n(u)                                       [higher terms]

PROVED: f_1 is strictly log-concave for all u >= 0.
  d^2/du^2 log(f_1) = -24*pi*e^{2u}/(2*pi*e^{2u}-3)^2 - 4*pi*e^{2u}

GOAL: Show that the correction from R(u) does not destroy log-concavity.

KEY IDENTITY:
  d^2/du^2 log(F) = d^2/du^2 log(f_1) + d^2/du^2 log(1 + r)
  where r(u) = R(u)/f_1(u).

  d^2/du^2 log(1+r) = [r''(1+r) - (r')^2] / (1+r)^2

For log-concavity of F, we need:
  |d^2/du^2 log(1+r)| < |d^2/du^2 log(f_1)|

This reduces to bounding r, r', r'' in terms of f_1 and its derivatives.

APPROACH 1: For u >= u_0, show |R/f_1| < epsilon and bound the correction.
APPROACH 2: For u near 0, use the explicit form of f_n to bound everything.
APPROACH 3: Prove log-concavity of the FULL sum using properties of the theta function.

Author: Polya kernel log-concavity investigation
Date: 2026-04-04
"""

import mpmath
import json

mpmath.mp.dps = 80


def F_term_derivatives(n, u):
    """Compute f_n(u), f_n'(u), f_n''(u)."""
    n = mpmath.mpf(n)
    u = mpmath.mpf(u)
    pi = mpmath.pi

    An = 2*pi**2*n**4
    Bn = -3*pi*n**2
    cn = pi*n**2
    alpha = mpmath.mpf(9)/2
    beta = mpmath.mpf(5)/2

    e2u = mpmath.exp(2*u)
    ea = mpmath.exp(alpha*u)
    eb = mpmath.exp(beta*u)

    g = mpmath.exp(-cn*e2u)
    gp = -2*cn*e2u*g
    gpp = (4*cn**2*e2u**2 - 4*cn*e2u)*g

    p = An*ea + Bn*eb
    pp = alpha*An*ea + beta*Bn*eb
    ppp = alpha**2*An*ea + beta**2*Bn*eb

    f = p*g
    fp = pp*g + p*gp
    fpp = ppp*g + 2*pp*gp + p*gpp

    return f, fp, fpp


def main():
    print("=" * 80)
    print("ANALYTIC PROOF ATTEMPT: LOG-CONCAVITY OF THE POLYA KERNEL")
    print("=" * 80)

    # =========================================================
    # APPROACH 1: Bound R(u)/f_1(u) for all u >= 0
    # =========================================================
    print("\n" + "=" * 60)
    print("APPROACH 1: Bounding the ratio R/f_1")
    print("=" * 60)

    print("""
    For n >= 2, the ratio f_n(u)/f_1(u) is controlled by the Gaussian factors:

    f_n(u)/f_1(u) = [(2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}) * exp(-pi*n^2*e^{2u})]
                    / [(2*pi^2*e^{9u/2} - 3*pi*e^{5u/2}) * exp(-pi*e^{2u})]

    = [(2*pi^2*n^4 - 3*pi*n^2*e^{-2u}) / (2*pi^2 - 3*pi*e^{-2u})] * exp(-pi*(n^2-1)*e^{2u})

    For u >= 0: e^{2u} >= 1, so the ratio of prefactors is bounded by:
      numerator <= 2*pi^2*n^4  (since Bn < 0)
      denominator >= 2*pi^2 - 3*pi = pi*(2*pi - 3) > 0

    So: |f_n(u)/f_1(u)| <= [2*pi^2*n^4 / (pi*(2*pi-3))] * exp(-pi*(n^2-1)*e^{2u})

    For u >= 0: exp(-pi*(n^2-1)*e^{2u}) <= exp(-pi*(n^2-1))

    Therefore: sum_{n>=2} |f_n/f_1| <= sum_{n>=2} C*n^4*exp(-pi*(n^2-1))
    where C = 2*pi / (2*pi - 3)
    """)

    pi = mpmath.pi
    C = 2*pi / (2*pi - 3)
    print(f"  Constant C = 2*pi/(2*pi-3) = {float(C):.8f}")

    # Compute the bound
    bound_sum = mpmath.mpf(0)
    for n in range(2, 100):
        n = mpmath.mpf(n)
        bound_sum += C * n**4 * mpmath.exp(-pi*(n**2 - 1))

    print(f"  sum_{{n>=2}} C*n^4*exp(-pi*(n^2-1)) = {float(bound_sum):.15e}")
    print(f"  This bounds |R(u)/f_1(u)| for all u >= 0.")
    print()

    # This gives us: |r(u)| <= bound_sum for all u >= 0
    r_bound = float(bound_sum)
    print(f"  |r(u)| = |R/f_1| <= {r_bound:.8e} for all u >= 0")

    # But we also need bounds on r'(u) and r''(u)!
    # r(u) = R(u)/f_1(u), so r' = (R'*f_1 - R*f_1')/(f_1)^2
    # This requires bounding R', f_1', etc.

    # =========================================================
    # Bound on r'(u) and r''(u)
    # =========================================================
    print("\n  Bounding r'(u) and r''(u):")

    print("""
    For each f_n(u), we can write:
    f_n(u) = P_n(e^u) * exp(-pi*n^2*e^{2u})

    where P_n involves polynomials in e^u times exponentials.

    The key observation: for the ratio r = R/f_1:

    d/du log(f_n/f_1) = d/du [log|f_n| - log|f_1|]

    For n >= 2 and u >= 0:
    f_n/f_1 ~ n^4 * exp(-pi*(n^2-1)*e^{2u})

    So d/du (f_n/f_1) ~ -2*pi*(n^2-1)*e^{2u} * (f_n/f_1)

    The derivative of the ratio ALSO decays exponentially!

    More precisely:
    |d^k/du^k (f_n/f_1)| <= C_k * n^{4+2k} * (pi*e^{2u})^k * exp(-pi*(n^2-1)*e^{2u})

    The factor (pi*e^{2u})^k * exp(-pi*(n^2-1)*e^{2u}) is maximized at
    e^{2u} = k/(pi*(n^2-1)), giving value <= (k/(n^2-1))^k * e^{-k} / pi^k

    But for u >= 0 (e^{2u} >= 1):
    (pi*e^{2u})^k * exp(-pi*(n^2-1)*e^{2u}) <= pi^k * exp(-pi*(n^2-1))
                                                (when the function is decreasing)
    """)

    # Let's compute the actual bounds on r' and r'' numerically
    # at several values of u
    print("\n  Numerical computation of r, r', r'' bounds:")
    print(f"  {'u':>6s} {'|r|':>14s} {'|r_prime|':>14s} {'|r_dblprime|':>14s}")

    for u_val in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
        u = mpmath.mpf(u_val)

        f1, f1p, f1pp = F_term_derivatives(1, u)

        # Compute R, R', R'' directly
        R = mpmath.mpf(0)
        Rp = mpmath.mpf(0)
        Rpp = mpmath.mpf(0)
        for n in range(2, 40):
            fn, fnp, fnpp = F_term_derivatives(n, u)
            R += fn
            Rp += fnp
            Rpp += fnpp

        # r = R/f1
        r = R/f1
        # r' = (R'*f1 - R*f1')/f1^2
        rp = (Rp*f1 - R*f1p)/f1**2
        # r'' = (R''*f1 - R*f1'')/f1^2 - 2*f1'*(R'*f1-R*f1')/f1^3
        rpp = (Rpp*f1 - R*f1pp)/f1**2 - 2*f1p*(Rp*f1 - R*f1p)/f1**3

        print(f"  {u_val:6.3f} {float(abs(r)):14.6e} {float(abs(rp)):14.6e} {float(abs(rpp)):14.6e}")

    # =========================================================
    # APPROACH 2: Direct bound on the correction to d^2 log
    # =========================================================
    print("\n" + "=" * 60)
    print("APPROACH 2: Direct bound on the log-concavity correction")
    print("=" * 60)

    print("""
    d^2/du^2 log(F) = d^2/du^2 log(f_1) + Delta

    where Delta = d^2/du^2 log(1+r) = [r''(1+r) - (r')^2] / (1+r)^2

    For log-concavity, we need |Delta| < |d^2/du^2 log(f_1)|.

    Since r is small (|r| < 0.0022 at u=0, exponentially smaller for u>0):

    |Delta| <= (|r''| + |r'|^2)/(1 - |r|)^2 + |r''|*|r|/(1-|r|)^2
             ~ |r''| + |r'|^2  (to leading order)

    We need to check this against |d^2/du^2 log(f_1)|.
    """)

    print(f"\n  {'u':>6s} {'|Delta|':>14s} {'|d2log_f1|':>14s} {'ratio':>10s} {'margin':>10s}")

    all_proven = True
    for u_val in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5]:
        u = mpmath.mpf(u_val)

        f1, f1p, f1pp = F_term_derivatives(1, u)

        R = mpmath.mpf(0)
        Rp = mpmath.mpf(0)
        Rpp = mpmath.mpf(0)
        for n in range(2, 40):
            fn, fnp, fnpp = F_term_derivatives(n, u)
            R += fn
            Rp += fnp
            Rpp += fnpp

        r = R/f1
        rp = (Rp*f1 - R*f1p)/f1**2
        rpp = (Rpp*f1 - R*f1pp)/f1**2 - 2*f1p*(Rp*f1 - R*f1p)/f1**3

        # Bound on Delta
        abs_r = abs(r)
        abs_rp = abs(rp)
        abs_rpp = abs(rpp)

        Delta_bound = (abs_rpp*(1 + abs_r) + abs_rp**2) / (1 - abs_r)**2

        # d^2/du^2 log(f_1)
        d2log_f1 = (f1*f1pp - f1p**2)/f1**2

        ratio = float(Delta_bound / abs(d2log_f1))
        margin = float(abs(d2log_f1) - Delta_bound)

        proven = margin > 0
        if not proven:
            all_proven = False

        print(f"  {u_val:6.3f} {float(Delta_bound):14.6e} {float(abs(d2log_f1)):14.6e} "
              f"{ratio:10.6f} {margin:10.4e} {'OK' if proven else 'FAIL'}")

    print(f"\n  All points proven: {all_proven}")

    # =========================================================
    # APPROACH 3: Refined analysis at u=0 (the hardest point)
    # =========================================================
    print("\n" + "=" * 60)
    print("APPROACH 3: Refined analysis at u=0")
    print("=" * 60)

    u = mpmath.mpf(0)
    mpmath.mp.dps = 120

    # Compute everything at very high precision
    f1, f1p, f1pp = F_term_derivatives(1, u)

    # Compute R and its derivatives with careful summation
    R = mpmath.mpf(0)
    Rp = mpmath.mpf(0)
    Rpp = mpmath.mpf(0)
    for n in range(2, 80):
        fn, fnp, fnpp = F_term_derivatives(n, u)
        R += fn
        Rp += fnp
        Rpp += fnpp

    F = f1 + R
    Fp = f1p + Rp
    Fpp = f1pp + Rpp

    # The exact log-concavity expression
    LC = F*Fpp - Fp**2
    d2log_F = LC / F**2

    # The n=1 contribution
    d2log_f1 = (f1*f1pp - f1p**2) / f1**2

    print(f"  At u=0 with {mpmath.mp.dps}-digit precision:")
    print(f"  f_1(0)  = {float(f1):.20e}")
    print(f"  R(0)    = {float(R):.20e}")
    print(f"  R/f_1   = {float(R/f1):.20e}")
    print(f"  F(0)    = {float(F):.20e}")
    print(f"  d^2/du^2 log(f_1(0)) = {float(d2log_f1):.20e}")
    print(f"  d^2/du^2 log(F(0))   = {float(d2log_F):.20e}")
    print(f"  Correction Delta     = {float(d2log_F - d2log_f1):.20e}")
    print(f"  |Correction/d2log_f1| = {float(abs((d2log_F - d2log_f1)/d2log_f1)):.10e}")
    print()

    # Is the correction small?
    correction_ratio = abs(float((d2log_F - d2log_f1)/d2log_f1))
    if correction_ratio < 0.05:
        print(f"  The correction is {correction_ratio*100:.2f}% of d^2/du^2 log(f_1).")
        print(f"  This is a small perturbation of the n=1 log-concavity.")

    mpmath.mp.dps = 80  # reset

    # =========================================================
    # APPROACH 4: The theta function / heat equation approach
    # =========================================================
    print("\n" + "=" * 60)
    print("APPROACH 4: Heat equation / convolution perspective")
    print("=" * 60)

    print("""
    The key structural insight:

    F(u) = d/du [e^{3u} * psi'(e^{2u})]  (up to constants)

    where psi(x) = sum_{n=1}^inf exp(-pi*n^2*x)

    psi(x) is a theta function, which satisfies the heat equation:
    d/dt psi(x,t) = (1/4pi) * d^2/dx^2 psi(x,t)

    The heat equation preserves log-concavity (Brascamp-Lieb 1976):
    If f(x,0) is log-concave in x, then f(x,t) is log-concave for all t > 0.

    QUESTION: Can we express F(u) as a heat-evolved version of a log-concave function?

    Let's analyze the structure:
    psi(x) = sum_n exp(-pi*n^2*x) = sum_n G_n(x)

    Each G_n(x) = exp(-pi*n^2*x) is log-AFFINE in x (linear log, so vacuously log-concave).

    But psi is a SUM of log-concave functions, which is NOT necessarily log-concave.
    However, psi is a completely monotone function of x (all derivatives alternate in sign).
    Complete monotonicity is stronger than log-concavity!

    CLAIM: psi(x) is log-concave in x for x > 0.

    Proof attempt:
    psi'(x) = -pi * sum_n n^2 * exp(-pi*n^2*x)
    psi''(x) = pi^2 * sum_n n^4 * exp(-pi*n^2*x)

    psi * psi'' - (psi')^2
    = [sum_n exp(-an*x)][sum_n an^2*exp(-an*x)] - [sum_n an*exp(-an*x)]^2

    where an = pi*n^2.

    By the Cauchy-Schwarz inequality for sums:
    [sum fn*gn]^2 <= [sum fn^2][sum gn^2]

    with fn = exp(-an*x/2), gn = an*exp(-an*x/2):
    [sum an*exp(-an*x)]^2 <= [sum exp(-an*x)][sum an^2*exp(-an*x)]

    THEREFORE: psi*psi'' >= (psi')^2

    i.e., psi is LOG-CONVEX!  (not log-concave)

    Wait, that's the OPPOSITE sign. Let me recheck...

    psi*psi'' - (psi')^2 >= 0 means d^2/du^2 log(psi) >= 0, which is log-CONVEX.

    So psi itself is log-convex. This is because it's a mixture of exponentials
    (which are log-convex), and mixtures of log-convex functions are log-convex.

    But F(u) is NOT psi. F involves a DERIVATIVE of psi and a change of variables.
    The differentiation and multiplication by e^{3u} change the convexity.
    """)

    # Verify psi is log-convex
    print("Verification: psi(x) is log-convex")
    for x_val in [1.0, 2.0, 5.0, 10.0]:
        x = mpmath.mpf(x_val)
        psi = sum(mpmath.exp(-mpmath.pi*n**2*x) for n in range(1, 50))
        psi_p = sum(-mpmath.pi*n**2*mpmath.exp(-mpmath.pi*n**2*x) for n in range(1, 50))
        psi_pp = sum((mpmath.pi*n**2)**2*mpmath.exp(-mpmath.pi*n**2*x) for n in range(1, 50))

        lc = psi*psi_pp - psi_p**2
        print(f"  x={x_val:.1f}: psi*psi'' - (psi')^2 = {float(lc):.6e} > 0 (log-convex)")

    # =========================================================
    # APPROACH 5: Log-concavity via the substitution x = e^{2u}
    # =========================================================
    print("\n" + "=" * 60)
    print("APPROACH 5: Analysis in the x = e^{2u} variable")
    print("=" * 60)

    print("""
    Let x = e^{2u}, so u = log(x)/2, du = dx/(2x).

    F(u(x)) = sum_n (2*pi^2*n^4*x^{9/4} - 3*pi*n^2*x^{5/4}) * exp(-pi*n^2*x)

    Let G(x) = F(u(x)) = sum_n g_n(x)
    where g_n(x) = (2*pi^2*n^4*x^{9/4} - 3*pi*n^2*x^{5/4}) * exp(-pi*n^2*x)

    The log-concavity of F in u is equivalent to a condition on G in x.
    Specifically, using du = dx/(2x):

    d/du = 2x * d/dx
    d^2/du^2 = 4x^2 * d^2/dx^2 + 4x * d/dx

    So d^2/du^2 log(F) = 4x^2 * (G''/G - (G'/G)^2) + 4x * G'/G
                        = 4x^2 * d^2/dx^2 log(G) + 4x * d/dx log(G)

    For this to be negative:
    x * d^2/dx^2 log(G) + d/dx log(G) < 0
    i.e., d/dx [x * d/dx log(G)] < 0 ... not quite, let me redo.

    d^2/du^2 log(G) = 4x[x * G''/G - x*(G'/G)^2 + G'/G]
    = 4x/G^2 [x*(G*G'' - G'^2) + G*G']

    So F is log-concave in u iff:
    x*(G*G'' - G'^2) + G*G' < 0
    i.e., x*G*G'' + G*G' < x*G'^2
    i.e., G*(x*G'' + G') < x*G'^2

    This is a weighted log-concavity condition on G in x.

    Actually, there's a cleaner way. F(u) is log-concave in u iff
    G(x) = F(log(x)/2) is log-concave in log(x), which is the same as saying
    G(x)*x is a "geometrically concave" function.

    The condition is: G(x) * x^alpha is log-concave in log(x) for appropriate alpha.
    """)

    # =========================================================
    # APPROACH 6: The de Bruijn flow perspective
    # =========================================================
    print("\n" + "=" * 60)
    print("APPROACH 6: de Bruijn-Newman flow and log-concavity")
    print("=" * 60)

    print("""
    The de Bruijn-Newman constant Lambda satisfies:
    - RH iff Lambda = 0
    - Lambda >= 0 (Rodgers-Tao 2020)
    - Lambda <= 0.2 (Platt-Trudgian 2021)

    The heat-evolved kernel:
    Phi_t(u) = integral exp(t*v^2) * Phi_0(u-v) dv / sqrt(4*pi*t)

    (where Phi_0 = Phi is our kernel)

    H_t(z) = integral Phi_t(u) * cos(zu) du

    Fact: H_t has only real zeros for t >= Lambda.
    RH: H_0 has only real zeros, i.e., Lambda = 0.

    POLYA'S CRITERION: If Phi_0 is log-concave, then H_0 has only real zeros.

    Connection to Lambda: Polya's criterion says Phi_0 is log-concave => Lambda <= 0.
    But we know Lambda >= 0. So if Phi_0 is log-concave, Lambda = 0, which is RH.

    THE CRITICAL SUBTLETY:
    Phi is the kernel at "time 0" in the heat flow. If Lambda = 0 (RH),
    then Phi is EXACTLY at the boundary of having all real zeros.

    For the heat flow, log-concavity is preserved forward in time.
    But Lambda = 0 means we're at the critical time.

    In principle, Phi could be:
    (a) Strictly log-concave (strong enough for RH with room to spare)
    (b) Log-concave but not strictly (just barely enough)
    (c) Not log-concave (Polya's criterion doesn't apply)

    Our numerical evidence shows (a): d^2/du^2 log(Phi(0)) = -18.73,
    which is STRONGLY negative. This is surprising given that Lambda = 0
    or very close to 0.

    HOWEVER: the de Bruijn-Newman flow acts on the FOURIER transform side.
    The heat equation in t acts multiplicatively on the Fourier modes.
    Strong log-concavity of Phi does NOT mean there's a large margin
    for the zeros. The connection between the magnitude of d^2/du^2 log(Phi)
    and the value of Lambda is subtle and nonlinear.
    """)

    # Compute: how does d^2/du^2 log(Phi_t) change as t increases from 0?
    # Phi_t(u) = integral Phi(u-v) * exp(-v^2/(4t)) dv / sqrt(4*pi*t)
    # For small t, this is a small Gaussian blur of Phi.

    print("How heat flow affects log-concavity:")
    print("(Computing d^2/du^2 log(Phi_t) at u=0 for various t)")

    # For the n=1 term, the heat flow gives:
    # f_1^{(t)}(u) ~ integral f_1(u-v) * (4*pi*t)^{-1/2} * exp(-v^2/(4t)) dv
    # This is a convolution of f_1 with a Gaussian.

    # Actually, the standard way is to look at the Fourier representation:
    # H_t(z) = integral Phi(u) * exp(t*u^2) * cos(zu) du ... NO
    # H_t(z) = integral e^{tu^2} * Phi(u) * e^{izu} du

    # The heat flow MULTIPLIES the Fourier integrand by e^{tu^2}.
    # So Phi_t(u) = e^{tu^2} * Phi(u) ... that can't be right either.

    # Actually, the standard definition (de Bruijn 1950):
    # H_t(z) = integral_{-inf}^{inf} e^{tu^2} Phi(u) e^{izu} du

    # This means the "kernel at time t" is Phi_t(u) = e^{tu^2} * Phi(u).

    # So log(Phi_t) = t*u^2 + log(Phi(u))
    # d^2/du^2 log(Phi_t) = 2t + d^2/du^2 log(Phi)

    # CRITICAL INSIGHT: d^2/du^2 log(Phi_t) = 2t + d^2/du^2 log(Phi)

    # For Phi_t to be log-concave: 2t + d^2/du^2 log(Phi) < 0 for all u
    # i.e., t < -max_u [d^2/du^2 log(Phi(u))] / 2

    # Our computation shows: max d^2/du^2 log(Phi) = -18.73 at u=0.
    # So Phi_t is log-concave for t < 18.73/2 = 9.37.

    max_d2log = mpmath.mpf('-18.7269049295')  # from our computation
    t_critical = -max_d2log / 2

    print(f"\n  d^2/du^2 log(Phi_t) = 2t + d^2/du^2 log(Phi)")
    print(f"  Max d^2/du^2 log(Phi) = {float(max_d2log):.6f} (at u=0)")
    print(f"  Phi_t log-concave requires: t < {float(t_critical):.4f}")
    print()
    print(f"  IMPLICATION: If Phi is log-concave, then Lambda <= 0.")
    print(f"  (Because Phi_t is also log-concave for t in [0, {float(t_critical):.2f}],")
    print(f"   which means H_t has only real zeros for t in [{float(-t_critical):.2f}, 0],")
    print(f"   implying Lambda <= -{float(t_critical):.2f}... wait, that gives Lambda < 0,")
    print(f"   which CONTRADICTS Lambda >= 0!")
    print()

    print("  WAIT: Let me reconsider the relationship between Polya's criterion")
    print("  and the de Bruijn-Newman constant.")
    print()
    print("  The standard form: H_t(z) = int exp(tu^2) Phi(u) cos(zu) du")
    print("  H_0(z) = Xi(z)")
    print("  Lambda = inf{t : H_t has only real zeros for all t' > t}")
    print()
    print("  Polya's criterion: Phi log-concave => H_0 has only real zeros")
    print("  But Polya's criterion does NOT directly give Lambda <= 0.")
    print("  It only tells us about the zeros of H_0, not H_t for t < 0.")
    print()
    print("  The relationship between log-concavity of Phi and Lambda is:")
    print("  If e^{tu^2}*Phi(u) is log-concave, then H_t has only real zeros.")
    print("  e^{tu^2}*Phi is log-concave iff 2t + d^2/du^2 log(Phi) < 0 for all u.")
    print("  So H_t has only real zeros for t < |max d^2 log Phi|/2.")
    print(f"  This gives: H_t has only real zeros for t > -{float(t_critical):.2f}")
    print(f"  => Lambda <= -{float(t_critical):.2f}")
    print()
    print("  BUT Lambda >= 0 (Rodgers-Tao)!")
    print()
    print("  CONCLUSION: If we could prove Phi is log-concave,")
    print("  we would get Lambda <= 0, and combined with Lambda >= 0,")
    print("  we would get Lambda = 0, which IS THE RIEMANN HYPOTHESIS.")
    print()
    print("  Moreover, log-concavity gives Lambda <= -9.36, which is even stronger.")
    print("  This stronger bound would contradict Lambda >= 0 UNLESS our value")
    print("  of max d^2/du^2 log(Phi) is wrong...")
    print()
    print("  WAIT. The issue is the SIGN CONVENTION.")
    print("  Let me re-examine more carefully.")

    # =========================================================
    # CRITICAL CHECK: Sign convention in de Bruijn-Newman
    # =========================================================
    print("\n" + "=" * 60)
    print("CRITICAL: Checking the de Bruijn-Newman sign convention")
    print("=" * 60)

    print("""
    The standard definition (Rodgers-Tao 2020):

    H_t(z) = integral_0^inf e^{tu^2} Phi(u) cos(zu) du

    For t > 0: e^{tu^2} AMPLIFIES the tails of Phi, making it LESS log-concave.
    For t < 0: e^{tu^2} SUPPRESSES the tails, making it MORE log-concave.

    The kernel for H_t is: K_t(u) = e^{tu^2} * Phi(u)
    d^2/du^2 log(K_t) = 2t + d^2/du^2 log(Phi)

    K_t is log-concave iff 2t + d^2/du^2 log(Phi(u)) < 0 for all u >= 0.

    For t = 0: need d^2/du^2 log(Phi) < 0 for all u. This is Polya's criterion.
    For t > 0: need d^2/du^2 log(Phi) < -2t for all u. HARDER.
    For t < 0: need d^2/du^2 log(Phi) < -2t = 2|t|. EASIER (always true if Phi is bounded).

    Now, Lambda is defined so that H_t has only real zeros for t >= Lambda.

    If Phi is log-concave: then K_0 = Phi is log-concave, so H_0 has only real zeros.
    But also K_t is log-concave for t in (-inf, -max_u d^2 log Phi / 2).

    Wait, K_t is log-concave when:
    2t + d^2/du^2 log Phi(u) < 0 for all u
    2t < -d^2/du^2 log Phi(u) for all u
    2t < min_u [-d^2/du^2 log Phi(u)]
    2t < -max_u [d^2/du^2 log Phi(u)]

    max_u d^2/du^2 log Phi = -18.73 (at u=0, where it's least negative)

    So: 2t < 18.73, i.e., t < 9.37.

    For t < 9.37, K_t is log-concave, so H_t has only real zeros.
    This means Lambda <= -9.37?? No...

    Lambda = inf{t : H_s has only real zeros for all s >= t}

    If H_t has real zeros for ALL t < 9.37, and we know Lambda >= 0...
    Then Lambda is in [0, 9.37).

    Actually, we're showing that H_t has real zeros for t IN [0, 9.37].
    But Lambda is defined as the INFIMUM of t such that H_s has only real zeros
    for ALL s >= t. So if H_t has only real zeros for all t >= -9.37,
    then Lambda <= -9.37. Combined with Lambda >= 0, contradiction!

    UNLESS: my computation is wrong, or Polya's criterion gives something weaker.

    Let me re-examine Polya's criterion more carefully.
    """)

    # The issue might be that log-concavity of K_t does NOT imply
    # that H_t has only real zeros. Let me check.

    print("\n  RESOLUTION: Polya's criterion is that if Phi is EVEN and log-concave,")
    print("  then int Phi(u) cos(zu) du has only real zeros.")
    print("  But K_t(u) = e^{tu^2} Phi(u) is NOT THE SAME as Phi evolved under heat.")
    print("  The heat equation on the FOURIER side is multiplication by e^{-tz^2}.")
    print("  So H_t(z) = e^{-tz^2} * H_0(z) ... NO, that's not right either.")
    print()
    print("  H_t(z) = int e^{tu^2} Phi(u) cos(zu) du")
    print("  This is NOT e^{-tz^2} * Xi(z) in general (e^{tu^2}*cos(zu) is not separable).")
    print()
    print("  The correct relationship: H_t(z) satisfies the backwards heat equation:")
    print("  dH_t/dt = -d^2H_t/dz^2")
    print()
    print("  For t > 0: H_t is a BACKWARDS heat evolution, which can CREATE zeros.")
    print("  For t < 0: H_t is a FORWARD heat evolution, which REMOVES zeros.")
    print()
    print("  Lambda = 0 means H_0 has only real zeros (RH).")
    print("  Lambda > 0 would mean we need some backwards evolution before zeros become real.")
    print()
    print("  Polya's criterion: log-concavity of Phi => H_0 has only real zeros => Lambda <= 0")
    print("  Combined with Lambda >= 0: Polya's criterion + Lambda >= 0 => Lambda = 0 => RH")
    print()
    print("  THE STRONGER STATEMENT:")
    print("  If e^{tu^2}*Phi is log-concave for some t_0 > 0, then H_{-t_0} has only real zeros.")
    print("  This means Lambda <= -t_0 < 0, contradicting Lambda >= 0.")
    print()
    print(f"  Our computation: max d^2/du^2 log(Phi) = {float(max_d2log):.4f} at u=0.")
    print(f"  e^{{tu^2}}*Phi is log-concave at u=0 iff 2t + {float(max_d2log):.4f} < 0,")
    print(f"  i.e., t < {float(t_critical):.4f}.")
    print()
    print("  But we need log-concavity FOR ALL u, not just u=0.")
    print("  As u -> infinity, d^2/du^2 log(Phi) -> -infinity (it gets MORE negative).")
    print("  So the weakest point is indeed u=0.")
    print()
    print("  THEREFORE: IF Phi is log-concave, then e^{tu^2}*Phi is log-concave")
    print(f"  for t < {float(t_critical):.2f}, which implies Lambda <= -{float(t_critical):.2f}.")
    print("  This CONTRADICTS Lambda >= 0!")
    print()
    print("  *** THIS MEANS EITHER: ***")
    print("  (1) Phi is NOT log-concave (our numerical evidence is misleading), OR")
    print("  (2) There's an error in the argument above, OR")
    print("  (3) There's a subtlety about the boundary behavior as u -> 0^+")
    print("       or the behavior for u < 0 (Phi is even, we need log-concavity")
    print("       on the whole real line, not just u >= 0)")
    print()

    # =========================================================
    # CRITICAL CHECK: Is Phi log-concave on (-inf, inf)?
    # =========================================================
    print("=" * 60)
    print("CRITICAL CHECK: Log-concavity on the FULL real line")
    print("=" * 60)

    print("""
    Phi(u) is defined as an EVEN function (Phi(-u) = Phi(u)).

    For an even function, d^2/du^2 log(Phi) at u=0 involves Phi''(0)/Phi(0) - 0
    (since Phi'(0) = 0 by evenness).

    But the issue is: is Phi GLOBALLY log-concave on (-inf, inf)?

    For an even function, log-concavity on (-inf,inf) requires:
    1. d^2/du^2 log Phi < 0 for all u (including u < 0)
    2. By evenness, this is equivalent to: d^2/du^2 log Phi < 0 for all u >= 0

    So the analysis on [0, inf) suffices!

    But wait: there's a subtlety at u=0. For an even function, Phi'(0) = 0.
    The log-concavity at u=0 is:
    d^2/du^2 log Phi(0) = Phi''(0)/Phi(0)

    (since (Phi')^2 = 0 at u=0 by evenness).

    Our computation gives Phi''(0)/Phi(0) = d^2/du^2 log Phi(0) = -18.73.

    Hmm, but our F is the HALF-line version. Phi(u) for u < 0 is defined by
    Phi(-u) = Phi(u). Let me verify that F(u) = Phi(u) for u >= 0 and
    Phi'(0) = 0 (not just F'(0) = some nonzero value).
    """)

    # Check: is F'(0) = 0?
    u = mpmath.mpf(0)
    F0, Fp0, Fpp0, _, _ = compute_F_and_derivs_full(u)
    print(f"  F(0)   = {float(F0):.15e}")
    print(f"  F'(0)  = {float(Fp0):.15e}")
    print(f"  F''(0) = {float(Fpp0):.15e}")
    print()

    if abs(Fp0) > 1e-10:
        print("  F'(0) != 0 !")
        print("  This means F(u) is NOT the same as Phi(u) on [0,inf).")
        print("  Phi is even: Phi(-u) = Phi(u), so Phi'(0) = 0.")
        print("  But F'(0) != 0, so F is the one-sided function.")
        print()
        print("  The FULL Phi function on the real line is:")
        print("  Phi(u) = F(|u|) for all u")
        print()
        print("  IMPORTANT: d^2/du^2 log(Phi) at u=0 is NOT the same as")
        print("  d^2/du^2 log(F) at u=0.")
        print()
        print("  For F(|u|): at u=0, by the chain rule:")
        print("  Phi'(0) = 0 (by evenness)")
        print("  Phi''(0) = F''(0)  (from the even extension)")
        print()
        print("  Actually, more carefully: Phi(u) = F(|u|) for an even extension.")
        print("  Near u=0: Phi(u) = F(u) for u > 0, and Phi''(0) = F''(0)")
        print("  since F'(0) != 0, the even extension has a kink at 0!")
        print()
        print("  NO WAIT: The correct even extension is F(|u|), which HAS Phi'(0)=0")
        print("  but Phi''(0) = |F''(0)| only if F'(0)=0.")
        print("  Since F'(0) != 0, the function F(|u|) is NOT differentiable at u=0.")
        print()
        print("  THIS IS THE KEY ISSUE.")
        print("  The Polya kernel Phi(u) as defined by the Fourier integral")
        print("  Xi(t) = int Phi(u) cos(tu) du")
        print("  is naturally defined on [0, inf) and then EVEN-EXTENDED.")
        print("  The even extension Phi(u) = F(|u|) has F'(0) != 0, which means")
        print("  Phi is NOT smooth at u=0.")
        print()
        print("  Actually, the STANDARD definition uses:")
        print("  Xi(t) = 2 * int_0^inf F(u) cos(tu) du")
        print("  or equivalently")
        print("  Xi(t) = int_{-inf}^inf F(|u|) cos(tu) du")
        print()
        print("  Polya's criterion requires F(|u|) to be log-concave on R.")
        print("  For an even function h(u) with h'(0-) = -h'(0+) != 0,")
        print("  d^2/du^2 log(h) involves a delta function at u=0 (from the kink).")
        print()
        print("  So Polya's criterion really requires:")
        print("  (a) F(u) is log-concave on (0, inf)  [we are checking this]")
        print("  (b) The even extension F(|u|) is log-concave at u=0")
        print("  Condition (b) requires F'(0) <= 0 (so the kink goes the right way).")

        if Fp0 < 0:
            print(f"\n  F'(0) = {float(Fp0):.6e} < 0: the even extension has a DOWNWARD kink.")
            print("  A downward kink means the function is more concave, so log-concavity")
            print("  at u=0 is HELPED by the kink. Condition (b) is satisfied!")
        else:
            print(f"\n  F'(0) = {float(Fp0):.6e} > 0: the even extension has an UPWARD kink.")
            print("  An upward kink means the function is LESS concave. This could")
            print("  violate log-concavity at u=0!")


def compute_F_and_derivs_full(u, n_terms=40):
    """Compute F(u), F'(u), F''(u) with the correct formula."""
    u = mpmath.mpf(u)
    F = mpmath.mpf(0)
    Fp = mpmath.mpf(0)
    Fpp = mpmath.mpf(0)

    for n in range(1, n_terms + 1):
        f, fp, fpp = F_term_derivatives(n, u)
        F += f
        Fp += fp
        Fpp += fpp

    return F, Fp, Fpp, mpmath.mpf(0), mpmath.mpf(0)


if __name__ == '__main__':
    main()
