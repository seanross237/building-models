"""
SED double-well simulations for E005.
Runs all target λ values using ALD equation with ZPF noise.
Saves results for each λ as it completes.

Parameters from E001 (verified):
  omega0=1, m=1, hbar=1, tau=0.001, omega_max=10, dt=0.05
  N=200000 (T=10000, T_measure=9000 after burn-in)
  N_traj=100

λ=0.075: N_traj=200
λ=0.05:  N=500000, N_traj=200
"""
import numpy as np
import time
import json
import os

np.random.seed(42)  # for reproducibility

def run_sed_double_well(lam, omega0=1.0, tau=0.001,
                        dt=0.05, N=200000, N_traj=100):
    """
    SED double-well simulation with ALD equation.
    V(x) = -½ω₀²x² + ¼λx⁴
    Returns: (Gamma_SED_mean, Gamma_SED_sem, crossing_counts, T_measure)
    """
    m = 1.0; hbar = 1.0

    # FFT noise generation (vectorized)
    freqs = np.fft.rfftfreq(N, d=dt) * 2 * np.pi  # angular frequencies
    S_F = 2.0 * tau * hbar * np.abs(freqs)**3 / m   # one-sided PSD
    A_k = np.sqrt(S_F * N / (2.0 * dt))              # FFT amplitude

    # Generate N_traj independent noise realizations
    phases = np.random.uniform(0, 2*np.pi, (N_traj, len(freqs)))
    noise_fft = A_k * np.exp(1j * phases)
    F_zpf_t = np.fft.irfft(noise_fft, n=N, axis=1)  # shape: (N_traj, N)

    # Time-derivative of noise (finite difference, prepend first column)
    dF_zpf_t = np.diff(F_zpf_t, axis=1, prepend=F_zpf_t[:, :1]) / dt

    # Initial conditions: x = +x_min, v = 0
    x_min_val = omega0 / np.sqrt(lam)
    x = np.full(N_traj, x_min_val)
    v = np.zeros(N_traj)

    # Burn-in: 1000 time units
    N_burnin = int(1000 / dt)
    N_measure = N - N_burnin

    sign_crossings = np.zeros(N_traj, dtype=int)
    x_prev_sign = np.sign(x)

    for i in range(N):
        # Conservative force: -V'(x) = ω₀²x - λx³
        cons_force = omega0**2 * x - lam * x**3

        # ALD damping: -τV''(x)ẋ  where V''(x) = -ω₀² + 3λx²
        Vpp = -omega0**2 + 3.0 * lam * x**2
        damp_force = -tau * Vpp * v

        # ZPF driving
        zpf_drive = F_zpf_t[:, i] + tau * dF_zpf_t[:, i]

        force = cons_force + damp_force + zpf_drive

        # Euler-Cromer (symplectic Euler)
        v += force * dt
        x += v * dt

        # Count sign crossings (after burn-in)
        if i >= N_burnin:
            new_sign = np.sign(x)
            crossings = (new_sign != x_prev_sign) & (new_sign != 0)
            sign_crossings += crossings.astype(int)
            x_prev_sign = new_sign

    T_measure = N_measure * dt
    Gamma_per_traj = sign_crossings / T_measure
    return Gamma_per_traj.mean(), Gamma_per_traj.std() / np.sqrt(N_traj), sign_crossings, T_measure


# QM values (from qm_rates_corrected.py)
qm_data = {
    0.10:  dict(Gamma_exact=4.278771e-04, S_WKB=6.2894,  V_b_E_zpf=3.5355, V_barrier=2.5),
    0.30:  dict(Gamma_exact=8.964654e-02, S_WKB=0.9865,  V_b_E_zpf=1.1785, V_barrier=0.8333),
    0.20:  dict(Gamma_exact=2.810832e-02, S_WKB=2.1059,  V_b_E_zpf=1.7678, V_barrier=1.25),
    0.15:  dict(Gamma_exact=7.468192e-03, S_WKB=3.4170,  V_b_E_zpf=2.3570, V_barrier=1.6667),
    0.075: dict(Gamma_exact=2.206057e-05, S_WKB=9.2679,  V_b_E_zpf=4.7140, V_barrier=3.3333),
    0.05:  dict(Gamma_exact=5.194501e-08, S_WKB=15.3328, V_b_E_zpf=7.0711, V_barrier=5.0),
}

# Results accumulator
results = {}
outfile = "code/results_all_lambda.json"

print("=" * 80)
print("SED Double-Well Simulations — E005")
print("=" * 80)

# Run each λ value
configs = [
    (0.30,  200000, 100),
    (0.20,  200000, 100),
    (0.15,  200000, 100),
    (0.075, 200000, 200),  # more trajectories for deeper barrier
    (0.05,  500000, 200),  # longer simulation + more trajectories
]

