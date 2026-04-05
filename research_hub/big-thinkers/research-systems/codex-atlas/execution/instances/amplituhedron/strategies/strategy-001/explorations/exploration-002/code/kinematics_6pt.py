"""
6-Particle Kinematics for N=4 SYM Amplitude Computations

Generates 6 massless momenta satisfying momentum conservation,
using the spinor-helicity formalism from exploration-001.

Strategy for real kinematics:
  - Choose spinors λᵢ for i=1,...,5 randomly
  - Set λ̃ᵢ = λᵢ* (for real momenta)
  - Compute p₆ = -(p₁+...+p₅) and extract spinors from it

Note: p₆ = -(p₁+...+p₅) is automatically lightlike only for special
configurations. We use a different approach: parametrize using
a known 6-particle phase-space parametrization that guarantees
all momenta lightlike AND sum to zero.

Parametrization: Use the "split" approach.
  - Particles 1,2,3 form one "cluster", 4,5,6 another
  - Build each cluster to sum to a common momentum K, with K² ≠ 0
  - Then boost/re-scale so total = 0

Better: Use the standard massless phase-space parametrization
via random spinors with a final momentum-conservation fix.
"""

import numpy as np
import sys
import os

# Path to exploration-001 code
EXPLORATION_001 = os.path.join(os.path.dirname(__file__),
    '../../exploration-001/code')
sys.path.insert(0, EXPLORATION_001)
sys.path.insert(0, os.path.dirname(__file__))

from spinor_helicity import (
    Particle, angle_bracket, square_bracket, ab, sb,
    spinors_from_momentum, sigma, sigma_bar
)


def make_6pt_kinematics(seed=42):
    """Generate 6 massless particles with momentum conservation.

    Method: "3+3 balanced" construction.

    Build particles 1,2,3 in a 3-body rest frame with total momentum K.
    Build particles 4,5,6 in a 3-body rest frame with total momentum -K.
    This guarantees p₁+...+p₆ = 0 exactly.

    In the K rest frame, the 3-body decay is parametrized by 2 angles.
    We use a concrete choice: uniform angular distribution.
    """
    rng = np.random.RandomState(seed)

    # ---- Cluster 1: particles 1,2,3 in rest frame of K = (E,0,0,0) ----
    # 3-body phase space: two angles per particle, constrained by energy-mom conservation
    # Simple parametrization via isotropic decay:

    E_cm = 1.0  # Center-of-mass energy of each cluster

    # Particle 1 in K-frame
    cos1 = rng.uniform(-1, 1)
    phi1 = rng.uniform(0, 2*np.pi)
    sin1 = np.sqrt(1 - cos1**2)

    # Particle 2 gets remaining energy after particle 1 emission
    # Use 2-body kinematics first: 1 → (1) + (23)
    # Then 2-body: (23) → (2) + (3)

    # Energy fractions: x1 in [0,1], x2 in [0, 1-x1], x3 = 1-x1-x2
    x1 = rng.uniform(0.2, 0.6)
    x2 = rng.uniform(0.1, min(0.6, 1 - x1 - 0.1))
    x3 = 1.0 - x1 - x2
    if x3 < 0.1:
        x3 = 0.1
        x2 = 1.0 - x1 - x3

    E1, E2, E3 = x1 * E_cm, x2 * E_cm, x3 * E_cm

    # Random directions (but must be consistent with momentum conservation)
    # Build explicitly: pick 1 and 2 directions, derive 3
    cos_a = rng.uniform(-1, 1); phi_a = rng.uniform(0, 2*np.pi)
    cos_b = rng.uniform(-1, 1); phi_b = rng.uniform(0, 2*np.pi)

    sin_a = np.sqrt(1 - cos_a**2)
    sin_b = np.sqrt(1 - cos_b**2)

    p1_3 = E1 * np.array([sin_a * np.cos(phi_a), sin_a * np.sin(phi_a), cos_a])
    p2_3 = E2 * np.array([sin_b * np.cos(phi_b), sin_b * np.sin(phi_b), cos_b])
    p3_3 = -(p1_3 + p2_3)

    # Check p3 is lightlike: |p3_3| must equal E3
    p3_norm = np.linalg.norm(p3_3)
    # Rescale x3 to make it work:
    # We have p3_3 fixed, so E3 = |p3_3|, then renormalize total energy
    E3_actual = p3_norm
    E_total = E1 + E2 + E3_actual
    # Rescale all to E_cm
    scale = E_cm / E_total
    E1 *= scale; p1_3 *= scale
    E2 *= scale; p2_3 *= scale
    E3_actual *= scale; p3_3 *= scale

    # Build 4-vectors (outgoing convention: positive energy)
    p1_4 = np.array([E1, p1_3[0], p1_3[1], p1_3[2]], dtype=complex)
    p2_4 = np.array([E2, p2_3[0], p2_3[1], p2_3[2]], dtype=complex)
    p3_4 = np.array([E3_actual, p3_3[0], p3_3[1], p3_3[2]], dtype=complex)

    # ---- Cluster 2: particles 4,5,6 must sum to -K = (-E_cm, 0, 0, 0) ----
    # So they sum to (E_cm, 0, 0, 0) but with negative energy 4-vectors
    # Actually: all-outgoing convention means p₁+...+p₆=0.
    # Cluster 1: p1+p2+p3 = (E_cm, 0, 0, 0)
    # Cluster 2: p4+p5+p6 = (-E_cm, 0, 0, 0)
    # For massless particles with all-outgoing convention, energies can be negative
    # (or we can boost to make them positive).

    cos_c = rng.uniform(-1, 1); phi_c = rng.uniform(0, 2*np.pi)
    cos_d = rng.uniform(-1, 1); phi_d = rng.uniform(0, 2*np.pi)

    y1 = rng.uniform(0.2, 0.6)
    y2 = rng.uniform(0.1, min(0.6, 1 - y1 - 0.1))

    sin_c = np.sqrt(1 - cos_c**2)
    sin_d = np.sqrt(1 - cos_d**2)

    E4 = y1 * E_cm
    E5 = y2 * E_cm

    p4_3 = E4 * np.array([sin_c * np.cos(phi_c), sin_c * np.sin(phi_c), cos_c])
    p5_3 = E5 * np.array([sin_d * np.cos(phi_d), sin_d * np.sin(phi_d), cos_d])
    p6_3 = -(p4_3 + p5_3)
    E6_actual = np.linalg.norm(p6_3)
    E_total2 = E4 + E5 + E6_actual
    scale2 = E_cm / E_total2
    E4 *= scale2; p4_3 *= scale2
    E5 *= scale2; p5_3 *= scale2
    E6_actual *= scale2; p6_3 *= scale2

    # Cluster 2 has negative total 4-momentum (all-outgoing):
    p4_4 = np.array([-E4, -p4_3[0], -p4_3[1], -p4_3[2]], dtype=complex)
    p5_4 = np.array([-E5, -p5_3[0], -p5_3[1], -p5_3[2]], dtype=complex)
    p6_4 = np.array([-E6_actual, -p6_3[0], -p6_3[1], -p6_3[2]], dtype=complex)

    # Build particles
    particles = []
    for i, p4v in enumerate([p1_4, p2_4, p3_4, p4_4, p5_4, p6_4]):
        pt = spinors_from_momentum(p4v, label=i+1)
        particles.append(pt)

    return particles


