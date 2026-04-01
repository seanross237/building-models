"""
Stage 1: Construct the Phase Freedom Space for a Qubit (N=2)

Given Gamma_ij = |U_ij|^2, find all Theta such that:
  1. |Theta_ij|^2 = Gamma_ij  (element-wise magnitude constraint)
  2. Theta is unitary (defines a valid quantum channel)

For a qubit with H = (omega/2)*sigma_z, t = pi/4:
  U = [[cos(pi/4), -i*sin(pi/4)], [-i*sin(pi/4), cos(pi/4)]]
  Gamma = [[1/2, 1/2], [1/2, 1/2]]

The most general Theta with |Theta_ij|^2 = Gamma_ij is:
  Theta = [[sqrt(Gamma_00)*e^(i*phi_00), sqrt(Gamma_01)*e^(i*phi_01)],
           [sqrt(Gamma_10)*e^(i*phi_10), sqrt(Gamma_11)*e^(i*phi_11)]]
       = (1/sqrt(2)) * [[e^(i*phi_00), e^(i*phi_01)],
                         [e^(i*phi_10), e^(i*phi_11)]]

Subject to: Theta must be UNITARY (Theta^dagger Theta = I).
"""

import numpy as np
from itertools import product

print("=" * 70)
print("STAGE 1: Phase Freedom Space for Qubit Transition Kernel")
print("=" * 70)

# ============================================================
# Setup: Define the quantum system
# ============================================================
omega = 1.0
hbar = 1.0
t = np.pi / 4

# Unitary evolution
U = np.array([
    [np.cos(t), -1j * np.sin(t)],
    [-1j * np.sin(t), np.cos(t)]
], dtype=complex)

# Transition kernel
Gamma = np.abs(U) ** 2
print(f"\nU =\n{U}")
print(f"\nGamma = |U|^2 =\n{Gamma}")
print(f"\nGamma should be [[1/2, 1/2], [1/2, 1/2]]:")
print(f"  Gamma_00 = {Gamma[0,0]:.6f} (expected 0.5)")
print(f"  Gamma_01 = {Gamma[0,1]:.6f} (expected 0.5)")

# Verify U is unitary
UdU = U.conj().T @ U
print(f"\nU^dag U = \n{UdU}")
print(f"Is U unitary? {np.allclose(UdU, np.eye(2))}")

# ============================================================
# General Theta with |Theta_ij|^2 = Gamma_ij
# ============================================================
print(f"\n{'='*70}")
print("CONSTRUCTING GENERAL THETA")
print("=" * 70)

# Theta = (1/sqrt(2)) * [[e^(i*a), e^(i*b)], [e^(i*c), e^(i*d)]]
# where a = phi_00, b = phi_01, c = phi_10, d = phi_11
#
# Unitarity: Theta^dag Theta = I
# Row 1 . Row 1: |Theta_00|^2 + |Theta_01|^2 = 1/2 + 1/2 = 1 ✓ (automatic)
# Row 2 . Row 2: |Theta_10|^2 + |Theta_11|^2 = 1/2 + 1/2 = 1 ✓ (automatic)
# Row 1 . Row 2 = 0: Theta_00* Theta_10 + Theta_01* Theta_11 = 0
#
# For Theta Theta^dag = I (columns):
# Col 1 . Col 1: automatic ✓
# Col 2 . Col 2: automatic ✓
# Col 1 . Col 2 = 0: Theta_00 Theta_01* + Theta_10 Theta_11* = 0
#
# Let's work out the orthogonality constraint:
# (1/2) * [e^(-ia) e^(ic) + e^(-ib) e^(id)] = 0
# => e^(i(c-a)) + e^(i(d-b)) = 0
# => e^(i(c-a)) = -e^(i(d-b))
# => c - a = d - b + pi + 2k*pi   (for some integer k)
# => (c - a) - (d - b) = pi + 2k*pi
# => c - a - d + b = pi (mod 2pi)
#
# So we have 4 phases (a,b,c,d) and 1 constraint: c - a - d + b = pi (mod 2pi)
# That leaves 3 free real parameters.
#
# But wait: global phase doesn't matter for quantum states.
# If we factor out e^(ia), we get Theta = e^(ia) * (1/sqrt(2)) * [[1, e^(i(b-a))], [e^(i(c-a)), e^(i(d-a))]]
# Setting alpha = b-a, beta = c-a, gamma = d-a:
# Constraint: beta - gamma + alpha... let me redo.
# c - a - d + b = pi => beta - gamma + alpha... wait:
# b - a = alpha, c - a = beta, d - a = gamma
# constraint: (c-a) - (d-a) + (b-a) = pi => beta - gamma + alpha = pi (mod 2pi)
# So gamma = alpha + beta - pi (mod 2pi)
# Free parameters: a (global phase), alpha, beta. gamma is determined.
# If global phase doesn't matter: 2 free parameters (alpha, beta).
#
# Let's verify this analytically and numerically.

