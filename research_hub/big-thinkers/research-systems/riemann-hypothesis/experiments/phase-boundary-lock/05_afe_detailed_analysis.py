"""
Experiment 5: Detailed Analysis of WHY the AFE Zeros Stay on the Critical Line

The approximate functional equation:
  AFE(s) = sum_{n<=N} n^{-s} + chi(s) * sum_{n<=N} n^{-(1-s)}

has the property AFE(s) = chi(s) * conj(AFE(1-conj(s))) when combined with
the chi-symmetry.

This experiment investigates:
1. WHY AFE zeros stay on sigma=1/2 while Dirichlet polynomial zeros don't
2. Whether this is exact or approximate
3. The mechanism: does the chi(s) factor "pull" zeros to the line?
"""

import numpy as np
from mpmath import mp, mpf, mpc, gamma, pi, zeta, findroot, fabs, log, zetazero

mp.dps = 30

def chi_func(s):
    """chi(s) = pi^{s-1/2} Gamma((1-s)/2) / Gamma(s/2)"""
    return pi**(s - mpf('0.5')) * gamma((1-s)/2) / gamma(s/2)

def dirichlet_poly(s, N):
    return sum(mpf(n)**(-s) for n in range(1, N+1))

def approx_func_eq(s, N):
    sum1 = sum(mpf(n)**(-s) for n in range(1, N+1))
    sum2 = sum(mpf(n)**(-(1-s)) for n in range(1, N+1))
    return sum1 + chi_func(s) * sum2

# ============================================================
# Part 1: Precision test - are AFE zeros EXACTLY on sigma=1/2?
# ============================================================
print("=" * 70)
print("PART 1: Are AFE zeros EXACTLY on sigma = 1/2?")
print("=" * 70)

mp.dps = 50  # High precision
print(f"\nUsing {mp.dps} decimal digits of precision\n")

for N in [10, 20, 50]:
    print(f"N = {N}:")
    afe = lambda s, N=N: approx_func_eq(s, N)
    
    for k in range(1, 6):
        t0 = float(zetazero(k).imag)
        try:
            z = findroot(afe, mpc('0.5', t0), tol=mpf('1e-40'))
            sigma = z.real
            t = z.imag
            dev = fabs(sigma - mpf('0.5'))
            print(f"  Zero #{k}: sigma = {float(sigma):.30f}, |sigma-0.5| = {float(dev):.2e}")
        except:
            print(f"  Zero #{k}: not found near t={t0:.3f}")
    print()

mp.dps = 30

# ============================================================
# Part 2: The symmetry structure of AFE
# ============================================================
print("=" * 70)
print("PART 2: Symmetry Structure of the AFE")
print("=" * 70)

# The AFE satisfies an approximate functional equation:
# AFE(s) = D_N(s) + chi(s) * D_N(1-s)
# 
# This means:
# AFE(s) / chi(s) = D_N(s)/chi(s) + D_N(1-s)
#
# And: chi(s) * AFE(1-s) = chi(s) * [D_N(1-s) + chi(1-s)*D_N(s)]
#                         = chi(s)*D_N(1-s) + chi(s)*chi(1-s)*D_N(s)
#
# Using chi(s)*chi(1-s) = 1:
# chi(s) * AFE(1-s) = chi(s)*D_N(1-s) + D_N(s) = AFE(s)
#
# So: AFE(s) = chi(s) * AFE(1-s)  EXACTLY!

print("\nVerification: AFE(s) = chi(s) * AFE(1-s)?")
print("Using chi(s)*chi(1-s) = 1")
print()

N = 20
for t_val in [14.13, 25.01, 50.0]:
    for sigma in [0.5, 0.6, 0.7, 0.8]:
        s = mpc(sigma, t_val)
        afe_s = approx_func_eq(s, N)
        afe_1ms = approx_func_eq(1-s, N)
        chi_s = chi_func(s)
        lhs = afe_s
        rhs = chi_s * afe_1ms
        rel_err = fabs(lhs - rhs) / max(fabs(lhs), mpf('1e-30'))
        print(f"  s = {sigma:.1f}+{t_val:.2f}i: |AFE(s) - chi(s)*AFE(1-s)| / |AFE(s)| = {float(rel_err):.2e}")

# Also verify chi(s)*chi(1-s) = 1
print("\nVerification: chi(s)*chi(1-s) = 1?")
for t_val in [14.13, 25.01, 100.0]:
    for sigma in [0.5, 0.6, 0.8]:
        s = mpc(sigma, t_val)
        prod = chi_func(s) * chi_func(1-s)
        print(f"  s = {sigma}+{t_val}i: chi(s)*chi(1-s) = {float(fabs(prod)):.15f}")

# ============================================================
# Part 3: WHY does the exact functional equation force zeros to sigma=1/2?
# ============================================================
print("\n" + "=" * 70)
print("PART 3: Why the Functional Equation Forces Zeros Near sigma=1/2")
print("=" * 70)

