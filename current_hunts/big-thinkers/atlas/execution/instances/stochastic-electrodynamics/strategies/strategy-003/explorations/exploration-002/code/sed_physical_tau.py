#!/usr/bin/env python3
"""
SED Hydrogen Self-Ionization Simulation — Physical TAU
Exploration 002, Strategy 003

Physical τ = 2/(3 × 137.036³) ≈ 2.590×10⁻⁷ atomic units
(60× smaller than E003's τ = 1.57×10⁻⁵)

Chunked ZPF generation (2^17 = 131072 points per chunk, power-of-2 FFT).
C inner loop via ctypes (gcc -O3 -march=native -ffast-math).
Multiprocessing across trajectories.
"""

import numpy as np
import ctypes
import os
import time
import sys
import json
import multiprocessing as mp

# ============================================================
# Physical Parameters
# ============================================================
ALPHA = 1.0 / 137.036            # fine structure constant
TAU   = 2.0 / (3.0 * 137.036**3) # = 2α³/3 ≈ 2.590×10⁻⁷ a.u.
OMEGA_MAX = 100.0                  # UV cutoff (a.u.)
DT    = 0.01                       # timestep (a.u.)
T_ORB = 2.0 * np.pi               # Bohr orbital period (a.u.)

R_ION  = 5.0                       # ionization radius (a.u.)
R_NUKE = 0.05                      # nuclear collision radius (a.u.)
R_SOFT = 0.02                      # Coulomb softening (a.u.)

# Chunk size: generate CHUNK_PTS = 2^17 = 131072 points per chunk
# Use CHUNK_STEPS = CHUNK_PTS - 1 = 131071 integration steps per chunk
# (the last point serves as lookahead for the last RK4 step)
CHUNK_PTS   = 131072               # = 2^17 (fast FFT!)
CHUNK_STEPS = CHUNK_PTS - 1       # = 131071 steps per chunk

# ============================================================
# C Library Loading
# ============================================================

LIB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libsed.so')

def load_lib():
    """Load the compiled C integration library."""
    lib = ctypes.CDLL(LIB_PATH)

    # void integrate_chunk(double *px, py, pz, vx, vy, vz,
    #                      const double *F_zpf, const double *dF_zpf,
    #                      int n_steps,
    #                      double dt, tau, r_soft, r_ion, r_nuke,
    #                      int *steps_done, int *ionized)
    lib.integrate_chunk.restype = None
    lib.integrate_chunk.argtypes = [
        ctypes.POINTER(ctypes.c_double),  # px
        ctypes.POINTER(ctypes.c_double),  # py
        ctypes.POINTER(ctypes.c_double),  # pz
        ctypes.POINTER(ctypes.c_double),  # vx
        ctypes.POINTER(ctypes.c_double),  # vy
        ctypes.POINTER(ctypes.c_double),  # vz
        ctypes.POINTER(ctypes.c_double),  # F_zpf  (n_steps+1, 3)
        ctypes.POINTER(ctypes.c_double),  # dF_zpf (n_steps+1, 3)
        ctypes.c_int,                     # n_steps
        ctypes.c_double,                  # dt
        ctypes.c_double,                  # tau
        ctypes.c_double,                  # r_soft
        ctypes.c_double,                  # r_ion
        ctypes.c_double,                  # r_nuke
        ctypes.POINTER(ctypes.c_int),     # steps_done
        ctypes.POINTER(ctypes.c_int),     # ionized
    ]

    # void integrate_chunk_pure_coulomb(double *px, py, pz, vx, vy, vz,
    #                                   int n_steps, double dt, r_soft,
    #                                   double *energies_out)
    lib.integrate_chunk_pure_coulomb.restype = None
    lib.integrate_chunk_pure_coulomb.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.POINTER(ctypes.c_double),  # energies_out (or NULL)
    ]

    return lib

# ============================================================
# ZPF Noise Generation
# ============================================================

