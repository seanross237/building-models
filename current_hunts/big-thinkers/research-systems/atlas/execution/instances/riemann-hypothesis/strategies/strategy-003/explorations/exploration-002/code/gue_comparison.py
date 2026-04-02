#!/usr/bin/env python3
"""
Task 4d & 5: GUE comparison and connection to spectral statistics.

Generate GUE random matrices, compute their "Li coefficients", and compare
the residual structure to the zeta zero Li coefficients.
"""

import numpy as np
import os
import json

CODE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load zeta Li coefficients
data = np.load(os.path.join(CODE_DIR, 'li_coefficients.npz'))
n_values = data['n_values']
lambda_real = data['lambda_real']
zero_imag = data['zero_imag_parts']

# Load residuals
res_data = np.load(os.path.join(CODE_DIR, 'residuals.npz'))
delta_coffey_zeta = res_data['delta_coffey']

print("=" * 70)
print("TASK 4d & 5: GUE COMPARISON")
print("=" * 70)

# ============================================================
# Generate GUE random matrix
# ============================================================

def generate_gue(N, seed=42):
    """Generate N×N GUE random matrix and return its eigenvalues."""
    rng = np.random.RandomState(seed)
    # GUE: H = (A + A†) / 2 where A has i.i.d. complex normal entries
    A = (rng.randn(N, N) + 1j * rng.randn(N, N)) / np.sqrt(2)
    H = (A + A.conj().T) / 2.0
    eigenvalues = np.linalg.eigvalsh(H)  # real eigenvalues, sorted
    return eigenvalues

# We want GUE eigenvalues scaled to be in the critical strip range
# Zeta zeros have Im(ρ) ~ 14.13 to ~742.84 (for first 2000 zeros)
# GUE eigenvalues of N×N matrix have bulk in [-2√N, 2√N]

N_GUE = 2000  # Match number of zeros
print(f"\nGenerating GUE({N_GUE}) random matrix...")

# Average over multiple GUE realizations for robustness
N_REALIZATIONS = 5
gue_lambdas_all = []

for trial in range(N_REALIZATIONS):
    eigenvalues_raw = generate_gue(N_GUE, seed=42 + trial)

    # Scale eigenvalues to match zeta zero range
    # Map [-2√N, 2√N] -> [t_1, t_{2000}] ≈ [14.13, 742.84]
    t_min, t_max = zero_imag[0], zero_imag[-1]
    ev_min, ev_max = eigenvalues_raw.min(), eigenvalues_raw.max()
    eigenvalues_scaled = t_min + (eigenvalues_raw - ev_min) / (ev_max - ev_min) * (t_max - t_min)

    # Create "complex zeros" matching zeta structure: ρ_GUE = 1/2 + i*t_k
    # For Li's formula, we need zeros in the critical strip
    rho_gue = 0.5 + 1j * eigenvalues_scaled

    # Compute Li coefficients for GUE
    max_n = min(500, int(n_values[-1]))
    lambda_gue = np.zeros(max_n)

    for n_idx, n in enumerate(range(1, max_n + 1)):
        total = 0.0 + 0.0j
        for rho in rho_gue:
            # ρ and its conjugate (same as for zeta)
            term1 = 1 - (1 - 1/rho)**n
            term2 = 1 - (1 - 1/rho.conjugate())**n
            total += term1 + term2
        lambda_gue[n_idx] = total.real

    gue_lambdas_all.append(lambda_gue)
    if trial == 0:
        print(f"  Trial {trial+1}: λ_1^GUE = {lambda_gue[0]:.10f}, λ_100^GUE = {lambda_gue[99]:.10f}")

# Average over realizations
gue_lambdas_mean = np.mean(gue_lambdas_all, axis=0)
gue_lambdas_std = np.std(gue_lambdas_all, axis=0)

print(f"\nGUE Li coefficients (averaged over {N_REALIZATIONS} realizations):")
for n in [1, 5, 10, 50, 100, 200, 300, 400, 500]:
    if n <= max_n:
        print(f"  λ_{n}^GUE = {gue_lambdas_mean[n-1]:.10f} ± {gue_lambdas_std[n-1]:.6f}")

