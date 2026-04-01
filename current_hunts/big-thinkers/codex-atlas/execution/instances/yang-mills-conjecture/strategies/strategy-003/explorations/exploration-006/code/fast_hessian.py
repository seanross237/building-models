"""
Fast Hessian computation using vectorized color kernel.
Key optimization: compute F_{ab} = Re Tr(iσ_a M iσ_b N) via closed-form formula
instead of 9 separate trace computations.

F = -2(β₀I + [β⃗×]) R_M  where MN = β₀I + iβ⃗·σ, R_M = adjoint(M).
"""

import numpy as np
from hessian_core import (
    Lattice, isigma, su2_inv, su2_exp, random_su2, project_su2,
    flat_config, random_config, anti_instanton_config, get_link
)

def _adjoint_fast(U):
    """Fast SO(3) adjoint from SU(2) quaternion decomposition.
    U = a*I + i(b*σ1 + c*σ2 + d*σ3)
    R_{ij} = (a²-|v|²)δ_{ij} + 2v_iv_j + 2a ε_{ijk}v_k
    """
    a = np.real(U[0,0] + U[1,1]) / 2
    b = np.imag(U[0,1] + U[1,0]) / 2  # coeff of iσ1
    c = np.real(U[0,1] - U[1,0]) / 2   # coeff of iσ2
    d = np.imag(U[0,0] - U[1,1]) / 2   # coeff of iσ3
    v = np.array([b, c, d])
    vsq = b*b + c*c + d*d
    R = (a*a - vsq) * np.eye(3) + 2*np.outer(v, v)
    # + 2a * [v×]
    R[0,1] -= 2*a*d; R[0,2] += 2*a*c
    R[1,0] += 2*a*d; R[1,2] -= 2*a*b
    R[2,0] -= 2*a*c; R[2,1] += 2*a*b
    return R.T  # Convention: R[a,b] = Re Tr(-iσ_a U iσ_b U†)/2

def _color_kernel_fast(M, N):
    """F_{ab} = Re Tr(iσ_a M iσ_b N) = -2(β₀I + [β⃗×]) R_M
    where MN = β₀I + iβ⃗·σ.
    """
    W = M @ N
    beta0 = np.real(W[0,0] + W[1,1]) / 2
    b1 = np.imag(W[0,1] + W[1,0]) / 2
    b2 = np.real(W[0,1] - W[1,0]) / 2
    b3 = np.imag(W[0,0] - W[1,1]) / 2

    R_M = _adjoint_fast(M)

    # P = β₀I + [β⃗×]
    P = np.array([
        [beta0, -b3, b2],
        [b3, beta0, -b1],
        [-b2, b1, beta0]
    ])
    return -2.0 * P @ R_M

def compute_hessian_fast(lat, Q, beta=1.0, N=2):
    """Fast full Hessian using vectorized color kernel."""
    ne = lat.nedges
    dim = 3 * ne
    H = np.zeros((dim, dim))

    for plaq in lat.plaquettes:
        # Compute holonomy
        U = np.eye(2, dtype=complex)
        for (e, s) in plaq:
            U = U @ (Q[e] if s == +1 else Q[e].conj().T)
        re_tr = np.real(U[0,0] + U[1,1])

        # Self-terms: diagonal contribution
        for (e, s) in plaq:
            val = (beta/N) * re_tr
            for a in range(3):
                H[3*e+a, 3*e+a] += val

        # Cross-terms: compute chain products and color kernel
        edges = plaq  # [(e0,s0), (e1,s1), (e2,s2), (e3,s3)]
        # Precompute cumulative products from left
        links = [Q[e] if s == +1 else Q[e].conj().T for (e, s) in edges]
        cum = [None]*5
        cum[0] = np.eye(2, dtype=complex)
        for k in range(4):
            cum[k+1] = cum[k] @ links[k]
        # cum[k] = product of links[0]...links[k-1]

        # Precompute cumulative products from right
        rcum = [None]*5
        rcum[4] = np.eye(2, dtype=complex)
        for k in range(3, -1, -1):
            rcum[k] = links[k] @ rcum[k+1]
        # rcum[k] = product of links[k]...links[3]

        for p in range(4):
            for q in range(p+1, 4):
                ep, sp = edges[p]
                eq, sq = edges[q]

                # L = cum[p+1], mid = product of links[p+1..q-1], R = rcum[q+1]
                L = cum[p+1]
                mid = np.eye(2, dtype=complex)
                for k in range(p+1, q):
                    mid = mid @ links[k]
                R = rcum[q+1]

                # F_{ab} = Re Tr(L iσ_a mid iσ_b R) = Re Tr(iσ_a mid iσ_b (R L))
                # Using formula: color_kernel(mid, R@L)
                F = _color_kernel_fast(mid, R @ L)
                F *= -(beta/N) * sp * sq

                # Fill H symmetrically
                for a in range(3):
                    for b in range(3):
                        H[3*ep+a, 3*eq+b] += F[a, b]
                        H[3*eq+b, 3*ep+a] += F[a, b]

    return H

