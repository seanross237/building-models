"""
Investigation 6: The Reverse Heat Flow Discovery and Schoenberg Analysis.

CRITICAL FINDING from Investigation 5:
The REVERSE heat flow e^{-tu^2} IMPROVES D5. At t = 1.0, D5 turns positive!

This is the OPPOSITE direction from the de Bruijn-Newman parameter.
Let K_{-t}(u) = e^{-tu^2} * Phi(|u|) for t > 0.

Questions:
1. At what t does D5 cross zero under reverse heat flow?
2. Does D5 stay positive for larger t?
3. What happens to D6 under reverse heat flow?
4. Can we achieve PF_infinity under sufficiently strong reverse heat flow?
5. What does this mean for Lambda?

Key insight: If K_{-t} = e^{-tu^2} * Phi(|u|), then
H_{-t}(x) = integral e^{-tu^2} Phi(u) cos(xu) du

This corresponds to the de Bruijn-Newman parameter at NEGATIVE t.
Lambda <= 0 iff H_t has all real zeros for all t >= 0.
Lambda = -delta iff H_t has all real zeros for t >= -delta.

If K_{-t} is PF_infinity for some t > 0, then H_{-t} has all real zeros,
which means Lambda <= -t < 0. This would PROVE RH (since RH <=> Lambda <= 0).

BUT: does PF_infinity of K_{-t} follow from PF of each order?
We need to check ALL orders, not just 5 and 6.

Also: Schoenberg's theorem. The converse direction needs careful analysis.
"""

from mpmath import mp, mpf, matrix, det, pi, exp
import time
import json

mp.dps = 80

def phi_term(n, u):
    n = mpf(n)
    u = mpf(u)
    return (2*pi**2*n**4*exp(9*u) - 3*pi*n**2*exp(5*u)) * exp(-pi*n**2*exp(4*u))

def phi(u, N=50):
    u = mpf(u)
    return sum(phi_term(n, u) for n in range(1, N+1))

def K(u, N=50):
    return phi(abs(mpf(u)), N)

def K_neg_t(u, t, N=50):
    """Reverse heat flow: K_{-t}(u) = e^{-tu^2} Phi(|u|)."""
    u_mpf = mpf(u)
    t_mpf = mpf(t)
    return exp(-t_mpf * u_mpf**2) * K(u, N)

def toeplitz_det(kfunc, u0, h, r):
    u0, h = mpf(u0), mpf(h)
    M = matrix(r, r)
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return det(M)


