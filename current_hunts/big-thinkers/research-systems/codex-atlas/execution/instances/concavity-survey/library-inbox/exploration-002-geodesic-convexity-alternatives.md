# Exploration 002: Geodesic Convexity on Riemannian Manifolds and Compact Lie Groups
# REPORT

## Goal Summary

Survey the mathematical literature on geodesic convexity/concavity on Riemannian manifolds and compact Lie groups, with focus on finding frameworks that can certify global optimality without requiring full geodesic concavity. The motivating problem: λ_max(H(Q)) achieves its global maximum at Q = I on SU(N)^E, but full geodesic concavity has been numerically falsified. What mathematical machinery can certify "local max = global max"?

---

## Section A: Geodesic Convexity/Concavity — Foundations

### Definitions

A smooth function f on a Riemannian manifold (M, g) is **geodesically concave** if for every geodesic γ: [a,b] → M, the composition f ∘ γ is a concave function of the parameter. Equivalently:

- **Differential criterion**: f is geodesically concave iff its Riemannian Hessian satisfies Hess_g f ≤ 0 pointwise (negative semidefinite as a bilinear form on each tangent space).
- **Strict version**: f is strictly geodesically concave if Hess_g f < 0 (negative definite).

The Riemannian Hessian at p ∈ M is Hess f(u,v) = g(∇_u ∇f, v) where ∇ is the Levi-Civita connection.

### Key Sufficient Condition (from literature)

For f to be geodesically concave on a geodesically convex subset U ⊂ M, it suffices that Hess_g f(u,u) ≤ 0 for all u ∈ TM|_U. On manifolds with non-positive sectional curvature (Hadamard manifolds), global geodesic concavity is achievable. On positively curved manifolds, it faces the obstruction described in Section B.

### Geodesically Convex Sets

A set C ⊂ M is geodesically convex if, for any two points in C, there is a unique minimizing geodesic connecting them that stays in C. Within any geodesic ball of radius less than the convexity radius (≤ injectivity radius / 2), the ball is geodesically convex.

---

## Section B: THE FUNDAMENTAL OBSTRUCTION — Compact Manifolds and Global Concavity

**This is the most important section of this report.** The numerical failure of geodesic concavity for our problem is not an accident — it is mathematically inevitable.

### Theorem (No globally concave functions on compact manifolds)

**On any compact connected Riemannian manifold without boundary, no nonconstant smooth function can be globally geodesically concave (or convex).**

**Proof sketch:**
1. Suppose f is smooth and geodesically concave, so Hess_g f ≤ 0 everywhere (negative semidefinite).
2. Taking the trace: Δf = trace_g(Hess_g f) ≤ 0 everywhere, so f is **superharmonic**.
3. On a compact manifold without boundary, the maximum principle for the Laplacian implies every superharmonic function is constant.

The same argument applies to geodesically convex f (which gives Δf ≥ 0, i.e., subharmonic, hence constant).

**Source**: This follows from Bochner's maximum principle and is standard in Riemannian geometry. References: Cheeger-Ebin "Comparison Theorems in Riemannian Geometry"; nLab "geodesic convexity"; explicitly noted in the context of optimization on compact manifolds.

### Implication for Our Problem

SU(N)^E is a compact connected Riemannian manifold without boundary (equipped with the bi-invariant product metric). Therefore:

> **λ_max(H(Q)) CANNOT be globally geodesically concave on SU(N)^E, regardless of the specific form of H.** This is not a numerical finding — it is a theorem.

The numerical falsification in exploration-001 was confirming a mathematical certainty. The question "is λ_max globally concave on SU(N)^E?" has answer **NO** for any nonconstant smooth function, by pure topology.

### What Geodesic Concavity Can Offer (in the compact setting)

All is not lost. One can meaningfully speak of:
- **Local geodesic concavity** — on geodesically convex neighborhoods (geodesic balls of radius < convexity radius)
- **Restricted concavity** — concavity along a specific family of geodesics (not all geodesics)
- **Concavity of f on a geodesically convex subset** of M (which is a proper open subset)

For SU(2), the convexity radius of the bi-invariant metric is π√2 / 2 ≈ π/√2. The injectivity radius of SU(2) is π√2 (confirmed: for SU(n), the injectivity radius is π√2, and for SU(2) the lower and upper bounds coincide at π√2). The convexity radius is half the injectivity radius = π√2/2.

---

