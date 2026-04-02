#!/usr/bin/env python3
"""
Verify the divergence-free reduction factor across multiple k₀ and N values.
Also check: does the factor depend on the number of modes (Gaussian regime)?
"""
import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import time

def setup_grid(N):
    k = fftfreq(N, d=1.0/N)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K_mag = np.sqrt(K2)
    return KX, KY, KZ, K2, K_mag

def get_positive_half(band_mask, N, KX, KY, KZ):
    indices = np.where(band_mask.ravel())[0]
    pos = []
    for idx in indices:
        ix, iy, iz = np.unravel_index(idx, (N, N, N))
        kx, ky, kz = KX[ix,iy,iz], KY[ix,iy,iz], KZ[ix,iy,iz]
        if kx > 0 or (kx == 0 and ky > 0) or (kx == 0 and ky == 0 and kz > 0):
            pos.append(idx)
    return np.array(pos)

def compute_scalar_ceff(N, pos_indices, KX, KY, KZ, K2, n_samples=300):
    """Mean C_eff for scalar fields with random phases."""
    n_pos = len(pos_indices)
    amps = np.ones(n_pos) / np.sqrt(n_pos)

    ratios = []
    for _ in range(n_samples):
        phases = np.random.uniform(0, 2*np.pi, n_pos)

        f_hat = np.zeros((N,N,N), dtype=complex)
        for i, idx in enumerate(pos_indices):
            ix, iy, iz = np.unravel_index(idx, (N,N,N))
            jx, jy, jz = (-ix)%N, (-iy)%N, (-iz)%N
            c = amps[i] * np.exp(1j*phases[i])
            f_hat[ix,iy,iz] = c
            f_hat[jx,jy,jz] = np.conj(c)

        F = N**3 * f_hat
        fp = ifftn(F).real

        L2 = np.sqrt(np.mean(fp**2))
        gx = ifftn(1j*KX*F).real
        gy = ifftn(1j*KY*F).real
        gz = ifftn(1j*KZ*F).real
        H1 = np.sqrt(np.mean(gx**2 + gy**2 + gz**2))
        L4 = np.mean(fp**4)**0.25

        if L2 > 1e-15 and H1 > 1e-15:
            ratios.append(L4 / (L2**0.25 * H1**0.75))

    return np.mean(ratios), np.std(ratios)

def compute_divfree_ceff(N, pos_indices, KX, KY, KZ, K2, K_mag, n_samples=300):
    """Mean C_eff for div-free vector fields with random polarization."""
    n_pos = len(pos_indices)
    kx_f = KX.ravel(); ky_f = KY.ravel(); kz_f = KZ.ravel()
    km_f = K_mag.ravel()

    # Precompute polarization basis
    e1 = np.zeros((n_pos, 3))
    e2 = np.zeros((n_pos, 3))
    for i, idx in enumerate(pos_indices):
        k_vec = np.array([kx_f[idx], ky_f[idx], kz_f[idx]])
        kn = km_f[idx]
        kh = k_vec / kn
        v = np.array([1,0,0]) if abs(kh[0]) < 0.9 else np.array([0,1,0])
        e1_i = v - np.dot(v, kh)*kh
        e1_i /= np.linalg.norm(e1_i)
        e2[i] = np.cross(kh, e1_i)
        e1[i] = e1_i

    ratios = []
    for _ in range(n_samples):
        a1 = (np.random.randn(n_pos) + 1j*np.random.randn(n_pos))/np.sqrt(2)
        a2 = (np.random.randn(n_pos) + 1j*np.random.randn(n_pos))/np.sqrt(2)

        fh = [np.zeros((N,N,N), dtype=complex) for _ in range(3)]
        for i, idx in enumerate(pos_indices):
            ix, iy, iz = np.unravel_index(idx, (N,N,N))
            jx, jy, jz = (-ix)%N, (-iy)%N, (-iz)%N
            cv = a1[i]*e1[i] + a2[i]*e2[i]
            for c in range(3):
                fh[c][ix,iy,iz] = cv[c]
                fh[c][jx,jy,jz] = np.conj(cv[c])

        F = [N**3 * h for h in fh]
        u = [ifftn(f).real for f in F]

        L2_sq = np.mean(u[0]**2 + u[1]**2 + u[2]**2)
        H1_sq = 0
        for c in range(3):
            gx = ifftn(1j*KX*F[c]).real
            gy = ifftn(1j*KY*F[c]).real
            gz = ifftn(1j*KZ*F[c]).real
            H1_sq += np.mean(gx**2 + gy**2 + gz**2)

        usq = u[0]**2 + u[1]**2 + u[2]**2
        L4_4 = np.mean(usq**2)

        L2 = np.sqrt(max(L2_sq,0)); H1 = np.sqrt(max(H1_sq,0)); L4 = max(L4_4,0)**0.25
        if L2 > 1e-15 and H1 > 1e-15:
            ratios.append(L4 / (L2**0.25 * H1**0.75))

    return np.mean(ratios), np.std(ratios)


