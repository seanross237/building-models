"""
Prime-by-prime PF decomposition analysis.

For zeta(s) = prod_p (1-p^{-s})^{-1}, the Xi function factorizes (in a certain sense)
over primes. We investigate whether the PF properties of the total kernel Phi
can be understood as arising from PF properties of individual Euler factor contributions.

Key idea: log zeta(s) = sum_p (-log(1 - p^{-s}))
So in some sense the "kernel" of zeta in the Fourier domain is a CONVOLUTION
of individual prime contributions. Since convolution of PF_infinity functions
preserves PF_infinity, if each prime contribution is PF_infinity, so is the total.

But the gamma factors and the s(s-1) prefactor break this simple picture.
"""

import mpmath
import numpy as np
import json

mpmath.mp.dps = 30

###############################################################################
# 1. Individual Euler factor contribution
###############################################################################

def euler_factor_log(p, s):
    """log((1-p^{-s})^{-1}) = -log(1-p^{-s})"""
    return -mpmath.log(1 - mpmath.power(p, -s))

def euler_factor_on_critical_line(p, t):
    """Evaluate -log(1 - p^{-1/2-it}) for real t"""
    s = mpmath.mpc(0.5, t)
    return euler_factor_log(p, s)

# Primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

###############################################################################
# 2. Contribution of each prime to Re(log zeta) on the critical line
###############################################################################

print("=== Individual prime contributions to Re(log zeta(1/2+it)) ===\n")

t_values = np.linspace(1, 50, 100)

# For each prime, compute the variance of its contribution over t
print("Prime contributions to variance of log|zeta(1/2+it)|:")
print(f"{'p':>4s}  {'Mean Re':>10s}  {'Var Re':>10s}  {'Mean |contrib|':>14s}")
print("-" * 50)

prime_variances = []
for p in primes[:15]:
    re_contribs = []
    for t in t_values:
        val = euler_factor_on_critical_line(p, t)
        re_contribs.append(float(mpmath.re(val)))

    mean_re = np.mean(re_contribs)
    var_re = np.var(re_contribs)
    mean_abs = np.mean(np.abs(re_contribs))
    prime_variances.append((p, var_re))
    print(f"{p:4d}  {mean_re:10.6f}  {var_re:10.6f}  {mean_abs:14.6f}")

###############################################################################
# 3. Independence test: cross-correlations between prime contributions
###############################################################################

print("\n=== Cross-correlations between prime contributions ===")
print("(If primes contribute independently, cross-correlations should be ~0)\n")

# Compute correlations between the contributions of different primes
prime_series = {}
for p in primes[:10]:
    series = []
    for t in t_values:
        val = euler_factor_on_critical_line(p, t)
        series.append(float(mpmath.re(val)))
    prime_series[p] = np.array(series)

# Compute correlation matrix
print(f"{'p1':>4s} {'p2':>4s}  {'Corr':>10s}")
print("-" * 25)
max_corr = 0
for i, p1 in enumerate(primes[:10]):
    for j, p2 in enumerate(primes[:10]):
        if j <= i:
            continue
        s1 = prime_series[p1] - np.mean(prime_series[p1])
        s2 = prime_series[p2] - np.mean(prime_series[p2])
        corr = np.dot(s1, s2) / (np.linalg.norm(s1) * np.linalg.norm(s2))
        if abs(corr) > 0.15:
            print(f"{p1:4d} {p2:4d}  {corr:10.6f}")
        max_corr = max(max_corr, abs(corr))

print(f"\nMax absolute cross-correlation: {max_corr:.6f}")

###############################################################################
# 4. Is each Euler factor's "kernel" PF_infinity?
###############################################################################

print("\n=== PF analysis of individual Euler factor kernels ===")
print("For each prime p, we compute the 'kernel' of (1-p^{-s})^{-1}")
print("via Fourier transform on the critical line.\n")

def euler_factor_kernel(p, u_values, t_max=100, n_quad=500):
    """
    Phi_p(u) = integral_0^{t_max} Re[-log(1 - p^{-1/2-it})] * cos(u*t) dt / pi

    This is the Fourier cosine transform of the real part of the p-contribution.
    """
    results = []
    for u in u_values:
        def integrand(t):
            s = mpmath.mpc(0.5, t)
            val = -mpmath.log(1 - mpmath.power(p, -s))
            return float(mpmath.re(val)) * float(mpmath.cos(u * t))

        integral = mpmath.quad(integrand, [0, t_max], maxdegree=6)
        results.append(float(integral) / float(mpmath.pi))
    return results