## Section C: Optimization on Compact Lie Groups — What's Known

### SU(N) with Bi-invariant Metric

SU(N) is a compact simple Lie group. With the bi-invariant metric g(u,v) = -Tr(uv) (up to normalization), it has:
- **Sectional curvature**: K(u,v) = (1/4)|[u,v]|² ≥ 0 (nonnegative sectional curvature)
- **Ricci curvature**: Ric(u,u) = (N/4)|u|² (constant Ricci curvature, proportional to metric)
- **Positive scalar curvature**: SU(N) is an Einstein manifold with positive Einstein constant

The positive sectional curvature is exactly what produces conjugate points and prevents global concavity.

### Injectivity and Convexity Radii

For SU(n) with standard bi-invariant metric:
- **Injectivity radius**: π√2 (verified for SU(2); for general SU(n), the min is π√2 at the identity)
- **Convexity radius**: ≤ π√2/2 ≈ 2.22

Within a geodesic ball of radius π√2/2, the ball is geodesically convex and any strictly concave function can have at most one local max (which is automatically global within the ball).

### Critical Point Landscape on Lie Groups

Studies of optimization on compact Lie groups (references: Helmke-Moore "Optimization and Dynamical Systems" 1994; Absil-Mahony-Sepulchre "Optimization Algorithms on Matrix Manifolds" 2008) show:

- For "trace-type" functions f(U) = Re Tr(AU†) on SU(N), all local minima are global minima and other critical points are saddle points — the **landscape is trap-free** for these simple functions.
- Gradient-based methods on compact Lie groups have known convergence properties but generally converge to *local* optima, not necessarily global ones.
- Absil-Mahony-Sepulchre: Methods based on retractions and vector transport have convergence guarantees to first-order critical points. The book notes: "methods produce sequences whose accumulation points are local minima of the cost function" — not global minima in general.

---

## Section D: Morse Theory on Lie Groups

### Classical Bott Morse Theory

Raoul Bott's foundational work (1954, 1959) applied Morse theory to homogeneous spaces and Lie groups. Key result:

**The function f_A(U) = Re Tr(AU) on SU(N) is a Morse-Bott function with critical points exactly at elements U commuting with A.** The critical set decomposes according to the eigenvalue structure of A.

For the specific case SU(2) ≅ S³:
- SU(2) has Poincaré polynomial 1 + t³ (Betti numbers b₀ = b₃ = 1, all others 0)
- A perfect Morse function on SU(2) has exactly **2 critical points**: one minimum (index 0) and one maximum (index 3 = dim SU(2))
- This means on SU(2), any perfect Morse function has a **unique global maximum**

### Product Structure SU(2)^E

For SU(2)^E:
- Poincaré polynomial: (1 + t³)^E = Σ_{k=0}^{E} C(E,k) t^{3k}
- A perfect Morse function on SU(2)^E has critical points with Morse index 3k having multiplicity C(E,k)
- **Unique global maximum** (index 3E): only one critical point at the maximum
- This means: if λ_max(H(Q)) is a **perfect Morse function** on SU(2)^E, its unique global maximum is also the unique local maximum

### Morse Index Calculation at Q = I

At Q = I (flat connection), if the Hessian is negative-definite in all tangent directions (confirmed numerically in our problem), then Q = I is a non-degenerate critical point with Morse index equal to dim(SU(N)^E) = 3E·(N²-1) (the dimension of the manifold). This means Q = I is a **local maximum** in the Morse-theoretic sense.

**Critical caveat on uniqueness**: The Morse inequalities alone do NOT force uniqueness of the global maximum. The strong Morse inequalities state c_{top} ≥ b_{top} = 1, meaning there is AT LEAST one top-index critical point. But there can be MORE. For example, on S³ with Euler characteristic 0, having two local maxima (c₃ = 2) is consistent with the Morse inequalities, provided there are two extra index-2 saddle points (c₂ = c₁ + 1).

### The Correct Morse Theory Statement

**Perfect Morse functions** (where M(t) = P(t) exactly) have:
- c_{3E} = b_{3E}(SU(2)^E) = 1 (unique global maximum)

If λ_max(H(Q)) is a perfect Morse function on SU(2)^E, then Q = I is the unique local (and hence global) maximum. But proving perfectness is a non-trivial task.

