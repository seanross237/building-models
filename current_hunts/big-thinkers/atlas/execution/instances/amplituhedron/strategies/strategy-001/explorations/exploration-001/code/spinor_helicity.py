"""
Spinor-Helicity Formalism — Core Infrastructure

Implements:
  - Complex 2-component Weyl spinors |i⟩ (lambda) and |i] (lambda_tilde)
  - Angle brackets ⟨ij⟩ = λ_i^1 λ_j^2 - λ_i^2 λ_j^1
  - Square brackets [ij] = λ̃_i^1 λ̃_j^2 - λ̃_i^2 λ̃_j^1
  - Momentum construction: p_i^{αα̇} = |i⟩[i| = p_μ σ^μ
  - Mandelstam invariants via s_{ij} = ⟨ij⟩[ij]

Conventions:
  - Signature (+,-,-,-)
  - σ^μ = (I, σ_x, σ_y, σ_z)
  - p^{αα̇} = p_μ σ^μ = |i⟩[i|
  - Identity: s_{ij} = (p_i + p_j)² = ⟨ij⟩[ij]
    Note: some refs using (-,+,+,+) write s = ⟨ij⟩[ji]; we use (+,-,-,-)
    so s = ⟨ij⟩[ij]. Both are self-consistent.
"""

import numpy as np
from dataclasses import dataclass
from typing import List

# Pauli matrices
sigma = np.array([
    [[1, 0], [0, 1]],      # σ^0 = I
    [[0, 1], [1, 0]],      # σ^1 = σ_x
    [[0, -1j], [1j, 0]],   # σ^2 = σ_y
    [[1, 0], [0, -1]]      # σ^3 = σ_z
], dtype=complex)

sigma_bar = np.array([
    [[1, 0], [0, 1]],
    [[0, -1], [-1, 0]],
    [[0, 1j], [-1j, 0]],
    [[-1, 0], [0, 1]]
], dtype=complex)


@dataclass
class Particle:
    """A massless particle with momentum and spinor data."""
    label: int
    lam: np.ndarray       # |i⟩ : 2-component (shape (2,))
    lam_tilde: np.ndarray  # |i] : 2-component (shape (2,))

    @property
    def momentum_matrix(self) -> np.ndarray:
        """p^{αα̇} = |i⟩[i|"""
        return np.outer(self.lam, self.lam_tilde)

    @property
    def four_momentum(self) -> np.ndarray:
        """p^μ from p^{αα̇} = p_μ σ^μ => p_μ = (1/2) Tr(σ̄_μ · P)"""
        P = self.momentum_matrix
        p = np.zeros(4, dtype=complex)
        for mu in range(4):
            p[mu] = 0.5 * np.trace(sigma_bar[mu] @ P)
        return p

    @property
    def mass_squared(self) -> complex:
        """p² with (+,-,-,-)"""
        p = self.four_momentum
        return p[0]**2 - p[1]**2 - p[2]**2 - p[3]**2


def angle_bracket(pi: Particle, pj: Particle) -> complex:
    """⟨ij⟩ = λ_i^1 λ_j^2 - λ_i^2 λ_j^1"""
    return pi.lam[0] * pj.lam[1] - pi.lam[1] * pj.lam[0]


def square_bracket(pi: Particle, pj: Particle) -> complex:
    """[ij] = λ̃_i^1 λ̃_j^2 - λ̃_i^2 λ̃_j^1"""
    return pi.lam_tilde[0] * pj.lam_tilde[1] - pi.lam_tilde[1] * pj.lam_tilde[0]


def ab(pi, pj):
    """Shorthand for angle bracket."""
    return angle_bracket(pi, pj)


def sb(pi, pj):
    """Shorthand for square bracket."""
    return square_bracket(pi, pj)


def mandelstam_sij(pi: Particle, pj: Particle) -> complex:
    """s_{ij} = (p_i + p_j)² = ⟨ij⟩[ij] in our (+,-,-,-) conventions."""
    return angle_bracket(pi, pj) * square_bracket(pi, pj)


def mandelstam_sij_from_4vec(pi: Particle, pj: Particle) -> complex:
    """s_{ij} from 4-vectors directly, for cross-checking."""
    p = pi.four_momentum + pj.four_momentum
    return p[0]**2 - p[1]**2 - p[2]**2 - p[3]**2


def momentum_sum(particles: List[Particle]) -> np.ndarray:
    """Sum of 4-momenta."""
    return sum(p.four_momentum for p in particles)


def spinors_from_momentum(p_mu: np.ndarray, label: int = 0) -> Particle:
    """Given a lightlike 4-vector p^μ, extract spinors |p⟩ and |p].

    Build p^{αα̇} = p_μ σ^μ, then factor as |p⟩[p|.
    For lightlike momentum, this 2x2 matrix has rank 1.
    """
    P = sum(p_mu[mu] * sigma[mu] for mu in range(4))

    # P is rank 1. Factor: pick a nonzero column for |p⟩
    col0_norm = abs(P[0, 0])**2 + abs(P[1, 0])**2
    col1_norm = abs(P[0, 1])**2 + abs(P[1, 1])**2

    if col0_norm >= col1_norm:
        lam = np.array([P[0, 0], P[1, 0]], dtype=complex)
    else:
        lam = np.array([P[0, 1], P[1, 1]], dtype=complex)

    # Extract [p| from P = |p⟩[p|: [p| = P^T |p⟩* / |⟨p|p⟩|
    # More directly: if lam[a] != 0, then lam_tilde[b] = P[a,b] / lam[a]
    if abs(lam[0]) >= abs(lam[1]):
        lam_tilde = P[0, :] / lam[0]
    else:
        lam_tilde = P[1, :] / lam[1]

    return Particle(label=label, lam=lam, lam_tilde=lam_tilde)


