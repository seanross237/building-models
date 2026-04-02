"""
ALD-SED spectrum scan for Exploration 007.
Tests how changing noise spectrum exponent n (S(ω) ~ ω^n) affects the β^α scaling.

Fixed parameters from GOAL.md:
  τ = 0.01, ω₀ = 1.0, ω_max = 10.0
  dt = 0.05 (FIXED — do NOT change)
  T = 20000, N_ensemble = 200
  β ∈ {0.0, 0.2, 0.5, 1.0}
"""

import numpy as np
from scipy.optimize import curve_fit
import json
import time

# ---- Fixed parameters ----
TAU = 0.01
OMEGA0 = 1.0
OMEGA_MAX = 10.0
DT = 0.05          # FIXED
T_TOTAL = 20000.0
N_STEPS = int(T_TOTAL / DT)   # 400000 steps
N_ENSEMBLE = 200
BETAS = [0.0, 0.2, 0.5, 1.0]
SPECTRUM_EXPONENTS = [3, 2, 1, 0]

# ---- QM reference values (will be computed by matrix diagonalization) ----
# Placeholder — overwritten by compute_qm_reference()
QM_REF = {0.0: 0.500, 0.1: 0.413, 0.2: None, 0.5: None, 1.0: 0.257}


def compute_qm_reference(betas, n_basis=150):
    """
    Compute QM var_x via matrix diagonalization for V(x) = ½x² + βx⁴.
    Uses harmonic oscillator basis.
    """
    from scipy.linalg import eigh

    results = {}

    # Matrix elements <m|x^4|n> and <m|x^2|n> in HO basis
    # x = (a + a†)/sqrt(2)
    # x^2 matrix elements: <m|x²|n>
    # x^4 matrix elements: <m|x⁴|n>

    # For each β, build Hamiltonian matrix and diagonalize
    for beta in betas:
        N = n_basis
        # Build x, x², x⁴ matrices in HO basis
        # x_{mn} = (1/√2)[√n δ_{m,n-1} + √(n+1) δ_{m,n+1}]
        # Indices 0..N-1

        # Build x matrix (tridiagonal)
        ns = np.arange(N, dtype=float)
        # x = (a + a†)/sqrt(2), a|n> = sqrt(n)|n-1>, a†|n> = sqrt(n+1)|n+1>
        diag_upper = np.sqrt(ns[1:] / 2.0)  # x_{n, n-1} = sqrt(n/2)
        x_mat = np.diag(diag_upper, 1) + np.diag(diag_upper, -1)

        # x² matrix
        x2_mat = x_mat @ x_mat

        # x⁴ matrix
        x4_mat = x2_mat @ x2_mat

        # Hamiltonian: H = p²/2 + x²/2 + βx⁴ = HO + βx⁴
        # HO energies: n + 1/2
        H_diag = ns + 0.5
        H = np.diag(H_diag) + beta * x4_mat

        # Diagonalize
        eigenvalues, eigenvectors = eigh(H)

        # Ground state
        psi_0 = eigenvectors[:, 0]

        # var_x = <x²> in ground state
        var_x = psi_0 @ x2_mat @ psi_0

        results[beta] = float(var_x)

    return results


def generate_colored_noise_force(n_exp, C_n, n_steps, dt, omega_max, rng):
    """
    Generate force time series with PSD S(ω) = C_n * ω^n (one-sided).
    Uses FFT method with amplitude A_k = sqrt(S(ω_k) * N / (2 * dt)).

    Parameters:
    -----------
    n_exp : int, spectral exponent (0,1,2,3)
    C_n : float, normalization constant
    n_steps : int, number of time steps
    dt : float, time step
    omega_max : float, maximum frequency cutoff
    rng : numpy random generator

    Returns:
    --------
    F : array of shape (n_steps,), force time series
    dF_dt : array of shape (n_steps,), time derivative (finite difference)
    """
    N = n_steps

    # Frequency array (angular frequency ω = 2π × freq)
    freqs = np.fft.rfftfreq(N, d=dt)   # cycles per unit time
    omegas = 2.0 * np.pi * freqs        # angular frequency

    # Number of positive frequencies (including DC, Nyquist)
    n_freq = len(omegas)

    # Spectral amplitudes: A_k = sqrt(S(ω_k) * N / (2 * dt))
    # S(ω_k) = C_n * ω_k^n, but only for ω_k <= ω_max
    amplitudes = np.zeros(n_freq)

    # Skip DC (k=0) — zero mean
    for k in range(1, n_freq):
        omega_k = omegas[k]
        if omega_k <= omega_max:
            S_k = C_n * (omega_k ** n_exp)
            amplitudes[k] = np.sqrt(S_k * N / (2.0 * dt))
        # else: amplitude stays 0 (hard cutoff)

    # Random phases
    phases = rng.uniform(0, 2 * np.pi, n_freq)

    # Complex Fourier coefficients
    F_fft = amplitudes * np.exp(1j * phases)

    # Enforce Hermitian symmetry for real output
    # (rfft already handles this correctly — we just need real part after irfft)

    # Transform back to time domain
    F = np.fft.irfft(F_fft, n=N)

    # Time derivative via finite difference
    dF_dt = np.zeros(N)
    dF_dt[:-1] = (F[1:] - F[:-1]) / dt
    dF_dt[-1] = dF_dt[-2]  # pad last element

    return F, dF_dt


