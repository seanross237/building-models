"""Parts 1-3: Number Variance, Spectral Rigidity, and Spectral Form Factor."""
import numpy as np
import json
import time

# Load zeros
data = np.load('zeros_data.npz')
t = data['t']
x = data['x']
N = len(x)

print(f"Loaded {N} zeros")
print(f"Unfolded range: [{x[0]:.4f}, {x[-1]:.4f}]")
print(f"Mean spacing: {np.mean(np.diff(x)):.6f}")

gamma_em = 0.5772156649015329  # Euler-Mascheroni constant

results = {}

# ============================================================
# PART 1: Number Variance Sigma^2(L)
# ============================================================
print("\n" + "="*60)
print("PART 1: Number Variance Sigma^2(L)")
print("="*60)

def sigma2_gue(L):
    """GUE prediction for number variance."""
    return (2.0 / np.pi**2) * (np.log(2 * np.pi * L) + gamma_em + 1 - np.pi**2 / 8)

# L values: logarithmically spaced from 0.1 to 100, 50 points
L_values_nv = np.logspace(np.log10(0.1), np.log10(100), 50)

sigma2_data = []
sigma2_gue_vals = []

t_start = time.time()

for i, L in enumerate(L_values_nv):
    # Slide window across unfolded zeros
    # Use step size appropriate for L
    step = max(0.5, L / 10.0)  # adaptive step

    # Range of window starts
    x_min_start = x[0]
    x_max_start = x[-1] - L

    if x_max_start <= x_min_start:
        sigma2_data.append(np.nan)
        sigma2_gue_vals.append(sigma2_gue(L))
        continue

    # Generate window start positions
    starts = np.arange(x_min_start, x_max_start, step)

    # For each start, count zeros in [start, start+L]
    counts = np.zeros(len(starts))
    for j, s in enumerate(starts):
        # Binary search for efficiency
        left = np.searchsorted(x, s, side='left')
        right = np.searchsorted(x, s + L, side='right')
        counts[j] = right - left

    var_n = np.var(counts)
    sigma2_data.append(float(var_n))
    sigma2_gue_vals.append(float(sigma2_gue(L)))

    if (i + 1) % 10 == 0:
        print(f"  L={L:.2f}: Sigma^2 = {var_n:.4f} (GUE = {sigma2_gue(L):.4f}), "
              f"windows={len(starts)}")

elapsed_nv = time.time() - t_start
print(f"Number variance computed in {elapsed_nv:.1f}s")

sigma2_data = np.array(sigma2_data)
sigma2_gue_vals = np.array(sigma2_gue_vals)

# Find valid entries
valid = ~np.isnan(sigma2_data) & (sigma2_data > 0) & (sigma2_gue_vals > 0)
L_valid_nv = L_values_nv[valid]
s2_valid = sigma2_data[valid]
s2_gue_valid = sigma2_gue_vals[valid]

# Deviations
abs_dev_nv = np.abs(s2_valid - s2_gue_valid)
rel_dev_nv = abs_dev_nv / s2_gue_valid * 100

max_abs_idx = np.argmax(abs_dev_nv)
max_rel_idx = np.argmax(rel_dev_nv)

print(f"\nNumber Variance Results:")
print(f"  Valid L points: {np.sum(valid)}")
print(f"  Max abs deviation: {abs_dev_nv[max_abs_idx]:.4f} at L={L_valid_nv[max_abs_idx]:.2f}")
print(f"  Max rel deviation: {rel_dev_nv[max_rel_idx]:.1f}% at L={L_valid_nv[max_rel_idx]:.2f}")
print(f"  Mean abs deviation: {np.mean(abs_dev_nv):.4f}")
print(f"  Mean rel deviation: {np.mean(rel_dev_nv):.1f}%")

