"""
Diagnose Δ₃ formula more carefully.

The staircase function N(x) must be integrated, not just sampled at eigenvalue positions.
Sampling at eigenvalue positions misses the flat segments between jumps.

This script tests the proper staircase integration approach.

GUE theoretical Δ₃(L) ≈ (1/(2π²)) × (ln(2πL) + γ - 5/4) for large L.
At L=25: ≈ 0.222; at L=50: ≈ 0.258; mean ≈ 0.24
"""
import numpy as np

def build_gue_matrix(N, rng):
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    H = (A + A.conj().T) / np.sqrt(2 * N)
    return H

def unfold_spectrum(eigenvalues, poly_degree=7):
    N = len(eigenvalues)
    eigs_sorted = np.sort(eigenvalues)
    cumulative = np.arange(1, N+1, dtype=float)
    coeffs = np.polyfit(eigs_sorted, cumulative, poly_degree)
    unfolded = np.polyval(coeffs, eigs_sorted)
    return unfolded

def compute_delta3_staircase(eigenvalues, L_max=50, n_windows=100, n_grid=500):
    """
    Proper Δ₃ via staircase integration.
    Evaluates N(t) on a fine grid, then fits line and integrates.
    """
    N = len(eigenvalues)
    L_values = np.linspace(1, L_max, 50)
    delta3 = np.zeros(len(L_values))

    step = max(1, int(N / n_windows))

    for i, L in enumerate(L_values):
        vals = []
        for start_idx in range(0, N - int(L * 2), step):
            x0 = eigenvalues[start_idx]
            x1 = x0 + L
            # Fine grid in [x0, x1]
            t_grid = np.linspace(x0, x1, n_grid)
            # Staircase: N(t) = number of eigenvalues <= t
            # Efficient: searchsorted
            N_grid = np.searchsorted(eigenvalues, t_grid, side='right').astype(float)
            t_shifted = t_grid - x0  # in [0, L]
            # Least-squares fit: N_grid ~ A*t + B
            A_mat = np.column_stack([t_shifted, np.ones(n_grid)])
            coeffs2, _, _, _ = np.linalg.lstsq(A_mat, N_grid, rcond=None)
            A_fit, B_fit = coeffs2
            res = N_grid - A_fit * t_shifted - B_fit
            # Integrate: (1/L) * trapz(res**2, t_shifted)
            d3_val = np.trapz(res**2, t_shifted) / L
            vals.append(d3_val)
        delta3[i] = np.mean(vals) if vals else np.nan

    return L_values, delta3