print("\nAnalytic analysis:")
print("  Theta = (1/√2) [[e^(ia), e^(ib)], [e^(ic), e^(id)]]")
print("  Unitarity constraint: c - a - d + b ≡ π (mod 2π)")
print("  => d = b + c - a - π (mod 2π)")
print("  Free parameters before global phase: a, b, c (3 real)")
print("  Global phase a is physically irrelevant → 2 free parameters (b-a, c-a)")
print("  => Phase freedom space has REAL DIMENSION 2")

# Let's verify by explicit construction
def make_theta(a, b, c):
    """Construct Theta from 3 phases (a is global, will be set to 0)."""
    d = b + c - a - np.pi  # unitarity constraint
    Theta = (1/np.sqrt(2)) * np.array([
        [np.exp(1j*a), np.exp(1j*b)],
        [np.exp(1j*c), np.exp(1j*d)]
    ], dtype=complex)
    return Theta

def make_theta_2param(alpha, beta):
    """Construct Theta from 2 free parameters (global phase = 0).
    alpha = b - a, beta = c - a, with a = 0.
    """
    a = 0.0
    b = alpha
    c = beta
    d = alpha + beta - np.pi
    return make_theta(a, b, c)

# ============================================================
# Verify: sample the 2-parameter family
# ============================================================
print(f"\n{'='*70}")
print("VERIFICATION: Sampling the 2-parameter phase freedom space")
print("=" * 70)

np.random.seed(42)
n_samples = 1000
n_valid = 0
n_invalid = 0
max_unitarity_err = 0
max_gamma_err = 0

for _ in range(n_samples):
    alpha = np.random.uniform(0, 2*np.pi)
    beta = np.random.uniform(0, 2*np.pi)
    Theta = make_theta_2param(alpha, beta)

    # Check |Theta_ij|^2 = Gamma_ij
    Gamma_check = np.abs(Theta)**2
    gamma_err = np.max(np.abs(Gamma_check - Gamma))

    # Check unitarity
    TdT = Theta.conj().T @ Theta
    unit_err = np.max(np.abs(TdT - np.eye(2)))

    max_unitarity_err = max(max_unitarity_err, unit_err)
    max_gamma_err = max(max_gamma_err, gamma_err)

    if unit_err < 1e-12 and gamma_err < 1e-12:
        n_valid += 1
    else:
        n_invalid += 1

print(f"  Sampled {n_samples} random (alpha, beta) pairs:")
print(f"  Valid (unitary AND |Theta|^2=Gamma): {n_valid}/{n_samples}")
print(f"  Max unitarity error: {max_unitarity_err:.2e}")
print(f"  Max Gamma error: {max_gamma_err:.2e}")

# Show a few explicit examples
print(f"\nExplicit examples:")
for alpha, beta, label in [(0, 0, "α=0,β=0"), (np.pi/2, 0, "α=π/2,β=0"),
                            (0, np.pi/2, "α=0,β=π/2"), (np.pi/4, np.pi/3, "α=π/4,β=π/3")]:
    Theta = make_theta_2param(alpha, beta)
    TdT = Theta.conj().T @ Theta
    det = np.linalg.det(Theta)
    print(f"\n  {label}:")
    print(f"    Theta = {Theta}")
    print(f"    |Theta|^2 = {np.abs(Theta)**2}")
    print(f"    Theta^dag Theta - I = {np.max(np.abs(TdT - np.eye(2))):.2e}")
    print(f"    det(Theta) = {det:.6f} (|det| = {abs(det):.6f})")

# ============================================================
# Topology: the space is a 2-torus T^2
# ============================================================
print(f"\n{'='*70}")
print("TOPOLOGY OF THE PHASE FREEDOM SPACE")
print("=" * 70)
print("  Parameters (alpha, beta) each range over [0, 2π)")
print("  Both are periodic (angles)")
print("  No additional constraints")
print("  => Topology is T^2 (2-torus)")
print("  => Real dimension = 2")

# ============================================================
# Which Theta corresponds to the original U?
# ============================================================
print(f"\n{'='*70}")
print("WHICH THETA GIVES THE ORIGINAL U?")
print("=" * 70)

# U = [[cos(t), -i*sin(t)], [-i*sin(t), cos(t)]]
# = [[1/√2, -i/√2], [-i/√2, 1/√2]]
# = (1/√2) [[1, -i], [-i, 1]]
# = (1/√2) [[e^(i*0), e^(i*(-π/2))], [e^(i*(-π/2)), e^(i*0)]]
# So a=0, b=-π/2, c=-π/2, d=0
# Check constraint: c - a - d + b = -π/2 - 0 - 0 + (-π/2) = -π ≡ π (mod 2π) ✓
# alpha = b - a = -π/2, beta = c - a = -π/2

alpha_U = -np.pi/2
beta_U = -np.pi/2
Theta_U = make_theta_2param(alpha_U, beta_U)
print(f"  Original U:\n  {U}")
print(f"  Reconstructed Theta(α=-π/2, β=-π/2):\n  {Theta_U}")
print(f"  Match? {np.allclose(U, Theta_U)}")

