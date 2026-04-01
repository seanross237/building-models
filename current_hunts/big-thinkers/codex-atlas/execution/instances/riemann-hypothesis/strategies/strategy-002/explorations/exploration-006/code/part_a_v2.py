"""
Part A v2: Spectral Form Factor — Primes vs Zeros vs GUE

Fixes from v1:
1. Use fine tau grid (step=0.002) + Gaussian smoothing for K_zeros
2. Use Berry's binning approach for K_primes (not cosine formula)
3. Show why the cosine formula fails (oscillatory, not the form factor)

Based on approach from strategy-001 exploration-005, which successfully
computed K_zeros and K_primes.
"""

import numpy as np
from sympy import primerange
import time

t0 = time.time()

ZEROS_PATH = "/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-003/code/zeta_zeros_2000.npy"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Load zeros, unfold with standard formula
# ─────────────────────────────────────────────────────────────────────────────
print("Loading zeta zeros...")
zeros = np.load(ZEROS_PATH)
N = len(zeros)
print(f"  N = {N} zeros, range: [{zeros[0]:.4f}, {zeros[-1]:.4f}]")

# Standard smooth counting function (matches exploration-005 exactly)
def N_smooth(T):
    """Smooth part of zero counting function."""
    if T <= 0:
        return 0.0
    return T / (2*np.pi) * np.log(T / (2*np.pi)) - T / (2*np.pi) + 7.0/8.0

print("  Unfolding zeros via N_smooth...")
eps = np.array([N_smooth(g) for g in zeros])
spacings = np.diff(eps)
mean_sp = np.mean(spacings)
print(f"  Unfolded eps range: [{eps[0]:.3f}, {eps[-1]:.3f}]")
print(f"  Mean spacing: {mean_sp:.6f} (should be ~1.0)")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Compute K_zeros with fine tau grid
# ─────────────────────────────────────────────────────────────────────────────
print("\nComputing K_zeros(tau) on fine grid...")
dtau = 0.002
tau_vals = np.arange(0, 3.01, dtau)
K_zeros = np.zeros(len(tau_vals))

for i, tau in enumerate(tau_vals):
    phases = 2 * np.pi * tau * eps
    re = np.sum(np.cos(phases))
    im = np.sum(np.sin(phases))
    K_zeros[i] = (re**2 + im**2) / N

K_zeros[0] = 0.0  # Remove tau=0 DC peak (K(0) = N, unphysical)

print(f"  K_zeros computed in {time.time()-t0:.1f}s")
print(f"  Raw K_zeros at tau=0.5: {K_zeros[int(0.5/dtau)]:.4f}")
print(f"  Raw K_zeros at tau=1.0: {K_zeros[int(1.0/dtau)]:.4f}")

# Smooth K_zeros with Gaussian kernel
sigma_bins = max(int(0.02 / dtau), 1)  # sigma = 0.02 in tau units
kernel_range = np.arange(-4*sigma_bins, 4*sigma_bins+1)
kernel = np.exp(-kernel_range**2 / (2*sigma_bins**2))
kernel /= np.sum(kernel)
K_zeros_smooth = np.convolve(K_zeros, kernel, mode='same')
# Fix boundary effects
K_zeros_smooth[:4*sigma_bins] = np.nan
K_zeros_smooth[-4*sigma_bins:] = np.nan

