# Subproblem B: Eigenvector Regularity and the Coalescence Problem

**Date:** 2026-04-02
**Context:** Strain-Vorticity Alignment GMT approach to 3D Navier-Stokes regularity (Angle 10).

---

## 0. Summary of Findings

The coalescence set where eigenvalues of the strain tensor S coincide has **codimension 2 generically** in R^3 (it forms curves), not codimension 1 as stated in the initial exploration document. This is a significant upgrade for the GMT approach. Away from coalescence, eigenvectors inherit the regularity of the velocity field (smooth if u is smooth, H^{k-2} if u is in H^k). Near coalescence, eigenvectors rotate by pi/2 over distances proportional to the eigenvalue gap, causing gradient blowup but preserving L^p integrability. The alignment angle angle(omega, e_2) is ill-defined on the coalescence set, but there exist smooth reformulations --- most importantly the scalar quantity omega . S omega / |omega|^2 --- that capture the same physical content without any eigenvector regularity requirement. **The coalescence problem does not kill the GMT approach**, provided the approach is reformulated to use these smooth scalar quantities rather than the alignment angle directly.

---

## 1. Eigenvalue Coalescence Set Structure

### 1.1. The Space of Real Symmetric 3x3 Matrices

The strain tensor S(x,t) = (nabla u + (nabla u)^T)/2 at each point is a real symmetric 3x3 matrix. The space Sym_3(R) of such matrices has dimension 6. The ordered eigenvalues s_1 >= s_2 >= s_3 are continuous functions of the matrix entries, and the discriminant locus where eigenvalues coincide has a well-understood structure.

**The von Neumann-Wigner theorem (1929).** In the space Sym_n(R) of real symmetric n x n matrices, the set of matrices with a repeated eigenvalue has codimension 2. For n = 3, Sym_3(R) has dimension 6, and the set {s_1 = s_2} union {s_2 = s_3} has dimension 4 (codimension 2 in the 6-dimensional space).

*Proof sketch for n = 3.* A symmetric 3x3 matrix A has eigenvalues determined by its characteristic polynomial p(lambda) = -lambda^3 + (tr A) lambda^2 - (1/2)((tr A)^2 - tr(A^2)) lambda + det A. The condition for a repeated root is that the discriminant Delta(A) vanishes. For a 3x3 matrix, the discriminant is:

Delta = 18 a b c d - 4 b^3 d + b^2 c^2 - 4 a c^3 - 27 a^2 d^2

where the characteristic polynomial is written as -lambda^3 + b lambda^2 - c lambda + d. This is a single polynomial equation in the 6 matrix entries, so naively the zero set has codimension 1. But the discriminant factors: Delta = (s_1 - s_2)^2 (s_2 - s_3)^2 (s_1 - s_3)^2 / 27, and the zero set {Delta = 0} = {s_1 = s_2} union {s_2 = s_3}. Each branch {s_i = s_j} is smooth, and the key point is that Delta vanishes to **second order** on each branch. A function that vanishes to second order on a smooth submanifold defines a submanifold of codimension determined by the rank of its Hessian restricted to the normal directions.

More directly: the condition s_i = s_j imposes that the matrix A commutes with a specific rank-1 perturbation. By Arnold's analysis (1971, "Modes and quasimodes"), one can parametrize a neighborhood of a matrix with s_1 = s_2 > s_3 as follows. The eigenspace for the double eigenvalue is 2-dimensional, spanned by orthonormal vectors v_1, v_2. A nearby matrix has the form:

A = (s + a) v_1 v_1^T + (s + d) v_2 v_2^T + b (v_1 v_2^T + v_2 v_1^T) + s_3 v_3 v_3^T + (perturbation rotating the eigenframe)

The splitting of the double eigenvalue to first order is governed by the 2x2 matrix [[a, b], [b, d]], whose eigenvalues are s +/- sqrt(((a-d)/2)^2 + b^2). The coalescence condition is a = d AND b = 0, which is **two independent equations**. Hence codimension 2 in the parameter space.

**Conclusion:** The codimension of the eigenvalue coalescence set in Sym_3(R) is 2.

### 1.2. For Spatial Families: Codimension in R^3

Now consider the strain tensor S(x) as a smooth map S: R^3 -> Sym_3(R). The coalescence set in physical space is:

C = {x in R^3 : s_1(x) = s_2(x)} union {x in R^3 : s_2(x) = s_3(x)}

By the parametric transversality theorem (or, more directly, by the preimage theorem applied to the discriminant), for a **generic** smooth map S: R^3 -> Sym_3(R), the coalescence set C is a smooth submanifold of codimension 2 in R^3, i.e., **C consists of smooth curves in R^3**.

More precisely: define the maps f_12: R^3 -> R^2 and f_23: R^3 -> R^2 that encode the two coalescence conditions (in the Arnold normal form, f_12(x) = (a(x) - d(x), b(x)) where a, b, d are the entries of the 2x2 splitting matrix for the s_1, s_2 pair). For a generic smooth S, the maps f_12 and f_23 are transverse to the origin, and their zero sets are smooth 1-dimensional submanifolds (curves) in R^3.

