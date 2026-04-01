"""
verify_bp_bound_l4.py — B_□ intermediate bound verification at L=4.

Mission: Yang-Mills strategy-003.
Verify: sum_P |B_P(Q, v)|^2 <= 4d * |v|^2 = 16 * |v|^2 (for d=4)

B_P is defined with parallel transport (from verify_bp_bound.py E010):
  B_P = sum_k s_k * Ad_{G_k}(v_{l_k})
  where G_k = W_0 * ... * W_{k-1}, Ad_G(v) = G v G^{-1}

At Q=I: B_P = sum_k s_k * v_{l_k} (no transport, G_k=I)

Key: at Q=I, B_P = "curl" of v over plaquette.
The B_P bound is sum_P |B_P|^2 / |v|^2 <= 4d = 16.

This is equivalent to lambda_max(M_curl) <= 4d where M_curl[l,l'] = sum_P s_{l,P} s_{l',P}

We compute this at Q=I (L=4) and verify numerically.
For general Q: use the full B_P formula with adjoint transport.
"""

import numpy as np
import json
import time

# ============================================================
# Setup
# ============================================================
L = 4
d = 4
N_SU = 2
beta = 1.0

n_sites = L**d     # 256
n_links = n_sites * d  # 1024
n_gen = 3
n_dof = n_links * n_gen  # 3072

print(f"L={L}, d={d}: n_sites={n_sites}, n_links={n_links}, n_dof={n_dof}")

sigma = np.zeros((3,2,2), dtype=complex)
sigma[0] = [[0,1],[1,0]]
sigma[1] = [[0,-1j],[1j,0]]
sigma[2] = [[1,0],[0,-1]]
tau = 1j*sigma/2  # |tau_a|^2 = -2Tr(tau_a^2) = 1
I2 = np.eye(2, dtype=complex)

def site_to_idx(x):
    idx = 0
    for i in range(d): idx = idx*L + x[i]
    return idx

def idx_to_site(idx):
    x=[]; r=idx
    for i in range(d): x.append(r%L); r//=L
    return tuple(reversed(x))

def link_idx(si, mu): return si*d + mu
def add_dir(site, mu):
    x=list(site); x[mu]=(x[mu]+1)%L; return tuple(x)

# Build plaquettes
plaquettes = []
for x_idx in range(n_sites):
    x = idx_to_site(x_idx)
    for mu in range(d):
        for nu in range(mu+1, d):
            x_mu = add_dir(x,mu); x_nu = add_dir(x,nu)
            l0=link_idx(site_to_idx(x),mu); l1=link_idx(site_to_idx(x_mu),nu)
            l2=link_idx(site_to_idx(x_nu),mu); l3=link_idx(site_to_idx(x),nu)
            plaquettes.append([(l0,+1),(l1,+1),(l2,-1),(l3,-1)])

n_plaq = len(plaquettes)
print(f"n_plaquettes = {n_plaq}")

link_to_plaqs = [[] for _ in range(n_links)]
for p_idx, plaq in enumerate(plaquettes):
    for pos,(l,s) in enumerate(plaq):
        link_to_plaqs[l].append((p_idx,pos))

def random_su2():
    q=np.random.randn(4); q/=np.linalg.norm(q)
    return q[0]*I2 + 1j*(q[1]*sigma[0]+q[2]*sigma[1]+q[3]*sigma[2])

def su2_dagger(U): return U.conj().T

def su2_exp(c):
    A=c[0]*tau[0]+c[1]*tau[1]+c[2]*tau[2]
    cs=float(np.real(c[0]**2+c[1]**2+c[2]**2))
    if cs<1e-30: return I2+A
    th=np.sqrt(cs)
    return np.cos(th/2)*I2+(np.sin(th/2)/(th/2))*A

def plaq_product(Q, plaq):
    r=I2.copy()
    for (l,s) in plaq: r=r@(Q[l] if s==+1 else su2_dagger(Q[l]))
    return r

