"""Save Part A intermediate data as .npz for reproducibility."""
import numpy as np
from scipy.linalg import eigh

np.random.seed(42)

def precompute_mangoldt(max_n):
    vals = np.zeros(max_n + 1)
    for p in range(2, max_n + 1):
        is_prime = True
        for d in range(2, int(p**0.5) + 1):
            if p % d == 0:
                is_prime = False
                break
        if is_prime:
            log_p = np.log(p)
            pk = p
            while pk <= max_n:
                vals[pk] = log_p
                pk *= p
    return vals

def build_c1_matrix_vectorized(N, mangoldt_vals, rng):
    j_idx = np.arange(N)
    k_idx = np.arange(N)
    jj, kk = np.meshgrid(j_idx, k_idx, indexing='ij')
    diffs = np.abs(jj - kk) + 1
    amps = mangoldt_vals[diffs]
    phases = rng.uniform(0, 2 * np.pi, (N, N))
    H = amps * np.exp(1j * phases)
    H = (H + H.conj().T) / 2
    return H

def unfold_eigenvalues(evals, deg=7):
    evals_sorted = np.sort(evals)
    N = len(evals_sorted)
    cum = np.arange(1, N + 1, dtype=float)
    x_min, x_max = evals_sorted[0], evals_sorted[-1]
    x_norm = (evals_sorted - x_min) / (x_max - x_min + 1e-15) * 2 - 1
    poly_coeffs = np.polyfit(x_norm, cum, deg=deg)
    unfolded = np.polyval(poly_coeffs, x_norm)
    spacings = np.diff(unfolded)
    mean_sp = spacings.mean()
    if mean_sp > 0:
        unfolded = unfolded / mean_sp
    return unfolded

N = 500
n_realizations = 5
mangoldt_vals = precompute_mangoldt(2 * N + 2)

all_eigenvalues = []
all_unfolded = []
all_spacings = []

for rep in range(n_realizations):
    rng = np.random.default_rng(rep * 1000 + 7)
    H = build_c1_matrix_vectorized(N, mangoldt_vals, rng)
    evals = eigh(H, eigvals_only=True)
    evals.sort()
    all_eigenvalues.append(evals)

    unfolded = unfold_eigenvalues(evals, deg=7)
    all_unfolded.append(unfolded)

    spacings = np.diff(unfolded)
    spacings = spacings / spacings.mean()
    spacings = spacings[spacings > 0]
    all_spacings.append(spacings)

import os
out_dir = os.path.dirname(os.path.abspath(__file__))
np.savez(os.path.join(out_dir, "part_a_data.npz"),
         eigenvalues=np.array(all_eigenvalues),
         unfolded=np.array(all_unfolded),
         mangoldt_vals=mangoldt_vals)
print(f"Saved part_a_data.npz with {n_realizations} realizations of {N} eigenvalues each")
