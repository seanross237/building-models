"""
04_lee_yang_analysis.py
=======================
Investigate the Lee-Yang connection to the primon gas and RH.

The Lee-Yang theorem (1952): For ferromagnetic Ising models,
all zeros of the partition function Z(z) (in the fugacity z = e^{beta*h})
lie on the unit circle |z| = 1.

This is structurally analogous to RH:
  - Lee-Yang: zeros on |z| = 1 (a circle)
  - RH: zeros on Re(s) = 1/2 (a line)

The connection is made precise via the change of variable:
  s = 1/2 + it => z = e^{-beta*E_0} * e^{i*theta}

Can the primon gas be formulated as a system where a Lee-Yang type
theorem applies?

Author: Strategy 2A exploration
Date: 2026-04-04
"""

import mpmath
import numpy as np
import json

mpmath.mp.dps = 30


def analyze_lee_yang_structure():
    """
    THE LEE-YANG / RH ANALOGY

    The Lee-Yang theorem applies to partition functions of the form:
      Z(z) = sum_{n=0}^{N} a_n * z^n
    where {a_n} are the coefficients of the partition function in the
    fugacity variable z.

    For the Ising model: Z(z) = sum_{config} z^{sum spins}
    Lee-Yang says: if the coupling is ferromagnetic (J > 0),
    all zeros of Z(z) are on |z| = 1.

    For the primon gas:
      Z(s) = zeta(s) = prod_p (1 - p^{-s})^{-1}

    The "fugacity" analogue: let z_p = p^{-s} for each prime p.
    Then Z = prod_p (1 - z_p)^{-1}.

    If we write z_p = p^{-sigma} * e^{-it*log(p)}, then:
    - z_p is "on the unit circle" when sigma = 0
    - z_p is "inside the unit circle" when sigma > 0

    This doesn't directly map to Lee-Yang. But there's a better approach.

    THE HEILMANN-LIEB / RUELLE FRAMEWORK:

    For graph polynomials (matching polynomials, independence polynomials),
    there are Lee-Yang type theorems:
    - Heilmann-Lieb (1972): matching polynomial has all real zeros
    - Ruelle (2010): pressure of a polymer gas with repulsive interactions
      has no zeros in a disk

    The primon gas can be viewed as a gas of "polymers" (prime power blocks)
    with the constraint that the total "volume" (= log(n)) must equal E.

    THE KEY MAPPING:

    Consider the truncated Euler product:
      Z_N(s) = prod_{p <= N} (1 - p^{-s})^{-1}

    Set w = p^{-s+1/2} for the "reduced fugacity." Then:
      Z_N = prod_p (1 - p^{-1/2} * w_p)^{-1}

    RH says: all zeros of Z_N have w_p on the unit circle for each p.

    The question: is there a positivity condition on the "interactions"
    between primes that forces Lee-Yang behavior?

    ANALYSIS:
    """
    print("=== Lee-Yang structure analysis ===\n")

    # The Xi function: Riemann's completed zeta function
    # Xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s)
    # Xi satisfies: Xi(s) = Xi(1-s), and all zeros have 0 < Re(s) < 1
    # RH: all zeros have Re(s) = 1/2

    # The Hadamard product:
    # Xi(s) = Xi(0) * prod_rho (1 - s/rho)
    # where the product is over nontrivial zeros rho

    # In the variable t where s = 1/2 + it:
    # Xi(1/2 + it) is a real-valued function of real t (by the reflection formula)
    # This is like a "partition function" in the variable t

    # If we write z = e^{alpha*t} for some alpha, then
    # Xi becomes a power series in z, and RH says all zeros are at |z| = 1

    # Specifically, define:
    # Phi(t) = Xi(1/2 + it)
    # Then Phi(t) is an even entire function with all real zeros (iff RH)
    # Phi(t) = sum_{n=0}^{inf} a_{2n} * t^{2n}

    # The Polya-Schur program: Phi has all real zeros iff {a_{2n}} satisfies
    # the "multiplier sequence" property (Laguerre-Polya class)

    # Compute the Taylor coefficients of Xi(1/2 + it) around t=0
    print("  Taylor coefficients of Xi(1/2 + it) around t = 0:")
    print("  (Xi must have all real zeros iff RH)")

    def Xi(s):
        """Riemann's Xi function."""
        return 0.5 * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)

    def Phi(t):
        """Phi(t) = Xi(1/2 + it), a real function when t is real."""
        return Xi(mpmath.mpf('0.5') + mpmath.mpc(0, t))

    # Compute Taylor coefficients
    # Phi(t) = sum a_n t^n, but Phi is even so odd coefficients vanish
    # Note: Phi(t) is real for real t, but mpmath may return mpc; take real part
    print(f"\n  {'n':>4s} {'a_n':>20s} {'sign':>6s}")
    coeffs = []
    for n in range(0, 20):
        if n == 0:
            val = Phi(mpmath.mpf(0))
            a_n = float(mpmath.re(val))
        else:
            taylor_coeffs = mpmath.taylor(Phi, 0, n)
            a_n = float(mpmath.re(taylor_coeffs[n]))
        coeffs.append(a_n)
        sign = '+' if a_n >= 0 else '-'
        print(f"  {n:4d} {a_n:20.12e} {sign:>6s}")

    # For Phi to have all real zeros, the even-index coefficients must form
    # a Polya frequency sequence of order 2 (or higher)
    print("\n  Even coefficients (should alternate in sign for all-real-zeros):")
    for n in range(0, 20, 2):
        print(f"    a_{n} = {coeffs[n]:.12e}")

    return coeffs