# Check for saturation: compare slope at large L with GUE slope
# GUE is logarithmic, so d(sigma2)/d(log L) should be 2/pi^2 ~ 0.2026
# If saturating, slope should decrease
if len(L_valid_nv) > 10:
    # Split into two halves
    mid = len(L_valid_nv) // 2

    # Slope in log-space for second half (large L)
    log_L_large = np.log(L_valid_nv[mid:])
    s2_large = s2_valid[mid:]
    slope_large = np.polyfit(log_L_large, s2_large, 1)[0]

    # Slope in log-space for first half (small L)
    log_L_small = np.log(L_valid_nv[:mid])
    s2_small = s2_valid[:mid]
    slope_small = np.polyfit(log_L_small, s2_small, 1)[0]

    gue_slope = 2.0 / np.pi**2
    print(f"\n  GUE theoretical slope (d Sigma^2/d ln L): {gue_slope:.4f}")
    print(f"  Data slope (small L): {slope_small:.4f}")
    print(f"  Data slope (large L): {slope_large:.4f}")
    print(f"  Slope ratio (large/small): {slope_large/slope_small:.3f}")

    saturation_detected_nv = (slope_large < 0.7 * slope_small)
    print(f"  Saturation detected: {saturation_detected_nv}")

# Print full table
print(f"\n  Full Number Variance Table:")
print(f"  {'L':>10s} {'Sigma2_data':>12s} {'Sigma2_GUE':>12s} {'AbsDev':>10s} {'RelDev%':>8s}")
for i in range(len(L_valid_nv)):
    print(f"  {L_valid_nv[i]:10.3f} {s2_valid[i]:12.4f} {s2_gue_valid[i]:12.4f} "
          f"{abs_dev_nv[i]:10.4f} {rel_dev_nv[i]:8.1f}")

results['number_variance'] = {
    'L_values': L_valid_nv.tolist(),
    'sigma2_data': s2_valid.tolist(),
    'sigma2_gue': s2_gue_valid.tolist(),
    'max_abs_dev': float(abs_dev_nv[max_abs_idx]),
    'max_abs_dev_L': float(L_valid_nv[max_abs_idx]),
    'max_rel_dev': float(rel_dev_nv[max_rel_idx]),
    'max_rel_dev_L': float(L_valid_nv[max_rel_idx]),
    'mean_abs_dev': float(np.mean(abs_dev_nv)),
    'mean_rel_dev': float(np.mean(rel_dev_nv)),
    'slope_small_L': float(slope_small),
    'slope_large_L': float(slope_large),
    'gue_slope': float(gue_slope),
}

# ============================================================
# PART 2: Spectral Rigidity Delta_3(L)
# ============================================================
print("\n" + "="*60)
print("PART 2: Spectral Rigidity Delta_3(L)")
print("="*60)

def delta3_gue(L):
    """GUE prediction for spectral rigidity."""
    return (1.0 / np.pi**2) * (np.log(2 * np.pi * L) + gamma_em - 5.0/4.0 - np.pi**2/12.0)

