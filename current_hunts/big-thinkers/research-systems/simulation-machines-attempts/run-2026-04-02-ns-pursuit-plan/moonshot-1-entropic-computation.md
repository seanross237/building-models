# Moonshot 1: Viscous Spectral Angular Suppression -- Full Computation

**Date:** 2026-04-02
**Parent:** three-moonshots.md (Moonshot 1: The Entropic Vortex), coupled-bootstrap-attempt.md (Theorem CB)
**Purpose:** Complete the explicit computation outlined in Moonshot 1, testing whether cumulative viscous diffusion constrains the angular distribution of spectral mass in a way that produces a logarithmic suppression of D_xi S.

---

## 0. Theorem CB Recap and the Precise Target

Theorem CB (from coupled-bootstrap-attempt.md): NS is regular if

    |D_xi S(x)| <= C |omega(x)|^{1+delta}    on {|omega| > M}

with delta > 1/2. The Calderon-Zygmund estimate gives exactly delta = 1/2 (i.e., |D_xi S| ~ |omega|^{3/2}/nu^{1/2}). A logarithmic improvement suffices:

    |D_xi S| <= C |omega|^{3/2} / (nu^{1/2} (log |omega|)^{1+epsilon})

The spectral angular suppression thesis: the Fourier multiplier for D_xi S weights frequency components by |k . xi|/|k| = cos(angle(k, xi)). If viscous diffusion forces the spectral mass of omega to concentrate perpendicular to xi, this cosine factor is systematically small, potentially producing the logarithmic deficit.

---

## 1. Angular Spectrum of the Burgers Vortex

### 1.1 Setup

The Burgers vortex has vorticity omega = omega_z(r) e_z with:

    omega_z(r) = (Gamma alpha / (4 pi nu)) exp(-alpha r^2 / (4 nu))

This is a Gaussian in the (x,y)-plane, constant in z. The Fourier transform in all three variables is:

    hat{omega}_z(k_x, k_y, k_z) = (Gamma alpha / (4 pi nu)) * (4 pi nu / alpha) exp(-nu |k_perp|^2 / alpha) * delta(k_z)

where k_perp = (k_x, k_y). Simplifying the prefactor:

    hat{omega}_z(k_perp, k_z) = Gamma exp(-nu |k_perp|^2 / alpha) * delta(k_z)

### 1.2 Spectral angular distribution

Define the angle theta between k and xi = e_z by cos(theta) = k_z/|k|. The spectral energy density |hat{omega}(k)|^2 has support ONLY at k_z = 0, i.e., at theta = pi/2. The angular distribution is:

    E(theta) = integral |hat{omega}(k)|^2 delta(theta - angle(k, e_z)) dk
             = Gamma^2 * delta(theta - pi/2) * integral exp(-2 nu |k_perp|^2 / alpha) dk_perp
             = Gamma^2 * (pi alpha / (2 nu)) * delta(theta - pi/2)

This is maximally concentrated perpendicular to xi. ALL spectral mass is at theta = pi/2.

### 1.3 D_xi S for the straight Burgers vortex

The Fourier multiplier for D_xi S involves the factor (k . xi) = k_z. Since hat{omega} is supported at k_z = 0:

    (D_xi S)^(k) ~ (k . xi) * |k| * hat{omega}(k) = k_z * |k| * hat{omega}(k) = 0

Therefore D_xi S = 0 identically for the straight Burgers vortex.

This is consistent with the direct computation: the Burgers vortex is z-independent, so partial_z S = 0 identically, and D_xi S = (e_z . nabla) S = partial_z S = 0.

**Assessment:** The straight Burgers vortex achieves perfect angular suppression (D_xi S = 0). This is the trivial case. The informative question is what happens when z-invariance is broken.

---

## 2. Perturbed Burgers Vortex with z-Variation

### 2.1 Modeling z-dependence through tube curvature

Consider a Burgers vortex tube whose axis has curvature kappa. The vorticity is no longer z-independent; the axis direction rotates on the scale 1/kappa. In a local coordinate system following the tube, the vorticity has the form:

    omega(x) = omega_z(r) e_z(s) + O(kappa r_c) corrections

where s is arclength along the tube axis. The z-variation of the core profile introduces spectral mass at k_z != 0.

### 2.2 Fourier spectrum of the curved tube

The along-axis variation of the vorticity direction occurs on the scale L_kappa = 1/kappa. The Fourier transform of e_z(s) (the rotating unit tangent) has the schematic form:

    hat{e}_z(k_z) ~ delta(k_z) + kappa * g(k_z/kappa)

where g is a function with integral 1, concentrated at |k_z| ~ kappa. The full vorticity spectrum is the convolution:

    hat{omega}(k_perp, k_z) ~ Gamma exp(-nu |k_perp|^2 / alpha) * [delta(k_z) + kappa g(k_z/kappa)]

The spectral energy at k_z != 0 is:

    |hat{omega}(k_perp, k_z)|^2 ~ Gamma^2 exp(-2 nu |k_perp|^2 / alpha) * kappa^2 |g(k_z/kappa)|^2

For a smooth axis with curvature kappa and curvature variation on scale L, g is approximately a Lorentzian:

    |g(q)|^2 ~ 1 / (q^2 + 1)^2

(The precise form depends on the tube geometry; for a circular arc, g is a sinc function; for a smoothly varying curvature, it is approximately Lorentzian. The qualitative features are the same.)

### 2.3 Angular energy distribution for the curved tube

The spectral energy as a function of angle theta from the perpendicular plane:

At wavenumber magnitude |k|, the angle theta satisfies sin(theta) = |k_z|/|k|, so |k_z| = |k| sin(theta) and |k_perp| = |k| cos(theta). The spectral energy at angle theta is:

    E(theta, |k|) ~ Gamma^2 exp(-2 nu |k|^2 cos^2(theta) / alpha) * kappa^2 / (|k|^2 sin^2(theta)/kappa^2 + 1)^2