def lee_yang_via_truncated_euler():
    """
    Study the zeros of the truncated Euler product in the fugacity plane.

    Z_N(s) = prod_{p <= N} (1 - p^{-s})^{-1}

    Write s = sigma + it. For fixed t, Z_N is a function of sigma.
    The zeros of Z_N occur where one of the factors vanishes:
    p^{-s} = 1, i.e., s = 2*pi*i*k / log(p) for integer k.

    These are all on the line sigma = 0, which is OUTSIDE the critical strip.

    But zeta(s) = lim_{N->inf} Z_N(s) has zeros IN the critical strip
    due to cancellation in the limit. This is fundamentally different from
    finite systems, where Lee-Yang theorems apply.

    The interesting question: what happens to the zeros as N grows?
    Do they approach Re(s) = 1/2?
    """
    print("\n=== Truncated Euler product zeros ===\n")

    # For a single prime p, (1 - p^{-s})^{-1} has no zeros.
    # For two primes: (1 - 2^{-s})^{-1} * (1 - 3^{-s})^{-1} also has no zeros.
    # The zeros of zeta arise from infinite cancellation.

    # A better approach: the Dirichlet polynomial
    # Z_N(s) = sum_{n=1}^{N} n^{-s}
    # This is a finite sum that approximates zeta(s).

    # Compute zeros of sum_{n=1}^{N} n^{-s} for various N
    # These partial sums DO have zeros, and they approach the zeta zeros as N -> inf

    print("  Zeros of partial sums of zeta(s):")
    print("  Z_N(s) = sum_{n=1}^{N} n^{-s}")

    for N in [10, 50, 100, 500]:
        def Z_N(s):
            return sum(mpmath.power(n, -s) for n in range(1, N + 1))

        # Find zeros near the known first zero of zeta (0.5 + 14.13i)
        try:
            z = mpmath.findroot(Z_N, mpmath.mpc(0.5, 14.13))
            print(f"  N={N:4d}: zero near first zeta zero: s = {float(z.real):.6f} + {float(z.imag):.6f}i")
            print(f"          Re(s) - 0.5 = {float(z.real) - 0.5:.8f}")
        except Exception as e:
            print(f"  N={N:4d}: findroot failed ({e})")

    return True