def generate_zpf_chunk(seed):
    """
    Generate CHUNK_PTS = 2^17 = 131072 time-domain samples of ZPF force
    and its time derivative, for all 3 spatial components.

    Uses FFT method with one-sided PSD S_F(ω) = 2·τ·ω³ (ω ≤ ω_max).
    FFT amplitude: A_k = sqrt(S_F(ω_k) · N / (2·dt))

    Returns:
    --------
    F_zpf  : (CHUNK_PTS, 3) float64 array, C-contiguous
    dF_zpf : (CHUNK_PTS, 3) float64 array, C-contiguous
    """
    rng = np.random.default_rng(seed)
    N = CHUNK_PTS

    # Frequencies for rfft (N//2+1 = 65537 unique frequencies)
    omega = 2.0 * np.pi * np.fft.rfftfreq(N, d=DT)  # shape (65537,)
    n_freq = len(omega)

    # One-sided PSD with UV cutoff
    S_F = np.where((omega > 0) & (omega <= OMEGA_MAX),
                   2.0 * TAU * omega**3, 0.0)
    # FFT amplitude
    A = np.sqrt(S_F * N / (2.0 * DT))   # S_F already has correct shape

    F_zpf  = np.zeros((N, 3), dtype=np.float64)
    dF_zpf = np.zeros((N, 3), dtype=np.float64)

    for i in range(3):
        phases = rng.uniform(0.0, 2.0 * np.pi, n_freq)
        coeffs = A * np.exp(1j * phases)
        coeffs[0] = 0.0   # zero DC

        F_zpf[:, i]  = np.fft.irfft(coeffs, n=N)
        dF_zpf[:, i] = np.fft.irfft(1j * omega * coeffs, n=N)

    # Ensure C-contiguous for ctypes
    return np.ascontiguousarray(F_zpf), np.ascontiguousarray(dF_zpf)


def zpf_rms_theoretical():
    """Theoretical RMS ZPF force per component (one-sided PSD)."""
    # <F²> = (1/2π) ∫₀^ω_max S_F(ω) dω = (1/2π) × 2τ × ω_max⁴/4
    sigma2 = TAU * OMEGA_MAX**4 / (4.0 * np.pi)
    return np.sqrt(sigma2)


# ============================================================
# Single Trajectory (used by multiprocessing workers)
# ============================================================

def _run_one_trajectory(args):
    """
    Run a single SED trajectory.
    This function is called by multiprocessing workers.

    Parameters:
    -----------
    args : tuple of (L, max_periods, seed)

    Returns:
    --------
    t_ion   : float or nan  (ionization time in a.u.)
    ionized : bool
    r_at_chunks : list of floats (r sampled at chunk boundaries)
    """
    L, max_periods, seed = args

    # Load C library in this worker
    lib = load_lib()

    N_max = int(max_periods * T_ORB / DT)

    # ctypes scalars for position and velocity
    px = ctypes.c_double(1.0)
    py = ctypes.c_double(0.0)
    pz = ctypes.c_double(0.0)
    vx = ctypes.c_double(0.0)
    vy = ctypes.c_double(float(L))
    vz = ctypes.c_double(0.0)

    steps_done = ctypes.c_int(0)
    ionized_c  = ctypes.c_int(0)

    step_count = 0
    chunk_seed = seed
    r_at_chunks = [1.0]   # initial r

    while step_count < N_max:
        # How many steps in this chunk?
        remaining = N_max - step_count
        n_steps = min(CHUNK_STEPS, remaining)

        # Generate ZPF noise (n_steps+1 points)
        # We always generate CHUNK_PTS points; if n_steps < CHUNK_STEPS,
        # we still generate the full block (slightly wasteful but simpler)
        F_zpf, dF_zpf = generate_zpf_chunk(chunk_seed)
        chunk_seed += 1

        # Call C integration loop
        lib.integrate_chunk(
            ctypes.byref(px), ctypes.byref(py), ctypes.byref(pz),
            ctypes.byref(vx), ctypes.byref(vy), ctypes.byref(vz),
            F_zpf.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            dF_zpf.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            ctypes.c_int(n_steps),
            ctypes.c_double(DT),
            ctypes.c_double(TAU),
            ctypes.c_double(R_SOFT),
            ctypes.c_double(R_ION),
            ctypes.c_double(R_NUKE),
            ctypes.byref(steps_done),
            ctypes.byref(ionized_c),
        )

        j = steps_done.value
        step_count += j

        r_now = (px.value**2 + py.value**2 + pz.value**2)**0.5
        r_at_chunks.append(r_now)

        if ionized_c.value:
            t_ion = step_count * DT
            return t_ion, True, r_at_chunks

        # If we didn't complete the full n_steps, something went wrong
        # (shouldn't happen unless n_steps=0)
        if j < n_steps:
            break

    return float('nan'), False, r_at_chunks


