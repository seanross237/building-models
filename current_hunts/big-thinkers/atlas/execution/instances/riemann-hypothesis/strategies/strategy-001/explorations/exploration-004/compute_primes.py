"""Compute prime oscillatory corrections to the smooth spectrum"""
import numpy as np
from sympy import primerange
import json
import time

# Load smooth zeros and derivatives
with open('smooth_zeros.json') as f:
    smooth_zeros = np.array(json.load(f))
with open('smooth_derivs.json') as f:
    derivs = np.array(json.load(f))

N = len(smooth_zeros)
M_max = 5  # powers of primes

# Precompute ln(p) for all primes up to 10000
all_primes = list(primerange(2, 10001))
ln_primes = np.log(np.array(all_primes, dtype=float))
print(f"Total primes up to 10000: {len(all_primes)}")

P_max_values = [100, 1000, 10000]
results = {}

for P_max in P_max_values:
    t0 = time.time()
    # Select primes up to P_max
    mask = np.array(all_primes) <= P_max
    primes = np.array(all_primes)[mask]
    lnp = ln_primes[mask]
    n_primes = len(primes)

    print(f"\n--- P_max = {P_max}, using {n_primes} primes ---")

    # Compute N_osc correction for each zero
    # N_osc(T) = -(1/pi) * sum_p sum_m (ln(p)/(m*p^{m/2})) * sin(m*T*ln(p))
    # delta_t = N_osc(t_smooth) / N_smooth'(t_smooth)

    corrections = np.zeros(N)

    for i_p in range(n_primes):
        p = primes[i_p]
        lp = lnp[i_p]
        for m in range(1, M_max + 1):
            coeff = lp / (m * p**(m/2.0))
            # Vectorized over all zeros
            sin_terms = np.sin(m * smooth_zeros * lp)
            corrections += -(1.0/np.pi) * coeff * sin_terms

    # Convert from N-correction to t-correction by dividing by N_smooth'
    delta_t = corrections / derivs

    corrected = smooth_zeros + delta_t

    elapsed = time.time() - t0
    print(f"Computation time: {elapsed:.2f}s")

    # Save results
    results[P_max] = {
        'corrections': delta_t.tolist(),
        'corrected': corrected.tolist(),
        'n_primes': n_primes,
        'time': elapsed
    }

with open('prime_corrections.json', 'w') as f:
    json.dump(results, f)

print("\nSaved prime corrections for all P_max values")
print(f"\nSample corrections (first 10) for P_max=10000:")
for i in range(10):
    print(f"  n={i+1}: delta_t = {results[10000]['corrections'][i]:.6f}")
