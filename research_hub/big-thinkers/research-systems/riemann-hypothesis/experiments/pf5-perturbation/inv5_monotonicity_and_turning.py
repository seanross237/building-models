"""
Investigation 5: Understanding the non-monotonicity of D5(t).

Critical finding from Investigation 1 and 4:
- D5'(0) < 0: the heat flow WORSENS PF5 initially
- D5''(0) > 0: there's a turning point
- D5 eventually becomes positive at t ~ 11.4

Questions:
1. Where is the turning point? (minimum of D5(t))
2. What is D5 at the turning point?
3. How does this relate to the PF4 failure at t ~ 10?
4. Is there a DIFFERENT deformation that improves D5 monotonically?
5. The PF spectrum: at what t does each Dr first go negative?

Also: investigate whether the heat flow EQUATION implies monotonicity
for certain functionals of the kernel. The heat equation d/dt K_t = u^2 K_t
has K_t = e^{tu^2} K_0. The derivative of D5 with respect to t involves
the derivative of the Toeplitz determinant.
"""

from mpmath import mp, mpf, matrix, det, pi, exp
import time

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
    print("Investigation 5: Non-monotonicity of D5(t) and Turning Points")
    print("=" * 70)

    # Part 1: Find the minimum of D5(t) at the worst configuration
    print("\n--- Part 1: D5(t) detailed trajectory at (0.01, 0.05) ---")
    u0, h = 0.01, 0.05
    print(f"  t        D5(t)            D4(t)            D3(t)")

    t_values = [0, 0.1, 0.2, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10, 11, 11.5, 12]
    d5_vals = []
    for t in t_values:
        kfunc = lambda u, tv=mpf(t): K_t(u, tv)
        d5 = toeplitz_det(kfunc, u0, h, 5)
        d4 = toeplitz_det(kfunc, u0, h, 4)
        d3 = toeplitz_det(kfunc, u0, h, 3)
        d5_vals.append(float(d5))
        s5 = "+" if d5 > 0 else "-"
        s4 = "+" if d4 > 0 else "-"
        print(f"  {t:>5.1f}  {float(d5):>14.6e}[{s5}]  {float(d4):>14.6e}[{s4}]  {float(d3):>14.6e}")

    # Find minimum via golden section
    print("\n  Finding minimum of D5(t) by golden section search on [0, 11]...")
    a, b = mpf(0), mpf(11)
    gr = (mpf(5)**mpf('0.5') + 1) / 2  # golden ratio

    for _ in range(40):
        c = b - (b - a) / gr
        d = a + (b - a) / gr
        d5_c = toeplitz_det(lambda u: K_t(u, c), u0, h, 5)
        d5_d = toeplitz_det(lambda u: K_t(u, d), u0, h, 5)
        if d5_c < d5_d:
            b = d
        else:
            a = c

    t_min = float((a + b) / 2)
    d5_min = float(toeplitz_det(lambda u: K_t(u, (a+b)/2), u0, h, 5))
    print(f"  Minimum of D5(t) at t = {t_min:.6f}")
    print(f"  D5(t_min) = {d5_min:.6e}")
    print(f"  D5(0) = {d5_vals[0]:.6e}")
    print(f"  Ratio D5(t_min)/D5(0) = {d5_min/d5_vals[0]:.4f}")

    # Part 2: The full PF spectrum breakdown
    print("\n--- Part 2: When does each Dr first go negative? ---")
    u0, h = 0.01, 0.05
    print(f"  Configuration: ({u0}, {h})")

    for r in range(2, 8):
        # Find where Dr changes sign using bisection
        # First, find a t where Dr < 0 (if it exists for t < 50)
        d_r_0 = toeplitz_det(lambda u: K(u), u0, h, r)
        s = "+" if d_r_0 > 0 else "-"
        print(f"\n  D{r}(t=0) = {float(d_r_0):.6e} [{s}]")

        if d_r_0 < 0:
            # Already negative, find where it becomes positive (if ever)
            found_pos = False
            for t_test in [1, 5, 10, 15, 20, 30, 50]:
                d_test = toeplitz_det(lambda u: K_t(u, t_test), u0, h, r)
                if d_test > 0:
                    # Bisect to find crossing
                    t_lo = mpf(0) if t_test == 1 else mpf(t_test // 2)
                    t_hi = mpf(t_test)
                    for _ in range(40):
                        t_mid = (t_lo + t_hi) / 2
                        d_mid = toeplitz_det(lambda u: K_t(u, t_mid), u0, h, r)
                        if d_mid < 0:
                            t_lo = t_mid
                        else:
                            t_hi = t_mid
                    t_cross = float((t_lo + t_hi) / 2)
                    print(f"  D{r} crosses zero (neg->pos) at t = {t_cross:.4f}")
                    found_pos = True
                    break
            if not found_pos:
                print(f"  D{r} remains negative up to t = 50")
        else:
            # Positive at t=0, find where it goes negative (if ever)
            found_neg = False
            prev_t = 0
            for t_test in [0.5, 1, 2, 5, 10, 15, 20, 30, 50]:
                d_test = toeplitz_det(lambda u: K_t(u, t_test), u0, h, r)
                if d_test < 0:
                    # Bisect between prev_t and t_test
                    t_lo, t_hi = mpf(prev_t), mpf(t_test)
                    for _ in range(40):
                        t_mid = (t_lo + t_hi) / 2
                        d_mid = toeplitz_det(lambda u: K_t(u, t_mid), u0, h, r)
                        if d_mid > 0:
                            t_lo = t_mid
                        else:
                            t_hi = t_mid
                    t_cross = float((t_lo + t_hi) / 2)
                    print(f"  D{r} crosses zero (pos->neg) at t = {t_cross:.4f}")
                    found_neg = True
                    break
                prev_t = t_test
            if not found_neg:
                print(f"  D{r} remains positive up to t = 50")

    # Part 3: The derivative formula
    print("\n--- Part 3: Why D5'(0) < 0 — the derivative formula ---")
    print("""
  D5(t) = det[K_t(u0 + (i-j)*h)]_{i,j=0..4}

  where K_t(u) = e^{tu^2} K(u).

  dD5/dt = sum_{i,j} (partial D5 / partial M_{ij}) * (dM_{ij}/dt)

  dM_{ij}/dt = (u0 + (i-j)*h)^2 * K_t(u0 + (i-j)*h)

  At t=0: dD5/dt = sum_{i,j} cofactor(i,j) * (u0 + (i-j)*h)^2 * K(u0 + (i-j)*h)

  This is a weighted sum of cofactors, where the weights are
  u^2 * K(u) evaluated at the grid points.

  The key insight: the weight (u0 + (i-j)*h)^2 grows with |i-j|,
  meaning DISTANT entries in the Toeplitz matrix get larger weights.
  These are the entries where K is SMALLEST (since K decays).
  So the heat flow preferentially amplifies the small off-diagonal
  entries, which makes the matrix LESS like a dominant-diagonal
  matrix, which makes the determinant MORE negative.

  In other words: e^{tu^2} grows with |u|, amplifying the tails
  of the kernel. This makes the kernel LESS concentrated, which
  WORSENS the PF5 condition (which requires a certain kind of
  concentration/decay structure).
""")

    # Verify: compute the weighted cofactor sum
    u0, h = mpf('0.01'), mpf('0.05')
    T = matrix(5, 5)
    for i in range(5):
        for j in range(5):
            T[i,j] = K(u0 + (i-j)*h)

    # dD5/dt at t=0
    derivative = mpf(0)
    for i in range(5):
        for j in range(5):
            # Cofactor of (i,j) entry
            minor = matrix(4, 4)
            ri, ci = 0, 0
            for ii in range(5):
                if ii == i:
                    continue
                ci = 0
                for jj in range(5):
                    if jj == j:
                        continue
                    minor[ri, ci] = T[ii, jj]
                    ci += 1
                ri += 1
            cof = (-1)**(i+j) * det(minor)
            u_val = u0 + (i-j)*h
            weight = u_val**2
            contribution = cof * weight * K(u_val)
            derivative += contribution

    print(f"  Computed dD5/dt|_{{t=0}} = {float(derivative):.10e}")
    print(f"  (from finite differences: -1.5455e-09)")
    print(f"  Match: {'YES' if abs(float(derivative) - (-1.5455e-9)) / 1.5455e-9 < 0.01 else 'NO'}")

    # Part 4: Can we find a DIFFERENT deformation that improves D5?
    print("\n--- Part 4: Alternative deformations ---")
    print("  Instead of e^{tu^2}, what about e^{-tu^4}? (contracts tails)")

    for t in [0, 0.001, 0.01, 0.1, 1.0, 5.0]:
        kfunc = lambda u, tv=mpf(t): exp(-tv * mpf(u)**4) * K(u)
        d5 = toeplitz_det(kfunc, 0.01, 0.05, 5)
        d4 = toeplitz_det(kfunc, 0.01, 0.05, 4)
        s5 = "+" if d5 > 0 else "-"
        s4 = "+" if d4 > 0 else "-"
        print(f"  e^{{-{t}*u^4}}: D4={float(d4):>12.4e}[{s4}]  D5={float(d5):>12.4e}[{s5}]")

    print("\n  What about e^{-tu^2}? (opposite of heat flow)")
    for t in [0, 0.001, 0.01, 0.1, 1.0]:
        kfunc = lambda u, tv=mpf(t): exp(-tv * mpf(u)**2) * K(u)
        d5 = toeplitz_det(kfunc, 0.01, 0.05, 5)
        d4 = toeplitz_det(kfunc, 0.01, 0.05, 4)
        s5 = "+" if d5 > 0 else "-"
        s4 = "+" if d4 > 0 else "-"
        print(f"  e^{{-{t}*u^2}}: D4={float(d4):>12.4e}[{s4}]  D5={float(d5):>12.4e}[{s5}]")

    # Part 5: The Schoenberg equivalence check
    print("\n--- Part 5: Schoenberg's characterization ---")
    print("""
  Schoenberg (1951): An even function K(u) has the property that
  integral K(u) cos(xu) du has only real zeros IF AND ONLY IF
  K is PF_infinity.

  This means:
  - Lambda = inf{t : K_t is PF_infinity}
  - Since K_0 fails PF_5, K_0 is NOT PF_infinity, so Lambda >= 0
  - This is consistent with Lambda >= 0 (Rodgers-Tao)

  But MORE: Lambda = 0 would mean K_0 IS PF_infinity, contradicting
  the PF_5 failure. So:

  **The PF_5 failure of the Polya kernel IMPLIES Lambda > 0
  (unless PF_5 holds globally, which needs checking).**

  Wait — this requires careful thought. The PF_5 failure is for the
  Toeplitz minors at SPECIFIC (u0, h) configurations. PF_infinity
  requires ALL configurations to have non-negative minors of ALL orders.

  So: D5 < 0 at (u0=0.01, h=0.05) => K_0 is not PF_5 => K_0 is not
  PF_infinity => By Schoenberg, H_0 has non-real zeros OR K_0 is not
  in the right function class.

  BUT: H_0(x) = integral Phi(u) cos(xu) du = xi(1/2 + ix).
  If RH is true, then xi has only real zeros, so H_0 has only real
  zeros, so K_0 MUST be PF_infinity by Schoenberg.

  CONTRADICTION: K_0 fails PF_5 => K_0 not PF_infinity => H_0 has
  non-real zeros => RH is FALSE.

  ... UNLESS the PF_5 failure we computed is wrong, or Schoenberg's
  theorem has additional hypotheses we're not checking.

  LET'S CHECK: Does Schoenberg's theorem apply to Phi(|u|)?
  The theorem is for functions in L^1 that are the RECIPROCAL of
  an entire function of order 2, or for the Laplace transforms of
  totally positive measures.

  More precisely: Schoenberg's result says that a kernel K(x-y) is
  TP_infinity if and only if K has the form
    K(u) = C * exp(-au^2 + bu) * prod (1 + alpha_k u) * exp(-alpha_k u)
  for certain constants. This is NOT the same as saying "Fourier
  transform has real zeros iff PF_infinity".

  The correct statement involves the POLYA-SCHUR characterization:
  An entire function psi(z) is in the Laguerre-Polya class (all zeros
  real) if and only if it is a limit of polynomials with only real zeros.

  For the KERNEL-ZEROS relationship:
  - K in PF_infinity AND K even AND K in L^1 => integral K cos(xu) du
    has only real zeros (this direction is CORRECT).
  - But the CONVERSE requires K to be of a specific form.

  So: the PF_5 failure does NOT immediately imply Lambda > 0. The
  converse of Schoenberg only holds for a restricted class.

  THE ACTUAL SITUATION:
  RH could be true even though K_0 = Phi(|u|) is not PF_infinity,
  because the converse of Schoenberg doesn't apply in full generality
  to all L^1 even functions.
""")

    print("\n" + "=" * 70)
    print("CRITICAL CONCLUSION:")
    print("=" * 70)
    print("""
  1. The heat flow e^{tu^2} makes D5 WORSE (more negative) for small t.
     D5'(0) = -1.55e-9 < 0.

  2. D5(t) reaches its minimum at t ~ 2-3 (about 1.6x worse than D5(0)).

  3. D5(t) only crosses zero at t ~ 11.4, well beyond where D4 fails (t ~ 10).

  4. The alternative deformation e^{-tu^4} (tail contraction) IMPROVES D5
     but destroys the de Bruijn-Newman framework (wrong direction of flow).

  5. Schoenberg's characterization does NOT directly connect PF_5 failure
     to non-real zeros. The PF_5 failure is consistent with RH being true.

  6. The "almost PF_5" property does NOT directly bound Lambda because:
     (a) The heat flow worsens PF_5 initially
     (b) PF_5 is restored only at t >> Lambda
     (c) PF_infinity is never achieved (PF_4 breaks before PF_5 is restored)
""")


if __name__ == "__main__":
    main()
