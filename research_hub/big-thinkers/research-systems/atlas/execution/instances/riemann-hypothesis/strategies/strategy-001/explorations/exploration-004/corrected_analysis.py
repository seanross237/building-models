"""
Corrected analysis: account for the 1/2 offset (Gibbs phenomenon).

At zero t_n, N(t_n) = n but the prime sum converges to (n - 1/2) - N_smooth(t_n)
due to the Fourier midpoint property at step discontinuities.

So: N_osc_prime(t_n) → N_osc_exact(t_n) - 1/2

After correcting for this, the TRUE residual is:
   residual_corrected = N_osc_exact - N_osc_prime - 1/2
"""
import numpy as np
from scipy.optimize import brentq
from sympy import primerange
import json

############################################################
# Load data
############################################################

with open('zeta_zeros.json') as f:
    actual_zeros = np.array(json.load(f))

with open('smooth_zeros.json') as f:
    smooth_zeros = np.array(json.load(f))

N = len(actual_zeros)
smooth_zeros = smooth_zeros[:N]

def N_smooth(T):
    if T <= 0:
        return 0
    return (T / (2 * np.pi)) * np.log(T / (2 * np.pi * np.e)) + 7/8

def N_smooth_deriv(T):
    if T <= 0:
        return 0
    return (1 / (2 * np.pi)) * np.log(T / (2 * np.pi))

# Exact N_osc at actual zeros
N_osc_exact = np.array([i+1 - N_smooth(actual_zeros[i]) for i in range(N)])
derivs_at_actual = np.array([N_smooth_deriv(t) for t in actual_zeros])

print(f"Using {N} zeros")
print(f"N_osc exact: mean={np.mean(N_osc_exact):.4f}, std={np.std(N_osc_exact):.4f}")

all_primes_list = list(primerange(2, 10001))
M_max = 5

############################################################
# Convergence with 1/2 correction
############################################################

print("\n" + "="*60)
print("CONVERGENCE ANALYSIS (with 1/2 offset correction)")
print("="*60)

P_max_sweep = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

print(f"\n{'P_max':>8} {'#primes':>8} {'mean|res|':>12} {'std(res)':>12} {'max|res|':>12} {'mean pos err':>14}")

convergence_data = {}

for P_max in P_max_sweep:
    primes = [p for p in all_primes_list if p <= P_max]

    N_osc_prime = np.zeros(N)
    for p in primes:
        lp = np.log(float(p))
        for m in range(1, M_max + 1):
            coeff = 1.0 / (m * float(p)**(m/2.0))
            N_osc_prime += -(1.0/np.pi) * coeff * np.sin(m * actual_zeros * lp)

    # CORRECTED residual: subtract the 1/2 Gibbs offset
    residual = N_osc_exact - N_osc_prime - 0.5

    # Position error
    pos_error = residual / derivs_at_actual

    mean_abs_res = np.mean(np.abs(residual))
    std_res = np.std(residual)
    max_abs_res = np.max(np.abs(residual))
    mean_pos_err = np.mean(np.abs(pos_error))

    convergence_data[P_max] = {
        'mean_abs_res': mean_abs_res,
        'std_res': std_res,
        'max_abs_res': max_abs_res,
        'mean_pos_err': mean_pos_err,
    }

    print(f"{P_max:8d} {len(primes):8d} {mean_abs_res:12.6f} {std_res:12.6f} {max_abs_res:12.6f} {mean_pos_err:14.6f}")

# Fit power law
P_arr = np.array(P_max_sweep, dtype=float)
res_arr = np.array([convergence_data[p]['mean_abs_res'] for p in P_max_sweep])
log_P = np.log(P_arr)
log_r = np.log(res_arr)
alpha, intercept = np.polyfit(log_P, log_r, 1)
print(f"\nPower law fit: mean|residual| ~ P_max^({alpha:.4f})")
print(f"  At P_max=10000: mean|residual| = {convergence_data[10000]['mean_abs_res']:.6f}")

# Also fit std
std_arr = np.array([convergence_data[p]['std_res'] for p in P_max_sweep])
alpha_std, _ = np.polyfit(np.log(P_arr), np.log(std_arr), 1)
print(f"  Std convergence: ~ P_max^({alpha_std:.4f})")

############################################################
# Individual prime contributions
############################################################

print("\n" + "="*60)
print("INDIVIDUAL PRIME CONTRIBUTIONS")
print("="*60)

# How much does each prime contribute?
first_20_primes = list(primerange(2, 72))  # First 20 primes
print(f"\nContribution of individual primes (RMS of N_osc contribution across all zeros):")
print(f"{'prime':>8} {'RMS contrib':>12} {'max contrib':>12} {'1/(sqrt(p))':>14}")