# ============================================================
# B_P(Q, v) with parallel transport (correct formula from E010)
# ============================================================
def compute_BP(Q, plaq, v_flat):
    """
    B_P = sum_k s_k * Ad_{G_k}(v_{l_k})
    G_k = W_0 W_1 ... W_{k-1}  (partial plaquette product)
    Ad_G(v) = G v G^{-1} = G v G^dag (for G in SU(2))
    v_flat: shape (n_dof,) = (n_links*n_gen,)
    Returns B_P as a 2x2 matrix in su(2).
    """
    # Transport matrices G[k] = W_0 ... W_{k-1}
    G = [I2.copy()]
    for k in range(4):
        l, s = plaq[k]
        Wk = Q[l] if s==+1 else su2_dagger(Q[l])
        G.append(G[-1] @ Wk)

    B_P = np.zeros((2,2), dtype=complex)
    for k in range(4):
        l, s = plaq[k]
        # v_l as su(2) matrix
        v_l = sum(float(v_flat[l*n_gen+a]) * tau[a] for a in range(n_gen))
        # Parallel transport to base
        v_transported = G[k] @ v_l @ su2_dagger(G[k])  # Ad_{G_k}(v_l)
        B_P += s * v_transported

    return B_P

def su2_norm_sq(A):
    """Compute |A|^2 = -2 Re Tr(A^2)."""
    return -2.0 * np.real(np.trace(A @ A))

def compute_BP_sum(Q, v_flat):
    """Compute sum_P |B_P(Q,v)|^2."""
    total = 0.0
    for plaq in plaquettes:
        B = compute_BP(Q, plaq, v_flat)
        total += su2_norm_sq(B)
    return total

# ============================================================
# PART A: Q=I, M_curl analysis
# At Q=I: B_P = sum_k s_k * v_{l_k}, so sum_P |B_P|^2 = v^T M_curl v
# M_curl[li*n_gen+a, lj*n_gen+b] = delta_{ab} * sum_P s_{li,P} * s_{lj,P}
# ============================================================
print("\n" + "="*60)
print("PART A: Curl matrix at Q=I")
print("="*60)

# Build M_curl (only the link-space matrix K_curl, then tensor with I_3)
K_curl = np.zeros((n_links, n_links))
for plaq in plaquettes:
    for (li, si) in plaq:
        for (lj, sj) in plaq:
            K_curl[li, lj] += si * sj

print(f"K_curl diagonal: [{K_curl.diagonal().min():.2f}, {K_curl.diagonal().max():.2f}]")
print(f"Expected diagonal = 2*(d-1) = {2*(d-1)} (each link in {2*(d-1)} plaquettes)")

# Full M_curl = K_curl tensor I_3
M_curl = np.zeros((n_dof, n_dof))
for li in range(n_links):
    for lj in range(n_links):
        if K_curl[li, lj] != 0:
            for a in range(n_gen):
                M_curl[li*n_gen+a, lj*n_gen+a] = K_curl[li, lj]

print(f"\nM_curl built: {M_curl.shape}")
print(f"M_curl symmetric: {np.allclose(M_curl, M_curl.T)}")

# Compute eigenvalues of K_curl (smaller matrix, exact same spectrum as M_curl with 3x multiplicity)
print("\nComputing K_curl eigenvalues...")
k_curl_eigs = np.linalg.eigvalsh(K_curl)

print(f"K_curl lambda_max = {k_curl_eigs.max():.6f}")
print(f"K_curl lambda_min = {k_curl_eigs.min():.6f}")
print(f"Bound 4d = {4*d}")
print(f"Conjecture: lambda_max(K_curl) <= 4d = 16: {k_curl_eigs.max() <= 4*d + 1e-6}")

# Unique eigenvalues
k_curl_unique = np.unique(np.round(k_curl_eigs, 4))
print(f"\nUnique K_curl eigenvalues (rounded to 4 dec):")
for ev in k_curl_unique:
    cnt = np.sum(np.abs(k_curl_eigs - ev) < 0.01)
    print(f"  {ev:8.4f} (multiplicity {cnt})")

# ============================================================
# PART B: Direct verification at Q=I using compute_BP
# ============================================================
print("\n" + "="*60)
print("PART B: Direct B_P verification at Q=I")
print("="*60)

Q_I = np.zeros((n_links,2,2), dtype=complex)
for l in range(n_links): Q_I[l] = I2.copy()