**Known perfect Morse results on related spaces**:
- Kirwan (1984): The Yang-Mills functional on a compact Riemann surface is **equivariantly perfect** as a Morse-Bott function (via the gauge group action). The space of connections A/G (gauge-equivalence classes) has the same cohomology as the moduli space of flat connections, computed using the equivariant Morse function.
- Atiyah-Bott (1983): Used equivariant perfectness to compute the cohomology of moduli spaces of holomorphic bundles.

For our finite-dimensional lattice problem on SU(N)^E, an analog of the Atiyah-Bott–Kirwan argument might apply, but it would need to be explicitly constructed.

### Gap: Proving Perfect Morse Property

The gap is proving that λ_max(H(Q)) is a perfect Morse function. This requires:
1. Non-degeneracy of all critical points (Morse condition)
2. Equality of Morse polynomial and Poincaré polynomial (perfectness)

### Frankel-Dynnikov-Veselov Connection

Dynnikov and Veselov (1996, "Integrable Gradient Flows and Morse Theory") studied integrable gradient flows on Lie groups and their Morse-theoretic properties. The Toda lattice, expressible in double-bracket form, provides an example where the Morse structure of certain spectral functions is completely understood.

---

## Section E: Łojasiewicz Inequality — Gradient Flow Convergence

### The Classical Łojasiewicz Inequality

For a real **analytic** function f near a critical point p on ℝⁿ, there exist constants C > 0 and θ ∈ (0, 1/2) such that:
|f(x) - f(p)|^{1-θ} ≤ C |∇f(x)|

This is the *local* Łojasiewicz inequality. It implies:
1. Every gradient flow trajectory has finite arc length and converges to a critical point
2. Convergence rate depends on θ (polynomial when θ = 1/2, exponential when analytic)

### Extension to Riemannian Manifolds (Łojasiewicz-Simon Inequality)

The Łojasiewicz-Simon inequality extends this to infinite-dimensional settings (Banach spaces, PDEs). On **compact analytic Riemannian manifolds**, the local Łojasiewicz inequality holds for any analytic f near any critical point.

**Key consequence for our problem**: SU(N)^E is a real analytic manifold (as an algebraic variety). λ_max(H(Q)) is analytic in Q (assuming H is analytic). Therefore:
- Every gradient ascent trajectory converges to a critical point (no oscillation or limit cycles)
- The convergence is at a specific algebraic rate

**Source**: Łojasiewicz inequality Wikipedia; Bolte-Daniilidis-Lewis (2007) paper on Łojasiewicz-Simon on analytic manifolds; Hosseini (2017) on Kurdyka-Łojasiewicz on Riemannian manifolds.

### What Łojasiewicz Does NOT Provide

Łojasiewicz guarantees convergence to *a* critical point, not to the *global* maximum. If there exist local maxima that are not global, gradient ascent might converge to a non-global local maximum.

**However**: combined with a proof that there are no local-non-global maxima (e.g., from Morse theory), Łojasiewicz provides the convergence rate result.

### The Polyak-Łojasiewicz (PL) Condition

A stronger global condition: (1/2)|∇f|² ≥ μ(f* - f) for some μ > 0 (for minimization). This is the "PL condition." It implies:
- Every stationary point is a global minimizer
- Gradient descent converges linearly

For our maximization problem, the "reverse PL" condition would say |∇f|² ≥ μ(f(Q*) - f(Q)). If this holds globally on SU(N)^E, it certifies Q = I as the unique global maximizer.

**Challenge**: Verifying the global PL condition is typically harder than checking a single point. On compact manifolds, analytic functions automatically satisfy the *local* Łojasiewicz condition near each critical point, but the *global* PL condition is much stronger.

---

## Section F: Mountain Pass Theorem and Topological Methods

### Lusternik-Schnirelmann Theory

The Lusternik-Schnirelmann theorem gives a lower bound on the number of critical points of a smooth function on a compact manifold in terms of the **Lusternik-Schnirelmann category** of the manifold (cat(M)).

For SU(2) ≅ S³: cat(S³) = 2. So any smooth function on SU(2) has at least 2 critical points.
For SU(2)^E: cat(SU(2)^E) = E+1 (for products of spheres). So any smooth function has at least E+1 critical points.

This gives a lower bound on critical point count but doesn't characterize which are global maxima.

### Mountain Pass Theorem

The mountain pass theorem (Ambrosetti-Rabinowitz 1973) states: if f has two local minima and f satisfies the Palais-Smale condition, then there is a third critical point (saddle point) between them. The dual statement for maxima: if two local maxima exist, there must be a saddle point between them.

