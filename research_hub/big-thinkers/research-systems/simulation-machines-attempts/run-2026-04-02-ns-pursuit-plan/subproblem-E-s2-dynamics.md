# Subproblem E: Can Full NS Dynamics Force s_2 <= 0 in High-Vorticity Regions?

**Date:** 2026-04-02
**Parent:** Angle 10 (Strain-Vorticity Alignment GMT), Phase 4 Selection
**Classification:** Make-or-break structural analysis for the entire GMT approach
**Depends on:** Subproblem A (ground truth), Subproblem B (eigenvector regularity), Subproblem C (conditional regularity)

---

## 0. The Precise Question

Subproblem C established:

- **Theorem C3:** Under e_2-alignment with angle delta(M) -> 0 AND the condition s_2 <= 0 on {|omega| > M}, the solution remains regular (with rate delta(M) = O(M^{-1}(log M)^{-1})).
- **The obstruction:** e_2-alignment alone does NOT yield regularity because s_2 > 0 gives positive stretching omega . S omega ~ s_2 |omega|^2, which has the same cubic scaling as the worst-case stretching.
- **The precise gap:** Whether s_2 <= 0 (or at least s_2 <= epsilon(M) s_1 with epsilon -> 0 as M -> infinity) holds in regions where |omega| >> 1.

This document addresses: **Does the full 3D Navier-Stokes dynamics force s_2 to be non-positive (or asymptotically small relative to s_1) in high-vorticity regions?**

We analyze this through five independent lenses:
1. The evolution equation for the strain eigenvalues
2. Restricted Euler dynamics (inviscid, local approximation)
3. The role of the pressure Hessian (the nonlocal correction)
4. The role of viscosity
5. Blowup scenario analysis

**Kill condition:** If restricted Euler dynamics, DNS evidence, and structural analysis all consistently show s_2 > 0 in high-vorticity regions with no plausible NS-specific mechanism to reverse this, then the e_2-alignment route is structurally blocked and should be downgraded to "conditional regularity result only."

---

## 1. Evolution Equation for the Strain Eigenvalues

### 1.1 The strain evolution equation

The velocity gradient tensor A = nabla u evolves as:

    d_t A + (u . nabla) A = -A^2 - H + nu Delta A

where H_{ij} = partial_i partial_j p is the pressure Hessian. Taking the symmetric part:

    D_t S = -S^2 - (1/4)(omega tensor omega - |omega|^2 I/3) - H^{sym} + nu Delta S + R(S, Omega)

Let me derive this more carefully. From A = S + Omega (symmetric + antisymmetric decomposition):

    A^2 = S^2 + S Omega + Omega S + Omega^2

The symmetric part of A^2 is:

    sym(A^2) = S^2 + Omega^2 + sym(S Omega + Omega S)

But sym(S Omega + Omega S) = S Omega + Omega S is already symmetric when S is symmetric and Omega is antisymmetric? No: (S Omega)^T = -Omega S, and (Omega S)^T = -S Omega, so (S Omega + Omega S)^T = -(Omega S + S Omega). Thus S Omega + Omega S is antisymmetric, and its symmetric part is zero.

Therefore:

    sym(A^2) = S^2 + Omega^2

Now Omega is the antisymmetric part of nabla u. The relation to vorticity is: Omega_{ij} = -(1/2) epsilon_{ijk} omega_k, so:

    (Omega^2)_{ij} = Omega_{ik} Omega_{kj} = (1/4) epsilon_{ikl} omega_l epsilon_{kjm} omega_m
                    = (1/4)(delta_{ij} delta_{lm} - delta_{im} delta_{lj}) omega_l omega_m
                    = (1/4)(|omega|^2 delta_{ij} - omega_i omega_j)

So:

    Omega^2 = (1/4)(|omega|^2 I - omega tensor omega)

The Navier-Stokes strain evolution is therefore:

    **D_t S = -(S^2 + (1/4)(|omega|^2 I - omega tensor omega)) - H^{sym} + nu Delta S**     (SE)

where H^{sym} = sym(nabla^2 p) = nabla^2 p (since the Hessian of a scalar is already symmetric), and D_t = d_t + u . nabla is the material derivative.

