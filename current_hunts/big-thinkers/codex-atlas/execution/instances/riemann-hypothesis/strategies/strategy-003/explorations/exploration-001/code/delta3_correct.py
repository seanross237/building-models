"""
Correct computation of Delta_3 using verified methods.

Strategy:
1. Compute GUE Delta_3 from random matrices as ground truth
2. Find the correct formula connecting K(tau) -> Delta_3
3. Apply corrections for zeta zeros

Key reference: Berry-Keating (1999) SIAM Rev., equations (4.2)-(4.28)
"""

import numpy as np
from scipy.integrate import quad as scipy_quad

np.random.seed(42)

# =============================================================================
# STEP 1: GUE Delta_3 from random matrices (ground truth)
# =============================================================================
print("=" * 70)
print("STEP 1: GUE Delta_3 from random matrices (ground truth)")
print("=" * 70)

def delta3_eigenvalues(eigenvalues, L, n_offsets=50):
    """Compute Delta_3(L) from eigenvalues using the confirmed integral form.

    Eigenvalues should be unfolded (mean spacing = 1).

    Uses: delta3 = F_min / L where
        I0 = n*L - sum(yk)
        I1 = n*L^2/2 - (1/2)*sum(yk^2)
        I2 = n^2*L - sum((2k-1)*yk)   [k=1,2,...,n]
        F_min = I2 - I0^2/L - 12*(I1 - I0*L/2)^2/L^3
    """
    eigs = np.sort(eigenvalues)
    N = len(eigs)

    # Sample multiple offsets
    min_eig = eigs[0]
    max_eig = eigs[-1]
    range_eig = max_eig - min_eig

    if range_eig < L:
        return float('nan')

    offsets = np.linspace(min_eig, max_eig - L, n_offsets)
    d3_values = []

    for alpha in offsets:
        # Find eigenvalues in [alpha, alpha+L]
        mask = (eigs >= alpha) & (eigs < alpha + L)
        yk = eigs[mask] - alpha  # shift to [0, L]
        n = len(yk)

        if n < 2:
            continue

        k = np.arange(1, n + 1)
        I0 = n * L - np.sum(yk)
        I1 = n * L**2 / 2.0 - 0.5 * np.sum(yk**2)
        I2 = n**2 * L - np.sum((2 * k - 1) * yk)
        F_min = I2 - I0**2 / L - 12.0 * (I1 - I0 * L / 2.0)**2 / L**3
        d3 = F_min / L
        d3_values.append(d3)

    return np.mean(d3_values) if d3_values else float('nan')


def generate_gue_eigenvalues(N):
    """Generate eigenvalues of an N×N GUE matrix."""
    # GUE: H = (A + A†)/(2*sqrt(2N)), A has iid complex normal entries
    A = (np.random.randn(N, N) + 1j * np.random.randn(N, N)) / np.sqrt(2)
    H = (A + A.conj().T) / (2.0)
    eigenvalues = np.linalg.eigvalsh(H)
    return np.sort(eigenvalues)


def unfold_semicircle(eigenvalues, N):
    """Unfold GUE eigenvalues using Wigner semicircle law.

    The integrated density is N(E) = (N/(2*pi)) [E*sqrt(4-E^2)/2 + 2*arcsin(E/2)]
    for |E| < 2 (with eigenvalues scaled by sqrt(N)).
    """
    # For GUE(N), eigenvalues are on [-2sqrt(N), 2sqrt(N)]
    # The semicircle density is rho(E) = (1/(2*pi)) * sqrt(4 - (E/sqrt(N))^2) / sqrt(N)
    # Wait, for H = (A+A†)/2 with A being N×N complex normal,
    # the eigenvalues have Wigner semicircle on [-sqrt(N), sqrt(N)] approximately
    # More precisely: scale e = E / sqrt(N), density rho(e) = (2/pi) sqrt(1-e^2)

    # Scale eigenvalues
    e = eigenvalues / np.sqrt(N)

    # Integrated semicircle density: N(e) = N * [(e*sqrt(1-e^2) + arcsin(e))/pi + 1/2]
    # for |e| <= 1
    mask = np.abs(e) <= 1.0
    unfolded = np.zeros_like(eigenvalues)
    for i, ei in enumerate(e):
        if abs(ei) > 1.0:
            ei = np.clip(ei, -0.9999, 0.9999)
        unfolded[i] = N * (ei * np.sqrt(1.0 - ei**2) + np.arcsin(ei)) / np.pi + N / 2.0

    return unfolded


