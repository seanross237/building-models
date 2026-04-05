# Literature Search: Connection Laplacian, Hessian Domination, and Yang-Mills Mass Gap

**Date:** 2026-03-28
**Search scope:** Seven topics related to bounding the covariant curl operator on lattices and the Yang-Mills mass gap.

---

## 1. "Connection Laplacian" Eigenvalue Bounds on Lattices

### 1a. Jiang, "Gauge theory on graphs" (arXiv:2211.17195, Nov 2022)

- **Authors:** Shuhan Jiang
- **Key result:** Defines connection 1-forms, curvature 2-forms, and a connection Laplacian on graphs. Proves a **discrete Weitzenböck formula** relating the connection Laplacian (Hodge-type) to the rough Laplacian plus curvature corrections. Also defines a discrete Yang-Mills functional and derives its Euler-Lagrange equations.
- **Relevance to bounding covariant curl:** This is the closest existing result to a discrete analogue of the continuum Weitzenböck identity `Delta_connection = Delta_rough + Ric + F` on lattices. The formula relates the "gauge-covariant Laplacian" to the scalar Laplacian plus curvature terms. In principle, if the curvature term is non-negative, the connection Laplacian is bounded below by the scalar Laplacian.
- **Operator domination M(Q) <= M(I)?** Not directly proved. The Weitzenböck formula gives a decomposition, not a comparison inequality. However, it provides the structural identity that such a comparison would need.
- **Connection Laplacian vs scalar Laplacian bound:** The Weitzenböck formula implies `lambda_1(connection) >= lambda_1(scalar) + min(curvature)`. For flat connections (zero curvature), the two Laplacians agree. For non-flat connections, the curvature correction can be either positive or negative depending on the sign of the curvature 2-form.

### 1b. Liu-Peyerimhoff, "Connection Laplacian on discrete tori with converging property" (arXiv:2403.06105, March 2024; J. Functional Analysis 289(3), 2025)

- **Authors:** Yong Liu, Norbert Peyerimhoff
- **Key result:** Proves that the rescaled eigenvalues of the connection Laplacian on discrete tori **converge** to those of the real torus as the mesh refines. The eigenvalues of the connection Laplacian on a real torus can be expressed in terms of standard Laplacian eigenvalues with a twist encoded in the torsion matrix (holonomy). Extends to heat kernels and log-determinants.
- **Relevance to bounding covariant curl:** Provides the rigorous connection between discrete and continuum connection Laplacians on tori. The eigenvalue formula shows that for flat connections (trivial holonomy), the connection Laplacian eigenvalues equal the scalar Laplacian eigenvalues. For non-trivial holonomy, eigenvalues shift by amounts determined by the torsion matrix.
- **Operator domination M(Q) <= M(I)?** Not addressed directly. However, the eigenvalue formula implies that **trivial holonomy maximizes certain spectral quantities**, since the torsion matrix shifts eigenvalues relative to the scalar case.
- **Connection Laplacian vs scalar Laplacian bound:** Explicit eigenvalue formula: `lambda_k(connection) = lambda_k(scalar Laplacian shifted by torsion)`. For trivial torsion (flat connection), these agree.

### 1c. Greensite-Olejnik-Polikarpov-Syritsyn-Zakharov, "Localized eigenmodes of the covariant lattice Laplacian" (arXiv:hep-lat/0509070, Sept 2005; Phys. Rev. D71, 114507, 2005)

- **Authors:** J. Greensite, S. Olejnik, M.I. Polikarpov, S.N. Syritsyn, V.I. Zakharov
- **Key result:** Numerical study of the eigenmode spectrum of the covariant lattice Laplacian in the fundamental SU(2) representation. Eigenmodes at the **lower and upper ends** of the spectrum are **localized** (finite localization volume in physical units set by string tension). The Faddeev-Popov operator eigenmodes are all extended. Localization disappears when center vortices are removed.
- **Relevance to bounding covariant curl:** Demonstrates that the covariant lattice Laplacian has a qualitatively different spectral structure than the scalar Laplacian (localization phenomenon). This is a cautionary result: the connection Laplacian is NOT simply a perturbation of the scalar Laplacian in typical gauge configurations.
- **Operator domination M(Q) <= M(I)?** Not addressed. The paper studies the fundamental (not adjoint) representation.
- **Connection Laplacian vs scalar Laplacian bound:** No explicit bound. The localization result implies the spectra can differ qualitatively.

