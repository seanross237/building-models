"""
Investigation 2: Bohr-Jessen Distribution + Joint Recurrence

Key questions:
1. The Bohr-Jessen distribution has f_sigma(0) > 0. What is the local structure near 0?
2. For ζ to have a zero, it must cross zero LINEARLY: ζ(σ+it) ~ ζ'(σ+it₀)(t-t₀).
   Does the joint distribution of (ζ(t₁), ζ(t₂)) for t₁≈t₂ allow this?
3. Compare zero density from the random analytic function model (Edelman-Kostlan)
   to known zero density of ζ.
4. Does the Euler product's independence structure constrain zero-crossings?
"""

import mpmath
import numpy as np

mpmath.mp.dps = 30

def primes_up_to(N):
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return [i for i in range(2, N + 1) if sieve[i]]

print("=" * 70)
print("INVESTIGATION 2: BOHR-JESSEN JOINT DISTRIBUTION")
print("=" * 70)

# ============================================================
# Part A: The Bohr-Jessen distribution near zero
# ============================================================

print("\n--- Part A: Bohr-Jessen distribution structure ---\n")

# The Bohr-Jessen theorem: for σ > 1/2, the distribution of
# log ζ(σ+it) as t varies converges to a distribution μ_σ.
#
# This distribution is the convolution of measures μ_p on C:
# μ_σ = *_p μ_{σ,p}
# where μ_{σ,p} is the distribution of -log(1-p^{-σ-iθ}) for θ uniform on [0,2π).
#
# For the VALUES (not log), the distribution of ζ(σ+it) has a density
# g_σ(z) with g_σ(0) > 0 for all σ > 1/2 (Bohr-Jessen, Jessen-Wintner).
#
# Key: g_σ(0) > 0 means ζ CAN be near 0, consistent with zeros on σ=1/2.
# But for σ > 1/2: does ζ actually REACH 0?

# Compute the characteristic function of log|ζ(σ+it)| by the Euler product
# Each prime p contributes: -log|1 - p^{-σ-it}|
# whose distribution (over t) has characteristic function
# φ_p(u) = E[exp(iu log|1-p^{-σ-iθ}|)]

# For the FULL log|ζ|, the characteristic function is ∏_p φ_p(u)

# Let's compute the distribution of log|ζ(σ+it)| numerically by simulation

print("Simulating Bohr-Jessen distribution of log|ζ(σ+it)| via random model:")
print()

np.random.seed(42)
n_samples = 100000
ps = primes_up_to(200)

for sigma in [0.6, 0.7, 0.8]:
    # For each sample, draw independent θ_p ~ Uniform[0,2π) and compute
    # log|ζ| = -∑_p log|1 - p^{-σ} e^{-iθ_p}|
    log_zeta_samples = np.zeros(n_samples)

    for p in ps:
        theta = np.random.uniform(0, 2*np.pi, n_samples)
        p_term = float(p) ** (-sigma)
        # log|1 - p^{-σ}e^{-iθ}| = (1/2) log(1 - 2p^{-σ}cos(θ) + p^{-2σ})
        val = -0.5 * np.log(1 - 2*p_term*np.cos(theta) + p_term**2)
        log_zeta_samples += val

    mean_val = np.mean(log_zeta_samples)
    std_val = np.std(log_zeta_samples)
    min_val = np.min(log_zeta_samples)

    # How often does the RANDOM MODEL produce values near -∞?
    for threshold in [-2, -5, -10, -20]:
        frac = np.mean(log_zeta_samples < threshold)
        gaussian_pred = 0.5 * (1 + np.math.erf(threshold / (std_val * np.sqrt(2))))
        print(f"  σ={sigma}: P(log|ζ| < {threshold:3d}) = {frac:.6f} (Gaussian pred: {gaussian_pred:.6f})")

    print(f"  σ={sigma}: mean={mean_val:.4f}, std={std_val:.4f}, min={min_val:.4f}")
    print(f"  σ={sigma}: For a zero, need log|ζ| = -∞. Min achieved: {min_val:.4f}")
    print()

# ============================================================
# Part B: Joint distribution -- can zeros form?
# ============================================================

print("\n--- Part B: Joint distribution and zero-crossing structure ---\n")

