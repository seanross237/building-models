# Curvature Evolution Analysis: Can Vortex-Line Curvature Blow Up Under NS Dynamics?

**Date:** 2026-04-02
**Parent:** Direction 3 (Vorticity-Direction Regularity), post-DHY-Burgers-Test
**Purpose:** Decisive analysis of whether the curvature kappa = |D_xi xi| of vortex lines can blow up in finite time, completing the chain from the DHY condition to (non-)regularity.
**Depends on:** direction-3-vorticity-direction.md, dhy-burgers-test.md, subproblem-E-s2-dynamics.md

---

## Summary of the Chain So Far

1. The Deng-Hou-Yu theorem (2005): if |D_xi xi| is bounded on {|omega| > M}, then the NS solution is regular.
2. The DHY-Burgers test (this pursuit): for a bent Burgers vortex tube with axis curvature kappa, |D_xi xi| = kappa + O(kappa^2 r_c), bounded uniformly in Re, with corrections that decrease at higher Re.
3. The remaining question: **does kappa = |D_xi xi| stay bounded for general NS solutions?**

This document derives the evolution equation for D_xi xi, analyzes its structure, and determines whether a structural mechanism prevents kappa blowup.

---

## Part 1: Derivation of the Evolution Equation for eta = D_xi xi

### 1.1 Setup and notation

We work with:
- omega: vorticity, evolving by D_t omega = (omega . nabla)u + nu Delta omega = S omega + nu Delta omega
- xi = omega/|omega|: unit vorticity direction
- |omega|: vorticity magnitude
- S = sym(nabla u): strain rate tensor
- P_perp = I - xi (x) xi: projection orthogonal to xi
- eta = D_xi xi = (xi . nabla)xi: curvature vector of vortex lines
- kappa = |eta|: curvature of vortex lines

The established xi evolution (from direction-3-vorticity-direction.md, equation (Dir)):

    D_t xi = P_perp(S xi) + (nu/|omega|) P_perp(Delta omega)                     (1)

We also use the magnitude evolution:

    D_t |omega| = (xi . S xi)|omega| + nu xi . Delta omega                        (2)

Note that eta is perpendicular to xi: since |xi|^2 = 1, taking D_xi gives 2 xi . D_xi xi = 0, i.e., xi . eta = 0.

### 1.2 The commutator [D_t, D_xi]

We need to apply D_xi = (xi . nabla) to equation (1). First, we compute the commutator [D_t, D_xi].

D_t = d_t + u . nabla is the material derivative. D_xi = xi . nabla = xi_k partial_k.

    [D_t, D_xi] f = D_t(D_xi f) - D_xi(D_t f)
                   = D_t(xi_k partial_k f) - xi_k partial_k(D_t f)

Expanding D_t(xi_k partial_k f):

    D_t(xi_k partial_k f) = (D_t xi_k)(partial_k f) + xi_k D_t(partial_k f)

Now D_t(partial_k f) = partial_k(D_t f) - (partial_k u_j)(partial_j f), from the commutator [D_t, partial_k] = -(partial_k u_j) partial_j (the standard material derivative commutator with spatial derivatives).

Therefore:

    D_t(xi_k partial_k f) = (D_t xi_k)(partial_k f) + xi_k partial_k(D_t f) - xi_k (partial_k u_j)(partial_j f)

So:

    [D_t, D_xi] f = (D_t xi_k)(partial_k f) - xi_k (partial_k u_j)(partial_j f)
                   = (D_t xi) . nabla f - (xi . nabla u) . nabla f
                   = ((D_t xi) - (xi . nabla)u) . nabla f                           (3)

Note: (xi . nabla)u = A xi where A = nabla u is the full velocity gradient tensor. Since A = S + Omega (with Omega the antisymmetric part), we have (xi . nabla)u = S xi + Omega xi.

Also, Omega xi = (1/2)(omega x xi) = (1/2)(|omega| xi x xi) = 0 (since omega = |omega| xi).

Wait -- this is only true when acting on xi itself. Let me be more careful. The vorticity-velocity relation gives Omega_{ij} = -(1/2) epsilon_{ijk} omega_k. So (Omega xi)_i = Omega_{ij} xi_j = -(1/2) epsilon_{ijk} omega_k xi_j = -(1/2)(omega x xi)_i. Since omega = |omega| xi, omega x xi = |omega| (xi x xi) = 0.

Therefore:

    (xi . nabla)u = S xi                                                             (4)

And the commutator becomes:

    [D_t, D_xi] f = (D_t xi - S xi) . nabla f                                       (5)

From equation (1): D_t xi = P_perp(S xi) + (nu/|omega|) P_perp(Delta omega). Now P_perp(S xi) = S xi - (xi . S xi) xi = S xi - Q xi, where Q = xi . S xi is the Rayleigh quotient. So:

    D_t xi - S xi = -Q xi + (nu/|omega|) P_perp(Delta omega)                         (6)

The commutator becomes:

    [D_t, D_xi] f = (-Q xi + (nu/|omega|) P_perp(Delta omega)) . nabla f             (7)

When f is a vector field and we interpret this as acting component-by-component:

    [D_t, D_xi] v = -Q (xi . nabla)v + (nu/|omega|)(P_perp(Delta omega) . nabla)v    (8)

### 1.3 Applying D_xi to the xi evolution equation

We apply D_xi to both sides of (1):

    D_xi(D_t xi) = D_xi(P_perp(S xi)) + D_xi((nu/|omega|) P_perp(Delta omega))       (9)

Using the commutator (8):

    D_t(D_xi xi) = [D_t, D_xi] xi + D_xi(P_perp(S xi)) + D_xi((nu/|omega|) P_perp(Delta omega))

    D_t eta = -Q (xi . nabla)xi + (nu/|omega|)(P_perp(Delta omega) . nabla)xi
              + D_xi(P_perp(S xi)) + D_xi((nu/|omega|) P_perp(Delta omega))

    D_t eta = -Q eta + (nu/|omega|)(P_perp(Delta omega) . nabla)xi
              + D_xi(P_perp(S xi)) + D_xi((nu/|omega|) P_perp(Delta omega))          (10)

### 1.4 Expanding the inviscid term D_xi(P_perp(S xi))

Let us compute D_xi(P_perp(S xi)). Recall P_perp = I - xi (x) xi. So:

    P_perp(S xi) = S xi - (xi . S xi) xi = S xi - Q xi

Taking D_xi:

    D_xi(P_perp(S xi)) = D_xi(S xi) - (D_xi Q) xi - Q (D_xi xi)
                        = D_xi(S xi) - (D_xi Q) xi - Q eta                            (11)

Now D_xi(S xi) = (D_xi S) xi + S (D_xi xi) = (D_xi S) xi + S eta.

Here D_xi S = (xi . nabla)S is the directional derivative of the strain tensor along the vorticity direction. This involves nabla S = nabla^2 u -- the second derivative of velocity.

So:

    D_xi(P_perp(S xi)) = (D_xi S) xi + S eta - (D_xi Q) xi - Q eta                   (12)

The term (D_xi Q) xi is parallel to xi. The perpendicular (dynamically relevant) part of D_xi(P_perp(S xi)) is:

    P_perp[D_xi(P_perp(S xi))] = P_perp[(D_xi S) xi] + P_perp(S eta) - Q eta         (13)

since P_perp[(D_xi Q) xi] = 0 (it is parallel to xi), and P_perp(Q eta) = Q eta (since eta is already perpendicular to xi).

Let us also compute D_xi Q:

    D_xi Q = D_xi(xi . S xi) = (D_xi xi) . S xi + xi . (D_xi S) xi + xi . S (D_xi xi)
           = eta . S xi + xi . (D_xi S) xi + xi . S eta
           = 2 (S xi) . eta + xi . (D_xi S) xi                                        (14)

(using symmetry of S: xi . S eta = S xi . eta = eta . S xi.)

### 1.5 Expanding the viscous term

The viscous contribution to D_t xi is V = (nu/|omega|) P_perp(Delta omega). We need to compute D_xi V.

    D_xi V = D_xi(nu/|omega|) P_perp(Delta omega) + (nu/|omega|) D_xi(P_perp(Delta omega))

    D_xi(nu/|omega|) = -nu (D_xi |omega|) / |omega|^2                                 (15)

From the vorticity equation and the definition |omega|^2 = omega . omega:

    D_xi |omega| = (xi . nabla)|omega| = (1/|omega|)(omega . (xi . nabla)omega)

Using omega = |omega| xi:

    (xi . nabla)omega = (D_xi |omega|) xi + |omega| (D_xi xi) = (D_xi |omega|) xi + |omega| eta

So: omega . (xi . nabla)omega = |omega|(D_xi |omega|) + |omega|^2 (xi . eta) = |omega|(D_xi |omega|)

since xi . eta = 0. This gives D_xi |omega| = D_xi |omega| (tautology). Let me use a different route.

More directly: |omega| = (omega_k omega_k)^{1/2}, so:

    D_xi |omega| = (omega_k / |omega|) (xi . nabla) omega_k = xi_k (omega_j / |omega|) partial_k omega_j

Since xi = omega/|omega|:

    D_xi |omega| = (xi_k xi_j) partial_k omega_j = xi . ((xi . nabla) omega)
                 = xi . D_xi omega                                                      (16)

