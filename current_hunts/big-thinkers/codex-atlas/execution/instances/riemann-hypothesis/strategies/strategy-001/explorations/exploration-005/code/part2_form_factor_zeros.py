"""
Part 2: Spectral Form Factor directly from Zeta Zeros

Compute K(tau) = (1/N)|sum_n exp(2*pi*i*tau*eps_n)|^2
where eps_n are the unfolded zero positions (mean spacing = 1).

This gives ground truth for the form factor, independent of any
prime sum formula. Compare to GUE prediction K(tau) = min(|tau|, 1).
"""

import numpy as np
from mpmath import zetazero, mp
import time

def N_smooth(T):
    """Smooth counting function for Riemann zeros: N(T) ~ T/(2pi) log(T/(2pi)) - T/(2pi) + 7/8"""
    if T <= 0:
        return 0
    return T/(2*np.pi) * np.log(T/(2*np.pi)) - T/(2*np.pi) + 7.0/8.0

def main():
    t0 = time.time()
    mp.dps = 25

    N_zeros = 2000

    # Check if zeros already computed
    try:
        gammas = np.load('zeta_zeros.npy')
        if len(gammas) >= N_zeros:
            print(f"Loaded {len(gammas)} zeros from cache.")
            gammas = gammas[:N_zeros]
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"Computing {N_zeros} zeta zeros with mpmath...")
        gammas = np.zeros(N_zeros)
        for n in range(1, N_zeros + 1):
            z = zetazero(n)
            gammas[n-1] = float(z.imag)
            if n % 200 == 0:
                print(f"  {n}/{N_zeros} zeros computed ({time.time()-t0:.1f}s)")
        np.save('zeta_zeros.npy', gammas)
        print(f"All zeros computed in {time.time()-t0:.1f}s")

    print(f"Zero range: gamma_1 = {gammas[0]:.4f}, gamma_{N_zeros} = {gammas[-1]:.4f}")

    # Unfold zeros
    eps = np.array([N_smooth(g) for g in gammas])
    spacings = np.diff(eps)
    print(f"Unfolded: mean spacing = {np.mean(spacings):.6f}, std = {np.std(spacings):.6f}")

    # === Spectral Form Factor ===
    tau_vals = np.arange(0, 3.01, 0.002)
    K_zeros = np.zeros_like(tau_vals)

    print(f"\nComputing form factor K(tau) for {len(tau_vals)} tau values...")
    for i, tau in enumerate(tau_vals):
        phases = 2 * np.pi * tau * eps
        re = np.sum(np.cos(phases))
        im = np.sum(np.sin(phases))
        K_zeros[i] = (re**2 + im**2) / N_zeros

    print(f"Form factor computed in {time.time()-t0:.1f}s")

    # At tau=0, K(0) = N (all phases = 0, sum = N, |sum|^2/N = N)
    # This is the trivial delta-function peak. The "connected" form factor
    # subtracts this, or we just ignore tau=0.
    K_zeros[0] = 0  # Remove trivial peak

    # GUE prediction
    K_GUE = np.minimum(tau_vals, 1.0)

    print("\n=== Form Factor: K_zeros(tau) vs K_GUE(tau) ===")
    print(f"{'tau':>6} {'K_GUE':>8} {'K_zeros':>10} {'ratio':>8}")
    print("-" * 40)
    for tau_target in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5]:
        idx = int(round(tau_target / 0.002))
        if idx < len(tau_vals):
            tau = tau_vals[idx]
            gue = K_GUE[idx]
            kz = K_zeros[idx]
            ratio = kz / gue if gue > 0 else float('inf')
            print(f"{tau:6.3f} {gue:8.4f} {kz:10.4f} {ratio:8.4f}")

    # Smooth K_zeros for cleaner comparison
    sigma_bins = max(int(0.02 / 0.002), 1)
    kernel = np.exp(-np.arange(-3*sigma_bins, 3*sigma_bins+1)**2 / (2*sigma_bins**2))
    kernel /= np.sum(kernel)
    K_zeros_smooth = np.convolve(K_zeros, kernel, mode='same')

    print("\n=== Smoothed Form Factor ===")
    print(f"{'tau':>6} {'K_GUE':>8} {'K_smooth':>10} {'ratio':>8}")
    print("-" * 40)
    for tau_target in [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0, 1.5, 2.0]:
        idx = int(round(tau_target / 0.002))
        if idx < len(tau_vals):
            tau = tau_vals[idx]
            gue = K_GUE[idx]
            ks = K_zeros_smooth[idx]
            ratio = ks / gue if gue > 0 else float('inf')
            print(f"{tau:6.3f} {gue:8.4f} {ks:10.4f} {ratio:8.4f}")

    # Error metrics
    mask_ramp = (tau_vals > 0.05) & (tau_vals < 0.95)
    mask_plat = (tau_vals > 1.05) & (tau_vals < 2.5)
    mae_ramp = np.mean(np.abs(K_zeros_smooth[mask_ramp] - K_GUE[mask_ramp]))
    mae_plat = np.mean(np.abs(K_zeros_smooth[mask_plat] - K_GUE[mask_plat]))
    print(f"\nMAE (smoothed) in ramp region: {mae_ramp:.6f}")
    print(f"MAE (smoothed) in plateau region: {mae_plat:.6f}")

    # === Pair Correlation R2(s) ===
    print("\n" + "=" * 60)
    print("PAIR CORRELATION R2(s) from unfolded zeros")
    print("=" * 60)

    # Compute nearest-neighbor and all-pairs spacings
    # For pair correlation, compute all (eps_i - eps_j) for i != j
    # Histogram them (normalized)
    max_s = 4.0
    ds = 0.05
    s_bins = np.arange(0, max_s + ds, ds)
    s_centers = (s_bins[:-1] + s_bins[1:]) / 2

    # For efficiency, only use nearby pairs (within max_s unfolded units)
    pair_diffs = []
    for i in range(len(eps)):
        for j in range(i+1, min(i+20, len(eps))):  # pairs within ~20 spacings
            diff = eps[j] - eps[i]
            if diff < max_s:
                pair_diffs.append(diff)
            else:
                break

    pair_diffs = np.array(pair_diffs)
    hist, _ = np.histogram(pair_diffs, bins=s_bins)

    # Normalize: R2(s) * ds * N = number of pairs in bin
    # For Poisson: R2 = 1, so we expect N pairs per bin (for large s)
    # Normalization: divide by (N * ds) where N ~ total zeros
    R2_zeros = hist / (N_zeros * ds)

    # GUE prediction
    R2_GUE = 1 - (np.sinc(s_centers))**2  # sinc(x) = sin(pi*x)/(pi*x) in numpy

    print(f"\nPair correlation: {len(pair_diffs)} pairs collected")
    print(f"\n{'s':>6} {'R2_GUE':>8} {'R2_zeros':>10} {'diff':>8}")
    print("-" * 40)
    for s_target in [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
        idx = int(round(s_target / ds))
        if idx < len(s_centers):
            s = s_centers[idx]
            gue = R2_GUE[idx]
            r2z = R2_zeros[idx]
            print(f"{s:6.3f} {gue:8.4f} {r2z:10.4f} {r2z - gue:8.4f}")

    # Save results
    np.savez('part2_results.npz',
             tau_vals=tau_vals, K_zeros=K_zeros, K_zeros_smooth=K_zeros_smooth,
             K_GUE=K_GUE, gammas=gammas, eps=eps,
             s_centers=s_centers, R2_zeros=R2_zeros, R2_GUE=R2_GUE)

    print(f"\nTotal time: {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
