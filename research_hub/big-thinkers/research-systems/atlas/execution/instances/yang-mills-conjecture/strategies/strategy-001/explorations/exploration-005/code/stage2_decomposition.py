"""
Stage 2: Algebraic decomposition of F_x into base-link and cross-link contributions.

Key decomposition (derived analytically):

For vertex x=0, WLOG |x|=0:
  B_{mu,nu} = a*(n + R_mu D_{mu,nu} n) + b*(R_mu n + R_mu D_{mu,nu} R_nu^T n)

where a = (-1)^mu, b = (-1)^{nu+1}, R_mu = Ad(Q_{0,mu}), D_{mu,nu} = Ad(Q_{e_mu,nu} Q_{e_nu,mu}^{-1})

|B|^2 = |u|^2 + |v|^2 + 2*sigma*<u, R_mu*v>

where u = n + R_mu D n, v = n + D R_nu^T n, sigma = (-1)^{mu+nu+1}

= 4 + 2*n^T R_mu D n + 2*n^T D R_nu^T n + 2*sigma*(n^T R_mu n + n^T D n + n^T R_nu n + n^T R_mu D R_nu^T n)

F_x = sum_{mu<nu} |B_{mu,nu}|^2

For D = I (cross-links = identity):
  F_x = 32 + 8<n,W> - |A|^2  where W = sum w_mu, A = sum s_mu w_mu

We decompose: F_x = F_base + Delta  where Delta = F_x - F_base depends on D_{mu,nu}.

Goal: Show Delta <= 0 for all base links and all cross-links.
"""

import numpy as np
from itertools import product as iproduct

np.random.seed(123)

# ============================================================
# SO(3) utilities
# ============================================================

def random_so3():
    """Random SO(3) via random quaternion."""
    q = np.random.randn(4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])

def so3_from_axis_angle(axis, angle):
    """SO(3) from axis-angle."""
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)

# ============================================================
# Plaquette structure
# ============================================================

# Active: mu+nu odd -> sigma = +1
# Inactive: mu+nu even -> sigma = -1
# Planes: (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)

planes = [(mu, nu) for mu in range(4) for nu in range(mu+1, 4)]
sigmas = {(mu,nu): (-1)**(mu+nu+1) for mu,nu in planes}

print("Plane classification:")
for mu, nu in planes:
    s = sigmas[(mu,nu)]
    typ = "active" if s == 1 else "inactive"
    print(f"  ({mu},{nu}): sigma = {s:+d}, type = {typ}")

# ============================================================
# F_x computation from SO(3) matrices
# ============================================================

def compute_Fx_from_matrices(R, D, n):
    """
    Compute F_x given:
      R = [R_0, R_1, R_2, R_3]  (4 base SO(3) matrices)
      D = {(mu,nu): D_{mu,nu}}  (6 cross-link SO(3) matrices)
      n = unit vector in R^3
    """
    Fx = 0.0
    for mu, nu in planes:
        R_mu = R[mu]
        R_nu = R[nu]
        D_mn = D[(mu,nu)]
        sigma = sigmas[(mu,nu)]

        # u = n + R_mu D n
        u = n + R_mu @ D_mn @ n
        # v = n + D R_nu^T n
        v = n + D_mn @ R_nu.T @ n

        # |B|^2 = |u|^2 + |v|^2 + 2*sigma*<u, R_mu*v>
        B_sq = np.dot(u, u) + np.dot(v, v) + 2 * sigma * np.dot(u, R_mu @ v)
        Fx += B_sq

    return Fx

def compute_Fx_base(R, n):
    """F_x with cross-links = I (the proved case)."""
    D_identity = {(mu,nu): np.eye(3) for mu,nu in planes}
    return compute_Fx_from_matrices(R, D_identity, n)

def compute_Fx_formula(R, n):
    """F_x via the closed-form formula: 32 + 8<n,W> - |A|^2"""
    w = [R[mu].T @ n for mu in range(4)]
    W = sum(w)
    s = [(-1)**mu for mu in range(4)]  # staggered signs for |x|=0
    A = sum(s[mu] * w[mu] for mu in range(4))
    return 32 + 8 * np.dot(n, W) - np.dot(A, A)

# ============================================================
# Verify decomposition
# ============================================================

n = np.array([1.0, 0.0, 0.0])

print("\n" + "=" * 70)
print("VERIFICATION: F_x from matrices vs closed formula (cross-links=I)")
print("=" * 70)

max_err = 0.0
for trial in range(100):
    R = [random_so3() for _ in range(4)]
    Fx_mat = compute_Fx_base(R, n)
    Fx_form = compute_Fx_formula(R, n)
    err = abs(Fx_mat - Fx_form)
    max_err = max(max_err, err)

print(f"Max discrepancy over 100 trials: {max_err:.2e}")
print(f"RESULT: {'PASS' if max_err < 1e-10 else 'FAIL'}")