**Contrapositive**: If one can show that no saddle point exists between Q = I and any other "candidate maximum," then there can be no other local maximum.

**Application challenge**: Proving the absence of saddle points in between is just as hard as proving uniqueness of the maximum directly.

### Topological Obstruction Argument

More directly useful: on SU(2) ≅ S³, the level sets of a smooth function behave like those on a sphere. For S³, a function with a single local maximum at the "north pole" and a single minimum at the "south pole" must have all other critical points as saddle points. This is the Morse-theoretic argument: if b₀ = b₃ = 1 (which they are for S³), and the function is Morse, then:
- At most 1 index-0 critical point (minimum)
- At most 1 index-3 critical point (maximum)
- The rest are saddles (indices 1 or 2)

For SU(2)^E ≅ (S³)^E, this extends: there can be at most 1 index-3E critical point (global maximum), and any local maximum (which would have index 3E) is automatically the global maximum if it exists and is non-degenerate.

---

## Section G: Palais-Smale Condition on Compact Manifolds

### Definition

A sequence (x_n) in M is a Palais-Smale sequence for f if f(x_n) → c and |∇f(x_n)| → 0. The function f satisfies the **Palais-Smale condition at level c** (PS)_c if every such sequence has a convergent subsequence.

### On Compact Manifolds

**On any compact Riemannian manifold, every smooth function automatically satisfies the Palais-Smale condition at every level.** This is because any bounded sequence in a compact manifold has a convergent subsequence (by compactness).

**Consequence**: On SU(N)^E, Palais-Smale is automatic and doesn't add information. The Palais-Smale condition is primarily useful in infinite-dimensional settings (e.g., Yang-Mills over continuous gauge fields) where compactness fails.

For our finite-dimensional lattice problem on SU(N)^E, Palais-Smale is trivially satisfied and is not the bottleneck.

---

## Section H: Conditional / Restricted Concavity Frameworks

### Geodesically Convex Subsets

Even though SU(N)^E doesn't support global concavity, one can ask whether f = λ_max(H(Q)) is concave on a **geodesically convex open subset** containing Q = I.

The largest geodesically convex neighborhood of Q = I in SU(N)^E is approximately the product of geodesic balls of radius π√2/2 in each factor. Within this neighborhood:
- If λ_max is strictly concave near I (which requires Hess ≤ 0 on this ball), then Q = I is the unique max in this neighborhood
- This is a local-to-global result within the convex neighborhood

**Limitation**: The geodesic ball of radius π√2/2 in SU(2) covers about half the manifold (diameter = π√2). So we're checking concavity on roughly half the space. Numerical falsification shows that concavity fails somewhere, but where?

### Invexity

A function f is **geodesically invex** if it satisfies: for any two points p, q in M, the critical direction of f at q points "toward" p in a generalized sense. Formally: f is geodesically invex iff every critical point of f is a global minimum (maximum for invex for maximization).

**Key theorem**: f is geodesically invex ⟺ every stationary point is a global minimum (Barani-Pouryayevali 2007, Generalized Geodesic Convexity).

**Application**: If we can prove λ_max(H(Q)) is geodesically invex (for maximization), then every local maximum is global.

**Challenge**: Invexity is hard to verify directly; it's essentially equivalent to the conclusion we want to prove.

### Log-Concavity / Prékopa Analogs on Groups

Prékopa-Leindler inequalities have been extended to Riemannian manifolds with nonneg Ricci curvature. SU(N) with bi-invariant metric has Ric = (N/4)g > 0. There may be analogs of log-concavity for measures on SU(N), but this doesn't directly help with eigenvalue functions.

---

## Section I: The Trap-Free Landscape Framework (Most Promising)

### Quantum Control Landscape Results

The most directly applicable framework comes from quantum control theory. The **Rabitz group's trap-free landscape results** (2004-2016) show that for generic quantum control objectives, no local optima exist except global ones.

**Key setup**: Optimize f(U) = J(U) where U ∈ SU(N) is a unitary evolution operator and J is an objective function (e.g., fidelity, expectation value). Under the "local surjectivity" condition (equivalent to controllability), the landscape is trap-free.

**Theorem (Russell-Rabitz 2016, arXiv:1608.06198)**: For "almost all" Hamiltonians (all but a null set), the quantum control landscape has no local optima except global ones. Specifically: every critical point of J(U) is either a global maximum or a saddle point.

