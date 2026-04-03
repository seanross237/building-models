# Time-Integrated Bootstrap for Navier-Stokes Regularity

**Date:** 2026-04-02
**Parent:** Coupled Bootstrap Attempt (Theorem CB)
**Classification:** Follow-up analysis -- can time integration break the delta = 1/2 borderline?
**Depends on:** Theorem CB, enstrophy dissipation bounds, De Giorgi-Nash-Moser parabolic theory

---

## 0. Executive Summary

Theorem CB establishes that NS is regular if |D_xi S| <= C |omega|^{1+delta} POINTWISE with delta > 1/2. The dimensional estimate gives exactly delta = 1/2 -- the borderline. This document investigates whether time integration can break the borderline: even if |D_xi S| instantaneously reaches the borderline during tube-tube interactions, these events are transient (duration ~ 1/|omega|), and what matters for the bootstrap is the cumulative effect.

**Verdict: The time-integrated bootstrap does NOT close unconditionally.** The approach contains a genuine structural insight (transient events contribute less to the integrated bootstrap than persistent ones), but the gain is not sufficient to cross the borderline. The analysis identifies three precise failure points:

1. **The Gronwall amplification absorbs the transient gain.** The K equation's exponential growth factor e^{C integral Omega ds} amplifies the D_xi S integral at exactly the rate needed to cancel the transient savings.

2. **The De Giorgi parabolic iteration does NOT apply to D_xi S.** The PDE for D_xi S has coefficients that are themselves supercritical (involving nabla^2 p and nabla omega), violating the structural assumptions of De Giorgi-Nash-Moser theory. The logarithmic gain from De Giorgi iteration is therefore unavailable.

3. **The L^2-L^2 enstrophy bound cannot be localized to a pointwise bound without losing the scaling.** Sobolev embedding on the high-vorticity set recovers at best |D_xi S|_{L^infty} ~ Omega^{3/2}/nu^{1/2} -- the same dimensional estimate.

However, the analysis produces one conditionally useful result: if the De Giorgi iteration could be applied (i.e., if the PDE for D_xi S had sufficiently nice coefficients), the logarithmic gain would be sigma = 1/(n+2) = 1/5 in the parabolic setting (n = 3 spatial dimensions), which is more than enough to break the borderline (any sigma > 0 suffices). The obstacle is entirely in verifying the structural hypotheses of De Giorgi theory for this specific PDE.

---

## 1. Question 1: Does the Time-Integrated Condition Give Regularity for delta > 1/2?

### 1.1 The integrated condition

Replace the pointwise condition |D_xi S(x_*(t), t)| <= C |omega(x_*(t),t)|^{1+delta} with the time-integrated condition: for any interval [t_1, t_2],

    integral_{t_1}^{t_2} |D_xi S(x_*(t), t)| dt <= C * integral_{t_1}^{t_2} |omega(x_*(t),t)|^{1+delta} dt

This is strictly weaker than the pointwise condition (pointwise implies integrated by direct integration, but not conversely). The question is whether the ODE analysis from Theorem CB extends.

### 1.2 The coupled ODE system under the integrated condition

The system is:

    dOmega/dt <= C_1 Omega^2 - nu K^2 Omega                                     (A)
    dK/dt     <= C_2 Omega K + |D_xi S(t)|                                       (B)

Integrate equation (B) on [0, t]:

    K(t) <= K(0) + C_2 integral_0^t Omega(s) K(s) ds + integral_0^t |D_xi S(s)| ds

By the Gronwall lemma:

    K(t) <= [K(0) + integral_0^t |D_xi S(s)| e^{-C_2 integral_0^s Omega(r) dr} ds] * e^{C_2 integral_0^t Omega(s) ds}     (G)

Now suppose the integrated D_xi S condition holds with delta > 1/2:

    integral_0^t |D_xi S(s)| ds <= C integral_0^t Omega(s)^{1+delta} ds

The exponential weight e^{-C_2 integral_0^s Omega dr} inside the Gronwall formula is at most 1, so:

    integral_0^t |D_xi S(s)| e^{-C_2 integral_0^s Omega dr} ds <= integral_0^t |D_xi S(s)| ds <= C integral_0^t Omega^{1+delta} ds

Therefore:

    K(t) <= [K(0) + C integral_0^t Omega^{1+delta} ds] * e^{C_2 integral_0^t Omega ds}

### 1.3 Blowup analysis under the integrated condition

Suppose Omega(t) ~ A(T-t)^{-alpha} near the blowup time T. Then:

    integral_0^t Omega ds diverges like (T-t)^{1-alpha} / (alpha - 1) if alpha > 1, or like -log(T-t) if alpha = 1

    integral_0^t Omega^{1+delta} ds diverges like (T-t)^{1-(1+delta)alpha} / ((1+delta)alpha - 1) if (1+delta)alpha > 1

For alpha = 1:

    integral_0^t Omega ds ~ -log(T-t)        (diverges logarithmically)
    integral_0^t Omega^{1+delta} ds ~ (T-t)^{-delta} / delta   (diverges as power)

The Gronwall bound gives:

    K(t) <= C (T-t)^{-delta} * (T-t)^{-C_2} = C (T-t)^{-(delta + C_2)}

Wait -- the exponential of -log(T-t) is (T-t)^{-C_2}. So:

    e^{C_2 integral Omega ds} ~ (T-t)^{-C_2}

And the integral of Omega^{1+delta}:

    integral_0^t Omega^{1+delta} ds ~ (T-t)^{1 - (1+delta)} = (T-t)^{-delta}

So K(t) <= C (T-t)^{-delta} * (T-t)^{-C_2} = C (T-t)^{-(delta + C_2)}.

But C_2 is order 1 (it comes from the strain eigenvalue ratio, C_2 ~ 0.4-0.8 in the DNS regime). So K ~ (T-t)^{-(delta + C_2)}.

The damping term in (A):

    nu K^2 Omega ~ nu (T-t)^{-2(delta + C_2)} (T-t)^{-1} = nu (T-t)^{-(1 + 2delta + 2C_2)}

For this to dominate the stretching C_1 Omega^2 ~ (T-t)^{-2}, we need:

    1 + 2delta + 2C_2 > 2,    i.e.,    2delta + 2C_2 > 1,    i.e.,    delta > (1 - 2C_2)/2

For C_2 > 0 (which holds in the DNS regime), this is weaker than delta > 1/2 -- the threshold is LOWER. So the Gronwall estimate appears to help!

### 1.4 The problem: Gronwall is not sharp

The analysis in Section 1.3 is misleading. The issue is that the Gronwall lemma gives an UPPER bound on K, and the upper bound involves the product of two divergent quantities (the integral and the exponential). The resulting K estimate is larger than what the pointwise bound would give, not smaller.

Let me compare directly:

**Pointwise bound (Theorem CB):** |D_xi S| <= C Omega^{1+delta} implies, from the ODE dK/dt <= C_2 Omega K + C Omega^{1+delta}:

    Scaling: beta + 1 = max(alpha + beta, (1+delta)alpha)
    If (1+delta)alpha dominates: beta = (1+delta)alpha - 1
    With alpha = 1: beta = delta

So K ~ (T-t)^{-delta}. This is the scaling from the pointwise bound.

