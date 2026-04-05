#!/usr/bin/env sage
"""
Phase 1: Derive the connection between ML beta_p and the RG running coupling.

The ML agent found:
  log(BSD_RHS) = (1/2)*log(N) + SUM beta_p * a_p + C_r
  where beta_p ~ 3.6 / p^{4.2}

The stat mech agent found:
  log|L_Lambda(E,1)| = -rank * log(log(Lambda)) + SUM a_p/p + lower order

If BSD holds:
  BSD_RHS = L^{(r)}(E,1)/r! * |Sha|^{-1}

Question: Can we derive beta_p from the explicit formula + Euler product expansion?

The key insight: log(Euler factor at p) = a_p/p + a_p^2/(2p^2) + higher order terms.
But the BSD RHS is NOT just the L-function value -- it's a product of arithmetic invariants.
The ML model is fitting log(Omega * Reg * prod(c_p) / |tors|^2), not log(L^{(r)}(E,1)/r!).

Strategy:
1. Compute log(Euler factor at p) expanded to high order
2. Compare with beta_p * a_p to find where the difference comes from
3. Track the BSD formula's individual components (Omega, Reg, c_p) to see which
   contributes what to the effective beta_p
"""

from sage.all import *
import json
import math
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(OUTPUT_DIR), 'approach-1-ml', 'data')

# Load the existing ML dataset
with open(os.path.join(DATA_DIR, 'bsd_invariants.json'), 'r') as f:
    all_curves = json.load(f)

print(f"Loaded {len(all_curves)} curves from ML dataset")

# ============================================================
# SECTION 1: Euler Product Expansion Analysis
# ============================================================

def euler_factor_log_expansion(p, ap, s=1, max_order=6):
    """
    Expand log(1/(1 - a_p*p^{-s} + p^{1-2s})) in powers of p^{-s}.

    log(Euler factor) = sum_{n=1}^{inf} b_n(p) / n
    where b_n involves a_p and p.

    At s=1, p^{-s} = 1/p, p^{1-2s} = 1/p.

    The local factor is 1/(1 - a_p/p + 1/p) = p/(p - a_p + 1).
    Its log is -log(1 - a_p/p + 1/p).

    Taylor expand: -log(1 - x) = x + x^2/2 + x^3/3 + ...
    where x = a_p/p - 1/p.

    But this is a formal expansion. Let's be more careful.

    Write the denominator as 1 - (a_p - 1)/p = 1 - u/p where u = a_p - 1.
    Then log(factor) = -log(1 - u/p) = u/p + u^2/(2p^2) + u^3/(3p^3) + ...

    Wait, that's not right either. The Euler factor at a good prime is:
    (1 - alpha_p * p^{-s})(1 - beta_p_root * p^{-s})
    where alpha_p + beta_p_root = a_p and alpha_p * beta_p_root = p.

    So log(Euler factor) = -log(1 - alpha_p/p) - log(1 - beta_p_root/p)
                         = sum_{n>=1} (alpha_p^n + beta_p_root^n) / (n * p^n)

    The power sums alpha_p^n + beta_p^n satisfy the recurrence:
    S_n = a_p * S_{n-1} - p * S_{n-2}
    with S_0 = 2, S_1 = a_p.
    """
    # Compute power sums S_n = alpha^n + beta^n
    S = [0] * (max_order + 1)
    S[0] = 2  # alpha^0 + beta^0
    S[1] = ap  # alpha + beta = a_p

    for n in range(2, max_order + 1):
        S[n] = ap * S[n-1] - p * S[n-2]

    # log(Euler factor) = sum_{n=1}^{max_order} S_n / (n * p^n)
    terms = []
    total = 0.0
    for n in range(1, max_order + 1):
        term = float(S[n]) / (n * float(p)**n)
        terms.append(term)
        total += term

    return total, terms, S


