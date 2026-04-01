"""
Stage 2b: Analytic and refined numerical analysis of consistent history families.

Key questions from Stage 2:
1. The 3-time consistency scan found 0 consistent families. Is this because:
   a) They exist at isolated points the grid missed?
   b) They genuinely don't exist for this system?
2. What about medium decoherence (Re D_off = 0)?
3. Can we solve the consistency equations analytically?

Strategy:
- Fix t_2 = computational basis
- Derive analytic expressions for D off-diagonal elements
- Use scipy.optimize to find roots
- Also try: eigenbasis of rho at each time (the "natural" consistent families)
"""

import numpy as np
from scipy.optimize import minimize, fsolve
from scipy.linalg import expm

print("=" * 70)
print("STAGE 2b: Refined Consistency Analysis")
print("=" * 70)

# ============================================================
# Setup
# ============================================================
omega = 1.0
t1 = np.pi / 4
t2 = np.pi / 2

def U(t):
    return np.array([
        [np.cos(t), -1j * np.sin(t)],
        [-1j * np.sin(t), np.cos(t)]
    ], dtype=complex)

U1 = U(t1)
U12 = U(t2 - t1)

plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
rho_0 = np.outer(plus, plus.conj())

def make_projector(theta, phi):
    a = np.array([np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)], dtype=complex)
    return np.outer(a, a.conj())

# ============================================================
# Section 1: Which bases are the "natural" consistent families?
# ============================================================
print(f"\n{'='*70}")
print("SECTION 1: Natural consistent families (eigenbases of evolved states)")
print("=" * 70)

# The most obvious consistent families come from the eigenbases of the
# evolved density matrices at each time.

rho_1 = U1 @ rho_0 @ U1.conj().T
rho_2 = U(t2) @ rho_0 @ U(t2).conj().T

print(f"rho_0 = \n{rho_0}")
print(f"\nrho_1 = U1 rho_0 U1† = \n{rho_1}")
print(f"\nrho_2 = U(t2) rho_0 U(t2)† = \n{rho_2}")

# Eigendecomposition
for name, rho in [("rho_0", rho_0), ("rho_1", rho_1), ("rho_2", rho_2)]:
    evals, evecs = np.linalg.eigh(rho)
    print(f"\n{name} eigenvalues: {evals}")
    print(f"{name} eigenvectors:\n  |0>: {evecs[:,0]}\n  |1>: {evecs[:,1]}")

# Note: rho_0 = |+><+| is rank-1, so eigenbasis = {|+>, |->}
# rho_1 and rho_2 are also rank-1 (pure states under unitary evolution)
# So the eigenbasis is {evolved|+>, orthogonal}

psi_1 = U1 @ plus
psi_2 = U(t2) @ plus
print(f"\n|ψ₁> = U1|+> = {psi_1}")
print(f"|ψ₂> = U2|+> = {psi_2}")

# ============================================================
# Section 2: Analytic consistency equations for t_2 = comp basis
# ============================================================
print(f"\n{'='*70}")
print("SECTION 2: Analytic consistency equations (t₂ = comp basis)")
print("=" * 70)

# Projectors at t_2: P_0 = |0><0|, P_1 = |1><1|
# Projectors at t_1: P_a(θ,φ), P_{a⊥}(θ,φ) = I - P_a

# Chain operators: C_{a,k} = P_k^(t2) U12 P_a^(t1) U1  (for a ∈ {0,1}, k ∈ {0,1})
# 4 histories indexed by (a,k)

# D((a,k), (a',k')) = Tr(C_{a,k} ρ₀ C_{a',k'}†)
# = Tr(P_k U12 P_a U1 ρ₀ U1† P_{a'} U12† P_{k'})

# For consistency: D((a,k), (a',k')) = 0 for (a,k) ≠ (a',k')

# Note: if k ≠ k', then P_k and P_{k'} are orthogonal (they're |0><0| and |1><1|)
# So D((a,k), (a',k')) = Tr(P_k ... P_{k'}) = 0 automatically when k ≠ k'!
# (Because we're computing Tr(... P_k M P_{k'}) and for the comp basis,
#  <k'|M|k> can be nonzero, wait, let me be more careful.)

# Actually: D((a,k), (a',k')) = Tr(P_k U12 P_a U1 ρ₀ U1† P_{a'} U12† P_{k'})
# = <k'| U12† |m><m| (some expression) |n><n| U12 |k> ... no, let me just compute:

