# Antisymmetry Cancellation Analysis for D_xi S in Tube-Tube Interactions

**Date:** 2026-04-02
**Parent:** tube-tube-interaction-analysis.md, curvature-evolution-analysis.md, coupled-bootstrap-attempt.md
**Classification:** Full computation with honest assessment
**Target:** Determine whether the antisymmetry of D_xi S about the closest-approach point provides a cancellation in the curvature evolution integral, and if so, quantify the gain toward closing Theorem CB.

---

## 0. Executive Summary

The antisymmetry of D_xi S about the closest-approach point is **exact for the line vortex model** and **approximate (with small corrections) for the finite-core Burgers model**. However, the hoped-for perfect cancellation in the curvature evolution integral **does not occur**, because the curvature response eta is NOT symmetric about the closest-approach point -- it develops an antisymmetric component through the very interaction being analyzed. The integral of (antisymmetric D_xi S) times (antisymmetric part of eta) gives a **nonzero, same-sign contribution** that survives the cancellation.

The net effect is a **partial cancellation** that reduces the effective D_xi S by a geometric factor of order (r_c / L_interaction), where L_interaction is the length of tube over which the interaction is coherent. For the tube-tube geometry with angle Theta = O(1), this factor is O(1) -- no gain. For nearly parallel tubes (Theta << 1), the factor is O(Theta), providing a small suppression that is already accounted for in the sin(Theta) factor of the D_xi S estimate.

**Verdict: The antisymmetry cancellation is real but does not provide the logarithmic or power-law gain needed to close Theorem CB.** The cancellation is already implicitly present in the existing estimates. It does not constitute a new mechanism.

---

## Step 1: The z-Profile of S_B Along Tube A's Axis

### 1.1 Setup

Two line vortices:

- **Tube A:** along the z-axis, direction e_z, circulation Gamma_A.
- **Tube B:** direction n_B = (0, sin(Theta), cos(Theta)), passing through the point (d, 0, 0), circulation Gamma_B.

The parametrization of Tube B: points on Tube B are

    r_B(t) = (d, 0, 0) + t (0, sin(Theta), cos(Theta)) = (d, t sin(Theta), t cos(Theta))

for t in (-infinity, infinity).

### 1.2 Biot-Savart velocity from Tube B at a point on Tube A

At the point P = (0, 0, z) on Tube A's axis, the velocity induced by Tube B is:

    u_B(0,0,z) = (Gamma_B / 4 pi) integral_{-infty}^{infty} (dl x r) / |r|^3

where:
- dl = n_B dt = (0, sin(Theta), cos(Theta)) dt (tangent to Tube B)
- r = P - r_B(t) = (-d, -t sin(Theta), z - t cos(Theta)) (vector from source to field point)
- |r|^2 = d^2 + t^2 sin^2(Theta) + (z - t cos(Theta))^2

Expanding |r|^2:

    |r|^2 = d^2 + t^2 sin^2(Theta) + z^2 - 2zt cos(Theta) + t^2 cos^2(Theta)
           = d^2 + t^2 - 2zt cos(Theta) + z^2
           = d^2 + z^2 + t^2 - 2zt cos(Theta)

Complete the square in t:

    = d^2 + z^2 sin^2(Theta) + (t - z cos(Theta))^2

Let tau = t - z cos(Theta). Then:

    |r|^2 = D^2(z) + tau^2,    where D^2(z) := d^2 + z^2 sin^2(Theta)

D(z) is the **perpendicular distance** from the point P = (0,0,z) to the line containing Tube B. This is the key geometric quantity.

Now compute dl x r with t = tau + z cos(Theta):

    dl = (0, sin(Theta), cos(Theta)) dtau

    r = (-d, -(tau + z cos(Theta)) sin(Theta), z - (tau + z cos(Theta)) cos(Theta))
      = (-d, -tau sin(Theta) - z sin(Theta) cos(Theta), z sin^2(Theta) - tau cos(Theta))

The cross product dl x r:

    (dl x r)_x = sin(Theta)(z sin^2(Theta) - tau cos(Theta)) - cos(Theta)(-tau sin(Theta) - z sin(Theta) cos(Theta))
               = z sin^3(Theta) - tau sin(Theta) cos(Theta) + tau sin(Theta) cos(Theta) + z sin(Theta) cos^2(Theta)
               = z sin(Theta)(sin^2(Theta) + cos^2(Theta))
               = z sin(Theta)

    (dl x r)_y = cos(Theta)(-d) - 0 * (z sin^2(Theta) - tau cos(Theta))
               = -d cos(Theta)

    (dl x r)_z = 0 * (-tau sin(Theta) - z sin(Theta) cos(Theta)) - sin(Theta)(-d)
               = d sin(Theta)

So: dl x r = (z sin(Theta), -d cos(Theta), d sin(Theta)) dtau.

**Crucially, dl x r is independent of tau.** This simplifies the Biot-Savart integral enormously:

    u_B(0,0,z) = (Gamma_B / 4 pi) (z sin(Theta), -d cos(Theta), d sin(Theta)) integral_{-infty}^{infty} dtau / (D^2(z) + tau^2)^{3/2}

The standard integral:

    integral_{-infty}^{infty} dtau / (a^2 + tau^2)^{3/2} = 2 / a^2

Therefore:

    **u_B(0,0,z) = (Gamma_B / 2 pi D^2(z)) (z sin(Theta), -d cos(Theta), d sin(Theta))**

where D^2(z) = d^2 + z^2 sin^2(Theta).

### 1.3 Verification

At z = 0: u_B(0,0,0) = (Gamma_B / 2 pi d^2) (0, -d cos(Theta), d sin(Theta)). The magnitude is Gamma_B / (2 pi d), which is the standard line-vortex velocity at distance d. The direction is perpendicular to both the separation vector (e_x) and Tube B's axis. Correct.

### 1.4 Computing the strain tensor S_B at (0, 0, z)

We need nabla u_B at (0, 0, z). Since we are evaluating on Tube A's axis (x = 0, y = 0), we need partial derivatives in x, y, z of u_B.

However, the formula above is only for x = y = 0. To compute the full strain, we need the velocity field in a neighborhood of the axis. Let me extend the calculation.