def analyze_euler_expansion():
    """
    For each prime p and each curve, compute the Euler factor expansion
    and compare the coefficient of a_p with the ML-fitted beta_p.

    The first-order term in the expansion is a_p/p.
    The second-order term is (a_p^2 - 2p)/(2p^2) = a_p^2/(2p^2) - 1/p.
    The third-order term involves a_p^3 - 3p*a_p.

    Since the ML model fits log(BSD_RHS) = ... + beta_p * a_p + ...,
    and we know log(Euler factor) ~ a_p/p + f(a_p^2, p)/p^2 + ...,
    the non-linear terms in a_p contribute to the effective beta_p when
    averaged over the ensemble.
    """
    print("\n" + "=" * 70)
    print("EULER PRODUCT EXPANSION ANALYSIS")
    print("=" * 70)

    primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    # For each prime, compute the average contribution of each order
    # across all rank-1 curves (since the ML model was best-fit there)
    rank1_curves = [c for c in all_curves if c['rank'] == 1]
    print(f"Using {len(rank1_curves)} rank-1 curves")

    # ML-fitted beta_p values (from findings)
    ml_beta = {2: 0.1920, 3: 0.0396, 5: -0.0109, 7: -0.0105, 11: -0.0021,
               13: 0.0004, 17: 0.0023, 19: 0.0026, 23: 0.0032}

    results = {}
    for p in primes_list[:15]:  # Focus on first 15 primes
        # Compute expansion for each curve
        order1_sum = 0.0  # a_p/p
        order2_sum = 0.0  # (a_p^2 - 2p)/(2p^2)
        order3_sum = 0.0
        total_sum = 0.0

        ap_values = []
        for curve in rank1_curves:
            ap = curve['a_p'].get(str(p), None)
            if ap is None:
                continue
            ap = int(ap)
            ap_values.append(ap)

            total_log, terms, S = euler_factor_log_expansion(p, ap, s=1, max_order=6)

            order1_sum += terms[0]  # a_p/p
            if len(terms) > 1:
                order2_sum += terms[1]  # S_2/(2p^2) = (a_p^2-2p)/(2p^2)
            if len(terms) > 2:
                order3_sum += terms[2]

            total_sum += total_log

        n = len(ap_values)
        if n == 0:
            continue

        mean_ap = sum(ap_values) / n
        mean_ap2 = sum(a**2 for a in ap_values) / n
        var_ap = mean_ap2 - mean_ap**2

        # The effective coefficient of a_p in the log Euler factor comes from:
        # Order 1: contributes exactly 1/p * a_p
        # Order 2: contributes (a_p^2 - 2p)/(2p^2), NOT linear in a_p
        # Order 3: contributes (a_p^3 - 3p*a_p)/(3p^3), which HAS an a_p term: -1/p^2 * a_p

        # The effective linear coefficient (from regression of total vs a_p):
        # beta_eff = cov(total, a_p) / var(a_p)
        cov_total_ap = sum(
            (euler_factor_log_expansion(p, ap, 1, 6)[0] - total_sum/n) * (ap - mean_ap)
            for ap in ap_values
        ) / n

        beta_eff = cov_total_ap / var_ap if var_ap > 0 else 0

        # Theoretical effective beta from order-by-order:
        # beta_order1 = 1/p (exact)
        # beta_order3 has -1/p^2 contribution (from -3p*a_p/(3p^3) = -a_p/p^2)
        # beta_order5 has contribution from S_5 = ... terms with a_p
        # In general, odd orders contribute linearly in a_p

        beta_theory_1 = 1.0/p  # from order 1
        beta_theory_3 = -1.0/p**2  # from order 3 (the a_p coefficient in S_3/(3p^3))
        # S_3 = a_p*S_2 - p*S_1 = a_p*(a_p^2-2p) - p*a_p = a_p^3 - 3p*a_p
        # S_3/(3p^3) has a_p coefficient = -3p/(3p^3) = -1/p^2

        # S_5 = a_p*S_4 - p*S_3, need S_4 first
        # S_4 = a_p*S_3 - p*S_2 = a_p*(a_p^3-3pa_p) - p*(a_p^2-2p)
        #      = a_p^4 - 3p*a_p^2 - p*a_p^2 + 2p^2 = a_p^4 - 4p*a_p^2 + 2p^2
        # S_5 = a_p*(a_p^4-4pa_p^2+2p^2) - p*(a_p^3-3pa_p)
        #      = a_p^5 - 4p*a_p^3 + 2p^2*a_p - p*a_p^3 + 3p^2*a_p
        #      = a_p^5 - 5p*a_p^3 + 5p^2*a_p
        # S_5/(5p^5) has a_p coefficient = 5p^2/(5p^5) = 1/p^3
        beta_theory_5 = 1.0/p**3

        beta_theory_all_odd = beta_theory_1 + beta_theory_3 + beta_theory_5
        # Pattern: 1/p - 1/p^2 + 1/p^3 - ... = 1/(p+1) (geometric series!)

        beta_geometric = 1.0/(p + 1)

        results[p] = {
            'p': p,
            'n_curves': n,
            'mean_ap': mean_ap,
            'var_ap': var_ap,
            'beta_eff_empirical': beta_eff,  # regression of log(euler) vs a_p
            'beta_order1': beta_theory_1,  # 1/p
            'beta_order1+3': beta_theory_1 + beta_theory_3,  # 1/p - 1/p^2
            'beta_odd_orders': beta_theory_all_odd,  # 1/p - 1/p^2 + 1/p^3
            'beta_geometric': beta_geometric,  # 1/(p+1) = sum of geometric series
            'order1_mean': order1_sum / n,
            'order2_mean': order2_sum / n,
            'order3_mean': order3_sum / n,
            'total_mean': total_sum / n,
        }

        ml_val = ml_beta.get(p, None)
        ml_str = f"{ml_val:.4f}" if ml_val is not None else "N/A"

        print(f"\n  p={p:>3d}: ML beta={ml_str:>8s}, "
              f"Euler_eff={beta_eff:.6f}, 1/p={1.0/p:.6f}, "
              f"1/(p+1)={1.0/(p+1):.6f}")
        print(f"         Order contributions: 1st={order1_sum/n:.6f}, "
              f"2nd={order2_sum/n:.6f}, 3rd={order3_sum/n:.6f}, "
              f"total={total_sum/n:.6f}")
        print(f"         Theoretical: 1/p={beta_theory_1:.6f}, "
              f"+3rd={beta_theory_1+beta_theory_3:.6f}, "
              f"geom_series={beta_geometric:.6f}")

    return results


# ============================================================
# SECTION 2: Component-Level Analysis
# ============================================================

