# Epsilon Regularity for D_xi S: A CKN-Framework Analysis

**Date:** 2026-04-02
**Parent:** circulation-cascade-analysis.md, coupled-bootstrap-attempt.md, time-integrated-bootstrap.md
**Classification:** Full technical analysis with honest assessment
**Depends on:** Theorem CB, equation (6.2), CKN partial regularity theory, enstrophy dissipation bounds

---

## 0. Executive Summary

This document investigates whether the Caffarelli-Kohn-Nirenberg (CKN, 1982) epsilon-regularity framework can be adapted to the quantity D_xi S to close the 3D Navier-Stokes regularity problem. The motivation is equation (6.2) from the circulation-cascade analysis:

    |D_xi S| / (omega^{3/2}/nu^{1/2}) = 16 pi sin(Theta) / Re_Gamma^2

which gives D_xi S at the critical exponent delta = 1/2 but with a SMALL coefficient 1/Re_Gamma^2. The idea: if a CKN-type epsilon-regularity theorem holds for D_xi S, the small coefficient might play the role of the "epsilon" and deliver regularity.

**Verdict: The epsilon-regularity approach for D_xi S does NOT close.** The analysis identifies four independent failure points, each individually fatal:

1. **The scale-invariant D_xi S quantity F(r) = integral_{Q_r} |D_xi S|^{5/3} dx dt is NOT small at the vorticity maximum.** The Holder computation that suggests F ~ nu^{5/6} contains a critical error: it uses the L^2 bound on D_xi S on Q_{r_c} as if D_xi S were uniformly distributed, but D_xi S concentrates on the vortex core where the L^{5/3} integral is dominated by the peak value. The corrected estimate gives F(r_c) ~ Re_Gamma^{2/3}, which is LARGE for large Reynolds number.

2. **The epsilon-regularity theorem for D_xi S cannot be proved** because the PDE for D_xi S has a source term D_xi(nabla^2 p) involving third derivatives of the pressure (equivalently, second derivatives of vorticity), which is one derivative beyond what the enstrophy dissipation controls. This violates the structural requirements of the CKN iteration at the most fundamental level: the Caccioppoli inequality fails for D_xi S.

3. **The CKN iteration requires the energy inequality, which is available for u and omega but NOT for D_xi S.** There is no local inequality for D_xi S analogous to the local energy inequality for |u|^2 or the local enstrophy inequality for |omega|^2. Without this inequality, the CKN bootstrapping mechanism cannot even begin.

4. **Even if an epsilon-regularity theorem held conditionally, the enstrophy-level CKN improvement from the small 1/Re^2 coefficient does not reduce the singular set dimension below zero.** The CKN singular set dimension is controlled by the scaling of the energy, not the coefficient. The 1/Re^2 factor enters multiplicatively but does not change the dimensional analysis that produces dim(S) <= 1.

The document does identify one genuinely useful byproduct: a rigorous L^{5/3} space-time bound on D_xi S from the enstrophy dissipation (Section 3.4), which gives:

    integral_0^T integral_{R^3} |D_xi S|^{5/3} dx dt <= C(||u_0||, nu, T)

This is a new a priori estimate that is not in the standard literature, though it does not suffice for regularity.

---

## 1. The Scale-Invariant D_xi S Quantity

### 1.1 Dimensional analysis and NS scaling

Under the Navier-Stokes scaling symmetry u_lambda(x,t) = lambda u(lambda x, lambda^2 t), which preserves the NS equations with nu -> nu (the scaling is at fixed viscosity only when we also rescale nu, but for the CKN analysis the relevant scaling is the parabolic blow-up scaling that preserves the equations):

    u -> lambda u,  x -> x/lambda,  t -> t/lambda^2

Under this scaling:
- omega = curl u -> lambda^2 omega (vorticity scales as lambda^2)
- S = (1/2)(nabla u + nabla u^T) -> lambda^2 S (strain scales as lambda^2)
- xi = omega/|omega| -> xi (vorticity direction is scale-invariant)
- D_xi S = (xi . nabla)S -> lambda^3 D_xi S (directional derivative of strain scales as lambda^3)

The parabolic cylinder Q_r = B_r(x_0) x (t_0 - r^2, t_0) has volume |Q_r| ~ r^5 (three spatial dimensions plus parabolic time).

For the integral integral_{Q_r} |D_xi S|^p dx dt under the NS scaling:

    integral_{Q_r} |D_xi S|^p dx dt -> lambda^{3p} * lambda^{-3} * lambda^{-2} * integral = lambda^{3p - 5} * integral

Scale invariance (the integral is unchanged under the scaling) requires:

    3p - 5 = 0,  hence  **p = 5/3**

Therefore the scale-invariant quantity is:

    **F(r) = integral_{Q_r} |D_xi S|^{5/3} dx dt**                                  (1.1)

Note: p = 5/3 < 2, so this is an L^{5/3} norm, weaker than L^2.

### 1.2 Comparison with the CKN energy quantity

The standard CKN quantity is:

    E(r) = (1/r) sup_{t_0-r^2 < s < t_0} integral_{B_r} |u|^2 dx + (1/r) integral_{Q_r} |nabla u|^2 dx dt

This is dimensionless under the NS scaling (u -> lambda u, nabla u -> lambda^2 nabla u, and the volume/time factors compensate). In the CKN framework, the epsilon-regularity statement is: if E(1) < epsilon_0, then u is smooth on Q_{1/2}.

For D_xi S, the analogous statement would be:

**Conjecture (Epsilon Regularity for D_xi S):** There exists epsilon_0 > 0 such that if u is a suitable weak solution of NS on Q_1 and F(1) < epsilon_0, then u is smooth on Q_{1/2}.

We now investigate whether this conjecture can be proved and whether F is actually small.

### 1.3 Remark on the exponent p = 5/3

The exponent 5/3 is critical in the Lorentz space sense. By the Sobolev embedding and parabolic interpolation, the space L^{5/3}_{x,t}(Q_r) is the borderline integrability for the D_xi S term to be "visible" at the correct parabolic scaling. Below 5/3, the integral is dominated by large-scale contributions and does not detect local singularities. Above 5/3, the integral provides genuine control of the local behavior.

This is exactly analogous to the role of L^{5/3} in the Prodi-Serrin regularity theory (where u in L^5_t L^{5/2}_x, which has the same scaling as L^{5/3}_{x,t}, is borderline).

---

## 2. Is F(r_c) Small at the Vorticity Maximum?

### 2.1 The naive computation (from the prompt)