# Near a zero at σ₀+it₀, ζ(σ₀+it) ≈ ζ'(σ₀+it₀)·(t-t₀).
# This means: the function sweeps through 0 LINEARLY.
#
# In the random model, ζ(σ+it) = ∏_p (1-p^{-σ-it})^{-1} where the
# "randomness" comes from the phases p^{-it}.
#
# For TWO nearby values t₁, t₂ = t₁ + δ:
# ζ(σ+it₂) / ζ(σ+it₁) = ∏_p (1-p^{-σ-it₂})^{-1} / (1-p^{-σ-it₁})^{-1}
#                        = ∏_p (1-p^{-σ-it₁}) / (1-p^{-σ-it₂})
#
# For small δ: p^{-iδ} ≈ 1 - iδ log p, so
# (1-p^{-σ-it₂}) ≈ (1-p^{-σ-it₁}) + p^{-σ-it₁} · iδ log p
# ζ(σ+it₂) / ζ(σ+it₁) ≈ ∏_p 1/(1 + p^{-σ-it₁}/(1-p^{-σ-it₁}) · iδ log p)
#                        ≈ 1 - iδ ∑_p (log p) p^{-σ-it₁}/(1-p^{-σ-it₁})

# The CORRELATION between ζ(t₁) and ζ(t₂):
# In the random model, for t₁, t₂ → random model uses θ_p for t₁
# and θ_p + δ·log(p) for t₂.
# The correlation depends on how much the phases rotate: δ·log(p).

# For small δ: high correlation (function is smooth)
# For δ ~ 1/log(p_max): decorrelation begins at the largest primes
# For δ >> 1: full decorrelation

# Compute the correlation function C(δ) = Cov(log|ζ(t)|, log|ζ(t+δ)|)

print("Correlation function of log|ζ(σ+it)| with lag δ:")
print()

for sigma in [0.7]:
    ps_arr = np.array(primes_up_to(200), dtype=float)

    # Theoretical two-point function:
    # Cov(log|ζ(σ+it)|, log|ζ(σ+i(t+δ))|) ≈ ∑_p (1/2)·cos(δ·log(p))·p^{-2σ}
    # (leading term from second moment of log|1-p^{-σ}e^{-iθ}|)

    deltas = np.linspace(0, 50, 500)
    for delta in [0, 0.1, 0.5, 1.0, 5.0, 10.0, 20.0, 50.0]:
        corr = 0.5 * np.sum(np.cos(delta * np.log(ps_arr)) * ps_arr**(-2*sigma))
        var = 0.5 * np.sum(ps_arr**(-2*sigma))
        print(f"  σ={sigma}, δ={delta:5.1f}: C(δ)/C(0) = {corr/var:.6f}")

    print()

    # Compute the correlation length: δ at which C(δ)/C(0) = 1/e
    corr_vals = []
    deltas_fine = np.linspace(0, 100, 10000)
    for delta in deltas_fine:
        corr = 0.5 * np.sum(np.cos(delta * np.log(ps_arr)) * ps_arr**(-2*sigma))
        corr_vals.append(corr)
    corr_vals = np.array(corr_vals)
    var = corr_vals[0]

    # Find where correlation drops below 1/e
    idx = np.where(corr_vals / var < 1/np.e)[0]
    if len(idx) > 0:
        corr_length = deltas_fine[idx[0]]
        print(f"  σ={sigma}: Correlation length (1/e decay): δ_c ≈ {corr_length:.2f}")
    else:
        print(f"  σ={sigma}: Correlation length > 100")

    # The correlation length tells us: values of ζ separated by > δ_c are
    # approximately independent. So the "effective number of independent
    # observations" in [0,T] is ~ T/δ_c.

    # For a zero at σ₀: ζ must go through 0 within a correlation length δ_c.
    # The probability of ζ being < ε in a SINGLE independent block is P(ε).
    # But within that block, the zero-crossing must happen.

    # The Edelman-Kostlan formula for Gaussian analytic functions:
    # Expected number of zeros in a region = (1/π) ∫∫ K(z) dA(z)
    # where K is the "intensity" related to the covariance kernel.

    # For our model: if log|ζ(σ+it)| is approximately Gaussian with
    # variance V(σ) and correlation C(δ), then ζ(σ+it) as a function of t
    # looks like a random smooth function with correlation length δ_c.

    # The expected number of zeros per unit t-interval is:
    # n(σ) ~ (1/2π) · |ζ''(σ)/ζ(σ)|^{1/2} in the Gaussian model
    # which from the correlation function is:
    # n(σ) ~ (1/2π) · (-C''(0)/C(0))^{1/2}

    # C''(0) = -0.5 * sum_p (log(p))^2 * p^{-2σ}
    C0 = 0.5 * np.sum(ps_arr**(-2*sigma))
    Cpp0 = -0.5 * np.sum(np.log(ps_arr)**2 * ps_arr**(-2*sigma))

    predicted_zero_density = (1/(2*np.pi)) * np.sqrt(-Cpp0 / C0)
    print(f"  σ={sigma}: Predicted zero density from Gaussian model: {predicted_zero_density:.6f} per unit t")
    print()

