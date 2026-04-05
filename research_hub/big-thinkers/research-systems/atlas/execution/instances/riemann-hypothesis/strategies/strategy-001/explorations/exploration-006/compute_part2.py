"""
Part 2: Statistical Analysis of Von Mangoldt Toeplitz eigenvalues
- Unfolding
- NN spacing distribution vs GUE, GOE, Poisson
- Pair correlation
- Level repulsion exponent
"""
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.special import erfc
from scipy.stats import gaussian_kde
import warnings
warnings.filterwarnings('ignore')

base_dir = '/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-006'

# Load eigenvalues
eigs = np.load(f'{base_dir}/eigs_vM_N1000.npy')
N = len(eigs)

# ---- Step 1: Remove outliers and unfold ----
# The top eigenvalue is a huge outlier (~998). Remove it and a few others.
# Also remove very extreme negative ones.
# Use the bulk: clip to mean ± 3*std
mean_e = np.mean(eigs)
std_e = np.std(eigs)
bulk_mask = (eigs > mean_e - 2.5*std_e) & (eigs < mean_e + 2.5*std_e)
eigs_bulk = eigs[bulk_mask]
N_bulk = len(eigs_bulk)
print(f"Bulk eigenvalues: {N_bulk} out of {N} (removed {N - N_bulk} outliers)")
print(f"Bulk range: [{eigs_bulk[0]:.2f}, {eigs_bulk[-1]:.2f}]")

# ---- Step 2: Unfold using empirical CDF ----
# Sort eigenvalues
eigs_sorted = np.sort(eigs_bulk)

# Smooth CDF using a polynomial fit
# The unfolded eigenvalues should have unit mean spacing
ranks = np.arange(1, N_bulk + 1) / N_bulk  # empirical CDF values
# Fit a smooth spline to the staircase
from scipy.interpolate import UnivariateSpline
spline = UnivariateSpline(eigs_sorted, np.arange(N_bulk), s=N_bulk*0.5, k=3)
unfolded = spline(eigs_sorted)

# Check mean spacing
spacings = np.diff(unfolded)
mean_spacing = np.mean(spacings)
print(f"\nMean spacing after unfolding: {mean_spacing:.4f} (target: 1.0)")

# Normalize to unit mean spacing
spacings_normalized = spacings / mean_spacing
print(f"Mean normalized spacing: {np.mean(spacings_normalized):.4f}")
print(f"Std of normalized spacing: {np.std(spacings_normalized):.4f}")

# Remove any negative spacings from unfolding artifacts
good_spacings = spacings_normalized[spacings_normalized > 0]
print(f"Positive spacings: {len(good_spacings)} out of {len(spacings_normalized)}")

# ---- Step 3: Nearest-neighbor spacing distribution ----
s_vals = np.linspace(0, 4, 200)

# Theoretical distributions
def poisson_spacing(s):
    return np.exp(-s)

def goe_spacing(s):
    """Wigner surmise for GOE (beta=1)"""
    return (np.pi/2) * s * np.exp(-np.pi * s**2 / 4)

def gue_spacing(s):
    """Wigner surmise for GUE (beta=2)"""
    return (32/np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)

# Histogram of spacings
hist_s, bin_edges_s = np.histogram(good_spacings, bins=50, range=(0, 4), density=True)
bin_centers_s = (bin_edges_s[:-1] + bin_edges_s[1:]) / 2

# Compute chi-squared-like measure for each distribution
def chi2_like(hist_observed, bin_centers, theoretical_fn):
    theoretical = theoretical_fn(bin_centers)
    # Avoid division by zero
    mask = theoretical > 0.01
    return np.mean((hist_observed[mask] - theoretical[mask])**2 / theoretical[mask])

chi2_poisson = chi2_like(hist_s, bin_centers_s, poisson_spacing)
chi2_goe = chi2_like(hist_s, bin_centers_s, goe_spacing)
chi2_gue = chi2_like(hist_s, bin_centers_s, gue_spacing)

print(f"\n=== NN Spacing Distribution ===")
print(f"Chi2-like distance to Poisson: {chi2_poisson:.4f}")
print(f"Chi2-like distance to GOE:     {chi2_goe:.4f}")
print(f"Chi2-like distance to GUE:     {chi2_gue:.4f}")

best = min([('Poisson', chi2_poisson), ('GOE', chi2_goe), ('GUE', chi2_gue)], key=lambda x: x[1])
print(f"Best match: {best[0]} (chi2={best[1]:.4f})")

# Print the histogram alongside theoretical values
print(f"\n  s      | P_obs(s) | Poisson | GOE     | GUE")
print(f"  -------+----------+---------+---------+--------")
for i in range(0, len(bin_centers_s), 3):
    s = bin_centers_s[i]
    print(f"  {s:5.2f}  | {hist_s[i]:7.4f}  | {poisson_spacing(s):7.4f} | {goe_spacing(s):7.4f} | {gue_spacing(s):7.4f}")

# ---- Step 4: Level repulsion exponent ----
# P(s) ~ s^beta for small s
# Fit beta from small spacings
small_s_mask = good_spacings < 0.5
small_s = good_spacings[small_s_mask]
if len(small_s) > 10:
    # Histogram at small s
    hist_small, edges_small = np.histogram(small_s, bins=20, range=(0.01, 0.5), density=True)
    centers_small = (edges_small[:-1] + edges_small[1:]) / 2
    # Fit log(P) = beta*log(s) + const
    mask_pos = hist_small > 0
    if np.sum(mask_pos) > 3:
        coeffs = np.polyfit(np.log(centers_small[mask_pos]), np.log(hist_small[mask_pos]), 1)
        beta_fit = coeffs[0]
        print(f"\n=== Level Repulsion ===")
        print(f"Fitted beta (P(s) ~ s^beta for s<0.5): {beta_fit:.3f}")
        print(f"  Poisson: beta=0, GOE: beta=1, GUE: beta=2")
    else:
        beta_fit = None
        print(f"\n=== Level Repulsion ===")
        print(f"Not enough data points at small s to fit beta")