# Let R = U12 P_a U1 ρ₀ U1† P_{a'} U12† (this is a 2x2 matrix)
# Then D = Tr(P_k R P_{k'}) = (P_{k'} P_k R)_{trace}
# = δ_{k,k'} R_{kk}  (for computational basis projectors!)

# So D((a,k), (a',k')) = δ_{k,k'} [U12 P_a U1 ρ₀ U1† P_{a'} U12†]_{kk}

# This means: histories with different k values automatically decohere!
# The only nontrivial consistency conditions are for k = k':
# D((a,k), (a',k)) = [U12 P_a U1 ρ₀ U1† P_{a'} U12†]_{kk} = 0 for a ≠ a'

# For the qubit, a ∈ {0, 1} (i.e., P_a and P_{a⊥}), so we need:
# [U12 P_a U1 ρ₀ U1† P_{a⊥} U12†]_{00} = 0  (for k=0)
# [U12 P_a U1 ρ₀ U1† P_{a⊥} U12†]_{11} = 0  (for k=1)

print("ANALYTIC SIMPLIFICATION:")
print("  Since t_2 uses computational basis: D((a,k),(a',k')) = δ_{k,k'} * R_{kk}")
print("  where R = U12 P_a U1 ρ₀ U1† P_{a'} U12†")
print("  Histories with different k automatically decohere!")
print("  Only need: [U12 P_a U1 ρ₀ U1† P_{a⊥} U12†]_{kk} = 0 for k=0,1")

# Compute this as a function of (theta, phi)
def off_diag_elements(theta, phi):
    """Compute the two off-diagonal elements that must vanish for consistency."""
    P_a = make_projector(theta, phi)
    P_b = np.eye(2) - P_a

    R = U12 @ P_a @ U1 @ rho_0 @ U1.conj().T @ P_b @ U12.conj().T
    return R[0, 0], R[1, 1]  # These must both be zero

# Scan with finer grid
print("\nFine scan of |D_off| as function of (θ, φ) (t₂ = comp basis):")
n_scan = 500
theta_scan = np.linspace(0.01, np.pi - 0.01, n_scan)
phi_scan = np.linspace(0, 2*np.pi - 0.01, n_scan)

min_total = 1.0
min_loc = None
near_consistent = []

for i, theta in enumerate(theta_scan):
    for j, phi in enumerate(phi_scan):
        d0, d1 = off_diag_elements(theta, phi)
        total = abs(d0) + abs(d1)
        if total < min_total:
            min_total = total
            min_loc = (theta, phi)
        if total < 0.001:
            near_consistent.append((theta, phi, total, abs(d0), abs(d1)))

print(f"  Minimum |D_off|_total = {min_total:.6e} at θ={min_loc[0]/np.pi:.4f}π, φ={min_loc[1]/np.pi:.4f}π")
print(f"  Near-consistent bases (|D_off| < 0.001): {len(near_consistent)}")

if near_consistent:
    for nc in near_consistent[:20]:
        print(f"    θ={nc[0]/np.pi:.4f}π, φ={nc[1]/np.pi:.4f}π, total={nc[2]:.6e}")

# Use optimization to find exact minimum
def objective(x):
    theta, phi = x
    d0, d1 = off_diag_elements(theta, phi)
    return abs(d0)**2 + abs(d1)**2

from scipy.optimize import minimize

# Try from multiple starting points
print(f"\nOptimization from multiple starting points:")
best_min = 1.0
best_loc = None

for th0 in np.linspace(0.1, np.pi-0.1, 20):
    for ph0 in np.linspace(0, 2*np.pi-0.1, 20):
        res = minimize(objective, [th0, ph0], method='Nelder-Mead',
                       options={'xatol': 1e-12, 'fatol': 1e-15, 'maxiter': 10000})
        if res.fun < best_min:
            best_min = res.fun
            best_loc = res.x

print(f"  Best minimum: {best_min:.6e}")
if best_loc is not None:
    print(f"  At θ={best_loc[0]/np.pi:.6f}π, φ={best_loc[1]/np.pi:.6f}π")
    d0, d1 = off_diag_elements(best_loc[0], best_loc[1])
    print(f"  D_off[0,0] = {d0}")
    print(f"  D_off[1,1] = {d1}")

    if best_min < 1e-20:
        print("  >>> CONSISTENT FAMILY FOUND! <<<")
    else:
        print("  >>> No exact consistency — minimum is nonzero <<<")

# ============================================================
# Section 3: Both bases free — refine with optimization
# ============================================================
print(f"\n{'='*70}")
print("SECTION 3: Full 3-time consistency (both bases free)")
print("=" * 70)

