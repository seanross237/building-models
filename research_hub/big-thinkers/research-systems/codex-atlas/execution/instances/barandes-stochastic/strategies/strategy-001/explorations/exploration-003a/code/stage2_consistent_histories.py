"""
Stage 2: Construct the Consistent History Families for a Qubit

System: H = (omega/2)*sigma_z, initial state rho_0 = |+><+|
Times: t_0 = 0, t_1 = pi/4, t_2 = pi/2

A history family at time t_1 is a choice of orthonormal basis {|a>, |a_perp>}
defining projectors P_a = |a><a|, P_{a_perp} = |a_perp><a_perp|.

For a qubit, every basis is parameterized by a point on the Bloch sphere:
  |a> = cos(theta/2)|0> + e^(i*phi)*sin(theta/2)|1>
  |a_perp> = sin(theta/2)|0> - e^(i*phi)*cos(theta/2)|1>

At t_2, we also need a basis choice. So a full 3-time history family
requires choosing bases at t_1 AND t_2.

The consistency condition (decoherence functional off-diagonal = 0) constrains
which combinations of (basis_t1, basis_t2) are allowed.

For SIMPLICITY, and following the GOAL: we fix the basis at t_2 to be the
computational basis {|0>,|1>} (a common choice), and find all consistent
bases at t_1. This is the standard CH realm selection problem at a single time.

Then we also do the full 2-time analysis.
"""

import numpy as np
from itertools import product

print("=" * 70)
print("STAGE 2: Consistent History Families for Qubit")
print("=" * 70)

# ============================================================
# Setup
# ============================================================
omega = 1.0
t1 = np.pi / 4
t2 = np.pi / 2

# Unitary evolution
def U(t):
    return np.array([
        [np.cos(t), -1j * np.sin(t)],
        [-1j * np.sin(t), np.cos(t)]
    ], dtype=complex)

U1 = U(t1)  # U(0 -> t1)
U2 = U(t2)  # U(0 -> t2)
U12 = U(t2 - t1)  # U(t1 -> t2)

print(f"U(t1) = U(π/4) =\n{U1}")
print(f"U(t2) = U(π/2) =\n{U2}")
print(f"U(t2-t1) = U(π/4) =\n{U12}")
print(f"Verify: U12 @ U1 ≈ U2? {np.allclose(U12 @ U1, U2)}")

# Initial state: |+> = (|0> + |1>)/sqrt(2)
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
rho_0 = np.outer(plus, plus.conj())
print(f"\nrho_0 = |+><+| =\n{rho_0}")

# ============================================================
# Part A: Single-time consistency (basis at t_1, fixed t_2 = comp basis)
# ============================================================
print(f"\n{'='*70}")
print("PART A: Single-time consistency condition")
print("(Fix t_2 projectors = computational basis, vary t_1 basis)")
print("=" * 70)

# A qubit basis is parameterized by (theta, phi):
# |a> = cos(th/2)|0> + e^(i*ph)*sin(th/2)|1>
# P_a = |a><a|, P_{a_perp} = I - P_a

def make_projector(theta, phi):
    """Make projector P = |a><a| for the state parameterized by (theta, phi)."""
    a = np.array([np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)], dtype=complex)
    return np.outer(a, a.conj())

def decoherence_functional(P1_list, P2_list, rho_0, U1, U12):
    """
    Compute the decoherence functional for 3-time histories.

    History (alpha_1, alpha_2):
      C_{a1,a2} = P2_{a2} U12 P1_{a1} U1 (chain operator, Heisenberg-like)

    D(a1 a2, a1' a2') = Tr(C_{a1,a2} rho_0 C_{a1',a2'}^dag)

    For consistency: D(a1 a2, a1' a2') = 0 whenever (a1,a2) != (a1',a2')
    """
    n1 = len(P1_list)
    n2 = len(P2_list)

    # Compute chain operators C_{a1,a2} = P2_{a2} @ U12 @ P1_{a1} @ U1
    chains = []
    for a1 in range(n1):
        for a2 in range(n2):
            C = P2_list[a2] @ U12 @ P1_list[a1] @ U1
            chains.append(((a1, a2), C))

    # Compute D matrix
    D = np.zeros((n1*n2, n1*n2), dtype=complex)
    for i, (idx_i, C_i) in enumerate(chains):
        for j, (idx_j, C_j) in enumerate(chains):
            D[i, j] = np.trace(C_i @ rho_0 @ C_j.conj().T)

    return D, chains