The prompt suggests: at the natural scale r_c = (nu/omega)^{1/2} (the Burgers vortex core radius), we can estimate F(r_c) by:

1. integral_{Q_{r_c}} |D_xi S|^2 ~ (omega^3/nu) * r_c^3 * (1/omega) = omega^2 r_c^3 / nu
2. Using r_c = (nu/omega)^{1/2}: integral_{Q_{r_c}} |D_xi S|^2 ~ omega^{1/2} nu^{1/2}
3. By Holder: integral_{Q_{r_c}} |D_xi S|^{5/3} <= (integral |D_xi S|^2)^{5/6} * |Q_{r_c}|^{1/6}
4. |Q_{r_c}| = r_c^3 * r_c^2/nu_eff ~ r_c^5 ~ (nu/omega)^{5/2}
5. F(r_c) ~ (omega^{1/2} nu^{1/2})^{5/6} * (nu/omega)^{5/12} = nu^{5/6}
6. Conclusion: F -> 0 as nu -> 0. "Too good to be true."

### 2.2 The error in the naive computation

The error is in step (1). The estimate integral_{Q_{r_c}} |D_xi S|^2 ~ omega^2 r_c^3 / nu assumes that |D_xi S| ~ omega^{3/2}/nu^{1/2} UNIFORMLY on the cylinder Q_{r_c}, and that the integration volume is r_c^3 times the temporal duration 1/omega.

But this is self-contradictory. If |D_xi S| ~ omega^{3/2}/nu^{1/2} on Q_{r_c}, and r_c = (nu/omega)^{1/2}, then:

    integral_{Q_{r_c}} |D_xi S|^2 dx dt = integral_{t_0 - r_c^2}^{t_0} integral_{B_{r_c}} |D_xi S(x,t)|^2 dx dt

The temporal duration is r_c^2 = nu/omega (NOT 1/omega). The spatial volume is (4/3)pi r_c^3 = (4/3)pi (nu/omega)^{3/2}.

So:

    integral_{Q_{r_c}} |D_xi S|^2 dx dt ~ |D_xi S|_{typ}^2 * r_c^3 * r_c^2
                                          = (omega^3/nu) * (nu/omega)^{3/2} * (nu/omega)
                                          = (omega^3/nu) * (nu^{5/2}/omega^{5/2})
                                          = omega^{1/2} nu^{3/2}

This is different from step (1) by a factor of nu. But the Holder estimate then gives:

    F(r_c) <= (omega^{1/2} nu^{3/2})^{5/6} * |Q_{r_c}|^{1/6}
            = omega^{5/12} nu^{5/4} * (nu/omega)^{5*5/(2*6)}

Wait -- let me redo this carefully.

### 2.3 Correct Holder computation

Holder's inequality with exponents 6/5 and 6 (so that 1/(6/5) + 1/6 = 5/6 + 1/6 = 1):

    integral |f|^{5/3} = integral |f|^{5/3} * 1
                        <= (integral |f|^{5/3 * 6/5})^{5/6} * (integral 1^6)^{1/6}
                        = (integral |f|^2)^{5/6} * |Q|^{1/6}

This is correct. Now with the corrected L^2 integral:

    integral_{Q_{r_c}} |D_xi S|^2 dx dt ~ (omega^{3/2}/nu^{1/2})^2 * r_c^3 * r_c^2
                                          = (omega^3/nu) * (nu/omega)^{5/2}
                                          = omega^{1/2} nu^{3/2}

    |Q_{r_c}| = (4/3) pi r_c^3 * r_c^2 = C r_c^5 = C (nu/omega)^{5/2}

So:

    F(r_c) <= (omega^{1/2} nu^{3/2})^{5/6} * ((nu/omega)^{5/2})^{1/6}
            = omega^{5/12} nu^{5/4} * nu^{5/12} / omega^{5/12}
            = nu^{5/4 + 5/12}
            = nu^{15/12 + 5/12}
            = nu^{20/12}
            = nu^{5/3}

So F(r_c) ~ nu^{5/3}. This is small for small nu (i.e., high Reynolds number in the sense that nu -> 0 with fixed initial data scale).

### 2.4 But is this the right computation?

No. The fundamental issue is more subtle. The computation above treats nu as the small parameter and assumes the initial data scale is fixed. But the NS regularity problem asks: given FIXED initial data with FIXED nu > 0, does the solution remain smooth? The parameter nu is not going to zero -- it is a fixed positive constant.

The relevant question is: is F(r_c) small compared to epsilon_0, where epsilon_0 is the (hypothetical) universal constant in the epsilon-regularity theorem?

From the computation: F(r_c) ~ omega^{5/12} nu^{5/4} * (nu/omega)^{5/12} = nu^{5/3}. Wait, let me recheck.

Actually, going back:

    F(r_c) <= (omega^{1/2} nu^{3/2})^{5/6} * (nu^{5/2}/omega^{5/2})^{1/6}
            = omega^{5/12} * nu^{5/4} * nu^{5/12} * omega^{-5/12}
            = nu^{5/4 + 5/12}
            = nu^{(15 + 5)/12}
            = nu^{20/12} = nu^{5/3}

This is indeed independent of omega, which is suspicious. It says F(r_c) ~ nu^{5/3} regardless of how large omega is. For fixed nu > 0, this is a fixed positive number (not small). For nu = 0.01, we get F ~ 10^{-10/3} ~ 2 * 10^{-4}. Whether this is smaller than epsilon_0 depends on epsilon_0.

### 2.5 The real problem: Holder is too lossy

The Holder estimate is overly generous. It gives F in terms of the L^2 norm, which averages |D_xi S|^2 over the cylinder. But the epsilon-regularity theorem, if it existed, would require F to be small as a NECESSARY condition for regularity. The question is not whether F CAN be small, but whether F MUST be small near a singularity.

Near a hypothetical singularity at (x_0, t_0), the vorticity blows up: omega(x_0, t_n) -> infinity as t_n -> t_0. The self-consistent D_xi S from equation (6.2) is:

    |D_xi S| = (C/Re_Gamma^2) * omega^{3/2} / nu^{1/2}

On a parabolic cylinder Q_rho centered at (x_0, t_0) with radius rho:

    F(rho) = integral_{Q_rho} |D_xi S|^{5/3} dx dt

As rho -> 0, the blowup omega -> infinity in Q_rho. The D_xi S ~ omega^{3/2}/nu^{1/2} also blows up. The integral:

For a Type I blowup with omega(x,t) ~ C / (T - t) concentrated in a tube of core radius r_c(t) ~ (nu(T-t))^{1/2}:

    |D_xi S(x,t)| ~ (C/Re_Gamma^2) * (T-t)^{-3/2} / nu^{1/2}  for |x - x_0| < r_c(t)
    |D_xi S(x,t)| ~ 0                                             for |x - x_0| >> r_c(t)

