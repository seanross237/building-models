"""Validation and refined analysis."""
import numpy as np
import json

# Load zeros
data = np.load('zeros_data.npz')
t = data['t']
x = data['x']
N = len(x)
gamma_em = 0.5772156649015329

print("="*60)
print("VALIDATION: Compare zeta zeros against Poisson and GUE simulation")
print("="*60)

# ============================================================
# 1. Validate Σ² computation against Poisson (should give Σ² ≈ L)
# ============================================================
print("\n--- Poisson Validation ---")
np.random.seed(42)
poisson_spacings = np.random.exponential(1.0, N - 1)
poisson_x = np.cumsum(np.concatenate([[0], poisson_spacings]))

L_test = [0.5, 1.0, 2.0, 5.0, 10.0, 50.0]
for L in L_test:
    step = max(0.5, L / 10.0)
    starts = np.arange(poisson_x[0], poisson_x[-1] - L, step)
    counts = np.zeros(len(starts))
    for j, s in enumerate(starts):
        left = np.searchsorted(poisson_x, s, side='left')
        right = np.searchsorted(poisson_x, s + L, side='right')
        counts[j] = right - left
    var_poisson = np.var(counts)
    print(f"  L={L:6.1f}: Σ²_poisson = {var_poisson:.3f}, expected ≈ {L:.3f}, ratio = {var_poisson/L:.3f}")

# ============================================================
# 2. Simulate a GUE matrix and compute its Σ²
# ============================================================
print("\n--- GUE Matrix Simulation Validation ---")
# Generate GUE eigenvalues (N x N Hermitian matrix)
M = 2000
rng = np.random.default_rng(42)
H_real = rng.standard_normal((M, M))
H_imag = rng.standard_normal((M, M))
H = (H_real + H_real.T) / 2.0 + 1j * (H_imag - H_imag.T) / 2.0
H = (H + H.conj().T) / (2.0 * np.sqrt(2 * M))
eigenvalues = np.sort(np.real(np.linalg.eigvalsh(H)))

# Unfold GUE eigenvalues using Wigner semicircle
# rho(E) = (2M)/(pi) * sqrt(1 - E^2) for |E| < 1
# Use bulk eigenvalues only (middle 50%)
idx_start = M // 4
idx_end = 3 * M // 4
eigs_bulk = eigenvalues[idx_start:idx_end]

# Unfold using empirical CDF
from scipy.interpolate import interp1d
# Local unfolding: use a polynomial fit to the integrated density
rank = np.arange(len(eigs_bulk))
# Fit polynomial to rank vs eigenvalue to get smooth N(E)
poly_coeffs = np.polyfit(eigs_bulk, rank, 5)
gue_x = np.polyval(poly_coeffs, eigs_bulk)

# Rescale so mean spacing = 1
gue_spacings = np.diff(gue_x)
gue_x = gue_x / np.mean(gue_spacings)
print(f"  GUE matrix: {len(gue_x)} bulk eigenvalues, mean spacing = {np.mean(np.diff(gue_x)):.4f}")

def sigma2_gue_theory(L):
    return (2.0 / np.pi**2) * (np.log(2 * np.pi * L) + gamma_em + 1 - np.pi**2 / 8)

print(f"\n  {'L':>8s} {'Σ²_zeta':>10s} {'Σ²_GUE_sim':>12s} {'Σ²_GUE_th':>11s} {'Σ²_Poisson':>12s}")
for L in [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]:
    step = max(0.5, L / 10.0)

    # Zeta
    starts_z = np.arange(x[0], x[-1] - L, step)
    counts_z = np.array([np.searchsorted(x, s + L, side='right') - np.searchsorted(x, s, side='left')
                          for s in starts_z])
    var_z = np.var(counts_z)

    # GUE sim
    starts_g = np.arange(gue_x[0], gue_x[-1] - L, step)
    counts_g = np.array([np.searchsorted(gue_x, s + L, side='right') - np.searchsorted(gue_x, s, side='left')
                          for s in starts_g])
    var_g = np.var(counts_g)

    # Poisson
    starts_p = np.arange(poisson_x[0], poisson_x[-1] - L, step)
    counts_p = np.array([np.searchsorted(poisson_x, s + L, side='right') - np.searchsorted(poisson_x, s, side='left')
                          for s in starts_p])
    var_p = np.var(counts_p)

    th = sigma2_gue_theory(L)
    print(f"  {L:8.1f} {var_z:10.4f} {var_g:12.4f} {th:11.4f} {var_p:12.4f}")

