"""
Verify that r ≈ 1 at flat connections is FD artifact,
and study the near-identity transition r(scale) carefully.
"""
import numpy as np
from numpy.linalg import eigvalsh, norm
import sys
import time

sys.path.insert(0, '.')
from fast_hessian import (
    Lattice, su2_exp, haar_random_su2, project_su2,
    T, I2, compute_hessian_fd, compute_hessian_formula,
)


def compute_r_detailed(Q, lattice, beta, h=1e-4):
    """Compute r with detailed info."""
    H_a = compute_hessian_fd(Q, lattice, beta, h)
    H_f = compute_hessian_formula(Q, lattice, beta)
    H_a = (H_a + H_a.T) / 2
    H_f = (H_f + H_f.T) / 2
    ea = eigvalsh(H_a)
    ef = eigvalsh(H_f)
    la, lf = ea[-1], ef[-1]
    diff = norm(H_a - H_f)
    return la / lf, la, lf, diff


def main():
    lat = Lattice(2, 4)
    beta = 1.0

    print("=" * 70)
    print("Part 1: FD step size dependence for flat connections")
    print("=" * 70)

    # Uniform config (flat)
    Q_flat = np.array([haar_random_su2()] * lat.n_links)

    for h in [1e-3, 5e-4, 1e-4, 5e-5, 1e-5]:
        r, la, lf, diff = compute_r_detailed(Q_flat, lat, beta, h)
        print(f"  h={h:.0e}: r={r:.12f}, λ_a={la:.10f}, λ_f={lf:.10f}, ||ΔH||={diff:.6e}")

    print("\n" + "=" * 70)
    print("Part 2: Near-identity transition r(scale)")
    print("=" * 70)

    # More scales for smooth transition plot
    scales = [0.001, 0.003, 0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1,
              0.15, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]

    np.random.seed(123)
    print(f"\n{'scale':>8s} {'r':>14s} {'λ_actual':>12s} {'λ_formula':>12s} {'||ΔH||':>12s} {'gap':>12s}")
    for scale in scales:
        # Average over 3 random samples
        rs = []
        for trial in range(3):
            n_links = lat.n_links
            Q = np.zeros((n_links, 2, 2), dtype=complex)
            for e in range(n_links):
                v = scale * np.random.randn(3)
                Q[e] = su2_exp(v)
            r, la, lf, diff = compute_r_detailed(Q, lat, beta, h=1e-4)
            rs.append(r)
        r_mean = np.mean(rs)
        gap = 1 - r_mean
        print(f"  {scale:8.4f} {r_mean:14.10f} {la:12.6f} {lf:12.6f} {diff:12.6e} {gap:12.8f}")

    print("\n" + "=" * 70)
    print("Part 3: One-hot perturbation — single link perturbed from identity")
    print("=" * 70)

    for angle in [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, np.pi/2, np.pi]:
        Q = np.array([I2.copy() for _ in range(lat.n_links)])
        Q[0] = su2_exp(np.array([angle, 0, 0]))  # perturb link 0
        r, la, lf, diff = compute_r_detailed(Q, lat, beta, h=1e-4)
        gap = 1 - r
        print(f"  angle={angle:6.3f}: r={r:.10f}, gap={gap:.10f}, λ_a={la:.6f}, λ_f={lf:.6f}")

    print("\n" + "=" * 70)
    print("Part 4: Verify truly non-flat configs always have r < 1")
    print("=" * 70)

    # Use h=1e-5 for higher precision on configs close to 1
    np.random.seed(999)
    print("\nNear-identity configs with h=1e-5:")
    for scale in [0.005, 0.01, 0.02, 0.05]:
        Q = np.zeros((lat.n_links, 2, 2), dtype=complex)
        for e in range(lat.n_links):
            v = scale * np.random.randn(3)
            Q[e] = su2_exp(v)
        r, la, lf, diff = compute_r_detailed(Q, lat, beta, h=1e-5)
        print(f"  scale={scale}: r={r:.12f}, gap={1-r:.12f}")


if __name__ == '__main__':
    main()
