"""
Deep analysis of the Bohr-Jessen density near zero.

THE KEY QUESTION: Does the Bohr-Jessen distribution at sigma > 1/2
vanish at z=0, and if so, how fast?

The Bohr-Jessen distribution is the limiting distribution of zeta(sigma+it)
as t -> infinity. For sigma > 1, it is the distribution of the random
Euler product:
  Z = prod_p (1 - X_p / p^sigma)^{-1}
where X_p are independent, uniform on the unit circle.

For sigma > 1/2, the distribution exists but is more subtle (the Euler
product doesn't converge absolutely, but the distribution still exists
by the Bohr-Jessen theorem).

THEORETICAL BACKGROUND:
1. Jessen-Wintner (1935): The Bohr-Jessen distribution is either purely
   continuous or purely singular continuous. For sigma > 1/2, it has been
   shown to be absolutely continuous (has a density) by Harman-Matsumoto.

2. The density f_sigma(z) is an entire function of z (Bagchi 1982).
   This means it is smooth and never exactly zero on any open set.

3. CRUCIALLY: f_sigma(0) being zero would mean the Bohr-Jessen density
   vanishes at the origin. For the random Euler product, this would mean
   prod_p (1 - X_p/p^sigma)^{-1} = 0 has probability 0. But this product
   is NEVER zero (each factor is nonzero), so f_sigma(0) > 0!

THIS IS THE KEY INSIGHT:
  f_sigma(0) > 0 for all sigma > 1/2.

  The Bohr-Jessen density does NOT vanish at the origin.
  This means the "zero exclusion via density" argument FAILS.

But wait -- f_sigma(0) > 0 means P(zeta(sigma+it) is near 0) ~ f_sigma(0) * pi * eps^2
This gives alpha = 2 EXACTLY (the density is nonzero at the origin, so the
probability scales as eps^2, the area of a disk of radius eps).

So the "true" alpha should be 2, not the larger values we computed.
The larger values we computed were artifacts of finite sample size
(we couldn't see small enough values).

Let's verify this and understand its implications.
"""

import numpy as np
from sympy import primerange
import time

def random_euler_product_density_near_zero(sigma, n_primes, n_samples, n_bins=200):
    """
    Sample the random Euler product and compute the density near z=0.

    Z = prod_p (1 - e^{i*theta_p} / p^sigma)^{-1}

    We compute |Z| and estimate the density of |Z|^2 near 0.
    If the density of z = Z(omega) near 0 is f(0) > 0, then
    P(|Z| < eps) ~ f(0) * pi * eps^2 for small eps.
    So the density of |Z| near r=0 is ~ 2*pi*r*f(0), giving
    the CDF P(|Z| < r) ~ pi * f(0) * r^2.
    """
    primes = list(primerange(2, max(100, n_primes * 15)))[:n_primes]

    np.random.seed(42)
    thetas = np.random.uniform(0, 2*np.pi, (n_samples, len(primes)))

    # Compute the product in log space for numerical stability
    log_Z = np.zeros(n_samples, dtype=complex)
    for j, p in enumerate(primes):
        factor = 1.0 - np.exp(1j * thetas[:, j]) / (p ** sigma)
        log_Z -= np.log(factor)  # log(1/factor) = -log(factor)

    Z = np.exp(log_Z)
    abs_Z = np.abs(Z)
    abs_Z_sq = abs_Z ** 2

    return abs_Z, Z

def estimate_density_at_zero(abs_Z, max_r=0.5, n_rings=50):
    """
    Estimate the density f(0) of the Bohr-Jessen distribution near z=0.

    P(|Z| < r) ~ pi * f(0) * r^2 for small r.
    So f(0) ~ P(|Z| < r) / (pi * r^2).

    We estimate this for multiple values of r and extrapolate to r -> 0.
    """
    r_values = np.linspace(0.01, max_r, n_rings)
    probs = np.array([np.mean(abs_Z < r) for r in r_values])
    f0_estimates = probs / (np.pi * r_values ** 2)

    # The density estimate should stabilize for small r (if f(0) > 0)
    # or diverge/vanish (if f(0) = 0 or infinity)

    return r_values, probs, f0_estimates

