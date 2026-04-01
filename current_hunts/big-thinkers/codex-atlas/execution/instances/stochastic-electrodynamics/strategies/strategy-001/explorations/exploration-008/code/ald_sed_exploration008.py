"""
ALD-SED Exploration 008 — Critical Spectral Index n* and α Discrepancy

Task A: Run non-integer n ∈ {2.25, 2.5, 2.75} with CALIBRATED normalization
        (var_x(β=0) ≈ 0.500). Measure Δe at β=1 to locate n* (sign flip).

Task B: Run n=3 with PHYSICAL normalization (C_3 = 2τħ/m = 0.02).
        Measure Δe and fit β^α to check if α→0.40.

Based on E007 code (ald_sed_optimized.py). All parameters preserved.
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.linalg import eigh
import json
import time
import os

# ---- Fixed parameters (from E004/E007) ----
TAU = 0.01
OMEGA0 = 1.0
OMEGA_MAX = 10.0
DT = 0.05          # FIXED — do NOT change
T_TOTAL = 20000.0
N_STEPS = int(T_TOTAL / DT)   # 400,000 steps
N_ENSEMBLE = 200
BETAS = [0.0, 0.2, 0.5, 1.0]
BATCH_SIZE = 20

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Physical normalization: C_3 = 2τħ/m = 2×0.01×1.0 = 0.02
C3_PHYSICAL = 2.0 * TAU  # = 0.02 (in units where ħ=m=1)

# Task A: non-integer exponents to test
TASK_A_EXPONENTS = [2.25, 2.50, 2.75]

# E007 anchors (already computed, included for interpolation)
E007_DELTA_E_B1 = {
    2.00: -0.06608836991715086,
    3.00:  0.04330533846678064,
}
E007_CN = {
    2.00: 0.01977634577886274,
    3.00: 0.01954057403358262,
}


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

        diag_upper = np.sqrt((ns[1:]) / 2.0)
        x_mat = np.diag(diag_upper, 1) + np.diag(diag_upper, -1)

        x2_mat = x_mat @ x_mat
        x4_mat = x2_mat @ x2_mat

        H = np.diag(ns + 0.5) + beta * x4_mat

        eigenvalues, eigenvectors = eigh(H)
        psi_0 = eigenvectors[:, 0]

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
    Works for non-integer n_exp.
    """
    N = n_steps

    freqs = np.fft.rfftfreq(N, d=dt)
    omegas = 2.0 * np.pi * freqs
    n_freq = len(omegas)

    amplitudes = np.zeros(n_freq)
    mask = (omegas > 0) & (omegas <= omega_max)

    if n_exp == 0:
        amplitudes[mask] = np.sqrt(C_n * N / (2.0 * dt))
    else:
        # Works for any real n_exp, including non-integers
        amplitudes[mask] = np.sqrt(C_n * omegas[mask]**n_exp * N / (2.0 * dt))

    phases = rng.uniform(0, 2 * np.pi, size=(n_traj, n_freq))
    F_fft = amplitudes[np.newaxis, :] * np.exp(1j * phases)
    F = np.fft.irfft(F_fft, n=N, axis=-1)

    dF_dt = np.zeros_like(F)
    dF_dt[:, :-1] = (F[:, 1:] - F[:, :-1]) / dt
    dF_dt[:, -1] = dF_dt[:, -2]

    return F, dF_dt


# ============================================================
# VECTORIZED BATCH INTEGRATION
# ============================================================

def integrate_batch(beta, F_batch, dF_batch, dt=DT, tau=TAU, omega0=OMEGA0):
    """
    Integrate ALD equation for a batch of trajectories.
    Returns var_x for each trajectory.
    """
    n_traj, n_steps = F_batch.shape

    x = np.zeros(n_traj)
    v = np.zeros(n_traj)

    t_therm = int(0.1 * n_steps)
    n_avg = n_steps - t_therm

    x2_sum = np.zeros(n_traj)

    for i in range(n_steps):
        gamma_eff = tau * (omega0**2 + 12.0 * beta * x**2)

        F_total = (
            -omega0**2 * x
            - 4.0 * beta * x**3
            - gamma_eff * v
            + F_batch[:, i]
            + tau * dF_batch[:, i]
        )

        v += F_total * dt
        x += v * dt

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

        F_batch, dF_batch = generate_noise_batch(
            n_exp=n_exp,
            C_n=C_n,
            n_traj=n_traj,
            n_steps=n_steps,
            dt=dt,
            omega_max=omega_max,
            rng=rng
        )

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
    Uses linear response: var_x ∝ C_n at β=0.
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