For |k| near the dissipation wavenumber k_d = (alpha/nu)^{1/2} = 1/r_c (the scale at which the Gaussian core rolls off):

    E(theta, k_d) ~ Gamma^2 exp(-2 cos^2(theta)) * kappa^2 / (sin^2(theta)/(kappa r_c)^2 + 1)^2

The key ratio is epsilon := kappa r_c << 1 (the tube slenderness parameter). The angular distribution at the dissipation scale has two regimes:

**Regime 1 (theta >> epsilon):** The Lorentzian factor is approximately 1, and:

    E(theta, k_d) ~ Gamma^2 exp(-2 cos^2(theta)) * kappa^2

This is the "bulk" of the spectral mass at k_z ~ kappa, which is far from the xi-direction.

**Regime 2 (theta << epsilon):** The Lorentzian suppresses:

    E(theta, k_d) ~ Gamma^2 * kappa^2 * (theta/epsilon)^4 / (1 + (theta/epsilon)^2)^2

For theta very close to 0 (the xi-direction): E ~ Gamma^2 kappa^2 (theta/epsilon)^4.

### 2.4 The angular suppression ratio

The ratio of spectral energy in the "dangerous" xi-aligned band (|theta| < epsilon, where cos(theta) ~ 1) to the total spectral energy at the dissipation scale:

    R = integral_0^{epsilon} E(theta, k_d) sin(theta) dtheta / integral_0^{pi/2} E(theta, k_d) sin(theta) dtheta

Numerator (dangerous band):

    integral_0^{epsilon} Gamma^2 kappa^2 * epsilon^{-4} theta^4 * theta dtheta
    = Gamma^2 kappa^2 epsilon^{-4} * integral_0^{epsilon} theta^5 dtheta
    = Gamma^2 kappa^2 epsilon^{-4} * epsilon^6/6
    = Gamma^2 kappa^2 epsilon^2 / 6

Denominator (total):

    integral_0^{pi/2} Gamma^2 kappa^2 * (1 + O(epsilon)) * theta dtheta
    ~ Gamma^2 kappa^2 * (pi/2)^2/2
    ~ Gamma^2 kappa^2

So:

    R ~ epsilon^2 / 6 = (kappa r_c)^2 / 6

**Result:** The fraction of spectral energy in the xi-aligned direction is suppressed by (kappa r_c)^2, the square of the tube slenderness parameter. This confirms the heuristic claim from the Moonshot 1 outline.

---

## 3. D_xi S for the Curved Burgers Tube

### 3.1 The D_xi S multiplier in terms of angular spectrum

The D_xi S Fourier multiplier involves the factor:

    (k . xi) / |k| = cos(angle(k, xi)) = sin(theta_perp)

where theta_perp is the angle from the plane perpendicular to xi. (We use the convention that theta_perp = 0 is perpendicular to xi, and theta_perp = pi/2 is along xi.) In our previous notation where theta was measured from the xi-direction, (k . xi)/|k| = cos(theta), and the spectral mass is concentrated near theta = pi/2 (i.e., near the perpendicular plane, where (k . xi)/|k| ~ 0).

The D_xi S integral in Fourier space has the schematic form (for the Biot-Savart representation):

    |D_xi S(x)| ~ || integral |k . xi| * |k| * |hat{omega}(k)| dk ||

More precisely, D_xi S involves the CZ kernel for nabla^2 u projected along xi, which in Fourier space is:

    (D_xi S)^{ij}(k) ~ (k_m xi_m) (k_i hat{omega}_j(k) + k_j hat{omega}_i(k)) / |k|^2 - trace terms

The key angular weight is (k . xi)/|k| = cos(theta) where theta is measured from the xi-direction. For the full nabla S, the corresponding weight is 1 (no angular dependence). So:

    |D_xi S| / |nabla S| ~ <|cos(theta)|>_E := integral |cos(theta)| E(theta)^{1/2} dtheta / integral E(theta)^{1/2} dtheta

### 3.2 Computing the angular average for the curved Burgers tube

The angular distribution E(theta) at the dissipation scale for the curved tube (from Section 2.3) is:

    E(theta) ~ Gamma^2 kappa^2 * exp(-2 sin^2(theta)) * 1/(cos^2(theta)/epsilon^2 + 1)^2

(Here theta is measured from the perpendicular plane, so theta = 0 is perpendicular and theta = pi/2 is along xi. This is the complement of the angle used in Section 2.)

Wait -- let me be careful with the angle conventions. Let phi = angle between k and xi. Then:

- phi = 0: k is along xi (dangerous direction)
- phi = pi/2: k is perpendicular to xi (safe direction)

The angular weight for D_xi S is cos(phi) = |k . xi|/|k|. The spectral mass of the Burgers tube is concentrated near phi = pi/2. Let me redo the computation in this convention.

The vorticity Fourier spectrum of the curved tube:

    |hat{omega}(k)|^2 ~ Gamma^2 exp(-2 nu |k|^2 sin^2(phi) / alpha) * kappa^2 / (|k|^2 cos^2(phi) / kappa^2 + 1)^2

At the dissipation scale |k| = k_d = 1/r_c:

    |hat{omega}(k_d, phi)|^2 ~ Gamma^2 exp(-2 sin^2(phi)) * kappa^2 / (cos^2(phi)/epsilon^2 + 1)^2

where epsilon = kappa r_c.

The D_xi S multiplier picks up cos(phi). The effective angular average is:

    <cos(phi)>_E = integral_0^{pi/2} cos(phi) |hat{omega}(k_d, phi)|^2 sin(phi) dphi / integral_0^{pi/2} |hat{omega}(k_d, phi)|^2 sin(phi) dphi

**Denominator** (total spectral energy at dissipation scale):

    D = integral_0^{pi/2} Gamma^2 exp(-2 sin^2(phi)) kappa^2 / (cos^2(phi)/epsilon^2 + 1)^2 sin(phi) dphi