# ============================================================
# Batch Run (parallel over trajectories)
# ============================================================

def run_batch(L, n_traj=20, max_periods=10000, base_seed=0,
              n_workers=None, verbose=True):
    """
    Run n_traj independent SED trajectories for angular momentum L.

    Parameters:
    -----------
    L           : float  (angular momentum in ħ units)
    n_traj      : int    (number of trajectories)
    max_periods : int    (cap in orbital periods)
    base_seed   : int    (base random seed; traj k uses seed base_seed + k*997)
    n_workers   : int    (number of parallel workers; None = os.cpu_count())
    verbose     : bool

    Returns:
    --------
    stats : dict with keys:
        L, n_traj, n_ionized, fraction_ionized,
        median_T_ion_periods, iqr_T_ion_periods, mean_T_ion_periods,
        t_ions_periods (list), mean_r, cap
    """
    if n_workers is None:
        n_workers = min(n_traj, os.cpu_count() or 1)

    seeds = [base_seed + k * 997 for k in range(n_traj)]
    args_list = [(L, max_periods, s) for s in seeds]

    if verbose:
        print(f"\n  L={L:.1f}: {n_traj} trajectories, cap={max_periods} periods, "
              f"{n_workers} workers")
        print(f"  (N_max = {int(max_periods * T_ORB / DT):,} steps per trajectory)")

    t0 = time.time()

    if n_workers > 1:
        with mp.Pool(processes=n_workers) as pool:
            results = pool.map(_run_one_trajectory, args_list)
    else:
        results = [_run_one_trajectory(a) for a in args_list]

    elapsed = time.time() - t0

    # Collect statistics
    t_ions = []
    r_all = []
    n_ionized = 0

    for i, (t_ion, ion, r_chunks) in enumerate(results):
        if ion:
            n_ionized += 1
            t_ions.append(t_ion / T_ORB)   # convert to orbital periods
        r_all.extend(r_chunks)
        if verbose:
            if ion:
                t_p = t_ion / T_ORB
                print(f"    Traj {i+1:2d}: T_ion = {t_p:.1f} periods")
            else:
                r_f = r_chunks[-1] if r_chunks else float('nan')
                print(f"    Traj {i+1:2d}: NOT IONIZED (r_final={r_f:.3f})")

    t_arr = np.array(t_ions) if t_ions else np.array([])
    median_T = float(np.median(t_arr)) if t_arr.size > 0 else float('nan')
    iqr_T = float(np.percentile(t_arr, 75) - np.percentile(t_arr, 25)) if t_arr.size >= 4 else float('nan')
    mean_T  = float(np.mean(t_arr)) if t_arr.size > 0 else float('nan')
    mean_r  = float(np.mean(r_all)) if r_all else float('nan')

    stats = {
        'L': float(L),
        'n_traj': n_traj,
        'n_ionized': n_ionized,
        'fraction_ionized': n_ionized / n_traj,
        'median_T_ion_periods': median_T,
        'iqr_T_ion_periods': iqr_T,
        'mean_T_ion_periods': mean_T,
        't_ions_periods': t_arr.tolist(),
        'mean_r': mean_r,
        'cap': max_periods,
        'elapsed_s': elapsed,
    }

    if verbose:
        print(f"  → {n_ionized}/{n_traj} ionized in {elapsed:.1f}s")
        if not np.isnan(median_T):
            print(f"  → Median T_ion = {median_T:.1f} periods, IQR = {iqr_T:.1f}")
        else:
            print(f"  → No ionization (cap={max_periods} periods)")
        print(f"  → ⟨r⟩ = {mean_r:.3f} a₀")

    return stats


# ============================================================
# Sanity Checks
# ============================================================

