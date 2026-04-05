"""
Experiment 2: Symmetry-Preserving Truncations of Xi

Xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s) satisfies Xi(s) = Xi(1-s).
Xi(1/2 + it) = sum_{n=0}^{inf} a_{2n} t^{2n}  (even Taylor series with real coefficients)

We study truncated Xi polynomials and check whether their zeros stay on sigma = 1/2.
"""

import numpy as np
from mpmath import mp, mpf, mpc, gamma, pi, zeta, diff, findroot, fabs, log, sqrt, exp, taylor, zetazero

mp.dps = 30

def Xi(s):
    """The completed Riemann Xi function: Xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s)"""
    return mpf('0.5') * s * (s - 1) * pi**(-s/2) * gamma(s/2) * zeta(s)

def xi_of_t(t):
    """Xi(1/2 + it) as a function of real t"""
    s = mpc('0.5', t)
    return Xi(s)

# ============================================================
# Compute Taylor coefficients
# ============================================================

print("=" * 70)
print("Xi Taylor Polynomial Truncation Experiment")
print("=" * 70)

print("\nComputing Xi Taylor coefficients...")
max_terms = 15
coeffs_raw = taylor(xi_of_t, 0, 2*max_terms)
# Extract even coefficients (Xi(1/2+it) is even in t)
coeffs = []
for k in range(max_terms + 1):
    if 2*k < len(coeffs_raw):
        c = float(coeffs_raw[2*k].real) if hasattr(coeffs_raw[2*k], 'real') else float(coeffs_raw[2*k])
        coeffs.append(c)
    else:
        coeffs.append(0.0)

print("\nCoefficients a_{2k} where Xi(1/2+it) = sum a_{2k} * t^{2k}:")
for k, c in enumerate(coeffs):
    if abs(c) > 1e-30:
        print(f"  a_{2*k:>2} = {c:>15.6e}")

# Check sign alternation 
signs = [np.sign(c) for c in coeffs if abs(c) > 1e-30]
alternating = all(signs[i] * signs[i+1] < 0 for i in range(len(signs)-1))
print(f"\nSign alternation: {['+' if s > 0 else '-' for s in signs]}")
print(f"Strictly alternating: {alternating}")

# ============================================================
# Find zeros of truncated polynomials
# ============================================================

print("\n" + "=" * 70)
print("ZEROS OF TRUNCATED Xi POLYNOMIALS")
print("=" * 70)

for N_terms in [3, 5, 8, 10, 12, 15]:
    if N_terms > len(coeffs) - 1:
        continue
    poly_coeffs = coeffs[:N_terms+1]
    
    # P(u) = sum_{k=0}^{N} a_{2k} * u^k where u = t^2
    # numpy roots wants highest power first
    np_coeffs = list(reversed(poly_coeffs))
    u_roots = np.roots(np_coeffs)
    
    real_positive = 0
    real_negative = 0
    complex_roots = 0
    
    t_on_line = []
    
    for u in u_roots:
        if abs(u.imag) < 1e-6 * max(abs(u.real), 1e-10):
            if u.real > 0:
                real_positive += 1
                t_on_line.append(np.sqrt(u.real))
            else:
                real_negative += 1
        else:
            complex_roots += 1
    
    t_on_line.sort()
    
    print(f"\nN = {N_terms} terms (poly degree {N_terms} in u = t^2, degree {2*N_terms} in t):")
    print(f"  u-roots: {len(u_roots)} total")
    print(f"    Real positive (zeros ON sigma=1/2): {real_positive}")
    print(f"    Real negative (zeros on real axis, OFF sigma=1/2): {real_negative}")
    print(f"    Complex (zeros OFF sigma=1/2): {complex_roots}")
    
    pct = 100.0 * real_positive / N_terms
    print(f"  Fraction on critical line: {real_positive}/{N_terms} = {pct:.1f}%")
    
    if t_on_line:
        print(f"  t-values on critical line: {[f'{t:.3f}' for t in t_on_line[:10]]}")
        # Compare with true zeros
        true_zeros_t = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738]
        n_match = min(len(t_on_line), len(true_zeros_t))
        if n_match > 0:
            print(f"  True zeros:                {[f'{t:.3f}' for t in true_zeros_t[:n_match]]}")
            errors = [abs(t_on_line[i] - true_zeros_t[i]) for i in range(min(n_match, len(t_on_line)))]
            print(f"  Errors:                    {[f'{e:.3f}' for e in errors]}")


# ============================================================
# Now check: as we increase N, do MORE roots become real positive?
# ============================================================

print("\n" + "=" * 70)
print("CONVERGENCE: Fraction of zeros on critical line vs N")
print("=" * 70)
print(f"{'N':>4} | {'Total u-roots':>14} | {'On line':>8} | {'Off line':>9} | {'% on line':>10}")
print("-" * 55)

for N_terms in range(2, max_terms+1):
    if N_terms > len(coeffs) - 1:
        break
    poly_coeffs = coeffs[:N_terms+1]
    np_coeffs = list(reversed(poly_coeffs))
    u_roots = np.roots(np_coeffs)
    
    on_line = sum(1 for u in u_roots if abs(u.imag) < 1e-6 * max(abs(u.real), 1e-10) and u.real > 0)
    off_line = N_terms - on_line
    pct = 100.0 * on_line / N_terms
    
    print(f"{N_terms:>4} | {N_terms:>14} | {on_line:>8} | {off_line:>9} | {pct:>9.1f}%")

# ============================================================
# Key question: for the Xi polynomial, do OFF-LINE zeros respect s <-> 1-s?
# ============================================================

print("\n" + "=" * 70)
print("STRUCTURE OF OFF-LINE ZEROS (N=10)")
print("=" * 70)

N_terms = 10
poly_coeffs = coeffs[:N_terms+1]
np_coeffs = list(reversed(poly_coeffs))
u_roots = np.roots(np_coeffs)
u_roots_sorted = sorted(u_roots, key=lambda u: (abs(u.imag), u.real))

for i, u in enumerate(u_roots_sorted):
    if abs(u.imag) < 1e-6 * max(abs(u.real), 1e-10):
        u_real = u.real
        if u_real > 0:
            t_val = np.sqrt(u_real)
            print(f"  u = {u_real:>12.3f}  => t = ±{t_val:.3f}  => s = 0.5 ± {t_val:.3f}i  [ON LINE]")
        else:
            y = np.sqrt(-u_real)
            print(f"  u = {u_real:>12.3f}  => t = ±{y:.3f}i  => s = {0.5+y:.3f} or {0.5-y:.3f}  [OFF, real axis, PAIRED by s<->1-s]")
    else:
        # Complex u = a + bi
        # t = sqrt(u) has two branches
        t1 = np.sqrt(u)
        t2 = -t1
        for t_c in [t1]:
            s_sigma = 0.5 - t_c.imag
            s_t = t_c.real
            s_conj_sigma = 0.5 + t_c.imag  # = 1 - s_sigma
            print(f"  u = {u.real:>10.3f} + {u.imag:>10.3f}i  => s = {s_sigma:.3f} + {s_t:.3f}i AND {s_conj_sigma:.3f} + {s_t:.3f}i  [OFF LINE, PAIRED]")

