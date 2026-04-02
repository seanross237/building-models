"""
Deeper analysis:
1. Is the problem the linearization or the prime sum itself?
2. What if we use the EXACT N_osc (direct mpmath) for correction?
3. Spectral form factor analysis
"""
import numpy as np
from scipy.optimize import brentq
import json
import mpmath

mpmath.mp.dps = 20

with open('zeta_zeros.json') as f:
    actual_zeros = np.array(json.load(f))
with open('smooth_zeros.json') as f:
    smooth_zeros = np.array(json.load(f))

N = len(actual_zeros)

def N_smooth(T):
    if T <= 0:
        return 0
    return (T / (2 * np.pi)) * np.log(T / (2 * np.pi * np.e)) + 7/8

def N_smooth_deriv(T):
    if T <= 0:
        return 0
    return (1 / (2 * np.pi)) * np.log(T / (2 * np.pi))

############################################################
# Test: exact N_osc at smooth zeros (via mpmath arg(zeta))
############################################################

print("=== EXACT N_osc at smooth zeros (first 30) ===\n")
print(f"{'n':>4} {'t_smooth':>12} {'N_osc_exact':>12} {'delta_lin':>12} {'actual':>12} {'error':>10}")

exact_N_osc = []
for i in range(30):
    T = smooth_zeros[i]
    s = mpmath.mpc(0.5, T)
    z = mpmath.zeta(s)
    arg_z = float(mpmath.arg(z))
    # N_osc = (1/pi) * Im(ln(zeta(1/2+iT)))
    N_osc = (1.0/np.pi) * arg_z
    exact_N_osc.append(N_osc)

    # Linearized correction
    deriv = N_smooth_deriv(T)
    delta = -N_osc / deriv
    corrected = T + delta

    error = actual_zeros[i] - corrected
    print(f"{i+1:4d} {T:12.4f} {N_osc:+12.6f} {delta:+12.6f} {actual_zeros[i]:12.4f} {error:+10.4f}")

############################################################
# Compare smooth, corrected (exact N_osc), corrected (prime sum)
############################################################

print("\n\n=== Displacement statistics ===\n")

# Displacement from smooth to actual
disp = actual_zeros[:30] - smooth_zeros[:30]
print(f"Smooth → Actual displacement:")
print(f"  Mean |δ|: {np.mean(np.abs(disp)):.4f}")
print(f"  RMS:      {np.sqrt(np.mean(disp**2)):.4f}")

# Exact correction (using exact N_osc from mpmath)
exact_corrections = []
for i in range(30):
    T = smooth_zeros[i]
    N_osc = exact_N_osc[i]
    deriv = N_smooth_deriv(T)
    delta = -N_osc / deriv
    exact_corrections.append(smooth_zeros[i] + delta)

exact_res = actual_zeros[:30] - np.array(exact_corrections)
print(f"\nExact N_osc linearized correction:")
print(f"  Mean |residual|: {np.mean(np.abs(exact_res)):.4f}")
print(f"  RMS residual:    {np.sqrt(np.mean(exact_res**2)):.4f}")
print(f"  Max |residual|:  {np.max(np.abs(exact_res)):.4f}")

# R² of exact correction
var_explained_exact = 1 - np.var(exact_res) / np.var(disp)
print(f"  Variance explained: {var_explained_exact*100:.1f}%")

############################################################
# Iterative correction (Newton-like) using exact N_osc
############################################################

print("\n\n=== ITERATIVE CORRECTION (exact N_osc, up to 5 iterations) ===\n")

