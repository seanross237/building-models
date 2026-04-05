"""
Stage 4: Characterize the gap and the curvature correction C(Q).
Focus on understanding WHY the inequality holds.
"""
import numpy as np
from numpy.linalg import eigvalsh, norm, eigh, inv
import sys

sys.path.insert(0, '.')
from fast_hessian import (
    Lattice, su2_exp, haar_random_su2, project_su2,
    T, I2, compute_hessian_fd, compute_hessian_formula,
    compute_ratio_data, random_su2_config,
)


def analyze_config(Q, lattice, beta, label=""):
    """Full analysis of a single configuration."""
    print(f"\n{'='*60}")
    print(f"Analysis: {label}")
    print(f"{'='*60}")

    res = compute_ratio_data(Q, lattice, beta)

    print(f"r(Q) = {res['r']:.10f}")
    print(f"λ_max(H_actual) = {res['lmax_actual']:.8f}")
    print(f"λ_max(H_formula) = {res['lmax_formula']:.8f}")
    print(f"Gap = {1 - res['r']:.8f}")

    C = res['H_formula'] - res['H_actual']
    eigs_C = res['eigs_C']

    print(f"\nCurvature correction C = H_formula - H_actual:")
    print(f"  ||C||_op = {res['C_norm']:.6f}")
    print(f"  λ_min(C) = {eigs_C[0]:.6f}")
    print(f"  λ_max(C) = {eigs_C[-1]:.6f}")
    print(f"  # positive eigenvalues: {np.sum(eigs_C > 1e-8)}")
    print(f"  # negative eigenvalues: {np.sum(eigs_C < -1e-8)}")
    print(f"  # near-zero eigenvalues: {np.sum(np.abs(eigs_C) < 1e-8)}")
    print(f"  Tr(C) = {np.sum(eigs_C):.6f}")
    print(f"  ||C⁺||_F = {norm(eigs_C[eigs_C > 0]):.6f}")  # Frobenius of positive part
    print(f"  ||C⁻||_F = {norm(eigs_C[eigs_C < 0]):.6f}")  # Frobenius of negative part

    # Top eigenvector alignment
    _, vecs_a = eigh(res['H_actual'])
    v_top_a = vecs_a[:, -1]

    _, vecs_f = eigh(res['H_formula'])
    v_top_f = vecs_f[:, -1]

    # What does C do to the top eigenvectors?
    c_on_va = v_top_a @ C @ v_top_a
    c_on_vf = v_top_f @ C @ v_top_f

    print(f"\nTop eigenvector alignment:")
    print(f"  v_a^T C v_a = {c_on_va:.8f} ({'positive → helps inequality' if c_on_va > 0 else 'NEGATIVE → hurts inequality'})")
    print(f"  v_f^T C v_f = {c_on_vf:.8f}")
    print(f"  |<v_a, v_f>| = {abs(np.dot(v_top_a, v_top_f)):.6f}")

    # What is the maximum of v^T H_actual v / v^T H_formula v?
    # This is the generalized eigenvalue problem H_actual v = λ H_formula v
    # For positive definite H_formula, this gives max generalized eigenvalue
    try:
        from scipy.linalg import eigh as scipy_eigh
        # Add small regularization to H_formula to ensure PD
        H_f_reg = res['H_formula'] + 1e-10 * np.eye(res['H_formula'].shape[0])
        gen_eigs = scipy_eigh(res['H_actual'], H_f_reg, eigvals_only=True)
        print(f"\nGeneralized eigenvalue max(v^T H_a v / v^T H_f v):")
        print(f"  max gen eig = {gen_eigs[-1]:.10f} (should be ≤ r(Q))")
        print(f"  min gen eig = {gen_eigs[0]:.10f}")
    except Exception as e:
        print(f"\nGeneralized eigenvalue computation failed: {e}")

    # Spectrum of H_actual and H_formula
    print(f"\nTop 10 eigenvalues:")
    print(f"  {'H_actual':>12s} {'H_formula':>12s} {'C=Hf-Ha':>12s}")
    for k in range(1, 11):
        print(f"  {res['eigs_actual'][-k]:12.6f} {res['eigs_formula'][-k]:12.6f} {eigs_C[-k]:12.6f}")

    print(f"\nBottom 5 eigenvalues of C (most negative):")
    for k in range(5):
        print(f"  C_eig[{k}] = {eigs_C[k]:.6f}")

    return res


def main():
    lat = Lattice(2, 4)
    beta = 1.0
    np.random.seed(42)

    # Configuration types
    configs = []

    # 1. Haar random (typical)
    Q = random_su2_config(lat.n_links)
    configs.append((Q, "Haar random"))

    # 2. Near-identity (small scale)
    Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
    for e in range(lat.n_links):
        Q[e] = su2_exp(0.01 * np.random.randn(3))
    configs.append((Q, "Near-identity (scale=0.01)"))

    # 3. Near-identity (medium)
    Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
    for e in range(lat.n_links):
        Q[e] = su2_exp(0.1 * np.random.randn(3))
    configs.append((Q, "Near-identity (scale=0.1)"))

    # 4. Abelian
    Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
    for e in range(lat.n_links):
        theta = np.random.uniform(0, 2*np.pi)
        Q[e] = su2_exp(np.array([0, 0, theta]))
    configs.append((Q, "Abelian (all T₃)"))

    # 5. One-hot π rotation
    Q = np.array([I2.copy() for _ in range(lat.n_links)])
    Q[0] = su2_exp(np.array([np.pi, 0, 0]))
    configs.append((Q, "One-hot π rotation"))

    for Q, label in configs:
        analyze_config(Q, lat, beta, label)

    # Summary table
    print("\n\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Config':30s} {'r':>10s} {'gap':>10s} {'||C||':>10s} {'λmin(C)':>10s} {'v_a^T C v_a':>12s}")
    print("-" * 82)

    for Q, label in configs:
        res = compute_ratio_data(Q, lat, beta)
        C = res['H_formula'] - res['H_actual']
        _, vecs = eigh(res['H_actual'])
        v_top = vecs[:, -1]
        c_va = v_top @ C @ v_top
        eigs_C = eigvalsh(C)
        print(f"{label:30s} {res['r']:10.6f} {1-res['r']:10.6f} {res['C_norm']:10.4f} {eigs_C[0]:10.4f} {c_va:12.6f}")


if __name__ == '__main__':
    main()
