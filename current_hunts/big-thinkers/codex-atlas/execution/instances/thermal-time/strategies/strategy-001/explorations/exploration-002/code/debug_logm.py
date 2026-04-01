"""
Debug the logm issue at lambda=0.
At lambda=0, K_A should equal beta*H_A_red + const*I exactly (up to machine precision).
But we're getting Frobenius norm ~3.85. Let's find why.
"""

import numpy as np
from scipy.linalg import expm, logm
from numpy.linalg import norm

N = 20
omega_A = 1.0
beta = 2.0
n_op = np.diag(np.arange(N, dtype=float))
a_op = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1)
ad_op = a_op.T
q_op = (a_op + ad_op) / np.sqrt(2)
I_N = np.eye(N)

H_A = np.kron(omega_A * n_op, I_N)
H_B = np.kron(I_N, omega_A * n_op)

# lambda = 0: product state
rho_AB = expm(-beta * H_A) @ expm(-beta * H_B)
Z = np.trace(rho_AB).real
rho_AB /= Z

print("rho_AB diagonal (first 10 elements):")
print(rho_AB.diagonal()[:10])
print("rho_AB off-diagonal max:", np.max(np.abs(rho_AB - np.diag(rho_AB.diagonal()))))

# Partial trace
def partial_trace_B(rho_AB, N):
    rho_A = np.zeros((N, N), dtype=complex)
    for k in range(N):
        rho_A += rho_AB[k::N, k::N]
    return rho_A

rho_A = partial_trace_B(rho_AB, N)
rho_A = (rho_A + rho_A.conj().T) / 2
print("\nrho_A diagonal (all 20):")
print(rho_A.diagonal().real)
print("rho_A off-diagonal max:", np.max(np.abs(rho_A - np.diag(rho_A.diagonal()))))

# Eigendecomposition of rho_A
evals, evecs = np.linalg.eigh(rho_A)
print("\nrho_A eigenvalues (sorted ascending):")
print(evals)

# Expected values: p_n = exp(-beta*n) / Z_A
Z_A = np.sum(np.exp(-beta * np.arange(N)))
p_n = np.exp(-beta * np.arange(N)) / Z_A
print("\nExpected p_n (descending order = matches evals ascending when reversed):")
print(p_n[::-1][:10])  # last few (smallest) first

# Check if rho_A diagonal matches expected:
print("\nActual rho_A diagonal vs expected p_n:")
rho_A_diag = rho_A.diagonal().real
for n in range(N):
    diff = rho_A_diag[n] - p_n[n]
    print(f"n={n:2d}: actual={rho_A_diag[n]:.6e}, expected={p_n[n]:.6e}, diff={diff:.2e}")

# Now compute logm two ways:
# Way 1: scipy logm
K_A_scipy = -logm(rho_A).real

# Way 2: eigendecomposition
K_A_eig = -evecs @ np.diag(np.log(np.maximum(evals, 1e-100))) @ evecs.T

print("\nK_A (scipy logm) diagonal:")
print(K_A_scipy.diagonal()[:10])
print("\nK_A (eigendecomp) diagonal:")
print(K_A_eig.diagonal()[:10])

# Expected K_A diagonal: beta*n + log(Z_A)
K_A_expected_diag = beta * np.arange(N) + np.log(Z_A)
print("\nExpected K_A diagonal (beta*n + log(Z_A)):")
print(K_A_expected_diag[:10])

# Check off-diagonal elements
print("\nK_A scipy off-diagonal max:", np.max(np.abs(K_A_scipy - np.diag(K_A_scipy.diagonal()))))
print("K_A eigendecomp off-diagonal max:", np.max(np.abs(K_A_eig - np.diag(K_A_eig.diagonal()))))

# Compute delta_K for both methods
H_A_red = omega_A * n_op

def delta_K_norm(K_A, H_A_red, N):
    diff = K_A - beta * H_A_red
    c = np.trace(diff).real / N
    delta_K = diff - c * np.eye(N)
    return norm(delta_K, 'fro'), c

frob_scipy, c_scipy = delta_K_norm(K_A_scipy, H_A_red, N)
frob_eig, c_eig = delta_K_norm(K_A_eig, H_A_red, N)
print(f"\ndelta_K Frobenius norm (scipy logm): {frob_scipy:.6f}")
print(f"delta_K Frobenius norm (eigendecomp): {frob_eig:.6f}")
print(f"Expected: ~0")
