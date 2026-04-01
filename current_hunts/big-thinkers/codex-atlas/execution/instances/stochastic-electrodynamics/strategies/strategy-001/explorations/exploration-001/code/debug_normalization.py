"""
Debug the spectral density normalization for the SED harmonic oscillator.

The key question: what is the correct one-sided PSD of the ZPF force
such that the equilibrium position variance equals hbar/(2*m*omega0)?

We derive:
  S_F^{one}(omega) = 2*tau*hbar*omega^3/m  (the CORRECT formula)
  NOT (2*tau*hbar/(pi*m))*omega^3 (what the original code had — off by factor pi)

And the FFT amplitude (numpy rfft convention):
  |F_k|^2 = N * S_F^{one}(omega_k) / (2*dt)

And the expected position variance:
  var_x = (2/N^2) * SUM_{k=1}^{K-1} |F_k|^2 / |H_k|^2

This script verifies all of this numerically.
"""

import numpy as np
from scipy import integrate

def compute_integral(omega0, tau, use_full_AL=True):
    """Compute I = integral_0^inf omega^3 / |H(omega)|^2 domega"""
    Gamma = tau * omega0**2
    def integrand(omega):
        if use_full_AL:
            H_sq = (omega0**2 - omega**2)**2 + (tau * omega**3)**2
        else:
            H_sq = (omega0**2 - omega**2)**2 + (Gamma * omega)**2
        if H_sq == 0:
            return 0
        return omega**3 / H_sq
    val, _ = integrate.quad(integrand, 1e-8, 500, limit=1000)
    return val

# Test for several tau values
print("Testing integral I = int omega^3/|H|^2 domega")
print("Expected: I ≈ pi/(2*tau) for small tau (near resonance approx)")
print()

for tau in [0.1, 0.01, 0.001, 0.0001]:
    I_AL = compute_integral(1.0, tau, True)
    I_eff = compute_integral(1.0, tau, False)
    print(f"tau={tau}:")
    print(f"  I (full A-L):   {I_AL:.4f},  pi/(2*tau) = {np.pi/(2*tau):.4f},  ratio = {I_AL/(np.pi/(2*tau)):.6f}")
    print(f"  I (eff damp):   {I_eff:.4f},  pi/(2*tau) = {np.pi/(2*tau):.4f},  ratio = {I_eff/(np.pi/(2*tau)):.6f}")
    # Expected var_x with correct normalization: tau*I/pi
    var_correct_AL = tau * I_AL / np.pi
    var_correct_eff = tau * I_eff / np.pi
    print(f"  var_x (A-L) = tau*I/pi = {var_correct_AL:.6f}  (target 0.5)")
    print(f"  var_x (eff) = tau*I/pi = {var_correct_eff:.6f}  (target 0.5)")
    print()

# Now verify with FFT simulation
print("="*60)
print("FFT verification: does the noise generate the right variance?")
print("="*60)

omega0 = 1.0
tau = 0.01
m = 1.0
hbar = 1.0
Gamma = tau * omega0**2
N_modes = 2**16
dt = 0.05
N_ensemble = 2000
seed = 42

rng = np.random.default_rng(seed)

freqs = np.fft.rfftfreq(N_modes, d=dt)
omega = 2 * np.pi * freqs
N_freq = len(omega)

# Transfer function (full A-L)
H = omega0**2 - omega**2 + 1j * tau * omega**3
H[0] = 1.0

# CORRECT one-sided PSD: S_one = 2*tau*hbar*omega^3/m
S_one = np.zeros(N_freq)
S_one[1:] = (2 * tau * hbar / m) * omega[1:]**3

# CORRECT FFT amplitude: |F_k|^2 = N * S_one / (2*dt)
F_amp_correct = np.sqrt(N_modes * S_one / (2 * dt))

# WRONG FFT amplitude (what the code had): |F_k|^2 = pi * N * S_wrong / dt
S_wrong = np.zeros(N_freq)
S_wrong[1:] = (2 * tau * hbar / (np.pi * m)) * omega[1:]**3
F_amp_wrong = np.sqrt(np.pi * N_modes * S_wrong / dt)

print(f"\nF_amp_correct^2 / F_amp_wrong^2 = {F_amp_correct[100]**2 / F_amp_wrong[100]**2:.6f}")
print(f"(should be 0.5 — the wrong version had 2x too much power)")

# Spectral sum for expected variance
K = N_modes // 2
var_x_correct = (2.0 / N_modes**2) * np.sum(F_amp_correct[1:K]**2 / np.abs(H[1:K])**2)
var_x_wrong = (2.0 / N_modes**2) * np.sum(F_amp_wrong[1:K]**2 / np.abs(H[1:K])**2)

print(f"\nSpectral sum var_x (correct): {var_x_correct:.6f}  (target 0.5)")
print(f"Spectral sum var_x (wrong):   {var_x_wrong:.6f}  (would be ~1.0)")

# Monte Carlo verification
x_correct = np.zeros(N_ensemble)
x_wrong = np.zeros(N_ensemble)

for i in range(N_ensemble):
    phases = rng.uniform(0, 2*np.pi, size=N_freq)

    # Correct noise
    F_k = F_amp_correct * np.exp(1j * phases)
    F_k[0] = 0
    X_k = F_k / H
    x_t = np.fft.irfft(X_k, n=N_modes)
    x_correct[i] = x_t[N_modes // 2]

    # Wrong noise (same phases for comparison)
    F_k_w = F_amp_wrong * np.exp(1j * phases)
    F_k_w[0] = 0
    X_k_w = F_k_w / H
    x_t_w = np.fft.irfft(X_k_w, n=N_modes)
    x_wrong[i] = x_t_w[N_modes // 2]

print(f"\nMonte Carlo var_x (correct): {np.var(x_correct):.6f}  (target 0.5)")
print(f"Monte Carlo var_x (wrong):   {np.var(x_wrong):.6f}")
print(f"Ratio wrong/correct: {np.var(x_wrong)/np.var(x_correct):.4f}  (expect ~2)")

# Also check velocity
v_correct = np.zeros(N_ensemble)
rng2 = np.random.default_rng(seed)
for i in range(N_ensemble):
    phases = rng2.uniform(0, 2*np.pi, size=N_freq)
    F_k = F_amp_correct * np.exp(1j * phases)
    F_k[0] = 0
    X_k = F_k / H
    V_k = 1j * omega * X_k
    v_t = np.fft.irfft(V_k, n=N_modes)
    x_t = np.fft.irfft(X_k, n=N_modes)
    x_correct[i] = x_t[N_modes // 2]
    v_correct[i] = v_t[N_modes // 2]

var_v_spectral = (2.0 / N_modes**2) * np.sum(omega[1:K]**2 * F_amp_correct[1:K]**2 / np.abs(H[1:K])**2)

print(f"\nvar_v spectral: {var_v_spectral:.6f}  (target 0.5)")
print(f"var_v MC:       {np.var(v_correct):.6f}")
print(f"\nMean energy:    {np.mean(0.5*v_correct**2 + 0.5*x_correct**2):.6f}  (target 0.5)")
