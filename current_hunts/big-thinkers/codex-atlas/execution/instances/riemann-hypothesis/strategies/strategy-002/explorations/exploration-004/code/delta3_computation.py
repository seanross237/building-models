"""
delta3_computation.py
=====================
Compute Δ₃ (spectral rigidity) from Riemann zeta zeros and compare to
Berry's (1985) theoretical prediction.

Parts:
  1. Unfold zeros correctly
  2. Compute Δ₃(L) using Dyson-Mehta formula
  3. Berry's theoretical prediction for saturation level
  4. Height-resolved analysis
"""

import numpy as np
import os
from scipy.optimize import minimize_scalar

# ─── Load zeros ───────────────────────────────────────────────────────────────
ZEROS_PATH = '../../exploration-003/code/zeta_zeros_2000.npy'
zeros = np.load(ZEROS_PATH)
N = len(zeros)
print(f"Loaded {N} zeta zeros. Range: {zeros[0]:.4f} to {zeros[-1]:.4f}")

# ─── Part 1: Unfold zeros ──────────────────────────────────────────────────────
# The smooth counting function (Weyl term) for Riemann zeros:
# N_smooth(T) ≈ (T/(2π)) * log(T/(2π)) - T/(2π) + 7/8
# Unfolding: xi_n = N_smooth(t_n)

def N_smooth(T):
    """Smooth part of zero counting function."""
    x = T / (2.0 * np.pi)
    return x * np.log(x) - x + 7.0/8.0

unfolded = N_smooth(zeros)
print(f"\nUnfolded zeros (first 10): {unfolded[:10]}")
print(f"Mean spacing of first 100 unfolded: {np.mean(np.diff(unfolded[:100])):.4f}")
print(f"Mean spacing of last 100 unfolded: {np.mean(np.diff(unfolded[-100:])):.4f}")

# After proper unfolding, mean spacing should be ≈ 1
# (The 7/8 constant shifts the count but doesn't affect spacings)

# ─── Part 2: Δ₃(L) computation ────────────────────────────────────────────────

def delta3_single(unfolded_sorted, L, E_start):
    """
    Compute Δ₃(L) for a single window starting at E_start.
    Uses the Dyson-Mehta least-squares formula.
    """
    mask = (unfolded_sorted >= E_start) & (unfolded_sorted < E_start + L)
    ys = unfolded_sorted[mask]
    n = len(ys)
    if n < 3:
        return np.nan

    # Staircase: rank i+1 for the i-th eigenvalue in window
    ranks = np.arange(1, n + 1, dtype=float)

    # Positions in window
    xs = ys - E_start  # in [0, L]

    # Least-squares fit: minimize Σ (rank_i - a*xs_i - b)^2
    # Design matrix
    A = np.column_stack([xs, np.ones(n)])
    result = np.linalg.lstsq(A, ranks, rcond=None)
    a, b = result[0]

    # Residuals
    residuals = ranks - (a * xs + b)

    # Δ₃(L) = (1/L) * sum of squared residuals
    return np.sum(residuals**2) / L


def delta3_average(unfolded_sorted, L, n_windows=200):
    """
    Compute Δ₃(L) averaged over n_windows starting positions.
    Windows are drawn from positions where there are enough zeros.
    """
    xmin = unfolded_sorted[0]
    xmax = unfolded_sorted[-1]

    # Valid start positions: ensure window [E_start, E_start+L] is inside range
    margin = L
    valid_start = xmin + 0.1
    valid_end = xmax - L - 0.1

    if valid_start >= valid_end:
        return np.nan

    starts = np.linspace(valid_start, valid_end, n_windows)
    vals = [delta3_single(unfolded_sorted, L, s) for s in starts]
    vals = [v for v in vals if not np.isnan(v)]

    if len(vals) == 0:
        return np.nan
    return np.mean(vals)


# Compute Δ₃(L) for range of L values
L_values = np.concatenate([
    np.linspace(1, 10, 10),
    np.linspace(10, 30, 21),
    np.linspace(30, 60, 11),
])
L_values = np.unique(np.round(L_values, 1))

print("\n\n=== Computing Δ₃(L) for range of L values ===")
print(f"{'L':>8} {'Δ₃(L)':>12} {'GUE_pred':>12}")
print("-" * 36)

# GUE prediction (asymptotic for large L)
gamma_E = 0.5772156649  # Euler-Mascheroni

