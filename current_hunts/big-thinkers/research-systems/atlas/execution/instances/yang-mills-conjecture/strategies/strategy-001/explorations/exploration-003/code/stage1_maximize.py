"""
Stage 1.3-1.4: Per-plaquette maximization of |B_sq(Q,v_stag)|^2
Uses pure numpy, no scipy dependency.

Two types:
  Type A (active, a=b):  |n + R1*n - R2*n - R3*n|^2
  Type I (inactive, a=-b): |n - R1*n - R2*n + R3*n|^2
"""

import numpy as np

def rotvec_to_matrix(v):
    """Convert rotation vector (axis*angle) to 3x3 rotation matrix via Rodrigues."""
    angle = np.linalg.norm(v)
    if angle < 1e-15:
        return np.eye(3)
    axis = v / angle
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)

def quat_to_rotation_matrix(q):
    """Convert quaternion [w,x,y,z] to 3x3 rotation matrix."""
    q = q / np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

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

def normalize_quat(q):
    return q / np.linalg.norm(q)

def random_quat():
    """Random unit quaternion (uniform on S^3)."""
    q = np.random.randn(4)
    return q / np.linalg.norm(q)

def bsq_type_A(R1, R2, R3, n):
    """Type A: n + R1*n - R2*n - R3*n"""
    return n + R1 @ n - R2 @ n - R3 @ n

def bsq_type_I(R1, R2, R3, n):
    """Type I: n - R1*n - R2*n + R3*n"""
    return n - R1 @ n - R2 @ n + R3 @ n

def gradient_bsq_A_rotvec(params, n, h=1e-7):
    """Numerical gradient of -|B_sq_A|^2 w.r.t. rotation vectors."""
    grad = np.zeros_like(params)
    f0 = eval_unconstrained_A(params, n)
    for i in range(len(params)):
        params_p = params.copy()
        params_p[i] += h
        grad[i] = (eval_unconstrained_A(params_p, n) - f0) / h
    return grad

def eval_unconstrained_A(params, n):
    R1 = rotvec_to_matrix(params[0:3])
    R2 = rotvec_to_matrix(params[3:6])
    R3 = rotvec_to_matrix(params[6:9])
    b = bsq_type_A(R1, R2, R3, n)
    return -np.dot(b, b)

def eval_unconstrained_I(params, n):
    R1 = rotvec_to_matrix(params[0:3])
    R2 = rotvec_to_matrix(params[3:6])
    R3 = rotvec_to_matrix(params[6:9])
    b = bsq_type_I(R1, R2, R3, n)
    return -np.dot(b, b)

def eval_constrained_A(params, n):
    q1 = normalize_quat(params[0:4])
    q2 = normalize_quat(params[4:8])
    q3 = normalize_quat(params[8:12])
    q4 = normalize_quat(params[12:16])
    R1 = quat_to_rotation_matrix(q1)
    partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
    R2 = quat_to_rotation_matrix(partial)
    usq = quat_mult(partial, quat_inv(q4))
    R3 = quat_to_rotation_matrix(usq)
    b = bsq_type_A(R1, R2, R3, n)
    return -np.dot(b, b)

def eval_constrained_I(params, n):
    q1 = normalize_quat(params[0:4])
    q2 = normalize_quat(params[4:8])
    q3 = normalize_quat(params[8:12])
    q4 = normalize_quat(params[12:16])
    R1 = quat_to_rotation_matrix(q1)
    partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
    R2 = quat_to_rotation_matrix(partial)
    usq = quat_mult(partial, quat_inv(q4))
    R3 = quat_to_rotation_matrix(usq)
    b = bsq_type_I(R1, R2, R3, n)
    return -np.dot(b, b)

def numerical_gradient(func, params, n, h=1e-7):
    grad = np.zeros_like(params)
    f0 = func(params, n)
    for i in range(len(params)):
        p = params.copy()
        p[i] += h
        grad[i] = (func(p, n) - f0) / h
    return grad

def gradient_descent_maximize(func, dim, n, n_starts=500, n_steps=200, lr=0.01):
    """Maximize -func via gradient descent (func returns negative of objective)."""
    best_val = -np.inf
    best_params = None

    for trial in range(n_starts):
        params = np.random.randn(dim) * np.pi
        if dim == 16:
            for i in range(4):
                q = params[4*i:4*i+4]
                params[4*i:4*i+4] = q / np.linalg.norm(q)

        val = -func(params, n)

        for step in range(n_steps):
            grad = numerical_gradient(func, params, n)
            params = params - lr * grad  # Gradient descent on func = -objective
            if dim == 16:
                for i in range(4):
                    q = params[4*i:4*i+4]
                    norm = np.linalg.norm(q)
                    if norm > 1e-10:
                        params[4*i:4*i+4] = q / norm

            new_val = -func(params, n)
            if new_val > val + 1e-12:
                val = new_val
            elif step > 20:
                break

        if val > best_val:
            best_val = val
            best_params = params.copy()

    return best_val, best_params

# =====================================================
# Run maximizations
# =====================================================

n = np.array([0.0, 0.0, 1.0])
np.random.seed(42)

print("=" * 60)
print("ANALYTICAL CHECKS FIRST")
print("=" * 60)

# Type A at R1=I, R2=R3=pi_x:
R_pi_x = np.diag([1., -1., -1.])  # rotation by pi around x
R_pi_y = np.diag([-1., 1., -1.])  # rotation by pi around y
R_pi_z = np.diag([-1., -1., 1.])  # rotation by pi around z