**The triple coalescence set** {s_1 = s_2 = s_3}: this requires s_1 = s_2 AND s_2 = s_3, imposing 4 independent conditions (2 for each pair, minus 1 for the redundancy of the trace constraint... but actually the full triple coalescence requires that S is a scalar multiple of the identity, i.e., S = (s/3) I with s = tr S = 0 from incompressibility, so S = 0). For incompressible flow, triple coalescence requires S(x) = 0 at x. This is codimension 5 in Sym_3(R) (a zero-trace symmetric matrix has 5 independent entries, all of which must vanish). For a generic spatial family, the preimage S^{-1}(0) is empty (codimension 5 > dim R^3 = 3).

**Conclusion for generic smooth S:**
- {s_1 = s_2} and {s_2 = s_3} are each smooth curves in R^3 (codimension 2).
- {s_1 = s_2 = s_3} = {S = 0} is generically empty in R^3.

**This corrects an error in the original angle-10 exploration**, which stated that eigenvalue coalescence is "a codimension-1 phenomenon" (Section 4, Fatal Problem 3). That claim is wrong. The codimension is 2, not 1. The coalescence set consists of **curves**, not surfaces.

### 1.3. Constraints from Divergence-Free Velocity Fields

For S derived from a smooth divergence-free velocity u (i.e., S_ij = (partial_i u_j + partial_j u_i)/2 with div u = 0), there are additional constraints:

1. **Trace constraint:** tr S = div u = 0, so s_1 + s_2 + s_3 = 0. This reduces the effective dimension of the target from 6 to 5 (trace-free symmetric matrices).

2. **Compatibility conditions.** Not every trace-free symmetric matrix field arises as the symmetric gradient of a divergence-free vector field. The strain tensor must satisfy the Saint-Venant compatibility conditions (it must be the symmetrized gradient of some vector field) AND the divergence-free condition. Specifically, S is determined by u through a first-order differential operator, and u is determined by omega = curl u (up to harmonic components) through Biot-Savart. So S is not freely specifiable; it is constrained by the elliptic system:

   -Delta u = curl omega, div u = 0

   and S = sym(nabla u). This means the entries of S satisfy additional differential relations (beyond being a smooth matrix field).

3. **Effect on genericity.** The compatibility conditions are open differential constraints, and the question is whether they force the map x -> S(x) to be non-transverse to the coalescence locus. The key result here is:

**Claim:** For a generic smooth divergence-free velocity field u, the eigenvalue coalescence set of S = sym(nabla u) still has codimension 2 in R^3.

*Argument:* The map u -> S = sym(nabla u) is a surjective first-order differential operator from divergence-free vector fields to trace-free symmetric matrix fields (surjectivity follows from the theory of the deformation tensor: given any smooth trace-free symmetric matrix field S, one can find a divergence-free u with sym(nabla u) = S, at least locally, by solving a Poisson system). Since the operator is surjective, the image is dense in C^infty, and transversality to the codimension-2 coalescence locus is a generic property (by the Thom transversality theorem applied in function spaces). The differential constraints do not reduce the codimension below 2.

However, for **specific** solutions of the Navier-Stokes equations (as opposed to arbitrary divergence-free fields), the strain tensor S evolves according to:

(partial_t - nu Delta) S_ij = -(S_ik S_kj + (1/4)(omega_i omega_j - |omega|^2 delta_ij)) - partial_i partial_j p + ...

This evolution equation couples S to itself and to omega in a specific way. The question is whether the NS dynamics can **drive** the eigenvalue coalescence set to be codimension less than 2 (e.g., force coalescence to occur on surfaces rather than curves). This is extremely unlikely for the following reason: the coalescence codimension is a **topological** property of the map S(x), and the NS evolution is a smooth PDE that deforms S continuously. A smooth deformation of a map that is transverse to a codimension-2 submanifold remains transverse (transversality is an open condition). So for smooth NS solutions with generic initial data, the coalescence set maintains codimension 2 for all t in [0,T].

**Conclusion:** For smooth solutions of 3D NS with generic initial data, the eigenvalue coalescence set of S consists of smooth curves in R^3 at each time t.

### 1.4. Time-Dependent Considerations

For the space-time coalescence set C_ST = {(x,t) in R^3 x [0,T] : s_1(x,t) = s_2(x,t) or s_2(x,t) = s_3(x,t)}, the analysis extends straightforwardly. The map (x,t) -> S(x,t) is smooth from R^4 to Sym_3^0(R) (trace-free symmetric matrices). The coalescence locus has codimension 2 in the target. For a generic map from R^4, the preimage has codimension 2 in R^4, i.e., it forms **surfaces** in space-time (2-dimensional submanifolds of R^4). This is consistent with the spatial picture: at each time t, the coalescence set is generically a collection of curves in R^3, and as t varies these curves sweep out surfaces in R^4.

---

## 2. Eigenvector Regularity Away from Coalescence

### 2.1. Classical Perturbation Theory

**Theorem (Rellich 1937, Kato 1976).** Let A(x) be a smooth (C^k, analytic) family of real symmetric n x n matrices parametrized by x in R^m. On the open set where all eigenvalues of A(x) are simple, the eigenvectors can be chosen to depend smoothly (C^k, analytically) on x.