def lee_yang_conditions_for_primon():
    """
    What conditions would the primon gas need to satisfy for a Lee-Yang
    type theorem to apply?

    The standard Lee-Yang theorem requires:
    1. Ferromagnetic interactions (positive couplings)
    2. External field coupling to a conserved quantity
    3. The partition function is a polynomial in the fugacity

    The primon gas:
    1. Interactions: the primon gas is a FREE gas (no interactions between primons).
       The lack of interaction actually makes Lee-Yang EASIER in principle.
    2. The partition function zeta(s) is NOT a polynomial — it's an infinite product.
    3. The "fugacity" is p^{-s} for each prime, which is a continuous variable.

    For the Ruelle approach (lattice gas / polymer gas):
    - The primon gas has "particles" at sites labeled by primes p
    - Each site can have occupation number n_p = 0, 1, 2, ...
    - The energy of configuration {n_p} is sum_p n_p * log(p)
    - The partition function is Z = prod_p sum_{n_p=0}^{inf} e^{-beta*n_p*log(p)}
                                  = prod_p 1/(1 - p^{-beta})
                                  = zeta(beta)

    The Ruelle approach to Lee-Yang zeros requires:
    - A repulsive interaction between particles
    - The interaction must be "hard enough" to prevent clustering

    For the primon gas with NO interactions, the partition function
    factorizes completely, and each factor (1 - z_p)^{-1} has no zeros
    inside the unit disk. The problem is that zeta has zeros despite
    the factors being non-zero — the zeros come from the infinite product.

    KEY INSIGHT: The primon gas IS free (no interactions), but the
    CONSTRAINT that all primes must be used (the Euler product runs
    over ALL primes) creates effective long-range correlations.
    These correlations are the number-theoretic content of RH.

    A Lee-Yang theorem for the primon gas would need to capture these
    correlations. The most promising framework is:

    DOBRUSHIN'S THEOREM (1996, generalized):
    For a lattice gas with complex fugacity z and interaction phi,
    all zeros of the grand partition function lie outside the region
    |z| < R where R depends on the interaction strength.

    For the primon gas, the "interaction" arises from the multiplicative
    structure of integers. Two primons at primes p and q "interact"
    through their products: the state n = p*q exists because BOTH
    primons are excited. This is an ATTRACTIVE interaction in
    the Dobrushin sense, which is the OPPOSITE of what Lee-Yang needs.

    This explains why a direct Lee-Yang approach fails and why RH is hard.
    """
    print("\n=== Lee-Yang conditions analysis ===\n")

    print("  Required for Lee-Yang theorem:")
    print("  1. Repulsive interactions between particles")
    print("  2. Partition function is polynomial or analytic in fugacity")
    print("  3. Symmetry: Z(z) = z^N * Z(1/z) or similar reflection")
    print()
    print("  Primon gas status:")
    print("  1. FREE gas (no direct interactions) -- factor 1/(1-z_p) per prime")
    print("     But multiplicative structure creates EFFECTIVE ATTRACTION")
    print("  2. Z = zeta(s) is an infinite product, NOT polynomial")
    print("     -> Lee-Yang applies to finite systems; infinite limit is the difficulty")
    print("  3. Functional equation: Xi(s) = Xi(1-s) provides the required symmetry")
    print("     This maps to the circle |z|=1 in the variable z = p^{-(s-1/2)}")
    print()
    print("  Conclusion: The primon gas satisfies condition (3) via the functional")
    print("  equation, but violates conditions (1) and (2). A Lee-Yang approach")
    print("  would need a NEW theorem that handles:")
    print("  a) Infinite products (rather than polynomials)")
    print("  b) Attractive/multiplicative interactions (rather than repulsive)")
    print()
    print("  The most promising path: use the GENERALIZED Lee-Yang framework")
    print("  of Borcea-Branden (2009), which characterizes all linear operators")
    print("  preserving the property of having zeros on a prescribed locus.")
    print("  Their theory works for entire functions, not just polynomials.")


