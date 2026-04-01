"""
delta3_integral_correct.py
==========================
Implement the CORRECT Dyson-Mehta Δ₃ formula using integral of staircase.

The Dyson-Mehta Δ₃ is:
   Δ₃(L) = (1/L) min_{a,b} ∫₀^L [N(x) - ax - b]² dx

where N(x) is the counting function (staircase), NOT a sum at eigenvalue positions.

This is DIFFERENT from the sum formula:
   Δ₃_sum = (1/L) Σᵢ [kᵢ - a*xᵢ - b]²

We implement both and compare on test cases.
"""

import numpy as np
from numpy.random import default_rng

rng = default_rng(42)

# ─── Integral version of Δ₃ ───────────────────────────────────────────────────

def delta3_integral_analytic(ys_in_window, L):
    """
    Compute Δ₃(L) using the INTEGRAL formula analytically.

    For eigenvalues y₁ < ... < yₙ in [0, L]:
      N(x) = k for y_k ≤ x < y_{k+1}  (where y₀=0, y_{n+1}=L)

    Δ₃(L) = (1/L) × [I₂ - I₀²/L - 12(I₁ - I₀L/2)²/L³]

    where:
      I₀ = ∫₀^L N(x)dx = n*L - Σy_k
      I₁ = ∫₀^L x*N(x)dx = n*L²/2 - (1/2)*Σy_k²
      I₂ = ∫₀^L N(x)²dx = n²*L - Σ(2k-1)*y_k
    """
    ys = np.sort(ys_in_window)
    n = len(ys)
    if n < 2:
        return np.nan

    k = np.arange(1, n + 1, dtype=float)  # ranks 1, 2, ..., n

    I0 = n * L - np.sum(ys)
    I1 = n * L**2 / 2 - np.sum(ys**2) / 2
    I2 = n**2 * L - np.sum((2*k - 1) * ys)

    F_min = I2 - I0**2 / L - 12 * (I1 - I0 * L / 2)**2 / L**3
    return F_min / L


def delta3_sum(ys_in_window, L, E_start=0):
    """
    Compute Δ₃ using sum formula (NOT the correct Dyson-Mehta formula).
    Included for comparison only.
    """
    ys = np.sort(ys_in_window)
    n = len(ys)
    if n < 3:
        return np.nan

    ranks = np.arange(1, n + 1, dtype=float)
    xs = ys  # already shifted to [0, L]

    A = np.column_stack([xs, np.ones(n)])
    result = np.linalg.lstsq(A, ranks, rcond=None)
    a, b = result[0]
    residuals = ranks - (a * xs + b)
    return np.sum(residuals**2) / L


def delta3_avg(eigenvalues, L, n_windows=300, formula='integral'):
    """Average Δ₃(L) over many windows."""
    xmin, xmax = eigenvalues[0], eigenvalues[-1]
    valid_start = xmin
    valid_end = xmax - L
    if valid_start >= valid_end:
        return np.nan

    starts = np.linspace(valid_start, valid_end, n_windows)
    vals = []
    for s in starts:
        mask = (eigenvalues >= s) & (eigenvalues < s + L)
        ys = eigenvalues[mask] - s  # shift to [0, L]
        if len(ys) < 3:
            continue
        if formula == 'integral':
            v = delta3_integral_analytic(ys, L)
        else:
            v = delta3_sum(ys, L)
        if not np.isnan(v):
            vals.append(v)

    return np.mean(vals) if vals else np.nan


# ─── Test on known distributions ──────────────────────────────────────────────
print("=" * 70)
print("TEST 1: Poisson (IID uniform points)")
print("  Expected Δ₃(L) = L/15")
print("=" * 70)

# Generate Poisson process: IID uniform on [0, 1000] with density 1
N_poisson = 1000
poisson_pts = np.sort(rng.uniform(0, N_poisson, N_poisson))

for L in [5, 10, 15, 20, 30]:
    d3_int = delta3_avg(poisson_pts, L, formula='integral')
    d3_sum = delta3_avg(poisson_pts, L, formula='sum')
    expected = L / 15.0
    print(f"L={L:5.1f}: integral={d3_int:.4f}, sum={d3_sum:.5f}, expected={expected:.4f}")

print()
print("=" * 70)
print("TEST 2: Regular lattice (perfectly spaced)")
print("  Expected Δ₃(L) ≈ 0")
print("=" * 70)

lattice_pts = np.arange(0.5, 1000.5, 1.0)  # exactly spaced by 1

for L in [5, 10, 15, 20, 30]:
    d3_int = delta3_avg(lattice_pts, L, formula='integral')
    d3_sum = delta3_avg(lattice_pts, L, formula='sum')
    print(f"L={L:5.1f}: integral={d3_int:.6f}, sum={d3_sum:.8f}")

