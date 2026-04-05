#!/usr/bin/env python3
"""
Task 3 & 4: Analyze asymptotic residuals of Li coefficients and search for patterns.

Residual δ_n = λ_n − [(n/2)·log(n/2πe) + (n/2)·(γ_E − 1)]
Coffey residual = λ_n − [(n/2)·log(n/2π) + (n/2)·(γ_E − 1) + (1/2)·log(π) + (1/8)·log(4π/e) + (1/2)]
"""

import numpy as np
import os
import json

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(CODE_DIR)

# Load computed Li coefficients
data = np.load(os.path.join(CODE_DIR, 'li_coefficients.npz'))
n_values = data['n_values']
lambda_real = data['lambda_real']
lambda_imag = data['lambda_imag']

print(f"Loaded {len(n_values)} Li coefficients (n=1..{n_values[-1]})")
print(f"Max |imag part|: {np.max(np.abs(lambda_imag)):.2e}")

# Constants
gamma_E = 0.5772156649015328606065120900824024310421593359  # Euler-Mascheroni
e = np.e

# ============================================================
# Task 3: Asymptotic Residual Analysis
# ============================================================

print("\n" + "=" * 70)
print("TASK 3: ASYMPTOTIC RESIDUAL ANALYSIS")
print("=" * 70)

# Bombieri-Lagarias leading asymptotics
# λ_n ~ (n/2)·log(n/(2πe)) + (n/2)·(γ_E − 1) + O(log n)
def bl_asymptotic(n):
    """Bombieri-Lagarias leading asymptotic."""
    return (n / 2) * np.log(n / (2 * np.pi * e)) + (n / 2) * (gamma_E - 1)

# Coffey (2004) more precise asymptotics
# λ_n = (n/2)·log(n/2π) + (n/2)·(γ_E − 1) + (1/2)·log(π) + (1/8)·log(4π/e) + (1/2) + O((log n)/n)
def coffey_asymptotic(n):
    """Coffey 2004 asymptotic."""
    return ((n / 2) * np.log(n / (2 * np.pi)) +
            (n / 2) * (gamma_E - 1) +
            0.5 * np.log(np.pi) +
            (1/8) * np.log(4 * np.pi / e) +
            0.5)

# Compute residuals
n_arr = n_values.astype(float)
delta_bl = lambda_real - np.array([bl_asymptotic(n) for n in n_arr])
delta_coffey = lambda_real - np.array([coffey_asymptotic(n) for n in n_arr])

print("\nResidual δ_n (Bombieri-Lagarias):")
print(f"{'n':>5} | {'λ_n':>18} | {'BL asymptotic':>18} | {'δ_n':>15}")
print("-" * 65)
for i in [0, 1, 2, 4, 9, 19, 49, 99, 199, 299, 399, 499]:
    if i < len(n_values):
        n = n_values[i]
        print(f"{n:>5} | {lambda_real[i]:>18.10f} | {bl_asymptotic(n):>18.10f} | {delta_bl[i]:>15.10f}")

print("\nResidual δ_n (Coffey 2004):")
print(f"{'n':>5} | {'λ_n':>18} | {'Coffey asymptotic':>18} | {'δ_n^C':>15}")
print("-" * 65)
for i in [0, 1, 2, 4, 9, 19, 49, 99, 199, 299, 399, 499]:
    if i < len(n_values):
        n = n_values[i]
        print(f"{n:>5} | {lambda_real[i]:>18.10f} | {coffey_asymptotic(n):>18.10f} | {delta_coffey[i]:>15.10f}")

# Compare BL vs Coffey residual magnitudes
mask = n_arr >= 50  # Use large n for comparison
if np.any(mask):
    mean_bl = np.mean(np.abs(delta_bl[mask]))
    mean_coffey = np.mean(np.abs(delta_coffey[mask]))
    print(f"\nMean |δ_n| for n≥50:")
    print(f"  Bombieri-Lagarias: {mean_bl:.10f}")
    print(f"  Coffey 2004:      {mean_coffey:.10f}")
    print(f"  Coffey reduces error by factor: {mean_bl/mean_coffey:.2f}x" if mean_coffey > 0 else "")