*Proof sketch:* If s_j(x_0) is a simple eigenvalue with eigenvector e_j(x_0), the implicit function theorem applied to the system F(x, s, e) = (A(x) e - s e, |e|^2 - 1) gives smooth dependence of (s_j, e_j) on x in a neighborhood of x_0. The non-degeneracy condition is exactly that s_j is simple.

**For the NS strain tensor:** If u in C^infty(R^3 x [0,T]), then S(x,t) is a smooth family of symmetric matrices, and on the set R^3 \ C(t) (complement of the coalescence set at time t), each eigenvector e_j(x,t) is a smooth function of x.

### 2.2. Sobolev Regularity: From u in H^k to e_j in H^{k-2}

The eigenvectors of S(x) depend on S through the implicit function theorem, and the regularity loss comes from two sources:

1. **Differentiation loss.** S = sym(nabla u), so S has one fewer derivative than u: if u in H^k, then S in H^{k-1}.

2. **Nonlinear loss.** The eigenvectors are nonlinear functions of the matrix entries. On the set where eigenvalues are bounded away from coalescence (i.e., min_{i != j} |s_i - s_j| >= delta > 0), the eigenvectors are smooth (Lipschitz, C^infty) functions of the matrix entries. But the Lipschitz constant of the map "matrix -> eigenvector" is proportional to 1/gap, where gap = min_{i != j} |s_i - s_j|. Precisely:

**Lemma (Davis-Kahan sin(theta) theorem, 1970).** If A, B are real symmetric matrices with eigenvalue s_j(A) simple and separated from the rest of the spectrum by gap delta_j = min_{i != j} |s_i(A) - s_j(A)|, then the angle between the corresponding eigenvectors satisfies:

sin(angle(e_j(A), e_j(B))) <= ||A - B|| / delta_j

**Consequence for Sobolev regularity.** If u in H^k(R^3) with k >= 3, then S in H^{k-1}(R^3). On the set Omega_delta = {x : min_{i != j} |s_i(x) - s_j(x)| >= delta}, the eigenvector e_j is a Lipschitz function of S with Lipschitz constant O(1/delta), and therefore:

||nabla e_j||_{L^2(Omega_delta)} <= C/delta ||nabla S||_{L^2} <= C/delta ||u||_{H^3}

More generally, on Omega_delta:
- e_j in H^{k-1}(Omega_delta) if u in H^k, with bounds degenerating as delta -> 0.
- The m-th derivative of e_j involves (schematically) products of derivatives of S divided by powers of the eigenvalue gaps: nabla^m e_j ~ sum_{l=0}^{m} nabla^{m-l} S / (gap)^{l+1}.

**Precise statement:** For u in H^k(R^3) with k >= 3, on the set Omega_delta, the eigenvector e_j satisfies:

||e_j||_{H^s(Omega_delta)} <= C(delta, ||u||_{H^k}) for s <= k - 2

The loss of 2 derivatives (from H^k for u to H^{k-2} for e_j) comes from: 1 derivative to form S = sym(nabla u), and 1 derivative lost in the implicit function theorem step (the eigenvector equation involves S, so differentiating e_j involves differentiating S and dividing by the gap).

### 2.3. Behavior Near Coalescence: The Key Degeneracy

Near the coalescence set, eigenvectors undergo rapid rotation. Let us analyze this in detail for the case s_1 = s_2 at a point x_0.

**Local model (Arnold normal form).** Near x_0 where s_1(x_0) = s_2(x_0) = s > s_3(x_0), the restriction of S to the 2D eigenspace {e_1, e_2} has the form (to leading order):

M(x) = s I_2 + [[a(x), b(x)], [b(x), -a(x)]]

where a, b are smooth functions vanishing at x_0 (since s_1 = s_2 at x_0). The eigenvalues are s +/- r(x) where r(x) = sqrt(a(x)^2 + b(x)^2).

The eigenvectors of M(x) in the 2D subspace are:

e_+(x) = (cos(phi/2), sin(phi/2)), e_-(x) = (-sin(phi/2), cos(phi/2))

where phi(x) = arctan(b(x)/a(x)).

**Critical observation:** As x traverses a small loop around the coalescence curve (where a = b = 0), the angle phi increases by 2*pi, so the eigenvectors rotate by pi. This is the famous **eigenvalue crossing monodromy**: the eigenvectors acquire a sign flip when transported around the coalescence set.

**Regularity consequences:**

1. **phi(x) = arctan(b/a)** has a singularity at a = b = 0 (the coalescence set). In polar coordinates (a,b) = r(cos theta, sin theta), we have phi = theta, so phi is the angular coordinate around the coalescence curve. This means:

   |nabla phi| ~ 1/dist(x, C)

   where C is the coalescence curve. Since C has codimension 2, the integral integral |nabla phi|^p dx converges for p < 2 in 3D (by comparison with integral_0^R (1/r)^p r dr in 2D polar coordinates transverse to C):

   integral |nabla phi|^p dx ~ integral_0^R r^{1-p} dr < infty iff p < 2

2. **Therefore:** The eigenvectors e_1, e_2 are in W^{1,p}(R^3) for all p < 2, but NOT in H^1 = W^{1,2}.

   More precisely: nabla e_j ~ (1/r) where r = dist(x, C), and since C is a 1-dimensional curve in R^3, the integral integral |nabla e_j|^p dx ~ integral_C (integral_0^{R} rho^{1-p} rho d rho) dl converges for p < 2.

