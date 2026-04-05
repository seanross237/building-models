"""
Experiment 6: Does the AFE have ANY off-line zeros?

Critical question: We showed AFE zeros near known zeta zeros are on sigma=1/2.
But the AFE is not the same function as zeta. Does it have ADDITIONAL zeros
that might be off the critical line?

The AFE(s,N) = D_N(s) + chi(s)*D_N(1-s) satisfies the functional equation exactly.
But it's NOT entire (chi has poles/singularities).

We do a BROAD zero search in the critical strip to find ALL zeros.
"""

import numpy as np
from mpmath import mp, mpf, mpc, gamma, pi, zeta, findroot, fabs

mp.dps = 25

def chi_func(s):
    return pi**(s - mpf('0.5')) * gamma((1-s)/2) / gamma(s/2)

def approx_func_eq(s, N):
    sum1 = sum(mpf(n)**(-s) for n in range(1, N+1))
    sum2 = sum(mpf(n)**(-(1-s)) for n in range(1, N+1))
    return sum1 + chi_func(s) * sum2

# ============================================================
# Broad zero search for AFE_20
# ============================================================
N = 20

print("=" * 70)
print(f"BROAD ZERO SEARCH for AFE_{N}")
print("=" * 70)
print(f"\nSearching in sigma in [0.0, 1.0], t in [5, 80]")
print("Grid: 50 x 200 points, Newton refinement from each cell\n")

# Search grid
sigma_vals = np.linspace(0.01, 0.99, 50)
t_vals = np.linspace(5, 80, 200)

afe_func = lambda s: approx_func_eq(s, N)

# Evaluate on grid
print("Evaluating AFE on grid...")
grid_vals = np.zeros((len(sigma_vals), len(t_vals)), dtype=complex)
for i, sig in enumerate(sigma_vals):
    for j, t in enumerate(t_vals):
        s = mpc(sig, t)
        v = afe_func(s)
        grid_vals[i,j] = complex(v)

# Find candidate zeros: cells where |AFE| has a local minimum
print("Searching for zero candidates...")
all_zeros = []

for i in range(len(sigma_vals)-1):
    for j in range(len(t_vals)-1):
        mags = [abs(grid_vals[i,j]), abs(grid_vals[i+1,j]), 
                abs(grid_vals[i,j+1]), abs(grid_vals[i+1,j+1])]
        min_mag = min(mags)
        max_mag = max(mags)
        
        # Liberal threshold for potential zeros
        if min_mag < 2.0 and min_mag < 0.3 * max_mag:
            s0 = mpc((sigma_vals[i]+sigma_vals[i+1])/2, (t_vals[j]+t_vals[j+1])/2)
            try:
                z = findroot(afe_func, s0, tol=1e-15)
                if fabs(afe_func(z)) < 1e-10:
                    sig_z = float(z.real)
                    t_z = float(z.imag)
                    if 0 < sig_z < 1 and 4 < t_z < 81:
                        # Check for duplicates
                        is_dup = False
                        for ez in all_zeros:
                            if abs(complex(z) - complex(ez)) < 0.1:
                                is_dup = True
                                break
                        if not is_dup:
                            all_zeros.append(z)
            except:
                pass

all_zeros.sort(key=lambda z: float(z.imag))

print(f"\nFound {len(all_zeros)} zeros in the critical strip")
print(f"\n{'#':>4} | {'sigma':>10} | {'t':>10} | {'|sigma-0.5|':>12} | {'On line?':>10}")
print("-" * 55)

on_line_count = 0
off_line_count = 0
for k, z in enumerate(all_zeros, 1):
    sig = float(z.real)
    t = float(z.imag)
    dev = abs(sig - 0.5)
    on_line = dev < 1e-6
    if on_line:
        on_line_count += 1
    else:
        off_line_count += 1
    label = "YES" if on_line else f"NO (sigma={sig:.6f})"
    print(f"{k:>4} | {sig:>10.6f} | {t:>10.4f} | {dev:>12.2e} | {label}")

print(f"\nSummary: {on_line_count} zeros on critical line, {off_line_count} zeros OFF critical line")
print(f"Percentage on line: {100*on_line_count/max(len(all_zeros),1):.1f}%")

if off_line_count > 0:
    print("\n*** OFF-LINE ZEROS FOUND! ***")
    print("These are zeros of AFE that are NOT on the critical line.")
    print("This means the functional equation alone is NOT sufficient")
    print("to force ALL zeros onto sigma=1/2.")
else:
    print("\n*** ALL ZEROS ARE ON THE CRITICAL LINE ***")
    print("This is strong evidence that for the AFE, the functional equation")
    print("combined with the Euler-product structure forces zeros to sigma=1/2.")

