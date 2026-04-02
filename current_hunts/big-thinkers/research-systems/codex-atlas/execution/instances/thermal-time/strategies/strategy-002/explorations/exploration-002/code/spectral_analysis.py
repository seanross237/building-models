"""
Refined FFT spectral analysis with zero-padding for better frequency resolution.
Also computes the time-domain difference C_QM - C_global_TTH.
"""

import numpy as np
from scipy.linalg import expm
from numpy.linalg import eigh, norm
import json

# ============================================================
# Parameters — longer time series + zero-padding for resolution
# ============================================================
N = 20
omega = 1.0
beta = 2.0
N_tau = 2000   # More points for better resolution
tau_max = 16 * np.pi  # Longer window
tau_arr = np.linspace(0, tau_max, N_tau)

print("=" * 70)
print("Refined Spectral Analysis — High-Resolution FFT")
print(f"N_tau={N_tau}, tau_max={tau_max:.2f} = 16*pi")
print("=" * 70)

# Build operators
n_op  = np.diag(np.arange(N, dtype=float))
a_op  = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op  = (a_op + ad_op) / np.sqrt(2)
I_N   = np.eye(N)

H_A_2mode    = np.kron(omega * n_op, I_N)
H_B_2mode    = np.kron(I_N, omega * n_op)
H_int_base   = np.kron(q_op, q_op)
H_uncoupled  = H_A_2mode + H_B_2mode
x_A_2mode    = np.kron(q_op, I_N)

# Post-quench state
rho_0 = expm(-beta * H_uncoupled)
rho_0 /= np.trace(rho_0).real


def compute_correlator(H_mat, rho_mat, x_op, tau_arr):
    evals, evecs = eigh(H_mat)
    rho_eig = evecs.conj().T @ rho_mat @ evecs
    x_eig   = evecs.conj().T @ x_op   @ evecs
    xrho = x_eig @ rho_eig
    B = x_eig * xrho.T
    conj_phase = np.exp(-1j * np.outer(tau_arr, evals))
    phase      = conj_phase.conj()
    inner = B @ conj_phase.T
    C = np.sum(phase * inner.T, axis=1).real
    return C


# Frequency resolution
dt = tau_arr[1] - tau_arr[0]
df_base = 1.0 / (N_tau * dt) * 2 * np.pi  # angular freq resolution
print(f"Base freq resolution: {df_base:.4f} rad/s")

# Zero-padding for 8x interpolation
N_pad = N_tau * 8
df_zp = 1.0 / (N_pad * dt) * 2 * np.pi
print(f"Zero-padded freq resolution: {df_zp:.4f} rad/s")

lambda_vals = [0.1, 0.2, 0.3, 0.5]

print(f"\n{'='*70}")
print("HIGH-RESOLUTION FFT RESULTS")
print(f"{'='*70}")