3. **The eigenvectors are in BV(R^3) (functions of bounded variation).** The jump set of e_j is a surface spanning the coalescence curve (a "Seifert surface" of the curve), across which e_j jumps by the monodromy sign flip. The total variation is finite because the jump has fixed magnitude (a sign flip, i.e., an O(1) jump) across a codimension-1 surface.

   Actually, let me be more careful. The eigenvectors are multi-valued: as one goes around the coalescence curve, they acquire a sign flip. To define them as single-valued functions, one must introduce a branch cut (a surface bounded by the coalescence curve) across which the eigenvectors jump. The BV norm of e_j is then bounded by the area of this branch cut surface, which is finite for a smooth coalescence curve in a bounded domain.

### 2.4. Summary of Eigenvector Regularity

For u in H^k(R^3) with k >= 3, and with the coalescence set C having codimension 2 (smooth curves):

| Quantity | Regularity | Notes |
|---|---|---|
| Eigenvalues s_1, s_2, s_3 | H^{k-1} (same as S) | Continuous functions of matrix entries, Lipschitz |
| Eigenvectors e_j on R^3 \ C | C^{k-2} (smooth if u smooth) | By implicit function theorem |
| Eigenvectors e_j globally | W^{1,p} for p < 2, BV | Not in H^1; gradient blows up as 1/dist(x,C) |
| Alignment angle angle(omega, e_j) | Same as e_j: W^{1,p} p < 2, BV | Plus orientation ambiguity |

---

## 3. The Alignment Angle as a Distributional Object

### 3.1. The Orientation Ambiguity

The eigenvectors e_j are defined only up to sign (e_j and -e_j are both valid choices). The angle angle(omega, e_j) is therefore only defined modulo the replacement theta -> pi - theta. The quantity cos(angle(omega, e_j)) flips sign under e_j -> -e_j.

To avoid this ambiguity, one should work with:

cos^2(angle(omega, e_j)) = (omega . e_j)^2 / |omega|^2

This is well-defined (independent of the sign choice for e_j) and is a smooth function of x on R^3 \ C.

### 3.2. Behavior of cos^2(angle(omega, e_2)) Near Coalescence

At a point x_0 where s_1 = s_2 > s_3, the eigenspace for the double eigenvalue s_1 = s_2 is 2-dimensional. Any unit vector in this 2D subspace is a valid choice for e_1 or e_2. The decomposition of omega into components along e_1 and e_2 is ambiguous: only the total projection onto the 2D eigenspace is well-defined.

Specifically:

(omega . e_1)^2 + (omega . e_2)^2 = |P_{12} omega|^2

where P_{12} is the orthogonal projection onto the eigenspace span{e_1, e_2}. This projection P_{12} is a **smooth** function of x (it depends on the eigenspace, not on the choice of basis within it). Therefore:

- (omega . e_1)^2 + (omega . e_2)^2 is smooth across the coalescence set {s_1 = s_2}.
- (omega . e_1)^2 and (omega . e_2)^2 individually are NOT continuous across the coalescence set (they exchange values as the eigenvectors rotate).
- (omega . e_3)^2 / |omega|^2 = cos^2(angle(omega, e_3)) IS smooth across {s_1 = s_2}, because e_3 (the eigenvector for the non-degenerate eigenvalue s_3) is smooth there.

Similarly, across {s_2 = s_3}, the eigenvector e_1 is smooth (non-degenerate eigenvalue), and (omega . e_1)^2 is continuous, while (omega . e_2)^2 and (omega . e_3)^2 are individually discontinuous but their sum (omega . e_2)^2 + (omega . e_3)^2 = |P_{23} omega|^2 is smooth.

**Conclusion:** cos^2(angle(omega, e_2)) is **not continuous** across either branch of the coalescence set. It jumps when s_1 = s_2 (where e_2 becomes ambiguous in the {e_1, e_2} plane) and when s_2 = s_3 (where e_2 becomes ambiguous in the {e_2, e_3} plane).

### 3.3. BV Structure of the Alignment Angle

Since the eigenvectors are in BV(R^3), the alignment angle theta_j(x) = arccos(|omega . e_j| / |omega|) is in BV(R^3) away from {omega = 0}. The jump set of theta_2 consists of branch cuts for the eigenvectors, which are surfaces bounded by the coalescence curves.

The total variation of theta_2 is bounded by the area of the branch cut surfaces times the jump magnitude. The jump magnitude is O(1) (a finite rotation in the eigenspace), so the BV norm is controlled by the geometry of the coalescence set.

However, BV regularity is generally insufficient for GMT arguments that require level-set estimates (co-area formula, Hausdorff dimension of level sets). The co-area formula does hold in BV, but the resulting level set estimates are weaker than those available for Sobolev functions.

### 3.4. Distributional Formulation: Possible but Weak

One can define the alignment angle theta_2 in the distributional sense as a BV function. It satisfies:

nabla theta_2 = (regular part) + (singular part supported on branch cuts)

The regular part is in L^p for p < 2 (as computed in Section 2.3). The singular part is a measure supported on the branch cut surfaces.

For GMT applications, the relevant question is whether the level sets {theta_2 = c} have controlled Hausdorff dimension. For a BV function in R^3, the co-area formula gives:

integral_0^{pi/2} H^2({theta_2 = c}) dc = |nabla theta_2|(R^3) < infty

so for a.e. c, the level set {theta_2 = c} has finite 2-dimensional Hausdorff measure. But this does not give dimension estimates for specific level sets; it is an averaged statement.

**Verdict:** The alignment angle theta_2 can be defined distributionally (in BV), but the resulting regularity is likely insufficient for the GMT arguments envisioned in the full program.

---

## 4. Reformulation Options: Smooth Scalar Quantities

The key insight is that the GMT approach does not actually need the alignment angle per se. What it needs is a quantity that:
(a) measures how much vortex stretching is self-limiting (i.e., how much the stretching is controlled by the intermediate eigenvalue rather than the largest),
(b) is smooth for smooth u (no coalescence singularities),
(c) has enough structure for GMT level-set arguments.

### 4.1. The Enstrophy Production Rate

The most natural smooth quantity is the **normalized enstrophy production rate**:

Q(x) = omega . S omega / |omega|^2 = sum_i s_i cos^2(theta_i)

where theta_i = angle(omega, e_i). This is a smooth function of x for smooth u (it depends only on omega and S = sym(nabla u), both of which are smooth). No eigenvector computation is needed:

Q(x) = (omega^T S omega) / (omega^T omega)

**Properties of Q:**
- Q is smooth wherever omega != 0.
- Q satisfies s_3 <= Q <= s_1 (by the min-max characterization of eigenvalues applied to the Rayleigh quotient).
- Q = s_2 if and only if omega is exactly aligned with e_2 (when s_2 is simple).
- Q = s_1 if and only if omega is aligned with e_1.
- The "dangerous" regime (strong positive stretching) is Q close to s_1.
- The "safe" regime (self-limiting stretching) is Q close to s_2 or Q < 0.

**Connection to the alignment angle:** The alignment angle theta_2 = angle(omega, e_2) can be recovered (away from coalescence) from Q via:

cos^2(theta_2) = (Q - s_1)(Q - s_3) / ((s_2 - s_1)(s_2 - s_3))   ... [when eigenvalues are distinct]

But this recovery is unnecessary. The quantity Q directly measures what the GMT approach needs (the effective stretching rate), without the detour through eigenvectors.

### 4.2. The Stretching Deficit

Define the **stretching deficit**:

D(x) = s_1(x) - Q(x) = s_1 - omega . S omega / |omega|^2 >= 0

This measures how far the actual stretching rate is from the maximum possible stretching rate. D = 0 when omega is aligned with e_1 (worst case); D = s_1 - s_2 when aligned with e_2; D = s_1 - s_3 when aligned with e_3.

D is continuous (as a function of x) because both s_1 and Q are continuous. However, s_1 is only Lipschitz (not C^1) at eigenvalue coalescence {s_1 = s_2}, so D has Lipschitz regularity at best. Still, Lipschitz is sufficient for many GMT arguments (Lipschitz functions have a well-behaved co-area formula with rectifiable level sets).

Actually, we need to be more careful about the regularity of s_1. The ordered eigenvalue s_1(x) = max eigenvalue of S(x) is a convex function of the matrix entries (the max of linear functions in a suitable sense), and therefore:

- s_1 is locally Lipschitz (by convexity).
- s_1 is C^1 where s_1 > s_2 (simple eigenvalue).
- s_1 is NOT C^1 at {s_1 = s_2} in general (the gradient has a corner).

So D = s_1 - Q is Lipschitz but not C^1 across {s_1 = s_2}.

### 4.3. The Strain-Vorticity Tensor (Full Smooth Alternative)

Instead of using any scalar reduction, one can work directly with the vector:

W(x) = S(x) omega(x)

This is a smooth vector field (for smooth u) with no eigenvector issues whatsoever. Its magnitude and direction encode all the strain-vorticity interaction:

- omega . W = omega . S omega = Q |omega|^2 (the enstrophy production).
- |W|^2 = sum_i s_i^2 cos^2(theta_i) |omega|^2 (weighted stretching).
- The angle between W and omega encodes the alignment information: cos(angle(W, omega)) = Q / sqrt(sum_i s_i^2 cos^2(theta_i)).

The tensor S omega is the object that appears directly in the vorticity equation:

D_t omega = S omega + nu Delta omega     (the stretching term is exactly S omega)

so working with S omega is not an artificial reformulation; it is the natural object from the PDE itself.

### 4.4. Comparison of Reformulation Options

| Quantity | Smoothness | Captures alignment info? | Suitable for GMT? |
|---|---|---|---|
| theta_2 = angle(omega, e_2) | BV, W^{1,p} (p<2) | Directly, but with ambiguity | Weak (BV co-area) |
| cos^2(theta_2) | Discontinuous at coalescence | Yes, modulo orientation | No (not even BV on its own) |
| Q = omega . S omega / \|omega\|^2 | C^infty (where omega != 0) | Yes (Q = s_2 iff aligned with e_2) | Yes (smooth co-area) |
| D = s_1 - Q | Lipschitz | Yes (D = 0 iff aligned with e_1) | Yes (Lipschitz co-area) |
| S omega | C^infty | Full information | Yes (smooth vector field) |

