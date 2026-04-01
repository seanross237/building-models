"""
SED Harmonic Oscillator Ground State — Production Simulation
=============================================================

Solves the SED harmonic oscillator EXACTLY in the frequency domain:
    X(w) = F_zpf(w) / H(w)

where H(w) = w0^2 - w^2 + i*tau*w^3 (full Abraham-Lorentz transfer function)
and S_F^one(w) = 2*tau*hbar*w^3/m (one-sided ZPF force PSD, physics convention)

Key results:
  - Position variance <x^2> = hbar/(2*m*w0) -- UV-convergent, matches QM
  - Velocity variance <v^2> -- UV-divergent (grows as ln(w_max))
  - Total energy includes UV contamination from ZPF tail
  - "Resonant energy" extracted from position gives E0 = hbar*w0/2

Natural units: m=1, w0=1, hbar=1

Author: Math Explorer (Atlas)
"""

import numpy as np
from scipy import stats, integrate
import json
import time as timer


# ============================================================
# Analytic reference values via numerical quadrature
# ============================================================

def analytic_integrals(omega0=1.0, tau=0.01, hbar=1.0, m=1.0,
                       omega_max=None, use_full_AL=True):
    """
    Compute variance integrals by numerical quadrature.

    S_F^one(w) = 2*tau*hbar*w^3/m
    <x^2> = (1/2pi) int_0^inf S_F(w)/|H(w)|^2 dw
    <v^2> = (1/2pi) int_0^inf w^2 S_F(w)/|H(w)|^2 dw

    If omega_max is given, integrate up to that cutoff.
    """
    Gamma = tau * omega0**2
    upper = omega_max if omega_max else 1e4

    def S_F(w):
        return 2 * tau * hbar * w**3 / m

    def H_sq(w):
        if use_full_AL:
            return (omega0**2 - w**2)**2 + (tau * w**3)**2
        else:
            return (omega0**2 - w**2)**2 + (Gamma * w)**2

    def integrand_x(w):
        return S_F(w) / H_sq(w)

    def integrand_v(w):
        return w**2 * S_F(w) / H_sq(w)

    var_x, _ = integrate.quad(integrand_x, 1e-8, upper, limit=2000)
    var_v, _ = integrate.quad(integrand_v, 1e-8, upper, limit=2000)

    var_x /= (2 * np.pi)
    var_v /= (2 * np.pi)

    E = 0.5 * m * var_v + 0.5 * m * omega0**2 * var_x

    return {'var_x': var_x, 'var_v': var_v, 'E': E}


# ============================================================
# Frequency-domain simulation
# ============================================================

