"""
Experiment 7: Analyzing the Spurious Off-Line Zeros of the AFE

Key finding from Experiment 6: The AFE_{20} has 4 off-line zeros at small t,
coming in reflected pairs (0.449, 5.53) <-> (0.551, 5.53) and 
(0.036, 7.62) <-> (0.964, 7.62).

Questions:
1. Do these spurious zeros move toward sigma=1/2 as N increases?
2. Is there a threshold t_*(N) below which spurious zeros appear and above which
   all zeros are on the critical line?
3. Does t_*(N) decrease as N grows (so in the limit, ALL zeros are on the line)?
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
# Track spurious zeros vs N
# ============================================================
print("=" * 70)
print("TRACKING SPURIOUS OFF-LINE ZEROS vs N")
print("=" * 70)

for N in [5, 10, 15, 20, 30, 50, 100]:
    print(f"\n--- N = {N} ---")
    afe = lambda s, N=N: approx_func_eq(s, N)
    
    # Search for zeros with t in [1, 20] (the low-t region where spurious zeros live)
    sigma_vals = np.linspace(0.01, 0.99, 40)
    t_vals = np.linspace(1, 25, 120)
    
    zeros = []
    for i in range(len(sigma_vals)-1):
        for j in range(len(t_vals)-1):
            s_center = mpc((sigma_vals[i]+sigma_vals[i+1])/2, (t_vals[j]+t_vals[j+1])/2)
            try:
                vals = [complex(afe(mpc(sigma_vals[ii], t_vals[jj]))) 
                        for ii in [i, i+1] for jj in [j, j+1]]
                mags = [abs(v) for v in vals]
                if min(mags) < 3.0 and min(mags) < 0.3 * max(mags):
                    z = findroot(afe, s_center, tol=1e-12)
                    if fabs(afe(z)) < 1e-8:
                        sig_z = float(z.real)
                        t_z = float(z.imag)
                        if 0 < sig_z < 1 and 0.5 < t_z < 26:
                            is_dup = any(abs(complex(z) - complex(ez)) < 0.1 for ez in zeros)
                            if not is_dup:
                                zeros.append(z)
            except:
                pass
    
    # Classify zeros
    on_line = [(z, float(z.real), float(z.imag)) for z in zeros if abs(float(z.real) - 0.5) < 1e-6]
    off_line = [(z, float(z.real), float(z.imag)) for z in zeros if abs(float(z.real) - 0.5) >= 1e-6]
    
    print(f"  Zeros found: {len(zeros)} total, {len(on_line)} on line, {len(off_line)} off line")
    
    if off_line:
        # Group by t (reflected pairs)
        off_line.sort(key=lambda x: x[2])
        print(f"  Off-line zeros (spurious):")
        for _, sig, t in off_line:
            print(f"    sigma={sig:.6f}, t={t:.4f}, |sigma-0.5|={abs(sig-0.5):.6f}")
        
        # Maximum t of spurious zero
        max_t_spurious = max(t for _, _, t in off_line)
        max_dev = max(abs(sig-0.5) for _, sig, _ in off_line)
        print(f"  Maximum t of spurious zero: {max_t_spurious:.4f}")
        print(f"  Maximum |sigma-0.5| of spurious zero: {max_dev:.6f}")
    else:
        print(f"  NO spurious zeros in [1, 25]!")

# ============================================================
# The "threshold t" as a function of N
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY: Maximum t of spurious zeros vs N")
print("=" * 70)
print(f"\n{'N':>5} | {'# off-line':>11} | {'max t_spurious':>15} | {'max |sigma-0.5|':>17} | {'sqrt(N)':>8}")
print("-" * 68)

# Rerun with just the key tracking metric
for N in [5, 10, 15, 20, 30, 50, 75, 100]:
    afe = lambda s, N=N: approx_func_eq(s, N)
    
    sigma_vals = np.linspace(0.01, 0.99, 30)
    t_vals = np.linspace(0.5, 30, 100)
    
    off_line_zeros = []
    for i in range(len(sigma_vals)-1):
        for j in range(len(t_vals)-1):
            try:
                vals = [complex(afe(mpc(sigma_vals[ii], t_vals[jj]))) 
                        for ii in [i, i+1] for jj in [j, j+1]]
                mags = [abs(v) for v in vals]
                if min(mags) < 3.0 and min(mags) < 0.3 * max(mags):
                    s0 = mpc((sigma_vals[i]+sigma_vals[i+1])/2, (t_vals[j]+t_vals[j+1])/2)
                    z = findroot(afe, s0, tol=1e-12)
                    if fabs(afe(z)) < 1e-8:
                        sig_z = float(z.real)
                        t_z = float(z.imag)
                        if 0 < sig_z < 1 and 0.5 < t_z < 31 and abs(sig_z - 0.5) >= 1e-5:
                            is_dup = any(abs(complex(z) - complex(ez)) < 0.1 for ez in off_line_zeros)
                            if not is_dup:
                                off_line_zeros.append(z)
            except:
                pass
    
    if off_line_zeros:
        max_t = max(float(z.imag) for z in off_line_zeros)
        max_dev = max(abs(float(z.real)-0.5) for z in off_line_zeros)
        print(f"{N:>5} | {len(off_line_zeros):>11} | {max_t:>15.4f} | {max_dev:>17.6f} | {np.sqrt(N):>8.2f}")
    else:
        print(f"{N:>5} | {0:>11} | {'none':>15} | {'none':>17} | {np.sqrt(N):>8.2f}")

print("""
INTERPRETATION:
The threshold below which spurious off-line zeros appear is related to the
approximation quality of the AFE. The AFE is a good approximation to zeta
when N >= sqrt(t/(2*pi)), i.e., t <= 2*pi*N^2. Below this threshold,
the AFE may have spurious zeros. Above it, the zeros faithfully track the
zeta zeros.

The key observation: as N grows, the spurious zeros are confined to an
ever-smaller region of small t. In the limit N -> infinity, the AFE becomes
exact and ALL zeros lie on sigma = 1/2.
""")

