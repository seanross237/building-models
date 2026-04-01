# Strategy 001 Final Report: Concavity of Spectral Functions on Matrix Groups

## Summary

Three focused explorations surveyed the mathematical landscape for proving that λ_max(HessS(Q)) achieves its global maximum at Q = I (flat connection) on SU(N)^E in lattice Yang-Mills theory. The original question — "is λ_max concave on SU(N)^E?" — was definitively answered: **no, and it can't be**, by theorem. But the survey identified multiple viable alternative frameworks, culminating in a novel approach (matrix domination) that emerged from synthesizing the two survey bodies.

## What Was Accomplished

### Exploration 001: Classical Eigenvalue Theorems
Cataloged 8+ major results (Davis-Lewis, Ando, Löwner, Fan, Weyl, Kostant/AGS, 2024 unitary paper). Found a **fundamental domain gap**: all classical theorems operate on vector spaces or open cones, not compact Lie groups. λ_max is convex (not concave) on vector spaces. No applications to lattice gauge theory exist in the literature.

### Exploration 002: Geodesic Convexity and Alternatives
Established that full geodesic concavity is **impossible by theorem** on compact manifolds (superharmonic → constant by max principle). Identified six frameworks for certifying local max = global max without concavity, with Morse perfectness and trap-free landscapes as the top two.

### Exploration 003: Synthesis
Cross-referenced the two surveys and produced a ranked list of 8 proof strategies. A new highest-priority approach emerged: **direct matrix domination H(I) ≥ H(Q) (PSD ordering)**. This subsumes majorization, requires no topology, and is directly testable.

## Directions Tried

| Direction | Explorations | Outcome |
|-----------|-------------|---------|
| Classical matrix analysis theorems | 001 | Domain gap — theorems don't apply to compact groups |
| Riemannian/topological frameworks | 002 | Full concavity impossible; 6 alternative frameworks found |
| Synthesis and proof strategy ranking | 003 | Matrix domination emerged as top approach |

## Most Promising Findings

### 1. Matrix Domination (NEW — emerged from synthesis)
If H(I) - H(Q) is positive semidefinite for all Q ∈ SU(N)^E, then λ_max(H(Q)) ≤ λ_max(H(I)) in two lines. The SZZ bound's 12-170x looseness (plaquette contributions destructively interfere) is strong circumstantial evidence this might hold. **This appears to be a genuinely novel direction** — the SZZ bound is a scalar bound on λ_max, not a matrix bound. A matrix bound would be far stronger.

**How to test:** Compute H(I) - H(Q) for ~1000 random Q ∈ SU(2)^E and check eigenvalue positivity. ~20 lines of numpy. Decisive: either all positive (strong evidence, pursue analytic proof) or a counterexample found (close this path).

### 2. Perfect Morse Theory (Kirwan-type)
On SU(2)^E ≅ (S³)^E, b_{3E} = 1. If λ_max(H(Q)) is a perfect Morse function, the unique top-index critical point must be the global max. Precedent: Atiyah-Bott (1983) proved the Yang-Mills functional is equivariantly perfect on Riemann surfaces. A finite-dimensional lattice analog has not been worked out.

### 3. Trap-Free Landscape (Rabitz-Russell)
If dH is generically surjective on SU(N)^E (transversality), then the optimization landscape is trap-free: no non-global local maxima. Checkable via rank computation at non-flat configurations.

## Recommended Critical Path

1. **FIRST:** Numerical matrix domination test (~20 lines numpy). Either solves it or closes the path.
2. **PARALLEL:** Gradient ascent landscape survey — confirm Q=I is the unique attractor from 1000+ random starts.
3. **IF domination holds:** Analytical proof via D+C Hessian decomposition.
4. **IF domination fails, landscape clean:** Verify Rabitz transversality (rank of dH at non-flat critical points).
5. **FALLBACK:** Kirwan-type equivariant Morse theory with gauge symmetry (hard, 2-4 weeks).

## What the Next Strategy Should Focus On

If continuing this mission:
- **Execute the matrix domination test** (computation #1 above). This is the single highest-value next step.
- **Run the gradient ascent survey** (computation #2). Independent of domination, valuable for Morse evidence.
- If both succeed, the proof architecture is: matrix domination for the bound + landscape survey for uniqueness.

If folding into the Yang-Mills mission:
- Add matrix domination to the Yang-Mills strategizer's toolkit. The H(I) ≥ H(Q) test uses the same Hessian formula already computed there.
- The Rabitz transversality check (rank of dH) is also directly computable from existing infrastructure.

## Novel Claims

### Claim 1: Matrix Domination as Proof Strategy
- **Claim:** The positive semidefinite ordering H(I) - H(Q) ≥ 0 for all Q ∈ SU(N)^E may hold for the lattice Yang-Mills Hessian, providing a direct proof that λ_max(H(Q)) ≤ λ_max(H(I)).
- **Evidence:** The SZZ bound is 12-170x loose due to plaquette destructive interference (from yang-mills/szz-lemma-4-1-hessian-slack.md). The D+C decomposition shows C has large indefinite components but λ_max(H_actual) ≤ λ_max(H_formula) consistently (from yang-mills/hessian-analytical-formula-c-decomposition.md). No counterexample found in existing numerical work.
- **Novelty search:** No paper applying PSD matrix ordering of Hessians to lattice gauge theory found in either survey. SZZ uses only scalar eigenvalue bounds.
- **Strongest counterargument:** Near anti-flat configurations (plaquette holonomy ≈ -I), the Hessian structure may differ enough that individual eigenvalues of H(Q) exceed those of H(I) even though λ_max doesn't. PSD ordering is much stronger than λ_max ordering — it could fail even when λ_max(H(Q)) ≤ λ_max(H(I)) holds.
- **Status:** Speculative — needs numerical verification.

### Claim 2: Impossibility of Geodesic Concavity
- **Claim:** Global geodesic concavity of λ_max(H(Q)) on SU(N)^E is impossible for any nonconstant H, by the maximum principle on compact manifolds.
- **Evidence:** Standard Riemannian geometry: geodesic concavity ⟹ superharmonic ⟹ Δf ≤ 0 everywhere ⟹ f is constant (by the maximum principle on compact manifolds without boundary). SU(N)^E is compact without boundary.
- **Novelty search:** This is a standard result in Riemannian geometry, not novel. However, its application to rule out concavity-based proofs in lattice gauge theory appears to be new.
- **Strongest counterargument:** None — this is a theorem.
- **Status:** Verified (standard result, correctly applied).

## Efficiency Notes

3/3 explorations used, all successful. Running explorations 001 and 002 in parallel saved ~30 minutes. The synthesis (003) was the most valuable — the matrix domination approach emerged from cross-referencing, not from either survey alone. This validates the strategy's three-phase design (classical → Riemannian → synthesis).
