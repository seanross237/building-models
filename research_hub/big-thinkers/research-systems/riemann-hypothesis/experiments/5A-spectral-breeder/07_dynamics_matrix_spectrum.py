#!/usr/bin/env python3
"""
Step 7: Analyze eigenvalue spectra of matrices constructed from CA dynamics.

Instead of the combinatorial transfer matrix, construct matrices from
the actual spacetime evolution:

1. Correlation matrix: C[i,j] = <s_i(t) s_j(t)>_t (spatial correlations)
2. Time-delay embedding matrix: M[t,k] = state vector at time t+k
3. Mutual information matrix: MI[i,j] between columns i and j
4. The "spacetime" Gram matrix: G = X X^T where X is the spacetime diagram

If any of these matrices have GUE-like eigenvalue spacing, it would
suggest deep connections between CA dynamics and random matrix theory.
"""

import numpy as np
from scipy import linalg, stats
from scipy.integrate import quad
import json
import time
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def wigner_surmise_pdf(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)

def wigner_surmise_cdf(s):
    if np.isscalar(s):
        val, _ = quad(wigner_surmise_pdf, 0, max(s, 0))
        return val
    return np.array([quad(wigner_surmise_pdf, 0, max(si, 0))[0] for si in s])

def ks_gue(spacings):
    sorted_s = np.sort(spacings)
    n = len(sorted_s)
    ecdf = np.arange(1, n + 1) / n
    cdf_vals = wigner_surmise_cdf(sorted_s)
    ecdf_minus = np.arange(0, n) / n
    return max(np.max(ecdf - cdf_vals), np.max(cdf_vals - ecdf_minus))

def ks_poisson(spacings):
    return stats.kstest(spacings, 'expon', args=(0, 1)).statistic


class ElementaryCA:
    def __init__(self, rule_number, width=200):
        self.rule_number = rule_number
        self.width = width
        self.rule_table = np.array([(rule_number >> i) & 1 for i in range(8)], dtype=np.uint8)

    def run(self, steps, seed=42):
        np.random.seed(seed)
        state = np.random.randint(0, 2, self.width, dtype=np.uint8)
        spacetime = np.zeros((steps, self.width), dtype=np.uint8)
        spacetime[0] = state
        for t in range(1, steps):
            padded = np.concatenate([[state[-1]], state, [state[0]]])
            neighborhood = (padded[:-2] << 2) | (padded[1:-1] << 1) | padded[2:]
            state = self.rule_table[neighborhood]
            spacetime[t] = state
        return spacetime


def eigenvalue_spacings(eigenvalues):
    """Compute normalized nearest-neighbor spacings of eigenvalues."""
    sorted_ev = np.sort(np.real(eigenvalues))
    spacings = np.diff(sorted_ev)
    spacings = spacings[spacings > 1e-12]  # Remove degeneracies
    if len(spacings) < 5:
        return np.array([])
    mean_s = np.mean(spacings)
    if mean_s > 0:
        return spacings / mean_s
    return np.array([])


