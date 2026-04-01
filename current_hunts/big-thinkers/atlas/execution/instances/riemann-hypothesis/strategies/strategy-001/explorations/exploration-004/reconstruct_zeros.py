"""
Reconstruct zeta zeros by solving N_smooth(T) + N_osc_prime(T) = n
where N_osc_prime is the prime sum approximation to the oscillatory part.

This is more accurate than the linearized correction formula.
"""
import numpy as np
from scipy.optimize import brentq
from sympy import primerange
import json
import time

def N_smooth(T):
    if T <= 0:
        return 0
    return (T / (2 * np.pi)) * np.log(T / (2 * np.pi * np.e)) + 7/8

def N_smooth_deriv(T):
    if T <= 0:
        return 0
    return (1 / (2 * np.pi)) * np.log(T / (2 * np.pi))

# Load smooth zeros for initial guesses
with open('smooth_zeros.json') as f:
    smooth_zeros = json.load(f)

# Precompute prime data
all_primes_list = list(primerange(2, 10001))
M_max = 5

def make_N_osc_func(primes, M_max=5):
    """Create N_osc function for a given set of primes."""
    primes_arr = np.array(primes, dtype=float)
    lnp = np.log(primes_arr)

    # Precompute coefficients for each (p, m)
    coeffs = []
    for ip, p in enumerate(primes_arr):
        for m in range(1, M_max + 1):
            c = 1.0 / (m * p**(m/2.0))
            coeffs.append((c, m, lnp[ip]))

    def N_osc(T):
        val = 0.0
        for c, m, lp in coeffs:
            val += -(1.0/np.pi) * c * np.sin(m * T * lp)
        return val

    return N_osc

def make_N_total_func(N_osc_func):
    """N_total(T) = N_smooth(T) + N_osc(T)"""
    def N_total(T):
        return N_smooth(T) + N_osc_func(T)
    return N_total

P_max_values = [100, 1000, 10000]
results = {}

for P_max in P_max_values:
    t0 = time.time()
    primes = [p for p in all_primes_list if p <= P_max]
    n_primes = len(primes)

    print(f"\n=== P_max = {P_max}, {n_primes} primes ===")

    N_osc = make_N_osc_func(primes, M_max)
    N_total = make_N_total_func(N_osc)

    # Find zeros: solve N_total(T) = n for each n
    corrected_zeros = []
    failures = 0

    for n in range(1, 2001):
        target = float(n)
        # Use smooth zero as initial guess, search in a window
        t_guess = smooth_zeros[n-1]
        spacing = 2 * np.pi / max(N_smooth_deriv(t_guess), 0.01) if N_smooth_deriv(t_guess) > 0 else 10

        # Search window: multiple of the mean spacing
        lo = max(1.0, t_guess - 2 * spacing)
        hi = t_guess + 2 * spacing

        f_lo = N_total(lo) - target
        f_hi = N_total(hi) - target

        # Extend if needed
        tries = 0
        while f_lo * f_hi > 0 and tries < 10:
            lo = max(1.0, lo - spacing)
            hi = hi + spacing
            f_lo = N_total(lo) - target
            f_hi = N_total(hi) - target
            tries += 1

        if f_lo * f_hi > 0:
            # Can't bracket, use smooth zero
            corrected_zeros.append(t_guess)
            failures += 1
        else:
            try:
                t_corr = brentq(lambda t: N_total(t) - target, lo, hi, xtol=1e-10)
                corrected_zeros.append(t_corr)
            except:
                corrected_zeros.append(t_guess)
                failures += 1

    elapsed = time.time() - t0
    print(f"Time: {elapsed:.1f}s, failures: {failures}")

    results[str(P_max)] = {
        'corrected': corrected_zeros,
        'n_primes': n_primes,
        'failures': failures,
        'time': elapsed
    }

    # Print first 20
    print(f"\n  First 20 corrected zeros:")
    for i in range(20):
        print(f"    n={i+1}: smooth={smooth_zeros[i]:.4f}, corrected={corrected_zeros[i]:.4f}, delta={corrected_zeros[i]-smooth_zeros[i]:.4f}")

# Save
with open('reconstructed_zeros.json', 'w') as f:
    json.dump(results, f)

print("\nSaved to reconstructed_zeros.json")
