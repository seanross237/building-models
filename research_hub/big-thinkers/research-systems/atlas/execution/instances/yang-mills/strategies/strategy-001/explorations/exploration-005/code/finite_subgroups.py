"""
Finite Subgroups of SU(2) — Quaternion Representations
=======================================================

Constructs the binary tetrahedral (2T, 24 elements), binary octahedral (2O, 48 elements),
and binary icosahedral (2I, 120 elements) groups as sets of unit quaternions.

Each element is stored as (a0, a1, a2, a3) where the corresponding SU(2) matrix is:
  U = a0*I + i*(a1*σ1 + a2*σ2 + a3*σ3)
"""

import numpy as np
from itertools import product


def normalize_quat(q):
    """Normalize quaternion to unit length."""
    return q / np.linalg.norm(q)


def quat_multiply(q1, q2):
    """Multiply two quaternions."""
    a0, a1, a2, a3 = q1
    b0, b1, b2, b3 = q2
    return np.array([
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0
    ])


def quat_conjugate(q):
    """Quaternion conjugate (= inverse for unit quaternions)."""
    return np.array([q[0], -q[1], -q[2], -q[3]])


def generate_group_closure(generators, max_size=200, tol=1e-10):
    """
    Generate a finite group from generators by closure.

    Parameters:
        generators: list of quaternions (numpy arrays of shape (4,))
        max_size: maximum expected group size (safety limit)
        tol: tolerance for identifying equal elements

    Returns:
        numpy array of shape (N, 4) containing all group elements
    """
    elements = [normalize_quat(g) for g in generators]
    # Also add inverses of generators
    for g in generators:
        elements.append(normalize_quat(quat_conjugate(g)))

    # Add identity
    identity = np.array([1.0, 0.0, 0.0, 0.0])
    elements.append(identity)

    def is_new(q, existing, tol):
        """Check if quaternion q is new (not already in the list)."""
        for e in existing:
            # Check both q and -q (same SU(2) element maps to two quaternions,
            # but for the double cover we keep both)
            if np.linalg.norm(q - e) < tol:
                return False
        return True

    # Remove duplicates from initial set
    unique = [elements[0]]
    for e in elements[1:]:
        if is_new(e, unique, tol):
            unique.append(e)
    elements = unique

    # Close under multiplication
    changed = True
    iteration = 0
    while changed and len(elements) < max_size:
        changed = False
        iteration += 1
        new_elements = []
        for g1 in elements:
            for g2 in elements:
                prod = normalize_quat(quat_multiply(g1, g2))
                if is_new(prod, elements + new_elements, tol):
                    new_elements.append(prod)
                    changed = True
                    if len(elements) + len(new_elements) >= max_size:
                        break
            if len(elements) + len(new_elements) >= max_size:
                break
        elements.extend(new_elements)

    return np.array(elements)


def binary_tetrahedral_group():
    """
    Binary tetrahedral group 2T (order 24).

    Elements: {±1, ±i, ±j, ±k} (8 quaternions, the quaternion group Q8)
    plus 16 elements of the form (1/2)(±1 ± i ± j ± k)
    Total: 24 elements
    """
    elements = []

    # Q8 elements: ±1, ±i, ±j, ±k
    for sign in [1, -1]:
        elements.append(np.array([sign, 0.0, 0.0, 0.0]))
        elements.append(np.array([0.0, sign, 0.0, 0.0]))
        elements.append(np.array([0.0, 0.0, sign, 0.0]))
        elements.append(np.array([0.0, 0.0, 0.0, sign]))

    # 16 elements: (1/2)(±1 ± i ± j ± k)
    for s0 in [1, -1]:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                for s3 in [1, -1]:
                    elements.append(np.array([s0, s1, s2, s3]) * 0.5)

    result = np.array(elements)
    assert len(result) == 24, f"Expected 24 elements, got {len(result)}"
    return result


def binary_octahedral_group():
    """
    Binary octahedral group 2O (order 48).

    Contains all elements of 2T (24) plus 24 additional elements of the form:
    (1/√2)(±1 ± i), (1/√2)(±1 ± j), (1/√2)(±1 ± k),
    (1/√2)(±i ± j), (1/√2)(±i ± k), (1/√2)(±j ± k)
    """
    elements = []

    # First, all 2T elements
    elements_2T = binary_tetrahedral_group()
    elements.extend([e for e in elements_2T])

    # 24 additional elements: permutations of (1/√2)(±a, ±b, 0, 0)
    s2 = 1.0 / np.sqrt(2.0)

    # All pairs of indices (i,j) from {0,1,2,3} with i<j
    for i in range(4):
        for j in range(i+1, 4):
            for si in [1, -1]:
                for sj in [1, -1]:
                    e = np.array([0.0, 0.0, 0.0, 0.0])
                    e[i] = si * s2
                    e[j] = sj * s2
                    elements.append(e)

    result = np.array(elements)
    assert len(result) == 48, f"Expected 48 elements, got {len(result)}"

    # Verify closure
    _verify_closure(result, "2O")

    return result