def sed_frequency_domain(omega0=1.0, tau=0.01, hbar=1.0, m=1.0,
                         N_modes=2**18, dt=0.05,
                         N_ensemble=1000, seed=42,
                         use_full_AL=True):
    """
    Exact frequency-domain solution of the SED harmonic oscillator.

    For a linear system X(w) = F(w)/H(w). We:
    1. Set FFT amplitudes from S_F^one(w) = 2*tau*hbar*w^3/m
    2. Generate random phases (each trajectory independent)
    3. Divide by transfer function H(w)
    4. IFFT to time domain; sample one time point per trajectory

    FFT normalization (derived in verify_normalization.py):
        |A_k| = sqrt(N * S_F(w_k) / (2 * dt))
    ensures correct variance for numpy rfft/irfft convention.
    """
    Gamma = tau * omega0**2
    rng = np.random.default_rng(seed)

    freqs = np.fft.rfftfreq(N_modes, d=dt)
    omega = 2 * np.pi * freqs
    N_freq = len(omega)

    # Transfer function
    if use_full_AL:
        H = omega0**2 - omega**2 + 1j * tau * omega**3
    else:
        H = omega0**2 - omega**2 + 1j * Gamma * omega
    H[0] = 1.0  # avoid div-by-zero at DC (F[0]=0 anyway)

    # One-sided PSD: S_F(w) = 2*tau*hbar*w^3/m
    S_F = np.zeros(N_freq)
    S_F[1:] = 2 * tau * hbar * omega[1:]**3 / m

    # FFT amplitudes: |A_k| = sqrt(N * S_F / (2*dt))
    F_amp = np.sqrt(N_modes * S_F / (2 * dt))
    F_amp[0] = 0

    domega = float(omega[1]) if len(omega) > 1 else 0.0
    omega_max = float(omega[-1])

    print(f"  Freq-domain: N_modes={N_modes}, dt={dt:.4f}")
    print(f"  w_max={omega_max:.1f}, dw={domega:.6f}, Gamma={Gamma:.6f}")
    print(f"  dw/Gamma = {domega/Gamma:.4f} (need << 1 to resolve resonance)")
    print(f"  Transfer: {'full Abraham-Lorentz' if use_full_AL else 'effective damping'}")

    # Discrete variance predictions
    K = N_modes // 2
    A_x = F_amp / np.abs(H)
    var_x_disc = 2 * np.sum(A_x[1:K]**2) / N_modes**2
    var_v_disc = 2 * np.sum((omega[1:K] * A_x[1:K])**2) / N_modes**2

    # Band-pass resonant energy: only modes within +/-5*Gamma of w0
    bw = 5 * Gamma
    idx = np.arange(N_freq)
    mask_res = (omega >= omega0 - bw) & (omega <= omega0 + bw) & (idx > 0) & (idx < K)
    var_x_res = 2 * np.sum(A_x[mask_res]**2) / N_modes**2
    var_v_res = 2 * np.sum((omega[mask_res] * A_x[mask_res])**2) / N_modes**2

    # Monte Carlo ensemble
    x_samples = np.zeros(N_ensemble)
    v_samples = np.zeros(N_ensemble)

    batch_size = min(200, N_ensemble)
    t0 = timer.time()
    n_done = 0

    while n_done < N_ensemble:
        bs = min(batch_size, N_ensemble - n_done)
        phases = rng.uniform(0, 2 * np.pi, size=(bs, N_freq))
        F_k = F_amp[None, :] * np.exp(1j * phases)
        F_k[:, 0] = 0

        X_k = F_k / H[None, :]
        V_k = 1j * omega[None, :] * X_k

        x_t = np.fft.irfft(X_k, n=N_modes, axis=1)
        v_t = np.fft.irfft(V_k, n=N_modes, axis=1)

        mid = N_modes // 2
        x_samples[n_done:n_done+bs] = x_t[:, mid]
        v_samples[n_done:n_done+bs] = v_t[:, mid]
        n_done += bs

    elapsed = timer.time() - t0
    print(f"  {N_ensemble} trajectories in {elapsed:.2f}s")

    energies = 0.5 * m * v_samples**2 + 0.5 * m * omega0**2 * x_samples**2

    # Band-pass filtered velocity (resonant modes only)
    n_filt = min(N_ensemble, 1000)
    rng2 = np.random.default_rng(seed)
    v_filt_samples = np.zeros(n_filt)

    n_done2 = 0
    while n_done2 < n_filt:
        bs2 = min(batch_size, n_filt - n_done2)
        phases2 = rng2.uniform(0, 2*np.pi, size=(bs2, N_freq))
        F_k2 = F_amp[None, :] * np.exp(1j * phases2)
        F_k2[:, 0] = 0

        X_k2 = F_k2 / H[None, :]
        V_k2 = 1j * omega[None, :] * X_k2

        filt = np.zeros(N_freq)
        filt[mask_res] = 1.0
        V_k2_filt = V_k2 * filt[None, :]

        v_filt = np.fft.irfft(V_k2_filt, n=N_modes, axis=1)
        v_filt_samples[n_done2:n_done2+bs2] = v_filt[:, mid]
        n_done2 += bs2

    var_v_filt_mc = np.var(v_filt_samples[:n_filt])

    params = {
        'omega0': omega0, 'tau': tau, 'Gamma': Gamma,
        'hbar': hbar, 'm': m,
        'N_modes': N_modes, 'dt': dt, 'N_ensemble': N_ensemble,
        'omega_max': omega_max, 'domega': domega,
        'use_full_AL': use_full_AL, 'seed': seed,
        'elapsed_s': elapsed,
    }

    return {
        'x_samples': x_samples,
        'v_samples': v_samples,
        'energies': energies,
        'var_x_disc': var_x_disc,
        'var_v_disc': var_v_disc,
        'var_x_res': var_x_res,
        'var_v_res': var_v_res,
        'var_v_filt_mc': var_v_filt_mc,
        'params': params,
    }


# ============================================================
# Analysis
# ============================================================

