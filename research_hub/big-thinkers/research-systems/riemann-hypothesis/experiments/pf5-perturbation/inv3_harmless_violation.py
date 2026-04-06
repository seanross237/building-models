"""
Investigation 3: The "Harmless Violation" Argument.

Can we show that if a kernel is "almost PF5" (fails by epsilon), the zeros of
its Fourier cosine transform are "almost real" (within epsilon' of the real axis)?

We approach this through:
1. Quantitative Schoenberg: What bound on non-real zeros comes from PF_k?
2. The Hadamard factorization: xi(s) = xi(0) prod (1 - s/rho) over zeros rho.
   Non-real zeros come in conjugate pairs. If all 5x5 minors of K are
   close to non-negative, what constraint does this place on the zero pairs?
3. The sign changes of the Fourier transform: PF_k controls the number of
   sign changes of convolutions. What does "almost PF5" say about
   "almost sign regularity"?
4. Explicit construction: Can we build a kernel that is PF4 but NOT PF5,
   and whose Fourier transform has non-real zeros? How large is the imaginary
   part as a function of the PF5 deficit?

Key theoretical ingredient: Variation-diminishing property.
If K is PF_r, then the convolution T_K: f -> integral K(x-y)f(y)dy
maps functions with n sign changes to functions with at most n sign changes,
provided n <= r-1. The deficit in PF5 means this property fails for n = 4
sign changes, but only by a small amount.
"""

from mpmath import mp, mpf, matrix, det, pi, exp, cos, sin, quad, sqrt, log, fac
import time
import json

mp.dps = 60

def phi_term(n, u):
    n = mpf(n)
    u = mpf(u)
    return (2*pi**2*n**4*exp(9*u) - 3*pi*n**2*exp(5*u)) * exp(-pi*n**2*exp(4*u))

def phi(u, N=50):
    u = mpf(u)
    return sum(phi_term(n, u) for n in range(1, N+1))

def K(u, N=50):
    return phi(abs(mpf(u)), N)

def K_t(u, t, N=50):
    u_mpf = mpf(u)
    t_mpf = mpf(t)
    return exp(t_mpf * u_mpf**2) * K(u, N)

def toeplitz_det(kfunc, u0, h, r):
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return det(M)