# Test with max eigenvector of K_curl
max_idx = np.argmax(k_curl_eigs)
k_vecs = np.linalg.eigh(K_curl)[1]
v_Kmax = np.zeros(n_dof)
# Use the K_curl max eigenvector in generator direction 0
for li in range(n_links):
    v_Kmax[li*n_gen + 0] = k_vecs[li, max_idx]
v_Kmax /= np.linalg.norm(v_Kmax)

BP_sum = compute_BP_sum(Q_I, v_Kmax)
v_nsq = np.sum(v_Kmax**2)
BP_ratio = BP_sum / v_nsq

print(f"Max K_curl eigenvector: BP_ratio = {BP_ratio:.6f}")
print(f"4d = {4*d}")
print(f"K_curl lambda_max = {k_curl_eigs.max():.6f}")
print(f"Consistent? {abs(BP_ratio - k_curl_eigs.max()) < 0.01}")

# Test with staggered mode
v_stag = np.zeros(n_dof)
for l in range(n_links):
    x = idx_to_site(l // d)
    v_stag[l*n_gen + 0] = (-1)**sum(x)
v_stag /= np.linalg.norm(v_stag)
BP_stag = compute_BP_sum(Q_I, v_stag)
print(f"\nStaggered mode: BP_ratio = {BP_stag/np.sum(v_stag**2):.6f} (expected 0)")

# ============================================================
# PART C: General Q verification (5 random configs)
# ============================================================
print("\n" + "="*60)
print("PART C: B_P bound for random L=4 configs")
print("="*60)
print("(Using v = random unit vector for speed; max eigenvector needs full Hessian)")

np.random.seed(42)
max_BP_ratio = 0.0
results_bp = []

for trial in range(30):
    Q = np.zeros((n_links,2,2), dtype=complex)
    if trial < 10:
        for l in range(n_links): Q[l] = random_su2()
        config_type = "random"
    elif trial < 20:
        eps = np.random.uniform(0.1, 1.5)
        for l in range(n_links):
            Q[l] = I2 @ su2_exp(eps * np.random.randn(3))
        config_type = f"perturbed-{eps:.2f}"
    else:
        # Near identity
        eps = 0.05
        for l in range(n_links):
            Q[l] = su2_exp(eps * np.random.randn(3))
        config_type = "near-id"

    # Test with 3 random v vectors
    for v_trial in range(3):
        v = np.random.randn(n_dof)
        v /= np.linalg.norm(v)
        BP_s = compute_BP_sum(Q, v)
        ratio = BP_s / np.sum(v**2)
        if ratio > max_BP_ratio:
            max_BP_ratio = ratio
            print(f"  New max: trial={trial}, v_trial={v_trial}, BP_ratio={ratio:.6f}")

    if trial % 5 == 0:
        print(f"  Completed {trial+1}/30 configs, max_BP_ratio so far: {max_BP_ratio:.6f}")

print(f"\nMax BP_ratio over {30*3} random (Q,v) pairs: {max_BP_ratio:.6f}")
print(f"Bound 4d = {4*d}")
print(f"Conjecture holds: {max_BP_ratio <= 4*d + 1e-4}")

# ============================================================
# Save results
# ============================================================
bp_results = {
    "L": L, "d": d, "n_sites": n_sites, "n_links": n_links, "n_plaq": n_plaq,
    "K_curl_lambda_max": float(k_curl_eigs.max()),
    "K_curl_lambda_min": float(k_curl_eigs.min()),
    "bound_4d": float(4*d),
    "conjecture_QI": bool(k_curl_eigs.max() <= 4*d + 1e-4),
    "K_curl_eigenvalues_unique": [float(e) for e in k_curl_unique],
    "BP_ratio_max_eigvec_QI": float(BP_ratio),
    "BP_ratio_staggered_QI": float(BP_stag/np.sum(v_stag**2)),
    "max_BP_ratio_random_configs": float(max_BP_ratio),
    "conjecture_random": bool(max_BP_ratio <= 4*d + 1e-4),
}

out_path = "/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/yang-mills/strategies/strategy-003/explorations/exploration-004/code/bp_results.json"
with open(out_path, "w") as f:
    json.dump(bp_results, f, indent=2)
print(f"\nResults saved to {out_path}")
print("verify_bp_bound_l4.py DONE")
