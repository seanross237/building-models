"""
FFT analysis with higher resolution to see beat structure in C_full.
Extend tau window to 20*pi to resolve omega_+ and omega_- separately.
"""
import numpy as np
from scipy.linalg import expm
from numpy.linalg import eigh, norm
import json

N = 20; beta = 2.0; omega_A = omega_B = 1.0
n_op  = np.diag(np.arange(N, dtype=float))
a_op  = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op  = (a_op + ad_op) / np.sqrt(2)
I_N   = np.eye(N)

H_A_2mode  = np.kron(omega_A * n_op, I_N)
H_B_2mode  = np.kron(I_N, omega_B * n_op)
H_int_base = np.kron(q_op, q_op)
x_A_2mode  = np.kron(q_op, I_N)
x_A_1mode  = q_op

def partial_trace_B(rho_AB, N):
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N): rho_A += rho_AB[k::N, k::N]
    return rho_A

def compute_K_A(rho_AB, N):
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2
    evals_A, evecs_A = eigh(rho_A)
    log_evals = -np.log(np.maximum(evals_A, 1e-300))
    K_A = (evecs_A @ np.diag(log_evals) @ evecs_A.T).real
    return K_A, rho_A.real

def compute_correlator(H_mat, rho_mat, x_op, tau_arr):
    evals, evecs = eigh(H_mat)
    rho_eig = evecs.conj().T @ rho_mat @ evecs
    x_eig   = evecs.conj().T @ x_op   @ evecs
    xrho = x_eig @ rho_eig
    B    = x_eig * xrho.T
    conj_phase = np.exp(-1j * np.outer(tau_arr, evals))
    phase      = conj_phase.conj()
    inner = B @ conj_phase.T
    return np.sum(phase * inner.T, axis=1).real

# High-resolution time window to resolve beat structure
tau_long = np.linspace(0, 20 * np.pi, 2000)

print("High-resolution FFT analysis")
print("="*60)

fft_results = {}
for lam in [0.1, 0.2, 0.3, 0.5]:
    H_AB   = H_A_2mode + H_B_2mode + lam * H_int_base
    rho_AB = expm(-beta * H_AB); rho_AB /= np.trace(rho_AB).real
    K_A, rho_A = compute_K_A(rho_AB, N)

    omega_plus  = np.sqrt(omega_A**2 + lam)
    omega_minus = np.sqrt(omega_A**2 - lam)

    C_full  = compute_correlator(H_AB,      rho_AB, x_A_2mode, tau_long)
    C_local = compute_correlator(K_A/beta,  rho_A,  x_A_1mode, tau_long)

    # FFT
    dt = tau_long[1] - tau_long[0]
    def fft_spectrum(C):
        fft_v = np.fft.rfft(C - C.mean())
        freqs = np.fft.rfftfreq(len(C), d=dt) * 2 * np.pi  # angular freq
        amps  = np.abs(fft_v)
        return freqs, amps

    freqs_f, amps_f = fft_spectrum(C_full)
    freqs_l, amps_l = fft_spectrum(C_local)

    # Find peaks: look for local maxima with amp > 5% of max
    def find_peaks(freqs, amps, min_frac=0.05, freq_range=(0.1, 5.0)):
        mask = (freqs > freq_range[0]) & (freqs < freq_range[1])
        f, a = freqs[mask], amps[mask]
        threshold = min_frac * a.max()
        peaks = []
        for i in range(1, len(a)-1):
            if a[i] > threshold and a[i] > a[i-1] and a[i] > a[i+1]:
                peaks.append((f[i], a[i]))
        return sorted(peaks, key=lambda x: -x[1])[:8]

    peaks_full  = find_peaks(freqs_f, amps_f)
    peaks_local = find_peaks(freqs_l, amps_l)

    print(f"\nlambda = {lam}")
    print(f"  Predicted: omega_+ = {omega_plus:.4f}, omega_- = {omega_minus:.4f}")
    print(f"  C_full  peaks (omega, amp):")
    for (f, a) in peaks_full[:6]:
        flag = ""
        if abs(f - omega_plus) < 0.05:  flag = " <- omega_+"
        if abs(f - omega_minus) < 0.05: flag = " <- omega_-"
        if abs(f - (omega_plus + omega_minus)) < 0.05: flag = " <- omega_+ + omega_-"
        print(f"    {f:.4f}  amp={a:.2f}{flag}")
    print(f"  C_local peaks (omega, amp):")
    for (f, a) in peaks_local[:4]:
        print(f"    {f:.4f}  amp={a:.2f}")

    # Check if omega_+ and omega_- are resolved in C_full
    found_plus  = any(abs(f - omega_plus)  < 0.03 for f, _ in peaks_full)
    found_minus = any(abs(f - omega_minus) < 0.03 for f, _ in peaks_full)
    print(f"  omega_+ found in C_full: {found_plus}")
    print(f"  omega_- found in C_full: {found_minus}")

    # Effective frequency from C_local dominant peak
    if peaks_local:
        omega_eff = peaks_local[0][0]
        print(f"  C_local dominant freq (omega_eff) = {omega_eff:.4f}")
        print(f"  Predicted omega_eff = omega_A * (beta/beta_eff), beta_eff = beta - 1.36*lam^2")
        beta_eff = beta - 1.36 * lam**2
        omega_eff_pred = omega_A * (beta / beta_eff)
        print(f"  Predicted omega_eff = {omega_eff_pred:.4f} (beta_eff={beta_eff:.4f})")

    # Save full spectrum for the report
    fft_results[str(lam)] = {
        "lambda": lam, "omega_plus": omega_plus, "omega_minus": omega_minus,
        "peaks_full": peaks_full, "peaks_local": peaks_local,
        "freqs_sample": freqs_f[1:100].tolist(),
        "amps_full_sample": amps_f[1:100].tolist(),
        "amps_local_sample": amps_l[1:100].tolist(),
    }

# Also load the main results and print final summary
save_dir = "/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-003/code/"
with open(save_dir + "fft_results.json", "w") as f:
    import json
    json.dump(fft_results, f, indent=2, default=lambda x: float(x) if hasattr(x,'__float__') else str(x))

print("\nDONE")
