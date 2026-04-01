"""
Detailed analysis of delta_K structure at lambda=0.3
and perturbative validation.
"""
import numpy as np
from scipy.linalg import expm
from numpy.linalg import norm, eigh
import json

N = 20
omega_A = 1.0
omega_B = 1.0
beta = 2.0

n_op = np.diag(np.arange(N, dtype=float))
a_op = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op = (a_op + ad_op) / np.sqrt(2)
I_N = np.eye(N)

H_A = np.kron(omega_A * n_op, I_N)
H_B = np.kron(I_N, omega_B * n_op)
H_int_base = np.kron(q_op, q_op)
H_A_red = omega_A * n_op

def partial_trace_B(rho_AB, N):
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A

def compute_K_A(lam):
    H_AB = H_A + H_B + lam * H_int_base
    rho_AB = expm(-beta * H_AB)
    rho_AB /= np.trace(rho_AB).real
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2
    evals, evecs = eigh(rho_A)
    log_evals = -np.log(np.maximum(evals, 1e-300))
    K_A = evecs @ np.diag(log_evals) @ evecs.T
    return K_A.real

def delta_K(lam):
    K_A = compute_K_A(lam)
    diff = K_A - beta * H_A_red
    c = np.trace(diff) / N
    return (diff - c * np.eye(N)).real, float(c)

# ============================================================
# 1. Structure at lambda=0.3
# ============================================================
print("="*60)
print("1. delta_K structure at lambda=0.3")
print("="*60)
dK_03, c_03 = delta_K(0.30)

print(f"||delta_K||_F = {norm(dK_03, 'fro'):.6f}")
print(f"Max off-diagonal: {np.max(np.abs(dK_03 - np.diag(dK_03.diagonal()))):.6f}")
print(f"Diagonal of delta_K (first 10):")
print(dK_03.diagonal()[:10])

# Check if diagonal: diagonal vs off-diagonal contribution to Frobenius
frob_diag = norm(np.diag(dK_03.diagonal()), 'fro')
frob_offdiag = norm(dK_03 - np.diag(dK_03.diagonal()), 'fro')
print(f"Frobenius norm from diagonal part: {frob_diag:.4f}")
print(f"Frobenius norm from off-diagonal part: {frob_offdiag:.4f}")
print(f"(Off-diag fraction: {frob_offdiag/norm(dK_03,'fro')*100:.1f}%)")

# Fit diagonal: A + B*n + C*n^2
n_arr = np.arange(N)
dK_d = dK_03.diagonal()
coeffs = np.polyfit(n_arr, dK_d, 2)
print(f"\nFit delta_K[n,n] = {coeffs[0]:.6f}*n^2 + {coeffs[1]:.6f}*n + {coeffs[2]:.6f}")
print(f"  (If linear: coeffs[0]~0, coeffs[1]~Δβ*ω_A)")
print(f"  => Δβ ≈ {coeffs[1]/omega_A:.4f} (effective beta shift = {beta + coeffs[1]/omega_A:.4f})")
print(f"  => Linear residual: {norm(dK_d - np.polyval(coeffs[:2] if coeffs[0] < 1e-6 else coeffs, n_arr), 2):.4f}")

# Check if delta_K proportional to n^2 - <n^2> (q^2 operator)
# q^2 = (a + a†)^2 / 2 = (2a†a + 1)/2 = n + 1/2
q2_op = q_op @ q_op  # = (n + 1/2)*I + off-diagonal terms
print(f"\nq^2 operator diagonal: {(q_op @ q_op).diagonal()[:5]}")
print(f"n+1/2 sequence: {np.arange(N)[:5] + 0.5}")

# Correlation with q^2 diagonal
q2_d = (q_op @ q_op).diagonal()
q2_d_centered = q2_d - np.mean(q2_d)
dK_d_centered = dK_d - np.mean(dK_d)
corr_q2 = np.dot(q2_d_centered, dK_d_centered) / (norm(q2_d_centered) * norm(dK_d_centered))
print(f"Correlation of delta_K diagonal with q^2 diagonal: {corr_q2:.4f}")

# ============================================================
# 2. Perturbative scaling: fine scan at small lambda
# ============================================================
print("\n" + "="*60)
print("2. Fine scan at small lambda for O(lambda^p) scaling")
print("="*60)
small_lambdas = [0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20]
frobs = []
for lam in small_lambdas:
    dK, _ = delta_K(lam)
    f = norm(dK, 'fro')
    frobs.append(f)
    print(f"  lambda={lam:.3f}: ||dK||_F = {f:.8f}")

# Fit power law
log_lam = np.log(small_lambdas)
log_frob = np.log(frobs)
p, a = np.polyfit(log_lam, log_frob, 1)
print(f"\nPower law fit: ||dK|| ~ {np.exp(a):.4f} * lambda^{p:.4f}")
print(f"=> ΔK_A is O(lambda^{p:.1f}) [expect 2 for second-order perturbation theory]")

# Ratio test for confirming O(lambda^2)
print("\nRatio test ||dK(2λ)|| / ||dK(λ)|| (should be ~4 for O(λ²)):")
for i in range(len(small_lambdas)-1):
    if small_lambdas[i+1] / small_lambdas[i] == 2.0:
        print(f"  {small_lambdas[i]:.3f} → {small_lambdas[i+1]:.3f}: ratio = {frobs[i+1]/frobs[i]:.4f}")

