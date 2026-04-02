"""
Fix the Jacobian dimension calculation.

The previous code evaluated the Jacobian at RANDOM points, not at
solutions of the constraint. At a solution, the Jacobian can have
reduced rank due to dependent constraints.

For N=2, we proved analytically that the Jacobian has rank 1 (not 2)
at a solution, giving phase freedom dimension = 4 - 1 - 1 = 2.
"""

import numpy as np

print("=" * 70)
print("CORRECTED DIMENSION CALCULATION")
print("=" * 70)

# Analytic proof for N=2:
print("""
ANALYTIC PROOF (N=2):

Constraint: f(a,b,c,d) = (cos(b-a)+cos(d-c), sin(b-a)+sin(d-c)) = (0,0)
Solution set: b-a = d-c + π (mod 2π)

Jacobian at a solution (X = b-a, Y = d-c = X-π):
  J = [[sin(X), -sin(X), -sin(X), sin(X)],
       [-cos(X), cos(X), cos(X), -cos(X)]]
     = [sin(X); -cos(X)] ⊗ [1, -1, -1, 1]

Both rows are proportional → rank(J) = 1 (not 2!)

Correct dimension: 4 phases - 1 constraint - 1 global = 2 ✓
""")

def find_solution_point(N):
    """Find a valid Theta (a solution point) for uniform Gamma = 1/N."""
    # Use the DFT matrix: U_jk = (1/√N) exp(2πi jk/N)
    phases = np.zeros(N*N)
    for j in range(N):
        for k in range(N):
            phases[j*N + k] = 2 * np.pi * j * k / N
    return phases

def compute_jacobian_at_solution(N):
    """Compute Jacobian rank at a valid solution point."""
    Gamma = np.ones((N, N)) / N
    phases0 = find_solution_point(N)

    # Verify it's a solution
    Theta = np.zeros((N, N), dtype=complex)
    for i in range(N):
        for j in range(N):
            Theta[i, j] = np.sqrt(Gamma[i, j]) * np.exp(1j * phases0[i*N + j])
    TdT = Theta.conj().T @ Theta
    err = np.max(np.abs(TdT - np.eye(N)))
    assert err < 1e-10, f"Not a valid solution! Error = {err}"

    # Compute unitarity residual
    def unitarity_residual(phases):
        Th = np.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                Th[i, j] = np.sqrt(Gamma[i, j]) * np.exp(1j * phases[i*N + j])
        R = Th.conj().T @ Th
        res = []
        for i in range(N):
            for j in range(i+1, N):
                res.append(R[i, j].real)
                res.append(R[i, j].imag)
        return np.array(res)

    # Numerical Jacobian at the solution
    r0 = unitarity_residual(phases0)
    n_constraints = len(r0)
    J = np.zeros((n_constraints, N*N))
    eps = 1e-8
    for k in range(N*N):
        phases_k = phases0.copy()
        phases_k[k] += eps
        J[:, k] = (unitarity_residual(phases_k) - r0) / eps

    rank = np.linalg.matrix_rank(J, tol=1e-5)
    return N*N, n_constraints, rank, J

print("EMPIRICAL JACOBIAN RANK AT SOLUTION POINTS (DFT matrix):")
print(f"{'N':>3} | {'Phases':>7} | {'Constraints':>12} | {'Jac Rank':>9} | {'Manifold':>9} | {'Mod Global':>11}")
print("-" * 70)

for N in [2, 3, 4, 5, 6]:
    n_phases, n_constr, rank, J = compute_jacobian_at_solution(N)
    manifold_dim = n_phases - rank
    moduli_dim = manifold_dim - 1
    print(f"{N:>3} | {n_phases:>7} | {n_constr:>12} | {rank:>9} | {manifold_dim:>9} | {moduli_dim:>11}")

# Also verify by finding solutions numerically near the DFT
print(f"\n{'='*70}")
print("VERIFICATION: Random perturbation of DFT solution")
print("=" * 70)

from scipy.optimize import minimize

for N in [2, 3, 4, 5]:
    Gamma = np.ones((N, N)) / N

    def objective(phases):
        Th = np.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                Th[i, j] = np.sqrt(Gamma[i, j]) * np.exp(1j * phases[i*N + j])
        R = Th.conj().T @ Th
        return np.sum(np.abs(R - np.eye(N))**2)

    # Start from DFT solution and explore local neighborhood
    phases_dft = find_solution_point(N)

    # Count connected solution dimensions by exploring
    # Start at DFT, perturb in random directions, project back to manifold
    n_independent = 0
    explored_directions = []

    np.random.seed(42)
    for trial in range(N*N + 5):
        direction = np.random.randn(N*N)
        direction /= np.linalg.norm(direction)

        # Project out previously explored directions
        for d in explored_directions:
            direction -= np.dot(direction, d) * d
        if np.linalg.norm(direction) < 1e-10:
            continue
        direction /= np.linalg.norm(direction)

        # Try to move in this direction while staying on manifold
        delta = 0.01
        phases_test = phases_dft + delta * direction
        res = minimize(objective, phases_test, method='BFGS',
                       options={'gtol': 1e-14, 'maxiter': 1000})

        if res.fun < 1e-20:
            # Check if we actually moved
            displacement = res.x - phases_dft
            # Project out global phase (direction = [1,1,...,1])
            global_dir = np.ones(N*N) / np.sqrt(N*N)
            displacement -= np.dot(displacement, global_dir) * global_dir
            if np.linalg.norm(displacement) > 1e-6:
                n_independent += 1
                explored_directions.append(displacement / np.linalg.norm(displacement))

    print(f"  N={N}: Found {n_independent} independent directions on solution manifold")
    print(f"        Expected phase freedom dimension: {n_independent}")

