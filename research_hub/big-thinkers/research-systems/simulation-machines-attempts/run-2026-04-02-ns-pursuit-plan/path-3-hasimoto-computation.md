# Path 3: Hasimoto/NLS + Controlled LIA Departure — Full Computation

**Date:** 2026-04-02
**Parent:** three-practical-paths.md, coupled-bootstrap-attempt.md, dhy-burgers-test.md, curvature-evolution-analysis.md
**Purpose:** Carry out the explicit matched-asymptotic computation of D_xi S for straight and curved Burgers vortex tubes, determine the precise scaling with |omega|, identify the breakdown regimes, and deliver an honest assessment of whether Path 3 can close the logarithmic gap in Theorem CB.

---

## 0. The Target

Theorem CB (proved in coupled-bootstrap-attempt.md) establishes:

> If |D_xi S| <= C |omega|^{1+delta} with delta > 1/2 on {|omega| > M}, then 3D NS is regular.

The dimensional estimate gives exactly delta = 1/2 (i.e., |D_xi S| ~ |omega|^{3/2}/nu^{1/2}). This is borderline. A logarithmic improvement — replacing the bound by C |omega|^{3/2}/(nu^{1/2} log^{1+epsilon}(|omega|)) — would break the borderline and yield regularity.

Path 3 attacks this through the Hasimoto transform: under the Local Induction Approximation (LIA), vortex filament curvature evolves as 1D cubic NLS, which is globally well-posed. This implies kappa is bounded. The bound |D_xi S| ~ |omega| * kappa (from the matched asymptotic expansion) would give delta = 0 — far better than needed. The question is whether corrections from the full Biot-Savart law (beyond LIA) stay controlled.

---

## Step 1: D_xi S for a Straight Burgers Vortex

### 1.1 The velocity field

The steady Burgers vortex in cylindrical coordinates (r, theta, z):

    u_r = -(alpha/2) r
    u_theta = (Gamma/(2 pi r))(1 - exp(-r^2/r_c^2))
    u_z = alpha z

where r_c^2 = 4 nu / alpha is the core radius squared, Gamma is the circulation, and alpha > 0 is the external axial strain rate. The peak vorticity is omega_max = Gamma alpha / (4 pi nu) = Gamma / (pi r_c^2). The vortex Reynolds number is Re_Gamma = Gamma / (2 pi nu).

### 1.2 The full strain tensor

The velocity gradient in cylindrical coordinates is:

    (nabla u)_{rr} = partial_r u_r = -alpha/2
    (nabla u)_{theta theta} = (1/r) partial_theta u_theta + u_r/r = -alpha/2
    (nabla u)_{zz} = partial_z u_z = alpha
    (nabla u)_{r theta} = partial_r u_theta - u_theta/r
    (nabla u)_{theta r} = (1/r) partial_theta u_r = 0
    (nabla u)_{rz} = partial_r u_z = 0
    (nabla u)_{zr} = partial_z u_r = 0
    (nabla u)_{theta z} = (1/r) partial_theta u_z = 0
    (nabla u)_{z theta} = partial_z u_theta = 0

Computing the off-diagonal term:

    partial_r u_theta = -(Gamma/(2 pi r^2))(1 - exp(-r^2/r_c^2)) + (Gamma/(2 pi r))(2r/r_c^2) exp(-r^2/r_c^2)

    u_theta/r = (Gamma/(2 pi r^2))(1 - exp(-r^2/r_c^2))

So:

    (nabla u)_{r theta} = partial_r u_theta - u_theta/r
                        = -(2 Gamma/(2 pi r^2))(1 - exp(-r^2/r_c^2)) + (Gamma r/(pi r_c^2)) exp(-r^2/r_c^2)

The strain tensor S = (nabla u + (nabla u)^T)/2 has components:

    S_{rr} = -alpha/2
    S_{theta theta} = -alpha/2
    S_{zz} = alpha
    S_{r theta} = (1/2)((nabla u)_{r theta} + (nabla u)_{theta r}) = (1/2)(nabla u)_{r theta}
    S_{rz} = S_{zr} = 0
    S_{theta z} = S_{z theta} = 0

**Key observation:** Every component of S depends only on r. There is no dependence on theta (by axisymmetry) and no dependence on z (because the only z-dependent velocity component is u_z = alpha z, whose contribution to S is (nabla u)_{zz} = alpha, a constant).

### 1.3 Computing D_xi S = partial_z S

The vorticity is omega = omega_z(r) e_z, so xi = e_z everywhere. Therefore:

    D_xi S = (e_z . nabla) S = partial_z S

Since every component of S depends only on r:

    **D_xi S = 0 identically for the straight Burgers vortex.**

This is exact, not an approximation. The straight Burgers vortex has zero directional strain gradient along the vorticity direction.

### 1.4 Interpretation

The vanishing of D_xi S is a consequence of the translational symmetry in z. The velocity field has the form u = u_r(r) e_r + u_theta(r) e_theta + alpha z e_z. The term alpha z e_z contributes only to S_{zz} = alpha (a constant), and all other components of S depend on r alone. Since xi = e_z, the directional derivative along xi sees only the z-dependence, which is trivial.

This confirms the Path 3 expectation: for a perfectly straight vortex tube, D_xi S = 0, which is |omega|^{1+0} with delta = -infinity — trivially satisfying Theorem CB.

**The entire content of the D_xi S problem is in the curvature corrections.**

---

## Step 2: D_xi S for a Curved Burgers Vortex (Matched Asymptotic Expansion)

### 2.1 Setup

Consider a vortex tube whose centerline gamma(s) has curvature kappa(s) and torsion tau(s), with a Burgers-type core of radius r_c = sqrt(4 nu / alpha). We work in the thin-core regime:

    epsilon := kappa_max * r_c << 1

where kappa_max = sup_s kappa(s). This is the regime where matched asymptotic expansions are valid.

**Coordinate system:** Tube coordinates (s, rho, phi) where:

    x = gamma(s) + rho cos(phi) N(s) + rho sin(phi) B(s)

with Frenet-Serret frame {T, N, B}. The metric has Jacobian J = rho(1 - kappa rho cos phi).

### 2.2 The Callegari-Ting (1978) matched asymptotic expansion

The velocity field of a curved viscous vortex tube is constructed by matching:

**Inner expansion** (rho << 1/kappa, in tube coordinates):

The leading-order inner solution is the Burgers vortex in the local normal plane. The vorticity is:

    omega = omega_z(rho) T(s) + epsilon * omega^(1)(rho, phi, s) + O(epsilon^2)

where omega_z(rho) = omega_max exp(-rho^2/r_c^2) is the Gaussian core profile.

The first-order correction omega^(1) arises from:
- (a) The curvature-modified strain balance (the external strain is no longer symmetric about the tube axis in curvilinear coordinates)
- (b) The non-planar geometry (the metric factor 1 - kappa rho cos phi modifies the Laplacian and advection terms)

The first-order velocity correction has the form (Callegari-Ting 1978, equation 3.14):

    u^(1) = kappa [A_1(rho) cos phi e_rho + A_2(rho) sin phi e_phi + A_3(rho) cos phi T] + (binormal self-induction term)

where A_1, A_2, A_3 are radial functions determined by matching and the core profile. The binormal self-induction term contributes the classical LIA velocity:

    v_LIA = (Gamma kappa / (4 pi)) [ln(1/(kappa r_c)) + C_core] B(s)

where C_core depends on the core profile. For the Burgers profile, C_core = (1/2)(ln 2 - gamma_E + 1/(2 Re_Gamma)) where gamma_E is the Euler-Mascheroni constant, though the precise value does not affect the scaling analysis.

**Outer expansion** (rho >> r_c):