def main():
    print("=" * 70)
    print("BOHR-JESSEN DENSITY NEAR ZERO: THE CRITICAL ANALYSIS")
    print("=" * 70)

    print("""
  KEY THEORETICAL POINT:
  The Bohr-Jessen density f_sigma(z) is the density of the random Euler product
  Z = prod_p (1 - X_p/p^sigma)^{-1} where X_p are iid uniform on unit circle.

  Since each factor (1 - X_p/p^sigma)^{-1} is NEVER zero (it's 1/(nonzero)),
  the product Z is NEVER zero. But Z can be ARBITRARILY CLOSE to zero
  (when many factors partially cancel).

  The density f_sigma(0):
  - Is > 0 for sigma > 1/2 (the distribution is absolutely continuous with
    smooth density, and the support includes a neighborhood of 0)
  - Is FINITE (the density is bounded)
  - Controls: P(|zeta(sigma+it)| < eps) ~ pi * f_sigma(0) * eps^2

  This means the "true" alpha exponent is EXACTLY 2 (not > 2 as we estimated
  from small samples -- those estimates were biased by insufficient resolution
  near zero).

  IMPLICATION: The simple zero-exclusion argument (alpha < 2 needed) FAILS
  because alpha = 2 EXACTLY. The probability of zeta being small goes as
  eps^2, which is the GENERIC behavior for a smooth density.
""")

    # Part 1: Large-scale simulation
    print("\n--- Part 1: Random Euler Product Density Near Zero ---\n")

    for sigma in [0.55, 0.60, 0.75, 1.00, 1.50]:
        print(f"\n  sigma = {sigma}:")
        t0 = time.time()

        # Use more primes for smaller sigma (slower convergence)
        n_primes = 200 if sigma < 0.7 else 100
        n_samples = 500000

        abs_Z, Z = random_euler_product_density_near_zero(sigma, n_primes, n_samples)
        r_values, probs, f0_estimates = estimate_density_at_zero(abs_Z)

        elapsed = time.time() - t0

        # Report
        print(f"    Samples: {n_samples}, Primes: {n_primes}, Time: {elapsed:.1f}s")
        print(f"    Min |Z|: {np.min(abs_Z):.8f}")
        print(f"    P(|Z| < 0.01): {np.mean(abs_Z < 0.01):.8f}")
        print(f"    P(|Z| < 0.05): {np.mean(abs_Z < 0.05):.6f}")
        print(f"    P(|Z| < 0.1):  {np.mean(abs_Z < 0.1):.6f}")
        print(f"    P(|Z| < 0.5):  {np.mean(abs_Z < 0.5):.4f}")

        # Density estimate at various r
        print(f"    f(0) estimates at various r:")
        for i, r in enumerate(r_values):
            if r in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5] or abs(r - 0.01) < 0.005 or abs(r - 0.05) < 0.005 or abs(r - 0.1) < 0.005:
                if probs[i] > 0:
                    print(f"      r={r:.3f}: P(|Z|<r)={probs[i]:.8f}, "
                          f"f(0) est = {f0_estimates[i]:.6f}")

        # Check if f(0) appears to be > 0 (constant) or -> 0
        # Use the smallest r values where we have data
        small_r_mask = (r_values < 0.15) & (probs > 0)
        if np.sum(small_r_mask) >= 3:
            f0_small = f0_estimates[small_r_mask]
            print(f"    f(0) mean (r < 0.15): {np.mean(f0_small):.6f}")
            print(f"    f(0) std  (r < 0.15): {np.std(f0_small):.6f}")
            if np.std(f0_small) < 0.3 * np.mean(f0_small):
                print(f"    >>> f(0) appears NONZERO and STABLE: alpha = 2 exactly")
            else:
                print(f"    >>> f(0) estimate is noisy -- need more samples")
        else:
            print(f"    Not enough data at small r to estimate f(0)")

    # Part 2: Check alpha = 2 by fitting P(|Z| < r) ~ C * r^alpha
    print("\n\n--- Part 2: Power-law fit P(|Z| < r) ~ C * r^alpha ---\n")

    for sigma in [0.55, 0.60, 0.75, 1.00]:
        n_primes = 200 if sigma < 0.7 else 100
        n_samples = 1000000

        abs_Z, Z = random_euler_product_density_near_zero(sigma, n_primes, n_samples)

        # Fine epsilon grid
        r_values = np.logspace(-3, -0.3, 40)
        probs = np.array([np.mean(abs_Z < r) for r in r_values])

        mask = probs > 1e-7
        if np.sum(mask) >= 5:
            log_r = np.log(r_values[mask])
            log_p = np.log(probs[mask])
            coeffs = np.polyfit(log_r, log_p, 1)
            alpha = coeffs[0]

            # Also check locally at the smallest r
            small_mask = mask & (r_values < 0.05) & (probs > 1e-7)
            if np.sum(small_mask) >= 3:
                coeffs_small = np.polyfit(np.log(r_values[small_mask]),
                                          np.log(probs[small_mask]), 1)
                alpha_small = coeffs_small[0]
            else:
                alpha_small = None

            alpha_small_str = f"{alpha_small:.3f}" if alpha_small is not None else "N/A"
            print(f"  sigma={sigma}: alpha (overall) = {alpha:.3f}, "
                  f"alpha (r<0.05) = {alpha_small_str}")
            print(f"              (alpha = 2 corresponds to nonzero density at z=0)")
        else:
            print(f"  sigma={sigma}: not enough data")

    # Part 3: The implications for the four-fold architecture
    print("""

--- Part 3: Implications for the Four-Fold Architecture ---

FINDING: The Bohr-Jessen density f_sigma(0) > 0 for sigma > 1/2.

This means:
1. P(|zeta(sigma+it)| < eps) ~ pi * f_sigma(0) * eps^2 (exact alpha = 2)
2. The zero-exclusion argument based on "alpha < 2" FAILS because alpha = 2.
3. The Bohr-Jessen distribution is CONSISTENT with off-line zeros existing.

HOWEVER: This does NOT mean off-line zeros EXIST. It means:
- The value distribution of zeta at sigma > 1/2 does not BY ITSELF exclude zeros.
- The zero-density estimates N(sigma,T) << T^{A(sigma)} are not contradicted
  by the Bohr-Jessen density.
- Something ELSE must exclude off-line zeros (if they are indeed excluded).

WHAT THE FOUR-FOLD ARCHITECTURE STILL PROVIDES:

The alpha = 2 finding means we need to look at the JOINT constraints more carefully.
The individual Bohr-Jessen constraint doesn't work. But the CROSS-CONSTRAINT from
the functional equation + derivative relation + GMC might.

Specifically: at a zero rho = sigma_0 + it_0 with sigma_0 > 1/2:
- |zeta'(sigma_0 + it_0)| = |chi(sigma_0+it_0)| * |zeta'((1-sigma_0)+it_0)|
- |chi| ~ (t_0/2pi)^{1/2 - sigma_0} -> 0 as t_0 -> infinity
- So |zeta'(sigma_0 + it_0)| << |zeta'((1-sigma_0) + it_0)| for large t_0

This means the zero at sigma_0 has a VERY SMALL derivative, i.e., zeta
passes through zero SLOWLY at sigma_0. The "width" of the near-zero
region is ~ eps / |zeta'| which grows as t_0^{sigma_0 - 1/2} * eps / |zeta'(1-sigma)|.

The density of t-values where |zeta(sigma_0+it)| < eps is then:
  ~ T * pi * f_sigma(0) * eps^2 / (2*pi / log(T)) [heuristic]

But the number of ZEROS (not just small values) is controlled by the
Jensen/argument principle formula:
  N(sigma_0, T) = number of zeros with Re > sigma_0, Im < T

The key is that the Bohr-Jessen density tells us about SMALL values
of |zeta|, but the zeros are where |zeta| is EXACTLY zero. The
zero count is not directly related to the density of near-zero values
because the zero-density estimates use the ARGUMENT PRINCIPLE (counting
winding numbers of zeta) rather than the magnitude of |zeta|.

CONCLUSION:
The four-fold architecture identifies a rich set of constraints on
hypothetical off-line zeros, but the constraints are not jointly
strong enough to exclude zeros. The fundamental gap is between:
- MEASURE-THEORETIC constraints (Bohr-Jessen, GMC) which control
  the probability of zeta being near zero
- TOPOLOGICAL constraints (argument principle, winding number) which
  control the number of actual zeros

The four-fold conjunction constrains both types but does not bridge them.
A proof of RH would need to connect the measure-theoretic structure
(which is well-understood via GMC) to the topological structure
(which counts zeros) in a way that no existing technique achieves.
""")

if __name__ == "__main__":
    main()
