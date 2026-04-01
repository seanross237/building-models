"""Run H_flat ensemble only — fast, no Von Mangoldt computation."""
import numpy as np
import time
from math import gamma

def build_flat_matrix(N, rng):
    H = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(j+1, N):
            phase = 2 * np.pi * rng.uniform()
            H[j, k] = np.exp(1j * phase)
            H[k, j] = np.conj(H[j, k])
    return H

def unfold_spectrum(eigenvalues, poly_degree=7):
    N = len(eigenvalues)
    eigs_sorted = np.sort(eigenvalues)
    cumulative = np.arange(1, N+1, dtype=float)
    coeffs = np.polyfit(eigs_sorted, cumulative, poly_degree)
    unfolded = np.polyval(coeffs, eigs_sorted)
    return unfolded

def compute_delta3(eigenvalues, L_max=50, n_windows=200):
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
            residuals.append(np.mean((n_vals - A_fit*t_vals - B_fit)**2) / L)
        delta3[i] = np.mean(residuals) if residuals else np.nan
    return L_values, delta3

def brody_fit(spacings, n_grid=50):
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

N = 500
N_REALIZATIONS = 5
print(f"H_flat: N={N}, realizations={N_REALIZATIONS}")

all_delta3 = []
all_beta = []
all_d3_sat = []

for i in range(N_REALIZATIONS):
    rng = np.random.default_rng(100 + i)
    t0 = time.time()
    H = build_flat_matrix(N, rng)
    t1 = time.time()
    eigs = np.linalg.eigvalsh(H)
    t2 = time.time()
    unfolded = unfold_spectrum(np.sort(eigs))
    spacings = np.diff(unfolded)
    spacings = spacings[spacings > 0]
    beta = brody_fit(spacings)
    all_beta.append(beta)
    L_values, d3 = compute_delta3(unfolded)
    t3 = time.time()
    all_delta3.append(d3)
    sat_mask = L_values >= 25
    d3_sat = float(np.nanmean(d3[sat_mask]))
    all_d3_sat.append(d3_sat)
    print(f"  r{i+1}: build={t1-t0:.1f}s eig={t2-t1:.1f}s d3={t3-t2:.1f}s | beta={beta:.3f} d3_sat={d3_sat:.4f}")

all_delta3 = np.array(all_delta3)
mean_d3 = np.nanmean(all_delta3, axis=0)
sat_mask = L_values >= 25
d3_sat_mean = float(np.nanmean(mean_d3[sat_mask]))
d3_sat_std = float(np.nanstd([np.nanmean(d[sat_mask]) for d in all_delta3]))
beta_mean = float(np.mean(all_beta))
beta_std = float(np.std(all_beta))

print(f"\nH_flat RESULT: beta={beta_mean:.4f}±{beta_std:.4f}, d3_sat={d3_sat_mean:.4f}±{d3_sat_std:.4f}")
print(f"RESULT_JSON: {{\"beta_mean\":{beta_mean:.6f},\"beta_std\":{beta_std:.6f},\"d3_sat_mean\":{d3_sat_mean:.6f},\"d3_sat_std\":{d3_sat_std:.6f}}}")

import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_flat.npz')
np.savez(out, all_delta3=all_delta3, L_values=L_values, beta=np.array(all_beta))
print(f"Saved: {out}")
