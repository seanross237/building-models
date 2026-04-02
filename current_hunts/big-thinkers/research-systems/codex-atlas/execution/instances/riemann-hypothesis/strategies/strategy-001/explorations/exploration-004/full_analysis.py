"""
Full analysis: compare actual zeros, smooth zeros, and prime-corrected zeros.
Focus on STATISTICAL properties rather than individual zero reconstruction.
"""
import numpy as np
from scipy.optimize import brentq, curve_fit
from scipy.integrate import quad
from sympy import primerange
import json
import time
import os

############################################################
# Load data
############################################################

# Use whatever zeros are available
if os.path.exists('zeta_zeros.json'):
    with open('zeta_zeros.json') as f:
        actual_zeros = np.array(json.load(f))
    print(f"Loaded {len(actual_zeros)} actual zeros (full set)")
else:
    with open('zeta_zeros_partial.json') as f:
        actual_zeros = np.array(json.load(f))
    print(f"Loaded {len(actual_zeros)} actual zeros (partial set)")

with open('smooth_zeros.json') as f:
    smooth_zeros_all = np.array(json.load(f))

N = len(actual_zeros)
smooth_zeros = smooth_zeros_all[:N]

print(f"Using {N} zeros for analysis")
print(f"Actual range: [{actual_zeros[0]:.4f}, {actual_zeros[-1]:.4f}]")
print(f"Smooth range: [{smooth_zeros[0]:.4f}, {smooth_zeros[-1]:.4f}]")

############################################################
# Helper functions
############################################################

def N_smooth(T):
    if T <= 0:
        return 0
    return (T / (2 * np.pi)) * np.log(T / (2 * np.pi * np.e)) + 7/8

def N_smooth_deriv(T):
    if T <= 0:
        return 0
    return (1 / (2 * np.pi)) * np.log(T / (2 * np.pi))

def unfold(zeros):
    """Unfold a spectrum to unit mean spacing using N_smooth"""
    return np.array([N_smooth(t) for t in zeros])

def nn_spacings(unfolded):
    """Compute nearest-neighbor spacings"""
    return np.diff(unfolded)

def pair_correlation(unfolded, L_max=5.0, n_bins=100):
    """Compute pair correlation function R2(r)"""
    N = len(unfolded)
    diffs = []
    for i in range(N):
        for j in range(i+1, min(i+50, N)):  # Only nearby pairs
            d = abs(unfolded[j] - unfolded[i])
            if d < L_max:
                diffs.append(d)

    hist, edges = np.histogram(diffs, bins=n_bins, range=(0, L_max))
    r = 0.5 * (edges[:-1] + edges[1:])
    dr = edges[1] - edges[0]
    # Normalize: R2(r) * dr * N ≈ count
    R2 = hist / (N * dr)
    return r, R2

def gue_pair_correlation(r):
    """GUE pair correlation: 1 - (sin(pi*r)/(pi*r))^2"""
    with np.errstate(divide='ignore', invalid='ignore'):
        sinc = np.where(r == 0, 1.0, np.sin(np.pi * r) / (np.pi * r))
    return 1 - sinc**2

def wigner_surmise(s):
    """GUE Wigner surmise: P(s) = (32/pi^2) * s^2 * exp(-4s^2/pi)"""
    return (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)

def poisson_spacing(s):
    """Poisson: P(s) = exp(-s)"""
    return np.exp(-s)

