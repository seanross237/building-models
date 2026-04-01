#!/usr/bin/env python3
"""
SED Hydrogen Self-Ionization Simulation
Exploration 003 — Stochastic Electrodynamics (Strategy 002)

Simulates a classical electron in a Coulomb potential plus SED zero-point field.
Measures ionization timescale T_ion as a function of angular momentum L.

Physics (atomic units: hbar = m_e = e = a0 = 1):
  - Coulomb: F_C = -r/|r|^3
  - ZPF PSD per component: S_F(omega) = 2*tau*omega^3, omega <= omega_max
  - ALD (Landau-Lifshitz form):
      a = F_C + tau*dF_C/dt + F_zpf + tau*dF_zpf/dt
  - tau = 1.57e-5 a.u.

Author: Atlas Math Explorer, Exploration 003
"""

import numpy as np
import time
import sys

# ============================================================
# Physical Parameters
# ============================================================
TAU = 1.57e-5       # radiation reaction time (atomic units)
OMEGA_MAX = 100.0   # UV cutoff frequency (atomic units)
DT = 0.01           # base timestep (atomic units)
T_ORB = 2 * np.pi   # orbital period for n=1 Bohr orbit

# Thresholds
R_ION = 5.0         # ionization: r > 5 a0
R_NUKE = 0.05       # nuclear collision: r < 0.05 a0
R_SOFT = 0.02       # Coulomb softening: max(r, R_SOFT)

# ============================================================
# ZPF Noise Generation
# ============================================================

def generate_zpf(N_steps, dt=DT, seed=None):
    """
    Generate ZPF stochastic force (3D) and its time derivative.

    Uses FFT method: generates colored Gaussian noise with
    one-sided PSD S_F(omega) = 2*tau*omega^3 per spatial component.

    FFT amplitude: A_k = sqrt(S_F(omega_k) * N / (2*dt))

    Parameters:
    -----------
    N_steps : int
        Number of timesteps to generate
    dt : float
        Timestep (atomic units)
    seed : int or None
        Random seed for reproducibility

    Returns:
    --------
    F_zpf : (N_steps, 3) array
        ZPF force in x, y, z directions
    dF_zpf : (N_steps, 3) array
        Time derivative of ZPF force (for tau*dF_zpf/dt term)
    """
    rng = np.random.default_rng(seed)
    N = N_steps

    # One-sided frequencies for rfft
    omega = 2 * np.pi * np.fft.rfftfreq(N, d=dt)  # shape: (N//2 + 1,)
    n_freq = len(omega)

    # One-sided PSD: S_F(omega) = 2*tau*omega^3, with UV cutoff
    S_F = np.where((omega > 0) & (omega <= OMEGA_MAX),
                   2.0 * TAU * omega**3, 0.0)

    # FFT amplitudes from GOAL.md formula: A_k = sqrt(S_F * N / (2*dt))
    A = np.sqrt(np.maximum(S_F * N / (2.0 * dt), 0.0))

    F_zpf = np.zeros((N, 3))
    dF_zpf = np.zeros((N, 3))

    for i in range(3):
        # Random phases in [0, 2*pi)
        phases = rng.uniform(0.0, 2.0 * np.pi, n_freq)

        # Complex FFT coefficients with prescribed amplitude and random phase
        coeffs = A * np.exp(1j * phases)
        coeffs[0] = 0.0  # no DC component

        # Time-domain force via inverse rfft
        # irfft uses convention: x[n] = (1/N) * sum_k C[k] * exp(+2*pi*i*k*n/N)
        # so d/dt x[n] corresponds to multiplying C[k] by +i*omega_k
        F_zpf[:, i] = np.fft.irfft(coeffs, n=N)

        # Time derivative of force in Fourier space: multiply by i*omega
        dF_zpf[:, i] = np.fft.irfft(1j * omega * coeffs, n=N)

    return F_zpf, dF_zpf


def zpf_rms_theoretical():
    """
    Theoretical RMS ZPF force per component.
    sigma^2 = (1/2pi) * int_0^omega_max S_F(omega) domega
             = (1/2pi) * tau * omega_max^4 / 2
    """
    sigma2 = TAU * OMEGA_MAX**4 / (4 * np.pi)
    return np.sqrt(sigma2)


# ============================================================
# Equations of Motion
# ============================================================

