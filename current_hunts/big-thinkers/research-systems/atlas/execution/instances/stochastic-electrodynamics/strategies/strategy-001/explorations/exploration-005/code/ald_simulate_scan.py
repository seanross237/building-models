"""
UV-Cutoff Scan: ALD Anharmonic SED Simulation
Modified from exploration-004/code/ald_simulate.py

Accepts command-line args:
    python ald_simulate_scan.py <beta> <omega_max> <tau>

Changes from E004:
  - dt = pi/omega_max  (Nyquist limit for each cutoff)
  - N_t = int(T_TOTAL / dt)
  - SAMPLE_STRIDE = int(200.0 / dt)  — keep 200-time-unit physical spacing
  - omega_max and tau are command-line args

Noise formula (VERIFIED in E003/E004):
    A_k = sqrt(S_F_one(omega_k) * N_t / (2*dt))
    S_F_one(omega) = 2*tau*omega^3

Author: Math Explorer (Exploration 005)
"""

import numpy as np
import json
import os
import sys
import time
import math

# ============================================================
# Parse command-line args
# ============================================================
if len(sys.argv) < 4:
    print("Usage: python ald_simulate_scan.py <beta> <omega_max> <tau>")
    print("  e.g.: python ald_simulate_scan.py 1.0 10 0.01")
    sys.exit(1)

BETA = float(sys.argv[1])
OMEGA_MAX = float(sys.argv[2])
TAU = float(sys.argv[3])

# ============================================================
# Derived parameters
# ============================================================
OMEGA0 = 1.0
DT = math.pi / OMEGA_MAX          # Nyquist limit: dt = pi / omega_max
T_TOTAL = 20000.0
N_T = int(T_TOTAL / DT)
N_EQ = N_T // 2                    # discard first half for equilibration

# Sample every 200 time units >> tau_corr (physical spacing preserved)
SAMPLE_STRIDE = max(1, int(200.0 / DT))
SAMPLE_STEPS_ARR = np.arange(N_EQ, N_T, SAMPLE_STRIDE)
IS_SAMPLE = np.zeros(N_T, dtype=bool)
IS_SAMPLE[SAMPLE_STEPS_ARR] = True
N_SAMPLES_PER_TRAJ = int(np.sum(IS_SAMPLE))

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


def generate_ald_noise_batch(B, N_t, dt, tau, omega_max, rng):
    """
    Generate B realizations of:
      F_noise    = F_zpf(t)           [shape (B, N_t)]
      F_prime    = tau * F'_zpf(t)    [shape (B, N_t)]

    F_zpf has one-sided PSD: S_F_one(omega) = 2*tau*omega^3
    F'_zpf is the time derivative: obtained by multiplying freq components by i*omega.

    Amplitude formula (verified in E003):
        A[n] = sqrt(S_F_one(omega_n) * N_t / (2*dt))
    """
    freqs = np.fft.rfftfreq(N_t, d=dt)
    omega = 2.0 * np.pi * freqs        # shape (n_rfft,)
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
        F_hat[:, -1] = F_hat[:, -1].real  # Nyquist is real for real signal

    # F_zpf in time domain
    F_noise = np.fft.irfft(F_hat, n=N_t, axis=1)

    # tau * F'_zpf: multiply by tau * i*omega in frequency domain
    # Zero out Nyquist to keep output real
    dF_hat = (1j * tau) * omega[None, :] * F_hat
    if N_t % 2 == 0:
        dF_hat[:, -1] = 0.0  # Nyquist -> 0 for real derivative
    F_prime = np.fft.irfft(dF_hat, n=N_t, axis=1)

    return F_noise, F_prime


def integrate_batch_ald(x0, v0, F_noise, F_prime, beta,
                        omega0, tau, dt, is_sample, n_samp):
    """
    Integrate LL equation for B trajectories simultaneously (Euler-Cromer).

    x'' = -omega0^2*x - 4*beta*x^3 - tau*(omega0^2 + 12*beta*x^2)*x'
           + F_noise[k] + F_prime[k]

    F_prime already includes the tau factor.

    Returns positions[B, n_samp] at sampled timesteps.
    """
    x = x0.copy()
    v = v0.copy()
    positions = np.zeros((len(x0), n_samp))
    sample_idx = 0
    F_T = F_noise.T     # (N_t, B) for efficient row access
    Fp_T = F_prime.T    # (N_t, B)
    omega0_sq = omega0**2

    for k in range(F_noise.shape[1]):
        # Position-dependent damping
        Gamma_eff = tau * (omega0_sq + 12.0 * beta * x * x)
        # Acceleration
        a = (-omega0_sq * x
             - 4.0 * beta * x * x * x
             - Gamma_eff * v
             + F_T[k]
             + Fp_T[k])
        # Euler-Cromer (update v first, then x)
        v += a * dt
        x += v * dt
        if is_sample[k]:
            positions[:, sample_idx] = x
            sample_idx += 1

    return positions