def compute_delta_e(results, betas=None):
    """
    Δe(β) = [var_x_SED(β) - var_x_QM(β)] - [var_x_SED(0) - 0.500]
    = raw_err(β) - raw_err(0)
    """
    if betas is None:
        betas = BETAS
    if 0.0 not in results:
        return {}
    baseline = results[0.0]['raw_err']

    delta_e = {}
    for b in betas:
        if b in results and results[b]['raw_err'] is not None:
            delta_e[b] = results[b]['raw_err'] - baseline

    return delta_e


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("ALD-SED Exploration 008 — Critical Spectral Index n* + α Discrepancy")
    print(f"Parameters: dt={DT}, T={T_TOTAL}, N_ensemble={N_ENSEMBLE}")
    print("=" * 70)

    t_total_start = time.time()

    # ---- Step 1: QM reference ----
    print("\n[1] Computing QM reference (matrix diagonalization, basis=150)...")
    qm_ref = compute_qm_reference(BETAS, n_basis=150)

    print("  QM reference values:")
    for b in sorted(qm_ref.keys()):
        print(f"    β={b:.1f}: var_x_QM = {qm_ref[b]:.6f}")

    json.dump({str(k): v for k, v in qm_ref.items()},
              open(os.path.join(OUTPUT_DIR, 'qm_reference.json'), 'w'), indent=2)

    # ===================================================
    # TASK A: Non-integer exponents with calibrated norm
    # ===================================================
    print("\n" + "=" * 70)
    print("TASK A: Non-integer exponents n ∈ {2.25, 2.50, 2.75}")
    print("=" * 70)

    print("\n[2] Calibrating normalization constants for non-integer n...")
    normalization_A = {}
    for n_exp in TASK_A_EXPONENTS:
        C_n, var_calib = calibrate_normalization(n_exp=n_exp, n_calib=50, t_calib=5000.0)
        normalization_A[n_exp] = {'C_n': C_n, 'var_calib': var_calib}

    print("\n  Task A normalization summary:")
    for n_exp in TASK_A_EXPONENTS:
        info = normalization_A[n_exp]
        print(f"    n={n_exp}: C_n = {info['C_n']:.6f}")

    print("\n[3] Verifying normalization at β=0 (full T=20000)...")
    for n_exp in TASK_A_EXPONENTS:
        C_n = normalization_A[n_exp]['C_n']
        t0 = time.time()
        mean_var, std_var = run_ensemble_batched(
            beta=0.0, C_n=C_n, n_exp=n_exp,
            n_ensemble=N_ENSEMBLE, n_steps=N_STEPS, seed=42
        )
        elapsed = time.time() - t0
        ok = '✓' if abs(mean_var - 0.500) < 0.015 else '✗ WARN'
        print(f"    n={n_exp}: var_x(β=0) = {mean_var:.4f} ± {std_var:.4f} {ok} ({elapsed:.1f}s)")
        normalization_A[n_exp]['var_verified'] = mean_var
        normalization_A[n_exp]['var_verified_std'] = std_var

    print(f"\n[4] Running β scans for Task A (N_ensemble={N_ENSEMBLE}, T={T_TOTAL})...")
    all_results_A = {}

    for n_exp in TASK_A_EXPONENTS:
        C_n = normalization_A[n_exp]['C_n']
        print(f"\n  === n={n_exp} ===")
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

        all_results_A[n_exp] = results

        # Save intermediate
        save_path = os.path.join(OUTPUT_DIR, f'results_n{n_exp}.json')
        json.dump({'n_exp': n_exp, 'C_n': C_n,
                   'results': {str(b): v for b, v in results.items()}},
                  open(save_path, 'w'), indent=2)
        print(f"  Saved: results_n{n_exp}.json")

    # ---- Compute Δe for Task A ----
    print("\n[5] Task A: Δe analysis and n* interpolation...")
    delta_e_A = {}
    for n_exp in TASK_A_EXPONENTS:
        delta_e_A[n_exp] = compute_delta_e(all_results_A[n_exp])

    # Add E007 anchors
    delta_e_all = {
        2.00: {1.0: E007_DELTA_E_B1[2.00]},
    }
    delta_e_all.update({n: delta_e_A[n] for n in TASK_A_EXPONENTS})
    delta_e_all[3.00] = {1.0: E007_DELTA_E_B1[3.00]}

    print("\n  Δe at β=1.0 (sign-change tracking):")
    print(f"  {'n':>6} | {'Δe(β=0.2)':>12} | {'Δe(β=0.5)':>12} | {'Δe(β=1.0)':>12} | {'sign':>5}")
    print(f"  {'------':>6}-+-{'------------':>12}-+-{'------------':>12}-+-{'------------':>12}-+-{'-----':>5}")

    # E007 n=2 anchor
    e007_n2 = {0.2: -0.055637260956530654,
               0.5: -0.065436922043152380,
               1.0: -0.066088369917150860}
    print(f"  {2.00:>6.2f} | {e007_n2[0.2]:>12.4f} | {e007_n2[0.5]:>12.4f} | {e007_n2[1.0]:>12.4f} | {'−':>5}")

    sorted_n = TASK_A_EXPONENTS
    for n_exp in sorted_n:
        de = delta_e_A[n_exp]
        de02 = de.get(0.2, float('nan'))
        de05 = de.get(0.5, float('nan'))
        de10 = de.get(1.0, float('nan'))
        sign_str = '+' if de10 > 0 else '−'
        print(f"  {n_exp:>6.2f} | {de02:>12.4f} | {de05:>12.4f} | {de10:>12.4f} | {sign_str:>5}")

    e007_n3 = {0.2: 0.029368071009688135,
               0.5: 0.039182397713617534,
               1.0: 0.043305338466780640}
    print(f"  {3.00:>6.2f} | {e007_n3[0.2]:>12.4f} | {e007_n3[0.5]:>12.4f} | {e007_n3[1.0]:>12.4f} | {'+':>5}")

    # ---- n* interpolation ----
    print("\n[6] n* interpolation:")
    de_b1_values = [(2.00, E007_DELTA_E_B1[2.00])]
    for n_exp in TASK_A_EXPONENTS:
        de_b1_values.append((n_exp, delta_e_A[n_exp].get(1.0, float('nan'))))
    de_b1_values.append((3.00, E007_DELTA_E_B1[3.00]))

    # Sort by n
    de_b1_values.sort(key=lambda x: x[0])

    # Find sign change bracket
    n_star = None
    n_star_method = None

    for i in range(len(de_b1_values) - 1):
        n1, de1 = de_b1_values[i]
        n2, de2 = de_b1_values[i+1]
        if de1 <= 0 and de2 > 0:
            # Linear interpolation
            n_star = n1 + (n2 - n1) * abs(de1) / (abs(de1) + abs(de2))
            n_star_method = f"linear interpolation between n={n1} and n={n2}"
            break
        elif de1 < 0 and de2 >= 0:
            n_star = n1 + (n2 - n1) * abs(de1) / (abs(de1) + abs(de2))
            n_star_method = f"linear interpolation between n={n1} and n={n2}"
            break

    print(f"\n  Δe(β=1) vs n:")
    for n, de in de_b1_values:
        sign_str = '+' if de > 0 else '−'
        print(f"    n={n:.2f}: Δe = {de:+.5f} ({sign_str})")

    if n_star is not None:
        print(f"\n  *** n* = {n_star:.3f} ({n_star_method}) ***")
    else:
        print("\n  WARNING: Sign change not found in range — check results!")

    # ---- Quadratic fit if 3+ points span the crossing ----
    n_arr = np.array([x[0] for x in de_b1_values])
    de_arr = np.array([x[1] for x in de_b1_values])

    # Fit quadratic to all points
    coeffs = np.polyfit(n_arr, de_arr, 2)
    # Solve for roots
    roots = np.roots(coeffs)
    real_roots = [r.real for r in roots if abs(r.imag) < 0.1 and 2.0 <= r.real <= 3.0]
    if real_roots:
        n_star_quad = float(real_roots[0])
        print(f"  Quadratic fit: n* = {n_star_quad:.3f}")
        print(f"  Quadratic coefficients: a={coeffs[0]:.4f}, b={coeffs[1]:.4f}, c={coeffs[2]:.4f}")
    else:
        n_star_quad = None
        print("  Quadratic fit: no root found in [2, 3]")

    # ===================================================
    # TASK B: Physical normalization n=3
    # ===================================================
    print("\n" + "=" * 70)
    print("TASK B: Physical normalization n=3 (C_3 = 0.02)")
    print("=" * 70)

    print(f"\n  Physical C_3 = {C3_PHYSICAL:.6f}")
    print(f"  Calibrated C_3 (E007) = {E007_CN[3.00]:.6f}")
    print(f"  Ratio = {C3_PHYSICAL / E007_CN[3.00]:.4f}")

    results_B = {}
    print(f"\n[7] Running β scan with physical normalization...")

    for beta in BETAS:
        t0 = time.time()
        mean_var, std_var = run_ensemble_batched(
            beta=beta, C_n=C3_PHYSICAL, n_exp=3,
            n_ensemble=N_ENSEMBLE, n_steps=N_STEPS,
            seed=42 + int(beta * 100)
        )
        elapsed = time.time() - t0

        qm_val = qm_ref.get(beta, None)
        raw_err = mean_var - qm_val if qm_val is not None else None

        results_B[beta] = {
            'var_x_mean': mean_var,
            'var_x_std': std_var,
            'var_x_qm': qm_val,
            'raw_err': raw_err
        }

        qm_str = f"QM={qm_val:.4f}" if qm_val else "QM=N/A"
        err_str = f"err={raw_err:+.4f}" if raw_err is not None else "err=N/A"
        print(f"  β={beta:.1f}: var_x={mean_var:.4f}±{std_var:.4f}, {qm_str}, {err_str} ({elapsed:.1f}s)")

    # Δe and power law fit
    delta_e_B = compute_delta_e(results_B)
    print(f"\n  Task B Δe values:")
    for b in sorted(delta_e_B.keys()):
        print(f"    β={b}: Δe = {delta_e_B[b]:+.5f}")

    betas_fit = [b for b in [0.2, 0.5, 1.0] if b in delta_e_B and delta_e_B[b] > 0]
    de_fit = [delta_e_B[b] for b in betas_fit]

    alpha_B, alpha_err_B, C_B, C_err_B = fit_power_law(betas_fit, de_fit)

    print(f"\n  Task B power law fit:")
    if alpha_B is not None:
        print(f"    α = {alpha_B:.3f} ± {alpha_err_B:.3f}")
        print(f"    C = {C_B:.4f} ± {C_err_B:.4f}")
        print(f"    Δe(β) ≈ {C_B:.4f} × β^{alpha_B:.3f}")
        print(f"    Consistent with E004 α=0.40? {abs(alpha_B - 0.40) < 0.15}")
        print(f"    Consistent with E007 α=0.25? {abs(alpha_B - 0.25) < 0.10}")
    else:
        print("    No positive Δe — cannot fit")

    # Save Task B results
    save_path = os.path.join(OUTPUT_DIR, 'results_taskB_physical.json')
    json.dump({
        'n_exp': 3,
        'C_n': C3_PHYSICAL,
        'normalization_type': 'physical',
        'results': {str(b): v for b, v in results_B.items()},
        'delta_e': {str(b): v for b, v in delta_e_B.items()},
        'fit': {'alpha': alpha_B, 'alpha_err': alpha_err_B, 'C': C_B, 'C_err': C_err_B}
    }, open(save_path, 'w'), indent=2)
    print(f"  Saved: results_taskB_physical.json")

    # ===================================================
    # FINAL SUMMARY
    # ===================================================
    total_elapsed = time.time() - t_total_start
    print(f"\n{'=' * 70}")
    print("FINAL SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total elapsed: {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")
    print()
    print(f"Task A — Critical spectral index n*:")
    if n_star is not None:
        print(f"  Linear interpolation: n* = {n_star:.3f}")
    if n_star_quad is not None:
        print(f"  Quadratic fit:        n* = {n_star_quad:.3f}")
    print()
    print(f"Task B — Physical normalization α:")
    if alpha_B is not None:
        print(f"  C_3 = {C3_PHYSICAL}, var_x(β=0) = {results_B[0.0]['var_x_mean']:.4f}")
        print(f"  α = {alpha_B:.3f} (E004: 0.40, E007 calibrated: 0.25)")
        diff_from_E004 = abs(alpha_B - 0.40)
        diff_from_E007 = abs(alpha_B - 0.25)
        if diff_from_E004 < diff_from_E007:
            print(f"  → α is closer to E004 result (physical norm)")
        else:
            print(f"  → α is closer to E007 result (calibrated norm)")
    print()

    # Save all final results
    final = {
        'parameters': {
            'tau': TAU, 'omega0': OMEGA0, 'omega_max': OMEGA_MAX,
            'dt': DT, 'T': T_TOTAL, 'N_ensemble': N_ENSEMBLE
        },
        'qm_ref': {str(k): v for k, v in qm_ref.items()},
        'task_A': {
            'exponents': TASK_A_EXPONENTS,
            'normalization': {str(k): v for k, v in normalization_A.items()},
            'raw_results': {
                str(n_exp): {str(b): v for b, v in results.items()}
                for n_exp, results in all_results_A.items()
            },
            'delta_e': {str(k): {str(b): v for b, v in de.items()}
                        for k, de in delta_e_A.items()},
            'n_star_linear': float(n_star) if n_star is not None else None,
            'n_star_quadratic': float(n_star_quad) if n_star_quad is not None else None,
            'e007_anchors': {
                '2.00': {'delta_e_b1': E007_DELTA_E_B1[2.00]},
                '3.00': {'delta_e_b1': E007_DELTA_E_B1[3.00]},
            }
        },
        'task_B': {
            'C3_physical': C3_PHYSICAL,
            'C3_calibrated_e007': E007_CN[3.00],
            'results': {str(b): v for b, v in results_B.items()},
            'delta_e': {str(b): v for b, v in delta_e_B.items()},
            'fit': {
                'alpha': alpha_B,
                'alpha_err': alpha_err_B,
                'C': C_B,
                'C_err': C_err_B
            }
        }
    }

    save_path = os.path.join(OUTPUT_DIR, 'final_results.json')
    json.dump(final, open(save_path, 'w'), indent=2)
    print(f"Saved: final_results.json")

    return final


if __name__ == '__main__':
    results = main()
