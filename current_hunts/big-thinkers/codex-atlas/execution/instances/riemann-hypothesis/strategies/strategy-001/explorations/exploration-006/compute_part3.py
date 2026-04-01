"""
Part 3: Variants — Normalized von Mangoldt, Möbius Toeplitz, Log-zeta Hankel
"""
import numpy as np
from sympy import isprime, factorint, mobius
from scipy.linalg import toeplitz
import time
import json

base_dir = '/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-006'

N_max = 1001

# ---- Precompute arithmetic functions ----
print("Precomputing arithmetic functions...")
t0 = time.time()

# Von Mangoldt
def von_mangoldt(n):
    if n <= 1: return 0.0
    factors = factorint(n)
    if len(factors) == 1:
        return float(np.log(list(factors.keys())[0]))
    return 0.0

Lambda_vals = np.array([von_mangoldt(n) for n in range(2 * N_max + 2)])

# Möbius function
def mobius_func(n):
    if n <= 0: return 0
    if n == 1: return 1
    factors = factorint(n)
    for p, e in factors.items():
        if e > 1:
            return 0
    return (-1)**len(factors)

mu_vals = np.array([mobius_func(n) for n in range(2 * N_max + 2)])

print(f"Done in {time.time()-t0:.2f}s")

# ---- Helper functions ----
def build_toeplitz_matrix(a_values, N, diag_val=0.0):
    """T_{ij} = a(|i-j|+1) for i!=j, T_{ii} = diag_val."""
    first_row = np.zeros(N)
    first_row[0] = diag_val
    for j in range(1, N):
        first_row[j] = a_values[j + 1]
    return toeplitz(first_row)

def unfold_eigenvalues(eigs_sorted, s_factor=0.5):
    """Unfold eigenvalues using spline smoothing of staircase."""
    from scipy.interpolate import UnivariateSpline
    N = len(eigs_sorted)
    spline = UnivariateSpline(eigs_sorted, np.arange(N), s=N*s_factor, k=3)
    unfolded = spline(eigs_sorted)
    return unfolded

def compute_spacing_stats(eigs, label, remove_outlier_sigma=2.5):
    """Full statistical analysis of eigenvalues."""
    # Remove outliers
    mean_e = np.mean(eigs)
    std_e = np.std(eigs)
    if std_e > 0:
        bulk_mask = (eigs > mean_e - remove_outlier_sigma*std_e) & (eigs < mean_e + remove_outlier_sigma*std_e)
        eigs_bulk = np.sort(eigs[bulk_mask])
    else:
        eigs_bulk = np.sort(eigs)
    N_bulk = len(eigs_bulk)

    print(f"\n=== {label} ===")
    print(f"Total eigenvalues: {len(eigs)}, Bulk: {N_bulk}")
    print(f"Range: [{eigs_bulk[0]:.4f}, {eigs_bulk[-1]:.4f}]")
    print(f"Mean: {np.mean(eigs_bulk):.4f}, Std: {np.std(eigs_bulk):.4f}")

    if N_bulk < 50:
        print("Too few bulk eigenvalues for meaningful statistics")
        return None

    # Unfold
    unfolded = unfold_eigenvalues(eigs_bulk)
    spacings = np.diff(unfolded)
    mean_sp = np.mean(spacings)
    if mean_sp <= 0:
        print("Unfolding failed (negative mean spacing)")
        return None
    spacings_norm = spacings / mean_sp
    good_spacings = spacings_norm[spacings_norm > 0]

    print(f"Mean spacing: {mean_sp:.4f}, Std of normalized spacing: {np.std(good_spacings):.4f}")

    # NN spacing histogram
    hist_s, edges_s = np.histogram(good_spacings, bins=40, range=(0, 4), density=True)
    centers_s = (edges_s[:-1] + edges_s[1:]) / 2

    # Reference distributions
    def poisson(s): return np.exp(-s)
    def goe(s): return (np.pi/2)*s*np.exp(-np.pi*s**2/4)
    def gue(s): return (32/np.pi**2)*s**2*np.exp(-4*s**2/np.pi)

    def chi2(obs, centers, fn):
        th = fn(centers)
        mask = th > 0.01
        return np.mean((obs[mask] - th[mask])**2 / th[mask])

    c_p = chi2(hist_s, centers_s, poisson)
    c_o = chi2(hist_s, centers_s, goe)
    c_u = chi2(hist_s, centers_s, gue)

    print(f"Chi2 to Poisson: {c_p:.4f}")
    print(f"Chi2 to GOE:     {c_o:.4f}")
    print(f"Chi2 to GUE:     {c_u:.4f}")
    best = min([('Poisson', c_p), ('GOE', c_o), ('GUE', c_u)], key=lambda x: x[1])
    print(f"Best match: {best[0]}")

    # Level repulsion
    small_mask = good_spacings < 0.5
    small_s = good_spacings[small_mask]
    beta_fit = None
    if len(small_s) > 20:
        hist_small, edges_small = np.histogram(small_s, bins=15, range=(0.02, 0.5), density=True)
        centers_small = (edges_small[:-1] + edges_small[1:]) / 2
        mask_pos = hist_small > 0
        if np.sum(mask_pos) > 3:
            coeffs = np.polyfit(np.log(centers_small[mask_pos]), np.log(hist_small[mask_pos]), 1)
            beta_fit = coeffs[0]
            print(f"Level repulsion beta: {beta_fit:.3f} (Poisson=0, GOE=1, GUE=2)")

    # Number variance for a few L values
    L_test = [1, 5, 10]
    print(f"Number variance:")
    for L in L_test:
        n_samples = min(500, N_bulk)
        starts = np.linspace(unfolded[0], unfolded[-1] - L, n_samples)
        vars_list = []
        for x0 in starts:
            count = np.sum((unfolded >= x0) & (unfolded < x0 + L))
            vars_list.append((count - L)**2)
        sv = np.mean(vars_list)
        gue_sv = (2/np.pi**2) * np.log(2*np.pi*L) + 0.442
        print(f"  L={L}: Sigma2={sv:.4f}, GUE={gue_sv:.4f}, ratio={sv/gue_sv:.3f}")

    return {
        'chi2_poisson': float(c_p),
        'chi2_goe': float(c_o),
        'chi2_gue': float(c_u),
        'best_match': best[0],
        'beta_fit': float(beta_fit) if beta_fit else None,
        'N_bulk': N_bulk,
        'spacing_std': float(np.std(good_spacings)),
    }