# t_2 projectors: computational basis
P2_0 = np.array([[1, 0], [0, 0]], dtype=complex)
P2_1 = np.array([[0, 0], [0, 1]], dtype=complex)
P2_list = [P2_0, P2_1]

# Scan over t_1 bases parameterized by (theta, phi) on the Bloch sphere
print("\nScanning (theta, phi) for consistent bases at t_1:")
print("Consistency = all off-diagonal elements of D are zero (or |D_offdiag| < tol)")

n_theta = 200
n_phi = 200
tol = 1e-8

consistent_bases = []
consistency_map = np.zeros((n_theta, n_phi))

theta_vals = np.linspace(0.01, np.pi - 0.01, n_theta)
phi_vals = np.linspace(0, 2*np.pi - 0.01, n_phi)

for i, theta in enumerate(theta_vals):
    for j, phi in enumerate(phi_vals):
        P1_a = make_projector(theta, phi)
        P1_b = np.eye(2) - P1_a  # orthogonal complement
        P1_list = [P1_a, P1_b]

        D, chains = decoherence_functional(P1_list, P2_list, rho_0, U1, U12)

        # Check off-diagonal: for 4x4 D, off-diag means (i,j) with i != j
        # But we also need to check: within each choice of a2, the a1 values decohere
        # The full D is indexed by (a1, a2) pairs
        max_offdiag = 0
        for ii in range(D.shape[0]):
            for jj in range(D.shape[1]):
                if ii != jj:
                    max_offdiag = max(max_offdiag, abs(D[ii, jj]))

        consistency_map[i, j] = max_offdiag

        if max_offdiag < tol:
            consistent_bases.append((theta, phi, max_offdiag))

print(f"\nFound {len(consistent_bases)} consistent bases (out of {n_theta*n_phi} scanned)")

if consistent_bases:
    print(f"\nConsistent bases (theta, phi, max_offdiag):")
    # Group by theta to see the pattern
    thetas_found = sorted(set([round(b[0], 4) for b in consistent_bases]))
    print(f"  Distinct theta values: {len(thetas_found)}")
    for th in thetas_found[:10]:  # show first 10
        phis = sorted([b[1] for b in consistent_bases if abs(b[0] - th) < 0.01])
        print(f"    theta = {th:.4f} ({th/np.pi:.4f}π): {len(phis)} phi values: [{phis[0]:.3f}, {phis[-1]:.3f}]" if phis else "")
    if len(thetas_found) > 10:
        print(f"    ... and {len(thetas_found) - 10} more theta values")
else:
    print("  NO consistent bases found with strict decoherence (tol=1e-8)")

# ============================================================
# Part B: Try weak (medium) consistency
# ============================================================
print(f"\n{'='*70}")
print("PART B: Weak consistency (Re[D_offdiag] = 0)")
print("=" * 70)

tol_weak = 1e-8
weak_consistent = []
weak_map = np.zeros((n_theta, n_phi))

for i, theta in enumerate(theta_vals):
    for j, phi in enumerate(phi_vals):
        P1_a = make_projector(theta, phi)
        P1_b = np.eye(2) - P1_a
        P1_list = [P1_a, P1_b]

        D, chains = decoherence_functional(P1_list, P2_list, rho_0, U1, U12)

        max_re_offdiag = 0
        for ii in range(D.shape[0]):
            for jj in range(D.shape[1]):
                if ii != jj:
                    max_re_offdiag = max(max_re_offdiag, abs(D[ii, jj].real))

        weak_map[i, j] = max_re_offdiag

        if max_re_offdiag < tol_weak:
            weak_consistent.append((theta, phi, max_re_offdiag))

