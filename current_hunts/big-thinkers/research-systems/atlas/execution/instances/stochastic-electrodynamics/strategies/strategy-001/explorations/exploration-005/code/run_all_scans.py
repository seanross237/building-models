"""
Run all UV-cutoff and tau scans for Exploration 005.

Runs sequentially:
  Part 1a: Baselines (beta=0), omega_max in {10, 20, 30}, tau=0.01
  Part 1b: beta=1.0, omega_max in {10, 20, 30}, tau=0.01
  Part 2:  beta=0.1, omega_max in {10, 20}, tau=0.01
  Part 3:  beta=0 and beta=1.0, tau in {0.005, 0.002}, omega_max=10
  (tau=0.01, omega_max=10 is covered in Part 1a/1b)

Saves all results to scan_results.json
"""

import numpy as np
import json
import os
import sys
import time
import math

# ============================================================
# Shared parameters
# ============================================================
OMEGA0 = 1.0
T_TOTAL = 20000.0
BATCH_SIZE = 50
N_ENSEMBLE = 200

QM_REF = {
    0.0:  {'var_x': 0.5000, 'x4': 0.7500, 'PE': 0.2500},
    0.01: {'var_x': 0.4862, 'x4': 0.7029, 'PE': 0.2501},
    0.05: {'var_x': 0.4458, 'x4': 0.5788, 'PE': 0.2519},
    0.1:  {'var_x': 0.4125, 'x4': 0.4887, 'PE': 0.2551},
    0.2:  {'var_x': 0.3700, 'x4': 0.3874, 'PE': 0.2625},
    0.5:  {'var_x': 0.3058, 'x4': 0.2602, 'PE': 0.2830},
    1.0:  {'var_x': 0.2571, 'x4': 0.1822, 'PE': 0.3108},
}


def generate_ald_noise_batch(B, N_t, dt, tau, omega_max, rng):
    freqs = np.fft.rfftfreq(N_t, d=dt)
    omega = 2.0 * np.pi * freqs
    S_F_one = 2.0 * tau * omega**3
    S_F_one[omega > omega_max] = 0.0
    S_F_one[0] = 0.0
    A = np.sqrt(S_F_one * N_t / (2.0 * dt))

    n_rfft = len(freqs)
    xi_real = rng.standard_normal((B, n_rfft))
    xi_imag = rng.standard_normal((B, n_rfft))
    F_hat = A[None, :] * (xi_real + 1j * xi_imag) / np.sqrt(2.0)
    F_hat[:, 0] = 0.0
    if N_t % 2 == 0:
        F_hat[:, -1] = F_hat[:, -1].real

    F_noise = np.fft.irfft(F_hat, n=N_t, axis=1)

    dF_hat = (1j * tau) * omega[None, :] * F_hat
    if N_t % 2 == 0:
        dF_hat[:, -1] = 0.0
    F_prime = np.fft.irfft(dF_hat, n=N_t, axis=1)

    return F_noise, F_prime


def integrate_batch_ald(x0, v0, F_noise, F_prime, beta,
                        omega0, tau, dt, is_sample, n_samp):
    x = x0.copy()
    v = v0.copy()
    positions = np.zeros((len(x0), n_samp))
    sample_idx = 0
    F_T = F_noise.T
    Fp_T = F_prime.T
    omega0_sq = omega0**2

    for k in range(F_noise.shape[1]):
        Gamma_eff = tau * (omega0_sq + 12.0 * beta * x * x)
        a = (-omega0_sq * x
             - 4.0 * beta * x * x * x
             - Gamma_eff * v
             + F_T[k]
             + Fp_T[k])
        v += a * dt
        x += v * dt
        if is_sample[k]:
            positions[:, sample_idx] = x
            sample_idx += 1

    return positions


