"""
Verify the ZPF spectral density normalization and FFT amplitude convention.

The key question: what is the correct one-sided PSD S_F(ω) for the ZPF
driving force per unit mass, and how does it map to numpy rfft amplitudes?

Convention: ⟨f²⟩ = (1/2π) ∫₀^∞ S^{one}(ω) dω   [physics convention]

Derivation from first principles:
  ZPF spectral energy density: ρ(ω) = ℏω³/(2π²c³)
  Electric field one component: ⟨E_x²⟩ = ∫₀^∞ dω ρ(ω)/(3ε₀)
     = ∫₀^∞ dω ℏω³/(6π²ε₀c³)         [cosine convention]
     = (1/2π) ∫₀^∞ dω ℏω³/(3πε₀c³)   [physics convention: S_E^one = ℏω³/(3πε₀c³)]

  Force per unit mass: a = (e/m)E_x
  Using τ = e²/(6πε₀mc³) → e²/m² = 6πε₀c³τ/m

  S_a^{one}(ω) = (e²/m²) × ℏω³/(3πε₀c³)
               = (6πε₀c³τ/m) × ℏω³/(3πε₀c³)
               = 2τℏω³/m

So: S_F^{one}(ω) = 2τℏω³/m   [one-sided, physics convention]

For numpy rfft/irfft:
  irfft(A, N) → f_n = (1/N) Σ A_k exp(i2πkn/N)  [with conjugate extension]

  For random phases A_k = |A_k| exp(iθ_k):
  ⟨f_n²⟩ = (2/N²) Σ_{k=1}^{K-1} |A_k|²   [K = N/2; factor 2 from conjugate modes]

  Matching to target PSD:
  (2/N²)|A_k|² = S(ω_k) Δω/(2π) = S(ω_k)/(N dt)

  Therefore: |A_k|² = N S(ω_k)/(2 dt)
             |A_k| = sqrt(N S_F(ω_k) / (2 dt))
"""

import numpy as np
from scipy import stats, integrate

def test_noise_normalization():
    """Generate noise, measure its PSD, compare to target."""

    # Parameters
    tau = 0.01
    hbar = 1.0
    m = 1.0
    omega0 = 1.0
    N = 2**16
    dt = 0.05

    freqs = np.fft.rfftfreq(N, d=dt)
    omega = 2 * np.pi * freqs
    K = N // 2 + 1

    # Target one-sided PSD (physics convention)
    S_F = np.zeros(K)
    S_F[1:] = 2 * tau * hbar * omega[1:]**3 / m

    # Correct FFT amplitudes
    A = np.sqrt(N * S_F / (2 * dt))
    A[0] = 0

    # Generate noise ensemble and measure variance
    rng = np.random.default_rng(42)
    n_trials = 500
    var_samples = np.zeros(n_trials)

    for i in range(n_trials):
        phases = rng.uniform(0, 2*np.pi, size=K)
        F_k = A * np.exp(1j * phases)
        F_k[0] = 0
        f = np.fft.irfft(F_k, n=N)
        var_samples[i] = np.var(f)

    # Theoretical variance
    var_theory = (1/(2*np.pi)) * integrate.trapezoid(S_F, omega)

    # Discrete sum prediction
    # ⟨f²⟩ = (2/N²) Σ A_k²
    var_discrete = 2 * np.sum(A[1:K-1]**2) / N**2

    print("=== NOISE NORMALIZATION TEST ===")
    print(f"N={N}, dt={dt}, tau={tau}")
    print(f"Target variance (integral): {var_theory:.6f}")
    print(f"Discrete prediction:        {var_discrete:.6f}")
    print(f"Measured variance:          {np.mean(var_samples):.6f} ± {np.std(var_samples)/np.sqrt(n_trials):.6f}")
    print(f"Ratio measured/theory:      {np.mean(var_samples)/var_theory:.4f}")
    print()

    return np.abs(np.mean(var_samples)/var_theory - 1) < 0.05