u_test = np.linspace(-1, 1, 21)

print("Computing kernels for small primes...")
euler_kernels = {}
for p in [2, 3, 5, 7, 11]:
    print(f"  p = {p}...", end=" ", flush=True)
    kernel = euler_factor_kernel(p, u_test, t_max=80, n_quad=300)
    euler_kernels[p] = kernel

    # Test log-concavity
    min_ratio = float('inf')
    for i in range(1, len(kernel) - 1):
        if kernel[i] > 0 and kernel[i-1] > 0 and kernel[i+1] > 0:
            ratio = kernel[i]**2 / (kernel[i-1] * kernel[i+1])
            min_ratio = min(min_ratio, ratio)

    is_pf2 = min_ratio >= 1.0 - 1e-6
    print(f"min PF2 ratio = {min_ratio:.6f}, PF2 = {is_pf2}")

###############################################################################
# 5. Theoretical: The convolution structure
###############################################################################

print("\n=== Convolution structure analysis ===")
print("""
Theoretical framework:
  log zeta(s) = sum_p log(1-p^{-s})^{-1}
  zeta(s) = prod_p (1-p^{-s})^{-1} = exp(sum_p log(1-p^{-s})^{-1})

In the Fourier domain (u-space), the exponentiation of a sum corresponds to
a multiplicative convolution. Specifically:

  If f(t) = sum_p g_p(t), then exp(f(t)) has Fourier transform that is
  the convolution of the individual exp(g_p) transforms.

  For PF properties: The Hadamard product (entrywise product) of PF_n and PF_m
  matrices is PF_{min(n,m)} (Schur product theorem for totally positive matrices).

  But convolution preserves PF_infinity: if K1 and K2 are both PF_infinity,
  then K1 * K2 (convolution) is also PF_infinity. This is a theorem of
  Schoenberg (1951).

This means: IF each Euler factor contributes a PF_infinity kernel,
the product (which becomes convolution in the kernel domain) preserves PF_infinity.

The question is whether:
(a) Individual Euler factor kernels ARE PF_infinity
(b) The gamma factors preserve/break PF properties
(c) The Davenport-Heilbronn linear combination breaks the product structure
""")

###############################################################################
# 6. Variance decomposition: Euler product vs DH
###############################################################################

print("\n=== Variance decomposition: sum_p (log p)^2 / p^{2*sigma} ===")
print("This sum controls the two-point function and diverges at sigma=1/2.\n")

def prime_var_sum(sigma, prime_list):
    """sum_p (log p)^2 / p^{2*sigma}"""
    total = 0
    for p in prime_list:
        total += np.log(p)**2 / p**(2*sigma)
    return total

# Extended prime list
extended_primes = []
p = 2
while p < 10000:
    if all(p % d != 0 for d in range(2, int(p**0.5)+1)):
        extended_primes.append(p)
    p += 1 if p == 2 else 2

print(f"Using {len(extended_primes)} primes (up to {extended_primes[-1]})")
print(f"\n{'sigma':>6s}  {'S(p<100)':>10s}  {'S(p<1000)':>10s}  {'S(p<10000)':>10s}  {'Behavior':>12s}")
print("-" * 60)

for sigma in [0.50, 0.51, 0.52, 0.55, 0.60, 0.75, 1.00]:
    s1 = prime_var_sum(sigma, [p for p in extended_primes if p < 100])
    s2 = prime_var_sum(sigma, [p for p in extended_primes if p < 1000])
    s3 = prime_var_sum(sigma, extended_primes)
    behavior = "DIVERGES" if sigma <= 0.50 else "Converges"
    print(f"{sigma:6.2f}  {s1:10.4f}  {s2:10.4f}  {s3:10.4f}  {behavior:>12s}")

###############################################################################
# 7. DH vs zeta: coefficient structure comparison
###############################################################################

print("\n=== Coefficient structure: zeta vs Davenport-Heilbronn ===")
print("Zeta has completely multiplicative structure: a(n) = 1 for all n")
print("DH has coefficients that are linear combinations of character values\n")

kappa_float = float((mpmath.sqrt(10 - 2*mpmath.sqrt(5)) - 2) / (mpmath.sqrt(5) - 1))

