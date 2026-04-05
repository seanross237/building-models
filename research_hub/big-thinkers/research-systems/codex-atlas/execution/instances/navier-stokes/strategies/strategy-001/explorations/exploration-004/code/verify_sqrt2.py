#!/usr/bin/env python3
"""
Verify the identity ||∇u||_{L²} = √2 ||S||_{L²} for divergence-free fields on T³.

Also verify ||∇u||_{L²} = ||ω||_{L²} (Parseval identity for periodic div-free fields).

Proof of ||∇u|| = √2 ||S||:
  ∇u = S + Ω where S = (∇u + (∇u)^T)/2, Ω = (∇u - (∇u)^T)/2
  ||∇u||² = ||S||² + ||Ω||² + 2⟨S, Ω⟩
  ⟨S, Ω⟩ = ∫ S_{ij} Ω_{ij} dx = 0 (symmetric × antisymmetric = 0)
  ||S||² - ||Ω||² = ∫ ∂_j u_i · ∂_i u_j dx = -∫ u_i · ∂_j ∂_i u_j dx = -∫ u_i · ∂_i(∇·u) dx = 0
  Therefore ||S|| = ||Ω||, so ||∇u||² = 2||S||², i.e., ||∇u|| = √2 ||S||.
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq

def test_identity(N=64, n_tests=5):
    """Test with random divergence-free fields."""
    nu = 0.01
    vol = (2 * np.pi)**3
    dx = 2 * np.pi / N

    k = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K2_safe = np.where(K2 == 0, 1, K2)

    print(f"Testing ||∇u|| = √2 ||S|| and ||∇u|| = ||ω|| for div-free fields on T³")
    print(f"N = {N}, {n_tests} random div-free fields")
    print(f"{'Test':>5s} {'||∇u||':>12s} {'√2||S||':>12s} {'||ω||':>12s} {'||∇u||/||S||':>14s} {'||∇u||/||ω||':>14s}")

    for test in range(n_tests):
        rng = np.random.RandomState(test + 42)

        # Random Fourier field
        ux_hat = rng.randn(N,N,N) + 1j*rng.randn(N,N,N)
        uy_hat = rng.randn(N,N,N) + 1j*rng.randn(N,N,N)
        uz_hat = rng.randn(N,N,N) + 1j*rng.randn(N,N,N)

        # Project to div-free
        kdotf = (KX*ux_hat + KY*uy_hat + KZ*uz_hat) / K2_safe
        kdotf[0,0,0] = 0
        ux_hat -= KX * kdotf
        uy_hat -= KY * kdotf
        uz_hat -= KZ * kdotf

        # Physical fields
        ux = ifftn(ux_hat).real
        uy = ifftn(uy_hat).real
        uz = ifftn(uz_hat).real

        # Gradient tensor
        grads = {}
        for i, (ni, u_hat) in enumerate(zip('xyz', [ux_hat, uy_hat, uz_hat])):
            for j, (nj, Kj) in enumerate(zip('xyz', [KX, KY, KZ])):
                grads[f'{ni}{nj}'] = ifftn(1j * Kj * u_hat).real

        # ||∇u||²
        grad_sq = sum(g**2 for g in grads.values())
        grad_L2 = np.sqrt(np.mean(grad_sq) * vol)

        # ||S||² where S_{ij} = 0.5*(∂u_i/∂x_j + ∂u_j/∂x_i)
        S_sq = 0.0
        names = ['x', 'y', 'z']
        for i in range(3):
            for j in range(3):
                S_ij = 0.5 * (grads[f'{names[i]}{names[j]}'] + grads[f'{names[j]}{names[i]}'])
                S_sq += np.mean(S_ij**2) * vol
        S_L2 = np.sqrt(S_sq)

        # Vorticity
        omega_x = grads['zy'] - grads['yz']
        omega_y = grads['xz'] - grads['zx']
        omega_z = grads['yx'] - grads['xy']
        omega_sq = omega_x**2 + omega_y**2 + omega_z**2
        omega_L2 = np.sqrt(np.mean(omega_sq) * vol)

        ratio_S = grad_L2 / S_L2
        ratio_omega = grad_L2 / omega_L2

        print(f"{test:5d} {grad_L2:12.6f} {np.sqrt(2)*S_L2:12.6f} {omega_L2:12.6f} "
              f"{ratio_S:14.10f} {ratio_omega:14.10f}")

    print(f"\nExpected: ||∇u||/||S|| = √2 = {np.sqrt(2):.10f}")
    print(f"Expected: ||∇u||/||ω|| = 1.0")


if __name__ == '__main__':
    test_identity()
