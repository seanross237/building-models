"""
SED Time-Domain Simulation for Anharmonic Oscillator
V(x) = 0.5*x^2 + beta*x^4

Langevin equation: x'' = -x - 4*beta*x^3 - Gamma*x' + F_zpf(t)
  Gamma = tau * omega_0^2 = 0.01
  S_F_one(omega) = 2*tau*hbar*omega^3  (one-sided PSD, natural units hbar=m=omega_0=1)
  omega_max = 10 (UV cutoff)

NORMALIZATION (corrected):
  The discrete force sample f_k has continuous-time two-sided PSD:
    S_F_cont_two(omega) = dt * A[n]^2 / N_t
  For S_F_cont_two = tau*omega^3 (required for var_x=0.5 at beta=0):
    A[n] = sqrt(S_F_one * N_t / (2*dt))  [CORRECT formula]
  WRONG formula: A = sqrt(S_F_one * N_t / (4*dt)) -> gives var_x=0.25

Verification (numerical):
  With A = sqrt(S_F_one * N_t / (2*dt)), beta=0 simulation gives
  var_x = 0.515 +/- 0.021 (target: 0.506, within 0.5-sigma). [COMPUTED]

Strategy:
  - Vectorized batches of trajectories (batch_size=50)
  - Pre-generate colored noise via FFT
  - Euler-Cromer (symplectic Euler) integration
  - Sample position multiple times per trajectory (every sample_stride steps)

Author: Math Explorer (Exploration 003)
"""

import numpy as np
import json
import os
import sys
import time

# ============================================================
# Parameters
# ============================================================
TAU = 0.01
OMEGA0 = 1.0
GAMMA = TAU * OMEGA0**2   # = 0.01
DT = 0.05
T_TOTAL = 20000.0
N_T = int(T_TOTAL / DT)   # = 400,000
N_EQ = N_T // 2            # = 200,000 (discard first half)
OMEGA_MAX = 10.0

# Sampling: every 200 time units (>> tau_corr=100) = every 4000 steps
SAMPLE_STRIDE = 4000
SAMPLE_STEPS_ARR = np.arange(N_EQ, N_T, SAMPLE_STRIDE)
IS_SAMPLE = np.zeros(N_T, dtype=bool)
IS_SAMPLE[SAMPLE_STEPS_ARR] = True
N_SAMPLES_PER_TRAJ = int(np.sum(IS_SAMPLE))

BATCH_SIZE = 50
N_ENSEMBLE = 200


def generate_colored_noise_batch(B, N_t, dt, tau, omega_max, rng):
    """
    Generate B realizations of ZPF colored noise.
    One-sided PSD: S_F_one(omega) = 2*tau*omega^3

    Amplitude: A[n] = sqrt(S_F_one * N_t / (2*dt))
    This gives continuous-time two-sided PSD = tau*omega^3,
    ensuring var_x = hbar/(2*m*omega0) = 0.5 for the harmonic oscillator.
    """
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

    return np.fft.irfft(F_hat, n=N_t, axis=1)


def integrate_batch(x0, v0, F_noise, beta,
                    omega0=OMEGA0, Gamma=GAMMA, dt=DT,
                    is_sample=IS_SAMPLE, n_samp=N_SAMPLES_PER_TRAJ):
    """
    Integrate Euler-Cromer for B trajectories simultaneously.
    Returns positions[B, n_samp] at sample time steps.
    """
    x = x0.copy()
    v = v0.copy()
    positions = np.zeros((len(x0), n_samp))
    sample_idx = 0
    F_T = F_noise.T  # (N_t, B) for efficient row access
    omega0_sq = omega0**2

    for k in range(F_noise.shape[1]):
        a = -omega0_sq * x - 4.0 * beta * x * x * x - Gamma * v + F_T[k]
        v += a * dt
        x += v * dt
        if is_sample[k]:
            positions[:, sample_idx] = x
            sample_idx += 1

    return positions