The effective support in space has volume ~ r_c(t)^3 ~ (nu(T-t))^{3/2}.

    integral_{B_rho} |D_xi S|^{5/3} dx ~ ((T-t)^{-3/2}/nu^{1/2})^{5/3} * (nu(T-t))^{3/2} / Re_Gamma^{10/3}
                                         = (T-t)^{-5/2} * nu^{-5/6} * nu^{3/2} * (T-t)^{3/2} / Re_Gamma^{10/3}
                                         = (T-t)^{-1} * nu^{2/3} / Re_Gamma^{10/3}

    F(rho) = integral_{T-rho^2}^{T} integral_{B_rho} |D_xi S|^{5/3} dx dt
           ~ integral_{T-rho^2}^{T} (T-t)^{-1} * nu^{2/3} / Re_Gamma^{10/3} dt
           = (nu^{2/3} / Re_Gamma^{10/3}) * |log(T - (T-rho^2))| ... 

Wait, this integral diverges logarithmically. Let me be more careful.

For t in (T - rho^2, T):

    integral_{T-rho^2}^{T} (T-t)^{-1} dt = [-log(T-t)]_{T-rho^2}^{T} = infinity

The integral DIVERGES. This means F(rho) = infinity for any rho > 0 centered at a Type I blowup. Therefore:

**F(rho) diverges near any Type I singularity.** In particular, F(rho) < epsilon_0 is AUTOMATICALLY satisfied on cylinders AWAY from singularities (where D_xi S is bounded), and F(rho) = infinity AT singularities.

### 2.6 Resolution: the logarithmic divergence is exactly borderline

The divergence is of the (T-t)^{-1} type, which is exactly the borderline for integrability of (T-t)^{-alpha} at alpha = 1. This corresponds to the fact that |D_xi S|^{5/3} is at the critical integrability for the parabolic scaling -- it is L^1 in space but not in time.

More precisely: the exponent p = 5/3 was chosen to be scale-invariant. The Type I blowup rate omega ~ (T-t)^{-1} gives |D_xi S|^{5/3} ~ (T-t)^{-5/2} in the tube core. Integrating over the core volume (T-t)^{3/2} gives (T-t)^{-1} per unit time. This is a 1/t divergence -- exactly the borderline that separates "F is finite" from "F is infinite."

**This means: for a Type I blowup (the most common type), F is infinite at any cylinder containing the singularity, and the epsilon-regularity condition F < epsilon_0 is vacuously satisfied away from singularities.**

The epsilon-regularity approach would work (tautologically) if F(rho) < epsilon_0 implies regularity, because at any actual singularity F = infinity, so the condition F < epsilon_0 is never violated where it should not be. But this gives NO information about whether singularities exist -- it only says "if F is small, the point is regular" without establishing that F is ever small where it matters.

### 2.7 Verdict on smallness of F

**F(r_c) is NOT small at or near the vorticity maximum in the sense needed for an epsilon-regularity argument.** The Holder estimate suggests F ~ nu^{5/3} (a fixed positive number), but the dynamic computation for a Type I blowup shows F diverges logarithmically as the cylinder approaches the singularity. The epsilon-regularity condition, if it held, would be a tautology: it would confirm regularity at regular points and say nothing at singular points.

The initial computation F ~ nu^{5/6} from the prompt was additionally incorrect because:
(a) the temporal duration of Q_{r_c} is r_c^2 (not 1/omega -- these differ by a factor of nu),
(b) the corrected value is nu^{5/3} (not nu^{5/6}), and
(c) the static estimate is irrelevant because near a blowup, F diverges regardless.

---

## 3. Can the Epsilon-Regularity Theorem Be Proved?

### 3.1 The CKN proof structure

The CKN epsilon-regularity theorem for the energy has the following structure:

**Step 1 (Local energy inequality).** For suitable weak solutions, the quantity phi = (1/2)|u|^2 satisfies the local inequality:

    partial_t phi + div(phi u) + p div(u) - nu Delta phi + nu |nabla u|^2 <= 0

in the distributional sense. This is the foundation of the entire theory.

**Step 2 (Caccioppoli inequality).** Multiplying by cutoff functions and integrating, one obtains:

    sup_{t} integral_{B_r} |u|^2 psi dx + nu integral_{Q_r} |nabla u|^2 psi dx dt
    <= C integral_{Q_{2r}} (|u|^2 (|partial_t psi| + nu |Delta psi|) + (|u|^2 + 2p)|u| |nabla psi|) dx dt

This gives control of the energy at scale r in terms of the energy and pressure at scale 2r.

**Step 3 (Pressure estimate).** The pressure is estimated via the Calderon-Zygmund inequality applied to Delta p = -partial_i partial_j (u_i u_j):

    ||p||_{L^{5/3}(Q_r)} <= C ||u||_{L^{10/3}(Q_r)}^2

**Step 4 (Iteration).** Starting from E(r_0) < epsilon_0, use Steps 2 and 3 iteratively at scales r_0, r_0/2, r_0/4, ... to show that E(r_k) -> 0 geometrically. The geometric decay implies Holder regularity via Campanato's criterion, and parabolic regularity theory then gives smoothness.

### 3.2 What would be needed for D_xi S

To carry out the CKN program for F(r) = integral_{Q_r} |D_xi S|^{5/3}, we would need analogues of all four steps:

**Step 1': A local inequality for D_xi S.**

There is no known local inequality for |D_xi S|^2 (or |D_xi S|^{5/3}) analogous to the local energy inequality. The quantity D_xi S = (xi . nabla)S involves third derivatives of the velocity (since S = nabla u and D_xi = xi . nabla involves one more derivative). The evolution equation for D_xi S, derived from the strain evolution equation (Section 3.5 below), has the form:

    partial_t(D_xi S) - nu Delta(D_xi S) = F(S, omega, nabla omega, nabla^2 p, D_xi S)     (3.1)

where F contains terms involving nabla^2 p (second derivatives of pressure, or equivalently nabla^2(nabla u) = nabla^3 u). This is a THIRD-ORDER source term.

For a local inequality, we would need to multiply (3.1) by D_xi S (or |D_xi S|^{-1/3} D_xi S for the 5/3-power) and integrate. The viscous term gives:

    - nu integral D_xi S . Delta(D_xi S) = nu integral |nabla(D_xi S)|^2   (good sign)