for p in first_20_primes:
    lp = np.log(float(p))
    contrib = np.zeros(N)
    for m in range(1, M_max + 1):
        coeff = 1.0 / (m * float(p)**(m/2.0))
        contrib += -(1.0/np.pi) * coeff * np.sin(m * actual_zeros * lp)
    rms = np.sqrt(np.mean(contrib**2))
    mx = np.max(np.abs(contrib))
    expected = 1.0 / (np.pi * np.sqrt(float(p)))
    print(f"{p:8d} {rms:12.6f} {mx:12.6f} {expected:14.6f}")

############################################################
# Reconstruct zeros with 1/2 correction
############################################################

print("\n" + "="*60)
print("ZERO RECONSTRUCTION (with 1/2 correction)")
print("="*60)

# For the best P_max, compute corrected zeros using:
# At t_n^smooth, N_smooth = n - 0.5
# We need N_smooth(t) + N_osc_prime(t) + 0.5 = n
# i.e., N_smooth(t) + N_osc_prime(t) = n - 0.5
# which is the same as finding where the total function equals n - 0.5

# Let's evaluate the total function at the actual zeros as a sanity check
primes_10k = [p for p in all_primes_list if p <= 10000]
N_osc_at_smooth = np.zeros(N)
for p in primes_10k:
    lp = np.log(float(p))
    for m in range(1, M_max + 1):
        coeff = 1.0 / (m * float(p)**(m/2.0))
        N_osc_at_smooth += -(1.0/np.pi) * coeff * np.sin(m * smooth_zeros * lp)

# At the smooth zeros: N_total = N_smooth + N_osc_prime = (n-0.5) + N_osc_prime
# We need this to equal n - 0.5 for the smooth zero to be the actual zero
# So if N_osc_prime(t_smooth) = 0, smooth zero IS the corrected zero
# Otherwise, delta_n = -N_osc_prime(t_smooth) / N_smooth'(t_smooth)

# With the corrected formula (adding 0.5):
# N_smooth(t) + N_osc_prime(t) + 0.5 = n
# At smooth zero: (n-0.5) + N_osc_prime(t_smooth) + 0.5 = n
# => N_osc_prime(t_smooth) = 0 is the condition for exact match!
# => delta = -N_osc_prime(t_smooth) / N_smooth'(t_smooth)

delta_corrected = -N_osc_at_smooth / derivs_at_actual[:N]  # using smooth derivs
corrected_zeros = smooth_zeros + delta_corrected

# Now the actual residual in zero position
pos_residual = actual_zeros - corrected_zeros

print(f"\nP_max = 10000, linearized correction with 1/2 offset:")
print(f"  Mean |position residual|: {np.mean(np.abs(pos_residual)):.6f}")
print(f"  RMS position residual:    {np.sqrt(np.mean(pos_residual**2)):.6f}")
print(f"  Max |position residual|:  {np.max(np.abs(pos_residual)):.6f}")

print(f"\n{'n':>4} {'actual':>12} {'corrected':>12} {'residual':>10} {'smooth':>12}")
for i in range(20):
    print(f"{i+1:4d} {actual_zeros[i]:12.4f} {corrected_zeros[i]:12.4f} {pos_residual[i]:+10.4f} {smooth_zeros[i]:12.4f}")

# What fraction of the smooth→actual displacement is explained by primes?
displacement = actual_zeros - smooth_zeros
explained = corrected_zeros - smooth_zeros
fraction_explained = 1 - np.var(pos_residual) / np.var(displacement)
print(f"\nVariance explained by prime corrections: {fraction_explained*100:.1f}%")

# Do the same for each P_max
print(f"\n{'P_max':>8} {'mean|res|':>12} {'RMS res':>12} {'Var explained':>14}")
for P_max in P_max_sweep:
    primes = [p for p in all_primes_list if p <= P_max]
    N_osc_s = np.zeros(N)
    for p in primes:
        lp = np.log(float(p))
        for m in range(1, M_max + 1):
            coeff = 1.0 / (m * float(p)**(m/2.0))
            N_osc_s += -(1.0/np.pi) * coeff * np.sin(m * smooth_zeros * lp)

    derivs_s = np.array([N_smooth_deriv(t) for t in smooth_zeros])
    delta = -N_osc_s / derivs_s
    corrected = smooth_zeros + delta
    res = actual_zeros - corrected
    var_expl = 1 - np.var(res) / np.var(displacement)
    print(f"{P_max:8d} {np.mean(np.abs(res)):12.6f} {np.sqrt(np.mean(res**2)):12.6f} {var_expl*100:13.1f}%")

############################################################
# GUE statistics of corrected spectrum
############################################################

print("\n" + "="*60)
print("GUE STATISTICS OF CORRECTED SPECTRUM (P_max=10000)")
print("="*60)

def unfold(zeros):
    return np.array([N_smooth(t) for t in zeros])

def wigner_surmise(s):
    return (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)

def poisson_spacing(s):
    return np.exp(-s)