# ============================================================
# Stage 2.1: Detailed inner-product decomposition
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2.1: Decompose F_x into inner-product terms")
print("=" * 70)

def decompose_Fx(R, D, n):
    """
    Decompose F_x into individual inner-product terms.
    Returns dict of named contributions.
    """
    terms = {}

    # Constant term
    terms['constant'] = 24.0  # 6 plaquettes × 4

    # d terms: n^T R_mu D n
    d_sum = 0.0
    for mu, nu in planes:
        d_sum += n @ R[mu] @ D[(mu,nu)] @ n  # d_{mu,nu}
        d_sum += n @ D[(mu,nu)] @ R[nu].T @ n  # d'_{mu,nu}
    terms['d_terms'] = 2 * d_sum

    # sigma * p terms (base link only)
    sigma_p = 0.0
    for mu, nu in planes:
        sigma_p += sigmas[(mu,nu)] * (n @ R[mu] @ n + n @ R[nu] @ n)
    terms['sigma_p'] = 2 * sigma_p

    # sigma * e terms: sigma * n^T D n
    sigma_e = 0.0
    for mu, nu in planes:
        sigma_e += sigmas[(mu,nu)] * (n @ D[(mu,nu)] @ n)
    terms['sigma_e'] = 2 * sigma_e

    # sigma * f terms: sigma * n^T R_mu D R_nu^T n
    sigma_f = 0.0
    for mu, nu in planes:
        sigma_f += sigmas[(mu,nu)] * (n @ R[mu] @ D[(mu,nu)] @ R[nu].T @ n)
    terms['sigma_f'] = 2 * sigma_f

    terms['total'] = sum(terms[k] for k in ['constant', 'd_terms', 'sigma_p', 'sigma_e', 'sigma_f'])
    return terms

# Verify decomposition
print("\nVerify decomposition agrees with direct computation:")
max_err = 0.0
for trial in range(100):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}

    Fx_direct = compute_Fx_from_matrices(R, D, n)
    terms = decompose_Fx(R, D, n)
    err = abs(Fx_direct - terms['total'])
    max_err = max(max_err, err)

print(f"Max discrepancy: {max_err:.2e}")
print(f"RESULT: {'PASS' if max_err < 1e-10 else 'FAIL'}")

# Verify cross-links=I decomposition
print("\nFor cross-links=I:")
R = [random_so3() for _ in range(4)]
D_I = {(mu,nu): np.eye(3) for mu,nu in planes}
terms_I = decompose_Fx(R, D_I, n)
for k, v in terms_I.items():
    print(f"  {k}: {v:.6f}")

# ============================================================
# Stage 2.2: Monotonicity test — is F_x maximized at D = I?
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2.2: Cross-link monotonicity test")
print("=" * 70)

n_tests = 1000
n_cross = 50  # random cross-link configs per base

monotone_violations = 0
max_delta = -np.inf
min_delta = np.inf

for trial in range(n_tests):
    R = [random_so3() for _ in range(4)]
    Fx_base = compute_Fx_base(R, n)

    for _ in range(n_cross):
        D = {(mu,nu): random_so3() for mu,nu in planes}
        Fx_gen = compute_Fx_from_matrices(R, D, n)
        delta = Fx_gen - Fx_base
        max_delta = max(max_delta, delta)
        min_delta = min(min_delta, delta)

        if delta > 1e-10:
            monotone_violations += 1

print(f"Tests: {n_tests} base configs × {n_cross} cross-link configs = {n_tests*n_cross}")
print(f"Max Delta (F_general - F_base): {max_delta:.6f}")
print(f"Min Delta: {min_delta:.6f}")
print(f"Monotonicity violations: {monotone_violations}")
print(f"RESULT: {'MONOTONICITY HOLDS' if monotone_violations == 0 else 'MONOTONICITY FAILS'}")

# ============================================================
# Stage 2.3: Adversarial gradient ascent over cross-links
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2.3: Adversarial gradient ascent over D (cross-links)")
print("=" * 70)

def gradient_ascent_crosslinks(R, n, n_steps=500, lr=0.01):
    """
    For fixed base links R, do gradient ascent over cross-links D to maximize F_x.
    Parameterize each D_{mu,nu} by axis-angle (3 params each).
    """
    # 6 cross-link rotations, each parameterized by 3-vector (axis * angle)
    params = np.zeros(18)  # Start at D = I

    best_Fx = compute_Fx_base(R, n)
    best_params = params.copy()

    for step in range(n_steps):
        # Compute gradient by finite differences
        eps = 1e-5
        D = {}
        for i, (mu, nu) in enumerate(planes):
            aa = params[3*i:3*i+3]
            angle = np.linalg.norm(aa)
            if angle < 1e-12:
                D[(mu,nu)] = np.eye(3)
            else:
                D[(mu,nu)] = so3_from_axis_angle(aa/angle, angle)

        Fx_curr = compute_Fx_from_matrices(R, D, n)

        grad = np.zeros(18)
        for j in range(18):
            params_p = params.copy()
            params_p[j] += eps
            D_p = {}
            for i, (mu, nu) in enumerate(planes):
                aa = params_p[3*i:3*i+3]
                angle = np.linalg.norm(aa)
                if angle < 1e-12:
                    D_p[(mu,nu)] = np.eye(3)
                else:
                    D_p[(mu,nu)] = so3_from_axis_angle(aa/angle, angle)
            grad[j] = (compute_Fx_from_matrices(R, D_p, n) - Fx_curr) / eps

        params += lr * grad

        if Fx_curr > best_Fx:
            best_Fx = Fx_curr
            best_params = params.copy()

    return best_Fx, best_params