def full_decoherence_offdiag(params):
    """Total off-diagonal norm of D for 4-parameter family."""
    th1, ph1, th2, ph2 = params
    P1_a = make_projector(th1, ph1)
    P1_b = np.eye(2) - P1_a
    P2_a = make_projector(th2, ph2)
    P2_b = np.eye(2) - P2_a

    P1_list = [P1_a, P1_b]
    P2_list = [P2_a, P2_b]

    # Compute all chain operators
    chains = []
    for a1 in range(2):
        for a2 in range(2):
            C = P2_list[a2] @ U12 @ P1_list[a1] @ U1
            chains.append(C)

    # Compute D matrix and off-diagonal sum
    total = 0.0
    for i in range(4):
        for j in range(4):
            if i != j:
                D_ij = np.trace(chains[i] @ rho_0 @ chains[j].conj().T)
                total += abs(D_ij)**2
    return total

# Global optimization
print("Optimizing from 1000 random starting points...")
best_val = 1.0
best_params = None
np.random.seed(42)

for trial in range(1000):
    x0 = [np.random.uniform(0.01, np.pi-0.01),
          np.random.uniform(0, 2*np.pi),
          np.random.uniform(0.01, np.pi-0.01),
          np.random.uniform(0, 2*np.pi)]
    res = minimize(full_decoherence_offdiag, x0, method='Nelder-Mead',
                   options={'xatol': 1e-12, 'fatol': 1e-18, 'maxiter': 5000})
    if res.fun < best_val:
        best_val = res.fun
        best_params = res.x

print(f"\nBest minimum of Σ|D_off|² = {best_val:.6e}")
if best_params is not None:
    th1, ph1, th2, ph2 = best_params
    print(f"  θ₁ = {th1/np.pi:.6f}π, φ₁ = {ph1/np.pi:.6f}π")
    print(f"  θ₂ = {th2/np.pi:.6f}π, φ₂ = {ph2/np.pi:.6f}π")

    if best_val < 1e-20:
        print("  >>> CONSISTENT 3-TIME FAMILY FOUND! <<<")
    elif best_val < 1e-10:
        print("  >>> NEAR-CONSISTENT (numerical tolerance) <<<")
    else:
        print("  >>> NO consistent 3-time family exists for this system <<<")
        print("  >>> This is a standard result: most 3-time qubit histories do not decohere <<<")

# ============================================================
# Section 4: Medium decoherence (Re D_off = 0 only)
# ============================================================
print(f"\n{'='*70}")
print("SECTION 4: Medium decoherence (Re D_off = 0)")
print("=" * 70)

def medium_decoherence_offdiag(params):
    """Total |Re(D_off)|² for medium decoherence."""
    th1, ph1, th2, ph2 = params
    P1_a = make_projector(th1, ph1)
    P1_b = np.eye(2) - P1_a
    P2_a = make_projector(th2, ph2)
    P2_b = np.eye(2) - P2_a

    P1_list = [P1_a, P1_b]
    P2_list = [P2_a, P2_b]

    chains = []
    for a1 in range(2):
        for a2 in range(2):
            C = P2_list[a2] @ U12 @ P1_list[a1] @ U1
            chains.append(C)

    total = 0.0
    for i in range(4):
        for j in range(4):
            if i != j:
                D_ij = np.trace(chains[i] @ rho_0 @ chains[j].conj().T)
                total += D_ij.real**2
    return total

best_med = 1.0
best_med_params = None

for trial in range(1000):
    x0 = [np.random.uniform(0.01, np.pi-0.01),
          np.random.uniform(0, 2*np.pi),
          np.random.uniform(0.01, np.pi-0.01),
          np.random.uniform(0, 2*np.pi)]
    res = minimize(medium_decoherence_offdiag, x0, method='Nelder-Mead',
                   options={'xatol': 1e-12, 'fatol': 1e-18, 'maxiter': 5000})
    if res.fun < best_med:
        best_med = res.fun
        best_med_params = res.x

print(f"\nBest minimum of Σ|Re(D_off)|² = {best_med:.6e}")
if best_med_params is not None:
    th1, ph1, th2, ph2 = best_med_params
    print(f"  θ₁ = {th1/np.pi:.6f}π, φ₁ = {ph1/np.pi:.6f}π")
    print(f"  θ₂ = {th2/np.pi:.6f}π, φ₂ = {ph2/np.pi:.6f}π")

    if best_med < 1e-20:
        print("  >>> MEDIUM-CONSISTENT FAMILY FOUND! <<<")

        # Check what the actual off-diag looks like
        P1_a = make_projector(th1, ph1)
        P1_b = np.eye(2) - P1_a
        P2_a = make_projector(th2, ph2)
        P2_b = np.eye(2) - P2_a
        chains = []
        for a1_p in [P1_a, P1_b]:
            for a2_p in [P2_a, P2_b]:
                C = a2_p @ U12 @ a1_p @ U1
                chains.append(C)
        print("  Full D matrix (4x4):")
        for i in range(4):
            row = []
            for j in range(4):
                D_ij = np.trace(chains[i] @ rho_0 @ chains[j].conj().T)
                row.append(D_ij)
            print(f"    [{', '.join([f'{x:.4f}' for x in row])}]")
    else:
        print("  >>> No medium-consistent families found <<<")