spectral_results = {}
for lam in lambda_vals:
    H_coupled = H_uncoupled + lam * H_int_base

    omega_plus  = np.sqrt(omega**2 + lam)
    omega_minus = np.sqrt(omega**2 - lam) if omega**2 > lam else 0.0
    delta_omega = omega_plus - omega_minus

    C_QM     = compute_correlator(H_coupled,   rho_0, x_A_2mode, tau_arr)
    C_global = compute_correlator(H_uncoupled, rho_0, x_A_2mode, tau_arr)
    C_diff   = C_QM - C_global

    # Zero-padded FFT
    fft_qm  = np.abs(np.fft.rfft(C_QM - C_QM.mean(), n=N_pad))
    fft_gl  = np.abs(np.fft.rfft(C_global - C_global.mean(), n=N_pad))
    fft_diff = np.abs(np.fft.rfft(C_diff - C_diff.mean(), n=N_pad))
    freq_axis = np.fft.rfftfreq(N_pad, d=dt) * 2 * np.pi

    # Find peaks: top 10 above 5% threshold
    def find_peaks(fft_data, freq_axis, threshold_frac=0.02, n_peaks=10):
        threshold = threshold_frac * fft_data.max()
        # Simple peak finding: local maxima above threshold
        peaks = []
        for i in range(1, len(fft_data)-1):
            if fft_data[i] > threshold and fft_data[i] > fft_data[i-1] and fft_data[i] > fft_data[i+1]:
                peaks.append((freq_axis[i], fft_data[i]))
        peaks.sort(key=lambda x: -x[1])
        return peaks[:n_peaks]

    peaks_qm   = find_peaks(fft_qm, freq_axis)
    peaks_gl   = find_peaks(fft_gl, freq_axis)
    peaks_diff = find_peaks(fft_diff, freq_axis)

    print(f"\nlambda = {lam}:")
    print(f"  Expected: omega_+ = {omega_plus:.6f}, omega_- = {omega_minus:.6f}, delta = {delta_omega:.6f}")
    print(f"  Expected omega = {omega:.6f} (uncoupled)")

    print(f"\n  C_QM peaks:")
    for freq, amp in peaks_qm[:6]:
        match = ""
        if abs(freq - omega_plus) < 0.05: match = " <-- omega_+"
        elif abs(freq - omega_minus) < 0.05: match = " <-- omega_-"
        elif abs(freq - omega) < 0.05: match = " <-- omega"
        elif abs(freq - 2*omega) < 0.05: match = " <-- 2*omega"
        elif abs(freq - (omega_plus + omega_minus)) < 0.05: match = " <-- omega_+ + omega_-"
        print(f"    omega = {freq:.4f}  amp = {amp:.3f}{match}")

    print(f"\n  C_global peaks:")
    for freq, amp in peaks_gl[:4]:
        match = ""
        if abs(freq - omega) < 0.05: match = " <-- omega"
        elif abs(freq - 2*omega) < 0.05: match = " <-- 2*omega"
        print(f"    omega = {freq:.4f}  amp = {amp:.3f}{match}")

    print(f"\n  C_QM - C_global difference spectrum peaks:")
    for freq, amp in peaks_diff[:6]:
        match = ""
        if abs(freq - omega_plus) < 0.05: match = " <-- omega_+"
        elif abs(freq - omega_minus) < 0.05: match = " <-- omega_-"
        elif abs(freq - omega) < 0.05: match = " <-- omega"
        elif abs(freq - 2*omega_plus) < 0.05: match = " <-- 2*omega_+"
        elif abs(freq - 2*omega_minus) < 0.05: match = " <-- 2*omega_-"
        elif abs(freq - (omega_plus + omega_minus)) < 0.05: match = " <-- omega_+ + omega_-"
        print(f"    omega = {freq:.4f}  amp = {amp:.3f}{match}")

    spectral_results[str(lam)] = {
        "omega_plus": float(omega_plus),
        "omega_minus": float(omega_minus),
        "peaks_qm": [(float(f), float(a)) for f,a in peaks_qm],
        "peaks_global": [(float(f), float(a)) for f,a in peaks_gl],
        "peaks_diff": [(float(f), float(a)) for f,a in peaks_diff],
    }


# ============================================================
# ANALYTICAL VERIFICATION
# ============================================================
print(f"\n{'='*70}")
print("ANALYTICAL VERIFICATION")
print("For the post-quench state (product thermal state), the correlators")
print("can be checked analytically.")
print(f"{'='*70}")

# For rho_0 = product thermal state at temp 1/beta of uncoupled system:
# <x_A(t) x_A(0)>_QM (evolving under H_coupled) can be computed by
# transforming to normal modes.
#
# The uncoupled state in the normal mode basis is NOT a thermal state
# of the normal mode Hamiltonian, which is the source of the discrepancy.