def binary_icosahedral_group():
    """
    Binary icosahedral group 2I (order 120).

    The 120 elements consist of:
    - 8 elements: ±1, ±i, ±j, ±k
    - 16 elements: (1/2)(±1 ± i ± j ± k)
    - 96 elements: all even permutations of (1/2)(0, ±1, ±φ^{-1}, ±φ)
      where φ = (1+√5)/2 is the golden ratio

    The 96 elements come from: take (0, ±1, ±1/φ, ±φ)/2 and apply
    all even permutations of the last 3 coordinates.
    Actually, for quaternions we permute all 4 components.
    """
    phi = (1.0 + np.sqrt(5.0)) / 2.0  # Golden ratio ≈ 1.618
    phi_inv = 1.0 / phi  # = φ - 1 ≈ 0.618

    elements = set()

    def add_element(q):
        """Add element, normalizing and using a canonical form for dedup."""
        q = q / np.linalg.norm(q)
        # Use tuple for set membership
        # Round to avoid floating point issues
        key = tuple(np.round(q, 10))
        elements.add(key)

    # Type 1: 8 elements — ±1, ±i, ±j, ±k
    for idx in range(4):
        for sign in [1, -1]:
            e = np.zeros(4)
            e[idx] = sign
            add_element(e)

    # Type 2: 16 elements — (1/2)(±1, ±1, ±1, ±1)
    for s0 in [1, -1]:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                for s3 in [1, -1]:
                    add_element(np.array([s0, s1, s2, s3]) * 0.5)

    # Type 3: 96 elements — even permutations of (0, ±1, ±φ^{-1}, ±φ)/2
    # The even permutations of (0,1,2,3) are:
    even_perms = [
        (0,1,2,3), (0,2,3,1), (0,3,1,2),
        (1,0,3,2), (1,2,0,3), (1,3,2,0),
        (2,0,1,3), (2,1,3,0), (2,3,0,1),
        (3,0,2,1), (3,1,0,2), (3,2,1,0)
    ]

    base_values = [0.0, 1.0, phi_inv, phi]

    for perm in even_perms:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                for s3 in [1, -1]:
                    vals = [0.0, s1 * 1.0, s2 * phi_inv, s3 * phi]
                    e = np.zeros(4)
                    for i, p in enumerate(perm):
                        e[i] = vals[p]
                    e *= 0.5
                    add_element(e)

    result = np.array([np.array(e) for e in elements])

    if len(result) != 120:
        print(f"WARNING: Got {len(result)} elements for 2I, expected 120. Attempting closure...")
        # Use closure to complete the group
        generators = result[:min(10, len(result))]
        result = generate_group_closure(list(generators), max_size=130)

    assert len(result) == 120, f"Expected 120 elements for 2I, got {len(result)}"

    # Verify closure
    _verify_closure(result, "2I")

    return result


def _verify_closure(elements, name, tol=1e-8):
    """Verify that a set of quaternions forms a group under multiplication."""
    n = len(elements)

    # Check a random sample of products (full check is O(n^2))
    n_checks = min(500, n * n)
    rng = np.random.RandomState(42)

    failures = 0
    for _ in range(n_checks):
        i = rng.randint(n)
        j = rng.randint(n)
        prod = normalize_quat(quat_multiply(elements[i], elements[j]))

        # Check if product is in the group
        dists = np.linalg.norm(elements - prod, axis=1)
        if np.min(dists) > tol:
            failures += 1

    if failures > 0:
        print(f"WARNING: {name} closure check: {failures}/{n_checks} products not found in group!")
    else:
        print(f"{name} closure check passed ({n_checks} random products verified)")


def precompute_multiplication_table(elements, tol=1e-8):
    """
    Precompute the multiplication table for a finite group.

    Returns:
        mult_table: numpy array of shape (N, N) where mult_table[i,j] = index of elements[i] * elements[j]
        inv_table: numpy array of shape (N,) where inv_table[i] = index of elements[i]^{-1}
    """
    n = len(elements)
    mult_table = np.zeros((n, n), dtype=np.int32)
    inv_table = np.zeros(n, dtype=np.int32)

    for i in range(n):
        for j in range(n):
            prod = normalize_quat(quat_multiply(elements[i], elements[j]))
            dists = np.linalg.norm(elements - prod, axis=1)
            idx = np.argmin(dists)
            if dists[idx] > tol:
                raise ValueError(f"Product of elements {i} and {j} not found in group! Min dist: {dists[idx]}")
            mult_table[i, j] = idx

    # Identity is the element closest to (1,0,0,0)
    identity = np.array([1.0, 0.0, 0.0, 0.0])
    id_idx = np.argmin(np.linalg.norm(elements - identity, axis=1))

    # Inverse table
    for i in range(n):
        inv_q = quat_conjugate(elements[i])
        inv_q = normalize_quat(inv_q)
        dists = np.linalg.norm(elements - inv_q, axis=1)
        inv_table[i] = np.argmin(dists)

    # Verify: e * e^{-1} = identity
    for i in range(n):
        assert mult_table[i, inv_table[i]] == id_idx, f"Inverse check failed for element {i}"

    print(f"Multiplication table computed: {n}x{n}, identity at index {id_idx}")

    return mult_table, inv_table, id_idx


if __name__ == "__main__":
    print("=" * 60)
    print("Constructing finite subgroups of SU(2)")
    print("=" * 60)

    print("\n--- Binary Tetrahedral Group 2T ---")
    elements_2T = binary_tetrahedral_group()
    print(f"Order: {len(elements_2T)}")
    _verify_closure(elements_2T, "2T")
    mt_2T, inv_2T, id_2T = precompute_multiplication_table(elements_2T)

    print("\n--- Binary Octahedral Group 2O ---")
    elements_2O = binary_octahedral_group()
    print(f"Order: {len(elements_2O)}")
    mt_2O, inv_2O, id_2O = precompute_multiplication_table(elements_2O)

    print("\n--- Binary Icosahedral Group 2I ---")
    elements_2I = binary_icosahedral_group()
    print(f"Order: {len(elements_2I)}")
    mt_2I, inv_2I, id_2I = precompute_multiplication_table(elements_2I)

    print("\n" + "=" * 60)
    print("All groups constructed successfully!")
    print(f"2T: {len(elements_2T)} elements")
    print(f"2O: {len(elements_2O)} elements")
    print(f"2I: {len(elements_2I)} elements")
    print("=" * 60)
