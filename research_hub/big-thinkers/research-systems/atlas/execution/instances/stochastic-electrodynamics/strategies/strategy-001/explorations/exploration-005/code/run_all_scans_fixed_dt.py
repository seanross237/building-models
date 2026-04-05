"""
UV-Cutoff Scan: ALD Anharmonic SED Simulation — FIXED dt=0.05
Modified from exploration-004/code/ald_simulate.py

Uses FIXED dt=0.05 for all cases (same as E004, guarantees stability).
The UV cutoff omega_max is controlled by zeroing modes above omega_max in the noise PSD.

Runs sequentially:
  Part 1a: Baselines (beta=0), omega_max in {10, 20, 30}, tau=0.01
  Part 1b: beta=1.0, omega_max in {10, 20, 30}, tau=0.01
  Part 2:  beta=0.1, omega_max in {10, 20, 30}, tau=0.01
  Part 3:  beta=0 and beta=1.0, tau in {0.005, 0.002}, omega_max=10

Saves all results to scan_results_fixed_dt.json

NOTE: E004 baseline (beta=0, omega_max=10, tau=0.01, dt=0.05):
  var_x = 0.5157 ± 0.0074  (baseline offset = +0.0157 above QM=0.5)
"""

import numpy as np
import json
import os
import sys
import time
import math

# ============================================================
# Fixed parameters (same as E004)
# ============================================================
OMEGA0 = 1.0
DT = 0.05
T_TOTAL = 20000.0
N_T = int(T_TOTAL / DT)       # = 400,000
N_EQ = N_T // 2               # = 200,000 (discard for equilibration)
SAMPLE_STRIDE = 4000           # = 200 time units (>> corr time ~100 @ tau=0.01)

SAMPLE_STEPS_ARR = np.arange(N_EQ, N_T, SAMPLE_STRIDE)
IS_SAMPLE_TEMPLATE = np.zeros(N_T, dtype=bool)
IS_SAMPLE_TEMPLATE[SAMPLE_STEPS_ARR] = True
N_SAMP = int(np.sum(IS_SAMPLE_TEMPLATE))

BATCH_SIZE = 50
N_ENSEMBLE = 200

# ============================================================
# QM reference values (from E003 matrix diagonalization)
# ============================================================
QM_REF = {
    0.0:  {'var_x': 0.5000, 'x4': 0.7500, 'PE': 0.2500},
    0.01: {'var_x': 0.4862, 'x4': 0.7029, 'PE': 0.2501},
    0.05: {'var_x': 0.4458, 'x4': 0.5788, 'PE': 0.2519},
    0.1:  {'var_x': 0.4125, 'x4': 0.4887, 'PE': 0.2551},
    0.2:  {'var_x': 0.3700, 'x4': 0.3874, 'PE': 0.2625},
    0.5:  {'var_x': 0.3058, 'x4': 0.2602, 'PE': 0.2830},
    1.0:  {'var_x': 0.2571, 'x4': 0.1822, 'PE': 0.3108},
}


def generate_ald_noise_batch(B, tau, omega_max, rng):
    """
    Generate B realizations of F_zpf(t) and tau*F'_zpf(t).
    Uses fixed global DT, N_T.
    Noise formula: A_k = sqrt(S_F_one(omega_k) * N_T / (2*DT))
    S_F_one(omega) = 2*tau*omega^3, zeroed for omega > omega_max.
    """
    freqs = np.fft.rfftfreq(N_T, d=DT)
    omega = 2.0 * np.pi * freqs
    S_F_one = 2.0 * tau * omega**3
    S_F_one[omega > omega_max] = 0.0
    S_F_one[0] = 0.0
    A = np.sqrt(S_F_one * N_T / (2.0 * DT))

    n_rfft = len(freqs)
    xi_real = rng.standard_normal((B, n_rfft))
    xi_imag = rng.standard_normal((B, n_rfft))
    F_hat = A[None, :] * (xi_real + 1j * xi_imag) / np.sqrt(2.0)
    F_hat[:, 0] = 0.0
    if N_T % 2 == 0:
        F_hat[:, -1] = F_hat[:, -1].real

    F_noise = np.fft.irfft(F_hat, n=N_T, axis=1)

    dF_hat = (1j * tau) * omega[None, :] * F_hat
    if N_T % 2 == 0:
        dF_hat[:, -1] = 0.0
    F_prime = np.fft.irfft(dF_hat, n=N_T, axis=1)

    return F_noise, F_prime