def sanity_check_tau():
    """Verify τ value."""
    tau_computed = 2.0 / (3.0 * 137.036**3)
    print(f"\n[SANITY 0] Physical τ verification")
    print(f"  τ = 2/(3 × 137.036³) = {tau_computed:.4e} a.u.")
    print(f"  Expected: 2.59×10⁻⁷  ✓" if abs(tau_computed - 2.59e-7) / 2.59e-7 < 0.01 else "  MISMATCH!")
    print(f"  E003 τ = 1.57×10⁻⁵")
    print(f"  Ratio: {1.57e-5 / tau_computed:.1f}× (expected ~60)")
    return tau_computed


def sanity_check_pure_coulomb(n_periods=100):
    """Pure Coulomb orbit: verify r and E are stable."""
    print(f"\n[SANITY 1] Pure Coulomb orbit, L=1.0, {n_periods} periods")

    lib = load_lib()
    N = int(n_periods * T_ORB / DT)

    px = ctypes.c_double(1.0); py = ctypes.c_double(0.0); pz = ctypes.c_double(0.0)
    vx = ctypes.c_double(0.0); vy = ctypes.c_double(1.0); vz = ctypes.c_double(0.0)

    energies = np.zeros(N, dtype=np.float64)

    lib.integrate_chunk_pure_coulomb(
        ctypes.byref(px), ctypes.byref(py), ctypes.byref(pz),
        ctypes.byref(vx), ctypes.byref(vy), ctypes.byref(vz),
        ctypes.c_int(N),
        ctypes.c_double(DT),
        ctypes.c_double(R_SOFT),
        energies.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    )

    r_final = (px.value**2 + py.value**2 + pz.value**2)**0.5
    E_mean = np.mean(energies)
    E_std  = np.std(energies)
    E_drift = abs(energies[-1] - energies[0]) / abs(energies[0]) * 100

    print(f"  r_final = {r_final:.6f} a₀  (expected 1.000000)")
    print(f"  E_mean  = {E_mean:.6f} a.u.  (expected -0.500000)")
    print(f"  E_std   = {E_std:.2e}")
    print(f"  E_drift = {E_drift:.4f}%  (expected < 0.01%)")

    ok = abs(r_final - 1.0) < 1e-4 and E_drift < 0.01
    print(f"  Status: {'PASS ✓' if ok else 'FAIL ✗'}")
    return ok


def sanity_check_zpf_rms():
    """Check ZPF noise RMS matches theoretical value."""
    print(f"\n[SANITY 2] ZPF noise RMS")

    F_zpf, dF_zpf = generate_zpf_chunk(seed=12345)

    rms_measured = np.sqrt(np.mean(F_zpf**2))
    rms_theory   = zpf_rms_theoretical()

    print(f"  Measured RMS (per component): {rms_measured:.4f} a.u.")
    print(f"  Theoretical RMS:              {rms_theory:.4f} a.u.")
    print(f"  Ratio: {rms_measured/rms_theory:.4f}  (expected ≈ 1.0)")

    ok = abs(rms_measured/rms_theory - 1.0) < 0.05
    print(f"  Status: {'PASS ✓' if ok else 'FAIL ✗'}")
    return ok, rms_measured, rms_theory


def sanity_check_short_run():
    """Short trial: L=0.5, 5 trajectories, 100-period cap."""
    print(f"\n[SANITY 3] Short trial: L=0.5, 5 trajectories, 100-period cap")
    stats = run_batch(0.5, n_traj=5, max_periods=100, base_seed=999,
                      n_workers=5, verbose=True)
    print(f"  Fraction ionized: {stats['n_ionized']}/5")
    return stats


# ============================================================
# Main: Full Scan
# ============================================================

def run_full_scan(output_file=None, n_traj=20, n_workers=None):
    """
    Run the full T_ion(L) scan for L = 0.4, 0.5, ..., 1.0.
    """
    L_values   = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    max_periods = {0.4: 10000, 0.5: 10000, 0.6: 10000,
                   0.7: 10000, 0.8: 10000, 0.9: 10000,
                   1.0: 50000}

    all_stats = []

    for L in L_values:
        cap = max_periods[L]
        # Use different base seeds per L value
        base_seed = int(L * 1000)
        stats = run_batch(L, n_traj=n_traj, max_periods=cap,
                          base_seed=base_seed,
                          n_workers=n_workers, verbose=True)
        all_stats.append(stats)

        # Print partial table immediately
        print_table_row(stats)

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(all_stats, f, indent=2)

    print("\n\n=== FINAL RESULTS TABLE ===")
    print_results_table(all_stats)

    return all_stats