def run_case(beta, omega_max, tau, n_ensemble=N_ENSEMBLE,
             batch_size=BATCH_SIZE, seed=42, verbose=True):
    dt = math.pi / omega_max
    N_t = int(T_TOTAL / dt)
    N_eq = N_t // 2
    sample_stride = max(1, int(200.0 / dt))
    sample_steps_arr = np.arange(N_eq, N_t, sample_stride)
    is_sample = np.zeros(N_t, dtype=bool)
    is_sample[sample_steps_arr] = True
    n_samp = int(np.sum(is_sample))

    if verbose:
        print(f"\n--- Case: beta={beta}, omega_max={omega_max}, tau={tau} ---")
        print(f"    dt={dt:.5f}, N_t={N_t}, N_eq={N_eq}, stride={sample_stride}, n_samp/traj={n_samp}")

    rng = np.random.default_rng(seed)
    n_batches = (n_ensemble + batch_size - 1) // batch_size
    batch_list = [min(batch_size, n_ensemble - i*batch_size) for i in range(n_batches)]
    batch_list = [b for b in batch_list if b > 0]

    all_positions = []
    t_start = time.time()
    n_unstable = 0

    for b_idx, B in enumerate(batch_list):
        F_noise, F_prime = generate_ald_noise_batch(B, N_t, dt, tau, omega_max, rng)
        positions = integrate_batch_ald(
            np.zeros(B), np.zeros(B), F_noise, F_prime, beta,
            omega0=OMEGA0, tau=tau, dt=dt,
            is_sample=is_sample, n_samp=n_samp
        )
        max_pos = np.max(np.abs(positions))
        if max_pos > 100.0:
            n_unstable += B
            if verbose:
                print(f"  WARNING: batch {b_idx+1} runaway! max|x|={max_pos:.1f}")
        del F_noise, F_prime
        all_positions.append(positions)

        if verbose:
            n_done = sum(batch_list[:b_idx+1])
            elapsed = time.time() - t_start
            print(f"  Batch {b_idx+1}/{len(batch_list)}: {n_done}/{n_ensemble} traj"
                  f" | max|x|={max_pos:.3f} | t={elapsed:.1f}s", flush=True)

    all_positions = np.vstack(all_positions)
    x_samples = all_positions.flatten()

    var_x = float(np.var(x_samples))
    mean_x = float(np.mean(x_samples))
    x4_mean = float(np.mean(x_samples**4))
    var_per_traj = np.var(all_positions, axis=1)
    std_var = float(np.std(var_per_traj) / np.sqrt(n_ensemble))
    elapsed_total = time.time() - t_start

    qm = QM_REF.get(beta, None)
    qm_var_x = qm['var_x'] if qm else float('nan')
    frac_diff = (var_x - qm_var_x) / qm_var_x if qm else float('nan')
    nsig = frac_diff * qm_var_x / std_var if qm and std_var > 0 else float('nan')

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
        'dt': dt,
        'N_t': N_t,
        'n_samp_per_traj': n_samp,
        'var_x_ald': var_x,
        'var_x_qm': qm_var_x,
        'std_var': std_var,
        'frac_diff': float(frac_diff) if not np.isnan(frac_diff) else None,
        'nsig': float(nsig) if not np.isnan(nsig) else None,
        'mean_x': mean_x,
        'x4_ald': x4_mean,
        'n_unstable': n_unstable,
        'n_samples': len(x_samples),
        'elapsed_s': elapsed_total,
    }


# ============================================================
# Main: run all cases
# ============================================================
if __name__ == '__main__':
    code_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(code_dir, 'scan_results.json')

    # Load existing results (allows resuming)
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

    print("=" * 60)
    print("UV-CUTOFF SCAN — Exploration 005")
    print("=" * 60)

    # ---- PART 1a: Baselines beta=0, omega_max scan ----
    print("\n[PART 1a] Baselines: beta=0, tau=0.01, omega_max in {10, 20, 30}")
    for om in [10, 20, 30]:
        run_and_save(0.0, om, 0.01)

    # ---- PART 1b: beta=1.0, omega_max scan ----
    print("\n[PART 1b] beta=1.0, tau=0.01, omega_max in {10, 20, 30}")
    for om in [10, 20, 30]:
        run_and_save(1.0, om, 0.01)

    # ---- PART 2: beta=0.1, omega_max scan ----
    print("\n[PART 2] Baseline beta=0.1")
    run_and_save(0.1, 10, 0.01)
    run_and_save(0.1, 20, 0.01)
    # Also get beta=0.1 at omega_max=30 as bonus
    run_and_save(0.1, 30, 0.01)

    # ---- PART 3: tau scan at beta=0 and beta=1.0, omega_max=10 ----
    print("\n[PART 3] tau scan: beta in {0, 1.0}, omega_max=10, tau in {0.01, 0.005, 0.002}")
    # tau=0.01 already done above
    for tau in [0.005, 0.002]:
        run_and_save(0.0, 10, tau)
        run_and_save(1.0, 10, tau)

    # ---- Summary ----
    print("\n" + "=" * 60)
    print("SUMMARY OF ALL RESULTS")
    print("=" * 60)
    print(f"{'Key':<35} {'var_ALD':>10} {'var_QM':>10} {'frac_diff':>12} {'nsig':>8}")
    print("-" * 80)
    for key, r in sorted(existing.items()):
        frac = r.get('frac_diff')
        nsig = r.get('nsig')
        frac_str = f"{frac:+.4f}" if frac is not None else "  N/A"
        nsig_str = f"{nsig:+.1f}" if nsig is not None else " N/A"
        print(f"{key:<35} {r['var_x_ald']:10.6f} {r['var_x_qm']:10.6f}"
              f" {frac_str:>12} {nsig_str:>8}")

    print(f"\nAll results saved to: {save_path}")