# Generate GUE eigenvalues and compute Delta_3
N_matrix = 500
n_trials = 20

print(f"\nGenerating {n_trials} GUE matrices of size {N_matrix}x{N_matrix}")
print("Computing Delta_3 at various L values...\n")

L_values = [1, 2, 5, 10, 15, 20, 25, 30, 40, 50]
d3_gue_all = {L: [] for L in L_values}

for trial in range(n_trials):
    eigs = generate_gue_eigenvalues(N_matrix)
    unfolded = unfold_semicircle(eigs, N_matrix)

    # Use middle 80% of eigenvalues (avoid edge effects)
    N_use = int(0.8 * N_matrix)
    start = int(0.1 * N_matrix)
    unfolded_center = unfolded[start:start + N_use]
    # Reshift so mean spacing is 1
    unfolded_center = unfolded_center - unfolded_center[0]

    for L in L_values:
        d3 = delta3_eigenvalues(unfolded_center, L, n_offsets=30)
        if not np.isnan(d3):
            d3_gue_all[L].append(d3)

    if (trial + 1) % 5 == 0:
        print(f"  Trial {trial + 1}/{n_trials} done")

print(f"\n{'L':>5s} {'Delta3_GUE':>12s} {'StdErr':>10s} {'N_trials':>10s}")
print("-" * 40)
d3_gue_mean = {}
for L in L_values:
    vals = d3_gue_all[L]
    if vals:
        mean = np.mean(vals)
        stderr = np.std(vals) / np.sqrt(len(vals))
        d3_gue_mean[L] = mean
        print(f"{L:5d} {mean:12.6f} {stderr:10.6f} {len(vals):10d}")
    else:
        print(f"{L:5d} {'N/A':>12s}")

# Save results
np.savez('code/gue_delta3_ground_truth.npz',
         L_values=np.array(L_values),
         d3_means=np.array([d3_gue_mean.get(L, np.nan) for L in L_values]),
         d3_all={str(L): np.array(d3_gue_all[L]) for L in L_values})

# =============================================================================
# STEP 2: Compute Delta_3 from form factor K(tau) using VERIFIED formula
# =============================================================================
print("\n" + "=" * 70)
print("STEP 2: Delta_3 from K(tau)")
print("=" * 70)

# The correct relation uses the Fourier pair:
# Sigma_2(L) = (2/pi^2) int_0^inf K(tau)/tau^2 sin^2(pi*L*tau) dtau
# and the Dyson-Mehta relation:
# Delta_3(L) = (2/L^4) int_0^L (L^3 - 2L^2*r + r^3) Sigma_2(r) dr

# Since Sigma_2 computed from K might have numerical issues,
# let's also use the DIRECT formula via pair correlation:

# Delta_3(L) = L/15 + (2/L^4) int_0^L (L-r)^2 (2Lr - r^2) (R2(r) - 1) dr
# where R2(r) is the pair correlation function.

# For GUE: R2(r) = 1 - (sin(pi*r)/(pi*r))^2
# So R2(r) - 1 = -(sin(pi*r)/(pi*r))^2

# Let me verify this formula by comparing with the GUE ground truth.

def R2_GUE(r):
    if abs(r) < 1e-15:
        return 0.0
    return 1.0 - (np.sin(np.pi * r) / (np.pi * r))**2

def delta3_from_R2_v2(L, R2_func, n_points=10000):
    """Delta_3 = L/15 + (2/L^4) int_0^L (L-r)^2 (2Lr-r^2) (R2(r)-1) dr"""
    r_vals = np.linspace(1e-10, L, n_points)
    R2_vals = np.array([R2_func(r) for r in r_vals])
    kernel = (L - r_vals)**2 * (2*L*r_vals - r_vals**2)
    integrand = kernel * (R2_vals - 1.0)
    integral = np.trapezoid(integrand, r_vals)
    return L/15.0 + (2.0 / L**4) * integral

