# Exploration History

## Exploration 001: Maximal Tree Gauge Decomposition

**Outcome:** Key single-link theorem discovered, but tree gauge alone not sufficient for full proof.

Key findings:
- **Single-link theorem [COMPUTED]**: Changing ANY one link to arbitrary U ∈ SU(2) leaves λ_max = 16 exactly. P^T R(Q) P is negative semidefinite (max_eig = 0) with 3D null space. Tested for all 64 edges × 10 trials = 640 tests.
- **Color-uniform density [COMPUTED]**: P_e P_e^T = (9/64) I_3 for ALL 64 edges — uniform density of staggered eigenspace.
- **Two-link perturbations**: strictly negative (max_eig ∈ [-0.02, -0.11]).
- **Gradient ascent**: best max_eig = -6.61, nowhere near 0.
- **Per-plaquette Tr(P^T R_□ P) < 0** for all 96 plaquettes in all tested configs.
- Tractability: NOT YET TRACTABLE via tree gauge alone. No inductive structure from single-link to multi-link.

## Exploration 002: Per-Plaquette Contribution Structure

**Outcome:** Partial success — cube-face grouping identified with zero violations in 160K tests. Algebraic proof for simplified case.

Key findings:
- **Active/inactive split [PROVED]**: Active plaquettes (μ+ν odd) have f_□ ≤ 0 always (triangle inequality). Inactive (μ+ν even) have f_□ ≥ 0 always (trivially, since |B_I|²=0).
- **Cube-face grouping [COMPUTED]**: Σ_{μ<ν} f_{(x,μ,ν)} ≤ 0 for ALL x, ALL Q — zero violations in 160,000 tests (10K configs × 16 vertices). Adversarial gradient ascent converges to Q=I.
- **Algebraic formula [PROVED for cross-links=I]**: Σ|B|² = 32 + 8⟨n,W⟩ − |A|² ≤ 64, where W = Σ w_μ and A = Σ s_μ w_μ. The staggered cancellation A → 0 at Q=I is the mechanism.
- **Proof gap**: Need to generalize cube-face inequality to arbitrary cross-links.
- **Key mechanism**: The staggered sign structure forces A = Σ s_μ w_μ → 0 at Q=I (since Σ s_μ = 0), making Q=I the global maximum.

## Exploration 003: SU(2)/SO(3) Representation Theory Bound

**Outcome:** Inconclusive — strong numerical evidence, parallelogram identity discovered, but no proof of global bound.

Key findings:
- **Parallelogram identity [VERIFIED]**: |B_active|² + |B_inactive|² = 2|n+R₂n|² + 2|R₁n+R₃n|² ≤ 16 for paired plaquettes with same R_k.
- **Per-plaquette constrained max = 16 [COMPUTED]**: Holonomy constraint does NOT reduce per-plaquette maximum.
- **Zero violations [COMPUTED]**: Over 5000+ configs, max sum ≈ 481 << 1024. Q=I value is 1024, ~2.5× the random mean.
- **Constant-link proved [VERIFIED]**: Sum = 512(1+cosθ) ≤ 1024 analytically.
- **Per-edge Hessian at Q=I**: d²f/dt² = -26 for perpendicular axes — clean formula.
- **Proof gap**: Cannot prove pairing argument for general Q. Need lattice structure analysis to show canonical active/inactive pairing exists.




## Exploration 004: Synthesis and Proof Design

**Outcome:** Successful synthesis — entire proof reduced to single lemma.

Key findings:
- **Best route: Cube-face inequality (Route A)**. 96 plaquettes partition into 16 groups of 6 (per vertex). If each satisfies F_x = Σ_{μ<ν} |B_{(x,μ,ν)}|² ≤ 64, then total ≤ 1024 = 4d|v|².
- **Lemma 5 (the single hardest step)**: F_x ≤ 64 for all vertices x, all Q. Proved for cross-links=I. Zero violations in 160K tests for general Q.
- **Route B (parallelogram pairing) BLOCKED**: No natural pairing of active/inactive plaquettes exists generically.
- **Route C (single-link induction) BLOCKED**: No inductive structure.
- **Cross-links only help**: Max F_x for general Q is 48.3, far below 64 (cross-links=I max). Suggests monotonicity.
- **Priority attack**: Symbolic expansion of F_x for general Q (50-100 line sympy). Could complete the proof or identify precise obstruction.
- The mechanism: staggered sign structure forces A = Σ s_μ w_μ → 0 at Q=I since Σ s_μ = 0.