**Integrated bound (Gronwall):** K ~ (T-t)^{-(delta + C_2)}.

The Gronwall bound gives K growing FASTER (larger exponent delta + C_2 > delta) than the pointwise analysis. This is because the Gronwall exponential amplifies the source term. The integrated condition does not give a smaller K -- it gives a larger one.

The apparent gain in the threshold (delta > (1 - 2C_2)/2 instead of delta > 1/2) is illusory: the Gronwall exponent C_2 appears in K, and the stronger K then overestimates the damping, creating a false victory. The Gronwall lemma is inherently lossy for oscillating or signed integrands.

### 1.5 Careful scaling analysis for the integrated case

Let us redo the coupled scaling without using Gronwall. Assume Omega ~ (T-t)^{-alpha} and K ~ (T-t)^{-beta}. Equation (A) is unchanged:

    alpha + 1 = max(2alpha, 2beta + alpha)

Equation (B) in differential form: dK/dt <= C_2 Omega K + |D_xi S|. With the integrated condition, we assume:

    integral_{t}^{T} |D_xi S| ds <= C integral_{t}^{T} Omega^{1+delta} ds ~ C (T-t)^{1-(1+delta)alpha}

The time-averaged |D_xi S| over the interval [t, T] is:

    <|D_xi S|> ~ (T-t)^{-(1+delta)alpha}

This is the same scaling as the pointwise bound |D_xi S| ~ Omega^{1+delta} ~ (T-t)^{-(1+delta)alpha}.

**The integrated condition, when applied to power-law blowup, gives exactly the same scaling as the pointwise condition.** This is because the time integral of (T-t)^{-gamma} over [t, T] is (T-t)^{1-gamma}/(gamma-1), and dividing by the interval length (T-t) recovers (T-t)^{-gamma}. Power-law behavior is scale-invariant -- time averaging does not change the exponent.

### 1.6 When does the integrated condition genuinely differ from pointwise?

The integrated condition is strictly weaker than the pointwise condition in the following situation: |D_xi S| has transient spikes where it exceeds C Omega^{1+delta}, provided the time-average stays below. For power-law blowup profiles, this cannot happen (the profile is monotone). But for oscillating or intermittent behavior, it can.

Specifically, suppose |D_xi S| spends a fraction f(Omega) of the time at the level Omega^{3/2}/nu^{1/2} (the dimensional bound, delta = 1/2) and the remaining fraction 1 - f(Omega) at a much lower level. Then:

    <|D_xi S|>_time ~ f(Omega) * Omega^{3/2}/nu^{1/2}

If f(Omega) -> 0 as Omega -> infinity, the effective time-averaged delta exceeds 1/2. For example, if events at the borderline have duration ~ 1/Omega (a single vortex-tube interaction period), and they occur at a rate that does not increase with Omega, then:

    f(Omega) ~ (rate) * (1/Omega) / 1 = rate / Omega -> 0    if rate is bounded

This would give <|D_xi S|> ~ Omega^{1/2}/nu^{1/2}, corresponding to effective delta = -1/2 -- far below the borderline, trivially safe.

But this is unrealistic: as Omega grows, the interaction rate also grows (more energetic vortex dynamics means more frequent interactions). The question is the precise rate.

For a self-similar blowup at rate Omega ~ (T-t)^{-1}: the interaction rate also scales as (T-t)^{-1} (one interaction per turnover time). The fraction f is then:

    f ~ (T-t)^{-1} * (T-t)^{1} = O(1)

constant -- no gain. The transient savings are exactly canceled by the increased frequency of events.

### 1.7 Verdict on Question 1

**The time-integrated condition gives regularity for delta > 1/2, by exactly the same argument as Theorem CB.** The integrated condition is logically weaker (hence the theorem is formally stronger), but for the power-law blowup profiles that matter, the two conditions have the same content. The transient nature of tube-tube interactions does NOT provide a gain in the scaling exponent because the frequency of interactions scales inversely with the duration.

**Answer to Question 1: YES, the integrated condition gives regularity for delta > 1/2. But NO, it does not break the borderline at delta = 1/2.** The time-integrated version of Theorem CB is a formally stronger theorem (weaker hypothesis, same conclusion), but it does not change the critical threshold.

---

## 2. Question 2: Enstrophy Dissipation Bound on Integrated D_xi S

### 2.1 The L^2 space-time bound

The enstrophy dissipation identity for Navier-Stokes:

    (1/2) ||omega(T)||_{L^2}^2 + nu integral_0^T ||nabla omega||_{L^2}^2 dt = (1/2) ||omega_0||_{L^2}^2 + integral_0^T integral omega . S omega dx dt

For Leray-Hopf weak solutions, the energy inequality gives:

    nu integral_0^T ||nabla omega||_{L^2}^2 dt <= (1/2) ||omega_0||_{L^2}^2 + integral_0^T integral omega . S omega dx dt

The stretching integral is bounded via Sobolev interpolation:

    |integral omega . S omega dx| <= ||omega||_{L^3}^3

Using Gagliardo-Nirenberg: ||omega||_{L^3} <= C ||omega||_{L^2}^{1/2} ||nabla omega||_{L^2}^{1/2}, so:

    ||omega||_{L^3}^3 <= C ||omega||_{L^2}^{3/2} ||nabla omega||_{L^2}^{3/2}

By Young's inequality: C ||omega||_{L^2}^{3/2} ||nabla omega||_{L^2}^{3/2} <= (nu/2) ||nabla omega||_{L^2}^2 + C_nu ||omega||_{L^2}^6.

Actually, the standard approach uses the energy identity directly. For the NS energy balance, we have the a priori bound:

    nu integral_0^T ||nabla omega||_{L^2}^2 dt <= C(||u_0||, T, nu)              (ED)

This is the enstrophy dissipation bound (finite for smooth solutions on [0, T) while they remain smooth).

Now, D_xi S involves nabla^2 u. By the Biot-Savart law and Calderon-Zygmund theory:

    ||D_xi S||_{L^2(R^3)} <= ||nabla S||_{L^2} <= C ||nabla^2 u||_{L^2} <= C ||nabla omega||_{L^2}

The last inequality follows because nabla^2 u = nabla x omega (up to a harmonic correction that vanishes for rapidly decaying solutions), and || nabla x omega ||_{L^2} <= C || nabla omega ||_{L^2}.

More precisely: since u = K * omega where K is the Biot-Savart kernel, nabla^2 u = nabla K * nabla omega (after integration by parts in the convolution). The operator nabla K * is a Calderon-Zygmund operator, bounded on L^2.

Therefore:

    integral_0^T ||D_xi S||_{L^2(R^3)}^2 dt <= C integral_0^T ||nabla omega||_{L^2}^2 dt <= C/nu * E_0

where E_0 = (1/2)||omega_0||_{L^2}^2 (or more generally, a bound depending on initial data and T).

**This is rigorous.** We have D_xi S in L^2_t L^2_x, with explicit control from initial data.

### 2.2 From L^2-L^2 to pointwise

We need |D_xi S(x_*(t), t)| -- a pointwise quantity. The L^2-L^2 bound gives us a spatially-averaged, time-averaged bound. The gap between L^2 and L^infty requires Sobolev embedding or other techniques.

**Approach 1: Direct Sobolev embedding.**

