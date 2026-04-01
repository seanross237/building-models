"""
Full computation: smooth spectrum + prime corrections + direct N_osc comparison
Uses the CORRECT explicit formula (without ln(p) factor).
"""
import numpy as np
from scipy.optimize import brentq
from sympy import primerange
import json
import time

############################################################
# Part 0: Helper functions
############################################################

def N_smooth(T):
    """Smooth zero counting function (Weyl term)"""
    if T <= 0:
        return 0
    return (T / (2 * np.pi)) * np.log(T / (2 * np.pi * np.e)) + 7/8

def N_smooth_deriv(T):
    """Derivative of smooth counting function"""
    if T <= 0:
        return 0
    return (1 / (2 * np.pi)) * np.log(T / (2 * np.pi))

############################################################
# Part 1: Load smooth zeros
############################################################

with open('smooth_zeros.json') as f:
    smooth_zeros = np.array(json.load(f))

N = len(smooth_zeros)
derivs = np.array([N_smooth_deriv(t) for t in smooth_zeros])

print(f"Loaded {N} smooth zeros")
print(f"Range: [{smooth_zeros[0]:.4f}, {smooth_zeros[-1]:.4f}]")

############################################################
# Part 2: Prime corrections (CORRECTED formula - no ln(p))
############################################################

all_primes = list(primerange(2, 10001))
M_max = 5

P_max_values = [100, 1000, 10000]
all_corrections = {}

for P_max in P_max_values:
    t0 = time.time()
    primes = [p for p in all_primes if p <= P_max]
    n_primes = len(primes)

    print(f"\n--- P_max = {P_max}, {n_primes} primes ---")

    # N_osc(T) = -(1/pi) * sum_p sum_m (1/(m*p^{m/2})) * sin(m*T*ln(p))
    # delta_n = -N_osc(t_smooth) / N_smooth'(t_smooth)
    #         = (1/pi) * sum / N_smooth'

    N_osc_vals = np.zeros(N)

    for p in primes:
        lp = np.log(float(p))
        for m in range(1, M_max + 1):
            coeff = 1.0 / (m * float(p)**(m/2.0))
            sin_terms = np.sin(m * smooth_zeros * lp)
            N_osc_vals += -(1.0/np.pi) * coeff * sin_terms

    # Correction to zero positions
    delta_t = -N_osc_vals / derivs

    corrected = smooth_zeros + delta_t

    elapsed = time.time() - t0
    print(f"Computation time: {elapsed:.2f}s")

    all_corrections[P_max] = {
        'N_osc': N_osc_vals.tolist(),
        'delta_t': delta_t.tolist(),
        'corrected': corrected.tolist(),
        'n_primes': n_primes,
    }

    # Print first 10
    print(f"  First 10 corrections delta_t:")
    for i in range(10):
        print(f"    n={i+1}: N_osc={N_osc_vals[i]:+.6f}, delta_t={delta_t[i]:+.6f}")

# Save all corrections
with open('all_corrections.json', 'w') as f:
    json.dump({str(k): v for k, v in all_corrections.items()}, f)

print("\nSaved all corrections to all_corrections.json")