def test_oscillator_response():
    """
    Test: generate ZPF noise, apply transfer function, measure position variance.
    Compare to ℏ/(2mω₀) = 0.5.
    """
    tau = 0.01
    hbar = 1.0
    m = 1.0
    omega0 = 1.0
    Gamma = tau * omega0**2

    N = 2**18  # need fine frequency resolution for narrow resonance
    dt = 0.05

    freqs = np.fft.rfftfreq(N, d=dt)
    omega = 2 * np.pi * freqs
    K = N // 2 + 1

    # One-sided PSD
    S_F = np.zeros(K)
    S_F[1:] = 2 * tau * hbar * omega[1:]**3 / m

    # FFT amplitudes
    A_F = np.sqrt(N * S_F / (2 * dt))
    A_F[0] = 0

    # Transfer function (full Abraham-Lorentz)
    H = omega0**2 - omega**2 + 1j * tau * omega**3
    H[0] = 1.0

    # Response amplitudes
    A_x = A_F / np.abs(H)

    # Theoretical position variance
    S_x = S_F / np.abs(H)**2
    var_x_theory = (1/(2*np.pi)) * integrate.trapezoid(S_x, omega)

    # Discrete prediction (what the FFT actually gives)
    var_x_discrete = 2 * np.sum(A_x[1:K-1]**2) / N**2

    # QM prediction
    var_x_qm = hbar / (2 * m * omega0)

    # Monte Carlo check
    rng = np.random.default_rng(42)
    n_trials = 1000
    x_samples = np.zeros(n_trials)
    v_samples = np.zeros(n_trials)

    batch = 100
    for start in range(0, n_trials, batch):
        end = min(start + batch, n_trials)
        bs = end - start
        phases = rng.uniform(0, 2*np.pi, size=(bs, K))
        F_k = A_F[None, :] * np.exp(1j * phases)
        F_k[:, 0] = 0

        X_k = F_k / H[None, :]
        V_k = 1j * omega[None, :] * X_k

        x_t = np.fft.irfft(X_k, n=N, axis=1)
        v_t = np.fft.irfft(V_k, n=N, axis=1)

        mid = N // 2
        x_samples[start:end] = x_t[:, mid]
        v_samples[start:end] = v_t[:, mid]

    var_x_mc = np.var(x_samples)
    var_v_mc = np.var(v_samples)
    E_mc = np.mean(0.5 * v_samples**2 + 0.5 * omega0**2 * x_samples**2)

    print("=== OSCILLATOR RESPONSE TEST ===")
    print(f"Parameters: ω₀={omega0}, τ={tau}, Γ={Gamma}")
    print(f"N_modes={N}, dt={dt}")
    print()
    print(f"Position variance:")
    print(f"  QM prediction:      {var_x_qm:.6f}")
    print(f"  Spectral integral:  {var_x_theory:.6f}")
    print(f"  Discrete sum:       {var_x_discrete:.6f}")
    print(f"  Monte Carlo ({n_trials} traj): {var_x_mc:.6f}")
    print()

    var_v_theory_int = (1/(2*np.pi)) * integrate.trapezoid(omega**2 * S_x, omega)
    E_theory = 0.5 * m * var_v_theory_int + 0.5 * m * omega0**2 * var_x_theory

    print(f"Velocity variance:")
    print(f"  QM prediction:      {hbar*omega0/(2*m):.6f}")
    print(f"  Spectral integral:  {var_v_theory_int:.6f}")
    print(f"  Monte Carlo:        {var_v_mc:.6f}")
    print()
    print(f"Energy:")
    print(f"  QM prediction:      {0.5*hbar*omega0:.6f}")
    print(f"  Spectral integral:  {E_theory:.6f}")
    print(f"  Monte Carlo:        {E_mc:.6f}")
    print()

    # Diagnostics
    print(f"Ratios (should be ~1.0):")
    print(f"  var_x_mc / var_x_qm:       {var_x_mc/var_x_qm:.4f}")
    print(f"  var_x_discrete / var_x_qm: {var_x_discrete/var_x_qm:.4f}")
    print(f"  var_x_theory / var_x_qm:   {var_x_theory/var_x_qm:.4f}")
    print(f"  E_mc / E_qm:               {E_mc/(0.5*hbar*omega0):.4f}")

    return var_x_mc, var_x_qm


if __name__ == '__main__':
    print("NORMALIZATION VERIFICATION")
    print("=" * 60)
    print()

    noise_ok = test_noise_normalization()
    print()

    var_mc, var_qm = test_oscillator_response()
    print()

    print("=" * 60)
    ratio = var_mc / var_qm
    print(f"FINAL: var_x ratio = {ratio:.4f} (target: 1.0)")
    if abs(ratio - 1) < 0.1:
        print("NORMALIZATION: CORRECT")
    else:
        print(f"NORMALIZATION: OFF by factor {ratio:.3f}")