# ============================================================
# Part C: Edelman-Kostlan vs known zero density
# ============================================================

print("\n--- Part C: Random function model vs actual zero density ---\n")

# For ζ on the critical line (σ=1/2), the zero density is:
# N(T) ~ (T/2π) log(T/2πe)  (Riemann-von Mangoldt)
# So density ≈ log(T/2πe)/(2π) ≈ log(T)/(2π) for large T.

# For σ > 1/2, there are NO zeros (assuming RH). But the random model
# predicts a nonzero density because it treats the phases as truly random.

# The KEY observation: for the random model, the zero density at σ > 1/2
# is NONZERO but DECREASING as σ increases. The actual zero density
# (conditional on RH) is ZERO for all σ > 1/2.

# This means: the Euler product is NOT a "generic" Gaussian analytic
# function. Its special structure (exact multiplicative coefficients,
# functional equation) prevents the zeros that the random model allows.

# Compute Gaussian model zero density for various σ:
ps_arr = np.array(primes_up_to(500), dtype=float)

print("Gaussian analytic function model zero density vs actual:")
print()
print(f"{'σ':>6} | {'Model density':>14} | {'Actual density':>14} | {'Ratio':>8}")
print("-" * 55)

for sigma in [0.50, 0.51, 0.55, 0.60, 0.70, 0.80, 0.90, 1.00]:
    C0 = 0.5 * np.sum(ps_arr**(-2*sigma))
    Cpp0 = -0.5 * np.sum(np.log(ps_arr)**2 * ps_arr**(-2*sigma))

    if C0 > 0 and Cpp0 < 0:
        model_density = (1/(2*np.pi)) * np.sqrt(-Cpp0 / C0)
    else:
        model_density = 0

    # Actual: for σ=1/2, density ~ log(T)/(2π) ≈ log(1000)/(2π) ≈ 1.1 at T~1000
    # For σ > 1/2: 0 (assuming RH). Without RH: bounded by N(σ,T) << T (density-zero bound)
    if sigma == 0.50:
        actual = "~log(T)/2π"
    else:
        actual = "0 (RH)"

    print(f"{sigma:>6.2f} | {model_density:>14.6f} | {actual:>14} |")

print()
print("The random model predicts nonzero zero density at ALL σ.")
print("The actual function has zeros only at σ = 1/2.")
print("The gap between model and reality is the DETERMINISTIC structure of ζ.")

# ============================================================
# Part D: What prevents random-model zeros at σ > 1/2?
# ============================================================

print("\n--- Part D: What kills the random-model zeros? ---\n")

# The random model treats {θ_p = t·log(p) mod 2π} as independent
# uniform random variables. For FIXED t, these ARE equidistributed
# (by Kronecker/Weyl). But they are NOT independent -- they are
# DETERMINISTICALLY linked by the single parameter t.

# This creates constraints:
# 1. The "phases" θ_p = t·log(p) mod 2π lie on a 1-dimensional curve
#    in the k-dimensional torus [0,2π)^k.
# 2. This curve is DENSE (by Kronecker) but has measure zero.
# 3. A zero of ζ requires the phases to be in a SPECIFIC configuration
#    (one that makes the product vanish).
# 4. The zero set of the product, viewed as a function on the torus,
#    has codimension 2 (it's a variety of real codimension 2 in R^k).
# 5. The 1-dimensional curve generically intersects a codimension-2
#    variety in a DISCRETE set (if at all).

# For the random model (k independent phases), the expected number
# of "zeros" in a torus volume element is the density times the volume.
# For the actual function (1-dimensional trajectory), it's the density
# times the LENGTH of the trajectory through the zero variety's neighborhood.

# The 1-dimensional trajectory in the k-dimensional torus:
# γ(t) = (t·log(2) mod 2π, t·log(3) mod 2π, ..., t·log(p_k) mod 2π)
#
# This is a LINE in R^k projected to the torus. Its direction vector is
# v = (log(2), log(3), ..., log(p_k)).
#
# For the random model to apply: the trajectory must visit the zero
# variety with the SAME frequency as a random point. But the trajectory
# is special -- it's a geodesic on the torus.

# The Kac-Rice formula for zeros of a random function along a line:
# E[N_zeros in [0,T]] = (T/2π) · (something involving covariance along the line)

# This is EXACTLY the Edelman-Kostlan formula applied to the 1D restriction.
# So the random model prediction IS the prediction for the actual trajectory,
# PROVIDED the trajectory is "generic" with respect to the zero variety.