**Proof technique**: Parametric transversality theorem. The end-point map U(T): controls → SU(N) is shown to be transverse to the level sets of J for generic Hamiltonians. This transversality implies that singular points of J are "generically" saddle points, not traps.

### Extension to Our Problem

Our function λ_max(H(Q)) on SU(N)^E is not exactly of the form studied by Rabitz. The key difference: Rabitz studies f: SU(N) → ℝ, while we have f: SU(N)^E → ℝ where E > 1. However:

1. The product structure means SU(N)^E is a larger group (specifically, SU(N)^E can be viewed as the holonomy group of the lattice gauge theory)
2. The plaquette structure means H(Q) depends on specific products of group elements — this is more constrained than a general function on SU(N)^E

**Applicability assessment**: The Rabitz framework requires a "controllability" condition that may or may not hold for lattice Yang-Mills. If the Yang-Mills plaquette dynamics are "controllable" in the appropriate sense, the trap-free result would apply. This requires checking:
- Does the differential of the map Q ↦ H(Q) span the relevant space?
- Is the level-set transversality condition satisfied?

### Newer Result: Top Manifold Connectedness (2024)

The 2024 paper arXiv:2409.15139 "Top Manifold Connectedness of Quantum Control Landscapes" extends the trap-free results to show the set of globally optimal solutions is **path-connected**. This means gradient ascent started anywhere near the optimal value will find the global optimum (no isolated local optima). For our problem, if Q = I is the global max, the set of global maxima is connected (and likely a manifold, due to gauge symmetry).

---

## Section J: Double Bracket Flows and Isospectral Optimization

### Brockett's Double Bracket Equation

The double bracket equation (Bloch-Brockett-Ratiu 1992, "Completely Integrable Gradient Flows"):
Ȧ = [A, [A, N]] (on an adjoint orbit of a compact Lie group)

is a gradient flow for the function f(A) = Tr(A·N) on the isospectral manifold (adjoint orbit). This flow:
1. Preserves the spectrum of A
2. Converges globally to the critical point where A is diagonal (aligned with N)
3. All non-diagonal critical points are saddle points

**Connection to our problem**: Our function H(Q) involves products of group elements (plaquettes) and we want to maximize λ_max(H(Q)) over the group SU(N)^E. If we can reformulate this as an isospectral optimization problem (fix the spectrum of H and optimize over gauge orbits), the double bracket flow provides a complete solution.

**Key insight from Helmke-Moore**: For "linear functions" on adjoint orbits (trace functions of the form Tr(gAg†N)), the global convergence of double bracket flows is understood. The question is whether λ_max(H(Q)) has a similar structure.

### Bott's Result on Perfect Morse Functions via Double Brackets

Bott (1954, "Nondegenerate Critical Manifolds") showed that on compact groups G, functions obtained as f(g) = Tr(gNg†M) are Morse functions (or Morse-Bott) with the structure dictated by the root system of G. For G = SU(N), the Morse-Bott structure gives:
- Each critical manifold is a flag manifold
- The Morse index of each critical manifold is computable from the root system
- The function is a perfect Morse-Bott function

**For SU(2) ≅ S³**: f(U) = Re Tr(U·N) for diagonal N = diag(n₁, n₂) has critical points at U = I (minimum if n₁ < n₂) and U = [[0,-1],[1,0]] (maximum). Two critical points total — perfect Morse function.

---

## Section K: Application to Our Problem — Feasibility Assessment

### The Problem Setup

- M = SU(N)^E with bi-invariant metric
- f(Q) = λ_max(H(Q)) where H(Q) = Σ_plaquettes H_p(Q), each H_p smooth Hermitian
- Numerically confirmed: f achieves global max at Q = I, all gradient ascent → Q = I
- Numerically confirmed: Hess f at Q = I is negative-definite (local max confirmed)
- Numerically falsified: global geodesic concavity

### Framework Rankings by Applicability

**Framework 1: Compactness Obstruction (Sections A-B)**
- Status: **Confirms the obstacle** — global concavity is impossible by theorem, not just by numerical accident
- Action: This closes the geodesic concavity door permanently