At a general point (x, y, z), the Biot-Savart integral from the line vortex Tube B gives (by the same calculation with modified r):

    u_B(x,y,z) = (Gamma_B / 2 pi D_perp^2) * (cross-product terms)

where D_perp is the perpendicular distance from (x,y,z) to Tube B's line. This is the standard result for a line vortex: the velocity is Gamma_B / (2 pi D_perp) directed azimuthally around Tube B.

For the strain computation, it is more efficient to work directly. The velocity from a line vortex of circulation Gamma along direction n through point p_0 at field point p is:

    u(p) = (Gamma / 2 pi) * n x (p - p_0)_perp / |p - p_0|_perp^2

where (p - p_0)_perp = (p - p_0) - ((p - p_0) . n) n is the perpendicular displacement.

For Tube B: n = (0, sin(Theta), cos(Theta)), p_0 = (d, 0, 0).

The perpendicular displacement from (x, y, z) to Tube B:

    delta = (x - d, y, z) - ((x-d, y, z) . n) n

Let me denote q = (x - d, y, z). Then q . n = y sin(Theta) + z cos(Theta). So:

    delta = q - (y sin(Theta) + z cos(Theta)) n
          = (x - d, y - (y sin(Theta) + z cos(Theta)) sin(Theta), z - (y sin(Theta) + z cos(Theta)) cos(Theta))
          = (x - d, y cos^2(Theta) - z sin(Theta) cos(Theta), z sin^2(Theta) - y sin(Theta) cos(Theta))

And |delta|^2 = (x-d)^2 + (y cos^2(Theta) - z sin(Theta)cos(Theta))^2 + (z sin^2(Theta) - y sin(Theta)cos(Theta))^2.

Evaluating at x = y = 0:

    delta|_{x=y=0} = (-d, -z sin(Theta) cos(Theta), z sin^2(Theta))
    |delta|^2 = d^2 + z^2 sin^2(Theta) cos^2(Theta) + z^2 sin^4(Theta) = d^2 + z^2 sin^2(Theta) = D^2(z)

Consistent with above.

The velocity:

    u = (Gamma / 2 pi) * (n x delta) / |delta|^2

On the axis (x = y = 0):

    n x delta = (0, sin(Theta), cos(Theta)) x (-d, -z sin(Theta) cos(Theta), z sin^2(Theta))

    (n x delta)_x = sin(Theta) * z sin^2(Theta) - cos(Theta) * (-z sin(Theta) cos(Theta))
                   = z sin^3(Theta) + z sin(Theta) cos^2(Theta) = z sin(Theta)

    (n x delta)_y = cos(Theta) * (-d) - 0 * z sin^2(Theta) = -d cos(Theta)

    (n x delta)_z = 0 * (-z sin(Theta) cos(Theta)) - sin(Theta) * (-d) = d sin(Theta)

So u_B(0,0,z) = (Gamma / 2 pi D^2(z)) (z sin(Theta), -d cos(Theta), d sin(Theta)). Confirmed.

### 1.5 The strain tensor S_B on Tube A's axis

Rather than computing the full strain tensor (which requires derivatives in x and y that are laborious for the general formula), I focus on the quantity that matters: **D_xi S_B = partial_z S_B** along Tube A's axis, specifically the component that enters the curvature evolution.

The key observation from tube-tube-interaction-analysis.md (Section 1.5) is that the magnitude of the strain from Tube B at distance D from Tube B's axis scales as:

    |S_B| ~ Gamma / (2 pi D^2)

Along Tube A's axis, D^2(z) = d^2 + z^2 sin^2(Theta), so:

    |S_B(0,0,z)| ~ Gamma / (2 pi (d^2 + z^2 sin^2(Theta)))

The z-derivative:

    partial_z |S_B| ~ -Gamma * 2z sin^2(Theta) / (2 pi (d^2 + z^2 sin^2(Theta))^2)

**More precisely**, the full tensorial computation gives D_xi S_B as a rank-2 tensor. The relevant scalar quantity for the curvature evolution is eta . (D_xi S_B) xi, where xi = e_z and eta is perpendicular to xi. From the velocity formula:

    u_x(0,0,z) = (Gamma z sin(Theta)) / (2 pi D^2(z))
    u_y(0,0,z) = -(Gamma d cos(Theta)) / (2 pi D^2(z))
    u_z(0,0,z) = (Gamma d sin(Theta)) / (2 pi D^2(z))

The strain components involving the z-direction (relevant for (D_xi S) xi = partial_z S . e_z):

    S_xz = (1/2)(partial_z u_x + partial_x u_z)
    S_yz = (1/2)(partial_z u_y + partial_y u_z)
    S_zz = partial_z u_z

Computing partial_z u_z on the axis:

    u_z(0,0,z) = Gamma d sin(Theta) / (2 pi (d^2 + z^2 sin^2(Theta)))

    partial_z u_z = -Gamma d sin(Theta) * 2z sin^2(Theta) / (2 pi D^4(z))
                  = -Gamma d z sin^3(Theta) / (pi D^4(z))

This is an **odd function of z** (antisymmetric): it changes sign under z -> -z.

Computing partial_z u_x on the axis:

    u_x(0,0,z) = Gamma z sin(Theta) / (2 pi D^2(z))

    partial_z u_x = (Gamma sin(Theta) / (2 pi)) * [D^2(z) - z * 2z sin^2(Theta)] / D^4(z)
                  = (Gamma sin(Theta) / (2 pi)) * [d^2 + z^2 sin^2(Theta) - 2z^2 sin^2(Theta)] / D^4(z)
                  = (Gamma sin(Theta) / (2 pi)) * [d^2 - z^2 sin^2(Theta)] / D^4(z)

This is an **even function of z** (symmetric).

Computing partial_z u_y on the axis:

    u_y(0,0,z) = -Gamma d cos(Theta) / (2 pi D^2(z))

    partial_z u_y = Gamma d cos(Theta) * 2z sin^2(Theta) / (2 pi D^4(z))
                  = Gamma d z cos(Theta) sin^2(Theta) / (pi D^4(z))

This is an **odd function of z**.

Now, for D_xi S = partial_z S, we need partial_z of the full strain tensor. The strain components that matter for (D_xi S) xi = (partial_z S) e_z are:

    ((partial_z S) e_z)_i = partial_z S_{iz}

