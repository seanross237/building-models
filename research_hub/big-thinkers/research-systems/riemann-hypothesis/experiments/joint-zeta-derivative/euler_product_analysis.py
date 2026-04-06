"""
Investigation 2 & 3: Euler product structure and derivative constraints.

Key idea: The Euler product log(zeta(s)) = -sum_p log(1 - p^{-s})
creates specific correlations between zeta and zeta'. We investigate:

1. Whether log|zeta| = -sum_p Re[log(1-p^{-s})] can diverge to -inf at sigma > 1/2
2. The conditional structure of zeta'/zeta given zeta is small
3. The random Euler product joint distribution of (Z, Z') where
   Z = prod_p (1-p^{-sigma-iU_p})^{-1} (Bohr-Jessen model)
"""

import mpmath
import random
import json
import sys
import math
import time

mpmath.mp.dps = 25

def primes_up_to(N):
    """Sieve of Eratosthenes."""
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return [i for i in range(2, N + 1) if sieve[i]]


def euler_product_log_sum(sigma, t, primes):
    """Compute log|zeta(sigma+it)| via Euler product over given primes.
    Returns: sum of -Re[log(1-p^{-s})] over primes, and individual terms."""
    s = complex(sigma, t)
    total = 0.0
    terms = []
    for p in primes:
        ps = p ** (-s)  # p^{-sigma-it}
        val = -math.log(abs(1 - ps))  # = -Re[log(1-p^{-s})]... approximately
        # More precisely: Re[log(1/(1-p^{-s}))] = -log|1-p^{-s}|
        log_factor = -math.log(abs(1 - ps))
        total += log_factor
        terms.append({'p': p, 'log_factor': log_factor, 'ps_abs': abs(ps)})
    return total, terms


def euler_product_derivative_log(sigma, t, primes):
    """Compute zeta'/zeta via Euler product: -sum_p (log p)*p^{-s}/(1-p^{-s}).
    This is the logarithmic derivative."""
    s = complex(sigma, t)
    total = complex(0, 0)
    for p in primes:
        ps = p ** (-s)
        term = -math.log(p) * ps / (1 - ps)
        total += term
    return total


def random_euler_product_joint(sigma, num_primes, num_samples):
    """Bohr-Jessen random model: Z = prod_p (1 - p^{-sigma} e^{i*theta_p})^{-1}
    where theta_p are independent uniform on [0, 2*pi).

    Compute BOTH Z and Z' = dZ/ds in the random model.
    Z' = Z * sum_p (log p) * p^{-sigma} e^{i*theta_p} / (1 - p^{-sigma} e^{i*theta_p})
    """
    primes = primes_up_to(500)[:num_primes]
    results = []

    for sample in range(num_samples):
        thetas = [random.uniform(0, 2 * math.pi) for _ in primes]

        # Compute log(Z) and (Z'/Z) = sum_p (log p) p^{-sigma} e^{itheta} / (1 - p^{-sigma} e^{itheta})
        log_Z = complex(0, 0)
        log_deriv = complex(0, 0)  # Z'/Z

        for i, p in enumerate(primes):
            ps = p ** (-sigma) * (math.cos(thetas[i]) + 1j * math.sin(thetas[i]))
            # log(1/(1-ps)) = -log(1-ps)
            one_minus_ps = 1 - ps
            log_Z -= cmath_log(one_minus_ps)
            # d/ds of log(1/(1-p^{-s})) = (log p) p^{-s} / (1 - p^{-s})
            log_deriv += math.log(p) * ps / one_minus_ps

        Z = cmath_exp(log_Z)
        Zprime = Z * log_deriv  # chain rule: Z' = Z * (Z'/Z) but with sign...
        # Actually ζ'/ζ = -Σ Λ(n)/n^s.  In Euler product form:
        # (d/ds) log ζ(s) = Σ_p (log p)/(p^s - 1)
        # So ζ'(s) = ζ(s) * Σ_p (log p)/(p^s - 1)
        # In the random model: Z' = Z * Σ_p (log p) * p^{-σ} e^{iθ_p} / (1 - p^{-σ} e^{iθ_p})
        # But the sign convention: ζ'(s)/ζ(s) = -Σ_n Λ(n)/n^s
        # = Σ_p log(p) * p^{-s}/(1-p^{-s})  [the positive Euler product form]
        # So Z' = -Z * log_deriv  (the minus sign from d/ds of p^{-s} = -log(p)*p^{-s})
        Zprime = -Z * log_deriv

        results.append({
            'abs_Z': abs(Z),
            'abs_Zprime': abs(Zprime),
            'arg_Z': cmath_phase(Z),
            'arg_Zprime': cmath_phase(Zprime),
            'log_abs_Z': math.log(max(abs(Z), 1e-300)),
            'log_abs_Zprime': math.log(max(abs(Zprime), 1e-300)),
        })

        if (sample + 1) % 10000 == 0:
            print(f"  Random EP: {sample+1}/{num_samples} samples done", file=sys.stderr)

    return results