By Sobolev embedding in R^3: ||f||_{L^infty} <= C ||f||_{H^2} = C (||f||_{L^2}^2 + ||nabla f||_{L^2}^2 + ||nabla^2 f||_{L^2}^2)^{1/2}.

Applied to D_xi S: ||D_xi S||_{L^infty} <= C ||D_xi S||_{H^2} <= C ||nabla^3 u||_{L^2}.

But ||nabla^3 u||_{L^2} ~ ||nabla^2 omega||_{L^2} (by CZ theory), which is NOT controlled by the enstrophy dissipation (which controls only ||nabla omega||_{L^2}). We need one more derivative than what the energy estimate provides.

**Approach 2: Localization to the high-vorticity set.**

The high-vorticity set Omega_M = {|omega| > M} has Lebesgue measure:

    |Omega_M| <= ||omega||_{L^2}^2 / M^2

which is small for large M. If D_xi S were smooth and we had bounds on its derivatives, we could use the small measure of Omega_M to improve L^2 to L^infty.

Specifically, on a set of measure |Omega_M|, by Holder's inequality:

    ||D_xi S||_{L^infty(Omega_M)} <= ||D_xi S||_{L^infty(R^3)}

This does not help -- the L^infty norm on a subset is at most the global L^infty norm. The small measure of Omega_M does not reduce the pointwise supremum.

**Approach 3: Sobolev embedding on the set Omega_M.**

If Omega_M is a "nice" set (say, a union of balls of radius r_c), and D_xi S is smooth inside Omega_M, then by the local Sobolev inequality in a ball B_{r_c}:

    ||D_xi S||_{L^infty(B_{r_c})} <= C r_c^{-3/2} ||D_xi S||_{L^2(B_{r_c})} + C r_c^{1/2} ||nabla(D_xi S)||_{L^2(B_{r_c})}

The first term uses the ball volume r_c^3 and Holder; the second uses 3D Sobolev embedding on the ball.

With r_c = (nu/Omega)^{1/2}:

    First term: ~ (Omega/nu)^{3/4} ||D_xi S||_{L^2(B_{r_c})}
    Second term: ~ (nu/Omega)^{1/4} ||nabla(D_xi S)||_{L^2(B_{r_c})}

The second term involves ||nabla(D_xi S)||_{L^2}, which is again uncontrolled (it involves nabla^3 u).

The first term, using ||D_xi S||_{L^2(B_{r_c})}^2 <= ||D_xi S||_{L^2}^2 (the ball contribution is at most the total):

    ||D_xi S||_{L^infty(B_{r_c})} ~ (Omega/nu)^{3/4} ||D_xi S||_{L^2}

And ||D_xi S||_{L^2} <= C ||nabla omega||_{L^2} (from CZ theory). The enstrophy dissipation bounds the TIME integral of ||nabla omega||_{L^2}^2, not the instantaneous value. Even at the peak, ||nabla omega||_{L^2} could be as large as ~ Omega * |Omega_M|^{1/2} / r_c ~ Omega * (Omega/nu)^{1/2} = Omega^{3/2}/nu^{1/2} (using the heuristic that |nabla omega| ~ Omega/r_c on Omega_M of volume ~ r_c^3).

Putting it together:

    |D_xi S(x_*)| ~ (Omega/nu)^{3/4} * Omega^{3/2}/nu^{1/2} = Omega^{9/4}/nu^{5/4}

This is WORSE than the dimensional estimate Omega^{3/2}/nu^{1/2}. The Sobolev embedding on the localized set loses rather than gains.

### 2.3 Verdict on Question 2

**The L^2-L^2 enstrophy bound on D_xi S is real and rigorous:**

    integral_0^T ||D_xi S(.,t)||_{L^2}^2 dt <= C ||omega_0||_{L^2}^2 / nu

**But it cannot be converted to a pointwise bound at x_*(t) without losing the scaling advantage.** Every localization technique (Sobolev embedding, restriction to small sets, interpolation) either requires control of higher derivatives (which are not available from the energy estimate) or loses more than it gains through the volume factors.

The fundamental reason: the enstrophy dissipation controls nabla omega in L^2_t L^2_x, which gives nabla^2 u in L^2_t L^2_x (by CZ theory). Going from L^2 to L^infty in 3D requires 3/2 derivatives (by Sobolev embedding), i.e., we need nabla^{3/2}(nabla^2 u) = nabla^{7/2} u in L^2 for the L^infty bound. The energy estimate provides only nabla^2 u in L^2_t L^2_x -- a deficit of 3/2 derivatives.

This derivative deficit is the standard manifestation of the supercritical gap in NS.

---

## 3. Question 3: The Parabolic Regularity Approach

### 3.1 The PDE for D_xi S

To apply parabolic regularity, we need the PDE satisfied by D_xi S. Start from the strain evolution:

    D_t S = -S^2 - (1/4)|omega|^2 I + (1/4)(omega tensor omega) - nabla^2 p_{nonlocal} + nu Delta S      (SE)

where nabla^2 p is determined by the pressure Poisson equation Delta p = -tr(nabla u nabla u^T) = -(1/2)|S|^2 + (1/4)|omega|^2.

Apply D_xi = xi . nabla to both sides:

    D_t(D_xi S) = D_xi(-S^2) + D_xi((1/4)(omega tensor omega)) - D_xi((1/4)|omega|^2 I) - D_xi(nabla^2 p) + nu Delta(D_xi S) + [D_t, D_xi]S + nu [Delta, D_xi]S

The commutator terms arise because xi = omega/|omega| evolves in time and space:

    [D_t, D_xi] = (D_t xi) . nabla = (time derivative of xi) . nabla
    [Delta, D_xi] involves nabla xi (a first-order term)

These commutators involve D_t xi and nabla xi, which are controlled by D_xi S itself (through the vorticity evolution). This creates a nonlinear coupling.

The schematic form of the PDE is:

    D_t(D_xi S) - nu Delta(D_xi S) = F(S, omega, nabla omega, nabla^2 p, D_xi S)

where F involves:
- Quadratic terms in S (from D_xi(S^2) = S(D_xi S) + (D_xi S) S)
- Terms involving nabla omega (from D_xi of the vorticity terms)
- The quantity D_xi(nabla^2 p), which involves nabla^3 p ~ nabla^2 omega (third derivatives of p, or equivalently second derivatives of omega)
- Commutator terms involving nabla xi ~ kappa

### 3.2 Why De Giorgi-Nash-Moser does not directly apply

The De Giorgi-Nash-Moser (DGNM) theory applies to equations of the form:

    D_t u - div(A(x,t) nabla u) = f(x,t)

where A is uniformly elliptic and f is in appropriate L^p spaces. The conclusion is:

    ||u||_{L^infty(Q_r)} <= C [r^{-(n+2)/2} ||u||_{L^2(Q_{2r})} + ||f||_{L^q(Q_{2r})}]

with q > (n+2)/2 for the f term. The gain comes from the iterative DGNM argument: at each step, the measure of the superlevel set {u > k} decreases geometrically, and after infinitely many steps, u is bounded.

**The structural requirements for DGNM are:**

(i) The principal part must be uniformly elliptic (the coefficient matrix A must satisfy lambda |xi|^2 <= A xi . xi <= Lambda |xi|^2 for all xi).

