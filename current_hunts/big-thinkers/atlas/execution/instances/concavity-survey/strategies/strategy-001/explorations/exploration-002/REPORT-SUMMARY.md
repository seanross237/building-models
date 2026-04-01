# Exploration 002: REPORT SUMMARY
## Geodesic Convexity on Riemannian Manifolds and Compact Lie Groups

---

## What Was the Goal

Survey the literature on geodesic convexity/concavity on Riemannian manifolds and compact Lie groups, with focus on frameworks for certifying global optimality without full geodesic concavity. The motivating problem: λ_max(H(Q)) achieves its global maximum at Q = I on SU(N)^E, but full geodesic concavity is numerically falsified.

---

## What Was Tried

Comprehensive web literature survey covering: geodesic convexity foundations, compact manifold obstructions, optimization on SU(N), Morse theory on Lie groups, Łojasiewicz inequality, mountain pass / Lusternik-Schnirelmann theory, Palais-Smale condition, quantum control trap-free landscape results, double bracket flows (Brockett-Bloch-Ratiu), and SDP global optimality certificates. Roughly 15 searches plus targeted paper fetch/reads.

---

## What Was the Outcome

**Successful survey. Six viable frameworks identified.**

---

## Key Takeaway

**The failure of global geodesic concavity is not a numerical accident — it is a mathematical theorem.** On any compact connected Riemannian manifold without boundary, no nonconstant smooth function can be globally geodesically concave or convex. Proof: geodesic concavity → Riemannian Hessian ≤ 0 → Laplacian ≤ 0 (superharmonic) → constant by maximum principle. SU(N)^E is compact without boundary, so this applies. The numerics confirmed what theory guaranteed.

This means the question "is λ_max globally concave on SU(N)^E?" was always going to be **NO** for any nonconstant smooth function, regardless of the specific H.

---

## Six Frameworks for Certifying Local Max = Global Max (Without Concavity)

| # | Framework | Promise | Key Gap |
|---|-----------|---------|---------|
| 1 | **Perfect Morse function** on SU(2)^E | ★★★★★ | Prove perfectness (Kirwan-type argument needed) |
| 2 | **Trap-Free Landscape** (Rabitz-Russell 2016) | ★★★★ | Verify controllability/transversality condition for lattice YM |
| 3 | **Gauge Symmetry + Unique Gauge Orbit** | ★★★★ | Classify flat connections as the only gauge-orbit of I |
| 4 | **Łojasiewicz + uniqueness of max** | ★★★ | Proves convergence but not global optimality alone |
| 5 | **Double Bracket Reformulation** | ★★★ | Extend from trace functions to λ_max |
| 6 | **SDP Certificate** (numerical) | ★★ | Not an analytic proof |

---

## Most Promising Framework: Perfect Morse + Symmetry

**Why Morse theory is the right lens:**

On SU(2)^E ≅ (S³)^E, the Poincaré polynomial is (1+t³)^E, which has b_{3E} = 1. For a **perfect Morse function**, the number of top-index critical points equals b_{3E} = 1 — meaning the unique local maximum is automatically the global maximum.

The numerics give us: Q = I is a non-degenerate local maximum (Hessian is negative-definite). This is the right Morse index (top index). If f is a perfect Morse function, uniqueness follows immediately.

**Caveat corrected in report**: Morse inequalities alone don't force c_{top} = 1. Multiple local maxima are algebraically consistent with χ = 0. Perfectness is what forces uniqueness. Proving perfectness requires additional structure (equivariant techniques, gauge symmetry, or direct analysis).

**Precedent**: Atiyah-Bott (1983) and Kirwan (1984) showed the Yang-Mills functional over Riemann surfaces is equivariantly perfect, which is used to compute the cohomology of moduli spaces. A finite-dimensional analog for lattice Yang-Mills on SU(N)^E has not been worked out in the literature.

---

## Trap-Free Landscape Framework (Close Second)

Russell-Rabitz (arXiv:1608.06198, 2016) proved that for almost all quantum Hamiltonians, the optimization landscape on SU(N) is trap-free: all critical points are either global optima or saddle points, never non-global local optima. The proof uses parametric transversality.