def run_simulation(beta, n_ensemble=N_ENSEMBLE, batch_size=BATCH_SIZE,
                   seed=42, verbose=True):
    """Run SED simulation. Returns statistics dict."""
    rng = np.random.default_rng(seed)
    n_batches = (n_ensemble + batch_size - 1) // batch_size
    batch_list = [min(batch_size, n_ensemble - i*batch_size) for i in range(n_batches)]
    batch_list = [b for b in batch_list if b > 0]

    all_positions = []
    t_start = time.time()

    for b_idx, B in enumerate(batch_list):
        F_noise = generate_colored_noise_batch(B, N_T, DT, TAU, OMEGA_MAX, rng)
        positions = integrate_batch(np.zeros(B), np.zeros(B), F_noise, beta)
        all_positions.append(positions)
        del F_noise

        if verbose:
            n_done = sum(batch_list[:b_idx+1])
            print(f"  Batch {b_idx+1}/{len(batch_list)}: {n_done}/{n_ensemble} "
                  f"| t={time.time()-t_start:.1f}s", flush=True)

    all_positions = np.vstack(all_positions)       # (n_ensemble, n_samp)
    x_samples = all_positions.flatten()

    var_x = float(np.var(x_samples))
    mean_x = float(np.mean(x_samples))
    x4_mean = float(np.mean(x_samples**4))
    var_per_traj = np.var(all_positions, axis=1)
    std_var = float(np.std(var_per_traj) / np.sqrt(n_ensemble))

    return {
        'beta': beta, 'n_samples': len(x_samples),
        'var_x': var_x, 'mean_x': mean_x, 'x4_mean': x4_mean,
        'std_var': std_var, 'x_samples': x_samples
    }


if __name__ == '__main__':
    beta = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0

    print(f"SED Simulation: beta={beta}, dt={DT}, T={T_TOTAL}, N_t={N_T}")
    print(f"N_ensemble={N_ENSEMBLE}, batch_size={BATCH_SIZE}")
    print(f"Samples/traj={N_SAMPLES_PER_TRAJ}, total_samples={N_ENSEMBLE*N_SAMPLES_PER_TRAJ}")
    print()

    ref_path = os.path.join(os.path.dirname(__file__), 'qm_reference_results.json')
    with open(ref_path) as f:
        qm_results = json.load(f)

    qm_key = None
    for k in qm_results:
        if abs(float(k) - beta) < 1e-9:
            qm_key = k; break

    qm_var_x = float(qm_results[qm_key]['var_x']) if qm_key else float('nan')
    qm_x4 = float(qm_results[qm_key]['x4_exp']) if qm_key else float('nan')
    qm_PE = float(qm_results[qm_key]['PE']) if qm_key else float('nan')

    print(f"QM: var_x={qm_var_x:.6f}, <x^4>={qm_x4:.6f}, PE={qm_PE:.6f}")
    print()

    t0 = time.time()
    result = run_simulation(beta, verbose=True)
    t1 = time.time()

    var_x_sed = result['var_x']
    frac_diff = (var_x_sed - qm_var_x) / qm_var_x if not np.isnan(qm_var_x) else float('nan')
    PE_sed = 0.5 * var_x_sed + beta * result['x4_mean']

    print(f"\n--- Results: beta={beta} ---")
    print(f"var_x_SED = {var_x_sed:.6f} ± {result['std_var']:.6f}")
    print(f"var_x_QM  = {qm_var_x:.6f}")
    print(f"Frac_diff = {frac_diff:+.4f} ({frac_diff*100:+.2f}%)")
    print(f"<x>_SED   = {result['mean_x']:.6f}  (should be ~0 by symmetry)")
    print(f"<x^4>_SED = {result['x4_mean']:.6f}  <x^4>_QM = {qm_x4:.6f}")
    print(f"PE_SED    = {PE_sed:.6f}  PE_QM = {qm_PE:.6f}")
    print(f"N_samples = {result['n_samples']}")
    print(f"Time: {t1-t0:.1f}s")

    # Save samples
    samp_path = os.path.join(os.path.dirname(__file__), f'sed_samples_beta{beta:.3f}.npy')
    np.save(samp_path, result['x_samples'])

    # Update results file
    save_path = os.path.join(os.path.dirname(__file__), 'sed_results.json')
    existing = {}
    if os.path.exists(save_path):
        with open(save_path) as f:
            existing = json.load(f)
    existing[str(beta)] = {
        'var_x_sed': var_x_sed, 'var_x_qm': qm_var_x,
        'std_var': result['std_var'],
        'frac_diff': frac_diff if not np.isnan(frac_diff) else None,
        'mean_x': result['mean_x'],
        'x4_sed': result['x4_mean'], 'x4_qm': qm_x4,
        'PE_sed': float(PE_sed), 'PE_qm': qm_PE,
        'n_samples': result['n_samples']
    }
    with open(save_path, 'w') as f:
        json.dump(existing, f, indent=2)
    print(f"Results saved to {save_path}")
