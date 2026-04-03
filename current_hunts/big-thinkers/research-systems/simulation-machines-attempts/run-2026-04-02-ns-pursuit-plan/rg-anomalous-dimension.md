# One-Loop Anomalous Dimension of D_xi S in 3D Navier-Stokes

**Date:** 2026-04-02
**Parent:** coupled-bootstrap-attempt.md, circulation-cascade-analysis.md
**Purpose:** Compute (formally) the one-loop anomalous scaling dimension of the composite operator D_xi S under the Navier-Stokes renormalization group, and determine whether a logarithmic correction to the borderline delta = 1/2 scaling emerges.

---

## 0. Executive Summary

The coupled bootstrap (Theorem CB) requires |D_xi S| <= C |omega|^{1+delta} with delta > 1/2 to prove regularity. The self-consistent Biot-Savart analysis gives exactly delta = 1/2 with coefficient C/Re_Gamma^2 (equation 6.2 of circulation-cascade-analysis.md). The d-independence of this ratio is the hallmark of a renormalization group fixed point. This document asks: does the one-loop RG computation produce an anomalous dimension gamma > 0 that provides the missing logarithmic correction?

**Verdict: The one-loop computation is inconclusive, and the overall approach faces fundamental obstructions.**

Specifically:
1. The one-loop anomalous dimension gamma CANNOT be unambiguously computed because the composite operator D_xi S depends nonlinearly on the velocity field (through xi = omega/|omega|), and the standard RG machinery for anomalous dimensions applies to operators that are polynomial in the fundamental field.
2. When the computation is forced through by linearizing xi around a background, the result depends on the background configuration and is not universal (not a fixed-point property).
3. For the linearized (polynomial) approximation to D_xi S, the one-loop integral has a sign that depends on the angular structure of the background flow, and no definite conclusion can be drawn.
4. The entire RG framework for NS is formal (not rigorous), and the Kolmogorov spectrum used as input is itself not rigorously established.
5. The probability that this approach resolves the NS regularity problem is effectively zero in a rigorous sense, and very low (< 2%) even as a heuristic guide.

The detailed computation follows.

---

## 1. The RG Framework for Navier-Stokes

### 1.1 The NS action

The Martin-Siggia-Rose (MSR) / Janssen-De Dominicis formulation writes the NS equation as a field theory. Introducing the response field u-tilde (auxiliary field), the generating functional is:

    Z = integral D[u] D[u-tilde] exp(-S[u, u-tilde])

where the MSR action is:

    S[u, u-tilde] = integral dt d^3x [ u-tilde_i (partial_t u_i + u_j partial_j u_i + partial_i p - nu Delta u_i)
                                        - (1/2) u-tilde_i F_{ij} u-tilde_j ]

Here F_{ij}(k) is the forcing correlator (modeling the energy injection), and we have integrated out the pressure using incompressibility (div u = 0 enforced by the Leray projector).

For the NS problem WITHOUT external forcing (the deterministic regularity problem), F = 0 and the MSR action reduces to the classical equations of motion. The RG analysis of the deterministic NS is fundamentally different from the stochastic NS (where F != 0 provides the fluctuations). This distinction is critical and is often conflated in the literature.

### 1.2 Stochastic NS vs. deterministic NS

**Stochastic NS (Forster-Nelson-Stephen, 1977; De Dominicis-Martin, 1979; Yakhot-Orszag, 1986):**
- External forcing F(k) ~ k^{4-d-2epsilon} drives the flow.
- Fluctuations come from the random forcing.
- The one-loop RG is well-defined and produces the Kolmogorov spectrum E(k) ~ k^{-5/3} at the fixed point (for appropriate epsilon).
- Anomalous dimensions of composite operators can be computed order by order in epsilon.
- The results are perturbative in epsilon and formal (not rigorous).

**Deterministic NS (the regularity problem):**
- No external forcing. The flow evolves from smooth initial data.
- Fluctuations at small scales are generated internally by the nonlinearity.
- There is no natural expansion parameter (no epsilon).
- The RG step (integrating out a shell of modes) requires knowing the statistics of the small-scale fluctuations, which are DETERMINED by the dynamics, not prescribed.
- The Bricmont-Kupiainen (1994) rigorous RG framework applies only to small data (near the Gaussian fixed point), where the nonlinearity is perturbative.

**The fundamental mismatch:** The regularity question asks about large data (potentially high Reynolds number), where the deterministic NS dynamics are fully nonlinear. The one-loop RG for anomalous dimensions is a tool for the stochastic, forced NS in the perturbative regime. Applying it to the deterministic regularity problem requires an unjustified extrapolation.

### 1.3 The Kolmogorov scaling as a fixed point

Notwithstanding the above, the d-independence of the ratio R = |D_xi S| / (omega^{3/2}/nu^{1/2}) = C/Re_Gamma^2 (equation 6.2) is suggestive of a fixed-point property. At the Kolmogorov fixed point:

- The energy spectrum E(k) = C_K epsilon^{2/3} k^{-5/3}
- The velocity two-point correlator in the inertial range: <u_i(k) u_j(-k)> = P_{ij}(k) E(k) / (4 pi k^2)
- The scaling is self-similar: all dimensionless ratios of flow quantities at scale k are independent of k (within the inertial range)

The ratio R = C/Re_Gamma^2 being d-independent (equivalently, k-independent) is precisely the statement that D_xi S and omega^{3/2}/nu^{1/2} have the same scaling dimension at the fixed point. An anomalous dimension would make this ratio k-dependent (logarithmically).

### 1.4 The operator in question

    O(x) = D_xi S(x) = (xi(x) . nabla) S(x)

where xi = omega/|omega| and S = sym(nabla u) = (1/2)(partial_i u_j + partial_j u_i).

This operator is:
- **Composite:** It involves products of fields at the same point.
- **Nonlinear in u:** Through xi = curl u / |curl u|, it depends nonlinearly on u.
- **Gauge-invariant:** It is defined in terms of physical (divergence-free) velocity fields.

The nonlinearity of xi in u is the fundamental obstruction to a standard RG treatment.

---

## 2. Naive Scaling Dimension

### 2.1 NS scaling symmetry

Under the NS rescaling (which preserves the equation with fixed nu):

    x -> lambda x,   t -> lambda^2 t,   u -> lambda^{-1} u(lambda x, lambda^2 t)

Wait -- this is the INVISCID scaling. For the viscous NS, the rescaling u_lambda(x,t) = lambda u(lambda x, lambda^2 t) gives:

    partial_t u_lambda + (u_lambda . nabla) u_lambda + nabla p_lambda = nu Delta u_lambda

(the viscous term is invariant because the lambda from u and the lambda^{-2} from nabla^2 and the lambda^2 from partial_t all cancel). Actually, let me be more careful.