# ============================================================
# 3. More careful saturation analysis
# ============================================================
print("\n" + "="*60)
print("DETAILED SATURATION ANALYSIS")
print("="*60)

# Compute Σ² with finer sampling for both zeta and GUE sim
L_fine = np.logspace(np.log10(0.3), np.log10(200), 80)
sigma2_zeta = []
sigma2_gue_sim = []
sigma2_gue_th = []

for L in L_fine:
    step = max(0.5, L / 10.0)

    # Zeta
    starts_z = np.arange(x[0], x[-1] - L, step)
    if len(starts_z) < 10:
        sigma2_zeta.append(np.nan)
        sigma2_gue_sim.append(np.nan)
        sigma2_gue_th.append(sigma2_gue_theory(L))
        continue
    counts_z = np.array([np.searchsorted(x, s + L, side='right') - np.searchsorted(x, s, side='left')
                          for s in starts_z])
    sigma2_zeta.append(np.var(counts_z))

    # GUE sim
    starts_g = np.arange(gue_x[0], gue_x[-1] - L, step)
    if len(starts_g) < 10:
        sigma2_gue_sim.append(np.nan)
    else:
        counts_g = np.array([np.searchsorted(gue_x, s + L, side='right') - np.searchsorted(gue_x, s, side='left')
                              for s in starts_g])
        sigma2_gue_sim.append(np.var(counts_g))

    sigma2_gue_th.append(sigma2_gue_theory(L))

sigma2_zeta = np.array(sigma2_zeta)
sigma2_gue_sim = np.array(sigma2_gue_sim)
sigma2_gue_th = np.array(sigma2_gue_th)

valid = ~np.isnan(sigma2_zeta) & ~np.isnan(sigma2_gue_sim) & (sigma2_gue_th > 0)
L_v = L_fine[valid]
sz = sigma2_zeta[valid]
sg = sigma2_gue_sim[valid]
st = sigma2_gue_th[valid]

print(f"\n  Comparison: Zeta vs GUE sim vs GUE theory")
print(f"  {'L':>8s} {'Σ²_zeta':>10s} {'Σ²_GUEsim':>11s} {'Σ²_GUEth':>10s} {'zeta/sim':>9s} {'sim/th':>8s}")
for i in range(0, len(L_v), 5):
    ratio_zs = sz[i] / sg[i] if sg[i] > 0 else np.nan
    ratio_st = sg[i] / st[i] if st[i] > 0 else np.nan
    print(f"  {L_v[i]:8.2f} {sz[i]:10.4f} {sg[i]:11.4f} {st[i]:10.4f} {ratio_zs:9.3f} {ratio_st:8.3f}")

# Key question: Does GUE sim also saturate (finite-size effect) or does only zeta saturate?
print("\n  Slope analysis (log-log):")
# Large L regime
large_mask = L_v > 10
if np.sum(large_mask) > 3:
    slope_z = np.polyfit(np.log(L_v[large_mask]), sz[large_mask], 1)[0]
    slope_g = np.polyfit(np.log(L_v[large_mask]), sg[large_mask], 1)[0]
    slope_t = np.polyfit(np.log(L_v[large_mask]), st[large_mask], 1)[0]
    print(f"  For L > 10:")
    print(f"    Zeta slope (dΣ²/d ln L): {slope_z:.4f}")
    print(f"    GUE sim slope:            {slope_g:.4f}")
    print(f"    GUE theory slope:         {slope_t:.4f}")
    print(f"    Zeta/GUEsim ratio:        {slope_z/slope_g:.3f}" if slope_g != 0 else "")

# ============================================================
# 4. Spectral Rigidity: Compare GUE sim to zeta
# ============================================================
print("\n" + "="*60)
print("SPECTRAL RIGIDITY: GUE sim comparison")
print("="*60)

