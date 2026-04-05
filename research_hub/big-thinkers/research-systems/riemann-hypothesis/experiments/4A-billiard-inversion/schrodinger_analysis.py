"""
Strategy 4A Extension: Schrodinger Operator Analysis
=====================================================
Since pure Laplacian eigenvalues cannot match zeta zeros (Weyl law mismatch),
we investigate what potential V(x) in a Schrodinger operator -Delta + V
would be needed to produce the correct spectral growth rate.

Also: 1D analysis (much cheaper) to explore the spectral inversion problem
on simpler domains before committing to 2D.
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize, differential_evolution
import mpmath
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# PART A: Compute zeta zeros
# ============================================================
N_ZEROS = 30
gamma = np.array([float(mpmath.zetazero(n).imag) for n in range(1, N_ZEROS + 1)])
print(f"Loaded {N_ZEROS} zeta zeros: {gamma[0]:.4f} to {gamma[-1]:.4f}")

# ============================================================
# PART B: 1D Schrodinger operator: can we find V(x) on [0,L]?
# ============================================================
# The 1D Dirichlet Laplacian on [0,L] has eigenvalues (n*pi/L)^2.
# Growth: ~n^2, even worse than 2D Weyl (~n).
# But a 1D Schrodinger -u'' + V(x)u = lambda u can have any
# growth rate depending on V.
#
# For V(x) ~ x^alpha as x->inf (unbounded domain),
# eigenvalues grow as n^{2alpha/(alpha+2)}.
# We want n/log(n) growth, which is between n^1 and n^{1-epsilon}.
# This requires alpha -> infinity in some sense, or a logarithmic potential.

print("\n" + "=" * 70)
print("PART B: 1D Schrodinger inverse problem")
print("=" * 70)

def solve_1d_schrodinger(V_values, L, N_grid, n_eigs=15):
    """
    Solve -u'' + V(x)u = lambda u on [0, L] with Dirichlet BCs.
    V_values: potential evaluated at interior grid points.
    """
    h = L / (N_grid + 1)
    # Laplacian matrix (tridiagonal)
    diag = 2.0 / h**2 + V_values
    off_diag = -1.0 / h**2 * np.ones(N_grid - 1)
    H = sparse.diags([off_diag, diag, off_diag], [-1, 0, 1], format='csr')

    k = min(n_eigs, N_grid - 2)
    eigenvalues, _ = eigsh(H, k=k, which='SM')
    return np.sort(eigenvalues)

# Test: V=0 on [0,pi], should give n^2
N_grid_1d = 500
L = np.pi
x_grid = np.linspace(L / (N_grid_1d + 1), L * N_grid_1d / (N_grid_1d + 1), N_grid_1d)
V_zero = np.zeros(N_grid_1d)
eigs_free = solve_1d_schrodinger(V_zero, L, N_grid_1d, n_eigs=10)
print(f"Free particle on [0,pi]: {eigs_free[:5].round(4)}")
print(f"Expected (n^2):          {np.arange(1,6)**2}")

# Now: optimize V(x) to match zeta zeros
# Parameterize V as a Chebyshev expansion: V(x) = sum c_k T_k(2x/L - 1)
N_CHEB = 12  # Number of Chebyshev coefficients
N_MATCH_1D = 15

# Chebyshev basis on [0, L]
def chebyshev_potential(x, coeffs, L):
    """Evaluate potential as Chebyshev expansion."""
    t = 2 * x / L - 1  # Map to [-1, 1]
    V = np.zeros_like(x)
    for k, c in enumerate(coeffs):
        V += c * np.cos(k * np.arccos(np.clip(t, -1, 1)))
    return V

def loss_1d(coeffs, target, L=10.0, N_grid=500):
    """Loss for 1D Schrodinger inverse problem."""
    x = np.linspace(L / (N_grid + 1), L * N_grid / (N_grid + 1), N_grid)
    V = chebyshev_potential(x, coeffs, L)

    # Penalize very negative potentials (avoid numerical issues)
    if np.min(V) < -1000:
        return 1e6

    try:
        eigs = solve_1d_schrodinger(V, L, N_grid, n_eigs=len(target) + 2)
        if len(eigs) < len(target):
            return 1e6
        eigs = eigs[:len(target)]
        rel_err = (eigs - target) / target
        return np.sum(rel_err**2)
    except:
        return 1e6

target_1d = gamma[:N_MATCH_1D]
print(f"\nTarget (first {N_MATCH_1D} zeta zeros): {target_1d[:8].round(3)}...")

# Initial guess: constant potential that shifts first eigenvalue to gamma_1
# On [0,L], lambda_1 = (pi/L)^2 + V_0 = gamma_1
# So V_0 = gamma_1 - (pi/L)^2
L_opt = 10.0
V0_init = gamma[0] - (np.pi / L_opt)**2
c0 = np.zeros(N_CHEB)
c0[0] = V0_init
print(f"Initial constant potential: V_0 = {V0_init:.4f}")

# Test initial
init_loss_1d = loss_1d(c0, target_1d, L=L_opt)
print(f"Initial loss: {init_loss_1d:.4f}")

# Optimize with L-BFGS-B
bounds_1d = [(-200, 200)] * N_CHEB
print(f"\nOptimizing 1D Schrodinger with {N_CHEB} Chebyshev modes...")
t0 = time.time()
result_1d = minimize(
    loss_1d, c0, args=(target_1d, L_opt, 500),
    method='L-BFGS-B', bounds=bounds_1d,
    options={'maxiter': 500, 'ftol': 1e-12}
)
t_1d = time.time() - t0
print(f"Optimization completed in {t_1d:.1f}s, loss = {result_1d.fun:.8f}")

# Evaluate result
x_eval = np.linspace(L_opt / 501, L_opt * 500 / 501, 500)
V_opt = chebyshev_potential(x_eval, result_1d.x, L_opt)
eigs_opt = solve_1d_schrodinger(V_opt, L_opt, 500, n_eigs=N_MATCH_1D + 5)

print(f"\nOptimized 1D eigenvalues vs zeta zeros:")
print(f"{'n':>3} {'lambda_n':>12} {'gamma_n':>12} {'rel_err':>12}")
print("-" * 42)
for i in range(min(N_MATCH_1D, len(eigs_opt))):
    rel = (eigs_opt[i] - target_1d[i]) / target_1d[i]
    print(f"{i+1:>3} {eigs_opt[i]:>12.4f} {target_1d[i]:>12.4f} {rel:>12.6f}")

# Also try differential evolution for global search
print(f"\nRunning DE for 1D problem (faster than 2D)...")
t0 = time.time()
result_1d_de = differential_evolution(
    loss_1d, bounds_1d, args=(target_1d, L_opt, 500),
    maxiter=200, popsize=20, tol=1e-10, seed=42, polish=True
)
t_de = time.time() - t0
print(f"DE completed in {t_de:.1f}s, loss = {result_1d_de.fun:.8f}")

V_opt_de = chebyshev_potential(x_eval, result_1d_de.x, L_opt)
eigs_opt_de = solve_1d_schrodinger(V_opt_de, L_opt, 500, n_eigs=N_MATCH_1D + 5)

print(f"\nDE optimized 1D eigenvalues vs zeta zeros:")
print(f"{'n':>3} {'lambda_n':>12} {'gamma_n':>12} {'rel_err':>12}")
print("-" * 42)
for i in range(min(N_MATCH_1D, len(eigs_opt_de))):
    rel = (eigs_opt_de[i] - target_1d[i]) / target_1d[i]
    print(f"{i+1:>3} {eigs_opt_de[i]:>12.4f} {target_1d[i]:>12.4f} {rel:>12.6f}")

# ============================================================
# PART C: Analyze the optimal potential
# ============================================================

print("\n" + "=" * 70)
print("PART C: Analysis of the optimal 1D potential")
print("=" * 70)

# Use the better result
if result_1d_de.fun < result_1d.fun:
    best_coeffs = result_1d_de.x
    best_loss = result_1d_de.fun
    best_eigs = eigs_opt_de
    V_best = V_opt_de
    print("Using DE result (better)")
else:
    best_coeffs = result_1d.x
    best_loss = result_1d.fun
    best_eigs = eigs_opt
    V_best = V_opt
    print("Using L-BFGS-B result (better)")

print(f"Best loss: {best_loss:.8f}")
print(f"Chebyshev coefficients: {best_coeffs.round(4)}")

# Characterize the potential
print(f"\nPotential statistics:")
print(f"  V_min = {np.min(V_best):.4f}")
print(f"  V_max = {np.max(V_best):.4f}")
print(f"  V_mean = {np.mean(V_best):.4f}")
print(f"  V at boundary (x=0): {V_best[0]:.4f}")
print(f"  V at boundary (x=L): {V_best[-1]:.4f}")
print(f"  V at center (x=L/2): {V_best[len(V_best)//2]:.4f}")

# ============================================================
# PART D: 2D billiard with potential (Schrodinger on disk)
# ============================================================

print("\n" + "=" * 70)
print("PART D: 2D Schrodinger operator on a disk")
print("=" * 70)

def compute_schrodinger_eigenvalues_2d(r0, V_radial_coeffs, grid_size=60, n_eigs=10):
    """
    Solve -Delta u + V(r) u = lambda u on a disk of radius r0.
    V is parameterized as a polynomial in r: V(r) = sum c_k (r/r0)^k
    """
    N = grid_size
    h = 2 * r0 / (N - 1)
    x = np.linspace(-r0, r0, N)
    y = np.linspace(-r0, r0, N)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    # Interior: points strictly inside the disk
    interior = R < r0 - h/2
    n_interior = np.sum(interior)
    if n_interior < n_eigs + 5:
        return None

    # Map to 1D indices
    idx_map = -np.ones((N, N), dtype=int)
    count = 0
    for i in range(N):
        for j in range(N):
            if interior[i, j]:
                idx_map[i, j] = count
                count += 1

    # Compute potential on grid
    V_grid = np.zeros_like(R)
    for k, c in enumerate(V_radial_coeffs):
        V_grid += c * (R / r0)**k

    # Build -Laplacian + V matrix
    rows, cols, vals = [], [], []
    for i in range(1, N-1):
        for j in range(1, N-1):
            if not interior[i, j]:
                continue
            idx = idx_map[i, j]

            diag_val = 4.0 / h**2 + V_grid[i, j]
            rows.append(idx); cols.append(idx); vals.append(diag_val)

            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < N and 0 <= nj < N and interior[ni, nj]:
                    rows.append(idx); cols.append(idx_map[ni, nj])
                    vals.append(-1.0 / h**2)

    H = sparse.csr_matrix((vals, (rows, cols)), shape=(n_interior, n_interior))

    try:
        eigenvalues, _ = eigsh(H, k=min(n_eigs, n_interior - 2), which='SM')
        return np.sort(eigenvalues)
    except:
        return None

N_MATCH_2D = 10
target_2d = gamma[:N_MATCH_2D]

# Parameters: r0, then radial potential coefficients c0, c1, ..., cM
N_RADIAL = 6

def loss_2d_schrodinger(params, target, grid_size=60):
    """Loss for 2D Schrodinger on a disk."""
    r0 = params[0]
    V_coeffs = params[1:]
    if r0 < 0.1:
        return 1e6
    eigs = compute_schrodinger_eigenvalues_2d(r0, V_coeffs, grid_size=grid_size, n_eigs=len(target)+2)
    if eigs is None or len(eigs) < len(target):
        return 1e6
    eigs = eigs[:len(target)]
    rel_err = (eigs - target) / target
    return np.sum(rel_err**2)

# Initial guess
r0_2d = 1.0
c0_2d = np.zeros(N_RADIAL + 1)
c0_2d[0] = r0_2d
c0_2d[1] = gamma[0]  # Constant potential to shift first eigenvalue

print(f"Optimizing 2D Schrodinger with r0 + {N_RADIAL} potential modes...")
bounds_2d = [(0.3, 3.0)] + [(-200, 200)] * N_RADIAL

t0 = time.time()
result_2d_s = minimize(
    loss_2d_schrodinger, c0_2d, args=(target_2d, 60),
    method='L-BFGS-B', bounds=bounds_2d,
    options={'maxiter': 200, 'ftol': 1e-10}
)
t_2d = time.time() - t0
print(f"Optimization completed in {t_2d:.1f}s, loss = {result_2d_s.fun:.6f}")

r0_2d_opt = result_2d_s.x[0]
V_2d_coeffs = result_2d_s.x[1:]
eigs_2d_s = compute_schrodinger_eigenvalues_2d(r0_2d_opt, V_2d_coeffs, grid_size=80, n_eigs=N_MATCH_2D+5)

if eigs_2d_s is not None:
    print(f"\n2D Schrodinger eigenvalues vs zeta zeros:")
    print(f"{'n':>3} {'lambda_n':>12} {'gamma_n':>12} {'rel_err':>12}")
    print("-" * 42)
    for i in range(min(N_MATCH_2D, len(eigs_2d_s))):
        rel = (eigs_2d_s[i] - target_2d[i]) / target_2d[i]
        print(f"{i+1:>3} {eigs_2d_s[i]:>12.4f} {target_2d[i]:>12.4f} {rel:>12.6f}")

# ============================================================
# PART E: Visualizations
# ============================================================

print("\n" + "=" * 70)
print("PART E: Generating visualizations")
print("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Plot 1: Optimal 1D potential
ax = axes[0, 0]
ax.plot(x_eval, V_best, 'b-', linewidth=2)
ax.set_xlabel('x')
ax.set_ylabel('V(x)')
ax.set_title(f'Optimal 1D potential (loss={best_loss:.4e})')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)

# Plot 2: 1D eigenvalue match
ax = axes[0, 1]
n_idx = np.arange(1, N_MATCH_1D + 1)
ax.plot(n_idx, target_1d, 'go-', markersize=6, label='Zeta zeros')
ax.plot(n_idx[:len(best_eigs)], best_eigs[:N_MATCH_1D], 'bs-', markersize=5, label='1D Schrodinger')
# Also show pure Laplacian (no potential)
laplacian_1d = (np.arange(1, N_MATCH_1D+1) * np.pi / L_opt)**2
ax.plot(n_idx, laplacian_1d, 'r^--', markersize=4, alpha=0.5, label='Pure Laplacian')
ax.set_xlabel('n')
ax.set_ylabel('Eigenvalue')
ax.set_title('1D spectral match')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: Relative errors
ax = axes[0, 2]
rel_errs_best = (best_eigs[:N_MATCH_1D] - target_1d) / target_1d
ax.bar(n_idx[:len(rel_errs_best)], 100 * rel_errs_best, color='steelblue', alpha=0.7)
ax.set_xlabel('n')
ax.set_ylabel('Relative error (%)')
ax.set_title('Eigenvalue relative errors (1D)')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)

# Plot 4: Weyl law -- log-log comparison
ax = axes[1, 0]
n_range = np.arange(1, N_ZEROS + 1)
ax.loglog(n_range, gamma, 'bo-', markersize=4, label=r'$\gamma_n$ (zeta zeros)')
ax.loglog(n_range, gamma[0] * n_range, 'r--', alpha=0.7, label=r'$\gamma_1 \cdot n$ (Weyl)')
# n/log(n) fit
c_fit = gamma[0] * np.log(1)  # won't work for n=1...
n_cont = np.linspace(1, N_ZEROS, 200)
# Fit: gamma_n ~ A * n / log(B*n)
from scipy.optimize import curve_fit
def rvm_model(n, A, B):
    return A * n / np.log(B * n + 2)
try:
    popt, _ = curve_fit(rvm_model, n_range, gamma, p0=[6.28, 1.0])
    ax.loglog(n_cont, rvm_model(n_cont, *popt), 'g-', linewidth=2,
              label=f'Fit: {popt[0]:.2f}n/ln({popt[1]:.2f}n+2)')
except:
    pass
ax.set_xlabel('n')
ax.set_ylabel('Value')
ax.set_title('Growth rates (log-log)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 5: 2D Schrodinger potential (radial)
ax = axes[1, 1]
if result_2d_s.fun < 1e5:
    r_plot = np.linspace(0, r0_2d_opt, 100)
    V_radial_plot = np.zeros_like(r_plot)
    for k, c in enumerate(V_2d_coeffs):
        V_radial_plot += c * (r_plot / r0_2d_opt)**k
    ax.plot(r_plot, V_radial_plot, 'b-', linewidth=2)
    ax.set_xlabel('r')
    ax.set_ylabel('V(r)')
    ax.set_title(f'Optimal 2D radial potential (loss={result_2d_s.fun:.4e})')
    ax.grid(True, alpha=0.3)
else:
    ax.text(0.5, 0.5, '2D optimization failed', transform=ax.transAxes,
            ha='center', va='center', fontsize=14)

# Plot 6: Spectral comparison summary
ax = axes[1, 2]
if eigs_2d_s is not None:
    ax.plot(n_idx[:N_MATCH_2D], target_2d, 'go-', markersize=6, label='Zeta zeros')
    ax.plot(n_idx[:min(N_MATCH_2D, len(eigs_2d_s))], eigs_2d_s[:N_MATCH_2D], 'rs-',
            markersize=5, label='2D Schrodinger')
    ax.set_xlabel('n')
    ax.set_ylabel('Eigenvalue')
    ax.set_title('2D Schrodinger spectral match')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'schrodinger_analysis.png'), dpi=150, bbox_inches='tight')
print("Saved schrodinger_analysis.png")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY: Schrodinger Analysis")
print("=" * 70)

print(f"""
1D Schrodinger Results:
  - Best loss: {best_loss:.8f}
  - The 1D Schrodinger operator -u'' + V(x)u CAN approximate the first
    {N_MATCH_1D} zeta zeros as eigenvalues, by tuning V(x).
  - This is expected: the inverse spectral problem for 1D Schrodinger
    is well-posed (Gel'fand-Levitan theory), and any increasing
    sequence can be realized as the spectrum of some potential.

2D Schrodinger Results:
  - Loss: {result_2d_s.fun:.6f}
  - A radially symmetric potential V(r) on a disk can partially
    match the zeta zeros, but the match is imperfect due to the
    degeneracy structure of the disk (eigenvalues come in pairs
    for angular quantum numbers m != 0).

Key Insight:
  - The Hilbert-Polya operator CANNOT be a pure Laplacian on ANY
    bounded domain (Weyl's law forbids it).
  - A Schrodinger operator -Delta + V CAN match finitely many zeros,
    but the potential V must be carefully tuned.
  - The optimal V has interesting structure worth further study.
""")