print(f"\n{'L':>5s} {'GUE_matrix':>12s} {'GUE_formula':>12s} {'Ratio':>8s}")
print("-" * 40)
for L in L_values:
    d3_matrix = d3_gue_mean.get(L, np.nan)
    d3_formula = delta3_from_R2_v2(L, R2_GUE)
    ratio = d3_formula / d3_matrix if d3_matrix > 0 else float('nan')
    print(f"{L:5d} {d3_matrix:12.6f} {d3_formula:12.6f} {ratio:8.4f}")

# =============================================================================
# STEP 3: Try alternative formulas for Delta_3
# =============================================================================
print("\n" + "=" * 70)
print("STEP 3: Alternative Delta_3 formulas")
print("=" * 70)

# Formula A: Sigma_2 route
def sigma2_GUE_exact(L, n_points=50000, tau_max=200):
    """Sigma_2(L) = (2/pi^2) int_0^inf K_GUE(tau)/tau^2 sin^2(pi*L*tau) dtau"""
    # Split integral: [0,1] with K=tau, [1,inf] with K=1
    # Part 1: int_0^1 sin^2(pi*L*tau)/tau dtau
    def f1(tau):
        return np.sin(np.pi * L * tau)**2 / tau
    part1, _ = scipy_quad(f1, 1e-15, 1.0, limit=200)

    # Part 2: int_1^inf sin^2(pi*L*tau)/tau^2 dtau
    def f2(tau):
        return np.sin(np.pi * L * tau)**2 / tau**2
    part2, _ = scipy_quad(f2, 1.0, np.inf, limit=200)

    return (2.0 / np.pi**2) * (part1 + part2)

# Formula B: Direct pair correlation route
def sigma2_GUE_from_R2(L, n_points=10000):
    """Sigma_2(L) = L + 2 int_0^L (L-r)(R2(r)-1) dr"""
    r_vals = np.linspace(1e-10, L, n_points)
    R2_vals = np.array([R2_GUE(r) for r in r_vals])
    integrand = (L - r_vals) * (R2_vals - 1.0)
    return L + 2.0 * np.trapezoid(integrand, r_vals)

print("\nSigma_2 comparison:")
print(f"{'L':>5s} {'S2_exact':>12s} {'S2_from_R2':>12s}")
print("-" * 30)
for L in [1, 5, 10, 20, 50]:
    s2_ex = sigma2_GUE_exact(L)
    s2_r2 = sigma2_GUE_from_R2(L)
    print(f"{L:5d} {s2_ex:12.6f} {s2_r2:12.6f}")

# Now use Sigma_2 in the Dyson-Mehta integral:
# Delta_3(L) = (2/L^4) int_0^L (L^3 - 2L^2*r + r^3) Sigma_2(r) dr
def delta3_from_sigma2(L, sigma2_func, n_points=500):
    """Delta_3(L) = (2/L^4) int_0^L (L^3 - 2L^2*r + r^3) Sigma_2(r) dr"""
    r_vals = np.linspace(1e-6, L, n_points)
    s2_vals = np.array([sigma2_func(r) for r in r_vals])
    kernel = L**3 - 2*L**2*r_vals + r_vals**3
    integrand = kernel * s2_vals
    return (2.0 / L**4) * np.trapezoid(integrand, r_vals)

print(f"\nDelta_3 formula comparison:")
print(f"{'L':>5s} {'GUE_matrix':>12s} {'via_R2':>12s} {'via_S2':>12s}")
print("-" * 50)
for L in [5, 10, 20]:
    d3_matrix = d3_gue_mean.get(L, np.nan)
    d3_r2 = delta3_from_R2_v2(L, R2_GUE, n_points=20000)
    d3_s2 = delta3_from_sigma2(L, sigma2_GUE_exact, n_points=200)
    print(f"{L:5d} {d3_matrix:12.6f} {d3_r2:12.6f} {d3_s2:12.6f}")

# =============================================================================
# STEP 4: Check if the kernel in Delta_3-R2 formula should be different
# =============================================================================
print("\n" + "=" * 70)
print("STEP 4: Checking alternative kernels for Delta_3")
print("=" * 70)

# Possible correct formulas:
# (A) Delta_3(L) = L/15 + (2/L^4) int_0^L (L-r)^2 (2Lr-r^2) (R2(r)-1) dr  [Haake?]
# (B) Delta_3(L) = (2/L^4) int_0^L (L^3-2L^2r+r^3) Sigma_2(r) dr  [Mehta?]
# (C) Delta_3(L) = (1/L^4) int_0^L (L-r)^2 (2L^2+rL-r^2) (R2(r)-1+delta(r)) dr

