"""
SED Double-Well Simulation — λ = 0.10
V(x) = -½ω₀²x² + ¼λx⁴  with ω₀=1, λ=0.10
→ barrier height V_barrier = ω₀⁴/(4λ) = 2.5  (MUCH higher than λ=0.25)
→ well minima at x_min = ±ω₀/√λ ≈ ±3.162

QM exact: Γ_exact = ΔE/(2ħ) = 0.000428 ω₀  (exponentially suppressed tunneling)
WKB: S_WKB = 6.29 ħ → Γ_WKB = 0.000591 ω₀

This test distinguishes two cases:
(A) SED barrier crossing rate ≈ Γ_WKB  → SED tracks quantum tunneling
(B) SED barrier crossing rate >> Γ_WKB → SED over-estimates via ZPF energy injection
"""

import numpy as np
import time

# ── Parameters ────────────────────────────────────────────────────────────────
omega0    = 1.0
lam       = 0.10
m         = 1.0
hbar      = 1.0
tau       = 0.001
omega_max = 10.0
dt        = 0.05
N         = 200_000     # T = 10,000 ω₀⁻¹
N_traj    = 100
burn_frac = 0.1
seed      = 456

x_min_val  = omega0 / np.sqrt(lam)
V_barrier  = omega0**4 / (4*lam)
omega_local = omega0 * np.sqrt(2.0)
escape_thr  = 3.0 * x_min_val

# QM references (from wkb_rates.py)
Gamma_WKB_goal = 0.00059068
Gamma_exact    = 0.00042789

print("=" * 70)
print(f"SED Double-Well: λ={lam}, ω₀={omega0}, V_barrier={V_barrier}")
print("=" * 70)
print(f"  x_min = ±{x_min_val:.3f},  ω_local = {omega_local:.3f} ω₀")
print(f"  Barrier height = {V_barrier:.3f} ħω₀  (2.5× the barrier for λ=0.25)")
print(f"  τ={tau}, dt={dt}, N={N}, N_traj={N_traj}")
print(f"  Initial condition: x = +{x_min_val:.3f}, v = 0")
print(f"  QM references: Γ_exact={Gamma_exact:.6f}, Γ_WKB={Gamma_WKB_goal:.6f} ω₀")
print()

rng = np.random.default_rng(seed)

# ── Generate ZPF forces ────────────────────────────────────────────────────────
print("Generating ZPF force arrays...", flush=True)
t0 = time.time()

freqs  = np.fft.rfftfreq(N, d=dt)
omegas = 2.0 * np.pi * freqs
S_F = np.where((omegas > 0) & (omegas <= omega_max),
               2.0 * tau * hbar * omegas**3 / m,
               0.0)
A_k = np.sqrt(S_F * N / (2.0 * dt))

n_fft  = len(freqs)
phases = rng.uniform(0, 2*np.pi, size=(N_traj, n_fft))
F_fft  = A_k[np.newaxis, :] * np.exp(1j * phases)
F_fft[:, 0] = 0.0
if N % 2 == 0:
    F_fft[:, -1] = F_fft[:, -1].real

F_zpf = np.fft.irfft(F_fft, n=N, axis=1).astype(np.float64)

dF_zpf = np.empty_like(F_zpf)
dF_zpf[:, :-1] = np.diff(F_zpf, axis=1) / dt
dF_zpf[:, -1]  = dF_zpf[:, -2]

print(f"  Done. ({time.time()-t0:.1f}s)")
print()

# ── Integration ────────────────────────────────────────────────────────────────
print("Integrating...", flush=True)
t1 = time.time()

burn_in = int(burn_frac * N)
T_measure = (N - burn_in) * dt

x = np.full(N_traj, x_min_val)
v = np.zeros(N_traj)

prev_sign = np.sign(x)
n_crossings  = np.zeros(N_traj, dtype=int)
n_escaped    = np.zeros(N_traj, dtype=bool)
escape_time  = np.full(N_traj, np.inf)

# Track max |x| per trajectory
max_abs_x = np.zeros(N_traj)

# Position stats (post-burn-in)
x_sq_sum  = np.zeros(N_traj)
x_sum     = np.zeros(N_traj)
pos_count = np.zeros(N_traj, dtype=int)

# Snapshots
x_snapshots = []