# Unfold each spectrum
unfolded_actual = unfold(actual_zeros)
unfolded_smooth = unfold(smooth_zeros)
unfolded_corrected = unfold(corrected_zeros)

spacings_actual = np.diff(unfolded_actual)
spacings_smooth = np.diff(unfolded_smooth)
spacings_corrected = np.diff(unfolded_corrected)

s_bins = np.linspace(0, 4, 81)
s_centers = 0.5 * (s_bins[:-1] + s_bins[1:])
wigner = wigner_surmise(s_centers)
poisson = poisson_spacing(s_centers)

for label, spacings in [("Actual", spacings_actual), ("Smooth", spacings_smooth), ("Corrected", spacings_corrected)]:
    hist, _ = np.histogram(spacings, bins=s_bins, density=True)
    mse_w = np.mean((hist - wigner)**2)
    mse_p = np.mean((hist - poisson)**2)

    # Level repulsion
    valid = (s_centers > 0.05) & (s_centers < 0.5) & (hist > 0)
    if np.sum(valid) > 2:
        beta_fit = np.polyfit(np.log(s_centers[valid]), np.log(hist[valid]), 1)
        beta = beta_fit[0]
    else:
        beta = float('nan')

    print(f"\n{label}:")
    print(f"  Mean spacing: {np.mean(spacings):.4f}")
    print(f"  Std spacing:  {np.std(spacings):.4f}")
    print(f"  MSE vs GUE:     {mse_w:.6f}")
    print(f"  MSE vs Poisson: {mse_p:.6f}")
    print(f"  Level repulsion β: {beta:.3f} (GUE: 2)")

# Number variance comparison
def number_variance(unfolded, L_values):
    N = len(unfolded)
    sigma2 = []
    for L in L_values:
        variances = []
        n_samples = min(500, N)
        for i in range(0, N, max(1, N//n_samples)):
            center = unfolded[i]
            lo, hi = center - L/2, center + L/2
            count = np.sum((unfolded >= lo) & (unfolded < hi))
            variances.append((count - L)**2)
        sigma2.append(np.mean(variances))
    return np.array(sigma2)

def gue_number_variance(L):
    gamma = 0.5772156649
    return (2/np.pi**2) * (np.log(2*np.pi*L) + gamma + 1 - np.pi**2/8)

L_values = np.array([0.5, 1, 2, 3, 5, 8, 10, 15, 20])
gue_nv = gue_number_variance(L_values)

print(f"\nNumber Variance Σ²(L):")
print(f"{'L':>6} {'actual':>10} {'smooth':>10} {'corrected':>10} {'GUE':>10}")
for label, unf in [("actual", unfolded_actual), ("smooth", unfolded_smooth), ("corrected", unfolded_corrected)]:
    nv = number_variance(unf, L_values)
    if label == "actual":
        nv_actual = nv
    elif label == "smooth":
        nv_smooth = nv
    else:
        nv_corrected = nv

for i, L in enumerate(L_values):
    print(f"{L:6.1f} {nv_actual[i]:10.4f} {nv_smooth[i]:10.4f} {nv_corrected[i]:10.4f} {gue_nv[i]:10.4f}")

# Summary score: MSE of number variance vs GUE
mse_nv_actual = np.mean((nv_actual - gue_nv)**2)
mse_nv_smooth = np.mean((nv_smooth - gue_nv)**2)
mse_nv_corrected = np.mean((nv_corrected - gue_nv)**2)
print(f"\nNumber variance MSE vs GUE:")
print(f"  Actual:    {mse_nv_actual:.6f}")
print(f"  Smooth:    {mse_nv_smooth:.6f}")
print(f"  Corrected: {mse_nv_corrected:.6f}")
print(f"  Improvement: {(1 - mse_nv_corrected/mse_nv_smooth)*100:.1f}% reduction from smooth")

############################################################
# Save all summary results
############################################################

summary = {
    'N': N,
    'formula_correction': 'Removed ln(p) factor; added 1/2 Gibbs offset',
    'convergence': {str(k): v for k, v in convergence_data.items()},
    'power_law_alpha': float(alpha),
    'std_convergence_alpha': float(alpha_std),
    'var_explained_P10000': float(fraction_explained),
    'spacing_MSE': {
        'actual_vs_GUE': float(np.mean((np.histogram(spacings_actual, bins=s_bins, density=True)[0] - wigner)**2)),
        'corrected_vs_GUE': float(np.mean((np.histogram(spacings_corrected, bins=s_bins, density=True)[0] - wigner)**2)),
        'smooth_vs_GUE': float(np.mean((np.histogram(spacings_smooth, bins=s_bins, density=True)[0] - wigner)**2)),
    },
    'number_variance_MSE_vs_GUE': {
        'actual': float(mse_nv_actual),
        'smooth': float(mse_nv_smooth),
        'corrected': float(mse_nv_corrected),
    }
}

with open('summary_results.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\n\nALL ANALYSIS COMPLETE")
