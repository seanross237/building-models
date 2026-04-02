# Direction 3: Vorticity-Direction Lipschitz Regularity

**Date:** 2026-04-02
**Parent:** April 2 pursuit plan, post-Angle-10 direction search
**Classification:** Adversarial exploration of a conditional-to-unconditional upgrade path
**Depends on:** Subproblems A-E from the Angle-10 pursuit (especially C and E)

---

## 1. Concise Statement of the Route

The Constantin-Fefferman theorem (1993) states: if the vorticity direction field xi(x,t) = omega(x,t)/|omega(x,t)| satisfies the Lipschitz condition

    |xi(x,t) - xi(y,t)| <= C|x - y|    for all x, y in {|omega(.,t)| > M}

for some constants C and M, then the solution remains smooth. Deng-Hou-Yu (2005) weakened this to a one-directional condition: regularity follows if

    |D_xi xi| is bounded    on {|omega| > M}

i.e., xi need only be Lipschitz along itself, not in all directions.

**The proposed route:** Prove the Deng-Hou-Yu condition directly from the Navier-Stokes equations, bypassing the strain-vorticity alignment approach that was structurally blocked by s_2 > 0. The idea is that the xi equation, while involving supercritical terms, might admit closure through the specific geometric structure of high-vorticity regions (where the Angle-10 pursuit confirmed that xi is approximately aligned with the smooth eigenvector e_2, and that the spectral gap of the strain tensor grows with |omega|).

This route avoids the s_2 > 0 obstruction entirely: the Constantin-Fefferman and Deng-Hou-Yu theorems make no reference to the sign of s_2 or the magnitude of stretching. They are purely geometric conditions on the direction field. The question shifts from "is the stretching self-limiting?" (which it is not, because s_2 > 0) to "does the geometry of the vorticity direction field remain controlled?"

---

## 2. The PDE for xi = omega/|omega|

### 2.1 Derivation

Start from the vorticity equation:

    D_t omega = S omega + nu Delta omega                                (V)

where D_t = d_t + u . nabla is the material derivative, S = sym(nabla u) is the strain tensor, and we used the identity (omega . nabla)u = S omega (since the antisymmetric part Omega omega = (1/2)(omega x omega) = 0).

Write omega = |omega| xi, where |omega| = (omega . omega)^{1/2} and xi = omega/|omega| is the unit vorticity direction. We compute D_t omega = (D_t |omega|) xi + |omega| D_t xi.

Taking the inner product with xi:

    D_t |omega| = xi . (S omega + nu Delta omega) = (xi . S xi)|omega| + nu xi . Delta omega

Let Q = xi . S xi = omega . S omega / |omega|^2 be the Rayleigh quotient (the smooth quantity from Subproblem B). Then:

    D_t |omega| = Q |omega| + nu xi . Delta omega                      (Mag)

The perpendicular part (projecting out the xi-component) gives the evolution of the direction:

    |omega| D_t xi = (I - xi tensor xi)(S omega + nu Delta omega)
                   = (I - xi tensor xi) S xi |omega| + nu (I - xi tensor xi) Delta omega

Define P_perp = I - xi tensor xi (the projection orthogonal to xi). Then:

    **D_t xi = P_perp S xi + (nu / |omega|) P_perp Delta omega**        (Dir)

This is the fundamental PDE for the vorticity direction. Let us examine each term.

### 2.2 Term-by-term analysis

**Term 1: The strain rotation term P_perp S xi.**

This is the component of the strain stretching perpendicular to the current vorticity direction. It rotates xi toward whichever strain eigenvector has the strongest perpendicular projection, weighted by eigenvalue. In the eigenbasis of S:

    P_perp S xi = sum_i s_i (xi . e_i) e_i  -  (sum_i s_i (xi . e_i)^2) xi

When xi is aligned with e_2 (as the Angle-10 pursuit confirmed in high-vorticity regions), the perpendicular components xi . e_1 and xi . e_3 are O(delta), and this term is O(delta |S|). The strain rotation is weak when alignment is strong.

Crucially, this term involves S = sym(nabla u), which has the same regularity as nabla u (one derivative of velocity). It does NOT involve nabla^2 u. So this term alone is subcritical for controlling xi.

**Term 2: The viscous curvature term (nu/|omega|) P_perp Delta omega.**