Now D_xi omega = (xi . nabla)(|omega| xi) = (D_xi |omega|) xi + |omega| eta. Taking the dot product with xi:

    xi . D_xi omega = D_xi |omega| + |omega| (xi . eta) = D_xi |omega|

This is circular. The issue is that D_xi |omega| is simply the gradient of |omega| in the xi-direction:

    D_xi |omega| = xi . nabla |omega| = nabla_xi |omega|                               (17)

This is a scalar quantity that we will denote as sigma := xi . nabla |omega| = nabla_xi |omega|, the rate of change of vorticity magnitude along the vortex line.

So: D_xi(nu/|omega|) = -nu sigma / |omega|^2.

The full viscous contribution to D_t eta involves:

    D_xi V = -(nu sigma / |omega|^2) P_perp(Delta omega) + (nu/|omega|) D_xi(P_perp(Delta omega))  (18)

The term D_xi(P_perp(Delta omega)) involves D_xi(Delta omega) and derivatives of the projection P_perp (through D_xi xi = eta):

    D_xi(P_perp w) = P_perp(D_xi w) - (eta (x) xi + xi (x) eta) w                     (19)

for any vector w (from differentiating P_perp = I - xi (x) xi along xi).

The viscous term is extremely complex in full generality. The key structural feature is that it contains:
- A term proportional to nu Delta eta (from commuting D_xi with the Laplacian in Delta omega) -- this is the viscous diffusion of the curvature vector
- Terms involving nabla^2 omega, nabla |omega|, nabla xi -- these are lower-order relative to the Laplacian but can contain singular coefficients (factors of 1/|omega|)
- A factor of nu/|omega| multiplying the dominant viscous contribution

### 1.6 The full eta evolution equation (schematic form)

Collecting all terms from (10), (12), (13), (18):

    **D_t eta = -2Q eta + P_perp(S eta) + P_perp((D_xi S) xi)**
    **         + (nu/|omega|)(P_perp(Delta omega) . nabla) xi**
    **         - (nu sigma/|omega|^2) P_perp(Delta omega)**
    **         + (nu/|omega|) D_xi(P_perp(Delta omega))**                               (20)

Let us identify and name each term:

**Term I: -2Q eta.** Linear damping/amplification of eta. Q = xi . S xi is the Rayleigh quotient (the stretching rate of vorticity). When Q > 0 (vortex stretching), this term DAMPS eta. When Q < 0 (vortex compression), it amplifies eta. Note the factor of 2: this comes from the -Q eta in (10) plus the -Q eta in (12).

Wait, let me recount. From equation (10): the first term is -Q eta. From equation (12): we get S eta - Q eta. But we need to be more careful about what survives the P_perp projection in the full equation. Let me redo this more carefully.

The full equation from (10) is:

    D_t eta = -Q eta + (nu/|omega|)(P_perp(Delta omega) . nabla)xi
              + [(D_xi S) xi + S eta - (D_xi Q) xi - Q eta]
              + D_xi((nu/|omega|) P_perp(Delta omega))

The xi-parallel components of D_t eta must vanish (since eta remains perpendicular to xi along the flow). So we can project everything onto the perpendicular plane. But let us first collect the terms without projecting:

    D_t eta = -Q eta + S eta - Q eta + (D_xi S) xi - (D_xi Q) xi
              + (viscous terms)
            = S eta - 2Q eta + (D_xi S) xi - (D_xi Q) xi + (viscous terms)             (21)

Now, the term (D_xi S) xi - (D_xi Q) xi needs examination. We have:

    (D_xi S) xi - (D_xi Q) xi = [(D_xi S) - (D_xi Q) I] xi

But D_xi Q is a scalar, so (D_xi Q) xi is a vector parallel to xi only if we read it as the scalar (D_xi Q) times the vector xi. And (D_xi S) xi is a vector that can have both parallel and perpendicular components.

The perpendicular part of (D_xi S) xi is:

    P_perp((D_xi S) xi)

This involves nabla S = nabla^2 u evaluated along the xi-direction. This is the **supercritical source term** -- it involves two derivatives of velocity.

The perpendicular projection of S eta: P_perp(S eta) = S eta - (xi . S eta) xi. Now xi . S eta = (S xi) . eta (by symmetry of S). Denoting S xi = Q xi + w_perp where w_perp = P_perp(S xi) is the perpendicular part of S xi (which drives the rotation of xi), we get:

    xi . S eta = Q (xi . eta) + w_perp . eta = w_perp . eta

since xi . eta = 0. So: P_perp(S eta) = S eta - (w_perp . eta) xi.

Collecting the perpendicular part of (21):

    **D_t eta = P_perp(S eta) - 2Q eta + P_perp((D_xi S) xi) + V_nu**                  (22)

where V_nu collects all viscous contributions.

More explicitly, projecting:

    **(D_t eta)_perp = [P_perp S P_perp - 2Q] eta + P_perp((D_xi S) xi) + V_nu**

But we need to account for the constraint that eta is perpendicular to xi throughout the evolution. The correct projected equation in the normal plane is:

    **D_t eta = [S_perp - 2Q I_perp] eta + P_perp((D_xi S) xi) + V_nu**                (23)

where S_perp = P_perp S P_perp is the restriction of S to the plane perpendicular to xi, I_perp is the identity in that plane, and the equation is understood in the 2D plane normal to xi at each point.

**Remark on the factor -2Q.** This factor is significant. In the strain eigenbasis with xi ~ e_2 (the aligned case), Q ~ s_2. Then the linear operator acting on eta has eigenvalues (s_j - 2s_2) for j = 1, 3 (the two directions perpendicular to xi ~ e_2 in the eigenbasis). These are:
- j = 1: s_1 - 2s_2
- j = 3: s_3 - 2s_2

With s_1 > s_2 > s_3 and s_1 + s_2 + s_3 = 0 (incompressibility):
- s_1 - 2s_2 = s_1 - 2s_2 (can be positive or negative depending on the ratio s_2/s_1)
- s_3 - 2s_2 = -(s_1 + s_2) - 2s_2 = -(s_1 + 3s_2) (always negative when s_1, s_2 > 0)

So one eigenvalue of the linear operator can be positive (destabilizing), while the other is negative (stabilizing). The sign depends on the ratio s_2/s_1.

### 1.7 Scaling identification of each term in (23)

Let Omega denote a typical vorticity magnitude and L a typical length scale. Then:
- |nabla u| ~ Omega (by Biot-Savart, loosely)
- S ~ Omega
- Q ~ Omega (or more precisely, Q ~ s_2 ~ fraction of Omega)
- D_xi S ~ |nabla^2 u| ~ Omega / L -- **the supercritical term**
- eta ~ kappa (by definition)
- V_nu ~ nu * (terms involving Delta eta, nabla^2 omega / |omega|, etc.)

The terms in (23) scale as:
- [S_perp - 2Q I_perp] eta ~ Omega * kappa
- P_perp((D_xi S) xi) ~ Omega / L -- independent of kappa, drives growth
- V_nu ~ nu * kappa / L^2 (viscous damping, leading order)

**The critical balance:** growth of kappa is driven by P_perp((D_xi S) xi) ~ Omega/L (a forcing term independent of kappa itself) and by [S_perp - 2Q] eta ~ Omega * kappa (a linear amplification/damping depending on the sign of the eigenvalues). Viscous damping acts at rate nu/L^2 per unit kappa.

---

## Part 2: Evolution Equation for kappa^2 = |eta|^2

### 2.1 Derivation

Taking the inner product of equation (22) with 2 eta:

    D_t(kappa^2) = D_t(eta . eta) = 2 eta . D_t eta

    D_t(kappa^2) = 2 eta . [P_perp(S eta) - 2Q eta + P_perp((D_xi S) xi)] + 2 eta . V_nu

Let us examine each contribution.

**Term A: 2 eta . P_perp(S eta).**

    2 eta . P_perp(S eta) = 2 eta . S eta - 2 (xi . S eta)(eta . xi)
                           = 2 eta . S eta    (since xi . eta = 0)

In the strain eigenbasis {e_1, e_2, e_3} with eigenvalues s_1 > s_2 > s_3, write eta = eta_1 e_1 + eta_3 e_3 (perpendicular to xi ~ e_2). Then:

    2 eta . S eta = 2(s_1 eta_1^2 + s_3 eta_3^2)

Since kappa^2 = eta_1^2 + eta_3^2, this equals:

    2(s_1 eta_1^2 + s_3 eta_3^2) = 2 s_1 eta_1^2 + 2 s_3 eta_3^2

The range of this expression for fixed kappa^2 is [2 s_3 kappa^2, 2 s_1 kappa^2].

**Term B: -4Q kappa^2.**

    2 eta . (-2Q eta) = -4Q kappa^2 = -4 s_2 kappa^2    (when xi ~ e_2)

**Terms A + B combined:**

    2(s_1 eta_1^2 + s_3 eta_3^2) - 4 s_2 kappa^2
    = 2(s_1 - 2s_2) eta_1^2 + 2(s_3 - 2s_2) eta_3^2
    = 2(s_1 - 2s_2) eta_1^2 + 2(-s_1 - 3s_2) eta_3^2                                 (24)

Using incompressibility s_3 = -(s_1 + s_2).

