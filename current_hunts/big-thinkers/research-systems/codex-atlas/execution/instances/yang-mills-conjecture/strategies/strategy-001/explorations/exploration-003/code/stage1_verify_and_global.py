"""
Verify constrained maximizer analytically, then do full global computation.
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
    """Map (x, mu) to a unique index in [0, 64)."""
    idx = 0
    for i in range(d):
        idx = idx * L + x[i]
    return idx * d + mu

# Build plaquette list with full edge info
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
                'x': x, 'mu': mu, 'nu': nu,
                'e1': e1, 'e2': e2, 'e3': e3, 'e4': e4,
                'e1_idx': edge_index(*e1), 'e2_idx': edge_index(*e2),
                'e3_idx': edge_index(*e3), 'e4_idx': edge_index(*e4),
                'eff': eff,
                'active': active
            })

print(f"Total plaquettes: {len(plaquettes)}")
print(f"Total edges: {L**d * d} = {16*4}")

# =====================================================
# Verify constrained per-plaquette max IS 16
# =====================================================

print("\n" + "=" * 60)
print("VERIFY: Constrained per-plaquette max = 16")
print("=" * 60)

n = np.array([0., 0., 1.])
q_id = np.array([1., 0., 0., 0.])
q_i = np.array([0., 1., 0., 0.])  # pure imaginary quaternion i
q_j = np.array([0., 0., 1., 0.])

# Type A analytical maximizer: q1=id, q4=id, q2*q3^{-1} = i (or any pure imag)
# R1 = Ad(q1) = I
# R2 = Ad(q1*q2*q3^{-1}) = Ad(i) = rotation by pi around x
# R3 = Ad(q1*q2*q3^{-1}*q4^{-1}) = Ad(i) = same as R2
q1 = q_id
q2 = q_i  # q2 = i
q3 = q_id  # q3 = 1, so q2*q3^{-1} = i
q4 = q_id

R1 = quat_to_rot(q1)
partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
R2 = quat_to_rot(partial)
usq = quat_mult(partial, quat_inv(q4))
R3 = quat_to_rot(usq)

bA = n + R1@n - R2@n - R3@n
print(f"Type A: q1=1, q2=i, q3=1, q4=1")
print(f"  R1 = {R1.diagonal()}")
print(f"  R2 = {R2.diagonal()}")
print(f"  R3 = {R3.diagonal()}")
print(f"  B = {bA}, |B|^2 = {np.dot(bA, bA):.4f}")

# Type I analytical maximizer: want R1=R2=pi_x, R3=I
# R1 = Ad(q1) = pi_x => q1 = ±i
# R3 = Ad(q1*q2*q3^{-1}*q4^{-1}) = I => q1*q2*q3^{-1}*q4^{-1} = ±1
# R2 = Ad(q1*q2*q3^{-1}) = pi_x => q1*q2*q3^{-1} = ±i
# From R1: q1 = i. From R2: i*q2*q3^{-1} = ±i, so q2*q3^{-1} = ±1.
# Take q2 = q3. Then partial = q1*q2*q3^{-1} = q1 = i. R2 = Ad(i) = pi_x. ✓
# R3: q1*q2*q3^{-1}*q4^{-1} = i*q4^{-1}. Need this = ±1.
# i*q4^{-1} = ±1 => q4^{-1} = ∓i => q4 = ±i.
q1 = q_i
q2 = q_id
q3 = q_id
q4 = q_i

R1 = quat_to_rot(q1)
partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
R2 = quat_to_rot(partial)
usq = quat_mult(partial, quat_inv(q4))
R3 = quat_to_rot(usq)

bI = n - R1@n - R2@n + R3@n
print(f"\nType I: q1=i, q2=1, q3=1, q4=i")
print(f"  R1 = Ad(q1) diag = {R1.diagonal()}")
print(f"  R2 = Ad(q1*q2*q3^{-1}) diag = {R2.diagonal()}")
print(f"  R3 = Ad(q1*q2*q3^{-1}*q4^{-1}) diag = {R3.diagonal()}")
print(f"  B = {bI}, |B|^2 = {np.dot(bI, bI):.4f}")

# Confirm: constrained max = 16 for BOTH types
print("\n>>> CONFIRMED: Constrained per-plaquette max = 16 for both types.")
print(">>> The per-plaquette bound is FALSE (f_sq can be positive).")
print(">>> The conjecture REQUIRES global constraints.\n")

# =====================================================
# FULL GLOBAL COMPUTATION: Sum_sq f_sq for random configs
# =====================================================

print("=" * 60)
print("GLOBAL SUM: Sum_sq f_sq over all 96 plaquettes")
print("=" * 60)

def compute_full_bsq_sum(Q, n):
    """
    Compute Sum_sq |B_sq(Q, v_stag)|^2 for the staggered mode with color n.
    Q is a dict mapping edge_index -> SU(2) quaternion.
    """
    total = 0.0
    for p in plaquettes:
        q1 = Q[p['e1_idx']]
        q2 = Q[p['e2_idx']]
        q3 = Q[p['e3_idx']]
        q4 = Q[p['e4_idx']]

        # R1 = Ad(Q_{e1})
        R1 = quat_to_rot(q1)
        # R2 = Ad(Q_{e1} Q_{e2} Q_{e3}^{-1})
        partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
        R2 = quat_to_rot(partial)
        # R3 = Ad(U_sq) = Ad(Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1})
        usq = quat_mult(partial, quat_inv(q4))
        R3 = quat_to_rot(usq)

        c1, c2, c3, c4 = p['eff']
        # B_sq = c1*n + c2*R1*n + c3*R2*n + c4*R3*n
        B = c1 * n + c2 * (R1 @ n) + c3 * (R2 @ n) + c4 * (R3 @ n)
        total += np.dot(B, B)

    return total

# At Q=I
Q_id = {i: np.array([1., 0., 0., 0.]) for i in range(64)}
sum_I = compute_full_bsq_sum(Q_id, n)
print(f"\nAt Q=I: Sum |B_sq|^2 = {sum_I:.4f}")
print(f"Expected: 4d * |v|^2 = {16 * 64:.4f}")
print(f"Match: {abs(sum_I - 16*64) < 0.01}")

# Random configs
np.random.seed(123)
n_trials = 2000
max_sum = -np.inf
min_sum = np.inf
exceed_count = 0
fsq_values = []

for trial in range(n_trials):
    Q = {i: random_quat() for i in range(64)}
    s = compute_full_bsq_sum(Q, n)
    fsq = s - 1024.0  # f_sq = Sum |B_sq(Q)|^2 - Sum |B_sq(I)|^2
    fsq_values.append(fsq)
    max_sum = max(max_sum, s)
    min_sum = min(min_sum, s)
    if s > 1024.0 + 0.01:
        exceed_count += 1

print(f"\nOver {n_trials} random configs:")
print(f"  Min Sum |B_sq|^2 = {min_sum:.4f}")
print(f"  Max Sum |B_sq|^2 = {max_sum:.4f}")
print(f"  Threshold (4d*|v|^2) = 1024.0000")
print(f"  Exceeded: {exceed_count}/{n_trials}")
print(f"  Max f_sq = {max(fsq_values):.6f}")
print(f"  Mean f_sq = {np.mean(fsq_values):.4f}")
print(f"  Min f_sq = {min(fsq_values):.4f}")

# Breakdown: active vs inactive contribution
print("\n" + "=" * 60)
print("BREAKDOWN: Active vs Inactive contribution")
print("=" * 60)

def compute_breakdown(Q, n):
    active_sum = 0.0
    inactive_sum = 0.0
    for p in plaquettes:
        q1 = Q[p['e1_idx']]
        q2 = Q[p['e2_idx']]
        q3 = Q[p['e3_idx']]
        q4 = Q[p['e4_idx']]

        R1 = quat_to_rot(q1)
        partial = quat_mult(quat_mult(q1, q2), quat_inv(q3))
        R2 = quat_to_rot(partial)
        usq = quat_mult(partial, quat_inv(q4))
        R3 = quat_to_rot(usq)

        c1, c2, c3, c4 = p['eff']
        B = c1 * n + c2 * (R1 @ n) + c3 * (R2 @ n) + c4 * (R3 @ n)
        bsq = np.dot(B, B)

        if p['active']:
            active_sum += bsq
        else:
            inactive_sum += bsq

    return active_sum, inactive_sum

# At Q=I:
a_I, i_I = compute_breakdown(Q_id, n)
print(f"At Q=I: active = {a_I:.4f}, inactive = {i_I:.4f}, total = {a_I+i_I:.4f}")

# Sample configs
np.random.seed(456)
print(f"\n{'Trial':<8} {'Active':<12} {'Inactive':<12} {'Total':<12} {'f_active':<12} {'f_inactive':<12} {'f_total':<12}")
for trial in range(20):
    Q = {i: random_quat() for i in range(64)}
    a_Q, i_Q = compute_breakdown(Q, n)
    f_active = a_Q - a_I
    f_inactive = i_Q - i_I
    f_total = (a_Q + i_Q) - (a_I + i_I)
    print(f"{trial:<8} {a_Q:<12.4f} {i_Q:<12.4f} {a_Q+i_Q:<12.4f} {f_active:<12.4f} {f_inactive:<12.4f} {f_total:<12.4f}")

# Try adversarial: all edge quaternions = i (maximizes Type A per-plaquette)
print("\n--- Adversarial configs ---")
for label, q_val in [
    ("all q=i", np.array([0.,1.,0.,0.])),
    ("all q=j", np.array([0.,0.,1.,0.])),
    ("all q=k", np.array([0.,0.,0.,1.])),
    ("all q=(1+i)/sqrt2", np.array([1.,1.,0.,0.])/np.sqrt(2)),
    ("all q=(-1+i)/sqrt2", np.array([-1.,1.,0.,0.])/np.sqrt(2)),
]:
    Q_adv = {i: q_val.copy() for i in range(64)}
    a_Q, i_Q = compute_breakdown(Q_adv, n)
    f_total = (a_Q + i_Q) - 1024
    print(f"  {label:<25}: active={a_Q:.4f}, inactive={i_Q:.4f}, total={a_Q+i_Q:.4f}, f_sq={f_total:.4f}")

# Try: one edge differs
print("\n--- Single-edge perturbation from Q=I ---")
for angle in [0.1, 0.5, 1.0, np.pi/2, np.pi]:
    Q_pert = {i: np.array([1., 0., 0., 0.]) for i in range(64)}
    Q_pert[0] = np.array([np.cos(angle/2), np.sin(angle/2), 0., 0.])
    a_Q, i_Q = compute_breakdown(Q_pert, n)
    f_total = (a_Q + i_Q) - 1024
    # Also compute Wilson action
    wilson_sum = 0.0
    for p in plaquettes:
        q1 = Q_pert[p['e1_idx']]
        q2 = Q_pert[p['e2_idx']]
        q3 = Q_pert[p['e3_idx']]
        q4 = Q_pert[p['e4_idx']]
        usq = quat_mult(quat_mult(quat_mult(q1, q2), quat_inv(q3)), quat_inv(q4))
        # Tr(U_sq) in fundamental = 2*Re(usq[0]) for SU(2) in quaternion form
        # But for adjoint: 1 - cos(theta) where cos(theta) = 2*usq[0]^2 - 1
        cos_theta = 2*usq[0]**2 - 1
        wilson_sum += (1 - cos_theta)
    print(f"  angle={angle:.4f}: f_sq={f_total:.6f}, Sum(1-cos theta_sq)={wilson_sum:.6f}, ratio={f_total/wilson_sum if wilson_sum > 1e-10 else 'inf'}")
