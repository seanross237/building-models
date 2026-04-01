"""
ALD-SED spectrum scan — OPTIMIZED version for Exploration 007.
Vectorizes over trajectories in batches to speed up computation.

Uses batch integration: process BATCH_SIZE trajectories simultaneously,
reducing Python loop overhead while keeping memory manageable.
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.linalg import eigh
import json
import time
import os

# ---- Fixed parameters ----
TAU = 0.01
OMEGA0 = 1.0
OMEGA_MAX = 10.0
DT = 0.05          # FIXED — do NOT change
T_TOTAL = 20000.0
N_STEPS = int(T_TOTAL / DT)   # 400,000 steps
N_ENSEMBLE = 200
BETAS = [0.0, 0.2, 0.5, 1.0]
SPECTRUM_EXPONENTS = [3, 2, 1, 0]
BATCH_SIZE = 20   # trajectories per batch (memory ~64MB per batch)

OUTPUT_DIR = '/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-001/explorations/exploration-007/code'


# ============================================================
# QM REFERENCE
# ============================================================

def compute_qm_reference(betas, n_basis=150):
    """
    Compute QM var_x = <x²> via matrix diagonalization.
    V(x) = ½x² + βx⁴ in harmonic oscillator basis.
    """
    results = {}

    for beta in betas:
        N = n_basis
        ns = np.arange(N, dtype=float)

        # x matrix: x_{m,n} = (1/√2)[√n δ_{m,n-1} + √(m+1) δ_{m+1,n}]
        diag_upper = np.sqrt((ns[1:]) / 2.0)   # off-diag elements
        x_mat = np.diag(diag_upper, 1) + np.diag(diag_upper, -1)

        x2_mat = x_mat @ x_mat
        x4_mat = x2_mat @ x2_mat

        # Hamiltonian: H = (n+½) + β*x⁴
        H = np.diag(ns + 0.5) + beta * x4_mat

        eigenvalues, eigenvectors = eigh(H)
        psi_0 = eigenvectors[:, 0]

        # <x²> = <ψ₀|x²|ψ₀>
        var_x = float(psi_0 @ x2_mat @ psi_0)
        results[beta] = var_x

    return results


# ============================================================
# NOISE GENERATION
# ============================================================

def generate_noise_batch(n_exp, C_n, n_traj, n_steps, dt, omega_max, rng):
    """
    Generate a batch of noise force time series.
    Returns F of shape (n_traj, n_steps) and dF_dt of same shape.
    """
    N = n_steps

    # Frequency array
    freqs = np.fft.rfftfreq(N, d=dt)  # Hz
    omegas = 2.0 * np.pi * freqs       # rad/s
    n_freq = len(omegas)

    # Spectral amplitudes: A_k = sqrt(S(ω_k) * N / (2*dt))
    amplitudes = np.zeros(n_freq)
    mask = (omegas > 0) & (omegas <= omega_max)
    if n_exp == 0:
        amplitudes[mask] = np.sqrt(C_n * N / (2.0 * dt))
    else:
        amplitudes[mask] = np.sqrt(C_n * omegas[mask]**n_exp * N / (2.0 * dt))
    # DC component stays 0

    # Random phases for each trajectory: shape (n_traj, n_freq)
    phases = rng.uniform(0, 2 * np.pi, size=(n_traj, n_freq))

    # Complex Fourier coefficients
    F_fft = amplitudes[np.newaxis, :] * np.exp(1j * phases)  # (n_traj, n_freq)

    # IFFT to get time-domain forces: (n_traj, n_steps)
    F = np.fft.irfft(F_fft, n=N, axis=-1)  # (n_traj, n_steps)

    # Time derivative (finite difference)
    dF_dt = np.zeros_like(F)
    dF_dt[:, :-1] = (F[:, 1:] - F[:, :-1]) / dt
    dF_dt[:, -1] = dF_dt[:, -2]

    return F, dF_dt


# ============================================================
# VECTORIZED BATCH INTEGRATION
# ============================================================

def integrate_batch(beta, F_batch, dF_batch, dt=DT, tau=TAU, omega0=OMEGA0):
    """
    Integrate ALD equation for a batch of trajectories simultaneously.
    F_batch, dF_batch: shape (n_traj, n_steps)
    Returns var_x for each trajectory: shape (n_traj,)
    """
    n_traj, n_steps = F_batch.shape

    # Initial conditions: x=0, v=0 for all trajectories
    x = np.zeros(n_traj)
    v = np.zeros(n_traj)

    # Thermalization: skip first 10%
    t_therm = int(0.1 * n_steps)
    n_avg = n_steps - t_therm

    x2_sum = np.zeros(n_traj)

    for i in range(n_steps):
        # Position-dependent damping: γ_eff = τ(ω₀² + 12βx²)
        gamma_eff = tau * (omega0**2 + 12.0 * beta * x**2)

        # Total force
        F_total = (
            -omega0**2 * x
            - 4.0 * beta * x**3
            - gamma_eff * v
            + F_batch[:, i]
            + tau * dF_batch[:, i]
        )

        # Euler-Cromer update
        v += F_total * dt
        x += v * dt

        # Accumulate x² after thermalization
        if i >= t_therm:
            x2_sum += x**2

    var_x = x2_sum / n_avg
    return var_x


def run_ensemble_batched(beta, C_n, n_exp, n_ensemble=N_ENSEMBLE, n_steps=N_STEPS,
                          dt=DT, omega_max=OMEGA_MAX, batch_size=BATCH_SIZE, seed=42):
    """
    Run full ensemble in batches. Returns (mean_var_x, std_error).
    """
    rng = np.random.default_rng(seed)

    all_var_x = []
    n_batches = (n_ensemble + batch_size - 1) // batch_size

    for batch_idx in range(n_batches):
        batch_start = batch_idx * batch_size
        batch_end = min(batch_start + batch_size, n_ensemble)
        n_traj = batch_end - batch_start

        # Generate noise batch
        F_batch, dF_batch = generate_noise_batch(
            n_exp=n_exp,
            C_n=C_n,
            n_traj=n_traj,
            n_steps=n_steps,
            dt=dt,
            omega_max=omega_max,
            rng=rng
        )

        # Integrate
        var_x_batch = integrate_batch(beta, F_batch, dF_batch, dt=dt)
        all_var_x.extend(var_x_batch.tolist())

    all_var_x = np.array(all_var_x)
    return float(np.mean(all_var_x)), float(np.std(all_var_x) / np.sqrt(len(all_var_x)))


# ============================================================
# CALIBRATION
# ============================================================

def calibrate_normalization(n_exp, n_calib=50, t_calib=5000.0, target=0.500,
                             dt=DT, omega_max=OMEGA_MAX, seed=100, batch_size=50):
    """
    Find C_n so that var_x(β=0) ≈ target.
    Runs with C_n=1 first, then scales (linear response at β=0).
    """
    n_steps_calib = int(t_calib / dt)
    print(f"  Calibrating n={n_exp}: running {n_calib} trajectories × T={t_calib}...")

    mean_var, std_var = run_ensemble_batched(
        beta=0.0,
        C_n=1.0,
        n_exp=n_exp,
        n_ensemble=n_calib,
        n_steps=n_steps_calib,
        dt=dt,
        omega_max=omega_max,
        batch_size=min(batch_size, n_calib),
        seed=seed
    )

    print(f"    C_n=1.0 → var_x = {mean_var:.4f} ± {std_var:.4f}")

    # Linear response: var_x ∝ C_n → scale accordingly
    C_n = target / mean_var
    print(f"    → C_n = {C_n:.6f}")

    return C_n, mean_var


# ============================================================
# POWER LAW FITTING
# ============================================================

def power_law(x, C, alpha):
    return C * np.array(x)**alpha


def fit_power_law(betas_fit, delta_e_fit):
    """Fit Δe(β) = C × β^α. Returns (alpha, alpha_err, C, C_err)."""
    betas_arr = np.array(betas_fit, dtype=float)
    de_arr = np.array(delta_e_fit, dtype=float)

    # Only use positive Δe values
    mask = de_arr > 0
    if mask.sum() < 2:
        print("    Warning: fewer than 2 positive Δe values — skipping fit")
        return None, None, None, None

    betas_arr = betas_arr[mask]
    de_arr = de_arr[mask]

    try:
        popt, pcov = curve_fit(
            power_law,
            betas_arr,
            de_arr,
            p0=[0.03, 0.5],
            bounds=([1e-10, 0.01], [10, 5.0]),
            maxfev=10000
        )
        perr = np.sqrt(np.diag(pcov))
        return float(popt[1]), float(perr[1]), float(popt[0]), float(perr[0])
    except Exception as e:
        print(f"    Curve fit failed: {e}. Using log-linear fallback.")
        log_b = np.log(betas_arr)
        log_d = np.log(de_arr)
        coeffs = np.polyfit(log_b, log_d, 1)
        alpha = float(coeffs[0])
        C = float(np.exp(coeffs[1]))
        return alpha, 0.0, C, 0.0


def compute_delta_e(results, betas=BETAS):
    """
    Δe(β) = [var_x_SED(β) - var_x_QM(β)] - [var_x_SED(0) - 0.500]
    """
    if 0.0 not in results:
        return {}
    baseline = results[0.0]['raw_err']

    delta_e = {}
    for b in betas:
        if b in results and results[b]['raw_err'] is not None:
            delta_e[b] = results[b]['raw_err'] - baseline

    return delta_e


def ratio_test(delta_e):
    """Compute ratio test for Δe(0.5)/Δe(0.2)."""
    if 0.5 not in delta_e or 0.2 not in delta_e:
        return {}
    if delta_e[0.2] == 0:
        return {}
    obs = delta_e[0.5] / delta_e[0.2]
    return {
        'observed': obs,
        'predicted_0.40': (0.5 / 0.2) ** 0.40,
        'predicted_1.0':  (0.5 / 0.2) ** 1.0,
        'predicted_2.0':  (0.5 / 0.2) ** 2.0,
    }


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 65)
    print("ALD-SED Spectrum Scan — Exploration 007")
    print(f"Parameters: dt={DT}, T={T_TOTAL}, N_ensemble={N_ENSEMBLE}")
    print("=" * 65)

    t_total_start = time.time()

    # ---- Step 1: QM reference ----
    print("\n[1] Computing QM reference (matrix diagonalization, basis=150)...")
    qm_betas = [0.0, 0.2, 0.5, 1.0]
    qm_ref = compute_qm_reference(qm_betas, n_basis=150)

    print("  QM reference values:")
    for b in sorted(qm_ref.keys()):
        print(f"    β={b:.1f}: var_x_QM = {qm_ref[b]:.5f}")

    json.dump({str(k): v for k, v in qm_ref.items()},
              open(os.path.join(OUTPUT_DIR, 'qm_reference.json'), 'w'), indent=2)

    # ---- Step 2: Calibrate ----
    print("\n[2] Calibrating normalization constants C_n...")
    normalization = {}
    for n_exp in SPECTRUM_EXPONENTS:
        C_n, var_calib = calibrate_normalization(n_exp=n_exp, n_calib=50, t_calib=5000.0)
        normalization[n_exp] = {'C_n': C_n, 'var_calib': var_calib}

    print("\n  Normalization summary:")
    for n_exp in SPECTRUM_EXPONENTS:
        info = normalization[n_exp]
        print(f"    n={n_exp}: C_n = {info['C_n']:.6f} (calibrated var_x = {info['var_calib']:.4f})")

    # ---- Step 3: Verify normalization at β=0 ----
    print("\n[3] Verifying normalization with full T=20000 run at β=0...")
    for n_exp in SPECTRUM_EXPONENTS:
        C_n = normalization[n_exp]['C_n']
        t0 = time.time()
        mean_var, std_var = run_ensemble_batched(
            beta=0.0, C_n=C_n, n_exp=n_exp,
            n_ensemble=N_ENSEMBLE, n_steps=N_STEPS,
            seed=42
        )
        elapsed = time.time() - t0
        ok = '✓' if abs(mean_var - 0.500) < 0.01 else '✗ WARN'
        print(f"    n={n_exp}: var_x(β=0) = {mean_var:.4f} ± {std_var:.4f} {ok} ({elapsed:.1f}s)")
        normalization[n_exp]['var_verified'] = mean_var
        normalization[n_exp]['var_verified_std'] = std_var

    # ---- Step 4: β scans ----
    print(f"\n[4] Running β scans (N_ensemble={N_ENSEMBLE}, T={T_TOTAL})...")
    all_results = {}

    for n_exp in SPECTRUM_EXPONENTS:
        C_n = normalization[n_exp]['C_n']
        print(f"\n  === n={n_exp} ({['white','ω¹','ω²','ω³'][n_exp]} spectrum) ===")
        results = {}

        for beta in BETAS:
            t0 = time.time()
            mean_var, std_var = run_ensemble_batched(
                beta=beta, C_n=C_n, n_exp=n_exp,
                n_ensemble=N_ENSEMBLE, n_steps=N_STEPS,
                seed=42 + int(beta * 100)
            )
            elapsed = time.time() - t0

            qm_val = qm_ref.get(beta, None)
            raw_err = mean_var - qm_val if qm_val is not None else None

            results[beta] = {
                'var_x_mean': mean_var,
                'var_x_std': std_var,
                'var_x_qm': qm_val,
                'raw_err': raw_err
            }

            qm_str = f"QM={qm_val:.4f}" if qm_val else "QM=N/A"
            err_str = f"err={raw_err:+.4f}" if raw_err is not None else "err=N/A"
            print(f"    β={beta:.1f}: var_x={mean_var:.4f}±{std_var:.4f}, {qm_str}, {err_str} ({elapsed:.1f}s)")

        all_results[n_exp] = results

        # Save intermediate results
        save_path = os.path.join(OUTPUT_DIR, f'results_n{n_exp}.json')
        json.dump({'n_exp': n_exp, 'C_n': C_n,
                   'results': {str(b): v for b, v in results.items()}},
                  open(save_path, 'w'), indent=2)
        print(f"  Saved: results_n{n_exp}.json")

    # ---- Step 5: Analysis ----
    print("\n[5] Power law analysis...")
    fit_results = {}

    for n_exp in SPECTRUM_EXPONENTS:
        delta_e = compute_delta_e(all_results[n_exp])

        # Prepare fit data
        betas_fit = [b for b in [0.2, 0.5, 1.0] if b in delta_e]
        de_fit = [delta_e[b] for b in betas_fit]

        alpha, alpha_err, C_fit, C_err = fit_power_law(betas_fit, de_fit)
        ratio_info = ratio_test(delta_e)

        # Direction
        v0 = all_results[n_exp].get(0.0, {}).get('var_x_mean', None)
        v1 = all_results[n_exp].get(1.0, {}).get('var_x_mean', None)
        direction = '↓' if (v0 and v1 and v1 < v0) else '↑'

        fit_results[n_exp] = {
            'delta_e': {str(b): v for b, v in delta_e.items()},
            'betas_fit': betas_fit,
            'alpha': alpha,
            'alpha_err': alpha_err,
            'C_fit': C_fit,
            'ratio_info': ratio_info,
            'direction': direction
        }

        print(f"\n  n={n_exp}:")
        print(f"    Δe: {', '.join([f'β={b}→{delta_e.get(b, 0):.4f}' for b in BETAS if b in delta_e])}")
        alpha_disp = f"{alpha:.3f} ± {alpha_err:.3f}" if alpha is not None else "N/A"
        print(f"    Power law fit: α = {alpha_disp}")
        if ratio_info:
            print(f"    Ratio test Δe(0.5)/Δe(0.2):")
            print(f"      Observed: {ratio_info.get('observed', 'N/A'):.3f}")
            print(f"      Pred (α=0.40): {ratio_info.get('predicted_0.40', 0):.3f}")
            print(f"      Pred (α=1.00): {ratio_info.get('predicted_1.0', 0):.3f}")
            print(f"      Pred (α=2.00): {ratio_info.get('predicted_2.0', 0):.3f}")
        print(f"    Direction: var_x {direction} with β (QM: ↓)")

    # ---- Summary table ----
    print("\n[6] Summary table:")
    print()
    spectrum_names = {3: 'ω³ ZPF', 2: 'ω²', 1: 'ω¹', 0: 'white'}
    print(f"  {'n':>3} | {'Spectrum':>10} | {'C_n':>10} | {'α':>12} | {'dir':>4} | {'β^0.40?':>8}")
    print(f"  {'---':>3}-+-{'----------':>10}-+-{'----------':>10}-+-{'------------':>12}-+-{'----':>4}-+-{'--------':>8}")
    for n_exp in SPECTRUM_EXPONENTS:
        C_n = normalization[n_exp]['C_n']
        fr = fit_results[n_exp]
        alpha = fr['alpha']
        alpha_err = fr['alpha_err']
        direction = fr['direction']
        if alpha is not None:
            a_str = f"{alpha:.2f} ± {alpha_err:.2f}"
            is_040 = 'YES' if abs(alpha - 0.40) < 0.15 else 'NO'
        else:
            a_str = "N/A"
            is_040 = "N/A"
        print(f"  {n_exp:>3} | {spectrum_names[n_exp]:>10} | {C_n:>10.4f} | {a_str:>12} | {direction:>4} | {is_040:>8}")

    # ---- Save final results ----
    total_elapsed = time.time() - t_total_start
    print(f"\nTotal elapsed: {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")

    final = {
        'parameters': {
            'tau': TAU, 'omega0': OMEGA0, 'omega_max': OMEGA_MAX,
            'dt': DT, 'T': T_TOTAL, 'N_ensemble': N_ENSEMBLE
        },
        'qm_ref': {str(k): v for k, v in qm_ref.items()},
        'normalization': {str(k): v for k, v in normalization.items()},
        'raw_results': {
            str(n_exp): {str(b): v for b, v in results.items()}
            for n_exp, results in all_results.items()
        },
        'fit_results': fit_results
    }

    save_path = os.path.join(OUTPUT_DIR, 'final_results.json')
    json.dump(final, open(save_path, 'w'), indent=2)
    print(f"Saved: final_results.json")

    return final


if __name__ == '__main__':
    results = main()