def analyze_bsd_components():
    """
    The BSD RHS = Omega * Reg * prod(c_p) / |tors|^2.
    But the ML model fits this as ~ sqrt(N) * exp(sum beta_p * a_p).

    Let's decompose: which part of BSD_RHS correlates with each a_p?
    - Omega (real period) depends on the curve's geometry
    - Reg (regulator) depends on rational points
    - prod(c_p) (Tamagawa product) depends on bad reduction
    - |tors|^2 depends on torsion structure

    The correction delta_p = beta_p - 1/p may come from the fact that
    we're fitting the BSD RHS, not log L(E,1).
    """
    print("\n" + "=" * 70)
    print("BSD COMPONENT DECOMPOSITION")
    print("=" * 70)

    rank1_curves = [c for c in all_curves if c['rank'] == 1]

    # For each curve, compute:
    # 1. log(BSD_RHS) = log(Omega * Reg * prod_cp / tors^2)
    # 2. log(L_approx) = sum of log Euler factors
    # 3. The difference = log(Sha) (should be ~0 for rank 1 in our dataset)

    primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    # Compute component contributions
    log_bsd = []
    log_omega = []
    log_reg = []
    log_tam = []
    log_tors = []
    log_N_half = []
    residual_after_N = []  # log(BSD_RHS) - 0.5*log(N)
    a_p_matrix = {p: [] for p in primes_list}

    for curve in rank1_curves:
        N = curve['conductor']
        omega = curve['real_period']
        reg = curve['regulator']
        tam = curve['tamagawa_product']
        tors = curve['torsion_order']

        bsd_rhs = omega * reg * tam / (tors**2)
        if bsd_rhs <= 0:
            continue

        lb = math.log(bsd_rhs)
        log_bsd.append(lb)
        log_omega.append(math.log(omega) if omega > 0 else 0)
        log_reg.append(math.log(reg) if reg > 0 else 0)
        log_tam.append(math.log(tam) if tam > 0 else 0)
        log_tors.append(math.log(tors**2) if tors > 0 else 0)
        log_N_half.append(0.5 * math.log(N))
        residual_after_N.append(lb - 0.5 * math.log(N))

        for p in primes_list:
            ap = curve['a_p'].get(str(p), 0)
            a_p_matrix[p].append(int(ap))

    n = len(log_bsd)
    print(f"  Analyzing {n} rank-1 curves")

    # Correlation of each component with each a_p
    print("\n  Correlation of BSD components with a_p:")
    print(f"  {'p':>3s}  {'log(Omega)':>10s}  {'log(Reg)':>10s}  {'log(Tam)':>10s}  {'log(tors^2)':>11s}  {'log(BSD)':>10s}  {'resid':>10s}")

    for p in primes_list[:9]:
        ap_vals = a_p_matrix[p]
        if len(ap_vals) != n:
            continue

        # Pearson correlations
        def corr(x, y):
            n_c = len(x)
            mx = sum(x)/n_c
            my = sum(y)/n_c
            cov = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y)) / n_c
            sx = (sum((xi-mx)**2 for xi in x)/n_c)**0.5
            sy = (sum((yi-my)**2 for yi in y)/n_c)**0.5
            return cov/(sx*sy) if sx*sy > 0 else 0

        r_omega = corr(ap_vals, log_omega)
        r_reg = corr(ap_vals, log_reg)
        r_tam = corr(ap_vals, log_tam)
        r_tors = corr(ap_vals, log_tors)
        r_bsd = corr(ap_vals, log_bsd)
        r_resid = corr(ap_vals, residual_after_N)

        print(f"  {p:>3d}  {r_omega:>10.4f}  {r_reg:>10.4f}  {r_tam:>10.4f}  {r_tors:>11.4f}  {r_bsd:>10.4f}  {r_resid:>10.4f}")

    # KEY QUESTION: What is the regression of log(Omega) alone vs a_p?
    # The real period Omega is related to the lattice of the curve,
    # which is determined by the Weierstrass model.
    # But Omega = integral of dx/(2y+a1*x+a3) over a real cycle.
    # How does this relate to a_p?

    # Regression of residual_after_N on all a_p simultaneously
    # Using numpy-like manual computation
    print("\n  Multivariate regression: log(BSD/sqrt(N)) = SUM beta_p * a_p + const")

    # Build design matrix X (n x p_count) and target y
    primes_used = [p for p in primes_list if len(a_p_matrix[p]) == n]
    X = []
    for i in range(n):
        row = [a_p_matrix[p][i] for p in primes_used]
        X.append(row)

    y = residual_after_N

    # Solve via normal equations: beta = (X^T X)^{-1} X^T y
    # Manual implementation
    p_count = len(primes_used)
    # Add intercept
    for i in range(n):
        X[i].append(1)  # intercept

    # X^T X
    XtX = [[0.0]*(p_count+1) for _ in range(p_count+1)]
    for i in range(p_count+1):
        for j in range(p_count+1):
            for k in range(n):
                XtX[i][j] += X[k][i] * X[k][j]

    # X^T y
    Xty = [0.0]*(p_count+1)
    for i in range(p_count+1):
        for k in range(n):
            Xty[i] += X[k][i] * y[k]

    # Solve via Sage matrix operations
    M = matrix(RR, p_count+1, p_count+1, [XtX[i][j] for i in range(p_count+1) for j in range(p_count+1)])
    b = vector(RR, Xty)
    try:
        beta = M.solve_right(b)

        print(f"\n  Fitted coefficients (effective beta_p for BSD RHS):")
        fitted_betas = {}
        for i, p in enumerate(primes_used):
            fitted_betas[p] = float(beta[i])
            print(f"    p={p:>3d}: beta_p = {float(beta[i]):>10.6f}, 1/p = {1.0/p:>10.6f}, "
                  f"delta = {float(beta[i]) - 1.0/p:>10.6f}")
        print(f"    intercept = {float(beta[-1]):.6f}")

        # Compute R^2
        y_pred = [sum(X[k][i]*float(beta[i]) for i in range(p_count+1)) for k in range(n)]
        y_mean = sum(y)/n
        ss_res = sum((y[k]-y_pred[k])**2 for k in range(n))
        ss_tot = sum((y[k]-y_mean)**2 for k in range(n))
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        print(f"    R^2 = {r2:.6f}")

        # Now compute separately for each component
        print("\n  Component-specific beta_p (regression on individual components):")
        for component_name, component_vals in [
            ('log(Omega)', log_omega),
            ('log(Reg)', log_reg),
            ('log(Tam)', log_tam),
            ('-log(tors^2)', [-v for v in log_tors]),
        ]:
            # Simple regression: component ~ a_2 * beta_2
            # Just do bivariate with a_2
            a2_vals = a_p_matrix[2]
            mx = sum(a2_vals)/n
            my = sum(component_vals)/n
            cov = sum((a2_vals[k]-mx)*(component_vals[k]-my) for k in range(n))/n
            var_x = sum((a2_vals[k]-mx)**2 for k in range(n))/n
            b2 = cov/var_x if var_x > 0 else 0
            print(f"    {component_name:>15s}: beta_2 (a_2 coeff) = {b2:.6f}")

    except Exception as e:
        print(f"  Matrix solve failed: {e}")