# ============================================================
# Compare residuals
# ============================================================
print("\n--- Residual Comparison ---")

gamma_E = 0.5772156649015328606065120900824024310421593359
e = np.e

def coffey_asymptotic(n):
    return ((n / 2) * np.log(n / (2 * np.pi)) +
            (n / 2) * (gamma_E - 1) +
            0.5 * np.log(np.pi) +
            (1/8) * np.log(4 * np.pi / e) +
            0.5)

n_common = np.arange(1, max_n + 1)
delta_gue = gue_lambdas_mean - np.array([coffey_asymptotic(n) for n in n_common])

# Compare to zeta residual (first max_n values)
delta_zeta = delta_coffey_zeta[:max_n]

# Correlation between GUE and zeta residuals
if len(delta_gue) > 50 and len(delta_zeta) >= len(delta_gue):
    # Use n=50 onwards (skip small n where asymptotics are poor)
    idx_start = 49
    corr = np.corrcoef(delta_gue[idx_start:], delta_zeta[idx_start:])[0, 1]
    print(f"Correlation of δ^GUE and δ^zeta (n≥50): {corr:.6f}")

    # Compare magnitudes
    mag_gue = np.mean(np.abs(delta_gue[idx_start:]))
    mag_zeta = np.mean(np.abs(delta_zeta[idx_start:]))
    print(f"Mean |δ^GUE| for n≥50: {mag_gue:.10f}")
    print(f"Mean |δ^zeta| for n≥50: {mag_zeta:.10f}")
    print(f"Ratio |δ^zeta|/|δ^GUE|: {mag_zeta/mag_gue:.6f}" if mag_gue > 0 else "")

    # Compare growth rates
    ratio_gue = delta_gue[idx_start:] / np.log(n_common[idx_start:])
    ratio_zeta = delta_zeta[idx_start:] / np.log(n_common[idx_start:])
    print(f"\nδ/log(n) convergence (last 50 values):")
    print(f"  GUE:  mean={np.mean(ratio_gue[-50:]):.10f}, std={np.std(ratio_gue[-50:]):.10f}")
    print(f"  Zeta: mean={np.mean(ratio_zeta[-50:]):.10f}, std={np.std(ratio_zeta[-50:]):.10f}")

# ============================================================
# Task 5: Spectral Statistics Connection (Δ₃)
# ============================================================
print("\n" + "=" * 70)
print("TASK 5: SPECTRAL STATISTICS CONNECTION")
print("=" * 70)

def compute_delta3(eigenvalues, L_values):
    """
    Compute the spectral rigidity Δ₃(L) for a set of eigenvalues.
    Δ₃(L) = (1/L) min_{A,B} ∫_0^L [N(x) - Ax - B]^2 dx
    where N(x) is the staircase function.
    Uses the midpoint of the eigenvalue spectrum.
    """
    results = []
    N = len(eigenvalues)
    ev = np.sort(eigenvalues)

    # Unfold: use mean spacing
    mean_spacing = (ev[-1] - ev[0]) / (N - 1)

    # Unfolded eigenvalues
    ev_unfolded = (ev - ev[0]) / mean_spacing

    for L in L_values:
        # Use center of spectrum
        center = N / 2
        low = center - L / 2
        high = center + L / 2
        if low < 0 or high > N:
            results.append(np.nan)
            continue

        # Eigenvalues in [low, high]
        mask = (ev_unfolded >= low) & (ev_unfolded <= high)
        ev_window = ev_unfolded[mask] - low

        # Staircase function
        if len(ev_window) < 2:
            results.append(np.nan)
            continue

        n_in = len(ev_window)

        # Analytical Δ₃ for given staircase (Mehta formula)
        # Δ₃(L) = (1/L) min_{A,B} ∫_0^L [N(x) - Ax - B]² dx
        # For discrete eigenvalues, compute analytically
        points = ev_window
        n_steps = np.arange(1, len(points) + 1)

        # Integrate [N(x) - Ax - B]^2 over [0, L] with optimal A, B
        # Moment method:
        S0 = L
        S1 = L**2 / 2
        S2 = L**3 / 3
        T0 = np.sum(L - points)
        T1 = np.sum((L**2 - points**2) / 2)
        T2 = np.sum(L - points)  # integral of step function * 1
        Tn2 = np.sum((L - points)**2)  # integral of N(x)^2 ... simplified

        # Actually, let's just compute numerically
        x_grid = np.linspace(0, L, 1000)
        N_x = np.array([np.sum(points <= x) for x in x_grid])

        # Best fit A, B
        A_mat = np.column_stack([x_grid, np.ones_like(x_grid)])
        fit = np.linalg.lstsq(A_mat, N_x, rcond=None)
        A_opt, B_opt = fit[0]

        residuals = N_x - A_opt * x_grid - B_opt
        delta3 = np.trapezoid(residuals**2, x_grid) / L

        results.append(delta3)

    return np.array(results)


