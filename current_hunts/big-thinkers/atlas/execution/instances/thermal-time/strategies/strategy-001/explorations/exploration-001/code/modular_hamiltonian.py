"""
Modular Hamiltonian Computation for TTH vs Standard QM Comparison

This script computes:
1. Modular Hamiltonian K for a harmonic oscillator in a thermal state
2. Modular flow sigma_t(x_A) for the position operator
3. Standard QM Heisenberg evolution of x_A
4. Lindblad decoherence rate for a coupled system
5. Comparison plot of TTH (modular flow) vs Standard QM trajectories

System: Two coupled harmonic oscillators A and B at different temperatures.
  H = omega_A * a†a + omega_B * b†b + lambda * (a†b + ab†)
  rho_AB = rho_A(beta_A) x rho_B(beta_B)

Author: Atlas Explorer (automated)
Date: 2026-03-27
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm, logm

# ============================================================
# Parameters
# ============================================================
omega_A = 1.0       # oscillator A frequency
omega_B = 1.0       # oscillator B frequency
beta_A  = 2.0       # inverse temperature for A (cold)
beta_B  = 0.5       # inverse temperature for B (hot)
lam     = 0.1       # coupling strength
N_max   = 15        # Fock space truncation (N_max + 1 levels)

print("=" * 60)
print("MODULAR HAMILTONIAN COMPUTATION")
print("=" * 60)
print(f"omega_A = {omega_A}, beta_A = {beta_A}  (T_A = {1/beta_A:.2f})")
print(f"omega_B = {omega_B}, beta_B = {beta_B}  (T_B = {1/beta_B:.2f})")
print(f"coupling lambda = {lam}")
print(f"Fock truncation: N_max = {N_max}")
print()

# ============================================================
# Build single-mode operators in truncated Fock space
# ============================================================
N = N_max + 1  # dimension

def creation_op(N):
    """Creation operator a† in Fock space truncated to N levels."""
    a_dag = np.zeros((N, N), dtype=complex)
    for n in range(N - 1):
        a_dag[n+1, n] = np.sqrt(n + 1)
    return a_dag

def annihilation_op(N):
    """Annihilation operator a in Fock space truncated to N levels."""
    return creation_op(N).conj().T

def number_op(N):
    return np.diag([n for n in range(N)], k=0).astype(complex)

# Single-mode operators
a_dag = creation_op(N)
a     = annihilation_op(N)
n_op  = number_op(N)
Id    = np.eye(N, dtype=complex)

# Position and momentum operators (dimensionless, m=1)
x = (a + a_dag) / np.sqrt(2)
p = 1j * (a_dag - a) / np.sqrt(2)

print("Single-mode operators built:")
print(f"  Hilbert space dimension: {N}")
print(f"  Commutator [a, a†] trace check: {np.trace(a @ a_dag - a_dag @ a):.4f}  (expect N={N})")
print()

# ============================================================
# Part 1: Modular Hamiltonian for thermal state
# ============================================================
print("-" * 40)
print("PART 1: MODULAR HAMILTONIANS")
print("-" * 40)

# Thermal state for oscillator A: rho_A = e^{-beta_A * H_A} / Z_A
H_A = omega_A * n_op  # = omega_A * diag(0, 1, 2, ...)

# Density matrix (exactly diagonal in Fock basis)
energies_A = omega_A * np.arange(N)
boltzmann_A = np.exp(-beta_A * energies_A)
Z_A = np.sum(boltzmann_A)
rho_A = np.diag(boltzmann_A / Z_A)

print("Thermal density matrix rho_A = e^{-beta_A H_A} / Z_A:")
print(f"  Z_A = {Z_A:.6f}")
print(f"  Tr[rho_A] = {np.trace(rho_A).real:.6f}  (should be 1.0)")
print(f"  Mean occupation <n_A> = {np.trace(rho_A @ n_op).real:.4f}")
print(f"  Expected n̄_A = 1/(e^{{beta_A*omega_A}}-1) = {1/(np.exp(beta_A*omega_A)-1):.4f}")
print()

# Modular Hamiltonian K_A = -log(rho_A)
# Since rho_A is diagonal: K_A = -log(rho_A) = beta_A * H_A + log(Z_A) * I
K_A_direct = beta_A * H_A + np.log(Z_A) * Id

# Verify via matrix log
K_A_matrix = -np.real(logm(rho_A))  # should match

print("Modular Hamiltonian K_A = -log(rho_A):")
print(f"  K_A = beta_A * H_A + log(Z_A) * I")
print(f"  beta_A * omega_A = {beta_A * omega_A:.4f}")
print(f"  log(Z_A) = {np.log(Z_A):.4f}")
print(f"  Max element (direct) = {np.max(np.abs(K_A_direct)):.4f}")
print(f"  Max element (matrix log) = {np.max(np.abs(K_A_matrix)):.4f}")
print(f"  Agreement: {np.allclose(K_A_direct, K_A_matrix, atol=1e-6)}")
print()

# Same for B
H_B = omega_B * n_op
energies_B = omega_B * np.arange(N)
boltzmann_B = np.exp(-beta_B * energies_B)
Z_B = np.sum(boltzmann_B)
rho_B = np.diag(boltzmann_B / Z_B)
K_B_direct = beta_B * H_B + np.log(Z_B) * Id

print(f"Thermal density matrix rho_B: Z_B = {Z_B:.4f}, Tr = {np.trace(rho_B).real:.4f}")
print(f"  <n_B> = {np.trace(rho_B @ n_op).real:.4f}, n̄_B = {1/(np.exp(beta_B*omega_B)-1):.4f}")
print()

# ============================================================
# Part 2: Modular Flow sigma_t(x_A)
# ============================================================
print("-" * 40)
print("PART 2: MODULAR FLOW")
print("-" * 40)

# Using K_A (without the constant log(Z) term, which doesn't affect flow):
K_A_flow = beta_A * H_A  # The constant drops out in the commutator

def modular_flow(A, K, t):
    """Compute sigma_t(A) = e^{itK} A e^{-itK}"""
    eitK = expm(1j * t * K)
    e_mitK = expm(-1j * t * K)
    return eitK @ A @ e_mitK

# TTH correlation function: C_TTH(t) = Tr[rho_A * sigma_t(x_A) * x_A]
def C_TTH(t):
    """TTH autocorrelation via modular flow."""
    x_t = modular_flow(x, K_A_flow, t)
    return np.trace(rho_A @ x_t @ x).real

# Standard QM correlation function (free oscillator A, no coupling):
def C_QM_free(t):
    """Standard QM autocorrelation for free oscillator."""
    # Heisenberg: x(t) = x cos(omega_A t) + p sin(omega_A t) / omega_A
    # <x(t) x(0)> = cos(omega_A t) <x^2> + sin(omega_A t)/omega_A <p x>
    x2_mean = np.trace(rho_A @ x @ x).real
    px_mean = np.trace(rho_A @ p @ x).real
    return x2_mean * np.cos(omega_A * t) + px_mean * np.sin(omega_A * t) / omega_A

# Compute frequencies
print("TTH modular flow oscillation:")
print(f"  sigma_t(x_A) = cos(beta_A * omega_A * t) x_A + sin(beta_A * omega_A * t) p_A / omega_A")
print(f"  Frequency = beta_A * omega_A = {beta_A * omega_A:.4f}")
print()
print("Standard QM free oscillation:")
print(f"  x_A(t) = cos(omega_A * t) x_A + sin(omega_A * t) p_A / omega_A")
print(f"  Frequency = omega_A = {omega_A:.4f}")
print()
print(f"Ratio of frequencies: {beta_A * omega_A / omega_A:.4f}  (= beta_A = {beta_A})")
print()

# Compute C_TTH and C_QM at a few points to verify
t_check = [0, np.pi/(4*beta_A*omega_A), np.pi/(2*beta_A*omega_A)]
print("Verification at key time points:")
print(f"{'t':>8}  {'C_TTH':>12}  {'C_QM_free':>12}  {'C_TTH/C_QM':>12}")
for t in t_check:
    c_tth = C_TTH(t)
    c_qm = C_QM_free(t)
    ratio = c_tth / c_qm if abs(c_qm) > 1e-10 else float('inf')
    print(f"{t:8.4f}  {c_tth:12.6f}  {c_qm:12.6f}  {ratio:12.4f}")
print()

# ============================================================
# Part 3: Lindblad decoherence rate
# ============================================================
print("-" * 40)
print("PART 3: LINDBLAD DECOHERENCE RATE")
print("-" * 40)

# Spectral density: J(omega) = gamma_0 (Ohmic)
gamma_0 = lam**2  # effective coupling squared -> decay rate

# Bose-Einstein occupations
n_bar_A = 1 / (np.exp(beta_A * omega_A) - 1)
n_bar_B = 1 / (np.exp(beta_B * omega_B) - 1)

print(f"n̄_A = {n_bar_A:.4f}  (mean photon number in A's thermal state)")
print(f"n̄_B = {n_bar_B:.4f}  (mean photon number in B's thermal state)")
print()

# Decoherence rate (coherence damping) for rho_A evolving with B as bath
# Gamma = gamma_0 * (2*n_bar_B + 1) = gamma_0 * coth(beta_B * omega_B / 2)
Gamma_decoherence = gamma_0 * (2 * n_bar_B + 1)
Gamma_coth = gamma_0 * (np.exp(beta_B*omega_B/2) + np.exp(-beta_B*omega_B/2)) / \
             (np.exp(beta_B*omega_B/2) - np.exp(-beta_B*omega_B/2))

print("Lindblad decoherence rate Gamma = gamma_0 * (2*n_bar_B + 1):")
print(f"  gamma_0 = lambda^2 = {gamma_0:.6f}")
print(f"  2*n_bar_B + 1 = {2*n_bar_B + 1:.4f}")
print(f"  Gamma = {Gamma_decoherence:.6f}")
print(f"  Gamma (coth formula) = {Gamma_coth:.6f}")
print(f"  Decoherence timescale tau_D = 1/Gamma = {1/Gamma_decoherence:.4f}")
print()

print("NOTE: Gamma depends on beta_B (bath temperature) only, NOT on beta_A.")
print("TTH would predict Gamma also depends on beta_A through modular flow mismatch.")
print()

# ============================================================
# Part 4: Compute and plot C(t) for TTH vs Standard QM
# ============================================================
print("-" * 40)
print("PART 4: CORRELATION FUNCTION COMPARISON")
print("-" * 40)

t_max = 3 * np.pi / omega_A  # cover ~1.5 full QM oscillations
t_arr = np.linspace(0, t_max, 500)

print(f"Computing correlation functions over t in [0, {t_max:.4f}]...")

# Standard QM: free oscillation + Lindblad damping
# C_QM(t) = <x_A>^2 + (Var[x_A]) * exp(-Gamma*t) * cos(omega_A * t)
# More precisely for a damped oscillator:
x2_mean = np.trace(rho_A @ x @ x).real
px_mean = np.trace(rho_A @ p @ x).real
print(f"  <x_A^2>_rho_A = {x2_mean:.6f}")
print(f"  Expected: (n̄_A + 1/2) = {n_bar_A + 0.5:.6f}")
print()

# TTH correlation (no damping — modular flow is unitary)
C_tth_arr = np.array([C_TTH(t) for t in t_arr])

# Standard QM free (no coupling, no damping)
C_qm_free_arr = x2_mean * np.cos(omega_A * t_arr) + px_mean * np.sin(omega_A * t_arr) / omega_A

# Standard QM with Lindblad damping
C_qm_damped_arr = C_qm_free_arr * np.exp(-Gamma_decoherence * t_arr / 2)

print("First 5 values of each correlation function:")
print(f"{'t':>8}  {'C_TTH':>12}  {'C_QM_free':>12}  {'C_QM_damped':>14}")
for i in range(0, 25, 5):
    t = t_arr[i]
    print(f"{t:8.4f}  {C_tth_arr[i]:12.6f}  {C_qm_free_arr[i]:12.6f}  {C_qm_damped_arr[i]:14.6f}")
print()

# ============================================================
# Create plots
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    f"TTH Modular Flow vs Standard QM\n"
    f"β_A={beta_A}, β_B={beta_B}, ω_A=ω_B={omega_A}, λ={lam}",
    fontsize=13
)

# Plot 1: Correlation functions
ax1 = axes[0, 0]
ax1.plot(t_arr, C_tth_arr, 'b-', linewidth=2, label=f'TTH: ω_mod={beta_A*omega_A:.1f} (β_A·ω_A)')
ax1.plot(t_arr, C_qm_free_arr, 'r--', linewidth=2, label=f'QM free: ω={omega_A:.1f}')
ax1.plot(t_arr, C_qm_damped_arr, 'r-', linewidth=1.5, alpha=0.7,
         label=f'QM Lindblad: ω={omega_A:.1f}, Γ={Gamma_decoherence:.3f}')
ax1.set_xlabel('Time t')
ax1.set_ylabel('C(t) = ⟨x_A(t) x_A(0)⟩')
ax1.set_title('Autocorrelation Function: TTH vs QM')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='k', linewidth=0.5)

# Plot 2: Modular Hamiltonian spectrum
ax2 = axes[0, 1]
n_vals = np.arange(N)
K_spectrum = beta_A * omega_A * n_vals + np.log(Z_A)  # eigenvalues of K_A
K_spectrum_B = beta_B * omega_B * n_vals + np.log(Z_B)
ax2.bar(n_vals - 0.2, K_spectrum, width=0.35, label=f'K_A (β_A={beta_A})', color='blue', alpha=0.7)
ax2.bar(n_vals + 0.2, K_spectrum_B, width=0.35, label=f'K_B (β_B={beta_B})', color='red', alpha=0.7)
ax2.set_xlabel('Fock level n')
ax2.set_ylabel('K eigenvalue = β·ω·n + log Z')
ax2.set_title('Modular Hamiltonian Spectra')
ax2.legend()
ax2.set_xlim(-0.5, 10.5)
ax2.grid(True, alpha=0.3)

# Plot 3: Thermal state populations
ax3 = axes[1, 0]
pop_A = np.diag(rho_A).real
pop_B = np.diag(rho_B).real
ax3.bar(n_vals - 0.2, pop_A, width=0.35, label=f'ρ_A (β_A={beta_A}, cold)', color='blue', alpha=0.7)
ax3.bar(n_vals + 0.2, pop_B, width=0.35, label=f'ρ_B (β_B={beta_B}, hot)', color='red', alpha=0.7)
ax3.set_xlabel('Fock level n')
ax3.set_ylabel('Population ⟨n|ρ|n⟩')
ax3.set_title('Thermal State Populations')
ax3.legend()
ax3.set_xlim(-0.5, 10.5)
ax3.grid(True, alpha=0.3)
ax3.set_yscale('log')

# Plot 4: Frequency comparison
ax4 = axes[1, 1]
beta_range = np.linspace(0.1, 5.0, 100)
freq_TTH = beta_range * omega_A   # TTH oscillation frequency
freq_QM = np.ones_like(beta_range) * omega_A  # QM oscillation frequency

ax4.plot(beta_range, freq_TTH, 'b-', linewidth=2, label='TTH: ω_TTH = β_A · ω_A')
ax4.plot(beta_range, freq_QM, 'r--', linewidth=2, label='QM: ω_QM = ω_A')
ax4.axvline(x=1.0, color='g', linestyle=':', linewidth=2, label='β_A=1 (agreement point)')
ax4.axvline(x=beta_A, color='purple', linestyle='--', linewidth=1.5,
            label=f'Current β_A={beta_A}')
ax4.set_xlabel('β_A (inverse temperature of A)')
ax4.set_ylabel('Oscillation frequency')
ax4.set_title('TTH vs QM Predicted Frequency')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)
ax4.fill_between(beta_range, freq_TTH, freq_QM,
                 where=(freq_TTH > freq_QM), alpha=0.2, color='blue', label='TTH faster')
ax4.fill_between(beta_range, freq_TTH, freq_QM,
                 where=(freq_TTH < freq_QM), alpha=0.2, color='red', label='QM faster')

plt.tight_layout()
plt.savefig('modular_flow_comparison.png', dpi=150, bbox_inches='tight')
print("Plot saved to: modular_flow_comparison.png")
plt.close()

# ============================================================
# Part 5: Direct matrix computation of modular flow
# ============================================================
print("-" * 40)
print("PART 5: DIRECT MATRIX VERIFICATION OF MODULAR FLOW")
print("-" * 40)

# Verify analytically: sigma_t(x) = cos(beta_A t) x + sin(beta_A t) p
t_test = 0.5
sigma_t_x_numerical = modular_flow(x, K_A_flow, t_test)
sigma_t_x_analytic  = np.cos(beta_A * omega_A * t_test) * x + \
                       np.sin(beta_A * omega_A * t_test) * p / omega_A

diff = np.max(np.abs(sigma_t_x_numerical - sigma_t_x_analytic))
print(f"At t = {t_test}:")
print(f"  sigma_t(x) numerical vs analytic max diff: {diff:.2e}")
print(f"  Agreement: {diff < 1e-6}")
print()

# ============================================================
# Summary output
# ============================================================
print("=" * 60)
print("SUMMARY OF KEY RESULTS")
print("=" * 60)
print()
print("System parameters:")
print(f"  omega_A = {omega_A}, beta_A = {beta_A} -> T_A = {1/beta_A:.2f}")
print(f"  omega_B = {omega_B}, beta_B = {beta_B} -> T_B = {1/beta_B:.2f}")
print()
print("Modular Hamiltonians:")
print(f"  K_A = beta_A * H_A = {beta_A} * omega_A * n_A")
print(f"  K_B = beta_B * H_B = {beta_B} * omega_B * n_B")
print()
print("Modular flow of x_A:")
print(f"  sigma_t(x_A) = cos(beta_A * omega_A * t) x_A + sin(...) p_A / omega_A")
print(f"  Oscillation frequency: {beta_A * omega_A}")
print()
print("TTH prediction for C(t) = <x_A(t) x_A(0)>:")
print(f"  C_TTH(t) = {x2_mean:.4f} * cos({beta_A * omega_A:.2f} * t)")
print()
print("Standard QM prediction:")
print(f"  C_QM(t) = {x2_mean:.4f} * cos({omega_A:.2f} * t) * exp(-{Gamma_decoherence:.4f} * t / 2)")
print()
print("Lindblad decoherence rate:")
print(f"  Gamma = lambda^2 * coth(beta_B * omega_B / 2)")
print(f"        = {lam}^2 * coth({beta_B * omega_B / 2:.2f})")
print(f"        = {Gamma_decoherence:.6f}")
print(f"  Decoherence time = {1/Gamma_decoherence:.4f}")
print()
print("The TTH oscillation frequency ({:.2f}) differs from QM ({:.2f}) by factor beta_A = {}".format(
    beta_A * omega_A, omega_A, beta_A))
print()
print("Discrimination criterion: If the measured C(t) oscillates at omega_A*beta_A")
print("rather than omega_A, TTH is supported (in the absence of a time rescaling).")
