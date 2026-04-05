"""
Alpha Exponent Estimation for the Bohr-Jessen Distribution

At sigma > 1/2, log|zeta(sigma+it)| has a limiting distribution (Bohr-Jessen).
The key quantity is the alpha-exponent: how does the probability
P(|zeta(sigma+it)| < epsilon) behave as epsilon -> 0?

If P(|zeta| < epsilon) ~ C * epsilon^alpha, then:
- alpha < 2: the zero density argument in findings.md Section 3.3 implies N(sigma,T) = 0
- alpha >= 2: zeros could potentially exist

We estimate alpha numerically by sampling |zeta(sigma+it)| at many random t-values
and computing the empirical CDF near zero.

We also compute the THEORETICAL alpha from the Bohr-Jessen random Euler product:
  log zeta(sigma+it) = -sum_p log(1 - p^{-sigma-it})
For sigma > 1, this is an absolutely convergent sum of independent random variables
(as t varies, p^{-it} is approximately uniform on the unit circle for different primes).
The distribution of zeta(sigma+it) is then the convolution of the distributions of
(1 - p^{-sigma} * e^{-it*log p})^{-1}, which are known explicitly.
"""

import numpy as np
from mpmath import mp, zeta, log, fabs, pi, zetazero
import time

mp.dps = 25  # 25 decimal digits

def sample_zeta_values(sigma, T_center, n_samples, spacing=1.0):
    """Sample |zeta(sigma + it)| at n_samples random t-values near T_center."""
    np.random.seed(42)
    # Use random t-values to avoid bias from zero locations
    t_values = T_center + np.random.uniform(-T_center/4, T_center/4, n_samples)
    t_values = t_values[t_values > 14.5]  # above first zero

    abs_values = []
    log_abs_values = []
    for t in t_values:
        z = zeta(sigma + 1j * float(t))
        az = float(fabs(z))
        abs_values.append(az)
        if az > 0:
            log_abs_values.append(float(log(az)))
        else:
            log_abs_values.append(-1e10)

    return np.array(abs_values), np.array(log_abs_values)

def estimate_alpha_exponent(abs_values, epsilons=None):
    """
    Estimate alpha from P(|zeta| < epsilon) ~ C * epsilon^alpha.

    Uses the empirical CDF at multiple epsilon values and fits a power law.
    """
    if epsilons is None:
        # Use a range of epsilon values
        epsilons = np.logspace(-2, 0, 20)

    n = len(abs_values)
    probs = np.array([np.sum(abs_values < eps) / n for eps in epsilons])

    # Only use points where probability is nonzero and less than 0.5
    mask = (probs > 0) & (probs < 0.5)
    if np.sum(mask) < 3:
        return None, None, epsilons, probs

    log_eps = np.log(epsilons[mask])
    log_probs = np.log(probs[mask])

    # Linear regression: log(P) = alpha * log(eps) + log(C)
    coeffs = np.polyfit(log_eps, log_probs, 1)
    alpha = coeffs[0]
    log_C = coeffs[1]

    return alpha, np.exp(log_C), epsilons, probs

def bohr_jessen_random_euler_product(sigma, n_primes=100, n_samples=10000):
    """
    Simulate the Bohr-Jessen distribution via random Euler product.

    zeta(sigma+it) = prod_p (1 - p^{-sigma} * e^{i*theta_p})^{-1}
    where theta_p are independent uniform on [0, 2*pi) for different primes.

    For sigma > 1/2, we can truncate the product at a finite number of primes.
    """
    from sympy import primerange
    primes = list(primerange(2, n_primes * 20))[:n_primes]

    np.random.seed(123)
    # Sample random phases
    thetas = np.random.uniform(0, 2*np.pi, (n_samples, len(primes)))

    # Compute log of Euler product
    log_zeta_samples = np.zeros(n_samples, dtype=complex)
    for j, p in enumerate(primes):
        # log(1 - p^{-sigma} * e^{i*theta})^{-1} = -log(1 - p^{-sigma} * e^{i*theta})
        p_power = p ** (-sigma)
        z = 1.0 - p_power * np.exp(1j * thetas[:, j])
        log_zeta_samples -= np.log(z)

    zeta_samples = np.exp(log_zeta_samples)
    abs_samples = np.abs(zeta_samples)

    return abs_samples