# ============================================================
# Section 5: Analytical argument
# ============================================================
print(f"\n{'='*70}")
print("SECTION 5: Analytical argument for non-existence")
print("=" * 70)

# For a pure initial state ρ₀ = |ψ₀><ψ₀| and unitary evolution,
# the state at any time is pure: |ψ(t)> = U(t)|ψ₀>.
#
# For a single fine-grained history (a₁, a₂), the amplitude is:
# <a₂|U12|a₁><a₁|U1|ψ₀>
#
# The decoherence functional is:
# D((a₁,a₂),(a₁',a₂')) = <a₂|U12|a₁><a₁|U1|ψ₀><ψ₀|U1†|a₁'><a₁'|U12†|a₂'>
#
# For this to vanish when (a₁,a₂) ≠ (a₁',a₂'):
# We need either <a₁|U1|ψ₀> = 0 for some a₁ (impossible for our ρ₀ and U)
# or <a₂|U12|a₁> = 0 for some (a₁,a₂) pair
#
# The second condition means U12 must have a zero entry in the chosen basis.
# But U12 = [[cos(π/4), -i sin(π/4)], [-i sin(π/4), cos(π/4)]]
# which has ALL entries nonzero (= ±1/√2).
#
# So in the computational basis for t_2:
# D((a₁,0),(a₁',0)) = <0|U12|a₁><a₁|U1|ψ₀><ψ₀|U1†|a₁'><a₁'|U12†|0>
# = <0|U12|a₁> <a₁'|U12†|0>* × <a₁|U1|ψ₀> <a₁'|U1|ψ₀>*
#
# Wait, that's not right. Let me redo:
# <0|U12|a₁> is always nonzero since U12 has no zeros.
# <a₁|U1|ψ₀> is always nonzero since ψ₁ = U1|ψ₀> is a superposition of any basis.
#
# So for consistency we need:
# Σ over intermediate expressions... actually the constraint is on
# the MATRIX PRODUCT, not individual terms.

# Let me just compute the condition explicitly for arbitrary t_1 basis.

print("For pure initial state, the decoherence functional at 3 times is:")
print("  D((a₁,a₂),(a₁',a₂')) = α(a₁,a₂) α*(a₁',a₂')")
print("  where α(a₁,a₂) = <a₂|U₁₂|a₁><a₁|U₁|ψ₀>")
print("")
print("Wait — that's only for FINE-GRAINED histories. For coarse-grained:")
print("  D_CG((α₁,α₂),(α₁',α₂')) = Σ_{a₁∈α₁,a₂∈α₂} Σ_{a₁'∈α₁',a₂'∈α₂'} D_FG")
print("")
print("For our 2×2 decompositions, the histories ARE fine-grained (each bin = 1 outcome)")
print("So D((a₁,a₂),(a₁',a₂')) = α(a₁,a₂) α*(a₁',a₂')")
print("This means D = |α><α| where α is a 4-vector!")
print("=> D is RANK 1 => off-diag is NEVER zero (unless α has zero entries)")

# Verify
print("\nVerification: compute α vector for specific basis choices")

def compute_alpha(th1, ph1, th2, ph2):
    """Compute amplitude vector for fine-grained histories."""
    a_states = []
    # t_1 basis
    a1_0 = np.array([np.cos(th1/2), np.exp(1j*ph1)*np.sin(th1/2)])
    a1_1 = np.array([np.sin(th1/2), -np.exp(1j*ph1)*np.cos(th1/2)])
    # t_2 basis
    a2_0 = np.array([np.cos(th2/2), np.exp(1j*ph2)*np.sin(th2/2)])
    a2_1 = np.array([np.sin(th2/2), -np.exp(1j*ph2)*np.cos(th2/2)])

    psi0 = plus
    alpha = []
    for a1 in [a1_0, a1_1]:
        for a2 in [a2_0, a2_1]:
            amp = (a2.conj() @ U12 @ np.outer(a1, a1.conj()) @ U1 @ psi0)
            # Actually: <a2|U12|a1><a1|U1|psi0>
            amp = (a2.conj() @ U12 @ a1) * (a1.conj() @ U1 @ psi0)
            alpha.append(amp)
    return np.array(alpha)