**The clear winner is Q = omega . S omega / |omega|^2**: it is smooth, it directly encodes the stretching rate, it avoids all eigenvector issues, and it is the natural quantity from the PDE.

---

## 5. Does the GMT Approach Survive with the Reformulated Quantity?

### 5.1. Level Sets of Q

For the GMT approach, one needs to study the level sets {Q(x) = c} and the sublevel sets {Q(x) >= c} (the "dangerous" regions of strong stretching). Since Q is smooth where omega != 0, the standard co-area formula and Sard's theorem apply:

- For a.e. value c in [s_3, s_1], the level set {Q = c} is a smooth 2-dimensional submanifold.
- The sublevel sets {Q >= c} are open sets with smooth boundary for a.e. c.
- The Hausdorff dimension of {Q = c} is exactly 2 for generic c (by the implicit function theorem).

The GMT approach can now be reformulated as: study the set

{|omega(x)| > M} intersect {Q(x) >= s_1(x) - epsilon}

(the high-vorticity, near-maximally-stretched region) and show that it has small Hausdorff dimension or measure.

### 5.2. The Critical Question: Does Directional Information Survive?

The original GMT approach distinguished between "aligned with e_1" (dangerous) and "aligned with e_2" (safe). The reformulation using Q partially preserves this:

- Q close to s_1: omega nearly aligned with e_1 (dangerous).
- Q close to s_2: omega nearly aligned with e_2 (safe, self-limiting stretching).
- Q < 0: net compression (safe).

However, there is a loss of information. When s_1 = s_2 (at coalescence), Q close to s_1 and Q close to s_2 become the same condition. This means the reformulation cannot distinguish "dangerous alignment" from "safe alignment" at coalescence points. But at coalescence, s_1 = s_2, so the stretching rate is the same whether omega aligns with e_1 or e_2 --- there is no distinction to be made. The directional information is genuinely absent at coalescence because there is no physically meaningful distinction between the two eigenvectors.

**Conclusion:** The directional information loss at coalescence is not a problem --- it corresponds to the physical reality that at coalescence, there is no preferred dangerous vs. safe direction.

### 5.3. Evolution Equation for Q

Since Q = omega . S omega / |omega|^2 is a smooth scalar, one can derive its evolution equation from the NS equations. Writing omega_hat = omega/|omega| (the vorticity direction, well-defined where omega != 0):

Q = omega_hat . S omega_hat

Using the evolution equations for omega and S:

D_t Q = omega_hat . (D_t S) omega_hat + 2 (D_t omega_hat) . S omega_hat

The first term involves the pressure Hessian and the strain self-interaction:

D_t S = nu Delta S - S^2 - (1/4)(omega tensor omega - |omega|^2 I/3) - Hess(p) + ...

The second term involves the evolution of the vorticity direction, which is:

D_t omega_hat = (S - Q I) omega_hat / |omega| + nu (Delta omega - (Delta |omega| / |omega|) omega) / |omega|
            ... [more precisely, the projection of (S omega + nu Delta omega)/|omega| perpendicular to omega_hat]

This gives a closed (albeit complicated) evolution equation for Q in terms of smooth quantities. The fact that Q satisfies a PDE makes it a legitimate object for GMT analysis (e.g., one can apply parabolic regularity theory, maximum principles, etc., to Q, or study its level sets using the implicit function theorem for solutions of parabolic PDEs).

### 5.4. What is Lost Compared to the Original Formulation

The reformulation from theta_2 to Q is not entirely without cost:

1. **The partition into "aligned" and "misaligned" sets becomes a partition into "{Q close to s_2}" and "{Q close to s_1}"**, which is a partition by stretching rate rather than by geometric alignment. This is arguably more natural from the PDE perspective (what matters is the stretching rate, not the geometric angle), but it loses the topological/geometric structure of vortex tubes that the original formulation tried to exploit.

2. **The "1D regularity on tubes" argument** cannot be directly phrased in terms of Q. The original argument relied on the aligned set being geometrically tube-like (1-dimensional). The set {Q close to s_2} has no reason to be tube-like; it is defined by a scalar inequality and is generically a 3D region with 2D boundary. The dimensional reduction that the original approach sought is not available through Q alone.

3. **The GMT dimensional estimates** on the "dangerous" set {Q close to s_1, |omega| > M} can be pursued, but they require understanding the joint behavior of two smooth quantities (Q and |omega|), which is a co-dimension question for a smooth map R^3 -> R^2. The expected dimension of {Q = c_1} intersect {|omega| = c_2} is 1 (a curve in R^3, for generic values c_1, c_2). But the set {Q >= s_1 - epsilon, |omega| > M} is an open set, not a level set, and its dimension is 3.

This last point reveals a structural issue: **the GMT dimensional reduction in the original approach was trying to show that a specific open set is "thin" (dimension < 3), but open sets in R^3 have dimension 3 by definition.** The only way around this is to show that the set has small **measure** (not small dimension), which is a different type of estimate.

---

## 6. Rigorous Assessment: Kill Condition Evaluation

Recall the kill condition for Subproblem B:

> If the coalescence set is codimension 1 (expected generically) AND the alignment angle has essential discontinuities across it that prevent any useful distributional formulation, then the GMT approach as stated is dead and needs a fundamentally different object.