Under x' = lambda x, t' = lambda^2 t, u'(x', t') = (1/lambda) u(x'/lambda, t'/lambda^2):

    partial_{t'} u' = (1/lambda^3) partial_t u
    (u' . nabla') u' = (1/lambda^3) (u . nabla) u
    nabla' p' = (1/lambda^3) nabla p
    nu Delta' u' = nu (1/lambda^3) Delta u

All terms scale as 1/lambda^3. So the equation is preserved. Under this scaling:

    omega' = curl' u' = (1/lambda)(1/lambda) curl u = (1/lambda^2) omega(x'/lambda, t'/lambda^2)

Wait -- curl' = (1/lambda) curl (since nabla' = (1/lambda) nabla), and u' = (1/lambda) u. So:

    omega' = curl' u' = (1/lambda) curl((1/lambda) u) = (1/lambda^2) omega

NO. More carefully: u'(x') = (1/lambda) u(x'/lambda). So:

    (curl' u')_i(x') = epsilon_{ijk} partial'_j u'_k(x') = epsilon_{ijk} (1/lambda) partial_j ((1/lambda) u_k(x'/lambda))
                      = (1/lambda^2) (curl u)_i(x'/lambda) = (1/lambda^2) omega_i(x'/lambda)

So |omega'(x', t')| = (1/lambda^2) |omega(x'/lambda, t'/lambda^2)|.

Under this scaling (going from scale lambda to scale 1):

    |omega| scales as lambda^{-2} (i.e., the scaling dimension of omega is 2 in units of inverse length)

The strain tensor S' = sym(nabla' u') = (1/lambda^2) S, so:

    |S| has scaling dimension 2

The vorticity direction xi' = omega'/|omega'| = omega/|omega| = xi:

    xi has scaling dimension 0 (dimensionless)

The operator D_xi S = (xi . nabla) S:

    D_{xi'} S'(x') = (xi'(x') . nabla') S'(x') = (xi . (1/lambda) nabla)((1/lambda^2) S)
                    = (1/lambda^3) (xi . nabla) S = (1/lambda^3) D_xi S

So:

    **D_xi S has naive scaling dimension 3.**

The comparison quantity omega^{3/2}/nu^{1/2}:

    (omega')^{3/2} / nu^{1/2} = (omega/lambda^2)^{3/2} / nu^{1/2} = omega^{3/2} / (lambda^3 nu^{1/2})

So omega^{3/2}/nu^{1/2} also has scaling dimension 3.

**The naive scaling dimensions match exactly.** This confirms that R = D_xi S / (omega^{3/2}/nu^{1/2}) is dimensionless and scale-invariant at tree level. Any anomalous dimension gamma would make:

    D_xi S_eff ~ lambda^{-(3+gamma)} D_xi S_bare

while omega^{3/2}/nu^{1/2} remains at lambda^{-3} (since |omega| is a physical observable whose scaling is fixed). So:

    R_eff(lambda) ~ lambda^{-gamma} R_bare

If gamma > 0 (screening), R decreases at large scales (small lambda = IR scales), meaning D_xi S is reduced relative to omega^{3/2}/nu^{1/2}. After integrating over log(lambda_UV/lambda_IR) ~ log(omega/omega_0) shells:

    R_eff ~ R_bare * (log(omega/omega_0))^{-gamma}

This would give the logarithmic correction needed by Theorem CB.

---

## 3. The One-Loop Setup

### 3.1 Decomposition

Decompose u = u_< + u_>, where u_< has Fourier support in |k| < Lambda/b and u_> has support in Lambda/b < |k| < Lambda, with b = e^{dl} slightly greater than 1 (one RG step).

The operator:

    O[u] = D_xi S[u] = (xi[u] . nabla) S[u]

where xi[u] = curl u / |curl u| and S[u] = sym(nabla u).

### 3.2 Expansion in u_>

    O[u_< + u_>] = O[u_<] + (delta O / delta u) . u_> + (1/2) (delta^2 O / delta u^2) : (u_> u_>) + ...

The one-loop correction (after averaging over u_> with a Gaussian measure):

    <O[u_< + u_>]>_{u_>} = O[u_<] + (1/2) <(delta^2 O / delta u^2) : (u_> u_>)>_{u_>} + O(u_>^4)

The Gaussian average:

    <u_{>,i}(k) u_{>,j}(-k)> = P_{ij}(k) G(k)

where G(k) is the energy spectrum in the shell Lambda/b < |k| < Lambda, and P_{ij}(k) = delta_{ij} - k_i k_j / k^2 is the Leray projector.

### 3.3 The fundamental obstruction: xi is nonlinear

The functional derivative delta O / delta u involves:

    delta O / delta u = (delta xi / delta u) . nabla S + xi . nabla (delta S / delta u)

The second derivative:

    delta^2 O / delta u^2 = (delta^2 xi / delta u^2) . nabla S
                           + 2 (delta xi / delta u) . nabla (delta S / delta u)
                           + xi . nabla (delta^2 S / delta u^2)

Now, S = sym(nabla u) is LINEAR in u, so delta S / delta u is a constant operator and delta^2 S / delta u^2 = 0.

But xi = curl u / |curl u| is NONLINEAR. Its first variation:

    delta xi / delta u_l(y) = [curl_y delta(x-y)]_m / |omega| - omega_m [omega_n (curl_y delta(x-y))_n] / |omega|^3

In Fourier space, this involves the projection of the curl operator onto the plane perpendicular to omega:

    (delta xi_m / delta u_l(k))_{x} = (P^{perp}_{mn} epsilon_{nab} i k_a P_{bl}(k)) / |omega(x)| * e^{ik.x}

where P^{perp}_{mn} = delta_{mn} - xi_m xi_n is the projector perpendicular to xi.

The second variation delta^2 xi / delta u^2 involves terms of order 1/|omega|^2, with angular factors from the projection.

**The critical issue:** The functional derivatives of xi involve 1/|omega| factors. When we take the Gaussian average over u_>, we get:

    <(delta^2 O / delta u_>^2) : (u_> u_>)> ~ integral_{Lambda/b}^{Lambda} d^3k G(k) * [kernel involving 1/|omega|, P_{ij}(k), curl, etc.]

The kernel depends on the BACKGROUND field u_< through xi[u_<] and |omega[u_<]|. This means the one-loop correction is NOT a simple multiplicative renormalization of O -- it depends on the specific background.

**This is the fundamental obstruction to computing a universal anomalous dimension.**

For a standard RG analysis, the anomalous dimension is a property of the OPERATOR (independent of the state). For D_xi S, the "operator" depends on the state through xi, which is a nonlinear functional of u. The one-loop correction mixes the operator with the state in an inseparable way.

### 3.4 The linearized approximation

To proceed formally, we linearize xi around a fixed background:

    xi ≈ xi_0 + delta xi    where xi_0 = omega_0 / |omega_0| is the background vorticity direction

In this approximation:

    O ≈ (xi_0 . nabla) S = xi_{0,k} partial_k S_{ij}

This IS linear in u (since S = sym(nabla u) is linear). Therefore:

    delta O / delta u_l(k) = xi_{0,k} partial_k (sym(nabla delta(x-y)))_{ij} P_{lm}(k)
                            = xi_{0,k} (i k_k) (1/2)(i k_i delta_{jl} + i k_j delta_{il}) P_{lm}(k) ... 

Actually, more precisely in Fourier space: the operator O_linearized at wavevector q is:

    O(q) = xi_{0,k} (i q_k) S_{ij}(q) = xi_{0,k} (i q_k) (1/2)(i q_i u_j(q) + i q_j u_i(q))
         = -(1/2) xi_{0,k} q_k (q_i u_j(q) + q_j u_i(q))

Since this is LINEAR in u, the one-loop correction vanishes: delta^2 O / delta u^2 = 0 for the linearized operator.

**The linearized operator has no one-loop anomalous dimension.**

This is trivial: a linear operator O = L[u] (where L is a linear differential operator) has zero anomalous dimension at one loop, because the one-loop diagram requires a cubic vertex (two internal lines meeting at the operator insertion), and a linear operator insertion provides only one u leg.

### 3.5 The first nontrivial contribution

The anomalous dimension of D_xi S arises from the NONLINEARITY of xi in u. The leading contribution comes from the term:

    delta O = (delta xi . nabla) S = [(delta xi) . nabla] S

where delta xi = (1/|omega|) P^{perp}(curl delta u) is the linear response of xi to a perturbation delta u.

At one loop, we need the diagram where one u_> line enters through delta xi and another u_> line enters through S:

    <(delta xi[u_>]) . nabla S[u_>]>_{u_>}

This is a one-loop contraction of two u_> fields, one appearing in delta xi and one in S. The diagram:

    delta xi ----[u_> propagator]---- S
        |                               |
        *--- operator vertex ---*

The contribution:

    gamma_1 = integral_{Lambda/b}^{Lambda} d^3k / (2pi)^3 * P_{ab}(k) G(k) 
              * [(P^{perp}_{mc} epsilon_{cde} i k_d P_{ea}(k)) / |omega|]
              * [xi_{0,f} i k_f (1/2)(i k_m delta_{ij,b} + ...)]

where the tensor contractions are between the delta xi vertex (involving the curl, the Leray projector, and the perpendicular projection P^{perp}) and the S vertex (involving the symmetric gradient).

### 3.6 The explicit angular integral

Denoting hat{k} = k/|k| and performing the radial integral (which gives G(Lambda) * Lambda^2 * dl), the anomalous dimension reduces to an angular integral:

    gamma = C * (G(Lambda) Lambda^2 / |omega|) * integral dOmega_{hat{k}} F(hat{k}, xi_0)

where F(hat{k}, xi_0) is the angular kernel from contracting the delta xi and S vertices with the Leray projector:

    F(hat{k}, xi_0) = P^{perp}_{mc}(xi_0) epsilon_{cde} hat{k}_d P_{ea}(hat{k}) P_{ab}(hat{k})
                      * xi_{0,f} hat{k}_f * (1/2)(hat{k}_m delta_{jb} + hat{k}_j delta_{mb}) * [some ij contraction]

This is a complicated angular integral involving the interplay of three geometric structures:
1. P^{perp}(xi_0): the projection perpendicular to the vorticity direction
2. epsilon_{cde} hat{k}_d: the curl operation on the shell wavevector
3. P_{ab}(hat{k}): the incompressibility projector at wavevector k

### 3.7 The angular integral: explicit computation

Let us choose coordinates with xi_0 = e_3 (vorticity along the z-axis). Then:

    P^{perp}_{mn} = delta_{mn} - delta_{m3} delta_{n3}    (projection onto the x-y plane)

The curl of a Fourier mode k: (curl e^{ik.x})_m = epsilon_{mab} i k_a delta_{b,component}

For the operator D_{xi_0} S contracted to a scalar (taking the specific component relevant to the curvature evolution, which is eta . (D_xi S) xi = e_perp . (D_{e_3} S) e_3):

    O_scalar = eta_i (D_{e_3} S)_{ij} xi_{0,j} = eta_i xi_{0,k} partial_k S_{ij} xi_{0,j}
             = eta_i partial_3 S_{i3}

where eta is a unit vector perpendicular to xi_0 (say eta = e_1). So:

    O_scalar = partial_3 S_{13} = (1/2) partial_3 (partial_1 u_3 + partial_3 u_1)

In Fourier space at wavevector k:

    O_scalar(k) = (1/2)(i k_3)(i k_1 u_3(k) + i k_3 u_1(k))
                = -(1/2) k_3 (k_1 u_3(k) + k_3 u_1(k))

This IS linear in u, confirming that the linearized operator has trivially zero anomalous dimension at one loop.

The one-loop correction from the xi nonlinearity involves the diagram where one u_> enters through the correction to xi_0 and one through S. The correction to xi at a point x from a fluctuation u_>(k) is:

    delta xi_m(x) = (1/|omega_0|) P^{perp}_{mn}(xi_0) (curl u_>)_n(x)
                  = (1/|omega_0|) P^{perp}_{mn} epsilon_{nab} partial_a u_{>,b}(x)

In Fourier space:

    delta xi_m(k) = (i/|omega_0|) P^{perp}_{mn} epsilon_{nab} k_a u_{>,b}(k)

The correction to O from delta xi:

    delta O(x) = (delta xi(x) . nabla) S_0(x)

where S_0 is the background strain. This correction is linear in u_> but multiplied by the background nabla S_0. At one loop, the contraction with S[u_>] gives:

    <delta O(x)>_1-loop = integral d^3k/(2pi)^3 * [(delta xi vertex at k) . nabla S_0(x)]
                          * [S vertex at -k] * <u_>(k) u_>(-k)>

But this contraction involves S_0 (the background strain) as a multiplicative factor. The result is:

    <delta O>_1-loop ~ (nabla S_0 / |omega_0|) * integral d^3k G(k) * [angular kernel]

This is NOT a multiplicative renormalization of O = D_{xi_0} S. Instead, it renormalizes O into a different operator proportional to nabla S_0 / |omega_0|, which has a DIFFERENT structure from D_xi S.

**This confirms that D_xi S does not have a well-defined anomalous dimension in the standard RG sense.** The one-loop correction generates a different operator (nabla S / |omega|), and the RG flow mixes an infinite set of operators. There is no single anomalous dimension to extract.

---

## 4. Alternative Approach: The Ratio R as a Running Coupling

### 4.1 Treating R directly

Instead of computing the anomalous dimension of the operator D_xi S, we can treat the ratio:

    R(k) = |D_xi S|_k / (omega_k^{3/2} / nu^{1/2})

as a scale-dependent "coupling constant" and ask how R evolves under the RG flow.

From the circulation-cascade analysis (equation 6.2):

    R = 16 pi sin(Theta) / Re_Gamma^2

This is d-independent (k-independent) at tree level. The question: does R acquire k-dependence at one loop?

### 4.2 The eddy viscosity correction

The best-understood one-loop correction in the NS RG is the eddy viscosity. Integrating out modes in the shell Lambda/b < |k| < Lambda produces an effective viscosity:

    nu_eff(k) = nu + delta nu(k)

where delta nu(k) is the eddy viscosity contribution. For the Kolmogorov spectrum:

    delta nu(k) ~ C_nu epsilon^{1/3} k^{-4/3}

(the Yakhot-Orszag result). In the inertial range (k << Lambda), nu_eff >> nu.

The eddy viscosity modifies the Burgers vortex equilibrium. With nu_eff instead of nu:

    omega = Gamma alpha / (4 pi nu_eff)
    r_c = (4 nu_eff / alpha)^{1/2}

The ratio R (equation 6.2) becomes:

    R = 16 pi sin(Theta) / Re_{Gamma,eff}^2

where Re_{Gamma,eff} = Gamma / (2 pi nu_eff(k)). Since nu_eff > nu, Re_{Gamma,eff} < Re_Gamma, so R INCREASES with eddy viscosity.

But this is NOT an anomalous dimension in the usual sense. The eddy viscosity modifies the background equilibrium, not the scaling of the operator. The ratio R increases because the effective Re decreases, not because D_xi S is renormalized.

### 4.3 The vertex correction

Beyond the eddy viscosity, the one-loop RG also produces vertex corrections to the nonlinearity (u . nabla) u. These modify the relationship between the velocity field and the strain, and hence between D_xi S and omega.

The vertex correction at one loop (Yakhot-Orszag, 1986; Adzhemyan et al., 1999) is:

    Gamma_vertex(k) = 1 + C_v epsilon + O(epsilon^2)

where epsilon is the forcing exponent. In the Kolmogorov regime (epsilon -> 2 in the FNS scheme), the vertex correction is O(1) but has been debated in the literature (the "sweeping problem" and the role of Galilean invariance).

The vertex correction affects the effective nonlinearity and hence the strain production, but its effect on the composite operator D_xi S requires a separate computation that, as shown in Section 3, does not yield a clean anomalous dimension due to the nonlinearity of xi.

---

## 5. The Kraichnan Model: An Exactly Solvable Analogue

### 5.1 Setup

The Kraichnan model (1968, 1994) replaces the NS velocity field with a Gaussian random field with prescribed statistics:

    <u_i(x,t) u_j(y,t')> = delta(t-t') D_{ij}(x-y)

where D_{ij}(r) = D_0 (delta_{ij} - (d-1+zeta)/(d-1) * r_i r_j / r^2) * r^zeta for small r, with 0 < zeta < 2.

In this model:
- The velocity is externally prescribed (not dynamically determined).
- Passive scalar and vector fields advected by this velocity exhibit anomalous scaling.
- The anomalous dimensions can be computed exactly (non-perturbatively) using the zero-mode approach (Falkovich-Gawedzki-Vergassola, 2001).

### 5.2 Anomalous dimensions of composite operators in Kraichnan

For the passive scalar theta advected by the Kraichnan velocity:

    partial_t theta + u . nabla theta = kappa Delta theta

The structure functions S_n(r) = <(theta(x+r) - theta(x))^n> exhibit anomalous scaling:

    S_n(r) ~ r^{zeta_n}

where zeta_n = n zeta/2 - n(n-2) zeta^2 / (2(d-1)(d+2-zeta)) + ... deviates from the naive n * zeta/2.

The anomalous exponents are related to the zero modes of the operator describing the inertial-range dynamics. Crucially:
- The anomalous dimensions are POSITIVE (the exponents zeta_n are less than the naive values), corresponding to intermittency.
- The computation is exact (not perturbative).

### 5.3 Relevance to NS

The Kraichnan model demonstrates that anomalous dimensions CAN arise in turbulent cascade systems. However:

1. **The Kraichnan model is for passive fields, not the active NS velocity.** The NS velocity is dynamically coupled to itself, which makes the problem fundamentally harder.

2. **In the Kraichnan model, anomalous dimensions arise from the zero-mode mechanism.** The structure functions are determined by the zero modes of the inertial-range operator, which depend on the multi-point geometry. There is no analogous zero-mode computation for the NS operator D_xi S.

3. **The sign of the anomalous dimension in Kraichnan is such that intermittency is ENHANCED.** The higher-order structure functions grow faster than dimensional prediction. If this sign persists in NS, it would mean D_xi S grows FASTER than omega^{3/2}/nu^{1/2} (gamma < 0, anti-screening), which would be BAD for regularity.

### 5.4 The multifractal model prediction

The multifractal model of turbulence (Frisch-Parisi, 1985; Meneveau-Sreenivasan, 1991) provides a phenomenological framework for anomalous scaling. In this model:

    <|nabla u|^p> ~ Re^{tau_p}

where tau_p is a convex function (the scaling exponent). The anomalous dimension is tau_p - p tau_1.

For the quantity D_xi S ~ nabla^2 u, the multifractal prediction involves the p = 3/2 moment of nabla u (since |D_xi S| ~ |nabla u|^{3/2} dimensionally). The multifractal exponent is:

    tau_{3/2} = (3/2) tau_1 + anomaly

DNS measurements (Meneveau-Sreenivasan, 1991; Kaneda et al., 2003) give:

    tau_p = p/3 + mu_p    where mu_p > 0 is the intermittency correction

The intermittency correction mu_p is POSITIVE for p > 3, meaning higher-order moments are enhanced. For p = 3/2, mu_{3/2} is typically very small but slightly positive in most intermittency models (e.g., the She-Leveque model gives tau_p = p/9 + 2(1 - (2/3)^{p/3}), and tau_{3/2} = 1/6 + 2(1 - (2/3)^{1/2}) ~ 0.533 vs. naive 0.5).

**The intermittency correction at p = 3/2 is positive but tiny (~0.03).** This is the WRONG SIGN for regularity -- it means D_xi S is slightly LARGER than the naive estimate, not smaller.

However, this multifractal prediction applies to volume-averaged moments, not to the pointwise maximum. The relationship between the two involves the local dimension of the most singular set, and the correspondence is not straightforward.

---

## 6. The Sign Question: Physical Arguments

### 6.1 Why gamma might be positive (favorable for regularity)

**Argument: Decorrelation.** At a given point x, D_xi S = (xi . nabla) S involves the strain gradient projected onto the local vorticity direction. The high-frequency fluctuations u_> create rapidly oscillating contributions to both xi and nabla S. When projected onto the low-frequency vorticity direction xi_<, these rapid oscillations tend to average out because:

- The high-frequency correction to xi oscillates on scale k^{-1} (small)
- The low-frequency xi_< varies on scale (k_<)^{-1} (large)
- The high-frequency nabla S oscillates on scale k^{-1}
- The product (delta xi_>) . (nabla S_>) averages to a smooth function when convolved over the shell

This decorrelation would reduce the effective D_xi S, giving gamma > 0.

**Counter-argument:** The decorrelation argument applies to the AVERAGE of D_xi S over a spatial region of size ~ k^{-1}. But the regularity question concerns the MAXIMUM of D_xi S. The maximum is controlled by intermittency -- the rare, extreme events where the high-frequency modes happen to be aligned with xi_<. Intermittency ENHANCES the maximum relative to the average.

### 6.2 Why gamma might be negative (unfavorable for regularity)

**Argument: Intermittency.** The high-frequency fluctuations u_> are intermittent -- they are concentrated in thin sheets and tubes rather than uniformly distributed. The most intense fluctuations tend to occur near the strongest low-frequency structures (a well-established feature of turbulent cascades). This spatial correlation between high-frequency intensity and low-frequency vorticity direction ENHANCES D_xi S at the vorticity maximum.

More specifically:
- The strongest high-frequency strain tends to occur near the strongest low-frequency vortex tubes.
- The strain gradient from high-frequency modes is therefore preferentially aligned with the low-frequency vorticity direction xi_<.
- This alignment increases D_xi S beyond the naive (decorrelated) estimate.

**Supporting evidence:** The DNS measurements of conditional averages (Tsinober et al., 1999; Hamlington et al., 2008) show that the strain gradient is indeed enhanced near strong vorticity structures, not reduced.

### 6.3 The vorticity-strain alignment effect

A more subtle effect: the vorticity direction xi tends to align with the intermediate eigenvector e_2 of the strain tensor S (the well-established DNS finding). This alignment means:

    Q = xi . S xi = s_2    (the intermediate eigenvalue)

Under the RG flow (integrating out high-frequency modes), the alignment STRENGTHENS (because the restricted Euler dynamics drive the alignment toward the RE attractor). The strengthened alignment has two competing effects on D_xi S:

1. **Alignment reduces D_xi S along the tube.** For a perfectly aligned vortex tube, D_xi S = 0 because the strain is axisymmetric and does not vary along the tube axis.

2. **Alignment concentrates D_xi S at tube tips and interaction regions.** The reduction of D_xi S in the tube interior is compensated by enhanced D_xi S at the ends of the tube and at locations where tubes interact.

The net effect on the maximum of D_xi S is ambiguous.

### 6.4 Assessment of the sign

There is no reliable way to determine the sign of gamma from physical arguments alone. The decorrelation effect (gamma > 0) and the intermittency effect (gamma < 0) compete, and the outcome depends on the detailed angular structure of the turbulent cascade.

The multifractal evidence (Section 5.4) weakly favors gamma < 0 (intermittency enhances extreme events), but the evidence is indirect and the correspondence between volume-averaged scaling exponents and pointwise anomalous dimensions is non-trivial.

**Honest assessment of the sign: unknown, with a slight lean toward gamma <= 0 (unfavorable) based on intermittency phenomenology.**

---

## 7. The Bricmont-Kupiainen Framework: Can Any of This Be Made Rigorous?

### 7.1 The BK RG for NS

Bricmont and Kupiainen (2007) developed a rigorous RG framework for the 3D NS equations. Their results:

1. **Small data global regularity.** For initial data with sufficiently small norm in a critical space, the NS solution exists globally and converges to a universal self-similar profile.

2. **The RG map.** The RG transformation is the map that relates the initial data at scale Lambda to the effective initial data at scale Lambda/b (after integrating out one shell of modes). For small data, this map is a contraction (the nonlinearity is irrelevant in the RG sense).

3. **Anomalous dimensions.** In the BK framework, the anomalous dimensions are ZERO at the Gaussian fixed point (which governs the small-data regime). The NS nonlinearity is irrelevant, and all operators retain their naive (engineering) scaling dimensions.

### 7.2 Relevance

The BK result is rigorous but applies only to small data. For large data (the regime relevant to the regularity question):

- The Gaussian fixed point is NOT the relevant fixed point.
- The Kolmogorov fixed point (if it exists rigorously) would be the relevant one.
- Anomalous dimensions at the Kolmogorov fixed point are not accessible by the BK perturbative methods.

**Conclusion:** The BK framework cannot provide a rigorous computation of the anomalous dimension at the Kolmogorov fixed point. Any such computation would require non-perturbative methods that do not currently exist.

### 7.3 Model problems where anomalous dimensions can be computed

1. **The Kraichnan model (passive scalar).** As discussed in Section 5, anomalous dimensions are exactly computable. The computation uses the passive nature of the scalar and does not extend to the active NS velocity.

2. **Stochastic NS with power-law forcing (epsilon-expansion).** The Forster-Nelson-Stephen / Yakhot-Orszag framework computes anomalous dimensions perturbatively in epsilon (the forcing exponent). For specific composite operators, the one-loop anomalous dimension can be computed. However:
   - The relevant operator D_xi S is nonlinear in u and cannot be treated in the standard epsilon-expansion.
   - The epsilon = 2 limit (relevant to the physical 3D Kolmogorov regime) is far from the perturbative regime (epsilon << 1).
   - The connection between the stochastic forced NS and the deterministic regularity problem is unclear.

3. **Shell models (GOY, Sabra).** These are simplified dynamical systems that mimic the NS cascade. Anomalous exponents can be computed numerically and sometimes analytically (Lvov et al., 1998). The shell model anomalous dimensions:
   - Are typically NEGATIVE (intermittency-enhancing), consistent with the multifractal prediction.
   - For the specific quantity analogous to D_xi S / omega^{3/2}, the scaling is exactly delta = 1/2 (the borderline), with no anomalous correction within numerical precision.

**None of the exactly solvable models provide evidence for a positive anomalous dimension of D_xi S.**

---

## 8. The Specific One-Loop Integral (Forced Through)

### 8.1 Setup

Despite the obstructions identified in Section 3, we can force through a formal one-loop computation by:
1. Working in the stochastic NS framework with Kolmogorov forcing.
2. Replacing xi by its linear approximation around a mean vorticity direction xi_0.
3. Computing the one-loop correction to the ratio R = <D_xi S> / <omega^{3/2}/nu^{1/2}>.

This is NOT a computation of the anomalous dimension of D_xi S (which does not have one, as argued above). It is a computation of the one-loop correction to the conditional average of D_xi S given the local vorticity.

### 8.2 The diagram

The one-loop correction involves the contraction of one u_> leg from the linearized delta xi correction with one u_> leg from the S operator, connected by the Gaussian propagator G(k):

```
        delta xi vertex              S vertex
             |                          |
         k,a ------[G(k) P_ab]------ -k,b
             |                          |
    (curl + P^perp)_a           (sym grad)_b
             |                          |
           O insertion
```

The amplitude:

    I = integral_{Lambda/b < |k| < Lambda} d^3k / (2pi)^3 * G(k) 
        * V^{xi}_{ma}(k, xi_0, omega_0) * V^{S}_{mb}(k, xi_0)
        * P_{ab}(k)

where:
- V^{xi}_{ma}(k) = (1/|omega_0|) P^{perp}_{mc}(xi_0) epsilon_{cde} i k_d P_{ea}(k) is the delta xi vertex
- V^{S}_{mb}(k) = xi_{0,f} i k_f (1/2)(i k_m delta_{ij,b} + ...) is the S vertex (specific tensor components depend on which component of D_xi S we track)

### 8.3 Explicit evaluation (choosing xi_0 = e_3, eta = e_1)

With xi_0 = e_3, the perpendicular projector P^{perp} projects onto the (1,2) plane.

The delta xi vertex (correction to xi_1, the e_1 component):

    V^{xi}_{1a}(k) = (1/|omega_0|) P^{perp}_{1c} epsilon_{cde} i k_d P_{ea}(k)

P^{perp}_{1c} = delta_{1c} (since m=1, and P^{perp}_{11} = 1, P^{perp}_{12} = 0). So c = 1:

    = (i/|omega_0|) epsilon_{1de} k_d P_{ea}(k) = (i/|omega_0|)(k_2 P_{3a}(k) - k_3 P_{2a}(k))

The S vertex for the specific component eta . (D_{xi_0} S) xi_0 = partial_3 S_{13}:

At wavevector -k (the other leg):

    V^{S}(k) = -(1/2) k_3 (k_1 P_{3b}(k) + k_3 P_{1b}(k))

(using S_{13} = (1/2)(partial_1 u_3 + partial_3 u_1) and D_{xi_0} = partial_3, contracted with P for incompressibility.)

The full one-loop integral:

    I = integral d^3k / (2pi)^3 * G(k) * P_{ab}(k)
        * (i/|omega_0|)(k_2 P_{3a}(k) - k_3 P_{2a}(k))
        * (-(1/2) k_3 (k_1 P_{3b}(k) + k_3 P_{1b}(k)))

Using P_{ab}(k) P_{bc}(k) = P_{ac}(k) (the projector property):

The a-contraction:

    P_{ab}(k) [k_2 P_{3a}(k) - k_3 P_{2a}(k)]
    = k_2 P_{ab}(k) P_{3a}(k) - k_3 P_{ab}(k) P_{2a}(k)
    = k_2 P_{3b}(k) - k_3 P_{2b}(k)

Then contracting with the b-index:

    [k_2 P_{3b}(k) - k_3 P_{2b}(k)] * [k_1 P_{3b}(k) + k_3 P_{1b}(k)]
    = k_1 k_2 P_{3b} P_{3b} + k_2 k_3 P_{3b} P_{1b} - k_1 k_3 P_{2b} P_{3b} - k_3^2 P_{2b} P_{1b}

Now, P_{ib}(k) P_{jb}(k) = P_{ij}(k) (since P is a projector). So:

    = k_1 k_2 P_{33}(k) + k_2 k_3 P_{31}(k) - k_1 k_3 P_{23}(k) - k_3^2 P_{21}(k)

Using P_{ij}(k) = delta_{ij} - k_i k_j / k^2 = delta_{ij} - hat{k}_i hat{k}_j:

    P_{33} = 1 - hat{k}_3^2
    P_{31} = -hat{k}_3 hat{k}_1
    P_{23} = -hat{k}_2 hat{k}_3
    P_{21} = -hat{k}_2 hat{k}_1

Substituting:

    = k_1 k_2 (1 - hat{k}_3^2) + k_2 k_3 (-hat{k}_3 hat{k}_1) - k_1 k_3 (-hat{k}_2 hat{k}_3) - k_3^2 (-hat{k}_2 hat{k}_1)

Using k_i = k hat{k}_i:

    = k^2 [hat{k}_1 hat{k}_2 (1 - hat{k}_3^2) - hat{k}_1 hat{k}_2 hat{k}_3^2 + hat{k}_1 hat{k}_2 hat{k}_3^2 + hat{k}_1 hat{k}_2 hat{k}_3^2]
    = k^2 [hat{k}_1 hat{k}_2 (1 - hat{k}_3^2) + hat{k}_1 hat{k}_2 hat{k}_3^2]
    = k^2 hat{k}_1 hat{k}_2 [(1 - hat{k}_3^2) + hat{k}_3^2]
    = k^2 hat{k}_1 hat{k}_2

Wait, let me redo this more carefully:

    Term 1: k_1 k_2 (1 - hat{k}_3^2) = k^2 hat{k}_1 hat{k}_2 (1 - hat{k}_3^2)
    Term 2: k_2 k_3 (-hat{k}_3 hat{k}_1) = -k^2 hat{k}_1 hat{k}_2 hat{k}_3^2
    Term 3: -k_1 k_3 (-hat{k}_2 hat{k}_3) = k^2 hat{k}_1 hat{k}_2 hat{k}_3^2
    Term 4: -k_3^2 (-hat{k}_2 hat{k}_1) = k^2 hat{k}_1 hat{k}_2 hat{k}_3^2

Sum: k^2 hat{k}_1 hat{k}_2 [(1 - hat{k}_3^2) - hat{k}_3^2 + hat{k}_3^2 + hat{k}_3^2]
   = k^2 hat{k}_1 hat{k}_2 [1 - hat{k}_3^2 + hat{k}_3^2]
   = k^2 hat{k}_1 hat{k}_2

So the contraction simplifies beautifully to k^2 hat{k}_1 hat{k}_2.

The full integral becomes:

    I = integral d^3k / (2pi)^3 * G(k) * (i/|omega_0|) * (-(1/2) k_3) * k^2 hat{k}_1 hat{k}_2

    = -(i/(2|omega_0|)) integral d^3k / (2pi)^3 * G(k) * k_3 * k^2 * hat{k}_1 * hat{k}_2

Now, k_3 = k hat{k}_3 and k^2 hat{k}_1 hat{k}_2 = k^2 hat{k}_1 hat{k}_2. So:

    I = -(i/(2|omega_0|)) integral_0^infty k^2 dk * G(k) * k^3 / (2pi)^3 
        * integral dOmega hat{k}_1 hat{k}_2 hat{k}_3

**The angular integral:**

    integral dOmega hat{k}_1 hat{k}_2 hat{k}_3 = 0

**The integral vanishes by symmetry.** The integrand hat{k}_1 hat{k}_2 hat{k}_3 is odd under the reflection hat{k}_1 -> -hat{k}_1 (or hat{k}_2 -> -hat{k}_2 or hat{k}_3 -> -hat{k}_3), so its integral over the full sphere is zero.

### 8.4 Interpretation of the vanishing

The vanishing of the one-loop integral for this specific component is a consequence of the PARITY symmetry of the NS equations. The operator D_xi S is a pseudoscalar (it changes sign under parity x -> -x, since xi is a pseudovector and S is a tensor), and the one-loop correction must preserve this parity structure. The angular integral of an odd number of hat{k} components over the sphere vanishes by parity.

However, this does NOT mean the one-loop anomalous dimension is zero. The parity argument shows that the one-loop correction to the EXPECTATION VALUE of D_xi S vanishes, not that the correction to its MAGNITUDE or its CORRELATION FUNCTIONS vanishes. The anomalous dimension would appear in the two-point function <O(x) O(y)>, not in the one-point function <O(x)>.

### 8.5 The two-point function approach

The anomalous dimension gamma would appear in:

    <O(x) O(y)> ~ |x-y|^{-(2 Delta_O + gamma)}

where Delta_O = 3 is the naive dimension. Computing <O(x)O(y)> at one loop requires a TWO-POINT diagram with two operator insertions and one loop, which involves:

- Four u legs total (two from each O insertion)
- The loop connects pairs of legs

The number of possible contractions proliferates, and each involves angular integrals over the shell. The computation is lengthy but systematic. Due to the nonlinearity of xi, the two-point function <D_{xi}S(x) . D_{xi}S(y)> involves fourth-order correlators of u_> that, under the Gaussian assumption, factorize into products of two-point functions. Each factorization gives a pair of loop integrals, and the anomalous dimension is extracted from the logarithmically divergent part (the part proportional to ln(Lambda/|x-y|^{-1})).

**This computation is feasible in principle but extremely tedious and, crucially, depends on the background flow (through |omega_0| and xi_0), making the result non-universal.**

I will not carry out the full two-point computation here because (a) it would require specifying the background completely, (b) the result would not be universal, and (c) even if a nonzero gamma were obtained, it would be a formal result in the stochastic NS framework with no rigorous bearing on the deterministic regularity problem.

---

## 9. Verdict

### 9.1 What is the sign of gamma?

**Unknown.** The one-loop computation of the one-point function of D_xi S gives a vanishing result by parity. The two-point function computation would give a nonzero result but is (a) background-dependent, (b) extremely lengthy, and (c) of uncertain sign.

Physical arguments weakly suggest gamma <= 0 (anti-screening / intermittency enhancement), based on:
- The multifractal model (Section 5.4) predicts intermittency corrections that enhance extreme events.
- Shell model calculations show no anomalous correction to the delta = 1/2 scaling.
- DNS evidence of enhanced strain gradients near strong vortex structures.

However, these arguments are indirect and not definitive. The decorrelation argument (Section 6.1) weakly suggests gamma > 0 but only for the average, not the maximum.

**Assessment: the sign of gamma is undetermined, with a slight lean toward gamma <= 0.**

### 9.2 What is the approximate magnitude?

If we take the multifractal prediction at face value, the anomalous correction to the scaling exponent of D_xi S is:

    delta_{anomalous} ~ 0.03    (from the She-Leveque model at p = 3/2)

This corresponds to |gamma| ~ 0.03, which is very small. Even if gamma were positive (favorable), a correction of this magnitude would produce a logarithmic factor (log omega)^{-0.03}, which is an extremely slow correction.

However, the multifractal exponent is for volume-averaged moments, not for the pointwise maximum that enters Theorem CB. The pointwise maximum could have a very different (and potentially larger) anomalous correction.

### 9.3 Is the computation rigorous?

**No.** The computation is formal at every step:

1. The MSR/field-theory framework for NS is formal (not rigorously justified for deterministic NS).
2. The Gaussian closure at one loop is an uncontrolled approximation.
3. The Kolmogorov spectrum used as input is empirically known but not rigorously derived.
4. The linearization of xi around a background is an approximation that discards the essential nonlinearity.
5. The product-over-shells assumption (that corrections are multiplicative and independent) is a mean-field-type approximation.

### 9.4 What would be needed to make it rigorous?

A rigorous version would require:

1. **A rigorous RG framework for NS at large data.** This does not exist. The Bricmont-Kupiainen framework handles small data (where gamma = 0 trivially).

2. **A rigorous definition of the Kolmogorov fixed point.** The existence of a non-trivial fixed point for the NS RG at large Reynolds number is an open problem, essentially equivalent to the regularity problem itself.

3. **A rigorous computation of anomalous dimensions at the non-trivial fixed point.** Even for the stochastic NS with prescribed forcing, this has not been achieved beyond the epsilon-expansion.

4. **A connection between the stochastic and deterministic settings.** Even if anomalous dimensions were computed rigorously for the stochastic NS, their relevance to the deterministic regularity problem would need to be established.

Each of these steps is an unsolved problem of comparable difficulty to the Millennium Prize.

### 9.5 Is there a model problem where the anomalous dimension can be computed exactly?

**The Kraichnan passive scalar** is the only turbulence model where anomalous dimensions are computed exactly. The result (Section 5.2) shows gamma < 0 (intermittency enhancement), which is the wrong sign for regularity.

**Shell models** can be numerically solved at very high Reynolds numbers. The evidence from shell models (Section 7.3) is that the borderline scaling delta = 1/2 is NOT corrected by anomalous effects -- the ratio R remains constant across scales within numerical precision.

**Stochastic Burgers equation.** The 1D stochastic Burgers equation is exactly solvable (Cole-Hopf transform), and the anomalous dimensions of velocity structure functions are known. The results show shocks (singularities) at the level analogous to the NS blowup, confirming that 1D models cannot provide evidence for 3D regularity.

### 9.6 Does this close the NS regularity problem?

**No.** The one-loop RG computation:

1. Cannot be carried through to a definite result (the composite operator D_xi S does not have a well-defined anomalous dimension in the standard RG sense, due to the nonlinearity of xi).
2. Even if forced through formally, gives a result whose sign is undetermined.
3. Even if the sign were favorable (gamma > 0), the computation is entirely formal and has no rigorous content.
4. Even if it could be made rigorous for the stochastic NS, the connection to deterministic regularity is unclear.
5. The available evidence from model problems (Kraichnan, shell models) weakly suggests gamma <= 0, the wrong sign.

### 9.7 Probability assessment

| Route | Probability of resolving NS regularity |
|-------|---------------------------------------|
| This one-loop RG computation producing gamma > 0 rigorously | < 0.1% |
| Any formal RG computation providing heuristic guidance | ~ 2% |
| The anomalous dimension being positive (favorable sign) | ~ 30% |
| The anomalous dimension being large enough to matter (|gamma| > 0.1) | ~ 10% |
| Any approach based on anomalous dimensions resolving the regularity problem | < 1% |
| The RG perspective providing useful STRUCTURAL insight (even without a proof) | ~ 40% |

### 9.8 What the RG perspective DOES provide

Despite the failure to compute a definitive anomalous dimension, the RG viewpoint yields several structural insights:

1. **The d-independence of R (equation 6.2) is a fixed-point property.** The ratio |D_xi S| / (omega^{3/2}/nu^{1/2}) = C/Re_Gamma^2 being scale-invariant is exactly what one expects at an RG fixed point. The question of regularity becomes: is this fixed point stable (gamma > 0) or unstable (gamma < 0)?

2. **The borderline nature of delta = 1/2 is structural, not accidental.** It follows from the Biot-Savart scaling law (both D_xi S and omega^{3/2} scale as d^{-3}), which is a consequence of the dimensional structure of the NS equations. Any improvement must come from CANCELLATIONS or CORRELATIONS, not from a change in power-law scaling.

3. **The eddy viscosity correction goes in the WRONG direction.** The eddy viscosity nu_eff > nu reduces the effective Reynolds number, which increases R (equation 6.2 with Re_{Gamma,eff} < Re_Gamma). This means the RG flow (in the eddy-viscosity sector) makes the ratio R LARGER, pushing toward the dangerous regime, not away from it.

4. **The decorrelation vs. intermittency competition is the heart of the matter.** The regularity question, in the RG language, reduces to whether the decorrelation of D_xi S across scales (which tends to reduce R) can overcome the intermittent concentration of strain gradients near strong vorticity (which tends to increase R). This is a well-defined physical question that could, in principle, be settled by high-precision DNS.

---

## 10. Connection to Other Approaches in This Pursuit

### 10.1 Relationship to the antisymmetry cancellation (path-1-cancellation-computation.md)

The antisymmetry of D_xi S at closest approach (identified in tube-tube-interaction-analysis.md and pursued in path-1-cancellation-computation.md) is a specific instance of the decorrelation mechanism discussed in Section 6.1. In the RG language:

- The tree-level (leading-order) D_xi S has an antisymmetric structure around the closest-approach point.
- When integrated against the curvature evolution equation, this antisymmetry provides a partial cancellation.
- This cancellation is analogous to a one-loop correction from the vertex structure, not from the propagator.
- If the cancellation is exact (which it is not, due to the nonlinearity of xi), it would correspond to gamma -> infinity (complete screening).
- In practice, the cancellation is partial, providing a finite reduction factor that may or may not reach the logarithmic correction needed.

### 10.2 Relationship to the Hasimoto/NLS approach (path-3-hasimoto-computation.md)

The Hasimoto transform maps the vortex filament dynamics to the nonlinear Schrodinger equation. In the RG framework:

- The NLS is integrable (in 1D), and its "anomalous dimensions" are exactly computable.
- The filament curvature kappa is bounded by the NLS conservation laws.
- The D_xi S term appears as a correction to the LIA (local induction approximation), which is subleading for thin filaments.
- The RG anomalous dimension of D_xi S in the Hasimoto framework would be computed from the NLS perturbation theory, not from the NS field theory.

This is a genuinely different approach that avoids the NS RG machinery entirely. The NLS perspective might provide the logarithmic correction through the integrability structure, rather than through loop diagrams.

### 10.3 Relationship to the coupled bootstrap (coupled-bootstrap-attempt.md)

The coupled bootstrap (Theorem CB) is the destination for any anomalous dimension computation. If gamma > 0 could be established (even heuristically), the chain would be:

1. D_xi S receives a negative anomalous correction: |D_xi S|_eff ~ |D_xi S|_bare * (log omega)^{-gamma}
2. Combined with equation 6.2: |D_xi S|_eff <= (C/Re_Gamma^2) * omega^{3/2}/nu^{1/2} * (log omega)^{-gamma}
3. For any gamma > 0, this gives delta_effective > 1/2 (by a logarithmic amount)
4. Theorem CB with delta > 1/2 gives regularity.

But step 1 is the unproven (and likely unprovable by current methods) step.

---

## 11. Summary

| Question | Answer | Confidence |
|---|---|---|
| Does D_xi S have a well-defined anomalous dimension? | No -- the nonlinearity of xi prevents a standard RG treatment | High |
| Can the one-loop correction be computed formally? | Partially -- the one-point function vanishes by parity; the two-point function is computable but non-universal | Medium |
| What is the sign of the anomalous correction? | Unknown; weak evidence for gamma <= 0 (wrong sign) from intermittency phenomenology | Low |
| Is the computation rigorous? | No, at every step | High |
| Does this close the NS regularity problem? | No | High |
| What would be needed to make it rigorous? | A rigorous NS RG framework at large data (essentially equivalent to solving the regularity problem) | High |
| Does the RG perspective provide useful structural insight? | Yes: the d-independence of R, the borderline nature of delta = 1/2, and the decorrelation vs. intermittency framing | Medium-High |
| Best probability this approach leads to resolution | < 1% for rigorous resolution; ~ 2% for heuristic guidance that informs a different approach | Assessment |

The RG anomalous dimension approach, while conceptually elegant, encounters a fundamental obstruction in the nonlinearity of the vorticity direction xi = omega/|omega|. This nonlinearity is the same obstruction that appears in every other approach to NS regularity -- it is the NS nonlinearity itself, merely repackaged in RG language. The logarithmic correction needed by Theorem CB is not delivered by the one-loop computation, and there is weak evidence that the true correction (if any) goes in the wrong direction.

The most promising thread to emerge from this analysis is the connection between the decorrelation/intermittency competition and the sign of gamma. This is a physically meaningful question that could be addressed by high-resolution DNS measurements of D_xi S conditioned on local vorticity magnitude, providing empirical evidence for or against the needed logarithmic correction.
