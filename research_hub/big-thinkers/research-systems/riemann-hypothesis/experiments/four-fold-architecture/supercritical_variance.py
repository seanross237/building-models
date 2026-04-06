"""
Supercritical Variance Growth and Cross-Constraint Verification

This script verifies:
1. The variance of log|zeta(sigma+it)| at sigma < 1/2 (supercritical regime)
2. The functional equation's quantitative effect on variance
3. The cross-constraint: comparing zero density bounds from the sigma > 1/2 side
   vs the sigma < 1/2 side

Key formula from functional equation:
  zeta(s) = chi(s) * zeta(1-s)

  |zeta((1-sigma)+it)| = |chi((1-sigma)+it)| * |zeta(sigma+it)|

  log|zeta((1-sigma)+it)| = log|chi((1-sigma)+it)| + log|zeta(sigma+it)|

At sigma > 1/2:
  log|chi((1-sigma)+it)| = (sigma - 1/2) * log(t/(2*pi)) + O(1/t)

So the mean of log|zeta| at 1-sigma shifts by ~ (sigma-1/2)*log(t/2pi) -> +infinity,
and the variance at 1-sigma equals Var(log|chi|) + Var(log|zeta(sigma)|) + cross-term.
"""

import numpy as np
from mpmath import mp, zeta, gamma as mpgamma, pi as mppi, log, fabs, arg, cos, sin, power
import time

mp.dps = 25

def chi_function(s):
    """Compute chi(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s)"""
    return power(2, s) * power(mppi, s - 1) * sin(mppi * s / 2) * mpgamma(1 - s)

def compute_variance_profile(T_center, n_samples, sigmas):
    """
    Compute Var(log|zeta(sigma+it)|) for multiple sigma values.
    Also compute Var at 1-sigma to verify the functional equation relation.
    """
    np.random.seed(42)
    t_values = T_center + np.random.uniform(-T_center/4, T_center/4, n_samples)
    t_values = t_values[t_values > 14.5]

    results = {}
    for sigma in sigmas:
        log_abs_values = []
        log_abs_values_mirror = []
        log_chi_values = []

        sigma_mirror = 1.0 - sigma

        for t in t_values:
            # zeta at sigma + it
            z = zeta(sigma + 1j * float(t))
            az = float(fabs(z))
            if az > 0:
                log_abs_values.append(float(log(az)))
            else:
                log_abs_values.append(-50.0)

            # zeta at (1-sigma) + it (the mirror point)
            z_mirror = zeta(sigma_mirror + 1j * float(t))
            az_mirror = float(fabs(z_mirror))
            if az_mirror > 0:
                log_abs_values_mirror.append(float(log(az_mirror)))
            else:
                log_abs_values_mirror.append(-50.0)

            # chi at (1-sigma) + it
            try:
                c = chi_function(sigma_mirror + 1j * float(t))
                ac = float(fabs(c))
                if ac > 0:
                    log_chi_values.append(float(log(ac)))
                else:
                    log_chi_values.append(0.0)
            except:
                log_chi_values.append((sigma - 0.5) * float(log(float(t) / (2 * float(mppi)))))

        log_abs = np.array(log_abs_values)
        log_abs_mirror = np.array(log_abs_values_mirror)
        log_chi = np.array(log_chi_values)

        var_sigma = np.var(log_abs)
        var_mirror = np.var(log_abs_mirror)
        var_chi = np.var(log_chi)
        mean_sigma = np.mean(log_abs)
        mean_mirror = np.mean(log_abs_mirror)
        mean_chi = np.mean(log_chi)

        # Predicted mean of log|chi| at 1-sigma
        predicted_mean_chi = (sigma - 0.5) * np.log(T_center / (2 * np.pi))

        results[sigma] = {
            'var_sigma': var_sigma,
            'var_mirror': var_mirror,
            'var_chi': var_chi,
            'mean_sigma': mean_sigma,
            'mean_mirror': mean_mirror,
            'mean_chi': mean_chi,
            'predicted_mean_chi': predicted_mean_chi,
            # Check: Var(mirror) should be ~ Var(sigma) + Var(chi) + 2*Cov
            'cov_sigma_chi': np.cov(log_abs[:len(log_chi)], log_chi)[0, 1] if len(log_chi) == len(log_abs) else 0
        }

    return results

