"""
SED Two-Oscillator Simulation: Shared ZPF and Bell-CHSH Correlations

Two harmonic oscillators (1D ALD equation) driven by the same ZPF realization,
sampled at positions r=0 and r=d respectively.

The key physics: ZPF field at position r has a phase shift e^{iωr/c} relative
to the field at the origin. This couples the two oscillators through the shared vacuum.

Observables:
- C_xx(d) = <x1 x2> / sqrt(<x1^2> <x2^2>)  — normalized position-position correlation
- C_pp(d) = <p1 p2> / sqrt(<p1^2> <p2^2>)  — normalized momentum-momentum correlation
- Bell-CHSH S using sign-threshold measurements

QM ground state predictions (no coupling):
- <x1 x2> = 0  (separable state)
- <x1^2> = hbar/(2 m omega0) = 0.5 in natural units
"""

import numpy as np
import json
from pathlib import Path

# ──────────────────────────────────────────────
# Parameters
# ──────────────────────────────────────────────
omega0 = 1.0   # natural frequency
m      = 1.0   # mass
hbar   = 1.0   # Planck constant / 2pi
tau    = 0.001 # radiation reaction time scale
c      = 1.0   # speed of light

omega_max = 10.0   # UV cutoff
dt        = 0.05   # time step
N         = 100_000  # time steps per trajectory
N_traj    = 200    # number of independent ZPF realizations

separations = [0.0, 0.1, 1.0, 10.0]

# ──────────────────────────────────────────────
# Frequency grid for noise generation
# ──────────────────────────────────────────────
# rfft gives N//2+1 non-negative frequencies
N_freq = N // 2 + 1
freqs  = np.fft.rfftfreq(N, d=dt)  # cycles per unit time
omegas = 2 * np.pi * freqs          # angular frequencies

# One-sided PSD: S_F(omega) = 2 * tau * hbar * omega^3 / m
# FFT amplitude: A_k = sqrt(S_F(omega_k) * N / (2 * dt))
S_F = np.where(omegas > 0, 2.0 * tau * hbar * omegas**3 / m, 0.0)
# Apply UV cutoff
S_F[omegas > omega_max] = 0.0

# Amplitude per frequency bin
A_k = np.sqrt(S_F * N / (2.0 * dt))


def generate_zpf_pair(d):
    """
    Generate a single ZPF realization as two time series (F1, F2),
    where F2 is the same field as F1 but with a position-dependent
    phase shift e^{i omega d / c} applied in frequency domain.

    Returns: (F1, F2) each of length N
    """
    # Random phases uniformly in [0, 2pi)
    phi = np.random.uniform(0, 2 * np.pi, N_freq)

    # Frequency-domain representation of F1
    F1_fft = A_k * np.exp(1j * phi)
    # Zero out DC and Nyquist to keep real signal clean
    F1_fft[0] = 0.0
    if N % 2 == 0:
        F1_fft[-1] = 0.0

    # Phase shift for position d: e^{i omega d / c}
    phase_shift = np.exp(1j * omegas * d / c)
    F2_fft = F1_fft * phase_shift

    # Inverse FFT → real time series
    F1 = np.fft.irfft(F1_fft, n=N)
    F2 = np.fft.irfft(F2_fft, n=N)

    return F1, F2


def compute_force_derivative(F, dt):
    """
    Numerical derivative dF/dt using central differences.
    Uses forward/backward differences at boundaries.
    """
    dF = np.empty_like(F)
    dF[1:-1] = (F[2:] - F[:-2]) / (2 * dt)
    dF[0]    = (F[1] - F[0]) / dt
    dF[-1]   = (F[-1] - F[-2]) / dt
    return dF


def integrate_oscillator(F, dF):
    """
    Euler-Cromer integration of ALD for a harmonic oscillator.

    ẍ = -omega0^2 x - tau*omega0^2 * xdot + F + tau * dF/dt

    Returns: (x, xdot) arrays of length N
    """
    x    = np.zeros(N)
    xdot = np.zeros(N)

    # Start from rest (equilibrium), ZPF will drive it to equilibrium distribution
    for i in range(N - 1):
        # Acceleration
        acc = (-omega0**2 * x[i]
               - tau * omega0**2 * xdot[i]
               + F[i]
               + tau * dF[i])

        # Euler-Cromer: update velocity first, then position
        xdot[i+1] = xdot[i] + acc * dt
        x[i+1]    = x[i] + xdot[i+1] * dt

    return x, xdot