def main():
    print("=" * 70)
    print("Investigation 6: Reverse Heat Flow and Schoenberg Analysis")
    print("=" * 70)

    results = {}

    # Part 1: D5 under reverse heat flow at multiple configurations
    print("\n--- Part 1: D5 under reverse heat flow ---")

    configs = [
        (0.001, 0.05),
        (0.01, 0.05),
        (0.001, 0.01),
        (0.02, 0.05),
        (0.03, 0.035),
    ]

    t_values = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0]

    for u0, h in configs:
        print(f"\n  Config ({u0}, {h}):")
        print(f"    {'t':>6} {'D5':>16} {'D4':>16} {'D3':>16} {'D2':>16}")
        for t in t_values:
            kfunc = lambda u, tv=mpf(t): K_neg_t(u, tv)
            d5 = toeplitz_det(kfunc, u0, h, 5)
            d4 = toeplitz_det(kfunc, u0, h, 4)
            d3 = toeplitz_det(kfunc, u0, h, 3)
            d2 = toeplitz_det(kfunc, u0, h, 2)
            s5 = "+" if d5 > 0 else "-"
            s4 = "+" if d4 > 0 else "-"
            s3 = "+" if d3 > 0 else "-"
            s2 = "+" if d2 > 0 else "-"
            print(f"    {t:>6.2f} {float(d5):>14.6e}[{s5}] {float(d4):>14.6e}[{s4}] {float(d3):>14.6e}[{s3}] {float(d2):>14.6e}[{s2}]")

    # Part 2: Find exact t where D5 crosses zero under reverse heat flow
    print("\n--- Part 2: Exact crossing point for D5 under reverse heat flow ---")
    for u0, h in configs[:3]:
        d5_0 = toeplitz_det(lambda u: K(u), u0, h, 5)
        if d5_0 >= 0:
            print(f"  ({u0}, {h}): D5 already >= 0 at t=0")
            continue

        # Check D5 at t=1
        d5_1 = toeplitz_det(lambda u: K_neg_t(u, 1), u0, h, 5)
        if d5_1 < 0:
            # Need larger t
            t_hi = mpf(5)
        else:
            t_hi = mpf(1)

        # Bisect
        t_lo = mpf(0)
        for _ in range(60):
            t_mid = (t_lo + t_hi) / 2
            d5_mid = toeplitz_det(lambda u: K_neg_t(u, t_mid), u0, h, 5)
            if d5_mid < 0:
                t_lo = t_mid
            else:
                t_hi = t_mid
        t_cross = float((t_lo + t_hi) / 2)
        print(f"  ({u0}, {h}): D5 crosses zero at reverse t = {t_cross:.10f}")
        results[f"({u0},{h})_reverse_cross"] = t_cross

    # Part 3: Full PF spectrum under reverse heat flow
    print("\n--- Part 3: Full PF spectrum under reverse heat flow ---")
    u0, h = 0.01, 0.05
    for t in [0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        print(f"\n  Reverse t = {t}:")
        kfunc = lambda u, tv=mpf(t): K_neg_t(u, tv)
        for r in range(2, 9):
            d = toeplitz_det(kfunc, u0, h, r)
            s = "+" if d > 0 else "-"
            print(f"    D{r} = {float(d):>16.6e} [{s}]")

    # Part 4: Does reverse heat flow achieve PF_infinity?
    print("\n--- Part 4: Higher orders under reverse heat flow ---")
    print("  Testing up to D10 at reverse t = 1.0, (u0=0.01, h=0.05)")
    kfunc = lambda u: K_neg_t(u, 1.0)
    u0, h = 0.01, 0.05
    for r in range(2, 11):
        t0 = time.time()
        d = toeplitz_det(kfunc, u0, h, r)
        t1 = time.time()
        s = "+" if d > 0 else "-"
        print(f"  D{r} = {float(d):>16.6e} [{s}]  ({t1-t0:.1f}s)")

    # Part 5: Scan more configurations at reverse t=1
    print("\n--- Part 5: D5-D8 at reverse t=1.0 across many configs ---")
    scan_configs = []
    for u0 in [0.001, 0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5]:
        for h in [0.01, 0.03, 0.05, 0.1, 0.2]:
            scan_configs.append((u0, h))

    print(f"  Scanning {len(scan_configs)} configs...")
    failures = {5: 0, 6: 0, 7: 0, 8: 0}
    total = len(scan_configs)
    kfunc = lambda u: K_neg_t(u, 1.0)

    for u0, h in scan_configs:
        signs = {}
        for r in [5, 6, 7, 8]:
            d = toeplitz_det(kfunc, u0, h, r)
            signs[r] = "+" if d > 0 else "-"
            if d < 0:
                failures[r] += 1

        if any(s == "-" for s in signs.values()):
            sig = "".join(signs[r] for r in [5,6,7,8])
            print(f"    ({u0:.3f}, {h:.3f}): D5..D8 = [{sig}]")

    print(f"\n  Summary at reverse t = 1.0:")
    for r in [5, 6, 7, 8]:
        print(f"    D{r} failures: {failures[r]}/{total}")

    # Part 6: The Schoenberg converse — careful analysis
    print("\n--- Part 6: Schoenberg's Theorem — Precise Statement ---")
    print("""
  THEOREM (Schoenberg, 1951, refined by Karlin):
  Let K: R -> R be a continuous, even, integrable function. Define
    hat{K}(x) = integral_{-inf}^{inf} K(u) e^{ixu} du

  Then the following are equivalent:
  (i)  K(u) = c * exp(-alpha * u^2) * prod_k (cosh(beta_k * u))^{-1}
       for some c > 0, alpha >= 0, sum beta_k^2 < inf
       [This is the "Polya frequency function" characterization]
  (ii) K is totally positive of order infinity (PF_infinity)
  (iii) 1/hat{K}(x) is an entire function of order <= 2, genus 0 or 1,
        with only REAL zeros

  Note: (iii) says 1/hat{K} has real zeros, NOT that hat{K} has real zeros.
  hat{K} having real zeros is a DIFFERENT condition.

  For the Polya kernel K(u) = Phi(|u|):
  - hat{K}(x) = 2 * integral_0^inf Phi(u) cos(xu) du = xi(1/2 + ix)
  - RH says xi has only real zeros, i.e., hat{K} has only real zeros
  - Schoenberg says: K is PF_inf iff 1/hat{K} has only real zeros
  - These are DIFFERENT conditions!

  hat{K} having only real zeros does NOT imply 1/hat{K} has only real zeros.
  In fact, since xi(s) has infinitely many zeros, 1/xi(s) has infinitely
  many POLES, which are at the zeros of xi. The function 1/xi is NOT entire.

  So Schoenberg's theorem does NOT directly apply in the way we were hoping.
  The PF characterization is about 1/hat{K} being entire with real zeros,
  not hat{K} having real zeros.

  CONCLUSION: The PF_5 failure of Phi(|u|) does NOT imply RH is false.
  It simply means Phi(|u|) is not a Polya frequency function, which is
  a statement about the structure of 1/xi, not about xi itself.

  However, there IS a related result:
  If K is PF_infinity, then hat{K} = c * exp(-alpha*x^2) / g(x)
  where g(x) has only real zeros. This means hat{K} has NO zeros
  (it's non-vanishing). So PF_infinity would imply xi is NON-VANISHING,
  which contradicts the known existence of zeros of xi.

  WAIT: This means Phi(|u|) CANNOT be PF_infinity, because xi has
  zeros. The PF_5 failure is not a bug — it's a FEATURE. The kernel
  must fail PF_infinity because the Fourier transform has zeros.

  This is a fundamental insight: PF_infinity of the kernel implies
  the Fourier transform is ZERO-FREE. Since xi has infinitely many
  zeros, Phi(|u|) necessarily fails PF_infinity. The question is
  at what ORDER it first fails, and what that failure means.
""")

    # Part 7: Recalibrate — what does the PF hierarchy really tell us?
    print("\n--- Part 7: Recalibrated Understanding ---")
    print("""
  CORRECT INTERPRETATION of the PF hierarchy:

  1. K in PF_infinity => hat{K} is zero-free (never zero)
  2. Phi(|u|) has hat{K} = xi with infinitely many zeros
  3. Therefore Phi(|u|) CANNOT be PF_infinity
  4. The PF_5 failure is NECESSARY, not a "near-miss"

  The question is not "can we make the kernel PF_infinity" but rather
  "what does the PF ORDER tell us about the SPACING and DISTRIBUTION
  of zeros of xi?"

  Higher PF order means the kernel is "closer to" having a zero-free
  Fourier transform, in a specific sense:
  - PF_2 (log-concavity) constrains 2-point correlations of zero positions
  - PF_4 constrains 4-point correlations
  - The failure at PF_5 is related to 5-point correlations of zero positions

  For RH: we need zeros to lie on a LINE (Re(s) = 1/2), not to be absent.
  PF theory says something about zeros being absent (for PF_infinity).
  So the PF approach is fundamentally about the WRONG question for RH.

  HOWEVER: The de Bruijn-Newman framework uses PF properties of K_t,
  not of K_0. The parameter t controls the "temperature" of the system.
  At t = Lambda, the function H_t first has all real zeros. But this
  does NOT mean K_Lambda is PF_infinity — it means H_Lambda has real zeros
  by a different mechanism (not through PF characterization).

  The REAL value of PF analysis:
  - PF_4 constrains the kernel's shape in ways relevant to zero distribution
  - The near-PF_5 property might imply constraints on the IMAGINARY parts
    of zeros (if any exist off the critical line)
  - But this requires new theory connecting finite PF order to zero location
""")

    # Part 8: Final verification — D6 at t=0 and under reverse flow
    print("\n--- Part 8: D6 behavior (also negative at t=0) ---")
    # D6 is negative at (0.01, 0.05). When does it cross under reverse flow?
    for u0, h in [(0.01, 0.05), (0.001, 0.05)]:
        d6_0 = toeplitz_det(lambda u: K(u), u0, h, 6)
        print(f"\n  Config ({u0}, {h}): D6(0) = {float(d6_0):.6e}")

        if d6_0 < 0:
            # Check if reverse flow fixes it
            t_vals_check = [0.5, 1.0, 2.0, 5.0]
            for t in t_vals_check:
                d6_t = toeplitz_det(lambda u: K_neg_t(u, t), u0, h, 6)
                s = "+" if d6_t > 0 else "-"
                print(f"    reverse t={t}: D6 = {float(d6_t):.6e} [{s}]")

            # Bisect
            t_lo, t_hi = mpf(0), mpf(5)
            d6_hi = toeplitz_det(lambda u: K_neg_t(u, t_hi), u0, h, 6)
            if d6_hi > 0:
                for _ in range(50):
                    t_mid = (t_lo + t_hi) / 2
                    d6_mid = toeplitz_det(lambda u: K_neg_t(u, t_mid), u0, h, 6)
                    if d6_mid < 0:
                        t_lo = t_mid
                    else:
                        t_hi = t_mid
                t_cross = float((t_lo + t_hi) / 2)
                print(f"    D6 crosses zero at reverse t = {t_cross:.6f}")

    # Save
    outfile = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/pf5-perturbation/inv6_results.json"
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")


if __name__ == "__main__":
    main()