print(f"Found {len(weak_consistent)} weakly consistent bases")

if weak_consistent:
    thetas_found_w = sorted(set([round(b[0], 4) for b in weak_consistent]))
    print(f"  Distinct theta values: {len(thetas_found_w)}")
    for th in thetas_found_w[:10]:
        phis = sorted([b[1] for b in weak_consistent if abs(b[0] - th) < 0.01])
        if phis:
            print(f"    theta = {th:.4f} ({th/np.pi:.4f}π): {len(phis)} phi values: [{phis[0]:.3f}, {phis[-1]:.3f}]")
    if len(thetas_found_w) > 10:
        print(f"    ... and {len(thetas_found_w) - 10} more theta values")

# ============================================================
# Part C: Simplify — single-time histories (no t_2 projectors)
# ============================================================
print(f"\n{'='*70}")
print("PART C: Single-time histories (projectors only at t_1)")
print("=" * 70)

# For a single intermediate time, the decoherence functional simplifies to:
# D(a, a') = Tr(P_a(t_1) rho_1 P_{a'}(t_1))
# where rho_1 = U1 rho_0 U1^dag is the state at t_1
#
# Wait, that's not quite right for CH. The standard formula for histories
# with projectors at a single time t_1 (and identity at t_0, t_2):
#
# D(a, a') = Tr(P_a rho_1 P_{a'})
# where rho_1 = U(t_1) rho_0 U(t_1)^dag
#
# Consistency: D(a, a') = 0 for a != a'
# This means P_a rho_1 P_{a'} must have trace 0 for a != a'.
#
# For a qubit with P_a = |a><a|, P_{a'} = |a_perp><a_perp|:
# D(a, a') = <a|rho_1|a_perp> <a_perp|...wait, let me compute:
# Tr(|a><a| rho_1 |a_perp><a_perp|) = <a_perp|a><a|rho_1|a_perp> = 0
# since <a_perp|a> = 0 (orthogonal projectors!)
#
# So for a single projective decomposition at one time:
# D(a,a') = delta_{a,a'} * <a|rho_1|a>
# ALL bases are trivially consistent!

rho_1 = U1 @ rho_0 @ U1.conj().T
print(f"rho_1 = U1 rho_0 U1^dag =\n{rho_1}")

print("\nFor single-time histories with projective decomposition at t_1:")
print("D(a, a') = Tr(P_a rho_1 P_{a'}) = <a'|a><a|rho_1|a'> = delta_{a,a'}<a|rho_1|a>")
print("=> D is automatically diagonal for ANY orthonormal basis!")
print("=> ALL bases are consistent (trivially)")
print("=> Consistent family space = full Bloch sphere S^2 (modulo phases)")
print("=> Real dimension = 2")

# Verify numerically
print("\nNumerical verification:")
for theta, phi, label in [(0, 0, "z-basis"), (np.pi/2, 0, "x-basis"),
                            (np.pi/2, np.pi/2, "y-basis"), (np.pi/4, np.pi/6, "random")]:
    P_a = make_projector(theta, phi)
    P_b = np.eye(2) - P_a
    D_aa = np.trace(P_a @ rho_1 @ P_a).real
    D_bb = np.trace(P_b @ rho_1 @ P_b).real
    D_ab = abs(np.trace(P_a @ rho_1 @ P_b))
    D_ba = abs(np.trace(P_b @ rho_1 @ P_a))
    print(f"  {label:10s}: D(a,a)={D_aa:.4f}, D(b,b)={D_bb:.4f}, |D(a,b)|={D_ab:.2e}, |D(b,a)|={D_ba:.2e}")

# ============================================================
# Part D: 3-time histories — vary both t_1 AND t_2 bases
# ============================================================
print(f"\n{'='*70}")
print("PART D: Full 3-time histories — vary basis at both t_1 and t_2")
print("=" * 70)

# Now the real problem: choose bases at t_1 AND t_2, check consistency.
# This is a 4-parameter space: (theta_1, phi_1, theta_2, phi_2)
# We need to find the subspace where the decoherence functional is diagonal.

