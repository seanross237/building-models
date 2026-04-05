"""
Experiment 1: Zeros of the Approximate Functional Equation vs Plain Dirichlet Polynomials

The approximate functional equation (Hardy-Littlewood):
  zeta(s) ≈ sum_{n<=x} n^{-s} + chi(s) * sum_{n<=y} n^{-(1-s)}
where chi(s) = pi^{s-1/2} * Gamma((1-s)/2) / Gamma(s/2) and xy = t/(2*pi)

This preserves the reflection symmetry. We compare zeros of:
  (A) D_N(s) = sum_{n=1}^N n^{-s}  (plain Dirichlet polynomial)
  (B) AFE_N(s) = sum_{n<=N} n^{-s} + chi(s) * sum_{n<=N} n^{-(1-s)}  (approximate functional equation)

Hypothesis: AFE zeros should cluster more tightly around sigma = 1/2.
"""

import numpy as np
from mpmath import mp, mpf, mpc, gamma, pi, zeta, zetazero, log, sqrt, exp, fabs
from mpmath import findroot, diff
import json

mp.dps = 30

def chi(s):
    """The chi function: chi(s) = pi^{s-1/2} * Gamma((1-s)/2) / Gamma(s/2)"""
    return pi**(s - mpf('0.5')) * gamma((1-s)/2) / gamma(s/2)

def dirichlet_poly(s, N):
    """Plain Dirichlet polynomial D_N(s) = sum_{n=1}^N n^{-s}"""
    return sum(mpf(n)**(-s) for n in range(1, N+1))

def approx_func_eq(s, N=None):
    """
    Approximate functional equation:
    AFE(s) = sum_{n<=x} n^{-s} + chi(s) * sum_{n<=y} n^{-(1-s)}
    
    With x = y = sqrt(t/(2*pi)) when on the critical strip.
    For general s = sigma + it, we use N as the cutoff for both sums.
    """
    if N is None:
        t_val = abs(float(s.imag))
        if t_val > 1:
            N = max(5, int(np.sqrt(t_val / (2*np.pi))) + 1)
        else:
            N = 10
    
    sum1 = sum(mpf(n)**(-s) for n in range(1, N+1))
    sum2 = sum(mpf(n)**(-(1-s)) for n in range(1, N+1))
    return sum1 + chi(s) * sum2

def find_zeros_grid(func, sigma_range, t_range, grid_sigma=50, grid_t=200):
    """Find zeros by grid search + Newton refinement"""
    zeros = []
    sigma_vals = np.linspace(sigma_range[0], sigma_range[1], grid_sigma)
    t_vals = np.linspace(t_range[0], t_range[1], grid_t)
    
    # Evaluate on grid
    vals = np.zeros((grid_sigma, grid_t), dtype=complex)
    for i, sig in enumerate(sigma_vals):
        for j, t in enumerate(t_vals):
            s = mpc(sig, t)
            v = func(s)
            vals[i,j] = complex(v)
    
    # Find sign changes in real and imaginary parts
    for i in range(grid_sigma - 1):
        for j in range(grid_t - 1):
            # Check if magnitude has a local minimum
            mags = [abs(vals[i,j]), abs(vals[i+1,j]), abs(vals[i,j+1]), abs(vals[i+1,j+1])]
            if min(mags) < 0.5 * max(mags):
                # Try Newton's method from center of cell
                s0 = mpc((sigma_vals[i] + sigma_vals[i+1])/2, (t_vals[j] + t_vals[j+1])/2)
                try:
                    z = findroot(func, s0, tol=1e-12)
                    # Check it's actually a zero
                    if fabs(func(z)) < 1e-8:
                        # Check it's in our range
                        if (sigma_range[0] - 0.1 <= float(z.real) <= sigma_range[1] + 0.1 and
                            t_range[0] - 0.5 <= float(z.imag) <= t_range[1] + 0.5):
                            # Check for duplicates
                            is_dup = False
                            for existing in zeros:
                                if abs(complex(z) - complex(existing)) < 0.01:
                                    is_dup = True
                                    break
                            if not is_dup:
                                zeros.append(z)
                except:
                    pass
    
    return sorted(zeros, key=lambda z: float(z.imag))

# ============================================================
# Experiment: Compare zeros for various N values
# ============================================================