# ============================================================
# Variant A: Normalized von Mangoldt: a(n) = Lambda(n)/sqrt(n)
# ============================================================
print("\n" + "="*60)
print("VARIANT A: Normalized von Mangoldt (Lambda(n)/sqrt(n))")
print("="*60)

N_A = 500
a_norm = np.zeros(N_A + 2)
for n in range(1, N_A + 2):
    a_norm[n] = Lambda_vals[n] / np.sqrt(n)

T_A = build_toeplitz_matrix(a_norm, N_A, diag_val=0.0)
eigs_A = np.linalg.eigvalsh(T_A)
np.save(f'{base_dir}/eigs_varA_N500.npy', eigs_A)
results_A = compute_spacing_stats(eigs_A, "Variant A: Normalized vM (N=500)")


# ============================================================
# Variant B: Möbius Toeplitz: a(n) = mu(n)
# ============================================================
print("\n" + "="*60)
print("VARIANT B: Möbius Toeplitz (mu(n))")
print("="*60)

N_B = 500
a_mu = np.zeros(N_B + 2)
for n in range(1, N_B + 2):
    a_mu[n] = mu_vals[n]

T_B = build_toeplitz_matrix(a_mu, N_B, diag_val=0.0)
eigs_B = np.linalg.eigvalsh(T_B)
np.save(f'{base_dir}/eigs_varB_N500.npy', eigs_B)
results_B = compute_spacing_stats(eigs_B, "Variant B: Möbius (N=500)")


# ============================================================
# Variant C: Log-zeta Hankel: H_{ij} = Lambda(i+j)
# ============================================================
print("\n" + "="*60)
print("VARIANT C: Log-zeta Hankel (Lambda(i+j))")
print("="*60)

N_C = 500
# H_{ij} = Lambda(i+j) where i,j go from 1 to N
# So we need Lambda(2) through Lambda(2*N)
H = np.zeros((N_C, N_C))
for i in range(N_C):
    for j in range(N_C):
        H[i, j] = Lambda_vals[(i+1) + (j+1)]  # 1-indexed: Lambda(i+j) for i,j=1..N

# Make it symmetric (it already is since H_{ij} = Lambda(i+j) = Lambda(j+i) = H_{ji})
eigs_C = np.linalg.eigvalsh(H)
np.save(f'{base_dir}/eigs_varC_N500.npy', eigs_C)
results_C = compute_spacing_stats(eigs_C, "Variant C: Hankel (N=500)")


# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("SUMMARY OF ALL VARIANTS")
print("="*60)

all_results = {}
for name, res in [("Von Mangoldt Toeplitz (original)", None),
                   ("Variant A: Normalized vM", results_A),
                   ("Variant B: Möbius", results_B),
                   ("Variant C: Hankel", results_C)]:
    if res:
        print(f"\n{name}:")
        print(f"  Best match: {res['best_match']}")
        print(f"  Chi2: Poisson={res['chi2_poisson']:.4f}, GOE={res['chi2_goe']:.4f}, GUE={res['chi2_gue']:.4f}")
        print(f"  Beta: {res['beta_fit']}")
        print(f"  Spacing std: {res['spacing_std']:.4f} (Poisson=1.0, GOE≈0.52, GUE≈0.42)")
        all_results[name] = res

with open(f'{base_dir}/results_part3.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print("\nPart 3 complete.")
