"""
Analyze the off-diagonal structure of delta_K_A at lambda=0.3.
The key question: is delta_K_A a 'simple' operator (a few terms)
or does it have a complex structure?
"""
import numpy as np
from scipy.linalg import expm
from numpy.linalg import norm, eigh

N = 20
omega_A = 1.0
omega_B = 1.0
beta = 2.0

n_op = np.diag(np.arange(N, dtype=float))
a_op = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op = (a_op + ad_op) / np.sqrt(2)
p_op = 1j * (ad_op - a_op) / np.sqrt(2)
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

def compute_rho_A_KA(lam):
    H_AB = H_A + H_B + lam * H_int_base
    rho_AB = expm(-beta * H_AB)
    rho_AB /= np.trace(rho_AB).real
    rho_A = partial_trace_B(rho_AB, N)
    rho_A = (rho_A + rho_A.conj().T) / 2
    evals, evecs = eigh(rho_A)
    log_evals = -np.log(np.maximum(evals, 1e-300))
    K_A = evecs @ np.diag(log_evals) @ evecs.T
    return rho_A.real, K_A.real

lam = 0.30
rho_A, K_A = compute_rho_A_KA(lam)

# Compute delta_K
diff = K_A - beta * H_A_red
c = np.trace(diff) / N
delta_K = (diff - c * np.eye(N)).real

print("="*60)
print(f"Off-diagonal structure of delta_K at lambda={lam}")
print("="*60)
print(f"Total ||delta_K||_F = {norm(delta_K, 'fro'):.4f}")
print(f"Diagonal contribution: {norm(np.diag(delta_K.diagonal()), 'fro'):.4f}")
print(f"Off-diagonal contribution: {norm(delta_K - np.diag(delta_K.diagonal()), 'fro'):.4f}")

# Show off-diagonal sparsity structure
print("\nOff-diagonal elements |delta_K[i,j]| > 0.05:")
count = 0
for i in range(N):
    for j in range(i+1, N):
        if abs(delta_K[i,j]) > 0.05:
            print(f"  [{i},{j}]: {delta_K[i,j]:.4f}  (i-j = {j-i})")
            count += 1
print(f"Total non-trivial off-diagonal pairs: {count}")

# Check: what is the pattern? delta_K[i,j] vs |i-j|
print("\n||delta_K|| by band (off-diagonal distance k):")
for k in range(1, 10):
    band_vals = [delta_K[i, i+k] for i in range(N-k)]
    band_norm = norm(band_vals)
    print(f"  Band {k}: ||.||_2 = {band_norm:.4f}, max = {max(abs(v) for v in band_vals):.4f}")

# Key operators to project onto
# K_A = sum_n coeff_n * O_n
operators = {
    "I": I_N,
    "n": n_op,
    "n^2": n_op @ n_op,
    "q^2": q_op @ q_op,
    "p^2": (p_op @ p_op).real,
    "qp+pq": (q_op @ p_op + p_op @ q_op).real,  # angular momentum type
    "q": q_op,  # only non-zero off-diagonals in bands 1,3,5,...
    "q^3": (q_op @ q_op @ q_op).real,
    "q^4": (q_op @ q_op @ q_op @ q_op).real,
    "a†a†+aa": (ad_op@ad_op + a_op@a_op).real,  # squeezing
    "a†a†a†a+h.c.": (ad_op@ad_op@a_op + a_op@a_op@ad_op).real,
}

print("\n" + "="*60)
print("Projection of delta_K onto simple operators (overlap/||op||)")
print("="*60)
for name, op in operators.items():
    # Hilbert-Schmidt inner product: <A,B> = Tr[A†B]
    op_normalized = op / norm(op, 'fro')
    overlap = np.trace(delta_K @ op_normalized) / norm(delta_K, 'fro')
    print(f"  {name:20s}: overlap = {overlap:.4f}")

# ============================================================
# Compute delta_K via operator decomposition
# ============================================================
# Try to decompose delta_K as: c1*(n - <n>) + c2*(q^2 - <q^2>) + c3*...
# using least squares over a basis
basis = [n_op, q_op@q_op, a_op@a_op + ad_op@ad_op, q_op@q_op@q_op@q_op]
basis_names = ["n", "q^2", "a^2+a†^2", "q^4"]

# Vectorize
delta_K_vec = delta_K.flatten()
A_mat = np.column_stack([op.flatten() for op in basis])

# Least squares: delta_K ≈ sum_i c_i * basis_i
result = np.linalg.lstsq(A_mat, delta_K_vec, rcond=None)
coeffs = result[0]
residual = delta_K_vec - A_mat @ coeffs
print("\nLeast-squares decomposition of delta_K:")
for name, c in zip(basis_names, coeffs):
    print(f"  {name}: coefficient = {c:.6f}")
print(f"  Residual fraction: {norm(residual)/norm(delta_K_vec):.4f}")

# ============================================================
# The O(lambda^2) operator analytically
# ============================================================
print("\n" + "="*60)
print("Analytic O(lambda^2) prediction for ΔK_A")
print("="*60)
print("""
At O(λ²), the correction to ρ_A comes from second-order Duhamel:
  δ²ρ_A = λ² * [second-order Kubo-Martin-Schwinger correlation]

For H_int = q_A ⊗ q_B, the correction involves:
  ΔK_A ≈ -λ² * ∫₀^β ds₁ ∫₀^{s₁} ds₂ C_B(s₁-s₂) * [ρ_A^{s₂} q_A ρ_A^{β-s₁} q_A ρ_A^{s₁-s₂} + ...]

where C_B(s) = Tr[ρ_B q_B(s) q_B(0)] is the thermal 2-point function of B.

The key structure: ΔK_A contains terms like q_A * [ρ_A^s terms] * q_A,
which are typically NOT proportional to H_A alone.

The structure is related to the 'modular operator' ΔK = ∫₀^β ds J_s(H_int)
where J_s is the modular conjugation at parameter s.
""")

# Check: does KA have the form beta * H_A + lambda^2 * something?
lam_small = 0.05
_, K_A_small = compute_rho_A_KA(lam_small)
diff_small = K_A_small - beta * H_A_red
c_small = np.trace(diff_small) / N
delta_K_small = (diff_small - c_small * np.eye(N)).real

# Scale to lambda^0: delta_K / lambda^2
dK_scaled = delta_K_small / lam_small**2
print(f"delta_K at lambda=0.05, scaled by 1/lambda^2:")
print(f"  Diagonal (first 6): {dK_scaled.diagonal()[:6]}")
print(f"  Off-diag [0,2]: {dK_scaled[0,2]:.4f} (from q^2 term)")
print(f"  Off-diag [0,4]: {dK_scaled[0,4]:.4f} (from q^4 term)")

dK_scaled_big = delta_K / 0.3**2
print(f"\ndelta_K at lambda=0.3, scaled by 1/lambda^2:")
print(f"  Diagonal (first 6): {dK_scaled_big.diagonal()[:6]}")
print(f"  Off-diag [0,2]: {dK_scaled_big[0,2]:.4f}")
print(f"  Off-diag [0,4]: {dK_scaled_big[0,4]:.4f}")

# Compare: are the shapes the same?
frac_same = np.dot(dK_scaled.flatten(), dK_scaled_big.flatten()) / (norm(dK_scaled.flatten()) * norm(dK_scaled_big.flatten()))
print(f"\nShape similarity (cosine) between lambda=0.05 and lambda=0.3 (scaled): {frac_same:.4f}")
print("(1.0 = same shape, confirming pure O(lambda^2) behavior)")