def compute_delta3(x_zeros, L, step=None):
    """Compute Delta_3(L) by averaging over intervals."""
    if step is None:
        step = max(1.0, L / 5.0)

    starts = np.arange(x_zeros[0], x_zeros[-1] - L, step)
    if len(starts) < 5:
        return np.nan

    d3_vals = []
    for x_start in starts:
        x_end = x_start + L
        idx_start = np.searchsorted(x_zeros, x_start, side='left')
        idx_end = np.searchsorted(x_zeros, x_end, side='right')
        zs_in = x_zeros[idx_start:idx_end]
        zs_in = zs_in[(zs_in > x_start) & (zs_in < x_end)]
        if len(zs_in) < 2:
            continue

        bp = np.concatenate([[x_start], zs_in, [x_end]])
        n_staircase = np.arange(len(bp) - 1, dtype=float)
        widths = np.diff(bp)

        int_N2 = np.sum(n_staircase**2 * widths)
        int_N = np.sum(n_staircase * widths)
        int_Nx = np.sum(n_staircase * (bp[1:]**2 - bp[:-1]**2) / 2.0)
        int_1 = L
        int_x = (x_end**2 - x_start**2) / 2.0
        int_x2 = (x_end**3 - x_start**3) / 3.0

        A_mat = np.array([[int_1, int_x], [int_x, int_x2]])
        b_vec = np.array([int_N, int_Nx])

        try:
            a_opt, b_opt = np.linalg.solve(A_mat, b_vec)
        except np.linalg.LinAlgError:
            continue

        integral = (int_N2 - 2*a_opt*int_N - 2*b_opt*int_Nx
                    + a_opt**2*int_1 + 2*a_opt*b_opt*int_x + b_opt**2*int_x2)
        d3_vals.append(integral / L)

    return np.mean(d3_vals) if d3_vals else np.nan

def delta3_gue_theory(L):
    return (1.0 / np.pi**2) * (np.log(2 * np.pi * L) + gamma_em - 5.0/4.0 - np.pi**2/12.0)

L_d3 = np.logspace(np.log10(1.0), np.log10(100), 25)
print(f"\n  {'L':>8s} {'Δ3_zeta':>10s} {'Δ3_GUEsim':>11s} {'Δ3_GUEth':>10s} {'zeta/sim':>9s}")
for L in L_d3:
    d3_z = compute_delta3(x, L)
    d3_g = compute_delta3(gue_x, L)
    d3_t = delta3_gue_theory(L)
    ratio = d3_z / d3_g if d3_g > 0 and not np.isnan(d3_g) else np.nan
    print(f"  {L:8.2f} {d3_z:10.4f} {d3_g:11.4f} {d3_t:10.4f} {ratio:9.3f}" if not np.isnan(ratio)
          else f"  {L:8.2f} {d3_z:10.4f} {'N/A':>11s} {d3_t:10.4f} {'N/A':>9s}")

# ============================================================
# 5. Berry saturation scale estimation
# ============================================================
print("\n" + "="*60)
print("BERRY SATURATION SCALE ESTIMATION")
print("="*60)

# For zeros at height T, L_max ~ T/(2*pi) * log(T/(2*pi))
# Our zeros range from T~14 to T~2515
# We're averaging over all heights, so use geometric mean T ~ sqrt(14*2515) ~ 188
T_geo = np.sqrt(14 * 2515)
T_mid = (14 + 2515) / 2.0
L_max_geo = T_geo / (2*np.pi) * np.log(T_geo / (2*np.pi))
L_max_mid = T_mid / (2*np.pi) * np.log(T_mid / (2*np.pi))
print(f"  T range: 14 to 2515")
print(f"  Geometric mean T: {T_geo:.1f}")
print(f"  L_max (geometric mean): {L_max_geo:.1f}")
print(f"  L_max (arithmetic mean T={T_mid:.0f}): {L_max_mid:.1f}")
print(f"  Our computation range: L = 0.1 to 100")
print(f"  Our L_max is much larger than our L range.")
print(f"  => Berry saturation should NOT be detectable in our L range")
print(f"  => The saturation we see must be a different effect")

# What about the actual formula for Berry's saturated Σ²?
# Berry 1985: Σ²_sat(L) = K_eff + (1/π²) * sum_{p prime} (ln p)² / p * ...
# For L >> L_max, Σ² approaches a constant.
# The GUE sim comparison will tell us if this is a finite-size artifact.

# Check: at what L does GUE sim start deviating from theory?
print(f"\n  Checking where GUE sim deviates from theory:")
for i in range(len(L_v)):
    if st[i] > 0 and sg[i] > 0:
        ratio = sg[i] / st[i]
        if ratio < 0.8 or ratio > 1.2:
            print(f"    GUE sim deviates >20% at L={L_v[i]:.1f}: sim={sg[i]:.4f}, th={st[i]:.4f}, ratio={ratio:.3f}")