# The decoherence functional for a history (a1, a2) with projectors at t_1 and t_2:
# C_{a1,a2} = P2_{a2}(t_2) P1_{a1}(t_1) (in Schrodinger picture with evolution inserted)
# Actually, the correct chain operator in Schrodinger picture is:
# C_{a1,a2} = U(t2,t1)^dag P2_{a2} U(t2,t1) . U(t1,0)^dag P1_{a1} U(t1,0)
# No wait. Let me be more careful.

# Standard CH: history class operator
# C_{a1,a2} = P_{a2}^{t2} . P_{a1}^{t1}
# where P_a^{t} = U(t)^dag P_a U(t) (Heisenberg picture projectors)
#
# Or equivalently in Schrodinger picture:
# C_{a1,a2} = P_{a2} U(t2-t1) P_{a1} U(t1) (applied to initial state)

# Decoherence functional:
# D((a1,a2), (a1',a2')) = Tr(C_{a1,a2} rho_0 C_{a1',a2'}^dag)

# For a qubit at each time, there are 2 projectors each, so 4 histories total.
# D is a 4x4 matrix. Consistency requires off-diagonal = 0.

# Let's do a coarser scan of the 4D space
n_th = 30
n_ph = 30

theta_vals2 = np.linspace(0.05, np.pi - 0.05, n_th)
phi_vals2 = np.linspace(0, 2*np.pi - 0.05, n_ph)

consistent_3time = []
n_checked = 0

print(f"Scanning 4D space: ({n_th} theta × {n_ph} phi) × 2 times = {n_th**2 * n_ph**2} points")

for i1, th1 in enumerate(theta_vals2):
    for j1, ph1 in enumerate(phi_vals2):
        P1_a = make_projector(th1, ph1)
        P1_b = np.eye(2) - P1_a
        P1_list = [P1_a, P1_b]

        for i2, th2 in enumerate(theta_vals2):
            for j2, ph2 in enumerate(phi_vals2):
                P2_a = make_projector(th2, ph2)
                P2_b = np.eye(2) - P2_a
                P2_list_var = [P2_a, P2_b]

                D, _ = decoherence_functional(P1_list, P2_list_var, rho_0, U1, U12)

                max_offdiag = 0
                for ii in range(4):
                    for jj in range(4):
                        if ii != jj:
                            max_offdiag = max(max_offdiag, abs(D[ii, jj]))

                n_checked += 1

                if max_offdiag < 1e-6:
                    consistent_3time.append({
                        'theta1': th1, 'phi1': ph1,
                        'theta2': th2, 'phi2': ph2,
                        'max_offdiag': max_offdiag
                    })

    if (i1 + 1) % 10 == 0:
        print(f"  Progress: {i1+1}/{n_th} (found {len(consistent_3time)} so far)")

print(f"\nTotal checked: {n_checked}")
print(f"Consistent 3-time families found: {len(consistent_3time)}")

if consistent_3time:
    # Analyze the structure
    th1_vals = [b['theta1'] for b in consistent_3time]
    ph1_vals = [b['phi1'] for b in consistent_3time]
    th2_vals = [b['theta2'] for b in consistent_3time]
    ph2_vals = [b['phi2'] for b in consistent_3time]

    print(f"\ntheta_1 range: [{min(th1_vals):.4f}, {max(th1_vals):.4f}]")
    print(f"phi_1 range: [{min(ph1_vals):.4f}, {max(ph1_vals):.4f}]")
    print(f"theta_2 range: [{min(th2_vals):.4f}, {max(th2_vals):.4f}]")
    print(f"phi_2 range: [{min(ph2_vals):.4f}, {max(ph2_vals):.4f}]")

    # Check if there's a relationship between t1 and t2 bases
    print(f"\nSample consistent families:")
    for b in consistent_3time[:20]:
        print(f"  (θ₁={b['theta1']/np.pi:.3f}π, φ₁={b['phi1']/np.pi:.3f}π) × "
              f"(θ₂={b['theta2']/np.pi:.3f}π, φ₂={b['phi2']/np.pi:.3f}π) "
              f" |D_off|={b['max_offdiag']:.2e}")

    # Count distinct theta_1 values
    th1_unique = sorted(set([round(t/np.pi, 3) for t in th1_vals]))
    th2_unique = sorted(set([round(t/np.pi, 3) for t in th2_vals]))
    print(f"\n  Distinct θ₁/π values ({len(th1_unique)}): {th1_unique[:15]}...")
    print(f"  Distinct θ₂/π values ({len(th2_unique)}): {th2_unique[:15]}...")

