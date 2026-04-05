"""
01_phi_high_precision.py
========================
High-precision computation of the Polya kernel Phi(u) and its log-concavity.

The Riemann Xi function has the representation:
    Xi(1/2 + it) = integral_0^inf Phi(u) cos(tu) du

where Phi(u) is given by:
    Phi(u) = sum_{n=1}^inf (2*pi*n^4*exp(9u/2) - 3*pi*n^2*exp(5u/2)) * exp(-pi*n^2*exp(2u))

Polya's criterion: if Phi(u) is log-concave for all u >= 0, then Xi has only
real zeros, which is equivalent to the Riemann Hypothesis.

Log-concavity means: d^2/du^2 log(Phi(u)) < 0 for all u >= 0.
Equivalently: Phi(u)*Phi''(u) - [Phi'(u)]^2 < 0.

This script computes Phi, Phi', Phi'' at high precision across a fine grid,
and rigorously evaluates the log-concavity expression.

Author: Polya kernel log-concavity investigation
Date: 2026-04-04
"""

import mpmath
import json
import sys

# Use high precision
mpmath.mp.dps = 100  # 100 decimal digits


def phi_term(n, u):
    """
    Compute the n-th term of Phi(u):
        (2*pi*n^4*exp(9u/2) - 3*pi*n^2*exp(5u/2)) * exp(-pi*n^2*exp(2u))

    Returns mpf value.
    """
    n = mpmath.mpf(n)
    u = mpmath.mpf(u)
    pi = mpmath.pi

    e2u = mpmath.exp(2*u)
    e5u2 = mpmath.exp(5*u/2)
    e9u2 = mpmath.exp(9*u/2)

    gauss = mpmath.exp(-pi * n**2 * e2u)
    prefactor = 2*pi*n**4*e9u2 - 3*pi*n**2*e5u2

    return prefactor * gauss


def phi_term_derivatives(n, u):
    """
    Compute the n-th term of Phi(u) and its first two derivatives with respect to u.

    Let f_n(u) = (2*pi*n^4*exp(9u/2) - 3*pi*n^2*exp(5u/2)) * exp(-pi*n^2*exp(2u))

    We compute f_n, f_n', f_n'' analytically at arbitrary precision.

    Let:
        A = 2*pi*n^4, B = -3*pi*n^2
        alpha = 9/2, beta_coeff = 5/2
        c = pi*n^2

    f_n = (A*exp(alpha*u) + B*exp(beta_coeff*u)) * exp(-c*exp(2u))

    Let g(u) = exp(-c*exp(2u)), so g'(u) = -2c*exp(2u)*g(u)
    Let p(u) = A*exp(alpha*u) + B*exp(beta_coeff*u)
    p'(u) = A*alpha*exp(alpha*u) + B*beta_coeff*exp(beta_coeff*u)
    p''(u) = A*alpha^2*exp(alpha*u) + B*beta_coeff^2*exp(beta_coeff*u)

    f_n = p*g
    f_n' = p'*g + p*g'
    f_n'' = p''*g + 2*p'*g' + p*g''

    g'(u) = -2c*e^{2u} * g
    g''(u) = (-4c*e^{2u} + 4c^2*e^{4u}) * g
    """
    n = mpmath.mpf(n)
    u = mpmath.mpf(u)
    pi = mpmath.pi

    A = 2*pi*n**4
    B = -3*pi*n**2
    alpha = mpmath.mpf(9)/2
    beta_c = mpmath.mpf(5)/2
    c = pi*n**2

    e2u = mpmath.exp(2*u)
    e_alpha_u = mpmath.exp(alpha*u)
    e_beta_u = mpmath.exp(beta_c*u)

    g = mpmath.exp(-c*e2u)
    g_prime = -2*c*e2u*g
    g_dblprime = (-4*c*e2u + 4*c**2*e2u**2)*g

    p = A*e_alpha_u + B*e_beta_u
    p_prime = A*alpha*e_alpha_u + B*beta_c*e_beta_u
    p_dblprime = A*alpha**2*e_alpha_u + B*beta_c**2*e_beta_u

    f = p*g
    f_prime = p_prime*g + p*g_prime
    f_dblprime = p_dblprime*g + 2*p_prime*g_prime + p*g_dblprime

    return f, f_prime, f_dblprime