# ============================================================
# 3. Analytic first-order perturbation theory check
# ============================================================
print("\n" + "="*60)
print("3. Why is delta_K O(lambda^2) not O(lambda)?")
print("  (Perturbation theory: KMS correlation argument)")
print("="*60)
print("""
At O(λ), the change in ρ_AB from the coupling λ*q_A⊗q_B satisfies:
  δρ_AB = -β ∫₀¹ ds ρ_AB^{(0),s} (λ H_int) ρ_AB^{(0),1-s}
         (Duhamel / Dyson expansion at first order)

For product state ρ_AB^{(0)} = ρ_A^{(0)} ⊗ ρ_B^{(0)}:
  δρ_A = Tr_B[δρ_AB] = -λβ ∫₀¹ ds Tr_B[ρ_A^s ⊗ ρ_B^s (q_A⊗q_B) ρ_A^{1-s} ⊗ ρ_B^{1-s}]
        = -λβ ∫₀¹ ds (ρ_A^s q_A ρ_A^{1-s}) Tr[ρ_B^s q_B ρ_B^{1-s}]

Now: Tr[ρ_B^s q_B ρ_B^{1-s}] = Tr[ρ_B q_B] by cyclicity (since q_B is linear)
    = ⟨q_B⟩ = 0  (q_B = (b + b†)/√2, zero mean in thermal state)

Therefore δρ_A = 0 at first order in λ!
=> ΔK_A = O(λ²) confirmed analytically.
""")

# Verify: <q_B> = 0 in thermal state
rho_B_thermal = np.diag(np.exp(-beta * np.arange(N)))
rho_B_thermal /= rho_B_thermal.trace()
print(f"Verification: <q_B> = Tr[rho_B * q_B] = {np.trace(rho_B_thermal @ q_op):.2e} (should be 0)")
print(f"Verification: <q_A> = {np.trace(rho_B_thermal @ q_op):.2e} (should be 0)")

# ============================================================
# 4. What operator IS delta_K?
# ============================================================
print("\n" + "="*60)
print("4. What operator is delta_K proportional to at O(λ²)?")
print("="*60)
# At O(λ²), ΔK_A should be related to the two-point function of H_int
# The correction to K_A involves: <q_A q_A>_β and <q_B q_B>_β
# Specifically: ΔK_A = λ² * something involving q_A^2 - <q_A^2>

# q_A^2 = (a + a†)^2/2 = (2a†a + a^2 + a†^2 + 1)/2
# In Fock basis: q^2[n,n] = n + 1/2

# Check: does delta_K at small lambda have the structure of q_A^2 (minus mean)?
lam_small = 0.05
dK_small, _ = delta_K(lam_small)

# q_A^2 diagonal
q2_diag = (q_op @ q_op).diagonal()
q2_centered = q2_diag - np.mean(q2_diag)

# Fit delta_K to q2_centered
scale_q2 = np.dot(dK_small.diagonal(), q2_centered) / np.dot(q2_centered, q2_centered)
residual_q2 = dK_small.diagonal() - scale_q2 * q2_centered
print(f"At lambda={lam_small}:")
print(f"  Fit coeff for q^2: {scale_q2:.6f}")
print(f"  Residual norm (||dK - c*q^2||): {norm(residual_q2):.6f} vs ||dK||: {norm(dK_small.diagonal()):.6f}")
print(f"  delta_K ≈ {scale_q2:.4f} * (q^2 - <q^2>): quality = {1 - norm(residual_q2)/norm(dK_small.diagonal()):.4f}")

# Also check n^2 operator (q^2 off-diagonal terms negligible for diagonal part)
# The diagonal of q^2 is n + 1/2 which is linear! So q^2 diagonal ~ n, linear.
print(f"\nq^2 diagonal = n + 1/2 (linear in n), so delta_K diagonal ≈ linear in n")
print(f"=> delta_K ≈ Δβ * H_A + const, i.e., renormalization of inverse temperature")
print(f"=> Effective beta_A shift: Δβ ≈ {coeffs[1]:.4f} at lambda=0.3")

# At O(λ²), the shift should scale as λ²
dK_shifts = []
test_lams = [0.1, 0.2, 0.3, 0.4, 0.5]
for lam in test_lams:
    dK, c_val = delta_K(lam)
    # Linear fit to diagonal
    cc = np.polyfit(n_arr[:12], dK.diagonal()[:12], 1)  # use first 12 points
    dK_shifts.append(cc[0])  # slope = Δβ * omega_A

print(f"\nΔβ (effective beta shift for A) vs lambda:")
for i, lam in enumerate(test_lams):
    print(f"  lambda={lam:.1f}: Δβ ≈ {dK_shifts[i]:.4f}, expected O(lam^2) ~ {-0.42*lam**2:.4f}")

# Fit Δβ ~ lambda^p
p_shift, a_shift = np.polyfit(np.log(test_lams), np.log(np.abs(dK_shifts)), 1)
print(f"\nΔβ scaling: Δβ ~ lambda^{p_shift:.2f} (expect 2.0 for O(λ²))")