for i in range(20):
    T = smooth_zeros[i]
    for iteration in range(5):
        s = mpmath.mpc(0.5, T)
        z = mpmath.zeta(s)
        arg_z = float(mpmath.arg(z))
        N_osc_here = (1.0/np.pi) * arg_z
        # N(T) = N_smooth(T) + N_osc(T). We want N(T) = i+1 (nth zero)
        # Actually, between zeros N is constant. At the nth zero it jumps.
        # The function S(T) = (1/pi)*arg(zeta(1/2+iT)) is what we add to N_smooth.
        # Newton step: T_{k+1} = T_k - (N_smooth(T_k) + S(T_k) - target) / (N_smooth'(T_k) + S'(T_k))
        # Approximate S' ≈ 0 (slowly varying), target = i + 0.5
        target = i + 0.5  # halfway
        f_val = N_smooth(T) + N_osc_here - target
        deriv = N_smooth_deriv(T)
        T = T - f_val / deriv

    error = actual_zeros[i] - T
    print(f"n={i+1:3d}: iterated={T:.6f}, actual={actual_zeros[i]:.6f}, error={error:+.6f}")

############################################################
# What fraction of pairs does the sign of N_osc predict correctly?
############################################################

print("\n\n=== SIGN PREDICTION: does N_osc predict direction of displacement? ===\n")

correct_signs = 0
for i in range(min(100, N)):
    T = smooth_zeros[i]
    s = mpmath.mpc(0.5, T)
    z = mpmath.zeta(s)
    N_osc = (1.0/np.pi) * float(mpmath.arg(z))

    actual_disp = actual_zeros[i] - smooth_zeros[i]
    predicted_direction = -N_osc  # correction is -N_osc/deriv, which has sign of -N_osc

    if actual_disp * predicted_direction > 0:
        correct_signs += 1

print(f"Sign prediction accuracy (first 100 zeros): {correct_signs}/100 = {correct_signs}%")

############################################################
# Spectral Form Factor
############################################################

print("\n\n=== SPECTRAL FORM FACTOR ===\n")

def unfold(zeros):
    return np.array([N_smooth(t) for t in zeros])

unfolded = unfold(actual_zeros)

# K(tau) = |sum_n exp(2*pi*i*tau*x_n)|^2 / N
# where x_n are unfolded eigenvalues and tau is in units of 1/mean_spacing

tau_values = np.linspace(0.01, 2.0, 200)
K_actual = np.zeros(len(tau_values))

for j, tau in enumerate(tau_values):
    phase_sum = np.sum(np.exp(2j * np.pi * tau * unfolded))
    K_actual[j] = np.abs(phase_sum)**2 / N

# GUE prediction: K(tau) = 2*tau for tau < 1, K(tau) = 2 - tau^{-1}...
# Actually for beta=2 (GUE): K(tau) = min(tau, 1) (the connected part)
# Full: K(tau) = 2*tau for tau < 1, 2 for tau >= 1
# Wait, the standard result is K(tau) = tau for tau < 1, 1 for tau > 1 (connected part)
# Actually for GUE: K_connected(tau) = 2tau - tau*ln(1+2tau) ... no
# Simple: for GUE, K(tau) = tau for 0 < tau < 1, and 1 for tau > 1

# Let me use the standard result:
# K_GUE(tau) = 2*tau - tau*log(1 + 2*tau) for small tau...
# Actually the simplest: K(tau) = min(2*tau, 2) for the 2-point form factor
# No... let me be precise.
# For GUE: b_2(r) = 1 - (sin(pi*r)/(pi*r))^2, and K(tau) = FT of b_2
# K_GUE(tau) = min(|tau|, 1) for the connected part (for beta=2)

K_gue = np.minimum(tau_values, 1.0)

# Print some values
print(f"{'tau':>8} {'K(actual)':>12} {'K(GUE)':>8}")
for tau_show in [0.1, 0.2, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0]:
    idx = np.argmin(np.abs(tau_values - tau_show))
    print(f"{tau_values[idx]:8.2f} {K_actual[idx]:12.4f} {K_gue[idx]:8.4f}")

# MSE of form factor
mask = tau_values < 2.0
mse_ff = np.mean((K_actual[mask] - K_gue[mask])**2)
print(f"\nMSE of form factor vs GUE: {mse_ff:.6f}")

print("\n\nDEEP ANALYSIS COMPLETE")
