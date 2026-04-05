# Exploration 001: Classical Eigenvalue Concavity/Convexity Theorems — Report

## Goal Summary

Survey classical mathematical results on concavity/convexity of eigenvalue functions of matrix-valued maps. Catalog major theorems with precise statements, domain conditions, and applicability to functions on compact Lie groups. Key context: global geodesic concavity of λ_max(H(Q)) on SU(N)^E has already been numerically falsified.

**Motivating problem:** H(Q) is a smooth Hermitian-matrix-valued function on SU(N)^E. When is λ_max(H(Q)) concave in Q? How can we prove Q=I is a global max?

---

## Section 1: Davis (1957) Theorem — Convex Invariant Functions on Hermitian Matrices

### Result

**Theorem (C. Davis, 1957):** A function F defined on the space of n×n Hermitian matrices H_n is unitarily invariant (F(UAU*) = F(A) for all unitary U) and convex if and only if it is convex and symmetrically invariant when restricted to diagonal matrices.

**Equivalently:** Unitarily invariant convex functions on H_n are precisely functions of the form F(A) = f(λ(A)), where λ(A) = (λ₁,...,λₙ) are the ordered eigenvalues and f: ℝⁿ → ℝ is a symmetric convex function.

**Precise domain:** The space H_n of n×n Hermitian matrices, treated as a REAL VECTOR SPACE. Convexity is standard (Euclidean) convexity: F(tA + (1-t)B) ≤ tF(A) + (1-t)F(B).

**Key conclusion:** F is convex on H_n ↔ the symmetric function f of eigenvalues is convex. Same holds for concavity.

**Also:** Davis proved the operator version of Jensen's inequality: if f is operator convex (f(∑_k A_k* X_k A_k) ≤ ∑_k A_k* f(X_k) A_k for ∑ A_k*A_k = I), then f is convex on H_n, but the converse fails.

### Key Limitations

1. **Domain is a vector space, not a group.** The convexity is in the EUCLIDEAN sense over H_n as a vector space. It says nothing about functions Q ↦ f(λ(H(Q))) where H(Q) is a matrix function evaluated on a compact group.
2. **Direction is wrong for our problem:** On H_n, λ_max(A) is CONVEX (not concave), because it is the maximum of linear functions A ↦ ⟨v, Av⟩. The theorem would give concavity of λ_min, not λ_max.
3. **No manifold structure:** The result does not extend to Riemannian/geodesic convexity.

### References
- C. Davis, "All convex invariant functions of hermitian matrices," *Archiv der Mathematik* 8(4), 276–278 (1957).
- arXiv:math/0208223: Another simple proof.

---

## Section 2: Lewis (1996) Theorem — Convex Spectral Functions

### Background

Adrian Lewis extended and systematized Davis's result. A **spectral function** F: H_n → ℝ is one that depends only on eigenvalues: F(A) = f(λ₁(A), ..., λₙ(A)) where λ₁ ≥ λ₂ ≥ ... ≥ λₙ.

### Result

**Theorem (Lewis, 1996):** Let F = f∘λ be a spectral function on H_n. Then:
1. F is convex on H_n ↔ f is symmetric and convex on ℝⁿ.
2. F is concave on H_n ↔ f is symmetric and concave on ℝⁿ.
3. F is twice (continuously) differentiable at A ↔ f is twice (continuously) differentiable at λ(A).

**Domain:** H_n as a real vector space (symmetric matrices or Hermitian matrices).

**Key examples:**
- F(A) = λ₁(A) = λ_max(A): symmetric convex → CONVEX on H_n.
- F(A) = λₙ(A) = λ_min(A): symmetric concave → CONCAVE on H_n.
- F(A) = ∑_{k=1}^m λ_k(A) (sum of m largest): symmetric convex → CONVEX.
- F(A) = -∑_{k=n-m+1}^n λ_k(A) (negative sum of m smallest): symmetric convex → CONVEX.
- F(A) = Tr(A) = ∑λ_k: linear → both convex and concave.