print("=" * 70)
print("EXPERIMENT 1: Approximate Functional Equation vs Dirichlet Polynomial Zeros")
print("=" * 70)

# Known first few zeta zeros for reference
known_zeros = []
for k in range(1, 11):
    z = zetazero(k)
    known_zeros.append(z)
    print(f"Zeta zero #{k}: {float(z.real):.6f} + {float(z.imag):.6f}i")

print()

# For each N, find zeros of both D_N and AFE_N near the first few zeta zeros
results = {}

for N in [10, 20, 50, 100]:
    print(f"\n{'='*50}")
    print(f"N = {N}")
    print(f"{'='*50}")
    
    dp_func = lambda s, N=N: dirichlet_poly(s, N)
    afe_func = lambda s, N=N: approx_func_eq(s, N)
    
    dp_zero_sigmas = []
    afe_zero_sigmas = []
    
    # For each known zeta zero, try to find nearby zeros of D_N and AFE_N
    for k, zz in enumerate(known_zeros[:5], 1):
        t0 = float(zz.imag)
        
        # Find Dirichlet polynomial zero near this t
        try:
            dp_z = findroot(dp_func, mpc(0.5, t0), tol=1e-12)
            dp_sigma = float(dp_z.real)
            dp_t = float(dp_z.imag)
            dp_zero_sigmas.append(dp_sigma)
            dp_status = f"sigma={dp_sigma:.4f}, t={dp_t:.4f}"
        except:
            dp_status = "not found"
            dp_sigma = None
        
        # Find AFE zero near this t
        try:
            afe_z = findroot(afe_func, mpc(0.5, t0), tol=1e-12)
            afe_sigma = float(afe_z.real)
            afe_t = float(afe_z.imag)
            afe_zero_sigmas.append(afe_sigma)
            afe_status = f"sigma={afe_sigma:.4f}, t={afe_t:.4f}"
        except:
            afe_status = "not found"
            afe_sigma = None
        
        print(f"\nZeta zero #{k} (t={t0:.4f}):")
        print(f"  Dirichlet D_{N}: {dp_status}")
        print(f"  AFE_{N}:         {afe_status}")
        if dp_sigma is not None and afe_sigma is not None:
            print(f"  |sigma_DP - 0.5| = {abs(dp_sigma - 0.5):.6f}")
            print(f"  |sigma_AFE - 0.5| = {abs(afe_sigma - 0.5):.6f}")
            if abs(afe_sigma - 0.5) < abs(dp_sigma - 0.5):
                print(f"  AFE is CLOSER to critical line by factor {abs(dp_sigma-0.5)/max(abs(afe_sigma-0.5), 1e-15):.2f}x")
            else:
                print(f"  Dirichlet is closer (or equal)")
    
    if dp_zero_sigmas:
        dp_mean_dev = np.mean([abs(s - 0.5) for s in dp_zero_sigmas])
        print(f"\nDirichlet mean |sigma - 0.5|: {dp_mean_dev:.6f}")
    if afe_zero_sigmas:
        afe_mean_dev = np.mean([abs(s - 0.5) for s in afe_zero_sigmas])
        print(f"AFE mean |sigma - 0.5|: {afe_mean_dev:.6f}")
    
    results[N] = {
        'dp_sigmas': dp_zero_sigmas,
        'afe_sigmas': afe_zero_sigmas,
        'dp_mean_dev': float(dp_mean_dev) if dp_zero_sigmas else None,
        'afe_mean_dev': float(afe_mean_dev) if afe_zero_sigmas else None
    }

print("\n\n" + "="*70)
print("SUMMARY TABLE")
print("="*70)
print(f"{'N':>5} | {'D_N mean |σ-½|':>18} | {'AFE_N mean |σ-½|':>18} | {'Ratio DP/AFE':>14}")
print("-" * 65)
for N in sorted(results.keys()):
    r = results[N]
    if r['dp_mean_dev'] is not None and r['afe_mean_dev'] is not None:
        ratio = r['dp_mean_dev'] / max(r['afe_mean_dev'], 1e-15)
        print(f"{N:>5} | {r['dp_mean_dev']:>18.6f} | {r['afe_mean_dev']:>18.6f} | {ratio:>14.2f}")