**Framework 2: Morse Theory + Topology (Section D)**
★★★★★ **Highest promise**
- Key insight: On SU(2)^E ≅ (S³)^E, the Poincaré polynomial is (1+t³)^E. A Morse function has at most one critical point of index 3E (top index = global maximum). So if f is Morse and non-degenerate at Q = I (with Morse index 3E), then Q = I is the **only possible local maximum**, hence it must be the global maximum.
- Gap: Need to show f is a Morse function (all critical points non-degenerate) and that Q = I has Morse index 3E.
- What Morse index 3E means: The Hessian at Q = I must be negative-definite in ALL 3E tangent directions. This is the "negative-definite second variation" that has been numerically confirmed!
- **Key theorem to prove**: If Q = I is a Morse-index-3E critical point of f on SU(2)^E, and f is a Morse function, then Q = I is the unique global maximum.
- The negative-definite Hessian at Q = I gives the Morse index, but one still needs all critical points to be non-degenerate (generically true but needs verification).

**Framework 3: Trap-Free Landscape via Controllability (Section I)**
★★★★ **High promise**
- The Rabitz-Russell framework says: if the quantum control landscape analog is controllable (the map Q ↦ H(Q) satisfies a transversality condition), the landscape is trap-free.
- Applied to lattice Yang-Mills: the map Q ↦ H(Q) from SU(N)^E to Herm(V) needs to be "surjective enough" in some sense. If the differential dH at each Q spans a full-rank map to the relevant perturbation space, the trap-free result would apply.
- This is a generic result — "almost all" problems are trap-free. The question is whether lattice Yang-Mills is in the generic class.
- **Research path**: Formulate lattice Yang-Mills as a quantum control problem on SU(N)^E. Check whether the rank condition of the differential d(λ_max ∘ H) holds at all non-maximal critical points.

**Framework 4: Łojasiewicz / PL Condition (Section E)**
★★★ **Moderate promise for convergence; limited for global max certification**
- SU(N)^E is real analytic, so the Łojasiewicz inequality holds near every critical point. This gives: gradient ascent converges to some critical point.
- Does NOT by itself certify Q = I is the global max — just that gradient flow converges somewhere.
- However: if combined with Morse theory to eliminate other local maxima, Łojasiewicz provides the convergence rate.
- The global PL condition would certify global optimality, but verifying it globally is hard.

**Framework 5: Double Bracket Flow Reformulation (Section J)**
★★★ **Moderate promise for specific function classes**
- Best for "trace-type" functions, not directly for λ_max
- Would require reformulating λ_max as a variational problem over isospectral orbits
- Possible: λ_max(H(Q)) = max_{||v||=1} v†H(Q)v = max over rank-1 projectors P of Tr(P·H(Q))
- This makes it a joint optimization over Q and P, and the double bracket flow may apply to the (Q,P) problem jointly

**Framework 6: SDP Certificate (Section H)**
★★ **Works as numerical certification, not analytic proof**
- Can certify Q = I is globally optimal by checking a PSD matrix condition (from OTSM framework)
- Requires: setting up the SDP relaxation of the problem and verifying dual feasibility
- This would be a numerical certificate, not an analytical proof

### Most Promising Proof Strategy

**Recommendation: Morse Theory + Symmetry + Negative-Definite Hessian**

The cleanest path to a proof:

**Step 1 (Done numerically)**: Establish that Q = I is a non-degenerate critical point (negative-definite Hessian in all tangent directions).

**Step 2 (Hard)**: Prove that λ_max(H(Q)) is a PERFECT Morse function on SU(N)^E. If this holds, then c_{top} = b_{top} = 1, so Q = I is the unique local maximum.

**Alternatively (Symmetry Route)**:
- The gauge symmetry group G_gauge acts on SU(N)^E and f is invariant
- For a local maximum p, the entire gauge orbit G_gauge · p consists of local maxima
- If the gauge orbit of any secondary maximum is infinite (continuous), there would be a manifold of maxima, which for a Morse function is impossible
- If the gauge orbit is finite, then secondary maxima would come in finite families
- **Key fact**: Flat connections on a simply connected lattice (topologically) have gauge orbits that are discrete. For the square lattice with periodic boundary conditions, the gauge symmetry acts freely except at the flat connection Q = I (the center acts trivially on flat connections).
- This suggests the gauge orbit of Q = I consists only of gauge-equivalent flat connections, which are finitely many (indexed by the center Z(SU(N)) of size N).

**Gap in this approach**: The Morse condition (non-degenerate critical set) + gauge symmetry argument needs to be made precise for the specific lattice geometry. The structure of the critical set of λ_max(H(Q)) for non-flat Q is not fully characterized analytically.

---