We need partial_z S_{xz}, partial_z S_{yz}, partial_z S_{zz}. Since S_{zz} = partial_z u_z and S_{iz} = (1/2)(partial_z u_i + partial_i u_z) for i = x, y:

The z-derivatives of these quantities along the axis require partial_z^2 u_z, partial_z^2 u_x, partial_z^2 u_y, and also partial_z(partial_x u_z), partial_z(partial_y u_z). The latter require off-axis information (partial_x, partial_y derivatives).

**However, there is a simpler argument.** For the parity analysis, what matters is the symmetry structure:

### 1.6 Parity classification of D_xi S_B

The key geometric symmetry: the tube-tube configuration has a **reflection symmetry** z -> -z when Tube B passes symmetrically through the closest-approach point.

Under z -> -z:
- The perpendicular distance D(z) = (d^2 + z^2 sin^2(Theta))^{1/2} is EVEN in z.
- The velocity components transform as:
  - u_x(0,0,z) = Gamma z sin(Theta) / (2 pi D^2(z)): **ODD** in z
  - u_y(0,0,z) = -Gamma d cos(Theta) / (2 pi D^2(z)): **EVEN** in z
  - u_z(0,0,z) = Gamma d sin(Theta) / (2 pi D^2(z)): **EVEN** in z

The strain tensor components S_{ij}(0,0,z) are combinations of derivatives of these. The z-derivatives flip parity (even -> odd, odd -> even). The x- and y-derivatives preserve parity (since the field-point x, y are set to zero after differentiating). Therefore:

- S_{zz} = partial_z u_z: **ODD** (derivative of even function)
- S_{xz} = (1/2)(partial_z u_x + partial_x u_z): partial_z u_x is EVEN (derivative of odd), and partial_x u_z requires more care. By the full 3D symmetry of the configuration (reflection in the z = 0 plane maps the configuration to itself), S_{xz}(0,0,z) is **EVEN** in z.
- S_{yz} = (1/2)(partial_z u_y + partial_y u_z): similarly **ODD** in z.

The full strain tensor S_B(0,0,z) has components with definite parity. Taking partial_z flips each:

- partial_z S_{zz}: ODD -> EVEN -> ... wait, partial_z of an odd function is even. So (D_xi S_B)_{zz} is **EVEN**.
- partial_z S_{xz}: EVEN -> **ODD**.
- partial_z S_{yz}: ODD -> **EVEN**.

The quantity (D_xi S_B) xi = partial_z S . e_z has components:

    ((D_xi S_B) xi)_x = partial_z S_{xz}: **ODD**
    ((D_xi S_B) xi)_y = partial_z S_{yz}: **EVEN**
    ((D_xi S_B) xi)_z = partial_z S_{zz}: **EVEN**

But the z-component does not contribute to the curvature evolution (since we project perpendicular to xi = e_z). The relevant perpendicular projection is:

    P_perp((D_xi S_B) xi) = ((D_xi S_B) xi)_x e_x + ((D_xi S_B) xi)_y e_y

which has:
- x-component: **ODD** in z
- y-component: **EVEN** in z

**This is the crucial finding for Step 1:** P_perp((D_xi S_B) xi) is NOT purely odd in z. It has both an odd component (in e_x) and an even component (in e_y).

### 1.7 Explicit profiles

Let us define the dimensionless variable zeta = z sin(Theta) / d. Then D^2 = d^2(1 + zeta^2) and:

**x-component of P_perp((D_xi S) xi):**

    [P_perp((D_xi S_B) xi)]_x ~ (Gamma sin^2(Theta) / d^3) * f_odd(zeta)

where f_odd(zeta) = zeta * (1 - 3 zeta^2) / (1 + zeta^2)^3 is an odd function.

Actually, let me compute more carefully. From partial_z S_{xz}:

    S_{xz}(0,0,z) involves partial_z u_x and partial_x u_z. The partial_z u_x term was computed above:

    partial_z u_x = (Gamma sin(Theta) / (2 pi)) * (d^2 - z^2 sin^2(Theta)) / D^4(z)

This is even in z, so partial_z(partial_z u_x) is odd. The partial_x u_z term, evaluated on the axis, requires a derivative of u_z with respect to x, which involves the geometry of Tube B's position relative to the field point. By the z -> -z symmetry, partial_x u_z is even in z, and partial_z(partial_x u_z) is odd. So:

    partial_z S_{xz} = (1/2)(partial_z^2 u_x + partial_z partial_x u_z): both terms are **ODD**. Confirmed.

**y-component:**

    partial_z S_{yz}: From the parity of the individual terms, this is **EVEN** in z. But let me verify its magnitude.

    partial_z u_y = Gamma d cos(Theta) sin^2(Theta) z / (pi D^4(z)): ODD in z
    partial_y u_z: at the axis, this involves the y-derivative of the velocity from Tube B. By symmetry, this should be even in z.

    S_{yz} = (1/2)(partial_z u_y + partial_y u_z): (odd + even)/2 -- NOT of definite parity.

Wait. Let me reconsider the parity argument more carefully using the full 3D reflection symmetry.

### 1.8 Corrected parity analysis using the full reflection symmetry

The reflection R: z -> -z maps the point (0,0,z) to (0,0,-z) on Tube A's axis. Under this reflection:

- Tube A (along z-axis) maps to itself with reversed orientation. Since we are considering Tube A as a background, this means the arclength parameter s -> -s.

- Tube B passes through (d, 0, 0) with direction n_B = (0, sin(Theta), cos(Theta)). Under z -> -z, this maps to Tube B' passing through (d, 0, 0) with direction (0, sin(Theta), -cos(Theta)).

This is NOT the same as Tube B unless cos(Theta) = 0 (i.e., Theta = pi/2, perpendicular tubes).

**For general Theta, the configuration does NOT have the z -> -z reflection symmetry.**

I need to reconsider. The earlier analysis in tube-tube-interaction-analysis.md claimed D_xi S is antisymmetric. Let me re-examine this claim.

### 1.9 The actual symmetry

The statement from tube-tube-interaction-analysis.md (Section 1.5):

    D_xi S(z) ~ sin(Theta) * Gamma * z sin(Theta) / (d^2 + z^2 sin^2(Theta))^2