def compute_delta3_interval(x_zeros, x_start, L):
    """Compute Delta_3 for a single interval [x_start, x_start+L].

    Delta_3 = min_{a,b} (1/L) * integral [N(x) - a - bx]^2 dx

    where N(x) is the staircase counting function.
    """
    x_end = x_start + L

    # Find zeros in this interval
    mask = (x_zeros >= x_start) & (x_zeros < x_end)
    zeros_in = x_zeros[mask]
    n_zeros = len(zeros_in)

    if n_zeros < 2:
        return np.nan

    # The staircase N(x) is piecewise constant, jumping by 1 at each zero.
    # We need N(x) relative to some offset. Let's define:
    # N(x) = number of zeros in x_zeros that are <= x and >= x_start
    # But we need the count relative to the whole sequence.

    # Actually, the standard approach:
    # N(x) jumps at each zero. Between zeros, it's constant.
    # The integral of [N(x) - a - bx]^2 over [x_start, x_end] can be computed
    # by summing contributions from each step of the staircase.

    # Let's set up the breakpoints
    # Include x_start and x_end
    # Find the first zero >= x_start
    idx_start = np.searchsorted(x_zeros, x_start, side='left')
    idx_end = np.searchsorted(x_zeros, x_end, side='right')

    # Breakpoints: x_start, zeros in interval, x_end
    breaks = [x_start]
    for idx in range(idx_start, idx_end):
        if x_zeros[idx] > x_start and x_zeros[idx] < x_end:
            breaks.append(x_zeros[idx])
    breaks.append(x_end)
    breaks = np.array(breaks)

    # N(x) value in each sub-interval [breaks[i], breaks[i+1])
    # N(breaks[0]+) = idx_start (number of zeros <= x_start in whole sequence)
    # Actually, we want N(x) = count of zeros in [x_start, x]
    # At x_start: N = 0
    # After first zero: N = 1, etc.

    n_vals = np.zeros(len(breaks) - 1)
    count = 0
    for i in range(len(breaks) - 1):
        # In interval [breaks[i], breaks[i+1]), N = count
        n_vals[i] = count
        # If breaks[i+1] is a zero (not x_end), increment
        if i + 1 < len(breaks) - 1:
            count += 1
    # Last interval: count = n_zeros if breaks[-1] is x_end
    # Actually need to be careful. Let me redo this.

    # Zeros in interval, sorted
    zs = x_zeros[idx_start:idx_end]
    zs_in = zs[(zs > x_start) & (zs < x_end)]

    # Breakpoints with staircase values
    bp = np.concatenate([[x_start], zs_in, [x_end]])
    n_staircase = np.zeros(len(bp) - 1)
    for i in range(len(bp) - 1):
        n_staircase[i] = i  # 0, 1, 2, ...

    # Now compute integrals needed for least-squares fit
    # We want min_{a,b} (1/L) * integral_{x_start}^{x_end} [N(x) - a - b*x]^2 dx
    #
    # Let y = x - x_start (shift to [0, L])
    # N(y) is piecewise constant
    # integral = sum over sub-intervals of n_i^2 * dy_i - 2*n_i*(a+b*(y_start_i+x_start))*dy_i + ...
    #
    # Actually, expand [N - a - bx]^2 = N^2 - 2N(a+bx) + (a+bx)^2
    # integral = int N^2 dx - 2*int N*(a+bx) dx + int (a+bx)^2 dx
    #
    # For piecewise constant N:
    # int N^2 dx = sum_i n_i^2 * (bp[i+1] - bp[i])
    # int N dx = sum_i n_i * (bp[i+1] - bp[i])
    # int N*x dx = sum_i n_i * (bp[i+1]^2 - bp[i]^2)/2

    widths = np.diff(bp)
    midpoints = (bp[:-1] + bp[1:]) / 2.0

    int_N2 = np.sum(n_staircase**2 * widths)
    int_N = np.sum(n_staircase * widths)
    int_Nx = np.sum(n_staircase * (bp[1:]**2 - bp[:-1]**2) / 2.0)
    int_1 = L
    int_x = (x_end**2 - x_start**2) / 2.0
    int_x2 = (x_end**3 - x_start**3) / 3.0

    # Minimize over a, b:
    # d/da = 0: -2*int_N + 2*a*int_1 + 2*b*int_x = 0
    #   => a*L + b*int_x = int_N
    # d/db = 0: -2*int_Nx + 2*a*int_x + 2*b*int_x2 = 0
    #   => a*int_x + b*int_x2 = int_Nx

    # Solve 2x2 system
    A_mat = np.array([[int_1, int_x], [int_x, int_x2]])
    b_vec = np.array([int_N, int_Nx])

    try:
        ab = np.linalg.solve(A_mat, b_vec)
    except np.linalg.LinAlgError:
        return np.nan

    a_opt, b_opt = ab

    # Compute the minimum value of the integral
    # integral = int_N2 - 2*a*int_N - 2*b*int_Nx + a^2*int_1 + 2*a*b*int_x + b^2*int_x2
    integral = (int_N2 - 2*a_opt*int_N - 2*b_opt*int_Nx
                + a_opt**2*int_1 + 2*a_opt*b_opt*int_x + b_opt**2*int_x2)

    return integral / L

# L values for Delta_3
L_values_d3 = np.logspace(np.log10(0.5), np.log10(100), 30)

delta3_data = []
delta3_gue_vals = []

t_start = time.time()

for i, L in enumerate(L_values_d3):
    step = max(1.0, L / 5.0)

    x_min_start = x[0]
    x_max_start = x[-1] - L

    if x_max_start <= x_min_start:
        delta3_data.append(np.nan)
        delta3_gue_vals.append(delta3_gue(L))
        continue

    starts = np.arange(x_min_start, x_max_start, step)

    d3_vals = []
    for s in starts:
        d3 = compute_delta3_interval(x, s, L)
        if not np.isnan(d3):
            d3_vals.append(d3)

    if len(d3_vals) > 0:
        d3_mean = np.mean(d3_vals)
    else:
        d3_mean = np.nan

    delta3_data.append(float(d3_mean))
    delta3_gue_vals.append(float(delta3_gue(L)))

    if (i + 1) % 5 == 0:
        elapsed = time.time() - t_start
        print(f"  L={L:.2f}: Delta_3 = {d3_mean:.4f} (GUE = {delta3_gue(L):.4f}), "
              f"windows={len(d3_vals)}, {elapsed:.1f}s")