def analyze(r, hbar=1.0, m=1.0, omega0=1.0):
    """Full analysis of simulation results."""
    x = r['x_samples']
    v = r['v_samples']
    E = r['energies']
    N = len(x)

    E_qm = 0.5 * hbar * omega0
    var_x_qm = hbar / (2 * m * omega0)
    var_v_qm = hbar * omega0 / (2 * m)

    E_mean = np.mean(E)
    E_std = np.std(E) / np.sqrt(N)

    var_x = np.var(x)
    var_x_err = var_x * np.sqrt(2.0 / (N - 1))
    var_v = np.var(v)
    var_v_err = var_v * np.sqrt(2.0 / (N - 1))

    # Resonant energy from position variance (equipartition at resonance)
    E_resonant = 2 * 0.5 * m * omega0**2 * var_x

    # Energy from filtered velocity
    E_filt = 0.5 * m * r['var_v_filt_mc'] + 0.5 * m * omega0**2 * var_x

    # Gaussianity tests
    x_std = (x - np.mean(x)) / np.std(x)
    ks_stat, ks_pval = stats.kstest(x_std, 'norm')

    if N <= 5000:
        sw_stat, sw_pval = stats.shapiro(x)
    else:
        idx = np.random.default_rng(0).choice(N, 5000, replace=False)
        sw_stat, sw_pval = stats.shapiro(x[idx])

    skew = stats.skew(x)
    kurt = stats.kurtosis(x)

    return {
        'N': N,
        'var_x': float(var_x),
        'var_x_err': float(var_x_err),
        'var_x_qm': float(var_x_qm),
        'var_x_rel_err': float(abs(var_x - var_x_qm) / var_x_qm),
        'var_x_disc': float(r['var_x_disc']),
        'var_v': float(var_v),
        'var_v_err': float(var_v_err),
        'var_v_qm': float(var_v_qm),
        'var_v_filt_mc': float(r['var_v_filt_mc']),
        'var_v_res_disc': float(r['var_v_res']),
        'E_total': float(E_mean),
        'E_total_std': float(E_std),
        'E_resonant': float(E_resonant),
        'E_filtered': float(E_filt),
        'E_qm': float(E_qm),
        'E_res_rel_err': float(abs(E_resonant - E_qm) / E_qm),
        'ks_stat': float(ks_stat),
        'ks_pval': float(ks_pval),
        'sw_stat': float(sw_stat),
        'sw_pval': float(sw_pval),
        'skewness': float(skew),
        'excess_kurtosis': float(kurt),
    }