# ============================================================
# Control check: Gamma = Identity (no evolution)
# ============================================================
print(f"\n{'='*70}")
print("CONTROL CHECK: Gamma = Identity (trivial evolution)")
print("=" * 70)

# If Gamma = I, then |Theta_ij|^2 = delta_ij
# So Theta_01 = 0, Theta_10 = 0 (off-diagonal are zero)
# Theta = diag(e^(ia), e^(id))
# This is automatically unitary for any a, d
# Phase freedom: 2 angles → T^2 (but one is global phase)
# So effectively 1 free parameter → T^1 (circle)

# But wait — for Gamma = I, we have sqrt(Gamma_00)=1, sqrt(Gamma_01)=0, etc.
# The off-diagonal entries are forced to be 0, so there's no phase freedom there.
# We get Theta = diag(e^(i*phi_0), e^(i*phi_1))
# Modulo global phase: 1 free parameter
# This is the expected result: pure gauge transformations

print("  Gamma = I:")
print("  Off-diagonal entries forced to 0 (|Theta_01|^2 = 0)")
print("  Theta = diag(e^(i*phi_0), e^(i*phi_1))")
print("  Modulo global phase: 1 free parameter (relative phase)")
print("  Phase freedom space: T^1 (circle) = diagonal gauge group")
print("  This matches expectation: no dynamics → only gauge freedom")

# Verify numerically
Gamma_triv = np.eye(2)
# For Gamma = I, Theta must be diagonal unitary
# Check: any diagonal unitary satisfies |Theta_ij|^2 = delta_ij
for phi in [0, np.pi/4, np.pi/2, np.pi]:
    Theta_diag = np.diag([1.0, np.exp(1j*phi)])
    assert np.allclose(np.abs(Theta_diag)**2, Gamma_triv)
    assert np.allclose(Theta_diag.conj().T @ Theta_diag, np.eye(2))
print("  Numerical verification: PASSED for diagonal unitaries")

# ============================================================
# CPTP Analysis
# ============================================================
print(f"\n{'='*70}")
print("CPTP CONSTRAINT ANALYSIS")
print("=" * 70)

# The GOAL asks about CPTP maps. Barandes' Theta defines a quantum channel via:
# E(rho) = Theta rho Theta^dag (if Theta is unitary, this is a unitary channel)
#
# A unitary channel is automatically CPTP:
# - Completely positive: yes (Kraus representation with single operator)
# - Trace preserving: Tr(Theta rho Theta^dag) = Tr(Theta^dag Theta rho) = Tr(rho) = 1
#
# So the CPTP constraint adds NOTHING beyond unitarity.
# The constraint is: |Theta_ij|^2 = Gamma_ij AND Theta is unitary.
# That's exactly what we computed above.

print("  Theta is unitary => the channel E(rho) = Theta rho Theta^dag is automatically CPTP")
print("  (Single Kraus operator K = Theta; Theta^dag Theta = I => trace-preserving)")
print("  => CPTP adds NO additional constraints beyond unitarity")
print("  => Phase freedom space dimension remains 2 (T^2 topology)")

# However, note: in Barandes' framework, Theta is not the unitary U.
# Theta is the matrix whose squared magnitudes give the transition probabilities.
# If we allow NON-unitary Theta (e.g., Kraus-type channels), the space could be larger.
# But the GOAL specifically says "Theta defines a valid quantum channel" and the
# simplest interpretation for a qubit is that Theta itself is unitary.
# Let me also check: could there be non-unitary Theta with CPTP?

print("\n  NOTE ON NON-UNITARY THETA:")
print("  In Barandes' framework, Theta_ij = sqrt(Gamma_ij) * e^(i*phase_ij)")
print("  The matrix Theta must be such that the map rho -> Theta rho Theta^dag is CPTP.")
print("  For a single Kraus operator K=Theta, CPTP requires K^dag K = I (unitarity).")
print("  So unitary is the ONLY option for a single-Kraus-operator channel.")
print("  Multiple Kraus operators would change the problem entirely.")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*70}")
print("STAGE 1 SUMMARY")
print("=" * 70)
print("  System: qubit, H = (ω/2)σ_z, t = π/4")
print("  Transition kernel: Γ = [[1/2, 1/2], [1/2, 1/2]]")
print("  Phase freedom space:")
print("    - Parameterized by (α, β) ∈ [0, 2π) × [0, 2π)")
print("    - Theta(α,β) = (1/√2)[[1, e^(iα)], [e^(iβ), e^(i(α+β-π))]]")
print("    - Real dimension: 2 (modulo global phase)")
print("    - Topology: T^2 (2-torus)")
print("    - CPTP imposes no additional constraints beyond unitarity")
print("    - Original U corresponds to (α,β) = (-π/2, -π/2)")
print("  Control check: Γ = I → dimension 1, T^1 (diagonal phases) ✓")
print("=" * 70)