For epsilon << 1, the Lorentzian factor kills the integrand for cos(phi) >> epsilon, i.e., for phi << pi/2 - epsilon. The integral is dominated by phi near pi/2. Setting psi = pi/2 - phi (so psi is the angle from the perpendicular plane):

    sin(phi) = cos(psi) ~ 1 for small psi
    cos(phi) = sin(psi) ~ psi
    exp(-2 sin^2(phi)) = exp(-2 cos^2(psi)) ~ exp(-2) for small psi

    D ~ Gamma^2 kappa^2 exp(-2) integral_0^{infty} dpsi / (psi^2/epsilon^2 + 1)^2

The integral integral_0^{infty} dpsi / (psi^2/epsilon^2 + 1)^2 = (pi epsilon / 4) (standard result for Lorentzian squared):

    D ~ Gamma^2 kappa^2 exp(-2) * (pi epsilon / 4) = Gamma^2 kappa^3 r_c exp(-2) pi/4

**Numerator** (D_xi S-weighted spectral energy):

    N = integral_0^{pi/2} cos(phi) * Gamma^2 exp(-2 sin^2(phi)) kappa^2 / (cos^2(phi)/epsilon^2 + 1)^2 sin(phi) dphi

In the psi = pi/2 - phi substitution:

    cos(phi) = sin(psi) ~ psi

    N ~ Gamma^2 kappa^2 exp(-2) integral_0^{infty} psi dpsi / (psi^2/epsilon^2 + 1)^2

The integral integral_0^{infty} psi dpsi / (psi^2/epsilon^2 + 1)^2 = epsilon^2/2 (by substitution u = psi^2/epsilon^2):

    N ~ Gamma^2 kappa^2 exp(-2) * epsilon^2/2 = Gamma^2 kappa^2 (kappa r_c)^2 exp(-2) / 2

**Angular suppression factor:**

    <cos(phi)>_E = N/D = (epsilon^2/2) / (pi epsilon/4) = 2 epsilon / pi = 2 kappa r_c / pi

**Result:**

    |D_xi S| / |nabla S| ~ (2/pi) kappa r_c

for the curved Burgers tube at the dissipation scale.

### 3.3 Absolute bound on D_xi S

Using |nabla S| ~ |omega|^{3/2}/nu^{1/2} (the CZ dimensional estimate, which is |nabla^2 u| at the dissipation scale):

    |D_xi S| ~ (2/pi) kappa r_c * |omega|^{3/2}/nu^{1/2}

Using r_c = (nu/|omega|)^{1/2} = (nu/Omega)^{1/2}:

    |D_xi S| ~ (2/pi) kappa (nu/Omega)^{1/2} * Omega^{3/2}/nu^{1/2} = (2/pi) kappa Omega

**This reproduces the LIA estimate from Path 3.** The spectral angular suppression and the matched asymptotic expansion give the same answer:

    |D_xi S|_{single tube} ~ C kappa |omega|

where C is a dimensionless constant of order 1. For bounded kappa (which NLS global well-posedness provides in the LIA regime), this is |omega|^{1+0}, far better than the |omega|^{3/2}/nu^{1/2} threshold needed for Theorem CB.

**Cross-validation:** Two completely independent methods -- (1) Fourier angular analysis of the spectral mass distribution and (2) matched asymptotics of the Biot-Savart integral for a thin tube (Path 3 in three-practical-paths.md) -- produce the same scaling |D_xi S| ~ kappa |omega|. This is strong evidence that the single-tube estimate is correct.

---

## 4. Can Viscous Spectral History Provide an ADDITIONAL Logarithmic Correction?

The computation in Section 3 produced a power-law suppression (by the factor kappa r_c) for the single tube. The question now is whether the cumulative viscous history provides a logarithmic correction ON TOP of this power-law gain.

### 4.1 Viscous angular diffusion of spectral mass

Consider the angular distribution of spectral energy at wavenumber |k|. The viscous term in the vorticity equation damps all frequencies at rate nu |k|^2, isotropically. In the angular variable, viscous diffusion acts as a heat kernel on the sphere S^2 in k-space: spectral mass at any point on the unit sphere |k| = const diffuses toward uniform distribution at rate nu |k|^2.

For a vortex tube, the nonlinear term (stretching + advection) preferentially injects spectral energy perpendicular to xi (because the vortex stretching creates fine-scale structure in the transverse plane). The steady-state angular distribution is determined by the balance:

    (injection rate) * f(phi) = nu |k|^2 * angular diffusion operator * E(phi, |k|)

where f(phi) is the angular injection pattern, peaked at phi = pi/2 (perpendicular to xi).

For the Burgers vortex, this balance is exact: the external strain alpha continually stretches the vortex in the transverse plane, maintaining the Gaussian core, while viscous diffusion maintains the steady state. The angular distribution we computed in Sections 1-2 IS the steady-state result of this viscous-stretching balance.

### 4.2 The question of logarithmic correction

The Lorentzian angular profile kappa^2 / (cos^2(phi)/epsilon^2 + 1)^2 from Section 2 was derived from the geometric structure (curvature kappa introduces k_z spectral mass at the scale kappa). Does the viscous history modify this profile by a logarithmic factor?

Consider the following refined model. The spectral energy at angle phi from the perpendicular plane and at wavenumber |k| satisfies the steady-state balance:

    nu |k|^2 E(phi, |k|) = F(phi, |k|)

where F is the injection rate from the nonlinear term. The injection at angle phi near 0 (the xi-direction) comes from the nonlinear transfer of energy from the perpendicular plane into the xi-direction. For a tube with curvature kappa, this transfer occurs because the tube axis is not perfectly straight -- the curvature couples perpendicular and parallel modes.

The transfer rate at angle phi from the nonlinear term scales as:

    F(phi, |k|) ~ (stretching rate) * E_{perp}(|k|) * T(phi)

where T(phi) is the angular transfer function due to the curvature. For a tube with curvature kappa, the coupling between modes at angle phi_1 and phi_2 involves the matrix element:

    <phi_1| stretching |phi_2> ~ kappa * (angular convolution kernel)

