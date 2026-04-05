"""
Joint distribution of (zeta, zeta') at sigma > 1/2.

Investigation 1: Compute (zeta(sigma+it), zeta'(sigma+it)) at many t values
and analyze the joint distribution, conditional distributions, and
test whether the chi-constraint region is accessible.
"""

import mpmath
import json
import time
import sys

mpmath.mp.dps = 25  # 25 decimal places

def compute_zeta_and_derivative(sigma, t):
    """Compute zeta(s) and zeta'(s) at s = sigma + it."""
    s = mpmath.mpc(sigma, t)
    z = mpmath.zeta(s)
    # Compute derivative via central difference (mpmath doesn't have built-in zeta')
    h = mpmath.mpf('1e-8')
    z_plus = mpmath.zeta(s + h)
    z_minus = mpmath.zeta(s - h)
    zp = (z_plus - z_minus) / (2 * h)
    return z, zp

def compute_zeta_derivative_series(sigma, t, N=2000):
    """Compute zeta'(s) = -sum_{n=2}^{N} log(n)/n^s via Dirichlet series.
    Only accurate for sigma > 1, but gives the Euler-product correlated structure."""
    s = mpmath.mpc(sigma, t)
    zp = mpmath.mpc(0, 0)
    for n in range(2, N+1):
        zp -= mpmath.log(n) * mpmath.power(n, -s)
    return zp

def chi_function(sigma, t):
    """Compute |chi(sigma+it)| where zeta(s) = chi(s)*zeta(1-s).
    chi(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s).
    For large t, |chi(sigma+it)| ~ (t/(2*pi))^{1/2-sigma}.
    """
    s = mpmath.mpc(sigma, t)
    chi = (mpmath.power(2, s) * mpmath.power(mpmath.pi, s - 1) *
           mpmath.sin(mpmath.pi * s / 2) * mpmath.gamma(1 - s))
    return abs(chi)

def survey_joint_distribution(sigma, t_start, t_end, t_step):
    """Sample (|zeta|, |zeta'|) at many t values for fixed sigma."""
    results = []
    t = t_start
    count = 0
    while t <= t_end:
        try:
            z, zp = compute_zeta_and_derivative(sigma, t)
            abs_z = float(abs(z))
            abs_zp = float(abs(zp))
            results.append({
                't': float(t),
                'abs_zeta': abs_z,
                'abs_zeta_prime': abs_zp,
                'arg_zeta': float(mpmath.arg(z)),
                'arg_zeta_prime': float(mpmath.arg(zp)),
            })
        except Exception as e:
            pass  # skip problematic points
        t += t_step
        count += 1
        if count % 500 == 0:
            print(f"  sigma={sigma}: completed {count} points, t={float(t):.1f}", file=sys.stderr)
    return results

