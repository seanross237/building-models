"""
Attempt 3: Fourier analysis at flat connections + perturbation argument.

At flat connections (Q=I), the Hessian is translation-invariant.
It block-diagonalizes in Fourier space into L^d blocks of size 3d x 3d.
Since it's also diagonal in color, each block further factorizes into
3 identical d x d blocks.

We:
1. Compute the Fourier blocks explicitly
2. Show the max eigenvalue is 4d (achieved at k=0)
3. Analyze perturbation away from flat
"""

import numpy as np
from itertools import product
import sys
sys.path.insert(0, '.')
from hessian_core import *

def fourier_blocks_at_flat(d, L, beta=1.0, N=2):
    """Compute Fourier blocks of the Hessian at flat config.

    At flat, H[(x,mu,a),(y,nu,b)] = delta_ab * K_mu_nu(x-y)
    where K is a d x d matrix depending on the relative position.

    In Fourier space: K_hat(k) = sum_r K(r) exp(-2*pi*i*k.r/L)
    """
    lat = Lattice(d, L)
    Q = flat_config(lat)
    H = compute_hessian(lat, Q, beta, N)

    # Verify color-diagonal structure
    ne = lat.nedges
    max_color_off = 0
    for e1 in range(ne):
        for e2 in range(ne):
            for a in range(3):
                for b in range(3):
                    if a != b:
                        max_color_off = max(max_color_off, abs(H[3*e1+a, 3*e2+b]))
    print(f"  Max color off-diagonal: {max_color_off:.2e} (should be ~0)")

    # Extract the d x d kernel K_mu_nu(x-y) from the a=0 slice
    # Edge index: e = mu * nsites + site_idx
    # K_mu_nu(r) = H[(x, mu, 0), (x+r, nu, 0)]
    nsites = lat.nsites
    sites = lat.sites
    site_idx = lat.site_index

    K_real = {}  # K_real[(mu,nu,r)] = value
    for mu in range(d):
        for nu in range(d):
            for r in sites:
                # Pick reference site (0,0,...,0)
                x = (0,) * d
                y = r
                ex = mu * nsites + site_idx[x]
                ey = nu * nsites + site_idx[y]
                K_real[(mu, nu, r)] = H[3*ex, 3*ey]

    # Fourier transform
    ks = list(product(range(L), repeat=d))
    blocks = {}

    for k in ks:
        K_hat = np.zeros((d, d), dtype=complex)
        for mu in range(d):
            for nu in range(d):
                for r in sites:
                    phase = np.exp(-2j * np.pi * sum(k[i]*r[i] for i in range(d)) / L)
                    K_hat[mu, nu] += K_real[(mu, nu, r)] * phase
        blocks[k] = K_hat

    return blocks, ks

print("=" * 70)
print("ATTEMPT 3: FOURIER ANALYSIS AT FLAT CONNECTIONS")
print("=" * 70)

for d in [2, 3, 4]:
    L = 2
    print(f"\n{'='*60}")
    print(f"d={d}, L={L}")
    print(f"{'='*60}")

    blocks, ks = fourier_blocks_at_flat(d, L)

    all_evals = []
    for k in ks:
        K = blocks[k]
        # Verify Hermitian
        assert np.allclose(K, K.conj().T), f"Block {k} not Hermitian!"
        evals = np.linalg.eigvalsh(K.real)  # Should be real since H is symmetric
        all_evals.append((k, evals))
        print(f"  k={k}: eigenvalues = {np.round(evals, 4)}, max = {evals[-1]:.6f}")

    max_eval = max(ev[-1] for k, ev in all_evals)
    max_k = [k for k, ev in all_evals if abs(ev[-1] - max_eval) < 1e-10]
    print(f"\n  Global max eigenvalue: {max_eval:.6f}")
    print(f"  Target (4d): {4*d}")
    print(f"  Achieved at k = {max_k}")

    # The eigenvalue of the full Hessian is 3 copies (one per color) of these
    # So lambda_max(HessS) = max_k max_eval(K_hat(k)) = max_eval above
    print(f"  lambda_max(HessS at flat) = {max_eval:.6f}")