print("\n  Smoothed K_zeros vs K_GUE:")
print(f"  {'tau':>6} | {'K_GUE':>8} | {'K_zeros_raw':>12} | {'K_zeros_smooth':>14}")
print("  " + "-"*50)
for tau_t in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0]:
    idx = int(round(tau_t / dtau))
    if idx < len(tau_vals) and not np.isnan(K_zeros_smooth[idx]):
        gue = min(tau_t, 1.0)
        kz_raw = K_zeros[idx]
        kz_sm = K_zeros_smooth[idx]
        print(f"  {tau_t:6.2f} | {gue:8.4f} | {kz_raw:12.4f} | {kz_sm:14.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Compute K_primes via Berry's BINNING approach
# ─────────────────────────────────────────────────────────────────────────────
print("\nComputing K_primes(tau) via Berry binning approach...")

# Characteristic height T = geometric mean of zeros
T = np.exp(np.mean(np.log(zeros)))
rho_bar = np.log(T / (2*np.pi)) / (2*np.pi)
print(f"  T = {T:.2f}, rho_bar = {rho_bar:.4f}, 2*pi*rho_bar = {2*np.pi*rho_bar:.4f}")
print(f"  Heisenberg time scale: log(T/2pi) = {np.log(T/(2*np.pi)):.4f}")

# Collect prime powers and their tau positions
T_int = int(T * 3)  # Go to 3T to get tau < 3
print(f"  Generating primes up to {T_int}...")
primes = list(primerange(2, T_int + 1))
print(f"  Found {len(primes)} primes up to {T_int}")

# For each prime power, compute: tau_pos, weight
positions_list = []
weights_list = []

for p in primes:
    m = 1
    pm = p
    log_p = np.log(p)
    while pm <= T_int:
        tau_pos = m * log_p / (2 * np.pi * rho_bar)  # = m*log(p)/log(T/2pi)
        weight = log_p**2 / pm
        if tau_pos < 3.1:  # Only keep in relevant range
            positions_list.append(tau_pos)
            weights_list.append(weight)
        m += 1
        pm *= p

positions = np.array(positions_list)
weights = np.array(weights_list)
print(f"  Total prime powers with tau < 3: {len(positions)}")
print(f"  Total weight: {np.sum(weights):.4f}")
print(f"  Weight in [0,1]: {np.sum(weights[positions < 1]):.4f}")
print(f"  Weight in [1,2]: {np.sum(weights[(positions >= 1) & (positions < 2)]):.4f}")

# Bin into K_primes
K_binned = np.zeros(len(tau_vals))
for pos, w in zip(positions, weights):
    idx = int(round(pos / dtau))
    if 0 <= idx < len(K_binned):
        K_binned[idx] += w

# Convert to density
K_density = K_binned / dtau

# Berry normalization: K_berry = K_density / (2*pi*rho_bar)
K_berry = K_density / (2 * np.pi * rho_bar)

# Smooth K_berry with Gaussian (same sigma as K_zeros)
K_primes_smooth = np.convolve(K_berry, kernel, mode='same')
K_primes_smooth[:4*sigma_bins] = np.nan
K_primes_smooth[-4*sigma_bins:] = np.nan

print("\n  Smoothed K_primes (binning) vs K_GUE:")
print(f"  {'tau':>6} | {'K_GUE':>8} | {'K_primes_sm':>12}")
print("  " + "-"*35)
for tau_t in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0]:
    idx = int(round(tau_t / dtau))
    if idx < len(tau_vals) and not np.isnan(K_primes_smooth[idx]):
        gue = min(tau_t, 1.0)
        kp = K_primes_smooth[idx]
        print(f"  {tau_t:6.2f} | {gue:8.4f} | {kp:12.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. ALSO compute K_primes via cosine formula from GOAL (for comparison/diagnosis)
# ─────────────────────────────────────────────────────────────────────────────
print("\nComputing K_primes via COSINE formula (GOAL's formula)...")

# Use only primes up to T for cosine formula
T_for_cosine = T
log_T_over_2pi = np.log(T_for_cosine / (2*np.pi))

primes_T = list(primerange(2, int(T_for_cosine) + 1))
cos_positions = []
cos_weights = []
for p in primes_T:
    m = 1
    pm = p
    log_p = np.log(p)
    while pm <= T_for_cosine:
        log_pm = m * log_p
        weight = log_p**2 / pm
        cos_positions.append(log_pm / log_T_over_2pi)  # = tau_pm
        cos_weights.append(weight)
        m += 1
        pm *= p

cos_positions = np.array(cos_positions)
cos_weights = np.array(cos_weights)
norm_cosine = np.sum(cos_weights)

K_cosine = np.zeros(len(tau_vals))
for i, tau in enumerate(tau_vals):
    cosines = np.cos(2 * np.pi * tau * cos_positions)
    K_cosine[i] = np.dot(cos_weights, cosines) / norm_cosine

print(f"  K_cosine at tau=0: {K_cosine[0]:.4f} (should be 1.0)")
print(f"  K_cosine at tau=0.5: {K_cosine[int(0.5/dtau)]:.4f}")
print(f"  K_cosine at tau=1.0: {K_cosine[int(1.0/dtau)]:.4f}")
print(f"  K_cosine min: {K_cosine.min():.4f}, max: {K_cosine.max():.4f}")
print(f"  Note: K_cosine is oscillatory and NOT the form factor K(tau) > 0")

# ─────────────────────────────────────────────────────────────────────────────
# 5. K_GUE reference
# ─────────────────────────────────────────────────────────────────────────────
K_GUE = np.minimum(tau_vals, 1.0)

# ─────────────────────────────────────────────────────────────────────────────
# 6. Quantitative comparison
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("QUANTITATIVE COMPARISON")
print("="*60)

# Ramp region: tau in [0.1, 0.9] (avoiding DC peak and plateau transition)
ramp_mask = (tau_vals >= 0.1) & (tau_vals <= 0.9) & ~np.isnan(K_zeros_smooth) & ~np.isnan(K_primes_smooth)
plateau_mask = (tau_vals >= 1.1) & (tau_vals <= 2.5) & ~np.isnan(K_zeros_smooth) & ~np.isnan(K_primes_smooth)

mad_zeros_gue_ramp = np.mean(np.abs(K_zeros_smooth[ramp_mask] - K_GUE[ramp_mask]))
mad_primes_gue_ramp = np.mean(np.abs(K_primes_smooth[ramp_mask] - K_GUE[ramp_mask]))
mad_zeros_primes_ramp = np.mean(np.abs(K_zeros_smooth[ramp_mask] - K_primes_smooth[ramp_mask]))

mad_zeros_gue_plat = np.mean(np.abs(K_zeros_smooth[plateau_mask] - K_GUE[plateau_mask]))
mad_primes_gue_plat = np.mean(np.abs(K_primes_smooth[plateau_mask] - K_GUE[plateau_mask]))

print(f"\nRamp region (tau in [0.1, 0.9]):")
print(f"  MAD(K_zeros_smooth, K_GUE)   = {mad_zeros_gue_ramp:.4f}")
print(f"  MAD(K_primes_smooth, K_GUE)  = {mad_primes_gue_ramp:.4f}")
print(f"  MAD(K_zeros_smooth, K_primes_smooth) = {mad_zeros_primes_ramp:.4f}")

print(f"\nPlateau region (tau in [1.1, 2.5]):")
print(f"  MAD(K_zeros_smooth, K_GUE=1) = {mad_zeros_gue_plat:.4f}")
print(f"  MAD(K_primes_smooth, K_GUE=1)= {mad_primes_gue_plat:.4f}")

# Ramp-to-plateau transition: does K_primes increase from ramp to plateau?
k_primes_ramp_mean = np.mean(K_primes_smooth[ramp_mask])
k_primes_plat_mean = np.mean(K_primes_smooth[plateau_mask])
k_zeros_ramp_mean = np.mean(K_zeros_smooth[ramp_mask])
k_zeros_plat_mean = np.mean(K_zeros_smooth[plateau_mask])
print(f"\nRamp-to-plateau transition:")
print(f"  K_zeros_smooth:  ramp mean = {k_zeros_ramp_mean:.4f}, plateau mean = {k_zeros_plat_mean:.4f}")
print(f"  K_primes_smooth: ramp mean = {k_primes_ramp_mean:.4f}, plateau mean = {k_primes_plat_mean:.4f}")

# Norm breakdown (diagnostic of previous failure)
print(f"\nNorm breakdown for K_primes (why P_max variation had small effect):")
w_total = np.sum(weights)
for P_max in [10, 50, 100, 200, 500, 1000]:
    w_cut = np.sum(weights[positions < np.log(P_max)/(2*np.pi*rho_bar)])
    # Primes up to P_max correspond to tau < log(P_max)/(2*pi*rho_bar)
    primes_up_to_P = list(primerange(2, P_max+1))
    w_P = sum(np.log(p)**2/p for p in primes_up_to_P)
    print(f"  P_max={P_max:5d}: weight_sum = {w_P:.4f} ({100*w_P/np.sum([np.log(p)**2/p for p in primes_T]):.1f}%)")

print(f"\n  These weights DON'T change much because sum_p (log p)^2/p converges slowly.")
print(f"  The key is WHERE the contributions fall in tau space (binning), not total weight.")

# ─────────────────────────────────────────────────────────────────────────────
# 7. Save results
# ─────────────────────────────────────────────────────────────────────────────
OUT_PATH = "/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-006/code/part_a_v2_results.npz"
np.savez(OUT_PATH,
         tau_vals=tau_vals,
         K_zeros=K_zeros,
         K_zeros_smooth=K_zeros_smooth,
         K_primes_smooth=K_primes_smooth,
         K_cosine=K_cosine,
         K_GUE=K_GUE,
         T=np.array([T]),
         rho_bar=np.array([rho_bar]),
         mad_zeros_gue_ramp=np.array([mad_zeros_gue_ramp]),
         mad_primes_gue_ramp=np.array([mad_primes_gue_ramp]),
         mad_zeros_primes_ramp=np.array([mad_zeros_primes_ramp]))
print(f"\nResults saved to {OUT_PATH}")
print(f"\nTotal time: {time.time()-t0:.1f}s")
print("\nDone.")