def run_single_trajectory(beta, F_zpf, dF_zpf, dt, tau=TAU, omega0=OMEGA0):
    """
    Integrate ALD equation for one trajectory.
    ẍ = −ω₀²x − 4βx³ − τ(ω₀² + 12βx²)ẋ + F_zpf(t) + τ·F'_zpf(t)

    Uses Euler-Cromer (symplectic Euler) integration.
    """
    N = len(F_zpf)

    x = 0.0
    v = 0.0

    x_sum = 0.0
    x2_sum = 0.0

    # Skip first 10% for thermalization
    t_therm = int(0.1 * N)
    n_avg = N - t_therm

    for i in range(N):
        # Effective damping (position-dependent from ALD)
        gamma_eff = tau * (omega0**2 + 12.0 * beta * x**2)

        # Total force on particle
        F_total = (
            -omega0**2 * x
            - 4.0 * beta * x**3
            - gamma_eff * v
            + F_zpf[i]
            + tau * dF_zpf[i]
        )

        # Euler-Cromer: update v first, then x
        v += F_total * dt
        x += v * dt

        # Accumulate statistics after thermalization
        if i >= t_therm:
            x2_sum += x * x

    var_x = x2_sum / n_avg
    return var_x


def run_ensemble(beta, C_n, n_exp, n_ensemble, n_steps, dt, omega_max, seed=42):
    """
    Run ensemble of trajectories and return mean and std of var_x.
    """
    rng = np.random.default_rng(seed)

    var_x_list = []

    for traj in range(n_ensemble):
        # Generate noise for this trajectory
        F_zpf, dF_zpf = generate_colored_noise_force(
            n_exp=n_exp,
            C_n=C_n,
            n_steps=n_steps,
            dt=dt,
            omega_max=omega_max,
            rng=rng
        )

        var_x = run_single_trajectory(beta, F_zpf, dF_zpf, dt)
        var_x_list.append(var_x)

    var_x_arr = np.array(var_x_list)
    mean_var = np.mean(var_x_arr)
    std_var = np.std(var_x_arr) / np.sqrt(n_ensemble)  # standard error

    return mean_var, std_var


def calibrate_normalization(n_exp, n_calib=50, t_calib=5000.0, target=0.500,
                            dt=DT, omega_max=OMEGA_MAX, seed=100):
    """
    Find C_n so that var_x(β=0) = target.
    Strategy: run with C_n=1, measure var_x, then scale C_n.
    Since var_x ∝ C_n (linear response at β=0), one calibration run suffices.
    """
    n_steps_calib = int(t_calib / dt)

    print(f"  Calibrating n={n_exp}: C_n=1.0, n_calib={n_calib}, T_calib={t_calib}...")

    mean_var, std_var = run_ensemble(
        beta=0.0,
        C_n=1.0,
        n_exp=n_exp,
        n_ensemble=n_calib,
        n_steps=n_steps_calib,
        dt=dt,
        omega_max=omega_max,
        seed=seed
    )

    print(f"    C_n=1.0 → var_x = {mean_var:.4f} ± {std_var:.4f}")

    # Since var_x ∝ C_n, scale accordingly
    C_n = target / mean_var

    print(f"    → C_n = {C_n:.6f} (to achieve var_x = {target})")

    return C_n, mean_var


def power_law(x, C, alpha):
    return C * x**alpha


def fit_power_law(betas_fit, delta_e_fit):
    """
    Fit Δe(β) = C × β^α using scipy curve_fit.
    Returns (alpha, alpha_err, C, C_err).
    """
    try:
        popt, pcov = curve_fit(
            power_law,
            betas_fit,
            delta_e_fit,
            p0=[0.03, 0.5],
            bounds=([0, 0.01], [10, 5.0])
        )
        perr = np.sqrt(np.diag(pcov))
        return popt[1], perr[1], popt[0], perr[0]
    except Exception as e:
        print(f"    Curve fit failed: {e}")
        # Manual log-linear fit as fallback
        log_b = np.log(betas_fit)
        log_d = np.log(np.abs(delta_e_fit))
        alpha = np.polyfit(log_b, log_d, 1)[0]
        C = np.exp(np.polyfit(log_b, log_d, 1)[1])
        return alpha, 0.0, C, 0.0


