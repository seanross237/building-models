"""
SED double-well simulations for E005 — WITH omega_max UV cutoff.
This matches E001's actual code (not GOAL.md which had a bug: omega_max in signature
but not applied to S_F).

Key difference from sed_sim_all.py:
  S_F = np.where((omegas > 0) & (omegas <= omega_max), 2*tau*hbar*omegas**3/m, 0.0)

This limits high-frequency noise injection, following E001's physical prescription.
E001 used seed=456, rng=np.random.default_rng(seed), and forward-difference for dF.
"""
import numpy as np
import time
import json

omega_max_global = 10.0  # rad/s — UV cutoff for ZPF noise (matches E001)

def run_sed_double_well_E001style(lam, omega0=1.0, tau=0.001, omega_max=10.0,
                                   dt=0.05, N=200000, N_traj=100, seed=None):
    """
    SED double-well with omega_max UV cutoff, matching E001's actual code.
    """
    m = 1.0; hbar = 1.0

    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng(42)

    freqs = np.fft.rfftfreq(N, d=dt)
    omegas = 2.0 * np.pi * freqs  # angular frequencies

    # UV cutoff at omega_max (matching E001)
    S_F = np.where((omegas > 0) & (omegas <= omega_max),
                   2.0 * tau * hbar * omegas**3 / m,
                   0.0)
    A_k = np.sqrt(S_F * N / (2.0 * dt))

    n_fft = len(freqs)
    phases = rng.uniform(0, 2*np.pi, size=(N_traj, n_fft))
    F_fft = A_k[np.newaxis, :] * np.exp(1j * phases)
    F_fft[:, 0] = 0.0  # DC = 0
    if N % 2 == 0:
        F_fft[:, -1] = F_fft[:, -1].real  # Nyquist must be real

    F_zpf = np.fft.irfft(F_fft, n=N, axis=1).astype(np.float64)

    # Forward difference for dF (matching E001's np.diff approach)
    dF_zpf = np.empty_like(F_zpf)
    dF_zpf[:, :-1] = np.diff(F_zpf, axis=1) / dt
    dF_zpf[:, -1] = dF_zpf[:, -2]

    # Initial conditions
    x_min_val = omega0 / np.sqrt(lam)
    x = np.full(N_traj, x_min_val)
    v = np.zeros(N_traj)

    # Burn-in: 10% = 1000 time units for N=200000, dt=0.05
    N_burnin = int(0.1 * N)  # = 20000 steps = 1000 time units
    N_measure = N - N_burnin

    sign_crossings = np.zeros(N_traj, dtype=int)
    x_prev_sign = np.sign(x)

    for i in range(N):
        cons_force = omega0**2 * x - lam * x**3
        Vpp = -omega0**2 + 3.0 * lam * x**2
        damp_force = -tau * Vpp * v
        zpf_drive = F_zpf[:, i] + tau * dF_zpf[:, i]
        force = cons_force + damp_force + zpf_drive
        v += force * dt
        x += v * dt

        if i >= N_burnin:
            new_sign = np.sign(x)
            crossings = (new_sign != x_prev_sign) & (new_sign != 0)
            sign_crossings += crossings.astype(int)
            x_prev_sign = new_sign
        else:
            x_prev_sign = np.sign(x)

    T_measure = N_measure * dt
    Gamma_per_traj = sign_crossings / T_measure
    return Gamma_per_traj.mean(), Gamma_per_traj.std() / np.sqrt(N_traj), sign_crossings, T_measure


# ============================================================
# Sanity check vs E001 first
# ============================================================
print("SANITY CHECK vs E001 at λ=0.10:")
print("E001 reported: Gamma_SED = 0.00790 ± 0.00137, ratio = 18.5")
Gamma_exact_010 = 4.278771e-04
for seed in [456, 42, 100]:
    mean, sem, crossings, T = run_sed_double_well_E001style(0.10, seed=seed)
    n_zero = np.sum(crossings == 0)
    print(f"  seed={seed}: Gamma_SED={mean:.5f}±{sem:.5f}, ratio={mean/Gamma_exact_010:.2f}, zero={n_zero}/100")

print()
print("Also check λ=0.25 vs E001: Gamma_SED = 0.0663, ratio = 1.15")
Gamma_exact_025 = 5.780326e-02
mean025, sem025, _, _ = run_sed_double_well_E001style(0.25, seed=456)
print(f"  seed=456: Gamma_SED={mean025:.5f}±{sem025:.5f}, ratio={mean025/Gamma_exact_025:.3f}")

print()
print("=" * 80)
print("NOW RUNNING ALL 5 TARGET λ VALUES WITH omega_max CUTOFF")
print("=" * 80)

# QM values
qm_data = {
    0.10:  dict(Gamma_exact=4.278771e-04, S_WKB=6.2894,  V_b_E_zpf=3.5355, V_barrier=2.5),
    0.25:  dict(Gamma_exact=5.780326e-02, S_WKB=1.4076,  V_b_E_zpf=1.4142, V_barrier=1.0),
    0.30:  dict(Gamma_exact=8.964654e-02, S_WKB=0.9865,  V_b_E_zpf=1.1785, V_barrier=0.8333),
    0.20:  dict(Gamma_exact=2.810832e-02, S_WKB=2.1059,  V_b_E_zpf=1.7678, V_barrier=1.25),
    0.15:  dict(Gamma_exact=7.468192e-03, S_WKB=3.4170,  V_b_E_zpf=2.3570, V_barrier=1.6667),
    0.075: dict(Gamma_exact=2.206057e-05, S_WKB=9.2679,  V_b_E_zpf=4.7140, V_barrier=3.3333),
    0.05:  dict(Gamma_exact=5.194501e-08, S_WKB=15.3328, V_b_E_zpf=7.0711, V_barrier=5.0),
}