def integrate_batch_ald(x0, v0, F_noise, F_prime, beta, tau):
    """
    Integrate LL equation for B trajectories (Euler-Cromer).
    x'' = -x - 4*beta*x^3 - tau*(1 + 12*beta*x^2)*x' + F_noise + F_prime
    Uses fixed global DT, IS_SAMPLE_TEMPLATE, N_SAMP.
    """
    x = x0.copy()
    v = v0.copy()
    positions = np.zeros((len(x0), N_SAMP))
    sample_idx = 0
    F_T = F_noise.T
    Fp_T = F_prime.T

    for k in range(N_T):
        Gamma_eff = tau * (1.0 + 12.0 * beta * x * x)
        a = (-x
             - 4.0 * beta * x * x * x
             - Gamma_eff * v
             + F_T[k]
             + Fp_T[k])
        v += a * DT
        x += v * DT
        if IS_SAMPLE_TEMPLATE[k]:
            positions[:, sample_idx] = x
            sample_idx += 1

    return positions


def run_case(beta, omega_max, tau, n_ensemble=N_ENSEMBLE,
             batch_size=BATCH_SIZE, seed=42, verbose=True):
    """Run one (beta, omega_max, tau) case and return stats dict."""
    if verbose:
        print(f"\n--- Case: beta={beta}, omega_max={omega_max}, tau={tau} ---")
        print(f"    dt={DT}, N_t={N_T}, n_samp/traj={N_SAMP}")

    rng = np.random.default_rng(seed)
    n_batches = (n_ensemble + batch_size - 1) // batch_size
    batch_list = [min(batch_size, n_ensemble - i*batch_size) for i in range(n_batches)]
    batch_list = [b for b in batch_list if b > 0]

    all_positions = []
    t_start = time.time()
    n_unstable = 0

    for b_idx, B in enumerate(batch_list):
        F_noise, F_prime = generate_ald_noise_batch(B, tau, omega_max, rng)
        positions = integrate_batch_ald(
            np.zeros(B), np.zeros(B), F_noise, F_prime, beta, tau
        )
        max_pos = float(np.nanmax(np.abs(positions)))
        has_nan = bool(np.any(np.isnan(positions)))
        if has_pos_prob := (max_pos > 100.0 or has_nan):
            n_unstable += B
            if verbose:
                print(f"  WARNING: batch {b_idx+1} unstable! max|x|={max_pos:.1f} nan={has_nan}")
        del F_noise, F_prime
        all_positions.append(positions)

        if verbose:
            n_done = sum(batch_list[:b_idx+1])
            elapsed = time.time() - t_start
            max_str = f"{max_pos:.3f}" if not has_nan else "NaN"
            print(f"  Batch {b_idx+1}/{len(batch_list)}: {n_done}/{n_ensemble} traj"
                  f" | max|x|={max_str} | t={elapsed:.1f}s", flush=True)

    all_positions = np.vstack(all_positions)
    x_samples = all_positions.flatten()

    # Exclude NaN trajectories from statistics
    if np.any(np.isnan(x_samples)):
        good_mask = ~np.any(np.isnan(all_positions), axis=1)
        n_good = int(np.sum(good_mask))
        if verbose:
            print(f"  NaN in {n_ensemble-n_good} trajectories; using {n_good}/{n_ensemble}")
        all_positions = all_positions[good_mask]
        x_samples = all_positions.flatten()
    else:
        n_good = n_ensemble

    if n_good == 0:
        if verbose:
            print("  ALL TRAJECTORIES UNSTABLE!")
        qm = QM_REF.get(beta, None)
        return {
            'beta': beta, 'omega_max': omega_max, 'tau': tau,
            'dt': DT, 'N_t': N_T, 'n_samp_per_traj': N_SAMP,
            'var_x_ald': None, 'var_x_qm': qm['var_x'] if qm else None,
            'std_var': None, 'frac_diff': None, 'nsig': None,
            'mean_x': None, 'x4_ald': None, 'n_unstable': n_unstable,
            'n_good': 0, 'n_samples': 0, 'elapsed_s': time.time() - t_start,
        }

    var_x = float(np.var(x_samples))
    mean_x = float(np.mean(x_samples))
    x4_mean = float(np.mean(x_samples**4))
    var_per_traj = np.var(all_positions, axis=1)
    std_var = float(np.std(var_per_traj) / np.sqrt(n_good))

    qm = QM_REF.get(beta, None)
    qm_var_x = qm['var_x'] if qm else float('nan')
    frac_diff = (var_x - qm_var_x) / qm_var_x if qm else float('nan')
    nsig = frac_diff * qm_var_x / std_var if qm and std_var > 0 else float('nan')
    elapsed_total = time.time() - t_start

    if verbose:
        print(f"  var_x_ALD = {var_x:.6f} ± {std_var:.6f}")
        print(f"  var_x_QM  = {qm_var_x:.6f}")
        print(f"  frac_diff = {frac_diff:+.4f} ({frac_diff*100:+.2f}%)")
        print(f"  nsig      = {nsig:+.1f}")
        print(f"  n_unstable= {n_unstable}/{n_ensemble}")
        print(f"  elapsed   = {elapsed_total:.1f}s")

    return {
        'beta': beta,
        'omega_max': omega_max,
        'tau': tau,
        'dt': DT,
        'N_t': N_T,
        'n_samp_per_traj': N_SAMP,
        'var_x_ald': var_x,
        'var_x_qm': float(qm_var_x),
        'std_var': std_var,
        'frac_diff': float(frac_diff) if not np.isnan(frac_diff) else None,
        'nsig': float(nsig) if not np.isnan(nsig) else None,
        'mean_x': mean_x,
        'x4_ald': x4_mean,
        'n_unstable': n_unstable,
        'n_good': n_good,
        'n_samples': len(x_samples),
        'elapsed_s': elapsed_total,
    }