def borcea_branden_analysis():
    """
    The Borcea-Branden program and its application to the primon gas.

    Borcea & Branden (Annals of Math., 2009) proved:
    The only linear operators T: C[z] -> C[z] that preserve the property
    "all zeros on the unit circle" are compositions of:
    (1) Multiplication by z^k * c (c constant on the unit circle)
    (2) Differentiation d/dz
    (3) The "symbol" operator associated with a stable polynomial

    They also characterized operators preserving "all zeros on a line"
    (the half-plane stability property).

    For the Riemann zeta function, the relevant operator is:
    T: polynomial P(z) -> entire function Xi(s) = Xi(1/2 + it)

    If we can express Xi as T(P) for some simple P with all real zeros,
    and T is in the Borcea-Branden class, then RH follows.

    The challenge: identifying T explicitly.
    """
    print("\n=== Borcea-Branden framework ===\n")

    # The Xi function can be written as a Fourier transform:
    # Xi(1/2 + it) = integral_0^inf Phi(u) cos(tu) du
    # where Phi(u) = sum_n (2*pi^2*n^4*e^{9u} - 3*pi*n^2*e^{5u}) * exp(-pi*n^2*e^{4u})

    # Polya showed: if Phi(u) is non-negative and log-concave,
    # then the Fourier transform has only real zeros.

    # Polya's condition is NOT proven for the actual Phi.
    # But numerically, we can check it.

    def Phi_kernel(u):
        """The kernel function in Xi's Fourier representation."""
        u = mpmath.mpf(u)
        result = mpmath.mpf(0)
        for n in range(1, 20):  # convergence is fast
            term1 = 2 * mpmath.pi**2 * n**4 * mpmath.exp(9*u)
            term2 = 3 * mpmath.pi * n**2 * mpmath.exp(5*u)
            gauss = mpmath.exp(-mpmath.pi * n**2 * mpmath.exp(4*u))
            result += (term1 - term2) * gauss
        return result

    print("  Polya's kernel Phi(u) for Xi(1/2 + it) = integral Phi(u) cos(tu) du:")
    print(f"  {'u':>8s} {'Phi(u)':>20s} {'log(Phi)':>20s}")

    u_vals = np.linspace(0, 3, 50)
    phi_vals = []
    log_phi_vals = []

    for u in u_vals:
        phi = float(Phi_kernel(u))
        phi_vals.append(phi)
        if phi > 0:
            log_phi_vals.append(np.log(phi))
        else:
            log_phi_vals.append(float('nan'))

    for i in range(0, len(u_vals), 5):
        lp = f"{log_phi_vals[i]:20.8f}" if not np.isnan(log_phi_vals[i]) else "            nan"
        print(f"  {u_vals[i]:8.4f} {phi_vals[i]:20.8e} {lp}")

    # Check positivity
    min_phi = min(phi_vals)
    print(f"\n  Minimum Phi(u) = {min_phi:.8e}")
    print(f"  Phi(u) > 0 for all tested u: {min_phi > 0}")

    # Check log-concavity: d^2/du^2 log(Phi) < 0?
    log_phi = np.array(log_phi_vals)
    valid = ~np.isnan(log_phi)
    u_valid = u_vals[valid]
    lp_valid = log_phi[valid]

    if len(lp_valid) > 2:
        du = u_valid[1] - u_valid[0]
        d2_log_phi = np.diff(lp_valid, 2) / du**2

        n_concave = np.sum(d2_log_phi < 0)
        n_total = len(d2_log_phi)
        print(f"\n  Log-concavity of Phi(u):")
        print(f"    d^2/du^2 log(Phi) < 0 at {n_concave}/{n_total} points")
        print(f"    Max d^2/du^2 log(Phi) = {np.max(d2_log_phi):.8f}")
        print(f"    Min d^2/du^2 log(Phi) = {np.min(d2_log_phi):.8f}")

        if n_concave == n_total:
            print("    => Phi is log-concave on tested range!")
            print("    => If this extends to all u, Polya's criterion gives RH")
        else:
            print("    => Phi is NOT log-concave everywhere on tested range")
            # Find where it fails
            violations = np.where(d2_log_phi >= 0)[0]
            for v in violations[:5]:
                print(f"       Violation at u = {u_valid[v+1]:.4f}: d^2 log Phi = {d2_log_phi[v]:.8f}")

    return phi_vals, log_phi_vals