## Section L: Summary of Key Findings

### Finding 1: Global Geodesic Concavity is Provably Impossible

Any smooth nonconstant function on SU(N)^E is NOT globally geodesically concave. This follows from the compactness of SU(N)^E and the maximum principle for superharmonic functions. The numerical falsification confirmed a mathematical certainty.

### Finding 2: Three Viable Frameworks for Certification

| Framework | Strength | Gap | Difficulty |
|-----------|----------|-----|------------|
| Morse Theory on (S³)^E | Directly applicable; clean topology | Verify Morse condition for f | Medium |
| Trap-Free (Rabitz-type) | Powerful; handles generic case | Verify controllability/transversality | Medium-Hard |
| Łojasiewicz + Morse | Gives convergence + uniqueness | Verify both conditions | Hard |
| Double Bracket Reformulation | Clean for trace functions | Extend to λ_max | Hard |
| SDP Certificate | Computational verification | Not analytic proof | Easy (numerical) |

### Finding 3: The Morse Theory Argument — Correct Statement

The fact that the Hessian at Q = I is numerically confirmed to be negative-definite means Q = I is a **non-degenerate local maximum** (top Morse index). But Morse theory alone does NOT guarantee uniqueness of the global maximum — the Euler characteristic constraint (χ(SU(2)^E) = 0) allows multiple local maxima if compensating saddle points exist.

**Uniqueness requires additional input**: either (a) prove λ_max is a perfect Morse function (c_{top} = b_{top} = 1), or (b) use symmetry to constrain the multiplicity of maxima, or (c) use the trap-free landscape approach to rule out non-global local maxima directly.

**The perfectness route has precedent**: Atiyah-Bott (1983) and Kirwan (1984) showed Yang-Mills is equivariantly perfect over surfaces. An analog for lattice gauge theory on SU(N)^E remains to be worked out.

### Finding 4: The Gauge Symmetry Argument

The gauge symmetry (constant gauge transformations) acts on SU(N)^E and f is invariant. Any gauge-equivalent configuration to Q = I (i.e., any configuration in the gauge orbit of I) is also a global max. Since the gauge orbit of I in the flat-connection moduli space consists only of flat connections with specific holonomy properties, and since SU(N) has finite center Z(SU(N)), the set of maxima is finite.

### Finding 5: Recent Literature Connecting to Our Problem

- arXiv:1608.06198 (Russell-Rabitz 2016): Trap-free quantum control landscapes — most directly applicable framework
- arXiv:2409.15139 (2024): Path-connectedness of optimal set — supports uniqueness
- PMC:8589322: OTSM global optimality certificate via SDP — computational certification approach
- Helmke-Moore (1994): Gradient flows on compact Lie groups — convergence theory
- Bloch-Brockett-Ratiu (1992): Double bracket flows — isospectral optimization

---

## Section M: What Could Not Be Resolved

1. **Whether λ_max(H(Q)) is a Morse function on SU(N)^E**: This requires showing all critical points are non-degenerate, which is a non-trivial analytic property of the specific function.

2. **Whether the Rabitz controllability condition applies to lattice Yang-Mills**: This requires checking the rank of d(λ_max ∘ H) at all critical points, which requires more detailed analysis of the plaquette structure.

3. **The exact count of saddle points**: The Poincaré polynomial (1+t³)^E implies the Euler characteristic χ = 0 for E ≥ 1 (since (1+(-1)³)^E = 0). A perfect Morse function on SU(2)^E has Σ_k (-1)^k c_k = χ = 0. The Morse numbers are c_{3k} = C(E,k) and c_j = 0 for j not divisible by 3. The alternating sum is Σ(-1)^{3k}C(E,k) = Σ(-1)^k C(E,k) = (1-1)^E = 0. Consistent!

4. **Gap between generic and specific**: The trap-free results hold "generically" (for almost all systems). Whether lattice Yang-Mills is in the generic class requires direct verification.

---

## Appendix: Explicit Formula for Convexity of λ_max

For completeness: λ_max is **convex** (not concave) as a function of Hermitian matrices (as a function H ↦ λ_max(H) on the vector space of Hermitian matrices). This is a standard result. The issue is that H is not a vector space variable here — it's evaluated at points on the Lie group, and the "convexity" of λ_max as a function of H does not translate directly to geodesic concavity of Q ↦ λ_max(H(Q)) when the map Q ↦ H(Q) is nonlinear.