def compute_accel(pos, vel, Fz, dFz):
    """
    Compute total acceleration from Landau-Lifshitz ALD:
      a = F_C + tau*dF_C/dt + F_zpf + tau*dF_zpf/dt

    Parameters:
    -----------
    pos : (3,) array  - position vector
    vel : (3,) array  - velocity vector
    Fz  : (3,) array  - ZPF force at current time
    dFz : (3,) array  - ZPF force time derivative

    Returns:
    --------
    accel : (3,) array - total acceleration
    """
    r = np.sqrt(np.dot(pos, pos))
    r_eff = max(r, R_SOFT)  # softened radius
    r3 = r_eff**3
    r2 = r_eff**2

    # Coulomb force: F_C = -pos/r^3
    F_C = -pos / r3

    # Time derivative of Coulomb force:
    # d/dt(-pos/r^3) = -vel/r^3 + 3*pos*(pos·vel/r^2)/r^3
    #                = (-vel + 3*pos*(pos·vel/r^2)) / r^3
    rdv = np.dot(pos, vel)
    dF_C = (-vel + 3.0 * pos * rdv / r2) / r3

    # Total acceleration
    return F_C + TAU * dF_C + Fz + TAU * dFz


# ============================================================
# RK4 Integrator (fixed step)
# ============================================================

def rk4_step(pos, vel, Fn, dFn, Fh, dFh, Fnp1, dFnp1, dt):
    """
    One RK4 step.

    Forces provided at: current (n), half-step (h = n+1/2), next (n+1).
    Half-step forces are linearly interpolated: Fh = 0.5*(Fn + Fnp1).
    """
    # k1: at (pos, vel) with forces at t_n
    a1 = compute_accel(pos, vel, Fn, dFn)

    # k2: at (pos + dt/2*vel, vel + dt/2*a1) with forces at t_{n+1/2}
    pos2 = pos + 0.5 * dt * vel
    vel2 = vel + 0.5 * dt * a1
    a2 = compute_accel(pos2, vel2, Fh, dFh)

    # k3: at (pos + dt/2*vel2, vel + dt/2*a2) with forces at t_{n+1/2}
    pos3 = pos + 0.5 * dt * vel2
    vel3 = vel + 0.5 * dt * a2
    a3 = compute_accel(pos3, vel3, Fh, dFh)

    # k4: at (pos + dt*vel3, vel + dt*a3) with forces at t_{n+1}
    pos4 = pos + dt * vel3
    vel4 = vel + dt * a3
    a4 = compute_accel(pos4, vel4, Fnp1, dFnp1)

    # Combine
    pos_new = pos + (dt / 6.0) * (vel + 2.0 * vel2 + 2.0 * vel3 + vel4)
    vel_new = vel + (dt / 6.0) * (a1 + 2.0 * a2 + 2.0 * a3 + a4)

    return pos_new, vel_new


# ============================================================
# Pure Coulomb (no ZPF, no radiation reaction)
# ============================================================

def compute_accel_pure(pos, vel):
    """Pure Coulomb acceleration (no ZPF, no radiation reaction)."""
    r = np.sqrt(np.dot(pos, pos))
    r_eff = max(r, R_SOFT)
    return -pos / r_eff**3


def rk4_step_pure(pos, vel, dt):
    """RK4 step for pure Coulomb orbit."""
    a1 = compute_accel_pure(pos, vel)
    pos2 = pos + 0.5 * dt * vel
    vel2 = vel + 0.5 * dt * a1
    a2 = compute_accel_pure(pos2, vel2)
    pos3 = pos + 0.5 * dt * vel2
    vel3 = vel + 0.5 * dt * a2
    a3 = compute_accel_pure(pos3, vel3)
    pos4 = pos + dt * vel3
    vel4 = vel + dt * a3
    a4 = compute_accel_pure(pos4, vel4)
    pos_new = pos + (dt / 6.0) * (vel + 2.0 * vel2 + 2.0 * vel3 + vel4)
    vel_new = vel + (dt / 6.0) * (a1 + 2.0 * a2 + 2.0 * a3 + a4)
    return pos_new, vel_new