# Detailed analysis for d=4
print(f"\n{'='*60}")
print("DETAILED FOURIER ANALYSIS (d=4)")
print(f"{'='*60}")

d = 4
for L in [2, 3, 4]:
    print(f"\nL={L}:")
    blocks, ks = fourier_blocks_at_flat(d, L)

    max_eval = 0
    for k in ks:
        evals = np.linalg.eigvalsh(blocks[k].real)
        if evals[-1] > max_eval:
            max_eval = evals[-1]
            max_k = k
            max_block = blocks[k]

    print(f"  Max eigenvalue: {max_eval:.6f} (target: {4*d})")
    print(f"  At k={max_k}")
    print(f"  Max block:\n{np.round(max_block.real, 4)}")
    evals, evecs = np.linalg.eigh(max_block.real)
    print(f"  Eigenvalues: {np.round(evals, 4)}")
    print(f"  Top eigenvector: {np.round(evecs[:, -1], 4)}")

# Analyze the k=0 block structure
print(f"\n{'='*60}")
print("k=0 BLOCK STRUCTURE")
print(f"{'='*60}")

for d in [2, 3, 4]:
    L = 4  # Use larger lattice for clarity
    blocks, ks = fourier_blocks_at_flat(d, L)
    K0 = blocks[(0,)*d].real
    print(f"\nd={d}, L={L}, k=0 block ({d}x{d}):")
    print(np.round(K0, 4))
    evals = np.linalg.eigvalsh(K0)
    print(f"  Eigenvalues: {np.round(evals, 4)}")
    print(f"  Max: {evals[-1]:.6f}")

    # What does the k=0 block look like analytically?
    # k=0 means sum over all sites of K(r).
    # This should be: diagonal = 4(d-1), off-diagonal = ?
    # Let's compute explicitly
    diag = K0[0,0]
    offdiag = K0[0,1] if d > 1 else 0
    print(f"  Diagonal entry: {diag:.4f}")
    print(f"  Off-diagonal entry: {offdiag:.4f}")
    print(f"  Predicted: diag=4(d-1)={4*(d-1)}, offdiag = 4 (from cross-term sum)")

    # At k=0, the eigenvector (1,1,...,1)/sqrt(d) should give eigenvalue
    # diag + (d-1)*offdiag
    v = np.ones(d) / np.sqrt(d)
    rayleigh = v @ K0 @ v
    print(f"  Rayleigh quotient for v=(1,...,1)/sqrt(d): {rayleigh:.4f}")
    print(f"  = diag + (d-1)*offdiag = {diag + (d-1)*offdiag:.4f}")

# Verify: k=0 block has diagonal 4(d-1) and off-diagonal 4 for all mu!=nu?
# That gives eigenvalues: 4(d-1) + (d-1)*4 = 4(d-1) + 4(d-1) = 8(d-1) for (1,...,1)
# and 4(d-1) - 4 for other eigenvectors.
# Wait, 4(d-1) + (d-1)*4 = 4(d-1)(1+1) = 8(d-1)?
# But we need 4d. Let me check d=4: 8*3 = 24 != 16.
# So the k=0 eigenvector (1,...,1) is NOT the maximum?

print(f"\n{'='*60}")
print("WHICH k MAXIMIZES THE EIGENVALUE?")
print(f"{'='*60}")

for d in [2, 3, 4]:
    L = 4
    blocks, ks = fourier_blocks_at_flat(d, L)

    results = []
    for k in ks:
        evals = np.linalg.eigvalsh(blocks[k].real)
        results.append((k, evals[-1], evals))

    results.sort(key=lambda x: -x[1])
    print(f"\nd={d}, L={L}: Top 5 wavevectors:")
    for k, lmax, evals in results[:5]:
        print(f"  k={k}: lambda_max={lmax:.4f}, all_evals={np.round(evals, 2)}")
