"""
Compute Li coefficients for GUE random matrices.
Replicate and improve E002's computation with more realizations and N-dependence study.

E002 approach:
- Generate N_GUE × N_GUE GUE matrix
- Get eigenvalues, scale to match zeta zero range [t_1, t_K]
- Map to ρ_k = 1/2 + i*t_k
- Compute λ_n = Σ_k [1 - (1-1/ρ_k)^n + 1 - (1-1/ρ̄_k)^n] (conjugate pairs)

Improvement: vectorized numpy, 100 realizations, multiple N values.
"""
import numpy as np
import time

# Load zeta zeros for scaling reference
zeros_2k = np.load('t_zeros_2k.npy')
t_min, t_max = zeros_2k[0], zeros_2k[-1]
print(f"Zeta zero range: [{t_min:.4f}, {t_max:.4f}]")

def compute_lambda_n_vectorized(t_values, n_val):
    """Compute λ_n from imaginary parts of zeros, vectorized over zeros."""
    # ρ_k = 0.5 + i*t_k
    # 1 - 1/ρ_k = 1 - 1/(0.5 + i*t_k) = 1 - (0.5 - i*t_k)/(0.25 + t_k^2)
    t = np.array(t_values, dtype=np.float64)
    denom = 0.25 + t**2
    real_part = 1 - 0.5/denom  # Re(1 - 1/ρ)
    imag_part = t/denom         # Im(1 - 1/ρ)

    # (1 - 1/ρ)^n using complex arithmetic
    z = real_part + 1j * imag_part
    z_n = z ** n_val  # numpy handles complex power

    # For conjugate: (1-1/ρ̄)^n = conj((1-1/ρ)^n) (assuming Re(ρ)=0.5)
    # Wait, let me verify: ρ̄ = 0.5 - it
    # 1 - 1/ρ̄ = 1 - 1/(0.5 - it) = 1 - (0.5+it)/(0.25+t^2) = real_part - i*imag_part = conj(z)
    # So (1-1/ρ̄)^n = conj(z)^n = conj(z^n) if z real axis symmetric... actually:
    # conj(z)^n = conj(z^n) always for real n
    # So the pair contribution: 2 - z^n - conj(z^n) = 2 - 2*Re(z^n)
    pair_contrib = 2.0 - 2.0 * np.real(z_n)

    return np.sum(pair_contrib)

def generate_gue_eigenvalues_scaled(N, t_min, t_max, rng):
    """Generate GUE(N) eigenvalues scaled to [t_min, t_max]."""
    A = (rng.randn(N, N) + 1j * rng.randn(N, N)) / np.sqrt(2)
    H = (A + A.conj().T) / 2.0
    evals = np.linalg.eigvalsh(H)
    # Linear scaling to match zeta zero range
    ev_min, ev_max = evals.min(), evals.max()
    evals_scaled = t_min + (evals - ev_min) / (ev_max - ev_min) * (t_max - t_min)
    return evals_scaled

# ============================================================
# Main computation: N=2000 (matching E002), 100 realizations
# ============================================================
n_test_values = [1, 10, 50, 100, 200, 300, 400, 500]
N_GUE = 2000
N_REALIZATIONS = 100

print(f"\n{'='*60}")
print(f"Computing GUE Li coefficients: N={N_GUE}, {N_REALIZATIONS} realizations")
print(f"n values: {n_test_values}")
print(f"{'='*60}")

results = {n_val: [] for n_val in n_test_values}
t0 = time.time()

for trial in range(N_REALIZATIONS):
    rng = np.random.RandomState(42 + trial)
    evals_scaled = generate_gue_eigenvalues_scaled(N_GUE, t_min, t_max, rng)

    for n_val in n_test_values:
        lam = compute_lambda_n_vectorized(evals_scaled, n_val)
        results[n_val].append(lam)

    if (trial + 1) % 20 == 0:
        elapsed = time.time() - t0
        print(f"  Trial {trial+1}/{N_REALIZATIONS} [{elapsed:.1f}s]")

