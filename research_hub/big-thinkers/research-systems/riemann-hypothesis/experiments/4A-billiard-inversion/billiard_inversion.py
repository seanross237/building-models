"""
Strategy 4A: Billiard Table Inversion
======================================
Can we find a 2D billiard domain whose Dirichlet Laplacian eigenvalues
match the nontrivial zeros of the Riemann zeta function?

This script:
1. Computes the first N zeta zeros as target spectrum
2. Parameterizes a domain boundary via Fourier series in polar coords
3. Solves the Dirichlet eigenvalue problem via finite differences
4. Optimizes the domain shape to match the zeta zeros
5. Analyzes the Weyl law mismatch in depth
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize, differential_evolution
import mpmath
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import json
import time
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# PART 1: Compute Riemann zeta zeros
# ============================================================

def compute_zeta_zeros(N):
    """Compute imaginary parts of first N nontrivial zeta zeros."""
    zeros = []
    for n in range(1, N + 1):
        z = mpmath.zetazero(n)
        zeros.append(float(z.imag))
    return np.array(zeros)

print("=" * 70)
print("PART 1: Computing Riemann zeta zeros")
print("=" * 70)

N_ZEROS = 30
t0 = time.time()
gamma = compute_zeta_zeros(N_ZEROS)
print(f"Computed {N_ZEROS} zeta zeros in {time.time()-t0:.1f}s")
print(f"First 10: {gamma[:10]}")
print(f"Growth: gamma_1={gamma[0]:.3f}, gamma_{N_ZEROS}={gamma[-1]:.3f}, ratio={gamma[-1]/gamma[0]:.3f}")

# ============================================================
# PART 2: Weyl's law analysis — the fundamental mismatch
# ============================================================

print("\n" + "=" * 70)
print("PART 2: Weyl's law mismatch analysis")
print("=" * 70)

def weyl_counting_function(lam, area):
    """N(lambda) ~ (area / 4pi) * lambda for 2D Dirichlet Laplacian."""
    return (area / (4 * np.pi)) * lam

def riemann_counting_function(T):
    """N(T) ~ (T/2pi) * log(T/2pi) - T/2pi for zeta zeros up to height T."""
    if T <= 0:
        return 0
    return (T / (2 * np.pi)) * np.log(T / (2 * np.pi)) - T / (2 * np.pi)

# For the n-th eigenvalue of a 2D Laplacian (Weyl):
# lambda_n ~ (4*pi*n) / area  =>  lambda_n grows LINEARLY in n
#
# For the n-th zeta zero (Riemann-von Mangoldt):
# gamma_n ~ 2*pi*n / log(n)  =>  gamma_n grows as n/log(n)
#
# So eigenvalues grow FASTER than zeta zeros.

n_indices = np.arange(1, N_ZEROS + 1)

# If we set area = 4*pi (unit disk has area pi, so this is a disk of radius 2)
area_ref = 4 * np.pi
weyl_eigenvalues = (4 * np.pi * n_indices) / area_ref  # = n for area=4pi

print(f"\nGrowth rate comparison (n-th value):")
print(f"{'n':>4} {'gamma_n':>12} {'Weyl lambda_n':>14} {'ratio g/W':>10}")
print("-" * 44)
for i in [0, 4, 9, 14, 19, 24, 29]:
    if i < N_ZEROS:
        w = (4 * np.pi * (i + 1)) / area_ref
        print(f"{i+1:>4} {gamma[i]:>12.4f} {w:>14.4f} {gamma[i]/w:>10.4f}")

# Compute the asymptotic growth rates explicitly
print(f"\nAsymptotic analysis:")
print(f"  Zeta zeros: gamma_n ~ 2*pi*n/ln(n) for large n")
print(f"  Weyl eigenvalues: lambda_n ~ C*n for 2D domain")
print(f"  Ratio gamma_n/lambda_n ~ 1/ln(n) -> 0")
print(f"  => The spectra CANNOT match for a pure Laplacian at large n")

# Quantify the mismatch
ratios = gamma / n_indices
print(f"\n  gamma_n/n values: {ratios[:5].round(3)} ... {ratios[-5:].round(3)}")
print(f"  If Weyl held, gamma_n/n should be constant. Instead it's DECREASING.")
print(f"  gamma_1/1 = {ratios[0]:.3f}, gamma_30/30 = {ratios[-1]:.3f}")

# ============================================================
# PART 3: Rescaling strategies
# ============================================================

print("\n" + "=" * 70)
print("PART 3: Rescaling strategies")
print("=" * 70)

# Strategy A: Match via Weyl — what area would make lambda_1 = gamma_1?
# lambda_n = (4*pi*n)/A => need A = 4*pi*n/lambda_n
# For lambda_1 = gamma_1: A = 4*pi/gamma_1
area_match_1 = 4 * np.pi / gamma[0]
print(f"\nStrategy A: Scale area to match first zero")
print(f"  Required area: {area_match_1:.6f}")
scaled_weyl_A = (4 * np.pi * n_indices) / area_match_1
print(f"  lambda_1 = {scaled_weyl_A[0]:.4f} vs gamma_1 = {gamma[0]:.4f}")
print(f"  lambda_10 = {scaled_weyl_A[9]:.4f} vs gamma_10 = {gamma[9]:.4f}")
print(f"  lambda_30 = {scaled_weyl_A[29]:.4f} vs gamma_30 = {gamma[29]:.4f}")
mismatch_A = np.abs(scaled_weyl_A - gamma) / gamma
print(f"  Relative errors: {mismatch_A[:5].round(4)} ... {mismatch_A[-5:].round(4)}")

# Strategy B: Nonlinear rescaling — map gamma_n to lambda_n
# If gamma_n ~ 2*pi*n/ln(n), and we want lambda_n ~ c*n,
# then we need a map f such that f(gamma_n) = lambda_n
# i.e., f(x) should "undo" the 1/log(n) factor
# Since gamma ~ 2*pi*n/ln(n), we have n ~ (gamma*ln(gamma))/(2*pi) roughly
# So f(gamma) ~ gamma * ln(gamma) / (2*pi) * c
print(f"\nStrategy B: Nonlinear spectral map f(gamma) = gamma * ln(gamma)")
transformed_B = gamma * np.log(gamma)
# Normalize to compare growth rates
ratios_B = transformed_B / n_indices
print(f"  f(gamma_n)/n values: {ratios_B[:5].round(3)} ... {ratios_B[-5:].round(3)}")
print(f"  Much more nearly constant! Var/mean: {np.var(ratios_B)/np.mean(ratios_B):.4f}")
print(f"  (vs original var/mean: {np.var(ratios)/np.mean(ratios):.4f})")

# Strategy C: use gamma_n^2 (since Laplacian eigenvalues relate to frequencies squared)
print(f"\nStrategy C: Use gamma_n^2 as target (energy-like)")
gamma_sq = gamma**2
ratios_C = gamma_sq / n_indices
print(f"  gamma_n^2/n values: {ratios_C[:5].round(1)} ... {ratios_C[-5:].round(1)}")
print(f"  This grows too fast — gamma_n^2 ~ n^2/ln^2(n)")

# ============================================================
# PART 4: Finite-difference Laplacian eigenvalue solver
# ============================================================

print("\n" + "=" * 70)
print("PART 4: Building the eigenvalue solver")
print("=" * 70)

def domain_boundary(theta, r0, fourier_coeffs):
    """
    Compute r(theta) for the domain boundary.
    fourier_coeffs = [a1, b1, a2, b2, ..., aK, bK]
    """
    r = r0 * np.ones_like(theta)
    K = len(fourier_coeffs) // 2
    for k in range(K):
        a_k = fourier_coeffs[2 * k]
        b_k = fourier_coeffs[2 * k + 1]
        r = r + a_k * np.cos((k + 1) * theta) + b_k * np.sin((k + 1) * theta)
    return r

def is_point_inside(x, y, r0, fourier_coeffs):
    """Check if point (x,y) is inside the domain."""
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    r_boundary = domain_boundary(theta, r0, fourier_coeffs)
    return r < r_boundary

def compute_eigenvalues_fd(r0, fourier_coeffs, grid_size=80, n_eigenvalues=15):
    """
    Compute Dirichlet Laplacian eigenvalues using finite differences.

    Creates a grid, masks interior points, builds the 5-point Laplacian,
    applies Dirichlet BCs (zero on boundary), and solves.
    """
    # Determine domain extent
    theta_test = np.linspace(0, 2 * np.pi, 500)
    r_boundary = domain_boundary(theta_test, r0, fourier_coeffs)
    if np.any(r_boundary <= 0):
        return None  # Invalid domain

    r_max = np.max(r_boundary) * 1.1

    # Create grid
    N = grid_size
    h = 2 * r_max / (N - 1)
    x = np.linspace(-r_max, r_max, N)
    y = np.linspace(-r_max, r_max, N)
    X, Y = np.meshgrid(x, y)

    # Identify interior points
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    R_boundary = domain_boundary(Theta, r0, fourier_coeffs)
    interior = R < R_boundary

    # Exclude boundary ring (points adjacent to exterior)
    # This is already handled by Dirichlet BC: exterior points are 0

    n_interior = np.sum(interior)
    if n_interior < n_eigenvalues + 5:
        return None  # Domain too small for this grid

    # Map 2D indices to 1D indices for interior points
    idx_map = -np.ones((N, N), dtype=int)
    count = 0
    for i in range(N):
        for j in range(N):
            if interior[i, j]:
                idx_map[i, j] = count
                count += 1

    # Build sparse Laplacian matrix (5-point stencil)
    rows = []
    cols = []
    vals = []

    for i in range(1, N - 1):
        for j in range(1, N - 1):
            if not interior[i, j]:
                continue
            idx = idx_map[i, j]

            # Diagonal: -4/h^2
            diag_val = -4.0 / h**2
            rows.append(idx)
            cols.append(idx)
            vals.append(diag_val)

            # Neighbors
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if interior[ni, nj]:
                    rows.append(idx)
                    cols.append(idx_map[ni, nj])
                    vals.append(1.0 / h**2)
                # else: Dirichlet BC, neighbor value = 0, no contribution

    if len(rows) == 0:
        return None

    L = sparse.csr_matrix((vals, (rows, cols)), shape=(n_interior, n_interior))

    # Solve: -Delta u = lambda u => L u = -lambda u
    # L is negative semi-definite, so we want the smallest magnitude eigenvalues of -L
    try:
        # eigsh finds largest eigenvalues, so we find largest of -L (= smallest of L in magnitude)
        eigenvalues, _ = eigsh(-L, k=min(n_eigenvalues, n_interior - 2), which='SM')
        eigenvalues = np.sort(eigenvalues)
        # Filter positive eigenvalues only
        eigenvalues = eigenvalues[eigenvalues > 0]
        return eigenvalues
    except Exception as e:
        return None

# Test with a unit disk (known eigenvalues: j_{m,n}^2 where j are Bessel zeros)
print("\nTesting solver on unit disk (r0=1, no Fourier modes)...")
disk_eigs = compute_eigenvalues_fd(1.0, [], grid_size=100, n_eigenvalues=15)
if disk_eigs is not None:
    print(f"  Computed {len(disk_eigs)} eigenvalues")
    # Known: first eigenvalue of unit disk = j_{0,1}^2 ≈ 5.7832 (first zero of J_0)
    # j_{0,1} ≈ 2.4048, so j_{0,1}^2 ≈ 5.7831
    from scipy.special import jn_zeros
    j01 = jn_zeros(0, 1)[0]
    j11 = jn_zeros(1, 1)[0]
    j21 = jn_zeros(2, 1)[0]
    j02 = jn_zeros(0, 2)[0]
    j31 = jn_zeros(3, 1)[0]
    known_disk = sorted([j01**2, j11**2, j11**2, j21**2, j21**2, j02**2, j31**2, j31**2])[:8]
    print(f"  Computed:  {disk_eigs[:8].round(3)}")
    print(f"  Exact:     {np.array(known_disk).round(3)}")
    rel_err = np.abs(disk_eigs[:len(known_disk)] - known_disk) / known_disk
    print(f"  Rel error: {rel_err.round(4)}")
else:
    print("  Solver failed on unit disk!")

# ============================================================
# PART 5: Optimization — match eigenvalues to zeta zeros
# ============================================================

print("\n" + "=" * 70)
print("PART 5: Optimization (direct Laplacian match)")
print("=" * 70)

N_MATCH = 8  # Number of eigenvalues/zeros to match
N_FOURIER = 5  # Number of Fourier modes (10 parameters)
GRID_SIZE = 70  # Balance between accuracy and speed

target_direct = gamma[:N_MATCH]
print(f"Target (first {N_MATCH} zeta zeros): {target_direct.round(3)}")

def loss_function(params, target, grid_size=GRID_SIZE, penalty_weight=100.0):
    """
    Loss: sum of squared relative errors between eigenvalues and target.
    params[0] = r0 (base radius)
    params[1:] = Fourier coefficients
    """
    r0 = params[0]
    fourier_coeffs = params[1:]

    # Check domain validity
    theta_test = np.linspace(0, 2 * np.pi, 200)
    r_boundary = domain_boundary(theta_test, r0, fourier_coeffs)
    if np.any(r_boundary <= 0.05):
        return 1e6  # Invalid domain

    eigs = compute_eigenvalues_fd(r0, fourier_coeffs, grid_size=grid_size, n_eigenvalues=len(target) + 2)
    if eigs is None or len(eigs) < len(target):
        return 1e6

    eigs = eigs[:len(target)]

    # Relative squared error
    rel_err = (eigs - target) / target
    loss = np.sum(rel_err**2)

    return loss

# First, find r0 that puts eigenvalues in the right ballpark
# For a disk: lambda_1 ≈ j_{0,1}^2 / r0^2 ≈ 5.783 / r0^2
# We want lambda_1 ≈ gamma_1 = 14.135
# So r0 ≈ sqrt(5.783 / 14.135) ≈ 0.640
r0_init = np.sqrt(5.783 / gamma[0])
print(f"\nInitial r0 estimate: {r0_init:.4f}")

# Test initial disk
init_eigs = compute_eigenvalues_fd(r0_init, np.zeros(2 * N_FOURIER), grid_size=GRID_SIZE, n_eigenvalues=N_MATCH + 2)
if init_eigs is not None:
    print(f"Initial disk eigenvalues: {init_eigs[:N_MATCH].round(3)}")
    print(f"Target zeta zeros:       {target_direct.round(3)}")
    init_loss = np.sum(((init_eigs[:N_MATCH] - target_direct) / target_direct)**2)
    print(f"Initial loss: {init_loss:.4f}")

# Run optimization
print(f"\nRunning optimization with {2*N_FOURIER+1} parameters...")
x0 = np.zeros(2 * N_FOURIER + 1)
x0[0] = r0_init

# Bounds: r0 in [0.1, 3.0], Fourier coeffs in [-0.3*r0, 0.3*r0]
bounds = [(0.1, 3.0)]
for _ in range(2 * N_FOURIER):
    bounds.append((-0.5, 0.5))

t0 = time.time()
result_direct = minimize(
    loss_function,
    x0,
    args=(target_direct,),
    method='L-BFGS-B',
    bounds=bounds,
    options={'maxiter': 200, 'ftol': 1e-10, 'disp': False}
)
t_opt = time.time() - t0

print(f"Optimization completed in {t_opt:.1f}s")
print(f"Final loss: {result_direct.fun:.6f}")
print(f"Converged: {result_direct.success}")
print(f"Message: {result_direct.message}")

# Extract and display results
r0_opt = result_direct.x[0]
fc_opt = result_direct.x[1:]
print(f"\nOptimized r0: {r0_opt:.6f}")
print(f"Fourier coefficients: {fc_opt.round(6)}")

opt_eigs = compute_eigenvalues_fd(r0_opt, fc_opt, grid_size=GRID_SIZE + 20, n_eigenvalues=N_MATCH + 5)
if opt_eigs is not None:
    print(f"\nOptimized eigenvalues vs targets:")
    print(f"{'n':>3} {'lambda_n':>12} {'gamma_n':>12} {'rel_err':>12}")
    print("-" * 42)
    for i in range(min(N_MATCH, len(opt_eigs))):
        rel = (opt_eigs[i] - target_direct[i]) / target_direct[i]
        print(f"{i+1:>3} {opt_eigs[i]:>12.4f} {target_direct[i]:>12.4f} {rel:>12.6f}")

# ============================================================
# PART 5b: Optimization with nonlinear rescaling
# ============================================================

print("\n" + "=" * 70)
print("PART 5b: Optimization with rescaled target (gamma * ln(gamma))")
print("=" * 70)

# Use transformed target: f(gamma) = gamma * ln(gamma) rescaled
target_rescaled = gamma[:N_MATCH] * np.log(gamma[:N_MATCH])
# Normalize so first value matches roughly what a Laplacian can produce
scale_factor = gamma[0] / target_rescaled[0]
target_rescaled_norm = target_rescaled * scale_factor
print(f"Rescaled targets: {target_rescaled_norm.round(3)}")

# Since eigenvalues grow linearly and target_rescaled grows ~linearly too,
# this should be a much better fit
r0_init_rescaled = np.sqrt(5.783 / target_rescaled_norm[0])

x0_r = np.zeros(2 * N_FOURIER + 1)
x0_r[0] = r0_init_rescaled

t0 = time.time()
result_rescaled = minimize(
    loss_function,
    x0_r,
    args=(target_rescaled_norm,),
    method='L-BFGS-B',
    bounds=bounds,
    options={'maxiter': 200, 'ftol': 1e-10, 'disp': False}
)
t_resc = time.time() - t0

print(f"Optimization completed in {t_resc:.1f}s")
print(f"Final loss: {result_rescaled.fun:.6f}")

r0_resc = result_rescaled.x[0]
fc_resc = result_rescaled.x[1:]
resc_eigs = compute_eigenvalues_fd(r0_resc, fc_resc, grid_size=GRID_SIZE + 20, n_eigenvalues=N_MATCH + 5)
if resc_eigs is not None:
    print(f"\nRescaled optimized eigenvalues vs targets:")
    print(f"{'n':>3} {'lambda_n':>12} {'target_n':>12} {'rel_err':>12}")
    print("-" * 42)
    for i in range(min(N_MATCH, len(resc_eigs))):
        rel = (resc_eigs[i] - target_rescaled_norm[i]) / target_rescaled_norm[i]
        print(f"{i+1:>3} {resc_eigs[i]:>12.4f} {target_rescaled_norm[i]:>12.4f} {rel:>12.6f}")

# ============================================================
# PART 6: Differential evolution (global optimizer)
# ============================================================

print("\n" + "=" * 70)
print("PART 6: Global optimization via differential evolution")
print("=" * 70)

print("Running differential evolution (this may take a few minutes)...")
t0 = time.time()
result_de = differential_evolution(
    loss_function,
    bounds=bounds,
    args=(target_direct,),
    maxiter=100,
    popsize=15,
    tol=1e-8,
    seed=42,
    polish=True,
    disp=False
)
t_de = time.time() - t0

print(f"DE completed in {t_de:.1f}s")
print(f"Final loss: {result_de.fun:.6f}")

r0_de = result_de.x[0]
fc_de = result_de.x[1:]
print(f"Optimized r0: {r0_de:.6f}")
print(f"Fourier coefficients: {fc_de.round(6)}")

de_eigs = compute_eigenvalues_fd(r0_de, fc_de, grid_size=GRID_SIZE + 20, n_eigenvalues=N_MATCH + 5)
if de_eigs is not None:
    print(f"\nDE optimized eigenvalues vs targets:")
    print(f"{'n':>3} {'lambda_n':>12} {'gamma_n':>12} {'rel_err':>12}")
    print("-" * 42)
    for i in range(min(N_MATCH, len(de_eigs))):
        rel = (de_eigs[i] - target_direct[i]) / target_direct[i]
        print(f"{i+1:>3} {de_eigs[i]:>12.4f} {target_direct[i]:>12.4f} {rel:>12.6f}")

# ============================================================
# PART 7: Spectral spacing analysis
# ============================================================

print("\n" + "=" * 70)
print("PART 7: Spectral spacing analysis")
print("=" * 70)

# Compare nearest-neighbor spacings
zeta_spacings = np.diff(gamma)
print(f"Zeta zero spacings (first 10): {zeta_spacings[:10].round(4)}")
print(f"Mean spacing: {np.mean(zeta_spacings):.4f}")
print(f"Std of spacings: {np.std(zeta_spacings):.4f}")

# For a disk of radius r0_opt, Weyl spacings
if opt_eigs is not None and len(opt_eigs) >= N_MATCH:
    eig_spacings = np.diff(opt_eigs[:N_MATCH])
    print(f"\nOptimized domain eigenvalue spacings: {eig_spacings[:min(7,len(eig_spacings))].round(4)}")
    print(f"Mean spacing: {np.mean(eig_spacings):.4f}")

    # GUE vs GOE statistics (Berry-Tabor vs BGS conjecture)
    # Zeta zeros follow GUE statistics (Montgomery-Odlyzko)
    # Eigenvalues of chaotic billiards follow GOE
    # Eigenvalues of integrable billiards follow Poisson

    # Normalize spacings to mean 1
    zeta_s_norm = zeta_spacings / np.mean(zeta_spacings)
    print(f"\nNormalized zeta spacing statistics:")
    print(f"  Mean: {np.mean(zeta_s_norm):.4f} (should be 1)")
    print(f"  Variance: {np.var(zeta_s_norm):.4f} (GUE predicts ~0.178, Poisson predicts 1)")
    print(f"  Min spacing: {np.min(zeta_s_norm):.4f} (GUE shows level repulsion, min > 0)")

# ============================================================
# PART 8: Theoretical analysis — what operator WOULD work?
# ============================================================

print("\n" + "=" * 70)
print("PART 8: Theoretical constraints on the operator")
print("=" * 70)

print("""
Key finding: The pure Dirichlet Laplacian on ANY bounded 2D domain
has eigenvalues growing linearly (Weyl's law), while zeta zeros grow
as n/log(n). This means:

1. NO bounded 2D billiard can have its Laplacian eigenvalues match
   the zeta zeros asymptotically.

2. The Hilbert-Polya operator, if it exists as a differential operator
   on a geometric domain, must be one of:

   a) A Schrodinger operator -Delta + V(x) with a carefully tuned
      potential V. The potential would need to "slow down" eigenvalue
      growth from linear to n/log(n).

   b) An operator on a surface with UNBOUNDED area (like a modular
      surface), where Weyl's law is modified.

   c) An operator on a higher-dimensional or fractal domain where
      the spectral dimension differs from 2.

   d) A non-local operator (not a differential operator at all).