def analyze_spacetime_matrices(rule_number, width=200, steps=500, skip=100):
    """
    Construct and analyze various matrices from CA spacetime dynamics.
    """
    ca = ElementaryCA(rule_number, width)
    spacetime = ca.run(steps + skip, seed=42)
    spacetime = spacetime[skip:]  # Remove transient
    steps = spacetime.shape[0]

    # Convert to float, center
    X = spacetime.astype(np.float64)
    X_centered = X - np.mean(X, axis=0, keepdims=True)

    results = {}

    # 1. Spatial correlation matrix: C = X^T X / steps
    print(f"  Computing spatial correlation matrix ({width}x{width})...")
    C = X_centered.T @ X_centered / steps
    ev_spatial = np.real(linalg.eigvalsh(C))
    spacings = eigenvalue_spacings(ev_spatial)
    if len(spacings) >= 10:
        results['spatial_correlation'] = {
            'ks_gue': float(ks_gue(spacings)),
            'ks_poisson': float(ks_poisson(spacings)),
            'n_spacings': len(spacings),
            'spectral_range': float(ev_spatial[-1] - ev_spatial[0]),
            'rank': int(np.sum(ev_spatial > 1e-8)),
        }
        print(f"    KS(GUE) = {results['spatial_correlation']['ks_gue']:.4f}, "
              f"KS(Poisson) = {results['spatial_correlation']['ks_poisson']:.4f}")

    # 2. Temporal correlation matrix: C_t = X X^T / width
    print(f"  Computing temporal correlation matrix ({steps}x{steps})...")
    C_t = X_centered @ X_centered.T / width
    # For large matrices, compute only eigenvalues
    ev_temporal = np.real(linalg.eigvalsh(C_t))
    spacings = eigenvalue_spacings(ev_temporal)
    if len(spacings) >= 10:
        results['temporal_correlation'] = {
            'ks_gue': float(ks_gue(spacings)),
            'ks_poisson': float(ks_poisson(spacings)),
            'n_spacings': len(spacings),
        }
        print(f"    KS(GUE) = {results['temporal_correlation']['ks_gue']:.4f}, "
              f"KS(Poisson) = {results['temporal_correlation']['ks_poisson']:.4f}")

    # 3. Circulant approximation: use DFT of the first row of C
    print(f"  Computing circulant spectrum...")
    row0 = C[0, :]
    circ_ev = np.fft.fft(row0)
    circ_spacings = eigenvalue_spacings(np.real(circ_ev))
    if len(circ_spacings) >= 10:
        results['circulant_approx'] = {
            'ks_gue': float(ks_gue(circ_spacings)),
            'ks_poisson': float(ks_poisson(circ_spacings)),
            'n_spacings': len(circ_spacings),
        }
        print(f"    KS(GUE) = {results['circulant_approx']['ks_gue']:.4f}, "
              f"KS(Poisson) = {results['circulant_approx']['ks_poisson']:.4f}")

    # 4. Time-delay embedding matrix
    # Construct: M[t, k] = mean(spacetime[t+k, :]) for k = 0..embed_dim
    embed_dim = min(100, steps // 3)
    print(f"  Computing time-delay embedding ({steps - embed_dim}x{embed_dim})...")
    M = np.zeros((steps - embed_dim, embed_dim))
    for k in range(embed_dim):
        M[:, k] = np.mean(X[k:k + steps - embed_dim], axis=1)
    M_centered = M - np.mean(M, axis=0, keepdims=True)
    C_embed = M_centered.T @ M_centered / M.shape[0]
    ev_embed = np.real(linalg.eigvalsh(C_embed))
    spacings = eigenvalue_spacings(ev_embed)
    if len(spacings) >= 10:
        results['time_delay_embed'] = {
            'ks_gue': float(ks_gue(spacings)),
            'ks_poisson': float(ks_poisson(spacings)),
            'n_spacings': len(spacings),
        }
        print(f"    KS(GUE) = {results['time_delay_embed']['ks_gue']:.4f}, "
              f"KS(Poisson) = {results['time_delay_embed']['ks_poisson']:.4f}")

    # 5. XOR evolution matrix: define T where T[i,j] = fraction of time
    #    that cell j at time t predicts cell i at time t+1
    print(f"  Computing empirical evolution matrix...")
    T_emp = np.zeros((width, width))
    for t in range(steps - 1):
        for dx in range(-3, 4):  # Look at local neighborhood
            j_col = np.arange(width)
            i_col = (j_col + dx) % width
            agreement = (spacetime[t+1, i_col] == spacetime[t, j_col]).astype(float)
            T_emp[i_col, j_col] += agreement
    T_emp /= (steps - 1)
    ev_emp = linalg.eigvals(T_emp)
    spacings = eigenvalue_spacings(ev_emp)
    if len(spacings) >= 10:
        results['empirical_evolution'] = {
            'ks_gue': float(ks_gue(spacings)),
            'ks_poisson': float(ks_poisson(spacings)),
            'n_spacings': len(spacings),
        }
        print(f"    KS(GUE) = {results['empirical_evolution']['ks_gue']:.4f}, "
              f"KS(Poisson) = {results['empirical_evolution']['ks_poisson']:.4f}")

    # 6. Spatial power spectrum: eigenvalues of the spectral density matrix
    print(f"  Computing spectral density matrix...")
    # Compute DFT of each row, then covariance of DFT coefficients
    X_dft = np.fft.fft(X, axis=1)
    # Cross-spectral density matrix for each frequency
    best_spec_ks = 1.0
    for freq_idx in range(1, width // 4):
        freq_col = X_dft[:, freq_idx]
        freq_col_centered = freq_col - np.mean(freq_col)
        # Build a small matrix from windowed segments
        window_size = 50
        n_windows = steps // window_size
        if n_windows < 10:
            continue
        windowed = np.array([freq_col_centered[i*window_size:(i+1)*window_size]
                           for i in range(n_windows)])
        C_spec = windowed @ windowed.conj().T / window_size
        ev_spec = np.sort(np.real(linalg.eigvalsh(C_spec)))
        sp = eigenvalue_spacings(ev_spec)
        if len(sp) >= 5:
            ks = ks_gue(sp)
            if ks < best_spec_ks:
                best_spec_ks = ks

    if best_spec_ks < 1.0:
        results['spectral_density_best'] = {
            'ks_gue': float(best_spec_ks),
            'note': 'Best KS(GUE) across frequency bins',
        }
        print(f"    Best spectral density KS(GUE) = {best_spec_ks:.4f}")

    return results


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    rules_to_analyze = [30, 45, 54, 73, 86, 89, 90, 105, 110, 150]

    all_results = {}

    for rule in rules_to_analyze:
        print(f"\n{'='*50}")
        print(f"Rule {rule}: Dynamics Matrix Spectrum")
        print(f"{'='*50}")

        t0 = time.time()
        result = analyze_spacetime_matrices(rule, width=200, steps=500, skip=100)
        elapsed = time.time() - t0

        all_results[f'rule_{rule}'] = result
        print(f"\nRule {rule} completed in {elapsed:.1f}s")

        # Find best method
        if result:
            best_method = min(result.items(), key=lambda x: x[1].get('ks_gue', 1.0))
            print(f"Best method: {best_method[0]} with KS(GUE) = {best_method[1].get('ks_gue', 'N/A')}")

    # Summary
    print(f"\n\n{'='*60}")
    print(f"=== DYNAMICS MATRIX SPECTRUM SUMMARY ===")
    print(f"{'='*60}")

    for rule_key, methods in all_results.items():
        rule_num = rule_key.split('_')[1]
        print(f"\nRule {rule_num}:")
        for method_name, data in sorted(methods.items(), key=lambda x: x[1].get('ks_gue', 1.0)):
            ks = data.get('ks_gue', 'N/A')
            ks_p = data.get('ks_poisson', 'N/A')
            n = data.get('n_spacings', 'N/A')
            if isinstance(ks, float):
                print(f"  {method_name:25s}: KS(GUE) = {ks:.4f}, KS(Poi) = {ks_p:.4f}, n = {n}")
            else:
                print(f"  {method_name:25s}: {data}")

    # Save
    with open(os.path.join(OUTPUT_DIR, 'dynamics_matrix_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nResults saved to dynamics_matrix_results.json")
