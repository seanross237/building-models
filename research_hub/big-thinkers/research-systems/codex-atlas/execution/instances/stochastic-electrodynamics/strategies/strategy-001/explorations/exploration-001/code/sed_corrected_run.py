"""
Corrected SED simulation: fixes the spectral density normalization and
demonstrates the UV divergence in velocity variance.
"""
import numpy as np
from scipy import stats
import time as timer

omega0 = 1.0; tau = 0.01; m = 1.0; hbar = 1.0
Gamma = tau * omega0**2

print("SED Harmonic Oscillator — CORRECTED Normalization")
print("="*60)

for label, N_modes, dt, N_ens, seed in [
    ("Run A: tau=0.01, N=2000", 2**17, 0.05, 2000, 42),
    ("Run B: tau=0.001, N=2000", 2**17, 0.1, 2000, 123),
    ("Run C: tau=0.01, dt=0.01 (higher w_max)", 2**17, 0.01, 2000, 42),
]:
    t_val = 0.01 if "tau=0.01" in label else 0.001
    G = t_val * omega0**2
    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"{'='*60}")

    rng = np.random.default_rng(seed)
    freqs = np.fft.rfftfreq(N_modes, d=dt)
    omega = 2 * np.pi * freqs
    N_freq = len(omega)
    w_max = omega[-1]
    dw = omega[1] if len(omega) > 1 else 0

    # Full Abraham-Lorentz transfer function
    H = omega0**2 - omega**2 + 1j * t_val * omega**3
    H[0] = 1.0

    # CORRECT: S_one = 2*tau*hbar*omega^3/m, F_amp = sqrt(N*S_one/(2*dt))
    S_one = np.zeros(N_freq)
    S_one[1:] = (2 * t_val * hbar / m) * omega[1:]**3
    F_amp = np.sqrt(N_modes * S_one / (2 * dt))

    K = N_modes // 2
    resp_amp_sq = F_amp[1:K]**2 / np.abs(H[1:K])**2
    var_x_spec = (2.0 / N_modes**2) * np.sum(resp_amp_sq)
    var_v_spec = (2.0 / N_modes**2) * np.sum(omega[1:K]**2 * resp_amp_sq)
    E_spec = 0.5 * var_v_spec + 0.5 * omega0**2 * var_x_spec

    print(f"  w_max={w_max:.1f}, dw={dw:.6f}, dw/G={dw/G:.3f}")
    print(f"  Spectral sums: var_x={var_x_spec:.4f}, var_v={var_v_spec:.4f}, E={E_spec:.4f}")

    # Monte Carlo
    x_samp = np.zeros(N_ens)
    v_samp = np.zeros(N_ens)
    t0 = timer.time()
    batch = 100
    for b in range(0, N_ens, batch):
        nb = min(batch, N_ens - b)
        phases = rng.uniform(0, 2*np.pi, size=(nb, N_freq))
        F_k = F_amp[np.newaxis,:] * np.exp(1j * phases)
        F_k[:, 0] = 0
        X_k = F_k / H[np.newaxis,:]
        V_k = 1j * omega[np.newaxis,:] * X_k
        x_t = np.fft.irfft(X_k, n=N_modes, axis=1)
        v_t = np.fft.irfft(V_k, n=N_modes, axis=1)
        mid = N_modes // 2
        x_samp[b:b+nb] = x_t[:, mid]
        v_samp[b:b+nb] = v_t[:, mid]
    elapsed = timer.time() - t0

    E_samp = 0.5 * v_samp**2 + 0.5 * omega0**2 * x_samp**2
    var_x_mc = np.var(x_samp)
    var_v_mc = np.var(v_samp)
    E_mc = np.mean(E_samp)

    # Gaussianity
    x_std = (x_samp - np.mean(x_samp)) / np.std(x_samp)
    ks_stat, ks_p = stats.kstest(x_std, 'norm')
    sw_stat, sw_p = stats.shapiro(x_samp[:min(5000, len(x_samp))])

    print(f"  MC ({elapsed:.1f}s): var_x={var_x_mc:.4f}, var_v={var_v_mc:.4f}, E={E_mc:.4f}")
    print(f"  var_x error: {abs(var_x_mc-0.5)/0.5*100:.1f}%")
    print(f"  KS test: stat={ks_stat:.4f}, p={ks_p:.4f}")
    print(f"  Shapiro: stat={sw_stat:.4f}, p={sw_p:.4f}")
    print(f"  Skew={stats.skew(x_samp):.4f}, Kurt={stats.kurtosis(x_samp):.4f}")

    # Potential energy only (the convergent part)
    PE = 0.5 * omega0**2 * var_x_mc
    print(f"  Potential energy = 0.5*w0^2*var_x = {PE:.4f} (target 0.25)")
    print(f"  => 2*PE (virial for just PE) = {2*PE:.4f}")

print(f"\n{'='*60}")
print("KEY INSIGHT: var_x converges to 0.5 (QM prediction)")
print("var_v diverges logarithmically with omega_max (UV cutoff)")
print("This is expected: velocity PSD ~ 1/omega for large omega (log divergent)")
print("Position PSD ~ 1/omega^3 for large omega (convergent)")
print("The physical prediction is var_x = hbar/(2*m*omega0), NOT the total energy.")
print("="*60)