for lam, N, N_traj in configs:
    print(f"\nλ = {lam}")
    print(f"  QM: Gamma_exact = {qm_data[lam]['Gamma_exact']:.4e}, S_WKB = {qm_data[lam]['S_WKB']:.4f}")
    print(f"  Sim params: N={N}, N_traj={N_traj}, T_total={N*0.05:.0f}, T_measure={N*0.05-1000:.0f}")
    print(f"  Starting simulation...")
    t0 = time.time()

    np.random.seed(42 + int(lam * 1000))  # reproducible per λ
    Gamma_mean, Gamma_sem, crossing_counts, T_measure = run_sed_double_well(
        lam, N=N, N_traj=N_traj)

    elapsed = time.time() - t0
    qm = qm_data[lam]
    ratio = Gamma_mean / qm['Gamma_exact'] if Gamma_mean > 0 else float('nan')
    ln_ratio = np.log(ratio) if ratio > 0 else float('nan')
    exponent = qm['S_WKB'] - qm['V_b_E_zpf']
    implied_A = np.exp(ln_ratio - exponent) if not np.isnan(ln_ratio) else float('nan')

    # Crossing stats
    n_zero = np.sum(crossing_counts == 0)
    n_nonzero = np.sum(crossing_counts > 0)
    mean_cross = crossing_counts.mean()
    max_cross = crossing_counts.max()

    print(f"  Done in {elapsed:.1f}s")
    print(f"  Gamma_SED = {Gamma_mean:.4e} ± {Gamma_sem:.4e}")
    print(f"  Zero-crossing trajectories: {n_zero}/{N_traj}")
    print(f"  Mean crossings per traj: {mean_cross:.1f}, max: {max_cross}")
    print(f"  Gamma_SED/Gamma_exact = {ratio:.3f}")
    print(f"  ln(Gamma_SED/Gamma_exact) = {ln_ratio:.4f}")
    print(f"  Exponent (S_WKB - Vb/Ezpf) = {exponent:.4f}")
    print(f"  Implied A = exp(ln_ratio - exponent) = {implied_A:.4f}")

    results[lam] = dict(
        lam=lam, N=N, N_traj=N_traj,
        Gamma_SED=Gamma_mean, Gamma_SEM=Gamma_sem,
        Gamma_exact=qm['Gamma_exact'],
        ratio=ratio, ln_ratio=ln_ratio,
        S_WKB=qm['S_WKB'],
        V_b_E_zpf=qm['V_b_E_zpf'],
        exponent=exponent,
        implied_A=implied_A,
        n_zero_crossings=int(n_zero),
        mean_crossings=float(mean_cross),
        elapsed=elapsed,
    )

    # Save after each run
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Saved to {outfile}")

print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)
print(f"{'λ':>8} {'S_WKB':>8} {'Vb/Ezpf':>8} {'exponent':>10} "
      f"{'Γ_SED':>12} {'Γ_exact':>12} {'ratio':>8} {'ln(ratio)':>10} {'A':>8}")
print("-" * 80)

ln_ratios = []
exponents = []
for lam, _, _ in configs:
    r = results[lam]
    print(f"{lam:>8.4f} {r['S_WKB']:>8.4f} {r['V_b_E_zpf']:>8.4f} {r['exponent']:>10.4f} "
          f"{r['Gamma_SED']:>12.4e} {r['Gamma_exact']:>12.4e} {r['ratio']:>8.3f} "
          f"{r['ln_ratio']:>10.4f} {r['implied_A']:>8.4f}")
    if not np.isnan(r['ln_ratio']):
        ln_ratios.append(r['ln_ratio'])
        exponents.append(r['exponent'])

# Also include E001 data points for the fit
e001_ln_ratios = [np.log(1.15), np.log(18.5)]
e001_exponents = [1.408 - 1.4142, 6.290 - 3.5355]

all_ln_ratios = np.array(e001_ln_ratios + ln_ratios)
all_exponents = np.array(e001_exponents + exponents)

# Linear fit: ln(ratio) = ln(A) + slope * exponent
if len(all_ln_ratios) >= 2:
    slope, intercept = np.polyfit(all_exponents, all_ln_ratios, 1)
    A_fit = np.exp(intercept)
    print(f"\nLinear fit of ln(Γ_SED/Γ_exact) vs (S_WKB - Vb/Ezpf):")
    print(f"  slope = {slope:.4f} (expected: 1.0)")
    print(f"  intercept = {intercept:.4f}")
    print(f"  A = exp(intercept) = {A_fit:.4f} (expected: ~1.15)")
    print(f"  Data points used: {len(all_ln_ratios)} (including 2 from E001)")

    results['linear_fit'] = dict(slope=slope, intercept=intercept, A_fit=A_fit,
                                  n_points=len(all_ln_ratios))
    with open(outfile, 'w') as f:
        json.dump(results, f, indent=2)
