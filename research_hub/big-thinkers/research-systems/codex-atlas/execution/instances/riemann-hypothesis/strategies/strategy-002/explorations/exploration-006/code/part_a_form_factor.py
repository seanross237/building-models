"""
Part A: Spectral Form Factor — Primes vs Zeros vs GUE

Computes:
1. K_zeros(tau) from actual zeta zeros (N=2000)
2. K_primes(tau) via Berry's prime power sum formula
3. K_GUE(tau) = min(tau, 1)

Then compares all three and answers: do primes determine spectral correlations?
"""

import numpy as np
import sys

ZEROS_PATH = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-003/code/zeta_zeros_2000.npy"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Load zeros
# ─────────────────────────────────────────────────────────────────────────────
print("Loading zeta zeros...")
zeros = np.load(ZEROS_PATH)
N = len(zeros)
print(f"  N = {N} zeros, range: [{zeros[0]:.4f}, {zeros[-1]:.4f}]")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Unfold zeros
# ─────────────────────────────────────────────────────────────────────────────
print("\nUnfolding zeros...")
# Standard unfolding: x_n = (t_n / 2pi) * log(t_n / (2*pi*e))
x_unfolded = (zeros / (2 * np.pi)) * np.log(zeros / (2 * np.pi * np.e))

# Normalize so mean spacing = 1
spacings = np.diff(x_unfolded)
mean_spacing = np.mean(spacings)
print(f"  Mean spacing before normalization: {mean_spacing:.6f}")
x_norm = x_unfolded / mean_spacing
print(f"  Mean spacing after normalization: {np.mean(np.diff(x_norm)):.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Compute K_zeros(tau)
# ─────────────────────────────────────────────────────────────────────────────
print("\nComputing K_zeros(tau)...")
tau_vals = np.linspace(0.01, 2.0, 200)

# K_zeros(tau) = (1/N) * |sum_n exp(2*pi*i*tau*x_n)|^2
# = (1/N) * |S(tau)|^2  where S(tau) = sum_n exp(2*pi*i*tau*x_n)
K_zeros = np.zeros(len(tau_vals))
for i, tau in enumerate(tau_vals):
    S = np.sum(np.exp(2j * np.pi * tau * x_norm))
    K_zeros[i] = np.abs(S)**2 / N

print(f"  K_zeros at tau=0.5: {K_zeros[np.argmin(np.abs(tau_vals - 0.5))]:.4f} (expect ~0.5)")
print(f"  K_zeros at tau=1.0: {K_zeros[np.argmin(np.abs(tau_vals - 1.0))]:.4f} (expect ~1.0)")
print(f"  K_zeros at tau=1.5: {K_zeros[np.argmin(np.abs(tau_vals - 1.5))]:.4f} (expect ~1.0)")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Compute K_primes(tau) via Berry's formula
# ─────────────────────────────────────────────────────────────────────────────
print("\nComputing K_primes(tau) via Berry formula...")

# T = geometric mean height of the zeros
T = np.exp(np.mean(np.log(zeros)))
print(f"  T (geometric mean of zeros) = {T:.2f}")
log_T_over_2pi = np.log(T / (2 * np.pi))
print(f"  log(T/2pi) = {log_T_over_2pi:.4f}")

# Generate prime powers up to T
def sieve_primes(limit):
    """Sieve of Eratosthenes."""
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.where(is_prime)[0]

T_int = int(T)
print(f"  Generating primes up to {T_int}...")
primes = sieve_primes(T_int)
print(f"  Found {len(primes)} primes up to {T_int}")

# Collect all prime powers p^m <= T
prime_powers = []
for p in primes:
    pm = p
    m = 1
    log_p = np.log(p)
    while pm <= T_int:
        log_pm = m * log_p
        weight = log_p**2 / pm
        prime_powers.append((pm, log_pm, weight))
        m += 1
        pm *= p

print(f"  Total prime powers: {len(prime_powers)}")

# Compute normalization Σ = sum of weights
norm = sum(w for _, _, w in prime_powers)
print(f"  Normalization Σ = {norm:.4f}")
print(f"  Expected Σ ~ log(T) = {np.log(T):.4f} (should be comparable)")

# Print norm breakdown
primes_100 = sum(w for pm, _, w in prime_powers if pm <= 100)
primes_1000 = sum(w for pm, _, w in prime_powers if pm <= 1000)
primes_10000 = sum(w for pm, _, w in prime_powers if pm <= 10000)
print(f"  Norm from p^m <= 100:   {primes_100:.4f} ({100*primes_100/norm:.1f}%)")
print(f"  Norm from p^m <= 1000:  {primes_1000:.4f} ({100*primes_1000/norm:.1f}%)")
print(f"  Norm from p^m <= 10000: {primes_10000:.4f} ({100*primes_10000/norm:.1f}%)")

# Compute K_primes(tau)
print(f"\n  Computing K_primes for {len(tau_vals)} tau values...")
log_pms = np.array([lpm for _, lpm, _ in prime_powers])
weights = np.array([w for _, _, w in prime_powers])

K_primes = np.zeros(len(tau_vals))
for i, tau in enumerate(tau_vals):
    cosines = np.cos(2 * np.pi * tau * log_pms / log_T_over_2pi)
    K_primes[i] = np.dot(weights, cosines) / norm

print(f"  K_primes at tau=0.5: {K_primes[np.argmin(np.abs(tau_vals - 0.5))]:.4f} (expect ~0.5)")
print(f"  K_primes at tau=1.0: {K_primes[np.argmin(np.abs(tau_vals - 1.0))]:.4f} (expect ~1.0)")
print(f"  K_primes at tau=1.5: {K_primes[np.argmin(np.abs(tau_vals - 1.5))]:.4f} (expect ~1.0)")

# Also compute with truncated sums to diagnose previous failure
print("\n  Testing convergence with different P_max cutoffs...")
for P_max in [100, 1000, 10000, T_int]:
    subset = [(pm, lpm, w) for pm, lpm, w in prime_powers if pm <= P_max]
    if not subset:
        continue
    n_sub = sum(w for _, _, w in subset)
    lpm_sub = np.array([lpm for _, lpm, _ in subset])
    w_sub = np.array([w for _, _, w in subset])
    tau_test = 0.5
    cos_sub = np.cos(2 * np.pi * tau_test * lpm_sub / log_T_over_2pi)
    # Two normalizations: (a) normalize by full norm, (b) normalize by subset norm
    k_full_norm = np.dot(w_sub, cos_sub) / norm
    k_sub_norm = np.dot(w_sub, cos_sub) / n_sub if n_sub > 0 else 0
    print(f"    P_max={P_max:6d}: partial_norm={n_sub:.4f} ({100*n_sub/norm:.1f}%), "
          f"K(0.5)_fullnorm={k_full_norm:.4f}, K(0.5)_subnorm={k_sub_norm:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. GUE form factor
# ─────────────────────────────────────────────────────────────────────────────
K_GUE = np.minimum(tau_vals, 1.0)

# ─────────────────────────────────────────────────────────────────────────────
# 6. Quantitative comparison
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("QUANTITATIVE COMPARISON")
print("="*60)

# Focus on ramp region tau < 1
ramp_mask = tau_vals < 1.0

mad_zeros_gue = np.mean(np.abs(K_zeros[ramp_mask] - K_GUE[ramp_mask]))
mad_primes_gue = np.mean(np.abs(K_primes[ramp_mask] - K_GUE[ramp_mask]))
mad_zeros_primes = np.mean(np.abs(K_zeros[ramp_mask] - K_primes[ramp_mask]))

print(f"\nIn ramp region (tau < 1):")
print(f"  MAD(K_zeros, K_GUE)   = {mad_zeros_gue:.4f}")
print(f"  MAD(K_primes, K_GUE)  = {mad_primes_gue:.4f}")
print(f"  MAD(K_zeros, K_primes)= {mad_zeros_primes:.4f}")

# Plateau region tau > 1
plateau_mask = tau_vals > 1.0
K_zeros_plateau = np.mean(K_zeros[plateau_mask])
K_primes_plateau = np.mean(K_primes[plateau_mask])
print(f"\nIn plateau region (tau > 1):")
print(f"  Mean K_zeros   = {K_zeros_plateau:.4f} (expect ~1.0)")
print(f"  Mean K_primes  = {K_primes_plateau:.4f} (expect ~1.0)")

# Does K_primes show ramp-to-plateau transition?
K_primes_ramp_mean = np.mean(K_primes[ramp_mask])
K_primes_plateau_mean = np.mean(K_primes[plateau_mask])
print(f"\nRamp-to-plateau transition:")
print(f"  K_primes mean in ramp  = {K_primes_ramp_mean:.4f}")
print(f"  K_primes mean in plateau = {K_primes_plateau_mean:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. Save results
# ─────────────────────────────────────────────────────────────────────────────
OUT_PATH = "/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-006/code/part_a_results.npz"
np.savez(OUT_PATH,
         tau_vals=tau_vals,
         K_zeros=K_zeros,
         K_primes=K_primes,
         K_GUE=K_GUE,
         T=np.array([T]),
         norm=np.array([norm]),
         mad_zeros_gue=np.array([mad_zeros_gue]),
         mad_primes_gue=np.array([mad_primes_gue]),
         mad_zeros_primes=np.array([mad_zeros_primes]))
print(f"\nResults saved to {OUT_PATH}")

# ─────────────────────────────────────────────────────────────────────────────
# 8. Print table for report
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("TAU TABLE (for report)")
print("="*60)
print(f"{'tau':>6} | {'K_zeros':>8} | {'K_primes':>8} | {'K_GUE':>6}")
print("-"*40)
for i in range(0, len(tau_vals), 20):
    print(f"{tau_vals[i]:6.2f} | {K_zeros[i]:8.4f} | {K_primes[i]:8.4f} | {K_GUE[i]:6.4f}")

print("\nDone.")