def validate_6pt(particles, verbose=True):
    """Check momentum conservation and masslessness for 6-particle kinematics."""
    n = len(particles)
    assert n == 6

    # Momentum conservation
    total = sum(p.four_momentum for p in particles)
    mom_err = np.max(np.abs(total))

    # Masslessness
    mass_errs = [abs(p.mass_squared) for p in particles]

    if verbose:
        print(f"Momentum conservation |Σp| = {mom_err:.2e}")
        for i, p in enumerate(particles):
            print(f"  p_{i+1}² = {p.mass_squared.real:.2e}  "
                  f"  E = {p.four_momentum[0].real:.4f}")

    return mom_err, max(mass_errs)


def spinor_brackets_6pt(particles, verbose=True):
    """Print all angle and square brackets for 6 particles."""
    n = len(particles)
    print("\nAngle brackets ⟨ij⟩:")
    for i in range(n):
        row = ""
        for j in range(n):
            if j > i:
                val = ab(particles[i], particles[j])
                row += f"  ⟨{i+1}{j+1}⟩={val.real:+.4f}{val.imag:+.4f}i"
        if row:
            print(row)

    print("\nSquare brackets [ij]:")
    for i in range(n):
        row = ""
        for j in range(n):
            if j > i:
                val = sb(particles[i], particles[j])
                row += f"  [{i+1}{j+1}]={val.real:+.4f}{val.imag:+.4f}i"
        if row:
            print(row)


if __name__ == "__main__":
    print("=" * 60)
    print("6-PARTICLE KINEMATICS TEST")
    print("=" * 60)

    for seed in [42, 137, 999]:
        print(f"\n--- Seed = {seed} ---")
        parts = make_6pt_kinematics(seed=seed)
        mom_err, mass_err = validate_6pt(parts, verbose=True)
        print(f"  Max mass error: {mass_err:.2e}")
        ok = mom_err < 1e-10 and mass_err < 1e-10
        print(f"  Kinematics valid: {'YES' if ok else 'NO'}")

    print("\n--- Detailed brackets for seed=42 ---")
    parts = make_6pt_kinematics(seed=42)
    spinor_brackets_6pt(parts, verbose=True)