---

## 2. "Discrete Covariant Laplacian" Spectral Bound

### 2a. Balaban, "Regularity and decay of lattice Green's functions" (Commun. Math. Phys. 89, 571-597, 1983)

- **Authors:** Tadeusz Balaban
- **Key result:** Proves that a class of lattice covariant Laplace operators with external gauge fields are positive, and their Green's functions **decay exponentially**. All bounds are **uniform in the lattice spacing**. Regularity properties parallel the continuous case.
- **Relevance to bounding covariant curl:** Provides the fundamental positivity and decay properties of the discrete covariant Laplacian needed for constructive field theory. The uniform bounds in lattice spacing are essential for taking the continuum limit.
- **Operator domination M(Q) <= M(I)?** Not in the form needed. Balaban's bounds are about positivity and decay, not comparison with the scalar Laplacian.
- **Connection Laplacian vs scalar Laplacian bound:** The covariant Laplacian is positive (like the scalar one), with exponential Green's function decay. No explicit eigenvalue comparison.

---

## 3. Lattice Gauge Theory Hessian Operator Domination

### 3a. Atlas Strategy-002 (this project), Exploration 008: Fourier-Hessian Proof

- **Key result (PROVED, Q=I):** For SU(N) Yang-Mills with action S = -(beta/N) Sum Re Tr(U_plaq), at the identity configuration Q=I:
  ```
  HessS(v,v)|_{Q=I} <= (2d beta / N)|v|^2
  ```
  giving H_norm = 1/12 for d=4, N=2. The bound is **tight**, achieved by the staggered mode v_{x,mu} = (-1)^{|x|+mu} v_0.

- **Key result (PROVED, all Q):** H_norm <= 1/8 for all Q via triangle inequality, giving mass gap at beta < 1/6 (8x SZZ, 4x CNS).

- **Operator domination M(Q) <= M(I)?** This is the **central open conjecture** of Strategy 003. At Q=I, M(I) = I_{N^2-1} tensor L, where L is the scalar discrete curl Laplacian. The conjecture states M(Q) is dominated (in PSD ordering) by M(I) for all Q. Proved for **uniform configurations** (all links equal). Numerically confirmed for 56 diverse configurations on L=2 and L=4 lattices with zero violations.

- **Structural finding:** Per-plaquette, the operator domination is FALSE (4 of 6 cross-term pairs have the wrong sign). The bound MUST use inter-plaquette cancellations from the lattice structure. This is why a per-plaquette proof is impossible and the lattice Weitzenböck identity or global argument is essential.

### 3b. No prior literature found

A thorough search found **no prior work** on:
- Proving M(Q) <= M(I) for the gauge-transported curl operator on lattices
- Fourier analysis of the discrete curl to bound the Hessian of the Wilson action
- The staggered mode as the Hessian maximizer
- The formula H_norm_max = ceil(d/2) floor(d/2) / (N^2 d(d-1))

**Verdict: The operator domination question appears to be NEW.**

---

## 4. "Bakry-Emery" Lattice Gauge Theory Mass Gap

### 4a. Shen-Zhu-Zhu (arXiv:2204.12737, CMP 400, 2023) -- see Section 5 below for full details

The foundational application of Bakry-Emery to lattice Yang-Mills. See Section 5.

### 4b. Cao-Nissim-Sheffield (arXiv:2509.04688, Sept 2025) -- see Section 6 below

Extends Bakry-Emery to sigma-model on vertices, doubling the threshold. See Section 6.

### 4c. Mondal, "A Geometric Approach to the Yang-Mills Mass Gap" (arXiv:2301.06996; JHEP 12, 191, 2023)