# ============================================================
# Also check rank at multiple different solution points
# ============================================================
print(f"\n{'='*70}")
print("JACOBIAN RANK AT NON-DFT SOLUTION POINTS")
print("=" * 70)

for N in [2, 3, 4, 5]:
    Gamma = np.ones((N, N)) / N
    ranks = []

    for seed in range(20):
        np.random.seed(seed + 100)
        # Generate random unitary with |U_ij|² = 1/N
        # Start from DFT and multiply by diagonal phases (which preserve |U_ij|²)
        phases_dft = find_solution_point(N)

        # Random gauge transformation: multiply rows by phases and columns by phases
        row_phases = np.random.uniform(0, 2*np.pi, N)
        col_phases = np.random.uniform(0, 2*np.pi, N)
        new_phases = np.zeros(N*N)
        for i in range(N):
            for j in range(N):
                new_phases[i*N + j] = phases_dft[i*N + j] + row_phases[i] + col_phases[j]

        # Verify it's still a solution
        Theta = np.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                Theta[i, j] = (1/np.sqrt(N)) * np.exp(1j * new_phases[i*N + j])
        err = np.max(np.abs(Theta.conj().T @ Theta - np.eye(N)))
        if err > 1e-8:
            continue

        _, _, rank, _ = compute_jacobian_at_solution.__wrapped__(N) if hasattr(compute_jacobian_at_solution, '__wrapped__') else (0, 0, 0, None)
        # Recompute at this point
        def unitarity_residual_v2(phases):
            Th = np.zeros((N, N), dtype=complex)
            for i in range(N):
                for j in range(N):
                    Th[i, j] = (1/np.sqrt(N)) * np.exp(1j * phases[i*N + j])
            R = Th.conj().T @ Th
            res = []
            for i in range(N):
                for j in range(i+1, N):
                    res.append(R[i, j].real)
                    res.append(R[i, j].imag)
            return np.array(res)

        r0 = unitarity_residual_v2(new_phases)
        n_c = len(r0)
        J = np.zeros((n_c, N*N))
        eps = 1e-8
        for k in range(N*N):
            p_k = new_phases.copy()
            p_k[k] += eps
            J[:, k] = (unitarity_residual_v2(p_k) - r0) / eps

        rank = np.linalg.matrix_rank(J, tol=1e-5)
        ranks.append(rank)

    if ranks:
        print(f"  N={N}: Jacobian ranks at {len(ranks)} solution points: {sorted(set(ranks))}")
        manifold = N*N - max(ranks)
        print(f"        → Manifold dimension: {manifold}, moduli: {manifold - 1}")

# ============================================================
# CORRECTED COMPARISON TABLE
# ============================================================
print(f"\n{'='*70}")
print("CORRECTED COMPARISON TABLE")
print("=" * 70)

# From Jacobian at solution: phase freedom dim = N*N - rank - 1
# But we need to subtract the gauge degrees of freedom too.
# Actually, the Jacobian already accounts for all constraints.
# The moduli = manifold_dim - 1 (global phase) is the correct answer.

# But there's ANOTHER subtlety: left and right diagonal multiplication
# preserves Gamma. So there are 2N-1 gauge degrees of freedom, not just 1.
# D_L * Theta * D_R has same Gamma for any diagonal unitaries D_L, D_R.
# But (D_L * Theta * D_R)†(D_L * Theta * D_R) = D_R† Theta† D_L† D_L Theta D_R
# = D_R† Theta† Theta D_R = D_R† I D_R = I
# Wait, that's only if Theta is unitary. And it gives a DIFFERENT unitary
# but with the SAME Gamma.
# So row/column rephasing is part of the phase freedom.
# The manifold dimension INCLUDES these gauge transformations.

# For uniform Gamma, the gauge group is: multiply row i by e^(i*α_i),
# multiply column j by e^(i*β_j). This changes phase_ij → phase_ij + α_i + β_j.
# This is 2N parameters with 1 overall redundancy = 2N-1 gauge parameters.

# These gauge transformations change Theta but preserve Gamma AND preserve unitarity.
# They are part of the solution manifold.

