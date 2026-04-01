"""Verify the explicit formula by comparing to direct computation of N_osc"""
import mpmath
import numpy as np
from sympy import primerange
import json

mpmath.mp.dps = 30

# Load smooth zeros
with open('smooth_zeros.json') as f:
    smooth_zeros = json.load(f)

# The EXACT oscillatory part is:
# N_osc(T) = (1/pi) * Im(ln(zeta(1/2 + iT)))
# Note: different references use different sign conventions. Let's compute directly.

print("=== Direct computation of N_osc vs prime sum ===\n")

# Test at first 10 smooth zeros
for i in range(10):
    T = smooth_zeros[i]
    s = mpmath.mpc(0.5, T)

    # Direct: arg(zeta(1/2+iT)) - careful with branch cuts
    z = mpmath.zeta(s)
    arg_z = float(mpmath.arg(z))
    # N_osc = (1/pi) * Im(ln(zeta(1/2+iT)))
    # But we need to be careful: Im(ln(z)) = arg(z) only up to branch cuts
    N_osc_direct = (1.0/np.pi) * arg_z

    # Prime sum WITHOUT ln(p): N_osc = -(1/pi) * sum (1/(m*p^{m/2})) * sin(mT*ln(p))
    primes = list(primerange(2, 10001))
    N_osc_no_lnp = 0
    for p in primes:
        lp = np.log(p)
        for m in range(1, 6):
            N_osc_no_lnp += -(1.0/np.pi) * (1.0/(m * p**(m/2.0))) * np.sin(m * T * lp)

    # Prime sum WITH ln(p) (as in GOAL.md): N_osc = -(1/pi) * sum (ln(p)/(m*p^{m/2})) * sin(mT*ln(p))
    N_osc_with_lnp = 0
    for p in primes:
        lp = np.log(p)
        for m in range(1, 6):
            N_osc_with_lnp += -(1.0/np.pi) * (lp/(m * p**(m/2.0))) * np.sin(m * T * lp)

    print(f"n={i+1}, T_smooth={T:.4f}")
    print(f"  N_osc (direct via mpmath):    {N_osc_direct:+.6f}")
    print(f"  N_osc (prime sum, NO ln(p)):  {N_osc_no_lnp:+.6f}")
    print(f"  N_osc (prime sum, WITH ln(p)):{N_osc_with_lnp:+.6f}")
    print()