print("""
THEOREM: The AFE satisfies AFE(s) = chi(s) * AFE(1-s) EXACTLY.

Proof: AFE(s) = D_N(s) + chi(s)*D_N(1-s)
       chi(s) * AFE(1-s) = chi(s)*[D_N(1-s) + chi(1-s)*D_N(s)]
                         = chi(s)*D_N(1-s) + chi(s)*chi(1-s)*D_N(s)
                         = chi(s)*D_N(1-s) + D_N(s)    [using chi(s)*chi(1-s)=1]
                         = AFE(s)                        QED

CONSEQUENCE: If AFE(s_0) = 0, then chi(s_0) * AFE(1-s_0) = 0.
Since chi(s_0) != 0 in the critical strip, AFE(1-s_0) = 0.

So if sigma_0 + it_0 is a zero, then (1-sigma_0) + it_0 is also a zero.
This is NECESSARY but NOT SUFFICIENT to force zeros to sigma = 1/2.
(Pairs of off-line zeros (sigma_0, 1-sigma_0) are still allowed.)

The additional mechanism: the AFE is the SUM of D_N(s) and chi(s)*D_N(1-s).
For the AFE to vanish:
  D_N(s) = -chi(s) * D_N(1-s)
  |D_N(s)| = |chi(s)| * |D_N(1-s)|

On the critical line sigma=1/2: |chi(1/2+it)| = 1, so |D_N(1/2+it)| = |D_N(1/2-it)|.
This is automatically satisfied since D_N(1-s)|_{s=1/2+it} = D_N(1/2-it) = conj(D_N(1/2+it)).

Off the critical line: |chi(sigma+it)| = (t/2pi)^{1/2-sigma} * (1+O(1/t)) for large t.
For sigma > 1/2: |chi| < 1, so |D_N(s)| < |D_N(1-s)| is required for a zero.
But for sigma > 1/2 and 1-sigma < 1/2: D_N(s) CONVERGES while D_N(1-s) OSCILLATES more.
""")

# ============================================================
# Part 4: The |chi| factor as "force field"
# ============================================================
print("=" * 70)
print("PART 4: |chi(sigma+it)| as the Zero-Attracting Force Field")
print("=" * 70)

print("\n|chi(sigma+it)| for various sigma and t:")
print(f"\n{'t':>8} | {'sigma=0.45':>12} | {'sigma=0.50':>12} | {'sigma=0.55':>12} | {'sigma=0.60':>12} | {'sigma=0.70':>12}")
print("-" * 72)

for t in [14.13, 25.01, 50.0, 100.0, 1000.0]:
    vals = []
    for sigma in [0.45, 0.50, 0.55, 0.60, 0.70]:
        c = chi_func(mpc(sigma, t))
        vals.append(float(fabs(c)))
    print(f"{t:>8.1f} | {'  |  '.join(f'{v:>8.4f}' for v in vals)}")

print("""
KEY OBSERVATION: |chi(1/2+it)| = 1 exactly, while |chi(sigma+it)| ~ (t/2pi)^{1/2-sigma}.

For sigma > 1/2: |chi| < 1 and DECREASING with t. This means the "reflected" 
contribution chi(s)*D_N(1-s) is SUPPRESSED compared to D_N(s) for large t.
For the sum to vanish, D_N(s) would need to nearly cancel chi(s)*D_N(1-s),
which becomes increasingly unlikely as |chi| deviates from 1.

For sigma = 1/2: |chi| = 1 exactly. The two contributions have EQUAL weight.
Cancellation is natural -- it happens whenever D_N(1/2+it) and the reflected 
term have opposite phases.

THIS is the "phase-boundary lock" mechanism:
- At sigma = 1/2: the two halves of the AFE have equal amplitude. Zeros form
  easily through phase cancellation.
- At sigma != 1/2: the amplitudes are MISMATCHED by factor |chi| != 1.
  Perfect cancellation is much harder.
- As t grows, the mismatch for sigma != 1/2 grows WITHOUT bound (like t^{|sigma-1/2|}).
  This creates an increasingly strong "force" pushing zeros toward sigma = 1/2.
""")

# ============================================================
# Part 5: Quantitative verification
# ============================================================
print("=" * 70)
print("PART 5: Quantitative Test -- How Hard is Cancellation off the Line?")
print("=" * 70)

# For a zero at sigma+it, we need: D_N(s) = -chi(s)*D_N(1-s)
# Equivalently: |D_N(s)/D_N(1-s)| = |chi(s)|
# 
# Measure the typical ratio |D_N(sigma+it)/D_N(1-sigma+it)| and compare to |chi(sigma+it)|

N = 50
print(f"\nN = {N}")
print(f"\nFor random t values, compare:")
print(f"  A = |D_N(sigma+it)/D_N(1-sigma+it)|  (the actual ratio)")
print(f"  B = |chi(sigma+it)|                    (the REQUIRED ratio for a zero)")
print()

np.random.seed(42)
t_samples = np.random.uniform(50, 500, 20)

for sigma in [0.55, 0.60, 0.70]:
    matches = 0
    near_matches = 0
    total = len(t_samples)
    
    for t in t_samples:
        s = mpc(sigma, t)
        d_s = dirichlet_poly(s, N)
        d_1ms = dirichlet_poly(1-s, N)
        actual_ratio = float(fabs(d_s / d_1ms))
        required_ratio = float(fabs(chi_func(s)))
        
        rel_diff = abs(actual_ratio - required_ratio) / required_ratio
        if rel_diff < 0.01:
            matches += 1
        if rel_diff < 0.1:
            near_matches += 1
    
    print(f"sigma = {sigma:.2f}: exact matches (<1%): {matches}/{total}, near matches (<10%): {near_matches}/{total}")

# Now do sigma = 0.50
sigma = 0.50
matches = 0
for t in t_samples:
    s = mpc(sigma, t)
    d_s = dirichlet_poly(s, N)
    d_1ms = dirichlet_poly(1-s, N)
    actual_ratio = float(fabs(d_s / d_1ms))
    required_ratio = float(fabs(chi_func(s)))
    rel_diff = abs(actual_ratio - required_ratio) / max(required_ratio, 1e-15)
    if rel_diff < 0.01:
        matches += 1
print(f"sigma = 0.50: |D_N(s)/D_N(1-s)| = 1 = |chi| automatically: {matches}/{total} match")