def run_pure_coulomb(n_periods=100, dt=DT):
    """
    Sanity check: pure Coulomb orbit.
    Should be stable indefinitely (up to numerical precision).
    Returns (t_arr, r_arr, E_arr).
    """
    N = int(n_periods * T_ORB / dt)
    pos = np.array([1.0, 0.0, 0.0])
    vel = np.array([0.0, 1.0, 0.0])  # circular orbit at r=1

    t_arr = np.zeros(N)
    r_arr = np.zeros(N)
    E_arr = np.zeros(N)

    for n in range(N):
        r = np.sqrt(np.dot(pos, pos))
        v2 = np.dot(vel, vel)
        E = 0.5 * v2 - 1.0 / r

        t_arr[n] = n * dt
        r_arr[n] = r
        E_arr[n] = E

        pos, vel = rk4_step_pure(pos, vel, dt)

    return t_arr, r_arr, E_arr


# ============================================================
# ZPF-only (no radiation reaction)
# ============================================================

def run_zpf_only(L, N_steps, seed, dt=DT):
    """
    ZPF only, no radiation reaction (tau=0).
    Expected: rapid ionization since there's no damping.
    """
    F_zpf, _ = generate_zpf(N_steps, dt=dt, seed=seed)

    pos = np.array([1.0, 0.0, 0.0])
    vel = np.array([0.0, float(L), 0.0])

    for n in range(N_steps - 1):
        r = np.sqrt(np.dot(pos, pos))
        if r > R_ION:
            return n * dt, r
        if r < R_NUKE:
            return n * dt, r

        Fz = F_zpf[n]
        Fh = 0.5 * (F_zpf[n] + F_zpf[n + 1])
        Fnp1 = F_zpf[n + 1]

        # Coulomb + ZPF only (no radiation reaction)
        def accel_no_rr(pos_, vel_, Fz_):
            r_ = max(np.sqrt(np.dot(pos_, pos_)), R_SOFT)
            return -pos_ / r_**3 + Fz_

        a1 = accel_no_rr(pos, vel, Fz)
        pos2 = pos + 0.5 * dt * vel; vel2 = vel + 0.5 * dt * a1
        a2 = accel_no_rr(pos2, vel2, Fh)
        pos3 = pos + 0.5 * dt * vel2; vel3 = vel + 0.5 * dt * a2
        a3 = accel_no_rr(pos3, vel3, Fh)
        pos4 = pos + dt * vel3; vel4 = vel + dt * a3
        a4 = accel_no_rr(pos4, vel4, Fnp1)

        pos = pos + (dt / 6.0) * (vel + 2 * vel2 + 2 * vel3 + vel4)
        vel = vel + (dt / 6.0) * (a1 + 2 * a2 + 2 * a3 + a4)

    return np.nan, np.sqrt(np.dot(pos, pos))


# ============================================================
# Full SED Simulation (Coulomb + Radiation Reaction + ZPF)
# ============================================================

def run_full_sed(L, N_steps, seed, dt=DT, record_every=500):
    """
    Full SED hydrogen simulation.

    Parameters:
    -----------
    L : float
        Initial angular momentum (= tangential velocity at r=1)
    N_steps : int
        Maximum number of timesteps
    seed : int
        Random seed for ZPF realization
    dt : float
        Timestep (atomic units)
    record_every : int
        Record r(t) every this many steps for diagnostics

    Returns:
    --------
    t_ion : float or nan
        Ionization time (atomic units), or nan if not ionized
    ionized : bool
        True if ionized, False if ran full simulation
    r_trace : list of (t, r) tuples
        Sampled radius history
    E_trace : list of (t, E) tuples
        Sampled energy history
    """
    F_zpf, dF_zpf = generate_zpf(N_steps, dt=dt, seed=seed)

    pos = np.array([1.0, 0.0, 0.0])
    vel = np.array([0.0, float(L), 0.0])

    r_trace = []
    E_trace = []

    t_ion = np.nan
    ionized = False
    final_r = np.nan

    for n in range(N_steps - 1):
        r = np.sqrt(np.dot(pos, pos))
        v2 = np.dot(vel, vel)
        E = 0.5 * v2 - 1.0 / max(r, R_SOFT)

        if n % record_every == 0:
            r_trace.append((n * dt, r))
            E_trace.append((n * dt, E))

        if r > R_ION:
            t_ion = n * dt
            ionized = True
            break
        if r < R_NUKE:
            t_ion = n * dt
            ionized = True  # treat nuclear collision as ionization event
            break

        # Precompute forces at n, n+1/2, n+1
        Fn = F_zpf[n]
        dFn = dF_zpf[n]
        Fh = 0.5 * (F_zpf[n] + F_zpf[n + 1])
        dFh = 0.5 * (dF_zpf[n] + dF_zpf[n + 1])
        Fnp1 = F_zpf[n + 1]
        dFnp1 = dF_zpf[n + 1]

        pos, vel = rk4_step(pos, vel, Fn, dFn, Fh, dFh, Fnp1, dFnp1, dt)

    if not ionized:
        final_r = np.sqrt(np.dot(pos, pos))

    return t_ion, ionized, r_trace, E_trace