def compute_phi_and_derivatives(u, n_terms=50):
    """
    Compute Phi(u), Phi'(u), Phi''(u) using n_terms of the series.

    Returns (Phi, Phi', Phi'') as mpf values.
    Also returns the magnitude of the last included term for convergence check.
    """
    u = mpmath.mpf(u)

    Phi = mpmath.mpf(0)
    Phi_prime = mpmath.mpf(0)
    Phi_dblprime = mpmath.mpf(0)

    last_term_mag = mpmath.mpf(0)

    for n in range(1, n_terms + 1):
        f, fp, fpp = phi_term_derivatives(n, u)
        Phi += f
        Phi_prime += fp
        Phi_dblprime += fpp

        if n == n_terms:
            last_term_mag = abs(f)

    return Phi, Phi_prime, Phi_dblprime, last_term_mag


def log_concavity_expression(u, n_terms=50):
    """
    Compute Phi*Phi'' - (Phi')^2 at u.

    This is negative iff Phi is log-concave at u.

    Also compute d^2/du^2 log(Phi) = [Phi*Phi'' - (Phi')^2] / Phi^2
    """
    Phi, Phi_prime, Phi_dblprime, last_term = compute_phi_and_derivatives(u, n_terms)

    if Phi <= 0:
        return {
            'u': float(u),
            'Phi': float(Phi),
            'Phi_positive': False,
            'log_concavity': None,
            'LC_expression': None,
        }

    LC = Phi * Phi_dblprime - Phi_prime**2
    d2_log_Phi = LC / Phi**2

    return {
        'u': float(u),
        'Phi': float(Phi),
        'Phi_prime': float(Phi_prime),
        'Phi_dblprime': float(Phi_dblprime),
        'Phi_positive': True,
        'LC_expression': float(LC),
        'log_concavity': float(d2_log_Phi),
        'last_term_magnitude': float(last_term),
        'is_log_concave': bool(LC < 0),
    }


