"""
Diagnose Δ₃ formula scaling issue.

The GOAL.md formula uses: np.mean(residuals**2) / L
Standard Δ₃ definition: (1/L) ∫[N(t) - At - B]² dt

For unit-density unfolded eigenvalues:
- n_in ≈ L points in window
- (1/L) ∫ ≈ (n_in/L) × mean(residuals²) ≈ mean(residuals²)
So the /L in the GOAL formula makes values ~L times too small.

This script tests both formulas to confirm.
"""
import numpy as np
from math import gamma

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

def compute_delta3_goal_formula(eigenvalues, L_max=50, n_windows=200):
    """Exact GOAL.md formula (with /L bug)."""
    N = len(eigenvalues)
    L_values = np.linspace(1, L_max, 50)
    delta3 = np.zeros(len(L_values))
    for i, L in enumerate(L_values):
        residuals = []
        for start_idx in range(0, N - int(L*2), max(1, int(N/n_windows))):
            x0 = eigenvalues[start_idx]
            x1 = x0 + L
            mask = (eigenvalues >= x0) & (eigenvalues <= x1)
            n_in = np.sum(mask)
            if n_in < 3:
                continue
            eigs_in = eigenvalues[mask]
            n_vals = np.arange(1, n_in+1, dtype=float)
            t_vals = eigs_in - x0
            A_mat = np.column_stack([t_vals, np.ones(n_in)])
            coeffs2, _, _, _ = np.linalg.lstsq(A_mat, n_vals, rcond=None)
            A_fit, B_fit = coeffs2
            # GOAL formula: extra /L
            residuals.append(np.mean((n_vals - A_fit*t_vals - B_fit)**2) / L)
        delta3[i] = np.mean(residuals) if residuals else np.nan
    return L_values, delta3

def compute_delta3_corrected(eigenvalues, L_max=50, n_windows=200):
    """Corrected formula: remove extra /L."""
    N = len(eigenvalues)
    L_values = np.linspace(1, L_max, 50)
    delta3 = np.zeros(len(L_values))
    for i, L in enumerate(L_values):
        residuals = []
        for start_idx in range(0, N - int(L*2), max(1, int(N/n_windows))):
            x0 = eigenvalues[start_idx]
            x1 = x0 + L
            mask = (eigenvalues >= x0) & (eigenvalues <= x1)
            n_in = np.sum(mask)
            if n_in < 3:
                continue
            eigs_in = eigenvalues[mask]
            n_vals = np.arange(1, n_in+1, dtype=float)
            t_vals = eigs_in - x0
            A_mat = np.column_stack([t_vals, np.ones(n_in)])
            coeffs2, _, _, _ = np.linalg.lstsq(A_mat, n_vals, rcond=None)
            A_fit, B_fit = coeffs2
            # Corrected: no extra /L
            residuals.append(np.mean((n_vals - A_fit*t_vals - B_fit)**2))
        delta3[i] = np.mean(residuals) if residuals else np.nan
    return L_values, delta3

N = 500
print(f"Diagnosing Δ₃ formula with GUE N={N}")

rng = np.random.default_rng(999)
H = build_gue_matrix(N, rng)
eigs = np.linalg.eigvalsh(H)
unfolded = unfold_spectrum(np.sort(eigs))

# Check unfolded stats
print(f"Unfolded: min={unfolded.min():.2f}, max={unfolded.max():.2f}, mean={unfolded.mean():.2f}")
spacings = np.diff(unfolded)
print(f"Spacings: mean={spacings.mean():.4f} (should be ~1.0)")

L_values, d3_goal = compute_delta3_goal_formula(unfolded)
L_values, d3_corrected = compute_delta3_corrected(unfolded)

sat_mask = L_values >= 25
goal_sat = float(np.nanmean(d3_goal[sat_mask]))
corrected_sat = float(np.nanmean(d3_corrected[sat_mask]))

print(f"\nGOAL formula Δ₃_sat = {goal_sat:.4f} (expected 0.20-0.30?)")
print(f"Corrected formula Δ₃_sat = {corrected_sat:.4f} (expected 0.20-0.30?)")

# Print Δ₃(L) at several L values
print("\nL-dependent Δ₃:")
for i, L in enumerate(L_values[::5]):
    print(f"  L={L:.1f}: GOAL={d3_goal[i*5]:.4f}, Corrected={d3_corrected[i*5]:.4f}")

# Also check ratio
mean_n_in = int(np.mean([np.sum((unfolded >= unfolded[0]) & (unfolded <= unfolded[0]+L)) for L in [25, 50]]))
print(f"\nMean n_in for L=25-50: approx {mean_n_in}")
print(f"Ratio corrected/goal at L=25-50: {corrected_sat/goal_sat:.1f}")
print(f"Mean L in [25,50] range: {np.mean(L_values[sat_mask]):.1f}")
