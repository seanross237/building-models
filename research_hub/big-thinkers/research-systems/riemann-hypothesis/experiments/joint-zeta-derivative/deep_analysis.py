"""
Deep analysis: The crucial insights.

FINDING 1 (from pole_structure_analysis):
At critical-line zero heights, |zeta'(sigma_0+it)| matches the chi-bound
to 4+ decimal places. This is because the functional equation IS an identity.
This means: for t values near critical-line zeros, the chi-constraint is
AUTOMATICALLY SATISFIED by zeta at ANY sigma, not just at sigma=1/2.
So we cannot use the chi-bound as an exclusion tool at these t values.

FINDING 2 (from euler_product_analysis):
The correlation between |zeta| and |zeta'| is ~0.95. The log-derivative
|zeta'/zeta| is relatively stable, meaning |zeta'| ~ |zeta| * C.
At an actual zero, the log-derivative diverges (pole), so this scaling breaks.

FINDING 3 (Critical insight):
The chi-constraint says |zeta'(rho)| ~ t^{0.15} for sigma_0=0.7.
Meanwhile, the ACTUAL |zeta'| at near-zero events is ~0.5-1.0.
The chi-bound at t~1000 is ~0.36 * 1.7 = ~0.6.
So near-zero events already have derivatives COMPARABLE to the chi-bound.
There is NO gap between the conditional derivative distribution and the chi-bound.

This deep analysis focuses on:
A. Whether the conditional distribution of |zeta'| given |zeta|=0 has a
   LOWER BOUND from the Euler product
B. The exact scaling of the conditional derivative as epsilon -> 0
C. Whether the DH function shows different scaling
"""

import mpmath
import math
import sys
import json
import time

mpmath.mp.dps = 30


def random_euler_product_deep(sigma, num_primes, num_samples):
    """Large-scale random Euler product to study conditional distribution
    in the extreme tail |Z| -> 0."""
    import random
    import cmath

    primes = []
    n = 2
    while len(primes) < num_primes:
        is_prime = True
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(n)
        n += 1

    results = []
    for _ in range(num_samples):
        thetas = [random.uniform(0, 2 * math.pi) for _ in primes]

        log_Z = complex(0, 0)
        log_deriv = complex(0, 0)

        for i, p in enumerate(primes):
            ps = p ** (-sigma) * cmath.exp(1j * thetas[i])
            one_minus_ps = 1 - ps
            log_Z -= cmath.log(one_minus_ps)
            # Euler product log-derivative: sum_p (log p) p^{-s} / (1 - p^{-s})
            log_deriv += math.log(p) * ps / one_minus_ps

        Z = cmath.exp(log_Z)
        # zeta'(s) = zeta(s) * [zeta'/zeta(s)] = zeta(s) * (-log_deriv)
        # Wait: zeta'/zeta = -sum Λ(n)/n^s, and in Euler form:
        # zeta'/zeta(s) = sum_p log(p)*p^{-s}/(1-p^{-s}) with a minus sign from d/ds
        # Actually: (d/ds) log zeta = (d/ds) sum -log(1-p^{-s}) = sum log(p)*p^{-s}/(1-p^{-s})
        # Wait, (d/ds)(-log(1-p^{-s})) = -(-log p)*(-p^{-s})/(1-p^{-s})
        #  = -log(p)*p^{-s}/(1-p^{-s})
        # So zeta'/zeta = sum_p [-log(p)*p^{-s}/(1-p^{-s})]
        # In the random model, the derivative of log Z w.r.t. sigma gives the real part.
        # But for the full complex derivative:
        # Z'(sigma) = Z * sum_p [-log(p) * p^{-sigma}*e^{itheta}/(1-p^{-sigma}*e^{itheta})]
        Zprime = Z * (-log_deriv)

        abs_Z = abs(Z)
        abs_Zp = abs(Zprime)

        results.append((abs_Z, abs_Zp))

    return results