# Run adversarial tests
max_adv_Fx = 0.0
max_adv_delta = -np.inf

print("Running adversarial gradient ascent (50 base configs, 500 steps each)...")
for trial in range(50):
    R = [random_so3() for _ in range(4)]
    Fx_base = compute_Fx_base(R, n)
    Fx_adv, params_adv = gradient_ascent_crosslinks(R, n)
    delta = Fx_adv - Fx_base

    max_adv_Fx = max(max_adv_Fx, Fx_adv)
    max_adv_delta = max(max_adv_delta, delta)

    if trial < 5 or delta > -0.1:
        print(f"  Trial {trial:2d}: F_base = {Fx_base:.4f}, F_adv = {Fx_adv:.4f}, delta = {delta:.6f}")

print(f"\nMax adversarial F_x: {max_adv_Fx:.6f}")
print(f"Max adversarial Delta: {max_adv_delta:.6f}")
print(f"RESULT: {'MONOTONICITY HOLDS' if max_adv_delta < 1e-6 else 'MONOTONICITY FAILS'}")

# ============================================================
# Stage 2.4: Per-term Delta analysis
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2.4: Per-term Delta analysis")
print("=" * 70)

# For the Delta, decompose into Delta_d, Delta_e, Delta_f
def compute_deltas(R, D, n):
    """Compute Delta = Delta_d + Delta_e + Delta_f"""
    D_I = {(mu,nu): np.eye(3) for mu,nu in planes}

    terms_gen = decompose_Fx(R, D, n)
    terms_base = decompose_Fx(R, D_I, n)

    Delta_d = terms_gen['d_terms'] - terms_base['d_terms']
    Delta_e = terms_gen['sigma_e'] - terms_base['sigma_e']
    Delta_f = terms_gen['sigma_f'] - terms_base['sigma_f']
    Delta_total = Delta_d + Delta_e + Delta_f

    return Delta_d, Delta_e, Delta_f, Delta_total

print("Sampling 500 random (R, D) configs:")
Delta_d_vals = []
Delta_e_vals = []
Delta_f_vals = []
Delta_tot_vals = []

for _ in range(500):
    R = [random_so3() for _ in range(4)]
    D = {(mu,nu): random_so3() for mu,nu in planes}
    dd, de, df, dt = compute_deltas(R, D, n)
    Delta_d_vals.append(dd)
    Delta_e_vals.append(de)
    Delta_f_vals.append(df)
    Delta_tot_vals.append(dt)

print(f"  Delta_d: min={min(Delta_d_vals):.4f}, max={max(Delta_d_vals):.4f}, mean={np.mean(Delta_d_vals):.4f}")
print(f"  Delta_e: min={min(Delta_e_vals):.4f}, max={max(Delta_e_vals):.4f}, mean={np.mean(Delta_e_vals):.4f}")
print(f"  Delta_f: min={min(Delta_f_vals):.4f}, max={max(Delta_f_vals):.4f}, mean={np.mean(Delta_f_vals):.4f}")
print(f"  Delta_total: min={min(Delta_tot_vals):.4f}, max={max(Delta_tot_vals):.4f}, mean={np.mean(Delta_tot_vals):.4f}")
print(f"\n  Max Delta_total: {max(Delta_tot_vals):.6f}")
print(f"  Delta_total > 0 count: {sum(1 for d in Delta_tot_vals if d > 1e-10)}")

# ============================================================
# Stage 2.5: Special analysis — D affects only one plaquette
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2.5: Single-plaquette cross-link effect")
print("=" * 70)

# Turn on D for just one plaquette at a time
for target_plane in planes:
    max_delta_sp = -np.inf
    for _ in range(200):
        R = [random_so3() for _ in range(4)]
        D = {(mu,nu): np.eye(3) for mu,nu in planes}
        D[target_plane] = random_so3()

        Fx_gen = compute_Fx_from_matrices(R, D, n)
        Fx_base = compute_Fx_base(R, n)
        delta = Fx_gen - Fx_base
        max_delta_sp = max(max_delta_sp, delta)

    typ = "active" if sigmas[target_plane] == 1 else "inactive"
    print(f"  Plane {target_plane} ({typ}): max Delta = {max_delta_sp:.6f}")

print("\nDone with Stage 2.")