# ============================================================
# Part E: Control check — H = 0 (trivial evolution)
# ============================================================
print(f"\n{'='*70}")
print("PART E: Control check — H = 0 (trivial evolution)")
print("=" * 70)

U_triv = np.eye(2, dtype=complex)
U12_triv = np.eye(2, dtype=complex)

n_th_ctrl = 50
n_ph_ctrl = 50
theta_ctrl = np.linspace(0.05, np.pi - 0.05, n_th_ctrl)
phi_ctrl = np.linspace(0, 2*np.pi - 0.05, n_ph_ctrl)

consistent_trivial = 0
total_trivial = 0

# Fix t_2 = computational basis, vary t_1
for th in theta_ctrl:
    for ph in phi_ctrl:
        P1_a = make_projector(th, ph)
        P1_b = np.eye(2) - P1_a
        P1_list = [P1_a, P1_b]

        D, _ = decoherence_functional(P1_list, P2_list, rho_0, U_triv, U12_triv)
        max_offdiag = max(abs(D[ii, jj]) for ii in range(4) for jj in range(4) if ii != jj)
        total_trivial += 1

        if max_offdiag < 1e-6:
            consistent_trivial += 1

print(f"  H=0: {consistent_trivial}/{total_trivial} bases consistent")
print(f"  (With fixed t2 = comp basis, not all t1 bases are consistent)")
print(f"  This is expected — 3-time consistency constrains even for H=0")

# For H=0 with BOTH bases free
consistent_trivial_both = 0
n_th_small = 20
n_ph_small = 20
theta_small = np.linspace(0.05, np.pi-0.05, n_th_small)
phi_small = np.linspace(0, 2*np.pi-0.05, n_ph_small)
total_both = 0

for i1, th1 in enumerate(theta_small):
    for j1, ph1 in enumerate(phi_small):
        P1_a = make_projector(th1, ph1)
        P1_b = np.eye(2) - P1_a
        for i2, th2 in enumerate(theta_small):
            for j2, ph2 in enumerate(phi_small):
                P2_a = make_projector(th2, ph2)
                P2_b = np.eye(2) - P2_a
                D, _ = decoherence_functional([P1_a, P1_b], [P2_a, P2_b],
                                               rho_0, U_triv, U12_triv)
                max_offdiag = max(abs(D[ii, jj]) for ii in range(4)
                                 for jj in range(4) if ii != jj)
                total_both += 1
                if max_offdiag < 1e-6:
                    consistent_trivial_both += 1

print(f"  H=0 (both bases free): {consistent_trivial_both}/{total_both} consistent")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*70}")
print("STAGE 2 SUMMARY")
print("=" * 70)
print(f"  System: qubit, H = (ω/2)σ_z, ρ₀ = |+><+|")
print(f"  Times: t₀=0, t₁=π/4, t₂=π/2")
print(f"")
print(f"  Single-time histories (projectors at t₁ only):")
print(f"    ALL bases are consistent (trivially)")
print(f"    Dimension: 2 (full Bloch sphere S²)")
print(f"")
print(f"  3-time histories (projectors at t₁ and t₂):")
print(f"    With t₂ = comp basis: {len(consistent_bases)} of {n_theta*n_phi} bases consistent")
print(f"    With both bases free: {len(consistent_3time)} of {n_checked} combinations consistent")
print(f"")
print(f"  Control (H=0): {consistent_trivial}/{total_trivial} (t₂ fixed), {consistent_trivial_both}/{total_both} (both free)")
print("=" * 70)