for lam in [0.1, 0.3, 0.5]:
    H_coupled = H_uncoupled + lam * H_int_base
    C_QM     = compute_correlator(H_coupled,   rho_0, x_A_2mode, tau_arr)
    C_global = compute_correlator(H_uncoupled, rho_0, x_A_2mode, tau_arr)

    omega_p = np.sqrt(omega**2 + lam)
    omega_m = np.sqrt(omega**2 - lam)

    # Analytical: uncoupled thermal state correlator
    # <x_A(t) x_A(0)>_uncoupled = 1/(2*omega) * coth(beta*omega/2) * cos(omega*t)
    n_bar = 1.0 / (np.exp(beta * omega) - 1)
    C_analytical_uncoupled = (2*n_bar + 1) / (2*omega) * np.cos(omega * tau_arr)

    # Check C_global matches analytical
    diff_analytic = norm(C_global - C_analytical_uncoupled) / norm(C_analytical_uncoupled)
    print(f"\nlam={lam}: ||C_global - analytical_uncoupled|| / ||analytical|| = {diff_analytic:.2e}")

    # Analytical: C_QM for post-quench
    # x_A = (x_+ + x_-)/sqrt(2), where x_± are normal mode positions
    # x_±(t) = x_±(0) cos(omega_± t) + p_±(0)/omega_± sin(omega_± t)
    # In uncoupled thermal state: <x_+ x_+> and <x_- x_-> have specific values
    # x_+ = (q_A + q_B)/sqrt(2), x_- = (q_A - q_B)/sqrt(2)
    # <x_+(0)^2>_{rho_0} = <q_A^2> + <q_B^2> / 2 ... wait, need to be careful

    # Normal modes: Q_+ = (q_A + q_B)/sqrt(2), Q_- = (q_A - q_B)/sqrt(2)
    # P_+ = (p_A + p_B)/sqrt(2), P_- = (p_A - p_B)/sqrt(2)
    # q_A = (Q_+ + Q_-)/sqrt(2)
    # <q_A(t) q_A(0)>_QM = 1/2 [<Q_+(t) Q_+(0)> + <Q_-(t) Q_-(0)>]
    # (cross terms vanish because H_coupled preserves Q_+/Q_- independently)
    #
    # <Q_+(t) Q_+(0)> = <Q_+(0)^2> cos(omega_+ t) + <Q_+(0) P_+(0)>/(omega_+) sin(omega_+ t)
    # In thermal state of uncoupled H:
    # <Q_+(0)^2> = <(q_A+q_B)^2>/2 = (<q_A^2> + <q_B^2>)/2 = (2n_bar+1)/(2*omega)
    # <Q_+(0) P_+(0)> = <(q_A+q_B)(p_A+p_B)>/2 = (<q_A p_A> + <q_B p_B>)/2
    # For thermal state: <q p> = i/2 (from [a, a†] commutation)
    # Actually <q_A p_A>_thermal = Tr[rho q p] - need to compute properly
    # <q p> = <(a+a†)(a†-a)/(2i)> ... let me just do it numerically

    # <Q_+(0)^2>_uncoupled = (2*n_bar+1)/(2*omega)  (since <q_A^2> = <q_B^2> = (2*n_bar+1)/(2*omega))
    # <P_+(0)^2>_uncoupled = omega*(2*n_bar+1)/2
    # <Q_+(0) P_+(0)>_sym = 0 (symmetric state, <q p + p q>/2 = 0 for thermal)

    qq = (2*n_bar + 1) / (2*omega)  # <Q_+^2> = <Q_-^2>
    pp = omega * (2*n_bar + 1) / 2  # <P_+^2> = <P_-^2>

    # <Q_+(t) Q_+(0)> = <Q_+^2> cos(omega_+ t) + <{Q_+, P_+}/2>/(omega_+) sin(omega_+ t)
    # The symmetric part <{q,p}/2> = 0 for thermal states (time-reversal symmetry)
    # So:
    C_QM_analytical = 0.5 * (qq * np.cos(omega_p * tau_arr) + qq * np.cos(omega_m * tau_arr))

    diff_qm_analytic = norm(C_QM - C_QM_analytical) / norm(C_QM)
    print(f"lam={lam}: ||C_QM - analytical_QM|| / ||C_QM|| = {diff_qm_analytic:.2e}")

    if diff_qm_analytic < 0.01:
        print(f"  GOOD: Numerical matches analytical formula")
        print(f"  C_QM(t) = (2n+1)/(4*omega) [cos(omega_+ t) + cos(omega_- t)]")
        print(f"  C_global(t) = (2n+1)/(2*omega) cos(omega t)")
        print(f"  Discrepancy = beating between cos(omega_+ t) and cos(omega_- t) vs single cos(omega t)")
    else:
        print(f"  MISMATCH: analytical formula needs correction")
        # Could be missing <P^2>/(omega^2) contribution
        # Full formula: <Q(t) Q(0)> = <Q^2> cos(wt) + <QP+PQ>/2 * sin(wt)/w
        # For free oscillator in non-eigenstate:
        # <Q_+(t) Q_+(0)> = <Q_+^2> cos(w_+ t) (since <{Q,P}/2>=0 for thermal state of Q with different w)
        # Wait - but Q_+ is not thermally distributed w.r.t. w_+
        # We need: <Q_+(t)Q_+(0)> with Q_+(t) = Q_+(0)cos(w_+t) + P_+(0)sin(w_+t)/w_+
        # = <Q_+^2>cos(w_+t) + <Q_+ P_+>sin(w_+t)/w_+
        # In the uncoupled thermal state, <Q_+ P_+> = <(q_A+q_B)(p_A+p_B)>/2
        # = (<q_A p_A> + <q_B p_B>)/2
        # For single-mode thermal state: <q p> = <(a+a†)(a†-a)>/(2i) = <a a† - a† a>/(2i) = 1/(2i)
        # Wait: <q p> = Tr[rho q p] is not necessarily real
        # Let me compute <q_A p_A> for thermal state of n_A directly:
        print(f"  Computing <q p> numerically...")
        qp = np.trace(rho_0 @ np.kron(q_op @ (1j*(ad_op - a_op)/np.sqrt(2)), I_N)).real
        print(f"  <q_A p_A> = {qp:.6e} (should be ~i/2 imaginary, real part ~0)")


# Save spectral results
save_dir = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-002/explorations/exploration-002/code/"
with open(save_dir + "spectral_results.json", "w") as f:
    json.dump(spectral_results, f, indent=2)

print(f"\nSpectral results saved.")
print("DONE — spectral analysis")