def conditional_analysis(results, epsilon_values):
    """Given |zeta| < epsilon, what is the distribution of |zeta'|?"""
    analysis = {}
    for eps in epsilon_values:
        near_zero = [r for r in results if r['abs_zeta'] < eps]
        if len(near_zero) == 0:
            analysis[eps] = {
                'count': 0,
                'total': len(results),
                'fraction': 0,
                'min_derivative': None,
                'max_derivative': None,
                'mean_derivative': None,
                'median_derivative': None,
            }
        else:
            derivs = sorted([r['abs_zeta_prime'] for r in near_zero])
            analysis[eps] = {
                'count': len(near_zero),
                'total': len(results),
                'fraction': len(near_zero) / len(results),
                'min_derivative': derivs[0],
                'max_derivative': derivs[-1],
                'mean_derivative': sum(derivs) / len(derivs),
                'median_derivative': derivs[len(derivs)//2],
                'percentile_10': derivs[max(0, len(derivs)//10)],
                'percentile_90': derivs[min(len(derivs)-1, 9*len(derivs)//10)],
                'all_t_values': [r['t'] for r in near_zero],
                'all_derivatives': derivs,
            }
    return analysis

def chi_constraint_check(sigma, t_values):
    """At given t values, compute |chi(sigma+it)| and check what derivative
    magnitude would be required at an off-line zero."""
    constraints = []
    for t in t_values:
        chi_val = float(chi_function(sigma, t))
        # At a zero, |zeta'(sigma+it)| = |chi| * |zeta'((1-sigma)+it)|
        # For the mirror derivative, use typical size ~ t^{0.49}
        typical_mirror_deriv = float(t)**0.49
        required_deriv = chi_val * typical_mirror_deriv
        constraints.append({
            't': t,
            'chi': chi_val,
            'typical_mirror_deriv': typical_mirror_deriv,
            'required_deriv_at_zero': required_deriv,
        })
    return constraints

def compute_correlation(results):
    """Compute correlation between |zeta| and |zeta'|."""
    n = len(results)
    abs_z = [r['abs_zeta'] for r in results]
    abs_zp = [r['abs_zeta_prime'] for r in results]

    mean_z = sum(abs_z) / n
    mean_zp = sum(abs_zp) / n

    var_z = sum((x - mean_z)**2 for x in abs_z) / n
    var_zp = sum((x - mean_zp)**2 for x in abs_zp) / n

    cov = sum((abs_z[i] - mean_z) * (abs_zp[i] - mean_zp) for i in range(n)) / n

    corr = cov / (var_z**0.5 * var_zp**0.5) if var_z > 0 and var_zp > 0 else 0

    # Also compute log-space correlation
    log_z = [mpmath.log(max(x, 1e-15)) for x in abs_z]
    log_zp = [mpmath.log(max(x, 1e-15)) for x in abs_zp]

    mean_lz = sum(log_z) / n
    mean_lzp = sum(log_zp) / n
    var_lz = sum((x - mean_lz)**2 for x in log_z) / n
    var_lzp = sum((x - mean_lzp)**2 for x in log_zp) / n
    cov_l = sum((log_z[i] - mean_lz) * (log_zp[i] - mean_lzp) for i in range(n)) / n

    log_corr = float(cov_l / (var_lz**0.5 * var_lzp**0.5)) if var_lz > 0 and var_lzp > 0 else 0

    return {
        'pearson_abs': float(corr),
        'pearson_log': log_corr,
        'mean_abs_zeta': float(mean_z),
        'mean_abs_zeta_prime': float(mean_zp),
        'std_abs_zeta': float(var_z**0.5),
        'std_abs_zeta_prime': float(var_zp**0.5),
    }


def main():
    sigmas = [0.6, 0.7, 0.8]
    all_results = {}

    # Phase 1: Survey at moderate range with fine step
    print("=" * 70, file=sys.stderr)
    print("PHASE 1: Joint distribution survey", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    for sigma in sigmas:
        print(f"\nSurveying sigma = {sigma}...", file=sys.stderr)
        start_time = time.time()

        # Sample from t=100 to t=10000, step ~3 (gives ~3300 points)
        results = survey_joint_distribution(sigma, 100, 10000, 3.0)
        elapsed = time.time() - start_time
        print(f"  Completed {len(results)} points in {elapsed:.1f}s", file=sys.stderr)

        all_results[sigma] = results

    # Phase 2: Conditional analysis
    print("\n" + "=" * 70, file=sys.stderr)
    print("PHASE 2: Conditional analysis", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    epsilon_values = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0]
    conditional_results = {}

    for sigma in sigmas:
        cond = conditional_analysis(all_results[sigma], epsilon_values)
        conditional_results[sigma] = cond

        print(f"\nConditional distribution at sigma = {sigma}:", file=sys.stderr)
        for eps in epsilon_values:
            c = cond[eps]
            if c['count'] > 0:
                print(f"  |zeta| < {eps}: {c['count']}/{c['total']} points "
                      f"({c['fraction']*100:.2f}%)", file=sys.stderr)
                print(f"    |zeta'| range: [{c['min_derivative']:.4f}, {c['max_derivative']:.4f}]", file=sys.stderr)
                print(f"    |zeta'| mean: {c['mean_derivative']:.4f}, median: {c['median_derivative']:.4f}", file=sys.stderr)
            else:
                print(f"  |zeta| < {eps}: 0 points found", file=sys.stderr)

    # Phase 3: Chi constraint check
    print("\n" + "=" * 70, file=sys.stderr)
    print("PHASE 3: Chi constraint analysis", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    chi_results = {}
    for sigma in sigmas:
        t_check = [100, 500, 1000, 5000, 10000]
        constraints = chi_constraint_check(sigma, t_check)
        chi_results[sigma] = constraints

        print(f"\nChi constraint at sigma = {sigma}:", file=sys.stderr)
        for c in constraints:
            print(f"  t={c['t']}: |chi|={c['chi']:.6f}, "
                  f"required |zeta'| at zero = {c['required_deriv_at_zero']:.6f}", file=sys.stderr)

    # Phase 4: Correlation analysis
    print("\n" + "=" * 70, file=sys.stderr)
    print("PHASE 4: Correlation analysis", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    correlation_results = {}
    for sigma in sigmas:
        corr = compute_correlation(all_results[sigma])
        correlation_results[sigma] = corr
        print(f"\nCorrelations at sigma = {sigma}:", file=sys.stderr)
        print(f"  Pearson(|zeta|, |zeta'|) = {corr['pearson_abs']:.4f}", file=sys.stderr)
        print(f"  Pearson(log|zeta|, log|zeta'|) = {corr['pearson_log']:.4f}", file=sys.stderr)
        print(f"  E[|zeta|] = {corr['mean_abs_zeta']:.4f}, "
              f"E[|zeta'|] = {corr['mean_abs_zeta_prime']:.4f}", file=sys.stderr)

    # Phase 5: Check if chi-constraint region is populated
    print("\n" + "=" * 70, file=sys.stderr)
    print("PHASE 5: Chi-constraint region accessibility", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    accessibility_results = {}
    for sigma in sigmas:
        results = all_results[sigma]

        # For each t, compute chi-constraint derivative threshold
        accessible_count = 0
        total_near_zero = 0
        details = []

        for r in results:
            t = r['t']
            chi_val = float(chi_function(sigma, t))
            # Required derivative at a zero: |zeta'| = |chi| * |zeta'_mirror|
            # Use typical mirror derivative ~ t^0.49
            required = chi_val * (t ** 0.49)

            # Is this point "near zero" AND has derivative below required?
            if r['abs_zeta'] < 0.5:
                total_near_zero += 1
                if r['abs_zeta_prime'] < required:
                    accessible_count += 1
                    details.append({
                        't': t,
                        'abs_zeta': r['abs_zeta'],
                        'abs_zeta_prime': r['abs_zeta_prime'],
                        'chi_threshold': required,
                    })

        accessibility_results[sigma] = {
            'near_zero_count': total_near_zero,
            'accessible_count': accessible_count,
            'details': details,
        }

        print(f"\nAccessibility at sigma = {sigma}:", file=sys.stderr)
        print(f"  Points with |zeta| < 0.5: {total_near_zero}", file=sys.stderr)
        print(f"  Of these, |zeta'| < chi-threshold: {accessible_count}", file=sys.stderr)
        if details:
            for d in details[:5]:
                print(f"    t={d['t']:.1f}: |zeta|={d['abs_zeta']:.6f}, "
                      f"|zeta'|={d['abs_zeta_prime']:.6f}, threshold={d['chi_threshold']:.6f}", file=sys.stderr)

    # Save all results
    output = {
        'sigmas': sigmas,
        'conditional': {},
        'chi_constraints': {},
        'correlations': correlation_results,
        'accessibility': {},
    }

    for sigma in sigmas:
        key = str(sigma)
        # Save conditional analysis (without full derivative lists for large eps)
        cond_save = {}
        for eps in epsilon_values:
            c = conditional_results[sigma][eps]
            cond_save[str(eps)] = {
                'count': c['count'],
                'total': c['total'],
                'fraction': c['fraction'],
                'min_derivative': c['min_derivative'],
                'max_derivative': c['max_derivative'],
                'mean_derivative': c['mean_derivative'],
            }
        output['conditional'][key] = cond_save
        output['chi_constraints'][key] = chi_results[sigma]
        output['accessibility'][key] = {
            'near_zero_count': accessibility_results[sigma]['near_zero_count'],
            'accessible_count': accessibility_results[sigma]['accessible_count'],
        }

    with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/joint-zeta-derivative/joint_distribution_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print("\nResults saved to joint_distribution_results.json", file=sys.stderr)

    # Print summary to stdout for capture
    print("JOINT DISTRIBUTION ANALYSIS COMPLETE")
    print("=" * 70)

    for sigma in sigmas:
        print(f"\n--- sigma = {sigma} ---")
        corr = correlation_results[sigma]
        print(f"Correlation (|zeta|, |zeta'|): {corr['pearson_abs']:.4f}")
        print(f"Correlation (log|zeta|, log|zeta'|): {corr['pearson_log']:.4f}")
        print(f"E[|zeta|] = {corr['mean_abs_zeta']:.4f}")
        print(f"E[|zeta'|] = {corr['mean_abs_zeta_prime']:.4f}")

        print(f"\nConditional |zeta'| given |zeta| < epsilon:")
        for eps in epsilon_values:
            c = conditional_results[sigma][eps]
            if c['count'] > 0:
                print(f"  eps={eps}: n={c['count']}, "
                      f"min|zeta'|={c['min_derivative']:.4f}, "
                      f"mean|zeta'|={c['mean_derivative']:.4f}")
            else:
                print(f"  eps={eps}: no points")

        print(f"\nChi-constraint accessibility (|zeta| < 0.5):")
        acc = accessibility_results[sigma]
        print(f"  {acc['near_zero_count']} near-zero points, "
              f"{acc['accessible_count']} with derivative below chi-threshold")

    # Phase 6: Dense sampling near near-zero events
    print("\n" + "=" * 70, file=sys.stderr)
    print("PHASE 6: Dense sampling around near-zero events", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    for sigma in sigmas:
        # Find t values where |zeta| was smallest
        results = all_results[sigma]
        sorted_by_zeta = sorted(results, key=lambda r: r['abs_zeta'])[:10]

        print(f"\nDense sampling near smallest |zeta| at sigma={sigma}:", file=sys.stderr)
        for r in sorted_by_zeta[:5]:
            t_center = r['t']
            # Sample densely around this t
            dense_results = []
            for dt in [x * 0.01 for x in range(-50, 51)]:
                t_local = t_center + dt
                try:
                    z, zp = compute_zeta_and_derivative(sigma, t_local)
                    dense_results.append({
                        't': float(t_local),
                        'dt': dt,
                        'abs_zeta': float(abs(z)),
                        'abs_zeta_prime': float(abs(zp)),
                    })
                except:
                    pass

            # Find minimum in dense sample
            if dense_results:
                min_pt = min(dense_results, key=lambda x: x['abs_zeta'])
                chi_val = float(chi_function(sigma, min_pt['t']))
                required = chi_val * (min_pt['t'] ** 0.49)

                print(f"  Near t={t_center:.1f}: min|zeta|={min_pt['abs_zeta']:.8f} "
                      f"at t={min_pt['t']:.4f}", file=sys.stderr)
                print(f"    |zeta'| there = {min_pt['abs_zeta_prime']:.6f}", file=sys.stderr)
                print(f"    chi-threshold = {required:.6f}", file=sys.stderr)
                print(f"    ratio |zeta'|/threshold = {min_pt['abs_zeta_prime']/required:.2f}", file=sys.stderr)


if __name__ == '__main__':
    main()