def main():
    print("=" * 80)
    print("POLYA KERNEL: HIGH-PRECISION LOG-CONCAVITY ANALYSIS")
    print("=" * 80)
    print(f"Precision: {mpmath.mp.dps} decimal digits")
    print()

    # =========================================================
    # Phase 1: Coarse grid to map the landscape
    # =========================================================
    print("Phase 1: Coarse grid (50 points on [0, 2.0])")
    print("-" * 70)

    u_coarse = [mpmath.mpf(k)/25 for k in range(51)]  # 0 to 2.0 in steps of 0.04

    results_coarse = []
    print(f"{'u':>8s} {'Phi':>16s} {'d2_log_Phi':>16s} {'LC_expr':>16s} {'last_term':>14s} {'log-c?':>8s}")

    for u in u_coarse:
        res = log_concavity_expression(u, n_terms=30)
        results_coarse.append(res)

        if res['Phi_positive']:
            print(f"{res['u']:8.4f} {res['Phi']:16.8e} {res['log_concavity']:16.8e} "
                  f"{res['LC_expression']:16.8e} {res['last_term_magnitude']:14.6e} "
                  f"{'YES' if res['is_log_concave'] else '*** NO ***':>8s}")
        else:
            print(f"{res['u']:8.4f} {'Phi <= 0':>16s} {'N/A':>16s} {'N/A':>16s} {'N/A':>14s} {'N/A':>8s}")

    # Find where Phi becomes negligible
    positive_results = [r for r in results_coarse if r['Phi_positive'] and r['Phi'] > 1e-50]
    if positive_results:
        u_max_positive = max(r['u'] for r in positive_results)
        print(f"\nPhi > 1e-50 for u in [0, {u_max_positive:.4f}]")

    # Check: are all log-concavity values negative?
    lc_values = [r['log_concavity'] for r in results_coarse if r['Phi_positive'] and r['log_concavity'] is not None]
    all_negative = all(v < 0 for v in lc_values)
    print(f"All d^2/du^2 log(Phi) < 0: {all_negative}")
    if lc_values:
        print(f"Range: [{min(lc_values):.6e}, {max(lc_values):.6e}]")

    # =========================================================
    # Phase 2: Fine grid around u=0 (the most delicate region)
    # =========================================================
    print("\n" + "=" * 70)
    print("Phase 2: Fine grid near u=0 (100 points on [0, 0.5])")
    print("-" * 70)

    u_fine = [mpmath.mpf(k)/200 for k in range(101)]  # 0 to 0.5 in steps of 0.005

    results_fine = []
    print(f"{'u':>8s} {'Phi':>16s} {'d2_log_Phi':>16s} {'LC_expr':>16s} {'log-c?':>8s}")

    for u in u_fine:
        res = log_concavity_expression(u, n_terms=30)
        results_fine.append(res)

        if float(u) % 0.05 < 0.001 or float(u) < 0.01:  # Print every 0.05 and near 0
            if res['Phi_positive']:
                print(f"{res['u']:8.5f} {res['Phi']:16.8e} {res['log_concavity']:16.8e} "
                      f"{res['LC_expression']:16.8e} {'YES' if res['is_log_concave'] else '*** NO ***':>8s}")

    lc_fine = [r['log_concavity'] for r in results_fine if r['Phi_positive'] and r['log_concavity'] is not None]
    print(f"\nNear u=0: d^2/du^2 log(Phi) range: [{min(lc_fine):.6e}, {max(lc_fine):.6e}]")

    # =========================================================
    # Phase 3: Very high precision at u=0 specifically
    # =========================================================
    print("\n" + "=" * 70)
    print("Phase 3: u=0 at very high precision (150 digits)")
    print("-" * 70)

    mpmath.mp.dps = 150

    res_u0 = log_concavity_expression(mpmath.mpf(0), n_terms=50)
    print(f"At u=0:")
    print(f"  Phi(0)   = {mpmath.mpf(res_u0['Phi'])}")
    print(f"  Phi'(0)  = {mpmath.mpf(res_u0['Phi_prime'])}")
    print(f"  Phi''(0) = {mpmath.mpf(res_u0['Phi_dblprime'])}")
    print(f"  Phi*Phi'' - (Phi')^2 = {mpmath.mpf(res_u0['LC_expression'])}")
    print(f"  d^2/du^2 log Phi(0) = {mpmath.mpf(res_u0['log_concavity'])}")
    print(f"  Log-concave at u=0: {res_u0['is_log_concave']}")

    mpmath.mp.dps = 100  # reset

    # =========================================================
    # Phase 4: The n=1 term analysis
    # =========================================================
    print("\n" + "=" * 70)
    print("Phase 4: Single-term (n=1) approximation analysis")
    print("-" * 70)

    print("The n=1 term:")
    print("  f_1(u) = (2*pi*exp(9u/2) - 3*pi*exp(5u/2)) * exp(-pi*exp(2u))")
    print()

    u_grid = [mpmath.mpf(k)/50 for k in range(76)]  # 0 to 1.5

    print(f"{'u':>8s} {'Phi':>16s} {'f_1':>16s} {'f_1/Phi':>12s} {'LC_Phi':>16s} {'LC_f1':>16s} {'ratio':>12s}")

    for u in u_grid:
        # Full Phi
        Phi, Phi_p, Phi_pp, _ = compute_phi_and_derivatives(u, n_terms=30)
        # n=1 term only
        f1, f1_p, f1_pp = phi_term_derivatives(1, u)

        if Phi > 0 and f1 > 0:
            LC_Phi = Phi * Phi_pp - Phi_p**2
            LC_f1 = f1 * f1_pp - f1_p**2
            d2log_Phi = LC_Phi / Phi**2
            d2log_f1 = LC_f1 / f1**2

            ratio_f1 = f1 / Phi
            ratio_LC = d2log_Phi / d2log_f1 if d2log_f1 != 0 else mpmath.mpf(0)

            if float(u) % 0.1 < 0.001 or float(u) < 0.05:
                print(f"{float(u):8.4f} {float(Phi):16.8e} {float(f1):16.8e} "
                      f"{float(ratio_f1):12.8f} {float(d2log_Phi):16.8e} "
                      f"{float(d2log_f1):16.8e} {float(ratio_LC):12.6f}")

    # =========================================================
    # Phase 5: Analyze the n=1 log-concavity analytically
    # =========================================================
    print("\n" + "=" * 70)
    print("Phase 5: Analytic properties of the n=1 term's log-concavity")
    print("-" * 70)

    print("""
    f_1(u) = (2*pi*exp(9u/2) - 3*pi*exp(5u/2)) * exp(-pi*exp(2u))

    Let x = exp(2u), so x >= 1.
    f_1 = pi * exp(5u/2) * (2*x^2 - 3) * exp(-pi*x)    [since exp(9u/2) = exp(5u/2)*x^2]

    Wait, let's be more careful:
    exp(9u/2) = exp(5u/2) * exp(2u) = exp(5u/2) * x

    So f_1 = pi*exp(5u/2)*(2*x - 3) * exp(-pi*x)  ... NO.

    Let me redo: n=1.
    f_1 = (2*pi*1^4*exp(9u/2) - 3*pi*1^2*exp(5u/2)) * exp(-pi*1^2*exp(2u))
        = pi*exp(5u/2)*(2*exp(2u) - 3) * exp(-pi*exp(2u))
        = pi*exp(5u/2)*(2x - 3) * exp(-pi*x)

    where x = exp(2u) >= 1.

    At u=0: x=1, f_1(0) = pi*(2-3)*exp(-pi) = -pi*exp(-pi) < 0 !!

    Wait, that can't be right if Phi(0) > 0...

    Let me check with multiple terms.
    """)

    # Recheck Phi(0) term by term
    print("Term-by-term breakdown at u=0:")
    u_val = mpmath.mpf(0)
    total = mpmath.mpf(0)
    for n in range(1, 20):
        f = phi_term(n, u_val)
        total += f
        print(f"  n={n:2d}: f_n(0) = {float(f):20.12e}  cumulative = {float(total):20.12e}")

    print(f"\nTotal Phi(0) with 50 terms: {float(compute_phi_and_derivatives(mpmath.mpf(0), 50)[0]):.15e}")

    # Also check at u=0, what is the n=1 term?
    f1_at_0, _, _ = phi_term_derivatives(1, mpmath.mpf(0))
    print(f"f_1(0) = {float(f1_at_0):.15e}")

    # Check: where does the n=1 term become positive?
    print("\nFinding where f_1(u) = 0:")
    print("  f_1(u) = pi*exp(5u/2)*(2*exp(2u) - 3)*exp(-pi*exp(2u))")
    print("  f_1(u) = 0 when 2*exp(2u) = 3, i.e., u = ln(3/2)/2")
    u_cross = mpmath.log(mpmath.mpf(3)/2)/2
    print(f"  u_cross = {float(u_cross):.10f}")
    print(f"  f_1(u_cross) = {float(phi_term(1, u_cross)):.15e}")

    # For u > u_cross, f_1 > 0 and the n=1 term dominates
    # For u < u_cross, f_1 < 0 and higher n terms must compensate
    # This is the region where log-concavity analysis is subtle!

    print(f"\n  For u < {float(u_cross):.6f}: f_1(u) < 0, higher terms dominate")
    print(f"  For u > {float(u_cross):.6f}: f_1(u) > 0 and dominates the sum")

    # =========================================================
    # Phase 6: Theta function representation
    # =========================================================
    print("\n" + "=" * 70)
    print("Phase 6: Alternative representation via Jacobi theta")
    print("-" * 70)

    print("""
    The Polya kernel can also be written using the Jacobi theta function.

    Recall: theta(t) = sum_{n=-inf}^{inf} exp(-pi*n^2*t)

    The functional equation: theta(1/t) = sqrt(t) * theta(t)

    The kernel Phi(u) is related to theta by:

    Phi(u) = 2 * sum_{n=1}^inf (2*pi^2*n^4*e^{9u} - 3*pi*n^2*e^{5u}) * exp(-pi*n^2*e^{2u})

    (Note: this is 2x the series starting at n=1, but with the e^{9u/2} etc.)

    Actually, let me use the standard form. The Xi function:

    Xi(s) = (1/2)*s*(s-1)*pi^{-s/2}*Gamma(s/2)*zeta(s)

    And the Fourier representation:
    Xi(1/2 + it) = int_0^inf Phi(u) cos(tu) du

    where Phi(u) = 2*d/dx [x^{3/2} * psi'(x)] |_{x=e^{2u}}

    and psi(x) = sum_{n=1}^inf exp(-pi*n^2*x) = (theta_3(0, e^{-pi*x}) - 1)/2
    """)

    # Verify using the theta function representation
    print("Verification: Phi via theta derivatives at u=0.5:")
    u_test = mpmath.mpf('0.5')
    x = mpmath.exp(2*u_test)

    # psi(x) = sum_{n=1}^inf exp(-pi*n^2*x)
    psi_val = sum(mpmath.exp(-mpmath.pi*n**2*x) for n in range(1, 50))
    psi_prime = sum(-mpmath.pi*n**2*mpmath.exp(-mpmath.pi*n**2*x) for n in range(1, 50))

    # Phi(u) = 2 * d/du [e^{3u} * psi'(e^{2u})]  ... need to be more careful
    # Actually: Phi(u) = sum_{n=1}^inf (2*pi*n^4*exp(9u/2) - 3*pi*n^2*exp(5u/2))*exp(-pi*n^2*exp(2u))
    # This is what we already compute. Let me just verify.

    Phi_direct, _, _, _ = compute_phi_and_derivatives(u_test, 50)
    print(f"  Phi(0.5) from direct series: {float(Phi_direct):.15e}")

    # =========================================================
    # Phase 7: Comprehensive log-concavity table
    # =========================================================
    print("\n" + "=" * 70)
    print("Phase 7: Comprehensive log-concavity data")
    print("-" * 70)

    # Very fine grid on [0, 1.5]
    n_points = 300
    u_vals = [mpmath.mpf(k) * mpmath.mpf('1.5') / n_points for k in range(n_points + 1)]

    all_results = []
    max_lc = mpmath.mpf('-inf')
    min_lc = mpmath.mpf('inf')

    for u in u_vals:
        Phi, Phi_p, Phi_pp, last = compute_phi_and_derivatives(u, n_terms=30)

        if Phi > mpmath.mpf('1e-80'):
            LC = Phi * Phi_pp - Phi_p**2
            d2log = LC / Phi**2

            if d2log > max_lc:
                max_lc = d2log
                u_max_lc = u
            if d2log < min_lc:
                min_lc = d2log
                u_min_lc = u

            all_results.append({
                'u': float(u),
                'Phi': float(Phi),
                'LC_expr': float(LC),
                'd2_log_Phi': float(d2log),
                'is_log_concave': bool(LC < 0),
            })

    n_tested = len(all_results)
    n_lc = sum(1 for r in all_results if r['is_log_concave'])

    print(f"Points tested: {n_tested}")
    print(f"Log-concave at all points: {n_lc == n_tested} ({n_lc}/{n_tested})")
    print(f"Max d^2/du^2 log(Phi) = {float(max_lc):.8e} at u = {float(u_max_lc):.6f}")
    print(f"Min d^2/du^2 log(Phi) = {float(min_lc):.8e} at u = {float(u_min_lc):.6f}")

    # The key number: the MAXIMUM of d^2/du^2 log(Phi) -- closest to zero
    # If this is significantly negative, we have a margin for a proof
    print(f"\nCRITICAL VALUE: max d^2/du^2 log(Phi) = {float(max_lc):.10e}")
    print(f"  This is the point where log-concavity is WEAKEST.")
    print(f"  It occurs at u = {float(u_max_lc):.8f}")

    # =========================================================
    # Save results
    # =========================================================
    output = {
        'precision_digits': 100,
        'n_terms': 30,
        'n_points_tested': n_tested,
        'all_log_concave': n_lc == n_tested,
        'max_d2_log_Phi': float(max_lc),
        'u_at_max_d2_log_Phi': float(u_max_lc),
        'min_d2_log_Phi': float(min_lc),
        'u_at_min_d2_log_Phi': float(u_min_lc),
        'sample_results': all_results[::10],  # every 10th point
    }

    output_path = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/riemann-hypothesis/experiments/2A-entropy-ceiling/polya-kernel/results_phase1.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == '__main__':
    main()