**Sign analysis of (24) in the physically relevant regime (s_2 > 0, s_1 > s_2):**

- Coefficient of eta_1^2: (s_1 - 2s_2). Positive when s_1 > 2s_2, i.e., s_2/s_1 < 1/2.
  DNS shows s_2/s_1 ~ 0.2-0.4 typically, so this coefficient is **typically positive**.

- Coefficient of eta_3^2: -(s_1 + 3s_2). Always negative when s_1, s_2 > 0.
  This coefficient is **always negative** in the physical regime.

So the curvature vector has one amplified component (along e_1) and one damped component (along e_3). The net effect depends on the orientation of eta relative to the strain eigenbasis.

**Term C: 2 eta . P_perp((D_xi S) xi).**

    2 eta . P_perp((D_xi S) xi) = 2 eta . (D_xi S) xi    (since xi . eta = 0)

This is the **source term**. It involves nabla^2 u and drives kappa^2 growth independently of the current value of kappa.

By Cauchy-Schwarz: |2 eta . (D_xi S) xi| <= 2 kappa |D_xi S|.

**Term D: Viscous contributions (2 eta . V_nu).**

The viscous terms have the schematic form:

    2 eta . V_nu = nu Delta(kappa^2) - 2 nu |nabla eta|^2 + (lower-order corrections)
                 + (terms from the 1/|omega| coefficient)

The leading viscous terms are:
- nu Delta(kappa^2): diffusion of kappa^2 (neutral -- redistributes but does not change the maximum)
- -2 nu |nabla eta|^2: viscous dissipation of curvature gradients (always stabilizing)
- Corrections from the factor nu/|omega| in the original xi equation, which introduce factors of nabla|omega|/|omega| and are small when |omega| is large

### 2.2 The kappa^2 evolution equation

Collecting all terms:

    **D_t(kappa^2) = 2(s_1 - 2s_2) eta_1^2 + 2(s_3 - 2s_2) eta_3^2**
    **             + 2 eta . (D_xi S) xi**
    **             + nu Delta(kappa^2) - 2 nu |nabla eta|^2**
    **             + (viscous corrections with coefficient nu/|omega|)**                (25)

Or more compactly:

    **D_t(kappa^2) = L[kappa^2] + Source + Viscous_Diffusion + Viscous_Damping + Lower_Order**

where:
- L[kappa^2] = 2(s_1 - 2s_2) eta_1^2 + 2(s_3 - 2s_2) eta_3^2 -- linear in kappa^2, sign-indefinite
- Source = 2 eta . (D_xi S) xi -- involves nabla^2 u, drives kappa^2 growth
- Viscous_Diffusion = nu Delta(kappa^2) -- redistributive
- Viscous_Damping = -2 nu |nabla eta|^2 -- always negative, stabilizing
- Lower_Order = terms with factors nu/|omega|, nu nabla|omega|/|omega|^2, etc.

### 2.3 Analysis: what drives kappa^2 growth?

**Driver 1: The linear term with coefficient (s_1 - 2s_2).**

When eta has a significant component along e_1 (the most extensional direction) and s_2/s_1 < 1/2 (which DNS data supports), this term amplifies kappa^2. The growth rate is proportional to (s_1 - 2s_2) ~ s_1 (1 - 2s_2/s_1) ~ s_1.

In terms of scaling: this drives exponential growth of kappa^2 at rate ~ s_1 ~ |nabla u| ~ Omega. So kappa^2 can grow exponentially with rate proportional to the vorticity magnitude. This is fast but not by itself a finite-time blowup (exponential growth for finite time gives a bounded result).

However, if |omega| itself is growing (as in vortex stretching), then s_1 is growing, and the exponential rate accelerates. If |omega| ~ (T-t)^{-1} (Type I blowup), then s_1 ~ (T-t)^{-1}, and:

    d_t(kappa^2) ~ (T-t)^{-1} kappa^2

which gives kappa^2 ~ (T-t)^{-C} for some C > 0 -- power-law blowup of kappa^2 at the same time as |omega| blows up.

**Driver 2: The source term 2 eta . (D_xi S) xi.**

This involves D_xi S = (xi . nabla)S, the directional derivative of the strain tensor along the vorticity direction. By the elliptic regularity of Biot-Savart, |nabla S| = |nabla^2 u| is bounded by (roughly) the Laplacian of omega. In high-vorticity regions:

    |D_xi S| <= |nabla S| ~ |nabla^2 u| ~ |nabla omega| / L or |omega| / L^2

The source term is bounded by 2 kappa |D_xi S|, so its contribution to D_t(kappa^2) is at most 2 kappa |D_xi S|. For small kappa, this dominates (it creates curvature from zero). For large kappa, the linear term dominates.

**Driver 3 (stabilizing): The viscous damping -2 nu |nabla eta|^2.**

This requires spatial gradients of eta. If kappa has spatial oscillations on scale ell, then |nabla eta|^2 ~ kappa^2/ell^2, and the damping rate is nu/ell^2. This competes with the linear growth rate s_1 when ell ~ sqrt(nu/s_1), which is precisely the Kolmogorov scale (or the vortex core radius r_c for a Burgers vortex). So viscous damping can control kappa^2 growth only at scales comparable to or below the core radius.

### 2.4 Key observation: the leading-order balance at large |omega| and large kappa

At a point of large |omega| and large kappa (the dangerous regime for blowup):

    D_t(kappa^2) ~ (s_1 - 2s_2) kappa^2 + O(kappa |nabla S|) + nu Delta(kappa^2)
                 - 2 nu |nabla eta|^2 + O(nu kappa^2 / |omega|)

The term (s_1 - 2s_2) kappa^2 is the leading interaction: it is linear in kappa^2 and proportional to s_1 ~ |S| ~ |nabla u|.

The viscous correction terms proportional to nu/|omega| become negligible at large |omega|. The bare viscous terms (nu Delta(kappa^2) and -2nu |nabla eta|^2) remain, but they act on the spatial structure of kappa, not on its pointwise value.

**The evolution of kappa^2 at its spatial maximum (where Delta(kappa^2) <= 0) is therefore:**

    D_t(kappa^2)|_{max} <= (s_1 - 2s_2) kappa_{max}^2 + 2 kappa_{max} |D_xi S| + O(nu/|omega| * kappa_{max}^2)

This is a Riccati-type inequality (linear in kappa_{max}^2 with a forcing term). The linear coefficient (s_1 - 2s_2) determines the growth rate.

---

## Part 3: Restricted Euler Analysis (nu = 0, H = 0)

### 3.1 The restricted Euler model

Setting nu = 0 and replacing the pressure Hessian nabla^2 p by its isotropic part (-(1/3)tr(A^2) I, the restricted Euler approximation), the velocity gradient tensor A = nabla u evolves as:

    dA/dt = -A^2 + (1/3) tr(A^2) I

(We use d/dt since in restricted Euler, spatial dependence is suppressed -- the model follows a single fluid particle.)

The strain evolution in restricted Euler is:

    dS/dt = -S^2 - Omega^2 + (1/3)(|S|^2 + |Omega|^2/2) I

where |S|^2 = tr(S^2) = s_1^2 + s_2^2 + s_3^2 and |Omega|^2 = |omega|^2/2.

The eigenvalue evolution (Vieillefosse 1982, 1984; Cantwell 1992):

    ds_i/dt = -s_i^2 - (1/4)|omega|^2 (xi . e_i)^2 + (1/4)|omega|^2/3 + (1/3)(s_1^2 + s_2^2 + s_3^2)

Under perfect e_2-alignment (xi = e_2, so (xi . e_1) = (xi . e_3) = 0, (xi . e_2) = 1):

    ds_1/dt = -s_1^2 + (1/12)|omega|^2 + (1/3)(s_1^2 + s_2^2 + s_3^2)
    ds_2/dt = -s_2^2 - (1/4)|omega|^2 + (1/12)|omega|^2 + (1/3)(s_1^2 + s_2^2 + s_3^2)
            = -s_2^2 - (1/6)|omega|^2 + (1/3)|S|^2
    ds_3/dt = -s_3^2 + (1/12)|omega|^2 + (1/3)|S|^2

And the vorticity magnitude evolution:

    d|omega|/dt = s_2 |omega|    (under e_2-alignment)

### 3.2 Can kappa diverge in restricted Euler?

In the restricted Euler model (with uniform gradient approximation), the velocity gradient is spatially uniform. Therefore nabla S = 0, and the source term P_perp((D_xi S) xi) = 0. The eta evolution reduces to:

    d eta/dt = [S_perp - 2Q I_perp] eta                                               (26)

(no source, no viscosity -- the eta equation is purely linear in eta).

This means: **in restricted Euler, if eta(0) = 0, then eta(t) = 0 for all t.** Curvature is not generated from zero. But if eta(0) is nonzero, it can be amplified or damped.

For nonzero eta(0), the restricted Euler dynamics of kappa^2:

    d(kappa^2)/dt = 2(s_1 - 2s_2) eta_1^2 + 2(s_3 - 2s_2) eta_3^2                    (27)

**Does kappa blow up when |omega| does?**

Along the Vieillefosse blow-up trajectory, the eigenvalue ratios approach s_2/s_1 -> 1 and s_3/s_1 -> -2. The coefficient of eta_1^2 in (27) is:

    s_1 - 2s_2 -> s_1 - 2s_1 = -s_1 < 0    (as s_2/s_1 -> 1)