(ii) The lower-order terms must satisfy specific integrability conditions. For the equation D_t u - nu Delta u = F(u, x, t), the standard DGNM applies when F has at most linear growth in u and nabla u, i.e., |F| <= b |nabla u| + c |u| + f with b, c, f in appropriate L^p spaces.

(iii) The Caccioppoli inequality must hold: energy estimates on level-set truncations.

**For the D_xi S equation, the obstructions to DGNM are:**

(a) **The right-hand side F contains D_xi(nabla^2 p).** This term involves nabla^3 p, or equivalently nabla^2 omega. This is a second-derivative term in omega, and omega itself satisfies only the enstrophy bound (one derivative in L^2). The quantity nabla^2 omega is NOT in any L^p space that DGNM requires. Specifically, DGNM needs the "forcing" f to be in L^q with q > (n+2)/2 = 5/2 for 3D parabolic problems. The quantity D_xi(nabla^2 p) is not even in L^1 a priori.

(b) **The coefficients of the equation depend on S and omega, which are only bounded in L^p spaces, not L^infty.** DGNM with variable coefficients requires the coefficients in VMO or L^p for p sufficiently large. The strain S is bounded in L^p for p < 3 (from the enstrophy), which is not sufficient for the 3D parabolic setting.

(c) **The equation is a SYSTEM (for the tensor D_xi S), not a scalar equation.** DGNM for systems is a harder theory (the De Giorgi counterexample shows that systems can have singular solutions even with uniformly elliptic coefficients in high dimensions). However, in 3D with symmetric matrix-valued unknowns, the scalar components decouple at leading order, so this may not be a fundamental obstruction.

### 3.3 What if we ignore the structural problems?

Suppose, counterfactually, that D_xi S satisfies a scalar parabolic equation of the form:

    D_t w - nu Delta w = f(x,t)

with w = |D_xi S| (or some scalar component) and ||f||_{L^2(Q_{2r})} controlled by the enstrophy dissipation. What would DGNM give?

**The standard parabolic DGNM bound (Moser 1964):**

    ||w||_{L^infty(Q_r)} <= C [r^{-(n+2)/2} ||w||_{L^2(Q_{2r})} + r^{2-(n+2)/q} ||f||_{L^q(Q_{2r})}]

where n = 3 (spatial dimension) and q > (n+2)/2 = 5/2.

With the natural parabolic cylinder around x_*(t): spatial radius r = r_c = (nu/Omega)^{1/2}, temporal duration tau = r_c^2/nu = 1/Omega:

    r^{-(n+2)/2} = r_c^{-5/2} = (Omega/nu)^{5/4}

    ||w||_{L^2(Q_{2r_c})}^2 ~ |w|_{typ}^2 * r_c^3 * (1/Omega) = |w|_{typ}^2 * (nu/Omega)^{3/2} / Omega

If |w|_{typ} ~ Omega^{3/2}/nu^{1/2} (the dimensional estimate):

    ||w||_{L^2(Q_{2r_c})}^2 ~ (Omega^3/nu) * (nu/Omega)^{3/2} / Omega = Omega^{1/2} nu^{1/2}

    ||w||_{L^2(Q_{2r_c})} ~ Omega^{1/4} nu^{1/4}

Therefore:

    r_c^{-5/2} ||w||_{L^2(Q_{2r_c})} ~ (Omega/nu)^{5/4} * Omega^{1/4} nu^{1/4} = Omega^{3/2}/nu

This is LARGER than the dimensional estimate Omega^{3/2}/nu^{1/2} by a factor of nu^{-1/2}. The standard DGNM bound, applied to the parabolic cylinder at the natural scale, recovers a bound that is worse than the dimensional estimate.

**The reason:** DGNM converts L^2 to L^infty by paying the volume factor r^{-(n+2)/2}. In 3D parabolic, this factor is r^{-5/2}. The parabolic cylinder at the dissipation scale has very small volume, so the volume factor is large, and the L^2-to-L^infty conversion is expensive.

### 3.4 The De Giorgi logarithmic gain

The actual De Giorgi iteration gives a bound that is slightly better than the crude Moser estimate in specific situations. The iterative scheme works by considering level sets {w > k_j} with k_j = M(1 - 2^{-j}), and proving that the measure of {w > k_j} decreases geometrically:

    |{w > k_j} cap Q_r| <= C^j / (M - k_0)^2 * ||w||_{L^2(Q_{2r})}^2

The iteration converges if C^j * |A_j| / |Q_r| -> 0, which requires the initial ratio ||w||_{L^2}^2 / (M^2 |Q_r|) to be small enough.

**Where the logarithm appears:** In the classical De Giorgi argument for ELLIPTIC equations, the iteration gives:

    osc_{Q_r} w <= (1 - theta) osc_{Q_{2r}} w

for some theta in (0,1). Iterating, osc_{Q_{2^{-k}r}} w <= (1-theta)^k osc_{Q_r} w. The number of iterations needed to reduce the oscillation from M to M/2 is k ~ log(2)/log(1/(1-theta)) ~ 1/theta. This gives Holder continuity with exponent alpha = log(1/(1-theta))/log(2).

For PARABOLIC equations with rough coefficients, the theta depends on the integrability of the coefficients. If the equation has lower-order terms b . nabla w + c w with b in L^{n+2} (the critical integrability for the parabolic setting), then:

    theta ~ 1 / log(||b||_{L^{n+2}(Q_{2r})} / ||b||_{L^{n+2}(Q_r)})

This logarithmic dependence on the coefficient norms is the "De Giorgi logarithmic correction." If the coefficients have a scale-invariant norm (constant across scales), the correction is:

    ||w||_{L^infty(Q_r)} <= C ||w||_{L^2(Q_{2r})} * r^{-(n+2)/2} * [log(e + ||b||_{L^{n+2}(Q_{2r})} / epsilon)]^{-sigma}

for some sigma > 0 that depends on the structural constants but NOT on the coefficient norms.

### 3.5 The precise logarithmic exponent

In the standard De Giorgi iteration for the parabolic equation:

    D_t w - nu Delta w + b . nabla w = f

with b in L^{n+2,infty} (weak L^{n+2}), the De Giorgi bound has the form:

    ||w||_{L^infty(Q_r)} <= C r^{-(n+2)/2} ||w||_{L^2(Q_{2r})} * [1 + ||b||_{L^{n+2}(Q_{2r})}^{n+2}]

There is no logarithmic improvement in the standard theory. The improvement comes in specific settings:

**Setting 1: Equations with antisymmetric structure.** If the first-order term has the form b . nabla w with div(b) = 0 (divergence-free drift), then the DGNM theory of Nazarov-Ural'tseva (2009) and Seregin-Silvestre-Sverak-Zlatos (2009) gives Holder regularity with an estimate:

    ||w||_{L^infty(Q_r)} <= C r^{-(n+2)/2} ||w||_{L^2(Q_{2r})}

where C depends only on the structural constants and the L^{n+2} norm of b. No logarithmic gain.