# ============================================================
# SECTION 3: Explicit Formula Connection
# ============================================================

def explicit_formula_analysis():
    """
    The explicit formula for L-functions says:
      sum_{p<=x} a_p * log(p) / p = -rank * log(x) + C(E) + error

    By partial summation:
      sum_{p<=Lambda} a_p / p ~ -rank * log(log(Lambda)) + C'(E)

    Now, log(Euler product up to Lambda) at s=1:
      log|L_Lambda(E,1)| = sum_{p<=Lambda} log|1/(1-a_p/p+1/p)|
                         = sum_{p<=Lambda} [a_p/p + (a_p^2-2p)/(2p^2) + ...]

    The first term gives: sum a_p/p ~ -rank*log(log(Lambda)) + C'
    The second term gives: sum (a_p^2-2p)/(2p^2) ~ sum a_p^2/(2p^2) - sum 1/p

    For Sato-Tate distributed a_p: E[a_p^2] = p (by Hasse-Weil, a_p^2 ~ p on average)
    So sum a_p^2/(2p^2) ~ sum 1/(2p) ~ (1/2)*log(log(Lambda))
    And sum 1/p ~ log(log(Lambda))

    Total from 2nd order: (1/2)*log(log(Lambda)) - log(log(Lambda)) = -(1/2)*log(log(Lambda))

    So log|L_Lambda| ~ -rank*log(log(Lambda)) - (1/2)*log(log(Lambda)) + ...
                      = -(rank + 1/2)*log(log(Lambda)) + ...

    Wait -- the stat mech agent found slope ~ log(log(Lambda)) per rank unit,
    with a ~8% excess. Could this 1/2 be the source?

    Let's compute this precisely.
    """
    print("\n" + "=" * 70)
    print("EXPLICIT FORMULA + HIGHER ORDER EULER PRODUCT ANALYSIS")
    print("=" * 70)

    # Use sage for precise computation with actual curves
    test_curves = [
        ('11a1', 0), ('37a1', 1), ('389a1', 2), ('5077a1', 3),
        ('14a1', 0), ('43a1', 1), ('433a1', 2),
    ]

    Lambda_values = [100, 500, 1000, 5000, 10000, 50000]

    for label, rank in test_curves:
        E = EllipticCurve(label)
        N = int(E.conductor())
        print(f"\n  {label} (rank {rank}, N={N}):")

        for Lambda in Lambda_values:
            sum_ap_over_p = 0.0       # sum a_p/p (order 1 of log Euler)
            sum_order2 = 0.0          # sum (a_p^2-2p)/(2p^2) (order 2)
            sum_order3 = 0.0          # order 3
            sum_higher = 0.0          # orders 4+
            log_L_exact = 0.0         # exact log|L_Lambda|

            sum_1_over_p = 0.0        # sum 1/p (for comparison)

            for p in prime_range(2, Lambda + 1):
                ap = int(E.ap(p))
                is_bad = (N % p == 0)

                if is_bad:
                    # Bad prime: factor is (1 - a_p/p)^{-1}
                    denom = 1 - float(ap)/p
                    if abs(denom) > 1e-50:
                        log_L_exact += -math.log(abs(denom))
                    sum_ap_over_p += float(ap)/p
                    # Bad primes: log(1/(1-ap/p)) = ap/p + ap^2/(2p^2) + ...
                    # but ap in {-1, 0, 1} for bad primes
                    sum_order2 += float(ap)**2 / (2*p**2)
                    continue

                # Good prime exact
                denom = 1 - float(ap)/p + 1.0/p
                if abs(denom) > 1e-50:
                    log_L_exact += -math.log(abs(denom))

                # Expansion
                total_log, terms, S = euler_factor_log_expansion(p, ap, 1, 6)
                sum_ap_over_p += terms[0]  # a_p/p
                sum_order2 += terms[1] if len(terms) > 1 else 0
                sum_order3 += terms[2] if len(terms) > 2 else 0
                sum_higher += sum(terms[3:]) if len(terms) > 3 else 0

                sum_1_over_p += 1.0/p

            loglog = math.log(math.log(Lambda))

            # The key: compare actual log|L| with sum a_p/p - sum 1/p
            # log|L| should be ~ sum a_p/p - sum 1/p + (order 2 corrections)
            # because log(1/(1-a_p/p+1/p)) = a_p/p - 1/p + higher order (APPROXIMATELY)

            # Actually: log(1/(1-x)) where x = a_p/p - 1/p
            # This is: x + x^2/2 + x^3/3 + ...
            # The first term is a_p/p - 1/p
            # The second term is (a_p/p - 1/p)^2/2
            # This is NOT the same as the Euler factor expansion above.

            # Let me be precise. The Euler factor expansion gives:
            # sum a_p/p (order 1) + sum (a_p^2-2p)/(2p^2) (order 2) + ...
            # = sum a_p/p + sum a_p^2/(2p^2) - sum 1/p + ...

            if Lambda >= 100:
                print(f"    Lambda={Lambda:>6d}: "
                      f"log|L|={log_L_exact:>8.4f}, "
                      f"sum(a_p/p)={sum_ap_over_p:>8.4f}, "
                      f"order2={sum_order2:>8.4f}, "
                      f"order3={sum_order3:>8.4f}, "
                      f"higher={sum_higher:>8.4f}, "
                      f"log(log(L))={loglog:>6.4f}")
                print(f"             Decomposition: {sum_ap_over_p:.4f} + {sum_order2:.4f} + {sum_order3:.4f} + {sum_higher:.4f} = {sum_ap_over_p+sum_order2+sum_order3+sum_higher:.4f} (vs exact {log_L_exact:.4f})")

    return