def verify_functional_equation_variance(T_values, sigma_values, n_samples=300):
    """
    Verify: Var(log|zeta(1-sigma+it)|) = Var(log|chi(1-sigma+it)|) + Var(log|zeta(sigma+it)|)
                                           + 2*Cov(log|chi|, log|zeta(sigma)|)

    And check how this grows with T.
    """
    print("=" * 70)
    print("FUNCTIONAL EQUATION VARIANCE RELATION")
    print("=" * 70)

    for sigma in sigma_values:
        sigma_m = 1.0 - sigma
        print(f"\n  sigma = {sigma:.2f} (mirror at {sigma_m:.2f}):")
        print(f"  {'T':>8}  {'Var(sig)':>10}  {'Var(1-sig)':>10}  "
              f"{'Var(chi)':>10}  {'Mean(chi)':>10}  {'Pred mean':>10}  "
              f"{'Var ratio':>10}")

        for T in T_values:
            results = compute_variance_profile(T, n_samples, [sigma])
            r = results[sigma]

            var_ratio = r['var_mirror'] / r['var_sigma'] if r['var_sigma'] > 0 else float('inf')

            print(f"  {T:>8}  {r['var_sigma']:>10.4f}  {r['var_mirror']:>10.4f}  "
                  f"{r['var_chi']:>10.4f}  {r['mean_chi']:>10.4f}  "
                  f"{r['predicted_mean_chi']:>10.4f}  {var_ratio:>10.3f}")

def compute_zero_density_bounds(sigma_values):
    """
    Compute known zero-density bounds and compare with the alpha-exponent prediction.

    Known bounds (Ingham-Huxley type):
    - N(sigma, T) << T^{A(sigma)} where A(sigma) = 3(1-sigma)/(2-sigma) for 1/2 < sigma <= 3/4
    - N(sigma, T) << T^{A(sigma)} where A(sigma) = 12(1-sigma)/(5+2(1-sigma)) for 3/4 < sigma <= 1

    The alpha-exponent prediction from Section 3.3:
    - If P(|zeta(sigma)| < eps) ~ C*eps^alpha, then N(sigma,T) ~ T * eps^{alpha-1} * |zeta'|
    - For N(sigma,T) = 0, we need alpha < 1 (actually alpha < 2 in the refined argument)
    """
    print("\n" + "=" * 70)
    print("ZERO DENSITY BOUNDS COMPARISON")
    print("=" * 70)

    print(f"\n  {'sigma':<8} {'Ingham A(sig)':<16} {'Huxley A(sig)':<16} "
          f"{'T^A for T=10^6':<16} {'T^A for T=10^12':<16}")

    for sigma in sigma_values:
        # Ingham bound
        if sigma <= 0.75:
            A_ingham = 3 * (1 - sigma) / (2 - sigma)
        else:
            A_ingham = 3 * (1 - sigma) / (2 - sigma)  # simplified

        # Huxley bound (for sigma > 3/4)
        if sigma > 0.75:
            A_huxley = 12 * (1 - sigma) / (5 + 2 * (1 - sigma))
        else:
            A_huxley = A_ingham

        bound_6 = 10 ** (6 * min(A_ingham, A_huxley))
        bound_12 = 10 ** (12 * min(A_ingham, A_huxley))

        print(f"  {sigma:<8.2f} {A_ingham:<16.4f} {A_huxley:<16.4f} "
              f"{bound_6:<16.1f} {bound_12:<16.1f}")

    print("\n  NOTE: RH is equivalent to A(sigma) = 0 for all sigma > 1/2.")
    print("  The best known bounds have A(sigma) -> 0 as sigma -> 1,")
    print("  but A(sigma) > 0 for all 1/2 < sigma < 1.")