def run_ald_simulation(beta, omega_max, tau, n_ensemble=N_ENSEMBLE,
                       batch_size=BATCH_SIZE, seed=42, verbose=True):
    """
    Run full ALD simulation for given beta, omega_max, tau.
    Returns statistics dict.
    """
    dt = math.pi / omega_max
    N_t = int(T_TOTAL / dt)
    N_eq = N_t // 2
    sample_stride = max(1, int(200.0 / dt))
    sample_steps_arr = np.arange(N_eq, N_t, sample_stride)
    is_sample = np.zeros(N_t, dtype=bool)
    is_sample[sample_steps_arr] = True
    n_samp = int(np.sum(is_sample))

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

    all_positions = np.vstack(all_positions)  # (n_ensemble, n_samp)
    x_samples = all_positions.flatten()

    var_x = float(np.var(x_samples))
    mean_x = float(np.mean(x_samples))
    x4_mean = float(np.mean(x_samples**4))
    var_per_traj = np.var(all_positions, axis=1)
    std_var = float(np.std(var_per_traj) / np.sqrt(n_ensemble))

    return {
        'beta': beta, 'omega_max': omega_max, 'tau': tau,
        'dt': dt, 'N_t': N_t, 'n_samp_per_traj': n_samp,
        'n_samples': len(x_samples),
        'var_x': var_x, 'mean_x': mean_x, 'x4_mean': x4_mean,
        'std_var': std_var,
        'n_unstable': n_unstable,
    }


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    code_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(code_dir, 'scan_results.json')

    print(f"=== ALD UV-Cutoff Scan: beta={BETA}, omega_max={OMEGA_MAX}, tau={TAU} ===")
    print(f"  dt={DT:.5f}, T_total={T_TOTAL}, N_t={N_T}")
    print(f"  N_EQ={N_EQ}, SAMPLE_STRIDE={SAMPLE_STRIDE}")
    print(f"  N_samples_per_traj={N_SAMPLES_PER_TRAJ}")
    print(f"  N_ensemble={N_ENSEMBLE}, batch_size={BATCH_SIZE}")
    print(f"  Total samples={N_ENSEMBLE * N_SAMPLES_PER_TRAJ}")
    print()

    qm = QM_REF.get(BETA, None)
    if qm:
        print(f"QM reference:  var_x = {qm['var_x']:.4f}")
    print()

    t0 = time.time()
    result = run_ald_simulation(BETA, OMEGA_MAX, TAU, verbose=True)
    elapsed = time.time() - t0

    var_x_ald = result['var_x']
    qm_var_x = qm['var_x'] if qm else float('nan')
    frac_diff = (var_x_ald - qm_var_x) / qm_var_x if qm else float('nan')
    nsig = frac_diff * qm_var_x / result['std_var'] if qm and result['std_var'] > 0 else float('nan')

    print(f"\n--- Results: beta={BETA}, omega_max={OMEGA_MAX}, tau={TAU} ---")
    print(f"dt          = {DT:.5f}")
    print(f"N_t         = {N_T}")
    print(f"var_x_ALD   = {var_x_ald:.6f} ± {result['std_var']:.6f}")
    print(f"var_x_QM    = {qm_var_x:.6f}")
    print(f"Frac_diff   = {frac_diff:+.4f} ({frac_diff*100:+.2f}%)")
    print(f"N_sigma     = {nsig:+.1f}")
    print(f"<x>_ALD     = {result['mean_x']:.6f}  (should be ~0)")
    print(f"N_unstable  = {result['n_unstable']}/{N_ENSEMBLE}")
    print(f"N_samples   = {result['n_samples']}")
    print(f"Elapsed     = {elapsed:.1f}s")

    # Load/update results file
    existing = {}
    if os.path.exists(save_path):
        with open(save_path) as f:
            existing = json.load(f)

    key = f"beta{BETA}_omax{OMEGA_MAX}_tau{TAU}"
    existing[key] = {
        'beta': BETA,
        'omega_max': OMEGA_MAX,
        'tau': TAU,
        'dt': DT,
        'N_t': N_T,
        'var_x_ald': var_x_ald,
        'var_x_qm': qm_var_x,
        'std_var': result['std_var'],
        'frac_diff': frac_diff if not np.isnan(frac_diff) else None,
        'nsig': nsig if not np.isnan(nsig) else None,
        'mean_x': result['mean_x'],
        'x4_ald': result['x4_mean'],
        'n_unstable': result['n_unstable'],
        'n_samples': result['n_samples'],
        'elapsed_s': elapsed,
    }
    with open(save_path, 'w') as f:
        json.dump(existing, f, indent=2)
    print(f"\nResults saved to {save_path}")