# ============================================================
# Main: run all cases
# ============================================================
if __name__ == '__main__':
    code_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(code_dir, 'scan_results_fixed_dt.json')

    existing = {}
    if os.path.exists(save_path):
        with open(save_path) as f:
            existing = json.load(f)
        print(f"Loaded {len(existing)} existing results from {save_path}")

    def run_and_save(beta, omega_max, tau):
        key = f"beta{beta}_omax{omega_max}_tau{tau}"
        if key in existing:
            print(f"  SKIP (already done): {key}")
            return
        result = run_case(beta, omega_max, tau)
        existing[key] = result
        with open(save_path, 'w') as f:
            json.dump(existing, f, indent=2)
        print(f"  Saved: {key}")

    print("=" * 70)
    print("UV-CUTOFF SCAN — Exploration 005 (Fixed dt=0.05)")
    print("=" * 70)

    # ---- PART 1a: Baselines beta=0, omega_max scan ----
    print("\n[PART 1a] Baselines: beta=0, tau=0.01, omega_max in {10, 20, 30}")
    for om in [10, 20, 30]:
        run_and_save(0.0, om, 0.01)

    # ---- PART 1b: beta=1.0, omega_max scan ----
    print("\n[PART 1b] beta=1.0, tau=0.01, omega_max in {10, 20, 30}")
    for om in [10, 20, 30]:
        run_and_save(1.0, om, 0.01)

    # ---- PART 2: beta=0.1, omega_max scan ----
    print("\n[PART 2] beta=0.1, tau=0.01, omega_max in {10, 20, 30}")
    for om in [10, 20, 30]:
        run_and_save(0.1, om, 0.01)

    # ---- PART 3: tau scan ----
    print("\n[PART 3] tau scan: omega_max=10, tau in {0.01, 0.005, 0.002}")
    for tau_val in [0.005, 0.002]:
        run_and_save(0.0, 10, tau_val)
        run_and_save(1.0, 10, tau_val)

    # ---- Summary ----
    print("\n" + "=" * 70)
    print("FULL SUMMARY")
    print("=" * 70)
    print(f"{'Key':<38} {'var_ALD':>10} {'var_QM':>10} {'frac_diff':>10} {'nsig':>7}")
    print("-" * 80)
    for key, r in sorted(existing.items()):
        frac = r.get('frac_diff')
        nsig = r.get('nsig')
        vald = r.get('var_x_ald')
        vqm = r.get('var_x_qm', float('nan'))
        frac_str = f"{frac:+.4f}" if frac is not None else "  FAIL"
        nsig_str = f"{nsig:+.1f}" if nsig is not None else "  FAIL"
        vald_str = f"{vald:.6f}" if vald is not None else "  FAIL  "
        vqm_str = f"{vqm:.6f}" if vqm is not None else "    N/A   "
        print(f"{key:<38} {vald_str:>10} {vqm_str:>10} {frac_str:>10} {nsig_str:>7}")

    print(f"\nAll results saved to: {save_path}")
