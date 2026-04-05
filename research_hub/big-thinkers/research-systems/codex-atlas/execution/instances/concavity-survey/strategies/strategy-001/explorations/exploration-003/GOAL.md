# Exploration 003: Synthesis — Proof Strategy Assessment for λ_max(HessS) Global Maximum

## Goal

Given the findings from two prior literature surveys, produce a ranked assessment of proof strategies for establishing that λ_max(HessS(Q)) achieves its global maximum at Q = I (flat connection) on SU(N)^E in lattice Yang-Mills theory.

This is a synthesis and assessment task — not a new literature survey. Your job is to evaluate which approaches are most tractable, identify where they connect, and produce a concrete recommendation for what to try first.

## Prior Findings to Synthesize

### From Survey 1: Classical Eigenvalue Concavity Theorems

**Main result:** All classical theorems (Davis-Lewis, Ando, Löwner, Fan, Weyl) operate on vector spaces or open cones. None directly apply to functions on compact Lie groups. Moreover, λ_max is CONVEX on vector spaces — the wrong direction.

**Viable leads from classical theory:**
1. **Majorization (Schur-Horn/Kostant):** If λ(H(Q)) ≺ λ(H(I)) for all Q ∈ SU(N)^E (eigenvalues are always majorized by those at the flat connection), then λ_max(H(Q)) ≤ λ_max(H(I)) follows immediately. This is a direct, computable condition.
2. **arXiv:2408.16906 (2024):** Convexity of sums of eigenvalue phases of segments of unitaries. Shows eigenvalue sums of u(t) = e^{itx}e^{iy} are convex for ‖u-I‖ < √2. The PROOF TECHNIQUE (second-variation formula for eigenvalue phases) may be adaptable even though the theorem itself gives the wrong direction.
3. **Second-variation analysis at Q=I:** Directly compute d²λ_max(H(Q(t)))/dt² for geodesics through I. Not covered by generic theory but explicitly computable from the Hessian formula.

### From Survey 2: Geodesic Convexity and Alternatives on Compact Lie Groups

**Main result:** Full geodesic concavity is IMPOSSIBLE on compact manifolds (superharmonic → constant by max principle). This is a theorem, not just a numerical observation.

**Six frameworks for certifying local max = global max:**

1. **Perfect Morse function (★★★★★):** On SU(2)^E ≅ (S³)^E, the top Betti number b_{3E} = 1. If λ_max(H(Q)) is a perfect Morse function, the unique top-index critical point is the global max. Precedent: Atiyah-Bott (1983) proved equivariant perfectness for Yang-Mills on Riemann surfaces. A lattice analog has not been worked out.

2. **Trap-free landscape (★★★★):** Russell-Rabitz (2016, arXiv:1608.06198) proved quantum control landscapes are trap-free under transversality (surjectivity of dH). If the differential of Q ↦ H(Q) is generically surjective, no non-global local maxima exist. This is CHECKABLE by computing the rank of dH at non-flat configurations.

3. **Gauge symmetry + unique orbit (★★★★):** If Q=I is the unique gauge orbit of flat connections, and λ_max is gauge-invariant, then gauge symmetry may force global optimality.

4. **Łojasiewicz + uniqueness (★★★):** Proves gradient flow convergence but not global optimality alone.

5. **Double bracket reformulation (★★★):** Brockett-type flows — extend from trace functions to λ_max.

6. **SDP certificate (★★):** Numerical, not analytic.

**Unexpected finding:** Invexity is the exact abstract characterization (every stationary point is global optimum iff function is invex), but it's a restatement rather than a proof technique.

## What the Synthesis Should Do

### A. Cross-Reference and Connect
- Do any classical matrix analysis techniques COMBINE with the Riemannian/topological frameworks?
- Specifically: does the majorization idea (λ(H(Q)) ≺ λ(H(I))) relate to the Kostant convexity theorem or the Atiyah-Bott equivariant theory?
- Could the 2024 unitary eigenvalue proof technique be adapted to prove concavity within the injectivity radius ball, feeding into a local-to-global argument?

### B. Rank the Approaches
For each approach, assess:
- **Feasibility:** How hard is it to carry out? (Easy/Moderate/Hard/Unknown)
- **Decisiveness:** If it works, does it solve the full problem? (Yes/Partial/No)
- **Verifiability:** Can progress be checked computationally? (Yes/No)
- **Novelty:** Has this approach been tried before for lattice gauge theory? (Novel/Partially known/Standard)

### C. Identify the Critical Path
What should be tried FIRST? Argue for a specific sequence of 2-3 proof attempts, ordered by expected value (probability of success × value of result).

### D. Identify Obstacles and Failure Modes
For each top approach, what is the most likely reason it fails? What would you check first to see if it's viable?

## Known Structure of the Problem

To help with the assessment, here is what's known about H(Q):

- **H(Q) = HessS(Q)** is the Hessian of the Wilson action S(Q) = -β Σ_P Re Tr(U_P(Q))
- **At Q=I:** H_norm(I) = d/(4(d-1)N²) = 1/12 for d=4, N=2 (PROVED via Fourier block-diagonalization)
- **Decomposition:** HessS = D (diagonal self-term) + C (off-diagonal cross-term), where C has indefinite components but λ_max(H_actual) ≤ λ_max(H_formula)
- **Symmetry:** Lattice symmetries (translations, rotations) + gauge symmetry
- **Numerics:** Q=I is confirmed as the unique global maximizer of λ_max for all tested lattice sizes. All gradient ascent trajectories converge there.
- **SZZ Lemma 4.1 bound is 12-170x loose** — the actual Hessian eigenvalue is much smaller than the worst-case bound. Plaquette contributions destructively interfere.

## Success Criteria

- A clear ranked list of proof strategies with feasibility/decisiveness/verifiability ratings
- Specific connections between the classical and Riemannian findings (not just listing them side by side)
- A recommended critical path: "try X first, then Y, then Z"
- For each top-2 approach, the most likely failure mode and how to detect it early

## Failure Criteria

- Just repeating the findings from both surveys without synthesis
- Ranking approaches without justification
- Missing the majorization ↔ Morse theory connection (if one exists)

## Output

Write REPORT.md and REPORT-SUMMARY.md in your exploration directory.