# Compute Δ₃ for GUE eigenvalues
L_values = np.array([1, 2, 5, 10, 20, 50, 100])
print(f"\nComputing Δ₃(L) for GUE eigenvalues...")
eigenvalues_raw = generate_gue(N_GUE, seed=42)
delta3_gue = compute_delta3(eigenvalues_raw, L_values)

print(f"\nΔ₃(L) for GUE({N_GUE}):")
print(f"{'L':>8} | {'Δ₃(L)':>12} | {'GUE theory':>12}")
for i, L in enumerate(L_values):
    # GUE theoretical: Δ₃(L) ~ (1/2π²)(log(2πL) + γ - 5/4 - π²/8) for large L
    if L > 0:
        gue_theory = (1/(2*np.pi**2)) * (np.log(2*np.pi*L) + 0.5772 - 5/4 - np.pi**2/8) if L > 2 else L/15.0
    else:
        gue_theory = 0
    print(f"{L:>8.0f} | {delta3_gue[i]:>12.6f} | {gue_theory:>12.6f}")

# Compute Δ₃ for zeta zeros (using imaginary parts as "eigenvalues")
print(f"\nComputing Δ₃(L) for zeta zero imaginary parts...")
delta3_zeta = compute_delta3(zero_imag, L_values)
print(f"\nΔ₃(L) for zeta zeros:")
print(f"{'L':>8} | {'Δ₃(L)':>12}")
for i, L in enumerate(L_values):
    print(f"{L:>8.0f} | {delta3_zeta[i]:>12.6f}")

# Compare Δ₃ saturation between GUE and zeta
print(f"\n--- Connection Summary ---")
if not np.isnan(delta3_zeta[-1]) and not np.isnan(delta3_gue[-1]):
    print(f"Δ₃ at L=100: GUE = {delta3_gue[-1]:.6f}, Zeta = {delta3_zeta[-1]:.6f}")
    print(f"Prior result: Δ₃_sat ≈ 0.155 (super-rigid)")

# Check if Li residual structure correlates with Δ₃ difference
print(f"\nLi residual vs Δ₃ comparison:")
print(f"  GUE mean |δ^Li|: {mag_gue:.8f}" if 'mag_gue' in dir() else "  GUE mean |δ^Li|: N/A")
print(f"  Zeta mean |δ^Li|: {mag_zeta:.8f}" if 'mag_zeta' in dir() else "  Zeta mean |δ^Li|: N/A")

# Save all GUE results
np.savez(os.path.join(CODE_DIR, 'gue_results.npz'),
         gue_lambdas_mean=gue_lambdas_mean,
         gue_lambdas_std=gue_lambdas_std,
         delta_gue=delta_gue,
         delta3_gue=delta3_gue,
         delta3_zeta=delta3_zeta,
         L_values=L_values)

print(f"\nGUE results saved to gue_results.npz")
print("\n=== GUE COMPARISON COMPLETE ===")