The key mechanism: viscous diffusion acts on the angular distribution at rate nu |k|^2, while the nonlinear transfer acts at rate ~ |omega|. At the dissipation scale |k| = k_d = (|omega|/nu)^{1/2}, these rates are comparable. But for k > k_d, the viscous damping dominates exponentially.

The cumulative effect of viscous diffusion from scales larger than k_d (where the angular distribution is set by the tube geometry) to the dissipation scale k_d (where D_xi S is evaluated) involves integrating the angular evolution over the wavenumber range. Each octave of wavenumber (from k to 2k) provides one e-folding of viscous angular diffusion. The number of octaves from the injection scale k_0 ~ kappa (where the z-variation enters) to the dissipation scale k_d = 1/r_c is:

    N_{oct} = log_2(k_d / k_0) = log_2(1/(kappa r_c)) = log_2(1/epsilon)

Over these N_{oct} octaves, the angular distribution undergoes N_{oct} e-foldings of angular diffusion. If each octave widens the angular spread by a fixed multiplicative factor, the cumulative effect is a power of epsilon:

    angular width at k_d ~ angular width at k_0 * (widening factor)^{N_{oct}}

This does NOT produce a logarithmic correction -- it produces a power-law correction that is already captured by the kappa r_c factor.

However, there is a subtlety: the angular diffusion on the sphere is NOT simply multiplicative in the octave structure. The angular heat kernel on S^2 has eigenvalues l(l+1) for the l-th spherical harmonic. The low-l modes (large angular scales) diffuse slowly, while the high-l modes (fine angular structure) diffuse rapidly. The angular structure relevant to D_xi S involves the l = 1 mode (the cos(phi) projection), which diffuses at rate 2 nu |k|^2.

