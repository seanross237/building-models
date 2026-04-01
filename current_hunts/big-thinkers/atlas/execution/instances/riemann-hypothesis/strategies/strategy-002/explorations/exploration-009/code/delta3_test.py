"""
Exploration 009 — Flat-Amplitude Δ₃ Spectral Rigidity Test
Compare Δ₃_sat for: H_flat, C1, GUE_control, H_diagonal_flat

Runs 5 realizations per ensemble, averages Δ₃(L) curves,
reports Δ₃_sat = mean(Δ₃) for L in [25, 50].
"""

import numpy as np
import time
import os
from math import gamma

# ─── Helper functions ────────────────────────────────────────────────────────

def von_mangoldt(n):
    """Λ(n) = log(p) if n = p^k for prime p, else 0."""
    if n <= 1:
        return 0.0
    orig = n
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            while n % p == 0:
                n //= p
            if n == 1:
                return np.log(p)
            else:
                return 0.0
    return np.log(orig)  # n is prime


def build_c1_matrix(N, rng):
    """C1: Von Mangoldt Hankel + random complex phases."""
    amplitudes = np.array([von_mangoldt(k) for k in range(1, 2*N+1)])
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(j+1, N):
            phase = 2 * np.pi * rng.uniform()
            amp = amplitudes[abs(j-k) + 1]
            H[j, k] = amp * np.exp(1j * phase)
            H[k, j] = np.conj(H[j, k])
    return H


def build_flat_matrix(N, rng):
    """H_flat: flat amplitude + random complex phases."""
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(j+1, N):
            phase = 2 * np.pi * rng.uniform()
            H[j, k] = np.exp(1j * phase)
            H[k, j] = np.conj(H[j, k])
    return H


def build_gue_matrix(N, rng):
    """Standard GUE sample."""
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    H = (A + A.conj().T) / np.sqrt(2 * N)
    return H


def build_diagonal_flat_matrix(N, rng):
    """H_diagonal_flat: flat amplitude, nearest-neighbor only (|j-k|==1)."""
    H = np.zeros((N, N), dtype=complex)
    for j in range(N-1):
        phase = 2 * np.pi * rng.uniform()
        H[j, j+1] = np.exp(1j * phase)
        H[j+1, j] = np.conj(H[j, j+1])
    return H


def unfold_spectrum(eigenvalues, poly_degree=7):
    """Unfold eigenvalues using polynomial fit to cumulative density."""
    N = len(eigenvalues)
    eigs_sorted = np.sort(eigenvalues)
    cumulative = np.arange(1, N+1, dtype=float)
    coeffs = np.polyfit(eigs_sorted, cumulative, poly_degree)
    unfolded = np.polyval(coeffs, eigs_sorted)
    return unfolded


def compute_delta3(eigenvalues, L_max=50, n_windows=200):
    """
    Dyson-Mehta Δ₃ statistic.
    eigenvalues: sorted, unfolded eigenvalues
    Returns: (L_values, delta3_values)
    """
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
            T = t_vals
            A_mat = np.column_stack([T, np.ones(n_in)])
            coeffs, _, _, _ = np.linalg.lstsq(A_mat, n_vals, rcond=None)
            A_fit, B_fit = coeffs
            residuals.append(np.mean((n_vals - A_fit*T - B_fit)**2) / L)

        delta3[i] = np.mean(residuals) if residuals else np.nan

    return L_values, delta3


def brody_fit(spacings, n_grid=50):
    """Manual Brody fit without scipy."""
    s = np.array(spacings)
    s = s / np.mean(s)

    best_beta = 0.0
    best_loss = np.inf

    for beta in np.linspace(0.0, 2.5, n_grid):
        b = (gamma((beta+2)/(beta+1)))**(beta+1)
        bins = np.linspace(0, 4, 30)
        hist, edges = np.histogram(s, bins=bins, density=True)
        centers = (edges[:-1] + edges[1:]) / 2
        pred = (1+beta) * b * centers**beta * np.exp(-b * centers**(beta+1))
        loss = np.sum((hist - pred)**2)
        if loss < best_loss:
            best_loss = loss
            best_beta = beta

    return best_beta