def print_results(a, params, label=""):
    """Pretty-print results."""
    print("=" * 65)
    print(f"  {label}")
    print(f"  w0={params['omega0']}, tau={params['tau']}, Gamma={params['Gamma']:.6f}")
    print(f"  N_ens={params['N_ensemble']}, N_modes={params['N_modes']}, w_max={params['omega_max']:.1f}")
    print("=" * 65)

    print("\n  --- POSITION VARIANCE (UV-convergent) ---")
    print(f"    QM:         var_x = {a['var_x_qm']:.6f}")
    print(f"    Discrete:   var_x = {a['var_x_disc']:.6f}")
    print(f"    MC sample:  var_x = {a['var_x']:.6f} +/- {a['var_x_err']:.6f}")
    print(f"    Rel. error:        {a['var_x_rel_err']*100:.2f}%")

    print("\n  --- VELOCITY VARIANCE (UV-divergent!) ---")
    print(f"    QM:                var_v = {a['var_v_qm']:.6f}")
    print(f"    MC total:          var_v = {a['var_v']:.6f}  (includes UV tail)")
    print(f"    MC resonant (+/-5G): var_v = {a['var_v_filt_mc']:.6f}")
    print(f"    Disc resonant:     var_v = {a['var_v_res_disc']:.6f}")

    print("\n  --- ENERGY ---")
    print(f"    QM:                      E = {a['E_qm']:.6f}")
    print(f"    MC total:                E = {a['E_total']:.6f} +/- {a['E_total_std']:.6f}  (UV)")
    print(f"    From <x^2> (=w0^2<x^2>): E = {a['E_resonant']:.6f}  (err: {a['E_res_rel_err']*100:.2f}%)")
    print(f"    Band-filtered:           E = {a['E_filtered']:.6f}")

    print("\n  --- POSITION DISTRIBUTION ---")
    print(f"    KS test:         stat={a['ks_stat']:.4f}, p={a['ks_pval']:.4f}")
    print(f"    Shapiro-Wilk:    stat={a['sw_stat']:.4f}, p={a['sw_pval']:.4f}")
    print(f"    Skewness:        {a['skewness']:.4f}")
    print(f"    Excess kurtosis: {a['excess_kurtosis']:.4f}")

    var_ok = a['var_x_rel_err'] < 0.05
    E_ok = a['E_res_rel_err'] < 0.05
    gauss_ok = a['ks_pval'] > 0.05

    print(f"\n  --- VERDICT ---")
    print(f"    var_x within 5% of QM:     {'PASS' if var_ok else 'FAIL'}")
    print(f"    E_res within 5% of QM:     {'PASS' if E_ok else 'FAIL'}")
    print(f"    Gaussian (KS p>0.05):      {'PASS' if gauss_ok else 'FAIL'}")
    print("=" * 65)

    return var_ok, E_ok, gauss_ok


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    all_results = {}

    print("=" * 65)
    print("SED HARMONIC OSCILLATOR -- GROUND STATE REPRODUCTION")
    print("Natural units: m=1, w0=1, hbar=1")
    print("Targets: E0=0.5, var_x=0.5, Gaussian distribution")
    print("=" * 65)

    # --- Step 0: Analytic check ---
    print("\n>>> ANALYTIC INTEGRALS (numerical quadrature)")
    for tau_val in [0.01, 0.005, 0.001]:
        for omax, label in [(None, "inf"), (62.83, "pi/dt")]:
            res = analytic_integrals(tau=tau_val, omega_max=omax)
            print(f"  tau={tau_val}, w_max={label}: "
                  f"var_x={res['var_x']:.6f}, var_v={res['var_v']:.4f}, "
                  f"E={res['E']:.4f}")
    print(f"  QM target: var_x=0.500000, var_v=0.5000, E=0.5000")
    print(f"  NOTE: var_v and E diverge as w_max -> inf (known UV issue in SED)")

    # --- Run 1: tau=0.01 ---
    print(f"\n\n>>> RUN 1: tau=0.01, N_ens=2000, full Abraham-Lorentz")
    r1 = sed_frequency_domain(tau=0.01, N_modes=2**18, dt=0.05,
                               N_ensemble=2000, seed=42)
    a1 = analyze(r1)
    p1 = print_results(a1, r1['params'], "Run 1: tau=0.01, full A-L")
    all_results['run1'] = a1

    # --- Run 2: tau=0.005 ---
    print(f"\n\n>>> RUN 2: tau=0.005, N_ens=2000, full Abraham-Lorentz")
    r2 = sed_frequency_domain(tau=0.005, N_modes=2**19, dt=0.05,
                               N_ensemble=2000, seed=123)
    a2 = analyze(r2)
    p2 = print_results(a2, r2['params'], "Run 2: tau=0.005, full A-L")
    all_results['run2'] = a2

    # --- Run 3: tau=0.01, larger ensemble ---
    print(f"\n\n>>> RUN 3: tau=0.01, N_ens=5000 (better statistics)")
    r3 = sed_frequency_domain(tau=0.01, N_modes=2**18, dt=0.05,
                               N_ensemble=5000, seed=777)
    a3 = analyze(r3)
    p3 = print_results(a3, r3['params'], "Run 3: tau=0.01, N=5000")
    all_results['run3'] = a3

    # --- Run 4: tau dependence ---
    print(f"\n\n>>> RUN 4: tau-dependence (should give same var_x for all tau)")
    tau_values = [0.1, 0.05, 0.02, 0.01, 0.005]
    tau_results = {}
    for tau_val in tau_values:
        N_m = max(2**16, int(2**18 * 0.01 / tau_val))
        N_m = min(N_m, 2**20)
        r = sed_frequency_domain(tau=tau_val, N_modes=N_m, dt=0.05,
                                  N_ensemble=1000, seed=42)
        a = analyze(r)
        tau_results[str(tau_val)] = {
            'var_x': a['var_x'], 'var_x_disc': a['var_x_disc'],
            'var_v': a['var_v'], 'E_resonant': a['E_resonant'],
            'ks_pval': a['ks_pval'],
        }
        print(f"  tau={tau_val:.3f}: var_x={a['var_x']:.4f} (disc={a['var_x_disc']:.4f}), "
              f"E_res={a['E_resonant']:.4f}, var_v_total={a['var_v']:.2f}, "
              f"KS p={a['ks_pval']:.3f}")
    all_results['tau_scan'] = tau_results

    # --- Summary ---
    print(f"\n\n{'='*65}")
    print("OVERALL SUMMARY")
    print(f"{'='*65}")
    runs = [
        ("Run 1: tau=0.01, N=2000", p1),
        ("Run 2: tau=0.005, N=2000", p2),
        ("Run 3: tau=0.01, N=5000", p3),
    ]
    for label, (v_ok, e_ok, g_ok) in runs:
        flags = []
        if not v_ok: flags.append("var_x")
        if not e_ok: flags.append("E_res")
        if not g_ok: flags.append("Gaussian")
        status = "ALL PASS" if not flags else f"FAIL: {', '.join(flags)}"
        print(f"  {label}: {status}")

    with open('results_summary.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=float)

    np.savez('samples_run3.npz',
             x=r3['x_samples'], v=r3['v_samples'], E=r3['energies'])

    print(f"\nData saved to results_summary.json, samples_run3.npz")