def newman_condition():
    """
    The de Bruijn-Newman constant Lambda.

    de Bruijn (1950) and Newman (1976) introduced a family of functions:
    H_t(z) = integral_0^inf e^{tu^2} Phi(u) cos(zu) du

    where Phi is the kernel from above. Key facts:
    - H_0(z) = Xi(1/2 + iz) (the Xi function)
    - For each t, H_t is entire with only real zeros iff t >= Lambda
    - RH is equivalent to Lambda <= 0
    - Lambda >= 0 was proved by Rodgers-Tao (2020)
    - Therefore Lambda = 0 iff RH

    The "heat flow" H_t evolves the zeros: as t increases, zeros spread out
    on the real line. Newman conjectured Lambda >= 0 (proved by Rodgers-Tao).

    Connection to the primon gas:
    - The parameter t is like an inverse temperature for the ZEROS
    - At t=0 (RH), the zeros are maximally "cold" — on the critical line
    - For t > 0, the zeros "heat up" and spread off the line
    - For t < 0, the zeros would have to be even more constrained

    RH says the zeros are at the PHASE BOUNDARY between spread and collapse.
    This is exactly the Lee-Yang circle theorem statement:
    the zeros are on the boundary of the "physical" region.
    """
    print("\n=== de Bruijn-Newman constant and the Lee-Yang analogy ===\n")

    print("  de Bruijn-Newman constant Lambda:")
    print("    Lambda <= 0 <==> RH")
    print("    Lambda >= 0 (Rodgers-Tao 2020)")
    print("    Best upper bound: Lambda <= 0.2 (Platt-Trudgian 2021)")
    print("    Therefore: 0 <= Lambda <= 0.2")
    print()
    print("  Lee-Yang analogy:")
    print("    In Lee-Yang: zeros on |z|=1 (the boundary)")
    print("    In RH: zeros on Re(s)=1/2 (the boundary)")
    print("    In Newman's picture: Lambda = 0 means zeros are at the")
    print("    PHASE BOUNDARY of the heat flow")
    print()
    print("  The primon gas thermodynamic interpretation:")
    print("    The heat flow parameter t corresponds to 'smearing' the")
    print("    microcanonical ensemble. At t=0 (RH), the entropy S(E)")
    print("    is maximally constrained — exactly concave.")
    print("    For t > 0, the entropy develops bumps (off-line zeros).")
    print("    For t < 0, the entropy would be 'super-concave'.")
    print()
    print("  CONJECTURE: RH is equivalent to the statement that the")
    print("  microcanonical entropy of the primon gas achieves MINIMAL")
    print("  fluctuation (Cramér-Rao bound) at the critical line.")
    print("  The Fisher information of the density of states is")
    print("  minimized when all zeros are at Re(s) = 1/2.")


if __name__ == '__main__':
    print("=" * 80)
    print("LEE-YANG ANALYSIS FOR THE PRIMON GAS")
    print("=" * 80)

    # 1. Structure analysis
    coeffs = analyze_lee_yang_structure()

    # 2. Truncated Euler product
    lee_yang_via_truncated_euler()

    # 3. Conditions analysis
    lee_yang_conditions_for_primon()

    # 4. Borcea-Branden / Polya kernel
    phi_vals, log_phi_vals = borcea_branden_analysis()

    # 5. Newman constant
    newman_condition()

    # Save
    output = {
        'xi_taylor_coefficients': coeffs,
        'phi_kernel_positive': min(phi_vals) > 0,
        'lee_yang_applicable': False,
        'borcea_branden_path': 'Promising but requires new theorem for infinite products',
        'newman_constant_bounds': [0, 0.2],
        'key_conjecture': 'RH equivalent to minimal Fisher information of primon gas density of states',
    }

    output_path = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/2A-entropy-ceiling/results_lee_yang.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n\nResults saved to {output_path}")
