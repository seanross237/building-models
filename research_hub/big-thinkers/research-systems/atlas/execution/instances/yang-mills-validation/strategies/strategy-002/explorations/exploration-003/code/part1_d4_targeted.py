"""
Part 1 Phase B: d=4, L=2 — Targeted perturbation analysis.
Only computes line scans and second-order coefficient (skips dH/dt matrix).
"""
import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))
from lattice_core import *

np.random.seed(42)
beta = 1.0
L, d = 2, 4
lat = Lattice(L, d)

print(f"Lattice: L={L}, d={d}, Links={lat.n_links}, DOF={lat.n_dof}, Plaquettes={len(lat.plaquettes())}")

Q_I = identity_config(lat)

# Step 1: Eigenstructure at identity
print("\n--- Eigenstructure at Q = I ---")
t0 = time.time()
H_I = compute_hessian_fd(Q_I, lat, beta)
H_I = (H_I + H_I.T) / 2
t1 = time.time()
print(f"Hessian computed in {t1-t0:.1f}s")

evals_I = eigvalsh(H_I)
lmax_I = evals_I[-1]
print(f"λ_max = {lmax_I:.10f}")

# Grouped spectrum
unique_evals = []
current_val = evals_I[0]
current_count = 1
for i in range(1, len(evals_I)):
    if abs(evals_I[i] - current_val) < 0.01:
        current_count += 1
    else:
        unique_evals.append((current_val, current_count))
        current_val = evals_I[i]
        current_count = 1
unique_evals.append((current_val, current_count))

print(f"\nSpectrum (grouped):")
for val, count in unique_evals:
    print(f"  λ = {val:8.4f} (degeneracy {count})")

# Top eigenspace
tol = 0.01
deg_mask = evals_I > (lmax_I - tol)
degeneracy = np.sum(deg_mask)
print(f"\nTop eigenvalue degeneracy: {degeneracy}")
print(f"Expected (d-1)(N²-1) = {(d-1)*3} = {(d-1)*3}")

# Step 2: Line scans (5 random + 3 structured directions)
print(f"\n{'='*70}")
print("LINE SCANS + SECOND-ORDER")
print(f"{'='*70}")

t_vals = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]

directions = []

# 5 random
for i in range(5):
    dQ = np.random.randn(lat.n_links, 3)
    dQ = dQ / np.sqrt(np.sum(dQ**2))
    directions.append((f"random_{i+1}", dQ))

# Structured: single-link
dQ = np.zeros((lat.n_links, 3))
dQ[0, 0] = 1.0
directions.append(("single_link_T1", dQ))

# Structured: uniform mu=0
dQ = np.zeros((lat.n_links, 3))
for x in range(lat.n_sites):
    link = lat.link_index(x, 0)
    dQ[link, 0] = 1.0 / np.sqrt(lat.n_sites)
directions.append(("uniform_mu0_T1", dQ))

# Structured: staggered
dQ = np.zeros((lat.n_links, 3))
for x in range(lat.n_sites):
    parity = sum(lat.coords[x]) % 2
    sign = 1 if parity == 0 else -1
    for mu in range(d):
        link = lat.link_index(x, mu)
        dQ[link, 0] = sign / np.sqrt(lat.n_links)
directions.append(("staggered_T1", dQ))

for name, dQ in directions:
    print(f"\n--- Direction: {name} ---")
    t_start = time.time()

    lmax_t = {}
    for t in t_vals:
        if t == 0.0:
            lmax_t[t] = lmax_I
        else:
            Qt = perturb_config(Q_I, dQ, t)
            lmax_t[t] = compute_lmax_actual(Qt, lat, beta)

    # Second-order from finite differences
    dt = 0.001
    Qp = perturb_config(Q_I, dQ, dt)
    Qm = perturb_config(Q_I, dQ, -dt)
    lp = compute_lmax_actual(Qp, lat, beta)
    lm = compute_lmax_actual(Qm, lat, beta)
    d2l = (lp + lm - 2*lmax_I) / dt**2

    t_elapsed = time.time() - t_start

    print(f"  d²λ/dt² = {d2l:.4f}")
    print(f"  Time: {t_elapsed:.1f}s")
    print(f"  t         λ_max(t)      gap         gap/t²")
    for t in t_vals:
        gap = lmax_I - lmax_t[t]
        c = gap/(t**2) if t > 0 else 0
        print(f"  {t:6.3f}  {lmax_t[t]:12.8f}  {gap:12.2e}  {c:12.6f}")

    all_decreasing = all(lmax_t[t_vals[i]] >= lmax_t[t_vals[i+1]] - 1e-6 for i in range(len(t_vals)-1))
    print(f"  Monotone: {all_decreasing}")

print("\n\nDONE")
