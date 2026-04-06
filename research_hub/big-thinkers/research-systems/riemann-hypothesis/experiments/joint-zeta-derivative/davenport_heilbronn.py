"""
Investigation 4: Davenport-Heilbronn comparison.

The DH function is a Dirichlet series that satisfies a functional equation
but has zeros OFF the critical line. We compare:
1. The joint (L, L') distribution at sigma > 1/2
2. The derivative at known off-line zeros
3. Whether the chi-constraint is satisfied or violated at DH off-line zeros
"""

import mpmath
import json
import sys
import time
import math

mpmath.mp.dps = 30

# ============================================================
# Davenport-Heilbronn function construction
# ============================================================
# The DH function is defined as:
#   f(s) = (1-i*kappa)/2 * L(s, chi_5^+) + (1+i*kappa)/2 * L(s, chi_5^-)
# where chi_5 is the non-principal character mod 5, and
# kappa = (sqrt(10-2*sqrt(5)) - 2) / (sqrt(5) - 1)
#
# More commonly, it's constructed as:
#   f(s) = sum_{n=1}^{infty} a_n / n^s
# with specific coefficients that give a functional equation of the form
#   phi(s) = phi(1-s)
# where phi(s) = (pi/5)^{-s/2} Gamma(s/2) f(s)

def chi5_values():
    """Character values for the primitive character mod 5.
    chi(1)=1, chi(2)=i, chi(3)=-i, chi(4)=-1, chi(0)=0."""
    return {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}

def dh_coefficients(N):
    """Compute Davenport-Heilbronn coefficients a_1, ..., a_N.

    f(s) = sum a_n n^{-s}

    The DH function uses:
    a_n = (1 - i*kappa)/2 * chi_+(n) + (1 + i*kappa)/2 * chi_-(n)

    where chi_+ and chi_- are the two characters mod 5 with chi_+(2)=i, chi_-(2)=-i,
    and kappa is chosen so the functional equation holds.

    Actually, the standard form (e.g., Titchmarsh):
    kappa = (sqrt(10 - 2*sqrt(5)) - 2) / (sqrt(5) - 1)
    """
    sqrt5 = math.sqrt(5)
    kappa = (math.sqrt(10 - 2 * sqrt5) - 2) / (sqrt5 - 1)

    # chi_+ (n mod 5): {0:0, 1:1, 2:i, 3:-i, 4:-1}
    # chi_- (n mod 5): {0:0, 1:1, 2:-i, 3:i, 4:-1}
    chi_plus = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}
    chi_minus = {0: 0, 1: 1, 2: -1j, 3: 1j, 4: -1}

    alpha = (1 - 1j * kappa) / 2
    beta = (1 + 1j * kappa) / 2

    coeffs = []
    for n in range(1, N + 1):
        r = n % 5
        a_n = alpha * chi_plus[r] + beta * chi_minus[r]
        coeffs.append(a_n)

    return coeffs, kappa


def eval_dh(s, coeffs):
    """Evaluate DH function at complex s using partial Dirichlet series."""
    total = complex(0, 0)
    for n, a_n in enumerate(coeffs, 1):
        total += a_n * (n ** (-s))
    return total


def eval_dh_derivative(s, coeffs):
    """Evaluate DH function derivative at complex s."""
    total = complex(0, 0)
    for n, a_n in enumerate(coeffs, 1):
        total -= a_n * math.log(n) * (n ** (-s))
    return total


def eval_dh_mpmath(s, coeffs_mp):
    """High-precision evaluation."""
    total = mpmath.mpc(0, 0)
    for n, a_n in enumerate(coeffs_mp, 1):
        total += a_n * mpmath.power(n, -s)
    return total


def find_dh_zeros(sigma_range, t_range, coeffs, grid_size=200):
    """Find approximate zeros of DH by grid search + Newton refinement."""
    # Grid search
    candidates = []
    sigma_vals = [sigma_range[0] + i * (sigma_range[1] - sigma_range[0]) / grid_size
                  for i in range(grid_size + 1)]
    t_vals = [t_range[0] + i * (t_range[1] - t_range[0]) / grid_size
              for i in range(grid_size + 1)]

    for si, sigma in enumerate(sigma_vals):
        for ti, t in enumerate(t_vals):
            s = complex(sigma, t)
            val = eval_dh(s, coeffs)
            if abs(val) < 1.0:
                candidates.append((sigma, t, abs(val)))

    # Sort by magnitude
    candidates.sort(key=lambda x: x[2])

    # Newton refinement on top candidates
    zeros = []
    for sigma0, t0, _ in candidates[:50]:
        s = complex(sigma0, t0)
        for _ in range(50):
            val = eval_dh(s, coeffs)
            deriv = eval_dh_derivative(s, coeffs)
            if abs(deriv) < 1e-20:
                break
            s_new = s - val / deriv
            if abs(s_new - s) < 1e-12:
                s = s_new
                break
            s = s_new

        final_val = eval_dh(s, coeffs)
        if abs(final_val) < 1e-6 and s.real > 0.5 + 1e-6:
            # Check this isn't a duplicate
            is_dup = False
            for z in zeros:
                if abs(z[0] - s.real) < 0.01 and abs(z[1] - s.imag) < 0.01:
                    is_dup = True
                    break
            if not is_dup:
                zeros.append((s.real, s.imag, abs(final_val)))

    return zeros


