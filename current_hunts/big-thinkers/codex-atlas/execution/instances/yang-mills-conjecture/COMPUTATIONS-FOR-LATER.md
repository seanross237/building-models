# Computation Registry

Computations identified during explorations that would significantly advance the mission. Maintained by the strategizer, read by the missionary and future strategizers.

## From Strategy 001, Explorations 001-003 (Phase 1)

### C1: Prove single-link theorem algebraically
- **What**: Prove that for Q differing from I on exactly one edge, λ_max(M(Q)) = 16 and P^T R(Q) P ≤_psd 0
- **Why**: This is the single-link special case of Conjecture 1, verified for 640 configs with max_eig exactly 0
- **What it resolves**: Extends known special cases. May provide the base case for an inductive proof.
- **Source**: Exploration 001 (maximal tree gauge)
- **Difficulty**: MODERATE — use Fourier decomposition of M(I) and color-uniform density P_e P_e^T = (9/64) I_3
- **Key equations**: Σ_{□∋e0} P^T [M_□(e0=U) − M_□(e0=I)] P ≤_psd 0 for all U ∈ SU(2)

### C2: Prove cube-face inequality for general Q
- **What**: Prove Σ_{μ<ν} |B_{(x,μ,ν)}(Q,v_stag)|² ≤ 64 for all vertices x, all Q
- **Why**: Zero violations in 160,000 tests. Would directly prove Conjecture 1 since there are 16 vertices × 64 = 1024.
- **What it resolves**: The full conjecture if proved for all Q
- **Source**: Exploration 002 (per-plaquette structure)
- **Difficulty**: HIGH — proved for cross-links=I case, general case open
- **Key equations**: Σ|B|² = 32 + 8⟨n,W⟩ − |A|² where W = Σ w_μ, A = Σ s_μ w_μ (for simplified case)

### C3: Prove active/inactive pairing gives global bound
- **What**: Show the parallelogram identity |B_active|² + |B_inactive|² ≤ 16 can be used with a canonical lattice pairing to get Σ ≤ 1024
- **Why**: The parallelogram identity is algebraically exact; the gap is showing the pairing covers all plaquettes
- **What it resolves**: The full conjecture if the pairing is proved to exist
- **Source**: Exploration 003 (SO(3) representation theory)
- **Difficulty**: MODERATE — need lattice combinatorics argument

### C4: Derive d²f/dt² = −26 analytically at Q=I
- **What**: Compute the Hessian curvature of f(Q) = Σ|B_□(Q,v_stag)|² at Q=I in direction of perpendicular rotation
- **Why**: Would give the local curvature at the conjectured maximum — useful for a local-to-global argument
- **Source**: Exploration 003
- **Difficulty**: LOW — explicit calculation using Ad(exp(tA)) expansion

## From Strategy 003, Exploration 001 (Phase 0)

### C5: Derive curvature correction C(Q) analytically
- **What**: Compute the explicit formula for HessS(Q) − (β/2N)M(Q), where HessS is the Hessian of the Wilson action S(Q) = −(β/N) Σ Re Tr(U_□)
- **Why**: E001 showed HessS ≠ (β/2N)M — there's a large curvature correction that suppresses M's eigenvalues. The diagonal blocks are HessS_{ee} = (β/4N) Σ_{□∋e} Re Tr(U_□) × I₃, but the full off-diagonal structure involves Im Tr(σ_a U_□). Need the explicit formula.
- **What it resolves**: Understanding C(Q) is the prerequisite for proving the revised conjecture λ_max(HessS) ≤ (β/2N)×4d
- **Source**: Strategy 003 Exploration 001
- **Difficulty**: MODERATE — standard lattice gauge theory calculation but with careful bookkeeping of adjoint representation
- **Key equations**: S(Q) = −(β/N) Σ_□ Re Tr(U_□), perturb Q_e → Q_e exp(εA), compute d²S/dε² to get HessS_{ee'} block by block

### C6: Numerical survey of λ_max(HessS) across 500+ configurations
- **What**: Compute the full 192×192 Hessian by finite differences for 500+ configs (random, adversarial, flat connections, near-saddle points)
- **Why**: E001 verified λ_max(HessS) ≤ (β/2N)×16 at Q=I, Q=iσ₃, and a few random configs. Need systematic survey.
- **What it resolves**: Confirms or falsifies the revised conjecture
- **Source**: Strategy 003 Exploration 001
- **Difficulty**: HIGH (computationally) — finite-difference Hessian is 43.7s per config, so 500 configs ≈ 6 hours. May need analytical formula from C5 instead.

### C7: Prove λ_max(HessS) ≤ (β/2N)×4d
- **What**: Prove the revised conjecture, using the analytical formula for HessS
- **Why**: This directly gives the mass gap at β < 1/4 via SZZ
- **What it resolves**: The Yang-Mills mass gap conjecture for lattice SU(2)
- **Source**: Strategy 003 Exploration 001
- **Difficulty**: UNKNOWN — depends on the structure of C(Q). May be straightforward if C(Q) has good positivity properties.