# Since neither A nor B seems to work well, let me try other kernels numerically

# The key identity: from (B) and Sigma_2(r) = r + 2 int_0^r (r-s)(R2(s)-1)ds:
# Substituting into (B) should give the correct R2-based formula

# Let me just numerically fit the GUE ground truth to find the correct behavior

# Direct approach: compute pair correlation from GUE eigenvalues
print("\nComputing pair correlation from GUE eigenvalues...")

eigs = generate_gue_eigenvalues(500)
unfolded = unfold_semicircle(eigs, 500)
N_use = int(0.8 * 500)
start = int(0.1 * 500)
u = unfolded[start:start + N_use]
u = u - u[0]

# Compute Delta_3 directly at L=10 using the confirmed formula
L_test = 10.0
d3_direct = delta3_eigenvalues(u, L_test, n_offsets=100)
print(f"Direct Delta_3({L_test}) from single trial: {d3_direct:.6f}")

# Compare with R2 formula
d3_r2 = delta3_from_R2_v2(L_test, R2_GUE, n_points=20000)
print(f"R2 formula Delta_3({L_test}): {d3_r2:.6f}")
print(f"Ratio: {d3_r2/d3_direct:.4f}")

# =============================================================================
# STEP 5: Derive the correct kernel by numerical experimentation
# =============================================================================
print("\n" + "=" * 70)
print("STEP 5: Numerical kernel fitting")
print("=" * 70)

# If I know Delta_3(L) from matrices and Sigma_2(r) exactly,
# I can verify different kernel hypotheses.

# Let me compute Delta_3(L) for many L values using the matrix approach
# and compare with different formulas

# Also: the NUMBER VARIANCE Sigma_2 and SPECTRAL RIGIDITY Delta_3 are
# related by a double integral. But maybe the formula in the strategy
# notes is wrong. Let me try computing via K(tau) directly.

# The DIRECT formula from the form factor (Berry 1985, eq 5.8 or similar):
# Delta_3(L) = (L/15) - (1/(pi^2)) int_0^inf K(tau) h(pi*L*tau) / (tau^2) dtau
# where h(x) = [1 - cos(2x)] / x^2 - sin(2x)/x^3 + ... (some specific function)

# Actually, from Mehta's book (Random Matrices, 3rd edition), the relation is:
# Delta_3(L) = (2/L^4) int_0^L (L^3-2L^2r+r^3) Sigma_2(r) dr
# where Sigma_2(r) = (2/pi^2) int_0^inf K(tau)/tau^2 sin^2(pi*r*tau) dtau

# Let me verify this with VERY high accuracy quadrature

def sigma2_GUE_highprec(r):
    """High-precision Sigma_2 for GUE using scipy.integrate.quad"""
    if r < 1e-10:
        return 0.0
    def f1(tau):
        return np.sin(np.pi * r * tau)**2 / tau
    def f2(tau):
        return np.sin(np.pi * r * tau)**2 / tau**2
    p1, _ = scipy_quad(f1, 1e-15, 1.0, limit=500)
    p2, _ = scipy_quad(f2, 1.0, 1000.0, limit=500)
    return (2.0 / np.pi**2) * (p1 + p2)

print("\nHigh-precision Sigma_2 -> Delta_3 route:")
for L_test in [5, 10, 20]:
    # Compute Sigma_2 at many points
    n_r = 500
    r_vals = np.linspace(0.01, L_test, n_r)
    s2_vals = np.array([sigma2_GUE_highprec(r) for r in r_vals])

    # Apply Dyson-Mehta kernel
    kernel = L_test**3 - 2*L_test**2*r_vals + r_vals**3
    d3 = (2.0 / L_test**4) * np.trapezoid(kernel * s2_vals, r_vals)

    d3_matrix = d3_gue_mean.get(L_test, np.nan)
    print(f"  L={L_test:2d}: D3_via_S2 = {d3:.6f}, D3_matrix = {d3_matrix:.6f}, ratio = {d3/d3_matrix:.4f}")

print("\n\nDone.")