def main():
    N_terms = 5000  # Number of terms in DH series
    coeffs, kappa = dh_coefficients(N_terms)

    print(f"Davenport-Heilbronn function with {N_terms} terms", file=sys.stderr)
    print(f"kappa = {kappa:.10f}", file=sys.stderr)

    # ============================================================
    # Step 1: Find off-line zeros of DH
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("STEP 1: Finding off-line zeros of DH function", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    # Known: DH has zeros near sigma=0.8, t ~ 10-30
    # Search in the region 0.5 < sigma < 1.0, 0 < t < 100
    zeros = find_dh_zeros((0.51, 0.99), (1, 100), coeffs, grid_size=300)

    print(f"\nFound {len(zeros)} off-line zeros:", file=sys.stderr)
    for sigma, t, residual in zeros:
        print(f"  sigma={sigma:.8f}, t={t:.8f}, |f|={residual:.2e}", file=sys.stderr)

    if len(zeros) == 0:
        # Try with more terms and wider search
        print("\nRetrying with wider search...", file=sys.stderr)
        zeros = find_dh_zeros((0.51, 0.99), (1, 200), coeffs, grid_size=500)
        print(f"Found {len(zeros)} zeros on retry", file=sys.stderr)
        for sigma, t, residual in zeros:
            print(f"  sigma={sigma:.8f}, t={t:.8f}, |f|={residual:.2e}", file=sys.stderr)

    # ============================================================
    # Step 2: Compute derivatives at off-line zeros
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("STEP 2: Derivatives at off-line zeros", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    zero_analysis = []
    for sigma, t, residual in zeros:
        s = complex(sigma, t)
        deriv = eval_dh_derivative(s, coeffs)

        # chi-constraint: what would the functional equation require?
        # DH satisfies phi(s) = phi(1-s) with phi(s) = (pi/5)^{-s/2} Gamma(s/2) f(s)
        # The chi factor for DH: |chi_DH(s)| ~ (5/pi)^{sigma-1/2} * |Gamma((1-s)/2)/Gamma(s/2)|
        # For large t: ~ (t/(2*pi/sqrt(5)))^{1/2-sigma} approximately

        # Compute chi_DH approximately
        chi_approx = (t / (2 * math.pi)) ** (0.5 - sigma)  # rough approximation

        analysis = {
            'sigma': sigma,
            't': t,
            'residual': residual,
            'derivative_abs': abs(deriv),
            'derivative_arg': math.atan2(deriv.imag, deriv.real),
            'chi_approx': chi_approx,
            'ratio_deriv_to_chi': abs(deriv) / chi_approx if chi_approx > 0 else float('inf'),
        }
        zero_analysis.append(analysis)

        print(f"\nZero at sigma={sigma:.6f}, t={t:.6f}:", file=sys.stderr)
        print(f"  |f'| = {abs(deriv):.6f}", file=sys.stderr)
        print(f"  |chi| ~ {chi_approx:.6f}", file=sys.stderr)
        print(f"  |f'|/|chi| = {analysis['ratio_deriv_to_chi']:.4f}", file=sys.stderr)
        print(f"  (If this is >> 1, the mirror derivative is large)", file=sys.stderr)

    # ============================================================
    # Step 3: Joint distribution survey for DH
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("STEP 3: Joint (f, f') distribution for DH at sigma > 1/2", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    dh_joint_results = {}
    for sigma in [0.6, 0.7, 0.8]:
        print(f"\nSurveying DH at sigma={sigma}...", file=sys.stderr)
        results = []
        for t in [i * 0.5 for i in range(20, 2000)]:  # t from 10 to 1000
            s = complex(sigma, t)
            val = eval_dh(s, coeffs)
            deriv = eval_dh_derivative(s, coeffs)
            results.append({
                't': t,
                'abs_f': abs(val),
                'abs_f_prime': abs(deriv),
            })

        dh_joint_results[sigma] = results

        # Conditional analysis
        abs_f_vals = [r['abs_f'] for r in results]
        abs_fp_vals = [r['abs_f_prime'] for r in results]

        # Correlation
        n = len(results)
        mean_f = sum(abs_f_vals) / n
        mean_fp = sum(abs_fp_vals) / n
        var_f = sum((x - mean_f)**2 for x in abs_f_vals) / n
        var_fp = sum((x - mean_fp)**2 for x in abs_fp_vals) / n
        cov = sum((abs_f_vals[i] - mean_f) * (abs_fp_vals[i] - mean_fp) for i in range(n)) / n
        corr = cov / (var_f**0.5 * var_fp**0.5) if var_f > 0 and var_fp > 0 else 0

        print(f"  Corr(|f|, |f'|) = {corr:.4f}", file=sys.stderr)
        print(f"  E[|f|] = {mean_f:.4f}, E[|f'|] = {mean_fp:.4f}", file=sys.stderr)
        print(f"  min|f| = {min(abs_f_vals):.6f}", file=sys.stderr)

        # Conditional derivative given small f
        for eps in [0.1, 0.5, 1.0, 2.0]:
            near_zero = [r for r in results if r['abs_f'] < eps]
            if len(near_zero) >= 3:
                derivs = [r['abs_f_prime'] for r in near_zero]
                print(f"  |f|<{eps}: n={len(near_zero)}, "
                      f"min|f'|={min(derivs):.4f}, mean|f'|={sum(derivs)/len(derivs):.4f}", file=sys.stderr)

    # ============================================================
    # Step 4: Compare DH vs zeta joint distributions
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("STEP 4: Comparison DH vs Zeta", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    # Compute zeta joint for same sigma values
    zeta_joint = {}
    for sigma in [0.6, 0.7, 0.8]:
        print(f"\nSurveying zeta at sigma={sigma} (for comparison)...", file=sys.stderr)
        results = []
        for t in [i * 0.5 for i in range(20, 2000)]:  # t from 10 to 1000
            s = mpmath.mpc(sigma, t)
            z = mpmath.zeta(s)
            h = mpmath.mpf('1e-8')
            zp = (mpmath.zeta(s + h) - mpmath.zeta(s - h)) / (2 * h)
            results.append({
                't': t,
                'abs_zeta': float(abs(z)),
                'abs_zeta_prime': float(abs(zp)),
            })

        zeta_joint[sigma] = results

        # Compare distributions
        zeta_f = sorted([r['abs_zeta'] for r in results])
        dh_f = sorted([r['abs_f'] for r in dh_joint_results[sigma]])
        zeta_fp = sorted([r['abs_zeta_prime'] for r in results])
        dh_fp = sorted([r['abs_f_prime'] for r in dh_joint_results[sigma]])

        n = len(results)
        q_indices = [int(n * q) for q in [0.01, 0.05, 0.1, 0.25, 0.5]]

        print(f"\nQuantile comparison at sigma={sigma}:", file=sys.stderr)
        print(f"  {'Quantile':>10} | {'|zeta|':>10} | {'|DH|':>10} | {'|zeta_p|':>10} | {'|DH_p|':>10}", file=sys.stderr)
        for qi, q in zip(q_indices, [0.01, 0.05, 0.1, 0.25, 0.5]):
            qi = min(qi, n - 1)
            print(f"  {q:>10.2f} | {zeta_f[qi]:>10.4f} | {dh_f[qi]:>10.4f} | "
                  f"{zeta_fp[qi]:>10.4f} | {dh_fp[qi]:>10.4f}", file=sys.stderr)

    # ============================================================
    # Summary
    # ============================================================
    print("\n" + "=" * 70)
    print("DAVENPORT-HEILBRONN COMPARISON SUMMARY")
    print("=" * 70)

    print(f"\nOff-line zeros found: {len(zeros)}")
    for a in zero_analysis:
        print(f"  sigma={a['sigma']:.6f}, t={a['t']:.6f}: |f'|={a['derivative_abs']:.6f}, "
              f"|chi|~{a['chi_approx']:.6f}, ratio={a['ratio_deriv_to_chi']:.4f}")

    print(f"\nKey question: At DH off-line zeros, is |f'|/|chi| >> 1?")
    if zero_analysis:
        ratios = [a['ratio_deriv_to_chi'] for a in zero_analysis]
        print(f"  Mean ratio: {sum(ratios)/len(ratios):.4f}")
        print(f"  Min ratio: {min(ratios):.4f}")
        print(f"  Max ratio: {max(ratios):.4f}")
        if all(r > 1 for r in ratios):
            print("  YES: All ratios > 1, meaning the mirror derivative is large.")
            print("  This suggests DH off-line zeros have 'normal' size derivatives,")
            print("  NOT the vanishing derivatives that the chi-constraint would require for zeta.")
        else:
            print("  MIXED: Some ratios are < 1.")

    # Save
    output = {
        'zeros': zero_analysis,
        'kappa': kappa,
        'N_terms': N_terms,
    }
    with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/joint-zeta-derivative/dh_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)


if __name__ == '__main__':
    main()