print()
print("=" * 70)
print("TEST 3: GUE random matrix eigenvalues (unfolded)")
print("  Expected Δ₃(L) ≈ (1/π²)[log(2πL) + γ + 1 - π²/8]")
print("=" * 70)

# Generate unfolded GUE eigenvalues
# Use a large GUE matrix and unfold
try:
    # Generate GUE matrix
    n_gue = 1000
    H = rng.standard_normal((n_gue, n_gue))
    H = (H + H.T) / np.sqrt(2)
    eigs = np.linalg.eigvalsh(H)
    # Unfold: the Wigner semicircle density for GUE is ρ(E) = sqrt(4N-E²)/(2πN) approximately
    # Use the empirical unfolding (sort + rank/N → N_smooth)
    from scipy.interpolate import interp1d
    n_sorted = np.arange(1, n_gue + 1)
    # Fit smooth cumulative
    from numpy.polynomial import polynomial as P
    # Simple unfolding: use empirical CDF
    eigs_sorted = np.sort(eigs)
    # Theoretical: Wigner semicircle CDF
    a_wigner = 2 * np.sqrt(n_gue)
    def wigner_cdf(x):
        t = x / a_wigner
        t = np.clip(t, -1, 1)
        return n_gue * (0.5 + t * np.sqrt(1 - t**2) / np.pi + np.arcsin(t) / np.pi)
    unfolded_gue = wigner_cdf(eigs_sorted)
    # Take middle 80% for clean statistics
    i_start = int(0.1 * n_gue)
    i_end = int(0.9 * n_gue)
    unfolded_gue_center = unfolded_gue[i_start:i_end]
    # Renormalize to mean spacing = 1
    mean_sp = np.mean(np.diff(unfolded_gue_center))
    unfolded_gue_center = unfolded_gue_center / mean_sp

    gamma_E = 0.5772156649
    def delta3_GUE_asymptotic(L):
        return (1.0/np.pi**2) * (np.log(2*np.pi*L) + gamma_E + 1.0 - np.pi**2/8.0)

    for L in [5, 10, 15, 20, 30]:
        d3_int = delta3_avg(unfolded_gue_center, L, n_windows=300, formula='integral')
        d3_sum = delta3_avg(unfolded_gue_center, L, n_windows=300, formula='sum')
        expected = delta3_GUE_asymptotic(L)
        print(f"L={L:5.1f}: integral={d3_int:.4f}, sum={d3_sum:.5f}, expected_asymptotic={expected:.4f}")

except Exception as e:
    print(f"GUE test failed: {e}")

# ─── Now apply to Riemann zeros ───────────────────────────────────────────────
print()
print("=" * 70)
print("MAIN: Δ₃ for Riemann zeta zeros (unfolded, integral formula)")
print("=" * 70)

zeros = np.load('../../exploration-003/code/zeta_zeros_2000.npy')
N_zeros = len(zeros)

def N_smooth(T):
    x = T / (2.0 * np.pi)
    return x * np.log(x) - x + 7.0/8.0

unfolded = N_smooth(zeros)
print(f"Loaded {N_zeros} zeros, unfolded range: [{unfolded[0]:.2f}, {unfolded[-1]:.2f}]")

L_values = [2, 3, 5, 7, 10, 12, 15, 17, 20, 25, 30, 40, 50]

print(f"\n{'L':>6}  {'Δ₃_int':>10}  {'Δ₃_sum':>10}  {'Δ₃_GUE':>10}")
print("-" * 44)

results = {}
for L in L_values:
    d3_int = delta3_avg(unfolded, L, n_windows=300, formula='integral')
    d3_sum = delta3_avg(unfolded, L, n_windows=300, formula='sum')
    d3_gue = delta3_GUE_asymptotic(L)
    results[L] = {'integral': d3_int, 'sum': d3_sum, 'gue': d3_gue}
    print(f"{L:6.1f}  {d3_int:10.5f}  {d3_sum:10.5f}  {d3_gue:10.5f}")

# Find saturation level (L > 15)
large_L_vals = [L for L in L_values if L >= 15]
sat_int = np.mean([results[L]['integral'] for L in large_L_vals])
sat_sum = np.mean([results[L]['sum'] for L in large_L_vals])
print(f"\nSaturation (L ≥ 15): integral={sat_int:.4f}, sum={sat_sum:.4f}")
print(f"Previously reported (strategy-001): 0.156")
print(f"GUE at L=15: {delta3_GUE_asymptotic(15):.4f}")

np.savez('delta3_both_formulas.npz',
         L_values=L_values,
         results_integral=[results[L]['integral'] for L in L_values],
         results_sum=[results[L]['sum'] for L in L_values],
         results_gue=[results[L]['gue'] for L in L_values])
print("\nSaved to delta3_both_formulas.npz")