# ============================================================
# Batch Run for Multiple Trajectories
# ============================================================

def run_batch(L, N_traj, N_steps, dt=DT, base_seed=0, verbose=True):
    """
    Run N_traj independent SED trajectories for angular momentum L.

    Returns:
    --------
    results : list of (t_ion, ionized, r_trace, E_trace)
    stats : dict with mean_T_ion, std_T_ion, fraction_ionized, mean_r_initial
    """
    results = []
    t_ions = []

    for k in range(N_traj):
        seed = base_seed + k * 1000
        t_start = time.time()
        t_ion, ionized, r_trace, E_trace = run_full_sed(L, N_steps, seed=seed, dt=dt)
        elapsed = time.time() - t_start

        t_ion_periods = t_ion / T_ORB if not np.isnan(t_ion) else np.nan
        r_final = r_trace[-1][1] if r_trace else np.nan

        if verbose:
            status = f"T_ion = {t_ion_periods:.1f} periods" if ionized else "STABLE"
            print(f"  Traj {k+1:2d}: {status}  (r_final={r_final:.2f}) [{elapsed:.1f}s]")

        results.append((t_ion, ionized, r_trace, E_trace))
        if ionized:
            t_ions.append(t_ion)

    # Statistics
    n_ionized = sum(1 for _, ion, _, _ in results if ion)
    fraction = n_ionized / N_traj

    t_ions_arr = np.array(t_ions) / T_ORB  # in orbital periods
    mean_T = np.nanmean(t_ions_arr) if t_ions_arr.size > 0 else np.nan
    std_T = np.nanstd(t_ions_arr) if t_ions_arr.size > 0 else np.nan

    # Mean radius during first 100 periods (from r_trace)
    r_early = []
    for _, _, r_trace, _ in results:
        early = [r for t, r in r_trace if t < 100 * T_ORB]
        if early:
            r_early.extend(early)
    mean_r = np.mean(r_early) if r_early else np.nan

    stats = {
        'L': L,
        'N_traj': N_traj,
        'n_ionized': n_ionized,
        'fraction_ionized': fraction,
        'mean_T_ion_periods': mean_T,
        'std_T_ion_periods': std_T,
        'mean_r_early': mean_r,
        't_ions_periods': t_ions_arr.tolist(),
    }

    return results, stats


# ============================================================
# ASCII Plot Helpers
# ============================================================

def ascii_plot_r(r_trace, E_trace=None, title="", width=70, height=20):
    """Simple ASCII plot of r(t)."""
    if not r_trace:
        print("  [no data]")
        return

    times = [t / T_ORB for t, r in r_trace]  # in orbital periods
    radii = [r for t, r in r_trace]

    t_min, t_max = min(times), max(times)
    r_min, r_max = min(radii), max(radii)
    r_min = 0.0  # force y-axis to start at 0

    if r_max <= r_min:
        r_max = r_min + 1

    print(f"\n  {title}")
    print(f"  r/a0 [{r_min:.1f}..{r_max:.1f}] vs t [0..{t_max:.0f} periods]")
    print(f"  {'─'*width}")

    # Build grid
    grid = [[' '] * width for _ in range(height)]

    for t, r in zip(times, radii):
        col = int((t - t_min) / (t_max - t_min + 1e-10) * (width - 1))
        row = int((r - r_min) / (r_max - r_min + 1e-10) * (height - 1))
        row = height - 1 - row  # flip y-axis
        col = max(0, min(width - 1, col))
        row = max(0, min(height - 1, row))
        grid[row][col] = '*'

    # Draw horizontal line at r=1 (Bohr radius)
    r1_row = int((1.0 - r_min) / (r_max - r_min + 1e-10) * (height - 1))
    r1_row = height - 1 - r1_row
    if 0 <= r1_row < height:
        for c in range(width):
            if grid[r1_row][c] == ' ':
                grid[r1_row][c] = '-'

    for row in grid:
        print(f"  |{''.join(row)}|")
    print(f"  {'─'*width}")
    print(f"  (--- = Bohr radius a0 = 1)")