def ratio_test(delta_e_dict, betas_fit=[0.2, 0.5, 1.0]):
    """
    Compute ratio Δe(0.5)/Δe(0.2) and compare to predictions for various α.
    """
    if 0.5 not in delta_e_dict or 0.2 not in delta_e_dict:
        return {}

    observed_ratio = delta_e_dict[0.5] / delta_e_dict[0.2]

    predictions = {}
    for alpha in [0.40, 1.0, 2.0]:
        predictions[alpha] = (0.5 / 0.2) ** alpha

    return {
        'observed': observed_ratio,
        'predicted_0.40': predictions[0.40],
        'predicted_1.0': predictions[1.0],
        'predicted_2.0': predictions[2.0]
    }


def run_full_scan(n_exp, C_n, qm_ref, beta_values=BETAS, n_ensemble=N_ENSEMBLE,
                  n_steps=N_STEPS, dt=DT, omega_max=OMEGA_MAX):
    """
    Run full β scan for a given spectrum exponent and normalization constant.
    Returns dict of results.
    """
    print(f"\n  Running β scan for n={n_exp}, C_n={C_n:.6f}...")

    results = {}

    for beta in beta_values:
        print(f"    β={beta}...", end='', flush=True)
        t0 = time.time()

        mean_var, std_var = run_ensemble(
            beta=beta,
            C_n=C_n,
            n_exp=n_exp,
            n_ensemble=n_ensemble,
            n_steps=n_steps,
            dt=dt,
            omega_max=omega_max,
            seed=42 + int(beta * 100)
        )

        elapsed = time.time() - t0
        print(f" var_x = {mean_var:.4f} ± {std_var:.4f} ({elapsed:.1f}s)")

        qm_val = qm_ref.get(beta, None)
        raw_err = (mean_var - qm_val) if qm_val is not None else None

        results[beta] = {
            'var_x_mean': mean_var,
            'var_x_std': std_var,
            'var_x_qm': qm_val,
            'raw_err': raw_err
        }

    return results


def compute_delta_e(results, beta_values=BETAS):
    """
    Compute baseline-corrected Δe(β):
    Δe(β) = [var_x_SED(β) - var_x_QM(β)] - [var_x_SED(β=0) - 0.500]
    """
    # Baseline: error at β=0
    baseline_err = results[0.0]['raw_err'] if 0.0 in results else 0.0

    delta_e = {}
    for beta in beta_values:
        if beta in results and results[beta]['raw_err'] is not None:
            delta_e[beta] = results[beta]['raw_err'] - baseline_err

    return delta_e