This is the dangerous term. Expand:

    Delta omega = Delta(|omega| xi) = (Delta |omega|) xi + 2 (nabla |omega| . nabla) xi + |omega| Delta xi

So:

    P_perp Delta omega = 2 (nabla |omega| . nabla) xi_perp + |omega| P_perp Delta xi

where xi_perp denotes the perpendicular part of the relevant expressions (the (Delta |omega|) xi term is parallel to xi and killed by P_perp). Actually, more carefully:

    P_perp Delta omega = P_perp [2 nabla |omega| . nabla xi + |omega| Delta xi]
                       = 2 (nabla |omega| . nabla) (P_perp xi) + |omega| P_perp Delta xi

But P_perp xi is not well-defined as a vector in the usual sense (P_perp depends on xi). Let me re-derive more carefully.

Write Delta omega_j = (Delta |omega|) xi_j + 2 (partial_k |omega|)(partial_k xi_j) + |omega| (Delta xi_j). Then:

    (P_perp Delta omega)_j = (Delta omega)_j - xi_j (xi . Delta omega)

This contains the term |omega| (P_perp Delta xi)_j, which involves second spatial derivatives of xi. Thus:

    **(nu/|omega|) P_perp Delta omega = nu P_perp Delta xi + (2nu/|omega|) (nabla |omega| . nabla) P_perp xi + ...**

The leading-order piece nu P_perp Delta xi is a viscous diffusion of the direction field. It acts as a regularizing Laplacian on xi: in isolation, it would smooth xi.

The term (2nu/|omega|)(nabla |omega| . nabla) P_perp xi is an advection of the direction by the gradient of the vorticity magnitude, with coefficient 2nu/|omega|. In regions of strong vorticity gradients, this can rotate xi rapidly.

### 2.3 The full xi equation in cleaned form

