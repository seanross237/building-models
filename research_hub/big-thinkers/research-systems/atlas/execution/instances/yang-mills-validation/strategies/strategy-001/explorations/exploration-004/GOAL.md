# Exploration 004: Large Lattice Verification of H_norm ≤ 1/12

## Mission Context

A research program proved mass gap for lattice SU(2) Yang-Mills at β < 1/6 and conjectured β < 1/4 (Conjecture 1: H_norm ≤ 1/12 for all Q). All prior numerical evidence is from L=2 and L=4 lattices (small). This exploration tests the conjecture on LARGER lattices.

## CRITICAL CONVENTION WARNING

**You MUST use the LEFT perturbation B_□ formula:**
```
P1 = I
P2 = Q1
P3 = Q1 @ Q2 @ Q3.conj().T           # INCLUDES Q3 inverse
P4 = Q1 @ Q2 @ Q3.conj().T @ Q4.conj().T  # = U_plaq (full holonomy)
```

Do NOT use P3 = Q1 @ Q2 (without Q3†) — this gives WRONG eigenvalues at Q ≠ I. This was the critical finding from Phase 1.

**Convention:**
- Action: S(Q) = −(β/N) Σ Re Tr(U_□), N=2
- Inner product: |A|² = −2Tr(A²)
- Sanity check: λ_max = 4β at Q=I

## Goal

Test whether H_norm ≤ 1/12 holds on lattices L=4, L=6, and L=8 (if tractable), using the correct LEFT B_□ formula.

## Tasks

### Task 1: L=4 Verification
L=4, d=4: 256 sites, 1024 links, 3072 DOFs. The full Hessian is 3072×3072 — too large for dense eigendecomposition but tractable with sparse methods.

1. Implement the Hessian as a sparse matrix or use power iteration / scipy.sparse.linalg.eigsh to find λ_max
2. Sanity check: λ_max = 4β at Q=I
3. Test 20 configurations:
   - 5 random Haar
   - 5 Gibbs at β=0.1 (use Metropolis: propose Q_e → random SU(2), accept with min(1, exp(-ΔS)))
   - 5 near-identity (Q_e = exp(ε·random su(2)) with ε=0.1)
   - 5 adversarial gradient ascent (start from random Q, compute ∂λ_max/∂Q, step in the gradient direction; use implicit differentiation: ∂λ_max/∂Q_e ∝ (v_max)^T (∂M/∂Q_e) (v_max))
4. Report max H_norm observed and whether any violation of 1/12

### Task 2: L=6 or L=8 (if tractable)
L=6: 1296 sites, 5184 links, 15552 DOFs. Full matrix won't fit in memory.
L=8: 4096 sites, 16384 links, 49152 DOFs.

Use ARPACK (scipy.sparse.linalg.eigsh with k=1, which='LM') to find just λ_max.

The Hessian-vector product M(Q)v can be computed without forming the full matrix:
```python
def hessian_matvec(v, U, plaq_list, beta, N, n_links, n_gen):
    """Compute H @ v without forming H."""
    result = np.zeros_like(v)
    prefactor = beta / (2 * N)
    v_by_link = v.reshape(n_links, n_gen)
    for plaq in plaq_list:
        # Compute B_□ · v for this plaquette
        # Then add back B_□^T · B_□ · v contribution
        ...
    return result
```
Use this with scipy.sparse.linalg.LinearOperator + eigsh.

Test at least 10 configurations on L=6 (or L=8). Focus on: Haar random, Gibbs at β=0.1, and adversarial.

### Task 3: Adversarial Gradient Ascent on λ_max

The prior mission found gradient ascent from random starts only reaches H_norm ≈ 0.063. Try harder:

1. Use the correct LEFT formula
2. Start from STRUCTURED configurations (not just random):
   - Q_e = exp(ε·τ₃) for various ε (aligned links)
   - Q_e = random rotation around a FIXED axis
   - Q_e = alternating pattern: odd sites get U, even sites get V
3. Run gradient ascent for at least 500 steps with adaptive step size
4. Report the maximum H_norm achieved and the structure of the maximizing configuration

### Task 4: Center Element Configurations
Specifically test configurations where all links are a center-adjacent element:
- U_all = exp((π/4)τ₁): halfway to the center
- U_all = exp((π/2)τ₁) = iσ₁
- U_all = iσ₃ (the Phase 1 test case — should give H_norm = 1/12 exactly)
- U_all = exp(θ·τ₁) for θ = 0.1, 0.5, 1.0, 1.5, 2.0, π

## Success Criteria
- [ ] L=4 sanity check passes (λ_max = 4β at Q=I)
- [ ] 20+ configurations tested on L=4 with correct LEFT formula
- [ ] At least 10 configurations on L≥6
- [ ] Adversarial gradient ascent from structured starts
- [ ] Clear table: max H_norm by config type and lattice size
- [ ] Any violation of H_norm ≤ 1/12 → STOP and characterize immediately

## Failure Criteria
- Convention error → STOP (check λ_max = 4β at Q=I first)
- Memory issues → reduce to L=4 or use matrix-free eigsh
- If H_norm > 1/12 is found → this is the MOST IMPORTANT FINDING, report immediately

## What to Write
Write REPORT.md and REPORT-SUMMARY.md. Put all code in code/ subdirectory. Every table entry must have reproducible code.
