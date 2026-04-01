"""
SED Double-Well Simulation — λ = 0.25
V(x) = -½ω₀²x² + ¼λx⁴  with ω₀=1, λ=0.25
→ barrier height V_barrier = ω₀⁴/(4λ) = 1.0
→ well minima at x_min = ±ω₀/√λ = ±2

ALD equation:
  ẍ = (ω₀²x - λx³) - τ(−ω₀² + 3λx²)ẋ + F_zpf + τ·dF_zpf/dt
    = (ω₀²x - λx³) + τ(ω₀² - 3λx²)ẋ + F_zpf + τ·dF_zpf/dt

Wait — check sign convention from GOAL:
  ẍ = -V'(x)/m - τ·V''(x)·ẋ + F_zpf + τ·F'_zpf
  V'(x) = -ω₀²x + λx³
  V''(x) = -ω₀² + 3λx²

So: force = ω₀²x - λx³   [= -V'(x)]
    damping = -τ(−ω₀² + 3λx²)ẋ = τ(ω₀² - 3λx²)ẋ

NOTE: At x=x_min, V''(x_min) = 2ω₀² > 0, so damping = -τ·2ω₀²·ẋ < 0 (removes energy)
      At x=0, V''(0) = -ω₀² < 0, so damping = τ·ω₀²·ẋ > 0 (adds energy at barrier)

This is the physical ALD radiation reaction: positive damping where the particle oscillates,
anti-damping near the unstable equilibrium.
"""

import numpy as np
import time

# ── Parameters ────────────────────────────────────────────────────────────────
omega0    = 1.0
lam       = 0.25
m         = 1.0
hbar      = 1.0
tau       = 0.001
omega_max = 10.0
dt        = 0.05
N         = 200_000     # T = 10,000 ω₀⁻¹
N_traj    = 100
burn_frac = 0.1
seed      = 123

x_min_val  = omega0 / np.sqrt(lam)           # = 2.0
V_barrier  = omega0**4 / (4*lam)             # = 1.0
omega_local = np.sqrt(2.0) * omega0          # local freq at well bottom = sqrt(V''(x_min))
escape_thr  = 3.0 * x_min_val               # = 6.0 (escape threshold)

print("=" * 70)
print(f"SED Double-Well: λ={lam}, ω₀={omega0}, V_barrier={V_barrier}")
print("=" * 70)
print(f"  x_min = ±{x_min_val:.3f},  ω_local = {omega_local:.3f} ω₀")
print(f"  Barrier height = {V_barrier:.3f} ħω₀")
print(f"  τ={tau}, dt={dt}, N={N}, N_traj={N_traj}")
print(f"  Initial condition: x = +{x_min_val:.2f} (right well bottom), v = 0")
print(f"  Escape threshold: |x| > {escape_thr:.1f}")
print()

rng = np.random.default_rng(seed)

# ── Generate all ZPF forces ────────────────────────────────────────────────────
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
print("Integrating double-well trajectories...", flush=True)
t1 = time.time()

burn_in = int(burn_frac * N)
T_measure = (N - burn_in) * dt   # measurement time

# Initial conditions: right well bottom
x = np.full(N_traj, x_min_val)
v = np.zeros(N_traj)

# Track sign of x for crossing count
prev_sign = np.sign(x)     # all +1 initially

# Counters
n_crossings  = np.zeros(N_traj, dtype=int)   # barrier crossing count
n_escaped    = np.zeros(N_traj, dtype=bool)  # did particle escape?
escape_time  = np.full(N_traj, np.inf)       # time of first escape

# Position stats (post-burn-in, non-escaped only)
x_sq_sum  = np.zeros(N_traj)
x_sum     = np.zeros(N_traj)
pos_count = np.zeros(N_traj, dtype=int)

# Position histogram for full distribution
x_hist_edges = np.linspace(-escape_thr, escape_thr, 201)
x_hist_all   = np.zeros(200)   # aggregate histogram

# Track trajectory snapshots for diagnosis
x_snapshots = []   # list of (step, x[0]) for trajectory 0