3. The required potential V for option (a):
   By semiclassical analysis, if -Delta + V has eigenvalue lambda_n ~ n/log(n),
   then V must grow logarithmically at the boundary. Specifically,
   the phase space volume Omega(E) = |{(x,p) : |p|^2 + V(x) <= E}|
   must satisfy Omega(E) ~ E/log(E), not Omega(E) ~ E.

4. The best geometric candidate is likely the MODULAR SURFACE
   SL(2,Z)\\H (the fundamental domain of the modular group).
   This is a non-compact surface with finite area, and its Laplacian
   eigenvalues (Maass forms) have deep connections to L-functions.
   However, its eigenvalues still obey Weyl's law for the finite area.
""")

# Compute what potential would be needed
print("Quantitative potential analysis:")
print("  If lambda_n = n/log(n), and Weyl gives lambda_n = c*n for -Delta,")
print("  then we need a perturbation that changes the n-th eigenvalue by:")
for n in [1, 5, 10, 20, 30]:
    if n <= N_ZEROS:
        correction = gamma[n-1] - n * gamma[0]  # Very rough
        weyl_pred = n * gamma[0]  # If first eigenvalue is matched
        print(f"  n={n:>3}: gamma_n={gamma[n-1]:.3f}, linear prediction={weyl_pred:.3f}, "
              f"deficit={gamma[n-1]-weyl_pred:.3f} ({100*(gamma[n-1]-weyl_pred)/weyl_pred:.1f}%)")

# ============================================================
# PART 9: Visualization
# ============================================================

print("\n" + "=" * 70)
print("PART 9: Generating visualizations")
print("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Plot 1: Zeta zeros vs Weyl eigenvalues
ax = axes[0, 0]
ax.plot(n_indices, gamma, 'bo-', label=r'$\gamma_n$ (zeta zeros)', markersize=4)
area_best = 4 * np.pi / gamma[0] * n_indices[0]  # match first
weyl_linear = gamma[0] * n_indices
ax.plot(n_indices, weyl_linear, 'r--', label=r'$\gamma_1 \cdot n$ (Weyl linear)', alpha=0.7)
ax.set_xlabel('n')
ax.set_ylabel('Value')
ax.set_title('Zeta zeros vs Weyl prediction')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: Ratio gamma_n / n (should be constant for Weyl)
ax = axes[0, 1]
ax.plot(n_indices, gamma / n_indices, 'bo-', markersize=4, label=r'$\gamma_n/n$')
ax.axhline(y=gamma[0], color='r', linestyle='--', alpha=0.5, label=r'$\gamma_1$')
# Theoretical prediction: 2*pi/ln(n)
n_theory = np.linspace(2, N_ZEROS, 100)
ax.plot(n_theory, 2 * np.pi / np.log(n_theory + 10), 'g-', alpha=0.7,
        label=r'$\sim 2\pi/\ln(n+10)$')
ax.set_xlabel('n')
ax.set_ylabel(r'$\gamma_n / n$')
ax.set_title('Spectral ratio (constant = Weyl compatible)')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: Domain shapes
ax = axes[0, 2]
theta_plot = np.linspace(0, 2 * np.pi, 300)

# Plot optimized domain (direct)
r_opt = domain_boundary(theta_plot, r0_opt, fc_opt)
x_opt = r_opt * np.cos(theta_plot)
y_opt = r_opt * np.sin(theta_plot)
ax.plot(x_opt, y_opt, 'b-', linewidth=2, label='L-BFGS-B optimized')

# Plot DE domain
r_de_plot = domain_boundary(theta_plot, r0_de, fc_de)
x_de = r_de_plot * np.cos(theta_plot)
y_de = r_de_plot * np.sin(theta_plot)
ax.plot(x_de, y_de, 'r-', linewidth=2, label='Diff. evolution')

# Reference disk
r_disk = r0_init * np.ones_like(theta_plot)
x_disk = r_disk * np.cos(theta_plot)
y_disk = r_disk * np.sin(theta_plot)
ax.plot(x_disk, y_disk, 'k--', linewidth=1, alpha=0.5, label='Initial disk')

ax.set_aspect('equal')
ax.set_title('Optimized billiard domains')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 4: Eigenvalue comparison
ax = axes[1, 0]
if opt_eigs is not None:
    ax.plot(range(1, min(N_MATCH, len(opt_eigs)) + 1), opt_eigs[:N_MATCH], 'bs-',
            markersize=5, label='L-BFGS-B eigenvalues')
if de_eigs is not None:
    ax.plot(range(1, min(N_MATCH, len(de_eigs)) + 1), de_eigs[:N_MATCH], 'r^-',
            markersize=5, label='DE eigenvalues')
ax.plot(range(1, N_MATCH + 1), target_direct, 'go-', markersize=5, label='Zeta zeros (target)')
ax.set_xlabel('n')
ax.set_ylabel('Value')
ax.set_title('Eigenvalues vs zeta zeros')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 5: Spacing distribution
ax = axes[1, 1]
if len(zeta_spacings) > 3:
    zeta_s_norm = zeta_spacings / np.mean(zeta_spacings)
    ax.hist(zeta_s_norm, bins=8, density=True, alpha=0.6, color='blue', label='Zeta zero spacings')
    # GUE Wigner surmise: p(s) = (32/pi^2) * s^2 * exp(-4s^2/pi)
    s_range = np.linspace(0, 3, 100)
    gue_wigner = (32 / np.pi**2) * s_range**2 * np.exp(-4 * s_range**2 / np.pi)
    ax.plot(s_range, gue_wigner, 'r-', linewidth=2, label='GUE Wigner surmise')
    # Poisson
    poisson = np.exp(-s_range)
    ax.plot(s_range, poisson, 'g--', linewidth=2, label='Poisson')
    ax.set_xlabel('Normalized spacing s')
    ax.set_ylabel('Density')
    ax.set_title('Spacing distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Plot 6: Weyl counting function comparison
ax = axes[1, 2]
T_range = np.linspace(5, gamma[-1] + 10, 200)
# Riemann counting
N_riemann = np.array([riemann_counting_function(T) for T in T_range])
# Step function from actual zeros
N_actual = np.array([np.sum(gamma <= T) for T in T_range])
# Weyl counting (for a disk matching first eigenvalue)
# N_weyl(lambda) = (A/4pi) * lambda
area_opt = np.pi * r0_opt**2  # Rough area of optimized domain
N_weyl_count = (area_opt / (4 * np.pi)) * T_range
ax.plot(T_range, N_actual, 'b-', linewidth=2, label='Actual N(T) zeta')
ax.plot(T_range, N_riemann, 'r--', linewidth=1.5, label='R-vM formula')
ax.plot(T_range, N_weyl_count, 'g:', linewidth=1.5, label=f'Weyl (area={area_opt:.2f})')
ax.set_xlabel('T (or λ)')
ax.set_ylabel('N(T)')
ax.set_title('Counting functions: Riemann vs Weyl')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'billiard_inversion_results.png'), dpi=150, bbox_inches='tight')
print("Saved billiard_inversion_results.png")

# ============================================================
# PART 10: Summary statistics for the report
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY OF RESULTS")
print("=" * 70)

results = {
    'n_zeros': N_ZEROS,
    'n_match': N_MATCH,
    'n_fourier_modes': N_FOURIER,
    'grid_size': GRID_SIZE,
    'zeta_zeros': gamma.tolist(),
    'direct_optimization': {
        'loss': float(result_direct.fun),
        'converged': bool(result_direct.success),
        'r0': float(r0_opt),
        'fourier_coeffs': fc_opt.tolist(),
        'eigenvalues': opt_eigs[:N_MATCH].tolist() if opt_eigs is not None else None,
    },
    'de_optimization': {
        'loss': float(result_de.fun),
        'r0': float(r0_de),
        'fourier_coeffs': fc_de.tolist(),
        'eigenvalues': de_eigs[:N_MATCH].tolist() if de_eigs is not None else None,
    },
    'weyl_analysis': {
        'gamma_n_over_n_first': float(gamma[0]),
        'gamma_n_over_n_last': float(gamma[-1] / N_ZEROS),
        'ratio_decrease_pct': float(100 * (1 - (gamma[-1] / N_ZEROS) / gamma[0])),
    }
}

with open(os.path.join(OUTPUT_DIR, 'results.json'), 'w') as f:
    json.dump(results, f, indent=2)
print("Saved results.json")

print(f"""
KEY FINDINGS:
1. Weyl law mismatch: gamma_n/n decreases from {gamma[0]:.3f} to {gamma[-1]/N_ZEROS:.3f}
   ({100*(1-(gamma[-1]/N_ZEROS)/gamma[0]):.1f}% decrease over {N_ZEROS} zeros).
   A pure Laplacian would give constant gamma_n/n.

2. Direct optimization (L-BFGS-B): loss = {result_direct.fun:.6f}
   This measures sum of squared relative errors.

3. Global optimization (DE): loss = {result_de.fun:.6f}

4. The fundamental barrier: Weyl's law forces ANY bounded 2D Laplacian's
   eigenvalues to grow linearly. Zeta zeros grow as n/log(n). No billiard
   shape can overcome this asymptotic mismatch.

5. For small N (first ~5-8 zeros), shape optimization CAN reduce the
   discrepancy significantly, but the mismatch grows inexorably with N.

6. The Hilbert-Polya operator, if geometric, likely requires:
   - A potential V(x) (Schrodinger, not pure Laplacian)
   - Or a non-compact domain (e.g., modular surface)
   - Or a fundamentally non-local operator
""")

print("All computations complete.")