Combining, the xi equation can be written as:

    **D_t xi = P_perp S xi + nu Delta xi - nu |nabla xi|^2 xi + (2nu/|omega|) P_perp (nabla |omega| . nabla xi)**     (Dir')

where the -nu |nabla xi|^2 xi term arises from the constraint |xi| = 1 (the Laplacian on the sphere S^2 has a curvature correction relative to the flat Laplacian).

More precisely, for a unit vector field xi with |xi| = 1, the identity

    Delta xi = Delta_{S^2} xi - |nabla xi|^2 xi

holds in the sense that the flat Laplacian Delta xi, applied to the components of a unit vector, produces a tangential part (the spherical Laplacian Delta_{S^2} xi, which is in T_{xi} S^2) and a normal part (-|nabla xi|^2 xi, which points radially inward on S^2 to maintain the constraint). So the viscous term in (Dir') should properly be read as nu Delta_{S^2} xi (the harmonic map heat flow on S^2), plus the correction from the vorticity gradient.

### 2.4 The equation for nabla xi (needed for Lipschitz control)

To control |nabla xi|, differentiate (Dir') spatially. Schematically:

    D_t (nabla xi) = nabla (P_perp S xi) + nu Delta (nabla xi) + (lower-order in nabla xi)
                     + (2nu/|omega|) nabla [P_perp (nabla |omega| . nabla xi)]
                     - (nabla u) . nabla xi    [from the material derivative commutator]

The term nabla(P_perp S xi) involves nabla S = nabla^2 u --- the second derivative of velocity, or equivalently the first derivative of strain. This is the source of the supercriticality problem. We need:

    **nabla^2 u is controlled at points where |omega| is large.**

By the Biot-Savart law, nabla^2 u is a singular integral of nabla omega, so controlling nabla^2 u requires controlling nabla omega. By the energy estimates, nabla omega is in L^2 (the enstrophy dissipation integral controls integral |nabla omega|^2 dt). But pointwise control of nabla^2 u requires more: it requires L^infinity bounds on nabla omega, which are at the same level of difficulty as the regularity problem itself.

**This is the supercriticality obstruction.** Controlling nabla xi requires controlling nabla^2 u, which requires controlling nabla omega at the same regularity level as the full regularity problem.

---

## 3. Known Obstructions

### 3.1 The supercriticality wall

The core obstruction is dimensional. The vorticity direction xi = omega/|omega| has the same regularity as omega near points where omega is nonzero. But to show xi is Lipschitz, we need |nabla xi| bounded, which requires controlling |nabla omega|/|omega| - |omega . nabla omega| |omega|^{-2} pointwise. By the energy estimates, omega is in L^2 and nabla omega is in L^2(dt; L^2(dx)), but pointwise bounds on either quantity are not available from the energy alone.

The natural scaling analysis: if |omega| ~ lambda (amplitude scale) and the spatial scale of variation is ~ ell, then |nabla omega| ~ lambda/ell, so |nabla xi| ~ |nabla omega|/|omega| ~ 1/ell. The Constantin-Fefferman condition requires 1/ell to be bounded, i.e., ell bounded away from zero. But the core difficulty of 3D NS is precisely that coherent vortex structures can develop ever-finer spatial scales.

### 3.2 Comparison with the Constantin-Fefferman and Deng-Hou-Yu conditions

The CF and DHY theorems are conditional regularity results. Neither paper proves that their respective conditions hold for actual NS solutions. The question "can we verify the CF/DHY condition from the equations?" has been open since 1993.

Key negative evidence:

1. **Hou-Li (2008)** studied a model problem (axisymmetric flow with swirl on a bounded domain) and showed that the vorticity direction can develop singularities in finite time for the model (though their construction does not apply to the full NS equations on R^3).

2. **No existing result proves Lipschitz regularity of xi even for special classes of NS solutions** (axisymmetric without swirl being regular for entirely different reasons, namely the conservation of omega_theta/r which gives a maximum principle).

3. The Deng-Hou-Yu condition (|D_xi xi| bounded) is weaker than full Lipschitz, but there is no known example where it can be verified for a class of potentially singular 3D NS solutions.

### 3.3 The role of the pressure

The xi equation (Dir') involves the strain S = sym(nabla u), whose evolution involves the pressure Hessian nabla^2 p. The pressure satisfies:

    -Delta p = partial_i partial_j (u_i u_j) = tr(S^2) - |omega|^2/2

so p is determined nonlocally by the velocity. The pressure Hessian nabla^2 p appears in the strain evolution and hence indirectly in the xi equation through the term nabla(P_perp S xi).

The pressure term is neither purely helpful nor purely harmful:

- **Helpful aspect:** The pressure enforces incompressibility and provides a restoring force against extreme strain configurations. It prevents the restricted Euler finite-time blowup (in restricted Euler, all solutions blow up in finite time; with pressure, many solutions are smoothed).

- **Harmful aspect:** The pressure is nonlocal. It couples distant parts of the flow. Even if the local geometry of xi is well-controlled, nonlocal pressure effects could inject sharp gradients into the vorticity direction field.

- **The isotropic pressure approximation** (used in restricted Euler) kills the anisotropic part of nabla^2 p. The anisotropic part is exactly the piece that could either help or hurt. Its effect on xi regularity is not well-understood.

### 3.4 Known results for special classes

**Axisymmetric without swirl:** Regularity is proved (Ladyzhenskaya 1968, Ukhovskii-Yudovich 1968) by entirely different methods (maximum principle for omega_theta/r). The vorticity direction is not used.

**Axisymmetric with swirl:** This remains open for large data. The vorticity direction xi varies in the (e_r, e_z) plane and can rotate rapidly near the axis r = 0. The Hou-Luo computations (2014) suggest possible singularity formation for this class, with |nabla xi| appearing to blow up.

**Helical solutions:** Regularity is proved (Mahalov-Titi-Leibovich 1990, Ettinger-Titi 2009) using the helical symmetry reduction to a 2D-like structure. The vorticity direction is constrained by the symmetry and cannot develop Lipschitz singularities.

**2D flows:** Trivially regular. The vorticity is scalar-valued, so the "direction" is constant (always pointing in the z-direction). Lipschitz regularity of the direction is vacuous.

**There is no known proof of the CF condition for any class of 3D NS solutions where regularity is not already known by other means.**

### 3.5 Can xi become irregular for smooth NS data?

This is the contrapositive question. If smooth initial data can produce solutions where xi develops Lipschitz singularity, then the route is dead in principle.

There is no rigorous construction showing that xi becomes non-Lipschitz for smooth NS data (because that would imply finite-time blowup, which is the open Millennium Problem). However:

- The Hou-Luo numerics for axisymmetric Euler with swirl on a cylinder suggest that |nabla xi| can grow without bound, with xi developing a sharp front near the boundary.
- Tao's averaged NS blowup solution does blow up in finite time with xi necessarily becoming singular (since the vorticity blows up, and the concentration into a thin structure means |nabla xi| ~ 1/ell diverges).
- For the real NS equations, there is no known mechanism that would prevent xi from becoming singular if |omega| blows up.

The honest assessment: proving Lipschitz regularity of xi is essentially as hard as proving regularity of the NS solution itself. The CF theorem gives a sufficient condition, but verifying it is not a shortcut -- it is the problem.

---

## 4. Strongest Argument For

The strongest case for this direction rests on three pillars from the completed Angle-10 pursuit:

**Pillar 1: The spectral gap grows with |omega|.** In the Burgers vortex (Subproblem A), the eigenvalue gap between s_2 and s_1 at the transition region scales as alpha (the external strain rate), while the off-diagonal strain grows with Gamma/r_c^2 ~ |omega|_peak. At high Reynolds number, the e_2-e_1 spectral gap at points of peak vorticity is O(alpha), while the vorticity magnitude is O(Gamma alpha / nu) >> alpha. This means the eigenvalue gap is O(|omega| nu / Gamma) ~ O(|omega| / Re), which vanishes relative to |omega| but grows in absolute terms.

The relevance: if xi is approximately aligned with e_2, and e_2 is smooth (away from codimension-2 coalescence), and the spectral gap controlling the smoothness of e_2 grows with |omega|, then xi inherits a form of enhanced smoothness at high vorticity. The Davis-Kahan theorem gives:

    |nabla e_2| <= C |nabla S| / gap

If gap ~ alpha (independent of |omega| at Burgers-type vortex tubes), and |nabla S| ~ |nabla^2 u| ~ |omega|/ell, then |nabla e_2| ~ |omega| / (alpha ell). For |nabla xi| to be bounded, we need ell bounded below by ~ |omega| / alpha, which links the spatial scale of vorticity variation to the external strain rate. This is plausible for Burgers-type vortex structures (where ell ~ r_c = sqrt(nu/alpha) is set by the balance of strain and diffusion), but it does not follow from the PDE alone.

**Pillar 2: The Deng-Hou-Yu condition is weaker.** The DHY condition only requires control of D_xi xi = (xi . nabla) xi, the derivative of the direction along itself. For a vortex tube oriented along the z-axis, xi ~ e_z, and D_xi xi ~ partial_z e_z. If the tube is approximately straight (which is the generic picture at high vorticity), then D_xi xi is small even though the cross-sectional derivatives nabla_perp xi could be large. The DHY condition captures the idea that vortex tubes need only be smooth along their length, not across their cross-section.

**Pillar 3: The connection to the harmonic map heat flow.** The xi equation (Dir') has the form of a forced harmonic map heat flow into S^2. Harmonic map heat flows from R^3 to S^2 with smooth initial data can develop singularities (unlike the 2D case where Struwe's theorem gives global regularity). However, the singularities of harmonic map heat flows are well-understood: they occur at isolated space-time points, and the singularity profile is a "bubble" (a nontrivial harmonic map S^2 -> S^2 at the singularity scale). The forcing terms in the xi equation (strain rotation and vorticity-gradient advection) could potentially prevent or promote such bubbling. If the strain structure of high-vorticity regions (which is essentially that of parallel vortex tubes) prevents bubble formation, this could give regularity of xi.

---

## 5. Strongest Argument Against

**Argument 1: The supercriticality is real and structural, not technical.**

The xi equation (Dir') involves the term P_perp S xi, where S = sym(nabla u). The spatial gradient nabla(P_perp S xi) involves nabla S = nabla^2 u, which is at the level of two derivatives of velocity. The energy gives us control of one derivative of velocity in L^2 (the enstrophy integral nabla u in L^2(dt; L^2)). Controlling two derivatives requires controlling nabla omega in L^2, which is the enstrophy dissipation. The enstrophy dissipation integral is finite: integral_0^T integral |nabla omega|^2 dx dt < infinity. But this is an integrated (L^1 in time, L^2 in space) estimate, not a pointwise one. To get Lipschitz control of xi, we need pointwise bounds on nabla^2 u, which is strictly stronger than what the energy gives.

This is not a matter of "we haven't tried hard enough." The gap between L^2 spatial control and L^infinity spatial control of nabla omega is a full Sobolev embedding, requiring 3/2 additional derivatives in 3D. This gap is the same one that makes the Millennium Problem hard. Proving Lipschitz regularity of xi requires bridging exactly this gap.

**Argument 2: The Deng-Hou-Yu condition does not make the problem dimensionally easier.**

The DHY condition D_xi xi bounded only requires one directional derivative of xi. But D_xi xi = (xi . nabla)xi involves nabla xi, and controlling even one component of nabla xi at a point requires the same regularity of nabla omega/|omega| that the full Lipschitz condition requires. The DHY condition is a weaker conclusion, but verifying it from the PDE involves the same supercritical estimates.

To see this more concretely: D_xi xi involves (omega/|omega|) . nabla(omega/|omega|). Expanding:

    D_xi xi_j = (omega_k / |omega|) partial_k (omega_j / |omega|)
              = (omega_k / |omega|^2) (partial_k omega_j - omega_j partial_k |omega| / |omega|)

Bounding this requires bounding |nabla omega| / |omega| along one specific direction (the direction of omega itself). While this is a single directional derivative rather than the full gradient, the estimate still requires controlling nabla omega at points of high vorticity. The vorticity equation gives nabla omega in terms of nabla S omega + S nabla omega + nu Delta nabla omega, and closing this requires the same machinery as the full regularity problem.

**Argument 3: The alignment findings do not provide a shortcut.**

The Angle-10 pursuit confirmed that xi ~ e_2 in high-vorticity regions, and that e_2 is smooth (away from codimension-2 coalescence). One might hope to transfer the smoothness of e_2 to xi. But this transfer requires controlling the alignment error delta and its spatial gradient nabla delta. The alignment error delta is not known to satisfy any helpful PDE: its evolution involves the same supercritical terms (through the xi equation). The spectral gap argument (Pillar 1 above) gives |nabla e_2| <= C / gap, but gap is bounded by |S| ~ |nabla u|, and using this bound gives |nabla e_2| <= C |nabla S| / |S|, which requires controlling the ratio nabla^2 u / nabla u -- again a supercritical quantity.

**Argument 4: The harmonic map heat flow analogy is misleading.**

The xi equation is a forced harmonic map heat flow, but:
(a) The forcing is supercritical (involves nabla u, which is at the critical level for NS).
(b) In dimension 3, harmonic map heat flows CAN develop singularities (Chang-Ding-Ye 1992). The forcing from the strain could promote rather than prevent them.
(c) The coefficient nu/|omega| in the viscous term of (Dir') goes to zero as |omega| -> infinity, meaning that the effective viscosity for the xi equation vanishes precisely in the high-vorticity regions where control is needed most. In the limit of very large |omega|, the xi equation is dominated by the inviscid strain rotation P_perp S xi, which has no regularizing mechanism.

**Argument 5: Historical evidence strongly suggests this is circular.**

The CF condition has been known since 1993. Deng-Hou-Yu weakened it in 2005. In the intervening 30+ years, no one has verified either condition from the NS equations for any class of potentially singular solutions. This is not for lack of attention: the problem is well-known and has been studied by top analysts. The lack of progress is strong evidence that verifying the CF/DHY condition is as hard as the regularity problem itself.

---

## 6. Concrete Subproblems

### Subproblem D3.1: The xi equation on Burgers-type profiles

**Statement:** For the Burgers vortex family (parameterized by Re_Gamma), compute |nabla xi| and |D_xi xi| explicitly. Determine how these quantities scale with Re_Gamma, the radial coordinate r, and the vorticity magnitude |omega|.

**Kill condition:** If |D_xi xi| grows with Re_Gamma (even for the steady Burgers solution), then the DHY condition fails at the exact-solution level, killing the route.

**Expected difficulty:** Low (explicit computation). This is a necessary sanity check.

### Subproblem D3.2: The effective viscosity problem

**Statement:** In the xi equation (Dir'), the viscous regularization has coefficient nu/|omega|. In high-vorticity regions where |omega| >> 1, this coefficient is small. Determine whether the strain rotation term P_perp S xi can drive |nabla xi| to grow faster than the effective viscosity can smooth it. Specifically: for the linearization of the xi equation around xi = e_2 (the aligned state), what is the spectral structure? Are there unstable modes that grow faster than the diminished viscosity can control?

**Kill condition:** If the linearized xi equation around the aligned state has modes growing at rate proportional to |omega| (which is the natural scale of the strain), while the viscous damping is at rate nu / length^2, then Lipschitz control requires length >= sqrt(nu / |omega|) = r_c (the vortex core radius). This would mean |nabla xi| ~ 1/r_c ~ sqrt(|omega| / nu), which diverges with |omega|. This would kill the route.

**Expected difficulty:** Medium (PDE spectral analysis on Burgers background).

### Subproblem D3.3: The DHY condition along vortex tubes

**Statement:** Consider a vortex tube geometry: xi is approximately constant along the tube axis and varies mainly in the cross-sectional directions. The DHY condition only requires control of D_xi xi (the axial derivative). Derive the PDE for D_xi xi from the xi equation. Does the axial derivative decouple from the cross-sectional derivatives in any useful sense? Is there a closed estimate for D_xi xi that does not require controlling nabla_perp xi?

**Kill condition:** If the equation for D_xi xi necessarily involves nabla_perp xi (the cross-sectional gradient, which is O(1/r_c) and potentially large), then the DHY condition cannot be verified without controlling the full gradient of xi, eliminating the advantage of the weaker DHY condition.

**Expected difficulty:** High (PDE commutator analysis).

### Subproblem D3.4: Maximum principle for |nabla xi|^2

**Statement:** Derive the evolution equation for |nabla xi|^2. Identify all source terms. Determine whether a maximum-principle argument can show |nabla xi|^2 stays bounded.

The quantity |nabla xi|^2 satisfies an equation of the form:

    D_t |nabla xi|^2 = nu Delta |nabla xi|^2 - 2nu |nabla^2 xi|^2 + (source terms involving nabla S, nabla omega, ...)

The key question is whether the source terms are all bounded by |nabla xi|^2 times a subcritical quantity (allowing Gronwall) or whether they involve supercritical quantities (meaning the maximum principle cannot close).

**Kill condition:** If the source terms necessarily involve |nabla^2 u|^2 or |nabla omega| |nabla xi| without compensation by |nabla^2 xi|^2 (the viscous dissipation), then the maximum-principle approach fails.

**Expected difficulty:** High (multi-term PDE computation).

### Subproblem D3.5: Comparison with Beale-Kato-Majda

**Statement:** The BKM criterion states regularity is equivalent to integrability of ||omega||_{L^infinity}. The CF condition states regularity follows from Lipschitz regularity of xi on the high-vorticity set. The question is: are these logically comparable? Specifically:

(a) Does BKM imply CF? (i.e., does ||omega||_{L^infinity} bounded imply |nabla xi| bounded on {|omega| > M}?)

(b) Does CF imply BKM? (i.e., does |nabla xi| bounded imply ||omega||_{L^infinity} bounded?)

If (a) holds, then the CF condition is weaker than BKM, and verifying CF is easier than verifying BKM. If (b) holds, then CF is equivalent to BKM, and we have gained nothing by the geometric reformulation.

**Kill condition:** If (a) holds (BKM implies CF), then the CF route is genuinely different from (and potentially easier than) the BKM route. If (b) also holds, the two are equivalent and the geometric reformulation provides no advantage.

**Expected difficulty:** Medium (functional analysis).

---

## 7. Classification

**Theorem-facing components:**
- The CF and DHY theorems themselves are rigorous conditional regularity results (already proved, not in question).
- Subproblem D3.5 (logical comparison with BKM) is a clean theorem question.

**Mechanism-facing components:**
- The connection between e_2-alignment, spectral gap, and xi smoothness (Pillar 1) is a mechanism-level observation. It requires translation into estimates.
- The effective viscosity problem (D3.2) is mechanism-facing: it asks whether the geometric structure of high-vorticity regions provides enough regularization.

**Speculative components:**
- The hope that the harmonic map heat flow structure of the xi equation provides regularity is speculative. Known results (Chang-Ding-Ye singularities for 3D harmonic map heat flows) suggest this is unlikely without additional structure.
- The hope that the DHY condition decouples from the full nabla xi is speculative. No PDE-level evidence supports this yet.

**Overall:** The route is approximately 20% theorem-facing (the conditional regularity results are solid), 40% mechanism-facing (the alignment/spectral-gap connection has substance from Angle-10), and 40% speculative (the closure of the xi estimates has no supporting evidence and faces a clear dimensional obstruction).

---

## 8. Verdict: Weakly Promising

**Not dead:** The route avoids the s_2 > 0 obstruction that killed the Angle-10 direct approach. It addresses a logically independent sufficient condition for regularity (geometric control of vorticity direction, not magnitude control of stretching). The alignment findings from Subproblem A provide genuine structural input (xi ~ e_2, e_2 smooth, spectral gap grows) that was not available before the Angle-10 pursuit.

**Not promising:** The supercriticality obstruction is real and structural. Controlling nabla xi requires controlling nabla^2 u, which is at the same level of difficulty as the full regularity problem. The Deng-Hou-Yu weakening reduces the geometric requirement but not the analytical difficulty. The effective viscosity nu/|omega| in the xi equation vanishes in high-vorticity regions, removing the only regularizing mechanism at the point where it is most needed. The 30-year failure of the community to verify CF/DHY from the equations is strong empirical evidence against the route.

**Weakly promising because:** There is exactly one structural feature that distinguishes this attempt from a naive "just prove xi is Lipschitz" approach: the quantitative alignment with the smooth eigenvector e_2, with a spectral gap that grows with |omega|. If this can be turned into a closed estimate for D_xi xi (not for the full nabla xi), specifically by exploiting the fact that D_xi xi involves the derivative of xi along the tube axis (where e_2 is smooth and slowly varying, because the spectral gap protects against rapid eigenvector rotation along that direction), then there is a narrow path. But this requires:

- Showing that D_xi xi, for xi approximately aligned with e_2, is controlled by D_xi e_2 plus an error term involving the alignment angle delta and its directional derivative D_xi delta.
- Showing that D_xi e_2 is controlled by the spectral gap (via Davis-Kahan) and the directional derivative of the strain D_xi S.
- Showing that D_xi S is controlled by a quantity that does NOT require full nabla omega control -- perhaps by exploiting the vortex tube geometry to reduce D_xi S to a combination of the strain self-interaction and the along-tube viscous correction.

Each of these steps faces a gap, and the cumulative probability of all three closing is small.

---

## 9. The Single Sharpest Next Theorem-Shaped Question

**Question:** For the steady Burgers vortex with circulation Gamma and strain rate alpha in viscous fluid with viscosity nu, compute the directional derivative D_xi xi = (xi . nabla)xi of the vorticity direction xi = omega/|omega| along itself. Express the answer in terms of the vortex Reynolds number Re_Gamma = Gamma/(2 pi nu). Determine:

(a) Is |D_xi xi| bounded uniformly in Re_Gamma?

(b) If so, what is the bound, and does it depend on the external strain rate alpha?

(c) If not, how does sup |D_xi xi| scale with Re_Gamma?

**Why this is the sharpest question:** The Burgers vortex is the canonical model of a high-Reynolds-number vortex tube. If the DHY condition fails even for this steady, exact, well-understood solution, the route is dead. If the DHY condition holds with a bound that improves at high Re (because higher Re means stronger alignment with e_2, which is smooth along the tube axis), this would provide the first positive evidence and identify the mechanism that any general proof would need to exploit.

**What the answer likely is (prediction to be tested):** For the Burgers vortex, xi = e_z everywhere (the vorticity is purely axial), so xi is constant and D_xi xi = 0 identically. This means the Burgers vortex trivially satisfies the DHY condition. The more informative question is therefore for a perturbed Burgers vortex (a slightly bent vortex tube), where the answer will depend on the bending curvature and the Reynolds number. The sharpened version of the question is:

**For a vortex tube with axis curvature kappa and core Reynolds number Re_Gamma, does |D_xi xi| remain bounded as Re_Gamma -> infinity at fixed kappa? Or does the high-Re concentration of vorticity into thinner cores amplify the directional derivative D_xi xi?**

The answer determines whether the route has any chance of working.