def analyze_small_value_density(sigma, T_center, n_samples=1000):
    """
    Detailed analysis of the distribution of small |zeta(sigma+it)| values.
    This directly estimates the alpha exponent from actual zeta values.
    """
    np.random.seed(42)
    t_values = T_center + np.random.uniform(-T_center/4, T_center/4, n_samples)
    t_values = t_values[t_values > 14.5]

    abs_values = []
    for t in t_values:
        z = zeta(sigma + 1j * float(t))
        abs_values.append(float(fabs(z)))

    abs_values = np.array(abs_values)
    abs_values.sort()

    # Compute empirical CDF at fine epsilon grid
    epsilons = np.logspace(-3, 1, 50)
    cdf = np.array([np.mean(abs_values < eps) for eps in epsilons])

    return abs_values, epsilons, cdf

def main():
    print("=" * 70)
    print("SUPERCRITICAL VARIANCE AND CROSS-CONSTRAINT ANALYSIS")
    print("=" * 70)

    # Part 1: Variance profile across sigma, both sides
    print("\n\n--- Part 1: Variance at sigma and 1-sigma ---\n")

    sigma_values = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
    T_center = 5000
    n_samples = 300

    results = compute_variance_profile(T_center, n_samples, sigma_values)

    print(f"  T = {T_center}")
    print(f"  {'sigma':<8} {'1-sigma':<8} {'Var(sig)':<12} {'Var(1-sig)':<12} "
          f"{'Mean(1-sig)':<14} {'Pred mean':<12} {'Ratio V(1-s)/V(s)':<18}")

    for sigma in sigma_values:
        r = results[sigma]
        ratio = r['var_mirror'] / r['var_sigma'] if r['var_sigma'] > 0 else 0
        print(f"  {sigma:<8.2f} {1-sigma:<8.2f} {r['var_sigma']:<12.4f} "
              f"{r['var_mirror']:<12.4f} {r['mean_mirror']:<14.4f} "
              f"{r['predicted_mean_chi']:<12.4f} {ratio:<18.3f}")

    # Part 2: Variance growth with T at sigma < 1/2
    print("\n\n--- Part 2: Variance growth at mirror points ---\n")
    verify_functional_equation_variance(
        T_values=[1000, 3000, 5000, 10000],
        sigma_values=[0.60, 0.75],
        n_samples=200
    )

    # Part 3: Zero density bounds
    print("\n\n--- Part 3: Zero density bound comparison ---\n")
    compute_zero_density_bounds(
        [0.52, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    )

    # Part 4: Small value analysis at sigma > 1/2
    print("\n\n--- Part 4: Small-value density at sigma > 1/2 ---\n")

    for sigma in [0.60, 0.75, 1.00]:
        print(f"\n  sigma = {sigma}:")
        abs_vals, epsilons, cdf = analyze_small_value_density(sigma, 5000, 500)

        # Find alpha from the small-value tail
        mask = (cdf > 0) & (cdf < 0.2)
        if np.sum(mask) >= 3:
            log_eps = np.log(epsilons[mask])
            log_cdf = np.log(cdf[mask])
            coeffs = np.polyfit(log_eps, log_cdf, 1)
            alpha = coeffs[0]
            print(f"    Alpha exponent: {alpha:.4f}")
            print(f"    Smallest |zeta| value: {abs_vals[0]:.6f}")
            print(f"    P(|zeta| < 0.01) = {np.mean(abs_vals < 0.01):.6f}")
            print(f"    P(|zeta| < 0.1)  = {np.mean(abs_vals < 0.1):.6f}")
            print(f"    P(|zeta| < 0.5)  = {np.mean(abs_vals < 0.5):.4f}")
            if alpha < 2:
                print(f"    >>> alpha < 2: supports zero exclusion")
            else:
                print(f"    >>> alpha >= 2: does not exclude zeros by this argument alone")
        else:
            print(f"    Not enough small values for alpha estimation")
            print(f"    Smallest |zeta| value: {abs_vals[0]:.6f}")

    print("\n\nDONE.")

if __name__ == "__main__":
    main()