def delta3_GUE(L):
    """GUE asymptotic formula: Δ₃_GUE(L) ≈ (1/π²)[log(2πL) + γ + 1 - π²/8]"""
    return (1.0/np.pi**2) * (np.log(2*np.pi*L) + gamma_E + 1.0 - np.pi**2/8.0)

delta3_vals = []
for L in L_values:
    d3 = delta3_average(unfolded, L, n_windows=200)
    gue_pred = delta3_GUE(L)
    delta3_vals.append(d3)
    print(f"{L:>8.1f} {d3:>12.5f} {gue_pred:>12.5f}")

delta3_vals = np.array(delta3_vals)

# Identify saturation level: look at L > 15
large_L_mask = L_values > 15
if np.sum(large_L_mask) > 0:
    sat_values = delta3_vals[large_L_mask]
    sat_values_clean = sat_values[~np.isnan(sat_values)]
    delta3_sat_measured = np.mean(sat_values_clean)
    delta3_sat_std = np.std(sat_values_clean)
    print(f"\nMeasured saturation level (L > 15): Δ₃_sat = {delta3_sat_measured:.4f} ± {delta3_sat_std:.4f}")

# ─── Part 3: Berry's theoretical prediction ────────────────────────────────────
print("\n\n=== Berry's (1985) theoretical prediction ===")

# Berry's key result:
# The spectral rigidity follows GUE for L < L_max, then saturates at Δ₃_GUE(L_max)
# For Riemann zeros at height T, L_max is approximately:
#   L_max ≈ T_H / (2π)   [in unfolded units]
# where T_H = log(T/(2π)) is the "Heisenberg time"
#
# Actually more carefully (Berry 1985, also Bogomolny-Keating 1996):
# In unfolded coordinates where mean spacing = 1:
#   L_max ~ (1/(2π)) * log(T/(2π)) * T^{1/2} / log(2)
# ... this doesn't seem right either.
#
# The correct statement from Berry (1985), eq (2.7), (3.15):
# For a system with classical period T_min = log(2) (shortest orbit = prime p=2),
# after unfolding with density ρ = log(T/2π)/(2π),
# the unfolded period is:
#   τ_min = ρ * T_min = log(2) * log(T/(2π)) / (2π)
#
# The form factor K(τ) follows GUE (K(τ) = τ for τ < 1, 1 for τ > 1) but
# the "saturation time" τ_1 where Riemann zeros first deviate from GUE is:
#   τ_1 = τ_min (the shortest orbit contribution)
#
# In L-space (unfolded), the saturation occurs at:
#   L_sat = 1/τ_1 = (2π) / (log(2) * log(T/(2π)))
#
# So Δ₃_sat = Δ₃_GUE(L_sat) = (1/π²) * [log(2π * L_sat) + γ + 1 - π²/8]
#
# Actually, I need to be more careful about the exact formula.
# Let me implement two versions:

# Version 1: Berry's L_max as T^{1/2} / (2π)  (from the GOAL.md hint)
# This comes from: L_max = T^{1/2} / (2π) in ORIGINAL coordinates, not unfolded
# In unfolded: L_max_unfolded = L_max * ρ(T) = T^{1/2}/(2π) * log(T/(2π))/(2π)
#            = T^{1/2} * log(T/(2π)) / (4π²)

# Version 2: L_max as the Heisenberg time (τ_H = 1 in GUE corresponds to L_H = T_H/something)

# Version 3: Direct Berry formula (approximate for zeros near height T):
# Δ₃_sat ≈ (1/π²) * log(T/(2π))   [often cited approximation]

# Let's compute all three for comparison

# Geometric mean height of all 2000 zeros
T_geo_all = np.exp(np.mean(np.log(zeros)))
T_median_all = np.median(zeros)

print(f"\nHeight statistics for 2000 zeros:")
print(f"  Geometric mean: T_geo = {T_geo_all:.2f}")
print(f"  Median: T_med = {T_median_all:.2f}")
print(f"  Range: [{zeros[0]:.2f}, {zeros[-1]:.2f}]")

# The unfolding density at height T
def rho(T):
    return np.log(T / (2*np.pi)) / (2*np.pi)

print(f"\nLocal density ρ(T_geo) = {rho(T_geo_all):.4f}")

# Approximation 1: Δ₃_sat ≈ (1/π²) * log(T/(2π))
# This is the simplest formula often cited
def delta3_sat_berry_simple(T):
    return (1.0/np.pi**2) * np.log(T / (2*np.pi))

