"""
Bell-CHSH analysis for correlated Gaussian variables.

For bivariate Gaussian (X1, X2) with zero means, equal variances sigma^2,
and correlation coefficient rho, the sign-correlation formula gives:

E[sign(X1) sign(X2)] = (2/pi) arcsin(rho)   [Stapp 1971; bivariate normal]

For thresholded measurements A = sign(X1 - a), A' = sign(X1 - a'),
B = sign(X2 - b), B' = sign(X2 - b'), the optimal CHSH for Gaussian
variables must be determined numerically.

Key question: Can the CHSH for SED correlated Gaussians ever exceed 2?
Answer: No — classical probability theory guarantees S <= 2.

But we want to understand HOW the optimal S depends on rho = C_xx.

Also: verify the arcsin formula against our simulation results.
"""

import numpy as np
from scipy.stats import norm

# Arcsin formula for sign correlation of bivariate Gaussian (zero thresholds)
def sign_corr_arcsin(rho):
    """E[sign(X) sign(Y)] = (2/pi) arcsin(rho) for bivariate Gaussian"""
    return (2 / np.pi) * np.arcsin(rho)

# More general: E[sign(X1-a) sign(X2-b)] for bivariate Gaussian
# with means mu1=mu2=0, sigma=1, correlation rho
# P(X1 > a, X2 > b) - P(X1 > a, X2 < b) - P(X1 < a, X2 > b) + P(X1 < a, X2 < b)
def sign_corr_shifted(rho, a, b, sigma=1.0):
    """
    E[sign(X1-a) sign(X2-b)] for zero-mean bivariate Gaussian with correlation rho.
    Uses the formula:
    = P(X1>a, X2>b) - P(X1>a, X2<b) - P(X1<a, X2>b) + P(X1<a, X2<b)
    = 2*P(X1>a, X2>b) - P(X1>a) - P(X2>b) + 1

    For bivariate normal, P(X1>a, X2>b) can be computed from the bivariate CDF.
    """
    from scipy.stats import multivariate_normal

    # P(X1 > a, X2 > b) = 1 - P(X1 <= a) - P(X2 <= b) + P(X1 <= a, X2 <= b)
    P1 = norm.sf(a / sigma)  # P(X1 > a)
    P2 = norm.sf(b / sigma)  # P(X2 > b)

    # P(X1 <= a, X2 <= b) from bivariate normal CDF
    cov = [[sigma**2, rho * sigma**2], [rho * sigma**2, sigma**2]]
    P12 = multivariate_normal.cdf([a, b], mean=[0, 0], cov=cov)

    P_both_above = 1 - norm.cdf(a/sigma) - norm.cdf(b/sigma) + P12

    result = 2 * P_both_above - P1 - P2 + 1
    return result

def chsh_optimal_gaussian(rho, sigma=1.0, n_grid=20):
    """
    Find the maximum CHSH for bivariate Gaussian with correlation rho,
    using a grid search over threshold settings.
    """
    best_S = 0.0
    best_params = None

    # Grid of threshold settings (in units of sigma)
    thresholds = np.linspace(-1.5, 1.5, n_grid) * sigma

    for a in thresholds:
        for ap in thresholds:
            if abs(a - ap) < 0.1 * sigma:
                continue
            for b in thresholds:
                for bp in thresholds:
                    if abs(b - bp) < 0.1 * sigma:
                        continue
                    AB   = sign_corr_shifted(rho, a, b, sigma)
                    ABp  = sign_corr_shifted(rho, a, bp, sigma)
                    ApB  = sign_corr_shifted(rho, ap, b, sigma)
                    ApBp = sign_corr_shifted(rho, ap, bp, sigma)

                    S = abs(AB + ABp + ApB - ApBp)
                    if S > best_S:
                        best_S = S
                        best_params = (a, ap, b, bp, AB, ABp, ApB, ApBp)

    return best_S, best_params


# ──────────────────────────────────────────────
# 1. Verify arcsin formula against simulation
# ──────────────────────────────────────────────
print("=" * 60)
print("Verification: arcsin formula vs simulation")
print(f"{'rho (C_xx)':>12} | {'arcsin pred':>12} | {'S_max (sim)':>12}")
print("-" * 40)

sim_data = [
    (0.0,  1.0000, 2.0000),
    (0.1,  0.9948, 1.9492),
    (1.0,  0.5384, 1.0916),
    (10.0, -0.8328, 1.6132),
]
for d, C_xx, S_sim in sim_data:
    arcsin_pred = sign_corr_arcsin(C_xx)
    print(f"d={d:>4.1f}: C_xx={C_xx:>7.4f} | arcsin={arcsin_pred:>12.4f} | S_sim={S_sim:>7.4f}")

print()
print("Note: arcsin formula gives E[sign(X1)sign(X2)] with zero thresholds,")
print("not the CHSH S value itself.")

# ──────────────────────────────────────────────
# 2. Optimal CHSH as a function of rho
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("Optimal CHSH S_max vs correlation rho (theory)")
header_col = "thresholds (a,a',b,b')"
print(f"{'rho':>6} | {'S_max':>6} | {header_col:>30}")
print("-" * 55)

rho_values = [0.9999, 0.995, 0.85, 0.54, 0.0, -0.54, -0.83]
for rho in rho_values:
    S_max, params = chsh_optimal_gaussian(rho, sigma=1.0, n_grid=15)
    if params:
        a, ap, b, bp = params[:4]
        print(f"{rho:>6.3f} | {S_max:>6.4f} | a={a:.2f}, a'={ap:.2f}, b={b:.2f}, b'={bp:.2f}")
    else:
        print(f"{rho:>6.3f} | {S_max:>6.4f} | (no params)")

print()
print(f"Classical Bell bound: S <= 2.000")
print(f"QM maximum (singlet): S = {2*np.sqrt(2):.4f}")

# ──────────────────────────────────────────────
# 3. Theoretical maximum CHSH for correlated Gaussians
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("Theory: Max CHSH for Gaussian bivariate with correlation rho")
print("Using only zero thresholds: CHSH <= 2|arcsin(rho)| trivially")
print()
print("For all classical (LHV) systems: S <= 2. This is guaranteed")
print("by the structure of classical probability. The Gaussian")
print("shared ZPF cannot exceed this regardless of rho.")
print()

# The maximum CHSH for any classical bivariate distribution is 2.
# For Gaussian variables with zero thresholds:
# CHSH = |E[sign(X)sign(Y)] + E[sign(X)sign(Y')] + E[sign(X')sign(Y)] - E[sign(X')sign(Y')]|
# <= 2 by Bell's theorem (since the common cause is the shared ZPF = LHV)

print("Key verification: Is S > 2 ever achievable with classical Gaussians?")
print("Testing extreme correlation rho -> 1:")
rho = 0.9999
S_max, params = chsh_optimal_gaussian(rho, sigma=1.0, n_grid=20)
print(f"rho = {rho}, S_max = {S_max:.6f} (should be <= 2.000)")