def compute_hessian_decomposed_fast(lat, Q, beta=1.0, N=2):
    """Fast decomposed Hessian: returns D (diagonal array) and C (cross-term matrix)."""
    ne = lat.nedges
    dim = 3 * ne
    D = np.zeros(dim)
    C = np.zeros((dim, dim))

    for plaq in lat.plaquettes:
        U = np.eye(2, dtype=complex)
        for (e, s) in plaq:
            U = U @ (Q[e] if s == +1 else Q[e].conj().T)
        re_tr = np.real(U[0,0] + U[1,1])

        for (e, s) in plaq:
            val = (beta/N) * re_tr
            for a in range(3):
                D[3*e+a] += val

        edges = plaq
        links = [Q[e] if s == +1 else Q[e].conj().T for (e, s) in edges]
        cum = [np.eye(2, dtype=complex)]
        for k in range(4):
            cum.append(cum[-1] @ links[k])
        rcum = [None]*5
        rcum[4] = np.eye(2, dtype=complex)
        for k in range(3, -1, -1):
            rcum[k] = links[k] @ rcum[k+1]

        for p in range(4):
            for q in range(p+1, 4):
                ep, sp = edges[p]
                eq, sq = edges[q]

                mid = np.eye(2, dtype=complex)
                for k in range(p+1, q):
                    mid = mid @ links[k]

                F = _color_kernel_fast(mid, rcum[q+1] @ cum[p+1])
                F *= -(beta/N) * sp * sq

                C[3*ep:3*ep+3, 3*eq:3*eq+3] += F
                C[3*eq:3*eq+3, 3*ep:3*ep+3] += F.T

    return D, C

def compute_per_plaquette_hessian_fast(lat, Q, pidx, beta=1.0, N=2):
    """Fast per-plaquette Hessian contribution."""
    ne = lat.nedges
    dim = 3 * ne
    H_p = np.zeros((dim, dim))

    plaq = lat.plaquettes[pidx]
    U = np.eye(2, dtype=complex)
    for (e, s) in plaq:
        U = U @ (Q[e] if s == +1 else Q[e].conj().T)
    re_tr = np.real(U[0,0] + U[1,1])

    for (e, s) in plaq:
        val = (beta/N) * re_tr
        for a in range(3):
            H_p[3*e+a, 3*e+a] += val

    edges = plaq
    links = [Q[e] if s == +1 else Q[e].conj().T for (e, s) in edges]
    cum = [np.eye(2, dtype=complex)]
    for k in range(4):
        cum.append(cum[-1] @ links[k])
    rcum = [None]*5
    rcum[4] = np.eye(2, dtype=complex)
    for k in range(3, -1, -1):
        rcum[k] = links[k] @ rcum[k+1]

    for p in range(4):
        for q in range(p+1, 4):
            ep, sp = edges[p]
            eq, sq = edges[q]
            mid = np.eye(2, dtype=complex)
            for k in range(p+1, q):
                mid = mid @ links[k]
            F = _color_kernel_fast(mid, rcum[q+1] @ cum[p+1])
            F *= -(beta/N) * sp * sq
            H_p[3*ep:3*ep+3, 3*eq:3*eq+3] += F
            H_p[3*eq:3*eq+3, 3*ep:3*ep+3] += F.T

    return H_p


if __name__ == "__main__":
    import time
    from hessian_core import compute_hessian, compute_hessian_decomposed

    lat = Lattice(4, 2)
    rng = np.random.default_rng(42)
    Q = random_config(lat, rng)

    # Verify correctness
    H_slow = compute_hessian(lat, Q)
    H_fast = compute_hessian_fast(lat, Q)
    print(f"||H_slow - H_fast|| = {np.max(np.abs(H_slow - H_fast)):.2e}")

    D_slow, C_slow = compute_hessian_decomposed(lat, Q)
    D_fast, C_fast = compute_hessian_decomposed_fast(lat, Q)
    print(f"||D_slow - D_fast|| = {np.max(np.abs(D_slow - D_fast)):.2e}")
    print(f"||C_slow - C_fast|| = {np.max(np.abs(C_slow - C_fast)):.2e}")

    # Benchmark
    t0 = time.time()
    for _ in range(10):
        Q = random_config(lat, rng)
        H = compute_hessian(lat, Q)
    t_slow = (time.time() - t0) / 10

    t0 = time.time()
    for _ in range(10):
        Q = random_config(lat, rng)
        H = compute_hessian_fast(lat, Q)
    t_fast = (time.time() - t0) / 10

    print(f"\nSlow: {t_slow*1000:.0f}ms/config")
    print(f"Fast: {t_fast*1000:.0f}ms/config")
    print(f"Speedup: {t_slow/t_fast:.1f}x")