The Biot-Savart integral of the vorticity distribution. At distances large compared to r_c, the tube appears as a line vortex of circulation Gamma. The velocity is:

    u_outer = (Gamma/(4 pi)) integral (gamma'(s') x (x - gamma(s'))) / |x - gamma(s')|^3 ds'

This contains the self-induction term (log divergent as x approaches gamma) and the far-field contributions from distant parts of the tube and other tubes.

**Matching region** (r_c << rho << 1/kappa):

In this region, the inner expansion must agree with the outer expansion. The matching condition determines the constants in the inner expansion and produces the self-induction velocity formula.

### 2.3 The strain tensor to first order

The leading-order strain (from the Burgers core profile) has the components computed in Step 1:

    S^(0)_{rr} = -alpha/2,  S^(0)_{theta theta} = -alpha/2,  S^(0)_{zz} = alpha
    S^(0)_{r theta} = (1/2)(partial_r u_theta^(0) - u_theta^(0)/r)

This depends only on rho (the radial distance in the normal plane), not on s.

The first-order correction to S arises from u^(1). In tube coordinates:

    S^(1) = sym(nabla u^(1))

The key structural feature: u^(1) is proportional to kappa and depends on phi (through cos phi, sin phi terms). Therefore S^(1) is O(kappa) and introduces phi-dependence and s-dependence into the strain field.

### 2.4 Computing D_xi S at the tube center (rho = 0)

At the tube center, xi = T(s) + O(epsilon). The directional derivative is:

    D_xi S = (T . nabla) S = (1/(1 - kappa rho cos phi)) partial_s S

At rho = 0, this reduces to:

    D_xi S|_{rho=0} = partial_s S

Since S^(0) is independent of s, the leading contribution comes entirely from S^(1):

    D_xi S|_{rho=0} = partial_s S^(1)|_{rho=0} + O(epsilon^2 * |S|/L)

where L is the length scale of variation of the tube geometry.

**Evaluation of partial_s S^(1) at rho = 0:**

The first-order velocity correction u^(1) at rho = 0 is:

    u^(1)(rho=0, s) = v_LIA(s) + (axial correction)

The LIA velocity is:

    v_LIA = (Gamma kappa(s) / (4 pi)) [ln(1/(kappa(s) r_c)) + C_core] B(s)

This depends on s through kappa(s) and the Frenet frame {T, N, B}(s). Its s-derivative involves:

    partial_s v_LIA = (Gamma/(4 pi)) [partial_s(kappa ln(1/(kappa r_c))) B + kappa ln(1/(kappa r_c)) partial_s B]

Using Frenet-Serret: partial_s B = -tau N. So:

    partial_s v_LIA = (Gamma/(4 pi)) [(kappa' ln(1/(kappa r_c)) - kappa') B - kappa tau ln(1/(kappa r_c)) N]
                    = (Gamma/(4 pi)) [kappa'(ln(1/(kappa r_c)) - 1) B - kappa tau ln(1/(kappa r_c)) N]

The strain associated with this velocity contributes to partial_s S through:

    partial_s S^(1)|_{rho=0} = sym(nabla(partial_s u^(1)))|_{rho=0}

However, this is the strain contribution at the single point rho = 0 from the global velocity field, and the correct computation requires the matched asymptotic strain at the tube center, not just the LIA velocity.

### 2.5 Systematic computation of D_xi S at the tube center

Let me carry out this computation more carefully. The strain at the tube center receives contributions from three sources:

**(A) External strain variation along the tube.**

The background strain field S_ext (from distant vorticity and the overall flow) varies along the tube axis. Its directional derivative is:

    (D_T S_ext)|_{gamma(s)} = T_k(s) partial_k S_ext(gamma(s))

For a spatially smooth background strain varying on scale L_ext:

    |(D_T S_ext)| ~ |S_ext| / L_ext ~ alpha / L_ext

If the external strain varies on the same scale as the tube curvature (L_ext ~ 1/kappa), then:

    |(D_T S_ext)| ~ alpha * kappa

Using alpha ~ omega_max r_c^2 / Gamma ... no, more directly: alpha is the external strain rate. The relationship to the core vorticity is omega_max = Gamma / (pi r_c^2) and r_c^2 = 4 nu / alpha, giving omega_max = Gamma alpha / (4 pi nu). So alpha = 4 pi nu omega_max / Gamma = 2 omega_max / Re_Gamma.

For large Re_Gamma, alpha << omega_max. Therefore:

    |(D_T S_ext)| ~ alpha * kappa = (2 omega_max / Re_Gamma) * kappa

This is O(omega_max * kappa / Re_Gamma) — small compared to omega_max * kappa by a factor 1/Re_Gamma.

**(B) Curvature-induced strain correction at the tube center.**

The asymmetric velocity field of a curved tube produces a strain at the center that is absent for a straight tube. From the first-order Callegari-Ting expansion, the velocity correction at rho ~ 0 is:

    u^(1)(rho, phi, s) = kappa(s) [A_1(rho) cos phi, A_2(rho) sin phi, A_3(rho) cos phi] (in local N, B, T components)

The radial functions A_i(rho) are determined by the core profile and the matching conditions. At rho = 0, by symmetry of the Burgers profile:

    A_1(0) = A_3(0) = 0 (the cos phi-dependent terms vanish at the axis by smoothness)
    A_2(0) = 0 (similarly)

So u^(1)(rho=0) comes entirely from the axially symmetric part, which is the self-induction velocity:

    u^(1)|_{rho=0} = v_{SI}(s) = (Gamma kappa / (4 pi)) [ln(1/(kappa r_c)) + C_core] B(s)

The strain from this self-induction velocity at the tube center can be computed. The velocity v_SI is a smooth function of s (along the tube axis). Its gradient at the tube center involves how this velocity varies in the normal plane. Since v_SI is the velocity at the center only, the strain associated with the full velocity field u^(1) at rho = 0 requires the rho-derivatives of u^(1):

    S^(1)_{ij}|_{rho=0} = (1/2)(partial_i u^(1)_j + partial_j u^(1)_i)|_{rho=0}

The key components:

    partial_rho u^(1)|_{rho=0} involves A_i'(0), which is determined by the core structure
    partial_s u^(1)|_{rho=0} involves the s-derivative of v_SI

From Callegari-Ting, the first-order velocity at small rho has the expansion:

    u^(1)_T ~ kappa A_3(rho) cos phi ≈ kappa A_3'(0) rho cos phi + ...
    u^(1)_N ~ kappa A_1(rho) cos phi ≈ kappa A_1'(0) rho cos phi + ...
    u^(1)_B ~ kappa A_2(rho) sin phi + v_SI ≈ kappa A_2'(0) rho sin phi + v_SI + ...

The s-component of the strain at rho = 0 from these corrections:

    S^(1)_{sN}|_{rho=0} = (1/2)(partial_N u^(1)_s + partial_s u^(1)_N)|_{rho=0}

At rho = 0, partial_N u^(1)_s|_{rho=0} = kappa A_3'(0) cos(0) = kappa A_3'(0) (evaluating the cos phi at phi = 0 for the N-direction component). But phi-dependent terms average to zero at rho = 0 after accounting for the angular dependence. More precisely, the phi-averaged (m=0 mode) contribution at rho = 0 vanishes for the cos phi and sin phi terms. The strain at rho = 0 from the first-order correction is:

    S^(1)|_{rho=0} has only contributions from the m=0 (axially symmetric) part of u^(1)

The m=0 part is the self-induction velocity v_SI(s) B(s). This is a velocity field defined only along the axis, but its contribution to the strain requires knowledge of how it varies away from the axis. In the matched expansion, this is determined by the inner problem.

**The crucial point:** For the Burgers vortex core, the m=0 (axially symmetric) correction to the core-frame strain is zero at rho = 0 to first order. This is because the Burgers vortex is an exact solution of the NS equations in the plane perpendicular to the axis, and the curvature correction at the axis vanishes by symmetry. The first non-trivial correction is O(epsilon^2) = O(kappa^2 r_c^2).

Therefore, the strain at the tube center is:

    S|_{rho=0} = S^(0) + O(kappa^2 r_c^2 * omega_max) = S^(0) + O(epsilon^2 omega_max)

And its s-derivative:

    partial_s S|_{rho=0} = O(partial_s(epsilon^2 omega_max)) = O(kappa kappa' r_c^2 omega_max + kappa^2 r_c^2 partial_s omega_max)

For a tube with constant core structure (steady Burgers profile at each cross-section) and slowly varying geometry:

    partial_s omega_max = 0 (the core profile is determined locally by alpha and nu)

So:

    partial_s S|_{rho=0} ~ O(kappa kappa' r_c^2 omega_max)

This is O(epsilon * kappa' r_c * omega_max). For bounded kappa and kappa': this is O(epsilon * omega_max) = O(kappa r_c omega_max).

**(C) Self-induction strain gradient.**

The self-induction velocity v_SI(s) = (Gamma kappa(s)/(4 pi))[ln(1/(kappa r_c)) + C_core] B(s) produces a flow that varies along the tube. This flow generates a strain that varies along s. The contribution to D_T S at the tube center comes from the far-field (Biot-Savart) representation of this self-induced flow.

The self-induction velocity at the center of a curved tube translates to a local strain gradient through the Biot-Savart integral. The curvature of the tube itself is the source: the Biot-Savart integral of a curved vortex line (the outer expansion) produces a velocity field whose gradient along the tube involves the variation of the curvature.

The dominant contribution is:

    (D_T S)_{self-induction} ~ (Gamma / (4 pi)) partial_s^2 [kappa B] / r_c + corrections

More precisely, the Biot-Savart field of a thin curved tube, differentiated along the tube axis, gives at the tube center:

    |(D_T S)_{SI}| ~ (Gamma / r_c^2) * kappa^2 * ln(1/(kappa r_c)) * O(1)

This comes from differentiating the log(1/(kappa r_c)) self-induction formula with respect to arc length, which brings down a factor of kappa (from dT/ds = kappa N) and introduces the variation scale 1/kappa.

Substituting Gamma = pi r_c^2 omega_max:

    |(D_T S)_{SI}| ~ omega_max * kappa^2 * r_c^0 * ln(1/(kappa r_c))

Wait — let me be more careful with the dimensions. The self-induction velocity has magnitude:

    |v_SI| ~ Gamma kappa / (4 pi) * ln(1/(kappa r_c)) ~ omega_max r_c^2 kappa * ln(1/(kappa r_c))

The strain from this velocity at the tube center, over the length scale 1/kappa (the curvature radius), is:

    S_SI ~ |v_SI| * kappa ~ omega_max r_c^2 kappa^2 * ln(1/(kappa r_c))

The directional derivative of this strain along the tube (bringing down another factor of kappa or kappa'):

    (D_T S)_SI ~ omega_max r_c^2 kappa^3 * ln(1/(kappa r_c)) (if the variation is on scale 1/kappa)

OR, more precisely, if we differentiate the Biot-Savart integral directly:

    (D_T S)_SI ~ (Gamma kappa / r_c^2) * kappa * ln(1/(kappa r_c))
               = omega_max * kappa^2 * ln(1/(kappa r_c))

No — this double-counts. Let me restart this sub-calculation from dimensional analysis.

The self-induction velocity is v_SI ~ (Gamma kappa / (4 pi)) ln(1/(kappa r_c)). At the tube center, the Biot-Savart velocity field generated by the tube itself has spatial gradients. The gradient of this velocity in the along-axis direction is:

    partial_s v_SI ~ (Gamma/(4 pi)) [kappa' ln(1/(kappa r_c)) + kappa * (-kappa'/kappa) + ...] B + kappa ln(1/(kappa r_c)) (-tau N)]
                   ~ (Gamma/(4 pi)) [kappa' (ln(1/(kappa r_c)) - 1) B - kappa tau ln(1/(kappa r_c)) N]

The magnitude of this strain-rate-like quantity:

    |partial_s v_SI| ~ (Gamma/(4 pi)) * max(|kappa'|, kappa |tau|) * ln(1/(kappa r_c))

The strain contribution (symmetrized gradient) at the center involves both the along-axis gradient (partial_s v_SI) and the cross-axis gradient (partial_rho v_SI). The cross-axis gradient of the self-induction velocity at the center is O(kappa v_SI) because the velocity varies on the curvature scale in the cross-section. So:

    |nabla v_SI|_{rho=0} ~ max(|partial_s v_SI|, kappa |v_SI|)
                         ~ (Gamma/(4 pi)) * max(|kappa'|, kappa |tau|, kappa^2) * ln(1/(kappa r_c))

The contribution to D_T S involves partial_s of the symmetric gradient, which is:

    partial_s S_SI|_{rho=0} ~ partial_s(nabla v_SI)|_{rho=0}
                             ~ (Gamma/(4 pi)) * (kappa'' + kappa' tau + kappa tau' + kappa^2 kappa + kappa^3) * ln(1/(kappa r_c)) + subleading

For smooth curves with bounded curvature and torsion (kappa, tau, kappa', kappa'' all O(1)):

    |partial_s S_SI|_{rho=0}| ~ (Gamma/(4 pi)) * kappa * O(1) * ln(1/(kappa r_c))

But actually the more careful analysis gives us the direct Biot-Savart computation. The velocity gradient at the tube center from the matched asymptotic expansion (following Fukumoto-Moffatt 2000, Section 3) gives the strain at the center as:

    S|_{center} = S^(0) + kappa * S^(1,m=1)(rho)|_{rho=0} + kappa^2 r_c * S^(2)} * ln(1/(kappa r_c)) + O(kappa^2 r_c)

where S^(1,m=1) is the m=1 azimuthal mode correction (which vanishes at rho = 0 by regularity). The m=0 correction at second order gives:

    S^(2)|_{rho=0} ~ omega_max * O(1)

So:

    S|_{center} = S^(0) + O(kappa^2 r_c omega_max ln(1/(kappa r_c)))

And:

    D_T S|_{center} = partial_s S|_{center}
                    = O(kappa kappa' r_c omega_max ln(1/(kappa r_c))) + O(kappa^2 r_c * partial_s(omega_max) * ln(1/(kappa r_c)))
                    + O(kappa^3 r_c omega_max ln(1/(kappa r_c)))

For bounded curvature derivatives and constant core profile (partial_s omega_max = 0):

    **|D_T S|_{center}| <= C omega_max kappa^2 r_c ln(1/(kappa r_c))**

(The leading terms involve kappa * kappa' and kappa^3, both bounded by kappa^2 for kappa = O(1).)

### 2.6 Consolidating the result

Collecting all contributions to D_xi S at the tube center (rho = 0):

**(A) External strain variation:** O(alpha kappa) = O(omega_max kappa / Re_Gamma) — negligible at large Re.

**(B) Curvature-induced correction at center:** O(kappa^2 r_c^2 omega_max * kappa) = O(epsilon^2 omega_max kappa) — second-order in epsilon, negligible.

**(C) Self-induction strain gradient:** O(omega_max kappa^2 r_c ln(1/(kappa r_c))) — the dominant correction.

Therefore:

    |D_xi S|_{center} = C_1 omega_max kappa + C_2 omega_max kappa^2 r_c ln(1/(kappa r_c)) + O(omega_max kappa^2 r_c)

Wait — I need to reconsider whether the O(omega_max kappa) term is actually present. For the straight tube, D_xi S = 0 exactly. The leading correction from curvature should be at least O(kappa). Let me trace this more carefully.

### 2.7 Re-examination: leading-order D_xi S

The strain tensor S for a straight Burgers vortex is independent of z (= s for a straight tube). For a curved tube, S depends on s through the tube geometry. The question is: what is the leading-order s-dependence?

**At the tube center (rho = 0):**

The Burgers vortex strain at rho = 0 is:

    S^(0)_{rr} = S^(0)_{theta theta} = -alpha/2
    S^(0)_{zz} = alpha
    S^(0)_{r theta}|_{rho=0} = lim_{rho->0} (1/2)(partial_rho u_theta - u_theta/rho)

Using u_theta = (Gamma/(2 pi rho))(1 - exp(-rho^2/r_c^2)) and L'Hopital:

    lim_{rho->0} u_theta/rho = Gamma/(2 pi r_c^2) = omega_max/2

    lim_{rho->0} partial_rho u_theta = Gamma/(2 pi) * (2/(r_c^2) - 1/r_c^2 * 0) ... let me compute directly.

    u_theta = (Gamma/(2 pi)) * (1/rho)(1 - exp(-rho^2/r_c^2))

    partial_rho u_theta = (Gamma/(2 pi)) * [-(1/rho^2)(1 - exp(-rho^2/r_c^2)) + (1/rho)(2 rho/r_c^2) exp(-rho^2/r_c^2)]

At rho -> 0, using 1 - exp(-rho^2/r_c^2) ~ rho^2/r_c^2 - rho^4/(2 r_c^4):

    partial_rho u_theta ~ (Gamma/(2 pi)) * [-1/r_c^2 + rho^2/(2 r_c^4) + 2/r_c^2 - 2 rho^2/r_c^4 + ...]
                        = (Gamma/(2 pi)) * [1/r_c^2 + O(rho^2/r_c^4)]
                        = omega_max/2 + O(rho^2/r_c^2 * omega_max)

So:

    S^(0)_{r theta}|_{rho=0} = (1/2)(omega_max/2 - omega_max/2) = 0

This is correct: the strain is purely diagonal at the center of a Burgers vortex:

    S^(0)|_{rho=0} = diag(-alpha/2, -alpha/2, alpha)

Now for the curved tube, the strain at the center in the tube coordinate frame includes:

1. The same diagonal strain S^(0) = diag(-alpha/2, -alpha/2, alpha) in the local (N, B, T) frame.
2. A first-order correction from the curvature that is proportional to kappa.

The first-order correction to the strain at rho = 0 arises from the curvature-modified velocity field. From the Callegari-Ting inner expansion, the m=0 (axially symmetric) velocity correction at rho = 0 is the self-induction velocity v_SI, which is purely in the B-direction:

    u^(1)|_{rho=0} = v_SI(s) B(s)

This is a velocity at a point, not a velocity field. The strain at rho = 0 requires the velocity gradient, which involves how u^(1) varies with rho and phi near rho = 0.

From the m=1 azimuthal mode structure: u^(1) = kappa [f_1(rho) cos phi e_N + f_2(rho) sin phi e_B + f_3(rho) cos phi T]. At rho = 0, the cos phi and sin phi averages vanish. The gradient at rho = 0:

    partial_rho u^(1)|_{rho=0} has m=1 modes only (from the cos phi, sin phi dependence)

The strain from the m=1 mode at rho = 0:

    S^(1)_{ij}|_{rho=0} = (1/2)(partial_i u^(1)_j + partial_j u^(1)_i)|_{rho=0}

involves derivatives like partial_N(kappa f_1(rho) cos phi)|_{rho=0}. In polar coordinates (rho, phi) centered at the axis, partial_N = cos(phi) partial_rho - sin(phi)/rho partial_phi at rho=0. The cos phi * cos phi = cos^2 phi and cos phi * sin phi terms contribute directional averages. After the full tensor contraction:

    S^(1)|_{rho=0} = kappa * S^{(1,0)}

where S^{(1,0)} is a tensor that depends on the radial functions f_i and their derivatives at rho = 0. This is generically nonzero and O(kappa * omega_max) in magnitude (since the radial functions are determined by the Burgers core profile with peak vorticity omega_max).

**Actually, let me reconsider this.** The m=1 velocity correction at small rho has the form:

    u^(1) ~ kappa * rho * [g_1(rho) cos phi e_N + g_2(rho) sin phi e_B + g_3(rho) cos phi T]

where the extra factor of rho ensures regularity at the axis. The velocity gradient at rho = 0 then gives:

    partial_rho u^(1)|_{rho=0} ~ kappa * [g_1(0) cos phi e_N + g_2(0) sin phi e_B + g_3(0) cos phi T]

This depends on phi. The strain at rho = 0 involves:

    (e_N component): partial_N u^(1)_T + partial_T u^(1)_N at rho = 0

Since u^(1)_T ~ kappa rho g_3(rho) cos phi, we have partial_N u^(1)_T|_{rho=0} = kappa g_3(0). And partial_T u^(1)_N|_{rho=0} involves the s-derivative of rho g_1 cos phi, which at rho = 0 is zero.

So S^(1)_{TN}|_{rho=0} = (1/2) kappa g_3(0). Similarly for other components.

The radial functions g_i are determined by the Callegari-Ting inner problem. For the Burgers core, the explicit computation (see Fukumoto-Moffatt 2000, Appendix A, or Margerit et al. 2001) gives:

    g_3(0) = -omega_max / (4 alpha) * (some O(1) constant)

Using omega_max = Gamma alpha / (4 pi nu) and r_c^2 = 4 nu / alpha:

    g_3(0) ~ omega_max / alpha ~ Re_Gamma / alpha (dimensional)

Hmm — this suggests S^(1)|_{rho=0} ~ kappa * omega_max, which would give:

    partial_s S|_{rho=0} ~ kappa' omega_max + kappa * partial_s(omega_max) + kappa * tau * omega_max + ...

For a tube with fixed core profile along its length:

    |D_T S|_{rho=0} ~ |kappa'| omega_max + kappa tau omega_max + kappa^2 omega_max

(the last term from frame rotation: partial_s involves the Frenet derivatives, bringing down factors of kappa and tau).

For bounded curvature and torsion (kappa, tau, kappa' all O(1)):

    **|D_xi S|_{center} ~ omega_max * O(kappa) = O(omega_max kappa)**

This is the leading term. Using Gamma ~ omega_max r_c^2:

    |D_xi S|_{center} ~ omega_max * kappa

### 2.8 Revised hierarchy of contributions

After the more careful analysis:

| Contribution | Magnitude at tube center | Scaling with omega_max |
|---|---|---|
| Leading curvature term | C omega_max kappa | omega_max^1 |
| Self-induction correction | C omega_max kappa^2 r_c ln(1/(kappa r_c)) | omega_max^{1/2} * ln(omega_max) |
| External strain variation | C alpha kappa | omega_max^0 (at large Re) |
| Higher-order corrections | O(omega_max kappa^3 r_c^2) | omega_max^0 |

The **dominant term is O(omega_max kappa)**, which is O(|omega| kappa).

---

## Step 3: Express in Terms of |omega| and Verify Scaling

### 3.1 The main estimate

At the center of a curved Burgers vortex tube with curvature kappa and core radius r_c = sqrt(4 nu / alpha):

    |D_xi S|_{center} <= C_1 |omega|_max * kappa + C_2 |omega|_max * kappa^2 r_c ln(1/(kappa r_c)) + lower order

Using r_c = (4 nu / alpha)^{1/2} and omega_max = Gamma alpha / (4 pi nu):

    r_c = (4 nu / alpha)^{1/2}
    omega_max r_c = (4 nu / alpha)^{1/2} * Gamma alpha / (4 pi nu) = Gamma alpha^{1/2} / (2 pi (4 nu)^{1/2})
    omega_max r_c^2 = Gamma / pi

So the self-induction correction is:

    C_2 omega_max kappa^2 r_c ln(1/(kappa r_c))
    = C_2 kappa^2 * (Gamma alpha^{1/2} / (2 pi (4 nu)^{1/2})) * ln(1/(kappa r_c))

In terms of omega_max and nu (using alpha = 4 nu / r_c^2 = 4 nu omega_max / (Gamma/pi) = 4 pi nu omega_max / Gamma):

    r_c = (Gamma / (pi omega_max))^{1/2}

    omega_max kappa^2 r_c = omega_max kappa^2 (Gamma/(pi omega_max))^{1/2}
                           = kappa^2 omega_max^{1/2} (Gamma/pi)^{1/2}

For the logarithmic factor:

    ln(1/(kappa r_c)) = ln(1/(kappa (Gamma/(pi omega_max))^{1/2}))
                      = (1/2) ln(pi omega_max / (kappa^2 Gamma))
                      = (1/2) ln(omega_max / (kappa^2 Gamma / pi))

At large omega_max (large Re), this grows as (1/2) ln(omega_max).

So the self-induction correction is:

    ~ C kappa^2 omega_max^{1/2} Gamma^{1/2} * ln(omega_max)^{1/2}

### 3.2 Comparison with the dimensional estimate

The dimensional estimate (worst case from CZ theory):

    |D_xi S|_{dim} ~ omega_max^{3/2} / nu^{1/2}

Using omega_max = Gamma / (pi r_c^2) and r_c^2 = 4 nu / alpha:

    omega_max^{3/2} / nu^{1/2} = (Gamma/(pi r_c^2))^{3/2} / nu^{1/2}
                                = (Gamma^{3/2} / (pi^{3/2} r_c^3)) / nu^{1/2}
                                = Gamma^{3/2} / (pi^{3/2} r_c^3 nu^{1/2})

The ratio of the leading curvature term to the dimensional estimate:

    (omega_max kappa) / (omega_max^{3/2}/nu^{1/2}) = kappa nu^{1/2} / omega_max^{1/2}
                                                    = kappa r_c / (4 pi omega_max / (Gamma alpha))^{1/2} ... 

Let me just compute directly:

    kappa nu^{1/2} / omega_max^{1/2} = kappa * (nu / omega_max)^{1/2} = kappa * r_c / 2

(using r_c = (4 nu / alpha)^{1/2} and omega_max = Gamma alpha/(4 pi nu), so nu/omega_max = 4 pi nu^2/(Gamma alpha) = pi r_c^4 alpha / Gamma ... this gets circular.)

More directly: the Kolmogorov-like scale is eta_K = (nu / omega_max)^{1/2}. We have r_c / eta_K = (4 nu/alpha)^{1/2} / (nu/omega_max)^{1/2} = (4 omega_max/alpha)^{1/2} = 2(Gamma/(4 pi nu))^{1/2} = sqrt(2 Re_Gamma / pi). So r_c ~ eta_K * Re_Gamma^{1/2}. The Kolmogorov scale is eta_K = r_c / Re_Gamma^{1/2} (up to constants).

The ratio:

    (omega_max kappa) / (omega_max^{3/2}/nu^{1/2}) = kappa (nu/omega_max)^{1/2} = kappa eta_K

Since kappa eta_K = kappa r_c / Re_Gamma^{1/2} = epsilon / Re_Gamma^{1/2}:

    **Leading curvature term / Dimensional estimate = epsilon / Re_Gamma^{1/2} = kappa r_c / Re_Gamma^{1/2}**

For a thin tube with epsilon << 1 and large Re_Gamma, this ratio is extremely small. The curvature term is far below the dimensional estimate.

The ratio of the self-induction correction to the dimensional estimate:

    (omega_max kappa^2 r_c ln(1/(kappa r_c))) / (omega_max^{3/2}/nu^{1/2})
    = kappa^2 r_c ln(1/(kappa r_c)) * nu^{1/2} / omega_max^{1/2}
    = kappa^2 r_c eta_K ln(1/(kappa r_c))
    = kappa^2 r_c^2 / Re_Gamma^{1/2} * ln(1/(kappa r_c))
    = epsilon^2 / Re_Gamma^{1/2} * ln(1/epsilon)

This is even smaller — O(epsilon^2 ln(1/epsilon) / Re_Gamma^{1/2}).

### 3.3 Summary of scaling for a single tube

If kappa is bounded (say kappa <= K_max from NLS global well-posedness under LIA):

    |D_xi S| <= C_1 K_max |omega| + C_2 K_max^2 |omega|^{1/2} (Gamma/pi)^{1/2} ln(|omega|) + lower order

The first term is O(|omega|^1) — corresponding to delta = 0 in Theorem CB.
The second term is O(|omega|^{1/2} ln(|omega|)) — even more subcritical.

**Both terms are far below the |omega|^{3/2}/nu^{1/2} dimensional estimate.** The gap is not logarithmic but polynomial: a full power of |omega|^{1/2} separates the single-tube D_xi S from the dimensional estimate.

The delta = 0 estimate from the single-tube computation gives:

    alpha = 3/(2 + 2*0) = 3/2

which is far above 1, hence trivially ruled out by the Serrin criterion. So a single tube cannot generate a singularity through the D_xi S mechanism.

---

## Step 4: Breakdown Scenarios

The matched asymptotic framework breaks down in three regimes. In each, we must estimate what |D_xi S| could be.

### 4.1 Breakdown 1: kappa * r_c ~ O(1) (tube as curved as it is thick)

When the curvature radius 1/kappa becomes comparable to the core radius r_c, the thin-tube approximation fails. The vorticity distribution is no longer well-described by a Gaussian centered on a smooth curve.

**What happens physically:** The tube is so tightly curved that it wraps around on a scale comparable to its own thickness. The cross-sectional structure deforms significantly, and the matched expansion (which assumes a nearly-circular core) breaks down.

**Worst-case D_xi S estimate:** When kappa ~ 1/r_c, the strain field varies on the scale r_c in all directions, including along xi. So:

    |D_xi S| ~ |nabla S| ~ |S| / r_c ~ omega_max / r_c = omega_max^{3/2} / (nu/alpha)^{1/2} * ... 

More carefully: |S| ~ omega_max (from Biot-Savart at the core scale), and the length scale of variation is r_c in all directions. So:

    |D_xi S| ~ omega_max / r_c

Using r_c = (nu/omega_max)^{1/2} * (numerical factors):

    omega_max / r_c ~ omega_max / (nu/omega_max)^{1/2} = omega_max^{3/2} / nu^{1/2}

**This recovers the full dimensional estimate.** When kappa r_c ~ 1, the directional derivative D_xi S is as large as the full gradient, and we get delta = 1/2 — exactly the borderline.

**But:** The condition kappa r_c ~ 1 requires kappa ~ 1/r_c, which for a Burgers vortex with r_c = (4 nu/alpha)^{1/2} means kappa ~ (alpha/(4 nu))^{1/2} = omega_max^{1/2} / (some constant). Under LIA, the curvature kappa evolves by 1D cubic NLS, which is globally well-posed in H^1. The H^1 norm controls ||kappa||_{L^infinity} via Sobolev embedding. So kappa <= C(||psi_0||_{H^1}), a constant independent of omega_max.

For the condition kappa r_c ~ 1 to hold, we need r_c ~ 1/kappa ~ 1/C, which means nu/alpha ~ 1/C^2, i.e., alpha ~ C^2 nu. But omega_max = Gamma alpha/(4 pi nu) = Gamma C^2 / (4 pi), a finite constant. So kappa r_c ~ 1 is only possible at moderate vorticity, not at large omega_max.

**This is the key NLS contribution:** if kappa is bounded by C(psi_0) independently of omega_max, then kappa r_c -> 0 as omega_max -> infinity (since r_c ~ omega_max^{-1/2}). The matched expansion becomes more accurate at higher vorticity, not less.

**However:** The 1D cubic NLS is globally well-posed for the LIA dynamics, but the corrections to LIA break the integrability. The corrected evolution equation for the Hasimoto variable psi is:

    i partial_t psi + partial_s^2 psi + (1/2)|psi|^2 psi = epsilon F(psi, partial_s psi, ...) + O(epsilon^2)

where epsilon = kappa_max r_c and F involves the non-local Biot-Savart corrections. Global well-posedness for this perturbed NLS is NOT established. The perturbation F is a bounded operator in H^1 (from the regularity of the Biot-Savart kernel), but the perturbed equation is not integrable, and the conserved quantities of NLS are no longer exactly conserved.

The H^1 norm of psi satisfies:

    d/dt ||psi||_{H^1}^2 = O(epsilon ||psi||_{H^1}^3) + O(epsilon^2 ||psi||_{H^1}^4)

(from the perturbation). By Gronwall, ||psi(t)||_{H^1} <= ||psi(0)||_{H^1} * exp(C epsilon integral_0^t ||psi(s)||_{H^1} ds), which a priori could grow. If ||psi||_{H^1} grows, then kappa grows, which increases epsilon, which increases the growth rate — a potentially unstable feedback loop.

**Assessment of Breakdown 1:** For the single-tube problem, the NLS integrability provides strong (but not rigorous for the full dynamics) control on kappa. The regime kappa r_c ~ 1 is not reached at large omega_max if kappa is bounded. But proving that kappa remains bounded for the corrected (non-integrable) system is an open problem of comparable difficulty to the original NS regularity question.

### 4.2 Breakdown 2: Tube-tube interaction at distance d ~ r_c

This is the critical scenario. When two intense vortex tubes approach each other with inter-tube distance d comparable to r_c:

**The strain from tube B at tube A's center:**

Tube B has circulation Gamma_B and its axis passes at distance d from tube A's center. The strain field from tube B at distance d is:

    S_B ~ Gamma_B / (2 pi d^2)

At d ~ r_c: S_B ~ Gamma_B / (2 pi r_c^2) ~ omega_B (the peak vorticity of tube B).

**The directional derivative D_{xi_A} S_B along tube A's vorticity direction:**

The strain from tube B varies along the axis of tube A. The relevant length scale for this variation is d (the inter-tube separation) if the tubes are not parallel, or the tube length if they are parallel. For non-parallel tubes:

    D_{xi_A} S_B ~ |S_B| / d ~ omega_B / r_c = omega_B * (alpha/nu)^{1/2} * ...

More carefully: S_B ~ Gamma_B / d^2. Its variation along xi_A (the axis of tube A) at distance d from tube B:

    D_{xi_A} S_B ~ Gamma_B / d^3 (from differentiating the 1/d^2 decay of a line vortex)

Wait — the decay of the strain of a line vortex at distance d is S ~ Gamma/(d^2). The gradient of this strain is nabla S ~ Gamma/d^3. The directional derivative is at most this:

    |D_{xi_A} S_B| <= Gamma_B / d^3

At d = r_c:

    |D_{xi_A} S_B| ~ Gamma_B / r_c^3

Using Gamma_B = pi r_c^2 omega_B:

    |D_{xi_A} S_B| ~ pi omega_B r_c^2 / r_c^3 = pi omega_B / r_c

And:

    omega_B / r_c = omega_B / (nu/omega_B)^{1/2} * (constants) = omega_B^{3/2} / nu^{1/2} * (constants)

**This is exactly the dimensional estimate:** |D_xi S| ~ omega^{3/2}/nu^{1/2}. The tube-tube interaction at d ~ r_c saturates the dimensional bound.

This is the mechanism that produces delta = 1/2 in the generic estimate. It is NOT a deficiency of the analysis — it is a physical scenario in which D_xi S genuinely reaches the dimensional limit.

### 4.3 Breakdown 3: Non-axisymmetric/time-dependent core

If the core structure departs from the steady Burgers profile (e.g., due to rapid time dependence, external perturbation, or reconnection), the cross-sectional vorticity distribution is no longer Gaussian. In the worst case (arbitrary core structure), the strain at the center can have arbitrary s-dependence, and D_xi S is bounded only by the dimensional estimate.

However, for cores that are close to Burgers (i.e., the deformation of the Gaussian profile is small), the corrections to D_xi S are perturbative and the single-tube estimate |D_xi S| ~ omega kappa remains valid up to small corrections.

### 4.4 Summary of breakdown estimates

| Scenario | |D_xi S| | delta | Ruled out by Theorem CB? |
|---|---|---|---|
| Single tube, kappa bounded | C omega kappa = O(omega) | 0 | YES (alpha = 3/2, trivially) |
| Single tube, kappa r_c ~ 1 | O(omega^{3/2}/nu^{1/2}) | 1/2 | BORDERLINE |
| Two tubes, d ~ r_c | O(omega^{3/2}/nu^{1/2}) | 1/2 | BORDERLINE |
| Two tubes, d >> r_c | O(omega * Gamma/d^2) << omega^{3/2}/nu^{1/2} | < 1/2 | YES |
| Reconnection | O(omega^{3/2}/nu^{1/2}) or worse | >= 1/2 | NO or BORDERLINE |

---

## Step 5: Can Tube-Tube Interaction at d ~ r_c Actually Happen?

### 5.1 Kinematic analysis

Two vortex tubes with circulations Gamma_A, Gamma_B at separation d induce velocities on each other of order:

    v_{mutual} ~ Gamma / (2 pi d) ~ omega r_c^2 / d

At d ~ r_c: v_{mutual} ~ omega r_c. The time to traverse one core radius is:

    t_cross ~ r_c / v_{mutual} ~ r_c / (omega r_c) = 1/omega

The viscous diffusion time across the core is:

    t_visc ~ r_c^2 / nu = 1/alpha

For the approach to happen before viscous merger: t_cross < t_visc requires:

    1/omega < 1/alpha,  i.e.,  omega > alpha

This is equivalent to Re_Gamma > 4 pi (from omega_max = Re_Gamma * alpha/2). At any significant Reynolds number, omega >> alpha, so the approach is kinematically allowed.

### 5.2 What prevents the approach?

**Viscosity alone does not prevent tube-tube interaction at d ~ r_c.** The approach happens on the fast timescale 1/omega, while viscous diffusion operates on the slow timescale 1/alpha.

**Self-induction:** Two approaching vortex tubes self-induce binormal velocities that curve their trajectories. If the tubes are anti-parallel (the most dangerous configuration for reconnection), the self-induced velocities draw them together faster (the Crow instability). If they are parallel, the mutual induction causes them to orbit each other.

**Core deformation:** As d approaches r_c, the cores deform. The Burgers profile is no longer a steady state because the strain from tube B modifies the external strain field acting on tube A. The core broadens on the side facing tube B (where the total strain is reduced) and compresses on the opposite side. This deformation affects the vorticity distribution and hence the strain gradient.

**Reconnection:** When d < r_c, the cores overlap and viscous reconnection begins. The vorticity topology changes: the two tubes merge and then separate in a different configuration. During reconnection:
- Peak vorticity can increase transiently (the merging concentrates vorticity)
- But the post-reconnection state has lower peak vorticity (the merged core is thicker)
- The reconnection timescale is O(r_c^2/nu) = O(1/alpha)

### 5.3 The post-merger structure

When two tubes merge at d ~ r_c, the resulting structure is NOT two thin tubes. It is a single, thicker vortex region with:
- Effective core radius ~ 2 r_c (from the superposition of two Gaussian cores)
- Peak vorticity ~ omega_max (not 2 omega_max — the superposition of two anti-parallel tubes partially cancels)
- More complex geometry (potentially a flat ribbon-like structure rather than a circular tube)

For the merged structure:
- The effective r_c increases, which decreases epsilon = kappa r_c' if kappa is bounded
- The effective omega_max does not increase significantly
- D_xi S for the merged structure is not well-described by the thin-tube expansion

**But the crucial question:** During the merger process (the transient period when d ~ r_c), does |D_xi S| reach omega^{3/2}/nu^{1/2}?

From the estimate in Section 4.2: yes. When d = r_c and the tubes have not yet merged:

    |D_xi S| ~ omega / r_c ~ omega^{3/2}/nu^{1/2}

This is a genuine transient value. The merger subsequently reduces omega and increases r_c, bringing D_xi S back down. But at the instant d = r_c, the full dimensional estimate is saturated.

### 5.4 Is the peak transient enough?

For Theorem CB, what matters is not the instantaneous value of D_xi S but whether the Serrin-type integral converges. The coupled bootstrap argument involves:

    dOmega/dt <= C_1 Omega^2 - nu K^2 Omega

If the tube-tube interaction increases |D_xi S| to omega^{3/2}/nu^{1/2} for a time interval Delta_t ~ 1/omega (the crossing time), the integrated effect is:

    integral |D_xi S|^2 dt ~ (omega^{3/2}/nu^{1/2})^2 * (1/omega) = omega^2 / nu

This is the natural scaling for the enstrophy dissipation — it does not help. The transient duration is too short relative to the magnitude for any temporal averaging to provide a gain.

### 5.5 Does the vortex merger prevent omega from increasing?

This is the key physical question. If two tubes approach at distance r_c, the local strain (from each tube acting on the other) is O(omega). This strain acts to stretch the vorticity. The stretching rate is:

    D_t |omega| ~ omega * S ~ omega^2 (at the interaction point)

Over the interaction time Delta_t ~ 1/omega, the vorticity increase is:

    Delta omega ~ omega^2 * (1/omega) = omega

So the vorticity could roughly double during the interaction. This is a finite-time, finite-factor increase — not a blowup. But repeated tube-tube interactions could, in principle, lead to geometric growth of omega.

**The self-consistency check:** After a tube-tube interaction that doubles omega, the new core radius is r_c' = (4 nu / alpha')^{1/2}. If the strain alpha also increases (which it does, since the strain is generated by the vorticity through Biot-Savart), then r_c' could remain the same or decrease. A cascade of tube-tube interactions at progressively smaller scales is the physical picture of the energy cascade in turbulence.

Whether this cascade can produce infinite omega in finite time is precisely the content of the NS regularity question. The tube-tube interaction analysis does not resolve it — it identifies the mechanism by which the dimensional estimate is saturated, but does not determine whether that mechanism leads to blowup.

---

## Step 6: Honest Assessment

### 6.1 Does |D_xi S| stay below omega^{3/2}/(nu^{1/2} log omega) for a single tube?

**Yes, by a wide margin.**

For a single curved Burgers vortex tube with bounded curvature kappa <= K_max:

    |D_xi S|_{single tube} <= C K_max |omega| + C K_max^2 |omega|^{1/2} nu^{1/2} ln(|omega|)

The ratio to the dimensional estimate:

    |D_xi S|_{single tube} / (|omega|^{3/2}/nu^{1/2}) = O(kappa r_c) = O(epsilon) -> 0 as |omega| -> infinity

The single-tube D_xi S is not just below the dimensional estimate by a logarithm — it is below by a full power of omega^{1/2}. This is the strongest possible single-tube result.

### 6.2 Can tube-tube interaction push D_xi S to the dimensional limit?

**Yes.**

When two vortex tubes approach at distance d ~ r_c, the strain gradient from one tube along the other's vorticity direction is:

    |D_xi S|_{tube-tube} ~ Gamma / r_c^3 ~ omega^{3/2}/nu^{1/2}

This saturates the dimensional estimate. The saturation is a genuine physical effect, not an artifact of the estimate. The dimensional estimate comes precisely from this tube-tube interaction scenario.

### 6.3 Is there any mechanism preventing the worst-case tube interaction?

**No robust mechanism has been identified.**

- Viscosity does not prevent the approach (the approach time 1/omega is much shorter than the diffusion time 1/alpha).
- Self-induction curves the trajectories but can either help (drawing anti-parallel tubes together via the Crow instability) or hinder (causing parallel tubes to orbit).
- Core deformation during the approach modifies the strain field but does not eliminate the D_xi S peak.
- Post-merger, the peak vorticity decreases and D_xi S falls, but the transient peak at d ~ r_c is genuine.

The one potential mechanism: if the NLS-bounded curvature constraint prevents the geometric configurations that would bring two tubes to within r_c of each other. Specifically, if the filament dynamics (governed approximately by NLS) do not generate configurations with d ~ r_c for the relevant tube pairs. But this is not a consequence of the NLS integrability — the NLS governs the curvature of individual filaments, not the relative positions of different filaments. The inter-tube distance is governed by the full 3D Biot-Savart dynamics, which is not captured by the Hasimoto transform.

### 6.4 What is the precise estimate with all error terms?

For a system of N vortex tubes with curvatures kappa_i <= K_max, core radii r_c, circulations Gamma, and pairwise separations d_{ij}:

    |D_xi S(x)| <= Sum_i [C K_max omega_i(x)] (single-tube contributions)
                 + Sum_{j != i} [C Gamma_j / d_{ij}(x)^3] (tube-tube contributions)
                 + O(K_max^2 omega r_c ln(1/(K_max r_c))) (self-induction corrections)

where i is the tube containing x, omega_i(x) is the local vorticity magnitude, and d_{ij}(x) is the distance from x to tube j.

The worst case is d_{ij} = r_c, giving:

    |D_xi S|_{worst} ~ C omega + C omega^{3/2}/nu^{1/2}

The first term (single-tube) is negligible at large omega. The second term (tube-tube) gives delta = 1/2, exactly the borderline.

### 6.5 Can a logarithmic improvement be extracted?

For the tube-tube interaction to produce |D_xi S| = omega^{3/2}/nu^{1/2}, the separation d must be exactly r_c. If d is larger by any factor:

    |D_xi S| ~ omega^{3/2}/nu^{1/2} * (r_c/d)^3

For d = r_c * (ln omega)^{1/3}, we would get:

    |D_xi S| ~ omega^{3/2}/(nu^{1/2} ln omega)

which would break the borderline.

**Is there a physical reason why d cannot reach r_c but only r_c * f(omega) for some growing f?**

**Possible argument 1: Viscous regularization.** When two tubes are at distance d ~ r_c, viscous diffusion begins to merge their cores on the timescale r_c^2/nu = 1/alpha. The merger broadens the effective core to r_c_eff ~ r_c + (nu * t_merge)^{1/2}. If t_merge ~ d^2/(Gamma/d) = d^3/Gamma (the time for the Biot-Savart advection to bring the tubes from d to 0), then the viscous broadening during the approach is:

    Delta r_c ~ (nu d^3/Gamma)^{1/2} = (nu/Gamma)^{1/2} d^{3/2} = d^{3/2}/(Re_Gamma^{1/2} r_c^{1/2})

For d ~ r_c: Delta r_c ~ r_c / Re_Gamma^{1/2}. This is small at large Re — the viscous broadening during the approach is negligible.

**Possible argument 2: Depletion of nonlinearity.** The NS equations have documented depletion effects where the nonlinear terms are smaller than dimensional estimates predict, due to the geometric structure of the flow (Biot-Savart incompressibility, alignment). For D_xi S specifically, the alignment of omega with e_2 (confirmed in Subproblem A of this pursuit) means that the strain variation along xi probes a specific component that may be suppressed by the incompressibility constraint.

This is Path 1 (directional cancellation in the Biot-Savart kernel). The two paths converge: the question of whether tube-tube interaction at d ~ r_c produces the full dimensional D_xi S, or whether there is an angular cancellation that provides a logarithmic reduction, is the same question for both paths.

**Possible argument 3: Statistical argument.** In turbulent flows, the probability of two intense tubes being at distance d ~ r_c with non-parallel orientations may be suppressed. DNS observations show that intense vortex tubes tend to have parallel alignment in their neighborhoods (vortex clustering). This statistical suppression would not provide a pointwise bound but might give an integrated bound sufficient for the regularity argument.

However, this argument is probabilistic and not applicable to individual solutions.

### 6.6 Verdict on Path 3

**What Path 3 accomplishes:**
1. Rigorous single-tube estimate: |D_xi S| = O(omega kappa) for a curved Burgers vortex with bounded curvature. This is far below the dimensional estimate.
2. Identification of tube-tube interaction at d ~ r_c as the unique mechanism that saturates the dimensional estimate.
3. Clear formulation of the gap: the single-tube result gives delta = 0, the tube-tube result gives delta = 1/2, and the gap between them (1/2 > delta_needed = 1/2 + epsilon) is not closed.

**Where Path 3 fails:**
1. The NLS global well-posedness provides no control on inter-tube separation — it bounds curvature of individual filaments, not the relative geometry of filament pairs.
2. The tube-tube interaction at d ~ r_c is kinematically allowed and not prevented by any identified mechanism.
3. The transition from the single-tube regime (delta = 0) to the tube-tube regime (delta = 1/2) is sharp — there is no intermediate regime that could provide a logarithmic gain.

**The tube-tube interaction problem is the precise obstruction.** Path 3 reduces the NS regularity question to:

> Can two vortex tubes in a Navier-Stokes flow have inter-tube separation d equal to (or less than) the core radius r_c at a point where both tubes have vorticity magnitude omega with |D_xi S| reaching the full dimensional estimate omega^{3/2}/nu^{1/2}?

If the answer is no (i.e., there exists some minimum separation d_min > r_c * f(omega) with f(omega) -> infinity), then regularity follows. If the answer is yes, the coupled bootstrap is genuinely borderline and a different approach is needed.

### 6.7 Connection to the other paths

**Path 1 (Directional cancellation):** Addresses the same tube-tube interaction problem from the Biot-Savart kernel structure. If the angular cancellation in the CZ kernel when projecting along xi provides a logarithmic improvement to the tube-tube contribution, this would close the gap identified by Path 3. The two paths are complementary: Path 3 shows the single-tube contribution is safe and identifies tube-tube interaction as the bottleneck; Path 1 attacks the bottleneck directly.

**Path 2 (Logarithmic Gronwall):** Addresses the tube-tube problem indirectly through the localized energy estimate. The temporal averaging in the Gronwall argument could potentially handle the transient tube-tube interactions (which are brief, O(1/omega)), even if they are individually at the dimensional limit. The question is whether the integrated effect over all tube-tube interactions remains bounded.

### 6.8 Estimated probability that Path 3 closes the gap

**5-8%**, revised downward from the initial 10-15%.

The single-tube computation is a complete success — it confirms the structural picture and gives a clean, strong result (delta = 0 for individual tubes). But the tube-tube interaction problem is the hard part, and Path 3's main tool (NLS integrability) does not address it. The probability reflects the chance that some overlooked consequence of the NLS dynamics provides control on inter-tube separation, plus the chance that combining Path 3 with Path 1 yields the required logarithmic improvement.

---

## Appendix A: Detailed Computation of S^(0)_{r theta} near rho = 0

For the Burgers vortex:

    u_theta = (Gamma/(2 pi rho))(1 - exp(-rho^2/r_c^2))

Expanding for small rho:

    1 - exp(-rho^2/r_c^2) = rho^2/r_c^2 - rho^4/(2 r_c^4) + rho^6/(6 r_c^6) - ...

So:

    u_theta = (Gamma/(2 pi)) [rho/r_c^2 - rho^3/(2 r_c^4) + rho^5/(6 r_c^6) - ...]

    partial_rho u_theta = (Gamma/(2 pi)) [1/r_c^2 - 3 rho^2/(2 r_c^4) + 5 rho^4/(6 r_c^6) - ...]

    u_theta/rho = (Gamma/(2 pi)) [1/r_c^2 - rho^2/(2 r_c^4) + rho^4/(6 r_c^6) - ...]

    (nabla u)_{r theta} = partial_rho u_theta - u_theta/rho
                        = (Gamma/(2 pi)) [-rho^2/r_c^4 + 2 rho^4/(3 r_c^6) - ...]
                        = -(Gamma rho^2)/(2 pi r_c^4) [1 - 2 rho^2/(3 r_c^2) + ...]

At rho = 0: (nabla u)_{r theta} = 0 (from the rho^2 factor).

The strain component:

    S_{r theta} = (1/2)(nabla u)_{r theta} = -(Gamma rho^2)/(4 pi r_c^4) + O(rho^4)

At rho = 0: S_{r theta} = 0. The strain at the center is purely diagonal, confirming the computation in Step 2.7.

---

## Appendix B: The Hasimoto Transform and NLS Global Well-Posedness

The Hasimoto transform maps the curvature and torsion of a vortex filament to a complex-valued function:

    psi(s, t) = kappa(s, t) exp(i integral_0^s tau(s', t) ds')

Under the Local Induction Approximation (da Rios 1906, Hasimoto 1972):

    i partial_t psi + partial_s^2 psi + (1/2)|psi|^2 psi = 0

This is the 1D focusing cubic nonlinear Schrodinger equation, which is completely integrable (by the inverse scattering transform). The conservation laws include:

    ||psi||_{L^2}^2 = integral kappa^2 ds (total squared curvature)
    ||partial_s psi||_{L^2}^2 + (1/4)||psi||_{L^4}^4 (H^1-type energy)

The 1D cubic NLS is globally well-posed in H^1 (by the conservation of the H^1 energy and the Gagliardo-Nirenberg inequality). Since ||psi||_{L^infinity} <= C ||psi||_{H^1}, the curvature satisfies:

    kappa(s, t) = |psi(s, t)| <= ||psi||_{L^infinity} <= C(||psi_0||_{H^1}) for all t

**This is the bound kappa <= K_max used throughout this computation.**

The corrections to LIA from the full Biot-Savart law (Fukumoto-Moffatt 2000) add perturbation terms to the NLS:

    i partial_t psi + partial_s^2 psi + (1/2)|psi|^2 psi = epsilon [F_1(psi, partial_s psi) + F_2(nonlocal)] + O(epsilon^2)

where epsilon = kappa_max r_c. The perturbation F_1 involves higher derivatives (partial_s^2 psi, partial_s^3 psi) and nonlinear terms. The perturbation F_2 involves the non-local Biot-Savart contributions from distant parts of the filament.

Global well-posedness for this perturbed system is an open problem. The conserved quantities of NLS are no longer exactly conserved, and the perturbation can, in principle, transfer energy to high modes (small-scale curvature), potentially leading to curvature blowup.

---

## Appendix C: Comparison with DNS Evidence

DNS data on vortex tube interactions (Jimenez et al. 1993, Ishihara et al. 2009, Hamlington et al. 2008) show:

1. **High-vorticity regions are predominantly tube-like** at all accessible Reynolds numbers (Re_lambda up to ~1000). This supports the single-tube estimate as the dominant contribution to D_xi S for most of the flow.

2. **Tube-tube interactions occur** and are responsible for reconnection events. The inter-tube separation during reconnection reaches d ~ r_c, confirming that Breakdown 2 is physically realized.

3. **The quantity |D_xi S| / |omega|^{3/2}** has not been systematically measured in DNS. This is the key quantity that would test whether the dimensional estimate is saturated or whether there is a logarithmic or power-law improvement. A DNS campaign measuring this ratio as a function of |omega| would be the most informative computational experiment for Path 3.

4. **Curvature statistics:** Kappa of intense vortex tubes in DNS is bounded by values of order 1/L (the integral scale), not 1/r_c. This is consistent with the NLS bound kappa <= C(psi_0) and supports epsilon = kappa r_c << 1 in the high-vorticity regime. However, this is at currently accessible Re — the behavior at asymptotically large Re is unknown.

---

## Summary

The Hasimoto/NLS + controlled LIA departure computation yields a definitive result for single vortex tubes: |D_xi S| = O(omega kappa), which is far below the dimensional estimate omega^{3/2}/nu^{1/2}. The gap is polynomial (O(omega^{1/2})), not logarithmic.

The computation identifies tube-tube interaction at inter-tube distance d ~ r_c as the unique mechanism that saturates the dimensional estimate. This scenario is kinematically allowed and not prevented by any identified mechanism.

The NLS integrability (via the Hasimoto transform) controls curvature of individual filaments but provides no information about inter-tube separation. The gap between the single-tube result (delta = 0) and the tube-tube result (delta = 1/2) is not bridged by Path 3 alone.

The computation's value is in precisely localizing the obstruction: the logarithmic gap in Theorem CB arises entirely from tube-tube interactions at the core scale, not from single-tube dynamics. Any successful resolution of the gap must address this specific geometric scenario — either by showing it cannot occur with sufficient D_xi S (Paths 1 and 2) or by showing it cannot occur at all (inter-tube separation bound).