# ============================================================
# 6. Refined Form Factor with more averaging
# ============================================================
print("\n" + "="*60)
print("REFINED SPECTRAL FORM FACTOR")
print("="*60)

# Use subsections of zeros to get ensemble averaging
# Split into 10 overlapping blocks of ~300 zeros each
block_size = 400
n_blocks = (N - block_size) // 100
tau_vals = np.linspace(0.01, 3.0, 200)

K_ensemble = np.zeros(len(tau_vals))
n_valid_blocks = 0

for b in range(0, N - block_size, 100):
    x_block = x[b:b+block_size]
    # Re-unfold within block (subtract mean and rescale)
    x_local = x_block - x_block[0]
    local_spacing = np.mean(np.diff(x_local))
    x_local = x_local / local_spacing
    N_block = len(x_local)

    for i, tau in enumerate(tau_vals):
        phases = 2 * np.pi * tau * x_local
        sum_real = np.sum(np.cos(phases))
        sum_imag = np.sum(np.sin(phases))
        K_ensemble[i] += (sum_real**2 + sum_imag**2) / N_block

    n_valid_blocks += 1

K_ensemble /= n_valid_blocks
print(f"  Averaged over {n_valid_blocks} blocks of {block_size} zeros")

# Also compute GUE sim form factor
K_gue_sim = np.zeros(len(tau_vals))
gue_block_size = min(400, len(gue_x) // 2)
n_gue_blocks = 0

for b in range(0, len(gue_x) - gue_block_size, 100):
    x_block = gue_x[b:b+gue_block_size]
    x_local = x_block - x_block[0]
    local_spacing = np.mean(np.diff(x_local))
    x_local = x_local / local_spacing
    N_block = len(x_local)

    for i, tau in enumerate(tau_vals):
        phases = 2 * np.pi * tau * x_local
        sum_real = np.sum(np.cos(phases))
        sum_imag = np.sum(np.sin(phases))
        K_gue_sim[i] += (sum_real**2 + sum_imag**2) / N_block

    n_gue_blocks += 1

K_gue_sim /= n_gue_blocks
print(f"  GUE sim: averaged over {n_gue_blocks} blocks of {gue_block_size}")

K_gue_th = np.array([tau if tau < 1 else 1.0 for tau in tau_vals])

# Smooth all with running average
w = 11
K_z_smooth = np.convolve(K_ensemble, np.ones(w)/w, mode='same')
K_g_smooth = np.convolve(K_gue_sim, np.ones(w)/w, mode='same')

print(f"\n  {'tau':>8s} {'K_zeta':>10s} {'K_GUEsim':>10s} {'K_GUEth':>8s}")
for i in range(0, len(tau_vals), 10):
    print(f"  {tau_vals[i]:8.3f} {K_z_smooth[i]:10.4f} {K_g_smooth[i]:10.4f} {K_gue_th[i]:8.4f}")

# Ramp and plateau analysis
ramp_mask = (tau_vals > 0.1) & (tau_vals < 0.8)
plateau_mask = (tau_vals > 1.3) & (tau_vals < 2.5)

if np.sum(ramp_mask) > 5:
    slope_z = np.polyfit(tau_vals[ramp_mask], K_z_smooth[ramp_mask], 1)
    slope_g = np.polyfit(tau_vals[ramp_mask], K_g_smooth[ramp_mask], 1)
    print(f"\n  Ramp (0.1 < tau < 0.8):")
    print(f"    Zeta slope: {slope_z[0]:.3f} (GUE theory: 1.0)")
    print(f"    GUE sim slope: {slope_g[0]:.3f}")

if np.sum(plateau_mask) > 5:
    plat_z = np.mean(K_z_smooth[plateau_mask])
    plat_g = np.mean(K_g_smooth[plateau_mask])
    plat_z_std = np.std(K_z_smooth[plateau_mask])
    plat_g_std = np.std(K_g_smooth[plateau_mask])
    print(f"  Plateau (1.3 < tau < 2.5):")
    print(f"    Zeta mean: {plat_z:.3f} ± {plat_z_std:.3f}")
    print(f"    GUE sim mean: {plat_g:.3f} ± {plat_g_std:.3f}")
    print(f"    GUE theory: 1.000")

print("\n=== DONE ===")
