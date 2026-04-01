"""
spectral_gap_group_laplacian.py
================================
Compute the spectral gap Δ_G of the group Laplacian for the binary polyhedral
subgroups 2T (24), 2O (48), 2I (120) of SU(2), and derive Adhikari-Cao mass
gap bounds.

Two Laplacian definitions are used:
1. Nearest-neighbor Cayley graph Laplacian (physically motivated by S³ geometry)
2. Heat-kernel random walk at β₀=1 (analytical comparison)

The Adhikari-Cao (2025) bound: β_min = (114 + 4*ln|G|) / Δ_G
guarantees exponential correlation decay for β ≥ β_min.
"""

import numpy as np
import sys
from itertools import product as iproduct

# ─────────────────────────────────────────────────────────
# Group Construction (from exploration-005)
# ─────────────────────────────────────────────────────────

def quat_multiply(q1, q2):
    a0,a1,a2,a3 = q1
    b0,b1,b2,b3 = q2
    return np.array([
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0
    ])

def quat_conjugate(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def normalize_quat(q):
    return q / np.linalg.norm(q)


def binary_tetrahedral_group():
    """Build 2T (24 elements)."""
    elements = []
    for sign in [1, -1]:
        for k in range(4):
            e = np.zeros(4); e[k] = sign
            elements.append(e)
    for s0 in [1,-1]:
        for s1 in [1,-1]:
            for s2 in [1,-1]:
                for s3 in [1,-1]:
                    elements.append(np.array([s0,s1,s2,s3])*0.5)
    result = np.array(elements)
    assert len(result) == 24
    return result


def binary_octahedral_group():
    """Build 2O (48 elements) = 2T + 24 face-centre elements."""
    elements = list(binary_tetrahedral_group())
    s2 = 1.0/np.sqrt(2.0)
    for i in range(4):
        for j in range(i+1, 4):
            for si in [1,-1]:
                for sj in [1,-1]:
                    e = np.zeros(4)
                    e[i] = si*s2; e[j] = sj*s2
                    elements.append(e)
    result = np.array(elements)
    assert len(result) == 48, f"Expected 48, got {len(result)}"
    return result


def binary_icosahedral_group():
    """Build 2I (120 elements) using quaternion icosians."""
    phi = (1.0+np.sqrt(5.0))/2.0
    phi_inv = 1.0/phi
    elements = set()

    def add(q):
        q = q / np.linalg.norm(q)
        key = tuple(np.round(q, 10))
        elements.add(key)

    # ±1, ±i, ±j, ±k
    for idx in range(4):
        for sign in [1,-1]:
            e = np.zeros(4); e[idx] = sign; add(e)

    # (1/2)(±1,±1,±1,±1)
    for s in iproduct([1,-1], repeat=4):
        add(np.array(s)*0.5)

    # (1/2)(0, ±1, ±1/φ, ±φ) and even permutations
    even_perms = [
        (0,1,2,3),(0,2,3,1),(0,3,1,2),
        (1,0,3,2),(1,2,0,3),(1,3,2,0),
        (2,0,1,3),(2,1,3,0),(2,3,0,1),
        (3,0,2,1),(3,1,0,2),(3,2,1,0)
    ]
    for perm in even_perms:
        for s1,s2,s3 in iproduct([1,-1], repeat=3):
            vals = [0.0, s1*1.0, s2*phi_inv, s3*phi]
            e = np.zeros(4)
            for i,p in enumerate(perm):
                e[i] = vals[p]
            e *= 0.5
            add(e)

    result = np.array([np.array(e) for e in elements])
    if len(result) != 120:
        print(f"WARNING: got {len(result)} elements for 2I")
    return result


def find_nearest_generators(elements, tol=1e-8):
    """
    Find the generating set S = elements at the minimum non-trivial angle
    from the identity (i.e., maximum Re(g0) among non-identity elements).

    Returns:
        generators: array of elements that constitute S
        angle: the angle of those elements from identity
        degree: |S|
    """
    identity = np.array([1.0, 0.0, 0.0, 0.0])
    id_idx = np.argmin(np.linalg.norm(elements - identity, axis=1))

    # Cosines of angles from identity: cos(θ) = Re(g0) = g[0]
    cos_angles = elements[:, 0]

    # Exclude identity (cos ≈ 1) and near-identity
    mask = np.abs(cos_angles - 1.0) > tol
    non_id_cos = cos_angles[mask]
    non_id_elems = elements[mask]

    # Maximum cos = minimum angle (nearest to identity)
    max_cos = np.max(non_id_cos)
    nearest_mask = np.abs(non_id_cos - max_cos) < tol

    generators = non_id_elems[nearest_mask]
    angle = np.arccos(np.clip(max_cos, -1, 1))

    return generators, angle, len(generators)


def find_nearest_generators_with_inverses(elements, tol=1e-8):
    """
    Find S = elements at minimum non-trivial angle, closed under inversion.
    (For these groups, g and g^{-1} have same angle, so this is automatic.)
    """
    generators, angle, degree = find_nearest_generators(elements, tol)
    print(f"  Generating set: {degree} elements at angle {np.degrees(angle):.2f}°")

    # Verify closure under inversion
    for g in generators:
        g_inv = quat_conjugate(g)
        g_inv = g_inv / np.linalg.norm(g_inv)
        dists = np.linalg.norm(generators - g_inv, axis=1)
        if np.min(dists) > tol:
            print(f"  WARNING: Generating set not closed under inversion!")
            break

    return generators, angle


def build_cayley_laplacian(elements, generators, tol=1e-8):
    """
    Build the Cayley graph Laplacian matrix.
    L_{ij} = degree * δ_{ij} - A_{ij}
    A_{ij} = 1 if g_j = g_i * s for some s in generators (i.e., g_i^{-1} g_j ∈ S)
    """
    n = len(elements)
    degree = len(generators)
    L = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                L[i, j] = degree
            else:
                # Check if g_i^{-1} * g_j is in S
                g_i_inv = quat_conjugate(elements[i])
                g_i_inv = g_i_inv / np.linalg.norm(g_i_inv)
                rel = normalize_quat(quat_multiply(g_i_inv, elements[j]))
                dists = np.linalg.norm(generators - rel, axis=1)
                if np.min(dists) < tol:
                    L[i, j] = -1.0

    # Verify row sums are zero
    row_sums = np.sum(L, axis=1)
    if np.max(np.abs(row_sums)) > tol:
        print(f"  WARNING: Row sums not zero! Max: {np.max(np.abs(row_sums)):.2e}")

    return L


def build_heat_kernel_transition(elements, beta0=1.0):
    """
    Build the heat-kernel transition matrix T_{gh} = exp(beta0 * 2*<g,h>) / Z_g
    where <g,h> = quaternion inner product = g[0]*h[0] + g[1]*h[1] + ...
    This is a stochastic matrix (rows sum to 1).
    """
    n = len(elements)
    # Inner product matrix: M[i,j] = <g_i, g_j> = g_i · g_j
    M = elements @ elements.T  # shape (n, n), entries in [-1, 1]

    # Transition matrix: T[i,j] = exp(beta0 * 2 * M[i,j]) / Z_i
    T = np.exp(beta0 * 2.0 * M)
    Z = T.sum(axis=1, keepdims=True)
    T = T / Z

    # Verify rows sum to 1
    assert np.allclose(T.sum(axis=1), 1.0, atol=1e-10), "Rows don't sum to 1"

    return T


def compute_spectral_gap_cayley(elements, group_name):
    """Compute spectral gap of Cayley graph Laplacian."""
    print(f"\n--- {group_name} (|G|={len(elements)}) ---")

    generators, angle = find_nearest_generators_with_inverses(elements)
    degree = len(generators)
    print(f"  Cayley graph: {len(elements)} vertices, degree {degree}")

    L = build_cayley_laplacian(elements, generators)
    print(f"  Laplacian matrix built ({len(elements)}x{len(elements)})")

    # Compute eigenvalues
    eigenvalues = np.linalg.eigvalsh(L)
    eigenvalues = np.sort(eigenvalues)

    # The smallest eigenvalue should be ~0 (constant function)
    lambda_0 = eigenvalues[0]
    lambda_1 = eigenvalues[1]  # First non-trivial eigenvalue = spectral gap

    print(f"  Eigenvalues (first 6): {eigenvalues[:6]}")
    print(f"  Spectral gap Δ_G (Cayley) = {lambda_1:.6f}")
    print(f"  Degree = {degree}, Δ_G/degree = {lambda_1/degree:.6f}")

    # Verify λ_0 ≈ 0
    if abs(lambda_0) > 0.01:
        print(f"  WARNING: λ_0 = {lambda_0:.4f} (should be ~0)")

    return lambda_1, degree, angle


def compute_spectral_gap_heat_kernel(elements, group_name, beta0=1.0):
    """Compute spectral gap of heat kernel random walk at β₀."""
    T = build_heat_kernel_transition(elements, beta0)
    eigenvalues = np.sort(np.linalg.eigvalsh(T))[::-1]  # Descending order

    lambda_1 = eigenvalues[0]  # Should be ≈ 1
    lambda_2 = eigenvalues[1]  # Second largest

    gap = lambda_1 - lambda_2

    print(f"  Heat kernel (β₀={beta0}): λ₁={lambda_1:.6f}, λ₂={lambda_2:.6f}")
    print(f"  Spectral gap Δ_G^(heat) = {gap:.6f}")

    return gap


def adhikari_cao_bound(G_size, delta_G, log_base='natural'):
    """Compute Adhikari-Cao β_min = (114 + 4*log|G|) / Δ_G."""
    if log_base == 'natural':
        log_G = np.log(G_size)
    elif log_base == 'log2':
        log_G = np.log2(G_size)
    else:
        log_G = np.log10(G_size)

    beta_min = (114.0 + 4.0 * log_G) / delta_G
    return beta_min


# ─────────────────────────────────────────────────────────
# Main analysis
# ─────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Spectral Gap of Group Laplacian and Adhikari-Cao Bounds")
    print("=" * 70)

    # Build the three groups
    print("\nConstructing groups...")
    groups = {
        '2T': binary_tetrahedral_group(),
        '2O': binary_octahedral_group(),
        '2I': binary_icosahedral_group(),
    }

    for name, elems in groups.items():
        print(f"  {name}: {len(elems)} elements")

    # ── Cayley graph spectral gaps ──
    print("\n" + "="*70)
    print("TASK B: CAYLEY GRAPH LAPLACIAN SPECTRAL GAPS")
    print("="*70)

    results = {}
    for name, elems in groups.items():
        delta_cayley, degree, angle = compute_spectral_gap_cayley(elems, name)
        results[name] = {
            'n': len(elems),
            'delta_cayley': delta_cayley,
            'degree_cayley': degree,
            'angle_degrees': np.degrees(angle),
        }

    # ── Heat kernel spectral gaps ──
    print("\n" + "="*70)
    print("HEAT KERNEL RANDOM WALK SPECTRAL GAPS (β₀=1.0)")
    print("="*70)

    for name, elems in groups.items():
        delta_heat = compute_spectral_gap_heat_kernel(elems, name, beta0=1.0)
        results[name]['delta_heat_b1'] = delta_heat

    # Also for β₀ = 0.1 (closer to uniform)
    print("\nHeat kernel at β₀=0.1 (closer to uniform random walk):")
    for name, elems in groups.items():
        delta_heat_small = compute_spectral_gap_heat_kernel(elems, name, beta0=0.1)
        results[name]['delta_heat_b01'] = delta_heat_small

    # ── Adhikari-Cao bounds ──
    print("\n" + "="*70)
    print("ADHIKARI-CAO BOUNDS β_min = (114 + 4*ln|G|) / Δ_G")
    print("="*70)
    print(f"\n{'Group':<8} {'|G|':<6} {'ln|G|':<8} {'Δ_G(Cayley)':<14} {'β_min(Cayley)':<16} {'Δ_G(heat,β₀=1)':<18} {'β_min(heat)':<14}")
    print("-" * 90)

    for name in ['2T', '2O', '2I']:
        r = results[name]
        n = r['n']
        delta_c = r['delta_cayley']
        delta_h = r['delta_heat_b1']
        beta_min_c = adhikari_cao_bound(n, delta_c)
        beta_min_h = adhikari_cao_bound(n, delta_h)
        ln_n = np.log(n)
        print(f"{name:<8} {n:<6} {ln_n:<8.3f} {delta_c:<14.6f} {beta_min_c:<16.4f} {delta_h:<18.6f} {beta_min_h:<14.4f}")

    print()

    # ── Scaling analysis ──
    print("\n" + "="*70)
    print("SCALING ANALYSIS: How does β_min scale with |G|?")
    print("="*70)

    group_sizes = [results[n]['n'] for n in ['2T', '2O', '2I']]
    delta_cayley_vals = [results[n]['delta_cayley'] for n in ['2T', '2O', '2I']]
    delta_heat_vals = [results[n]['delta_heat_b1'] for n in ['2T', '2O', '2I']]

    # Fit power law: Δ_G ~ |G|^α
    log_sizes = np.log(group_sizes)
    log_delta_c = np.log(delta_cayley_vals)
    log_delta_h = np.log(delta_heat_vals)

    # Linear fit: log(Δ) = α * log(|G|) + const
    if len(group_sizes) >= 2:
        fit_c = np.polyfit(log_sizes, log_delta_c, 1)
        fit_h = np.polyfit(log_sizes, log_delta_h, 1)
        print(f"\nPower law fit Δ_G ~ |G|^α:")
        print(f"  Cayley graph: α = {fit_c[0]:.4f} (expected ~-2/3 for S³ lattice)")
        print(f"  Heat kernel:  α = {fit_h[0]:.4f}")

    # β_min scaling
    beta_min_cayley = [adhikari_cao_bound(r['n'], r['delta_cayley']) for r in results.values()]
    beta_min_heat   = [adhikari_cao_bound(r['n'], r['delta_heat_b1']) for r in results.values()]

    log_beta_c = np.log(beta_min_cayley)
    log_beta_h = np.log(beta_min_heat)
    if len(group_sizes) >= 2:
        fit_bc = np.polyfit(log_sizes, log_beta_c, 1)
        fit_bh = np.polyfit(log_sizes, log_beta_h, 1)
        print(f"\nPower law fit β_min ~ |G|^γ:")
        print(f"  Cayley graph: γ = {fit_bc[0]:.4f}")
        print(f"  Heat kernel:  γ = {fit_bh[0]:.4f}")

    # ── Compare to known β_c from exploration-005 ──
    print("\n" + "="*70)
    print("COMPARISON WITH MEASURED β_c (from exploration-005)")
    print("="*70)
    print(f"\nPhase transition β_c values from exploration-005:")
    beta_c = {'2T': 2.2, '2O': 3.2, '2I': 5.8}
    for name in ['2T', '2O', '2I']:
        r = results[name]
        beta_min_c = adhikari_cao_bound(r['n'], r['delta_cayley'])
        beta_min_h = adhikari_cao_bound(r['n'], r['delta_heat_b1'])
        bc = beta_c[name]
        print(f"  {name}: β_c(measured)={bc:.1f}, β_min(Cayley)={beta_min_c:.2f}, β_min(heat)={beta_min_h:.2f}")

    # ── Extrapolation to SU(2) ──
    print("\n" + "="*70)
    print("EXTRAPOLATION: β_min AS |G| → ∞ (approaching SU(2))")
    print("="*70)

    # For large |G|, Δ_G ~ |G|^α (fitted above)
    # β_min ~ |G|^γ where γ = 1-α = 1 - fitted exponent
    if len(group_sizes) >= 2:
        alpha_c = fit_c[0]
        # β_min = (114 + 4*ln|G|) / (C * |G|^α)
        # ~ |G|^{-α} * ln|G| (for large |G|)
        print(f"\nWith Δ_G ~ |G|^{alpha_c:.3f} and β_min = (114 + 4*ln|G|)/Δ_G:")
        print(f"  β_min ~ |G|^{-alpha_c:.3f} * (114 + 4*ln|G|)")
        if alpha_c < 0:
            print(f"  Since α = {alpha_c:.3f} < 0, Δ_G decreases with |G|")
            print(f"  → β_min DIVERGES as |G| → ∞ (bound becomes vacuous for SU(2))")
        else:
            print(f"  Since α = {alpha_c:.3f} > 0, Δ_G increases with |G|")
            print(f"  → β_min might converge as |G| → ∞")

    # ── Summary table ──
    print("\n" + "="*70)
    print("FINAL RESULTS TABLE")
    print("="*70)
    print(f"\n{'Group':<6} {'|G|':<6} {'angle°':<10} {'|S|':<6} {'Δ_G(Cay)':<12} {'Δ_G(heat)':<12} {'β_min(Cay)':<12} {'β_min(heat)':<12}")
    print("-" * 80)
    for name in ['2T', '2O', '2I']:
        r = results[name]
        beta_min_c = adhikari_cao_bound(r['n'], r['delta_cayley'])
        beta_min_h = adhikari_cao_bound(r['n'], r['delta_heat_b1'])
        print(f"{name:<6} {r['n']:<6} {r['angle_degrees']:<10.3f} {r['degree_cayley']:<6} "
              f"{r['delta_cayley']:<12.6f} {r['delta_heat_b1']:<12.6f} "
              f"{beta_min_c:<12.4f} {beta_min_h:<12.4f}")

    print()
    return results


if __name__ == "__main__":
    results = main()