The contribution of the l = 1 angular mode to the spectrum at wavenumber k is:

    E_1(k) ~ E_1(k_0) * exp(-2 nu integral_{k_0}^{k} |k'|^2 dk'/|k'|)

Wait -- this is not quite right. The angular diffusion occurs in time, not in wavenumber. The viscous damping at each wavenumber acts at rate nu |k|^2, but the angular diffusion and the radial (wavenumber) diffusion are coupled through the same viscous operator.

Let me reconsider more carefully.

### 4.3 Angular evolution in the spectral balance equation

The vorticity equation in Fourier space is:

    d/dt hat{omega}(k) = (nonlinear)^(k) - nu |k|^2 hat{omega}(k)

The viscous term -nu |k|^2 hat{omega}(k) damps ALL angular modes at the same rate (at fixed |k|). It does NOT diffuse angular structure -- it only damps the amplitude isotropically.

**This is a critical observation.** The viscous term in the vorticity equation, when written in Fourier space, is a multiplication by -nu |k|^2. This multiplication is isotropic in k -- it treats all angular directions equally. It does NOT cause angular spreading of the spectrum. It damps ALL directions at the same rate.

Angular spreading of the spectrum in k-space would require the viscous term to act differently on different angular modes at the same |k|. But the Laplacian Delta = -|k|^2 in Fourier space is perfectly isotropic.

**Correction to the Moonshot 1 thesis:** The claim that "viscous diffusion acts as a Gaussian channel that increases entropy at rate proportional to nu -- it spreads spectral mass isotropically" is INCORRECT in the following sense: in PHYSICAL space, the heat kernel is isotropic and spreads mass in all spatial directions. But in FOURIER space, the viscous damping is multiplicative and does NOT spread spectral mass in k-space. The spectral angular distribution is preserved (up to uniform damping) by the viscous term alone.

Therefore, the angular distribution of |hat{omega}(k)|^2 is determined entirely by the NONLINEAR term and the initial condition, not by the viscous term. The viscous term only sets the overall dissipation scale k_d, not the angular distribution at that scale.

### 4.4 What the viscous term DOES constrain

While the viscous term does not directly cause angular diffusion in k-space, it constrains the angular distribution indirectly through the energy balance:

1. **The enstrophy dissipation bound:** integral_0^T integral nu |nabla omega|^2 dx dt = integral_0^T integral nu |k|^2 |hat{omega}(k)|^2 dk dt < infinity. This bounds the total spectral energy at high wavenumbers, but says nothing about the angular distribution.

2. **The palinstrophy bound:** integral_0^T integral nu |Delta omega|^2 dx dt bounds integral nu |k|^4 |hat{omega}|^2 dk dt, which still says nothing angular.

3. **The DIRECTIONAL enstrophy:** integral nu |D_xi omega|^2 dx = integral nu |k . xi|^2 |hat{omega}(k)|^2 dk. This IS an angular quantity -- it weights by (k . xi)^2 = |k|^2 cos^2(phi). But this quantity is not directly bounded by the viscous balance unless we have additional information about the D_xi omega evolution.

**Bottom line:** The viscous term in the vorticity equation, by itself, does NOT produce angular diffusion in k-space and does NOT constrain the angular distribution of spectral mass. The angular distribution is set by the nonlinear dynamics (stretching + advection), which ARE anisotropic (they prefer to create perpendicular spectral structure for tube-like vorticity). But the anisotropy of the nonlinear term is geometry-dependent, not viscosity-dependent.

### 4.5 Revised understanding: the angular suppression is GEOMETRIC, not VISCOUS

The suppression of D_xi S for tube-like vorticity (|D_xi S| ~ kappa |omega| rather than |omega|^{3/2}/nu^{1/2}) is a consequence of the TUBE GEOMETRY, not of viscous spectral angular diffusion. The tube geometry causes:

1. Spectral mass to concentrate perpendicular to xi (because the physical vorticity is localized in the transverse plane).
2. The D_xi S multiplier (which weights by cos(phi)) to be suppressed by the angular concentration ratio ~ kappa r_c.

The viscous term's role is LIMITED to:
- Setting the core radius r_c = (nu/|omega|)^{1/2}, which determines the dissipation scale.
- Maintaining the steady-state Gaussian core profile (for the Burgers vortex).
- Damping fluctuations that would disrupt the tube structure.

But it does NOT produce an additional logarithmic correction to the angular distribution.

---

## 5. The Logarithmic Integral from the Angular Distribution

### 5.1 Revisiting Step 6 from the outline

The outline claimed that the integral

    I = integral_0^{pi/2} cos(phi) * (kappa r_c)^2 sin^2(phi) / (cos^2(phi) + (kappa r_c)^2) dphi

produces a logarithmic factor. Let us compute this carefully.

Setting epsilon = kappa r_c and making the substitution u = cos(phi):

    du = -sin(phi) dphi,  sin^2(phi) = 1 - u^2

    I = integral_0^1 u * epsilon^2 (1 - u^2) / (u^2 + epsilon^2) * (1/sin(phi)) du

Wait -- this substitution does not simplify cleanly because of the measure factor. Let me use the substitution psi = pi/2 - phi (angle from the perpendicular plane):

    cos(phi) = sin(psi) ~ psi for small psi
    sin(phi) = cos(psi) ~ 1
    dphi = -dpsi

    I = integral_0^{pi/2} sin(psi) * epsilon^2 * cos^2(psi) / (sin^2(psi) + epsilon^2) cos(psi) dpsi

For epsilon << 1, the dominant contribution comes from psi ~ epsilon. Setting t = psi/epsilon:

    I ~ integral_0^{1/epsilon} epsilon t * epsilon^2 * 1 / (epsilon^2 t^2 + epsilon^2) * 1 * epsilon dt
      = integral_0^{1/epsilon} epsilon^4 t / (epsilon^2 (t^2 + 1)) dt
      = epsilon^2 integral_0^{1/epsilon} t / (t^2 + 1) dt
      = epsilon^2 * (1/2) log(1 + 1/epsilon^2)
      = epsilon^2 * log(1/epsilon)

(up to factors of order 1).

**Yes, there IS a logarithmic factor in the angular integral.** The integral produces:

    I ~ (kappa r_c)^2 * log(1/(kappa r_c))

### 5.2 Where does this logarithm enter the D_xi S estimate?

The D_xi S integral involves a convolution of the vorticity spectrum with the CZ kernel. The precise form is:

    D_xi S(x) = PV integral (xi . nabla_x) K(x - y) omega(y) dy

In Fourier space, the relevant angular integral (at fixed |k|) is:

    (D_xi S contribution at scale |k|) ~ integral_{S^2} cos(phi) * (angular CZ kernel) * |hat{omega}(k, phi)|^2 d sigma(phi)

The angular CZ kernel for the Biot-Savart strain gradient has a more complex angular structure than a simple cos(phi), but the leading-order angular dependence is captured by cos(phi) (the projection onto xi).

**However**, the computation in Section 3.2 already accounted for the angular integral and produced:

    <cos(phi)>_E ~ 2 kappa r_c / pi

without a logarithmic factor. Where is the discrepancy?

The logarithmic factor in Section 5.1 came from using a DIFFERENT angular profile -- specifically, (kappa r_c)^2 sin^2(phi) / (cos^2(phi) + (kappa r_c)^2) -- compared to the Lorentzian-squared profile (kappa r_c)^2 / (cos^2(phi)/(kappa r_c)^2 + 1)^2 used in Section 3.2. These have different tails:

- The Lorentzian-squared falls as cos^{-4}(phi) at small phi (strong suppression)
- The linear Lorentzian falls as cos^{-2}(phi) at small phi (weaker suppression)
- The profile with the sin^2(phi) factor in the numerator has different behavior near phi = pi/2

The discrepancy arises because the outline's Step 6 used a simplified angular profile. The more careful computation in Section 3.2 (with the Lorentzian-squared profile, which correctly accounts for the Fourier transform of a Lorentzian tube profile in z) gives a cleaner result without the logarithm.

### 5.3 Can a logarithm arise from a different mechanism?

Consider the Biot-Savart integral for D_xi S not in Fourier space but in physical space:

    D_xi S(x_*) = PV integral (xi . nabla) K(x_* - y) omega(y) dy

Decompose the integral into shells by distance r = |x_* - y|:

    D_xi S = integral_0^{infty} F(r) dr/r

where F(r) is the contribution from the shell at distance r. For a tube of radius r_c and curvature kappa:

- At r << r_c: inside the core. The kernel is smooth, and F(r) ~ |omega| * r (from the near-field expansion).
- At r_c << r << 1/kappa: outside the core but inside the radius of curvature. The vorticity is essentially zero (Gaussian roll-off), so F(r) is exponentially small.
- At r ~ 1/kappa: the tube curves, and the vorticity from adjacent segments of the tube contributes. F(r) ~ kappa |omega| r_c^2 / r^2.
- At r >> 1/kappa: the contribution from distant tube segments. F(r) ~ |omega| r_c^2 / r^2 (from the far-field Biot-Savart).

The integral integral_{r_c}^{1/kappa} F(r) dr/r involves the gap between the core and the curvature scale. The integrand is exponentially small in this range (because the Gaussian core cuts off at r_c). There is NO power-law intermediate regime, and hence NO logarithmic integral.

**Contrast with the LIA velocity:** The self-induction velocity of a vortex filament involves:

    v_{LIA} = (Gamma / 4 pi) integral_tube (x_* - y) x omega(y) / |x_* - y|^3 dy

For this integral, the intermediate range r_c << r << 1/kappa contributes a logarithmic factor log(1/(kappa r_c)) because the integrand decays as 1/r (not exponentially). This is the classical Biot-Savart logarithm for the filament velocity.

For D_xi S, the kernel involves SECOND derivatives (one extra power of 1/r), making the integrand F(r)/r ~ 1/r^3 in the intermediate range. But the vorticity support is concentrated at r ~ r_c, so the intermediate range is void.

**However**, if we consider the D_xi S contribution from the tube's own curvature (the self-induced strain gradient), the computation involves:

    (D_xi S)_{self} ~ integral_{r_c}^{1/kappa} (d/dr)[kappa-induced flow] * (vorticity at distance r) dr

The kappa-induced flow variation at distance r from the tube center is ~ Gamma kappa / r, and its gradient is ~ Gamma kappa / r^2. The vorticity at distance r is the core Gaussian omega_z(r) ~ |omega|_{max} exp(-r^2/r_c^2). So:

    F(r) ~ Gamma kappa r^{-2} * |omega|_{max} exp(-r^2/r_c^2)

For r >> r_c, this is exponentially small. The integral is dominated by r ~ r_c:

    (D_xi S)_{self} ~ Gamma kappa / r_c^2 * |omega|_{max} * r_c ~ kappa |omega|_{max} (Gamma/r_c)

Using Gamma ~ |omega| r_c^2: (D_xi S)_{self} ~ kappa |omega|_{max}^2 r_c. Hmm, this has an extra power of |omega| r_c = |omega| (nu/|omega|)^{1/2} = (|omega| nu)^{1/2}. Let me recheck.

For the Burgers vortex: Gamma = 2 pi Re_Gamma nu, omega_max = alpha Re_Gamma / 2, r_c = (4 nu/alpha)^{1/2}.

    Gamma / r_c^2 = 2 pi Re_Gamma nu / (4 nu/alpha) = pi alpha Re_Gamma / 2 = pi omega_max

So Gamma kappa / r_c^2 = pi kappa omega_max. And:

    (D_xi S)_{self} ~ kappa omega_max * integral_{r_c}^{infty} f(r/r_c) dr

where f is a function involving the core profile. The integral gives a constant (no logarithm) because the core profile is Gaussian.

**Conclusion:** For the Gaussian-core (Burgers) vortex, there is NO logarithmic factor in D_xi S from the self-induced strain gradient. The result is:

    |D_xi S|_{self} ~ C kappa |omega|

with C a dimensionless constant, confirming the result of Section 3.

### 5.4 When does a logarithm appear?

A logarithmic factor log(1/(kappa r_c)) DOES appear in:
1. The filament velocity (LIA): v ~ (Gamma kappa / 4 pi) log(1/(kappa r_c))
2. The self-induced rotation of the Frenet frame

But it does NOT appear in D_xi S because D_xi S involves higher-order derivatives of the velocity field, which are dominated by the near-core contribution (r ~ r_c) rather than the intermediate range (r_c << r << 1/kappa).

The logarithm in the LIA velocity comes from the 1/r decay of the Biot-Savart integrand, which produces a logarithmic integral over the intermediate range. For D_xi S, the integrand decays as 1/r^3 (or faster), which produces a convergent integral without a logarithm.

---

## 6. The Tube-Tube Interaction Problem

### 6.1 Where the angular suppression breaks down

The angular suppression of D_xi S relies on the spectral mass of omega being concentrated perpendicular to xi. This is true for a SINGLE tube viewed at its own vorticity maximum. But when a second tube (tube B) approaches tube A at distance d ~ r_c with a different vorticity direction xi_B != xi_A, the spectral mass of tube B's vorticity is concentrated perpendicular to xi_B, NOT perpendicular to xi_A.

The D_xi_A S contribution from tube B at the core of tube A involves:

    (D_{xi_A} S_B)(x_A) ~ integral (xi_A . nabla) K(x_A - y) omega_B(y) dy

Tube B's vorticity is concentrated along xi_B, so its Fourier spectrum is concentrated perpendicular to xi_B. The D_{xi_A} multiplier picks up cos(angle(k, xi_A)). If xi_A and xi_B are not aligned, the spectral mass of tube B at angle phi from xi_A is NOT suppressed -- it is distributed broadly (peaked at angle pi/2 - angle(xi_A, xi_B) from xi_A).

For tubes with angle Theta between their axes (0 < Theta < pi/2):

    (D_{xi_A} S_B)_{interaction} ~ sin(Theta) * |omega_B| * Gamma_B / d^3

where d is the inter-tube distance. At d ~ r_c:

    |(D_{xi_A} S_B)| ~ sin(Theta) * |omega| * |omega| r_c^2 / r_c^3 = sin(Theta) * |omega|^2 / (|omega|/nu)^{1/2} * ... 

Let me be more careful. The CZ kernel for nabla^2 u at distance d is ~ 1/d^4. The vorticity source from tube B at distance d has magnitude ~ |omega_B| * r_c^2 (the total vorticity times the cross-section area). So:

    |(D_{xi_A} S)_{from B}| ~ (1/d^4) * |omega_B| * r_c^2 * d^3 (from the volume element in the integral)

Wait, this is not right. Let me use the Biot-Savart representation directly.

The strain at point x due to a vortex tube B passing at closest distance d is:

    S ~ (Gamma_B / d^2) * (geometric factor)

The strain gradient in the xi_A direction:

    D_{xi_A} S ~ (Gamma_B / d^3) * sin(Theta)

where sin(Theta) accounts for the angular mismatch (if xi_A is parallel to the tube B axis, D_{xi_A} S is suppressed by the same mechanism as the single-tube case).

At d ~ r_c:

    |D_{xi_A} S|_{interaction} ~ Gamma_B / r_c^3 * sin(Theta) ~ |omega_B| r_c^2 / r_c^3 * sin(Theta)
                                = |omega_B| / r_c * sin(Theta) = |omega_B|^{3/2} / nu^{1/2} * sin(Theta)

**This is the FULL dimensional estimate |omega|^{3/2}/nu^{1/2}**, multiplied only by sin(Theta). For non-parallel tubes (Theta = O(1)), the interaction D_xi S reaches the CZ bound with no suppression.

### 6.2 The angular suppression provides NO gain for tube-tube interactions

The spectral angular suppression mechanism works for the SELF-INDUCED contribution of a tube (where the spectral alignment between the source vorticity and the D_xi direction is guaranteed by the shared geometry). For tube-tube interactions, the spectral alignment is broken, and the D_xi S contribution has the full dimensional magnitude.

This is the same conclusion reached by Path 3 (Hasimoto + LIA) in three-practical-paths.md: single-tube estimates give D_xi S ~ kappa |omega| (well below the threshold), but tube-tube interactions at distance d ~ r_c give D_xi S ~ |omega|^{3/2}/nu^{1/2} (at the threshold).

### 6.3 Can the entropic argument constrain tube-tube interactions?

The original Moonshot 1 thesis was that the cumulative viscous history constrains the angular spectrum of the ENTIRE vorticity field, not just individual tubes. If this global constraint limits the spectral energy at angles near xi_A for all contributions (including from tube B), it could suppress the interaction term.

But Section 4.4 showed that the viscous term does NOT cause angular diffusion in Fourier space. The angular distribution of |hat{omega}(k)|^2 is determined by the nonlinear dynamics, not by viscosity. The viscous term damps all angular modes at the same rate (at fixed |k|).

Therefore, the global angular distribution of the vorticity spectrum is NOT constrained by the viscous history in a way that helps. Two tubes approaching each other at distance r_c with angle Theta between their axes can produce D_xi S of order |omega|^{3/2}/nu^{1/2} * sin(Theta), and there is no viscous mechanism that prevents this.

### 6.4 Is there a constraint from enstrophy dissipation?

The total enstrophy dissipation integral integral_0^T nu ||nabla omega||_{L^2}^2 dt is finite for smooth solutions. During a tube-tube interaction event of duration Delta t ~ 1/|omega| (the eddy turnover time at the interaction scale), the enstrophy dissipation is at least:

    nu * |nabla omega|^2 * Volume * Delta t ~ nu * (|omega|/r_c)^2 * r_c^3 * (1/|omega|) = nu * |omega| * r_c

This is the baseline dissipation from the individual tubes. The interaction could enhance this by creating steeper gradients (sheet-like structures between the tubes), but it ALSO enhances |D_xi S|. The ratio:

    |D_xi S|^2 / (nu |nabla omega|^2) ~ (|omega|^3/nu) / (nu * |omega|^2/r_c^2) = |omega| r_c^2 / nu^2 = 1/nu

This ratio depends only on nu, not on |omega|. The enstrophy dissipation constraint cannot produce a |omega|-dependent suppression of D_xi S.

---

## 7. Summary of Attempt and Honest Verdict

### 7.1 What was computed

1. **Angular spectrum of the Burgers vortex (Section 1):** Confirmed that the straight Burgers vortex has spectral mass entirely perpendicular to xi, producing D_xi S = 0. This is the trivial case.

2. **Angular spectrum of the curved Burgers tube (Section 2):** Computed the spectral angular distribution for a tube with curvature kappa. The spectral mass at angles near xi is suppressed by (kappa r_c)^2 relative to the total.

3. **D_xi S for the curved tube (Section 3):** Computed the angular suppression factor for D_xi S:

    |D_xi S|_{single tube} ~ (2/pi) kappa r_c * |omega|^{3/2}/nu^{1/2} = (2/pi) kappa |omega|

   This reproduces the LIA estimate from Path 3, confirming the cross-validation between two independent methods.

4. **Viscous angular diffusion (Section 4):** Showed that the viscous term -nu |k|^2 hat{omega}(k) in Fourier space is isotropic and does NOT cause angular spreading of the spectrum. The angular distribution is set by the nonlinear dynamics, not by viscosity. **This falsifies the core mechanism of Moonshot 1** -- the claim that cumulative viscous history constrains the angular spectrum is incorrect. The viscous term constrains the amplitude (via the dissipation scale k_d), not the angular distribution.

5. **Logarithmic integral (Section 5):** Showed that the angular integral over a Lorentzian-type profile can produce a factor of (kappa r_c)^2 log(1/(kappa r_c)), but this logarithm does not appear in D_xi S for Gaussian-core tubes because the dominant contribution comes from the near-core region r ~ r_c, where the Gaussian cutoff eliminates the intermediate range that would produce the logarithm.

6. **Tube-tube interactions (Section 6):** Showed that the angular suppression is specific to the self-induced contribution of a single tube. For tube-tube interactions at distance d ~ r_c with angle Theta between axes, D_xi S reaches the full CZ magnitude |omega|^{3/2}/nu^{1/2} * sin(Theta). No viscous or enstrophy constraint prevents this.

### 7.2 Answers to the four questions from Step 9

**Q1: Does the entropic/spectral approach produce a log gain for single tubes?**

No. The approach produces a POWER-LAW gain (kappa r_c suppression), not a logarithmic one. The power-law gain is the same as Path 3's LIA result. No additional logarithmic correction arises from the viscous spectral history, because the viscous term does not cause angular diffusion in Fourier space.

A logarithmic factor log(1/(kappa r_c)) appears in the filament self-induction velocity (the classical LIA logarithm) but NOT in D_xi S, because D_xi S involves higher-order derivatives that are dominated by the near-core contribution.

**Q2: Does it say anything new about tube-tube interactions?**

No. The spectral angular suppression breaks down for tube-tube interactions because the spectral alignment between source vorticity and the D_xi direction is not maintained when the source tube has a different axis direction. The interaction D_xi S has the full CZ magnitude. No global viscous constraint on the angular spectrum helps, because viscosity does not cause angular spectral diffusion.

**Q3: What is the precise estimate?**

For a single Burgers tube with curvature kappa:

    |D_xi S|_{self} = C kappa |omega|

where C is a dimensionless constant. This is |omega|^{1+0}, far better than the Theorem CB threshold of |omega|^{3/2}/nu^{1/2}. But it is NOT the full story.

For two tubes interacting at distance d with angle Theta between axes:

    |D_xi S|_{interaction} ~ sin(Theta) |omega|^{3/2}/nu^{1/2}

which saturates the CZ bound (up to the geometric factor sin(Theta)).

**Q4: Does it close Theorem CB?**

**No.** The spectral angular suppression approach does NOT close Theorem CB. It provides the same information as Path 3: single-tube D_xi S is well-controlled, but tube-tube interactions at the core scale can reach the CZ bound. The "entropic" mechanism (cumulative viscous history constraining angular spectral distribution) is a mirage -- the viscous term is angularly isotropic in Fourier space and does not produce the claimed constraint.

### 7.3 What was learned

1. **The core thesis of Moonshot 1 is falsified.** The viscous term does not constrain the angular distribution of spectral mass. The angular distribution is determined by the nonlinear dynamics (tube geometry), and the viscous term only sets the dissipation scale. The "entropic" mechanism as stated is not operative.

2. **The cross-validation between spectral analysis and matched asymptotics is confirmed.** Two independent methods (Fourier angular analysis and physical-space Callegari-Ting asymptotics) produce the same estimate D_xi S ~ kappa |omega| for single tubes. This strengthens confidence in the single-tube estimate.

3. **The tube-tube interaction at d ~ r_c is definitively identified as the bottleneck.** Both the spectral approach and the matched asymptotic approach identify the same obstruction: when two high-vorticity tubes interact at distance comparable to the core radius, the angular suppression of D_xi S breaks down, and the CZ bound is saturated.

4. **The logarithmic factor from the LIA velocity does NOT transfer to D_xi S.** The classical log(1/(kappa r_c)) in the filament self-induction velocity arises from an intermediate-range integral that does not exist for D_xi S (because D_xi S involves higher-order derivatives that are dominated by the near-core region).

5. **No information-theoretic or entropic constraint on D_xi S has been found.** The attempt to use Shannon-type entropy or spectral entropy as a regularity tool has not produced bounds beyond what direct estimation gives. The fundamental issue is that entropy measures are insensitive to angular structure in Fourier space when the viscous operator is angularly isotropic.

### 7.4 Updated probability assessment

The original estimate was 8-12% for Moonshot 1. After the computation:

**Updated probability: < 1%.** The core mechanism (viscous angular spectral diffusion) is falsified. The approach reduces to the same single-tube estimate as Path 3, with no additional gain for the critical tube-tube interaction scenario. There is no viable path from the entropic/spectral framework to a logarithmic improvement of the CZ bound.

### 7.5 Comparison with the other approaches

| | Moonshot 1 (this document) | Path 3 (LIA/Hasimoto) | Path 1 (Directional cancellation) |
|---|---|---|---|
| Single-tube D_xi S | ~ kappa |omega| (confirmed) | ~ kappa |omega| (confirmed) | ~ kappa |omega| (expected) |
| Tube-tube D_xi S | ~ sin(Theta) |omega|^{3/2}/nu^{1/2} (no gain) | ~ sin(Theta) |omega|^{3/2}/nu^{1/2} (no gain) | Possible angular cancellation (untested) |
| Log gain mechanism | Viscous angular diffusion (FALSIFIED) | NLS integrability + matched asymptotics | Angular CZ kernel cancellation under alignment |
| Status | **KILLED** | Alive but blocked at tube-tube | Alive, first computation needed |

**The surviving approaches** are those that address the tube-tube interaction directly: Path 1 (which seeks angular cancellation in the CZ kernel when the interacting vorticity is aligned with e_2) and Path 2 (which uses variation-norm estimates that might bound the cumulative effect of D_xi S along vortex lines). Moonshot 1 and Path 3 both fail at the same point -- the tube-tube interaction at the core scale.

---

## 8. Salvageable Elements

Despite the failure of the core mechanism, the computation produced useful intermediate results:

1. **The angular spectral profile of a curved Burgers tube** (Section 2) is a clean, explicit calculation that can serve as a model for more detailed spectral analyses. The Lorentzian-squared profile in k_z with width kappa is a robust feature of thin-tube vorticity.

2. **The angular suppression ratio** R ~ (kappa r_c)^2 (Section 2.4) and the D_xi S suppression factor ~ kappa r_c (Section 3.2) provide quantitative confirmation that single-tube D_xi S is far below the blowup threshold. This is not new (it follows from LIA), but the Fourier-space derivation is independent and provides a different physical picture.

3. **The identification that viscosity is angularly isotropic in Fourier space** (Section 4.3-4.4) is a negative result with positive value: it eliminates a plausible-sounding but incorrect mechanism and clarifies what viscosity does and does not constrain in the spectral domain. This should be recorded to prevent future wasted effort on the same idea.

4. **The absence of a log factor in D_xi S** (Section 5.4), despite its presence in the LIA velocity, is a subtle point that distinguishes the regularity problem from the filament dynamics problem. The regularity problem requires controlling higher derivatives (D_xi S involves nabla^2 u), which are dominated by the near-core contribution and do not benefit from the long-range logarithmic integral.

---

## 9. Implications for the Overall NS Pursuit

The bottleneck is now clearly localized: **tube-tube interaction D_xi S at the core scale**. All three independent approaches (spectral angular analysis, matched asymptotics, and direct Biot-Savart estimation) agree on this.

The remaining question is whether there is a mechanism -- beyond single-tube geometry and beyond viscous spectral constraints -- that prevents two high-vorticity tubes from maintaining a close-range, non-parallel interaction for long enough to accumulate the D_xi S that would trigger blowup. This is a question about the DYNAMICS of tube-tube interaction, not about the SPECTRUM of individual tubes.

Possible avenues for the tube-tube interaction problem:
1. **Topological constraints:** Linked vortex tubes cannot pass through each other; reconnection dissipates energy and reduces curvature. Does the topology of vortex lines prevent sustained close-range non-parallel interaction?
2. **Strain-induced repulsion:** Two approaching tubes deform each other's cores, increasing the effective core radius r_c and reducing |omega|. Does this deformation prevent |D_xi S| from reaching the threshold?
3. **Time-integrated bounds:** Even if |D_xi S| can instantaneously reach |omega|^{3/2}/nu^{1/2} during a tube-tube interaction, the interaction has finite duration ~ 1/|omega|. Does the time-integrated effect on the coupled bootstrap remain subcritical?

These questions go beyond the scope of Moonshot 1 and are better addressed by Path 1 (angular CZ cancellation, which might provide instantaneous bounds during interaction) or Path 2 (variation-norm estimates, which naturally handle time-integrated effects).