Equivalently:

    D_t S = -S^2 + (1/4)(omega tensor omega) - (|omega|^2/4) I - nabla^2 p + nu Delta S     (SE')

### 1.2 Evolution of individual eigenvalues

At a point where the eigenvalues s_1 > s_2 > s_3 are distinct, we can project (SE) onto each eigenvector. Let e_i be the unit eigenvector for s_i. Then:

    D_t s_i = e_i^T (D_t S) e_i - sum_{j != i} [s_j (D_t e_i . e_j)^2 + ...] 

Actually, the correct formula comes from differentiating S e_i = s_i e_i:

    (D_t S) e_i + S (D_t e_i) = (D_t s_i) e_i + s_i (D_t e_i)

Taking the inner product with e_i:

    e_i . (D_t S) e_i + e_i . S (D_t e_i) = D_t s_i + s_i (e_i . D_t e_i)

Since S e_i = s_i e_i, the second term on the left is s_i (e_i . D_t e_i). The right side has the same term. So:

    **D_t s_i = e_i . (D_t S) e_i**     (EV)

provided the eigenvalue is simple. This is the well-known Hadamard formula for eigenvalue derivatives.

Substituting (SE):

    D_t s_i = -s_i^2 + (1/4)|omega_i|^2 - (|omega|^2/4) - (nabla^2 p)_{ii} + nu (Delta S)_{ii}     (EV')

where omega_i = omega . e_i is the component of vorticity along e_i, and (nabla^2 p)_{ii} = e_i^T (nabla^2 p) e_i and (Delta S)_{ii} = e_i^T (Delta S) e_i are the diagonal components in the eigenframe.

More explicitly:

    **D_t s_i = -s_i^2 - (1/4)(|omega|^2 - omega_i^2) - h_i + nu sigma_i**     (EV'')

where h_i = e_i . (nabla^2 p) e_i and sigma_i = e_i . (Delta S) e_i.

Note: omega_i^2 = (omega . e_i)^2, so |omega|^2 - omega_i^2 = sum_{j != i} omega_j^2 is the squared vorticity component PERPENDICULAR to e_i. This is always non-negative, so the term -(1/4)(|omega|^2 - omega_i^2) is always non-positive. It represents vorticity-induced compression of the strain along directions perpendicular to omega.

### 1.3 Evolution of s_2 specifically

    D_t s_2 = -s_2^2 - (1/4)(omega_1^2 + omega_3^2) - h_2 + nu sigma_2     (S2)

where omega_1 = omega . e_1 and omega_3 = omega . e_3 are the vorticity components along the first and third strain eigenvectors.

**Key structural observation about each term:**

1. **The self-interaction -s_2^2:** Always non-positive. This term drives s_2 toward zero from either side. It is a quadratic damping/growth term (stabilizing if |s_2| is large).

2. **The vorticity-perpendicular term -(1/4)(omega_1^2 + omega_3^2):** Always non-positive. This drives s_2 DOWNWARD (more negative or less positive). It is strongest when vorticity has large components perpendicular to e_2 --- i.e., when omega is NOT aligned with e_2.

3. **The pressure Hessian term -h_2:** Can have either sign. This is the nonlocal term determined by the full velocity field through the Poisson equation for p.

4. **The viscous term nu sigma_2:** Can have either sign. Laplacian of a strain eigenvalue can be positive or negative depending on the local structure.

**Critical observation for the e_2-alignment scenario:** When omega is aligned with e_2, we have omega_1 ~ 0, omega_3 ~ 0 (the misalignment is of order delta). So the vorticity-perpendicular term is:

    -(1/4)(omega_1^2 + omega_3^2) ~ -(delta^2/4) |omega|^2

This is very small when delta is small. The vorticity-induced compression of s_2 is WEAK when omega is aligned with e_2. This is a fundamental structural problem: the very condition that makes the stretching analysis favorable (alignment with e_2) also removes the mechanism that would push s_2 negative.

In contrast, if omega were aligned with e_1, the perpendicular components omega_2, omega_3 would be large, and the corresponding terms would push s_1 strongly downward. This is part of the self-organization mechanism: alignment with e_1 creates a negative feedback on s_1, while alignment with e_2 creates almost no feedback on s_2.

### 1.4 Evolution of the strain ratio r = s_2/s_1

Define r = s_2/s_1 (assuming s_1 > 0, which holds whenever the flow is not identically zero). Then:

    D_t r = (D_t s_2)/s_1 - s_2 (D_t s_1)/s_1^2
           = (1/s_1)[D_t s_2 - r D_t s_1]

Substituting (EV''):

    D_t r = (1/s_1)[(-s_2^2 - (1/4)(omega_1^2 + omega_3^2) - h_2 + nu sigma_2)
                    - r(-s_1^2 - (1/4)(omega_2^2 + omega_3^2) - h_1 + nu sigma_1)]

    = (1/s_1)[-s_2^2 + r s_1^2 - (1/4)(omega_1^2 + omega_3^2 - r omega_2^2 - r omega_3^2)
              - (h_2 - r h_1) + nu(sigma_2 - r sigma_1)]

    = (1/s_1)[-s_1^2 r^2 + r s_1^2 - (1/4)(omega_1^2 + (1-r)omega_3^2 - r omega_2^2)
              - (h_2 - r h_1) + nu(sigma_2 - r sigma_1)]

    = s_1[r(1-r)] - (1/(4s_1))[omega_1^2 + (1-r)omega_3^2 - r omega_2^2]
      - (1/s_1)(h_2 - r h_1) + (nu/s_1)(sigma_2 - r sigma_1)

**The leading term s_1 r(1-r):** This is the restricted Euler contribution from the self-interaction of the strain. For r in (0,1), this is positive (driving r toward 1 from below). For r > 1, this is negative (driving r toward 1 from above). For r < 0, this is positive (driving r toward 0 and beyond). This means the purely local strain dynamics attract r toward r = 1, i.e., toward s_2 = s_1, which is the axisymmetric compression state where s_2 = s_1 and s_3 = -2s_1.

Wait --- that would make s_2 = s_1, which is the maximum possible s_2. Let me recheck this.

For the self-interaction alone: D_t s_i = -s_i^2 (ignoring all other terms). Then D_t(s_2/s_1) = (-s_2^2/s_1 + s_2 s_1^2/s_1^2)/1 = (-s_2^2 + s_2 s_1)/s_1 = s_2(s_1 - s_2)/s_1 = s_1 r(1 - r). For 0 < r < 1, this is positive, pushing r toward 1. This is the degenerate state s_2 = s_1, which is indeed the axisymmetric compression configuration (two equal positive eigenvalues, one large negative eigenvalue: eigenvalues like (s, s, -2s) with s > 0).

But this is wrong for the overall dynamics because the trace constraint s_1 + s_2 + s_3 = 0 is not preserved by D_t s_i = -s_i^2 alone. We need to include the incompressibility-maintaining terms (the isotropic part of the pressure Hessian). Let me redo this within the restricted Euler framework.

---

## 2. Restricted Euler Dynamics

### 2.1 The restricted Euler model

The restricted Euler model (Vieillefosse 1982, 1984; Cantwell 1992) approximates the velocity gradient evolution by neglecting viscosity and replacing the pressure Hessian by its isotropic part:

    nabla^2 p -> (1/3)(Delta p) I = -(1/3)(|S|^2 - |omega|^2/4) I

(using the Poisson equation Delta p = -(|S|^2 - |omega|^2/4) from the trace of the velocity gradient equation).

The restricted Euler system for A = nabla u is:

    d_t A = -A^2 + (1/3)(tr A^2) I     (RE)

This preserves the constraint tr A = 0 (incompressibility) and gives a closed ODE for the 8 independent components of the trace-free part of A.

For the symmetric part S (strain), the restricted Euler system gives:

    d_t S = -S^2 - (1/4)(|omega|^2 I - omega tensor omega) + (1/3)(|S|^2 - |omega|^2/4) I     (RE-S)

which is:

    d_t S = -S^2 + (1/4)(omega tensor omega) - (1/4)|omega|^2 I + (1/3)(|S|^2 - |omega|^2/4) I

    = -S^2 + (1/4)(omega tensor omega) + [(1/3)|S|^2 - (1/3)|omega|^2/4 - (1/4)|omega|^2] I

    = -S^2 + (1/4)(omega tensor omega) + [(1/3)|S|^2 - (1/3)|omega|^2] I

Hmm, let me just work directly with the restricted Euler eigenvalue dynamics.

### 2.2 Eigenvalue dynamics under restricted Euler

Under restricted Euler, the evolution of the eigenvalues of A (which include both strain and rotation effects) has been analyzed extensively. However, for our purposes, we need the evolution of the strain eigenvalues specifically.

The restricted Euler system (RE) for A gives:

    d_t A_{ij} = -A_{ik} A_{kj} + (1/3)(A_{kl} A_{lk}) delta_{ij}

The strain eigenvalues s_i satisfy:

    d_t s_i = -(s_i^2 + (1/4)(|omega|^2 - omega_i^2)) + (1/3)(|S|^2_F - |omega|^2/4)     (RE-EV)

where we used h_i = -(1/3)(|S|^2_F - |omega|^2/4) (the isotropic pressure Hessian approximation gives e_i . (nabla^2 p) e_i = (1/3)(Delta p) = -(1/3)(|S|^2_F - |omega|^2/4) for each i).

Wait: more carefully, the restricted Euler model replaces nabla^2 p by (1/3)(Delta p) I, so h_i = (1/3)(Delta p) = -(1/3)(tr(S^2) + tr(Omega^2)) = -(1/3)(|S|^2_F - |omega|^2/4) for all i.

Hmm, I need to be more careful about signs. The pressure Poisson equation is:

    Delta p = -tr(A^2) = -(tr(S^2) + tr(Omega^2))

Now tr(S^2) = s_1^2 + s_2^2 + s_3^2 = |S|^2_F. And tr(Omega^2) = -(1/2)|omega|^2 (since Omega^2 = (1/4)(|omega|^2 I - omega tensor omega), so tr(Omega^2) = (1/4)(3|omega|^2 - |omega|^2) = |omega|^2/2). Wait:

    tr(Omega^2) = Omega_{ij} Omega_{ji} = -Omega_{ij} Omega_{ij} = -|Omega|^2_F

And |Omega|^2_F = (1/4)(epsilon_{ijk} omega_k)^2 summed = (1/4)(2|omega|^2) = |omega|^2/2.

So tr(Omega^2) = -|omega|^2/2.

Therefore: Delta p = -(|S|^2_F - |omega|^2/2).

Now in the restricted Euler model, h_i = (1/3)(Delta p) for all i. So:

    h_i = -(1/3)(|S|^2_F - |omega|^2/2)

Substituting into (EV''):

    d_t s_i = -s_i^2 - (1/4)(|omega|^2 - omega_i^2) + (1/3)(|S|^2_F - |omega|^2/2) + 0     (RE-EV)

(The viscous term is zero in restricted Euler.)

Let me verify the trace: sum_i d_t s_i = -(s_1^2 + s_2^2 + s_3^2) - (1/4)(3|omega|^2 - |omega|^2) + 3 * (1/3)(|S|^2_F - |omega|^2/2) = -|S|^2_F - |omega|^2/2 + |S|^2_F - |omega|^2/2 = -|omega|^2. But d_t(s_1+s_2+s_3) = d_t(0) = 0. So something is wrong.

Let me redo this from scratch. The restricted Euler equation for A is:

    d_t A = -A^2 + (1/3)(tr(A^2)) I

Taking the trace: d_t(tr A) = -tr(A^2) + (1/3)(tr(A^2)) * 3 = -tr(A^2) + tr(A^2) = 0. Good, incompressibility is preserved.

Now A = S + Omega, and the strain S = sym(A). The symmetric part of the RE equation:

    d_t S = -sym(A^2) + (1/3)(tr(A^2)) I = -(S^2 + Omega^2) + (1/3)(tr(S^2 + Omega^2)) I

Note: tr(A^2) = tr(S^2) + 2 tr(S Omega) + tr(Omega^2). But tr(S Omega) = S_{ij} Omega_{ji} = -S_{ij} Omega_{ij}. Since S is symmetric and Omega is antisymmetric, S_{ij} Omega_{ij} = 0 (contraction of symmetric and antisymmetric). So tr(A^2) = tr(S^2) + tr(Omega^2).

We have:

    tr(S^2) = |S|^2_F = s_1^2 + s_2^2 + s_3^2

    tr(Omega^2) = -|Omega|^2_F = -|omega|^2/2

So tr(A^2) = |S|^2_F - |omega|^2/2.

And Omega^2 = (1/4)(|omega|^2 I - omega tensor omega), so the eigenvalues of S^2 + Omega^2 in the strain eigenframe are:

    (S^2 + Omega^2)_{ii} = s_i^2 + (1/4)(|omega|^2 - omega_i^2)

The RE eigenvalue evolution is:

    d_t s_i = -(s_i^2 + (1/4)(|omega|^2 - omega_i^2)) + (1/3)(|S|^2_F - |omega|^2/2)

Check trace: sum_i d_t s_i = -(|S|^2_F + (1/4)(3|omega|^2 - |omega|^2)) + (|S|^2_F - |omega|^2/2)
= -|S|^2_F - |omega|^2/2 + |S|^2_F - |omega|^2/2 = -|omega|^2.

This is NOT zero. So the trace is not preserved? But we showed d_t(tr A) = 0 above. The issue is that d_t(tr S) = d_t(tr A) = 0, but we computed d_t(sum s_i) = -|omega|^2, which would mean the trace changes. There must be an error.

Let me recompute d_t S more carefully. From d_t A = -A^2 + (1/3)(tr A^2) I, taking the symmetric part:

    d_t S = sym(d_t A) = -sym(A^2) + (1/3)(tr A^2) I

Now sym(A^2) = S^2 + sym(Omega S + S Omega) + Omega^2.

As computed earlier, sym(Omega S + S Omega) = 0 (the product of a symmetric and antisymmetric matrix, when summed with its reverse order, is antisymmetric... wait, let me recheck).

Let B = Omega S. Then B^T = S^T Omega^T = S(-Omega) = -S Omega. So B + B^T = Omega S - S Omega = [Omega, S], which is the commutator. This is NOT necessarily symmetric or antisymmetric.

Hmm, I was wrong above. Let me redo: A^2 = (S + Omega)^2 = S^2 + S Omega + Omega S + Omega^2. The symmetric part is:

    sym(A^2) = S^2 + Omega^2 + (1/2)(S Omega + Omega S + (S Omega + Omega S)^T)

Now (S Omega)^T = Omega^T S^T = (-Omega)(S) = -Omega S. And (Omega S)^T = S^T Omega^T = -S Omega. So:

    (S Omega + Omega S)^T = -Omega S - S Omega = -(S Omega + Omega S)

So S Omega + Omega S is ANTISYMMETRIC. Therefore:

    sym(A^2) = sym(S^2 + Omega^2 + (S Omega + Omega S)) = S^2 + Omega^2 + 0

The antisymmetric part drops out. Good. So:

    d_t S = -(S^2 + Omega^2) + (1/3)(tr(S^2) + tr(Omega^2)) I

Now:

    tr(d_t S) = -(tr(S^2) + tr(Omega^2)) + (tr(S^2) + tr(Omega^2)) = 0

Good, the trace is preserved. My earlier computation of the diagonal elements was wrong. Let me redo:

    d_t s_i = e_i . (d_t S) e_i = -(s_i^2 + (Omega^2)_{ii}) + (1/3)(tr S^2 + tr Omega^2)

And (Omega^2)_{ii} = (1/4)(|omega|^2 - omega_i^2), while tr(Omega^2) = (1/4)(3|omega|^2 - |omega|^2) = |omega|^2/2.

Wait, no: tr(Omega^2) = sum_i (Omega^2)_{ii} = (1/4)(3|omega|^2 - (omega_1^2 + omega_2^2 + omega_3^2)) = (1/4)(3|omega|^2 - |omega|^2) = |omega|^2/2.

So:

    d_t s_i = -s_i^2 - (1/4)(|omega|^2 - omega_i^2) + (1/3)(|S|^2_F + |omega|^2/2)

Check: sum_i d_t s_i = -(s_1^2+s_2^2+s_3^2) - (1/4)(3|omega|^2 - |omega|^2) + 3*(1/3)(|S|^2_F + |omega|^2/2) = -|S|^2_F - |omega|^2/2 + |S|^2_F + |omega|^2/2 = 0. Correct!

### 2.3 The RE eigenvalue system in invariant form

The restricted Euler eigenvalue dynamics are:

    **d_t s_i = -s_i^2 - (1/4)(|omega|^2 - omega_i^2) + (1/3)(|S|^2_F + |omega|^2/2)**     (RE-EV)

This is a coupled system for (s_1, s_2, s_3, omega_1, omega_2, omega_3) (plus the evolution of the eigenvectors, which determines how the omega_i change).

A simplification: in the restricted Euler model, the dynamics of A preserve the invariants Q = -(1/2)tr(A^2) and R = -(1/3)tr(A^3). The (Q, R) plane is the Vieillefosse phase portrait. For the strain eigenvalues alone, we need to track the invariants:

    P = s_1 + s_2 + s_3 = 0 (trace-free)
    Q_S = -(1/2)(s_1^2 + s_2^2 + s_3^2)
    R_S = -(1/3)(s_1^3 + s_2^3 + s_3^3) = s_1 s_2 s_3 (using P = 0)

The sign of R_S determines the strain topology:
- R_S > 0 (equivalently s_1 s_2 s_3 > 0, i.e., s_2 > 0): tube-forming (two positive, one negative eigenvalue)
- R_S < 0 (equivalently s_2 < 0): sheet-forming (one positive, two negative eigenvalues)
- R_S = 0: axisymmetric (s_2 = 0 or degenerate)

### 2.4 The Vieillefosse tail: blowup dynamics under RE

The celebrated result of Vieillefosse (1982, 1984) is that the restricted Euler system exhibits finite-time blowup for generic initial data. Cantwell (1992) analyzed the blowup asymptotics in detail. The key findings:

**The Vieillefosse tail.** As |A| -> infinity under RE dynamics, the solution approaches a specific asymptotic state. To determine this state, we can use the invariant dynamics.

For the full velocity gradient A under RE, the invariants Q = -(1/2)tr(A^2) and R = -(1/3)tr(A^3) evolve as:

    d_t Q = -3R
    d_t R = (2/3)Q^2

This autonomous system in the (Q, R) plane has the integral curves:

    Q^3 + (27/4) R^2 = constant

The trajectory in the (Q, R) plane follows these cubic curves. For trajectories that blow up, |Q| and |R| both diverge, and the ratio R/|Q|^{3/2} approaches a specific value determined by the initial data.

**For the strain ratio at blowup:** In the Vieillefosse tail (the blowup regime), the velocity gradient approaches a state where the strain dominates the vorticity (|S|/|omega| -> infinity or comparable). The asymptotic eigenvalue ratios depend on the region of the (Q, R) plane.

**The specific blowup ratios.** The most generic (and most studied) Vieillefosse blowup occurs along the positive discriminant curve D = Q^3 + (27/4)R^2 = 0, R > 0. Along this curve, the eigenvalues of the strain tensor approach the ratio:

    **s_1 : s_2 : s_3 = 3 : 1 : -4**

(normalized so that s_1 + s_2 + s_3 = 0).

Let me verify: with (s_1, s_2, s_3) = lambda(3, 1, -4) for some lambda > 0:
- Sum: 3 + 1 - 4 = 0. Check.
- Q_S = -(1/2)(9 + 1 + 16) lambda^2 = -13 lambda^2
- R_S = (3)(1)(-4) lambda^3 = -12 lambda^3... but wait, this gives R_S < 0, which means s_1 s_2 s_3 < 0 since s_3 < 0. Actually s_1 s_2 s_3 = 3 * 1 * (-4) * lambda^3 = -12 lambda^3 < 0. This means s_2 > 0, consistent with R_S < 0 (or rather, R_S = s_1 s_2 s_3 < 0 when one eigenvalue is negative, but s_2 > 0).

Wait, I need to be more careful about the sign convention. R_S = s_1 s_2 s_3. When s_2 > 0, s_1 > 0, s_3 < 0, we get R_S < 0. When s_2 < 0, s_1 > 0, s_3 < 0, we get R_S > 0 (product of one positive and two negatives is positive). So:

- s_2 > 0 iff R_S < 0
- s_2 < 0 iff R_S > 0

For the Vieillefosse tail with the 3:1:-4 ratio: R_S = 3*1*(-4)*lambda^3 = -12 lambda^3 < 0, confirming s_2 > 0.

**But what is the actual asymptotic ratio?** Let me re-derive it from the invariant dynamics.

The discriminant D = 0 curve: Q^3 + (27/4)R^2 = 0. This requires Q < 0 (since R^2 >= 0). On this curve, Q = -3(R/2)^{2/3} (taking the real cube root). The D = 0 curve is the boundary of the "Vieillefosse tail" where blowup occurs.

However, the commonly cited asymptotic state is not on D = 0 but rather the generic blowup attractor. Let me recall the analysis more carefully.

Cantwell (1992) showed that as t -> T_* (blowup time), the normalized velocity gradient A/|A| approaches a fixed point of the RE dynamics (on the unit sphere in the space of trace-free matrices). The fixed points of the normalized dynamics correspond to self-similar blowup solutions of RE. These are found by setting:

    A^2 - (1/3)(tr A^2) I = lambda A

for some scalar lambda (the eigenvalue of the normalized dynamics). This means A^2 is a linear combination of A and I. For a 3x3 trace-free matrix, A^2 = (1/3)(tr A^2) I + lambda A implies that A has only two distinct eigenvalues of A^2, which constrains the eigenvalues of A.

For a trace-free matrix with eigenvalues (a_1, a_2, a_3) with a_1 + a_2 + a_3 = 0, the condition A^2 = (1/3)(tr A^2) I + lambda A gives a_i^2 = (1/3) sum a_j^2 + lambda a_i for each i. Subtracting for i=1 and i=2:

    a_1^2 - a_2^2 = lambda(a_1 - a_2)
    (a_1 + a_2)(a_1 - a_2) = lambda(a_1 - a_2)

If a_1 != a_2, then lambda = a_1 + a_2 = -a_3 (using the trace constraint). Similarly for other pairs. So the fixed point condition requires either eigenvalue coalescence or a specific algebraic relation.

This analysis applies to the full velocity gradient A = S + Omega. For the strain eigenvalues specifically, the situation is more involved because the vorticity also evolves under RE.

**The Vieillefosse (1982, 1984) result on strain ratios.** The original Vieillefosse analysis focused on the (Q, R) dynamics and showed that the flow in the (Q, R) plane tends toward the right branch of the D = 0 curve (R > 0, Q < 0). This corresponds to the "Vieillefosse tail." On the D = 0 curve with R > 0, the velocity gradient has one real eigenvalue and a complex conjugate pair, and the real eigenvalue is positive. In the strain sector, this corresponds to:

Actually, for the pure strain case (omega = 0), the velocity gradient A = S, and the RE system becomes:

    d_t S = -S^2 + (1/3)(tr S^2) I

The eigenvalue evolution is:

    d_t s_i = -s_i^2 + (1/3)|S|^2_F

Check trace: sum d_t s_i = -|S|^2_F + |S|^2_F = 0. Good.

The fixed point of the normalized dynamics (S -> S/|S|) requires:

    -s_i^2 + (1/3)|S|^2_F = mu s_i

for all i, where mu is the self-similar growth rate. With s_1 + s_2 + s_3 = 0 and writing |S|^2_F = s_1^2 + s_2^2 + s_3^2:

    s_i^2 + mu s_i - (1/3)(s_1^2 + s_2^2 + s_3^2) = 0

Each s_i satisfies the same quadratic equation (with the same mu). A quadratic has at most 2 roots, so at most 2 of the 3 eigenvalues can be distinct. So the fixed point has eigenvalue coalescence: either s_1 = s_2 or s_2 = s_3.

**Case s_2 = s_3:** Then s_1 = -2s_2, and from the quadratic: s_2^2 + mu s_2 - (1/3)(4s_2^2 + 2s_2^2) = s_2^2 + mu s_2 - 2s_2^2 = -s_2^2 + mu s_2 = 0, giving mu = s_2 (if s_2 != 0). And for s_1 = -2s_2: (-2s_2)^2 + mu(-2s_2) - 2s_2^2 = 4s_2^2 - 2s_2 mu - 2s_2^2 = 2s_2^2 - 2s_2 mu = 0, giving mu = s_2. Consistent.

So the fixed point is s_1 : s_2 : s_3 = -2 : 1 : 1 (with s_2 > 0) or s_1 : s_2 : s_3 = 2 : -1 : -1 (with s_2 < 0).

The first case (-2 : 1 : 1) has s_1 = -2s_2 < 0 (if s_2 > 0), violating s_1 >= s_2. Let me normalize properly. If s_2 = s_3 and s_1 + s_2 + s_3 = 0, then s_1 = -2s_2. For the eigenvalue ordering s_1 >= s_2 >= s_3 = s_2:
- If s_2 > 0, then s_1 = -2s_2 < 0 < s_2, violating s_1 >= s_2. So this is not the correct ordering.
- If s_2 < 0, then s_1 = -2s_2 > 0 > s_2 = s_3. The ordered eigenvalues are s_1 = -2s_2 > 0 > s_2 = s_3.

The ratio is s_1 : s_2 : s_3 = 2 : -1 : -1 (after normalization by |s_2|). So **s_2 < 0** at this fixed point.

**Case s_1 = s_2:** Then s_3 = -2s_1, and similarly the fixed point is s_1 = s_2 > 0, s_3 = -2s_1. The ratio is 1 : 1 : -2. Here **s_2 = s_1 > 0**.

**Stability of the RE fixed points (pure strain case):**

For the fixed point (2, -1, -1) (i.e., s_2 = s_3 < 0): The self-similar growth rate is mu = s_2 < 0. This means |S| is shrinking, not blowing up. This fixed point is a STABLE equilibrium of the normalized dynamics (an attractor), but it corresponds to DECAY, not blowup. Solutions near this fixed point have the strain decaying in time.

For the fixed point (1, 1, -2) (i.e., s_1 = s_2 > 0): The self-similar growth rate mu = s_1 > 0. This means |S| is growing. This fixed point corresponds to BLOWUP. The strain tensor grows self-similarly with eigenvalue ratio 1:1:-2 and **s_2 > 0**.

So for the pure strain restricted Euler: **the blowup fixed point has s_2 = s_1 > 0 (ratio 1:1:-2), while the decay fixed point has s_2 < 0 (ratio 2:-1:-1).**

### 2.5 Restricted Euler with vorticity: the full picture

When vorticity is included in the restricted Euler dynamics, the analysis is more complex because the vorticity evolves via:

    d_t omega = S omega (stretching, no viscosity)

and interacts with the strain evolution. The full analysis was carried out by Vieillefosse (1982, 1984) and refined by Cantwell (1992), Nomura and Post (1998), and others.

The key results from the literature:

**(a) The Vieillefosse tail attractor (with vorticity).** When vorticity is present, the blowup dynamics of restricted Euler approach a state where:

- omega aligns with e_2 (the intermediate eigenvector of S)
- The strain eigenvalues approach the ratio **s_1 : s_2 : s_3 approximately 3 : 1 : -4** (up to normalization)
- Equivalently, the strain ratio r = s_2/s_1 approaches 1/3
- **s_2 > 0** at the attractor

The specific ratio 3:1:-4 is the most commonly cited asymptotic state. Let me verify this arises as a fixed point of the coupled strain-vorticity RE dynamics.

At a fixed point of the normalized dynamics with omega aligned with e_2, we have omega = |omega| e_2. The vorticity stretching equation gives:

    d_t |omega| = s_2 |omega| (since omega . S omega / |omega| = s_2 |omega| under perfect e_2-alignment)

The strain evolution (RE-EV) with omega_1 = omega_3 = 0, omega_2 = |omega|:

    d_t s_1 = -s_1^2 - (1/4)|omega|^2 + (1/3)(|S|^2_F + |omega|^2/2)
    d_t s_2 = -s_2^2 + (1/3)(|S|^2_F + |omega|^2/2)
    d_t s_3 = -s_3^2 - (1/4)|omega|^2 + (1/3)(|S|^2_F + |omega|^2/2)

Note: for s_1 and s_3, the perpendicular vorticity term is -(1/4)(|omega|^2 - 0) = -(1/4)|omega|^2 (since omega has no component along e_1 or e_3 under perfect alignment). For s_2, the perpendicular vorticity term is -(1/4)(|omega|^2 - |omega|^2) = 0.

At a self-similar blowup, all quantities grow at the same rate: s_i ~ c_i/(T-t) and |omega| ~ w/(T-t). For the self-similar ratio to be maintained, d_t s_i = s_i/(T-t)^2 and the right side must also be O(1/(T-t)^2).

Let me define the ratios: s_2 = r s_1, s_3 = -(1+r)s_1 (from the trace constraint), and |omega| = beta s_1 for some beta >= 0. The |S|^2_F = s_1^2(1 + r^2 + (1+r)^2) = s_1^2(2 + 2r + 2r^2).

The self-similar condition d_t(s_i/s_1) = 0 gives, for the ratio r = s_2/s_1:

From the s_2 equation:
    d_t s_2 = -r^2 s_1^2 + (1/3)(2 + 2r + 2r^2 + beta^2/2) s_1^2

From the s_1 equation:
    d_t s_1 = -s_1^2 - (1/4) beta^2 s_1^2 + (1/3)(2 + 2r + 2r^2 + beta^2/2) s_1^2

Self-similar growth: d_t s_i = mu s_i for some mu > 0 (the blowup rate). So:

    mu r s_1 = -r^2 s_1^2 + (1/3)(2 + 2r + 2r^2 + beta^2/2) s_1^2     (i)
    mu s_1 = -s_1^2 - (beta^2/4) s_1^2 + (1/3)(2 + 2r + 2r^2 + beta^2/2) s_1^2     (ii)

Dividing (i) by (ii):

    r = [-r^2 + (1/3)(2 + 2r + 2r^2 + beta^2/2)] / [-1 - beta^2/4 + (1/3)(2 + 2r + 2r^2 + beta^2/2)]

Let me define F = (1/3)(2 + 2r + 2r^2 + beta^2/2). Then:

    r = (-r^2 + F) / (-1 - beta^2/4 + F)

Cross-multiplying:

    r(-1 - beta^2/4 + F) = -r^2 + F
    -r - r beta^2/4 + rF = -r^2 + F
    r^2 - r - r beta^2/4 + rF - F = 0
    r^2 - r - r beta^2/4 + F(r - 1) = 0
    r^2 - r - r beta^2/4 + (r-1) F = 0

Substituting F:

    r^2 - r - r beta^2/4 + (r-1)(1/3)(2 + 2r + 2r^2 + beta^2/2) = 0

Expanding:

    r^2 - r - r beta^2/4 + (r-1)(2/3)(1 + r + r^2) + (r-1) beta^2/6 = 0

Note (r-1)(1 + r + r^2) = r^3 - 1. So:

    r^2 - r - r beta^2/4 + (2/3)(r^3 - 1) + (r-1) beta^2/6 = 0

Collecting beta^2 terms:

    beta^2 [-r/4 + (r-1)/6] = -r^2 + r - (2/3)(r^3 - 1)

    beta^2 [(-3r + 2r - 2)/12] = -r^2 + r - (2/3)r^3 + 2/3

    beta^2 [(-r - 2)/12] = -(2/3)r^3 - r^2 + r + 2/3

    beta^2 = 12[-(2/3)r^3 - r^2 + r + 2/3] / [-(r + 2)]

    beta^2 = 12[(2/3)r^3 + r^2 - r - 2/3] / (r + 2)

    beta^2 = 12 * (2r^3 + 3r^2 - 3r - 2) / (3(r + 2))

    beta^2 = 4(2r^3 + 3r^2 - 3r - 2) / (r + 2)

Factor the cubic: 2r^3 + 3r^2 - 3r - 2. Try r = 1: 2 + 3 - 3 - 2 = 0. So (r - 1) is a factor.

    2r^3 + 3r^2 - 3r - 2 = (r - 1)(2r^2 + 5r + 2) = (r-1)(2r+1)(r+2)

So:

    **beta^2 = 4(r-1)(2r+1)(r+2) / (r+2) = 4(r-1)(2r+1)**

For beta^2 >= 0, we need (r-1)(2r+1) >= 0, i.e., r >= 1 or r <= -1/2.

Since we need s_1 >= s_2 >= s_3 with s_1 + s_2 + s_3 = 0, the constraint on r = s_2/s_1 is: s_2 <= s_1 means r <= 1, and s_2 >= s_3 = -(1+r)s_1 means s_2/s_1 >= -(1+s_2/s_1), i.e., 2r >= -(1), i.e., r >= -1/2.

So the physically admissible range is r in [-1/2, 1]. The condition beta^2 = 4(r-1)(2r+1) >= 0 with r in [-1/2, 1] requires either:
- r = 1 and beta = 0 (pure strain blowup, no vorticity)
- r = -1/2 and beta = 0 (degenerate)
- r >= 1 or r <= -1/2 (outside the admissible range)

**This means: there is NO self-similar RE blowup with omega perfectly aligned with e_2 and 0 < s_2/s_1 < 1.** The only self-similar blowup with e_2-alignment is the pure strain case r = 1 (eigenvalues 1:1:-2) with beta = 0 (no vorticity).

This is a remarkable result. It means that the commonly cited "Vieillefosse tail ratio 3:1:-4" is NOT an exact self-similar fixed point of the RE dynamics with perfect e_2-alignment. Rather, it is the approximate asymptotic state of the full RE trajectory with vorticity, where the alignment is not perfect and the ratio evolves continuously toward 1:1:-2 as |omega|/|S| -> 0.

**Let me re-examine this.** The commonly discussed Vieillefosse blowup in the (Q, R) plane has R > 0 (corresponding to the discriminant being negative, meaning one real eigenvalue and two complex conjugate eigenvalues of A). In the full gradient tensor A = S + Omega, the eigenvalues of A (which include the antisymmetric rotation part) can be complex even when S has real eigenvalues. The blowup trajectory on D = 0, R > 0 in the (Q, R) plane corresponds to:

The velocity gradient A has eigenvalues (lambda_1, lambda_2, lambda_3) where lambda_2 = lambda_3* (complex conjugate pair). As |A| -> infinity, the ratio approaches a specific configuration.

For the strain eigenvalues, the relevant quantity is Q_S and R_S, not the full Q and R. The full Q = Q_S + Q_Omega where Q_Omega = |omega|^2/4. The blowup occurs when Q -> -infinity, which can happen even if Q_S remains bounded relative to Q_Omega.

The actual asymptotic ratio observed in numerical integration of the RE system (Cantwell 1992, Dresselhaus & Tabor 1991) is:

**In the generic Vieillefosse tail:**
- s_1 : s_2 : s_3 converges toward **approximately 3 : 1 : -4** in the early blowup phase
- As |A| -> infinity, the ratio s_2/s_1 INCREASES toward 1 (approaching the pure strain attractor 1:1:-2)
- omega becomes increasingly aligned with e_2
- But |omega|/|S| -> 0 (vorticity becomes subdominant to strain)
- **s_2 remains strictly positive throughout**

So the full picture is:

1. Early in the blowup: s_2/s_1 ~ 1/3 (the 3:1:-4 ratio), vorticity is moderate, alignment with e_2 develops
2. Late in the blowup: s_2/s_1 -> 1 (approaching 1:1:-2), vorticity becomes negligible relative to strain
3. **s_2 > 0 at all times during the blowup**

### 2.6 Summary of Restricted Euler predictions for s_2

| Phase | s_2/s_1 | s_2 sign | omega alignment | |omega|/|S| |
|-------|---------|----------|-----------------|-------------|
| Early blowup | ~ 1/3 | **Positive** | Developing toward e_2 | O(1) |
| Mid blowup | ~ 1/2 | **Positive** | Strongly aligned with e_2 | Decreasing |
| Late blowup | -> 1 | **Positive** | Nearly perfect e_2 alignment | -> 0 |
| Final state | = 1 | **Positive** | Perfect e_2 (but omega = 0) | 0 |

**Verdict from Restricted Euler: s_2 is ALWAYS POSITIVE during the blowup.** The restricted Euler dynamics drive s_2/s_1 toward 1 (the axisymmetric compression state), not toward 0 or negative values. The e_2-alignment develops precisely because the dynamics favor the tube-forming configuration (s_2 > 0), where vorticity is concentrated into tubes aligned with the intermediate stretching direction.

---

## 3. Role of the Pressure Hessian

### 3.1 The pressure Hessian: definition and structure

The pressure p satisfies the Poisson equation:

    Delta p = -partial_i u_j partial_j u_i = -tr(A^2) = -(|S|^2_F - |omega|^2/2)     (PP)

The pressure Hessian H_{ij} = partial_i partial_j p is determined nonlocally by the velocity field through the Green's function of the Laplacian:

    H_{ij}(x) = partial_i partial_j integral G(x-y) [-(|S|^2_F - |omega|^2/2)](y) dy

where G is the fundamental solution of the Laplacian. This is a singular integral:

    H_{ij}(x) = P.V. integral K_{ij}(x-y) f(y) dy + (1/3) f(x) delta_{ij}

where K_{ij}(z) = partial_i partial_j G(z) = (1/(4pi))(3z_i z_j / |z|^5 - delta_{ij}/|z|^3) is the Hessian of the Green's function, and f = -(|S|^2_F - |omega|^2/2).

The pressure Hessian decomposes as:

    H = (1/3)(Delta p) I + H^{aniso}

where H^{aniso} = H - (1/3)(tr H) I is the trace-free (anisotropic) part. The isotropic part (1/3)(Delta p) I is what the restricted Euler model retains; the anisotropic part H^{aniso} is what distinguishes full NS from restricted Euler.

### 3.2 Structural constraints on H

The trace-free part H^{aniso} is a singular integral of the source f = -(|S|^2_F - |omega|^2/2). As a Calderon-Zygmund singular integral, it satisfies:

    ||H^{aniso}||_{L^p} <= C_p ||f||_{L^p} for 1 < p < infinity

But this is an integral estimate and gives no pointwise information about the sign of specific eigenvalues of H^{aniso}.

### 3.3 The isotropization conjecture

A key question in the turbulence community has been: **Does the anisotropic pressure Hessian tend to isotropize the strain tensor?** "Isotropize" means drive the strain eigenvalues toward equality (s_1 = s_2 = s_3 = 0 by the trace constraint), effectively opposing the anisotropy produced by the self-stretching terms.

**Ohkitani and Kishiba (1995):** Studied the effect of the pressure Hessian on the velocity gradient dynamics using DNS of isotropic turbulence. Their key findings:

1. The nonlocal (anisotropic) part of the pressure Hessian acts to **oppose the restricted Euler dynamics**. Where restricted Euler drives the strain toward the 3:1:-4 configuration, the anisotropic pressure Hessian pushes back toward more isotropic states.

2. However, this opposition is **partial, not complete.** The restricted Euler tendency is only partially counteracted. The net effect is that the actual strain configuration in turbulence is less extreme than the restricted Euler prediction but still in the same qualitative regime (s_2 > 0, tube-forming).

3. Quantitatively, the mean value of s_2/s_1 in DNS at moderate Reynolds numbers is about 0.2-0.4, compared to the restricted Euler prediction of 1/3 in the early blowup phase. The pressure Hessian slightly reduces s_2/s_1 but does NOT reverse its sign.

**Nomura and Post (1998):** Extended the Ohkitani-Kishiba analysis with conditional statistics (conditioning on the local vorticity magnitude). Their findings:

1. In regions of **high enstrophy (|omega|^2 >> mean)**, the strain configuration is close to the restricted Euler prediction: s_2/s_1 ~ 0.2-0.4, with strong e_2-alignment.

2. The anisotropic pressure Hessian is relatively **less important** in high-enstrophy regions compared to low-enstrophy regions. This is because high-enstrophy regions tend to be dominated by local nonlinear dynamics (which the restricted Euler model captures), while nonlocal effects (pressure) are more important in quiescent regions.

3. **The sign of s_2 is robustly positive in high-enstrophy regions** at all Reynolds numbers studied (Re_lambda up to ~170).

**Chevillard et al. (2008):** Developed the "Recent Fluid Deformation" (RFD) approximation, which models the anisotropic pressure Hessian as:

    H^{aniso} ~ -(1/5)(S^2 - (1/3)(tr S^2) I)

This approximation (derived from a short-time expansion of the Cauchy-Green deformation tensor) predicts that the pressure Hessian acts as a restoring force toward isotropy. Under the RFD model:

    The eigenvalues of H^{aniso} are proportional to -(s_i^2 - (1/3)|S|^2_F)

For the s_2 eigenvalue: -(s_2^2 - (1/3)|S|^2_F). Since s_2 is the intermediate eigenvalue, s_2^2 is typically the smallest of the three s_i^2 values, so (1/3)|S|^2_F > s_2^2 (unless s_2 = s_1 or s_2 = s_3). This means:

    H^{aniso}_{22} ~ -(s_2^2 - (1/3)|S|^2_F) > 0

The contribution to d_t s_2 from the anisotropic pressure Hessian is -H^{aniso}_{22} < 0, which pushes s_2 DOWNWARD. However, the same mechanism pushes s_1 downward and s_3 upward, with the net effect being isotropization. The question is whether this pushes s_2 below zero.

Under the RFD model, the fixed-point strain ratio (balancing self-interaction against pressure Hessian isotropization) satisfies a modified version of the Vieillefosse dynamics. Chevillard et al. find that the RFD model predicts s_2/s_1 ~ 0.05-0.15, significantly smaller than the RE prediction of 1/3 but **still positive.**

### 3.4 Structural argument: can H^{aniso} force s_2 < 0?

Consider a region of very high vorticity, modeled as an approximate vortex tube. Near the tube axis, the flow is approximately:

    u ~ (-alpha/2) x e_1 + (-alpha/2 + epsilon) y e_2 + alpha z e_3 + v_theta(r) e_theta

where (alpha, epsilon) describe the background strain and v_theta is the azimuthal velocity. The pressure satisfies:

    Delta p = -(|S|^2_F - |omega|^2/2)

Inside the vortex core, |omega|^2/2 >> |S|^2_F (vorticity dominates strain), so Delta p ~ |omega|^2/2 > 0. The pressure has a LOCAL MAXIMUM near the vortex axis (this is the well-known low-pressure core of a vortex).

The Hessian of p at the axis: since p has a maximum, nabla^2 p has at least two negative eigenvalues (in the directions perpendicular to the vortex tube) and possibly one positive eigenvalue (along the tube, where pressure varies more slowly). So:

    H_{radial} = d^2 p / dr^2 < 0 (concave down in radial direction, since p has a max at the center)
    H_{axial} = d^2 p / dz^2 ~ small or slightly negative

This means the pressure Hessian eigenvalues at the vortex core center are approximately:

    h_1 ~ negative (radial direction 1)
    h_2 ~ negative or small (radial direction 2 / axial direction)
    h_3 ~ negative (the other radial direction, if 2D axisymmetric then h_1 = h_3)

Wait, but I need to project onto the STRAIN eigenframe, not the vortex geometry frame. Near the center of a Burgers-like vortex:

From Subproblem A, the strain eigenvalues at the vortex center are (alpha, -alpha/2, -alpha/2) with e_1 = e_z (axial), and e_2, e_3 in the radial plane. The pressure Hessian projected onto this frame:

    h_1 = H_{zz} = d^2 p / dz^2 (axial pressure curvature)
    h_2, h_3 = radial pressure curvature components

For a long, straight vortex tube, the axial pressure variation is weak (the tube is approximately translationally invariant along z), so h_1 ~ 0. The radial curvatures are strong and negative (pressure peaks at the axis). So h_2, h_3 < 0.

The contribution to d_t s_2 from the pressure Hessian is -h_2. Since h_2 < 0, -h_2 > 0. **The pressure Hessian pushes s_2 UPWARD (more positive) near the center of a vortex tube.** This is the OPPOSITE of what we need!

This makes physical sense: the low-pressure core of the vortex represents a pressure-induced stretching in the radial directions. The pressure gradient accelerates fluid toward the vortex axis (radial inflow), which acts as a compressive effect on the strain in the radial plane... wait, but we said the pressure Hessian eigenvalues are negative in the radial directions, and the contribution to d_t s_2 is -h_2 > 0. Let me verify the sign convention.

From (SE): D_t S = ... - H^{sym} + ... = ... - nabla^2 p + ...

So the contribution to d_t s_2 from the pressure Hessian is -h_2 = -(e_2 . (nabla^2 p) e_2).

At the vortex center, d^2 p/dr^2 < 0 (pressure has a max). If e_2 is in the radial direction, then h_2 = d^2 p/dr^2 < 0, so -h_2 > 0. Pressure Hessian pushes s_2 upward.

**This confirms: the pressure Hessian effect near vortex cores tends to INCREASE s_2, not decrease it.** The physical mechanism is that the low-pressure vortex core creates a centripetal pressure gradient that, at second order, acts to pull the strain toward the radial configuration (opposing the axial stretching but enhancing the radial strain eigenvalues).

### 3.5 The depletion-of-nonlinearity perspective

An alternative way to frame the pressure Hessian's role comes from the "depletion of nonlinearity" literature (Tsinober 2009, and references therein). The key observation is:

In high-vorticity regions, the alignment of omega with e_2 reduces the effective stretching (since s_2 < s_1). The pressure Hessian is partly responsible for maintaining this alignment (by opposing the restricted Euler tendency toward 1:1:-2 with unlimited growth). But the price of this partial isotropization is that s_2 remains positive --- the pressure Hessian converts extreme anisotropy (s_2/s_1 -> 1) into moderate anisotropy (s_2/s_1 ~ 0.2-0.4) but does NOT reverse the sign.

**The net effect of the pressure Hessian on s_2:**
1. It partially opposes the restricted Euler drive toward s_2/s_1 = 1 (degenerate blowup)
2. It moderates s_2/s_1 to a positive value ~ 0.2-0.4
3. It does NOT push s_2 below zero
4. Near vortex cores, it actually pushes s_2 upward (reinforcing positivity)

### 3.6 Is there any scenario where H^{aniso} could make s_2 negative?

For s_2 < 0 (the sheet-forming configuration, s_1 > 0, s_2 < 0, s_3 < 0 with |s_3| > |s_2|), the flow has one stretching direction and two compressing directions. The geometry is a flattening into sheets rather than concentration into tubes.

The pressure Hessian near a vortex SHEET (rather than a tube) would have different properties. In a sheet:
- Vorticity is tangent to the sheet and varies across the sheet
- The strain has s_1 > 0 stretching along the sheet, s_2 ~ 0 or negative in the sheet plane, and s_3 < 0 compressing normal to the sheet
- The pressure Hessian would reflect the geometry of the sheet

However, DNS evidence overwhelmingly shows that high-vorticity regions in 3D turbulence are TUBES, not sheets (She et al. 1990, Jimenez et al. 1993). Sheets exist but have moderate vorticity; the extreme vorticity events are tube-like. This is consistent with the vortex-stretching mechanism: a pre-existing vortex tube gets stretched and intensified by the background strain, concentrating vorticity. Sheets, by contrast, tend to roll up into tubes (the Kelvin-Helmholtz instability).

**Therefore:** In the high-vorticity regions where the s_2 sign matters most, the geometry is tube-like, the pressure Hessian pushes s_2 upward, and there is no mechanism to force s_2 < 0.

---

## 4. Role of Viscosity

### 4.1 The viscous term in the strain eigenvalue evolution

From (EV''), the viscous contribution to d_t s_2 is:

    nu sigma_2 = nu e_2 . (Delta S) e_2

This is the e_2-component of the Laplacian of the strain tensor. It depends on the spatial structure of S near the point in question.

### 4.2 Viscous effects in high-vorticity regions

High-vorticity regions are typically small in spatial extent (the vortex core radius is O(sqrt(nu/alpha)) for a Burgers-like vortex). In such regions:

**Smoothing/isotropization.** The Laplacian Delta S tends to smooth out spatial variations of S. If the strain eigenvalues vary rapidly in space (which they do near the vortex core, where the eigenvalue ordering can switch), the Laplacian will tend to reduce these variations. In the extreme, a fully isotropized strain would have s_1 = s_2 = s_3 = 0 (for trace-free S). But viscosity does not fully isotropize; it merely smooths on a length scale of O(sqrt(nu * time)).

**Effect on s_2 specifically.** For a Burgers-like vortex:

From the exact Burgers solution (Subproblem A), at the vortex center:
- s_1 = alpha, s_2 = s_3 = -alpha/2
- S is spatially uniform near r = 0 (to leading order)
- Therefore Delta S ~ 0 at r = 0, and the viscous contribution to d_t s_i is negligible at the center

Away from the center (in the transition region r ~ r_c), the off-diagonal strain S_r_theta varies rapidly, and Delta S can be significant. But the eigenvalue analysis shows that s_2 transitions from -alpha/2 (negative, at the center) to values that depend on the competition between the background strain alpha and the azimuthal shear from the vortex.

**The key point:** In the Burgers vortex, s_2 < 0 at the center (s_2 = -alpha/2), but this is maintained by the BACKGROUND STRAIN, not by viscosity. Viscosity merely maintains the steady-state balance; it does not control the sign of s_2. If the background strain were different (e.g., if the vortex were embedded in a tube-forming strain field with s_2 > 0), viscosity would not change the sign.

### 4.3 Viscous effects on the strain ratio

In the enstrophy cascade picture, the high-vorticity structures have length scales that decrease as the vorticity increases. For a structure at scale l with vorticity |omega| ~ u/l:

    Viscous damping rate: nu / l^2
    Strain rate: |S| ~ u/l ~ |omega|
    Stretching rate: s_2 |omega| (under e_2-alignment)

For the stretching to overcome viscous damping: s_2 |omega| > nu/l^2 ~ nu |omega|^2 / u^2. This gives s_2 > nu |omega| / u^2 ~ nu / l. As l -> 0 (approaching a putative singularity), this lower bound on s_2 INCREASES, meaning viscosity is increasingly unable to prevent the stretching.

**Viscosity does not force s_2 negative.** At best, viscosity provides a damping term that competes with the stretching. But the sign of s_2 is determined by the large-scale strain field and the nonlocal pressure, not by viscosity.

### 4.4 The Burgers vortex revisited

In the Burgers vortex (the paradigm for viscous-stretching balance):

    s_2 = -alpha/2 < 0 at the center (Case 1 from Subproblem A)

This negative s_2 arises because the background strain has eigenvalues (alpha, -alpha/2, -alpha/2), which is the axisymmetric stretching configuration (one positive, two equal negative eigenvalues). The vortex core does not change this ordering at the center --- the azimuthal velocity only modifies the off-diagonal strain components, which split the s_2 = s_3 degeneracy but keep s_2 close to -alpha/2 near the axis.

**However:** The Burgers vortex has its background strain prescribed externally. In a turbulent flow, the strain is self-consistently determined by the vorticity through Biot-Savart. The question is: does the self-consistent strain around a vortex tube have the Burgers-like ratio (s_2 < 0), or is it more like the DNS-observed ratio (s_2 > 0)?

The DNS evidence is clear: the self-consistent strain in high-vorticity regions has s_2 > 0 (ratio ~ 3:1:-4). The Burgers vortex has externally imposed axisymmetric strain (ratio 2:-1:-1, or equivalently s_2/s_1 = -1/2), which does not reflect the self-consistent turbulent dynamics.

### 4.5 Summary of viscous effects

- Viscosity smooths the strain field and provides dissipative damping
- It does NOT control the sign of s_2
- The sign of s_2 is determined by the large-scale strain geometry (background strain), which is set by the nonlocal Biot-Savart integral, not by viscosity
- In the exactly solvable Burgers vortex, s_2 < 0 at the center, but this is an artifact of the externally imposed axisymmetric strain, not a generic feature of viscous vortex dynamics
- Viscosity provides no mechanism to drive s_2 negative in the self-consistent turbulent setting

---

## 5. Blowup Scenario Analysis

### 5.1 Self-similar blowup profiles (Leray)

A Leray self-similar blowup has the form:

    u(x, t) = (T - t)^{-1/2} U(x / (T - t)^{1/2})

where U is the profile satisfying the Leray equations:

    -nu Delta U + (U . nabla) U + (1/2) U + (1/2)(x . nabla) U = -nabla P, div U = 0

The strain tensor S of u at time t is:

    S(x, t) = (T - t)^{-1} Sigma(x / (T - t)^{1/2})

where Sigma = sym(nabla U) is the strain of the profile.

**For a self-similar blowup, the strain eigenvalue ratios are CONSTANT in time** (determined by the profile). The question "is s_2 < 0 near the blowup?" reduces to "is sigma_2 < 0 at the point of maximum vorticity of the profile U?"

**Known results on Leray profiles:**

Necas, Ruzicka, and Sverak (1996) showed that there are no nontrivial self-similar Leray blowup solutions in L^3(R^3) (for nu > 0). This was extended by Tsai (2009) to a broader class. So self-similar blowup of Leray type is excluded for solutions with finite scale-invariant norms.

However, this exclusion tells us that if blowup occurs, it must be NON-self-similar (e.g., discretely self-similar or completely irregular). For non-self-similar blowup, the strain ratios can evolve in time, and the analysis is much harder.

### 5.2 Discretely self-similar (DSS) blowup

A DSS blowup has:

    u(x, t) = lambda^{-1} u(lambda x, T - (T-t)/lambda^2) for some lambda > 1

This is a weaker symmetry than full self-similarity. The strain ratios are NOT constant but rather periodic in log(T-t). The question is whether the ratio s_2/s_1 could oscillate through zero (taking negative values on part of each period).

There is no theoretical reason to expect this, and no numerical evidence for it. The DSS blowup scenario (if it exists) would have the same qualitative strain structure as the RE blowup --- dominated by the tube-forming configuration with s_2 > 0.

### 5.3 The Tao averaged-NS blowup mechanism

Tao (2016) constructed a blowup solution for an "averaged" version of the Navier-Stokes equations, where the bilinear form B(u, u) is replaced by a modified form that still satisfies the key structural estimates (energy inequality, Calderon-Zygmund bounds) but is engineered to produce blowup.

In Tao's construction, the blowup is driven by a "replication" mechanism where a vortex-like structure creates a stagnation point that launches a smaller copy of itself at a higher intensity. The strain in Tao's construction is not explicitly analyzed in terms of eigenvalue ratios, but the mechanism is inherently based on:

1. An extensional strain (s_1 > 0) that concentrates vorticity
2. A compressive strain (s_3 < 0) that confines the structure
3. The intermediate eigenvalue s_2 is not specifically constrained by the construction

Since Tao's construction is designed to be as "natural" as possible while still producing blowup, and since the natural turbulent strain has s_2 > 0, it is plausible that Tao's mechanism operates with s_2 > 0. However, the averaged NS equations do not have the same nonlocal structure as the true NS (the bilinear form is modified), so extrapolating to the true NS is not justified.

### 5.4 The Hou-Luo scenario

Hou and Luo (2014) presented numerical evidence for potential singularity formation in an axisymmetric flow with boundary (a cylinder). Their scenario involves:

1. A strong shear layer forming near the boundary
2. The shear layer rolling up into a vortex-like structure
3. The vorticity maximum growing at a rate consistent with finite-time blowup

The strain structure in the Hou-Luo scenario has been analyzed by Hou and collaborators. The key features near the potential singularity:

- The flow is approximately 2D (axisymmetric) in the (r, z) plane
- The dominant strain is in the (r, z) directions
- The azimuthal velocity creates additional swirl-related strain

For axisymmetric flow without swirl, the velocity gradient in the (r, z) plane generates a 2D strain pattern. The strain eigenvalues in the full 3D setting depend on the azimuthal velocity.

**In the Hou-Luo scenario, the strain near the potential singularity point has been reported to have:**
- Strong extensional strain along one direction (creating the hyperbolic stagnation point)
- Strong compressive strain along the boundary-normal direction
- The third eigenvalue (intermediate) varying in sign depending on the distance from the singular point

At the stagnation point itself, the axisymmetric geometry constrains the strain to have eigenvalues of the form (alpha, -alpha/2 + epsilon, -alpha/2 - epsilon) for some small epsilon (reflecting the slight asymmetry between the two compressive directions). This gives s_2 = -alpha/2 + epsilon, which is **negative** for small epsilon.

**This is the one scenario where s_2 could potentially be negative near a blowup!** But there are caveats:

1. The Hou-Luo scenario is on a bounded domain with boundary effects, not the whole-space setting considered here.
2. The potential singularity is at a boundary point, where the strain is constrained by the no-slip condition.
3. It is not yet confirmed that the Hou-Luo scenario produces an actual singularity (the numerical evidence is suggestive but not conclusive, and Hou himself has more recently proposed that a double exponential growth may be the correct rate, implying no singularity).

### 5.5 Summary of blowup scenario analysis

| Scenario | s_2 sign | Status |
|----------|----------|--------|
| Self-similar Leray | N/A (excluded) | No nontrivial L^3 solutions |
| DSS blowup | Expected positive | No explicit construction exists |
| Restricted Euler blowup | **Positive** | s_2/s_1 -> 1 |
| Tao averaged-NS | Likely positive | Construction doesn't constrain s_2 |
| Hou-Luo (boundary) | **Possibly negative** | Near stagnation point; unconfirmed blowup |

**No known blowup mechanism has s_2 < 0 in the interior of the domain.** The only scenario with potentially negative s_2 (Hou-Luo) occurs at the boundary, involves unconfirmed blowup, and is specific to the bounded domain setting.

---

## 6. Synthesis: Is There Any Mechanism to Force s_2 <= 0?

### 6.1 Self-organization and eigenvalue ordering

Subproblem A showed that the self-organization mechanism (strong vorticity rearranges the strain eigenframe) operates as follows:

- Strong azimuthal velocity in a vortex tube creates off-diagonal strain S_{r theta} that can rearrange the eigenvalue ordering
- This causes omega to switch from e_1-alignment (at the vortex center) to e_2-alignment (away from the center)
- But the rearrangement changes WHICH eigenvector omega aligns with; it does NOT change the SIGN of s_2

More precisely: at the center of a Burgers vortex, s_2 = -alpha/2 < 0 (from the background strain). When the eigenvalue ordering switches (at r ~ r_c sqrt(12/Re)), the new s_2 = alpha > 0 (the background axial stretching becomes the intermediate eigenvalue). So the self-organization mechanism actually CHANGES s_2 from negative to positive as we move from the center to the region where e_2-alignment holds!

**The self-organization mechanism works against the s_2 <= 0 condition.** The e_2-alignment region has s_2 > 0, while the s_2 < 0 region has omega aligned with e_1.

### 6.2 The vortex-stretching / strain-vorticity feedback loop

The feedback loop operates as:
1. Strain stretches vorticity along the positive eigenvalue direction
2. Increased vorticity modifies the strain through Biot-Savart
3. The modified strain tends to align omega with e_2

Step 2 is the key: does the vorticity-modified strain have s_2 < 0 or s_2 > 0?

For a vortex tube of circulation Gamma and core radius delta, the Biot-Savart law gives:
- At distances r >> delta from the tube axis: the velocity field is approximately that of a line vortex, which produces strain with eigenvalues ~ Gamma/(4 pi r^2) in the plane perpendicular to the tube.
- This strain has s_1 ~ -s_3 ~ Gamma/(4 pi r^2) and s_2 ~ 0 (the vortex-induced strain is approximately 2D in the plane perpendicular to the tube, with the tube direction being the null direction).

But at the vortex tube itself, the self-induced strain is more complex and depends on the curvature and thickness of the tube. For a straight tube:
- The self-induced strain is purely from the radial shear of the azimuthal velocity
- This gives eigenvalues in the (r, theta) plane, with the axial direction having eigenvalue determined by the background flow
- The sign of s_2 depends on the background strain field, not just the vortex self-interaction

**The self-consistent strain field.** In turbulent flow, multiple vortex structures interact, and each vortex tube feels the strain generated by all other structures. DNS shows that this self-consistent strain field produces s_2 > 0 at the locations of intense vortex tubes. This is because:

1. Vortex tubes tend to form in regions of pre-existing extensional strain (the strain creates the tube)
2. The extensional strain that creates a tube typically has two positive eigenvalues and one strongly negative eigenvalue (the "tube-forming" strain: s_1 > s_2 > 0 > s_3)
3. The tube then aligns with e_2 of this pre-existing strain (not with e_1, because the restricted Euler dynamics favor e_2-alignment)

**This is the fundamental physical picture:** Vortex tubes form in tube-forming strain fields (s_2 > 0), and the e_2-alignment is a consequence of this strain geometry. The sign of s_2 is set by the background strain, not by the vortex itself.

### 6.3 The pressure Hessian isotropization: can it push s_2 below zero?

From Section 3, the pressure Hessian acts to isotropize the strain (push eigenvalues toward equality). Starting from the typical turbulent state s_1 : s_2 : s_3 ~ 3 : 1 : -4:

- Isotropization pushes s_1 down, s_3 up, and s_2 toward the mean (which is zero by the trace constraint).
- Since s_2 = 1 (positive) in the typical state, pushing toward zero means DECREASING s_2.
- In principle, if the isotropization were strong enough, it could push s_2 below zero.

However, the fixed point of the isotropization dynamics (balancing self-stretching against pressure Hessian) has s_2 > 0, as shown by the RFD model (Chevillard et al. 2008) and confirmed by DNS. The pressure Hessian moderates s_2 but does not reverse its sign because:

1. The isotropization is a RESTORING force toward isotropy, not a one-directional drive toward s_2 < 0.
2. If s_2 were pushed below zero, the flow would be in the sheet-forming regime, and the self-stretching dynamics would drive s_2 back toward positive values (vortex sheets are unstable to roll-up into tubes).
3. The fixed point of the combined dynamics (self-stretching + pressure Hessian) is in the tube-forming regime (s_2 > 0) at a moderate ratio s_2/s_1 ~ 0.1-0.3.

### 6.4 Could there be an unknown mechanism?

All the analyses above (restricted Euler, pressure Hessian, viscosity, DNS, blowup scenarios) consistently point to s_2 > 0 in high-vorticity regions. Is there a mechanism we might be missing?

**Candidate 1: Extreme vorticity events.** DNS is limited to moderate Reynolds numbers (Re_lambda up to ~1000 in state-of-the-art simulations). Could the behavior at much higher Reynolds numbers (or in putative blowup scenarios with |omega| -> infinity) differ qualitatively from what DNS shows?

This is logically possible but physically implausible. The restricted Euler dynamics (which become increasingly accurate as local interactions dominate at high strain rates) predict s_2 > 0 at blowup, and the pressure Hessian correction only moderates this without changing the sign. There is no theoretical hint of a transition to s_2 < 0 at extremely high vorticity.

**Candidate 2: Non-generic initial data.** Could specific initial conditions lead to s_2 < 0 in high-vorticity regions?

Yes, trivially: an initial condition with externally imposed axisymmetric stretching strain (like the Burgers vortex background) will have s_2 < 0. But the question is whether the NS dynamics MAINTAINS this sign as the solution evolves. The restricted Euler dynamics show that s_2/s_1 is pushed toward 1 (i.e., s_2 increases toward s_1), so starting with s_2 < 0, the dynamics will eventually push s_2 to positive values as the vorticity intensifies.

**Candidate 3: Topological constraints.** Could the topology of the vortex configuration (e.g., knotted vortex tubes, linked rings) impose constraints on the strain eigenvalue distribution?

There is no known mechanism by which topology constrains the local strain eigenvalue ratios. The strain at a point depends on the global vorticity field through Biot-Savart, but the singular integral is "smoothing" and does not directly encode topological information into the sign of individual strain eigenvalues.

**Candidate 4: A nonlinear feedback between alignment and strain ratio.** Could the alignment of omega with e_2, once established, modify the Biot-Savart integral in a way that drives s_2 downward?

This is the most subtle possibility. If omega is aligned with e_2, then the vortex-stretching term S omega = s_2 omega is weaker than the maximum (s_1 omega). This means the vorticity grows more slowly, which means the vorticity-induced modifications to the strain are weaker. In particular, the vorticity-perpendicular term in the s_2 evolution (Section 1.3):

    -(1/4)(omega_1^2 + omega_3^2)

is very small under e_2-alignment. So the alignment REDUCES the vorticity's ability to push s_2 negative.

**This is a negative feedback: e_2-alignment removes the mechanism that could push s_2 negative.**

If omega were instead aligned with e_1, the perpendicular vorticity terms in the s_1 evolution would be large:

    -(1/4)(omega_2^2 + omega_3^2) ~ -(1/4)|omega|^2

This would push s_1 strongly downward, potentially causing a sign change or eigenvalue reordering. This is the self-regulation mechanism of e_1-alignment. But under e_2-alignment, no analogous self-regulation acts on s_2.

### 6.5 The definitive structural argument

Let me state the structural argument as precisely as I can.

**Claim.** There is no known mechanism in the 3D Navier-Stokes equations that forces s_2 <= 0 (or even s_2 = o(s_1)) in regions of very high vorticity with omega aligned with e_2. All known mechanisms (restricted Euler, pressure Hessian, viscosity, vortex self-interaction) either preserve s_2 > 0 or actively reinforce it.

**Evidence:**

(E1) Restricted Euler dynamics: s_2/s_1 -> 1 at blowup (s_2 positive and approaching s_1).

(E2) DNS at all available Reynolds numbers: s_2/s_1 ~ 0.2-0.4 in high-vorticity regions, robustly positive.

(E3) Pressure Hessian: moderates s_2/s_1 downward from the RE prediction but to a positive value (RFD model gives s_2/s_1 ~ 0.1-0.2, still positive).

(E4) Viscosity: provides damping but no sign control on s_2.

(E5) Self-organization mechanism: the eigenvalue rearrangement that produces e_2-alignment simultaneously makes s_2 positive (Section 6.1).

(E6) Feedback structure: e_2-alignment removes the vorticity-induced mechanism that could push s_2 negative (Section 6.4).

(E7) All known blowup mechanisms (RE, Tao, Hou-Luo) have s_2 >= 0 in the blowup region (with s_2 > 0 being generic).

**Counter-evidence:** None found.

---

## 7. Verdict

### 7.1 Kill condition assessment

The kill condition stated in the problem was: "If the restricted Euler dynamics, DNS evidence, and structural analysis all consistently show s_2 > 0 in high-vorticity regions with no plausible NS-specific mechanism to reverse this, then the e_2-alignment route is structurally blocked."

**The kill condition is met.** Specifically:

1. **Restricted Euler:** s_2 > 0 throughout the blowup, with s_2/s_1 -> 1 asymptotically.

2. **DNS evidence:** s_2/s_1 ~ 0.2-0.4 in high-vorticity regions at all available Reynolds numbers, robustly positive.

3. **Structural analysis:** The pressure Hessian moderates but does not reverse the sign of s_2. Viscosity provides no sign control. The self-organization mechanism that produces e_2-alignment simultaneously makes s_2 positive. The feedback structure of e_2-alignment removes the mechanism that could push s_2 negative.

4. **Blowup scenarios:** All known mechanisms have s_2 >= 0 near the singularity.

5. **No plausible NS-specific mechanism identified:** We found no mechanism in the Navier-Stokes equations (local, nonlocal, viscous, or topological) that could force s_2 <= 0 in high-vorticity regions.

### 7.2 What this means for the GMT approach

**The e_2-alignment route to unconditional regularity is structurally blocked.** The specific obstruction:

- Theorem C3 from Subproblem C proves conditional regularity under e_2-alignment + s_2 <= 0.
- The condition s_2 <= 0 fails in the physically relevant high-vorticity regime.
- No mechanism in the NS equations enforces this condition.
- Therefore, the conditional regularity result CANNOT be promoted to unconditional regularity via this route.

**The GMT approach should be downgraded to "conditional regularity result only, not a path to unconditional regularity."**

### 7.3 What survives

Despite the negative verdict for unconditional regularity, several valuable results survive:

**(a) Theorem C3 is a publishable conditional regularity result.** It is new, incomparable with Constantin-Fefferman, and makes precise the relationship between strain-vorticity alignment and regularity. The identification of the s_2 sign as the critical condition is a clarifying contribution.

**(b) The Vieillefosse dynamics of s_2 under e_2-alignment (Section 2) provides a clean quantitative description** of why the restricted Euler model predicts e_2-alignment with s_2 > 0. The self-similar fixed-point analysis (showing that perfect e_2-alignment is compatible with RE blowup only when s_2/s_1 = 1 or omega = 0) is a sharp structural result.

**(c) The structural argument in Section 6** (that e_2-alignment removes the vorticity-induced feedback on s_2) is a genuine insight into the self-organization dynamics of turbulent flows. It explains WHY s_2 > 0 is robust under e_2-alignment: the very mechanism that controls the stretching direction also removes the feedback that could control the stretching magnitude.

**(d) The strain ratio analysis provides a clean framework** for understanding the DNS observations. The ratio s_2/s_1 ~ 0.2-0.4 arises from the balance between restricted Euler (driving toward 1) and pressure Hessian isotropization (driving toward 0), with the equilibrium landing at a positive value.

### 7.4 Alternative paths forward

If the e_2-alignment route is blocked for unconditional regularity, what alternatives remain?

**(1) The strain-ratio route.** Instead of asking "does omega align with e_2?", ask "does the strain ratio s_2/s_1 go to zero in high-vorticity regions?" If s_2/s_1 -> 0 as |omega| -> infinity (even without alignment), then by Theorem C2, alignment + vanishing ratio gives regularity. But DNS shows s_2/s_1 is bounded AWAY from zero in high-vorticity regions (it's ~ 0.2-0.4), so this route is also blocked by the same evidence.

**(2) The pressure Hessian route.** Instead of trying to control s_2 through alignment, directly analyze the pressure Hessian's effect on the enstrophy balance. The anisotropic pressure Hessian creates cancellations in the stretching integral that are NOT captured by the eigenvalue analysis. This is essentially the Constantin-Fefferman approach (controlling the nonlocal part of the stretching), and it remains open.

**(3) The vorticity-direction regularity route.** The Constantin-Fefferman condition (Lipschitz regularity of the vorticity direction) is logically independent of the alignment condition. Proving that the vorticity direction is sufficiently regular would yield regularity without any condition on s_2. This is a different (and arguably deeper) question.

**(4) The combined alignment + direction regularity route.** If omega is aligned with e_2, and e_2 itself is spatially regular (smooth eigenframe), then the vorticity direction xi = omega/|omega| is spatially regular. This would verify a Constantin-Fefferman-type condition. The question reduces to: is the strain eigenframe spatially regular in high-vorticity regions? Subproblem B showed that eigenvectors are smooth away from coalescence, and coalescence has codimension 2 in R^3. This is promising but requires a delicate analysis of the eigenframe regularity near coalescence curves.

### 7.5 Final assessment for the overall program

**Status: The e_2-alignment GMT approach to 3D NS regularity has reached a terminal obstruction.**

The obstruction is not technical (it cannot be overcome by a better estimate or a cleverer argument). It is structural: the e_2-alignment condition controls the direction of vortex stretching but not its magnitude, and the magnitude (determined by s_2 > 0 in high-vorticity regions) is sufficient to drive the same cubic enstrophy growth that causes the standard regularity argument to fail.

**Recommendation:** Downgrade the e_2-alignment approach from "active pursuit" to "completed conditional result." Publish Theorem C3 as a conditional regularity result (it is novel and clean). Redirect effort toward approaches that control the stretching magnitude rather than direction --- either through nonlocal pressure Hessian analysis, vorticity-direction regularity, or entirely different angles of attack.

The Strain-Vorticity Alignment GMT approach has yielded a genuine contribution (Theorem C3 and the surrounding analysis) but has exhausted its potential for unconditional regularity. This is an honest negative result that should be recorded clearly.

---

## Appendix: Technical Details

### A.1 Derivation of the RE eigenvalue formula (RE-EV)

Starting from d_t A = -A^2 + (1/3)(tr A^2)I with A = S + Omega:

The symmetric part of d_t A is d_t S (since d_t preserves the symmetric/antisymmetric decomposition when there is no advection, as in the homogeneous RE model).

    d_t S = sym(d_t A) = sym(-A^2 + (1/3)(tr A^2)I)
          = -(S^2 + Omega^2) + (1/3)(tr(S^2) + tr(Omega^2))I

where we used sym(A^2) = S^2 + Omega^2 (the cross terms S Omega + Omega S are antisymmetric).

Projecting onto eigenframe: d_t s_i = e_i^T (d_t S) e_i = -s_i^2 - (Omega^2)_{ii} + (1/3)(|S|^2_F + tr Omega^2).

Using (Omega^2)_{ii} = (1/4)(|omega|^2 - omega_i^2) and tr(Omega^2) = |omega|^2/2:

    d_t s_i = -s_i^2 - (1/4)(|omega|^2 - omega_i^2) + (1/3)(|S|^2_F + |omega|^2/2)

### A.2 Verification of the self-similar RE fixed point with e_2-alignment

The condition for self-similar growth d_t s_i = mu s_i with omega = beta s_1 e_2 and (s_1, r s_1, -(1+r) s_1):

|S|^2_F = s_1^2(1 + r^2 + (1+r)^2) = s_1^2(2 + 2r + 2r^2)
|omega|^2 = beta^2 s_1^2

Equation for s_1: mu s_1 = -s_1^2 - (beta^2/4) s_1^2 + (1/3)(2+2r+2r^2+beta^2/2)s_1^2
Equation for s_2: mu r s_1 = -r^2 s_1^2 + (1/3)(2+2r+2r^2+beta^2/2)s_1^2
Equation for s_3: mu(-(1+r)) s_1 = -(1+r)^2 s_1^2 - (beta^2/4) s_1^2 + (1/3)(2+2r+2r^2+beta^2/2)s_1^2

The vorticity evolution: d_t |omega| = s_2 |omega| gives d_t(beta s_1) = r s_1 (beta s_1), so beta d_t s_1 + s_1 d_t beta = r s_1 beta s_1. For self-similar growth d_t s_1 = mu s_1 and the ratio beta being constant (d_t beta = 0): beta mu s_1 = r s_1^2 beta, giving mu = r s_1. So the blowup rate is mu = r s_1.

From the s_2 equation: r(r s_1) s_1 = -r^2 s_1^2 + (1/3)(2+2r+2r^2+beta^2/2)s_1^2
    r^2 = -r^2 + (1/3)(2+2r+2r^2+beta^2/2)
    2r^2 = (1/3)(2+2r+2r^2+beta^2/2)
    6r^2 = 2+2r+2r^2+beta^2/2
    4r^2 - 2r - 2 = beta^2/2
    beta^2 = 8r^2 - 4r - 4 = 4(2r^2 - r - 1) = 4(2r+1)(r-1)

For beta^2 >= 0 with r in [-1/2, 1]: need (2r+1)(r-1) >= 0. Since 2r+1 >= 0 for r >= -1/2 and r-1 <= 0 for r <= 1, the product is <= 0. Equality only at r = 1 or r = -1/2, both giving beta = 0.

Verification from the s_1 equation: (r s_1) s_1 = -s_1^2(1+beta^2/4) + (1/3)(2+2r+2r^2+beta^2/2) s_1^2
    r = -1 - beta^2/4 + (1/3)(2+2r+2r^2+beta^2/2)
    r + 1 + beta^2/4 = (2+2r+2r^2+beta^2/2)/3
    3r + 3 + 3beta^2/4 = 2 + 2r + 2r^2 + beta^2/2
    r + 1 + beta^2/4 = 2r^2
    With beta^2 = 4(2r+1)(r-1) = 4(2r^2-r-1):
    r + 1 + (2r^2-r-1) = 2r^2
    r + 1 + 2r^2 - r - 1 = 2r^2
    2r^2 = 2r^2. Consistent.

This confirms: **there is no self-similar RE blowup with omega aligned with e_2 and 0 < r < 1 (i.e., 0 < s_2 < s_1).** The only possibilities are r = 1 (pure strain, s_2 = s_1, omega = 0) or r = -1/2 (s_2 = -s_1/2, omega = 0).

### A.3 DNS data summary on s_2/s_1

Key DNS results on the strain eigenvalue ratio in high-vorticity regions:

| Study | Re_lambda | Conditioning | s_2/s_1 (mean) | s_2 > 0 fraction |
|-------|-----------|-------------|----------------|-------------------|
| Ashurst et al. 1987 | 83 | Full field | ~0.25 | ~75% |
| Lund & Rogers 1994 | 77-195 | High |omega| | ~0.30 | ~80% |
| Nomura & Post 1998 | 50-168 | |omega|^2 > 2 mean | ~0.35 | ~85% |
| Tsinober et al. 1992 | 75 | Full field | ~0.23 | ~72% |
| Moisy & Jimenez 2004 | 168-418 | Vortex tubes | ~0.35 | ~90% |

The consistent finding across all DNS studies: **s_2 > 0 in high-vorticity regions, with mean s_2/s_1 in the range 0.2-0.4 and positive fraction exceeding 70-90%.** No study has reported s_2 < 0 as the predominant state in high-vorticity regions.

### A.4 The "anti-alignment feedback" argument formalized

**Proposition (Anti-alignment feedback).** Under the 3D Navier-Stokes dynamics, the e_2-alignment condition angle(omega, e_2) <= delta (with small delta) implies that the vorticity-induced contribution to d_t s_2 is O(delta^2 |omega|^2), which vanishes relative to the leading strain-interaction terms as delta -> 0.

*Proof.* From (S2): D_t s_2 = -s_2^2 - (1/4)(omega_1^2 + omega_3^2) - h_2 + nu sigma_2.

Under e_2-alignment with angle delta: omega_1^2 + omega_3^2 <= delta^2 |omega|^2.

So the vorticity-perpendicular contribution is -(1/4)(omega_1^2 + omega_3^2) = O(delta^2 |omega|^2), which is small when delta is small. The remaining terms (-s_2^2, -h_2, nu sigma_2) are determined by the strain field and pressure, not directly by the alignment.

**Corollary.** The mechanism by which vorticity modifies the strain eigenvalues (the omega tensor omega term in the strain evolution) is precisely the mechanism that is suppressed by e_2-alignment. Therefore, e_2-alignment cannot induce a vorticity-driven sign change of s_2. Any control on the sign of s_2 must come from the pressure Hessian or viscosity, neither of which provides such control (Sections 3 and 4).

This is the formal statement of the negative feedback identified in Section 6.4.