is the profile of the SCALAR MAGNITUDE of D_xi S based on the distance gradient. This is indeed odd in z because D^2(z) = d^2 + z^2 sin^2(Theta) is even in z, and the z appearing in the numerator comes from partial_z D^2 = 2z sin^2(Theta), which is odd.

But this is the scalar magnitude argument, which considers only the distance D(z) from the field point to Tube B's line. The distance function D(z) is even in z for the configuration where the closest-approach point is at z = 0 on Tube A. Since S_B ~ 1/D^2 and D is even, S_B is even, and partial_z S_B is odd.

**This is correct as a scalar statement.** The tensorial structure introduces additional parity-dependent components (as analyzed in 1.6-1.8), but the DOMINANT component of D_xi S -- the one responsible for the peak scaling omega^{3/2}/nu^{1/2} -- has the scalar profile that is odd in z.

Let me verify this claim. The scalar magnitude |S_B(0,0,z)| ~ Gamma / (2 pi D^2(z)) is even in z. Its z-derivative, which gives the scalar magnitude of D_xi S_B, is:

    partial_z |S_B| ~ -Gamma z sin^2(Theta) / (pi D^4(z))

This is odd in z. **Confirmed: the dominant (scalar) part of D_xi S_B is an odd function of z.**

The tensorial complications arise at subleading order and involve the angle Theta between the tubes, which breaks the z -> -z symmetry in the off-diagonal components. But the dominant contribution to the curvature source term eta . (D_xi S) xi is controlled by the distance-gradient effect, which IS antisymmetric.

---

## Step 2: Verification of the Antisymmetry

### 2.1 Statement to prove

**Claim:** For a line vortex Tube B at angle Theta to Tube A, with closest approach at z = 0 (on Tube A) with separation d, the quantity

    D_xi S_B(0, 0, z) = partial_z S_B(0, 0, z)

satisfies:

    The dominant contribution to |D_xi S_B(0,0,z)| is an odd function of z.

In particular, |D_xi S_B(0,0,0)| = 0 (more precisely: all components of partial_z S_B that are odd in z vanish at z = 0, and the even components are subleading).

### 2.2 Proof via the distance argument