- **Authors:** Puskar Mondal
- **Key result:** Proposes that the regularized Bakry-Emery Ricci curvature of the **orbit space** (space of connections modulo gauge transformations) produces a mass gap for 2+1 and 3+1 dimensional Yang-Mills theory. The orbit space is equipped with a Riemannian metric from the reduced classical action with everywhere positive sectional curvature. Uses zeta-function regularization (following I.M. Singer) for the infinite-dimensional Ricci tensor.
- **Relevance to bounding covariant curl:** The orbit-space Bakry-Emery approach is conceptually related to but distinct from the SZZ lattice approach. SZZ works on the finite-dimensional configuration space SU(N)^E; Mondal works on the infinite-dimensional orbit space A/G. The positive curvature of the orbit space is related to the positive Ricci curvature of SU(N), but the regularization introduces additional subtleties.
- **Operator domination M(Q) <= M(I)?** Not directly relevant. The orbit-space approach does not decompose the Hessian into per-plaquette contributions.
- **Connection Laplacian vs scalar Laplacian bound:** Not addressed. The Laplace-Beltrami operator on the orbit space is the relevant operator, not the connection Laplacian on the lattice.
- **Status:** The result is described by the author as "at least heuristic" — it assumes the existence of a quantized Yang-Mills theory and uses formal regularization of infinite-dimensional operators.

### 4d. Bakry-Emery on Graphs (general theory)

- **Key references:**
  - Cushing-Liu-Peyerimhoff, "Bakry-Emery curvature functions on graphs" (Canadian J. Math., 2020)
  - Erbar-Maas, "Ricci curvature of finite Markov chains via convexity of entropy" (Arch. Ration. Mech. Anal. 206, 2012)
  - Fathi-Maas, "An entropic interpolation proof of the HWI inequality" (Stoch. Process. Appl. 130, 2020)
- **Key result:** Bakry-Emery curvature on graphs (discrete setting) implies spectral gap (Poincare inequality), log-Sobolev inequality, diameter bounds, and exponential concentration. For **Cartesian products** of graphs, the curvature of the product equals an abstract product of the curvatures — the product preserves the curvature lower bound.
- **Relevance:** The lattice configuration space SU(N)^E is a product of copies of SU(N). The Bakry-Emery condition on SU(N)^E inherits the curvature of each factor (Ric = N/2 per copy). The SZZ proof exploits exactly this product structure. The graph-theoretic Bakry-Emery literature provides the abstract framework that SZZ applies to Yang-Mills.

---

## 5. Shen-Zhu-Zhu, "A stochastic analysis approach to lattice Yang-Mills at strong coupling" (arXiv:2204.12737, CMP 400, 2023)

- **Authors:** Hao Shen, Rongchan Zhu, Xiangchan Zhu
- **Key result:** First mass gap result for continuous gauge groups. For SU(N) in d dimensions:
  ```
  K_S = N/2 - 8N(d-1)|beta| > 0  iff  |beta| < 1/(16(d-1))
  ```
  In d=4: **beta < 1/48** (strong coupling regime).

- **Technique:** Verify Bakry-Emery condition (positive Ricci curvature of configuration space) for lattice Yang-Mills Langevin dynamics. Two competing terms:
  - **Ricci curvature of SU(N):** Ric(u,u) = (N/2)|u|^2 (exact, from bi-invariant metric)
  - **Hessian of Wilson action (Lemma 4.1):** |HessS(v,v)| <= 8(d-1)N|beta||v|^2

- **Hessian bound derivation (the 8(d-1) factor):**
  - Diagonal contribution: 2(d-1)|beta| per edge (plaquette count)
  - Off-diagonal contribution: 6(d-1)|beta| (Holder + shared plaquettes)
  - Combined: 8(d-1)|beta|

- **Operator domination M(Q) <= M(I)?** Not addressed. SZZ uses a **worst-case bound** over all Q (the 8(d-1) factor). They do not compare M(Q) to M(I); they bound M(Q) independently for each Q using triangle inequalities.

- **Connection Laplacian vs scalar Laplacian bound:** Not directly. The Hessian bound is a uniform bound, not a comparison inequality. However, the structure at Q=I (Hessian = squared discrete curl) establishes the connection between the Hessian and the curl Laplacian.