for i in range(N):
    t_now = i * dt

    # Conservative force: -V'(x) = ω₀²x - λx³
    cons_force = omega0**2 * x - lam * x**3

    # ALD damping: -τV''(x)ẋ, V''(x) = -ω₀² + 3λx²
    Vpp = -omega0**2 + 3.0*lam * x**2
    damp_force = -tau * Vpp * v

    # ZPF
    zpf_drive = F_zpf[:, i] + tau * dF_zpf[:, i]

    force = cons_force + damp_force + zpf_drive

    # Symplectic Euler
    v += force * dt
    x += v * dt

    # Escape detection
    abs_x = np.abs(x)
    max_abs_x = np.maximum(max_abs_x, abs_x)
    newly_escaped = (~n_escaped) & (abs_x > escape_thr)
    n_escaped |= newly_escaped
    escape_time[newly_escaped] = t_now

    # Crossing count (post-burn-in)
    if i >= burn_in:
        curr_sign = np.sign(x)
        crossed   = (curr_sign != prev_sign) & (curr_sign != 0) & (~n_escaped)
        n_crossings[crossed] += 1
        prev_sign = curr_sign

        active = ~n_escaped
        x_sq_sum[active] += x[active]**2
        x_sum[active]    += x[active]
        pos_count[active] += 1
    else:
        prev_sign = np.sign(x)

    if i % 20_000 == 0:
        x_snapshots.append((t_now, float(x[0]), float(v[0])))

    if (i+1) % 50_000 == 0:
        elapsed = time.time() - t1
        n_esc_now = n_escaped.sum()
        print(f"  Step {i+1:7d}/{N}  t={t_now:.0f}  escaped={n_esc_now}/{N_traj}  "
              f"avg_crossings={n_crossings.sum()/N_traj:.2f}  "
              f"max|x|_traj0={max_abs_x[0]:.3f}  ({elapsed:.1f}s)", flush=True)

print(f"  Done. ({time.time()-t1:.1f}s)")
print()

# ── Results ───────────────────────────────────────────────────────────────────
n_esc_total = n_escaped.sum()
n_active    = N_traj - n_esc_total

print("=" * 70)
print(f"RESULTS — Double-Well (λ={lam}, V_barrier={V_barrier})")
print("=" * 70)
print(f"  Escaped: {n_esc_total}/{N_traj}")
if n_esc_total > 0:
    ft = escape_time[np.isfinite(escape_time)]
    print(f"  Escape times: mean={np.mean(ft):.1f}, min={np.min(ft):.1f}")
print()

if n_active > 0:
    rates_active = n_crossings[~n_escaped] / T_measure
    mean_rate    = np.mean(rates_active)
    sem_rate     = np.std(rates_active, ddof=1)/np.sqrt(n_active)
    print(f"  Non-escaped: {n_active}")
    print(f"  Crossings (non-escaped): {n_crossings[~n_escaped].tolist()}")
    print(f"  T_measure = {T_measure:.0f} ω₀⁻¹")
    print(f"  Γ_SED (non-escaped) = {mean_rate:.8f} ± {sem_rate:.8f} ω₀")
else:
    rates_all = n_crossings / T_measure
    mean_rate = np.mean(rates_all)
    sem_rate  = np.std(rates_all, ddof=1)/np.sqrt(N_traj)
    print(f"  ALL escaped. Estimated crossing rate: {mean_rate:.8f} ± {sem_rate:.8f} ω₀")

print()
print(f"  Γ_WKB (goal formula) = {Gamma_WKB_goal:.8f} ω₀")
print(f"  Γ_exact (QM)         = {Gamma_exact:.8f} ω₀")
print(f"  Γ_SED / Γ_WKB  = {mean_rate/Gamma_WKB_goal:.4f}")
print(f"  Γ_SED / Γ_exact = {mean_rate/Gamma_exact:.4f}")
print()

print("  Max |x| per trajectory:", np.round(max_abs_x, 2).tolist())
print()
print("  Trajectory-0 snapshots (t, x, v):")
for snap in x_snapshots:
    print(f"    t={snap[0]:7.1f}  x={snap[1]:8.4f}  v={snap[2]:8.4f}")

print()
print("=== SUMMARY FOR REPORT ===")
print(f"λ = {lam},  V_barrier = {V_barrier}")
print(f"N_escaped = {n_esc_total}/{N_traj}")
print(f"Γ_SED = {mean_rate:.8f} ± {sem_rate:.8f} ω₀")
print(f"Γ_WKB = {Gamma_WKB_goal:.8f} ω₀")
print(f"Γ_exact = {Gamma_exact:.8f} ω₀")
print(f"Γ_SED/Γ_WKB = {mean_rate/Gamma_WKB_goal:.4f}")
print(f"Γ_SED/Γ_exact = {mean_rate/Gamma_exact:.4f}")