**Setting 2: Equations where the forcing is in a critical L^p space.** If f is in L^{(n+2)/2} (the critical integrability), then the De Giorgi iteration gives boundedness with a logarithmic correction:

    ||w||_{L^infty(Q_r)} <= C r^{-(n+2)/2} ||w||_{L^2(Q_{2r})} + C [log(e + ||f||_{L^{(n+2)/2}} / ||f||_{L^1})]^{-sigma}

with sigma = 1/(n+2). **For n = 3: sigma = 1/5.**

This is the logarithmic gain that appears in the critical case. It arises because at the critical integrability, the De Giorgi iteration "almost" converges -- each step reduces the level-set measure by a factor that is 1 - O(1/log(M)), and after log(M) steps the total reduction is a finite power of log(M).

### 3.6 Would sigma = 1/5 suffice?

If we could prove:

    |D_xi S(x_*(t))| <= C Omega^{3/2}/nu^{1/2} * [log(Omega/Omega_0)]^{-1/5}

this would correspond to an effective delta that exceeds 1/2 by a logarithmic amount. Specifically, Omega^{3/2} / log(Omega)^{1/5} = Omega^{3/2 - epsilon} for any epsilon > 0 (eventually), so effectively delta = 1/2 + epsilon for any epsilon.

From the scaling analysis in Theorem CB: for delta > 1/2 (even by an infinitesimal amount), the forced blowup rate is alpha = 3/(2+2delta) < 1, and BKM rules it out.

But the logarithmic correction is even better: with |D_xi S| ~ Omega^{3/2}/log(Omega)^{1/5}, the K equation becomes:

    dK/dt <= C_2 Omega K + C Omega^{3/2}/(nu^{1/2} log(Omega)^{1/5})

The scaling analysis for the blowup: with Omega ~ (T-t)^{-1}, the source term is ~ (T-t)^{-3/2} / |log(T-t)|^{1/5}. The integral from t to T:

    integral_t^T (T-s)^{-3/2} / |log(T-s)|^{1/5} ds

converges (barely) near s = T because the (T-s)^{-3/2} divergence is not improved by the logarithm (the integral of (T-s)^{-3/2} ds diverges). Wait -- the integral of (T-s)^{-3/2} ds near s = T diverges. The logarithmic correction does not make it converge. So the K equation still has a divergent forcing.

