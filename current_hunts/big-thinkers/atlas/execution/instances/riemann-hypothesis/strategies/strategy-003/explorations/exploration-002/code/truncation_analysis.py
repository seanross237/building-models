#!/usr/bin/env python3
"""
Analyze truncation effects: how does the number of zeros affect λ_n?
Also compute the convergence rate to understand the Coffey residual growth.
"""

import numpy as np
import pickle
import os
from mpmath import mp, mpf, mpc, re as mpre, im as mpim, fsum, log, pi, euler

mp.dps = 50

CODE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load cached zeros
with open(os.path.join(CODE_DIR, 'zeros_cache.pkl'), 'rb') as f:
    zeros = pickle.load(f)

print("=" * 70)
print("TRUNCATION ANALYSIS")
print("=" * 70)

# Compute λ_n for various truncation levels
truncation_levels = [100, 200, 500, 1000, 1500, 2000]
test_ns = [1, 5, 10, 20, 50, 100, 200, 500]

print(f"\nλ_n as a function of truncation level K (number of zero pairs):")
print(f"{'n':>5}", end="")
for K in truncation_levels:
    print(f" | {'K='+str(K):>14}", end="")
print()
print("-" * (6 + 17 * len(truncation_levels)))

results = {}
for n in test_ns:
    row = {}
    for K in truncation_levels:
        total = mpf(0)
        for rho in zeros[:K]:
            term_rho = 1 - (1 - 1/rho)**n
            rho_bar = rho.conjugate()
            term_rho_bar = 1 - (1 - 1/rho_bar)**n
            total += term_rho + term_rho_bar
        val = float(mpre(total))
        row[K] = val

    print(f"{n:>5}", end="")
    for K in truncation_levels:
        print(f" | {row[K]:>14.8f}", end="")
    print()

    # Rate of convergence: (λ_n(2000) - λ_n(1000)) / (λ_n(1000) - λ_n(500))
    if 500 in row and 1000 in row and 2000 in row:
        d1 = row[2000] - row[1000]
        d2 = row[1000] - row[500]
        ratio = d1 / d2 if d2 != 0 else float('inf')
        results[n] = {
            'vals': row,
            'convergence_ratio': ratio,
            'last_increment': d1
        }

print(f"\n--- Convergence Analysis ---")
print(f"{'n':>5} | {'Δ(500→1000)':>14} | {'Δ(1000→2000)':>14} | {'Ratio':>10} | {'Est. missing':>14}")
print("-" * 68)
for n in test_ns:
    if n in results:
        r = results[n]
        d500_1000 = r['vals'][1000] - r['vals'][500]
        d1000_2000 = r['vals'][2000] - r['vals'][1000]
        ratio = d1000_2000 / d500_1000 if d500_1000 != 0 else float('inf')

        # Estimate missing contribution (extrapolate):
        # If convergence is like K^(-α), then missing ≈ d1000_2000 * ratio / (1-ratio)
        # This is a geometric series extrapolation
        if 0 < abs(ratio) < 1:
            est_missing = d1000_2000 * ratio / (1 - ratio)
        else:
            est_missing = float('inf')

        print(f"{n:>5} | {d500_1000:>14.8f} | {d1000_2000:>14.8f} | {ratio:>10.6f} | {est_missing:>14.8f}")

# Expected λ_1 check
print(f"\n--- λ_1 Convergence ---")
expected_l1 = float(1 + euler/2 - log(2) - log(pi)/2)
for K in truncation_levels:
    total = mpf(0)
    for rho in zeros[:K]:
        total += 1 - (1 - 1/rho)**1 + 1 - (1 - 1/rho.conjugate())**1
    val = float(mpre(total))
    print(f"  K={K:>5}: λ_1 = {val:.15f}, error = {abs(val - expected_l1):.6e}")

# Understand the individual zero contribution magnitude
print(f"\n--- Individual zero contribution for large n ---")
print(f"How much does zero #k contribute to λ_n?")
print(f"For ρ = 1/2 + it, contribution ≈ 2*Re[1 - (1-1/ρ)^n]")
print(f"|1-1/ρ|² = 1 - 2/(1 + 4t²) + 1/(1/4 + t²)")
for k_idx in [0, 9, 99, 499, 999, 1999]:
    rho = zeros[k_idx]
    t = float(mpim(rho))
    r_sq = float(abs(1 - 1/rho)**2)
    r = r_sq**0.5
    print(f"  Zero #{k_idx+1}: t = {t:.2f}, |1-1/ρ| = {r:.10f}")
    for n in [10, 100, 500]:
        decay = r**n
        print(f"    n={n}: |1-1/ρ|^n = {decay:.2e}, so contribution ≈ {2*(1-decay):.6f} (of 2)")

# Key insight: for large n, each zero contributes ~2 (its maximum).
# The tail (zeros > 2000) contributes ~2 each, so missing ≈ 2*(total_zeros - 2000).
# Total zeros up to height T: N(T) ~ (T/2π)log(T/2πe)
# Our last zero is at t ≈ 2515, so N(2515) ≈ (2515/2π)log(2515/2πe) ≈ 2515/6.28 * 5.99 ≈ 2399
# We have 2000 pairs, so we're missing about 399 pairs (798 zeros) up to t=2515 — wait, no.
# We actually have the FIRST 2000 zeros (all zeros up to t ≈ 2515).
# The missing zeros are those with t > 2515. For large n, each contributes ≈ 2.
# True λ_n ≈ 2 * N(∞) = ∞ ... no, that's wrong.
# Actually λ_n for finite n converges because (1-1/ρ)^n doesn't go to 1 fast enough.

print(f"\n--- Saturation analysis for large n ---")
print(f"As n → ∞, for each zero ρ with |1-1/ρ| < 1:")
print(f"  (1-1/ρ)^n → 0, so each zero contributes 2 to λ_n")
print(f"  With K zero pairs, λ_n → 4K = {4*len(zeros)}")
print(f"  True λ_n ~ (n/2)log(n) → ∞")
print(f"  So truncation causes λ_n to plateau while true value grows")
print(f"\nFor our values:")
for n in [100, 200, 300, 400, 500]:
    # Check how close each zero's contribution is to saturation (2)
    total_contribution = 0.0
    near_saturation = 0
    for rho in zeros:
        r_sq = float(abs(1 - 1/rho)**2)
        decay = r_sq**(n/2)
        contribution = 2 * (1 - decay)
        total_contribution += contribution
        if decay < 0.01:
            near_saturation += 1
    print(f"  n={n}: λ_n ≈ {total_contribution:.2f}, zeros at >99% saturation: {near_saturation}/{len(zeros)} ({100*near_saturation/len(zeros):.1f}%)")

print(f"\n=== TRUNCATION ANALYSIS COMPLETE ===")