**Fenchel conjugate formula:** Lewis also gave F*(B) = f*(λ(B)) via a simple duality formula, enabling subgradient computation.

### Key Limitations

1. **Domain is a vector space.** Applies to H_n as a real vector space. Does NOT apply to F(Q) = f(λ(H(Q))) where Q ∈ SU(N)^E.
2. **Convexity is Euclidean.** Even if H(Q) were linear in Q (it isn't), composing with λ_max would give a convex function — which is the wrong direction for proving Q=I is a global MAX.
3. **No manifold extension.** Lewis's 2003 paper "The mathematics of eigenvalue optimization" develops semidefinite programming connections, but does not extend spectral convexity to group manifolds.

### References
- A.S. Lewis, "Convex analysis on the Hermitian matrices," *SIAM J. Optim.* 6(1), 164–177 (1996).
- A.S. Lewis, "Derivatives of spectral functions," *Math. Oper. Res.* 21, 576–588 (1996).
- A.S. Lewis, "Twice differentiable spectral functions," *SIAM J. Matrix Anal. Appl.* 23(2), 368–386 (2001).
- A.S. Lewis, "The mathematics of eigenvalue optimization," *Math. Programming* 97, 155–176 (2003).

---

## Section 3: Ando (1979) Theorem — Concavity on Positive Definite Matrices

### Context

T. Ando's 1979 paper "Concavity of certain maps on positive definite matrices and applications to Hadamard products" proved Lieb's concavity theorem by a new real-variable method and established several new concavity/convexity results.

### Key Result: Lieb's Concavity Theorem (Ando's proof)

**Theorem (Lieb 1973, Ando's proof 1979):** For any fixed m×n matrix K and all 0 ≤ q ≤ 1, 0 ≤ r ≤ 1 with q+r ≤ 1:
- The map (A,B) ↦ Tr(K* A^q K B^r) is **jointly concave** in (A,B) on H_m^{++} × H_n^{++} (positive definite matrices).

**Ando's complement:** For 1 ≤ q ≤ 2, 0 ≤ r ≤ 1 with q-r ≥ 1:
- The map (A,B) ↦ Tr(K* A^q K B^{-r}) is **convex** on H_m^{++} × H_n^{++}.

**Ando's full theorem structure (1979):** If f is a positive function on (0,∞) that is operator monotone of all orders (in Löwner's sense) and Φ₁, Φ₂ are concave maps on positive definite matrices, then
(A,B) ↦ f[Φ₁(A)^{-1} ⊗ Φ₂(B)] · (Φ₁(A) ⊗ I)
is concave. This yields Lieb's concavity (A,B) ↦ A^{1-p} ⊗ B^p (0<p≤1) as a special case.

**Domain:** H_n^{++} (strictly positive definite matrices), which is an OPEN CONE, not a vector space and not a compact set. Convexity is standard Euclidean.

### What Ando Does NOT Do

- Does not address λ_max as an individual eigenvalue.
- Does not address functions on unitary/compact groups.
- Concerns TRACE functions (integrated over all eigenvalues), not individual eigenvalue extrema.

### Related: Generalization 2022+

Recent work (2022, Tandfonline) extends "Lieb-type convexity" for positive operator monotone decreasing functions. The core structure remains the same: trace functionals on positive definite matrices.

### References
- T. Ando, "Concavity of certain maps on positive definite matrices and applications to Hadamard products," *Linear Algebra Appl.* 26, 203–241 (1979).
- E.H. Lieb, "Convex trace functions and the Wigner-Yanase-Dyson conjecture," *Adv. Math.* 11, 267–288 (1973).

---

## Section 4: Löwner (1934) Theorem — Operator Monotone Functions

### The Theorem

**Theorem (K. Löwner, 1934):** A real-valued continuous function f: I → ℝ (I an interval) is **operator monotone** — meaning A ≥ B (as Hermitian matrices with eigenvalues in I) implies f(A) ≥ f(B) — if and only if f extends analytically to the upper half-plane with non-negative imaginary part (i.e., f is a **Pick function** / **Nevanlinna function**).

**Equivalent integral representation:** f is operator monotone on (0,∞) iff
  f(t) = at + b + ∫₀^∞ t/(t+s) dμ(s)
for some a ≥ 0, b ∈ ℝ, and a positive Borel measure μ.

**Examples of operator monotone functions:** f(t) = t^α for 0 < α ≤ 1; f(t) = log t; f(t) = t/(1+t).

**The Löwner-Heinz inequality:** If A ≥ B ≥ 0 then A^α ≥ B^α for all α ∈ [0,1].

### Connection to Operator Convexity

**Theorem (Bendat-Sherman, Krauss):** f is operator convex on I if and only if t ↦ f(t) is convex in the classical sense AND f has a particular second-order condition. More precisely:
- f is operator convex on (0,∞) iff t ↦ f(t)/t is operator monotone on (0,∞).
- Every operator monotone function is operator concave.

**Jensen's Operator Inequality (Davis 1957, Hansen-Pedersen 1982):** If f is operator convex, C_k are contractions with ∑ C_k*C_k = I, and X_k are operators with spectra in I, then:
  f(∑_k C_k* X_k C_k) ≤ ∑_k C_k* f(X_k) C_k.

### Key Limitations for Our Problem

1. **Operator monotone / operator convex** is about functions of a SINGLE operator, not about functions of a group element Q.
2. These results characterize how f(A) ≥ f(B) when A ≥ B as matrices — this is operator ordering, not a statement about maximizing over a manifold.
3. No direct connection to λ_max of a matrix-valued function on a group.
4. The characterization (Pick functions) is beautiful mathematically but does not extend to domains with curvature.

### References
- K. Löwner, "Über monotone Matrixfunktionen," *Math. Z.* 38, 177–216 (1934).
- B. Simon, *Loewner's Theorem on Monotone Matrix Functions*, Springer 2019.
- R. Bhatia, *Matrix Analysis*, Springer 1997 (authoritative textbook reference).

---

## Section 5: Fan's Inequality and Weyl's Inequality

### Fan's (Ky Fan) Inequality

**Theorem (Ky Fan, 1951):** For Hermitian matrices A and B and any 1 ≤ k ≤ n:
  λ₁(A+B) + ... + λ_k(A+B) ≤ [λ₁(A) + ... + λ_k(A)] + [λ₁(B) + ... + λ_k(B)]

where λ₁ ≥ ... ≥ λₙ are eigenvalues in decreasing order.

**Consequence:** The sum of the k largest eigenvalues is **subadditive**, hence **convex** as a function on H_n. In particular, λ_max = λ₁ is subadditive and convex.

**Fan's Dominance Theorem:** For A, B ∈ H_n, the inequalities ‖A‖_{(k)} ≤ ‖B‖_{(k)} (1 ≤ k ≤ n), where ‖·‖_{(k)} is the Ky Fan k-norm (sum of k largest singular values), hold if and only if ‖A‖ ≤ ‖B‖ for all unitarily invariant norms.

**From Tao's notes (Proposition 3):** The map A ↦ λ₁(A) + ... + λ_k(A) is **convex** on H_n; dually, A ↦ λ_{n-k+1}(A) + ... + λₙ(A) is **concave**. These are "the next best thing to linear" — minimax expressions.

### Weyl's Inequality

**Theorem (Weyl, 1912; extended by Ky Fan):** For Hermitian n×n matrices A and B:
  λ_{i+j-1}(A+B) ≤ λ_i(A) + λ_j(B) for i+j-1 ≤ n.

**Operator norm perturbation bound:** For any i:
  |λ_i(A+B) - λ_i(A)| ≤ ‖B‖_{op}

**Consequence:** Individual eigenvalues are Lipschitz functions of the matrix (with Lipschitz constant 1 in the operator norm). This is stability, not convexity or concavity.

### Limitations for Our Problem

1. Fan's inequality gives **convexity** of λ_max on the vector space H_n — the WRONG direction for proving a maximum.
2. Weyl's inequality gives STABILITY (Lipschitz bound), not concavity.
3. Neither result extends to functions on compact groups.
4. These are perturbation results for matrices as a vector space.

---

## Section 6: Matrix Convexity — Operator Convex/Concave Functions

### Definitions

A function f: I → ℝ is **operator convex** if for all n, all A,B ∈ H_n with eigenvalues in I, and 0 < λ < 1:
  f(λA + (1-λ)B) ≤ λf(A) + (1-λ)f(B)    (matrix inequality ≤ in Loewner order)

This is STRONGER than scalar convexity: f(t) = t² is operator convex; f(t) = t³ is NOT operator convex.

Key operator convex functions on [0,∞): t², -t^α (0 < α ≤ 1), -log t.
Key operator concave functions on [0,∞): t^α (0 < α ≤ 1), log t.

### Jensen's Operator Inequality (Matrix Jensen)

**Theorem (Davis 1957 / Hansen-Pedersen 1982):** f is operator convex on I if and only if for all self-adjoint contractions C₁,...,C_m with ∑C_k*C_k = I and self-adjoint X₁,...,X_m with spectra in I:
  f(∑_k C_k* X_k C_k) ≤ ∑_k C_k* f(X_k) C_k    (matrix inequality)

### What Operator Convexity Implies for Eigenvalues

If f is operator convex, then by the Davis-Lewis result, A ↦ Tr f(A) is convex on H_n (trace of operator convex functions gives scalar convex functions). However, this concerns TRACE (sum of all eigenvalues), not λ_max.

**Key fact:** Operator convexity does NOT imply convexity of λ_max as a SCALAR function, except trivially through the Davis-Lewis characterization.

### Schur-Convexity Connection

A symmetric function g: ℝⁿ → ℝ is Schur-convex if it is nondecreasing under majorization. By Davis-Lewis, F = g∘λ is convex on H_n if g is symmetric and convex; g being Schur-convex is a related but different condition.

---

## Section 7: Kostant Convexity Theorem and AGS — Compact Lie Groups

This section addresses the classical results for eigenvalue-like functions on compact Lie groups directly.

### Kostant's Convexity Theorem (1973)

**Theorem (Kostant):** Let K be a connected compact Lie group with Lie algebra k, maximal torus T with Lie algebra t, and Weyl group W. Let P: k → t be the orthogonal projection onto the Cartan subalgebra (in an Ad-invariant inner product). Then for any X ∈ k:
  P(Ad(K)·X) = convex hull of {w(X) : w ∈ W}

**In matrix terms:** For Hermitian matrices, this says: the set of diagonal parts of all unitary conjugates of a fixed Hermitian matrix A is the convex hull of all permutations of the eigenvalues of A. This is the **Schur-Horn theorem**.

**What it gives:** This is a convexity result about PROJECTIONS of orbits, not about eigenvalue functions per se. It implies that the "diagonal entries" (and hence certain linear eigenvalue functionals) have convex image.

**Domain:** Compact connected Lie group K acting on its Lie algebra by adjoint action. This IS a compact group setting!

**Limitation:** This is about the image of a projection being convex — it's a geometric statement about orbits, not about maximizing λ_max(H(Q)) over a group.

### Atiyah-Guillemin-Sternberg (AGS) Convexity Theorem (1982)

**Theorem (Atiyah; Guillemin-Sternberg 1982):** Let (M, ω) be a compact connected symplectic manifold with a Hamiltonian action of a torus T = U(1)^k, and let μ: M → t* be the moment map. Then:
  μ(M) is a convex polytope (= convex hull of the images of fixed points of T).

**Connection to eigenvalues:** The sum ∑_{i=1}^m λ_i(A) for Hermitian matrices is a moment map for the U(m) action on a Grassmannian. The convexity theorem then recovers the convexity of eigenvalue sums.

**What it gives for our problem:** If the Yang-Mills action or its Hessian eigenvalue function can be realized as a moment map component, the AGS theorem would give convexity of its image over the group. BUT:
1. This gives convexity of the IMAGE (range of values), not concavity of the function itself.
2. The domain for AGS is a SYMPLECTIC manifold with HAMILTONIAN structure; SU(N)^E with the Yang-Mills action is not obviously in this form.
3. This gives a MAXIMUM over the entire group (boundary of the polytope), which is the WRONG direction for showing a flat connection is a GLOBAL MAX of λ_max.

### References
- B. Kostant, "On convexity, the Weyl group and the Iwasawa decomposition," *Ann. Sci. Éc. Norm. Sup.* 6, 413–455 (1973).
- M.F. Atiyah, "Convexity and commuting Hamiltonians," *Bull. London Math. Soc.* 14, 1–15 (1982).
- V. Guillemin, S. Sternberg, "Convexity properties of the moment mapping," *Invent. Math.* 67, 491–513 (1982).

---

## Section 8: Recent Results on Compact/Unitary Groups (2016-2026)

### Result 1: Convexity of Sums of Eigenvalues of Unitaries (2024)

**Paper:** "Convexity of sums of eigenvalues of a segment of unitaries," arXiv:2408.16906, published *Linear Algebra and Applications* 2025.

**Setting:** A path in the unitary group of the form u(t) = e^{itx}e^{iy}, where x, y are self-adjoint matrices. This is a "geodesic segment" in U(n) for any bi-invariant metric.

**Main Theorem (Theorem 3.3):** If ||u(t) - I|| < √2 throughout the interval and all eigenvalues e^{iθ_k(t)} are distinct with θ₁ > ... > θₙ, then:
  t ↦ ∑_{k=1}^m θ_k(t)  is **convex** for each 1 ≤ m ≤ n.

**Extended version (Theorem 3.9):** By limiting argument, convexity extends to the case of collapsing eigenvalues.

**Optimality:** The condition ||u(t) - I|| < √2 (equivalently, all eigenvalues in the open upper hemisphere of the unit circle) is OPTIMAL — the result fails outside this neighborhood.

**Mechanism:** The second derivative formula is
  d²/dt² ∑_{k=1}^m θ_k(t) = 2∑_{k≤m, j>m} [sin(θ_k - θ_j)/|e^{iθ_k} - e^{iθ_j}|²] |⟨xv_k, v_j⟩|²
Each summand is non-negative when all angles θ_k are in (-π/2, π/2), i.e., when ||u(t) - I|| < √2. The proof is purely analytic (second variation formula), not geometric.

**Application to SU(N):** The result extends to SU(N) via Ad-invariant Finsler norms. This applies to paths in SU(N), not to eigenvalues of separate matrix functions.

**Direct relevance to our problem:**
- This gives convexity of the TOP eigenvalue phase θ₁(t) of u(t) as a function of t — i.e., λ_max of the unitary group element u(t) (in angle).
- This is CONVEXITY, not concavity. To use this for proving a maximum, one would need a different argument.
- This does NOT directly address λ_max(H(Q)) for a separately defined matrix function H.

**Critical observation:** The condition ||u(t)-I|| < √2 means the path stays within the "upper hemisphere" of U(n). Global geodesic concavity fails exactly when paths go OUTSIDE this region — consistent with the existing numerical falsification.

### Result 2: Geodesic Convexity of Eigenvalue Problem on Positive Definite Matrices (2024)

**Paper:** "Geodesic Convexity of the Symmetric Eigenvalue Problem and Convergence of Steepest Descent," *J. Optim. Theory Appl.* 2024, also PMC11530568.

**Setting:** Symmetric positive definite matrices with Riemannian metric. Block Rayleigh quotient f(X) = -Tr(X^T A X) on the Grassmann manifold.

**Key Theorem (A.1):** Full geodesic convexity holds in a neighborhood B* of the global minimizer where sin²(θ_k) ≤ δ/(λ₁ + λ_k) (δ = eigengap).

**Important correction:** The authors note that a prior claim of gap-independent convexity is WRONG (Corollary 5 of a previous paper), and provide a counterexample. The corrected theorem shows convexity necessarily depends on the eigengap.

**What it gives:** Local geodesic convexity near the minimizer on the Grassmannian, with a size that depends on the eigengap.

**Relevance:** Confirms the pattern that global geodesic concavity/convexity fails but LOCAL results can hold near critical points.

### Result 3: Convexity and Concavity of Eigenvalue Sums — Spectral Shift Function

**Paper:** Hundertmark-Simon (arXiv:math/0112279, 2001), *J. Functional Analysis*.

**Result:** The spectral shift function integrated from -∞ to λ is concave with respect to trace-class perturbations. For finite matrices: the sum of the k SMALLEST eigenvalues is CONCAVE in A (viewed as a function on H_n).

This is the converse of Fan's inequality: while the sum of k LARGEST eigenvalues is convex, the sum of k SMALLEST is concave.

**Domain:** Self-adjoint operators on Hilbert space, trace-class perturbations.

---

## Section 9: Gaps — What Prevents Application to SU(N)^E

### Fundamental Obstacle: Domain Mismatch

All classical results (Davis, Lewis, Fan, Weyl, Löwner, Ando) operate on:
- H_n as a VECTOR SPACE (Euclidean convexity)
- H_n^{++} as an OPEN CONE (Euclidean convexity or positive definite structure)

Our problem lives on:
- SU(N)^E, a COMPACT MANIFOLD (no global convex structure)

This is not just a technical difference. Key obstruction:
- On a vector space, λ_max is CONVEX (it's a max of linear functions). This is useful for MINIMIZATION but we need MAXIMIZATION.
- On a compact group, there is no global notion of "convex" that matches the Euclidean theory.
- The AGS/Kostant results give convexity of orbit images, not function values.

### Mismatch Between Classical Results and Needed Result

What we WANT: λ_max(H(Q)) is GEODESICALLY CONCAVE on SU(N)^E → global max at Q=I.
What we HAVE from classical theory: λ_max is CONVEX on H_n (Euclidean, vector space sense).

These point in opposite directions. The classical results are not just "not applicable" — they suggest that proving concavity would require exploiting special structure of H(Q), not just eigenvalue theory alone.

### The Compound Function Problem

Even if we had good results about geodesic concavity of eigenvalue functions on groups, we would need to compose:
- Q ∈ SU(N)^E (group element, curved domain)
- Q ↦ H(Q) (a matrix-valued function that involves plaquette products and inverse operations)
- H(Q) ↦ λ_max(H(Q)) (eigenvalue extraction)

The final composition of a curved-domain map with a convex spectral function is not controlled by any classical theorem.

### What the 2024 Unitary Result Suggests

The result of arXiv:2408.16906 shows that along geodesic segments in U(n) NEAR THE IDENTITY (||u-I|| < √2), eigenvalue sums ARE convex. This means:
- Concavity of eigenvalue sums fails GLOBALLY on SU(N) (since the group wraps around).
- Near the identity, CONVEXITY (not concavity!) holds.
- If our H(Q) can be expressed as a function of the eigenvalues of Q itself (which it cannot in general), we might use this.

**The key gap:** The relevant result gives convexity of eigenvalue sums of u(t) as a function of the parameter t. This is NOT the same as convexity/concavity of λ_max(H(Q)) as a function of Q ∈ SU(N)^E.

---

## Section 10: Closest Applicable Theorem

**Best candidate for restricted/local concavity:** The 2024 paper (arXiv:2408.16906) + local second-variation analysis.

**Reasoning:**
1. At Q = I (flat connection), the second variation of λ_max(H(Q)) is known to be negative-definite (the flat connection is a LOCAL maximum). This is LOCAL geodesic concavity at Q = I.
2. The 2024 result gives CONVEXITY of eigenvalue sums of group elements within the upper hemisphere (||u-I|| < √2). This is CONVEXITY near identity, not concavity.
3. These two facts are in tension: the second derivative of λ_max(H(Q)) (in the Hessian sense) is negative at Q=I, suggesting local concavity of λ_max∘H; but the pure-group result gives local convexity of eigenvalue sums of u itself.
4. The resolution: H(Q) is NOT the same as the eigenvalue function of Q. H(Q) is a derived matrix, and its eigenvalue behavior is different.

**Most directly applicable classical result:**
Fan's inequality / Lewis's theorem shows that if we could express λ_max(H(Q)) as a convex function of H(Q) and H(Q) as a concave function of Q (in some linear sense), then the composition would be monotone. But neither part of this decomposition holds in general.

**For local-to-global:** The strongest available tool is a combination of:
(a) Local concavity at Q=I (to be verified/proved rigorously by second variation)
(b) A topological/degree-theoretic argument (unique critical point implies global max on compact group)
(c) Gradient ascent convergence (numerical evidence that all trajectories converge to Q=I)

---

## Section 11: Has Anyone Applied These Theorems to Lattice Gauge Theory?

**Short answer: No direct applications found.**

Extensive search found no papers applying Davis-Lewis, Ando, Löwner, Fan/Weyl, AGS/Kostant theorems to:
- Lattice Yang-Mills Hessian eigenvalue functions
- λ_max of any gauge-theory-related matrix function
- Eigenvalue optimization on SU(N)^E specifically

The literature on lattice Yang-Mills theory (Chatterjee, Cao-Nissim-Sheffield, Shen-Zhu-Zhu) addresses mass gap and other properties via probabilistic and stochastic methods, not via the classical matrix convexity literature.

The optimization-on-manifolds literature (Lewis, Overton) addresses eigenvalue optimization on vector spaces or positive definite cones, not compact groups.

**One indirect connection:** The Yang-Mills Hessian involves the Weitzenbock formula, which relates to Laplacians and curvature. Spectral theory of these operators could in principle connect to operator-theoretic results, but no concrete theorem is available.

---

## Summary Table

| Theorem | Domain | What it says | Type | Applicable to SU(N)^E? |
|---------|--------|--------------|------|----------------------|
| Davis 1957 | H_n (vector space) | Unitarily inv. convex ↔ sym. convex of eigenvalues | Characterization | No — wrong domain |
| Lewis 1996 | H_n (vector space) | F = f∘λ convex ↔ f sym. convex | Characterization | No — wrong domain |
| Fan 1951 | H_n (vector space) | Sum of k largest eigenvalues is convex | Convexity | No — λ_max is convex (wrong direction) |
| Weyl 1912 | H_n (vector space) | Eigenvalue Lipschitz stability | Perturbation bound | No — stability only |
| Ando 1979 | H_n^{++} (pos. def.) | Tr(K*A^q KB^r) jointly concave | Concavity | No — trace functions only |
| Löwner 1934 | H_n (any dim) | f operator monotone ↔ f is Pick function | Characterization | No — single operator theory |
| Kostant 1973 | Compact Lie group K | P(Ad(K)·X) = convex hull of Weyl orbit | Orbit projection | Partial — wrong question |
| AGS 1982 | Symplectic + Hamiltonian | Moment map image is convex polytope | Orbit image | Partial — wrong question |
| 2024 (arXiv:2408.16906) | U(n) geodesic segments near I | θ_1+...+θ_m is convex when ‖u-I‖ < √2 | Restricted convexity on group | Nearest — but gives CONVEXITY, not concavity |
| 2024 (PMC11530568) | Grassmannian manifold | Eigenvalue problem is locally geodesically convex near minimizer | Local geodesic | No — different problem |

---

## Section 12: Key Takeaway

**The classical matrix convexity/concavity literature does not contain a theorem that directly proves geodesic concavity of λ_max(H(Q)) on a compact group.**

The fundamental obstruction is the domain gap: classical results live on vector spaces or open cones; our problem lives on a compact manifold SU(N)^E. Furthermore, even on vector spaces, λ_max is CONVEX (useful for minimization), not concave (needed for proving a global maximum).

**What IS available:**
1. Local concavity at Q=I can potentially be proved by direct second-variation computation (negative Hessian of λ_max∘H at the flat connection). This is supported by existing numerical evidence.
2. The 2024 unitary result (arXiv:2408.16906) gives a restricted CONVEXITY result for eigenvalue sums of group elements near identity — interesting but not directly the needed concavity.
3. The AGS/Kostant framework provides a theoretical backdrop for why eigenvalue functions on compact groups have constrained behavior, but does not give the needed result.

**Most promising path forward:** NOT full global concavity (already falsified), but rather:
- Prove local concavity at Q=I (second variation argument)
- Prove no other local maxima exist (topological/structural argument using the specific form of H(Q))
- Combine these for global maximality

OR: Explore whether the Schur-Horn/Kostant framework can be applied to the SPECIFIC structure of the Yang-Mills Hessian (plaquette sum structure), which might provide restricted concavity along specific submanifolds (e.g., torus-aligned directions).

---

## References (Full List)

- C. Davis, "All convex invariant functions of hermitian matrices," *Archiv der Mathematik* 8, 276–278 (1957).
- K. Löwner, "Über monotone Matrixfunktionen," *Math. Z.* 38, 177–216 (1934).
- E.H. Lieb, "Convex trace functions and the Wigner-Yanase-Dyson conjecture," *Adv. Math.* 11, 267–288 (1973).
- T. Ando, "Concavity of certain maps on positive definite matrices and applications to Hadamard products," *Linear Algebra Appl.* 26, 203–241 (1979).
- M.F. Atiyah, "Convexity and commuting Hamiltonians," *Bull. London Math. Soc.* 14, 1–15 (1982).
- V. Guillemin and S. Sternberg, "Convexity properties of the moment mapping," *Invent. Math.* 67, 491–513 (1982).
- B. Kostant, "On convexity, the Weyl group and the Iwasawa decomposition," *Ann. Sci. Éc. Norm. Sup.* 6, 413–455 (1973).
- A.S. Lewis, "Convex analysis on the Hermitian matrices," *SIAM J. Optim.* 6, 164–177 (1996).
- A.S. Lewis and M.L. Overton, "Eigenvalue optimization," *Acta Numerica* 5, 149–190 (1996).
- D. Hundertmark and B. Simon, "Concavity of eigenvalue sums and the spectral shift function," *J. Functional Analysis* (2001); arXiv:math/0112279.
- B. Simon, *Loewner's Theorem on Monotone Matrix Functions*, Springer 2019.
- R. Bhatia, *Matrix Analysis*, Springer 1997.
- T. Tao, "254A Notes 3a: Eigenvalues and sums of Hermitian matrices" (2010 lecture notes).
- arXiv:2408.16906, "Convexity of sums of eigenvalues of a segment of unitaries" (2024).
- PMC11530568, "Geodesic Convexity of the Symmetric Eigenvalue Problem and Convergence of Steepest Descent," *J. Optim. Theory Appl.* (2024).