# Main
N = 32
KX, KY, KZ, K2, K_mag = setup_grid(N)

print("="*70)
print("DIVERGENCE-FREE REDUCTION FACTOR VERIFICATION")
print("="*70)

k0_values = [3, 4, 6, 8, 10, 12]
results = []

for k0 in k0_values:
    band = (K_mag >= k0/2) & (K_mag <= 2*k0) & (K_mag > 0)
    pos = get_positive_half(band, N, KX, KY, KZ)
    n_pos = len(pos)
    n_total = int(np.sum(band))

    t0 = time.time()
    scalar_mean, scalar_std = compute_scalar_ceff(N, pos, KX, KY, KZ, K2, n_samples=400)
    divfree_mean, divfree_std = compute_divfree_ceff(N, pos, KX, KY, KZ, K2, K_mag, n_samples=400)
    dt = time.time() - t0

    ratio = divfree_mean / scalar_mean
    results.append((k0, n_total, scalar_mean, divfree_mean, ratio))

    print(f"k0={k0:2d} ({n_total:5d} modes): scalar={scalar_mean:.6f}±{scalar_std:.6f}, "
          f"divfree={divfree_mean:.6f}±{divfree_std:.6f}, ratio={ratio:.4f} ({dt:.1f}s)")

# Summary
print("\nSummary:")
ratios_all = [r[4] for r in results]
print(f"  Mean ratio: {np.mean(ratios_all):.4f} ± {np.std(ratios_all):.4f}")
print(f"  Range: [{min(ratios_all):.4f}, {max(ratios_all):.4f}]")

# Theoretical prediction for the div-free factor
# For a d-dimensional vector field with div-free constraint:
# The constraint removes 1 of d degrees of freedom per mode.
# If the L⁴ norm scales with the number of effective degrees of freedom:
# C_{L,divfree} / C_{L,scalar} ≈ ((d-1)/d)^{some power}
# For d=3: (2/3)^{1/4} ≈ 0.903 or (2/3)^{1/2} ≈ 0.816
print(f"\n  Theoretical predictions:")
print(f"    (2/3)^{{1/4}} = {(2/3)**0.25:.4f}")
print(f"    (2/3)^{{1/3}} = {(2/3)**(1/3):.4f}")
print(f"    (2/3)^{{3/8}} = {(2/3)**(3/8):.4f}")
print(f"    (2/3)^{{1/2}} = {(2/3)**0.5:.4f}")
print(f"  Observed: {np.mean(ratios_all):.4f}")
# The observed 0.863 is closest to (2/3)^{1/3} = 0.874 or maybe a different power
# Let's find the best fit: ratio = (2/3)^p => p = log(ratio)/log(2/3)
obs = np.mean(ratios_all)
p = np.log(obs) / np.log(2/3)
print(f"  Best fit: (2/3)^{{{p:.4f}}} = {(2/3)**p:.4f}")