def main():
    import os

    print("=" * 60)
    print("ALD-SED Spectrum Scan — Exploration 007")
    print("=" * 60)

    # ---- Step 1: Compute QM reference values ----
    print("\n[1] Computing QM reference values via matrix diagonalization...")
    qm_betas = [0.0, 0.2, 0.5, 1.0]
    qm_ref = compute_qm_reference(qm_betas, n_basis=150)
    print("  QM reference values:")
    for b, v in sorted(qm_ref.items()):
        print(f"    β={b}: var_x_QM = {v:.4f}")

    # Save QM reference
    with open('qm_reference.json', 'w') as f:
        json.dump({str(k): v for k, v in qm_ref.items()}, f, indent=2)

    # ---- Step 2: Calibrate normalization for each n ----
    print("\n[2] Calibrating normalization constants...")

    normalization = {}

    for n_exp in SPECTRUM_EXPONENTS:
        C_n, var_calib = calibrate_normalization(
            n_exp=n_exp,
            n_calib=50,
            t_calib=5000.0
        )
        normalization[n_exp] = {'C_n': C_n, 'var_calib': var_calib}

    print("\n  Normalization summary:")
    print(f"  {'n':>4} | {'C_n':>12} | {'var_x(β=0,calib)':>18}")
    print(f"  {'-'*4}-+-{'-'*12}-+-{'-'*18}")
    for n_exp in SPECTRUM_EXPONENTS:
        info = normalization[n_exp]
        print(f"  {n_exp:>4} | {info['C_n']:>12.6f} | {info['var_calib']:>18.4f}")

    # ---- Step 3: Run full β scans ----
    print("\n[3] Running full β scans (T=20000, N=200)...")

    all_results = {}

    for n_exp in SPECTRUM_EXPONENTS:
        C_n = normalization[n_exp]['C_n']

        results = run_full_scan(
            n_exp=n_exp,
            C_n=C_n,
            qm_ref=qm_ref,
            beta_values=BETAS,
            n_ensemble=N_ENSEMBLE,
            n_steps=N_STEPS
        )

        all_results[n_exp] = results

        # Intermediate save
        save_path = f'results_n{n_exp}.json'
        with open(save_path, 'w') as f:
            json.dump({
                'n_exp': n_exp,
                'C_n': C_n,
                'results': {str(b): v for b, v in results.items()}
            }, f, indent=2)
        print(f"  Saved: {save_path}")

    # ---- Step 4: Compute Δe and fit power laws ----
    print("\n[4] Computing Δe and fitting power laws...")

    fit_results = {}

    for n_exp in SPECTRUM_EXPONENTS:
        delta_e = compute_delta_e(all_results[n_exp])

        # Fit for β ∈ {0.2, 0.5, 1.0}
        betas_fit = [b for b in [0.2, 0.5, 1.0] if b in delta_e and delta_e[b] > 0]
        delta_e_fit = [delta_e[b] for b in betas_fit]

        if len(betas_fit) >= 2:
            alpha, alpha_err, C_fit, C_err = fit_power_law(betas_fit, delta_e_fit)
        else:
            alpha, alpha_err, C_fit, C_err = None, None, None, None

        # Ratio test
        ratio_info = ratio_test(delta_e)

        # Direction of var_x with β
        var_at_0 = all_results[n_exp][0.0]['var_x_mean'] if 0.0 in all_results[n_exp] else None
        var_at_1 = all_results[n_exp][1.0]['var_x_mean'] if 1.0 in all_results[n_exp] else None
        direction = '↓' if (var_at_1 is not None and var_at_0 is not None and var_at_1 < var_at_0) else '↑'

        fit_results[n_exp] = {
            'delta_e': delta_e,
            'alpha': alpha,
            'alpha_err': alpha_err,
            'C_fit': C_fit,
            'betas_fit': betas_fit,
            'ratio_info': ratio_info,
            'direction': direction
        }

        print(f"\n  n={n_exp}:")
        print(f"    Δe values: {', '.join([f'β={b}: {delta_e.get(b, None):.4f}' for b in BETAS if b in delta_e])}")
        if alpha is not None:
            print(f"    α = {alpha:.3f} ± {alpha_err:.3f}")
        if ratio_info:
            print(f"    Ratio Δe(0.5)/Δe(0.2): observed={ratio_info.get('observed', 'N/A'):.3f}, "
                  f"pred(0.40)={ratio_info.get('predicted_0.40', 0):.3f}, "
                  f"pred(1.0)={ratio_info.get('predicted_1.0', 0):.3f}, "
                  f"pred(2.0)={ratio_info.get('predicted_2.0', 0):.3f}")
        print(f"    Direction: {direction}")

    # ---- Step 5: Print summary ----
    print("\n[5] Summary table:")
    print(f"\n  {'n':>4} | {'Spectrum':>12} | {'C_n':>12} | {'α':>8} | {'dir':>5} | {'β^0.40?':>8}")
    print(f"  {'-'*4}-+-{'-'*12}-+-{'-'*12}-+-{'-'*8}-+-{'-'*5}-+-{'-'*8}")

    spectrum_names = {3: 'ω³ ZPF', 2: 'ω²', 1: 'ω¹', 0: 'white'}

    for n_exp in SPECTRUM_EXPONENTS:
        C_n = normalization[n_exp]['C_n']
        fr = fit_results[n_exp]
        alpha = fr['alpha']
        direction = fr['direction']

        if alpha is not None:
            alpha_str = f"{alpha:.2f} ± {fr['alpha_err']:.2f}"
            is_040 = 'YES' if abs(alpha - 0.40) < 0.15 else 'NO'
        else:
            alpha_str = "N/A"
            is_040 = "N/A"

        print(f"  {n_exp:>4} | {spectrum_names[n_exp]:>12} | {C_n:>12.4f} | {alpha_str:>8} | {direction:>5} | {is_040:>8}")

    # ---- Save all results ----
    final_results = {
        'qm_ref': {str(k): v for k, v in qm_ref.items()},
        'normalization': {str(k): v for k, v in normalization.items()},
        'fit_results': {
            str(n): {
                'alpha': fr['alpha'],
                'alpha_err': fr['alpha_err'],
                'C_fit': fr['C_fit'],
                'direction': fr['direction'],
                'delta_e': {str(b): v for b, v in fr['delta_e'].items()},
                'ratio_info': fr['ratio_info']
            }
            for n, fr in fit_results.items()
        }
    }

    with open('final_results.json', 'w') as f:
        json.dump(final_results, f, indent=2)

    print("\n  Saved: final_results.json")
    print("\nDone!")

    return final_results


if __name__ == '__main__':
    import os
    os.chdir('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-001/explorations/exploration-007/code')
    main()