elapsed_d3 = time.time() - t_start
print(f"Spectral rigidity computed in {elapsed_d3:.1f}s")

delta3_data = np.array(delta3_data)
delta3_gue_vals = np.array(delta3_gue_vals)

valid_d3 = ~np.isnan(delta3_data) & (delta3_data > 0) & (delta3_gue_vals > 0)
L_valid_d3 = L_values_d3[valid_d3]
d3_valid = delta3_data[valid_d3]
d3_gue_valid = delta3_gue_vals[valid_d3]

abs_dev_d3 = np.abs(d3_valid - d3_gue_valid)
rel_dev_d3 = abs_dev_d3 / d3_gue_valid * 100

max_abs_idx_d3 = np.argmax(abs_dev_d3)
max_rel_idx_d3 = np.argmax(rel_dev_d3)

print(f"\nSpectral Rigidity Results:")
print(f"  Valid L points: {np.sum(valid_d3)}")
print(f"  Max abs deviation: {abs_dev_d3[max_abs_idx_d3]:.4f} at L={L_valid_d3[max_abs_idx_d3]:.2f}")
print(f"  Max rel deviation: {rel_dev_d3[max_rel_idx_d3]:.1f}% at L={L_valid_d3[max_rel_idx_d3]:.2f}")
print(f"  Mean abs deviation: {np.mean(abs_dev_d3):.4f}")
print(f"  Mean rel deviation: {np.mean(rel_dev_d3):.1f}%")

# Check for saturation in Delta_3
if len(L_valid_d3) > 6:
    mid = len(L_valid_d3) // 2
    log_L_large = np.log(L_valid_d3[mid:])
    d3_large = d3_valid[mid:]
    slope_large_d3 = np.polyfit(log_L_large, d3_large, 1)[0]

    log_L_small = np.log(L_valid_d3[:mid])
    d3_small = d3_valid[:mid]
    slope_small_d3 = np.polyfit(log_L_small, d3_small, 1)[0]

    gue_slope_d3 = 1.0 / np.pi**2
    print(f"\n  GUE theoretical slope (d Delta_3/d ln L): {gue_slope_d3:.4f}")
    print(f"  Data slope (small L): {slope_small_d3:.4f}")
    print(f"  Data slope (large L): {slope_large_d3:.4f}")
    print(f"  Slope ratio (large/small): {slope_large_d3/slope_small_d3:.3f}")

print(f"\n  Full Spectral Rigidity Table:")
print(f"  {'L':>10s} {'Delta3_data':>12s} {'Delta3_GUE':>12s} {'AbsDev':>10s} {'RelDev%':>8s}")
for i in range(len(L_valid_d3)):
    print(f"  {L_valid_d3[i]:10.3f} {d3_valid[i]:12.4f} {d3_gue_valid[i]:12.4f} "
          f"{abs_dev_d3[i]:10.4f} {rel_dev_d3[i]:8.1f}")

results['spectral_rigidity'] = {
    'L_values': L_valid_d3.tolist(),
    'delta3_data': d3_valid.tolist(),
    'delta3_gue': d3_gue_valid.tolist(),
    'max_abs_dev': float(abs_dev_d3[max_abs_idx_d3]),
    'max_abs_dev_L': float(L_valid_d3[max_abs_idx_d3]),
    'max_rel_dev': float(rel_dev_d3[max_rel_idx_d3]),
    'max_rel_dev_L': float(L_valid_d3[max_rel_idx_d3]),
    'mean_abs_dev': float(np.mean(abs_dev_d3)),
    'mean_rel_dev': float(np.mean(rel_dev_d3)),
}
if len(L_valid_d3) > 6:
    results['spectral_rigidity']['slope_small_L'] = float(slope_small_d3)
    results['spectral_rigidity']['slope_large_L'] = float(slope_large_d3)

# ============================================================
# PART 3: Spectral Form Factor K(tau)
# ============================================================
print("\n" + "="*60)
print("PART 3: Spectral Form Factor K(tau)")
print("="*60)