# ============================================================
# SECTION 4: The Key Derivation — beta_p from Euler + BSD structure
# ============================================================

def derive_beta_p():
    """
    THE MAIN DERIVATION.

    The ML model fits: log(BSD_RHS) ~ 0.5*log(N) + sum beta_p * a_p + C_r
    The Euler product gives: log L(E,1) ~ sum a_p/p + higher order terms

    BSD says: BSD_RHS * |Sha| = L^{(r)}(E,1)/r!

    For rank 0: L(E,1) = BSD_RHS * |Sha|
    So: log(BSD_RHS) = log L(E,1) - log|Sha|

    Now the functional equation for L(E,s) relates it to the conductor:
    Lambda(E,s) = N^{s/2} * (2pi)^{-s} * Gamma(s) * L(E,s)
    with Lambda(E,s) = w * Lambda(E, 2-s), w = +/- 1 (root number)

    The "completed" L-function at s=1:
    Lambda(E,1) = sqrt(N)/(2pi) * L(E,1)

    So L(E,1) = 2pi/sqrt(N) * Lambda(E,1)

    And log L(E,1) = log(2pi) - 0.5*log(N) + log(Lambda(E,1))

    WAIT -- that's the WRONG sign on N. The ML model found +0.5*log(N),
    but the functional equation gives a -0.5*log(N) factor.

    This means log(BSD_RHS) = log L(E,1) = +0.5*log(N) + ...
    would require BSD_RHS ~ sqrt(N) * (something).

    Actually, let me be more careful. The BSD RHS is:
    Omega * Reg * prod(c_p) / |tors|^2

    The period Omega is related to the conductor via:
    Omega ~ C * N^{-1/2} for the "minimal" model

    Actually no, let me think about this differently.

    For rank 0, the BSD formula says:
    L(E,1) = Omega * prod(c_p) * |Sha| / |tors|^2

    The L-function satisfies a functional equation with conductor N.
    The period Omega is the real period of the Neron differential.

    The Manin constant c_E satisfies Omega = c_E * 2pi * i * integral(f(z)dz)
    where f is the associated weight-2 modular form.

    For the modular form f of level N:
    L(f,1) = -2pi*i * integral_0^{i*inf} f(z) dz

    And the Petersson norm relates to N:
    ||f||^2 ~ N (up to arithmetic factors)

    This gives L(E,1) ~ N^{-1/2} * (arithmetic)

    So Omega ~ N^{-1/2} would mean BSD_RHS ~ N^{-1/2} * ...

    But the ML model found BSD_RHS ~ N^{+1/2}!

    Let me just compute directly.
    """
    print("\n" + "=" * 70)
    print("DIRECT COMPUTATION: BSD_RHS vs N and L(E,1)")
    print("=" * 70)

    # For each curve, compute everything
    rank0_curves = [c for c in all_curves if c['rank'] == 0][:50]
    rank1_curves = [c for c in all_curves if c['rank'] == 1][:50]

    for rank, curves in [(0, rank0_curves), (1, rank1_curves)]:
        print(f"\n  Rank {rank} ({len(curves)} curves):")
        bsd_vals = []
        for c in curves:
            N = c['conductor']
            omega = c['real_period']
            reg = c['regulator']
            tam = c['tamagawa_product']
            tors = c['torsion_order']
            bsd_rhs = omega * reg * tam / (tors**2)
            bsd_vals.append({
                'N': N, 'bsd': bsd_rhs, 'omega': omega, 'reg': reg,
                'tam': tam, 'tors': tors,
                'log_bsd': math.log(bsd_rhs) if bsd_rhs > 0 else None,
            })

        # Check: is Omega ~ N^alpha?
        xs = [math.log(v['N']) for v in bsd_vals if v['log_bsd'] is not None]
        ys_omega = [math.log(v['omega']) for v in bsd_vals if v['omega'] > 0]
        ys_bsd = [v['log_bsd'] for v in bsd_vals if v['log_bsd'] is not None]

        if len(xs) > 3 and len(ys_omega) == len(xs):
            # Linear regression log(Omega) vs log(N)
            n_pts = len(xs)
            sx = sum(xs); sy = sum(ys_omega); sxx = sum(x**2 for x in xs)
            sxy = sum(x*y for x,y in zip(xs, ys_omega))
            slope_omega = (n_pts*sxy - sx*sy)/(n_pts*sxx - sx**2) if (n_pts*sxx - sx**2) != 0 else 0

            sy = sum(ys_bsd)
            sxy = sum(x*y for x,y in zip(xs, ys_bsd))
            slope_bsd = (n_pts*sxy - sx*sy)/(n_pts*sxx - sx**2) if (n_pts*sxx - sx**2) != 0 else 0

            print(f"    Omega ~ N^{slope_omega:.4f}")
            print(f"    BSD_RHS ~ N^{slope_bsd:.4f}")

            # For rank 1, also check Reg ~ N^alpha
            if rank == 1:
                ys_reg = [math.log(v['reg']) for v in bsd_vals if v['reg'] > 0]
                if len(ys_reg) == len(xs):
                    sy = sum(ys_reg)
                    sxy = sum(x*y for x,y in zip(xs, ys_reg))
                    slope_reg = (n_pts*sxy - sx*sy)/(n_pts*sxx - sx**2)
                    print(f"    Reg ~ N^{slope_reg:.4f}")

    # Compute for specific well-known curves with sage
    print("\n  Direct BSD invariants from SageMath:")
    for label in ['11a1', '37a1', '389a1', '5077a1']:
        E = EllipticCurve(label)
        N = int(E.conductor())
        r = int(E.rank())
        omega = float(E.real_components()) * float(E.period_lattice().basis()[0])
        # Actually let's use the standard BSD formula
        omega_real = float(E.real_components() * abs(E.period_lattice().basis()[0].real()))
        reg = float(E.regulator()) if r > 0 else 1.0
        tam = int(E.tamagawa_product())
        tors = int(E.torsion_order())
        sha_an = float(E.sha().an_numerical())

        bsd_rhs = omega_real * reg * tam / tors**2
        L_val = bsd_rhs * sha_an  # This should equal L^{(r)}(1)/r!

        print(f"    {label}: N={N}, rank={r}")
        print(f"      Omega={omega_real:.6f}, Reg={reg:.6f}, Tam={tam}, "
              f"|tors|={tors}, Sha_an={sha_an:.4f}")
        print(f"      BSD_RHS = {bsd_rhs:.6f}")
        print(f"      L_value = {L_val:.6f}")
        print(f"      sqrt(N) = {math.sqrt(N):.6f}")
        print(f"      BSD_RHS/sqrt(N) = {bsd_rhs/math.sqrt(N):.6f}")