def compute_delta3_exact_staircase(eigenvalues, L_max=50, n_windows=100):
    """
    Exact Δ₃ via analytical integration of the piecewise-linear residuals.
    Uses the fact that N(t) is constant between consecutive eigenvalues.
    After the optimal (A,B) fit, integrates residuals analytically.
    """
    N = len(eigenvalues)
    L_values = np.linspace(1, L_max, 50)
    delta3 = np.zeros(len(L_values))

    step = max(1, int(N / n_windows))

    for i, L in enumerate(L_values):
        vals = []
        for start_idx in range(0, N - int(L*2), step):
            x0 = eigenvalues[start_idx]
            x1 = x0 + L
            # Eigenvalues in window
            mask = (eigenvalues >= x0) & (eigenvalues <= x1)
            eigs_in = eigenvalues[mask]
            n_in = len(eigs_in)
            if n_in < 3:
                continue

            # Build breakpoints for staircase in shifted [0, L] coords
            # Staircase: at t in [eigs_in[j]-x0, eigs_in[j+1]-x0), N(t) = j+1
            # Including boundary effects: before first eig and after last eig

            # Grid of staircase breakpoints: x0, eigs_in[0], ..., eigs_in[-1], x1
            breaks = np.concatenate([[x0], eigs_in, [x1]]) - x0  # shifted
            # N values in each segment: 0, 1, 2, ..., n_in
            N_vals = np.arange(0, n_in+1, dtype=float)  # N(t) in each segment

            # Least-squares fit: minimize ∫₀ᴸ [N(t) - At - B]² dt
            # = Σⱼ ∫_{bⱼ}^{bⱼ₊₁} [nⱼ - At - B]² dt
            # Each piece ∫_a^b [c - At - B]² dt = (b-a)[(c-B-A(a+b)/2)² + A²(b-a)²/12]
            # We need to minimize over A, B.
            # Equivalently: set up normal equations.

            # For minimization: ∂/∂B = 0, ∂/∂A = 0
            # ∫[N(t) - At - B]² dt = ∫N² - 2∫N(At+B) + ∫(At+B)²
            # → ∫N dt = A∫t dt + B∫dt   (from ∂/∂B = 0)
            # → ∫Nt dt = A∫t² dt + B∫t dt  (from ∂/∂A = 0)

            # Compute needed integrals analytically over each piece
            I0 = 0.0  # ∫ 1 dt = L
            I1 = 0.0  # ∫ t dt
            I2 = 0.0  # ∫ t² dt
            IN = 0.0  # ∫ N(t) dt
            INt = 0.0  # ∫ N(t)*t dt

            for j in range(len(breaks)-1):
                a, b = breaks[j], breaks[j+1]
                n = N_vals[j]
                dt = b - a
                I0 += dt
                I1 += (b**2 - a**2) / 2
                I2 += (b**3 - a**3) / 3
                IN += n * dt
                INt += n * (b**2 - a**2) / 2

            # Normal equations: [I2, I1] [A]   [INt]
            #                   [I1, I0] [B] = [IN ]
            det = I2*I0 - I1**2
            if abs(det) < 1e-12:
                continue
            A_fit = (I0*INt - I1*IN) / det
            B_fit = (I2*IN - I1*INt) / det

            # Now compute ∫₀ᴸ [N(t) - At - B]² dt analytically
            integral = 0.0
            for j in range(len(breaks)-1):
                a, b = breaks[j], breaks[j+1]
                n = N_vals[j]
                # ∫_a^b [n - At - B]² dt = ∫_a^b [c - At]² dt where c = n - B
                # = ∫_a^b [c² - 2cAt + A²t²] dt
                c = n - B_fit
                dt = b - a
                integral += c**2 * dt - 2*c*A_fit*(b**2-a**2)/2 + A_fit**2*(b**3-a**3)/3

            vals.append(integral / L)

        delta3[i] = np.mean(vals) if vals else np.nan

    return L_values, delta3

# GUE theoretical prediction
def gue_theory(L):
    """GUE Δ₃(L) theoretical formula (large L)."""
    import math
    gamma_euler = 0.5772156649
    return (1 / (2 * math.pi**2)) * (np.log(2 * math.pi * L) + gamma_euler - 5/4)

N = 500
print(f"Testing Δ₃ formulas with GUE N={N}")

rng = np.random.default_rng(999)
H = build_gue_matrix(N, rng)
eigs = np.linalg.eigvalsh(H)
unfolded = unfold_spectrum(np.sort(eigs))

# GUE theoretical predictions
L_test = np.array([10, 25, 35, 50])
print("\nGUE theoretical Δ₃(L):")
for L in L_test:
    print(f"  L={L}: Δ₃ = {gue_theory(L):.4f}")
print(f"  Δ₃_sat (mean L=25-50) ≈ {np.mean([gue_theory(L) for L in range(25,51)]):.4f}")

print("\nRunning staircase integration...")
import time
t0 = time.time()
L_values, d3_staircase = compute_delta3_staircase(unfolded, n_grid=500, n_windows=100)
print(f"  Staircase (grid=500): {time.time()-t0:.1f}s")

t0 = time.time()
L_values, d3_exact = compute_delta3_exact_staircase(unfolded, n_windows=100)
print(f"  Exact staircase: {time.time()-t0:.1f}s")

sat_mask = L_values >= 25
staircase_sat = float(np.nanmean(d3_staircase[sat_mask]))
exact_sat = float(np.nanmean(d3_exact[sat_mask]))
theory_sat = np.mean([gue_theory(L) for L in L_values[sat_mask]])

print(f"\nΔ₃_sat comparison (L=25-50):")
print(f"  GUE theory:           {theory_sat:.4f}")
print(f"  Staircase grid 500:   {staircase_sat:.4f}")
print(f"  Exact staircase:      {exact_sat:.4f}")
print(f"  GOAL formula (buggy): ~0.0041")
print(f"  Corrected (no /L):    ~0.1487")

print("\nL-dependent Δ₃:")
print(f"{'L':>6} {'Theory':>10} {'Staircase':>12} {'Exact':>10}")
for i, L in enumerate(L_values[::5]):
    idx = i*5
    print(f"{L:>6.1f} {gue_theory(L):>10.4f} {d3_staircase[idx]:>12.4f} {d3_exact[idx]:>10.4f}")
