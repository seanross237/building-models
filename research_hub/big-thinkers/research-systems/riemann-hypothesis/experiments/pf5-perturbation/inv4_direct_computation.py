"""
Investigation 4: Direct computation of D5 for K_t at small t values.

The key computation: at what heat-flow time t does PF5 get restored?
If PF5 is restored at t = 0.001, that would suggest Lambda is very close to 0.

We compute D5 for K_t(u) = e^{t*u^2} * Phi(|u|) at:
- t = 0, 0.0001, 0.001, 0.01, 0.1
- Multiple (u0, h) configurations

CRITICAL INSIGHT from prior work: The Gaussian deformation does NOT
monotonically improve PF order. At t ~ 10, PF4 BREAKS. So there's a
window problem: we need PF5 restored BEFORE PF4 breaks.

New approach: Instead of the Gaussian deformation e^{tu^2}, consider:
1. The ACTUAL de Bruijn-Newman heat kernel convolution
2. Perturbations that preserve the theta structure
3. The Hermite expansion approach

Also: compute higher-order minors D6, D7 at t=0 to understand the full
PF spectrum.
"""

from mpmath import mp, mpf, matrix, det, pi, exp, cos, quad, sqrt
import time
import json

mp.dps = 80  # High precision for sensitive computations

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
    print("Investigation 4: Direct Computation of D5 at Small Heat Flow")
    print("=" * 70)

    results = {}

    # Part 1: Very fine t scan at the worst configuration
    print("\n--- Part 1: Ultra-fine t scan at worst configurations ---")

    worst_configs = [
        (0.001, 0.05),  # Worst |D5|/D4
        (0.01, 0.05),   # Paper counterexample
        (0.001, 0.04),
        (0.01, 0.04),
    ]

    # Focus on small t: does D5 improve at all?
    t_ultra_fine = [0, 1e-6, 1e-5, 1e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1, 2e-1, 5e-1, 1.0]

    for u0, h in worst_configs:
        print(f"\n  Config ({u0}, {h}):")
        print(f"    {'t':>10} {'D5':>16} {'D4':>16} {'|D5|/D4':>14} {'D5 improvement':>16}")
        d5_0 = None
        for t in t_ultra_fine:
            kfunc = lambda u, tv=mpf(t): K_t(u, tv)
            d5 = toeplitz_det(kfunc, u0, h, 5)
            d4 = toeplitz_det(kfunc, u0, h, 4)
            ratio = float(abs(d5)/d4) if d4 > 0 else float('inf')
            if d5_0 is None:
                d5_0 = d5
                improvement = 0.0
            else:
                improvement = float((d5 - d5_0) / abs(d5_0)) if d5_0 != 0 else 0
            print(f"    {t:>10.1e} {float(d5):>16.6e} {float(d4):>16.6e} {ratio:>14.6e} {improvement:>16.6e}")

        key = f"({u0},{h})"
        results[key] = {
            't_values': t_ultra_fine,
        }

    # Part 2: Higher-order minors at t=0
    print("\n--- Part 2: Higher-order minors D6, D7 at t=0 ---")
    for u0, h in [(0.01, 0.05), (0.001, 0.05), (0.05, 0.1), (0.1, 0.1)]:
        print(f"\n  Config ({u0}, {h}):")
        for r in range(2, 8):
            t0 = time.time()
            d = toeplitz_det(K, u0, h, r)
            t1 = time.time()
            s = "+" if d > 0 else "-"
            print(f"    D{r} = {float(d):>16.6e} [{s}]  ({t1-t0:.1f}s)")

    # Part 3: The CORRECT de Bruijn-Newman heat flow
    print("\n--- Part 3: Correct Heat Flow Analysis ---")
    print("""
  The de Bruijn-Newman constant Lambda is defined via:
    H_t(x) = integral e^{tu^2} Phi(u) cos(xu) du

  This means K_t(u) = e^{tu^2} Phi(|u|) is indeed the correct kernel.

  HOWEVER, the question "does PF_infinity of K_t imply all zeros of H_t
  are real?" requires Schoenberg's theorem, which needs:
  (a) K_t is PF_infinity (i.e., all Toeplitz minors non-negative), AND
  (b) K_t is even

  K_t(u) = e^{tu^2} Phi(|u|) IS even (since Phi(|u|) is even and e^{tu^2} is even).
  So Schoenberg's theorem applies: PF_infinity of K_t => real zeros of H_t.

  The CONVERSE is also relevant: if H_t has all real zeros, is K_t PF_infinity?
  By Schoenberg's characterization, for even kernels:
    all zeros of H real <=> K is PF_infinity

  So Lambda = inf{t: K_t is PF_infinity}.

  This means: if we could show K_t is PF_infinity for t=0, that would prove RH.
  We know K_0 is NOT PF_infinity (fails PF_5). So RH is NOT a direct consequence
  of PF analysis at t=0.

  But: if K_t becomes PF_infinity at t = delta for small delta, then Lambda <= delta.
  The key question is whether PF_infinity is EVER achieved at finite t, or whether
  there's always some PF_k that fails.
""")

    # Part 4: Check multiple PF orders at small t
    print("\n--- Part 4: Full PF spectrum at small t ---")
    u0, h = 0.01, 0.05
    for t in [0, 0.001, 0.01, 0.1, 0.5, 1.0]:
        print(f"\n  t = {t}:")
        kfunc = lambda u, tv=mpf(t): K_t(u, tv)
        for r in range(2, 8):
            d = toeplitz_det(kfunc, u0, h, r)
            s = "+" if d > 0 else "-"
            print(f"    D{r} = {float(d):>16.6e} [{s}]")

    # Part 5: Alternative approach - the de la Vallee-Poussin deformation
    # Instead of e^{tu^2}, consider multiplying by a sequence of PF_infinity kernels
    # that converge to the identity. E.g., K_epsilon(u) = (1/sqrt(4*pi*epsilon)) * exp(-u^2/(4*epsilon))
    # is PF_infinity and its convolution with Phi should improve PF order.
    print("\n--- Part 5: Convolution approach (smoothing kernel) ---")
    print("  Instead of multiplicative deformation e^{tu^2}, consider")
    print("  convolving with a Gaussian: (Phi * G_eps)(u)")
    print("  where G_eps(u) = (1/sqrt(4*pi*eps)) * exp(-u^2/(4*eps))")
    print("")
    print("  Convolution preserves PF order (Karlin's composition formula):")
    print("  If A is PF_r and B is PF_s, then A*B is PF_{min(r,s)}")
    print("")
    print("  Since G_eps is PF_infinity and Phi is PF_4,")
    print("  the convolution Phi * G_eps is at least PF_4.")
    print("")
    print("  But wait — this CANNOT improve PF order beyond PF_4!")
    print("  The composition formula gives PF_{min(4, infinity)} = PF_4.")
    print("")
    print("  So convolution with a PF_infinity kernel PRESERVES but does not")
    print("  IMPROVE the PF order. This is a dead end for this direction.")
    print("")
    print("  The multiplicative deformation e^{tu^2} is NOT a convolution.")
    print("  In fact, multiplication by e^{tu^2} in the u-domain corresponds")
    print("  to convolution with a Gaussian in the FREQUENCY domain.")
    print("  This is why it can change PF properties non-monotonically.")

    # Part 6: Asymptotic expansion of D5 in powers of t
    print("\n--- Part 6: Taylor expansion of D5(t) around t=0 ---")
    u0, h = 0.01, 0.05
    # D5(t) = D5(0) + t * D5'(0) + t^2/2 * D5''(0) + ...
    # Compute numerically via Richardson extrapolation

    eps_values = [mpf('0.001'), mpf('0.0005'), mpf('0.0001')]

    # First derivative: D5'(0) ~ [D5(eps) - D5(-eps)] / (2*eps)
    # But t >= 0, so use forward differences
    # D5'(0) ~ [D5(eps) - D5(0)] / eps
    d5_0 = toeplitz_det(lambda u: K_t(u, 0), u0, h, 5)
    print(f"  D5(0) = {float(d5_0):.10e}")

    derivs = []
    for eps in eps_values:
        d5_eps = toeplitz_det(lambda u: K_t(u, eps), u0, h, 5)
        deriv1 = (d5_eps - d5_0) / eps
        derivs.append(float(deriv1))
        print(f"  eps={float(eps):.4f}: D5'(0) ~ {float(deriv1):.10e}")

    # Second derivative via central difference
    print(f"\n  Second derivative (forward):")
    for eps in eps_values:
        d5_eps = toeplitz_det(lambda u: K_t(u, eps), u0, h, 5)
        d5_2eps = toeplitz_det(lambda u: K_t(u, 2*eps), u0, h, 5)
        deriv2 = (d5_2eps - 2*d5_eps + d5_0) / eps**2
        print(f"  eps={float(eps):.4f}: D5''(0) ~ {float(deriv2):.10e}")

    # Part 7: The quadratic approximation
    print("\n--- Part 7: When does the Taylor approximation predict D5 = 0? ---")
    # D5(t) ~ D5(0) + t * D5'(0)
    # D5(t) = 0 when t = -D5(0) / D5'(0)
    if derivs:
        d5_prime = derivs[-1]  # Use the most accurate derivative
        if d5_prime > 0:
            t_zero_linear = -float(d5_0) / d5_prime
            print(f"  D5(0) = {float(d5_0):.6e}")
            print(f"  D5'(0) ~ {d5_prime:.6e}")
            print(f"  Linear prediction: D5 = 0 at t ~ {t_zero_linear:.6e}")
            print(f"  (Compare: Lambda in [0, 0.2])")
        else:
            print(f"  D5'(0) ~ {d5_prime:.6e} (NEGATIVE — heat flow makes D5 MORE negative!)")
            print(f"  This means PF5 gets WORSE before it gets better.")

    # Save
    outfile = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf5-perturbation/inv4_results.json"
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")


if __name__ == "__main__":
    main()