elapsed = time.time() - t0
print(f"\nDone in {elapsed:.1f}s")

# Compute statistics
print(f"\n{'n':>5} {'GUE mean':>15} {'GUE std':>12} {'GUE stderr':>12}")
gue_stats = {}
for n_val in n_test_values:
    arr = np.array(results[n_val])
    mean = np.mean(arr)
    std = np.std(arr, ddof=1)
    stderr = std / np.sqrt(N_REALIZATIONS)
    gue_stats[n_val] = (mean, std, stderr)
    print(f"{n_val:>5} {mean:>15.4f} {std:>12.4f} {stderr:>12.4f}")

# Load zeta values for comparison
li_data = np.load('li_zeta_2k.npz')
li_n_values = li_data['n_values']
li_lambda_values = li_data['lambda_values']
zeta_dict = dict(zip(li_n_values, li_lambda_values))

print(f"\n{'='*60}")
print(f"RATIO COMPARISON: λ_n^zeta / λ_n^GUE")
print(f"{'='*60}")
print(f"{'n':>5} {'λ^zeta':>12} {'λ^GUE':>12} {'Ratio':>10} {'(R-1)/σ':>10} {'Signif':>8}")
for n_val in n_test_values:
    if n_val in zeta_dict:
        zeta_val = zeta_dict[n_val]
        gue_mean, gue_std, gue_stderr = gue_stats[n_val]
        ratio = zeta_val / gue_mean
        n_sigma = (zeta_val - gue_mean) / gue_std if gue_std > 0 else 0
        print(f"{n_val:>5} {zeta_val:>12.4f} {gue_mean:>12.4f} {ratio:>10.6f} {n_sigma:>10.2f} {'***' if abs(n_sigma) > 3 else ''}")

# Save results
np.savez('gue_li_N2000_100trials.npz',
         n_values=n_test_values,
         gue_means=np.array([gue_stats[n][0] for n in n_test_values]),
         gue_stds=np.array([gue_stats[n][1] for n in n_test_values]),
         gue_stderrs=np.array([gue_stats[n][2] for n in n_test_values]),
         N_GUE=N_GUE,
         N_REALIZATIONS=N_REALIZATIONS)

print(f"\nSaved to gue_li_N2000_100trials.npz")

# ============================================================
# N-dependence study: N = 500, 1000, 2000, 3000
# ============================================================
print(f"\n{'='*60}")
print(f"N-DEPENDENCE STUDY")
print(f"{'='*60}")

N_values = [500, 1000, 2000, 3000]
N_TRIALS_DEP = 50
n_focus = [100, 300, 500]

for N_val in N_values:
    dep_results = {n: [] for n in n_focus}
    t0 = time.time()
    for trial in range(N_TRIALS_DEP):
        rng = np.random.RandomState(1000 + trial)
        evals = generate_gue_eigenvalues_scaled(N_val, t_min, t_max, rng)
        for n_val in n_focus:
            lam = compute_lambda_n_vectorized(evals, n_val)
            dep_results[n_val].append(lam)
    elapsed = time.time() - t0

    print(f"\nN={N_val} ({N_TRIALS_DEP} trials, {elapsed:.1f}s):")
    print(f"  {'n':>5} {'GUE mean':>12} {'GUE std':>10} {'ζ value':>12} {'Ratio':>10}")
    for n_val in n_focus:
        arr = np.array(dep_results[n_val])
        mean_v = np.mean(arr)
        std_v = np.std(arr, ddof=1)
        zeta_v = zeta_dict.get(n_val, float('nan'))
        ratio = zeta_v / mean_v if mean_v != 0 else float('nan')
        print(f"  {n_val:>5} {mean_v:>12.4f} {std_v:>10.4f} {zeta_v:>12.4f} {ratio:>10.6f}")

print("\n=== GUE COMPUTATION COMPLETE ===")