def make_kinematics_com(E: float, theta: float) -> List[Particle]:
    """4-particle COM kinematics, all-outgoing convention.

    p1 + p2 + p3 + p4 = 0, all lightlike.

    p1 = (E, 0, 0, E)           # "incoming" along +z
    p2 = (E, 0, 0, -E)          # "incoming" along -z
    p3 = (-E, -E sinθ, 0, -E cosθ)  # "outgoing" scattered
    p4 = (-E, E sinθ, 0, E cosθ)    # "outgoing" scattered
    """
    st, ct = np.sin(theta), np.cos(theta)
    vecs = [
        np.array([E, 0, 0, E], dtype=complex),
        np.array([E, 0, 0, -E], dtype=complex),
        np.array([-E, -E*st, 0, -E*ct], dtype=complex),
        np.array([-E, E*st, 0, E*ct], dtype=complex),
    ]
    return [spinors_from_momentum(v, label=i+1) for i, v in enumerate(vecs)]


def make_kinematics_from_spinors(seed: int = 42) -> List[Particle]:
    """Generate 4-particle kinematics from random spinors.

    Strategy: pick spinors for 1,2,3 freely. For real momenta, use λ̃ = λ*.
    Then p4 = -(p1+p2+p3) must be lightlike.

    Better strategy: parametrize 2→2 scattering directly.
    Use COM frame: pick random energy and angle.
    """
    rng = np.random.RandomState(seed)
    E = 1.0 + rng.rand()  # random energy between 1 and 2
    theta = 0.3 + rng.rand() * 2.0  # random angle
    return make_kinematics_com(E, theta)


def validate_kinematics(particles: List[Particle], verbose: bool = True) -> dict:
    """Check momentum conservation, masslessness, and bracket identities."""
    info = {}

    # Momentum conservation
    total_p = momentum_sum(particles)
    mom_cons = np.max(np.abs(total_p.real))
    info['mom_conservation'] = mom_cons
    if verbose:
        print(f"Momentum conservation |Σp| = {mom_cons:.2e}")

    # Masslessness
    for p in particles:
        m2 = p.mass_squared
        if verbose:
            print(f"  p_{p.label}² = {m2.real:.2e}")

    # Mandelstam invariants — two independent ways
    p1, p2, p3, p4 = particles
    s_ab = mandelstam_sij(p1, p2)
    s_4v = mandelstam_sij_from_4vec(p1, p2)
    t_ab = mandelstam_sij(p2, p3)
    t_4v = mandelstam_sij_from_4vec(p2, p3)
    u_ab = mandelstam_sij(p1, p3)
    u_4v = mandelstam_sij_from_4vec(p1, p3)

    info['s'] = s_ab
    info['t'] = t_ab
    info['u'] = u_ab

    if verbose:
        print(f"\nMandelstam invariants (spinor / 4-vector):")
        print(f"  s₁₂ = {s_ab:.6f} / {s_4v:.6f}")
        print(f"  t₂₃ = {t_ab:.6f} / {t_4v:.6f}")
        print(f"  u₁₃ = {u_ab:.6f} / {u_4v:.6f}")
        print(f"  s+t+u = {(s_ab+t_ab+u_ab):.2e} (should be 0)")

    # Schouten identity check: ⟨12⟩⟨34⟩ + ⟨13⟩⟨42⟩ + ⟨14⟩⟨23⟩ = 0
    schouten = (ab(p1,p2)*ab(p3,p4) + ab(p1,p3)*ab(p4,p2) + ab(p1,p4)*ab(p2,p3))
    info['schouten'] = schouten
    if verbose:
        print(f"  Schouten identity = {abs(schouten):.2e} (should be 0)")

    return info


if __name__ == "__main__":
    print("=" * 60)
    print("TEST: Center-of-mass kinematics (E=1, θ=π/3)")
    print("=" * 60)
    particles = make_kinematics_com(E=1.0, theta=np.pi/3)
    validate_kinematics(particles)

    print("\nSpinor brackets:")
    for i in range(4):
        for j in range(i+1, 4):
            a = angle_bracket(particles[i], particles[j])
            s = square_bracket(particles[i], particles[j])
            print(f"  ⟨{i+1}{j+1}⟩ = {a:.6f},  [{i+1}{j+1}] = {s:.6f}")

    print("\n" + "=" * 60)
    print("TEST: Random kinematics")
    print("=" * 60)
    particles2 = make_kinematics_from_spinors(seed=42)
    validate_kinematics(particles2)