# ============================================================
# SECTION 5: Effective beta_p from Full Euler Product
# ============================================================

def compute_effective_beta():
    """
    Compute the effective beta_p that arises from fitting
    log(Euler factor at p) vs a_p, including ALL higher order terms.

    For good primes at s=1:
    log(1/(1-ap/p+1/p)) = sum_{n>=1} S_n/(n*p^n)

    where S_n = alpha^n + beta^n with alpha+beta=ap, alpha*beta=p.

    The LINEAR part (in a_p) of this is:
    a_p * [1/p - 1/p^2 + 1/p^3 - ...] = a_p/(p+1)

    This is EXACT (not an approximation). The effective linear coefficient
    of a_p in the log Euler factor is exactly 1/(p+1), not 1/p.

    So the naive prediction for the ML beta_p should be 1/(p+1), and
    the correction from 1/p should be -1/(p(p+1)).

    Let's verify this and see if it matches the ML findings.
    """
    print("\n" + "=" * 70)
    print("EFFECTIVE LINEAR COEFFICIENT: beta_p = 1/(p+1) DERIVATION")
    print("=" * 70)

    # Proof:
    # S_n = alpha^n + beta^n where alpha*beta = p
    # The linear part of S_n in (alpha+beta) = a_p:
    # S_1 = a_p (linear)
    # S_2 = a_p^2 - 2p (quadratic in a_p)
    # S_3 = a_p^3 - 3p*a_p = a_p*(a_p^2 - 3p) (the linear coefficient in a_p is 0... wait)
    #
    # Actually, to find the effective linear coefficient, we need:
    # beta_eff = d/d(a_p) [sum S_n/(n*p^n)] evaluated at... what?
    #
    # No. The ML model fits log(BSD_RHS) = const + beta_p * a_p.
    # This is a LINEAR model. The effective beta_p from the Euler product
    # is the regression coefficient of log(Euler factor) on a_p.
    #
    # For a linear model, beta = cov(log_factor, a_p) / var(a_p).
    #
    # Since a_p is Sato-Tate distributed (for non-CM curves), we have:
    # E[a_p] = 0
    # E[a_p^2] = p (Hasse-Weil)
    # E[a_p^3] = 0 (by symmetry of Sato-Tate)
    # E[a_p^4] = 2p^2 (Sato-Tate fourth moment)
    # E[a_p^{2k+1}] = 0 (odd moments vanish)
    # E[a_p^{2k}] = (2k choose k) * p^k / (k+1) (Catalan numbers * p^k, from semicircle)
    #
    # Now:
    # cov(log_factor, a_p) = E[log_factor * a_p] - E[log_factor]*E[a_p]
    #                       = E[log_factor * a_p]  (since E[a_p] = 0)
    #
    # E[log_factor * a_p] = E[sum S_n/(n*p^n) * a_p]
    #                     = sum E[S_n * a_p] / (n*p^n)
    #
    # E[S_n * a_p]:
    # S_1*a_p = a_p^2, so E[S_1*a_p] = E[a_p^2] = p
    # S_2*a_p = (a_p^2-2p)*a_p = a_p^3 - 2p*a_p, E = 0 - 0 = 0
    # S_3*a_p = (a_p^3-3p*a_p)*a_p = a_p^4 - 3p*a_p^2, E = 2p^2 - 3p*p = -p^2
    # S_4*a_p = (a_p^4-4p*a_p^2+2p^2)*a_p = a_p^5-4p*a_p^3+2p^2*a_p, E = 0
    # S_5*a_p = ..., need E[a_p^6] = 5p^3 (Catalan)
    #   S_5 = a_p^5 - 5p*a_p^3 + 5p^2*a_p
    #   S_5*a_p = a_p^6 - 5p*a_p^4 + 5p^2*a_p^2
    #   E[S_5*a_p] = 5p^3 - 5p*2p^2 + 5p^2*p = 5p^3 - 10p^3 + 5p^3 = 0
    #
    # Wait, let me redo this. E[a_p^{2k}] under Sato-Tate (normalized):
    # If theta is uniform on [0,pi] with weight sin^2(theta) (Sato-Tate measure),
    # then a_p = 2*sqrt(p)*cos(theta), and
    # E[a_p^{2k}] = p^k * (2/pi) * integral_0^pi (2cos(theta))^{2k} * sin^2(theta) d(theta)
    # = p^k * C_k where C_k = Catalan number k-th = (2k)! / ((k+1)! * k!)
    #
    # C_0 = 1, C_1 = 1, C_2 = 2, C_3 = 5, C_4 = 14
    # E[a_p^2] = p*1 = p (CHECK)
    # E[a_p^4] = p^2*2 = 2p^2 (CHECK)
    # E[a_p^6] = p^3*5 = 5p^3

    # OK so:
    # E[S_1*a_p]/(1*p^1) = p/p = 1
    # E[S_3*a_p]/(3*p^3) = -p^2/(3p^3) = -1/(3p)
    # E[S_5*a_p]/(5*p^5) = 0/(5p^5) = 0 (!!!)
    #
    # Hmm, let me recheck S_5:
    # S_5 = a_p*S_4 - p*S_3 = a_p*(a_p^4-4pa_p^2+2p^2) - p*(a_p^3-3pa_p)
    #      = a_p^5 - 4p*a_p^3 + 2p^2*a_p - p*a_p^3 + 3p^2*a_p
    #      = a_p^5 - 5p*a_p^3 + 5p^2*a_p
    # S_5*a_p = a_p^6 - 5p*a_p^4 + 5p^2*a_p^2
    # E[S_5*a_p] = 5p^3 - 5p*2p^2 + 5p^2*p = 5p^3 - 10p^3 + 5p^3 = 0
    #
    # So E[S_{2k+1}*a_p]/(2k+1)*p^{2k+1} gives:
    # n=1: p/(1*p) = 1
    # n=3: -p^2/(3*p^3) = -1/(3p)
    # n=5: 0
    # n=7: need to compute...
    #
    # Actually let me approach this differently. The linear coefficient is:
    # d/d(a_p) [log(1/(1-a_p/p+1/p))] = (1/p - 0) / (1 - a_p/p + 1/p)
    #                                  -- wait, that's the derivative of the log
    #
    # d/d(a_p) [-log(1-a_p/p+1/p)] = (1/p) / (1-a_p/p+1/p)
    #
    # For the effective regression coefficient, we want E[derivative * 1] = E[(1/p)/(1-a_p/p+1/p)]
    # No that's not right either. For the regression:
    #
    # beta_eff = E[f(a_p)*a_p] / E[a_p^2] where f = log(Euler factor)
    # = (1/p) * [E[a_p/(1-a_p/p+1/p)]] ... no, this is getting circular.
    #
    # Let me just compute it numerically and compare.

    print("\n  THEORETICAL PREDICTION vs ML RESULT:")
    print(f"  {'p':>3s}  {'1/p':>8s}  {'1/(p+1)':>8s}  {'ML beta':>8s}  {'Empirical':>10s}  {'delta(ML-1/p)':>14s}  {'delta(ML-1/(p+1))':>18s}")

    # ML values
    ml_beta = {2: 0.1920, 3: 0.0396, 5: -0.0109, 7: -0.0105, 11: -0.0021,
               13: 0.0004, 17: 0.0023, 19: 0.0026, 23: 0.0032}

    # Empirical: use our dataset
    rank1_curves = [c for c in all_curves if c['rank'] == 1]

    primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23]

    for p in primes_list:
        ml_val = ml_beta.get(p, None)
        if ml_val is None:
            continue

        # Empirical: compute cov(log_euler_factor, a_p) / var(a_p)
        ap_vals = []
        log_euler_vals = []
        for c in rank1_curves:
            ap = c['a_p'].get(str(p), None)
            if ap is None:
                continue
            ap = int(ap)
            N = c['conductor']
            is_bad = (N % p == 0)

            if is_bad:
                denom = 1 - float(ap)/p
            else:
                denom = 1 - float(ap)/p + 1.0/p

            if abs(denom) > 1e-50:
                log_factor = -math.log(abs(denom))
                ap_vals.append(ap)
                log_euler_vals.append(log_factor)

        if len(ap_vals) < 10:
            continue

        n_pts = len(ap_vals)
        mean_ap = sum(ap_vals)/n_pts
        mean_log = sum(log_euler_vals)/n_pts
        cov = sum((ap_vals[i]-mean_ap)*(log_euler_vals[i]-mean_log) for i in range(n_pts))/n_pts
        var_ap = sum((ap_vals[i]-mean_ap)**2 for i in range(n_pts))/n_pts
        beta_emp = cov/var_ap if var_ap > 0 else 0

        print(f"  {p:>3d}  {1.0/p:>8.4f}  {1.0/(p+1):>8.4f}  {ml_val:>8.4f}  {beta_emp:>10.6f}  {ml_val-1.0/p:>14.6f}  {ml_val-1.0/(p+1):>18.6f}")

    # KEY INSIGHT: The ML beta_p should be related to but DIFFERENT from 1/(p+1)
    # because the ML model fits log(BSD_RHS), not log(L(E,1)).
    #
    # The difference between log(BSD_RHS) and log(L(E,1)) involves:
    # 1. The Sha factor (=1 for most curves in our dataset)
    # 2. The factorial 1/r! for rank r
    # 3. Possible period/regulator normalization differences
    #
    # The BIG discrepancy at p=2 (ML: 0.19, Euler: 0.33) suggests that the
    # real period Omega absorbs some of the a_2 dependence independently.

    # Let me compute: what is the regression coefficient of log(Omega) on a_2?
    print("\n  DECOMPOSITION: How much of beta_2 comes from each BSD component?")
    a2_vals = []
    omega_vals = []
    reg_vals = []
    tam_vals = []
    tors_vals = []
    bsd_vals = []
    N_vals = []

    for c in rank1_curves:
        ap2 = c['a_p'].get('2', None)
        if ap2 is None:
            continue
        a2_vals.append(int(ap2))
        omega_vals.append(math.log(c['real_period']) if c['real_period'] > 0 else 0)
        reg_vals.append(math.log(c['regulator']) if c['regulator'] > 0 else 0)
        tam_vals.append(math.log(c['tamagawa_product']) if c['tamagawa_product'] > 0 else 0)
        tors_vals.append(math.log(c['torsion_order']**2) if c['torsion_order'] > 0 else 0)
        bsd_rhs = c['real_period'] * c['regulator'] * c['tamagawa_product'] / c['torsion_order']**2
        bsd_vals.append(math.log(bsd_rhs) if bsd_rhs > 0 else 0)
        N_vals.append(math.log(c['conductor']))

    n_pts = len(a2_vals)
    mean_a2 = sum(a2_vals)/n_pts
    var_a2 = sum((v-mean_a2)**2 for v in a2_vals)/n_pts

    for name, vals in [('log(Omega)', omega_vals), ('log(Reg)', reg_vals),
                       ('log(Tam)', tam_vals), ('-log(tors^2)', [-v for v in tors_vals]),
                       ('0.5*log(N)', [0.5*v for v in N_vals]),
                       ('log(BSD_RHS)', bsd_vals)]:
        mean_v = sum(vals)/n_pts
        cov = sum((a2_vals[i]-mean_a2)*(vals[i]-mean_v) for i in range(n_pts))/n_pts
        beta = cov/var_a2 if var_a2 > 0 else 0
        print(f"    cov({name}, a_2)/var(a_2) = {beta:.6f}")

    print(f"\n    Sum of components: cov(log(Omega)+log(Reg)+log(Tam)-log(tors^2), a_2)/var(a_2)")
    sum_vals = [omega_vals[i] + reg_vals[i] + tam_vals[i] - tors_vals[i] for i in range(n_pts)]
    mean_v = sum(sum_vals)/n_pts
    cov = sum((a2_vals[i]-mean_a2)*(sum_vals[i]-mean_v) for i in range(n_pts))/n_pts
    beta_sum = cov/var_a2 if var_a2 > 0 else 0
    print(f"    = {beta_sum:.6f} (should match log(BSD_RHS) coefficient)")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("PHASE 1: DERIVING THE CONNECTION")
    print("ML beta_p <--> Euler Product <--> RG Running Coupling")
    print("=" * 70)

    results1 = analyze_euler_expansion()
    analyze_bsd_components()
    explicit_formula_analysis()
    derive_beta_p()
    compute_effective_beta()

    print("\n" + "=" * 70)
    print("PHASE 1 COMPLETE")
    print("=" * 70)