The coefficient of eta_3^2 is:

    s_3 - 2s_2 -> -2s_1 - 2s_1 = -4s_1 < 0   (as s_3/s_1 -> -2, s_2/s_1 -> 1)

So in the Vieillefosse blowup (s_2/s_1 -> 1), **both eigenvalues of the linear operator are negative**, and kappa^2 is DAMPED. Curvature decreases along the restricted Euler blowup trajectory.

This is a significant finding. Let us verify the computation more carefully.

The Vieillefosse blowup has the eigenvalue ratios approaching:

    s_1 : s_2 : s_3 = 1 : 1 : -2    (the Vieillefosse attractor)

At this ratio, the linear operator in (27) has eigenvalues:
- s_1 - 2s_2 = s_1 - 2s_1 = -s_1
- s_3 - 2s_2 = -2s_1 - 2s_1 = -4s_1

Both are proportional to -s_1, which is negative (s_1 > 0). As the blowup proceeds, s_1 ~ (T-t)^{-1}, so the damping rate accelerates:

    d(kappa^2)/dt <= -s_1 kappa^2 ~ -(T-t)^{-1} kappa^2

This gives: kappa^2(t) ~ kappa^2(0) (T-t)^{C} for some C > 0 (a constant depending on the initial eta orientation). So:

    **kappa -> 0 as t -> T in the Vieillefosse restricted Euler blowup.**

The curvature of vortex lines DECREASES as the restricted Euler blowup proceeds. This is because the blowup attracts toward a uniform strain configuration (the 1:1:-2 ratio), which straightens vortex lines.

### 3.3 Blowup rate of |omega| vs. kappa

In restricted Euler:
- |omega| ~ (T-t)^{-1} (blows up)
- kappa ~ (T-t)^{C/2} for C > 0 (goes to zero)

The curvature is ANTI-CORRELATED with vorticity magnitude in the restricted Euler model. Stronger vorticity means straighter vortex lines.

### 3.4 What about different eigenvalue ratios?

The restricted Euler blowup always attracts to the Vieillefosse ratio 1:1:-2. But earlier in the evolution, when s_2/s_1 is smaller, the coefficient (s_1 - 2s_2) can be positive. For s_2/s_1 < 1/2:

    s_1 - 2s_2 > 0 (amplifying the e_1-component of eta)
    s_3 - 2s_2 < 0 (damping the e_3-component)

So for intermediate eigenvalue ratios (the regime observed in DNS, s_2/s_1 ~ 0.2-0.4), kappa^2 can grow in the e_1-direction while being damped in the e_3-direction. The net effect depends on the angle of eta in the normal plane.

However, even in this regime, the dynamics of the restricted Euler system drive s_2/s_1 toward 1, where both components are damped. So any transient growth of kappa is eventually reversed.

**Conclusion for restricted Euler:** kappa blowup is NOT possible in the restricted Euler model. In fact, kappa is damped to zero at the blowup time. The restricted Euler analysis gives a **favorable** answer for the DHY route.

### 3.5 Important caveat: the source term vanishes in restricted Euler

In restricted Euler, nabla S = 0 (the gradient is spatially uniform), so the source term P_perp((D_xi S) xi) = 0. In the real NS flow, this source term is generically nonzero and involves nabla^2 u. The restricted Euler favorable answer eliminates one mechanism for kappa blowup (linear amplification by strain) but does not address the source-term mechanism (creation of curvature by strain gradients).

---

## Part 4: Effect of Viscosity on Kappa Evolution

### 4.1 The viscous contribution to D_t(kappa^2)

Restoring nu > 0 (but still setting H = 0 -- no pressure Hessian corrections beyond isotropic):

The viscous terms in the xi equation are:

    V_xi = (nu/|omega|) P_perp(Delta omega)

The leading-order viscous contribution to D_t(kappa^2) from the xi equation has two distinct pieces:

**Piece 1: Direct viscous diffusion of eta.**

When we expand the viscous terms carefully, the leading contribution is:

    V_kappa = nu Delta(kappa^2) - 2 nu |nabla eta|^2 + (terms with coefficient nu/|omega|)

The first two terms are the standard viscous dissipation structure for a squared quantity. The term nu Delta(kappa^2) redistributes kappa^2 in space (neutral at a maximum since Delta(kappa^2) <= 0 there). The term -2 nu |nabla eta|^2 damps spatial gradients of the curvature vector (always stabilizing).

**Piece 2: The effective viscosity correction.**

The xi equation has the structure:

    D_t xi = P_perp(S xi) + nu [Delta xi - |nabla xi|^2 xi + (2/|omega|) P_perp((nabla |omega| . nabla) xi)]