def run_simulation_for_separation(d, N_traj=N_traj):
    """
    Run N_traj trajectories for oscillator separation d.
    Returns statistics over the second half of each trajectory (after equilibration).
    """
    # Use second half of trajectory for statistics (discard first half as burn-in)
    half = N // 2

    # Accumulators
    sum_x1sq  = 0.0
    sum_x2sq  = 0.0
    sum_x1x2  = 0.0
    sum_p1sq  = 0.0
    sum_p2sq  = 0.0
    sum_p1p2  = 0.0

    # Store per-trajectory averages for Bell-CHSH (we need single time-point samples)
    # Collect (x1, x2, p1, p2) samples from across all trajectories
    x1_samples = []
    x2_samples = []
    p1_samples = []
    p2_samples = []

    for traj_idx in range(N_traj):
        F1, F2 = generate_zpf_pair(d)
        dF1 = compute_force_derivative(F1, dt)
        dF2 = compute_force_derivative(F2, dt)

        x1, xdot1 = integrate_oscillator(F1, dF1)
        x2, xdot2 = integrate_oscillator(F2, dF2)

        # Use second half for statistics
        x1_h = x1[half:]
        x2_h = x2[half:]
        p1_h = xdot1[half:] * m  # p = m * xdot
        p2_h = xdot2[half:] * m

        sum_x1sq += np.mean(x1_h**2)
        sum_x2sq += np.mean(x2_h**2)
        sum_x1x2 += np.mean(x1_h * x2_h)
        sum_p1sq += np.mean(p1_h**2)
        sum_p2sq += np.mean(p2_h**2)
        sum_p1p2 += np.mean(p1_h * p2_h)

        # Sample every 10th point from second half for Bell-CHSH
        # (sub-sample to reduce autocorrelation)
        step = max(1, (N - half) // 50)
        x1_samples.extend(x1_h[::step].tolist())
        x2_samples.extend(x2_h[::step].tolist())
        p1_samples.extend(p1_h[::step].tolist())
        p2_samples.extend(p2_h[::step].tolist())

    # Ensemble averages
    var_x1  = sum_x1sq / N_traj
    var_x2  = sum_x2sq / N_traj
    corr_x1x2 = sum_x1x2 / N_traj
    var_p1  = sum_p1sq / N_traj
    var_p2  = sum_p2sq / N_traj
    corr_p1p2 = sum_p1p2 / N_traj

    # Normalized correlations
    C_xx = corr_x1x2 / np.sqrt(var_x1 * var_x2) if (var_x1 > 0 and var_x2 > 0) else 0.0
    C_pp = corr_p1p2 / np.sqrt(var_p1 * var_p2) if (var_p1 > 0 and var_p2 > 0) else 0.0

    x1_arr = np.array(x1_samples)
    x2_arr = np.array(x2_samples)

    return {
        "d": d,
        "var_x1": var_x1,
        "var_x2": var_x2,
        "corr_x1x2": corr_x1x2,
        "var_p1": var_p1,
        "var_p2": var_p2,
        "corr_p1p2": corr_p1p2,
        "C_xx": C_xx,
        "C_pp": C_pp,
        "x1_samples": x1_arr,
        "x2_samples": x2_arr,
    }


def compute_chsh(x1, x2, a, a_prime, b, b_prime):
    """
    Compute CHSH parameter for threshold measurements.

    A = sign(x1 - a), A' = sign(x1 - a')
    B = sign(x2 - b), B' = sign(x2 - b')

    CHSH = |<AB> + <AB'> + <A'B> - <A'B'>|

    For Gaussian correlated variables, the optimal settings are
    a = b = 0 (mean), a' = b' = sigma/sqrt(2)
    """
    A  = np.sign(x1 - a)
    Ap = np.sign(x1 - a_prime)
    B  = np.sign(x2 - b)
    Bp = np.sign(x2 - b_prime)

    AB   = np.mean(A * B)
    ABp  = np.mean(A * Bp)
    ApB  = np.mean(Ap * B)
    ApBp = np.mean(Ap * Bp)

    S = np.abs(AB + ABp + ApB - ApBp)
    return S, AB, ABp, ApB, ApBp


def compute_bell_chsh_sweep(x1, x2):
    """
    Sweep over several threshold settings and report the maximum CHSH S.
    """
    sigma1 = np.std(x1)
    sigma2 = np.std(x2)
    mean1  = np.mean(x1)
    mean2  = np.mean(x2)

    best_S = 0.0
    best_settings = None
    results = []

    # Try a grid of threshold settings
    a_values  = [mean1, mean1 + sigma1 / np.sqrt(2), mean1 - sigma1 / np.sqrt(2)]
    ap_values = [mean1, mean1 + sigma1 / np.sqrt(2), mean1 - sigma1 / np.sqrt(2)]
    b_values  = [mean2, mean2 + sigma2 / np.sqrt(2), mean2 - sigma2 / np.sqrt(2)]
    bp_values = [mean2, mean2 + sigma2 / np.sqrt(2), mean2 - sigma2 / np.sqrt(2)]

    for a in a_values:
        for ap in ap_values:
            if a == ap:
                continue
            for b in b_values:
                for bp in bp_values:
                    if b == bp:
                        continue
                    S, AB, ABp, ApB, ApBp = compute_chsh(x1, x2, a, ap, b, bp)
                    results.append({
                        "S": S, "a": a, "ap": ap, "b": b, "bp": bp,
                        "AB": AB, "ABp": ABp, "ApB": ApB, "ApBp": ApBp
                    })
                    if S > best_S:
                        best_S = S
                        best_settings = {
                            "a": a, "ap": ap, "b": b, "bp": bp,
                            "AB": AB, "ABp": ABp, "ApB": ApB, "ApBp": ApBp
                        }

    return best_S, best_settings, results


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
print("=" * 60)
print("SED Two-Oscillator Simulation")
print(f"Parameters: omega0={omega0}, tau={tau}, N={N}, N_traj={N_traj}")
print(f"dt={dt}, omega_max={omega_max}")
print(f"QM prediction: var_x = hbar/(2*m*omega0) = {hbar/(2*m*omega0):.4f}")
print("=" * 60)

np.random.seed(42)

all_results = []

for d in separations:
    print(f"\n--- Separation d = {d} ---")
    result = run_simulation_for_separation(d, N_traj=N_traj)

    print(f"  var_x1 = {result['var_x1']:.4f}  (QM: {hbar/(2*m*omega0):.4f})")
    print(f"  var_x2 = {result['var_x2']:.4f}  (QM: {hbar/(2*m*omega0):.4f})")
    print(f"  <x1 x2> = {result['corr_x1x2']:.6f}  (QM: 0.0000)")
    print(f"  C_xx = {result['C_xx']:.4f}")
    print(f"  var_p1 = {result['var_p1']:.4f}")
    print(f"  var_p2 = {result['var_p2']:.4f}")
    print(f"  <p1 p2> = {result['corr_p1p2']:.6f}")
    print(f"  C_pp = {result['C_pp']:.4f}")

    # Bell-CHSH
    x1_arr = result["x1_samples"]
    x2_arr = result["x2_samples"]
    best_S, best_settings, all_chsh = compute_bell_chsh_sweep(x1_arr, x2_arr)
    result["best_S"] = best_S
    result["best_settings"] = best_settings

    print(f"  Bell-CHSH S_max = {best_S:.4f}  (classical bound: 2.000, QM max: 2.828)")
    if best_settings:
        bs = best_settings
        print(f"  Best settings: a={bs['a']:.3f}, a'={bs['ap']:.3f}, b={bs['b']:.3f}, b'={bs['bp']:.3f}")
        print(f"  Components: <AB>={bs['AB']:.4f}, <AB'>={bs['ABp']:.4f}, <A'B>={bs['ApB']:.4f}, <A'B'>={bs['ApBp']:.4f}")

    # Clean up for JSON serialization (remove numpy arrays)
    result_clean = {k: v for k, v in result.items() if k not in ("x1_samples", "x2_samples")}
    all_results.append(result_clean)

# Save results to JSON
out_path = Path(__file__).parent / "results.json"
with open(out_path, "w") as f:
    json.dump(all_results, f, indent=2, default=float)
print(f"\nResults saved to {out_path}")

# Final summary table
print("\n" + "=" * 70)
print("SUMMARY TABLE")
print(f"{'d':>6} | {'var_x1':>7} | {'C_xx':>7} | {'C_pp':>7} | {'S_max':>7} | {'S>2?':>6}")
print("-" * 70)
for r in all_results:
    flag = "YES*" if r["best_S"] > 2.0 else "no"
    print(f"{r['d']:>6.1f} | {r['var_x1']:>7.4f} | {r['C_xx']:>7.4f} | {r['C_pp']:>7.4f} | {r['best_S']:>7.4f} | {flag:>6}")
print("=" * 70)
print(f"QM prediction for var_x: {hbar/(2*m*omega0):.4f}")
print("Classical Bell bound: S <= 2.000")
print("QM maximum (max entanglement): S = 2.828")