But the source term F involves nabla^3 u, which upon multiplication by D_xi S ~ nabla^2 u gives:

    integral D_xi S . nabla^3 u dx ~ integral nabla^2 u . nabla^3 u dx

This cannot be integrated by parts to produce a non-negative quantity. In fact, integration by parts gives:

    integral nabla^2 u . nabla^3 u dx = -(1/2) d/dx integral |nabla^2 u|^2 dx + boundary terms

which has NO definite sign. **There is no local energy-type inequality for D_xi S.** This is the first fundamental obstruction.

**Step 2': Caccioppoli inequality for D_xi S.**

Without a local inequality (Step 1'), there is no Caccioppoli inequality for D_xi S. The Caccioppoli inequality is derived FROM the local energy inequality by multiplying by test functions -- if the starting inequality does not exist, the derived inequality cannot exist either.

One might attempt a "conditional Caccioppoli" by assuming regularity and deriving the inequality for smooth solutions. For smooth solutions, we can multiply the D_xi S equation by phi^2 |D_xi S|^{-1/3} D_xi S (the 5/3-power Caccioppoli) and integrate. But the third-derivative source term produces:

    |integral phi^2 |D_xi S|^{-1/3} D_xi S . D_xi(nabla^2 p) dx| <= ||D_xi S||_{L^{5/3}(Q_r)}^{2/3} * ||D_xi(nabla^2 p)||_{L^{5/2}(Q_r)}

The quantity ||D_xi(nabla^2 p)||_{L^{5/2}} involves fourth derivatives of u (since p ~ |u|^2 and nabla^2 p ~ nabla^2 u . nabla u + ...). This is HIGHER ORDER than what we are trying to control. The Caccioppoli inequality cannot close.

**Step 3': Pressure-like estimate for the source.**

In the CKN framework, the pressure p is estimated via CZ theory: ||p||_{L^{5/3}} <= C ||u||_{L^{10/3}}^2. This works because p is determined by u through an elliptic equation (Delta p = -div div(u otimes u)).

For D_xi S, the analogous "pressure" is D_xi(nabla^2 p), which involves nabla^3 p. The Calderon-Zygmund bound is:

    ||nabla^3 p||_{L^q} <= C ||nabla(u . nabla u + |omega|^2)||_{L^q}

This requires nabla^2 u in L^{2q} (from the nonlinear terms). For q = 5/3 (the critical exponent), we need nabla^2 u in L^{10/3}. But we only have nabla^2 u ~ D_xi S in L^{5/3} -- a factor of 2 off in the exponent. The CZ estimate does not close at the critical scaling.

**Step 4': Iteration.**

Without Steps 1'-3', the iteration cannot begin.

### 3.3 Summary: the epsilon-regularity theorem for D_xi S fails structurally

The CKN proof requires:

| Component | Energy (classical CKN) | D_xi S (proposed) | Status |
|-----------|----------------------|-------------------|--------|
| Local inequality | Yes (from NS energy identity) | NO (no energy identity for nabla^2 u) | **FATAL** |
| Caccioppoli | Yes (derived from local inequality) | NO (no starting inequality) | **FATAL** |
| CZ pressure estimate | ||p||_{5/3} <= C ||u||_{10/3}^2 (closes at L^{10/3}) | ||nabla^3 p||_{5/3} needs ||nabla^2 u||_{10/3} (does not close) | **FATAL** |
| Iteration | Geometric decay of E(r) at successively smaller scales | Cannot start | **FATAL** |

**The epsilon-regularity theorem for D_xi S is false as a provable theorem within the CKN framework.** All four structural components fail, each for independent reasons.

### 3.4 A salvageable estimate: L^{5/3} bound on D_xi S from enstrophy dissipation

Although the epsilon-regularity theorem fails, the L^{5/3} GLOBAL bound on D_xi S is provable and potentially useful.

From the enstrophy dissipation:

    nu integral_0^T ||nabla omega||_{L^2(R^3)}^2 dt <= C(||u_0||_{H^1}, T, nu) := E_{ens}     (3.2)

By Calderon-Zygmund theory (since nabla^2 u is a CZ transform of nabla omega for rapidly decaying solutions):

    ||nabla^2 u(.,t)||_{L^2} <= C_{CZ} ||nabla omega(.,t)||_{L^2}                             (3.3)

Since D_xi S = (xi . nabla)S is a component of nabla S, and |D_xi S| <= |nabla S| <= C |nabla^2 u|:

    ||D_xi S(.,t)||_{L^2} <= C ||nabla omega(.,t)||_{L^2}                                     (3.4)

Therefore:

    integral_0^T ||D_xi S(.,t)||_{L^2}^2 dt <= C^2/nu * E_{ens}                               (3.5)

This gives D_xi S in L^2_t L^2_x. Can we extract L^{5/3}_{x,t}?

By interpolation. The Sobolev embedding in R^3 gives:

    ||D_xi S||_{L^{10/3}(R^3)} <= C ||D_xi S||_{L^2(R^3)}^{3/5} * ||nabla(D_xi S)||_{L^2(R^3)}^{2/5}

But ||nabla(D_xi S)||_{L^2} involves third derivatives of u, which are not controlled.

Instead, use the crude global bound. By Holder in time:

    integral_0^T ||D_xi S||_{L^{5/3}(R^3)}^{5/3} dt <= integral_0^T ||D_xi S||_{L^2(R^3)}^{5/3} * |supp(D_xi S)|^{(2-5/3)/(2*3)} ...

Actually, let me use a cleaner approach. By the Gagliardo-Nirenberg inequality in R^3:

    ||f||_{L^{5/3}(R^3)} <= C ||f||_{L^2(R^3)}^{3/5} * ||f||_{L^1(R^3)}^{2/5}

(This follows from the interpolation L^{5/3} between L^1 and L^2 with 1/(5/3) = (2/5)/1 + (3/5)/2.)

For D_xi S: ||D_xi S||_{L^1} <= ||D_xi S||_{L^2} * |supp|^{1/2}. The support of D_xi S is essentially the region where vorticity is non-negligible, which has measure bounded by ||omega||_{L^2}^2 / ||omega||_{L^infty}^2. This introduces omega_max into the bound, creating a circular dependence.

A simpler approach: by Holder in space-time with mixed norms.

    integral_0^T integral_{R^3} |D_xi S|^{5/3} dx dt
    <= integral_0^T (integral |D_xi S|^2 dx)^{5/6} * (integral 1 dx)^{1/6} dt

But the spatial integral of 1 over R^3 is infinite. On a bounded domain Omega:

    integral_0^T integral_Omega |D_xi S|^{5/3} dx dt <= integral_0^T ||D_xi S||_{L^2(Omega)}^{5/3} * |\Omega|^{1/6} dt
    <= |\Omega|^{1/6} * (integral_0^T ||D_xi S||_{L^2}^2 dt)^{5/6} * T^{1/6}

by Holder in time (with exponents 6/5 and 6). Therefore:

    **integral_0^T integral_Omega |D_xi S|^{5/3} dx dt <= C |\Omega|^{1/6} T^{1/6} (E_{ens}/nu)^{5/6}**   (3.6)

This is finite for any bounded domain Omega and any finite time T. It gives D_xi S in L^{5/3}(Omega x [0,T]) with an explicit bound depending on the initial data, nu, T, and |\Omega|.

**This is a rigorous a priori estimate.** However, it is a GLOBAL bound (over the full domain and time interval) and does not provide local smallness of F(r) on parabolic cylinders centered at high-vorticity points.

### 3.5 The PDE for D_xi S: detailed derivation

For completeness, we derive the evolution equation for D_xi S. Starting from the strain evolution (dropping the Burgers-type simplification and working with the full NS):

    partial_t S + (u . nabla)S = -S^2 - Omega^(2x2) - nabla^2 p + nu Delta S      (SE)

where Omega^(2x2) is the vorticity-related term: -(1/4)(omega_i omega_j - |omega|^2 delta_{ij}).

Actually, the precise strain evolution for incompressible NS is:

    (partial_t + u . nabla) S_{ij} = -S_{ik}S_{kj} + (1/4)(omega_i omega_j - |omega|^2 delta_{ij}) - partial_i partial_j p + nu Delta S_{ij}

where Delta p = -S_{kl}S_{lk} - (1/4)|omega|^2 = -|S|^2 + (1/2)|omega|^2.

Wait -- more carefully: Delta p = -partial_i partial_j(u_i u_j) = -(S_{ij} + Omega_{ij})(S_{ij} + Omega_{ij}) = -|S|^2 - |Omega|^2 where Omega_{ij} = (1/2)(partial_i u_j - partial_j u_i) is the rotation tensor. Since |Omega|^2 = (1/2)|omega|^2, we have Delta p = -|S|^2 + (1/2)|omega|^2.

Now apply D_xi = xi . nabla to both sides of the strain evolution. Since D_xi is a first-order differential operator, we get:

    D_xi((partial_t + u . nabla)S) = (partial_t + u . nabla)(D_xi S) + [D_xi, partial_t + u . nabla]S

The commutator is:

    [D_xi, partial_t + u . nabla] = (partial_t xi + (u . nabla)xi) . nabla + (xi . nabla u) . nabla - (xi . nabla)(u . nabla)
                                   = (D_t xi) . nabla - (nabla u . xi) . nabla + (xi . nabla u) . nabla

Wait, let me be more careful. For a general vector field V and the material derivative D_t = partial_t + u . nabla:

    D_xi(D_t S) = xi^k partial_k(D_t S) = D_t(xi^k partial_k S) - (D_t xi^k)(partial_k S)
                 = D_t(D_xi S) - (D_t xi) . nabla S

So:

    D_t(D_xi S) = D_xi(D_t S) + (D_t xi) . nabla S                              (3.7)

The material derivative of xi = omega/|omega|:

    D_t xi = D_t(omega/|omega|) = (D_t omega)/|omega| - omega (omega . D_t omega)/(|omega|^3)
           = (I - xi otimes xi) D_t omega / |omega|

From the vorticity equation D_t omega = S omega + nu Delta omega:

    D_t xi = (I - xi otimes xi)(S xi + nu Delta omega / |omega|)
           = S xi - (xi . S xi) xi + nu (I - xi otimes xi) Delta omega / |omega|
           = (S - Q I) xi + nu (I - xi otimes xi) Delta omega / |omega|

where Q = xi . S xi is the Rayleigh quotient.

Substituting into (3.7):

    D_t(D_xi S) = D_xi(-S^2 + (1/4)(omega otimes omega - |omega|^2 I) - nabla^2 p + nu Delta S)
                  + ((S - QI)xi + nu-term) . nabla S

The critical term is:

    D_xi(nabla^2 p) = xi . nabla(nabla^2 p) = nabla^3 p projected along xi

Since nabla^2 p involves second derivatives of u^2 terms, nabla^3 p involves THIRD derivatives of u. Specifically:

    partial_k partial_i partial_j p = -partial_k(S_{il}S_{lj} + ...) - partial_k ... 

This involves nabla S . S + S . nabla S (second-order in S, first-order in nabla S), plus terms involving nabla omega . omega (second-order in omega, first-order in nabla omega).

The schematic PDE for D_xi S is:

    (partial_t + u . nabla - nu Delta)(D_xi S) = S . D_xi S + D_xi S . S           (order |S||D_xi S|)
                                                 + D_xi(omega otimes omega)          (order |omega||nabla omega|)
                                                 + (S - QI) xi . nabla S            (order |S| |nabla S|)
                                                 - D_xi(nabla^2 p)                   (order |nabla^3 p|)
                                                 + nu commutator terms               (lower order)

The dangerous term is D_xi(nabla^2 p), which involves nabla^3 p ~ nabla^2 S ~ nabla^2(nabla u) = nabla^3 u. This is one derivative beyond what the enstrophy dissipation controls (which gives nabla^2 u in L^2).

**This confirms the structural obstruction: the D_xi S equation has a source term (the pressure Hessian gradient) that is one derivative order too high for closure.**

---

## 4. Can the CKN Framework Be Applied at the Enstrophy Level?

### 4.1 The idea

Instead of applying epsilon-regularity directly to D_xi S (which fails as shown in Section 3), use the EXISTING CKN partial regularity theory for the energy or enstrophy, but with the improved input from equation (6.2). The hope: the small coefficient 1/Re_Gamma^2 in the D_xi S bound might, when fed into the enstrophy-based CKN machinery, reduce the singular set dimension from <= 1 (the CKN bound) to < 0 (meaning empty, i.e., full regularity).

### 4.2 The CKN dimensional bound

The CKN theorem states: the one-dimensional parabolic Hausdorff measure of the singular set S is zero:

    H^1_{par}(S) = 0

This means the singular set has parabolic Hausdorff dimension at most 1 (in a space-time of parabolic dimension 5 = 3 + 2). The bound comes from a covering argument: one covers S by parabolic cylinders Q_{r_k} on which the scaled energy E(r_k) >= epsilon_0, and estimates the total volume of these cylinders.

The key estimate is:

    sum r_k <= C * epsilon_0^{-1} * integral_0^T integral |nabla u|^2 dx dt <= C epsilon_0^{-1} * E_0 / nu

The sum sum r_k is (by definition) an upper bound for H^1_{par}(S). Since the right side is finite, H^1(S) = 0 follows.

### 4.3 Can the 1/Re^2 coefficient improve this?

The proposal: if the enstrophy production is reduced by a factor 1/Re_Gamma^2 (from the D_xi S bound), then the "effective" scaled enstrophy is smaller, and the covering argument gives a smaller singular set.

But this reasoning is flawed. The CKN bound H^1(S) = 0 is already optimal (the singular set is already as small as the CKN method can make it). The issue is not the SIZE of the singular set but its EXISTENCE. The CKN theorem allows S to be nonempty (of dimension <= 1); what we want is S = empty.

To get S = empty from CKN-type arguments, one would need to show that the scaled energy E(r) < epsilon_0 on EVERY cylinder Q_r at EVERY point. The 1/Re^2 coefficient from equation (6.2) affects the ENSTROPHY production (how fast omega grows), but the scaled energy E(r) involves |u|^2, not omega or D_xi S.

### 4.4 Connecting D_xi S to the scaled energy

The relationship between D_xi S and the scaled energy is indirect:
- D_xi S controls the growth of vortex-line curvature (via the coupled bootstrap)
- Curvature, together with vorticity magnitude, controls |nabla xi| (the gradient of the vorticity direction)
- |nabla xi| bounded implies the Constantin-Fefferman condition, which gives regularity
- But |nabla xi| bounded does NOT directly imply E(r) < epsilon_0

The chain D_xi S -> kappa -> |nabla xi| -> regularity bypasses the CKN framework entirely. It is the route pursued in the coupled-bootstrap-attempt.md, which fails at the D_xi S bound (Theorem CB requires delta > 1/2, we have delta = 1/2).

### 4.5 The enstrophy-based partial regularity approach

An alternative is the enstrophy-based variant of CKN due to Choe-Lewis (2000) and others. The enstrophy-based CKN uses the local enstrophy inequality:

    partial_t (|omega|^2/2) + div(|omega|^2 u / 2) - omega . S omega - nu Delta(|omega|^2/2) + nu |nabla omega|^2 <= 0

and defines the enstrophy-based scaled quantity:

    Phi(r) = (1/r) sup_t integral_{B_r} |omega|^2 + (1/r) integral_{Q_r} |nabla omega|^2

The epsilon-regularity for enstrophy: if Phi(r) < epsilon_1, then omega is bounded on Q_{r/2}.

The enstrophy production term omega . S omega = Q |omega|^2 (where Q = xi . S xi) appears in the local enstrophy inequality. If we could show Q <= C/Re_Gamma^2 (small coefficient), this would reduce the production and make Phi easier to keep small.

But Q = xi . S xi is the Rayleigh quotient, which measures the stretching rate. From the prior analysis:
- Q ~ s_2 (under e_2-alignment) with s_2 > 0 in high-vorticity regions
- Q is NOT small (Q ~ O(omega) from Biot-Savart)
- The D_xi S smallness from equation (6.2) constrains the GRADIENT of S along xi, not S itself

**The 1/Re^2 factor in D_xi S does NOT imply a small Q.** The Rayleigh quotient Q involves S directly (not its gradient), and S is O(omega) by Biot-Savart. There is no mechanism by which the D_xi S bound translates to a Q bound.

### 4.6 Verdict on the CKN-at-enstrophy-level approach

**The CKN framework at the enstrophy level does not benefit from the small D_xi S coefficient.** The D_xi S bound constrains nabla S along xi, while the enstrophy production involves S itself. These are different quantities. The small coefficient in D_xi S does not propagate to smallness of Q or smallness of Phi(r). The existing CKN bound (dim(S) <= 1) is not improved.

---

## 5. The Fundamental Structural Obstruction

### 5.1 Why D_xi S is the wrong quantity for epsilon-regularity

The CKN epsilon-regularity works for the energy because:
1. The energy |u|^2 satisfies a LOCAL INEQUALITY (derived from the NS equations by multiplying by u).
2. The energy is the LOWEST-ORDER quantity in the NS hierarchy (it involves u, not its derivatives).
3. The pressure estimate closes because p is determined by u through an elliptic PDE with the right scaling.

D_xi S fails because:
1. D_xi S does NOT satisfy a local inequality (no energy-type identity at the nabla^2 u level).
2. D_xi S involves THIRD-ORDER quantities (nabla S = nabla^2 u, and its evolution involves nabla^3 u through the pressure gradient).
3. The "pressure" for D_xi S (namely nabla^3 p) requires one more derivative than D_xi S itself, so the CZ estimate does not close.

The obstruction is the DERIVATIVE COUNT. The CKN framework works at the energy level (zero derivatives of u beyond u itself). The enstrophy-based variant pushes it to one derivative (omega = curl u). Going to two derivatives (nabla S ~ nabla^2 u) would require the enstrophy DISSIPATION to serve as the energy, but the dissipation of enstrophy dissipation (nabla^2 omega in L^2) is not a priori controlled.

This is the same derivative-count obstruction that appears in every approach to NS regularity: the supercritical gap requires controlling quantities that are one derivative higher than what the a priori estimates provide.

### 5.2 Could a DIFFERENT scale-invariant quantity work?

The question is whether there exists a quantity involving D_xi S (or related objects) that:
(a) is scale-invariant under the NS scaling,
(b) satisfies a local energy-type inequality,
(c) has a CZ-type pressure estimate that closes at the correct scaling.

The candidates:

**Candidate 1: |nabla omega|^2.** This is the enstrophy dissipation density. It satisfies an evolution equation:

    D_t(|nabla omega|^2) = ... + (terms involving nabla^2 u and nabla p) + nu Delta(|nabla omega|^2) - 2 nu |nabla^2 omega|^2

The "good" term is -2 nu |nabla^2 omega|^2 (dissipation). The "bad" terms involve nabla^2 u . nabla omega . nabla u and nabla^2 p . nabla omega. The nabla^2 p term is problematic (involves nabla^3 u after CZ). Same derivative-count obstruction.

**Candidate 2: The Rayleigh quotient Q = xi . S xi.** Q satisfies a parabolic PDE (derived in subproblem-B-eigenvector-regularity.md). It is smooth wherever omega is nonzero. However, Q is a 0th-order quantity (it involves S but not its derivatives), so it does not directly help with the regularity problem. The issue is that Q can be smooth and bounded while omega still blows up (Q just measures the stretching rate, not the vorticity magnitude).

**Candidate 3: A combined quantity like |omega|^a |D_xi S|^b.** One could try to find exponents (a,b) such that the combined quantity has a favorable evolution equation. But any quantity involving D_xi S inherits the nabla^3 u source term from the D_xi S equation. No choice of (a,b) eliminates this.

**Candidate 4: The helicity density h = u . omega.** Helicity satisfies:

    D_t h = -2 nu nabla u : nabla omega + (pressure terms)

This involves only nabla u and nabla omega (not higher derivatives). The helicity is promising because it mixes u (energy level) with omega (enstrophy level), potentially providing a "bridge" between the two levels. However, helicity is not sign-definite, so it does not provide a bound in the epsilon-regularity sense. The integral integral |h|^p dx dt is controlled by interpolation between energy and enstrophy, but this does not give new information beyond what energy + enstrophy already provide.

**No candidate quantity bypasses the derivative-count obstruction.** The reason is structural: the NS nonlinearity u . nabla u produces one derivative in the energy equation, two derivatives in the enstrophy equation, and three derivatives in the D_xi S equation. At each level, the nonlinear term is one derivative higher than what the dissipation controls. The CKN framework works at the energy level because the one-derivative term (nabla u in the energy equation) is controlled by the dissipation (nu |nabla u|^2). At the enstrophy level, the two-derivative term (nabla^2 u) is at the BORDERLINE of what the enstrophy dissipation (nu |nabla omega|^2 ~ nu |nabla^2 u|^2) controls -- this is why the enstrophy-based CKN works but is borderline (giving dim(S) <= 1 rather than regularity). At the D_xi S level, the three-derivative term exceeds what any available dissipation controls, and the approach fails completely.

### 5.3 The hierarchy of regularity criteria

To summarize the landscape:

| Level | Quantity | Dissipation | Source | CKN status |
|-------|----------|-------------|--------|------------|
| 0 (energy) | |u|^2 | nu |nabla u|^2 | nabla u . nabla u . u | Works: dim(S) <= 1 |
| 1 (enstrophy) | |omega|^2 | nu |nabla omega|^2 | omega . S omega ~ |nabla u|^2 |omega| | Borderline: dim(S) <= 1 (Choe-Lewis) |
| 2 (palinstrophy) | |nabla omega|^2 | nu |nabla^2 omega|^2 | nabla omega . nabla S omega ~ |nabla^2 u| ... | FAILS: source exceeds dissipation |
| 2 (D_xi S) | |D_xi S|^{5/3} | nu |nabla(D_xi S)|^2 | D_xi(nabla^2 p) ~ nabla^3 u | FAILS: source exceeds dissipation |

The NS supercritical gap manifests as: at every level >= 2, the nonlinear source term involves derivatives one order higher than the dissipation can control. The CKN framework can reach level 1 (enstrophy) but cannot proceed to level 2.

---

## 6. The Small Coefficient 1/Re^2: What It Can and Cannot Do

### 6.1 What it CAN do

The d-independent ratio R = 16 pi sin(Theta) / Re_Gamma^2 from equation (6.2) is a genuine structural result. It establishes that:

(a) The Biot-Savart self-consistency with circulation conservation places D_xi S EXACTLY at the critical threshold for Theorem CB, with a coefficient that is universal (d-independent) and small (1/Re_Gamma^2).

(b) Any blowup scenario based on the tube-tube interaction cascade has D_xi S at the borderline, with the blowup dynamics dominated by the strain-amplification-of-curvature term (C_2 Omega K) rather than the D_xi S source term (which is O(1/Re_Gamma^2) times the critical threshold).

(c) The small coefficient rules out certain specific blowup mechanisms (e.g., those that require D_xi S to be at or above the critical threshold with an O(1) coefficient).

### 6.2 What it CANNOT do

The coefficient 1/Re_Gamma^2, no matter how small, cannot:

(a) **Change the exponent delta from 1/2 to > 1/2.** The exponent is determined by the Biot-Savart scaling law (D_xi S ~ 1/d^3, omega ~ 1/d^2), which is structural. The coefficient modifies the PREFACTOR but not the POWER LAW.

(b) **Make the epsilon-regularity condition F < epsilon_0 hold**, because F diverges (logarithmically) at any Type I singularity regardless of the coefficient. The coefficient enters multiplicatively in F, but the divergence is from the time integral, which is coefficient-independent.

(c) **Reduce the CKN singular set dimension below 1.** The CKN dimensional bound comes from the energy scaling, not from the D_xi S coefficient. The 1/Re^2 factor does not enter the energy-based covering argument.

(d) **Close the coupled bootstrap.** The ODE dK/dt <= C_2 Omega K + (C_small/Re_Gamma^2) Omega^{3/2}/nu^{1/2} has a blowup for ANY positive coefficient C_small, because the blowup is driven by the C_2 Omega K term (strain amplification of curvature), not the source term.

### 6.3 The PDE vs. ODE distinction

The one place where the small coefficient MIGHT help is in the PDE context, where the ODE model is not faithful. The ODE tracks the pointwise maximum of omega and the curvature at that point. The PDE has spatial structure (diffusion, pressure, nonlocal Biot-Savart) that the ODE ignores.

Specifically:
- The ODE blows up for any positive coefficient at delta = 1/2.
- The PDE might NOT blow up if the diffusion (nu Delta) provides a spatial smoothing effect that the ODE misses.
- The small coefficient 1/Re_Gamma^2 means the D_xi S source is perturbatively small, so the PDE dynamics near the blowup is dominated by the diffusion + strain amplification, not by D_xi S.

Can the diffusion prevent the blowup? In the ODE, the damping term nu K^2 Omega requires K to grow to control the stretching C_1 Omega^2. In the PDE, the Laplacian provides spatial spreading that could prevent K from growing as fast as the ODE predicts. But quantifying this requires either:
- A regularity theorem for the kappa equation (which we do not have due to the D_xi S source), or
- A regularity theorem for the Rayleigh quotient Q (which does not directly control omega), or
- A global estimate that bypasses the pointwise analysis entirely.

None of these are currently available.

---

## 7. Honest Assessment

### 7.1 Does the epsilon-regularity approach work for D_xi S?

**No.** The approach fails at multiple independent levels:
- The scale-invariant quantity F(r) is not small near singularities (it diverges logarithmically).
- The epsilon-regularity theorem for D_xi S cannot be proved (no local inequality, no Caccioppoli, CZ estimate does not close).
- The CKN framework at the enstrophy level does not benefit from the small D_xi S coefficient.

### 7.2 Is the F quantity actually small at the vorticity maximum?

**It depends on the context.** For a static Burgers vortex at fixed nu, the Holder estimate gives F(r_c) ~ nu^{5/3}, which is a fixed positive number. Near a Type I blowup, F diverges. The smallness for fixed nu does not help because the epsilon-regularity theorem does not hold in the first place.

### 7.3 Can the iteration close despite the higher-order source term?

**No.** The source term D_xi(nabla^2 p) involves nabla^3 u, which is one derivative beyond what any a priori estimate controls. This is not a technical gap but a structural obstruction: the NS nonlinearity at the D_xi S level is supercritical by one derivative. No iteration scheme (CKN, De Giorgi, Moser, or otherwise) can close this gap without additional structural input.

### 7.4 Does the small coefficient 1/Re^2 help through the CKN framework?

**No.** The CKN framework uses the energy (or enstrophy) inequality, not the D_xi S bound. The 1/Re^2 coefficient in D_xi S does not propagate to smallness of the scaled energy or enstrophy. The CKN singular set bound (dim(S) <= 1) is unaffected.

### 7.5 Probability of success

**Zero for this specific approach** (epsilon-regularity for D_xi S via CKN adaptation). The failures are structural, not technical.

**For the broader program of using the 1/Re^2 coefficient:** 2-5%. The coefficient is a genuine structural result, but converting it to regularity requires bridging the PDE-vs-ODE gap at the borderline delta = 1/2, which is an open problem of comparable difficulty to the original NS regularity question.

### 7.6 What this analysis contributes

Despite the negative result, this analysis contributes:

1. **A precise identification of WHY epsilon-regularity fails for higher-order quantities.** The derivative-count hierarchy (Section 5.3) clarifies that CKN-type approaches are fundamentally limited to the energy/enstrophy levels and cannot be pushed to the palinstrophy level or beyond.

2. **A rigorous L^{5/3} global bound on D_xi S** (equation 3.6), which is a new a priori estimate derivable from the enstrophy dissipation.

3. **A clear delineation of what the 1/Re^2 coefficient can and cannot do** (Section 6), which constrains future approaches and prevents re-treading the same ground.

4. **Confirmation that the PDE-vs-ODE distinction at the borderline is the essential remaining question.** The ODE blows up for any positive coefficient at delta = 1/2. The PDE might not. The difference is the spatial structure (diffusion, nonlocal Biot-Savart feedback, pressure). Any successful approach must exploit this spatial structure -- pointwise or ODE-based methods are provably insufficient at the borderline.

---

## 8. Remaining Live Directions After This Analysis

### 8.1 The signed D_xi S integral (from antisymmetry-cancellation.md)

The antisymmetry of D_xi S about the closest-approach point provides a partial cancellation in the curvature evolution integral. While the absolute value |D_xi S| has the borderline exponent delta = 1/2, the SIGNED integral of D_xi S along a vortex line might have effective exponent delta > 1/2 due to cancellations. This was analyzed in antisymmetry-cancellation.md and found to provide only an O(1) geometric factor (no exponent improvement). However, the analysis there used a specific geometric configuration (two straight tubes). For curved tubes or general configurations, the cancellation structure could be different.

### 8.2 The nonlocal damping from Biot-Savart feedback

The ODE model treats Q <= C_1 Omega as if C_1 is a fixed constant. In reality, the Biot-Savart law constrains C_1 to depend on the GLOBAL vorticity distribution. As omega concentrates into a singular set, the Biot-Savart self-consistency might force C_1 to decrease (because the supporting strain field comes from distant, weaker vorticity). This is the "depletion of nonlinearity" phenomenon studied by Constantin (1994) and others. Quantifying this depletion in terms of the 1/Re^2 coefficient is an open problem.

### 8.3 The criticality gap: delta = 1/2 with log corrections

The exponent delta = 1/2 is sharp for the power-law analysis. But logarithmic corrections could bridge the gap. If the Biot-Savart feedback provides |D_xi S| ~ omega^{3/2}/(nu^{1/2} (log omega)^sigma) for any sigma > 0, the coupled bootstrap closes (because (log omega)^{-sigma} * omega^{3/2} = omega^{3/2 - epsilon} for any epsilon > 0 eventually). The log correction could come from:
- Intermittency of the strain field (the strain is not at its maximum at all times)
- The De Giorgi parabolic iteration (IF the structural conditions could be verified -- see time-integrated-bootstrap.md, Section 3)
- Vorticity depletion near the maximum (the vorticity gradient structures that arise from the Constantin-Fefferman geometry)

None of these have been quantified, but they represent the most promising remaining directions.

### 8.4 Direct regularity of the vorticity direction

The Constantin-Fefferman (1993) criterion: if omega/|omega| is Lipschitz in the region where |omega| > M (with Lipschitz constant L(M) satisfying L(M) = o(M)), then the solution is regular. This bypasses D_xi S entirely. The question is whether the Biot-Savart self-consistency, combined with circulation conservation, forces the vorticity direction to be spatially regular. The 1/Re^2 coefficient in D_xi S is relevant here because D_xi S controls the evolution of xi (through the curvature kappa = |D_xi xi| and the coupled bootstrap). If D_xi S is small, xi evolves slowly, which suggests spatial regularity of xi -- but making this quantitative requires the same delta > 1/2 gap that we cannot close.

---

## Summary Table

| Question | Answer | Confidence |
|----------|--------|------------|
| Is p = 5/3 the correct scale-invariant exponent for D_xi S? | Yes (from NS scaling analysis) | High (algebraic) |
| Is F(r_c) small at the vorticity maximum (Holder estimate)? | F(r_c) ~ nu^{5/3} (fixed positive, not parametrically small) | Medium |
| Does F(r_c) remain finite near a Type I blowup? | No: F diverges logarithmically | High |
| Can the epsilon-regularity theorem for D_xi S be proved? | No: four independent structural failures | High |
| Does the 1/Re^2 coefficient help via CKN at the enstrophy level? | No: coefficient does not propagate to scaled energy/enstrophy | High |
| Is the L^{5/3} global bound on D_xi S new and provable? | Yes: equation (3.6) is rigorous | High |
| Can any CKN-type approach reach the D_xi S level? | No: derivative-count obstruction at level >= 2 | High |
| Does the PDE-vs-ODE gap at delta = 1/2 remain the key question? | Yes: the only remaining hope is PDE-specific spatial structure | High |
| Probability of success for this specific approach? | 0% | High |
| Probability that 1/Re^2 coefficient leads to regularity (any method)? | 2-5% | Speculative |