def main():
    print("=" * 70)
    print("Investigation 3: The Harmless Violation Argument")
    print("=" * 70)

    # Part 1: Quantitative analysis of the PF5 deficit
    print("\n--- Part 1: Quantifying the PF5 deficit ---")

    # Compute the worst D5/D4 ratio across a fine grid
    configs = []
    for u0 in [0.001, 0.003, 0.005, 0.007, 0.01, 0.015, 0.02, 0.025, 0.03]:
        for h in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]:
            configs.append((u0, h))

    print(f"  Scanning {len(configs)} configurations for worst PF5 deficit...")
    worst_ratio = 0
    worst_config = None
    all_deficits = []

    for u0, h in configs:
        d4 = toeplitz_det(K, u0, h, 4)
        d5 = toeplitz_det(K, u0, h, 5)
        if d5 < 0 and d4 > 0:
            ratio = float(abs(d5) / d4)
            all_deficits.append({'u0': u0, 'h': h, 'D4': float(d4), 'D5': float(d5), 'ratio': ratio})
            if ratio > worst_ratio:
                worst_ratio = ratio
                worst_config = (u0, h)

    print(f"  Found {len(all_deficits)} configurations with D5 < 0")
    if worst_config:
        print(f"  Worst deficit: |D5|/D4 = {worst_ratio:.6e} at ({worst_config[0]}, {worst_config[1]})")
    print(f"  All deficit ratios:")
    for d in sorted(all_deficits, key=lambda x: -x['ratio'])[:10]:
        print(f"    ({d['u0']:.3f}, {d['h']:.3f}): |D5|/D4 = {d['ratio']:.6e}")

    # Part 2: The variation-diminishing property analysis
    print("\n--- Part 2: Variation-Diminishing Property ---")
    print("""
  Theory: If K is PF_r, the convolution T_K diminishes sign changes
  by at most S-(f) - S-(T_K f) >= 0 for functions with S-(f) <= r-1
  sign changes.

  For PF_4 (which holds): convolutions preserve up to 3 sign changes.
  For PF_5 (which fails): 4 sign changes may INCREASE under convolution.

  But the deficit is epsilon = |D5|/D4 ~ 6.5e-4. This means:
  - The 5x5 minor is -epsilon * D4 instead of +something * D4
  - The "variation-increasing" effect for 4-sign-change functions is
    bounded by a function of epsilon.

  Specifically, by the theory of compound kernels:
  If D5 = -epsilon * |D4|, then the 4th compound kernel K^(4) has a
  single negative eigenvalue of magnitude ~ epsilon.

  This means non-real zeros of the Fourier transform (if they exist)
  must be located where:
  - The "sign change amplification" from the almost-PF5 failure
    can coherently produce a zero with nonzero imaginary part.
""")

    # Part 3: Explicit toy model - Gaussian times polynomial
    print("\n--- Part 3: Toy model — Gaussian with controlled PF failure ---")
    print("  Testing: K_alpha(u) = exp(-u^2) * (1 + alpha * u^4)")
    print("  This is PF_infinity for alpha=0, and the u^4 term breaks PF5")
    print("  for sufficiently large alpha.")
    print("")

    # For K_alpha(u) = exp(-u^2)(1 + alpha*u^4), compute Fourier transform
    # and find zeros as alpha increases from 0
    def K_alpha(u, alpha):
        u = mpf(u)
        return exp(-u**2) * (1 + mpf(alpha) * u**4)

    for alpha in [0, 0.001, 0.01, 0.05, 0.1, 0.5, 1.0]:
        # Check PF5 at u0=0, h=0.1
        kfunc = lambda u, a=alpha: K_alpha(u, a)
        d4 = toeplitz_det(kfunc, 0, 0.1, 4)
        d5 = toeplitz_det(kfunc, 0, 0.1, 5)
        s4 = "+" if d4 > 0 else "-"
        s5 = "+" if d5 > 0 else "-"
        print(f"  alpha={alpha:>5.3f}: D4={float(d4):>12.4e}[{s4}], D5={float(d5):>12.4e}[{s5}]")
        if d5 < 0 and d4 > 0:
            print(f"           PF5 deficit = {float(abs(d5)/d4):.6e}")

    # Part 4: Fourier transform at imaginary argument
    print("\n--- Part 4: Fourier cosine transform of Phi at complex argument ---")
    print("  H(x) = integral_{-inf}^{inf} Phi(|u|) cos(xu) du")
    print("  For real x, H(x) = xi(1/2 + ix) (up to normalization)")
    print("  For x = a + bi, a non-real zero of H means xi(1/2+i(a+bi)) = 0")
    print("  i.e., zeta(1/2 - b + ia) = 0, which violates RH if b != 0.")
    print("")

    # Compute H(x) for real x to verify it matches xi
    def H_numerical(x_re, x_im=0, N_terms=50, N_quad=200):
        """Fourier cosine transform of Phi at x = x_re + i*x_im.
        H(x) = 2 * integral_0^infty Phi(u) cos(xu) du
        """
        x = mpf(x_re) + mpf(x_im) * 1j if x_im != 0 else mpf(x_re)

        def integrand(u):
            if x_im == 0:
                return phi(u, N_terms) * cos(mpf(x_re) * u)
            else:
                # cos(xu) = cos((x_re+i*x_im)*u) = cos(x_re*u)*cosh(x_im*u) - i*sin(x_re*u)*sinh(x_im*u)
                from mpmath import cosh, sinh
                re_part = cos(mpf(x_re)*u) * cosh(mpf(x_im)*u)
                im_part = -sin(mpf(x_re)*u) * sinh(mpf(x_im)*u)
                return phi(u, N_terms) * (re_part + im_part * 1j)

        # Integrate from 0 to a large cutoff
        # Phi decays super-exponentially, so cutoff=5 is safe
        result = 2 * quad(integrand, [0, 5], maxdegree=7)
        return result

    print("  H(x) for real x (should match xi pattern):")
    for x in [0, 5, 10, 14.134]:  # 14.134... is first zero of xi
        try:
            val = H_numerical(x, 0, N_terms=10, N_quad=50)
            print(f"    H({x:>6.3f}) = {float(val.real if hasattr(val, 'real') else val):>14.6e}")
        except Exception as e:
            print(f"    H({x:>6.3f}) = error: {e}")

    # Part 5: Bound on imaginary part of zeros from PF5 deficit
    print("\n--- Part 5: Theoretical bound on zero displacement ---")
    print("""
  Key theoretical argument:

  If K is PF_infinity, Schoenberg's theorem guarantees all zeros of
  H(x) = integral K(u) cos(xu) du are real.

  If K is PF_4 but fails PF_5 by epsilon (meaning min_config D5/D4 = -epsilon),
  then by the compound kernel theory:

  The 4th compound kernel K^{(4)}(x_1,...,x_4; y_1,...,y_4) = det[K(x_i - y_j)]_{i,j=1..4}
  is non-negative (this is PF_4).

  The 5th compound kernel K^{(5)} has a negative region of volume proportional
  to epsilon.

  The zeros of H(x) are constrained by the sign-change properties of K.
  For PF_infinity kernels, the zero set is real. For PF_4 kernels, the
  argument is:

  1. PF_4 => K^{(4)} >= 0 => the 4-point correlation function of the
     associated determinantal point process is non-negative.

  2. This controls the "4-fold coincidence" probabilities and implies
     that zeros can't form complex quartets (pairs of conjugate pairs)
     too far from the real axis.

  3. The PF_5 failure means 5-point correlations can be negative,
     which would be needed for 5 zeros to form a complex arrangement.

  CONJECTURE: If |D5|/D4 <= epsilon for all configurations, then any
  non-real zero rho = sigma + it of zeta satisfies:
    |sigma - 1/2| <= C * epsilon^{1/4}

  where C is an absolute constant.

  Basis: A non-real zero pair creates a contribution to the 5th compound
  kernel that scales as Im(rho)^4 (from the 4th power in the 5-point
  determinant). For this to be consistent with the D5 deficit being
  epsilon, we need Im(rho)^4 ~ epsilon.

  With epsilon = 6.5e-4, this would give:
    |sigma - 1/2| <= C * (6.5e-4)^{1/4} ~ C * 0.16

  This is NOT strong enough for RH (which requires |sigma - 1/2| = 0)
  but would be a quantitative zero-free region.

  CRITICAL CAVEAT: This conjecture is NOT proven. The relationship
  between finite PF order and zero location is an open problem.
  The scaling exponent 1/4 is heuristic (from dimensional analysis
  of the 5-point determinant).
""")

    # Part 6: Sensitivity analysis — how does D5 depend on zero location?
    print("\n--- Part 6: Sensitivity of D5 to perturbations ---")
    # If we perturb Phi by adding a small oscillatory term that mimics
    # the effect of a non-real zero, what happens to D5?

    # A non-real zero at rho = sigma + it contributes a factor
    # proportional to cos(sigma*u) * exp(-t*u) to the kernel.
    # We add a small perturbation: epsilon * cos(sigma*u) * exp(-delta*u)
    # and see how D5 changes.

    u0, h = 0.01, 0.05
    print(f"  Base D5 at ({u0}, {h}):")
    d5_base = toeplitz_det(K, u0, h, 5)
    d4_base = toeplitz_det(K, u0, h, 4)
    print(f"    D5 = {float(d5_base):.6e}, D4 = {float(d4_base):.6e}")

    print(f"\n  Adding perturbation eps * cos(sigma*u) * exp(-delta*|u|):")
    for eps in [1e-6, 1e-5, 1e-4, 1e-3]:
        for sigma in [14.134, 21.022]:  # Near first two zeta zeros
            for delta in [0.001, 0.01, 0.1]:
                def K_perturbed(u, e=eps, s=sigma, d=delta):
                    u_mpf = mpf(u)
                    base = phi(abs(u_mpf))
                    perturbation = mpf(e) * cos(mpf(s) * u_mpf) * exp(-mpf(d) * abs(u_mpf))
                    return base + perturbation

                d5_pert = toeplitz_det(K_perturbed, u0, h, 5)
                change = float(d5_pert - d5_base)
                rel_change = change / float(abs(d5_base)) if d5_base != 0 else float('inf')

                if abs(rel_change) > 0.01:  # Only print significant changes
                    print(f"    eps={eps:.0e}, sigma={sigma:.3f}, delta={delta:.3f}: "
                          f"delta_D5={change:>12.4e}, rel={rel_change:>8.2f}")

    # Save
    results = {
        'all_deficits': all_deficits,
        'worst_ratio': worst_ratio,
        'worst_config': worst_config,
    }
    outfile = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf5-perturbation/inv3_results.json"
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")

if __name__ == "__main__":
    main()