# Approximation 2: Use L_max = T^{1/2}/(2π) in GUE formula
# (Berry 1985 - saturation occurs when prime orbit with log p starts contributing)
def delta3_sat_berry_v2(T):
    """Using L_max ~ T^{1/2}/(2π) as Berry's saturation scale."""
    L_max = np.sqrt(T) / (2*np.pi)
    return delta3_GUE(L_max)

# Approximation 3: Bogomolny-Keating (1996) correction / Berry exact
# L_max_unfolded = (1/(2π)) * log(T/(2π)) where factor accounts for unfolding
# This arises from: shortest orbit log(2) in unfolded units becomes log(2)*ρ(T)
# Saturation at L where L * log(2) * ρ(T) ≈ constant
def delta3_sat_berry_v3(T):
    """Using L_max via shortest prime orbit (log 2)."""
    rho_T = np.log(T / (2*np.pi)) / (2*np.pi)
    # Shortest orbit period τ_min = log(2) in original units
    # In unfolded units: τ_min_unf = log(2) * rho_T
    # Saturation at L_max = 1/τ_min_unf (spectral ~ 1/orbit-length)
    # But this is very small...
    # Alternative: the "coherence length" from Berry
    # L_max ~ (2π) / (log(2) * log(T/(2π))) - this is L in unfolded coords
    tau_min = np.log(2) * rho_T
    L_max = 1.0 / tau_min  # L_max in unfolded units where mean spacing = 1
    return delta3_GUE(L_max)

print("\n\n=== Berry's theoretical predictions ===")
print(f"\nFor T_geo = {T_geo_all:.2f}:")
pred1 = delta3_sat_berry_simple(T_geo_all)
pred2 = delta3_sat_berry_v2(T_geo_all)
pred3 = delta3_sat_berry_v3(T_geo_all)
print(f"  Version 1 [simple, (1/π²)log(T/2π)]: Δ₃_sat = {pred1:.4f}")
print(f"  Version 2 [L_max=√T/(2π)]:           Δ₃_sat = {pred2:.4f}")
print(f"  Version 3 [L_max=1/(log(2)*ρ(T))]:   Δ₃_sat = {pred3:.4f}")
print(f"\nMeasured: Δ₃_sat = {delta3_sat_measured:.4f}")

# Also compute GUE at L=15 (observed saturation onset)
print(f"\nGUE prediction at L=15: {delta3_GUE(15):.4f}")
print(f"GUE prediction at L=20: {delta3_GUE(20):.4f}")

# ─── Part 4: Height-resolved analysis ─────────────────────────────────────────
print("\n\n=== Height-resolved Δ₃ analysis ===")

# Split zeros into 4 height bins
bins = [
    (0, 500),
    (500, 1000),
    (1000, 1500),
    (1500, 2000),
]

print(f"\n{'Bin':>12} {'T_min':>8} {'T_max':>8} {'T_geo':>8} {'Δ₃_sat_meas':>14} {'Berry_v1':>10} {'Berry_v2':>10}")
print("-" * 75)

for (i_start, i_end) in bins:
    zeros_bin = zeros[i_start:i_end]
    unfolded_bin = unfolded[i_start:i_end]

    T_geo_bin = np.exp(np.mean(np.log(zeros_bin)))

    # Compute Δ₃ saturation for this bin (use L = 15-30 range)
    sat_vals = []
    for L in [15, 17, 20, 22, 25]:
        d3 = delta3_average(unfolded_bin, L, n_windows=100)
        if not np.isnan(d3):
            sat_vals.append(d3)

    d3_sat = np.mean(sat_vals) if sat_vals else np.nan

    berry1 = delta3_sat_berry_simple(T_geo_bin)
    berry2 = delta3_sat_berry_v2(T_geo_bin)

    print(f"  {i_start+1:4d}-{i_end:4d}  {zeros_bin[0]:>8.1f} {zeros_bin[-1]:>8.1f} {T_geo_bin:>8.1f} {d3_sat:>14.4f} {berry1:>10.4f} {berry2:>10.4f}")

print("\n\nNote: Berry predicts Δ₃_sat should increase with T_geo.")

# ─── Save results ──────────────────────────────────────────────────────────────
np.savez('delta3_results.npz',
         L_values=L_values,
         delta3_vals=delta3_vals,
         unfolded=unfolded,
         zeros=zeros)
print("\n\nResults saved to delta3_results.npz")
print("Done.")