# Check a few cases
for (th1, ph1, th2, ph2, label) in [
    (np.pi/2, 0, 0, 0, "x-basis, z-basis"),
    (0, 0, 0, 0, "z-basis, z-basis"),
    (np.pi/2, np.pi/2, 0, 0, "y-basis, z-basis"),
    (np.pi/4, np.pi/6, np.pi/3, np.pi/5, "random"),
]:
    alpha = compute_alpha(th1, ph1, th2, ph2)
    n_zeros = sum(abs(a) < 1e-10 for a in alpha)
    print(f"  {label:30s}: α = {alpha}, zeros: {n_zeros}")
    if n_zeros > 0:
        print(f"    *** Has zero entries → COULD be consistent! ***")

# When does α have zero entries?
print("\n\nSearching for bases where α has zero entries (necessary for consistency):")
print("α(a₁,a₂) = <a₂|U₁₂|a₁><a₁|U₁|ψ₀> = 0")
print("Either <a₁|U₁|ψ₀> = 0 or <a₂|U₁₂|a₁> = 0")

# Condition 1: <a₁|U₁|ψ₀> = 0 means a₁ is orthogonal to ψ₁ = U₁|ψ₀>
psi_1 = U1 @ plus
print(f"\nψ₁ = U₁|+> = {psi_1}")
# a₁ ⊥ ψ₁ means a₁ = e^(iδ) ψ₁_perp
psi_1_perp = np.array([-psi_1[1].conj(), psi_1[0].conj()])
psi_1_perp = psi_1_perp / np.linalg.norm(psi_1_perp)
print(f"ψ₁⊥ = {psi_1_perp}")
print(f"<ψ₁⊥|ψ₁> = {psi_1_perp.conj() @ psi_1:.6e} (should be 0)")

# If a₁ = ψ₁⊥, then α(ψ₁⊥, a₂) = 0 for ALL a₂
# The other basis vector a₁ = ψ₁ gives α(ψ₁, a₂) = <a₂|U₁₂|ψ₁> · 1
# (since <ψ₁|ψ₁> = 1... wait, <ψ₁|U₁|ψ₀> = <ψ₁|ψ₁> = 1)

print("\nIf t₁ basis = {ψ₁, ψ₁⊥}:")
print("  α(ψ₁⊥, a₂) = 0 for all a₂ (half the histories have zero amplitude)")
print("  α(ψ₁, a₂) = <a₂|U₁₂|ψ₁> for a₂ in t₂ basis")
print("  D becomes block-diagonal with two 0 rows/columns → automatically consistent!")

# Verify
th1_psi1 = 2 * np.arctan2(abs(psi_1[1]), abs(psi_1[0]))
ph1_psi1 = np.angle(psi_1[1]) - np.angle(psi_1[0])
print(f"\nψ₁ in Bloch coords: θ={th1_psi1:.6f} ({th1_psi1/np.pi:.4f}π), φ={ph1_psi1:.6f} ({ph1_psi1/np.pi:.4f}π)")

# Actually, let me find psi_1's Bloch angles more carefully
# psi_1 = [cos(th/2), e^(i*ph)*sin(th/2)]
# We need cos(th/2) = |psi_1[0]|*e^(i*arg(psi_1[0]))
# So th = 2*arccos(|psi_1[0]|), and we need to account for global phase
print(f"\nψ₁ = {psi_1}")
global_phase = np.angle(psi_1[0])
psi_1_normalized = psi_1 * np.exp(-1j * global_phase)
print(f"ψ₁ (global phase removed) = {psi_1_normalized}")
th_bloch = 2 * np.arccos(abs(psi_1_normalized[0]))
ph_bloch = np.angle(psi_1_normalized[1])
print(f"Bloch: θ = {th_bloch:.6f} ({th_bloch/np.pi:.4f}π), φ = {ph_bloch:.6f} ({ph_bloch/np.pi:.4f}π)")

# Now test consistency with this basis at t_1 and ANY basis at t_2
print(f"\nTesting consistency with t₁ = eigenbasis of ψ₁:")
alpha_test = compute_alpha(th_bloch, ph_bloch, 0, 0)
print(f"  α vector (t₂ = z-basis): {alpha_test}")
print(f"  Zero entries: {sum(abs(a) < 1e-10 for a in alpha_test)}")