## Exploration 005: Proof Attempt — Cube-Face Inequality (PARTIAL — timed out)

**Outcome:** Partial — timed out after Stage 2 (Stage 3 proof attempts not completed). KEY reformulation discovered.

Key findings:
- **F_x = n^T M_total n [VERIFIED]**: F_x is a quadratic form in direction n, where M_total is a 3×3 PSD matrix. The bound F_x ≤ 64 is EQUIVALENT to λ_max(M_total) ≤ 64.
- **Cross-link monotonicity FAILS [COMPUTED]**: Cross-links can INCREASE F_x by up to +28 for fixed base links. Approach A is DEAD. Inactive plaquettes are the main source.
- **λ_max saturation [COMPUTED]**: Over 10K random configs, max λ_max = 56.9 (below 64). Adversarial gradient ascent on λ_max: ALL 30 trials converge to exactly 64.000000.
- **At adversarial maxima**: eigenvalues = [small, medium, 64.000]. Top eigenvalue saturates at 64 while others vary.
- **Tr(M_total)**: ranges 40-128 (random), max 192 at Q=I. Trace bound too weak (192/3 = 64 only works if M ∝ I).
- **M_total formula**: M_total = Σ_{μ<ν} A_{μν}^T A_{μν} where A = aS + bT with S = I + R_μ D, T = R_μ + R_μ D R_ν^T.
- **Proof approaches A (monotonicity), B (general formula), C (gauge fixing) not attempted** — explorer stalled in thinking mode.

## Exploration 006: Prove λ_max(M_total) ≤ 64 — PROOF COMPLETE

**Outcome:** SUCCESS — Complete proof with numerical verification at every step.

### The Proof (5 steps):

1. **Trace identity [VERIFIED]**: Decompose M = cI + P. Then c + Tr(P) = 24 + 2×20 = 64 identically (independent of all rotation parameters). Comes from sign structure: 28 positive, 8 negative cross-terms.

2. **Equivalence [VERIFIED]**: λ_max(M) ≤ 64 ⟺ λ_max(P) ≤ Tr(P)

3. **Expansion [VERIFIED]**: Define f(R) = 1 − n^T R n ≥ 0 for R ∈ SO(3). Then:
   64I − M = 2 × [group_02 + group_13 + group_active]
   where group_02 = f(R₀)+f(R₂)+f(R₀D₀₂)+f(D₀₂R₂^T)−f(D₀₂)−f(R₀D₀₂R₂^T)
   (similar for group_13; group_active = sum of 16 non-negative f-terms)
   Error < 4×10⁻¹⁴ over 100K configs.

4. **Combined Bound Lemma (HEART OF PROOF) [VERIFIED]**:
   f(A)+f(B)+f(AD)+f(DB^T)−f(D)−f(ADB^T) ≥ 0

   **Proof**: Algebraic factorization identity:
   LHS = n^T(I−A)D(I−B^T)n + f(A) + f(B)

   By Cauchy-Schwarz: |cross term| ≤ 2√(f(A)f(B))
   By AM-GM: f(A)+f(B)−2√(f(A)f(B)) = (√f(A)−√f(B))² ≥ 0

   Verified: error < 3×10⁻¹⁵ over 100K tests. Cauchy-Schwarz tight at ratio = 1.000.

5. **Assembly [VERIFIED]**: All three groups ≥ 0, so 64I − M ≥ 0, i.e., λ_max(M_total) ≤ 64. ∎
   100K configs: min(group_02) = 0.000220, min(group_13) = 0.000628, min(group_active) = 2.741.

### Implications:
- This completes the proof of Conjecture 1: λ_max(M(Q)) ≤ 16 for all Q ∈ SU(2)^E
- Implies H_norm ≤ 1/12 for all Q, giving mass gap at β < 1/4 (12× improvement over SZZ 2023)
- Proof works for all lattice sizes L ≥ 2 (unconstrained optimization over SO(3)^{10})