print("\nType A: |n + R1*n - R2*n - R3*n|^2")
for label, R1, R2, R3 in [
    ("R1=I, R2=R3=pi_x", np.eye(3), R_pi_x, R_pi_x),
    ("R1=I, R2=R3=pi_y", np.eye(3), R_pi_y, R_pi_y),
    ("R1=I, R2=R3=pi_z", np.eye(3), R_pi_z, R_pi_z),
    ("R1=R2=R3=I", np.eye(3), np.eye(3), np.eye(3)),
    ("R1=I, R2=pi_x, R3=pi_y", np.eye(3), R_pi_x, R_pi_y),
    ("all pi_x", R_pi_x, R_pi_x, R_pi_x),
]:
    b = bsq_type_A(R1, R2, R3, n)
    print(f"  {label}: B = {b}, |B|^2 = {np.dot(b,b):.4f}")

print("\nType I: |n - R1*n - R2*n + R3*n|^2")
for label, R1, R2, R3 in [
    ("R1=R2=pi_x, R3=I", R_pi_x, R_pi_x, np.eye(3)),
    ("R1=R2=pi_y, R3=I", R_pi_y, R_pi_y, np.eye(3)),
    ("R1=I, R2=pi_x, R3=pi_x", np.eye(3), R_pi_x, R_pi_x),
    ("R1=R2=R3=I", np.eye(3), np.eye(3), np.eye(3)),
    ("R1=R2=R3=pi_x", R_pi_x, R_pi_x, R_pi_x),
]:
    b = bsq_type_I(R1, R2, R3, n)
    print(f"  {label}: B = {b}, |B|^2 = {np.dot(b,b):.4f}")

# Now systematic numerical search
print("\n" + "=" * 60)
print("NUMERICAL MAXIMIZATION (gradient descent, 500 starts)")
print("=" * 60)

# Use a simpler but faster approach: random sampling + local refinement
def fast_maximize(func, dim, n_unit, n_random=10000, n_refine=50, lr=0.1):
    """Quick maximize: random sample, then refine top candidates."""
    # Random sample
    vals = []
    all_params = []
    for _ in range(n_random):
        if dim == 9:
            params = np.random.randn(dim) * np.pi
        else:
            params = np.random.randn(dim)
            for i in range(4):
                q = params[4*i:4*i+4]
                params[4*i:4*i+4] = q / np.linalg.norm(q)
        val = -func(params, n_unit)
        vals.append(val)
        all_params.append(params)

    # Sort and refine top candidates
    indices = np.argsort(vals)[-20:]  # top 20
    best_val = -np.inf
    best_params = None

    for idx in indices:
        params = all_params[idx].copy()
        val = vals[idx]
        for step in range(n_refine):
            grad = numerical_gradient(func, params, n_unit)
            params_new = params - lr * grad
            if dim == 16:
                for i in range(4):
                    q = params_new[4*i:4*i+4]
                    norm = np.linalg.norm(q)
                    if norm > 1e-10:
                        params_new[4*i:4*i+4] = q / norm
            new_val = -func(params_new, n_unit)
            if new_val > val:
                val = new_val
                params = params_new
                lr_local = lr
            else:
                lr *= 0.8
                if lr < 1e-8:
                    break
            lr = 0.1  # reset

        if val > best_val:
            best_val = val
            best_params = params.copy()

    return best_val, best_params

print("\nType A unconstrained (9 params):")
val_A_unc, _ = fast_maximize(eval_unconstrained_A, 9, n, n_random=50000)
print(f"  Max |B_sq_A|^2 = {val_A_unc:.6f}")
print(f"  f_sq = {val_A_unc:.6f} - 16 = {val_A_unc - 16:.6f}")

print("\nType I unconstrained (9 params):")
val_I_unc, _ = fast_maximize(eval_unconstrained_I, 9, n, n_random=50000)
print(f"  Max |B_sq_I|^2 = {val_I_unc:.6f}")
print(f"  f_sq = {val_I_unc:.6f}")

print("\nType A constrained (16 params):")
val_A_con, params_A_best = fast_maximize(eval_constrained_A, 16, n, n_random=50000)
print(f"  Max |B_sq_A|^2 = {val_A_con:.6f}")
print(f"  f_sq = {val_A_con:.6f} - 16 = {val_A_con - 16:.6f}")

print("\nType I constrained (16 params):")
val_I_con, params_I_best = fast_maximize(eval_constrained_I, 16, n, n_random=50000)
print(f"  Max |B_sq_I|^2 = {val_I_con:.6f}")
print(f"  f_sq = {val_I_con:.6f}")

# Summary
print("\n" + "=" * 60)
print("PER-PLAQUETTE MAXIMUM TABLE")
print("=" * 60)
print(f"{'Type':<10} {'|B(I)|^2':<12} {'Max unc.':<12} {'Max con.':<12} {'f_sq unc.':<12} {'f_sq con.':<12}")
print(f"{'A(active)':<10} {'16.0':<12} {val_A_unc:<12.4f} {val_A_con:<12.4f} {val_A_unc-16:<12.4f} {val_A_con-16:<12.4f}")
print(f"{'I(inact.)':<10} {'0.0':<12} {val_I_unc:<12.4f} {val_I_con:<12.4f} {val_I_unc:<12.4f} {val_I_con:<12.4f}")

print("\n" + "=" * 60)
print("GLOBAL SUM ANALYSIS")
print("=" * 60)
# Worst case global sum if per-plaquette maxima achieved simultaneously:
worst_A = 64 * (val_A_con - 16)  # 64 active plaquettes
worst_I = 32 * val_I_con          # 32 inactive plaquettes
print(f"If all active plaquettes at max: 64 * {val_A_con-16:.4f} = {worst_A:.4f}")
print(f"If all inactive plaquettes at max: 32 * {val_I_con:.4f} = {worst_I:.4f}")
print(f"Worst case total f_sq: {worst_A + worst_I:.4f}")
print(f"Need total f_sq <= 0 for conjecture")