- **Key limitation:** beta < 1/48 is the strong coupling regime, far from the physically relevant weak coupling/continuum limit. The SZZ Hessian bound (Lemma 4.1) is **12-170x loose** on Gibbs configurations (numerically verified by Atlas strategy-002 explorations 005-006).

---

## 6. Cao-Nissim-Sheffield, Lattice Yang-Mills Papers (2025)

### 6a. "Dynamical approach to area law for lattice Yang-Mills" (arXiv:2509.04688, Sept 2025)

- **Authors:** Sky Cao, Ron Nissim, Scott Sheffield
- **Key result (Theorem 1.6):** Wilson's area law for G in {U(N), SU(N), SO(2(N-1))} when:
  ```
  beta < 1/(8(d-1))  [i.e., beta < 1/24 in d=4 for SU(N) and U(N)]
  ```
  This **doubles** the SZZ threshold.

- **Technique:** Bakry-Emery on the **sigma-model on vertices** instead of Yang-Mills on edges. The vertex Hessian bound is 4(d-1)N*beta (half of SZZ's 8(d-1)N*beta for edges), because each vertex has 2(d-1) edges, and the diagonal + off-diagonal contributions total 4(d-1) instead of 8(d-1).

- **Area law derivation:** Uses Durhuus-Frohlich (1980) slab condition rather than Chatterjee's Definition 2.3. The sigma-model on a height-1 slab satisfies exponential decay of covariances uniform in boundary conditions A, B.

- **Operator domination M(Q) <= M(I)?** Not addressed. CNS uses the same type of worst-case Hessian bound as SZZ, just on a different formulation (vertices vs edges).

- **Connection Laplacian vs scalar Laplacian bound:** Not directly. The vertex formulation avoids the connection Laplacian entirely by working with the sigma-model.

- **Limitation:** String tension constant c decays with N.

### 6b. "Expanded regimes of area law for lattice Yang-Mills theories" (arXiv:2505.16585, May 2025)

- **Authors:** Sky Cao, Ron Nissim, Scott Sheffield
- **Key result (Theorem 1.2):** For G = U(N), there exists beta_0(d) > 0 (N-independent) such that area law holds for all beta <= beta_0(d) and all N >= 1:
  ```
  |<W_ell>| <= C_{1,d} C_N^{|ell|} exp(-C_{2,d} area(ell))
  ```
  Constants C_{1,d}, C_{2,d} depend only on d, not N.

- **Technique:** Master loop equations / string duality (completely distinct from Bakry-Emery). Curvature-free proof. Optimized ceiling: beta_0(4)_max = 1/(32e) ~ 1/87.

- **Operator domination M(Q) <= M(I)?** Not relevant. Different proof technique entirely.

### 6c. Cao, "U(N) lattice Yang-Mills in the 't Hooft regime" (arXiv:2510.22788, Oct 2025)

- **Authors:** Sky Cao (Note: earlier version attributed to Nissim; Cao is listed as author on arXiv)
- **Key result:** Mass gap, unique infinite volume limit, and large-N limit for U(N) lattice Yang-Mills in the 't Hooft regime. Overcomes the obstacle that U(N) has non-uniformly-positive Ricci curvature (unlike SU(N)). Recasts U(N) as random-environment SU(N) model with U(1) field.
- **Operator domination:** Not addressed.

---

## 7. "Weitzenböck Identity" Lattice Gauge Theory Discrete

### 7a. Jiang, "Gauge theory on graphs" (arXiv:2211.17195, 2022) -- see Section 1a above

This is the **primary reference** for a discrete Weitzenböck identity in gauge theory. The paper defines:
- Connection 1-forms on graphs (discrete parallel transport)
- Curvature 2-forms (discrete holonomy around faces)
- Connection Laplacian (gauge-covariant Laplacian on the graph)
- **Weitzenböck formula:** Relates the Hodge-type connection Laplacian to the rough Laplacian plus a curvature term

The Weitzenböck formula on graphs takes the form:
```
Delta_Hodge = Delta_rough + R
```
where R involves the curvature 2-form. This is the discrete analogue of the continuum identity relating the Hodge Laplacian on bundle-valued forms to the connection (rough) Laplacian plus Riemann curvature.

**Gap between this result and our needs:** Jiang works on general graphs with general connections. The specific question of whether the connection Laplacian eigenvalues are bounded by the scalar Laplacian eigenvalues (our M(Q) <= M(I)) requires additional analysis of the curvature term R. In particular:
- If R >= 0 (positive curvature), then lambda_k(connection) >= lambda_k(scalar), which gives the OPPOSITE direction from what we need
- Our inequality M(Q) <= M(I) corresponds to showing that the TOP eigenvalue of the connection Laplacian does not exceed the TOP eigenvalue of the scalar Laplacian -- this is about an UPPER bound, not a lower bound

The Weitzenböck identity alone does not resolve the question. It provides the structural decomposition, but the sign analysis of the curvature correction term in the specific lattice Yang-Mills setting is the open step.

### 7b. Continuum Weitzenböck / Bochner-Lichnerowicz (background)

The continuum Weitzenböck identity for bundle-valued 1-forms:
```
Delta_Hodge omega = nabla* nabla omega + Ric(omega) + F(omega)
```
where nabla* nabla is the rough (connection) Laplacian, Ric is the Ricci curvature of the base manifold, and F is the curvature of the connection acting on the form.

For Yang-Mills connections on flat space (Ric = 0):
```
Delta_Hodge omega = nabla* nabla omega + [F, omega]
```

The curvature term [F, omega] can have either sign. For self-dual connections in 4D (instantons), the curvature term has a definite sign that gives spectral bounds, but this is special to the self-dual case.

**No continuum result directly proves M(Q) <= M(I) for general connections.** The Weitzenböck identity is a decomposition, not a comparison.

---

## Summary Table

| Paper | Key Result for Bounding Covariant Curl | M(Q) <= M(I)? | Connection vs Scalar Laplacian Bound? |
|-------|---------------------------------------|----------------|--------------------------------------|
| Jiang (2022) | Discrete Weitzenböck formula on graphs | Not proved | Decomposition only (sign depends on curvature) |
| Liu-Peyerimhoff (2024) | Eigenvalue convergence on discrete tori | Not addressed | Trivial holonomy = scalar case; non-trivial shifts eigenvalues |
| Greensite et al. (2005) | Covariant Laplacian eigenmodes are localized | Not addressed | Spectra qualitatively different |
| Balaban (1983) | Covariant Laplacian positivity + exponential decay | Not addressed | Both positive; no eigenvalue comparison |
| SZZ (2023) | K_S = N/2 - 8N(d-1)beta; beta < 1/48 | Not addressed | Worst-case Hessian bound (not comparison) |
| CNS Sept 2025 | Doubled threshold beta < 1/24 via vertex sigma-model | Not addressed | Vertex formulation avoids connection Laplacian |
| CNS May 2025 | N-independent area law via master loops; beta_0 ~ 1/87 | Not relevant | Different technique |
| Mondal (2023) | Orbit-space Bakry-Emery (heuristic mass gap) | Not addressed | Orbit-space Laplacian (different operator) |
| **Atlas S002-E008** | **H_norm <= 1/12 at Q=I (proved); <= 1/8 all Q (proved)** | **Conjectured, proved for uniform Q** | **At Q=I: connection Lap = scalar Lap** |
| **Atlas S003-E001** | **M(Q) <= M(I) proved for uniform Q; zero violations on L=2,4** | **Numerically confirmed (56 configs)** | **Uniform Q: eigenvalues equal to scalar case** |

---

## Key Findings

### What exists in the literature:
1. **SZZ (2023):** Bakry-Emery mass gap at beta < 1/48 with a Hessian bound (Lemma 4.1) that is 12-170x loose
2. **CNS Sept 2025:** Doubled threshold to beta < 1/24 via vertex sigma-model reformulation
3. **CNS May 2025:** N-independent area law via master loop equations (different technique, weaker threshold ~1/87)
4. **Jiang (2022):** Discrete Weitzenböck formula on graphs (structural identity, not a comparison bound)
5. **Liu-Peyerimhoff (2024):** Connection Laplacian eigenvalue convergence on discrete tori
6. **Greensite et al. (2005):** Covariant lattice Laplacian eigenmodes are localized in SU(2) configurations
7. **Mondal (2023):** Heuristic orbit-space Bakry-Emery argument for mass gap

### What does NOT exist in the literature (appears novel):
1. The operator domination inequality M(Q) <= M(I) for the gauge-transported curl
2. The Fourier proof that H_norm = 1/12 at Q=I with the staggered mode as maximizer
3. The improved threshold beta < 1/6 (proved) or beta < 1/4 (conjectured)
4. Any explicit comparison between the connection Laplacian and scalar Laplacian eigenvalues that would bound the covariant curl operator in the Yang-Mills Hessian setting
5. The formula H_norm_max = ceil(d/2) floor(d/2) / (N^2 d(d-1))

### The exact gap remaining:
Proving Sum_plaq |B_plaq(Q,v)|^2 <= 4d |v|^2 for all Q in SU(N)^E. The closest tools in the literature are:
- **Jiang's discrete Weitzenböck formula** (provides the structural decomposition but not the sign control)
- **Liu-Peyerimhoff's eigenvalue formula** (shows trivial connection maximizes spectral quantities on tori, but only for flat connections)
- **The per-pair bound (2I + R + R^T) <= 4I for R in SO(3)** (proved in Atlas S003-E001 for uniform configs, needs extension to non-uniform)

The proof for general Q likely requires either:
1. A gauge-covariant Fourier analysis extending the Q=I proof
2. A geodesic concavity argument showing lambda_max(M(Q)) has its global maximum at Q=I
3. A direct application of the discrete Weitzenböck identity with sign control on the curvature term

---

## Full Bibliography

1. Balaban, T. "Regularity and decay of lattice Green's functions." Commun. Math. Phys. 89, 571-597 (1983).
2. Cao, S. "U(N) lattice Yang-Mills in the 't Hooft regime." arXiv:2510.22788 (Oct 2025).
3. Cao, S., Nissim, R., Sheffield, S. "Dynamical approach to area law for lattice Yang-Mills." arXiv:2509.04688 (Sept 2025).
4. Cao, S., Nissim, R., Sheffield, S. "Expanded regimes of area law for lattice Yang-Mills theories." arXiv:2505.16585 (May 2025).
5. Chatterjee, S. "A short proof of confinement in three-dimensional lattice gauge theories with a central U(1)." arXiv:2602.00436 (Jan 2026).
6. Chatterjee, S. "Yang-Mills for probabilists." arXiv:1803.01950 (2018).
7. Cushing, D., Liu, S., Peyerimhoff, N. "Bakry-Emery curvature functions on graphs." Canadian J. Math. (2020).
8. Greensite, J., Olejnik, S., Polikarpov, M.I., Syritsyn, S.N., Zakharov, V.I. "Localized eigenmodes of the covariant lattice Laplacian." arXiv:hep-lat/0509070; Phys. Rev. D71, 114507 (2005).
9. Jiang, S. "Gauge theory on graphs." arXiv:2211.17195 (Nov 2022).
10. Liu, Y., Peyerimhoff, N. "Connection Laplacian on discrete tori with converging property." arXiv:2403.06105; J. Funct. Anal. 289(3) (2025).
11. Mondal, P. "A geometric approach to the Yang-Mills mass gap." arXiv:2301.06996; JHEP 12, 191 (2023).
12. Shen, H., Zhu, R., Zhu, X. "A stochastic analysis approach to lattice Yang-Mills at strong coupling." arXiv:2204.12737; Commun. Math. Phys. 400, 805-851 (2023).
13. Adhikari, A., Cao, S. "Exponential decay of correlations in finite-group gauge theories." Ann. Prob. 53(1), 140-174 (2025). arXiv:2202.10375.
14. Rajasekaran, A., Yakir, O., Zhou, F. "Gaussian limits for all compact groups." arXiv:2603.24555 (March 2026).