### Unexpected findings:
- Subadditivity f(AB) ≤ f(A)+f(B) FAILS for SO(3) (ratio up to 1.97)
- The proof uses a DEEPER structure: algebraic factorization + Cauchy-Schwarz + AM-GM
- The "Three Unit Vectors Lemma" f(AB) ≤ 4f(A)+4f(B) suffices for D=I but not general D

## Exploration 007: Adversarial Review of Proof — CONDITIONAL PASS

**Outcome:** Core proof verified correct. Two gaps identified.

### Verdict: CONDITIONAL PASS

**Core proof: CORRECT.** All 5 algebraic steps independently verified:
- Sign structure 28+/8- (net 20) ✓ [VERIFIED independently]
- Trace identity c+Tr(P) = 64 ✓ [VERIFIED]
- Expansion 64I−M = 2×[groups] (error < 4.3×10⁻¹⁴) ✓ [VERIFIED]
- Combined Bound Lemma: factorization (error < 2.7×10⁻¹⁵), Cauchy-Schwarz (ratio < 1.0), AM-GM ✓ [VERIFIED]
- Assembly (100K configs, 0 violations) ✓ [VERIFIED]

### Gap 1 (MODERATE): Full Matrix vs. Staggered Mode

The proof establishes n^T M_total n ≤ 64|n|² for fixed color n, covering only 3 of 9 dimensions of P. The other 6 eigenvectors of P (non-uniform-color staggered modes) are NOT covered by the cube-face argument. Numerically: 0 violations in 200 tests. Need separate proof or reduction.

### Gap 2 (MINOR): Odd L Sign Structures

The M_total formula A = a(I+RD)+b(R+RDR^T) is valid for EVEN L only. On L=3, boundary vertices have different sign structures (max formula discrepancy 31.8). Proof valid for even L. Odd L needs variant.

### Verification Scorecard:
- 13 VERIFIED (machine-checked)
- 5 COMPUTED (numerically, 0 violations)
- 1 CONJECTURED (full matrix reduction)

### Key Recommendation:
Close Gap 1 by proving that the full 9D eigenspace P reduces to the 3D staggered subspace for the purpose of bounding λ_max. At Q=I, staggered modes are IN P. The spectral gap (16 vs 14) provides a 2-unit buffer.

## Exploration 008: Close Gap 1 — Full Eigenspace Bound

**Outcome:** PARTIAL SUCCESS — bound holds numerically (0 violations, 110K+ tests) but no algebraic proof.

Key findings:
- **Per-vertex 12×12 formulation [VERIFIED]**: F_x for general modes is a quadratic form in a d×3 = 12-dim matrix T, restricted to V = {T : Σ_μ T_μ = 0} (9-dim constraint space).
- **0 violations [COMPUTED]**: 110K+ random configs, 350+ adversarial gradient ascent trials. Best adversarial: λ_max = 15.997 (below 16).
- **Gap decomposition [VERIFIED]**: 16‖T‖² − F_x = f_same + cross, where f_same ≥ 0 always. Harmful cross < 8.2% of f_same.
- **Maximizing T NOT always rank-1 [COMPUTED]**: Min rank-1 fraction = 0.56 at adversarial maxima. No simple reduction to uniform-color case.
- **E006 trace identity FAILS [COMPUTED]** for general spatial patterns. Proof cannot use trace arguments.
- **Constraint Σ_μ T_μ = 0 is ESSENTIAL [COMPUTED]**: Without it, eigenvalue reaches ~21.
- **Algebraic proof not achieved**: E006's combined bound lemma doesn't directly generalize due to cross-color coupling.

### Status of the Proof:
- **PROVED**: λ_max of uniform-color staggered Rayleigh quotient ≤ 16 for all Q (even L)
- **NUMERICALLY VERIFIED**: Full λ_max(M(Q)) ≤ 16 (110K+ tests, 0 violations)
- **OPEN**: Algebraic proof for general modes in the 9D eigenspace