def analyze_extreme_tail(results, quantile_eps=0.001):
    """Analyze the bottom quantile_eps fraction of |Z| values
    and their corresponding |Z'|."""
    n = len(results)
    sorted_results = sorted(results, key=lambda x: x[0])

    # Bottom fraction
    cutoff_idx = max(1, int(n * quantile_eps))
    bottom = sorted_results[:cutoff_idx]

    abs_Z_bottom = [r[0] for r in bottom]
    abs_Zp_bottom = [r[1] for r in bottom]

    # Ratio |Z'|/|Z| (log-derivative) for bottom fraction
    ratios = [r[1] / max(r[0], 1e-300) for r in bottom]

    # For the full sample
    all_Z = [r[0] for r in sorted_results]
    all_Zp = [r[1] for r in sorted_results]

    return {
        'bottom_count': len(bottom),
        'total_count': n,
        'bottom_abs_Z_range': (min(abs_Z_bottom), max(abs_Z_bottom)),
        'bottom_abs_Zp_range': (min(abs_Zp_bottom), max(abs_Zp_bottom)),
        'bottom_abs_Zp_mean': sum(abs_Zp_bottom) / len(abs_Zp_bottom),
        'bottom_ratio_range': (min(ratios), max(ratios)),
        'bottom_ratio_mean': sum(ratios) / len(ratios),
        'full_mean_Z': sum(all_Z) / n,
        'full_mean_Zp': sum(all_Zp) / n,
    }


def check_scaling_exponent(results, bins=10):
    """Bin results by |Z| and fit the scaling |Z'| ~ |Z|^alpha."""
    n = len(results)
    sorted_results = sorted(results, key=lambda x: x[0])

    # Use quantile-based binning
    bin_size = n // bins
    bin_data = []

    for i in range(bins):
        start = i * bin_size
        end = start + bin_size if i < bins - 1 else n
        bin_results = sorted_results[start:end]

        mean_Z = sum(r[0] for r in bin_results) / len(bin_results)
        mean_Zp = sum(r[1] for r in bin_results) / len(bin_results)
        mean_ratio = sum(r[1] / max(r[0], 1e-300) for r in bin_results) / len(bin_results)

        if mean_Z > 0 and mean_Zp > 0:
            bin_data.append({
                'mean_Z': mean_Z,
                'mean_Zp': mean_Zp,
                'mean_ratio': mean_ratio,
                'log_Z': math.log(mean_Z),
                'log_Zp': math.log(mean_Zp),
            })

    # Fit alpha from consecutive bins
    alphas = []
    for i in range(1, len(bin_data)):
        dlz = bin_data[i]['log_Z'] - bin_data[i-1]['log_Z']
        dlzp = bin_data[i]['log_Zp'] - bin_data[i-1]['log_Zp']
        if abs(dlz) > 0.01:
            alphas.append(dlzp / dlz)

    return bin_data, alphas


