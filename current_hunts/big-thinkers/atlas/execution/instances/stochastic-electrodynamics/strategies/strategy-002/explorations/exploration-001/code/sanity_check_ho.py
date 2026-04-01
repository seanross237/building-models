"""
SED Harmonic Oscillator Sanity Check
Verifies var_x ≈ 0.500 (in natural units ħ=m=ω₀=1)
Uses ALD equation with ZPF noise (colored noise, PSD = 2τħω³/m)

ALD for HO V = ½ω₀²x²:
  ẍ = -ω₀²x - τω₀²ẋ + F_zpf + τ·dF_zpf/dt

Vectorized: all N_traj trajectories evolved simultaneously.
Integration: symplectic Euler (Euler-Cromer) — stable for oscillatory systems.
"""

import numpy as np
import time

# ── Parameters ────────────────────────────────────────────────────────────────
omega0    = 1.0       # natural frequency
m         = 1.0       # mass
hbar      = 1.0       # reduced Planck constant
tau       = 0.001     # radiation damping time
omega_max = 10.0      # UV cutoff [rad/time]
dt        = 0.05      # timestep  (π/omega_max ≈ 0.314, so dt is well below Nyquist)
N         = 200_000   # steps per trajectory → T = 10,000 ω₀⁻¹
N_traj    = 50        # trajectories
burn_frac = 0.1       # discard first 10% as burn-in
seed      = 42

print("=" * 60)
print("SED Harmonic Oscillator Sanity Check")
print("=" * 60)
print(f"  ω₀={omega0}, m={m}, ħ={hbar}, τ={tau}")
print(f"  ω_max={omega_max}, dt={dt}, N={N}, N_traj={N_traj}")
print(f"  T = {N*dt:.0f} ω₀⁻¹")
print(f"  Expected: var_x = ħ/(2mω₀) = {hbar/(2*m*omega0):.4f}")
print()

rng = np.random.default_rng(seed)

# ── Generate all ZPF forces at once ───────────────────────────────────────────
t0 = time.time()
print("Generating ZPF force arrays...", flush=True)

freqs  = np.fft.rfftfreq(N, d=dt)          # shape (N//2+1,)
omegas = 2.0 * np.pi * freqs               # angular frequencies

# One-sided PSD: S_F(ω) = 2τħω³/m, with UV cutoff
S_F = np.where((omegas > 0) & (omegas <= omega_max),
               2.0 * tau * hbar * omegas**3 / m,
               0.0)

# FFT amplitude (verified formula from Strategy-001)
A_k = np.sqrt(S_F * N / (2.0 * dt))         # shape (N//2+1,)

# Generate all N_traj realizations: phases shape (N_traj, N//2+1)
n_fft = len(freqs)
phases = rng.uniform(0, 2*np.pi, size=(N_traj, n_fft))
F_fft = A_k[np.newaxis, :] * np.exp(1j * phases)  # (N_traj, n_fft)

# Enforce DC=0 and Nyquist real
F_fft[:, 0] = 0.0
if N % 2 == 0:
    F_fft[:, -1] = F_fft[:, -1].real

# Transform: F shape (N_traj, N)
F_zpf = np.fft.irfft(F_fft, n=N, axis=1).astype(np.float64)

# Time-derivative of ZPF force: dF/dt by finite difference
dF_zpf = np.empty_like(F_zpf)
dF_zpf[:, :-1] = np.diff(F_zpf, axis=1) / dt
dF_zpf[:, -1]  = dF_zpf[:, -2]

print(f"  Done. ({time.time()-t0:.1f}s)")
print(f"  ZPF force RMS check: {np.std(F_zpf[0]):.4f}")
print()

# ── Integrate all trajectories simultaneously ─────────────────────────────────
print("Integrating...", flush=True)
t1 = time.time()

burn_in = int(burn_frac * N)

x = np.zeros(N_traj)    # initial position
v = np.zeros(N_traj)    # initial velocity

x_sq_sum = np.zeros(N_traj)
x_sum    = np.zeros(N_traj)
count    = 0

for i in range(N):
    # ALD forcing for HO: V'=ω₀²x, V''=ω₀²
    force = (-omega0**2 * x
             - tau * omega0**2 * v
             + F_zpf[:, i]
             + tau * dF_zpf[:, i])

    # Symplectic Euler (Euler-Cromer): update v first, then x with new v
    v += force * dt
    x += v * dt

    if i >= burn_in:
        x_sq_sum += x * x
        x_sum    += x
        count    += 1

    if (i+1) % 50_000 == 0:
        elapsed = time.time() - t1
        print(f"  Step {i+1:7d}/{N}  ({elapsed:.1f}s elapsed)  "
              f"x_rms_traj0={np.sqrt(x_sq_sum[0]/count):.4f}", flush=True)

print(f"  Integration done. ({time.time()-t1:.1f}s)")
print()

# ── Compute var_x per trajectory ──────────────────────────────────────────────
mean_x = x_sum / count
var_x  = x_sq_sum / count - mean_x**2   # shape (N_traj,)

grand_mean_var = np.mean(var_x)
sem_var        = np.std(var_x, ddof=1) / np.sqrt(N_traj)

# ── Report ────────────────────────────────────────────────────────────────────
print("=" * 60)
print("RESULTS")
print("=" * 60)
print(f"  Per-trajectory var_x: {var_x}")
print()
print(f"  Mean var_x = {grand_mean_var:.4f}")
print(f"  SEM        = {sem_var:.4f}")
print(f"  Expected   = 0.5000")
print(f"  Ratio      = {grand_mean_var/0.5:.4f}")
print()

if abs(grand_mean_var - 0.5) < 3 * sem_var + 0.02:
    verdict = "PASS"
else:
    verdict = "FAIL"
print(f"  Verdict: {verdict}")
print(f"  (deviation = {abs(grand_mean_var-0.5):.4f}, threshold = {3*sem_var+0.02:.4f})")