(from equation (Dir') in direction-3-vorticity-direction.md). The first viscous term nu Delta xi is a standard diffusion; the second -nu |nabla xi|^2 xi is the harmonic map curvature correction (maintaining |xi| = 1); the third involves nabla|omega|/|omega|, which can be large but is multiplied by nu.

When we derive the eta = D_xi xi equation, the viscous terms propagate as:

    V_eta ~ nu Delta eta - nu |nabla xi|^2 eta + (2 nu/|omega|) D_xi P_perp((nabla |omega| . nabla) xi) + ...

The key observation: the leading viscous term nu Delta eta provides diffusion at rate nu/ell^2, where ell is the spatial scale of variation of eta. This is the SAME diffusion rate as for vorticity itself.

### 4.2 Viscous damping vs. inviscid source at the point of maximum |omega|

At the point of maximum |omega|, several simplifications occur:
- nabla |omega| = 0 (it is a maximum)
- Delta |omega| <= 0

The viscous contribution to D_t |omega| at the maximum point is:

    nu xi . Delta omega = nu (Delta |omega| + |omega| |nabla xi|^2) = nu Delta |omega| + nu |omega| |nabla xi|^2

Wait -- let me derive this more carefully. We have omega = |omega| xi, so:

    Delta omega = (Delta |omega|) xi + 2 (nabla |omega| . nabla) xi + |omega| Delta xi

At the maximum of |omega|, nabla |omega| = 0, so:

    xi . Delta omega = Delta |omega| + |omega| (xi . Delta xi)

Now xi . Delta xi = -|nabla xi|^2 (from differentiating |xi|^2 = 1 twice). So:

    xi . Delta omega |_{max |omega|} = Delta |omega| - |omega| |nabla xi|^2

Since Delta |omega| <= 0 at the maximum, the viscous contribution to D_t |omega| is:

    nu (Delta |omega| - |omega| |nabla xi|^2) <= -nu |omega| |nabla xi|^2 < 0

Viscosity damps the maximum of |omega|. The damping rate is nu |nabla xi|^2. Since |nabla xi| >= kappa (because D_xi xi is one component of nabla xi), we get:

    **Viscous damping of |omega|_{max} >= nu kappa^2 |omega|**

This is a remarkable connection: **the curvature of vortex lines directly controls the viscous damping of vorticity.** Large kappa means more viscous damping, which opposes the vortex stretching D_t |omega| ~ s_2 |omega|.

### 4.3 What about the viscous contribution to D_t(kappa^2)?

At the maximum of kappa^2 (which may not coincide with the maximum of |omega|):

    D_t(kappa^2)|_{max kappa^2} <= [terms A+B from (24)] + Source + O(nu/|omega| * kappa^2)

The bare viscous terms give: nu Delta(kappa^2) <= 0 (at the maximum) and -2 nu |nabla eta|^2 <= 0. Both are favorable.

The unfavorable viscous corrections come from the nu/|omega| terms in the xi equation, which produce:

    O(nu kappa^2 |nabla xi|^2 / |omega|) + O(nu kappa |nabla^2 omega| / |omega|^2)

These are suppressed by the factor nu/|omega| and are negligible at large |omega|.

### 4.4 The regime analysis

**Regime 1: |omega| moderate, kappa large.**

Viscous damping of kappa^2: -2 nu |nabla eta|^2 ~ -2 nu kappa^2/ell^2 where ell is the scale of spatial variation. The inviscid growth rate is ~ s_1 kappa^2 (from Term A+B). The balance requires ell ~ sqrt(nu/s_1) = r_c (the core radius). If kappa varies on scale r_c (which is the natural scale), viscosity can control kappa growth. In this regime, **viscosity wins** and kappa remains bounded.

**Regime 2: |omega| large, kappa moderate.**

The inviscid source term P_perp((D_xi S) xi) injects curvature at rate ~ |nabla S|. For the source to be controlled, we need the viscous damping (at rate nu/ell^2) to exceed the injection rate. This requires |nabla S| ell^2 / nu to be bounded -- essentially a regularity condition on nabla^2 u.

**Regime 3: Both |omega| and kappa large.**

The restricted Euler analysis (Part 3) shows that the linear interaction term DAMPS kappa in the Vieillefosse regime (s_2/s_1 -> 1). With viscosity added, there is additional damping. The danger comes only from the source term D_xi S, which requires nabla^2 u control.

### 4.5 Key finding: viscosity does not provide a standalone mechanism

The viscous damping of kappa^2 is:
- Proportional to nu (vanishes in the inviscid limit)
- Effective on scales ~ r_c = sqrt(nu/|S|) (the dissipative scale)
- Insufficient to control the source term P_perp((D_xi S) xi) without additional bounds on nabla^2 u

**Viscosity helps but cannot close the argument by itself.** The missing ingredient is control of nabla^2 u (the strain gradient), which is at the supercritical level.

---

## Part 5: Effect of the Pressure Hessian

### 5.1 The pressure Hessian's role in the strain evolution

The full NS strain evolution (equation (SE) from subproblem-E):

    D_t S = -S^2 + (1/4)(omega (x) omega) - (|omega|^2/4) I - nabla^2 p + nu Delta S

The pressure Hessian H = nabla^2 p satisfies the trace condition tr(H) = Delta p = -(tr(S^2) - |omega|^2/4) (from the NS pressure equation). The traceless part of H, denoted H^0 = H - (1/3)(Delta p) I, is the anisotropic pressure Hessian. This is determined nonlocally by the Biot-Savart structure:

    H_{ij}^0 = -PV integral K_{ijkl}(x-y) [S_{kl}(y) S_{mn}(y) delta_{mn,kl} + vorticity terms] dy

where K is the Calderon-Zygmund kernel associated with the biharmonic operator.

### 5.2 The pressure Hessian's contribution to D_t(kappa^2)

The pressure Hessian modifies the strain evolution, and hence the strain gradient D_xi S, which enters the source term of the kappa^2 equation. The effect propagates through:

    Source = 2 eta . P_perp((D_xi S) xi)

where D_xi S now includes the pressure Hessian contribution.

Additionally, the pressure Hessian modifies the eigenvalues s_i, changing the coefficients in the linear terms (s_1 - 2s_2) and (s_3 - 2s_2). From subproblem-E: the anisotropic pressure Hessian acts to isotropize the strain, pushing s_2/s_1 toward an intermediate value (DNS shows s_2/s_1 ~ 0.2-0.4 rather than the restricted Euler attractor of s_2/s_1 -> 1).

**Effect on the linear terms:** with s_2/s_1 ~ 0.3 (DNS value) instead of s_2/s_1 -> 1 (restricted Euler):

    s_1 - 2s_2 ~ s_1(1 - 0.6) = 0.4 s_1 > 0    (AMPLIFYING, not damping!)
    s_3 - 2s_2 ~ s_1(-1.3 - 0.6) = -1.9 s_1 < 0  (damping)

So the pressure Hessian, by keeping s_2/s_1 away from 1, actually MAINTAINS the amplifying coefficient for the e_1-component of eta. This is the opposite of the restricted Euler behavior, where s_2/s_1 -> 1 makes both coefficients negative.

**This is a critical observation:** the pressure Hessian prevents the natural Vieillefosse damping mechanism for kappa. By keeping the eigenvalue ratios in the intermediate range (s_2/s_1 ~ 0.3), the pressure Hessian ensures that the e_1-component of eta can be amplified by the strain.

### 5.3 Does the pressure Hessian help or hurt kappa control?

**It hurts, on balance.** The restricted Euler model (without pressure Hessian) has kappa -> 0 at blowup (Part 3). The pressure Hessian, by modifying the eigenvalue ratios, prevents this damping and allows one component of kappa to grow. Specifically:

- Without pressure Hessian (restricted Euler): s_2/s_1 -> 1, both kappa components damped.
- With pressure Hessian (DNS regime): s_2/s_1 ~ 0.3, one kappa component amplified (eta_1), one damped (eta_3).

The net effect depends on the competition between amplification along e_1 and damping along e_3, plus the source term. In the worst case, if eta aligns with e_1, kappa grows at rate (s_1 - 2s_2) ~ 0.4 s_1.

### 5.4 Nonlocal structure near high-vorticity regions

The pressure satisfies Delta p = -(|S|^2 - |omega|^2/4). Near a concentrated vortex tube with |omega| >> |S|_{background}:

    Delta p ~ |omega|^2/4 > 0    (inside the tube)
    Delta p ~ -|S|^2 < 0         (outside)

So the pressure has a local maximum inside the vortex tube (low pressure in the core, consistent with the centrifugal balance of the swirling flow). The Hessian nabla^2 p at the tube core has eigenvalues that are O(|omega|^2/r_c^2) in the cross-sectional directions and O(alpha |omega|) in the axial direction.

The strain gradient D_xi S, which enters the source term, is modified by:

    D_xi H = (xi . nabla)(nabla^2 p)

This involves the third derivative of the pressure, or equivalently (by the pressure equation) the first derivatives of |S|^2 and |omega|^2. Along the tube axis, these vary on the geometric scale 1/kappa, giving:

    |D_xi H| ~ |omega|^2 kappa / r_c^2    or    |omega|^2 kappa

(depending on whether the cross-sectional or axial variation dominates). This feeds back into the source term for D_t(kappa^2), creating a nonlinear coupling between kappa and the pressure Hessian.

### 5.5 DNS evidence on vortex-line curvature

Direct numerical simulations provide some data on the geometry of vortex lines:

1. **Siggia (1985), Jimenez et al. (1993):** Vortex tubes in isotropic turbulence have approximately circular cross-sections with radii ~ eta_K (Kolmogorov scale). The tubes are relatively straight over lengths ~ 10-50 eta_K, then curve. The curvature of the tube axes is typically kappa ~ 1/(10 eta_K) to 1/(50 eta_K), bounded by 1/eta_K.

2. **Bermejo-Moreno & Pullin (2008):** Multi-scale analysis of vortical structures. The largest curvatures are found at small scales, near reconnection events.

3. **No DNS study has reported divergent or anomalously large vortex-line curvature in high-vorticity regions.** The curvature appears bounded by O(1/eta_K), where eta_K is the Kolmogorov scale. Since eta_K ~ Re^{-3/4} L (L = integral scale), this bound grows with Reynolds number. But it does not grow faster than the vorticity (which scales as ~ Re^{1/2} / L in Kolmogorov theory), so the ratio kappa/|omega| ~ 1/(eta_K |omega|) ~ 1/(Re^{1/4}) actually DECREASES with Re.

4. **Hamlington, Schumacher, Dahm (2008):** Studied vortex line geometry in DNS. Found that the curvature PDF has exponential tails, not algebraic tails. The maximum curvature at Re_lambda ~ 100-200 is bounded and shows no indication of blowup.

**Summary of DNS evidence:** vortex-line curvature appears bounded in DNS at accessible Reynolds numbers, with the bound growing at most as O(1/eta_K) ~ O(Re^{3/4}/L). There is no evidence of curvature blowup, but DNS cannot access the infinite-Re limit.

---

## Part 6: The Critical Scaling Analysis

### 6.1 Type I blowup scaling

At a hypothetical Type I blowup point with |omega| ~ (T-t)^{-1}:

The self-similar blowup ansatz: u(x,t) = (T-t)^{-1/2} U((x - x_0)/(T-t)^{1/2}). In the self-similar variables y = (x-x_0)/(T-t)^{1/2}, tau = -log(T-t):

    Omega(y) = curl U(y)  (the self-similar vorticity profile)

The vorticity direction xi = Omega/|Omega| in self-similar variables is a FIXED field (independent of tau). Therefore, the curvature:

    kappa = |D_xi xi| in physical coordinates

transforms as:

    kappa(x,t) = (T-t)^{-1/2} kappa_ss(y)

where kappa_ss(y) = |(Xi . nabla_y) Xi| is the curvature in self-similar variables, which is time-independent.

So under Type I self-similar blowup:

    **kappa ~ (T-t)^{-1/2}** (blows up, but slower than |omega| ~ (T-t)^{-1})

The DHY condition requires kappa bounded, so kappa ~ (T-t)^{-1/2} -> infinity VIOLATES the DHY condition. But wait -- the DHY condition requires kappa bounded on {|omega| > M} for some fixed M. If kappa ~ (T-t)^{-1/2} and |omega| ~ (T-t)^{-1}, then at {|omega| = M} the distance is |y| ~ ((T-t) log(M(T-t)))^{1/2} and kappa(x) = (T-t)^{-1/2} kappa_ss(y). For fixed M, as t -> T:

    {|omega| > M} shrinks to a neighborhood of the blowup point of size ~ (T-t)^{1/2}

On this set, kappa ~ (T-t)^{-1/2} -> infinity. So:

    **sup_{{|omega| > M}} kappa -> infinity as t -> T**

**Conclusion: Type I self-similar blowup necessarily violates the DHY condition.** But this is consistent: if the blowup occurs, the DHY condition fails, and the DHY theorem (which says bounded DHY implies regularity) does not give a contradiction.

The real question is: does the DHY condition PREVENT the blowup from occurring in the first place? In other words: is the statement "kappa stays bounded -> regularity" useful, or is it circular?

The DHY theorem states: if sup_{{|omega|>M}} kappa stays bounded for all t in [0,T], then the solution is regular on [0,T]. The contrapositive: if the solution blows up at time T, then kappa -> infinity on {|omega| > M}.

Under Type I blowup, kappa ~ (T-t)^{-1/2} while |omega| ~ (T-t)^{-1}. The ratio kappa/|omega| ~ (T-t)^{1/2} -> 0. So **curvature blows up, but more slowly than vorticity.** In relative terms, the vortex lines are actually STRAIGHTENING (in a scaled sense) as the blowup proceeds. The curvature blowup is a mild, dimensional consequence of the spatial concentration, not a geometric instability.

### 6.2 Under self-similar blowup ansatz

As computed above: kappa_ss(y) = |(Xi . nabla_y) Xi| is a property of the self-similar profile. For any smooth, nontrivial self-similar profile, kappa_ss is bounded and nonzero somewhere.

The physical kappa = (T-t)^{-1/2} kappa_ss -> infinity, but this is entirely due to the spatial rescaling. In self-similar variables, kappa is constant.

**The DHY condition in self-similar variables:** the condition becomes kappa_ss(y) bounded for |Omega(y)| > M (T-t)^{1}, which for t -> T means kappa_ss bounded on an expanding subset of the self-similar profile. If kappa_ss is globally bounded (which it is for a smooth profile), then the DHY condition fails only because the M-threshold in physical variables drops relative to the self-similar vorticity.

### 6.3 The Hou-Luo scenario

In the Hou-Luo computation (2014) of axisymmetric Euler flow with swirl on a cylinder, the potential singularity forms at the boundary. The vorticity omega = omega_theta e_theta develops a sharp front near the stagnation point on the boundary.

In this scenario:
- The vorticity direction xi = e_theta (azimuthal) near the high-vorticity region
- D_xi xi = (e_theta . nabla) e_theta involves the curvature of the theta-lines, which are circles of radius r
- For points near the boundary at r = R: D_xi xi = -e_r/R, giving kappa = 1/R (bounded by the geometry of the cylinder)

However, the Hou-Luo blowup involves a sharp front in |omega| that develops at the wall, with |nabla xi| growing (the direction field develops a discontinuity). The question is whether D_xi xi = (xi . nabla)xi also grows.

For the Hou-Luo scenario: xi ~ e_theta, so D_xi xi = (e_theta/r) partial_theta (e_theta) = -e_r/r. Near the wall (r ~ R), kappa = 1/R is bounded. But the sharp front in the vorticity direction occurs in the z-direction, not the theta-direction, so |nabla xi| can be large while D_xi xi remains bounded by 1/R.

**This is an interesting case where the DHY condition might remain satisfied even as the full Lipschitz condition fails.** The DHY condition (derivative of xi along itself) avoids the sharp front (which is in the z-direction, perpendicular to xi = e_theta).

However, this analysis is for axisymmetric Euler, not full 3D NS. And the Hou-Luo computation remains controversial regarding whether a genuine singularity forms.

---

## Part 7: Structural Mechanisms Preventing Kappa Blowup

### 7.1 Attempt: Maximum principle for kappa^2

The kappa^2 evolution (equation 25):

    D_t(kappa^2) = 2(s_1 - 2s_2) eta_1^2 + 2(s_3 - 2s_2) eta_3^2
                 + 2 eta . (D_xi S) xi
                 + nu Delta(kappa^2) - 2 nu |nabla eta|^2
                 + (lower-order viscous corrections)

At the spatial maximum of kappa^2 (where Delta(kappa^2) <= 0):

    D_t(kappa^2)|_{max} <= 2(s_1 - 2s_2) eta_1^2 + 2(s_3 - 2s_2) eta_3^2
                          + 2 kappa |D_xi S|
                          - 2 nu |nabla eta|^2                                         (28)

For a maximum principle to close, we need the right-hand side to be bounded by C kappa^2 + C' (for Gronwall) or by -c kappa^{2+alpha} + C (for a pointwise bound).

**The obstruction:** the term 2 kappa |D_xi S| involves |D_xi S| = |(xi . nabla)S|, which involves nabla^2 u. There is no a priori bound on |D_xi S| in terms of kappa^2 or |omega|^2 alone. The quantity |nabla^2 u| is supercritical: controlling it requires controlling nabla omega, which is at the level of the full regularity problem.

Specifically: |D_xi S| <= |nabla S| ~ |nabla^2 u|, and the only available estimate is:

    integral |nabla^2 u|^2 dx dt ~ integral |nabla omega|^2 dx dt < infinity    (enstrophy dissipation)

This is an L^2(dt; L^2(dx)) bound, not an L^infinity bound. Without pointwise control of |nabla^2 u|, the source term 2 kappa |D_xi S| cannot be bounded, and the maximum principle cannot close.

**Verdict on maximum principle: FAILS due to the supercritical source term D_xi S.**

### 7.2 Attempt: Monotone quantity

We seek a functional F(kappa, |omega|, ...) such that D_t F <= 0 along NS trajectories.

A natural candidate: F = kappa^2 / |omega|^{2alpha} for some alpha > 0. The evolution:

    D_t F = D_t(kappa^2) / |omega|^{2alpha} - 2alpha kappa^2 D_t(|omega|) / |omega|^{2alpha + 1}

Using D_t |omega| ~ s_2 |omega| (at leading order):

    D_t F ~ [D_t(kappa^2) - 2alpha s_2 kappa^2] / |omega|^{2alpha}

The term -2alpha s_2 kappa^2 provides additional damping of kappa^2 (when s_2 > 0). This is the curvature-vorticity interplay: growth of |omega| (through s_2 > 0) helps damp the RATIO kappa^2/|omega|^{2alpha}.

From Part 6.1: under Type I blowup, kappa ~ (T-t)^{-1/2} and |omega| ~ (T-t)^{-1}, so kappa^2/|omega| ~ (T-t)^{0} = const. This suggests alpha = 1/2 might give a bounded ratio. Indeed:

    kappa^2 / |omega| = kappa^2 / |omega|

and under self-similar blowup this ratio is bounded. The question is whether D_t(kappa^2/|omega|) can be controlled.

    D_t(kappa^2/|omega|) = (1/|omega|)(D_t kappa^2) - (kappa^2/|omega|^2)(D_t |omega|)
                          = (1/|omega|)[D_t kappa^2 - (kappa^2 s_2) + ...]

The term D_t kappa^2 includes the source 2 kappa |D_xi S| ~ 2 kappa |nabla^2 u|. The damping from the |omega| growth gives -kappa^2 s_2/|omega| ~ -kappa^2 Q/|omega|. For this to dominate the source, we need:

    kappa^2 Q / |omega| >= 2 kappa |D_xi S| / |omega|

i.e., kappa Q >= 2 |D_xi S|, i.e., kappa >= 2 |D_xi S| / Q.

This requires kappa to be LARGE for the damping to win -- the opposite of what we want. The monotone quantity approach does not appear to help.

**Verdict on monotone quantity: No useful monotone combination found.** The ratio kappa^2/|omega|^{2alpha} is bounded under self-similar scaling but its evolution still involves the supercritical source D_xi S.

### 7.3 Attempt: Topological/geometric constraint from incompressibility

The vorticity field is divergence-free: div omega = 0. This means vortex lines form closed loops or extend to infinity -- they cannot start or end. This topological constraint prevents certain types of curvature concentration.

Specifically: if a vortex line has curvature kappa at a point, the line must curve through an angle kappa * ds over an arc length ds. To return to a smooth closed loop (or to extend to infinity), the curvature must average out over the line. A crude bound: for a closed vortex line of total length L_line, the average curvature is <= 2 pi / L_line (since the total turning angle for a closed plane curve is 2 pi, and for a space curve it is at least 2 pi).

But this constrains the AVERAGE curvature, not the MAXIMUM. A vortex line can have arbitrarily high curvature at one point if it has low curvature elsewhere. So div omega = 0 does not directly bound the maximum curvature.

**The Biot-Savart constraint:** The velocity u is determined from omega by:

    u(x) = (1/(4 pi)) integral (omega(y) x (x-y)) / |x-y|^3 dy

The strain S = sym(nabla u) is then:

    S(x) = (1/(4 pi)) integral [kernel] omega(y) dy

The strain gradient D_xi S involves integrating omega against a more singular kernel. The Calderon-Zygmund theory gives |D_xi S| <= C M(|nabla omega|), where M is the maximal function. This does not directly constrain kappa through the Biot-Savart structure.

**However:** the Biot-Savart law creates a specific coupling between vorticity and strain that is not captured by the local (restricted Euler) analysis. In particular, the strain at a point is influenced by distant vorticity, and this nonlocal averaging tends to smooth the strain field. Whether this smoothing is sufficient to control D_xi S at high-vorticity points is not known.

**Verdict on topological/geometric constraint: No direct mechanism found.** The divergence-free condition and Biot-Savart structure provide nonlocal averaging but not pointwise bounds on curvature.

### 7.4 Attempt: Curvature-vorticity feedback via Biot-Savart

This is the most promising structural mechanism. The idea: if vortex lines become highly curved (kappa large), the resulting velocity field (via Biot-Savart) tends to straighten the lines.

**The self-induction mechanism.** For a thin vortex tube with curvature kappa, the Biot-Savart self-induced velocity is:

    v_{induced} ~ (Gamma kappa / (4 pi)) log(1/(kappa r_c)) * b

where b is the binormal direction and Gamma is the circulation. This is the classical Local Induction Approximation (LIA) velocity. The induced velocity is in the binormal direction and proportional to kappa.

Under this velocity, the tube axis moves in the binormal direction, which changes the curvature according to:

    D_t kappa = (from the LIA/Hasimoto equations)

The Hasimoto transform maps the filament evolution to the 1D cubic NLS:

    i psi_t + psi_{ss} + (1/2)|psi|^2 psi = 0

where psi = kappa * exp(i integral_0^s tau(s') ds'). The curvature kappa = |psi|.

For 1D cubic NLS: the equation is completely integrable and globally well-posed in H^1. In particular, ||psi||_{L^infinity} <= C(||psi_0||_{H^1}) is bounded for all time. This means:

    **kappa(s,t) = |psi(s,t)| is bounded for all time under LIA dynamics.**

This is a structural regularity result for the curvature under LIA/NLS dynamics!

### 7.5 The Hasimoto transform perspective: strengths and limitations

**What this gives:**

Under the LIA (valid for thin filaments with epsilon = kappa r_c << 1), the curvature kappa satisfies a completely integrable equation (1D cubic NLS) that has global solutions. The curvature is bounded by the initial H^1 norm of the Hasimoto variable psi = kappa e^{i integral tau ds}.

This means: for a single thin vortex tube evolving under its own self-induction, with the core adjusting quasi-statically (the thin-core/LIA regime), the curvature kappa does NOT blow up.

**What this does not give:**

1. **The LIA is only valid for epsilon = kappa r_c << 1.** If kappa grows to the point where kappa r_c ~ O(1), the thin-core approximation breaks down, and the LIA/NLS description fails. The NLS global well-posedness guarantees that kappa stays in the regime kappa r_c << 1 (provided it starts there), but this is for the LIA dynamics -- the question is whether the full NS dynamics agree.

2. **The LIA ignores non-local Biot-Savart interactions.** For multiple vortex tubes, or for a single tube with self-intersection, the LIA breaks down. The interactions are not captured by the cubic NLS.

3. **The LIA ignores viscous diffusion of the core.** In NS, viscosity causes the core radius to evolve: r_c^2 = 4 nu (t - t_0) + r_c(0)^2 (without external strain) or r_c^2 = 4 nu / alpha (with Burgers-type strain balance). The core evolution is coupled to the curvature evolution through the epsilon = kappa r_c condition.

4. **The 1D NLS is for a single filament.** The full NS flow involves a field of vorticity, not a single filament. The Hasimoto transform applies only to the 1D geometry of a single filament center-line.

5. **Higher-order corrections to LIA are not integrable.** The Fukumoto-Moffatt (2000) higher-order correction to LIA adds dispersive and dissipative terms that break integrability. Global well-posedness of the corrected system is not established.

**Despite these limitations, the Hasimoto/NLS result provides the strongest structural evidence that curvature does not blow up for tube-like vortex structures.** It shows that the self-induction dynamics of a thin vortex tube contain a structural mechanism (the complete integrability of cubic NLS) that prevents curvature concentration. This is not a proof for the full NS system, but it is a strong structural signal.

### 7.6 The curvature-vorticity feedback mechanism

Combining the viscous result from Part 4.2 with the self-induction result:

1. Large kappa means large viscous damping of |omega| at the vorticity maximum (Part 4.2: damping rate ~ nu kappa^2).
2. Large kappa drives self-induction motion that redistributes curvature (Part 7.4-7.5: LIA/NLS dynamics keep kappa bounded for thin filaments).
3. The restricted Euler dynamics DAMP kappa as |omega| grows (Part 3: the Vieillefosse attractor straightens vortex lines).

These three mechanisms combine to suggest a self-regulating system: curvature growth is resisted by multiple independent mechanisms, each operating in a different regime:
- At low kappa, high |omega|: restricted Euler damping dominates
- At high kappa, moderate |omega|: self-induction (Biot-Savart) and viscous damping dominate
- At high kappa, high |omega|: all three mechanisms act simultaneously

However, the source term D_xi S can inject curvature from external strain gradients, and none of the three mechanisms directly controls this source. The source is controlled only if nabla^2 u is bounded, which is the supercritical gap.

### 7.7 A fourth mechanism: the alignment mechanism for curvature direction

There is an additional geometric mechanism that has not been discussed in the literature. The curvature vector eta = D_xi xi points in the direction of maximum bending of the vortex line. In the strain eigenbasis, eta has components along e_1 and e_3.

From Part 2.1, the linear operator in the kappa^2 evolution has:
- Amplification along e_1 (when s_2/s_1 < 1/2)
- Damping along e_3 (always)

This means the curvature vector is preferentially damped in the e_3-direction and can only grow in the e_1-direction. Over time, this drives eta toward alignment with e_1. But the vorticity xi is aligned with e_2. So the curvature vector eta tends to align with e_1 -- meaning the vortex line bends toward the most extensional direction.

Now, a vortex line bending toward the most extensional direction will be stretched along that direction, which tends to STRAIGHTEN it (stretching reduces curvature). This is the geometric feedback:

    kappa growth along e_1 -> bending toward e_1 -> stretching along e_1 -> straightening

This feedback is analogous to how a rubber band, when bent and stretched, straightens out. The stretching mechanism naturally opposes the curvature it amplifies.

Quantitatively: if eta ~ kappa e_1 (curvature in the e_1-direction), then the induced curvature change along e_1 is at rate (s_1 - 2s_2) kappa. But the stretching s_1 also acts on the arc length of the vortex line, increasing the distance between points. In the frame moving with the line, this stretching REDUCES the effective curvature by the factor s_1 (the stretching rate dilates arc length, reducing angles per unit arc length).

The precise balance: the curvature of a material curve in a strain field evolves as:

    D_t kappa = kappa [kappa_n . S kappa_n - (T . S T)] + (terms involving nabla S)

where T is the tangent vector and kappa_n = eta/|eta| is the unit normal (curvature direction). The term in brackets is (S_{nn} - S_{TT}), which is the difference between the strain in the normal direction and the tangent direction.

For T ~ e_2 (aligned vortex) and kappa_n ~ e_1 (curvature toward e_1):

    S_{nn} - S_{TT} = s_1 - s_2

The full D_t kappa involves this term minus 2 times the tangential strain Q = s_2:

Actually, the correct evolution for the curvature of a material line in a flow is (from differential geometry of curves in a flow field):

    D_t kappa = -kappa (t . S t) + n . (D_xi S) t + (terms involving nabla u, nabla^2 u)

where t = xi is the unit tangent, n = eta/kappa is the unit normal, and D_xi = t . nabla. This is related to but not identical with the kappa^2 evolution in (25). The term -kappa(t . S t) = -kappa Q represents the curvature reduction due to tangential stretching: stretching along the line dilates arc length, which reduces curvature.

The factor -kappa Q = -kappa s_2 competes with the amplification rate (s_1 - 2s_2) kappa from the linear term. The net rate is:

    (s_1 - 2s_2) - additional factor from the tangential stretching

A careful accounting (see the kappa^2 equation derivation) gives the combined rate as (s_1 - 2s_2) for the e_1-component, which already accounts for the 2Q subtraction. The extra -Q from the tangential stretching is already included in the -2Q term in equation (22).

So the geometric feedback (stretching straightens) IS already captured in the factor -2Q in the eta evolution. The factor -2Q provides twice the damping from the tangential stretching rate. This is the mechanism that makes the restricted Euler attractor damping work (in Part 3).

**Verdict on the curvature-vorticity feedback mechanism:** The feedback exists and is already captured in the -2Q term of the eta evolution. It provides significant damping (especially near the restricted Euler attractor where s_2/s_1 -> 1). But in the DNS regime (s_2/s_1 ~ 0.3), the feedback only partially compensates the amplification, leaving a positive net growth rate for the e_1-component of eta. The feedback alone is insufficient to prevent kappa growth.

---

## Part 8: Honest Verdict

### 8.1 Which outcome is most likely?

**Outcome 2: Ambiguous (nice reformulation, not a proof).**

The analysis produced several concrete results but did not resolve the question definitively. Here is the scorecard:

| Finding | Favors kappa bounded (regularity) | Favors kappa blowup (route dead) |
|---------|:-:|:-:|
| Restricted Euler: kappa DAMPED at Vieillefosse blowup | X | |
| Pressure Hessian: keeps s_2/s_1 ~ 0.3, maintaining e_1 amplification | | X |
| Hasimoto/NLS: kappa bounded under LIA for thin filaments | X | |
| Type I self-similar: kappa ~ (T-t)^{-1/2} (mild blowup) | | Neutral* |
| Viscous feedback: large kappa damps |omega| | X | |
| Source term D_xi S: supercritical, not controlled | | X |
| DNS evidence: kappa appears bounded at accessible Re | X | |
| Hou-Luo: D_xi xi may remain bounded even if |nabla xi| blows up | X | |

*Neutral because the kappa blowup under Type I scaling is a dimensional consequence, not a dynamical instability. If Type I blowup is excluded (which is itself an open problem), this concern disappears.

The weight of evidence SLIGHTLY favors kappa remaining bounded for the full NS dynamics:
- Three independent structural mechanisms (restricted Euler damping, LIA/NLS boundedness, viscous feedback) all point toward kappa control
- DNS evidence (limited) supports boundedness
- The Hou-Luo scenario shows DHY could hold even when CF fails (a valuable qualitative insight)

But the evidence AGAINST is also serious:
- The source term D_xi S involves supercritical quantities (nabla^2 u) that cannot be controlled from available estimates
- The pressure Hessian prevents the restricted Euler damping from operating at full strength in the physical regime
- No closed estimate for kappa has been found that does not require controlling nabla^2 u

### 8.2 Main results

**Result 1 (Theorem-level).** The evolution equation for eta = D_xi xi under 3D NS is equation (22):

    D_t eta = P_perp(S eta) - 2Q eta + P_perp((D_xi S) xi) + V_nu

The linear operator [S_perp - 2Q I_perp] acting on eta has eigenvalues (s_1 - 2s_2) and (s_3 - 2s_2) in the strain eigenbasis (under the e_2-alignment assumption). The first eigenvalue is positive for s_2/s_1 < 1/2 (the DNS regime) and negative for s_2/s_1 > 1/2 (the restricted Euler attractor regime). The second eigenvalue is always negative.

**Result 2 (Theorem-level).** In the restricted Euler model (nu = 0, H = isotropic), kappa is DAMPED along the blowup trajectory. The Vieillefosse attractor s_2/s_1 -> 1 makes both eigenvalues of the linear operator negative, causing kappa -> 0 as |omega| -> infinity. Restricted Euler blowup straightens vortex lines.

**Result 3 (Structural).** The Hasimoto transform maps the evolution of vortex filament curvature to 1D cubic NLS, which is globally well-posed. This provides a structural mechanism preventing curvature blowup for thin, isolated vortex tubes under LIA dynamics.

**Result 4 (Structural).** Large curvature kappa directly enhances viscous damping of |omega| at vorticity maxima, with damping rate >= nu kappa^2 |omega|. This creates a negative feedback: large curvature resists vorticity amplification.

**Result 5 (Negative).** The evolution of kappa^2 contains a source term 2 eta . (D_xi S) xi involving nabla^2 u, which is supercritical and cannot be controlled by available energy estimates. No maximum principle for kappa^2 can close without controlling this term.

**Result 6 (Observation).** Under Type I self-similar blowup, kappa ~ (T-t)^{-1/2}, which is milder than |omega| ~ (T-t)^{-1}. The ratio kappa/|omega| -> 0, meaning vortex lines become relatively straighter as vorticity blows up (in a scaled sense).

### 8.3 Kill conditions

**Kill condition for the vorticity-direction route (Direction 3): NOT triggered.**

The route is not dead. The structural evidence (restricted Euler damping, LIA/NLS, viscous feedback, DNS) all point toward kappa boundedness. No mechanism for kappa blowup has been identified that does not simultaneously require |omega| blowup (which the DHY condition prevents).

However, the route is also not complete. The supercritical source term D_xi S prevents closure of the kappa^2 estimate. The route remains at the stage of a "conditional result + structural evidence" -- it identifies the right geometric quantity (kappa) and the right mechanisms (multiple damping pathways), but cannot close the final estimate.

**Kill condition for the specific approach of proving kappa bounded via maximum principle: TRIGGERED.** The maximum principle approach for kappa^2 fails due to the supercritical source term. A different approach is needed.

### 8.4 Additions for the canonical NS status document

The following should be added:

**New structural results:**

1. **Curvature evolution equation.** The evolution of the vortex-line curvature kappa = |D_xi xi| under NS has been derived. The linear part damps kappa in the restricted Euler regime (s_2/s_1 -> 1) but has one amplifying direction in the DNS regime (s_2/s_1 ~ 0.3). The evolution contains a supercritical source term involving nabla^2 u.

2. **Restricted Euler damps curvature.** In the restricted Euler model, kappa -> 0 as |omega| -> infinity along the Vieillefosse blowup trajectory. Both eigenvalues of the curvature evolution operator become negative at the blowup attractor (eigenvalue ratio 1:1:-2). This means restricted Euler blowup straightens vortex lines -- the opposite of what was needed for DHY failure.

3. **Hasimoto/NLS connection.** Vortex-line curvature under LIA maps to 1D cubic NLS via the Hasimoto transform. Global well-posedness of 1D cubic NLS implies curvature boundedness for thin vortex filaments under LIA dynamics. This is a structural regularity mechanism not present in the standard PDE analysis.

4. **Curvature-viscosity feedback.** Large vortex-line curvature directly enhances viscous damping of vorticity maxima: the damping rate is >= nu kappa^2 |omega|. This creates a self-regulating mechanism opposing simultaneous growth of both |omega| and kappa.

5. **Type I self-similar scaling of kappa.** Under Type I blowup, kappa ~ (T-t)^{-1/2} while |omega| ~ (T-t)^{-1}. The ratio kappa/|omega| -> 0. Curvature blowup is a mild dimensional consequence, not a dynamical instability. Vortex lines become relatively straighter under self-similar blowup.

**Route status update:**

The vorticity-direction regularity route (via DHY condition) survives this analysis with the status: **structurally supported but analytically incomplete.** The curvature kappa = |D_xi xi| is the correct geometric quantity controlling the DHY condition. Multiple independent mechanisms (restricted Euler damping, LIA/NLS, viscous feedback) resist kappa blowup. But no closed estimate has been found: the source term D_xi S involves supercritical quantities (nabla^2 u) that prevent closure via maximum-principle or energy methods.

**Closed sub-approaches:**
- Maximum principle for kappa^2: killed by the supercritical source term.
- Monotone quantity kappa^2/|omega|^{2alpha}: no useful choice of alpha found.

**Open sub-approaches:**
- Exploit the LIA/NLS structure to prove kappa boundedness for tube-like configurations, then show high-vorticity regions are tube-like. (This requires proving two independent hard results.)
- Find a geometric functional that combines kappa with other curvature invariants (torsion, etc.) and that satisfies a better evolution equation. (Speculative.)
- Use the curvature-viscosity feedback (kappa damps |omega|) to show that simultaneous blowup of both is impossible. (This is a coupled bootstrap argument that might close if the coupling is sufficiently nonlinear.)

### 8.5 What should be pursued next

**Highest priority: the coupled bootstrap argument.**

The most promising avenue is to combine:
- The kappa evolution: D_t(kappa^2) <= C s_1 kappa^2 + C kappa |D_xi S| + viscous terms
- The |omega| evolution at the maximum: D_t |omega|_{max} <= s_2 |omega|_{max} - nu kappa^2 |omega|_{max}
- The Biot-Savart constraints: s_1 <= C |omega| (from the BKM-type logarithmic estimate)

If kappa^2 and |omega| can be shown to satisfy a COUPLED system where each quantity's growth is damped by the other, then the coupled system might have global bounds even though each individual equation does not close.

Specifically: large |omega| damps kappa (through restricted Euler dynamics with s_2/s_1 -> 1). Large kappa damps |omega| (through the viscous term nu kappa^2 |omega|). If these dampings interact in the right order, the coupled system could be bounded.

The key technical challenge: the source term D_xi S in the kappa equation involves nabla^2 u, which grows with |omega|. Whether the coupled damping beats this source growth is a quantitative question that requires a careful analysis of the scaling exponents.

**Estimated probability of success: 10-20%.** The structural signals are favorable, but the supercritical gap (control of nabla^2 u) remains the central obstacle, and coupled bootstrap arguments at the supercritical level have no precedent in the NS literature.

**Second priority: the Hou-Luo test.**

Compute kappa = |D_xi xi| numerically from the Hou-Luo data (or reproduce their computation and extract kappa). If kappa remains bounded even as |nabla xi| diverges, this provides strong numerical evidence for the DHY route and against the CF route. If kappa also diverges, the route is (numerically) dead.

**Third priority: LIA/NLS to NS comparison.**

Quantify the regime of validity of the LIA/NLS description for NS vortex tubes. Specifically: at what curvature does the thin-core approximation break down, and what happens to the curvature evolution beyond this threshold? If the NS dynamics take over and damp curvature when kappa r_c ~ O(1) (through viscous core thickening), then there may be a handoff from the LIA/NLS regime to the viscous regime that keeps kappa bounded throughout.

---

## Summary

The curvature of vortex lines, kappa = |D_xi xi|, is the decisive geometric quantity for the Deng-Hou-Yu regularity criterion. This analysis derived its evolution equation, identified the key terms (linear interaction with strain eigenvalues, supercritical source from strain gradients, viscous diffusion), and analyzed its behavior under progressively more realistic models:

1. **Restricted Euler:** kappa is damped. The blowup attractor straightens vortex lines.
2. **With viscosity:** additional damping, especially at vorticity maxima.
3. **With pressure Hessian:** the damping is partially undermined (eigenvalue ratios stay in the amplifying regime for one component), but no blowup mechanism is introduced.
4. **Under LIA/Hasimoto:** kappa is bounded by the global well-posedness of 1D cubic NLS.

No mechanism for kappa blowup was found. Multiple independent mechanisms for kappa control were found. But the supercritical source term D_xi S prevents any closed estimate, placing this result firmly in the category of "strong structural evidence, no proof."

The honest bottom line: **the vorticity-direction route via DHY is the most structurally promising approach to NS regularity identified in this pursuit.** It has genuine geometric content (curvature boundedness), multiple supporting mechanisms, favorable DNS evidence, and connections to integrable systems (NLS). But it remains at the level of a beautifully motivated conjecture, not a proof. The gap between the structural understanding and a rigorous proof is exactly the gap of the Millennium Prize problem: control of nabla^2 u at the supercritical level.