# K(tau) = (1/N) * |sum_{n=1}^{N} exp(2*pi*i*tau*x_n)|^2
# Use connected version (subtract disconnected part)

tau_values = np.linspace(0.01, 3.0, 100)

def K_gue(tau):
    """GUE prediction for spectral form factor (connected part)."""
    if tau < 1:
        return tau
    else:
        return 1.0

def compute_K(tau_vals, x_unfolded, N_zeros):
    """Compute spectral form factor."""
    K_vals = np.zeros(len(tau_vals))
    for i, tau in enumerate(tau_vals):
        # Sum of exp(2*pi*i*tau*x_n)
        phases = 2 * np.pi * tau * x_unfolded
        sum_real = np.sum(np.cos(phases))
        sum_imag = np.sum(np.sin(phases))
        K_vals[i] = (sum_real**2 + sum_imag**2) / N_zeros
    return K_vals

t_start = time.time()

# For the connected form factor, we should subtract the disconnected part
# The disconnected part is |<exp(2*pi*i*tau*x)>|^2 * N
# But for the standard definition K(tau) = (1/N)|sum exp(2*pi*i*tau*x_n)|^2,
# the disconnected part is a delta at tau=0 which we avoid.
# The connected part for large N should approach the GUE prediction.

K_data = compute_K(tau_values, x, N)

elapsed_ff = time.time() - t_start
print(f"Form factor computed in {elapsed_ff:.1f}s")

K_gue_vals = np.array([K_gue(tau) for tau in tau_values])

# Smooth K_data (it's very noisy) — use running average
window_size = 5
K_smoothed = np.convolve(K_data, np.ones(window_size)/window_size, mode='same')

# Find transition region
# The ramp should be tau < 1 where K ~ tau
# The plateau should be tau > 1 where K ~ 1
ramp_mask = tau_values < 0.8
plateau_mask = tau_values > 1.2

if np.sum(ramp_mask) > 3:
    # Fit slope in ramp region
    ramp_fit = np.polyfit(tau_values[ramp_mask], K_smoothed[ramp_mask], 1)
    print(f"  Ramp region (tau < 0.8): slope = {ramp_fit[0]:.3f} (GUE predicts 1.0)")
    print(f"    intercept = {ramp_fit[1]:.3f}")

if np.sum(plateau_mask) > 3:
    plateau_mean = np.mean(K_smoothed[plateau_mask])
    plateau_std = np.std(K_smoothed[plateau_mask])
    print(f"  Plateau region (tau > 1.2): mean = {plateau_mean:.3f} ± {plateau_std:.3f} (GUE predicts 1.0)")

# Overall deviation
dev_K = np.abs(K_smoothed - K_gue_vals)
mean_dev_K = np.mean(dev_K)
max_dev_K = np.max(dev_K)
max_dev_tau = tau_values[np.argmax(dev_K)]
print(f"  Mean absolute deviation from GUE: {mean_dev_K:.4f}")
print(f"  Max absolute deviation: {max_dev_K:.4f} at tau={max_dev_tau:.2f}")

# Print table (subset)
print(f"\n  Spectral Form Factor Table (every 5th point):")
print(f"  {'tau':>8s} {'K_raw':>10s} {'K_smooth':>10s} {'K_GUE':>8s} {'AbsDev':>8s}")
for i in range(0, len(tau_values), 5):
    print(f"  {tau_values[i]:8.3f} {K_data[i]:10.4f} {K_smoothed[i]:10.4f} "
          f"{K_gue_vals[i]:8.4f} {dev_K[i]:8.4f}")

results['form_factor'] = {
    'tau_values': tau_values.tolist(),
    'K_data': K_data.tolist(),
    'K_smoothed': K_smoothed.tolist(),
    'K_gue': K_gue_vals.tolist(),
    'ramp_slope': float(ramp_fit[0]) if np.sum(ramp_mask) > 3 else None,
    'plateau_mean': float(plateau_mean) if np.sum(plateau_mask) > 3 else None,
    'plateau_std': float(plateau_std) if np.sum(plateau_mask) > 3 else None,
    'mean_dev': float(mean_dev_K),
    'max_dev': float(max_dev_K),
    'max_dev_tau': float(max_dev_tau),
}

# Save all results
with open('analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nAll results saved to analysis_results.json")