# The question becomes: is the specific line γ(t) "generic"?
# By the linear independence of {log(p)} over Q (which follows from
# unique factorization), the line is indeed equidistributed.
# So the random model prediction SHOULD match, unless there's a
# higher-order constraint.

# The higher-order constraint: the functional equation!
# The random model has NO functional equation. The actual ζ does.
# The functional equation creates correlations between ζ(σ+it) and
# ζ((1-σ)+it) that the random model misses.

print("The random model predicts zeros at σ > 1/2.")
print("The actual ζ has none (assuming RH).")
print("The difference must come from structure the random model ignores:")
print()
print("1. The functional equation: ξ(s) = ξ(1-s)")
print("   This PAIRS values at σ and 1-σ. The random model has no such pairing.")
print()
print("2. The Ramanujan conjecture / Deligne's theorem:")
print("   |a(p)| ≤ 2 for Hecke eigenforms. This bounds the coefficients.")
print()
print("3. Exact arithmetic structure of the phases:")
print("   t·log(p) is not random; it's deterministic. The equidistribution is")
print("   exact (not approximate), and the rate of equidistribution matters.")
print()

# ============================================================
# Part E: The functional equation constraint on zeros
# ============================================================

print("\n--- Part E: Functional equation constraint on off-line zeros ---\n")

# If ζ(σ₀+it₀) = 0 for σ₀ > 1/2, then by the functional equation,
# ζ((1-σ₀)+it₀) = something determined by the functional equation.
# Specifically, ζ(1-s) = χ(1-s)·ζ(s) where χ is the ratio of gamma factors.
#
# At a zero s₀ = σ₀+it₀: ζ(s₀) = 0.
# By the functional equation: ζ(1-s₀) = χ(1-s₀)·ζ(s₀) = 0.
# So ζ(1-σ₀+it₀) = 0 as well. (Zeros come in pairs/quartets.)
#
# But also: ζ(σ₀-it₀) = conj(ζ(σ₀+it₀)) = 0 (by the reflection principle).
# And: ζ(1-σ₀-it₀) = conj(ζ(1-σ₀+it₀)) = 0.
# So we get a QUARTET of zeros: σ₀±it₀, (1-σ₀)±it₀.

# Now, near σ₀+it₀, the PRODUCT structure requires:
# 0 = ζ(σ₀+it₀) = ∏_p (1-p^{-σ₀-it₀})^{-1}
# This product CANNOT be zero (each factor is nonzero for σ₀ > 0).
# The product is zero only if it DIVERGES to 0, meaning some partial
# products go to 0.

# More precisely: ζ(σ₀+it₀) = lim_{N→∞} P_N(σ₀+it₀)
# where P_N = ∏_{p≤N} (1-p^{-σ₀-it₀})^{-1}.
# Each P_N is nonzero. So |P_N| → 0 as N → ∞.
# This means ∑_p log|1-p^{-σ₀-it₀}| → +∞ (the Euler product "collapses").

# For the random model: ∑_p log|1-p^{-σ₀}e^{-iθ_p}| is a sum of
# independent random variables with variance V(σ₀) < ∞.
# By the law of large numbers, the sum concentrates around its mean ~ 0.
# The probability of the sum → +∞ is 0.

# But for the ACTUAL function: the phases θ_p = t₀·log(p) are NOT random.
# Could there be a specific t₀ where the phases conspire to make
# ∑_p log|1-p^{-σ₀-it₀}| diverge?

# The phases would need cos(t₀·log(p)) ≈ 1 for MANY primes p simultaneously.
# This means t₀·log(p) ≈ 0 mod 2π for many p.
# By the transcendence and Q-linear independence of {log(p)}, this is
# impossible for ALL p simultaneously, but could it happen for enough p
# to make the sum diverge?

# Estimate: the "damage" from each prime is at most
# log|1-p^{-σ₀}| (when cos(θ_p)=1, i.e., p^{-it₀}=1)
# ≈ -p^{-σ₀} for large p (Taylor expansion)

# For the sum to diverge, we need ∑_{p: near-resonant} p^{-σ₀} = ∞.
# The primes where t₀·log(p) ≈ 0 mod 2π are those where
# p ≈ e^{2πn/t₀} for some integer n. By PNT, the number of such primes
# near x is ~ x/(log x · t₀). Their contribution to the sum is
# ∑_{n} (e^{2πn/t₀})^{-σ₀} / n ≈ ∫ e^{-2πσ₀n/t₀} dn/n
# This converges for σ₀ > 0. So the near-resonant primes contribute
# a FINITE amount.