results = {}

configs = [
    (0.30,  200000, 100,  456),
    (0.20,  200000, 100,  457),
    (0.15,  200000, 100,  458),
    (0.075, 200000, 200,  459),
    (0.05,  500000, 200,  460),
]

for lam, N, N_traj, seed in configs:
    print(f"\nλ = {lam} (N={N}, N_traj={N_traj}, seed={seed})")
    t0 = time.time()

    mean, sem, crossing_counts, T_measure = run_sed_double_well_E001style(
        lam, N=N, N_traj=N_traj, seed=seed)

    elapsed = time.time() - t0
    qm = qm_data[lam]
    ratio = mean / qm['Gamma_exact']
    ln_ratio = np.log(ratio) if ratio > 0 else float('nan')
    exponent = qm['S_WKB'] - qm['V_b_E_zpf']
    implied_A = np.exp(ln_ratio - exponent) if not np.isnan(ln_ratio) else float('nan')

    n_zero = int(np.sum(crossing_counts == 0))
    mean_cross = float(crossing_counts.mean())

    print(f"  Done in {elapsed:.1f}s")
    print(f"  Gamma_SED = {mean:.4e} ± {sem:.4e}")
    print(f"  Zero-crossing trajectories: {n_zero}/{N_traj}, mean crossings: {mean_cross:.1f}")
    print(f"  ratio = {ratio:.4f}, ln(ratio) = {ln_ratio:.4f}")
    print(f"  exponent = {exponent:.4f}, implied A = {implied_A:.4f}")

    results[lam] = dict(lam=lam, N=N, N_traj=N_traj, seed=seed,
                        Gamma_SED=mean, Gamma_SEM=sem,
                        Gamma_exact=qm['Gamma_exact'],
                        ratio=ratio, ln_ratio=ln_ratio,
                        S_WKB=qm['S_WKB'], V_b_E_zpf=qm['V_b_E_zpf'],
                        exponent=exponent, implied_A=implied_A,
                        n_zero_crossings=n_zero, mean_crossings=mean_cross, elapsed=elapsed)

with open("code/results_corrected.json", 'w') as f:
    json.dump(results, f, indent=2)

# ============================================================
# Summary table
# ============================================================
print("\n" + "=" * 90)
print("SUMMARY TABLE (omega_max cutoff applied)")
print("=" * 90)
print(f"{'λ':>8} {'S_WKB':>8} {'Vb/Ez':>8} {'exponent':>10} "
      f"{'Γ_SED':>12} {'Γ_exact':>12} {'ratio':>10} {'ln(ratio)':>10} {'A':>8}")
print("-" * 90)

ln_ratios = []
exponents = []
for lam, _, _, _ in configs:
    r = results[lam]
    print(f"{lam:>8.4f} {r['S_WKB']:>8.4f} {r['V_b_E_zpf']:>8.4f} {r['exponent']:>10.4f} "
          f"{r['Gamma_SED']:>12.4e} {r['Gamma_exact']:>12.4e} {r['ratio']:>10.4f} "
          f"{r['ln_ratio']:>10.4f} {r['implied_A']:>8.4f}")
    ln_ratios.append(r['ln_ratio'])
    exponents.append(r['exponent'])

# Add E001 data and do linear fit
e001_data = [(0.25, 1.4076, 1.4142, 0.0663, 5.780326e-02),
             (0.10, 6.2894, 3.5355, 0.00790, 4.278771e-04)]
e001_ln_ratios = [np.log(g_sed/g_exact) for _, _, _, g_sed, g_exact in e001_data]
e001_exponents = [s - v for _, s, v, _, _ in e001_data]

all_ln = np.array(e001_ln_ratios + ln_ratios)
all_exp = np.array(e001_exponents + exponents)

slope, intercept = np.polyfit(all_exp, all_ln, 1)
y_pred = slope * all_exp + intercept
SS_res = np.sum((all_ln - y_pred)**2)
SS_tot = np.sum((all_ln - all_ln.mean())**2)
R2 = 1 - SS_res/SS_tot

print(f"\nLinear fit (all 7 points including E001):")
print(f"  slope = {slope:.4f} (expected: 1.0)")
print(f"  intercept = {intercept:.4f}, A = {np.exp(intercept):.4f}")
print(f"  R² = {R2:.6f}")

# E005 only
slope_e5, int_e5 = np.polyfit(exponents, ln_ratios, 1)
y5_pred = slope_e5 * np.array(exponents) + int_e5
SS5_res = np.sum((np.array(ln_ratios) - y5_pred)**2)
SS5_tot = np.sum((np.array(ln_ratios) - np.mean(ln_ratios))**2)
R2_e5 = 1 - SS5_res/SS5_tot
print(f"\nLinear fit (E005 only, 5 new points):")
print(f"  slope = {slope_e5:.4f}, intercept = {int_e5:.4f}, A = {np.exp(int_e5):.4f}")
print(f"  R² = {R2_e5:.6f}")
