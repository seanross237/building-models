"""
Sanity check: reproduce E001 result at λ=0.10.
E001 reported: Gamma_SED = 0.00790 ± 0.00137 → ratio = 18.5

This uses the same code but a different random seed to check reproducibility.
"""
import numpy as np
import time

def run_sed_double_well(lam, omega0=1.0, tau=0.001,
                        dt=0.05, N=200000, N_traj=100, seed=None):
    if seed is not None:
        np.random.seed(seed)
    m = 1.0; hbar = 1.0
    freqs = np.fft.rfftfreq(N, d=dt) * 2 * np.pi
    S_F = 2.0 * tau * hbar * np.abs(freqs)**3 / m
    A_k = np.sqrt(S_F * N / (2.0 * dt))
    phases = np.random.uniform(0, 2*np.pi, (N_traj, len(freqs)))
    noise_fft = A_k * np.exp(1j * phases)
    F_zpf_t = np.fft.irfft(noise_fft, n=N, axis=1)
    dF_zpf_t = np.diff(F_zpf_t, axis=1, prepend=F_zpf_t[:, :1]) / dt

    x_min_val = omega0 / np.sqrt(lam)
    x = np.full(N_traj, x_min_val)
    v = np.zeros(N_traj)

    N_burnin = int(1000 / dt)
    N_measure = N - N_burnin
    sign_crossings = np.zeros(N_traj, dtype=int)
    x_prev_sign = np.sign(x)

    for i in range(N):
        cons_force = omega0**2 * x - lam * x**3
        Vpp = -omega0**2 + 3.0 * lam * x**2
        damp_force = -tau * Vpp * v
        zpf_drive = F_zpf_t[:, i] + tau * dF_zpf_t[:, i]
        force = cons_force + damp_force + zpf_drive
        v += force * dt
        x += v * dt
        if i >= N_burnin:
            new_sign = np.sign(x)
            crossings = (new_sign != x_prev_sign) & (new_sign != 0)
            sign_crossings += crossings.astype(int)
            x_prev_sign = new_sign

    T_measure = N_measure * dt
    Gamma_per_traj = sign_crossings / T_measure
    return Gamma_per_traj.mean(), Gamma_per_traj.std() / np.sqrt(N_traj), sign_crossings

# E001 reference values
Gamma_exact = 4.278771e-04

print("Sanity check at λ=0.10: expecting Gamma_SED ≈ 0.00790 ± 0.00137")
print("Running 3 independent trials...\n")

for seed in [42, 100, 999]:
    t0 = time.time()
    mean, sem, crossings = run_sed_double_well(0.10, seed=seed)
    elapsed = time.time() - t0
    n_zero = np.sum(crossings == 0)
    ratio = mean / Gamma_exact
    print(f"  Seed {seed}: Gamma_SED = {mean:.5f} ± {sem:.5f}, "
          f"ratio = {ratio:.2f}, zero-traj = {n_zero}/100, t={elapsed:.1f}s")

# Also try E001's exact seed
print()
for seed in [42]:
    mean, sem, crossings = run_sed_double_well(0.10, seed=42)
    print(f"  E001 seed (42): Gamma_SED = {mean:.5f} ± {sem:.5f}, "
          f"ratio = {mean/Gamma_exact:.2f}")
