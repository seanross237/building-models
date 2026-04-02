"""Compute the smooth spectrum by inverting N_smooth(T) = n - 1/2"""
import numpy as np
from scipy.optimize import brentq
import json

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

# Compute smooth spectrum: solve N_smooth(t) = n - 1/2 for each n
smooth_zeros = []
for n in range(1, 2001):
    target = n - 0.5
    # N_smooth is monotonically increasing, use brentq
    # Need good bounds: N_smooth(T) ~ T/(2*pi) * ln(T/(2*pi*e))
    # Rough inversion: T ~ 2*pi*n / ln(n) for large n
    if n == 1:
        lo, hi = 1.0, 20.0
    else:
        lo = smooth_zeros[-1]
        hi = lo + 20  # spacing is roughly 2*pi/ln(T/(2*pi))

    # Extend hi if needed
    while N_smooth(hi) < target:
        hi *= 1.5

    t_smooth = brentq(lambda t: N_smooth(t) - target, lo, hi)
    smooth_zeros.append(t_smooth)

with open('smooth_zeros.json', 'w') as f:
    json.dump(smooth_zeros, f)

print(f"Computed {len(smooth_zeros)} smooth zeros")
print(f"First 10: {[f'{z:.4f}' for z in smooth_zeros[:10]]}")
print(f"Last 5: {[f'{z:.4f}' for z in smooth_zeros[-5:]]}")

# Also save the derivative values at smooth zeros for Part 2
derivs = [N_smooth_deriv(t) for t in smooth_zeros]
with open('smooth_derivs.json', 'w') as f:
    json.dump(derivs, f)

print(f"\nN_smooth'(t) at first 5 smooth zeros: {[f'{d:.6f}' for d in derivs[:5]]}")