A subsequent 2024 paper (arXiv:2409.15139) showed the set of globally optimal solutions is path-connected.

**Application to our problem**: If the map Q ↦ λ_max(H(Q)) satisfies the "controllability" (transversality) condition, the trap-free result applies. Specifically: if dH is surjective at generic Q (the plaquette contributions collectively span the Hermitian matrix space), the landscape is trap-free and Q = I is the only non-saddle critical point.

**This is checkable**: the rank of dH at non-flat configurations can be computed numerically or analytically from the lattice geometry.

---

## Unexpected Finding

**Invexity is the "right" abstract framework.** A function f is geodesically invex iff every stationary point is a global minimum (or maximum for the maximization version). So "λ_max is invex on SU(N)^E" is *equivalent* to "every local max is global" — it's a restatement of the goal, not a proof technique. But the invexity literature provides tools for proving this: sufficient conditions exist in terms of directional derivatives and the geometry of the connecting geodesics.

Also unexpected: Palais-Smale is trivially satisfied on compact manifolds (compactness implies every sequence has a convergent subsequence). The PS condition, prominent in infinite-dimensional variational analysis, adds nothing in our finite-dimensional lattice setting.

---

## Computations Identified

1. **Rank of dH on SU(N)^E**: Compute the rank of the differential of Q ↦ H(Q) at multiple non-flat configurations. If generically full rank, this verifies the Rabitz transversality condition and makes the trap-free result applicable. Moderate difficulty: 50-100 line numpy script, needs the explicit formula for H(Q) from the Yang-Mills exploration.

2. **Morse perfectness check**: For small lattices (E = 2 or E = 3 on SU(2)), numerically count the critical points of λ_max(H(Q)) by gradient ascent from random initializations. If the number of local maxima found is always 1, this is strong numerical evidence for perfectness. Moderate difficulty: gradient ascent sweep.

3. **Convexity radius verification**: Compute whether λ_max(H(Q)) is geodesically concave within the π√2/2 convexity ball around Q = I in SU(2)^E. If yes, this gives a local-to-global result within the geodesically convex ball. Low difficulty: modify existing second-derivative computation.

---

## Leads Worth Pursuing

1. **Kirwan/Atiyah-Bott equivariant Morse theory for lattice gauge theory** — This is the main unexplored mathematical direction. Does the lattice Yang-Mills function λ_max(H(Q)) satisfy the conditions of Kirwan's theorem on equivariantly perfect Morse functions? The gauge group G_gauge acting on SU(N)^E is the right symmetry group.

2. **Trap-free verification via controllability** — Compute the rank condition for the plaquette map. If it holds, the Rabitz-type theorem gives the result immediately without needing full Morse analysis.

3. **Connection to Brockett double bracket** — λ_max(H(Q)) = max_{||v||=1} v†H(Q)v = max_P Tr(P·H(Q)) where P ranges over rank-1 projectors. This is a joint optimization over Q ∈ SU(N)^E and P ∈ ℂP^{N-1}. The double bracket flow on the joint space might give global convergence.

---

## Sources Used

- Russell, Rabitz (2016): arXiv:1608.06198 — Quantum control landscapes are almost always trap-free
- arXiv:2409.15139 (2024) — Top manifold connectedness of quantum control landscapes
- PMC:8589322 — Orthogonal trace-sum maximization: global optimality certificate via SDP
- Absil, Mahony, Sepulchre (2008) — Optimization Algorithms on Matrix Manifolds
- Helmke, Moore (1994) — Optimization and Dynamical Systems
- Bloch, Brockett, Ratiu (1992) — Completely Integrable Gradient Flows (CMP 147:57)
- Standard Riemannian geometry: nLab geodesic convexity; BIMSA notes; Hopf-Rinow theorem
- Seth Axen blog (2023) — Injectivity radii of unitary groups (confirms inj(SU(2)) = π√2)
- Standard Morse theory references: Milnor, Bott, Frankel