def compute_ensemble(name, build_fn, N, n_realizations, seed_base=42):
    """Compute Δ₃ for n_realizations of a given matrix ensemble."""
    print(f"\n=== {name} === ({n_realizations} realizations, N={N})")
    all_delta3 = []
    all_beta = []

    for i in range(n_realizations):
        rng = np.random.default_rng(seed_base + i)
        t0 = time.time()

        H = build_fn(N, rng)
        t_build = time.time()

        eigs = np.linalg.eigvalsh(H)
        t_eig = time.time()

        unfolded = unfold_spectrum(np.sort(eigs))
        spacings = np.diff(unfolded)
        spacings = spacings[spacings > 0]

        beta = brody_fit(spacings)
        all_beta.append(beta)

        L_values, d3 = compute_delta3(unfolded)
        t_d3 = time.time()
        all_delta3.append(d3)

        # Δ₃_sat: mean over L ∈ [25, 50]
        sat_mask = L_values >= 25
        d3_sat = np.nanmean(d3[sat_mask])

        print(f"  Realization {i+1}: build={t_build-t0:.1f}s, eig={t_eig-t_build:.1f}s, "
              f"Δ₃={t_d3-t_eig:.1f}s | β={beta:.3f}, Δ₃_sat={d3_sat:.4f}")

    all_delta3 = np.array(all_delta3)
    mean_d3 = np.nanmean(all_delta3, axis=0)
    std_d3 = np.nanstd(all_delta3, axis=0)

    sat_mask = L_values >= 25
    d3_sat_mean = np.nanmean(mean_d3[sat_mask])
    d3_sat_std = np.nanstd(all_delta3[:, sat_mask])
    beta_mean = np.mean(all_beta)
    beta_std = np.std(all_beta)

    print(f"\n  {name} SUMMARY:")
    print(f"    β = {beta_mean:.3f} ± {beta_std:.3f}")
    print(f"    Δ₃_sat = {d3_sat_mean:.4f} ± {d3_sat_std:.4f}")

    return {
        'name': name,
        'L_values': L_values,
        'all_delta3': all_delta3,
        'mean_d3': mean_d3,
        'std_d3': std_d3,
        'd3_sat_mean': d3_sat_mean,
        'd3_sat_std': d3_sat_std,
        'beta_mean': beta_mean,
        'beta_std': beta_std,
    }


# ─── Main execution ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    N = 500
    N_REALIZATIONS = 5

    output_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("Exploration 009 — Flat-Amplitude Δ₃ Test")
    print(f"N={N}, realizations={N_REALIZATIONS}")
    print("=" * 60)

    results = {}

    # ── H_flat ────────────────────────────────────────────────────
    r = compute_ensemble('H_flat', build_flat_matrix, N, N_REALIZATIONS, seed_base=100)
    results['H_flat'] = r
    np.savez(os.path.join(output_dir, 'results_partial.npz'),
             delta3_flat=r['all_delta3'],
             L_values=r['L_values'])
    print(f"\n[CHECKPOINT: H_flat saved]")

    # ── C1 ────────────────────────────────────────────────────────
    r2 = compute_ensemble('C1', build_c1_matrix, N, N_REALIZATIONS, seed_base=200)
    results['C1'] = r2
    np.savez(os.path.join(output_dir, 'results_partial.npz'),
             delta3_flat=results['H_flat']['all_delta3'],
             delta3_c1=r2['all_delta3'],
             L_values=r2['L_values'])
    print(f"\n[CHECKPOINT: C1 saved]")

    # ── GUE control ───────────────────────────────────────────────
    r3 = compute_ensemble('GUE_control', build_gue_matrix, N, N_REALIZATIONS, seed_base=300)
    results['GUE_control'] = r3
    print(f"\n[CHECKPOINT: GUE_control done]")

    # ── H_diagonal_flat ───────────────────────────────────────────
    r4 = compute_ensemble('H_diagonal_flat', build_diagonal_flat_matrix, N, N_REALIZATIONS, seed_base=400)
    results['H_diagonal_flat'] = r4
    print(f"\n[CHECKPOINT: H_diagonal_flat done]")

    # ── Save all results ─────────────────────────────────────────
    np.savez(os.path.join(output_dir, 'results.npz'),
             delta3_flat=results['H_flat']['all_delta3'],
             delta3_c1=results['C1']['all_delta3'],
             delta3_gue=results['GUE_control']['all_delta3'],
             delta3_diag_flat=results['H_diagonal_flat']['all_delta3'],
             L_values=results['H_flat']['L_values'])
    print(f"\n[ALL RESULTS SAVED to results.npz]")

    # ── Print final summary table ─────────────────────────────────
    print("\n" + "=" * 60)
    print("FINAL COMPARISON TABLE")
    print("=" * 60)
    print(f"{'Ensemble':<20} {'β mean±std':<18} {'Δ₃_sat mean±std':<20}")
    print("-" * 58)
    for name, r in results.items():
        print(f"{name:<20} {r['beta_mean']:.3f} ± {r['beta_std']:.3f}     "
              f"{r['d3_sat_mean']:.4f} ± {r['d3_sat_std']:.4f}")
    print("-" * 58)
    print(f"{'Riemann zeros':<20} {'(known)':<18} 0.155 (known)")
    print("=" * 60)

    # ── Print verdict ─────────────────────────────────────────────
    flat_sat = results['H_flat']['d3_sat_mean']
    c1_sat = results['C1']['d3_sat_mean']
    diff = abs(flat_sat - c1_sat)
    c1_std = results['C1']['d3_sat_std']

    print("\nVERDICT:")
    if diff < 2 * max(results['H_flat']['d3_sat_std'], c1_std):
        print(f"  H_flat Δ₃_sat ({flat_sat:.4f}) ≈ C1 Δ₃_sat ({c1_sat:.4f})")
        print("  Von Mangoldt amplitude does NOT explain intermediate rigidity.")
        print("  C1's Δ₃ is GENERIC GUE-class behavior at N=500.")
    elif flat_sat > c1_sat + 2*c1_std:
        print(f"  H_flat Δ₃_sat ({flat_sat:.4f}) >> C1 Δ₃_sat ({c1_sat:.4f})")
        print("  Von Mangoldt amplitude DOES cause anomalous rigidity in C1.")
    else:
        print(f"  H_flat ({flat_sat:.4f}) vs C1 ({c1_sat:.4f}): ambiguous (diff={diff:.4f})")