# Growth rate analysis
print("\n--- Growth Rate Analysis ---")
mask2 = n_arr >= 10
if np.any(mask2):
    ratio_logn = delta_coffey[mask2] / np.log(n_arr[mask2])
    ratio_sqrtn = delta_coffey[mask2] / np.sqrt(n_arr[mask2])
    ratio_1 = delta_coffey[mask2]  # raw

    print(f"\nδ_n^C / log(n) for selected n:")
    for i in [9, 19, 49, 99, 199, 299, 399, 499]:
        if i < len(n_values):
            n = n_values[i]
            if n >= 10:
                print(f"  n={n}: {delta_coffey[i]/np.log(n):.10f}")

    print(f"\nδ_n^C / √n for selected n:")
    for i in [9, 19, 49, 99, 199, 299, 399, 499]:
        if i < len(n_values):
            n = n_values[i]
            if n >= 10:
                print(f"  n={n}: {delta_coffey[i]/np.sqrt(n):.10f}")

    # Check if δ_n^C / log(n) converges
    last_50 = delta_coffey[-50:] / np.log(n_arr[-50:])
    print(f"\nδ_n^C / log(n) for last 50 values: mean={np.mean(last_50):.10f}, std={np.std(last_50):.10f}")

# Monotonicity check
print("\n--- Monotonicity/Trend Analysis ---")
if len(delta_coffey) > 1:
    diffs = np.diff(delta_coffey)
    n_increasing = np.sum(diffs > 0)
    n_decreasing = np.sum(diffs < 0)
    print(f"Coffey residual: {n_increasing} increases, {n_decreasing} decreases")
    if len(diffs) > 0:
        print(f"Fraction increasing: {n_increasing/len(diffs):.4f}")

# ============================================================
# Task 4: Pattern Search
# ============================================================

print("\n" + "=" * 70)
print("TASK 4: PATTERN SEARCH")
print("=" * 70)

# 4a: FFT Analysis
print("\n--- 4a: FFT Analysis ---")
# Use Coffey residual for n=50 to max_n
start_n = 50
mask_fft = n_arr >= start_n
if np.sum(mask_fft) > 10:
    signal = delta_coffey[mask_fft]
    # Remove mean and linear trend
    x = np.arange(len(signal))
    coeffs = np.polyfit(x, signal, 1)
    detrended = signal - np.polyval(coeffs, x)

    fft_vals = np.fft.rfft(detrended)
    fft_power = np.abs(fft_vals) ** 2
    fft_freqs = np.fft.rfftfreq(len(detrended), d=1.0)  # d=1 since n increments by 1

    # Find dominant frequencies (excluding DC)
    fft_power_noDC = fft_power.copy()
    fft_power_noDC[0] = 0
    top_k = min(10, len(fft_power_noDC))
    top_indices = np.argsort(fft_power_noDC)[-top_k:][::-1]

    print(f"FFT of detrended Coffey residual (n={start_n}..{int(n_arr[mask_fft][-1])})")
    print(f"Signal length: {len(signal)}")
    print(f"\nTop {top_k} FFT peaks:")
    print(f"{'Rank':>5} | {'Freq':>12} | {'Period':>12} | {'Power':>15} | {'log(period)':>12}")
    print("-" * 70)
    for rank, idx in enumerate(top_indices):
        freq = fft_freqs[idx]
        period = 1.0 / freq if freq > 0 else float('inf')
        power = fft_power[idx]
        logp = np.log(period) if period < float('inf') else float('inf')
        print(f"{rank+1:>5} | {freq:>12.6f} | {period:>12.4f} | {power:>15.6f} | {logp:>12.6f}")

    # Check if any period matches log(p) for small primes
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    log_primes = {p: np.log(p) for p in primes}
    print(f"\nComparison with log(prime) periods:")
    for p in primes:
        lp = log_primes[p]
        # Find closest FFT peak
        if len(fft_freqs) > 1:
            periods = 1.0 / fft_freqs[1:]  # exclude DC
            closest_idx = np.argmin(np.abs(periods - lp))
            closest_period = periods[closest_idx]
            power_at = fft_power[closest_idx + 1]
            print(f"  log({p}) = {lp:.6f}: closest FFT period = {closest_period:.6f}, "
                  f"power = {power_at:.6f}, match = {abs(closest_period - lp)/lp*100:.1f}%")

    # Save FFT results
    np.savez(os.path.join(CODE_DIR, 'fft_results.npz'),
             fft_freqs=fft_freqs, fft_power=fft_power,
             detrended_signal=detrended, start_n=start_n)

