"""
Landau-Lifshitz Order-Reduced Abraham-Lorentz Dynamics
Anharmonic SED Oscillator: V(x) = 0.5*x^2 + beta*x^4

LL equation:
    x'' = -omega0^2*x - 4*beta*x^3 - Gamma_eff(x)*x' + F_zpf(t) + tau*F'_zpf(t)

where:
    Gamma_eff(x) = tau*(omega0^2 + 12*beta*x^2)  [POSITION-DEPENDENT damping]

Key differences from E003 (Langevin):
  1. Damping is Gamma_eff(x,beta) not constant Gamma=tau*omega0^2
  2. Extra noise term tau*F'_zpf(t) from the LL reduction

Noise:
    S_F_one(omega) = 2*tau*omega^3  (one-sided ZPF PSD)
    A_k = sqrt(S_F_one * N_t / (2*dt))  [VERIFIED in E003]

F'_zpf(t): obtained from FFT by multiplying frequency components by i*omega.

Parameters:
    tau = 0.01, omega0 = 1, omega_max = 10
    dt = 0.05, T_total = 20000 per trajectory
    N_ensemble = 200, batch_size = 50

Author: Math Explorer (Exploration 004)
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
DT = 0.05
T_TOTAL = 20000.0
N_T = int(T_TOTAL / DT)   # = 400,000
N_EQ = N_T // 2            # = 200,000 (discard first half for equilibration)
OMEGA_MAX = 10.0

# Sampling: every 200 time units (>> tau_corr=100) = every 4000 steps
SAMPLE_STRIDE = 4000
SAMPLE_STEPS_ARR = np.arange(N_EQ, N_T, SAMPLE_STRIDE)
IS_SAMPLE = np.zeros(N_T, dtype=bool)
IS_SAMPLE[SAMPLE_STEPS_ARR] = True
N_SAMPLES_PER_TRAJ = int(np.sum(IS_SAMPLE))

BATCH_SIZE = 50
N_ENSEMBLE = 200


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
                        omega0=OMEGA0, tau=TAU, dt=DT,
                        is_sample=IS_SAMPLE, n_samp=N_SAMPLES_PER_TRAJ):
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


def run_ald_simulation(beta, n_ensemble=N_ENSEMBLE, batch_size=BATCH_SIZE,
                       seed=42, verbose=True):
    """
    Run full ALD simulation for given beta.
    Returns statistics dict.
    """
    rng = np.random.default_rng(seed)
    n_batches = (n_ensemble + batch_size - 1) // batch_size
    batch_list = [min(batch_size, n_ensemble - i*batch_size) for i in range(n_batches)]
    batch_list = [b for b in batch_list if b > 0]

    all_positions = []
    t_start = time.time()
    n_unstable = 0

    for b_idx, B in enumerate(batch_list):
        F_noise, F_prime = generate_ald_noise_batch(B, N_T, DT, TAU, OMEGA_MAX, rng)
        positions = integrate_batch_ald(
            np.zeros(B), np.zeros(B), F_noise, F_prime, beta
        )
        # Check for runaway: positions should be order 1
        max_pos = np.max(np.abs(positions))
        if max_pos > 100.0:
            n_unstable += B
            if verbose:
                print(f"  WARNING: batch {b_idx+1} runaway detected! max|x|={max_pos:.1f}")
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
        'beta': beta, 'n_samples': len(x_samples),
        'var_x': var_x, 'mean_x': mean_x, 'x4_mean': x4_mean,
        'std_var': std_var,
        'n_unstable': n_unstable,
        'x_samples': x_samples
    }


# -------------------------------------------------------------------
# QM reference values (from exploration 003 matrix diagonalization)
# -------------------------------------------------------------------
QM_REF = {
    0.0:  {'var_x': 0.5000, 'x4': 0.7500, 'PE': 0.2500},
    0.01: {'var_x': 0.4862, 'x4': 0.7029, 'PE': 0.2501},
    0.05: {'var_x': 0.4458, 'x4': 0.5788, 'PE': 0.2519},
    0.1:  {'var_x': 0.4125, 'x4': 0.4887, 'PE': 0.2551},
    0.2:  {'var_x': 0.3700, 'x4': 0.3874, 'PE': 0.2625},
    0.5:  {'var_x': 0.3058, 'x4': 0.2602, 'PE': 0.2830},
    1.0:  {'var_x': 0.2571, 'x4': 0.1822, 'PE': 0.3108},
}

# E003 Langevin results (for comparison)
LANGEVIN_REF = {
    0.0:  {'var_x': 0.515, 'std': 0.007},
    0.01: {'var_x': 0.529, 'std': 0.008},
    0.1:  {'var_x': 0.735, 'std': 0.014},
    1.0:  {'var_x': 2.411, 'std': 0.043},
}


if __name__ == '__main__':
    beta = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0

    code_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(code_dir, 'ald_results.json')

    print(f"=== ALD Simulation: beta={beta} ===")
    print(f"  tau={TAU}, omega0={OMEGA0}, omega_max={OMEGA_MAX}")
    print(f"  dt={DT}, T_total={T_TOTAL}, N_t={N_T}")
    print(f"  N_ensemble={N_ENSEMBLE}, batch_size={BATCH_SIZE}")
    print(f"  Samples/traj={N_SAMPLES_PER_TRAJ}, total_samples={N_ENSEMBLE*N_SAMPLES_PER_TRAJ}")
    print()

    # QM reference
    qm = QM_REF.get(beta, None)
    if qm:
        print(f"QM reference:  var_x = {qm['var_x']:.4f}")
    lang = LANGEVIN_REF.get(beta, None)
    if lang:
        print(f"Langevin (E003): var_x = {lang['var_x']:.3f} ± {lang['std']:.3f}")
    print()

    t0 = time.time()
    result = run_ald_simulation(beta, verbose=True)
    elapsed = time.time() - t0

    var_x_ald = result['var_x']
    qm_var_x = qm['var_x'] if qm else float('nan')
    frac_diff = (var_x_ald - qm_var_x) / qm_var_x if qm else float('nan')
    nsig = frac_diff * qm_var_x / result['std_var'] if qm and result['std_var'] > 0 else float('nan')
    PE_ald = 0.5 * var_x_ald + beta * result['x4_mean']

    print(f"\n--- Results: beta={beta} ---")
    print(f"var_x_ALD   = {var_x_ald:.6f} ± {result['std_var']:.6f}")
    print(f"var_x_QM    = {qm_var_x:.6f}")
    print(f"Frac_diff   = {frac_diff:+.4f} ({frac_diff*100:+.2f}%)")
    print(f"Significance= {nsig:+.1f} sigma")
    print(f"<x>_ALD     = {result['mean_x']:.6f}  (should be ~0)")
    print(f"<x^4>_ALD   = {result['x4_mean']:.6f}")
    if qm:
        print(f"<x^4>_QM    = {qm['x4']:.6f}")
    print(f"PE_ALD      = {PE_ald:.6f}")
    if qm:
        print(f"PE_QM       = {qm['PE']:.6f}")
    print(f"N_unstable  = {result['n_unstable']}/{N_ENSEMBLE}")
    print(f"N_samples   = {result['n_samples']}")
    print(f"Elapsed     = {elapsed:.1f}s")

    # Load/update results file
    existing = {}
    if os.path.exists(save_path):
        with open(save_path) as f:
            existing = json.load(f)
    existing[str(beta)] = {
        'var_x_ald': var_x_ald,
        'var_x_qm': qm_var_x,
        'std_var': result['std_var'],
        'frac_diff': frac_diff if not np.isnan(frac_diff) else None,
        'nsig': nsig if not np.isnan(nsig) else None,
        'mean_x': result['mean_x'],
        'x4_ald': result['x4_mean'],
        'x4_qm': qm['x4'] if qm else None,
        'PE_ald': float(PE_ald),
        'PE_qm': qm['PE'] if qm else None,
        'n_unstable': result['n_unstable'],
        'n_samples': result['n_samples'],
        'elapsed_s': elapsed,
    }
    with open(save_path, 'w') as f:
        json.dump(existing, f, indent=2)
    print(f"\nResults saved to {save_path}")

    # Save samples
    samp_path = os.path.join(code_dir, f'ald_samples_beta{beta:.3f}.npy')
    np.save(samp_path, result['x_samples'])
    print(f"Samples saved to {samp_path}")