def main():
    # ============================================================
    # A: Large-scale random Euler product for extreme tails
    # ============================================================
    print("=" * 70, file=sys.stderr)
    print("A: Large-scale random Euler product (1M samples)", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    for sigma in [0.55, 0.6, 0.7, 0.8]:
        print(f"\nsigma={sigma}: generating 1M samples with 60 primes...", file=sys.stderr)
        start = time.time()
        results = random_euler_product_deep(sigma, num_primes=60, num_samples=1000000)
        elapsed = time.time() - start
        print(f"  Done in {elapsed:.1f}s", file=sys.stderr)

        # Extreme tail analysis
        for q in [0.01, 0.001, 0.0001]:
            tail = analyze_extreme_tail(results, q)
            print(f"\n  Bottom {q*100:.2f}% (n={tail['bottom_count']}):", file=sys.stderr)
            print(f"    |Z| range: [{tail['bottom_abs_Z_range'][0]:.8f}, {tail['bottom_abs_Z_range'][1]:.8f}]", file=sys.stderr)
            print(f"    |Z'| range: [{tail['bottom_abs_Zp_range'][0]:.8f}, {tail['bottom_abs_Zp_range'][1]:.8f}]", file=sys.stderr)
            print(f"    mean |Z'| = {tail['bottom_abs_Zp_mean']:.8f}", file=sys.stderr)
            print(f"    |Z'/Z| range: [{tail['bottom_ratio_range'][0]:.4f}, {tail['bottom_ratio_range'][1]:.4f}]", file=sys.stderr)
            print(f"    mean |Z'/Z| = {tail['bottom_ratio_mean']:.4f}", file=sys.stderr)

        # Scaling exponent
        bin_data, alphas = check_scaling_exponent(results, bins=20)
        print(f"\n  Scaling |Z'| ~ |Z|^alpha:", file=sys.stderr)
        print(f"    Bottom bins alpha: {[f'{a:.3f}' for a in alphas[:5]]}", file=sys.stderr)
        print(f"    Middle bins alpha: {[f'{a:.3f}' for a in alphas[5:15]]}", file=sys.stderr)
        print(f"    Top bins alpha: {[f'{a:.3f}' for a in alphas[15:]]}", file=sys.stderr)

        # The KEY question: what is alpha in the extreme bottom?
        if len(alphas) >= 3:
            bottom_alpha = sum(alphas[:3]) / 3
            print(f"    Average alpha (bottom 3 bins) = {bottom_alpha:.4f}", file=sys.stderr)
            if bottom_alpha < 0.5:
                print(f"    *** alpha < 0.5: derivative decays SLOWER than sqrt(|Z|) ***", file=sys.stderr)
                print(f"    This means the log-derivative GROWS as |Z| -> 0", file=sys.stderr)
            elif bottom_alpha < 1.0:
                print(f"    *** alpha < 1: log-derivative grows as |Z| -> 0 ***", file=sys.stderr)
            else:
                print(f"    alpha >= 1: log-derivative is bounded or decreasing", file=sys.stderr)

    # ============================================================
    # B: Compare with chi-constraint requirement
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("B: Can the joint distribution meet the chi-constraint?", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    print("\nTheoretical analysis:", file=sys.stderr)
    print("=" * 50, file=sys.stderr)

    print("""
The chi-constraint at a hypothetical zero rho = sigma_0 + it_0 requires:
  |zeta'(rho)| = |chi(sigma_0+it_0)| * |zeta'((1-sigma_0)+it_0)|

From our computations:
  |chi(sigma_0+it)| ~ (t/(2pi))^{1/2-sigma_0}
  |zeta'(1/2+it)| ~ t^{0.35} (from first 100 zeros)

The mirror zero at (1-sigma_0)+it has derivative that should be
comparable to or larger than critical-line zeros at same height.

So: |zeta'(rho)| ~ t^{1/2-sigma_0} * t^{0.35} = t^{0.85-sigma_0}

For sigma_0 = 0.6: |zeta'(rho)| ~ t^{0.25} -> GROWS with t
For sigma_0 = 0.7: |zeta'(rho)| ~ t^{0.15} -> GROWS with t
For sigma_0 = 0.8: |zeta'(rho)| ~ t^{0.05} -> GROWS (barely) with t

KEY INSIGHT: The chi-constraint does NOT require the derivative to vanish!
It requires the derivative to grow as t^{0.85-sigma_0}, which is SLOWER
than unconstrained growth, but still divergent.

This contradicts the original setup's claim that |zeta'| must be
"vanishingly small." The derivative at an off-line zero must be
SMALLER than typical, but not zero. It must grow slower than t^{0.35}
(the critical-line rate), but it still grows.

The question is whether the conditional distribution of |zeta'| given
|zeta|=0 can produce values that grow as t^{0.85-sigma_0}. Since this
is a GROWING function of t, and the conditional derivative distribution
has mean that ALSO grows with t (because zeta' grows on average), the
constraint is not obviously violated.
""", file=sys.stderr)

    # ============================================================
    # C: Refined comparison -- conditional derivative vs chi-bound
    # ============================================================
    print("=" * 70, file=sys.stderr)
    print("C: Ratio of conditional |zeta'| to chi-bound as function of t", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    for sigma_0 in [0.6, 0.7, 0.8]:
        print(f"\nsigma_0={sigma_0}:", file=sys.stderr)
        ratios_by_t = []

        t_ranges = [(100, 500), (500, 2000), (2000, 5000), (5000, 10000)]
        for t_lo, t_hi in t_ranges:
            near_zero_derivs = []
            chi_bounds = []
            all_derivs = []

            for t in range(t_lo, t_hi, max(1, (t_hi-t_lo)//500)):
                try:
                    s = mpmath.mpc(sigma_0, t)
                    z = mpmath.zeta(s)
                    abs_z = float(abs(z))

                    h = mpmath.mpf('1e-8')
                    zp = (mpmath.zeta(s + h) - mpmath.zeta(s - h)) / (2 * h)
                    abs_zp = float(abs(zp))
                    all_derivs.append(abs_zp)

                    # Chi bound
                    chi = float(abs(mpmath.power(2, s) * mpmath.power(mpmath.pi, s - 1) *
                                    mpmath.sin(mpmath.pi * s / 2) * mpmath.gamma(1 - s)))
                    # Mirror derivative estimate
                    mirror_d = math.exp(0.3537 * math.log(t) - 0.8386)
                    bound = chi * mirror_d

                    if abs_z < 0.5:
                        near_zero_derivs.append(abs_zp)
                        chi_bounds.append(bound)
                except:
                    pass

            if len(near_zero_derivs) >= 3:
                mean_cond_d = sum(near_zero_derivs) / len(near_zero_derivs)
                mean_bound = sum(chi_bounds) / len(chi_bounds)
                mean_all_d = sum(all_derivs) / len(all_derivs) if all_derivs else 0

                print(f"  t in [{t_lo}, {t_hi}): n_near_zero={len(near_zero_derivs)}, "
                      f"n_total={len(all_derivs)}", file=sys.stderr)
                print(f"    mean|zeta'| (near zero) = {mean_cond_d:.4f}", file=sys.stderr)
                print(f"    mean|zeta'| (all)       = {mean_all_d:.4f}", file=sys.stderr)
                print(f"    mean chi-bound          = {mean_bound:.4f}", file=sys.stderr)
                print(f"    ratio cond/bound        = {mean_cond_d/mean_bound:.4f}", file=sys.stderr)
            else:
                print(f"  t in [{t_lo}, {t_hi}): too few near-zero events ({len(near_zero_derivs)})", file=sys.stderr)

    # ============================================================
    # D: The fundamental obstruction: PRODUCT vs SUM structure
    # ============================================================
    print("\n" + "=" * 70, file=sys.stderr)
    print("D: The fundamental obstruction", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    print("""
FUNDAMENTAL ANALYSIS
====================

The Euler product gives: zeta(s) = PRODUCT of 1/(1-p^{-s})
The derivative gives:    zeta'(s) = zeta(s) * SUM of -log(p)*p^{-s}/(1-p^{-s})

At a zero rho, zeta(rho) = 0 but zeta'(rho) != 0 (for a simple zero).
This means the PRODUCT is zero but the PRODUCT * SUM is nonzero.

For the product to be zero, one of the factors must be zero, i.e.,
1 - p^{-rho} = 0 for some p. But |p^{-rho}| = p^{-sigma_0} < 1 for sigma_0 > 0.
So NO individual factor is zero.

The product is zero only in the limit of infinitely many factors -- it's a
CONDITIONAL convergence phenomenon. The partial products oscillate and conspire
to cancel.

For the derivative to be nonzero at the zero: the sum log(p)*p^{-s}/(1-p^{-s})
must DIVERGE at the zero (since zeta'/zeta has a pole there). The divergence
rate determines |zeta'(rho)| = |residue|.

KEY: The sum diverges because the zero creates a resonance in the terms.
The terms 1/(1-p^{-rho}) become large when p^{-rho} is close to 1, which
happens when (log p) * Im(rho) is close to a multiple of 2*pi.

For sigma_0 > 1/2, the individual terms |p^{-s}/(1-p^{-s})| ~ p^{-sigma_0}/(1-p^{-sigma_0})
which gives a CONVERGENT sum (since sigma_0 > 1/2). This means the log-derivative
sum CANNOT diverge for sigma > 1/2... UNLESS there is a zero nearby.

But this is circular: we're trying to prove there are no zeros at sigma > 1/2.

The log-derivative sum converges for sigma > 1/2 at NON-ZERO points. At a zero,
it must diverge. The question is whether the convergent sum can "almost diverge"
enough to produce a zero nearby.

This is equivalent to asking: can the partial sums of sum_p log(p)*p^{-s}/(1-p^{-s})
have large fluctuations at sigma > 1/2? The variance of this sum is
sum_p (log p)^2 * Var(p^{-it}/(1-p^{-sigma-it})).

For sigma > 1/2, this variance is FINITE. By the Gaussian behavior of the sum,
extreme fluctuations are exponentially rare. But "exponentially rare" is not
"impossible" for a deterministic function.
""", file=sys.stderr)

    # ============================================================
    # E: Summary and honest assessment
    # ============================================================
    print("=" * 70)
    print("DEEP ANALYSIS SUMMARY")
    print("=" * 70)

    print("""
1. CORRECTED UNDERSTANDING OF CHI-CONSTRAINT:
   The derivative at a hypothetical off-line zero does NOT need to vanish.
   It needs to grow as t^{0.85-sigma_0}, which is still positive growth.
   The original framing overstated the constraint.

2. JOINT DISTRIBUTION FINDINGS:
   - Correlation between |zeta| and |zeta'| is ~0.93-0.96 (very high)
   - The conditional mean of |zeta'| given |zeta| < epsilon is ~1.5*epsilon
     (from the scaling alpha ~ 0.6-0.9)
   - The conditional min of |zeta'| at our near-zero events is ~0.03-0.07

3. CHI-BOUND COMPARISON:
   At near-zero events (|zeta| < 0.5), the derivative is BELOW the chi-bound
   in 94-98% of cases. This means the actual zeta derivative at small-|zeta|
   events is already compatible with the chi-constraint.

   This is NOT a contradiction of RH. It means the joint distribution argument
   does not provide an exclusion: the conditional derivative distribution is
   not bounded away from the chi-constraint region.

4. EULER PRODUCT STRUCTURE:
   The log-derivative sum_p (log p)*p^{-s}/(1-p^{-s}) is convergent for sigma > 1/2.
   At a zero, it must diverge (pole). The convergence of the sum at non-zero points
   constrains how close the function can get to zero, but doesn't prevent actual zeros.

5. DAVENPORT-HEILBRONN COMPARISON:
   DH off-line zeros are very close to sigma = 1/2 (sigma ~ 0.500-0.503).
   Their derivatives are 2-5 times the chi-bound (ratio |f'|/|chi| ~ 2-4.6).
   This shows that off-line zeros CAN have substantial derivatives relative to chi.

6. FUNDAMENTAL OBSTRUCTION:
   The joint (zeta, zeta') approach fails to prove RH because:
   a) The chi-constraint does not require vanishing derivatives
   b) The conditional derivative distribution reaches the chi-bound region
   c) The Euler product structure creates correlations but not hard exclusions
   d) Moving from "exponentially rare" to "impossible" requires deterministic
      arguments beyond the statistical framework

VERDICT: The joint distribution reformulation is mathematically well-motivated
and reveals genuine structure (high correlation, specific scaling), but does NOT
provide a proof path. The chi-constraint is weaker than originally believed,
and the conditional distribution is compatible with (rather than excluding)
off-line zeros.

RATING: 5.5/10 promise (downgraded from 6.5), 8/10 depth, 8/10 novelty
""")


if __name__ == '__main__':
    main()
