"""
SED Double-Well Simulation — λ = 1.0
V(x) = -½ω₀²x² + ¼λx⁴  with ω₀=1, λ=1.0
→ barrier height V_barrier = ω₀⁴/(4λ) = 0.25  (shallow well)
→ well minima at x_min = ±ω₀/√λ = ±1.0

NOTE: QM ground state energy E₀ = +0.147 > V(0) = 0.
So the QM ground state is ABOVE the barrier. No tunneling regime.
This is classically over-barrier propagation.

The SED will show very frequent crossings — we report the rate.
"""

import numpy as np
import time

omega0    = 1.0
lam       = 1.0
m         = 1.0
hbar      = 1.0
tau       = 0.001
omega_max = 10.0
dt        = 0.05
N         = 200_000
N_traj    = 100
burn_frac = 0.1
seed      = 789

x_min_val  = omega0 / np.sqrt(lam)        # = 1.0
V_barrier  = omega0**4 / (4*lam)          # = 0.25
escape_thr  = 5.0 * x_min_val             # = 5.0

print("=" * 70)
print(f"SED Double-Well: λ={lam}, V_barrier={V_barrier}")
print("=" * 70)
print(f"  x_min = ±{x_min_val:.3f}")
print(f"  V_barrier = {V_barrier:.3f} (QM E₀ = 0.147 > V_barrier → ABOVE barrier!)")
print(f"  No WKB tunneling regime for λ=1.0")
print()

rng = np.random.default_rng(seed)

freqs  = np.fft.rfftfreq(N, d=dt)
omegas = 2.0 * np.pi * freqs
S_F = np.where((omegas > 0) & (omegas <= omega_max),
               2.0 * tau * hbar * omegas**3 / m, 0.0)
A_k = np.sqrt(S_F * N / (2.0 * dt))
n_fft  = len(freqs)
phases = rng.uniform(0, 2*np.pi, size=(N_traj, n_fft))
F_fft  = A_k[np.newaxis, :] * np.exp(1j * phases)
F_fft[:, 0] = 0.0
if N % 2 == 0:
    F_fft[:, -1] = F_fft[:, -1].real
F_zpf  = np.fft.irfft(F_fft, n=N, axis=1).astype(np.float64)
dF_zpf = np.empty_like(F_zpf)
dF_zpf[:, :-1] = np.diff(F_zpf, axis=1) / dt
dF_zpf[:, -1]  = dF_zpf[:, -2]

burn_in   = int(burn_frac * N)
T_measure = (N - burn_in) * dt

x = np.full(N_traj, x_min_val)
v = np.zeros(N_traj)
prev_sign    = np.sign(x)
n_crossings  = np.zeros(N_traj, dtype=int)
n_escaped    = np.zeros(N_traj, dtype=bool)

print("Integrating...", flush=True)
t1 = time.time()
for i in range(N):
    cons_force = omega0**2 * x - lam * x**3
    Vpp        = -omega0**2 + 3.0*lam * x**2
    damp_force = -tau * Vpp * v
    force      = cons_force + damp_force + F_zpf[:, i] + tau * dF_zpf[:, i]
    v         += force * dt
    x         += v * dt

    newly_escaped = (~n_escaped) & (np.abs(x) > escape_thr)
    n_escaped |= newly_escaped

    if i >= burn_in:
        curr_sign = np.sign(x)
        crossed   = (curr_sign != prev_sign) & (curr_sign != 0) & (~n_escaped)
        n_crossings[crossed] += 1
        prev_sign = curr_sign
    else:
        prev_sign = np.sign(x)

    if (i+1) % 50_000 == 0:
        elapsed = time.time() - t1
        print(f"  Step {i+1}/{N}  escaped={n_escaped.sum()}/{N_traj}  "
              f"avg_cross={n_crossings.sum()/N_traj:.1f}  ({elapsed:.1f}s)", flush=True)

print(f"  Done ({time.time()-t1:.1f}s)")

n_esc_total = n_escaped.sum()
n_active = N_traj - n_esc_total

rates = n_crossings[~n_escaped] / T_measure if n_active > 0 else n_crossings / T_measure
mean_rate = np.mean(rates)
sem_rate  = np.std(rates, ddof=1)/np.sqrt(len(rates))

print()
print(f"  Escaped: {n_esc_total}/{N_traj}")
print(f"  Γ_SED = {mean_rate:.6f} ± {sem_rate:.6f} ω₀")
print(f"  (No WKB comparison since E₀ > V_barrier for λ=1)")
print()
print(f"  Crossing counts: {n_crossings.tolist()}")
print()
print("=== SUMMARY FOR REPORT ===")
print(f"λ={lam}, V_barrier={V_barrier}")
print(f"N_escaped={n_esc_total}/{N_traj}")
print(f"Γ_SED = {mean_rate:.6f} ± {sem_rate:.6f} ω₀")
print(f"NOTE: λ=1.0 is over-barrier (E₀>V_barrier), not a tunneling test.")
