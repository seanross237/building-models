"""
Part 1: Montgomery's Spectral Form Factor from Prime Sums

Montgomery (1973) showed that the pair correlation of zeta zeros connects
to primes. The spectral form factor K(tau) can be related to periodic orbit
sums (primes = periodic orbits of the Riemann dynamics).

The key relationship via the diagonal approximation:
  K(tau) = (2*pi / (log T)^2) * sum_p sum_m (log p)^2 / p^m * delta(tau - m*log(p)/(2*pi*rho_bar))

where rho_bar = log(T/(2*pi))/(2*pi) is the mean density at height T.

Since this is a sum of delta functions, the ramp K(tau) = |tau| emerges
after smoothing/binning. We compute this explicitly.

We also compute the raw sum S(x) = sum_p (ln p)^2/p * cos(x*ln p)
to demonstrate that it diverges without normalization.
"""

import numpy as np
from sympy import primerange
import time
import json

def compute_raw_prime_sum(x_vals, P_max):
    """Compute S(x) = sum_{p <= P_max} (ln p)^2 / p * cos(x * ln p)"""
    primes = np.array(list(primerange(2, P_max + 1)), dtype=float)
    ln_p = np.log(primes)

    S_x = np.zeros_like(x_vals)
    for i, x in enumerate(x_vals):
        S_x[i] = np.sum(ln_p**2 / primes * np.cos(x * ln_p))
    return S_x, len(primes)

def compute_normalized_form_factor_primes(tau_vals, T, P_max, M_max=5):
    """
    Compute the spectral form factor from prime sums with proper normalization.

    The Heisenberg time is tau_H = 1 (in unfolded units).
    The mean density at height T is rho_bar = log(T/(2*pi))/(2*pi).

    K_primes(tau) = smoothed version of:
      (2*pi) / N * sum_p sum_m (log p)^2/p^m * delta_smoothed(tau - m*log(p) * rho_bar)

    We implement this by binning: place weight (log p)^2/p^m at position
    tau_p = m*log(p) * rho_bar / N, then smooth.
    """
    rho_bar = np.log(T / (2 * np.pi)) / (2 * np.pi)
    # Number of zeros up to T
    N = T / (2 * np.pi) * np.log(T / (2 * np.pi)) - T / (2 * np.pi) + 7/8

    primes = np.array(list(primerange(2, P_max + 1)), dtype=float)
    ln_p = np.log(primes)

    # Collect (position, weight) pairs
    positions = []
    weights = []
    for m in range(1, M_max + 1):
        for j, p in enumerate(primes):
            tau_pos = m * ln_p[j] / (2 * np.pi * rho_bar)  # in units where Heisenberg time = 1
            weight = ln_p[j]**2 / p**m
            if tau_pos < 6:  # only keep relevant range
                positions.append(tau_pos)
                weights.append(weight)

    positions = np.array(positions)
    weights = np.array(weights)

    # Normalization: sum of all weights should give integral of K(tau)
    # For GUE, integral from 0 to 1 of tau dtau = 1/2
    # The diagonal approximation weight sum is sum_p sum_m (log p)^2/p^m
    total_weight = np.sum(weights)

    # Bin the contributions
    dtau = tau_vals[1] - tau_vals[0]
    K_binned = np.zeros_like(tau_vals)
    for pos, w in zip(positions, weights):
        idx = int(round(pos / dtau))
        if 0 <= idx < len(K_binned):
            K_binned[idx] += w

    # Normalize: K_binned / dtau gives density, then normalize so that
    # the integral matches the expected K(tau) = tau integral
    K_density = K_binned / dtau

    # The normalization factor: by the prime number theorem,
    # sum_p (log p)^2/p ≈ (1/2)(log P_max)^2
    # The Heisenberg time in "orbit length" units is 2*pi*rho_bar
    # K(tau) = tau means K_density * normalization = tau
    # We normalize by total_weight to get the "shape"
    # Then scale so that integral from 0 to 1 equals 1/2

    # Actually, the correct normalization from Berry (1985):
    # K(tau) = (1/(2*pi*rho_bar)) * sum of weights in bin at tau
    # Let's compute it this way
    K_berry = K_density / (2 * np.pi * rho_bar)

    # Smooth with Gaussian kernel
    sigma_bins = max(int(0.05 / dtau), 1)  # smooth over ~0.05 in tau
    kernel = np.exp(-np.arange(-3*sigma_bins, 3*sigma_bins+1)**2 / (2*sigma_bins**2))
    kernel /= np.sum(kernel)
    K_smoothed = np.convolve(K_berry, kernel, mode='same')

    return K_smoothed, K_berry, positions, weights, rho_bar, N

