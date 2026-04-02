# Exploration 001: Counterexample Verification + SZZ Framework Clarification

## Mission Context

We are investigating Conjecture 1 for lattice SU(2) Yang-Mills: **λ_max(M(Q)) ≤ 4d = 16 for all Q ∈ SU(2)^E** on the d=4 hypercubic torus.

Over 15 prior explorations (Strategies 001 + 002), we proved:
- **Per-vertex staggered bound**: F_x(Q, T) ≤ 16||T||² for ALL staggered modes T with ΣT_μ = 0 — PROVED
- **Single-link theorem**: Changing one link leaves λ_max = 16 — COMPUTED (640 configs)
- **H_norm ≤ 1/8** rigorous bound (mass gap at β < 1/6)

However, Strategy 002 Exploration 007 (E007) ran gradient ascent on the full spectrum and found **λ_max(M(Q)) ≈ 16.08** — potentially falsifying the conjecture. But E007 may have used the **wrong B-field formula** (fundamental representation Q·v instead of adjoint Ad_Q(v) = QvQ⁻¹).

Your job: resolve this definitively.

## The Correct Formulas

### B-field (from MISSION.md, verified in Strategy 001)

For a plaquette □ with oriented edges (e₁, e₂, e₃, e₄) traversed in order:

B_□(Q, v) = v_{e₁} + Ad_{Q_{e₁}}(v_{e₂}) − Ad_{Q_{e₁}Q_{e₂}Q_{e₃}⁻¹}(v_{e₃}) − Ad_{U_□}(v_{e₄})

where:
- U_□ = Q_{e₁} Q_{e₂} Q_{e₃}⁻¹ Q_{e₄}⁻¹ is the holonomy around the plaquette
- Backward edges include their OWN link in the partial holonomy
- v_{eᵢ} ∈ ℝ³ (the su(2) ≅ ℝ³ component at edge eᵢ)

### Adjoint Representation (CRITICAL)

Ad_Q(v) = QvQ⁻¹ where Q ∈ SU(2) acts on v ∈ su(2) ≅ ℝ³.

In matrix form: [Ad_Q]_{ij} = (1/2) Tr(σ_i Q σ_j Q⁻¹) where σ_i are Pauli matrices.

This gives a **3×3 SO(3) matrix** for each Q ∈ SU(2).

**THIS IS NOT** the fundamental representation Q·v (which would be 2×2). If you implement Q·v instead of QvQ⁻¹, you get wrong eigenvalues.

### M(Q) operator

M(Q) is the (3|E|) × (3|E|) matrix defined by:

v^T M(Q) v = Σ_□ |B_□(Q, v)|²

For L=2, d=4: |E| = 64 edges, so M(Q) is 192×192. There are 96 plaquettes.

### Convention

We use SZZ convention: S(Q) = −(β/N) Σ_□ Re Tr(U_□), with N=2.

The Hessian of S satisfies HessS(v,v; Q) = (β/2N) · v^T M(Q) v. So bounding λ_max(M(Q)) ≤ 16 is equivalent to H_norm = sup_Q (β · λ_max(M(Q))) / (2N · 4d) ≤ β/12. The mass gap threshold is β < 1/(4 · H_norm_max) = 1/4 if λ_max(M(Q)) ≤ 16.

## Your Tasks

### Stage 0: Sanity Check (MUST PASS before proceeding)

Implement the B-field formula and M(Q) construction for L=2, d=4, SU(2).

**Validation at Q = I** (all links = identity):
- Expected: λ_max(M(I)) = 16 with multiplicity 9 (the staggered modes)
- Expected: Next eigenvalue = 12 (from momentum modes with 3 π-components)
- Expected: Total size 192×192, with rank considerations from gauge orbits

If λ_max(M(I)) ≠ 16 exactly (to machine precision), your implementation is WRONG. Stop and fix before proceeding.

**Validation via finite differences:**
Pick 3 random Q configurations. For each:
1. Compute v^T M(Q) v directly from your B-field formula
2. Compute the same quantity by finite differences: perturb Q along a link by exp(εA), compute S(Q'), take d²S/dε²
3. These must agree to relative error < 10⁻⁶

### Stage 1: Reproduce and Verify E007's Counterexample

Run edge-by-edge gradient ascent to maximize λ_max(M(Q)):
1. Start from 20 independent random SU(2)^E configurations
2. For each edge e, optimize Q_e ∈ SU(2) to maximize λ_max(M(Q)) while holding all other links fixed
3. Cycle through all edges repeatedly until convergence (change < 10⁻⁸ per cycle)
4. Record the maximum λ_max found across all 20 trials

**Critical question:** Does λ_max ever exceed 16?

If YES (λ_max > 16 + 10⁻⁶):
- Save the exact configuration Q* (all link matrices)
- Compute B_□(Q*, v*) term by term for the maximizing eigenvector v*
- Verify v^T M(Q*) v / |v|² > 16 by direct B-field computation (not just eigenvalue)
- Check: is v* predominantly staggered or non-staggered?
- Report the exact value and the configuration

If NO (λ_max ≤ 16 + 10⁻⁶ for all trials):
- Report the maximum found
- Try also: start 5 trials from near-identity configurations (Q_e = exp(εA) with ε ~ 0.3)
- Try also: start 5 trials from "adversarial" initializations: set half the links to random SU(2) elements

### Stage 2: SZZ Framework Verification

The library indicates HessS(v,v; Q) = (β/2N) · v^T M(Q) v. Verify this numerically:
1. Pick a random Q and random v
2. Compute HessS(v,v; Q) by finite differences of the Wilson action S(Q)
3. Compute (β/2N) · v^T M(Q) v using your M(Q) implementation
4. These must match (β = 1.0 for testing)

If they match: the conjecture λ_max(M(Q)) ≤ 16 is EXACTLY what SZZ needs.
If they don't: there IS a curvature correction. Compute it, characterize it.

### Stage 3: Characterize the Eigenvalue Landscape

For the 20 converged configurations from Stage 1:
- Report λ_max for each
- Decompose the top eigenvector into staggered vs non-staggered components
- Report the max non-staggered eigenvalue separately
- Create a histogram or table of results

### Stage 4: Verdict

State clearly:
1. Is the E007 counterexample (λ_max ≈ 16.08) confirmed or refuted?
2. Does HessS = (β/2N) · v^T M(Q) v (no curvature correction)?
3. What is the empirical sup λ_max(M(Q)) from your gradient ascent? (with error bars)
4. Is Conjecture 1 (λ_max(M(Q)) ≤ 16) consistent with your numerical evidence?
5. What is the correct proof target for the mass gap argument?

## Success Criteria

- Stage 0 passes (Q=I gives λ_max = 16, finite-difference validation)
- Clear YES/NO on whether λ_max > 16 is achievable
- If yes: verified counterexample with saved configuration
- If no: report on maximum achieved with sufficient trials (≥ 20)
- HessS vs M(Q) relationship numerically verified

## Failure Criteria

- Stage 0 fails and cannot be fixed → formula implementation error, report it
- Ambiguous results (λ_max ≈ 16 ± 10⁻³ without clear resolution) → report the ambiguity

## Output

Write your findings to REPORT.md (≤ 250 lines) and a concise REPORT-SUMMARY.md (≤ 30 lines) in your exploration directory. Write incrementally — update REPORT.md after each stage.
