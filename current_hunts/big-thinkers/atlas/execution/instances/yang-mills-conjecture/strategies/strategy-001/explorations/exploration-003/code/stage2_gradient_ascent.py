"""
Stage 2: Gradient ascent on f_sq = Sum|B_sq(Q)|^2 - 1024
Try to push f_sq toward 0 (or above). If we can't, the conjecture likely holds.
"""

import numpy as np
from itertools import product

# =====================================================
# SU(2) utilities
# =====================================================

def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_inv(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def quat_to_rot(q):
    q = q / np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def random_quat():
    q = np.random.randn(4)
    return q / np.linalg.norm(q)

# =====================================================
# Lattice setup
# =====================================================

L = 2
d = 4
coords = list(product(range(L), repeat=d))

def add_mod(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def staggered_sign(x, mu):
    return (-1) ** (sum(x) + mu)

def edge_index(x, mu):
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx * d + mu

plaquettes = []
for x in coords:
    for mu in range(d):
        for nu in range(mu+1, d):
            e1 = (x, mu)
            e2 = (add_mod(x, mu), nu)
            e3 = (add_mod(x, nu), mu)
            e4 = (x, nu)

            s1 = staggered_sign(*e1)
            s2 = staggered_sign(*e2)
            s3 = staggered_sign(*e3)
            s4 = staggered_sign(*e4)

            eff = (s1, s2, -s3, -s4)
            active = (mu + nu) % 2 == 1

            plaquettes.append({
                'e1_idx': edge_index(*e1), 'e2_idx': edge_index(*e2),
                'e3_idx': edge_index(*e3), 'e4_idx': edge_index(*e4),
                'eff': eff, 'active': active
            })

n_edges = 64

def compute_fsq(Q_flat, n):
    """
    Q_flat: array of shape (64*4,) = 256 parameters
    Returns f_sq = Sum |B_sq|^2 - 1024
    """
    total = 0.0
    for p in plaquettes:
        q1 = Q_flat[p['e1_idx']*4:(p['e1_idx']+1)*4]
        q2 = Q_flat[p['e2_idx']*4:(p['e2_idx']+1)*4]
        q3 = Q_flat[p['e3_idx']*4:(p['e3_idx']+1)*4]
        q4 = Q_flat[p['e4_idx']*4:(p['e4_idx']+1)*4]

        q1 = q1 / np.linalg.norm(q1)
        q2 = q2 / np.linalg.norm(q2)
        q3 = q3 / np.linalg.norm(q3)
        q4 = q4 / np.linalg.norm(q4)

        R1 = quat_to_rot(q1)
        partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
        R2 = quat_to_rot(partial)
        usq = quat_mult(partial, quat_inv(q4))
        R3 = quat_to_rot(usq)

        c1, c2, c3, c4 = p['eff']
        B = c1 * n + c2 * (R1 @ n) + c3 * (R2 @ n) + c4 * (R3 @ n)
        total += np.dot(B, B)

    return total - 1024.0

def numerical_gradient_fsq(Q_flat, n, h=1e-6):
    """Numerical gradient of f_sq."""
    grad = np.zeros_like(Q_flat)
    f0 = compute_fsq(Q_flat, n)
    for i in range(len(Q_flat)):
        Q_p = Q_flat.copy()
        Q_p[i] += h
        grad[i] = (compute_fsq(Q_p, n) - f0) / h
    return grad

def project_to_sphere(Q_flat):
    """Project each quaternion back to unit sphere."""
    for i in range(64):
        q = Q_flat[i*4:(i+1)*4]
        norm = np.linalg.norm(q)
        if norm > 1e-10:
            Q_flat[i*4:(i+1)*4] = q / norm
    return Q_flat

# =====================================================
# Gradient ascent to maximize f_sq
# =====================================================

n = np.array([0., 0., 1.])
np.random.seed(42)

n_starts = 50
n_steps = 100
best_fsq_overall = -np.inf
best_config = None

print("=" * 70)
print("GRADIENT ASCENT on f_sq (trying to push toward 0 or above)")
print(f"n_starts = {n_starts}, n_steps = {n_steps}")
print("=" * 70)

for start in range(n_starts):
    # Random initial config
    Q_flat = np.random.randn(256)
    Q_flat = project_to_sphere(Q_flat)

    fsq = compute_fsq(Q_flat, n)
    best_fsq = fsq

    lr = 0.01
    for step in range(n_steps):
        grad = numerical_gradient_fsq(Q_flat, n)
        # Project gradient onto tangent space of product of spheres
        for i in range(64):
            q = Q_flat[i*4:(i+1)*4]
            g = grad[i*4:(i+1)*4]
            # Remove normal component
            g = g - np.dot(g, q) * q
            grad[i*4:(i+1)*4] = g

        Q_flat_new = Q_flat + lr * grad
        Q_flat_new = project_to_sphere(Q_flat_new)

        fsq_new = compute_fsq(Q_flat_new, n)

        if fsq_new > fsq:
            Q_flat = Q_flat_new
            fsq = fsq_new
            lr *= 1.1  # increase step
        else:
            lr *= 0.5  # decrease step

        if fsq > best_fsq:
            best_fsq = fsq

        if lr < 1e-12:
            break

    if best_fsq > best_fsq_overall:
        best_fsq_overall = best_fsq
        best_config = Q_flat.copy()

    if start % 10 == 0:
        print(f"  Start {start}: best_fsq = {best_fsq:.6f} (overall best: {best_fsq_overall:.6f})")

print(f"\nOverall best f_sq achieved: {best_fsq_overall:.6f}")
print(f"Conjecture holds? (f_sq <= 0): {best_fsq_overall <= 0.001}")

# Try starting from adversarial configs
print("\n" + "=" * 70)
print("GRADIENT ASCENT from adversarial starting points")
print("=" * 70)

# Config: all edges = identity except use "k" axis which gives f_sq = 0
for label, start_func in [
    ("all q=k", lambda: np.tile(np.array([0.,0.,0.,1.]), 64)),
    ("all q=(1+k)/sqrt2", lambda: np.tile(np.array([1.,0.,0.,1.])/np.sqrt(2), 64)),
    ("all q=random_near_k", lambda: project_to_sphere(
        np.tile(np.array([0.,0.,0.,1.]), 64) + 0.1*np.random.randn(256)
    )),
]:
    Q_flat = start_func()
    Q_flat = project_to_sphere(Q_flat)
    fsq = compute_fsq(Q_flat, n)
    print(f"\n  {label}: initial f_sq = {fsq:.6f}")

    lr = 0.01
    for step in range(200):
        grad = numerical_gradient_fsq(Q_flat, n)
        for i in range(64):
            q = Q_flat[i*4:(i+1)*4]
            g = grad[i*4:(i+1)*4]
            g = g - np.dot(g, q) * q
            grad[i*4:(i+1)*4] = g

        Q_flat_new = Q_flat + lr * grad
        Q_flat_new = project_to_sphere(Q_flat_new)
        fsq_new = compute_fsq(Q_flat_new, n)

        if fsq_new > fsq:
            Q_flat = Q_flat_new
            fsq = fsq_new
            lr = min(lr * 1.1, 0.1)
        else:
            lr *= 0.5
        if lr < 1e-12:
            break

    print(f"  After gradient ascent: f_sq = {fsq:.6f}")

# Now try optimizing over n as well
print("\n" + "=" * 70)
print("JOINT OPTIMIZATION over Q and n")
print("=" * 70)

def compute_fsq_joint(params):
    """params = (256 for Q) + (3 for n direction)"""
    Q_flat = params[:256]
    n_dir = params[256:259]
    n_dir = n_dir / np.linalg.norm(n_dir)
    return compute_fsq(Q_flat, n_dir)

np.random.seed(2024)
best_joint = -np.inf
for start in range(30):
    Q_flat = np.random.randn(256)
    Q_flat = project_to_sphere(Q_flat)
    n_dir = np.random.randn(3)
    n_dir = n_dir / np.linalg.norm(n_dir)
    params = np.concatenate([Q_flat, n_dir])

    fsq = compute_fsq_joint(params)

    lr = 0.01
    for step in range(80):
        grad = np.zeros(259)
        f0 = compute_fsq_joint(params)
        for i in range(259):
            p = params.copy()
            p[i] += 1e-6
            grad[i] = (compute_fsq_joint(p) - f0) / 1e-6

        # Project Q part
        for i in range(64):
            q = params[i*4:(i+1)*4]
            g = grad[i*4:(i+1)*4]
            g = g - np.dot(g, q) * q
            grad[i*4:(i+1)*4] = g
        # Project n part
        n_cur = params[256:259]
        g_n = grad[256:259]
        g_n = g_n - np.dot(g_n, n_cur) * n_cur
        grad[256:259] = g_n

        params_new = params + lr * grad
        # Re-project
        for i in range(64):
            q = params_new[i*4:(i+1)*4]
            params_new[i*4:(i+1)*4] = q / np.linalg.norm(q)
        n_new = params_new[256:259]
        params_new[256:259] = n_new / np.linalg.norm(n_new)

        fsq_new = compute_fsq_joint(params_new)
        if fsq_new > fsq:
            params = params_new
            fsq = fsq_new
            lr = min(lr * 1.1, 0.1)
        else:
            lr *= 0.5
        if lr < 1e-12:
            break

    if fsq > best_joint:
        best_joint = fsq

    if start % 10 == 0:
        print(f"  Start {start}: f_sq = {fsq:.6f} (best: {best_joint:.6f})")

print(f"\nBest joint f_sq: {best_joint:.6f}")
print(f"Conjecture holds? {best_joint <= 0.001}")

# =====================================================
# More focused: perturbation from Q=k (f_sq=0)
# =====================================================

print("\n" + "=" * 70)
print("PERTURBATION from f_sq=0 config (all q=k)")
print("=" * 70)

Q_k = np.tile(np.array([0.,0.,0.,1.]), 64)
fsq_base = compute_fsq(Q_k, n)
print(f"Base: f_sq = {fsq_base:.6f}")

# Try perturbing each edge and see if f_sq increases
print("Single edge perturbations from all-k config:")
for edge_idx in range(64):
    best_pert_fsq = -np.inf
    for trial in range(20):
        pert = np.random.randn(4) * 0.3
        Q_pert = Q_k.copy()
        Q_pert[edge_idx*4:(edge_idx+1)*4] += pert
        Q_pert = project_to_sphere(Q_pert)
        f = compute_fsq(Q_pert, n)
        best_pert_fsq = max(best_pert_fsq, f)
    if edge_idx < 10 or best_pert_fsq > -0.01:
        print(f"  Edge {edge_idx}: best_pert f_sq = {best_pert_fsq:.6f}")

# Gradient at Q=k
print("\nGradient at Q=k:")
grad = numerical_gradient_fsq(Q_k, n)
grad_norm = np.linalg.norm(grad)
print(f"  |grad| = {grad_norm:.6f}")

# Check if Q=k is a critical point (gradient = 0 on tangent space)
projected_grad = grad.copy()
for i in range(64):
    q = Q_k[i*4:(i+1)*4]
    g = projected_grad[i*4:(i+1)*4]
    g = g - np.dot(g, q) * q
    projected_grad[i*4:(i+1)*4] = g
proj_grad_norm = np.linalg.norm(projected_grad)
print(f"  |projected grad| = {proj_grad_norm:.6f}")
print(f"  Q=k is critical point? {proj_grad_norm < 0.01}")