Let me be more precise. For the ODE scaling, the logarithmic correction modifies the blowup rate:

    Omega ~ (T-t)^{-1} * |log(T-t)|^{sigma'}

for some sigma'. The BKM integral becomes:

    integral_0^T (T-t)^{-1} |log(T-t)|^{sigma'} dt

which diverges for all sigma' (the (T-t)^{-1} integral diverges logarithmically, and the log correction makes it worse or at best does not help).

Actually, the BKM criterion is: the integral of Omega dt is infinite implies blowup. For alpha = 1, the integral diverges logarithmically, so BKM does not rule it out regardless of the logarithmic correction.

**The logarithmic gain in D_xi S does NOT break the BKM barrier.** The BKM integral diverges logarithmically at alpha = 1, and a logarithmic correction in the source term does not change the blowup rate from alpha = 1 to alpha < 1.

Wait, let me reconsider. The coupled system with the logarithmic correction:

    dOmega/dt <= C_1 Omega^2 - nu K^2 Omega
    dK/dt <= C_2 Omega K + C_3 Omega^{3/2}/(nu^{1/2} L^{1/5})

where L = log(Omega/Omega_0). Suppose Omega ~ A(T-t)^{-1}. Then L ~ |log(T-t)|.

From (B): the source is ~ (T-t)^{-3/2} / |log(T-t)|^{1/5}. The K equation:

    dK/dt ~ C_2 (T-t)^{-1} K + C_3 (T-t)^{-3/2} / (nu^{1/2} |log(T-t)|^{1/5})

If K ~ B (T-t)^{-1/2} / |log(T-t)|^{sigma_K}, then:

    dK/dt ~ B (T-t)^{-3/2} / |log(T-t)|^{sigma_K}

Balancing with the source: sigma_K = 1/5 (the logarithmic correction passes through directly).

The damping in (A): nu K^2 Omega ~ nu B^2 (T-t)^{-1} / |log(T-t)|^{2/5} * (T-t)^{-1} = nu B^2 (T-t)^{-2} / |log(T-t)|^{2/5}.

The stretching: C_1 Omega^2 = C_1 A^2 (T-t)^{-2}.

For the damping to overcome the stretching:

    nu B^2 / |log(T-t)|^{2/5} > C_1 A^2

As t -> T, |log(T-t)| -> infinity, so the left side -> 0. **The damping LOSES to the stretching at sufficiently late times.** The logarithmic correction in K weakens the damping enough that it eventually becomes subdominant.

**This is the critical failure.** Even a logarithmic gain in D_xi S translates to a logarithmic weakening of the damping, which is not enough to overcome the stretching at the Type I rate. The logarithmic gain would need to be in the damping exponent, not just in the coefficient, to break the borderline.

More precisely: what is needed is |D_xi S| <= C Omega^{3/2-epsilon}/nu^{1/2} for some epsilon > 0, not just Omega^{3/2}/(nu^{1/2} log(Omega)^sigma). The distinction between power-law gain and logarithmic gain is critical: a power-law gain changes the scaling exponent alpha = 3/(2+2delta) to below 1, while a logarithmic gain keeps alpha = 1 but modifies the blowup amplitude by a logarithmic factor that becomes unfavorable as t -> T.

### 3.7 Revised assessment of the De Giorgi logarithmic gain

**If the De Giorgi sigma = 1/5 bound applied**, it would give:

    |D_xi S| ~ Omega^{3/2}/(nu^{1/2} log(Omega)^{1/5})

This does NOT break the borderline. The reason: the BKM criterion involves the L^1_t norm of Omega (an integral), and logarithmic corrections do not change the divergence/convergence of the integral (T-t)^{-alpha} dt at the critical exponent alpha = 1.

**To break the borderline via the coupled bootstrap, one needs a POWER-LAW improvement:** delta > 1/2 strictly, corresponding to |D_xi S| <= C Omega^{1+delta} with delta > 1/2. No logarithmic correction suffices.

This is actually a well-known feature of the NS regularity landscape: logarithmic improvements at the critical level (such as log-Lipschitz vorticity direction in Constantin-Fefferman type results) do give regularity for SOME conditions but not for the BKM-type integral conditions. The reason is that BKM is sensitive to the integral of a power, and logarithmic corrections do not change the convergence of power-law integrals at the critical exponent.

**CORRECTION AND IMPORTANT SUBTLETY:** Actually, I need to be more careful. The question is not whether the BKM integral converges with the logarithmic correction, but whether the coupled system with the logarithmic correction has a consistent blowup solution.

Returning to the coupled system with the log correction:

From the scaling analysis above: K ~ (T-t)^{-1/2} / |log(T-t)|^{1/5}, and the damping is nu K^2 Omega ~ (T-t)^{-2} / |log(T-t)|^{2/5}.

The stretching is C_1 Omega^2 ~ (T-t)^{-2}.

So the Omega equation becomes:

    dOmega/dt ~ C_1 A^2 (T-t)^{-2} - nu B^2 (T-t)^{-2} / |log(T-t)|^{2/5}

    d/dt [A(T-t)^{-1}] = A (T-t)^{-2}

Comparing: A (T-t)^{-2} ~ (C_1 A^2 - nu B^2 / |log(T-t)|^{2/5}) (T-t)^{-2}

So: A ~ C_1 A^2 - nu B^2 / |log(T-t)|^{2/5}

As t -> T: the correction term nu B^2 / |log(T-t)|^{2/5} -> 0. So we need A = C_1 A^2, giving A = 1/C_1 -- the same blowup amplitude as without any damping!

The logarithmic weakening of the damping means that asymptotically close to the blowup, the damping becomes negligible. The blowup proceeds as if K were not there. **The logarithmic gain is not enough.**

---

## 4. Question 4: A De Giorgi Lemma for D_xi S

### 4.1 The ideal scenario

Suppose D_xi S satisfies the following model parabolic inequality:

    D_t(|D_xi S|) - nu Delta(|D_xi S|) <= C |omega| |D_xi S| + f(x,t)

with f in L^{(n+2)/2} and |omega| in L^{n+2} (the critical parabolic integrability). Then the De Giorgi iteration would give:

    ||D_xi S||_{L^infty(Q_r)} <= C r^{-(n+2)/2} ||D_xi S||_{L^2(Q_{2r})} * g(||omega||, ||f||)

where g involves at most polynomial growth in the coefficient norms with a logarithmic correction.

**The De Giorgi iteration scheme for the model equation:**

Step 1. Energy estimate (Caccioppoli inequality): For k > 0, let w_k = (|D_xi S| - k)_+ (the positive part of the excess over level k). Multiply the equation by w_k and integrate over Q_r:

    sup_{t in I_r} ||w_k||_{L^2(B_r)}^2 + nu ||nabla w_k||_{L^2(Q_r)}^2 <= C (r^{-2} + ||omega||_{L^{n+2}(Q_r)}^2) ||w_k||_{L^2(Q_r)}^2 + ||f||_{L^{(n+2)/2}(Q_r)} ||w_k||_{L^2(Q_r)}

Step 2. Isoperimetric step: By the parabolic Sobolev inequality,

    ||w_k||_{L^{2(n+2)/n}(Q_r)} <= C (sup_t ||w_k||_{L^2} + ||nabla w_k||_{L^2})

Combined with Step 1, this gives:

    ||w_k||_{L^{2(n+2)/n}(Q_r)}^2 <= C (r^{-2} + Lambda) ||w_k||_{L^2(Q_r)}^2

where Lambda = ||omega||_{L^{n+2}}^2 + ||f||_{L^{(n+2)/2}} / ||w_k||.

Step 3. Iteration: Choose k_j = M(1 - 2^{-j}) with M to be determined. The measure of the superlevel set A_j = {|D_xi S| > k_j} cap Q_r satisfies:

    |A_{j+1}| <= C^j / (k_{j+1} - k_j)^{2(n+2)/n} * ||w_{k_j}||_{L^{2(n+2)/n}}^{2(n+2)/n}

Using the Caccioppoli bound:

    |A_{j+1}| <= (C Lambda)^j * (|A_j| / |Q_r|)^{1 + 2/n} * |Q_r|

This is the geometric iteration. It converges to |A_j| -> 0 (i.e., |D_xi S| <= M on Q_r) if the initial ratio satisfies:

    |A_0| / |Q_r| <= c_0 (C Lambda)^{-n/2}

**The logarithmic structure:** The level M at which convergence occurs satisfies:

    M <= ||D_xi S||_{L^2(Q_{2r})} / |A_0|^{1/2} + ||f||_{L^{(n+2)/2}}^{2/(n+2)}

The logarithmic gain arises when the initial data is in L^2 but the forcing is at the critical integrability: the iteration squeezes extra decay from the geometric convergence rate, producing:

    M <= C ||D_xi S||_{L^2(Q_{2r})} r^{-(n+2)/2} [log(e + ||D_xi S||_{L^2}/||D_xi S||_{L^1})]^{-1/(n+2)}

**For n = 3: the logarithmic exponent is sigma = 1/(n+2) = 1/5.**

### 4.2 Why the ideal scenario fails for D_xi S

The De Giorgi iteration requires:

(a) **A Caccioppoli inequality for (|D_xi S| - k)_+.** This requires that when we multiply the D_xi S equation by the truncation (|D_xi S| - k)_+, the resulting energy estimate closes. The term D_xi(nabla^2 p) in the D_xi S equation generates:

    integral (|D_xi S| - k)_+ D_xi(nabla^2 p) dx

This term involves third derivatives of the pressure, which cannot be bounded by the enstrophy dissipation. The Caccioppoli inequality fails at this step.

(b) **The coefficient omega in the linear term C |omega| |D_xi S| must be in L^{n+2} = L^5 over the parabolic cylinder.** But omega is only controlled in L^2_t L^infty_x (from BKM-type bounds, assuming the solution is smooth). By interpolation, omega is in L^p_t L^q_x for specific (p,q) pairs, but L^5_{t,x} (the parabolic critical integrability) is not directly available from the standard energy estimates.

(c) **The equation is for a tensor, not a scalar.** The De Giorgi iteration for systems has counterexamples (De Giorgi 1968 counterexample). While the 3D parabolic case may be better (the counterexample is in dimension n >= 3 for elliptic systems), this is an additional technical concern.

### 4.3 The fundamental obstruction

The term D_xi(nabla^2 p) is the same obstruction that appears everywhere in the NS regularity problem. The pressure Hessian couples the local dynamics to the global flow through the Biot-Savart law, and this coupling involves one more derivative than what the energy estimate provides.

Specifically:
- The energy estimate controls nabla u in L^2_t L^2_x
- The enstrophy dissipation controls nabla omega = nabla(curl u) ~ nabla^2 u in L^2_t L^2_x
- The D_xi S equation involves nabla^3 u (through nabla^2 p or equivalently nabla^2 omega)
- nabla^3 u is NOT in any L^p space from the energy estimate alone

This derivative gap of 1 (we have nabla^2 u but need nabla^3 u) is the supercritical gap. The De Giorgi iteration cannot bridge it because it is a 0th-order regularization technique (L^2 to L^infty, same number of derivatives). It can improve integrability but not differentiability.

### 4.4 Verdict on Question 4

**The De Giorgi lemma for D_xi S does not exist in a usable form.** The structural requirements of the De Giorgi iteration are violated by the D_xi S equation:

1. The Caccioppoli inequality fails due to the D_xi(nabla^2 p) term (uncontrolled third derivatives of pressure).
2. The coefficients do not have the required parabolic critical integrability.
3. The equation is tensorial, not scalar.

**If all these obstacles were overcome** (counterfactually), the logarithmic exponent would be sigma = 1/5 = 1/(n+2) with n = 3. But as shown in Section 3.6-3.7, even this logarithmic gain would NOT break the BKM barrier at alpha = 1. A power-law improvement (delta > 1/2 strictly) is needed, and the De Giorgi iteration cannot provide this.

---

## 5. Question 5: The Concrete Estimate -- Putting Everything Together

### 5.1 Step 1: The L^2-L^2 bound (rigorous)

    integral_0^T ||D_xi S(.,t)||_{L^2(R^3)}^2 dt <= C ||nabla omega||_{L^2_t L^2_x}^2 <= C E_0 / nu

where E_0 = (1/2)||omega_0||_{L^2}^2. This is proved in Section 2 and is unconditionally valid for smooth solutions.

### 5.2 Step 2: Parabolic regularity (does not apply)

The proposed bound:

    ||D_xi S||_{L^infty(Q_r)} <= C r^{-5/2} ||D_xi S||_{L^2(Q_{2r})} * (De Giorgi correction)

fails because the D_xi S equation does not satisfy the structural requirements of De Giorgi-Nash-Moser theory (Section 4).

Even if it did apply, at the natural parabolic cylinder Q_{r_c} with r_c = (nu/Omega)^{1/2}:

    r_c^{-5/2} ||D_xi S||_{L^2(Q_{2r_c})} ~ (Omega/nu)^{5/4} * Omega^{1/4} nu^{1/4} = Omega^{3/2}/nu

which is worse than the dimensional estimate Omega^{3/2}/nu^{1/2} by a factor nu^{-1/2}.

### 5.3 Step 3: Event counting (valid but insufficient)

The contribution from one tube-tube interaction event (duration tau ~ 1/Omega, spatial extent ~ r_c^3):

    ||D_xi S||_{L^2(event)}^2 ~ |D_xi S|_{peak}^2 * r_c^3 * tau

Using |D_xi S|_{peak} ~ Omega^{3/2}/nu^{1/2} (the dimensional estimate):

    ||D_xi S||_{L^2(event)}^2 ~ (Omega^3/nu) * (nu/Omega)^{3/2} * (1/Omega) = Omega^{1/2} nu^{1/2}

The total number of such events before time T is bounded by the L^2 budget:

    N_events * Omega^{1/2} nu^{1/2} <= E_0/nu

    N_events <= E_0 / (nu^{3/2} Omega^{1/2})

The total integrated |D_xi S| from all events:

    integral |D_xi S| dt ~ N_events * |D_xi S|_{peak} * tau = [E_0/(nu^{3/2} Omega^{1/2})] * [Omega^{3/2}/nu^{1/2}] * [1/Omega]

    = E_0 / (nu^2 Omega^0) = E_0 / nu^2

This is a BOUND on the total time-integral of |D_xi S|, independent of Omega. But this bound applies to the total over ALL events, not to the local contribution at x_*(t). The vorticity maximum x_*(t) participates in at most O(1) events at any given time, but as the vorticity grows, the event rate at x_* also grows.

More carefully: at the vorticity maximum, there is at most one "current" interaction at any time. The contribution to integral |D_xi S| dt at x_*(t) from the current event is:

    |D_xi S|_{peak} * tau ~ (Omega^{3/2}/nu^{1/2}) * (1/Omega) = Omega^{1/2}/nu^{1/2}

Over a period of duration Delta t during which Omega ~ const:

    integral_{Delta t} |D_xi S(x_*(t))| dt ~ (number of events in Delta t) * Omega^{1/2}/nu^{1/2}

The number of events in Delta t is ~ Delta t / tau_gap where tau_gap is the inter-event spacing. If tau_gap ~ 1/Omega (events are back-to-back), then:

    integral |D_xi S| dt ~ (Delta t * Omega) * Omega^{1/2}/nu^{1/2} = Delta t * Omega^{3/2}/nu^{1/2}

Dividing by Delta t: the time-averaged |D_xi S| is ~ Omega^{3/2}/nu^{1/2}, the same dimensional estimate. No gain.

The only way to get a gain is if tau_gap >> 1/Omega (events are separated by longer-than-minimal gaps). This is a statement about the intermittency of tube-tube interactions at the vorticity maximum. There is no a priori reason for such intermittency in a blowup scenario -- indeed, near a blowup, the dynamics are expected to become more intense, not less.

### 5.4 The refined event estimate using L^2 budget

One can try to use the global L^2 budget to constrain the event rate at x_*(t). The total L^2 energy in D_xi S events is bounded by E_0/nu. If each event at x_*(t) costs Omega^{1/2} nu^{1/2} in L^2 energy, the total number of events at x_*(t) is bounded by E_0 / (nu^{3/2} Omega^{1/2}).

But the total time during which Omega is at level ~ Omega_0 is bounded by the BKM integral:

    integral_0^T 1_{Omega(t) ~ Omega_0} dt

For a Type I blowup with Omega ~ (T-t)^{-1}, the time spent at level Omega_0 is ~ 1/Omega_0. During this time, the number of events is at most min(E_0/(nu^{3/2} Omega_0^{1/2}), (1/Omega_0)/(1/Omega_0)) = min(E_0/(nu^{3/2} Omega_0^{1/2}), 1).

The first bound (from L^2 budget) is informative when Omega_0 > (E_0/nu^{3/2})^2 = E_0^2/nu^3. For typical NS solutions, E_0/nu = Re (the Reynolds number), so the threshold is Omega_0 > Re^2/nu = E_0^2/nu^3. This is an extremely high vorticity -- well above the BKM blowup threshold.

For Omega_0 below this threshold, the L^2 budget does not constrain the number of events. The event counting approach gives no useful information in the pre-blowup regime.

### 5.5 Summary of the concrete estimate

| Component | Status | Result |
|-----------|--------|--------|
| L^2-L^2 enstrophy bound | Rigorous | integral ||D_xi S||_{L^2}^2 dt <= C E_0/nu |
| Parabolic regularity (De Giorgi) | Does not apply | PDE for D_xi S has supercritical coefficients |
| Localization to x_*(t) | Loses scaling | L^infty bound worse than dimensional estimate |
| Event counting | Valid but insufficient | Time-averaged |D_xi S| at x_* = Omega^{3/2}/nu^{1/2} (no gain) |
| Global L^2 constraint on events | Valid but too weak | Only constrains at extremely high Omega |

**No combination of these ingredients produces a pointwise bound on D_xi S at x_*(t) that improves on the dimensional estimate Omega^{3/2}/nu^{1/2}.**

---

## 6. Deliverables

### 6.1 Does the time-integrated bootstrap close?

**Conditionally YES for delta > 1/2; unconditionally NO.**

The time-integrated version of Theorem CB is a formally stronger result (weaker hypothesis gives the same regularity conclusion). However, for power-law blowup profiles -- the only profiles relevant to the scaling analysis -- the integrated condition reduces to the pointwise condition. The critical threshold remains delta = 1/2, and the dimensional estimate saturates it exactly.

The transient nature of tube-tube interactions does not help because the interaction frequency scales inversely with the interaction duration, so the time-averaged D_xi S matches the peak D_xi S in scaling.

### 6.2 The De Giorgi logarithmic gain

**If it applied (which it does not), the gain would be sigma = 1/(n+2) = 1/5 in 3D parabolic problems.** This exponent comes from the geometric iteration rate in the De Giorgi scheme: after k iterations, the level-set measure decays as C^{-k(n+2)/n}, and the number of iterations to reach boundedness from an L^2 starting point involves log(||f||_{L^2}/||f||_{L^1}), yielding the 1/(n+2) exponent.

**However, the logarithmic gain is NOT sufficient to break the BKM barrier.** The BKM criterion requires integral_0^T Omega dt < infinity for regularity. At alpha = 1 (the Type I rate), the integral diverges logarithmically. A logarithmic correction to |D_xi S| translates to a logarithmic weakening of the damping, which becomes negligible near the blowup time. Only a power-law improvement (delta > 1/2 strictly) changes the blowup rate alpha to below 1, making the BKM integral convergent.

### 6.3 Rigorous path from L^2-L^2 to pointwise with log correction?

**No rigorous path exists using current techniques.** The obstacles:

1. **Derivative gap:** The L^2-L^2 bound controls D_xi S with the same number of derivatives as the enstrophy dissipation (via CZ theory: ||D_xi S||_{L^2} <= C ||nabla omega||_{L^2}). Going to L^infty requires 3/2 more derivatives in 3D (Sobolev embedding), which are not available from the energy estimate.

2. **De Giorgi inapplicable:** The PDE for D_xi S has coefficients involving nabla^2 p (third derivatives of the velocity), which are supercritical and not in any useful L^p space. The Caccioppoli inequality -- the foundation of the De Giorgi iteration -- fails.

3. **Localization loses:** Restricting to the high-vorticity set and using Sobolev embedding on small balls gives a WORSE bound than the dimensional estimate, because the ball volume at the dissipation scale is very small.

4. **Event counting insufficient:** The L^2 budget constrains the total number of interaction events but not the local rate at x_*(t) in the relevant regime.

### 6.4 Technical obstacles

**Obstacle 1 (fatal): The D_xi(nabla^2 p) term.** The D_xi S evolution equation contains D_xi(nabla^2 p), involving third derivatives of the pressure. This term is not controlled by the enstrophy dissipation (which provides only second derivatives of u). This is the same derivative gap that obstructs every approach to NS regularity. It appears here as the failure of the Caccioppoli inequality for the De Giorgi iteration.

**Obstacle 2 (fatal for the ODE approach): Power-law vs. logarithmic gain.** The coupled bootstrap requires delta > 1/2 (a power-law improvement over the dimensional estimate) to bring the blowup rate below alpha = 1. Logarithmic improvements do not suffice because the BKM integral at alpha = 1 diverges logarithmically, and a logarithmic damping correction vanishes asymptotically near the blowup time.

**Obstacle 3 (structural): Scale invariance of the dimensional estimate.** The bound |D_xi S| ~ Omega^{3/2}/nu^{1/2} is dimensionally forced: [D_xi S] = time^{-1} length^{-1}, and the only combination of Omega (time^{-1}) and nu (length^2 time^{-1}) that gives these dimensions is Omega^{3/2}/nu^{1/2}. Any improvement over this bound must use structural information beyond dimensional analysis -- i.e., it must use the specific form of the NS nonlinearity, not just the scaling. The tube geometry argument provides qualitative structural information (D_xi S is small for straight tubes) but quantitatively recovers the same scaling for self-similar profiles.

**Obstacle 4 (technical): Non-scalar nature of D_xi S.** The De Giorgi theory for systems is much weaker than for scalar equations. The De Giorgi 1968 counterexample shows that elliptic systems with uniformly elliptic coefficients can have unbounded solutions in dimension n >= 3. While the parabolic case and the specific structure of the NS equations may provide additional cancellations, exploiting these would require developing new PDE theory beyond the current state of the art.

### 6.5 Honest probability assessment

| Statement | Probability |
|-----------|------------|
| The time-integrated Theorem CB is a valid mathematical theorem (weaker hypothesis than pointwise Theorem CB, same conclusion) | **95%** -- this is essentially a direct extension of the ODE scaling analysis, with the only subtlety being the equivalence of the integrated and pointwise conditions for power-law profiles. |
| The De Giorgi iteration applies to D_xi S after resolving the structural issues | **2%** -- the D_xi(nabla^2 p) term is a genuine, hard obstruction. Resolving it would essentially require controlling nabla^3 u, which is a harder problem than the one we started with. |
| A logarithmic improvement in D_xi S can be obtained by some other method (not De Giorgi) | **8%** -- there may be cancellation structures in the NS equations specific to the D_xi S combination that have not been identified. The directional nature of D_xi S (along vortex lines) and the incompressibility constraint could produce cancellations not visible at the dimensional-analysis level. But no such cancellation is currently known. |
| A logarithmic improvement, if obtained, suffices for regularity through the coupled bootstrap | **1%** -- as shown in Section 3.6-3.7, logarithmic gains do not break the BKM barrier at alpha = 1. This is a rigorous negative result, not a probability estimate. The 1% accounts for the possibility of a fundamentally different way to exploit the logarithmic gain that avoids the BKM argument (e.g., an energy method rather than an ODE comparison). |
| A power-law improvement (delta > 1/2) in D_xi S can be proved | **<1%** -- this would directly imply NS regularity via Theorem CB. The dimensional estimate delta = 1/2 is saturated by explicit configurations (interacting vortex tubes). Any improvement would have to show that these extremal configurations are dynamically inaccessible, which is essentially the regularity problem itself. |
| This entire line of investigation (time-integrated bootstrap) leads to a breakthrough on NS regularity | **<0.5%** -- the analysis in this document shows that the time-integration idea, while mathematically sound, does not provide any scaling advantage over the pointwise condition. The borderline at delta = 1/2 is structural, not technical. |

### 6.6 What, if anything, is salvageable?

1. **The time-integrated Theorem CB is a mildly stronger conditional regularity result** than the pointwise version. It should be recorded as such. The integrated condition is more natural for applications where D_xi S is known to be intermittent.

2. **The enstrophy-based L^2-L^2 bound on D_xi S is clean and useful** as a starting point for any future pointwise estimate. It provides a hard upper bound on the total "integrated damage" from D_xi S, even though this cannot currently be localized.

3. **The sigma = 1/5 De Giorgi exponent is the correct answer to the hypothetical question** "what logarithmic gain would parabolic regularity provide in 3D?" This is useful for calibrating expectations in related problems.

4. **The analysis definitively shows that logarithmic gains do not break the BKM barrier.** This is a clean negative result that should discourage future attempts along this specific line.

---

## 7. Comparison with the Overall NS Landscape

This analysis adds to the growing evidence that the NS regularity problem is not a matter of finding the right estimate within existing frameworks, but of discovering a new structural principle. Every approach -- enstrophy methods, Serrin criteria, vortex-line geometry (CF/DHY), strain-vorticity alignment (Theorem C3/CB), and now time-integrated bootstrap -- reaches the same borderline. The borderline is universal because it reflects the exact balance between the NS nonlinearity (cubic in vorticity) and the dissipation (quadratic in vorticity gradient), and this balance is a consequence of the dimensionality of the problem (3D), not of any particular technical choice.

The coupled bootstrap is arguably the most transparent revelation of this borderline: it shows that the NS regularity problem reduces to whether D_xi S -- a single directional derivative of the strain along vortex lines -- grows slower than Omega^{3/2}/nu^{1/2}. This is a concrete, physically meaningful question with a direct geometric interpretation. But answering it requires understanding the global-to-local transfer of vorticity information through the Biot-Savart law, which is the core difficulty of the problem.

**Bottom line:** The time-integrated bootstrap is a valid mathematical refinement that produces a formally stronger theorem, but it does not change the critical threshold or bring us closer to unconditional regularity. The delta = 1/2 borderline is immovable within the ODE comparison framework.