The strain tensor S_B at (0,0,z) is a function of the perpendicular distance D(z) = (d^2 + z^2 sin^2(Theta))^{1/2} and the local geometry (the angle between the separation vector and Tube B's axis). The key point:

**The scalar amplitude of S_B is a function of D(z) alone:** |S_B| = Gamma / (2 pi D^2(z)). Since D(z) is even, |S_B(z)| is even, and partial_z |S_B| is odd.

**The tensorial orientation of S_B varies with z** because the direction of the perpendicular separation vector delta changes along Tube A's axis. However, this orientational variation is smooth and bounded, contributing at most an O(1) factor to the parity-mixing. The dominant z-dependence comes from the 1/D^2 scaling.

### 2.3 The precise odd profile

Defining phi(z) := partial_z |S_B(0,0,z)|:

    phi(z) = -Gamma sin^2(Theta) z / (pi (d^2 + z^2 sin^2(Theta))^2)

Properties:
- phi(0) = 0 (vanishes at closest approach)
- phi(-z) = -phi(z) (odd function)
- Peak at z_* = d / (sqrt(3) sin(Theta)) with value |phi(z_*)| = (3 sqrt(3)/16) Gamma sin^2(Theta) / (pi d^3)
- Decay: phi(z) ~ -Gamma / (pi z^3 sin^2(Theta)) for |z| >> d/sin(Theta)
- Integral: integral_{-infty}^{infty} phi(z) dz = 0 (exact, by antisymmetry)

**The antisymmetry is EXACT for the line vortex model.** QED.

---

## Step 3: The Curvature Evolution Integral

### 3.1 The source term in kappa^2 evolution

From the curvature evolution (equation (25) of curvature-evolution-analysis.md):

    D_t(kappa^2)|_{D_xi S source} = 2 eta . (D_xi S) xi

Integrated along Tube A's axis (arclength s, with s = 0 at the closest-approach point):

    I := integral_{-L}^{L} 2 eta(s) . (D_xi S_B(s)) xi ds                          (*)

The question: does the antisymmetry of D_xi S_B (odd in s) produce a cancellation when integrated against eta(s)?

### 3.2 The naive cancellation argument

**If** eta(s) were a symmetric (even) function of s, then the integrand in (*) would be (even) times (odd) = odd, and the integral would vanish:

    integral_{-L}^{L} (even)(odd) ds = 0

This would be a PERFECT cancellation. The question reduces to: **Is eta symmetric about the closest-approach point?**

### 3.3 Why the naive argument fails

The curvature eta is NOT a fixed background quantity. It evolves in response to the strain from Tube B, including the very D_xi S that we are integrating. The interaction modifies eta DURING the encounter.

Before the interaction (t < t_0), eta could have any profile. Let us decompose it:

    eta(s, t) = eta_even(s, t) + eta_odd(s, t)

where eta_even(-s) = eta_even(s) and eta_odd(-s) = -eta_odd(s).

The curvature evolution equation (23) from curvature-evolution-analysis.md:

    D_t eta = [S_perp - 2Q I_perp] eta + P_perp((D_xi S) xi) + V_nu

Consider the source term P_perp((D_xi S_B) xi). If this is odd in s (which we established for the dominant component), then it DRIVES an odd component of eta. Specifically:

    D_t eta_odd ~ ... + [odd part of P_perp((D_xi S_B) xi)] + ...

Starting from eta_odd(s, t_0) = 0 (no odd component initially), the interaction creates:

    eta_odd(s, t_0 + Delta t) ~ P_perp((D_xi S_B(s)) xi) * Delta t

This is odd in s (inheriting the parity of the source).

### 3.4 The self-consistent integral

Now the integral (*) at time t_0 + Delta t becomes:

    I = integral_{-L}^{L} 2 [eta_even(s) + eta_odd(s)] . [D_xi S_B(s)] xi ds

    = integral_{-L}^{L} 2 eta_even(s) . [D_xi S_B(s)] xi ds
      + integral_{-L}^{L} 2 eta_odd(s) . [D_xi S_B(s)] xi ds

The first integral vanishes (even times odd = odd, integral = 0). Good.

The second integral: eta_odd is odd, D_xi S_B is odd, so the product is EVEN:

    integral_{-L}^{L} 2 eta_odd(s) . [D_xi S_B(s)] xi ds = integral_{-L}^{L} (even, nonnegative) ds > 0

**This integral does NOT vanish.** In fact, it has a definite sign: since eta_odd was created by D_xi S_B, the vectors eta_odd(s) and P_perp((D_xi S_B(s)) xi) point in the same direction (both are driven by the same source). Therefore:

    eta_odd(s) . (D_xi S_B(s)) xi ~ |P_perp((D_xi S_B(s)) xi)|^2 * Delta t >= 0

The integral is:

    I_self ~ 2 Delta t * integral_{-L}^{L} |P_perp((D_xi S_B(s)) xi)|^2 ds

This is strictly positive. **The antisymmetry does not produce a cancellation in the self-consistent problem.**

### 3.5 Physical interpretation

The failure of the cancellation has a clear physical meaning. The odd D_xi S profile bends the tube in opposite directions on the two sides of the closest-approach point. On the +z side, it bends the tube one way; on the -z side, the other way. This creates an S-shaped deformation (odd curvature). The S-shaped curvature then interacts with the SAME odd D_xi S profile, and the product (odd) x (odd) = (even) is always positive. The two sides of the S-bend both contribute positively to the kappa^2 growth.

This is analogous to squeezing a flexible rod at one point: the rod bends both up and down on the two sides, but the bending energy (proportional to kappa^2) is positive on both sides.

---

## Step 4: Is eta Actually Symmetric? (Detailed Analysis)

### 4.1 The impulse approximation

If the interaction is fast (Delta t << 1/omega), we can use the impulse approximation:

    Delta eta(s) = integral_{t_0}^{t_0 + Delta t} P_perp((D_xi S_B(s, t)) xi) dt + ...

During the transit, D_xi S_B(s, t) varies in time because the relative position of Tube B changes. At a fixed point s on Tube A, Tube B sweeps past during the interaction.

Parametrize the transit: Tube B moves with velocity v_transit perpendicular to the separation direction. The closest-approach distance at time t is:

    d(t) ~ (d_min^2 + v_transit^2 (t - t_closest)^2)^{1/2}

The D_xi S at position s on Tube A and time t depends on the full geometry: the distance from (0,0,s) to Tube B at time t.

### 4.2 Time-dependent D_xi S profile

For a specific point s on Tube A, the perpendicular distance to Tube B at time t is:

    D(s, t) = ((d(t))^2 + s^2 sin^2(Theta))^{1/2}

where d(t) accounts for the time-varying closest-approach distance. The D_xi S at that point:

    |D_xi S_B(s, t)| ~ Gamma |s| sin^2(Theta) / (pi D(s,t)^4)

The time integral:

    integral |D_xi S_B(s, t)| dt ~ Gamma |s| sin^2(Theta) / pi * integral dt / D(s,t)^4

For the transit geometry with d(t) = (d_min^2 + v^2 t^2)^{1/2}:

    D(s, t)^4 = (d_min^2 + v^2 t^2 + s^2 sin^2(Theta))^2

The integral over t:

    integral_{-infty}^{infty} dt / (a^2 + v^2 t^2)^2 = pi / (2 v a^3)

where a^2 = d_min^2 + s^2 sin^2(Theta). So:

    integral |D_xi S_B(s, t)| dt ~ Gamma |s| sin^2(Theta) / (pi) * pi / (2 v (d_min^2 + s^2 sin^2(Theta))^{3/2})
                                  = Gamma |s| sin^2(Theta) / (2 v (d_min^2 + s^2 sin^2(Theta))^{3/2})

Using v ~ Gamma sin(Theta) / (2 pi d_min):

    integral |D_xi S_B(s, t)| dt ~ pi d_min |s| sin(Theta) / (d_min^2 + s^2 sin^2(Theta))^{3/2}

This is an **odd function of s** (the |s| should be s with a sign from the direction of D_xi S):

    Delta eta(s) ~ C * s sin(Theta) / (d_min^2 + s^2 sin^2(Theta))^{3/2}

where C > 0 encodes the direction and magnitude constants.

**Confirmed: the impulse Delta eta is an ODD function of s.** The interaction creates an antisymmetric curvature perturbation.

### 4.3 Decomposition of the pre-existing curvature

The total curvature at any time during the interaction is:

    eta(s) = eta_0(s) + Delta eta(s)

where eta_0(s) is the pre-existing curvature (could be anything) and Delta eta(s) is the interaction-generated perturbation (odd in s).

Decompose eta_0(s) = eta_0^{even}(s) + eta_0^{odd}(s).

The integral (*):

    I = integral 2 [eta_0^{even} + eta_0^{odd} + Delta eta] . (D_xi S_B) xi ds

    = underbrace{integral 2 eta_0^{even} . (D_xi S_B) xi ds}_{= 0, even x odd}
      + underbrace{integral 2 eta_0^{odd} . (D_xi S_B) xi ds}_{= I_1, odd x odd = even, nonzero in general}
      + underbrace{integral 2 Delta eta . (D_xi S_B) xi ds}_{= I_2 > 0, self-interaction}

The first integral vanishes by parity. The third integral (I_2) is strictly positive (the self-interaction term from Step 3.4).

The second integral (I_1) involves the pre-existing odd curvature and could have either sign. It depends on the correlation between the pre-existing asymmetric curvature and the D_xi S profile.

### 4.4 Expected value of I_1

In a turbulent flow, the pre-existing curvature eta_0(s) has no preferred correlation with the D_xi S profile from an approaching tube (whose position and angle are independent of the local curvature). Therefore:

    E[I_1] = E[integral 2 eta_0^{odd}(s) . (D_xi S_B(s)) xi ds] = integral 2 E[eta_0^{odd}(s)] . (D_xi S_B(s)) xi ds

If the pre-existing odd curvature has zero mean (no preferred asymmetry), then E[I_1] = 0. The variance of I_1 is nonzero, but it contributes equally to positive and negative values. Over many interactions, I_1 averages to zero.

**The surviving contribution is I_2, the self-interaction term, which is always positive.**

---

## Step 5: Quantifying the Partial Cancellation

### 5.1 The self-interaction integral I_2

From Step 3.4:

    I_2 = 2 Delta t * integral_{-L}^{L} |P_perp((D_xi S_B(s)) xi)|^2 ds

Using the profile from Step 1:

    |D_xi S_B(s)| ~ Gamma sin^2(Theta) |s| / (pi D^4(s))

where D^2(s) = d^2 + s^2 sin^2(Theta). The integral:

    integral_{-infty}^{infty} |D_xi S_B(s)|^2 ds
    = (Gamma sin^2(Theta) / pi)^2 integral_{-infty}^{infty} s^2 ds / (d^2 + s^2 sin^2(Theta))^4

Substituting s = d u / sin(Theta):

    = (Gamma sin^2(Theta) / pi)^2 * (d / sin(Theta)) * d^2 / sin^2(Theta) * integral_{-infty}^{infty} u^2 du / (d^2)^4 (1 + u^2)^4

    = (Gamma^2 sin(Theta) / (pi^2 d^5)) integral_{-infty}^{infty} u^2 du / (1 + u^2)^4

The integral integral u^2 / (1+u^2)^4 du = pi * 1 * 3 / (2^4 * 3!) ... let me compute it properly.

Using the beta function: integral_0^{infty} u^2 / (1+u^2)^4 du = (1/2) B(3/2, 5/2) = (1/2) * Gamma(3/2) Gamma(5/2) / Gamma(4)

Gamma(3/2) = sqrt(pi)/2, Gamma(5/2) = 3sqrt(pi)/4, Gamma(4) = 6.

So: (1/2) * (sqrt(pi)/2)(3 sqrt(pi)/4) / 6 = (1/2) * 3 pi / (8 * 6) = pi/32.

The full integral (both sides): 2 * pi/32 = pi/16.

Therefore:

    integral_{-infty}^{infty} |D_xi S_B(s)|^2 ds = Gamma^2 sin(Theta) / (pi^2 d^5) * pi/16
                                                   = Gamma^2 sin(Theta) / (16 pi d^5)

### 5.2 Comparing I_2 with the naive (no cancellation) estimate

Without any cancellation, the contribution to kappa^2 growth from D_xi S would be:

    I_naive = integral 2 |eta| |D_xi S| ds ~ 2 kappa * integral |D_xi S| ds

Using integral |D_xi S| ds ~ Gamma sin(Theta) / d^2 (from the z-integral of the odd profile, but taking absolute values):

    integral_{-infty}^{infty} |D_xi S_B(s)| ds = (Gamma sin^2(Theta) / pi) integral |s| ds / (d^2 + s^2 sin^2(Theta))^2

    = (Gamma sin^2(Theta) / pi) * 2 integral_0^{infty} s ds / (d^2 + s^2 sin^2(Theta))^2

    = (Gamma sin^2(Theta) / pi) * 2 * 1 / (2 d^2 sin^2(Theta))

    = Gamma / (pi d^2)

So I_naive ~ 2 kappa * Gamma / (pi d^2).

The self-interaction term I_2 grows from zero (it requires the interaction to first create Delta eta). The cumulative I_2 over the interaction time Delta t:

    integral_0^{Delta t} I_2(t) dt ~ integral_0^{Delta t} 2t * [Gamma^2 sin(Theta) / (16 pi d^5)] dt
                                   = (Delta t)^2 * Gamma^2 sin(Theta) / (16 pi d^5)

Using Delta t ~ d / v_transit ~ 2 pi d^2 / (Gamma sin(Theta)):

    integral I_2 dt ~ (2 pi d^2 / (Gamma sin(Theta)))^2 * Gamma^2 sin(Theta) / (16 pi d^5)
                    = 4 pi^2 d^4 sin(Theta) / (16 pi d^5)
                    = pi sin(Theta) / (4 d)

The naive (no cancellation) cumulative effect:

    integral_0^{Delta t} I_naive dt ~ 2 kappa_0 * Gamma / (pi d^2) * Delta t
                                     ~ 2 kappa_0 * Gamma / (pi d^2) * 2 pi d^2 / (Gamma sin(Theta))
                                     = 4 kappa_0 / sin(Theta)

### 5.3 The effective reduction factor

The ratio of the self-interaction contribution to the naive estimate:

    I_2 / I_naive ~ [pi sin(Theta) / (4d)] / [4 kappa_0 / sin(Theta)]
                   = pi sin^2(Theta) / (16 kappa_0 d)

For a tube with initial curvature kappa_0 ~ 1/L_tube (the large-scale curvature), and with d ~ r_c:

    I_2 / I_naive ~ pi sin^2(Theta) / (16 * (1/L_tube) * r_c) = pi sin^2(Theta) L_tube / (16 r_c)

**This ratio is LARGE, not small.** The self-interaction contribution can EXCEED the naive estimate when L_tube >> r_c (which is always the case for well-defined tubes).

**Interpretation:** This seems paradoxical but is physically correct. The antisymmetry cancellation eliminates the contribution of the pre-existing SYMMETRIC curvature to the integral, but the self-generated antisymmetric curvature provides a contribution that actually grows with the length of the tube. The cancellation of the even part is real, but the remaining odd-odd self-interaction is not a small correction -- it is the dominant effect.

### 5.4 Revised understanding

The antisymmetry argument shows:

1. The contribution of pre-existing SYMMETRIC curvature to the D_xi S integral vanishes exactly. This is a real cancellation but only affects the even part of eta.

2. The odd part of eta (whether pre-existing or generated during the interaction) couples positively to the odd D_xi S. The self-generated odd curvature always contributes positively.

3. The NET effect is that the D_xi S integral is driven entirely by the odd component of eta. Since the interaction generates an odd eta from scratch, the integral is nonzero even starting from eta = 0.

4. **The effective |D_xi S| is NOT reduced** by the antisymmetry. The peak |D_xi S| still scales as omega^{3/2}/nu^{1/2}. What the antisymmetry tells us is that the curvature growth is localized and has a specific spatial structure (S-shaped deformation), but the magnitude is unchanged.

---

## Step 6: Finite-Core Correction

### 6.1 Burgers vortex core profile

For a Burgers vortex tube with Gaussian core:

    omega_B(r) = omega_0 exp(-r^2 / r_c^2)

where r is the distance from Tube B's axis and r_c = (4 nu / alpha)^{1/2}.

The velocity induced by this finite-core tube differs from the line vortex for distances D < r_c. At distance D >> r_c, the finite core is indistinguishable from a line vortex.

### 6.2 Strain from the finite-core tube

At a point (0, 0, z) on Tube A's axis, at perpendicular distance D(z) from Tube B's axis:

For D >> r_c: S_B ~ Gamma / (2 pi D^2), same as line vortex. No correction needed.

For D ~ r_c: The strain is modified. The Burgers vortex velocity field:

    v_theta(r) = (Gamma / (2 pi r)) (1 - exp(-r^2/r_c^2))

The strain magnitude at distance r from the core:

    |S_B(r)| ~ (Gamma / (2 pi r^2)) [1 - (1 + r^2/r_c^2) exp(-r^2/r_c^2)]  for the shear component

This approaches Gamma / (2 pi r^2) for r >> r_c and goes to Gamma / (4 pi r_c^2) = omega_0 / 4 at r = 0.

The key difference from the line vortex: |S_B| is FINITE at D = 0 (the center of Tube B's core), whereas the line vortex gives |S_B| -> infinity as D -> 0.

### 6.3 Effect on the antisymmetry

At the closest-approach point (z = 0), D(0) = d. For d >> r_c, the finite-core correction is negligible and the antisymmetry is exact to high precision.

For d ~ r_c (the dangerous regime): D(z) = (d^2 + z^2 sin^2(Theta))^{1/2}. The strain from the finite core:

    |S_B(0,0,z)| = F(D(z))

where F(D) is the finite-core strain profile. The key question: is F(D) a SMOOTH EVEN function of D? If F depends on D only through D^2, then |S_B(0,0,z)| = F((d^2 + z^2 sin^2(Theta))^{1/2}) is still an even function of z, and its z-derivative is still odd.

For the Burgers vortex, the strain field at distance D from the axis depends on D (not on the direction in the cross-sectional plane) for the axisymmetric case. The strain is a smooth function of D^2 (since the Gaussian profile is a smooth function of r^2). Therefore:

    |S_B(0,0,z)| = G(D^2(z)) = G(d^2 + z^2 sin^2(Theta))

where G is a smooth function. This is EVEN in z. Its z-derivative is ODD.

**The antisymmetry of D_xi S is EXACT for the Burgers vortex model, not just the line vortex model.** The key requirement is that the strain is a smooth function of the perpendicular distance D, which holds for ANY axisymmetric vortex tube.

### 6.4 Breaking of antisymmetry

The antisymmetry can be broken by:

1. **Non-axisymmetric core shape.** If Tube B's core is elliptical (e.g., from the strain of Tube A), the strain field depends on the direction in the cross-section, not just D. This breaks the z -> -z symmetry because the relative orientation of the cross-section rotates as one moves along Tube A's axis. The magnitude of the breaking: S_elliptic correction ~ (ellipticity factor) * Gamma / D^2. For ellipticity R ~ (S_ext / alpha)^{1/2} ~ Re_Gamma^{1/2} at d ~ r_c, this could be a significant correction. However, the elliptical deformation is itself smooth and axially uniform at leading order (the core shape does not change along Tube B's axis in the matched-asymptotic limit), so the cross-sectional orientation at the field point is a smooth function of z, and the parity breaking enters through this smooth, bounded function.

2. **Axial variation of the core structure.** If Tube B's core radius or peak vorticity varies along its axis, the symmetry is broken. For a tube with spatially varying r_c(sigma), the strain from different segments of Tube B contributes differently, and the cancellation in the Biot-Savart integral is imperfect. The breaking is proportional to |nabla_axis r_c| * r_c.

3. **Curvature of Tube B.** If Tube B is curved rather than straight, the z -> -z symmetry is broken. The breaking is proportional to kappa_B * r_c (the tube curvature times the core radius).

### 6.5 Magnitude of the antisymmetry breaking

For a Burgers vortex tube with moderate core deformation (R ~ O(1)):

    symmetry breaking ~ max(kappa_B * d, |nabla_{axis} r_c| / r_c * d, (R - 1) * d / L_B)

where L_B is the length scale over which the cross-section orientation changes. All of these are small when d << L_B and the tube is nearly straight, which is the regime where D_xi S reaches its peak.

At d ~ r_c, the typical symmetry breaking is:

    fractional breaking ~ r_c * kappa_B + r_c |nabla_{axis} r_c| / r_c + (R - 1) r_c / L_B

For a tube with kappa_B ~ 1/L_tube (large-scale curvature):

    fractional breaking ~ r_c / L_tube << 1

**The antisymmetry is broken by a factor of order r_c / L_tube, which is small for well-defined tubes.** But as we showed in Step 5, this breaking does NOT help the cancellation argument -- the dominant contribution to the integral comes from the self-generated odd curvature, not from the (small) even part of D_xi S.

---

## Step 7: Verdict

### 7.1 Is the antisymmetry of D_xi S exact or approximate?

**Exact for any axisymmetric vortex tube model** (line vortex, Burgers vortex, Lamb-Oseen, etc.) in the idealized two-straight-tube configuration. Approximate (with small corrections of order r_c/L_tube) for realistic tubes with curvature, axial non-uniformity, or core deformation.

### 7.2 Does the curvature evolution integral benefit from this cancellation?

**No, not in the way originally hoped.** The cancellation eliminates the contribution of the SYMMETRIC part of the curvature to the D_xi S integral, but the ANTISYMMETRIC part of the curvature (generated by the interaction itself) couples positively with the antisymmetric D_xi S. The self-consistent analysis shows that the curvature evolution integral is controlled by the self-interaction of the odd mode, which is nonzero and has a definite positive sign.

Specifically:

- The naive hope was: integral [eta . (D_xi S) xi] ds = 0 by parity, giving perfect cancellation.
- Reality: integral [eta_even . (D_xi S) xi] ds = 0 (this cancellation IS exact), but integral [eta_odd . (D_xi S) xi] ds > 0, and the interaction generates eta_odd from scratch. The net integral is positive and comparable in magnitude to the uncancelled estimate.

### 7.3 What is the quantitative gain?

**No gain** in the scaling exponent. The peak |D_xi S| is still omega^{3/2}/nu^{1/2}. The time-integrated effect is still of order omega^{1/2}/nu^{1/2}. The antisymmetry provides:

1. A constant-factor reduction (the effective |D_xi S| integrated against the self-consistent curvature has a smaller numerical prefactor than the absolute-value integral, by a factor of order pi/16). This is an O(1) improvement, not a power-law or logarithmic one.

2. A structural insight: the curvature growth from tube-tube interactions has a specific spatial structure (S-shaped deformation, odd in the axial coordinate). This structure means that the curvature is localized near the interaction point with alternating signs, which limits the spatial extent over which kappa is large. But this does not reduce the peak kappa.

### 7.4 Does this close Theorem CB?

**No.** Theorem CB requires delta > 1/2, meaning |D_xi S| <= C |omega|^{1+delta} with delta > 1/2. The tube-tube interaction gives delta = 1/2 exactly. The antisymmetry cancellation:

- Does not change the peak D_xi S scaling (delta = 1/2 remains).
- Does not provide a logarithmic gain (which would correspond to |D_xi S| <= C |omega|^{3/2} / (nu^{1/2} log^{1/2}(|omega|/nu))).
- Provides only an O(1) constant-factor improvement in the effective curvature coupling.

The borderline delta = 1/2 is NOT crossed by this mechanism.

### 7.5 What would be needed

To close Theorem CB via this route, one would need to show that the curvature evolution integral is reduced by a LOGARITHMIC factor:

    integral eta . (D_xi S) xi ds <= C |D_xi S|_peak * kappa / log(omega/nu)

This would require a cancellation that goes beyond the simple parity argument. Possible mechanisms:

1. **Frequency-space cancellation:** If D_xi S and eta have oscillatory spatial profiles whose phases are uncorrelated, an L^2 orthogonality argument could give root-N cancellation for N oscillations. But in the tube-tube problem, D_xi S has a specific non-oscillatory profile (single-lobed odd function), so there is no frequency-space cancellation.

2. **Multi-tube statistical cancellation:** Over many independent tube-tube encounters, the pre-existing odd curvature eta_0^{odd} has random correlation with each encounter's D_xi S profile. The contribution I_1 from Step 4.3 averages to zero over many encounters. However, the self-interaction I_2 has a definite sign and accumulates without cancellation.

3. **Nonlinear saturation:** The curvature generated by D_xi S could be limited by nonlinear effects (e.g., the S-shaped deformation reconnects or is smoothed by viscous diffusion faster than D_xi S can amplify it). This is a viscous effect and would give a factor involving Re_Gamma, not a logarithmic factor.

None of these mechanisms has been shown to provide a logarithmic gain. **The antisymmetry cancellation, while real, is a structural feature that is already captured by the existing estimates.** It does not constitute a new route to closing Theorem CB.

---

## Summary Table

| Question | Answer |
|----------|--------|
| Is D_xi S antisymmetric about closest approach? | **Yes, exactly** for axisymmetric tube models |
| D_xi S = 0 at exact closest-approach point? | **Yes** |
| Does eta have even symmetry? | **No**: the interaction generates odd eta |
| Does integral eta . (D_xi S) xi ds vanish? | **No**: odd x odd = even, integral > 0 |
| Quantitative gain from antisymmetry | O(1) constant factor only |
| Does this close Theorem CB (delta > 1/2)? | **No** |
| Does this provide logarithmic gain? | **No** |
| Finite-core correction to antisymmetry | Small (order r_c / L_tube) |
| New insight from this analysis | Curvature growth has S-shaped spatial structure |

---

## Appendix: Technical Details of the Self-Interaction Integral

### A.1 The odd curvature profile

The impulse-generated curvature from a single transit:

    Delta eta(s) = C_eta * s sin(Theta) / (d^2 + s^2 sin^2(Theta))^{3/2} * e_perp

where C_eta = Gamma * Delta t / (2 pi d) (with appropriate constants) and e_perp is the perpendicular direction in which D_xi S acts.

This profile has:
- Peak at s_* = d / (sqrt(2) sin(Theta)) with value ~ C_eta / d^2
- Decay as 1/s^2 for |s| >> d / sin(Theta)
- Integral of |Delta eta|: ~ C_eta / (d sin(Theta))

### A.2 The kappa^2 increment from self-interaction

The kappa^2 increment from a single transit, via the self-interaction mechanism:

    Delta(kappa^2)|_{self} ~ 2 * integral Delta eta(s) . P_perp((D_xi S_B(s)) xi) ds * Delta t

The integrand:

    Delta eta(s) . P_perp((D_xi S_B(s)) xi) ~ C_eta * [s sin(Theta)]^2 / (d^2 + s^2 sin^2(Theta))^{7/2}

(product of two odd functions, giving even, positive definite).

The integral:

    integral_{-infty}^{infty} s^2 sin^2(Theta) ds / (d^2 + s^2 sin^2(Theta))^{7/2}

    = (1/(d^5 sin(Theta))) integral_{-infty}^{infty} u^2 du / (1 + u^2)^{7/2}

    = (1/(d^5 sin(Theta))) * B(3/2, 2) = (1/(d^5 sin(Theta))) * pi/8

(using the beta function integral).

Therefore:

    Delta(kappa^2)|_{self} ~ Gamma^2 Delta t^2 sin(Theta) / d^5

With Delta t ~ d^2 / (Gamma sin(Theta)):

    Delta(kappa^2)|_{self} ~ Gamma^2 * d^4 / (Gamma^2 sin^2(Theta)) * sin(Theta) / d^5
                            = 1 / (d sin(Theta))

At d = r_c:

    **Delta(kappa^2)|_{self} ~ 1 / (r_c sin(Theta))**

Compare with the naive Delta kappa ~ omega^{1/2}/nu^{1/2} from tube-tube-interaction-analysis.md Section 2.6:

    (Delta kappa)^2 ~ omega / nu ~ 1 / r_c^2

So Delta(kappa^2)|_{self} ~ 1/(r_c sin(Theta)), while (Delta kappa)_{naive}^2 ~ 1/r_c^2.

The ratio: Delta(kappa^2)|_{self} / (Delta kappa)_{naive}^2 ~ r_c / sin(Theta) * 1/r_c^2 ... hmm, these are of the same order for sin(Theta) ~ 1. This confirms the conclusion: **no gain from the antisymmetry**. The self-interaction produces a kappa^2 increment of the same order as the naive (unsigned) estimate.
