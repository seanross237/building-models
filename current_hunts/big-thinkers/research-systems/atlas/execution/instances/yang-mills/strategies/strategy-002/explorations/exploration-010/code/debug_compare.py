"""
Debug: compare E009-style K matrix with my analytical Hessian at Q=I.
Find where the factor-of-2 discrepancy comes from.
"""
import numpy as np

L = 2; d = 4; n_gen = 3
n_sites = L**d
n_links = n_sites * d
n_dof = n_links * n_gen
beta = 1.0

sigma = np.zeros((3, 2, 2), dtype=complex)
sigma[0] = [[0, 1], [1, 0]]
sigma[1] = [[0, -1j], [1j, 0]]
sigma[2] = [[1, 0], [0, -1]]
tau = 1j * sigma / 2
I2 = np.eye(2, dtype=complex)

def site_to_idx(x):
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx

def idx_to_site(idx):
    x = []
    r = idx
    for i in range(d):
        x.append(r % L)
        r //= L
    return tuple(reversed(x))

def link_idx(site_idx, mu):
    return site_idx * d + mu

def add_dir(site, mu):
    x = list(site)
    x[mu] = (x[mu] + 1) % L
    return tuple(x)

# Build plaquettes
plaquettes = []
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    for mu in range(d):
        for nu in range(mu + 1, d):
            x_mu = add_dir(x, mu)
            x_nu = add_dir(x, nu)
            l0 = link_idx(site_to_idx(x), mu)
            l1 = link_idx(site_to_idx(x_mu), nu)
            l2 = link_idx(site_to_idx(x_nu), mu)
            l3 = link_idx(site_to_idx(x), nu)
            plaquettes.append([(l0, +1), (l1, +1), (l2, -1), (l3, -1)])

print(f"n_plaq = {len(plaquettes)}")

# ---- Method 1: E009-style K matrix ----
K = np.zeros((n_links, n_links))
for plaq in plaquettes:
    for i, (li, si) in enumerate(plaq):
        for j, (lj, sj) in enumerate(plaq):
            K[li, lj] += (beta / 2) * si * sj

# Build H_e009 = K tensor I_3
H_e009 = np.zeros((n_dof, n_dof))
for li in range(n_links):
    for lj in range(n_links):
        for a in range(n_gen):
            H_e009[li * n_gen + a, lj * n_gen + a] = K[li, lj]

eigs_e009 = np.linalg.eigvalsh(H_e009)
print(f"\nE009 Hessian:")
print(f"  K diagonal: {K[0,0]:.4f} (expected 3.0)")
print(f"  lambda_max(H) = {eigs_e009[-1]:.6f}")
print(f"  lambda_max / beta = {eigs_e009[-1]/beta:.6f}")

# ---- Method 2: My analytical Hessian ----
Q = np.zeros((n_links, 2, 2), dtype=complex)
for l in range(n_links):
    Q[l] = I2.copy()

H_mine = np.zeros((n_dof, n_dof))
for plaq in plaquettes:
    W = np.zeros((4, 2, 2), dtype=complex)
    link_ids = []
    signs = []
    for k, (l, s) in enumerate(plaq):
        link_ids.append(l)
        signs.append(s)
        if s == +1:
            W[k] = Q[l]
        else:
            W[k] = Q[l].conj().T

    # Prefix
    Lpre = np.zeros((5, 2, 2), dtype=complex)
    Lpre[0] = I2
    for k in range(4):
        Lpre[k + 1] = Lpre[k] @ W[k]
    U_P = Lpre[4]
    retr_UP = np.real(np.trace(U_P))

    # Suffix
    Rsuf = np.zeros((4, 2, 2), dtype=complex)
    Rsuf[3] = I2
    for k in range(2, -1, -1):
        Rsuf[k] = W[k + 1] @ Rsuf[k + 1]

    # Diagonal
    diag_val = (beta / 4.0) * retr_UP
    for k in range(4):
        lk = link_ids[k]
        for a in range(n_gen):
            idx = lk * n_gen + a
            H_mine[idx, idx] += diag_val

    # Off-diagonal
    for k in range(4):
        lk = link_ids[k]
        sk = signs[k]
        for m in range(k + 1, 4):
            lm = link_ids[m]
            sm = signs[m]
            M_km = I2.copy()
            for j in range(k + 1, m):
                M_km = M_km @ W[j]
            for a in range(n_gen):
                if sk == +1:
                    Ak = W[k] @ tau[a]
                else:
                    Ak = -tau[a] @ W[k]
                LAM = Lpre[k] @ Ak @ M_km
                for b in range(n_gen):
                    if sm == +1:
                        Am = W[m] @ tau[b]
                    else:
                        Am = -tau[b] @ W[m]
                    product = LAM @ Am @ Rsuf[m]
                    val = np.real(np.trace(product))
                    i_idx = lk * n_gen + a
                    j_idx = lm * n_gen + b
                    H_mine[i_idx, j_idx] += -beta * val
                    H_mine[j_idx, i_idx] += -beta * val

eigs_mine = np.linalg.eigvalsh(H_mine)
print(f"\nMy analytical Hessian:")
print(f"  H_mine[0,0] = {H_mine[0,0]:.4f} (expected 3.0)")
print(f"  lambda_max(H) = {eigs_mine[-1]:.6f}")

# ---- Compare ----
diff = np.max(np.abs(H_mine - H_e009))
print(f"\nmax |H_mine - H_e009| = {diff:.2e}")

if diff > 1e-10:
    # Find where they differ
    i, j = np.unravel_index(np.argmax(np.abs(H_mine - H_e009)), H_mine.shape)
    li, ai = i // n_gen, i % n_gen
    lj, aj = j // n_gen, j % n_gen
    print(f"  Max diff at ({i},{j}): link ({li},{ai}) x ({lj},{aj})")
    print(f"  H_mine = {H_mine[i,j]:.6f}, H_e009 = {H_e009[i,j]:.6f}")

    # Check if H_mine has cross-generator terms
    cross_gen_max = 0
    for li in range(n_links):
        for lj in range(n_links):
            for a in range(n_gen):
                for b in range(n_gen):
                    if a != b:
                        v = abs(H_mine[li*n_gen+a, lj*n_gen+b])
                        if v > cross_gen_max:
                            cross_gen_max = v
    print(f"\n  Max cross-generator entry |H[li*3+a, lj*3+b]| (a!=b): {cross_gen_max:.2e}")

    # Print first few diagonal elements
    print(f"\n  First few diagonals:")
    for idx in range(min(12, n_dof)):
        print(f"    H_mine[{idx},{idx}]={H_mine[idx,idx]:.4f}  H_e009[{idx},{idx}]={H_e009[idx,idx]:.4f}")

    # Sample off-diagonal
    print(f"\n  Sample off-diagonals:")
    for i in range(0, min(12, n_dof)):
        for j in range(i+1, min(12, n_dof)):
            if abs(H_mine[i,j]) > 0.01 or abs(H_e009[i,j]) > 0.01:
                print(f"    H[{i},{j}]: mine={H_mine[i,j]:.4f}  e009={H_e009[i,j]:.4f}  diff={H_mine[i,j]-H_e009[i,j]:.4f}")

else:
    print("  Matrices match! Same eigenvalues expected.")
    print(f"  But lambda_max: mine={eigs_mine[-1]:.6f}, e009={eigs_e009[-1]:.6f}")