for i in range(N):
    t_now = i * dt

    # Double-well force: -V'(x) = ω₀²x - λx³
    cons_force = omega0**2 * x - lam * x**3

    # ALD damping: -τV''(x)ẋ where V''(x) = -ω₀² + 3λx²
    Vpp = -omega0**2 + 3.0*lam * x**2
    damp_force = -tau * Vpp * v

    # ZPF driving
    zpf_drive = F_zpf[:, i] + tau * dF_zpf[:, i]

    force = cons_force + damp_force + zpf_drive

    # Symplectic Euler
    v += force * dt
    x += v * dt

    # Detect escape (before recording stats)
    newly_escaped = (~n_escaped) & (np.abs(x) > escape_thr)
    n_escaped |= newly_escaped
    escape_time[newly_escaped] = t_now

    # Count barrier crossings (sign change of x, only post-burn-in, non-escaped)
    if i >= burn_in:
        curr_sign = np.sign(x)
        crossed   = (curr_sign != prev_sign) & (curr_sign != 0) & (~n_escaped)
        n_crossings[crossed] += 1
        prev_sign = curr_sign

        # Position stats (non-escaped only)
        active = ~n_escaped
        x_sq_sum[active] += x[active]**2
        x_sum[active]    += x[active]
        pos_count[active] += 1

    # Update prev_sign even during burn-in
    if i < burn_in:
        prev_sign = np.sign(x)

    # Snapshot for trajectory 0
    if i % 10_000 == 0:
        x_snapshots.append((i * dt, float(x[0]), float(v[0])))

    if (i+1) % 50_000 == 0:
        elapsed = time.time() - t1
        n_esc_now = n_escaped.sum()
        mean_cross = n_crossings.sum() / N_traj
        print(f"  Step {i+1:7d}/{N}  t={t_now:.0f}  escaped={n_esc_now}/{N_traj}  "
              f"avg_crossings={mean_cross:.1f}  x[0]={x[0]:.3f}  ({elapsed:.1f}s)", flush=True)

print(f"  Done. ({time.time()-t1:.1f}s)")
print()

# ── Analysis ─────────────────────────────────────────────────────────────────
n_esc_total = n_escaped.sum()
n_active    = N_traj - n_esc_total

print("=" * 70)
print("RESULTS — Double-Well (λ=0.25, V_barrier=1.0)")
print("=" * 70)
print(f"  Escaped particles:  {n_esc_total}/{N_traj} ({100*n_esc_total/N_traj:.0f}%)")
if n_esc_total > 0:
    finite_escape = escape_time[np.isfinite(escape_time)]
    print(f"  Escape times:  mean={np.mean(finite_escape):.1f}, min={np.min(finite_escape):.1f} ω₀⁻¹")
print()

# Barrier crossing rate (Γ_SED)
# For non-escaped trajectories: rate = n_crossings / T_measure
# For escaped trajectories: use crossings before escape
if n_active > 0:
    rates_active = n_crossings[~n_escaped] / T_measure
    mean_rate = np.mean(rates_active)
    sem_rate  = np.std(rates_active, ddof=1) / np.sqrt(n_active) if n_active > 1 else 0
    print(f"  Non-escaped trajectories: {n_active}")
    print(f"  Crossings (non-escaped): {n_crossings[~n_escaped]}")
    print(f"  T_measure = {T_measure:.0f} ω₀⁻¹")
    print(f"  Γ_SED (non-escaped) = {mean_rate:.6f} ± {sem_rate:.6f} ω₀")
else:
    print("  All particles escaped — no stable barrier-crossing rate measured")
    # Compute rate from crossings before escape
    all_rates = n_crossings / T_measure  # rough estimate
    mean_rate = np.mean(all_rates)
    sem_rate  = np.std(all_rates, ddof=1) / np.sqrt(N_traj)
    print(f"  Estimated total crossing rate: {mean_rate:.6f} ± {sem_rate:.6f} ω₀ (all traj)")

print()

# Position distribution
if n_active > 0 and pos_count[~n_escaped].sum() > 0:
    active_mask  = ~n_escaped
    mean_x_sq   = x_sq_sum[active_mask].sum() / pos_count[active_mask].sum()
    mean_xval   = x_sum[active_mask].sum() / pos_count[active_mask].sum()
    var_x_total = mean_x_sq - mean_xval**2
    print(f"  〈x〉 (non-escaped) = {mean_xval:.4f}")
    print(f"  var_x (non-escaped) = {var_x_total:.4f}")
    print(f"  x_rms (non-escaped) = {np.sqrt(mean_x_sq):.4f}")

print()
print("  Trajectory-0 snapshots (t, x, v):")
for snap in x_snapshots:
    print(f"    t={snap[0]:7.1f}  x={snap[1]:8.4f}  v={snap[2]:8.4f}")

print()
print("  Crossing counts per trajectory:", n_crossings)
print()
print(f"  Mean crossings per trajectory: {np.mean(n_crossings):.2f}")
print(f"  Total measurement time (non-escaped): T_measure = {T_measure:.0f} ω₀⁻¹")

# ── Save summary for REPORT ───────────────────────────────────────────────────
print()
print("=== SUMMARY FOR REPORT ===")
print(f"λ = {lam}")
print(f"V_barrier = {V_barrier}")
print(f"x_min = {x_min_val}")
print(f"ω_local = {omega_local:.4f}")
print(f"N_escaped = {n_esc_total}/{N_traj}")
if n_active > 0:
    print(f"Γ_SED = {mean_rate:.6f} ± {sem_rate:.6f} ω₀")
else:
    print(f"Γ_SED = ALL ESCAPED (no stable rate)")
print(f"Crossings: {n_crossings.tolist()}")
