# Exploration 002: Geodesic Convexity on Riemannian Manifolds and Compact Lie Groups

## Goal

Survey the mathematical literature on geodesic convexity/concavity of functions defined on Riemannian manifolds, with particular focus on compact Lie groups. The motivating problem is proving that a spectral function (maximum eigenvalue) achieves its global maximum at a known point on SU(N)^E.

## Specific Topics to Cover

### A. Geodesic Convexity Foundations
1. **Definition and characterization** of geodesically convex/concave functions on Riemannian manifolds
2. **Sufficient conditions** for geodesic convexity — Riemannian Hessian criteria, sectional curvature conditions
3. **Geodesic convexity on compact manifolds** — what special structure exists? (compact manifolds can't have globally convex functions in the usual sense — what's the right notion?)

### B. Optimization on Matrix Groups
4. **Optimization on SU(N) and products of SU(N)** — what's known about the landscape of smooth functions on compact Lie groups?
5. **Morse theory on Lie groups** — using Morse-theoretic structure to count/characterize critical points
6. **Results by Helmke, Moore, Brockett, Absil** on optimization on matrix manifolds — especially gradient flow convergence results

### C. Conditional/Restricted Concavity
7. **Concavity along geodesics vs. global concavity** — when can local geodesic concavity + other structure give global optimality?
8. **Concavity on convex subsets** — geodesically convex subsets of Lie groups
9. **Log-concavity and related notions** on groups — Prékopa-type theorems on groups

### D. Alternatives to Full Concavity
10. **Mountain pass theorems** — using the topology of the configuration space to relate local and global structure
11. **Łojasiewicz inequality** — gradient flow convergence without convexity
12. **Palais-Smale condition** on compact manifolds — does it help characterize global maxima?
13. **Convexity of the spectral radius** (as opposed to individual eigenvalues) — the spectral radius ρ(A) is known to be convex for nonnegative matrices (Perron-Frobenius); what about Hermitian matrices on groups?

## Critical Context

**The full concavity approach has been numerically falsified for our problem.** Specifically, for the lattice Yang-Mills Hessian H(Q) on SU(2)^E:
- λ_max(H(Q)) is NOT globally geodesically concave (second derivative along geodesics is positive at some Q ≠ I)
- But λ_max(H(Q)) still achieves its global max at Q = I (flat connection), confirmed numerically
- All gradient ascent trajectories converge to Q = I
- The second variation at Q = I is negative-definite (confirmed local max)

So the question is: **what mathematical framework, short of full geodesic concavity, can certify that a local max on a compact Lie group is the global max?**

Relevant structure of our specific problem:
- H(Q) is a sum over plaquettes (local structure in a lattice)
- SU(N)^E has positive Ricci curvature (Ric(u,u) = (N/2)|u|^2 from bi-invariant metric)
- The function has a large symmetry group (lattice symmetries + gauge symmetry)

## Success Criteria

- Coverage of ≥3 frameworks for establishing global optimality on compact Lie groups without full concavity
- At least one framework that could plausibly apply to a sum-of-plaquettes structure on SU(N)^E
- Honest assessment of which approaches are most promising for our problem
- Recent references (2020-2026) if they exist

## Failure Criteria

- Only covering geodesic convexity without alternatives
- Missing the compact manifold subtlety (no globally convex functions on compact manifolds)
- Not addressing the "local max → global max" question

## Output

Write REPORT.md and REPORT-SUMMARY.md in your exploration directory.