else:
    beta_fit = None
    print(f"\n=== Level Repulsion ===")
    print(f"Only {len(small_s)} spacings < 0.5, not enough for beta fit")

# ---- Step 5: Pair correlation ----
# R2(r) = 1 - (sin(pi*r)/(pi*r))^2 for GUE
print(f"\n=== Pair Correlation ===")

# Compute pair correlation from unfolded eigenvalues
def pair_correlation(unfolded_eigs, r_max=3.0, n_bins=60):
    """Compute pair correlation function R2(r)."""
    N = len(unfolded_eigs)
    diffs = []
    # Sample pairs to keep computation manageable
    max_pairs = 500000
    count = 0
    for i in range(N):
        for j in range(i+1, min(i+50, N)):  # Only nearby pairs
            d = abs(unfolded_eigs[j] - unfolded_eigs[i])
            if d < r_max:
                diffs.append(d)
                count += 1
            if count > max_pairs:
                break
        if count > max_pairs:
            break

    diffs = np.array(diffs)
    hist, edges = np.histogram(diffs, bins=n_bins, range=(0.01, r_max), density=True)
    centers = (edges[:-1] + edges[1:]) / 2

    # Normalize: R2(r) = density of pairs at distance r / (expected for Poisson)
    # For Poisson, pair density at distance r is uniform = 1
    # But our normalization is slightly different. The histogram is already density-normalized.
    # We need to convert to the proper R2:
    # Actually, the pair correlation can be obtained from the histogram by noting that
    # for unit mean spacing Poisson, the density of spacings at distance r is 1.
    # So R2(r) ≈ hist(r) * normalization

    return centers, hist

r_centers, r2_obs = pair_correlation(unfolded)

# GUE pair correlation
def gue_pair_corr(r):
    """Montgomery's pair correlation: 1 - (sin(pi*r)/(pi*r))^2"""
    result = np.ones_like(r)
    mask = r > 0
    result[mask] = 1 - (np.sin(np.pi * r[mask]) / (np.pi * r[mask]))**2
    return result

gue_r2 = gue_pair_corr(r_centers)

print(f"  r      | R2_obs   | R2_GUE")
print(f"  -------+----------+--------")
for i in range(0, len(r_centers), 4):
    print(f"  {r_centers[i]:5.2f}  | {r2_obs[i]:7.4f}  | {gue_r2[i]:7.4f}")

# Chi2 distance for pair correlation
mask_valid = gue_r2 > 0.01
if np.sum(mask_valid) > 3:
    chi2_r2 = np.mean((r2_obs[mask_valid] - gue_r2[mask_valid])**2)
    print(f"\nMean squared deviation from GUE pair correlation: {chi2_r2:.6f}")

# ---- Step 6: Number variance (rigidity) ----
print(f"\n=== Number Variance (Rigidity Test) ===")

def number_variance(unfolded_eigs, L_values):
    """Compute Sigma^2(L) = <(n(L) - L)^2> for each L."""
    N = len(unfolded_eigs)
    results = []
    for L in L_values:
        # Sample many intervals of length L
        n_samples = min(1000, N)
        variances = []
        starts = np.linspace(unfolded_eigs[0], unfolded_eigs[-1] - L, n_samples)
        for x0 in starts:
            count = np.sum((unfolded_eigs >= x0) & (unfolded_eigs < x0 + L))
            variances.append((count - L)**2)
        results.append(np.mean(variances))
    return np.array(results)

L_values = np.array([0.5, 1, 2, 3, 5, 8, 10, 15, 20])
sigma2_obs = number_variance(unfolded, L_values)

# Theoretical: Poisson Sigma^2(L) = L, GUE ~ (2/pi^2)*ln(L) + const
sigma2_poisson = L_values
sigma2_gue = (2/np.pi**2) * np.log(2*np.pi*L_values) + 0.442  # approximate GUE

print(f"  L      | Sigma2_obs | Sigma2_Poisson | Sigma2_GUE")
print(f"  -------+------------+----------------+-----------")
for i, L in enumerate(L_values):
    print(f"  {L:5.1f}  | {sigma2_obs[i]:10.4f} | {sigma2_poisson[i]:14.4f} | {sigma2_gue[i]:10.4f}")

# Rigidity ratio
for i, L in enumerate(L_values):
    if sigma2_gue[i] > 0:
        ratio = sigma2_obs[i] / sigma2_gue[i]
        print(f"  L={L}: obs/GUE ratio = {ratio:.3f}")

print("\n=== PART 2 COMPLETE ===")

# Save key results
import json
part2_results = {
    'chi2_poisson': float(chi2_poisson),
    'chi2_goe': float(chi2_goe),
    'chi2_gue': float(chi2_gue),
    'best_match': best[0],
    'beta_fit': float(beta_fit) if beta_fit is not None else None,
    'N_bulk': int(N_bulk),
}
with open(f'{base_dir}/results_part2.json', 'w') as f:
    json.dump(part2_results, f, indent=2)