def cmath_log(z):
    """Complex logarithm."""
    import cmath
    return cmath.log(z)

def cmath_exp(z):
    """Complex exponential."""
    import cmath
    return cmath.exp(z)

def cmath_phase(z):
    """Complex phase."""
    import cmath
    return cmath.phase(z)


def analyze_conditional_derivative(results, epsilon_values):
    """Given |Z| < epsilon, analyze the distribution of |Z'|."""
    analysis = {}
    for eps in epsilon_values:
        near_zero = [r for r in results if r['abs_Z'] < eps]
        if len(near_zero) < 3:
            analysis[eps] = {'count': len(near_zero), 'total': len(results)}
            continue

        derivs = sorted([r['abs_Zprime'] for r in near_zero])
        n = len(derivs)
        analysis[eps] = {
            'count': n,
            'total': len(results),
            'fraction': n / len(results),
            'min': derivs[0],
            'max': derivs[-1],
            'mean': sum(derivs) / n,
            'median': derivs[n // 2],
            'p10': derivs[n // 10] if n >= 10 else derivs[0],
            'p90': derivs[9 * n // 10] if n >= 10 else derivs[-1],
        }
    return analysis


def investigate_log_divergence(sigma, primes, num_t_samples=5000):
    """Investigate whether sum_p -log|1-p^{-sigma-it}| can diverge.

    For the Euler product to give a zero, we need log|zeta| -> -infty,
    i.e., sum_p log|1-p^{-sigma-it}| -> +infty.

    Each term log|1-p^{-sigma-it}| ranges from log(1-p^{-sigma}) to log(1+p^{-sigma}).
    The sum's variance is sum_p Var(log|1-p^{-sigma-it}|).

    Can the sum ever diverge? Only if terms can conspire to all be near their maximum.
    """
    results = []
    min_log_zeta = float('inf')
    min_log_zeta_t = 0

    for _ in range(num_t_samples):
        t = random.uniform(100, 100000)
        log_sum = 0.0
        for p in primes:
            s = complex(sigma, t)
            ps = p ** (-s)
            log_sum += math.log(abs(1 - ps))

        # log|zeta| = -log_sum (approximately)
        log_zeta = -log_sum
        results.append({'t': t, 'log_zeta_euler': log_zeta})
        if log_zeta < min_log_zeta:
            min_log_zeta = log_zeta
            min_log_zeta_t = t

    # Statistics
    log_vals = [r['log_zeta_euler'] for r in results]
    mean_log = sum(log_vals) / len(log_vals)
    var_log = sum((x - mean_log)**2 for x in log_vals) / len(log_vals)

    # Theoretical variance from individual terms
    # Var(log|1-p^{-sigma-it}|) can be computed from the Bohr-Jessen theory
    # For large p: ~ (1/2) p^{-2sigma}
    theoretical_var = sum(0.5 * p ** (-2 * sigma) for p in primes)

    return {
        'sigma': sigma,
        'num_primes': len(primes),
        'num_samples': num_t_samples,
        'mean_log_zeta': mean_log,
        'var_log_zeta': var_log,
        'std_log_zeta': var_log ** 0.5,
        'min_log_zeta': min_log_zeta,
        'min_log_zeta_t': min_log_zeta_t,
        'theoretical_var': theoretical_var,
        'min_in_stds': (min_log_zeta - mean_log) / (var_log ** 0.5) if var_log > 0 else 0,
    }


def euler_product_conditional_derivative_structure(sigma, t_near_zero, primes):
    """At a t where |zeta| is small, analyze the structure of the Euler product
    and its derivative.

    Key question: when the Euler product is near zero (many factors conspire),
    what does the derivative look like?
    """
    s = complex(sigma, t_near_zero)

    # Compute each factor
    factors = []
    log_deriv_terms = []
    for p in primes:
        ps = p ** (-s)
        factor = 1.0 / (1 - ps)
        log_deriv_term = math.log(p) * ps / (1 - ps)
        factors.append({
            'p': p,
            'factor_abs': abs(factor),
            'factor_arg': cmath_phase(factor),
            'log_deriv_abs': abs(log_deriv_term),
        })
        log_deriv_terms.append(log_deriv_term)

    # Total log derivative
    total_log_deriv = sum(log_deriv_terms)

    # Product of all factors
    product = complex(1, 0)
    for p in primes:
        ps = p ** (-s)
        product *= 1.0 / (1 - ps)

    zeta_approx = product
    zeta_prime_approx = -zeta_approx * total_log_deriv

    return {
        't': t_near_zero,
        'sigma': sigma,
        'zeta_euler_abs': abs(zeta_approx),
        'zeta_prime_euler_abs': abs(zeta_prime_approx),
        'log_deriv_abs': abs(total_log_deriv),
        'num_small_factors': sum(1 for f in factors if f['factor_abs'] < 0.5),
        'smallest_factor': min(f['factor_abs'] for f in factors),
    }


def main():
    primes = primes_up_to(200)
    print(f"Using {len(primes)} primes up to 200", file=sys.stderr)

    # ============================================================
    # Investigation 2A: Can log|zeta| diverge to -infty?
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("INVESTIGATION 2A: Log divergence analysis", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    divergence_results = {}
    for sigma in [0.55, 0.6, 0.7, 0.8, 1.0]:
        result = investigate_log_divergence(sigma, primes, 10000)
        divergence_results[sigma] = result
        print(f"\nsigma={sigma}:", file=sys.stderr)
        print(f"  E[log|zeta|] = {result['mean_log_zeta']:.4f}", file=sys.stderr)
        print(f"  Std[log|zeta|] = {result['std_log_zeta']:.4f}", file=sys.stderr)
        print(f"  Min log|zeta| = {result['min_log_zeta']:.4f} "
              f"({result['min_in_stds']:.1f} stds below mean)", file=sys.stderr)
        print(f"  Theoretical var = {result['theoretical_var']:.4f}, "
              f"measured var = {result['var_log_zeta']:.4f}", file=sys.stderr)

    # ============================================================
    # Investigation 2B: Random Euler product joint distribution
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("INVESTIGATION 2B: Random Euler product joint (Z, Z')", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    random_ep_results = {}
    for sigma in [0.6, 0.7, 0.8]:
        print(f"\nSampling random Euler product at sigma={sigma}...", file=sys.stderr)
        start = time.time()
        samples = random_euler_product_joint(sigma, num_primes=46, num_samples=100000)
        elapsed = time.time() - start
        print(f"  {len(samples)} samples in {elapsed:.1f}s", file=sys.stderr)

        random_ep_results[sigma] = samples

        # Basic statistics
        abs_Z = [s['abs_Z'] for s in samples]
        abs_Zp = [s['abs_Zprime'] for s in samples]

        # Correlation
        n = len(samples)
        mean_z = sum(abs_Z) / n
        mean_zp = sum(abs_Zp) / n
        var_z = sum((x - mean_z)**2 for x in abs_Z) / n
        var_zp = sum((x - mean_zp)**2 for x in abs_Zp) / n
        cov = sum((abs_Z[i] - mean_z) * (abs_Zp[i] - mean_zp) for i in range(n)) / n
        corr = cov / (var_z**0.5 * var_zp**0.5) if var_z > 0 and var_zp > 0 else 0

        print(f"  E[|Z|] = {mean_z:.4f}, E[|Z'|] = {mean_zp:.4f}", file=sys.stderr)
        print(f"  Corr(|Z|, |Z'|) = {corr:.4f}", file=sys.stderr)
        print(f"  min|Z| = {min(abs_Z):.6f}, min|Z'| = {min(abs_Zp):.6f}", file=sys.stderr)

        # Conditional analysis
        eps_values = [0.01, 0.05, 0.1, 0.5, 1.0]
        cond = analyze_conditional_derivative(samples, eps_values)

        print(f"\n  Conditional |Z'| given |Z| < epsilon:", file=sys.stderr)
        for eps in eps_values:
            c = cond[eps]
            if c['count'] >= 3:
                print(f"    |Z|<{eps}: n={c['count']}, "
                      f"min|Z'|={c['min']:.4f}, mean|Z'|={c['mean']:.4f}, "
                      f"median|Z'|={c['median']:.4f}", file=sys.stderr)
            else:
                print(f"    |Z|<{eps}: n={c['count']} (too few)", file=sys.stderr)

    # ============================================================
    # Investigation 2C: Key theoretical analysis
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("INVESTIGATION 2C: Why zeros need sigma <= 1/2", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    # The Euler product tells us log|zeta(sigma+it)| = sum_p f_p(t)
    # where f_p(t) = -log|1 - p^{-sigma-it}|.
    # For sigma > 1/2, the variance sum_p Var(f_p) < infty.
    # By CLT-type results, log|zeta| is approximately Gaussian.
    # A Gaussian variable can take any value, but with probability:
    # P(log|zeta| < -L) ~ exp(-L^2 / (2*V(sigma)))
    # For a zero, we need log|zeta| = -infty, which has probability 0.
    # But this is for the RANDOM model -- actual zeta could in principle have zeros.

    # The derivative: Z'(s) = -Z(s) * sum_p (log p) p^{-s} / (1 - p^{-s})
    # When Z is small, Z' = Z * (Z'/Z). The log-derivative Z'/Z is essentially
    # independent of Z (since it's the derivative of the log, which is the SUM
    # of independent terms, not the PRODUCT).
    # So the conditional distribution of Z' given Z = z is approximately:
    # Z' = z * (random variable with fixed distribution)
    # This means |Z'| ~ |Z| * C, so |Z'| -> 0 as |Z| -> 0!

    # THIS IS THE KEY INSIGHT: the Euler product structure means that
    # as |zeta| -> 0, the derivative |zeta'| also -> 0, proportionally.
    # Specifically: |zeta'|/|zeta| has a well-defined limiting distribution
    # as |zeta| -> 0 (it approaches the distribution of the log-derivative).

    # Let's verify this computationally
    print("\nVerifying: is |Z'/Z| = |log-derivative| stable as |Z| -> 0?", file=sys.stderr)

    for sigma in [0.6, 0.7, 0.8]:
        samples = random_ep_results[sigma]

        # Bin samples by |Z| and compute |Z'/Z| statistics in each bin
        bins = [(0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 5.0), (5.0, 100.0)]

        print(f"\nsigma={sigma}: |Z'/Z| (log-derivative magnitude) by |Z| bin:", file=sys.stderr)
        for lo, hi in bins:
            in_bin = [s for s in samples if lo <= s['abs_Z'] < hi]
            if len(in_bin) < 5:
                print(f"  [{lo:.1f}, {hi:.1f}): n={len(in_bin)} (too few)", file=sys.stderr)
                continue
            ratios = [s['abs_Zprime'] / max(s['abs_Z'], 1e-15) for s in in_bin]
            mean_ratio = sum(ratios) / len(ratios)
            ratios_sorted = sorted(ratios)
            median_ratio = ratios_sorted[len(ratios_sorted) // 2]
            print(f"  [{lo:.1f}, {hi:.1f}): n={len(in_bin)}, "
                  f"mean|Z'/Z|={mean_ratio:.4f}, median|Z'/Z|={median_ratio:.4f}", file=sys.stderr)

    # ============================================================
    # Investigation 3: Derivative at zeros via Z'/Z
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("INVESTIGATION 3: Implications for derivative at zeros", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    # If |Z'/Z| has a well-defined distribution (call it mu) as |Z| -> 0,
    # then at a hypothetical zero with |Z| = 0:
    #   |Z'| = |Z| * |Z'/Z| -> 0 * (finite) = 0
    # But this is just the trivial statement that lim |Z'| -> 0 as Z -> 0.
    #
    # However, for a genuine zero, Z' = lim_{s->rho} (s-rho)*Z(s) * (Z'/Z(s)) / (s-rho)
    # which involves a 0/0 limit. The actual derivative is:
    #   Z'(rho) = lim_{s->rho} Z(s)/(s-rho) * (s-rho) * Z'(s)/Z(s) ... no, simpler:
    #   Z(s) = (s-rho)*Z_1(s) where Z_1(rho) != 0 (for a simple zero)
    #   Z'(s) = Z_1(s) + (s-rho)*Z_1'(s)
    #   Z'(rho) = Z_1(rho)
    #
    # So the derivative at a zero is the "regularized value" Z_1(rho), NOT
    # the naive limit of Z(s) * (Z'/Z)(s).
    #
    # The Euler product analysis tells us about the REGULAR part of zeta.
    # At a zero, Z'/Z has a POLE (simple pole with residue 1 for a simple zero).
    # So the Euler product sum sum_p (log p) p^{-rho}/(1-p^{-rho}) DIVERGES at a zero.

    # Let's study the behavior of the prime sum near actual zeros (on the critical line)
    print("\nPrime sum behavior near critical-line zeros:", file=sys.stderr)
    primes_100 = primes_up_to(100)

    # Use known zeros of zeta on the critical line
    known_zeros_t = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
                     37.5862, 40.9187, 43.3271, 48.0052, 49.7738]

    for t0 in known_zeros_t[:5]:
        s0 = complex(0.5, t0)
        # Compute the prime sum at points approaching the zero
        print(f"\n  Zero at t={t0}:", file=sys.stderr)
        for delta in [1.0, 0.1, 0.01, 0.001]:
            s = complex(0.5, t0 + delta)
            log_deriv_sum = complex(0, 0)
            for p in primes_100:
                ps = p ** (-s)
                log_deriv_sum += math.log(p) * ps / (1 - ps)

            z_val = mpmath.zeta(mpmath.mpc(0.5, t0 + delta))
            z_prime = mpmath.zeta(mpmath.mpc(0.5, t0 + delta), derivative=1) if hasattr(mpmath, 'zeta') else None

            # Compute zeta'/zeta directly
            h = 1e-8
            z_plus = mpmath.zeta(mpmath.mpc(0.5, t0 + delta + h))
            z_minus = mpmath.zeta(mpmath.mpc(0.5, t0 + delta - h))
            z_deriv = (z_plus - z_minus) / (2 * h)

            if abs(z_val) > 1e-15:
                log_deriv_exact = z_deriv / z_val
                print(f"    delta={delta}: |zeta|={float(abs(z_val)):.6e}, "
                      f"|zeta'/zeta| exact={float(abs(log_deriv_exact)):.4f}, "
                      f"prime sum={abs(log_deriv_sum):.4f}", file=sys.stderr)
            else:
                print(f"    delta={delta}: |zeta|={float(abs(z_val)):.6e} (very small)", file=sys.stderr)

    # ============================================================
    # Print summary
    # ============================================================
    print("\n" + "=" * 70)
    print("EULER PRODUCT ANALYSIS SUMMARY")
    print("=" * 70)

    print("\n--- Log Divergence Analysis ---")
    for sigma in sorted(divergence_results.keys()):
        r = divergence_results[sigma]
        print(f"sigma={sigma}: E[log|zeta|]={r['mean_log_zeta']:.3f}, "
              f"Std={r['std_log_zeta']:.3f}, "
              f"Min={r['min_log_zeta']:.3f} ({r['min_in_stds']:.1f} sigma)")

    print("\n--- Key Theoretical Finding ---")
    print("The Euler product structure implies |Z'/Z| has a STABLE distribution")
    print("as |Z| -> 0. This means |Z'| ~ |Z| * C (a constant drawn from the")
    print("log-derivative distribution). As |Z| -> 0, |Z'| -> 0 proportionally.")
    print("")
    print("At a genuine ZERO, however, Z'/Z has a POLE (with residue 1 for simple zeros).")
    print("The Euler product sum over primes DIVERGES at an actual zero.")
    print("This divergence is what 'creates' the finite nonzero derivative Z'(rho).")
    print("")
    print("The chi-constraint requires |Z'(rho)| ~ t^{1/2-sigma} -> 0.")
    print("But the pole-residue structure gives |Z'(rho)| a specific value related to")
    print("HOW the Euler product sum diverges. This is the key tension.")

    # Save results
    output = {
        'divergence': {str(k): {kk: vv for kk, vv in v.items() if kk != 'all_results'}
                       for k, v in divergence_results.items()},
    }
    with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/joint-zeta-derivative/euler_product_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)


if __name__ == '__main__':
    main()