# If we want "physically distinct" Theta's (i.e., those giving different quantum channels),
# we need to mod out by LEFT diagonal multiplication only (which preserves the channel
# E(ρ) = Theta ρ Theta†? No: D_L Theta ρ Theta† D_L† ≠ Theta ρ Theta† in general).

# Actually, Theta and D_L Theta give different channels in general.
# But Theta and Theta D_R also give different channels.
# The only equivalence is global phase: e^(iδ) Theta gives the same channel.

# So the phase freedom space (before modding out global phase) is the full manifold.
# After modding out global phase: manifold_dim - 1.

print("""
KEY INSIGHT: Row/column rephasing is NOT a gauge symmetry for the channel.
  D_L Theta ρ Theta† D_L† ≠ Theta ρ Theta† (in general)
  So left diagonal multiplication gives DIFFERENT quantum channels.

  The only true gauge freedom is global phase: e^(iδ)Theta → same channel.
  Phase freedom = manifold dimension - 1.

  For uniform Gamma and DFT solution point:
""")

for N in [2, 3, 4, 5, 6]:
    n_phases, n_constr, rank, J = compute_jacobian_at_solution(N)
    pf_dim = n_phases - rank - 1  # manifold minus global phase
    rs_dim = N**2 - N  # realm selection: flag manifold for t₂
    # But also need to add t₁ freedom (choice of basis within ψ₁⊥)
    # For pure state, t₁ must include ψ₁. The other N-1 vectors form a basis of ψ₁⊥.
    # Choice of ONB in (N-1)-dim subspace: U(N-1)/U(1)^(N-1), dim = (N-1)²-(N-1) = (N-1)(N-2)
    # But these don't affect probabilities (zero-probability histories), so they're trivial gauge.
    # Physically meaningful CH dimension = t₂ choice only = N²-N.

    print(f"  N={N}: Phase Freedom = {pf_dim}, Realm Selection (t₂ free) = {rs_dim}")

print(f"\nFormula check:")
for N in [2, 3, 4, 5, 6]:
    n_phases, n_constr, rank, J = compute_jacobian_at_solution(N)
    pf = n_phases - rank - 1
    print(f"  N={N}: N²={N*N}, Jac rank={rank}, PF={pf} = N²-rank-1 = {N*N}-{rank}-1 = {N*N-rank-1}")

# What is the rank formula?
print(f"\n  rank(J) values: ", end="")
for N in [2, 3, 4, 5, 6]:
    _, _, rank, _ = compute_jacobian_at_solution(N)
    print(f"N={N}→{rank}, ", end="")
print()
print("  Does rank = N(N-1) - (2N-2) = N²-3N+2 = (N-1)(N-2)?")
for N in [2, 3, 4, 5, 6]:
    _, _, rank, _ = compute_jacobian_at_solution(N)
    formula = (N-1)*(N-2)
    print(f"    N={N}: rank={rank}, (N-1)(N-2)={formula}, match={rank==formula}")

print("\n  Or rank = N(N-1) - something?")
for N in [2, 3, 4, 5, 6]:
    _, _, rank, _ = compute_jacobian_at_solution(N)
    n_c_raw = N*(N-1)
    deficit = n_c_raw - rank
    print(f"    N={N}: #constraints={n_c_raw}, rank={rank}, deficit={deficit}, 2N-2={2*N-2}")

print(f"\n  rank = N(N-1) - (2N-2) = N²-3N+2 → PF = N²-(N²-3N+2)-1 = 3N-3 = 3(N-1)")
print(f"  Let's check:")
for N in [2, 3, 4, 5, 6]:
    _, _, rank, _ = compute_jacobian_at_solution(N)
    pf = N*N - rank - 1
    formula_3n = 3*(N-1)
    print(f"    N={N}: PF={pf}, 3(N-1)={formula_3n}, match={pf==formula_3n}")

print(f"\n  Hmm, let me check: PF = N² - rank - 1")
for N in [2, 3, 4, 5, 6]:
    _, _, rank, _ = compute_jacobian_at_solution(N)
    pf = N*N - rank - 1
    print(f"    N={N}: PF = {N*N} - {rank} - 1 = {pf}")
    print(f"           = N² - (N²-3N+2) - 1 = 3N - 3 = {3*N-3}? PF={pf}, 3N-3={3*N-3}")

# Final corrected table
print(f"\n{'='*70}")
print("FINAL CORRECTED COMPARISON")
print("=" * 70)
print(f"{'N':>3} | {'Phase Freedom':>14} | {'Realm Selection':>16} | {'Equal?':>7}")
print("-" * 50)
for N in [2, 3, 4, 5, 6]:
    _, _, rank, _ = compute_jacobian_at_solution(N)
    pf = N*N - rank - 1
    rs = N*N - N
    eq = "YES" if pf == rs else "NO"
    print(f"{N:>3} | {pf:>14} | {rs:>16} | {eq:>7}")
    print(f"    |   (3(N-1)={3*(N-1):>3})  |  (N(N-1)={N*(N-1):>3})    |")