# 4b: Growth rate analysis (detailed)
print("\n--- 4b: Detailed Growth Rate Analysis ---")
if len(n_arr) >= 100:
    # Fit δ_n^C to various models
    mask_fit = n_arr >= 20
    n_fit = n_arr[mask_fit]
    d_fit = delta_coffey[mask_fit]

    # Model 1: δ ~ a * log(n) + b
    A = np.column_stack([np.log(n_fit), np.ones_like(n_fit)])
    result1 = np.linalg.lstsq(A, d_fit, rcond=None)
    c1 = result1[0]
    resid1 = np.sum((d_fit - A @ c1)**2)
    print(f"Model δ ~ a·log(n) + b: a={c1[0]:.10f}, b={c1[1]:.10f}, RSS={resid1:.6e}")

    # Model 2: δ ~ a * log(n)/n + b/n + c
    A2 = np.column_stack([np.log(n_fit)/n_fit, 1.0/n_fit, np.ones_like(n_fit)])
    result2 = np.linalg.lstsq(A2, d_fit, rcond=None)
    c2 = result2[0]
    resid2 = np.sum((d_fit - A2 @ c2)**2)
    print(f"Model δ ~ a·log(n)/n + b/n + c: a={c2[0]:.6f}, b={c2[1]:.6f}, c={c2[2]:.10f}, RSS={resid2:.6e}")

    # Model 3: δ ~ a/n + b
    A3 = np.column_stack([1.0/n_fit, np.ones_like(n_fit)])
    result3 = np.linalg.lstsq(A3, d_fit, rcond=None)
    c3 = result3[0]
    resid3 = np.sum((d_fit - A3 @ c3)**2)
    print(f"Model δ ~ a/n + b: a={c3[0]:.6f}, b={c3[1]:.10f}, RSS={resid3:.6e}")

    print(f"\nBest fit (lowest RSS): ", end="")
    best = min([(resid1, "a·log(n)+b"), (resid2, "a·log(n)/n+b/n+c"), (resid3, "a/n+b")], key=lambda x: x[0])
    print(f"{best[1]} with RSS={best[0]:.6e}")

# 4c: Prime correlation test
print("\n--- 4c: Prime Correlation Test ---")
from sympy import isprime

if len(n_arr) >= 50:
    prime_mask = np.array([isprime(int(n)) for n in n_arr])
    prime_minus1_mask = np.array([isprime(int(n) + 1) for n in n_arr])

    # Compare |δ_n| at primes vs non-primes
    d_at_primes = np.abs(delta_coffey[prime_mask])
    d_at_nonprimes = np.abs(delta_coffey[~prime_mask])
    d_at_pm1 = np.abs(delta_coffey[prime_minus1_mask])

    if len(d_at_primes) > 0 and len(d_at_nonprimes) > 0:
        mean_primes = np.mean(d_at_primes)
        mean_nonprimes = np.mean(d_at_nonprimes)
        mean_pm1 = np.mean(d_at_pm1) if len(d_at_pm1) > 0 else float('nan')

        print(f"Number of primes in range: {np.sum(prime_mask)}")
        print(f"Mean |δ_n^C| at prime n:     {mean_primes:.10f}")
        print(f"Mean |δ_n^C| at non-prime n: {mean_nonprimes:.10f}")
        print(f"Mean |δ_n^C| at n=p-1:       {mean_pm1:.10f}")
        print(f"Ratio (prime/non-prime): {mean_primes/mean_nonprimes:.6f}")

        # Welch's t-test (manual, avoiding scipy)
        n1, n2 = len(d_at_primes), len(d_at_nonprimes)
        s1, s2 = np.std(d_at_primes, ddof=1), np.std(d_at_nonprimes, ddof=1)
        m1, m2 = mean_primes, mean_nonprimes
        t_stat = (m1 - m2) / np.sqrt(s1**2/n1 + s2**2/n2)
        print(f"Welch's t-statistic: {t_stat:.4f} (|t|>2 would suggest significance)")

# Save analysis results
results = {
    'task3': {
        'mean_abs_delta_bl_n50plus': float(mean_bl) if np.any(mask) else None,
        'mean_abs_delta_coffey_n50plus': float(mean_coffey) if np.any(mask) else None,
    },
    'task4a': {
        'fft_dominant_period': float(1.0/fft_freqs[top_indices[0]]) if len(top_indices) > 0 and fft_freqs[top_indices[0]] > 0 else None,
        'fft_dominant_power': float(fft_power[top_indices[0]]) if len(top_indices) > 0 else None,
    },
    'task4c': {
        'mean_delta_at_primes': float(mean_primes) if 'mean_primes' in dir() else None,
        'mean_delta_at_nonprimes': float(mean_nonprimes) if 'mean_nonprimes' in dir() else None,
        't_statistic': float(t_stat) if 't_stat' in dir() else None,
    }
}

with open(os.path.join(CODE_DIR, 'analysis_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

np.savez(os.path.join(CODE_DIR, 'residuals.npz'),
         n_values=n_values, delta_bl=delta_bl, delta_coffey=delta_coffey)

print("\nAnalysis saved to residuals.npz and analysis_results.json")
print("\n=== ANALYSIS COMPLETE ===")