### 6.1. The Coalescence Set is Codimension 2 (Not 1)

The first clause of the kill condition is **not triggered**. The coalescence set has codimension 2 (curves in R^3), which is much better than the feared codimension 1 (surfaces). This means:

- The set where eigenvectors are ill-defined is 1-dimensional, not 2-dimensional.
- Eigenvectors are smooth on an open dense set whose complement has measure zero.
- The gradient singularity (1/distance to coalescence curve) is L^p-integrable for p < 2.

### 6.2. The Alignment Angle Has Discontinuities, but Smooth Reformulations Exist

The second clause is **partially triggered**: the alignment angle theta_2 does have essential discontinuities (sign ambiguity, branch cuts) across the coalescence set. The quantity cos^2(theta_2) = (omega . e_2)^2 / |omega|^2 is discontinuous at both branches of the coalescence set.

However, the smooth reformulation Q = omega . S omega / |omega|^2 completely avoids this problem while retaining the essential physical content (the stretching rate). The GMT approach can be reformulated entirely in terms of Q.

### 6.3. Verdict: The GMT Approach is NOT Killed by Eigenvector Coalescence

The coalescence problem does **not** kill the GMT approach. Specifically:

1. The coalescence set is thin enough (codimension 2) that it does not pose a topological obstruction.
2. Smooth reformulations exist that capture the same stretching physics without any eigenvector issues.
3. The reformulated quantity Q satisfies a PDE derived from NS, making it amenable to PDE-based GMT analysis.

However, the reformulation changes the character of the GMT approach:

- **The alignment-based partition** (into tube-like aligned regions and thin misaligned regions) is no longer available in its original form. The reformulation works with stretching-rate sublevel sets rather than geometric alignment sets.
- **The "1D regularity on tubes" argument** (which was the original approach's main payload) does not translate to the Q-based reformulation. The set {Q approximately s_2} is not a union of tubes; it is a generic open set.
- **The dimensional reduction** sought by the original approach (showing the "dangerous" set has dimension < 3) is structurally impossible for open sets. The reformulation shifts the question to **measure estimates** (showing the dangerous set has small measure) rather than dimension estimates.

---

## 7. Implications for the Broader GMT Approach

### 7.1. What Survives

1. The quantity Q = omega . S omega / |omega|^2 is a smooth, well-defined scalar that directly measures the vortex stretching rate.
2. The level sets of Q are smooth submanifolds (for generic values), amenable to GMT analysis.
3. Q satisfies a parabolic PDE derived from NS, so regularity theory and maximum-principle-type arguments can be applied.
4. The self-limiting stretching mechanism (Q bounded by s_2 when omega aligns with e_2) is captured by Q without eigenvector ambiguity.

### 7.2. What is Lost or Weakened

1. The geometric partition into "aligned tubes" and "misaligned regions" is lost. The reformulation cannot exploit the 1D tube structure of high-vorticity regions.
2. The dimensional reduction from 3 to lower dimension for the dangerous set is not achievable through Q alone (the dangerous set {Q close to s_1, |omega| large} is generically open, hence dimension 3).
3. The connection to the Constantin-Fefferman condition (which involves the geometric regularity of the vorticity direction) is weakened: Q encodes the stretching rate but not the full geometric content of the vorticity direction field.

### 7.3. Honest Bottom Line

The eigenvector coalescence problem is **solvable** (by reformulation to Q), but the cure is worse than the disease in one important respect: the reformulation strips away the geometric content (tube structure, alignment directions) that gave the original GMT approach its power. What remains is a smooth scalar (the stretching rate Q) that satisfies a PDE and measures how dangerous the local dynamics are. This is a perfectly legitimate object of study, but analyzing it is essentially equivalent to understanding the enstrophy production term omega . S omega, which is the central object of the classical NS regularity theory. The reformulation has not circumvented the core difficulty; it has repackaged it.

The approach is **not killed** by the coalescence problem, but it is **significantly weakened**. The original vision --- using the geometric structure of alignment sets as a GMT tool for dimensional reduction --- requires the alignment angle itself, and the alignment angle is too irregular (BV, not Sobolev). The smooth alternative Q is analytically tractable but does not support the geometric arguments that were the approach's raison d'etre.

**Recommendation for the next subproblem (C):** The conditional regularity theorem should be stated in terms of Q directly:

> "If Q(x,t) <= s_2(x,t) + delta * (s_1(x,t) - s_2(x,t)) on the set {|omega| > M} for some delta < 1 and all t in [0,T], then the solution is regular on [0,T]."

This is a clean, well-posed conditional regularity question that avoids all eigenvector issues and directly expresses the "self-limiting stretching" mechanism. It is equivalent to saying that in high-vorticity regions, the stretching rate Q is bounded away from its maximum value s_1, i.e., the vorticity is not too closely aligned with the most stretching direction. This subsumes and refines the Constantin-Fefferman condition in the specific direction suggested by DNS evidence.

---

## Appendix A: Key References and Precedents

**Eigenvalue perturbation theory:**
- Rellich, F. (1937). "Storungstheorie der Spektralzerlegung." Key result: analytic dependence of eigenvalues/vectors on parameters for analytic families.
- Kato, T. (1976). *Perturbation Theory for Linear Operators*, 2nd ed. Comprehensive treatment of eigenvalue perturbation; Chapter II for finite-dimensional theory.
- von Neumann, J. and Wigner, E. (1929). "Uber merkwurdige diskrete Eigenwerte." Established codimension-2 for eigenvalue crossings of real symmetric matrices.
- Arnold, V.I. (1971). "Modes and quasimodes." Normal form for eigenvalue crossings in parametric families.

**Eigenvalue crossings in matrix families:**
- Arnold, V.I. (1972). "Matrices depending on parameters." Proved that for generic k-parameter families of real symmetric n x n matrices, eigenvalue crossings form submanifolds of codimension 2 in parameter space (for real crossings). For k = 3 (spatial dimension), crossings form curves.
- Teytel, M. (1999). "How rare are multiple eigenvalues?" Quantitative transversality results for eigenvalue crossings.

**Davis-Kahan sin(theta) theorem:**
- Davis, C. and Kahan, W.M. (1970). "The rotation of eigenvectors by a perturbation. III." Quantitative bounds on eigenvector perturbation in terms of eigenvalue gaps.

**Strain-vorticity alignment in NS:**
- Ashurst, W.T., Kerstein, A.R., Kerr, R.M., and Gibson, C.H. (1987). "Alignment of vorticity and scalar gradient with strain rate in simulated Navier-Stokes turbulence." First DNS evidence for intermediate-eigenvector alignment.
- Constantin, P. and Fefferman, C. (1993). "Direction of vorticity and the problem of global regularity for the Navier-Stokes equations." Conditional regularity from geometric regularity of vorticity direction.

**Geometric measure theory and level sets:**
- Federer, H. (1969). *Geometric Measure Theory*. Co-area formula for Lipschitz maps, Hausdorff dimension of level sets.
- Hardt, R. and Simon, L. (1989). "Nodal sets for solutions of elliptic equations." Dimension estimates for zero sets of solutions of elliptic PDEs.

## Appendix B: Detailed Computation of Eigenvector Gradient Near Coalescence

Consider the model situation where S(x) has a double eigenvalue at the origin x = 0 in R^3. Using Arnold's normal form, let the 2x2 splitting matrix in the degenerate eigenspace be:

M(x) = [[x_1, x_2], [x_2, -x_1]]

(here we use x_1, x_2 as the two transverse coordinates to the coalescence curve, which runs along the x_3 direction).

Eigenvalues: s_+/- = +/- r, where r = sqrt(x_1^2 + x_2^2).

Eigenvectors (in the 2D subspace):
e_+ = (cos(phi/2), sin(phi/2))
e_- = (-sin(phi/2), cos(phi/2))

where phi = arctan(x_2/x_1).

Gradient computation:

nabla phi = (-x_2/(x_1^2 + x_2^2), x_1/(x_1^2 + x_2^2), 0) = (1/r) e_phi_hat

where e_phi_hat is the angular unit vector in the (x_1, x_2) plane.

Therefore:

nabla e_+ = (1/2) nabla phi (-sin(phi/2), cos(phi/2)) = (1/2r) e_phi_hat tensor e_-

|nabla e_+| = 1/(2r)

The L^p integrability in a ball B_R around the coalescence curve (parametrized by x_3):

integral_{B_R} |nabla e_+|^p dx = integral_0^L dx_3 integral_0^R (1/(2r))^p 2*pi*r dr
                                 = pi L / 2^{p-1} integral_0^R r^{1-p} dr

This converges if and only if 1 - p > -1, i.e., **p < 2**.

For p = 2 (the H^1 case): integral_0^R r^{-1} dr = log(R/0) = +infinity. So e_+ is NOT in H^1.

For p < 2: integral_0^R r^{1-p} dr = R^{2-p}/(2-p) < infinity. So e_+ IS in W^{1,p} for all p < 2.

This confirms the regularity statement in Section 2.3.

## Appendix C: Explicit Verification that Q is Smooth at Coalescence

Let S(x) have eigenvalues s_1(x), s_2(x), s_3(x) with s_1 = s_2 at x = x_0. We show Q = omega . S omega / |omega|^2 is smooth at x_0.

Q(x) = omega(x)^T S(x) omega(x) / |omega(x)|^2

Both S(x) and omega(x) are smooth functions of x (S is smooth because u is smooth; omega = curl u is smooth). The numerator omega^T S omega is a smooth function of x (a polynomial in the entries of S and omega). The denominator |omega|^2 is smooth wherever omega != 0. Therefore Q is smooth on {omega != 0}, regardless of eigenvalue coalescence.

There is no issue at eigenvalue coalescence because Q is expressed directly in terms of the matrix S and the vector omega, with no reference to eigenvectors or eigenvalues. The eigendecomposition S = sum_i s_i e_i e_i^T is a way of computing Q = sum_i s_i (omega . e_i)^2 / |omega|^2, but this intermediate representation introduces artificial singularities (in the individual terms s_i and e_i) that cancel in the sum.

This cancellation is not accidental; it reflects the fact that Q is the Rayleigh quotient of a smooth bilinear form S applied to a smooth vector omega. The Rayleigh quotient is a smooth function of the matrix and vector entries; no eigendecomposition is needed to evaluate or differentiate it.
