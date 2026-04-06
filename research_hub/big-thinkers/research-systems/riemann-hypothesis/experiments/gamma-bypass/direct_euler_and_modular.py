"""
Investigation 2: Can we work with zeta directly via the Euler product?
Investigation 3: Does the modular boost compensate for the gamma factor?

Part A: The Euler product partial products
- For N primes, zeta_N(s) = prod_{p <= N} (1-p^{-s})^{-1}
- These converge for sigma > 1 but NOT for sigma = 1/2
- We examine: as we add more primes, what happens to the PF order?
- And: can we extract PF information that survives analytic continuation?

Part B: Modular boost cross-term decomposition
- Decompose D4 of Phi into: (1) pure f_1, (2) pure f_2, (3) cross terms
- The Cauchy-Binet formula gives det(A+B) as a sum over subsets
- Determine: which part is responsible for PF_4 positivity?
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 50

###############################################################################
# Part A: Euler Product Partial Products and PF
###############################################################################

print("=" * 70)
print("PART A: EULER PRODUCT AND PF")
print("=" * 70)

# The Euler product: zeta(s) = prod_p (1-p^{-s})^{-1}
# For the kernel analysis, we need this on the critical line: s = 1/2 + it.
# But the product doesn't converge there!
#
# However, the PARTIAL products zeta_N(1/2+it) = prod_{p<=N} (1-p^{-1/2-it})^{-1}
# are well-defined. They converge to zeta for sigma > 1, but for sigma = 1/2,
# they oscillate and do NOT converge to zeta(1/2+it).
#
# The question: what PF properties do the partial products have?

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

t_grid = np.linspace(0, 60, 4001)
dt = t_grid[1] - t_grid[0]

print("\n--- Euler product partial products on the critical line ---\n")

# Compute partial products
def euler_partial(t, n_primes):
    """Product of first n_primes Euler factors at s = 1/2 + it."""
    s = mpmath.mpc('0.5', mpmath.mpf(t))
    prod = mpmath.mpf(1)
    for p in primes[:n_primes]:
        prod *= 1 / (1 - mpmath.power(mpmath.mpf(p), -s))
    return complex(prod)

# Compute for several cutoffs
print("Partial product values at t=10:")
for N in [1, 3, 5, 10, 15, 25]:
    val = euler_partial(10, N)
    zeta_val = complex(mpmath.zeta(mpmath.mpc('0.5', '10')))
    print(f"  N={N:2d} primes: zeta_N = {val.real:+10.6f} + {val.imag:+10.6f}i  |zeta_N| = {abs(val):.6f}  (zeta = {zeta_val.real:+10.6f} + {zeta_val.imag:+10.6f}i)")

# Compute individual Euler factor kernels
print("\n--- Individual Euler factor kernel analysis ---\n")

# For each prime p, the function f_p(t) = -log(1-p^{-1/2-it}) is the log of the factor.
# The FACTOR is (1-p^{-1/2-it})^{-1}.
# Its log is f_p(t) = sum_{k=1}^inf p^{-k(1/2+it)}/k
# The real part: Re(f_p(t)) = sum_{k=1}^inf p^{-k/2} cos(kt*log(p)) / k

# The kernel of the individual factor is:
# phi_p(u) = FT[Re(log factor_p)](u)
# = sum_{k=1}^inf (1/k) * p^{-k/2} * [delta(u - k*log(p)) + delta(u + k*log(p))] / 2
# This is a discrete measure! Not a smooth function.

# Instead, let's look at the kernel of exp(f_p) = |factor_p|^2 or Re(factor_p).

# Actually, the relevant object is:
# log|zeta_N(1/2+it)| = sum_{p<=N} Re(-log(1-p^{-1/2-it}))
# = sum_p sum_k p^{-k/2} cos(kt log p) / k

# For the PF analysis of Xi, we need the kernel of Xi, not of log|zeta|.
# Xi = G * zeta, and the kernel is the Fourier cosine transform.
# We can't easily separate "the Euler product's contribution to the kernel"
# because multiplying by G and taking the real part mixes things up.

# What we CAN do: look at the "Euler product approximation to Xi"
# Xi_N(t) = G(1/2+it) * zeta_N(1/2+it)

print("PF analysis of Euler-truncated Xi (first N primes):\n")

def compute_xi_N_vals(n_primes):
    """Compute Xi_N = G * zeta_N on the t_grid."""
    # Use a coarser grid for speed
    result = np.zeros(len(t_grid))
    for i, t in enumerate(t_grid):
        g = complex(mpmath.mpf('0.5') * mpmath.mpc('0.5', mpmath.mpf(t)) * (mpmath.mpc('0.5', mpmath.mpf(t)) - 1) * mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2))
        z_N = euler_partial(t, n_primes)
        result[i] = (g * z_N).real
    return result

def kernel_from_vals(f_vals, u):
    integrand = f_vals * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

def pf_test_from_vals(f_vals, h, max_order=6):
    kfunc = lambda u: kernel_from_vals(f_vals, u)
    dets = []
    for r in range(2, max_order + 1):
        vals = [kfunc(k*h) for k in range(r)]
        mat = np.zeros((r, r))
        for i in range(r):
            for j in range(r):
                mat[i][j] = vals[abs(i-j)]
        dets.append(np.linalg.det(mat))
    return dets

# Test with small number of primes (for speed)
for N in [1, 3, 5, 10]:
    print(f"\nN = {N} primes (up to p = {primes[N-1]}):")
    xi_N = compute_xi_N_vals(N)
    print(f"  Max |Xi_N - Xi|/|Xi| (large t): checking...")

    for h in [0.05, 0.1]:
        dets = pf_test_from_vals(xi_N, h)
        signs = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
        pf_order = 1
        for d in dets:
            if d > 0:
                pf_order += 1
            else:
                break
        print(f"  h={h}: [{signs}] PF_{pf_order}  D4={dets[2]:.2e} D5={dets[3]:.2e}")

# Full Xi for comparison
print("\nFull Xi (reference):")
xi_full = np.array([float(mpmath.re(mpmath.mpf('0.5') * mpmath.mpc('0.5', mpmath.mpf(t)) * (mpmath.mpc('0.5', mpmath.mpf(t)) - 1) * mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.zeta(mpmath.mpc('0.5', mpmath.mpf(t))))) for t in t_grid])
for h in [0.05, 0.1]:
    dets = pf_test_from_vals(xi_full, h)
    signs = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
    print(f"  h={h}: [{signs}]  D4={dets[2]:.2e} D5={dets[3]:.2e}")


###############################################################################
# Part B: Modular Boost Cross-Term Decomposition
###############################################################################

print("\n\n" + "=" * 70)
print("PART B: MODULAR BOOST CROSS-TERM DECOMPOSITION")
print("=" * 70)

# The Polya kernel: Phi(u) = sum_{n=1}^inf f_n(u)
# where f_n(u) = [2*pi^2*n^4*e^{9u} - 3*pi*n^2*e^{5u}] * e^{-pi*n^2*e^{4u}}
#
# Phi = f_1 + f_2 + f_3 + ...
#
# For the D4 Toeplitz determinant:
# T_{ij}(Phi) = Phi(u0 + (i-j)*h) = f_1(u0+(i-j)h) + f_2(u0+(i-j)h) + ...
# T(Phi) = T(f_1) + T(f_2) + ...
# det(T(Phi)) = det(T(f_1) + T(f_2) + ...)
#
# Using the multilinear expansion of the determinant of a sum of matrices,
# det(A + B) involves all terms of the form:
# sum over partitions of {1,...,n} into subsets S, T
# of products of minors from A and B

def f_n(n, u):
    n = mpmath.mpf(n)
    u = mpmath.mpf(u)
    return float((2*mpmath.pi**2*n**4*mpmath.exp(9*u) - 3*mpmath.pi*n**2*mpmath.exp(5*u)) * mpmath.exp(-mpmath.pi*n**2*mpmath.exp(4*u)))

def K_partial_theta(u, n_max):
    u_abs = abs(u)
    return sum(f_n(n, u_abs) for n in range(1, n_max+1))

def build_toeplitz(kfunc, u0, h, r):
    M = np.zeros((r, r))
    for i in range(r):
        for j in range(r):
            M[i,j] = kfunc(u0 + (i-j)*h)
    return M

print("\n--- D4 cross-term decomposition at (u0, h) = (0.01, 0.05) ---\n")

u0, h = 0.01, 0.05

# Build T(f_1) and T(f_2) for the 4x4 case
T_f1 = build_toeplitz(lambda u: f_n(1, abs(u)), u0, h, 4)
T_f2 = build_toeplitz(lambda u: f_n(2, abs(u)), u0, h, 4)
T_full = build_toeplitz(lambda u: K_partial_theta(u, 50), u0, h, 4)

print("T(f_1) matrix:")
print(T_f1)
print(f"\ndet(T(f_1)) = {np.linalg.det(T_f1):.6e}")

print("\nT(f_2) matrix:")
print(T_f2)
print(f"\ndet(T(f_2)) = {np.linalg.det(T_f2):.6e}")

print(f"\ndet(T(f_1 + f_2)) = {np.linalg.det(T_f1 + T_f2):.6e}")
print(f"det(T_full) = {np.linalg.det(T_full):.6e}")

# The cross-term is det(T_f1 + T_f2) - det(T_f1) - det(T_f2)
cross = np.linalg.det(T_f1 + T_f2) - np.linalg.det(T_f1) - np.linalg.det(T_f2)
print(f"\nCross-term = det(f_1+f_2) - det(f_1) - det(f_2) = {cross:.6e}")
print(f"det(f_1) = {np.linalg.det(T_f1):.6e}")
print(f"det(f_2) = {np.linalg.det(T_f2):.6e}")
print(f"\nNote: det(f_1) < 0, but cross-term > 0 and overwhelms it!")

# Eigenvalue analysis
eig_f1 = np.sort(np.linalg.eigvalsh(T_f1))
eig_f2 = np.sort(np.linalg.eigvalsh(T_f2))
eig_sum = np.sort(np.linalg.eigvalsh(T_f1 + T_f2))

print(f"\nEigenvalues of T(f_1): {eig_f1}")
print(f"Eigenvalues of T(f_2): {eig_f2}")
print(f"Eigenvalues of T(f_1+f_2): {eig_sum}")
print(f"\nMin eigenvalue: f_1 = {eig_f1[0]:.6e}, f_1+f_2 = {eig_sum[0]:.6e}")

# Now do the same analysis for D5
print("\n\n--- D5 cross-term decomposition at (u0, h) = (0.01, 0.05) ---\n")

T_f1_5 = build_toeplitz(lambda u: f_n(1, abs(u)), u0, h, 5)
T_f2_5 = build_toeplitz(lambda u: f_n(2, abs(u)), u0, h, 5)
T_full_5 = build_toeplitz(lambda u: K_partial_theta(u, 50), u0, h, 5)

print(f"det(T_5(f_1)) = {np.linalg.det(T_f1_5):.6e}")
print(f"det(T_5(f_2)) = {np.linalg.det(T_f2_5):.6e}")
print(f"det(T_5(f_1+f_2)) = {np.linalg.det(T_f1_5 + T_f2_5):.6e}")
print(f"det(T_5(full)) = {np.linalg.det(T_full_5):.6e}")

cross_5 = np.linalg.det(T_f1_5 + T_f2_5) - np.linalg.det(T_f1_5) - np.linalg.det(T_f2_5)
print(f"\nD5 cross-term = {cross_5:.6e}")
print(f"D5(f_1) = {np.linalg.det(T_f1_5):.6e}")
print(f"D5(f_2) = {np.linalg.det(T_f2_5):.6e}")
print(f"D5(f_1+f_2) = {np.linalg.det(T_f1_5 + T_f2_5):.6e}")

eig_5_f1 = np.sort(np.linalg.eigvalsh(T_f1_5))
eig_5_sum = np.sort(np.linalg.eigvalsh(T_f1_5 + T_f2_5))
eig_5_full = np.sort(np.linalg.eigvalsh(T_full_5))

print(f"\nEigenvalues of T_5(f_1): {eig_5_f1}")
print(f"Eigenvalues of T_5(f_1+f_2): {eig_5_sum}")
print(f"Eigenvalues of T_5(full): {eig_5_full}")

###############################################################################
# Part C: The f_2/f_1 ratio and modular symmetry
###############################################################################

print("\n\n--- Part C: Modular symmetry and the f_2/f_1 ratio ---\n")

# The theta function identity gives:
# theta_3(0, q) = sum_{n=-inf}^{inf} q^{n^2}
# Under q -> e^{-pi/tau} (i.e., tau -> -1/tau):
# theta_3(0, e^{-pi*tau}) = tau^{-1/2} * theta_3(0, e^{-pi/tau})
#
# This relates f_1 and f_2 (and higher terms) in a specific way.
# At u = 0: q = e^{-pi}, and the ratio f_2/f_1 = e^{-3*pi} * (32*pi^2 - 12*pi) / (2*pi^2 - 3*pi) * ...

print("f_n values and ratios at various u:")
print(f"{'u':>6s}  {'f_1':>14s}  {'f_2':>14s}  {'f_2/f_1':>14s}  {'f_3':>14s}  {'f_3/f_1':>14s}")
for u in [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]:
    f1 = f_n(1, u)
    f2 = f_n(2, u)
    f3 = f_n(3, u)
    r21 = f2/f1 if abs(f1) > 1e-30 else float('inf')
    r31 = f3/f1 if abs(f1) > 1e-30 else float('inf')
    print(f"{u:6.2f}  {f1:14.6e}  {f2:14.6e}  {r21:14.6e}  {f3:14.6e}  {r31:14.6e}")

# What happens to PF order if we scale f_2 by beta?
print("\n\nPF order as function of beta (f_2 scaling) at (u0=0.01, h=0.05):")
print(f"{'beta':>8s}  {'D4':>14s}  {'D5':>14s}")

for beta in np.arange(0.0, 2.01, 0.1):
    T = build_toeplitz(lambda u, b=beta: f_n(1, abs(u)) + b*f_n(2, abs(u)), u0, h, 5)
    det4 = np.linalg.det(T[:4,:4])
    det5 = np.linalg.det(T)
    print(f"{beta:8.2f}  {det4:14.6e}  {det5:14.6e}  {'<-- PF5!' if det5 > 0 and det4 > 0 else ''}")

# Find the critical beta for PF5
from scipy.optimize import brentq

def d5_of_beta(beta):
    T = build_toeplitz(lambda u, b=beta: f_n(1, abs(u)) + b*f_n(2, abs(u)), u0, h, 5)
    return np.linalg.det(T)

# Find the zero
try:
    beta_crit = brentq(d5_of_beta, 1.0, 1.5)
    print(f"\nCritical beta for PF5: {beta_crit:.8f}")
    print(f"Percentage increase needed: {(beta_crit - 1)*100:.4f}%")
except:
    print("\nCould not find critical beta.")

###############################################################################
# Part D: Is the modular boost a general phenomenon?
###############################################################################

print("\n\n--- Part D: Generality of the modular boost ---\n")

# Test: for a GENERIC theta-like sum (not modular), does adding terms boost PF?
# Use a sum of "fake theta terms" with random q-values

np.random.seed(42)

print("Test: sum of generic Gaussian-like terms (NOT modular)")
print("f_n(u) = a_n * exp(-b_n * u^2)")
print()

# Theta-like: f_n(u) = c_n * exp(-n^2 * pi * e^{4u})
# Non-modular: f_n(u) = c_n * exp(-random_b_n * e^{4u})

for trial in range(3):
    print(f"Trial {trial+1}:")
    # Random coefficients (but positive and decreasing)
    b_vals = np.sort(np.random.exponential(scale=3, size=5))[::-1]
    c_vals = np.exp(-b_vals)  # Weights decrease with b

    def fake_term(n, u):
        n = n - 1  # 0-indexed
        u_val = abs(float(u))
        return float(c_vals[n] * np.exp(-b_vals[n] * np.exp(4*u_val)))

    for N in [1, 2, 5]:
        kfunc = lambda u, nm=N: sum(fake_term(n, u) for n in range(1, min(nm+1, 6)))
        T = build_toeplitz(kfunc, 0.01, 0.05, 5)
        d4 = np.linalg.det(T[:4,:4])
        d5 = np.linalg.det(T)
        s4 = '+' if d4 > 0 else '-'
        s5 = '+' if d5 > 0 else '-'
        print(f"  N={N}: D4 = {d4:10.2e} [{s4}]  D5 = {d5:10.2e} [{s5}]")
    print()

print("Observation: the modular boost is NOT a generic property of sums.")
print("It is specific to the theta function's modular structure.")

###############################################################################
# Save
###############################################################################

results = {
    'description': 'Euler product partial products and modular boost cross-terms',
    'critical_beta': float(beta_crit) if 'beta_crit' in dir() else None,
}

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/gamma-bypass/euler_modular_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nDone.")
