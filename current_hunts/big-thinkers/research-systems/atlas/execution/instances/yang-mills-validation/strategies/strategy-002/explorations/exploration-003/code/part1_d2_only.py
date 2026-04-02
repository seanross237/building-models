"""Part 1 - d=2 only, full output saved."""
import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import *

np.random.seed(42)
beta = 1.0
L, d = 2, 2
lat = Lattice(L, d)

print(f"Lattice: L={L}, d={d}, Links={lat.n_links}, DOF={lat.n_dof}, Plaquettes={len(lat.plaquettes())}")

Q_I = identity_config(lat)
H_I = compute_hessian_fd(Q_I, lat, beta)
H_I = (H_I + H_I.T) / 2
evals_I, evecs_I = eigh(H_I)
lmax_I = evals_I[-1]

print(f"\nλ_max(H(I)) = {lmax_I:.12f}")
print(f"\nFull spectrum:")
for i, e in enumerate(evals_I):
    print(f"  λ_{i+1:3d} = {e:.10f}")

# Top eigenspace
tol = 0.005
deg_mask = evals_I > (lmax_I - tol)
degeneracy = np.sum(deg_mask)
print(f"\nDegeneracy: {degeneracy}")
top_evecs = evecs_I[:, deg_mask]

# Perturbation analysis: 20 directions
n_dir = 20
dt = 0.001
t_vals = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, np.pi]

print(f"\n{'='*80}")
print("PERTURBATION ANALYSIS (20 directions)")
print(f"{'='*80}")

for idx in range(n_dir):
    dQ = np.random.randn(lat.n_links, 3)
    dQ = dQ / np.sqrt(np.sum(dQ**2))

    # λ_max at each t
    lmax_t = {}
    for t in t_vals:
        if t == 0.0:
            lmax_t[t] = lmax_I
        else:
            Qt = perturb_config(Q_I, dQ, t)
            lmax_t[t] = compute_lmax_actual(Qt, lat, beta)

    # First-order Δ matrix
    Hp = compute_hessian_fd(perturb_config(Q_I, dQ, dt), lat, beta)
    Hm = compute_hessian_fd(perturb_config(Q_I, dQ, -dt), lat, beta)
    Hp = (Hp + Hp.T)/2; Hm = (Hm + Hm.T)/2
    dHdt = (Hp - Hm) / (2*dt)
    Delta = top_evecs.T @ dHdt @ top_evecs
    Delta_eigs = eigvalsh(Delta)

    # Second-order
    lp = eigvalsh(Hp)[-1]
    lm = eigvalsh(Hm)[-1]
    d2l = (lp + lm - 2*lmax_I) / dt**2

    # Also compute full second-order matrix on degenerate subspace
    d2Hdt2 = (Hp + Hm - 2*H_I) / dt**2
    # Direct second-order contribution
    d2_direct = top_evecs.T @ d2Hdt2 @ top_evecs

    # Level-repulsion contribution from non-top modes
    non_top_evecs = evecs_I[:, ~deg_mask]
    non_top_evals = evals_I[~deg_mask]

    V1 = non_top_evecs.T @ dHdt @ top_evecs  # shape (n-deg, deg)
    # Level repulsion: Σ_k |<w_k|dH|v_i>|² / (λ_max - λ_k)
    level_rep = np.zeros((degeneracy, degeneracy))
    for k in range(len(non_top_evals)):
        denom = lmax_I - non_top_evals[k]
        if abs(denom) > 1e-10:
            level_rep += np.outer(V1[k], V1[k]) / denom

    # Full second-order matrix = direct + 2 * level_repulsion
    # Note: level repulsion SUBTRACTS because eigenvalues are pushed DOWN
    # Actually: second-order = d2_direct - 2 * level_rep (pushed down by lower levels)
    # Wait, let me think more carefully. For max eigenvalue:
    # d²λ/dt² = <v|d²H/dt²|v> + 2 Σ_{k≠top} |<w_k|dH/dt|v>|² / (λ_max - λ_k)
    # Since λ_max > λ_k, the denominator is positive, and this term is POSITIVE
    # So level repulsion INCREASES d²λ/dt², i.e., it acts to make the eigenvalue curve UP
    # The direct term is the question.
    second_order_matrix = d2_direct + 2 * level_rep
    so_eigs = eigvalsh(second_order_matrix)

    print(f"\nDirection {idx+1}:")
    print(f"  First-order Δ eigenvalues: {Delta_eigs}")
    print(f"  d²λ/dt² (numerical):      {d2l:.6f}")
    print(f"  Second-order matrix eigenvalues: {so_eigs}")
    print(f"  Direct second-order eigs:  {eigvalsh(d2_direct)}")
    print(f"  Level repulsion contribution (trace): {np.trace(level_rep):.6f}")
    print(f"  λ_max values along scan:")
    for t in t_vals:
        gap = lmax_I - lmax_t[t]
        c = gap/(t**2) if t > 0 else 0
        print(f"    t={t:6.3f}: λ={lmax_t[t]:.10f}, gap={gap:.2e}, gap/t²={c:.4f}")

print("\n\nDONE")