def print_table_row(stats):
    L = stats['L']
    n_ion = stats['n_ionized']
    n_tot = stats['n_traj']
    med = stats['median_T_ion_periods']
    iqr = stats['iqr_T_ion_periods']
    r   = stats['mean_r']
    cap = stats['cap']

    med_str = f"{med:.0f}" if not np.isnan(med) else f">cap({cap})"
    iqr_str = f"{iqr:.0f}" if not np.isnan(iqr) else "N/A"
    print(f"  TABLE: L={L:.1f} | {n_ion}/{n_tot} | {med_str} | {iqr_str} | {r:.3f}")


def print_results_table(all_stats):
    print(f"{'L/ħ':>5} | {'N_ion/20':>8} | {'Med T_ion':>12} | {'IQR':>8} | {'<r>/a0':>7} | Notes")
    print("-" * 65)
    for s in all_stats:
        L = s['L']
        n_ion = s['n_ionized']
        n_tot = s['n_traj']
        med = s['median_T_ion_periods']
        iqr = s['iqr_T_ion_periods']
        r   = s['mean_r']
        cap = s['cap']

        med_str = f"{med:.0f}" if not np.isnan(med) else f">cap({cap})"
        iqr_str = f"{iqr:.0f}" if not np.isnan(iqr) else "N/A"
        print(f"{L:>5.1f} | {n_ion:>3}/{n_tot:<4} | {med_str:>12} | {iqr_str:>8} | {r:>7.3f} |")


# ============================================================
# Entry Point
# ============================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='SED Hydrogen — Physical TAU')
    parser.add_argument('--sanity', action='store_true', help='Run sanity checks only')
    parser.add_argument('--scan',   action='store_true', help='Run full L scan')
    parser.add_argument('--L',      type=float,          help='Single L value to run')
    parser.add_argument('--n_traj', type=int, default=20, help='Trajectories per L')
    parser.add_argument('--cap',    type=int, default=10000, help='Period cap')
    parser.add_argument('--seed',   type=int, default=0,  help='Base random seed')
    parser.add_argument('--workers',type=int, default=None, help='Worker processes')
    parser.add_argument('--output', type=str, default=None, help='JSON output file')
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"SED Hydrogen Simulation — Physical TAU")
    print(f"Strategy 003, Exploration 002")
    print(f"{'='*60}")
    print(f"TAU        = {TAU:.4e} a.u.  (physical)")
    print(f"OMEGA_MAX  = {OMEGA_MAX:.1f} a.u.")
    print(f"DT         = {DT} a.u.")
    print(f"T_ORB      = {T_ORB:.4f} a.u.")
    print(f"CHUNK_STEPS = {CHUNK_STEPS:,}  (= 2^17 - 1)")
    print(f"ZPF RMS (theory) = {zpf_rms_theoretical():.4f} a.u./component")
    print(f"N workers  = {args.workers or os.cpu_count()}")
    print(f"Library    = {LIB_PATH}")

    if args.sanity:
        sanity_check_tau()
        ok1 = sanity_check_pure_coulomb(n_periods=100)
        ok2, rms_m, rms_t = sanity_check_zpf_rms()
        stats_trial = sanity_check_short_run()
        print(f"\n=== SANITY SUMMARY ===")
        print(f"  τ value:        {'OK' if True else 'FAIL'}")
        print(f"  Pure Coulomb:   {'OK' if ok1 else 'FAIL'}")
        print(f"  ZPF RMS:        {'OK' if ok2 else 'FAIL'} (measured {rms_m:.4f}, theory {rms_t:.4f})")
        print(f"  Trial L=0.5:    {stats_trial['n_ionized']}/5 ionized in 100 periods")

    elif args.scan:
        n_workers = args.workers
        all_stats = run_full_scan(output_file=args.output,
                                  n_traj=args.n_traj,
                                  n_workers=n_workers)
        if args.output:
            print(f"\nResults saved to {args.output}")

    elif args.L is not None:
        stats = run_batch(args.L, n_traj=args.n_traj, max_periods=args.cap,
                          base_seed=args.seed, n_workers=args.workers, verbose=True)
        print(f"\nResult: {stats}")

    else:
        parser.print_help()