def main():
    t0 = time.time()

    x_vals = np.arange(0, 5.01, 0.01)

    # === Part A: Raw prime sum (demonstrating divergence) ===
    print("=" * 70)
    print("PART A: Raw prime sum S(x) = sum_p (ln p)^2/p * cos(x*ln p)")
    print("=" * 70)

    P_max_values = [100, 1000, 10000, 100000]
    raw_results = {}

    for P_max in P_max_values:
        S_x, n_primes = compute_raw_prime_sum(x_vals, P_max)
        raw_results[P_max] = 2 * S_x
        print(f"P_max = {P_max:>6d}: {n_primes} primes, S(0) = {S_x[0]:.4f}")

    print("\nRaw 2*S(x) at selected points (should approach |x| if converging):")
    print(f"{'x':>6} {'|x|':>6} {'P=100':>10} {'P=1K':>10} {'P=10K':>10} {'P=100K':>10}")
    print("-" * 58)
    for x_target in [0.0, 0.1, 0.3, 0.5, 0.7, 1.0, 2.0]:
        idx = int(round(x_target / 0.01))
        gue = min(abs(x_vals[idx]), 1.0)
        vals = [raw_results[P][idx] for P in P_max_values]
        print(f"{x_vals[idx]:6.2f} {gue:6.2f} {vals[0]:10.2f} {vals[1]:10.2f} {vals[2]:10.2f} {vals[3]:10.2f}")

    print("\n>>> RESULT: Raw sum DIVERGES. S(0) ~ (1/2)(ln P_max)^2.")
    print(">>> This is expected: Mertens' theorem gives sum_p (ln p)^2/p ~ (1/2)(ln x)^2")
    print(">>> The form factor emerges only after proper normalization + smoothing.")

    # === Part B: Properly normalized form factor ===
    print("\n" + "=" * 70)
    print("PART B: Properly normalized form factor from primes")
    print("=" * 70)

    # Use T = 1000 (height on critical line, ~650 zeros below this)
    T_values = [100, 500, 1000, 5000]
    tau_vals = np.arange(0, 3.01, 0.005)
    K_GUE = np.minimum(tau_vals, 1.0)

    for T in T_values:
        P_max = int(T**1.5)  # Include primes up to T^{3/2}
        P_max = min(P_max, 500000)
        K_smooth, K_raw, positions, weights, rho_bar, N_est = \
            compute_normalized_form_factor_primes(tau_vals, T, P_max, M_max=3)

        # Compute error in ramp region
        mask = (tau_vals > 0.1) & (tau_vals < 0.9)
        mae_ramp = np.mean(np.abs(K_smooth[mask] - K_GUE[mask]))

        print(f"\nT = {T}, P_max = {P_max}, rho_bar = {rho_bar:.4f}, N_est = {N_est:.0f}")
        print(f"  # orbit contributions: {len(positions)}")
        print(f"  MAE in ramp (0.1 < tau < 0.9): {mae_ramp:.6f}")
        print(f"  K_smooth at selected tau values:")
        for tau_target in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]:
            idx = int(round(tau_target / 0.005))
            if idx < len(tau_vals):
                print(f"    tau={tau_target:.1f}: K_primes={K_smooth[idx]:.4f}, K_GUE={K_GUE[idx]:.4f}")

    # Save results for best T
    T = 1000
    P_max = min(int(T**1.5), 500000)
    K_smooth_best, K_raw_best, pos_best, wt_best, rho_best, N_best = \
        compute_normalized_form_factor_primes(tau_vals, T, P_max, M_max=5)

    np.savez('part1_results.npz',
             tau_vals=tau_vals, K_GUE=K_GUE,
             K_smooth=K_smooth_best, K_raw=K_raw_best,
             positions=pos_best, weights=wt_best,
             x_vals=x_vals, raw_results_100k=raw_results.get(100000))

    print(f"\nTotal time: {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