def main():
    print("=" * 70)
    print("ALPHA EXPONENT ESTIMATION FOR BOHR-JESSEN DISTRIBUTION")
    print("=" * 70)

    # Part 1: Direct sampling of zeta
    print("\n--- Part 1: Direct sampling of |zeta(sigma+it)| ---\n")

    sigmas = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00]
    T_centers = [1000, 5000, 10000]
    n_samples = 500

    results = {}

    for sigma in sigmas:
        print(f"\n  sigma = {sigma}:")
        for T in T_centers:
            t0 = time.time()
            abs_vals, log_abs_vals = sample_zeta_values(sigma, T, n_samples)
            elapsed = time.time() - t0

            alpha, C, epsilons, probs = estimate_alpha_exponent(abs_vals)

            min_val = np.min(abs_vals)
            frac_small = np.mean(abs_vals < 0.1)

            print(f"    T={T:6d}: min|zeta|={min_val:.4f}, "
                  f"P(|z|<0.1)={frac_small:.4f}, "
                  f"alpha={alpha:.3f}" if alpha else
                  f"    T={T:6d}: min|zeta|={min_val:.4f}, "
                  f"P(|z|<0.1)={frac_small:.4f}, "
                  f"alpha=N/A (no small values)")

            results[(sigma, T)] = {
                'alpha': alpha,
                'min_val': min_val,
                'frac_small': frac_small,
                'mean': np.mean(abs_vals),
                'var_log': np.var(log_abs_vals)
            }

    # Part 2: Random Euler product simulation
    print("\n\n--- Part 2: Random Euler Product (Bohr-Jessen) Simulation ---\n")

    n_primes_list = [20, 50, 100]
    n_sim = 50000

    for sigma in [0.55, 0.60, 0.75, 1.00]:
        print(f"\n  sigma = {sigma}:")
        for n_primes in n_primes_list:
            t0 = time.time()
            abs_samples = bohr_jessen_random_euler_product(sigma, n_primes, n_sim)
            elapsed = time.time() - t0

            alpha, C, epsilons, probs = estimate_alpha_exponent(abs_samples)

            min_val = np.min(abs_samples)
            frac_small = np.mean(abs_samples < 0.1)

            alpha_str = f"{alpha:.3f}" if alpha is not None else "N/A"
            print(f"    {n_primes:3d} primes: min={min_val:.6f}, "
                  f"P(|z|<0.1)={frac_small:.5f}, "
                  f"alpha={alpha_str}, time={elapsed:.1f}s")

    # Part 3: Fine-grained alpha at sigma = 0.75 with large sample
    print("\n\n--- Part 3: Fine-grained alpha at sigma=0.75 (large sample) ---\n")

    n_big = 200000
    for sigma in [0.60, 0.75]:
        print(f"  sigma = {sigma}:")
        abs_samples = bohr_jessen_random_euler_product(sigma, 100, n_big)

        # Use finer epsilon grid
        epsilons = np.logspace(-3, -0.3, 30)
        probs = np.array([np.mean(abs_samples < eps) for eps in epsilons])

        mask = (probs > 1e-6) & (probs < 0.3)
        if np.sum(mask) >= 3:
            log_eps = np.log(epsilons[mask])
            log_probs = np.log(probs[mask])
            coeffs = np.polyfit(log_eps, log_probs, 1)
            alpha = coeffs[0]
            print(f"    Alpha = {alpha:.4f}")
            print(f"    Epsilon range: [{epsilons[mask][0]:.4f}, {epsilons[mask][-1]:.4f}]")
            print(f"    Prob range: [{probs[mask][0]:.6f}, {probs[mask][-1]:.4f}]")

            # Check for alpha < 2 (the critical threshold)
            if alpha < 2:
                print(f"    >>> alpha < 2: CONSISTENT with zero exclusion!")
            else:
                print(f"    >>> alpha >= 2: zeros could potentially exist")
        else:
            print(f"    Not enough data points for alpha estimation")

    # Part 4: Alpha as a function of sigma (the key plot)
    print("\n\n--- Part 4: Alpha(sigma) function ---\n")
    print(f"  {'sigma':<8} {'alpha (100 primes)':<22} {'alpha (50 primes)':<22}")
    print(f"  {'-----':<8} {'------------------':<22} {'------------------':<22}")

    for sigma in [0.52, 0.55, 0.58, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]:
        alphas = []
        for n_primes in [50, 100]:
            abs_samples = bohr_jessen_random_euler_product(sigma, n_primes, 100000)
            alpha, C, _, _ = estimate_alpha_exponent(abs_samples, np.logspace(-2.5, -0.3, 25))
            alphas.append(alpha)

        a50 = f"{alphas[0]:.3f}" if alphas[0] is not None else "N/A"
        a100 = f"{alphas[1]:.3f}" if alphas[1] is not None else "N/A"

        threshold = ""
        if alphas[1] is not None:
            if alphas[1] < 2:
                threshold = " [< 2: excludes zeros]"
            else:
                threshold = " [>= 2: allows zeros]"

        print(f"  {sigma:<8.2f} {a100:<22} {a50:<22}{threshold}")

    print("\n\nDONE.")

if __name__ == "__main__":
    main()