# The D matrix should be consistent
P1_a = make_projector(th_bloch, ph_bloch)
P1_b = np.eye(2) - P1_a
P2_0 = np.array([[1,0],[0,0]], dtype=complex)
P2_1 = np.array([[0,0],[0,1]], dtype=complex)

chains = []
for P1 in [P1_a, P1_b]:
    for P2 in [P2_0, P2_1]:
        C = P2 @ U12 @ P1 @ U1
        chains.append(C)

D = np.zeros((4, 4), dtype=complex)
for i in range(4):
    for j in range(4):
        D[i, j] = np.trace(chains[i] @ rho_0 @ chains[j].conj().T)

print(f"\nD matrix:")
for i in range(4):
    row = [f"{D[i,j]:.6f}" for j in range(4)]
    print(f"  [{', '.join(row)}]")

max_offdiag = max(abs(D[i,j]) for i in range(4) for j in range(4) if i != j)
print(f"\nMax |D_off| = {max_offdiag:.6e}")
if max_offdiag < 1e-10:
    print(">>> CONSISTENT! Using ψ₁ eigenbasis at t₁ gives a consistent family <<<")

# ============================================================
# Section 6: Characterize the full consistent family space
# ============================================================
print(f"\n{'='*70}")
print("SECTION 6: Full consistent family space for 3-time histories")
print("=" * 70)

# From the analysis above:
# The only way to get D = diagonal is to have zero entries in α.
#
# Case 1: <a₁|ψ₁> = 0 for one basis element (say a₁ = ψ₁⊥)
#   → The t₁ basis must be {ψ₁, ψ₁⊥} (up to phases)
#   → This is a SINGLE POINT on the Bloch sphere (θ₁, φ₁ fixed)
#   → The t₂ basis is UNCONSTRAINED (any basis works)
#   → Family space dimension: 2 (from θ₂, φ₂)
#
# Case 2: <a₂|U₁₂|a₁> = 0 for some (a₁, a₂) pair
#   → U₁₂|a₁> ⊥ a₂
#   → a₂ = (U₁₂|a₁>)⊥
#   → For each a₁, this fixes one a₂. But we need consistency for ALL pairs.

# Let's check Case 2 more carefully.
# We need α(a₁,a₂) = 0 for enough entries that D becomes diagonal.
# Since D = |α><α| (rank 1), the ONLY way D is diagonal is if α has at most 1 nonzero entry.
# (Because if α has 2+ nonzero entries, D has off-diagonal terms.)
#
# So we need: at most 1 of the 4 amplitudes α(a₁,a₂) is nonzero.
# This means 3 of the 4 must be zero.

print("Key insight: D_FG = |α><α| (rank 1 for pure initial state)")
print("For D to be diagonal: α must have at most 1 nonzero entry")
print("(i.e., exactly 1 history has nonzero probability)")
print("")

# Enumerate cases where 3 out of 4 are zero:
# α(0,0) = <a₂⁰|U₁₂|a₁⁰> <a₁⁰|ψ₁>
# α(0,1) = <a₂¹|U₁₂|a₁⁰> <a₁⁰|ψ₁>
# α(1,0) = <a₂⁰|U₁₂|a₁¹> <a₁¹|ψ₁>
# α(1,1) = <a₂¹|U₁₂|a₁¹> <a₁¹|ψ₁>
#
# Case A: <a₁¹|ψ₁> = 0 (so α(1,0) = α(1,1) = 0)
#   Need also α(0,0) = 0 or α(0,1) = 0
#   α(0,0) = 0: <a₂⁰|U₁₂|a₁⁰> = 0 → a₂⁰ ⊥ U₁₂|a₁⁰>
#     → t₁ = {ψ₁, ψ₁⊥}, t₂ = {(U₁₂ψ₁)⊥, U₁₂ψ₁} (specific)
#   α(0,1) = 0: <a₂¹|U₁₂|a₁⁰> = 0 → a₂¹ ⊥ U₁₂|a₁⁰>
#     → Since a₂¹ = (a₂⁰)⊥, this means a₂⁰ = U₁₂ψ₁ (up to phase)
#     → t₁ = {ψ₁, ψ₁⊥}, t₂ = {U₁₂ψ₁, (U₁₂ψ₁)⊥} (specific)
#
# Case B: <a₁⁰|ψ₁> = 0 (symmetric to Case A with relabeling)
#
# Case C: <a₂⁰|U₁₂|a₁⁰> = 0 and <a₂⁰|U₁₂|a₁¹> = 0
#   → a₂⁰ ⊥ U₁₂|a₁⁰> AND a₂⁰ ⊥ U₁₂|a₁¹>
#   → a₂⁰ ⊥ span{U₁₂|a₁⁰>, U₁₂|a₁¹>} = C² → impossible (no nonzero a₂⁰)