# ============================================================
# Main entry point
# ============================================================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='SED Hydrogen Simulation')
    parser.add_argument('--L', type=float, default=1.0, help='Angular momentum (hbar)')
    parser.add_argument('--N_traj', type=int, default=20, help='Number of trajectories')
    parser.add_argument('--N_periods', type=int, default=200, help='Max orbital periods')
    parser.add_argument('--sanity', action='store_true', help='Run sanity checks only')
    parser.add_argument('--seed', type=int, default=42, help='Base random seed')
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"SED Hydrogen Simulation — Exploration 003")
    print(f"{'='*60}")
    print(f"Parameters: TAU={TAU}, OMEGA_MAX={OMEGA_MAX}, DT={DT}")
    print(f"ZPF RMS force (theoretical): {zpf_rms_theoretical():.3f} a.u./component")

    if args.sanity:
        # Sanity check 1: pure Coulomb
        print("\n[SANITY 1] Pure Coulomb orbit (no ZPF, no radiation reaction)")
        print(f"  Running {100} orbital periods...")
        t_arr, r_arr, E_arr = run_pure_coulomb(n_periods=100)
        r_mean = np.mean(r_arr)
        r_std = np.std(r_arr)
        E_mean = np.mean(E_arr)
        E_std = np.std(E_arr)
        print(f"  r: mean = {r_mean:.6f}, std = {r_std:.2e}  (expected: 1.000000, ~0)")
        print(f"  E: mean = {E_mean:.6f}, std = {E_std:.2e}  (expected: -0.500000, ~0)")

        # Sanity check 2: ZPF noise statistics
        print("\n[SANITY 2] ZPF noise statistics")
        N_test = 100000
        F_test, dF_test = generate_zpf(N_test, seed=123)
        rms_measured = np.sqrt(np.mean(F_test**2))
        rms_theory = zpf_rms_theoretical()
        print(f"  Measured RMS: {rms_measured:.3f} a.u.")
        print(f"  Theoretical:  {rms_theory:.3f} a.u.")
        print(f"  Ratio: {rms_measured/rms_theory:.3f}  (expected: ~1.0)")

        # Sanity check 3: ZPF only (no damping)
        print("\n[SANITY 3] ZPF only, no radiation reaction (L=1.0)")
        N_max_zpf = int(20 * T_ORB / DT)
        t_ion, r_final = run_zpf_only(1.0, N_max_zpf, seed=42)
        if np.isnan(t_ion):
            print(f"  Not ionized within 20 periods (r_final={r_final:.3f})")
        else:
            print(f"  Ionized at t = {t_ion/T_ORB:.2f} periods (r={r_final:.2f})")
        print()

    else:
        L = args.L
        N_periods = args.N_periods
        N_steps = int(N_periods * T_ORB / DT) + 1
        N_traj = args.N_traj

        print(f"\nRunning L = {L} ħ, {N_traj} trajectories, cap = {N_periods} periods")
        print(f"  N_steps per trajectory: {N_steps:,}")
        print(f"  Estimated memory per trajectory: {N_steps*6*8/1e6:.1f} MB")

        t0 = time.time()
        results, stats = run_batch(L, N_traj, N_steps,
                                   base_seed=args.seed, verbose=True)
        elapsed = time.time() - t0

        print(f"\n--- Results for L = {L} ħ ---")
        print(f"  Fraction ionized: {stats['fraction_ionized']:.0%} ({stats['n_ionized']}/{N_traj})")
        if not np.isnan(stats['mean_T_ion_periods']):
            print(f"  Mean T_ion:  {stats['mean_T_ion_periods']:.1f} ± {stats['std_T_ion_periods']:.1f} orbital periods")
            print(f"  Min T_ion:   {min(stats['t_ions_periods']):.1f} periods")
            print(f"  Max T_ion:   {max(stats['t_ions_periods']):.1f} periods")
        else:
            print(f"  No ionization observed within {N_periods} periods")
        print(f"  Mean r (early): {stats['mean_r_early']:.3f} a0")
        print(f"  Total time: {elapsed:.1f} s")

        # Plot first trajectory
        if results:
            _, _, r_trace, E_trace = results[0]
            ascii_plot_r(r_trace, E_trace, title=f"r(t) for L={L}, trajectory 1")

        # Print statistics dict
        print(f"\n  Raw t_ions (periods): {[f'{t:.1f}' for t in stats['t_ions_periods']]}")