def dh_coefficients(N):
    """Compute the first N Dirichlet coefficients of the DH function."""
    coeffs = []
    c1 = complex((1 - 1j*kappa_float)/2)
    c2 = complex((1 + 1j*kappa_float)/2)

    chi_vals = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}  # chi1 mod 5

    for n in range(1, N+1):
        r = n % 5
        chi = chi_vals[r]
        chi_bar = chi.conjugate()
        coeff = c1 * chi + c2 * chi_bar
        coeffs.append(coeff)
    return coeffs

dh_coeffs = dh_coefficients(50)
print(f"{'n':>4s}  {'a_zeta(n)':>10s}  {'a_DH(n)':>20s}  {'|a_DH(n)|':>10s}  {'Multiplicative?':>15s}")
print("-" * 70)

for n in range(1, 31):
    a_dh = dh_coeffs[n-1]
    a_dh_str = f"{a_dh.real:.4f}+{a_dh.imag:.4f}i"

    # Check multiplicativity: a(mn) = a(m)*a(n) for coprime m,n
    is_mult = ""
    if n == 6:  # 2*3
        a6 = dh_coeffs[5]
        a2 = dh_coeffs[1]
        a3 = dh_coeffs[2]
        prod = a2 * a3
        is_mult = f"a(2)*a(3)={prod.real:.4f}+{prod.imag:.4f}i"
    elif n == 10:  # 2*5
        a10 = dh_coeffs[9]
        a2 = dh_coeffs[1]
        a5 = dh_coeffs[4]
        prod = a2 * a5
        is_mult = f"a(2)*a(5)={prod.real:.4f}+{prod.imag:.4f}i"
    elif n == 15:  # 3*5
        a15 = dh_coeffs[14]
        a3 = dh_coeffs[2]
        a5 = dh_coeffs[4]
        prod = a3 * a5
        is_mult = f"a(3)*a(5)={prod.real:.4f}+{prod.imag:.4f}i"

    print(f"{n:4d}  {'1':>10s}  {a_dh_str:>20s}  {abs(a_dh):10.6f}  {is_mult:>15s}")

###############################################################################
# 8. Key structural difference: product vs linear combination
###############################################################################

print("\n=== The fundamental structural difference ===")
print("""
Zeta: zeta(s) = prod_p (1-p^{-s})^{-1}
  -> log zeta(s) = SUM of INDEPENDENT terms
  -> The kernel Phi is built from CONVOLUTION of prime factors
  -> Each factor is PF_infinity (Gaussian/exponential type)
  -> Convolution preserves PF_infinity (Schoenberg)

DH:   L_DH(s) = c1 * L(s,chi1) + c2 * L(s,chi1_bar)
  -> L_DH = LINEAR COMBINATION of two L-functions
  -> Even though each L(s,chi) has an Euler product, the SUM does not
  -> The DH kernel is a linear combination of two kernels
  -> Linear combinations do NOT preserve PF properties in general!
  -> A convex combination c1*K1 + c2*K2 of PF_2 kernels can fail PF_2

This is the KEY: the Euler product gives a MULTIPLICATIVE (convolution) structure
that preserves PF properties, while the DH function's ADDITIVE structure
destroys them.
""")

###############################################################################
# 9. Quantify: how badly does linear combination break PF?
###############################################################################

print("=== How linear combination breaks PF ===")
print("Consider two PF_infinity functions f1, f2. Their sum f1+f2 may fail PF_2.")
print("Example: f1(x) = exp(-x^2), f2(x) = exp(-(x-a)^2)")
print("For large a, f1+f2 is bimodal and NOT log-concave.\n")

# Demonstrate with Gaussians
for a in [0, 1, 2, 3, 4]:
    x = np.linspace(-5, 5+a, 200)
    f = np.exp(-x**2) + np.exp(-(x-a)**2)
    # Test log-concavity
    log_f = np.log(f)
    d2 = np.diff(log_f, 2)
    is_concave = np.all(d2 <= 1e-10)
    min_d2 = np.min(d2)
    print(f"a = {a}: log-concave = {is_concave}, min(d2 log f) = {min_d2:.6f}")

###############################################################################
# 10. Save all results
###############################################################################

results = {
    "prime_variances": [(p, float(v)) for p, v in prime_variances],
    "max_cross_correlation": float(max_corr),
    "euler_kernels": {str(p): k for p, k in euler_kernels.items()},
    "u_test": u_test.tolist(),
    "dh_coefficients": [(float(c.real), float(c.imag)) for c in dh_coeffs[:30]],
}

with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/euler-product-repulsion/euler_factor_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nAll results saved.")