print("Classification of consistent families (3-time, pure state):")
print("")
print("Case A: t₁ = {ψ₁, ψ₁⊥}, t₂ arbitrary")
print("  → All α(ψ₁⊥, ·) = 0. Only α(ψ₁, a₂) survives.")
print("  → D is automatically diagonal (has two zero rows/cols)")
print("  → Phase freedom: t₂ basis choice = 2 parameters (θ₂, φ₂)")
print("")
print("Case B: t₁ = {ψ₁, ψ₁⊥}, t₂ = {ψ₂, ψ₂⊥} where ψ₂ = U₁₂ψ₁")
print("  → This is a SPECIFIC case of Case A")
print("  → Only α(ψ₁, ψ₂) ≠ 0, which = <ψ₂|ψ₂><ψ₁|ψ₁> = 1")
print("  → Single deterministic history with probability 1")
print("")
print("Case C: t₁ ≠ {ψ₁, ψ₁⊥}")
print("  → Both <a₁⁰|ψ₁> ≠ 0 and <a₁¹|ψ₁> ≠ 0")
print("  → Need <a₂|U₁₂|a₁> = 0 for 3 pairs → requires a₂⁰ ⊥ all of C² → impossible")
print("  → NO consistent family with t₁ ≠ eigenbasis of ψ₁")

# Wait — I need to reconsider. The D matrix for fine-grained histories is rank-1,
# which is always consistent IF we treat it as already fine-grained. But the
# COARSE-GRAINED D matrix for the binary decomposition might differ.

# Actually, for projective decomposition into orthogonal projectors,
# the fine-grained and coarse-grained are the same thing (each projector = one history).
# So D = |α><α| and for it to be diagonal we need α to have at most 1 nonzero entry.

# But wait — there's a subtlety. A "consistent family" in CH doesn't require
# D to be fully diagonal. It requires D to be diagonal for each SAMPLE SPACE.
# If we have a Boolean algebra of histories, some coarsenings might be consistent
# even if the fine-grained decomposition isn't.

# For 3 times with binary decomposition at each, the finest grain is 4 histories.
# Coarser families could group these. But for our qubit case with rank-1 projectors,
# the standard requirement is that the fine-grained D be diagonal.

# Let me verify: with t₁ = ψ₁ eigenbasis and t₂ arbitrary, is D truly diagonal?
# We showed α(ψ₁⊥, a₂) = 0 for all a₂.
# So α = (α(ψ₁, a₂⁰), α(ψ₁, a₂¹), 0, 0)
# D = |α><α| has D_{00} = |α₀|², D_{01} = α₀ α₁*, D_{11} = |α₁|², others 0
# But D_{01} = α₀ α₁* is generally NONZERO!
# So D is NOT diagonal! Only the lower-right block is zero.

# I made an error. Let me reconsider.

print(f"\n{'='*70}")
print("CORRECTION: Re-examining D diagonality")
print("=" * 70)

print("\nWith t₁ = {ψ₁, ψ₁⊥}:")
print("  α = (<a₂⁰|U₁₂|ψ₁>, <a₂¹|U₁₂|ψ₁>, 0, 0)")
print("  D₀₁ = α₀ α₁* = <a₂⁰|U₁₂|ψ₁> · <ψ₁|U₁₂†|a₂¹> ≠ 0 in general!")
print("  So D is NOT diagonal unless α has only 1 nonzero entry!")
print("")
print("  To get α₀ or α₁ = 0:")
print("  α₀ = 0: a₂⁰ ⊥ U₁₂ψ₁ → a₂⁰ = (U₁₂ψ₁)⊥ → t₂ = {(U₁₂ψ₁)⊥, U₁₂ψ₁}")
print("  α₁ = 0: a₂¹ ⊥ U₁₂ψ₁ → a₂¹ = (U₁₂ψ₁)⊥ → t₂ = {U₁₂ψ₁, (U₁₂ψ₁)⊥}")
print("  Both give the same basis: t₂ = {U₁₂ψ₁, (U₁₂ψ₁)⊥} = eigenbasis of ψ₂")

# So the ONLY consistent family has:
# t₁ = eigenbasis of ψ₁
# t₂ = eigenbasis of ψ₂
# This is a DISCRETE CHOICE (0 continuous parameters)!