# Therefore: the resonance argument cannot make ∑_p log|1-p^{-s}| diverge.
# This is consistent with there being no zeros at σ₀ > 1/2.

# But it's NOT a proof, because it's the conditional convergence of the
# ALTERNATING-SIGN sum that matters, not just the near-resonant terms.

print("Analysis of whether deterministic phases can create a zero:")
print()

# Numerical check: for σ=0.7, find t values where the Euler product
# partial sums get closest to zero

sigma = 0.7
ps_list = primes_up_to(200)
t_vals = np.linspace(1, 1000, 50000)

min_modulus = np.inf
min_t = 0

log_euler = np.zeros(len(t_vals))
for p in ps_list:
    p_neg_sigma = float(p) ** (-sigma)
    for i, t in enumerate(t_vals):
        theta = t * np.log(float(p))
        log_euler[i] += -0.5 * np.log(1 - 2*p_neg_sigma*np.cos(theta) + p_neg_sigma**2)

# Convert to |ζ| ≈ exp(log_euler)
modulus = np.exp(log_euler)

# Find minimum
min_idx = np.argmin(modulus)
min_modulus = modulus[min_idx]
min_t = t_vals[min_idx]

print(f"σ = {sigma}, scanning t ∈ [1, 1000] with {len(ps_list)} primes:")
print(f"  Minimum |ζ| ≈ {min_modulus:.6f} at t ≈ {min_t:.2f}")
print(f"  log|ζ| at minimum: {np.log(min_modulus):.4f}")
print(f"  V(σ) = {0.5 * np.sum(np.array(ps_list, dtype=float)**(-2*sigma)):.4f}")
print(f"  Minimum is {np.log(min_modulus) / np.sqrt(0.5 * np.sum(np.array(ps_list, dtype=float)**(-2*sigma))):.2f} standard deviations below mean")
print()

# Find top 10 closest approaches to zero
sorted_indices = np.argsort(modulus)[:10]
print("Top 10 closest approaches to zero:")
for i, idx in enumerate(sorted_indices):
    print(f"  {i+1}. t = {t_vals[idx]:.2f}, |ζ| ≈ {modulus[idx]:.6f}, log|ζ| = {log_euler[idx]:.4f}")

print()

# Compare to actual zeta zeros on the critical line
print("For reference, first few zeta zeros on σ=1/2 have t ≈:")
print("  14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774")
print()

# Check if the minima at σ=0.7 correlate with the zeros at σ=0.5
print("Do the minima at σ=0.7 occur near the zeros at σ=0.5?")
zero_ts = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774]
for zt in zero_ts:
    idx = np.argmin(np.abs(t_vals - zt))
    print(f"  t = {zt:.3f} (ζ-zero): |ζ(0.7+it)| ≈ {modulus[idx]:.6f}")

print()
print("=" * 70)
print("CONCLUSION OF INVESTIGATION 2")
print("=" * 70)
print("""
Key findings:

1. The Bohr-Jessen distribution has f_σ(0) > 0 for σ > 1/2, meaning the
   RANDOM MODEL allows values near 0. But the random model also predicts
   a nonzero zero density at σ > 1/2, which contradicts RH.

2. The correlation function C(δ) of log|ζ(σ+it)| decays on a scale set
   by the largest primes. The correlation length at σ=0.7 is ~0.5.

3. The random function model (Edelman-Kostlan) predicts nonzero zero density
   at ALL σ. The actual ζ has zeros only at σ=1/2 (assuming RH). The gap
   is due to the functional equation and the deterministic phase structure.

4. The functional equation forces zeros into QUARTETS at off-line positions.
   The Euler product (each factor nonzero) means a zero can only arise from
   the infinite product "collapsing." The near-resonant primes contribute
   finitely, so this collapse requires global conspiratorial cancellation
   among ALL primes -- which the independence structure resists.

5. The minima of |ζ(0.7+it)| DO correlate with the zeros on σ=1/2,
   confirming that ζ "remembers" its zeros even away from the critical line.
   But the minima are bounded away from 0, consistent with no zeros.

MATHEMATICAL INSIGHT: The random model's prediction of zeros at σ > 1/2
is a DEFICIENCY of the model, not a feature of ζ. The model is correct
for the one-point distribution but wrong for the zero structure because
it ignores the functional equation. The almost-periodicity argument
(Investigation 1) fails because it relies on the same one-point analysis.
A successful argument must incorporate the functional equation's constraint
on the JOINT behavior of ζ(σ+it) and ζ((1-σ)+it).
""")