def number_variance(unfolded, L_values):
    """Compute number variance Sigma^2(L)"""
    N = len(unfolded)
    sigma2 = []
    for L in L_values:
        variances = []
        # Sample random intervals of length L
        n_samples = min(500, N)
        for i in range(0, N, max(1, N//n_samples)):
            center = unfolded[i]
            lo, hi = center - L/2, center + L/2
            count = np.sum((unfolded >= lo) & (unfolded < hi))
            variances.append((count - L)**2)
        sigma2.append(np.mean(variances))
    return np.array(sigma2)

def gue_number_variance(L):
    """GUE number variance (asymptotic): (2/pi^2) * (ln(2*pi*L) + gamma + 1 - pi^2/8)"""
    gamma = 0.5772156649
    return (2/np.pi**2) * (np.log(2*np.pi*L) + gamma + 1 - np.pi**2/8)

def spectral_rigidity(unfolded, L_values):
    """Compute spectral rigidity Delta_3(L)"""
    N = len(unfolded)
    delta3 = []
    for L in L_values:
        vals = []
        n_samples = min(300, N)
        for i in range(0, N, max(1, N//n_samples)):
            center = unfolded[i]
            lo, hi = center - L/2, center + L/2
            mask = (unfolded >= lo) & (unfolded < hi)
            pts = unfolded[mask] - lo  # shift to [0, L]
            n_pts = len(pts)
            if n_pts < 2:
                continue
            # Fit a line and compute residual
            # Delta_3 = min_{a,b} (1/L) * integral of (N(x) - ax - b)^2
            # N(x) = number of pts <= x
            # Use least squares on the staircase
            x = np.sort(pts)
            stair = np.arange(1, n_pts + 1)
            # Fit line to staircase
            if len(x) > 1:
                coeffs = np.polyfit(x, stair, 1)
                fitted = np.polyval(coeffs, x)
                residual = np.mean((stair - fitted)**2) / L
                vals.append(residual)
        if vals:
            delta3.append(np.mean(vals))
        else:
            delta3.append(0)
    return np.array(delta3)

def gue_delta3(L):
    """GUE spectral rigidity (asymptotic): (1/pi^2) * (ln(2*pi*L) + gamma - 5/4 - pi^2/8)"""
    gamma = 0.5772156649
    return (1/np.pi**2) * (np.log(2*np.pi*L) + gamma - 5.0/4 - np.pi**2/8)

############################################################
# Part 1: Basic comparison - actual vs smooth
############################################################

print("\n" + "="*60)
print("PART 1: ACTUAL vs SMOOTH ZEROS")
print("="*60)

deltas = actual_zeros - smooth_zeros
print(f"\nDisplacement (actual - smooth):")
print(f"  Mean: {np.mean(deltas):.6f}")
print(f"  Std:  {np.std(deltas):.6f}")
print(f"  Min:  {np.min(deltas):.6f}")
print(f"  Max:  {np.max(deltas):.6f}")
print(f"  Mean |delta|: {np.mean(np.abs(deltas)):.6f}")

# First 20
print(f"\nFirst 20 zeros comparison:")
print(f"{'n':>4} {'actual':>12} {'smooth':>12} {'delta':>10}")
for i in range(min(20, N)):
    print(f"{i+1:4d} {actual_zeros[i]:12.4f} {smooth_zeros[i]:12.4f} {deltas[i]:+10.4f}")

############################################################
# Part 2: Unfold and compute statistics for actual zeros
############################################################

print("\n" + "="*60)
print("PART 2: GUE STATISTICS OF ACTUAL ZEROS")
print("="*60)

unfolded_actual = unfold(actual_zeros)
spacings_actual = nn_spacings(unfolded_actual)

print(f"\nUnfolded spacings:")
print(f"  Mean: {np.mean(spacings_actual):.6f} (should be ~1)")
print(f"  Std:  {np.std(spacings_actual):.6f}")
print(f"  Min:  {np.min(spacings_actual):.6f}")
print(f"  Max:  {np.max(spacings_actual):.6f}")

# NN spacing distribution
s_bins = np.linspace(0, 4, 81)
s_centers = 0.5 * (s_bins[:-1] + s_bins[1:])
ds = s_bins[1] - s_bins[0]
hist_actual, _ = np.histogram(spacings_actual, bins=s_bins, density=True)

# Compare to Wigner surmise
wigner = wigner_surmise(s_centers)
mse_wigner = np.mean((hist_actual - wigner)**2)
mse_poisson = np.mean((hist_actual - poisson_spacing(s_centers))**2)

print(f"\nNN spacing comparison:")
print(f"  MSE vs GUE Wigner surmise: {mse_wigner:.6f}")
print(f"  MSE vs Poisson:            {mse_poisson:.6f}")
print(f"  Ratio (Poisson/GUE MSE):   {mse_poisson/mse_wigner:.1f}x worse for Poisson")

# Level repulsion: fit P(s) ~ s^beta for small s
small_s_mask = s_centers < 0.5
if np.any(hist_actual[small_s_mask] > 0):
    valid = (s_centers > 0.05) & (s_centers < 0.5) & (hist_actual > 0)
    if np.sum(valid) > 2:
        log_s = np.log(s_centers[valid])
        log_P = np.log(hist_actual[valid])
        beta_fit = np.polyfit(log_s, log_P, 1)
        beta = beta_fit[0]
        print(f"\nLevel repulsion: P(s) ~ s^β")
        print(f"  Fitted β = {beta:.3f} (GUE: β=2, GOE: β=1, Poisson: β=0)")

# Pair correlation
print("\nPair correlation R2(r):")
r, R2 = pair_correlation(unfolded_actual)
gue_R2 = gue_pair_correlation(r)
# Compare in the range [0.1, 3]
mask = (r > 0.1) & (r < 3.0)
mse_R2 = np.mean((R2[mask] - gue_R2[mask])**2)
print(f"  MSE vs GUE (r in [0.1, 3]): {mse_R2:.6f}")

# Number variance
L_values = np.array([0.5, 1, 2, 3, 5, 8, 10, 15, 20])
sigma2 = number_variance(unfolded_actual, L_values)
gue_sig2 = gue_number_variance(L_values)
print(f"\nNumber variance Σ²(L):")
print(f"{'L':>6} {'actual':>10} {'GUE':>10} {'ratio':>8}")
for i, L in enumerate(L_values):
    r = sigma2[i] / gue_sig2[i] if gue_sig2[i] > 0 else float('inf')
    print(f"{L:6.1f} {sigma2[i]:10.4f} {gue_sig2[i]:10.4f} {r:8.3f}")

# Spectral rigidity
delta3 = spectral_rigidity(unfolded_actual, L_values)
gue_d3 = gue_delta3(L_values)
print(f"\nSpectral rigidity Δ₃(L):")
print(f"{'L':>6} {'actual':>10} {'GUE':>10} {'ratio':>8}")
for i, L in enumerate(L_values):
    r = delta3[i] / gue_d3[i] if gue_d3[i] > 0 else float('inf')
    print(f"{L:6.1f} {delta3[i]:10.4f} {gue_d3[i]:10.4f} {r:8.3f}")

############################################################
# Part 3: Statistics of SMOOTH spectrum
############################################################

print("\n" + "="*60)
print("PART 3: GUE STATISTICS OF SMOOTH SPECTRUM")
print("="*60)

unfolded_smooth = unfold(smooth_zeros)
spacings_smooth = nn_spacings(unfolded_smooth)

print(f"\nUnfolded spacings (smooth):")
print(f"  Mean: {np.mean(spacings_smooth):.6f}")
print(f"  Std:  {np.std(spacings_smooth):.6f}")

hist_smooth, _ = np.histogram(spacings_smooth, bins=s_bins, density=True)
mse_wigner_smooth = np.mean((hist_smooth - wigner)**2)
mse_poisson_smooth = np.mean((hist_smooth - poisson_spacing(s_centers))**2)

print(f"\nSmooth NN spacing comparison:")
print(f"  MSE vs GUE: {mse_wigner_smooth:.6f}")
print(f"  MSE vs Poisson: {mse_poisson_smooth:.6f}")

# Number variance for smooth
sigma2_smooth = number_variance(unfolded_smooth, L_values)
print(f"\nSmooth Number variance Σ²(L):")
print(f"{'L':>6} {'smooth':>10} {'GUE':>10} {'Poisson':>10}")
for i, L in enumerate(L_values):
    print(f"{L:6.1f} {sigma2_smooth[i]:10.4f} {gue_sig2[i]:10.4f} {L:10.4f}")

############################################################
# Part 4: N_osc quality and prime contribution analysis
############################################################

print("\n" + "="*60)
print("PART 4: PRIME SUM QUALITY")
print("="*60)

# Compute N_osc_exact = N(t) - N_smooth(t) at actual zero positions
# At the nth actual zero, N(t_n) = n, so N_osc(t_n) = n - N_smooth(t_n)
N_osc_exact = np.array([i+1 - N_smooth(actual_zeros[i]) for i in range(N)])

print(f"\nExact N_osc at actual zeros:")
print(f"  Mean: {np.mean(N_osc_exact):.6f}")
print(f"  Std:  {np.std(N_osc_exact):.6f}")
print(f"  Range: [{np.min(N_osc_exact):.4f}, {np.max(N_osc_exact):.4f}]")

# Compute prime sum N_osc at actual zero positions for each P_max
all_primes_list = list(primerange(2, 10001))
M_max = 5

for P_max in [100, 1000, 10000]:
    primes = [p for p in all_primes_list if p <= P_max]

    N_osc_prime = np.zeros(N)
    for p in primes:
        lp = np.log(float(p))
        for m in range(1, M_max + 1):
            coeff = 1.0 / (m * float(p)**(m/2.0))
            N_osc_prime += -(1.0/np.pi) * coeff * np.sin(m * actual_zeros * lp)

    residual = N_osc_exact - N_osc_prime
    print(f"\nP_max = {P_max} ({len(primes)} primes):")
    print(f"  N_osc residual (exact - prime sum):")
    print(f"    Mean: {np.mean(residual):.6f}")
    print(f"    Std:  {np.std(residual):.6f}")
    print(f"    Mean |residual|: {np.mean(np.abs(residual)):.6f}")
    print(f"    Max |residual|: {np.max(np.abs(residual)):.6f}")

    # Convert residual to position error via N_smooth'
    derivs_at_actual = np.array([N_smooth_deriv(t) for t in actual_zeros])
    pos_error = residual / derivs_at_actual
    print(f"  Implied position error:")
    print(f"    Mean |error|: {np.mean(np.abs(pos_error)):.6f}")
    print(f"    Max |error|: {np.max(np.abs(pos_error)):.6f}")
    print(f"    RMS error: {np.sqrt(np.mean(pos_error**2)):.6f}")

############################################################
# Part 5: Convergence analysis - finer P_max sweep
############################################################

print("\n" + "="*60)
print("PART 5: CONVERGENCE ANALYSIS")
print("="*60)

P_max_sweep = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
mean_residuals = []
std_residuals = []
max_residuals = []

for P_max in P_max_sweep:
    primes = [p for p in all_primes_list if p <= P_max]

    N_osc_prime = np.zeros(N)
    for p in primes:
        lp = np.log(float(p))
        for m in range(1, M_max + 1):
            coeff = 1.0 / (m * float(p)**(m/2.0))
            N_osc_prime += -(1.0/np.pi) * coeff * np.sin(m * actual_zeros * lp)

    residual = N_osc_exact - N_osc_prime
    mean_residuals.append(np.mean(np.abs(residual)))
    std_residuals.append(np.std(residual))
    max_residuals.append(np.max(np.abs(residual)))

print(f"\n{'P_max':>8} {'# primes':>8} {'mean|res|':>12} {'std(res)':>12} {'max|res|':>12}")
for i, P_max in enumerate(P_max_sweep):
    n_primes = len([p for p in all_primes_list if p <= P_max])
    print(f"{P_max:8d} {n_primes:8d} {mean_residuals[i]:12.6f} {std_residuals[i]:12.6f} {max_residuals[i]:12.6f}")

# Fit power law: mean|residual| ~ P_max^alpha
valid = np.array(mean_residuals) > 0
log_P = np.log(np.array(P_max_sweep)[valid])
log_r = np.log(np.array(mean_residuals)[valid])
if len(log_P) > 2:
    alpha, intercept = np.polyfit(log_P, log_r, 1)
    print(f"\nPower law fit: mean|residual| ~ P_max^({alpha:.4f})")
    print(f"  (Expected: ~P_max^(-1/2) for Gibbs-like convergence)")

############################################################
# Part 6: Is the residual systematic or random?
############################################################

print("\n" + "="*60)
print("PART 6: RESIDUAL STRUCTURE ANALYSIS")
print("="*60)

# Compute residual for P_max = 10000 in detail
primes = [p for p in all_primes_list if p <= 10000]
N_osc_prime_best = np.zeros(N)
for p in primes:
    lp = np.log(float(p))
    for m in range(1, M_max + 1):
        coeff = 1.0 / (m * float(p)**(m/2.0))
        N_osc_prime_best += -(1.0/np.pi) * coeff * np.sin(m * actual_zeros * lp)

residual_best = N_osc_exact - N_osc_prime_best

# Autocorrelation of residual
from numpy.fft import fft, ifft
res_centered = residual_best - np.mean(residual_best)
acf = np.real(ifft(np.abs(fft(res_centered))**2)) / np.sum(res_centered**2)
print(f"\nResidual autocorrelation (P_max=10000):")
print(f"  lag 1: {acf[1]:.4f}")
print(f"  lag 2: {acf[2]:.4f}")
print(f"  lag 5: {acf[5]:.4f}")
print(f"  lag 10: {acf[10]:.4f}")
print(f"  (Random noise: ~±{1/np.sqrt(N):.4f})")

# Is the residual correlated with zero height (T)?
corr_T = np.corrcoef(actual_zeros, residual_best)[0,1]
print(f"\nCorrelation of residual with T: {corr_T:.4f}")

# Is the residual correlated with spacing?
actual_spacings = np.diff(actual_zeros)
corr_spacing = np.corrcoef(actual_spacings, residual_best[1:])[0,1]
print(f"Correlation of residual with local spacing: {corr_spacing:.4f}")

# Distribution of residual
print(f"\nResidual distribution (P_max=10000):")
print(f"  Skewness: {float(np.mean(((residual_best - np.mean(residual_best))/np.std(residual_best))**3)):.4f}")
print(f"  Kurtosis: {float(np.mean(((residual_best - np.mean(residual_best))/np.std(residual_best))**4)):.4f} (Gaussian: 3)")

# Save detailed results for report
results = {
    'N': N,
    'actual_zeros_first20': actual_zeros[:20].tolist(),
    'smooth_zeros_first20': smooth_zeros[:20].tolist(),
    'deltas_first20': deltas[:20].tolist(),
    'spacings_actual_stats': {
        'mean': float(np.mean(spacings_actual)),
        'std': float(np.std(spacings_actual)),
        'min': float(np.min(spacings_actual)),
        'max': float(np.max(spacings_actual)),
    },
    'mse_wigner': float(mse_wigner),
    'mse_poisson': float(mse_poisson),
    'mse_wigner_smooth': float(mse_wigner_smooth),
    'mse_poisson_smooth': float(mse_poisson_smooth),
    'convergence': {
        'P_max': P_max_sweep,
        'mean_residual': mean_residuals,
    },
    'power_law_alpha': float(alpha) if 'alpha' in dir() else None,
}

with open('analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n\nSaved analysis results to analysis_results.json")
print("ANALYSIS COMPLETE")