# Wait, no. Let me reconsider coarser-grained histories.
# Actually, we don't need FULL diagonality. In CH, we need:
# D(α, α') = 0 for histories α ≠ α' in the SAME SAMPLE SPACE.
# If we only have a 2-outcome decomposition at t₁ (and similarly at t₂),
# the sample space has 4 elements. Consistency requires all off-diagonal = 0.

# Alternative: we could consider a COARSER family that groups histories.
# E.g., only observe at t₁ (not t₂), giving a 2-element sample space.
# Or only observe at t₂. These are automatically consistent as shown in Part C.

# But for the FULL 3-time family with binary decomposition at both times:
# Only 1 consistent family exists (up to relabeling) = eigenbases of evolved state.

print(f"\n*** REVISED CONCLUSION ***")
print(f"For 3-time histories with fine-grained projective decomposition at t₁ and t₂:")
print(f"  Exactly ONE consistent family exists:")
print(f"  t₁ basis = {{ψ₁, ψ₁⊥}} = eigenbasis of evolved state at t₁")
print(f"  t₂ basis = {{ψ₂, ψ₂⊥}} = eigenbasis of evolved state at t₂")
print(f"  Continuous parameter count: 0 (DISCRETE)")

# Verify this claim numerically
psi_2 = U12 @ psi_1
print(f"\nψ₂ = U₁₂ψ₁ = {psi_2}")

# Get Bloch angles for psi_2
gp2 = np.angle(psi_2[0])
psi_2_norm = psi_2 * np.exp(-1j * gp2)
th2_bloch = 2 * np.arccos(np.clip(abs(psi_2_norm[0]), 0, 1))
ph2_bloch = np.angle(psi_2_norm[1])
print(f"ψ₂ Bloch: θ = {th2_bloch:.6f} ({th2_bloch/np.pi:.4f}π), φ = {ph2_bloch:.6f} ({ph2_bloch/np.pi:.4f}π)")

alpha_exact = compute_alpha(th_bloch, ph_bloch, th2_bloch, ph2_bloch)
print(f"\nα vector for exact eigenbases: {alpha_exact}")
print(f"Zero entries: {sum(abs(a) < 1e-10 for a in alpha_exact)}")
print(f"Nonzero entries: {sum(abs(a) > 1e-10 for a in alpha_exact)}")

# Build and check D
P1_a = make_projector(th_bloch, ph_bloch)
P1_b = np.eye(2) - P1_a
P2_a = make_projector(th2_bloch, ph2_bloch)
P2_b = np.eye(2) - P2_a
chains_exact = []
for P1 in [P1_a, P1_b]:
    for P2 in [P2_a, P2_b]:
        C = P2 @ U12 @ P1 @ U1
        chains_exact.append(C)

D_exact = np.zeros((4, 4), dtype=complex)
for i in range(4):
    for j in range(4):
        D_exact[i, j] = np.trace(chains_exact[i] @ rho_0 @ chains_exact[j].conj().T)

print(f"\nD matrix for eigenbasis family:")
for i in range(4):
    row = [f"{D_exact[i,j]:.8f}" for j in range(4)]
    print(f"  [{', '.join(row)}]")

max_off = max(abs(D_exact[i,j]) for i in range(4) for j in range(4) if i != j)
print(f"\nMax |D_off| = {max_off:.6e}")
print(f"Consistent? {max_off < 1e-10}")

# Also check: what if we allow RELABELING (different assignment of ψ₁ to 0 or 1)?
# The other family has t₁ = {ψ₁⊥, ψ₁} (swapped). But this gives the same
# projectors, so it's the same family.

# What about the trivial families (only observe at t₁ OR only at t₂)?
print(f"\n{'='*70}")
print("ADDITIONAL: Trivial families (single-time observation)")
print("=" * 70)
print("  Observe only at t₁: any basis works → 2-parameter family")
print("  Observe only at t₂: any basis works → 2-parameter family")
print("  Observe at neither: trivial → 0 parameters")
print("  Observe at both (fine-grained): exactly 1 choice → 0 parameters")

print(f"\n{'='*70}")
print("CONSISTENT FAMILY SPACE SUMMARY (3-time qubit)")
print("=" * 70)
print("  Discrete families: 1 (eigenbasis of ψ at each time)")
print("  If we include trivial/partial families:")
print("    - Observe at t₁ only: S² of bases (2 parameters)")
print("    - Observe at t₂ only: S² of bases (2 parameters)")
print("    - Observe at both: 1 discrete choice (0 parameters)")
print("    - Observe at neither: 1 (trivial)")
print("  Total counting ambiguity depends on what we count as a 'family'")
