# Path 1: Directional Cancellation in the Biot-Savart Kernel for D_xi S

**Date:** 2026-04-02
**Parent:** three-practical-paths.md, coupled-bootstrap-attempt.md
**Classification:** Full computation, honest assessment
**Target:** Logarithmic improvement |D_xi S| <= C |omega|^{3/2} / (nu^{1/2} log^{1/2}(|omega|))
**Depends on:** Theorem CB (delta > 1/2 suffices), e_2-alignment (Subproblem A), Biot-Savart structure

---

## 0. Executive Summary

This document carries out the explicit computation of the doubly-projected Biot-Savart kernel for D_xi S and determines whether the angular cancellation from the self-referential structure (the direction xi is determined by the same vorticity field that generates S) produces a logarithmic improvement over the standard Calderon-Zygmund estimate.

**Verdict: The cancellation is real but insufficient.** The double contraction xi_k ... xi_l of the Biot-Savart kernel with the Levi-Civita tensor produces a genuine angular cancellation that eliminates one spherical harmonic mode from the kernel. However, this cancellation is a *finite multiplicative constant* improvement, not a logarithmic one. The surviving angular modes have the same homogeneity degree as the original kernel, and after integrating over radial shells in the near-field, they produce the same 1/rho scaling as the unprojected kernel. The logarithmic gain does not materialize from the angular structure alone.

A secondary mechanism -- the coherent alignment of vorticity directions in the near-field, combined with the mean-zero property of the CZ kernel -- does produce a cancellation in the near-field integral. However, this cancellation is defeated by the *variation* of |omega(y)| across the near-field ball, which reintroduces the full dimensional scaling. The logarithmic gain would require not just directional coherence of xi but also approximate constancy of |omega| on a ball of radius >> r_c, which fails at the vorticity maximum (where |omega| has a quadratic profile with curvature of order Omega/r_c^2).

The computation does produce a precise structural result: the doubly-projected kernel has a specific tensorial form that constrains which components of D_xi S are large. This constraint is geometrically meaningful but does not reduce the scalar magnitude below the CZ bound.

---

## 1. The Biot-Savart Kernel and Its Derivatives

### 1.1 Setup

The Biot-Savart law in R^3:

    u_i(x) = integral K_{il}(x - y) omega_l(y) dy

where:

    K_{il}(z) = (1/(4 pi)) epsilon_{ilm} z_m / |z|^3

We use the convention that repeated indices are summed. Here epsilon_{ilm} is the Levi-Civita symbol.

### 1.2 First derivatives of K

    partial_k K_{il}(z) = (1/(4 pi)) epsilon_{ilm} partial_k (z_m / |z|^3)
                        = (1/(4 pi)) epsilon_{ilm} [delta_{km} / |z|^3 - 3 z_k z_m / |z|^5]

So:

    partial_k K_{il}(z) = (1/(4 pi)) epsilon_{ilm} [delta_{km} |z|^{-3} - 3 z_k z_m |z|^{-5}]     (1.1)

### 1.3 Second derivatives of K

    partial_j partial_k K_{il}(z) = (1/(4 pi)) epsilon_{ilm} partial_j [delta_{km} |z|^{-3} - 3 z_k z_m |z|^{-5}]

Computing each part:

    partial_j (|z|^{-3}) = -3 z_j |z|^{-5}

    partial_j (z_k z_m |z|^{-5}) = delta_{jk} z_m |z|^{-5} + z_k delta_{jm} |z|^{-5} - 5 z_j z_k z_m |z|^{-7}

Therefore:

    partial_j partial_k K_{il}(z) = (1/(4 pi)) epsilon_{ilm} [-3 delta_{km} z_j |z|^{-5}
                                     - 3 (delta_{jk} z_m + z_k delta_{jm}) |z|^{-5}
                                     + 15 z_j z_k z_m |z|^{-7}]                        (1.2)

This can be written more compactly. Define hat{z} = z/|z| and r = |z|. Then z_j = r hat{z}_j and:

    partial_j partial_k K_{il}(z) = (1/(4 pi)) epsilon_{ilm} r^{-4} 
        [-3 delta_{km} hat{z}_j - 3 delta_{jk} hat{z}_m - 3 delta_{jm} hat{z}_k + 15 hat{z}_j hat{z}_k hat{z}_m]
                                                                                         (1.3)

**Verification of homogeneity:** The kernel K_{il}(z) is homogeneous of degree -2. Its first derivative is degree -3. Its second derivative is degree -4. Confirmed: (1.3) scales as r^{-4}.

### 1.4 The strain kernel

The strain is S_{ij}(x) = (partial_i u_j + partial_j u_i) / 2. Using u_i = integral K_{il} omega_l dy:

    S_{ij}(x) = (1/2) integral [partial_i K_{jl}(x - y) + partial_j K_{il}(x - y)] omega_l(y) dy

The gradient of the strain:

    partial_k S_{ij}(x) = (1/2) integral [partial_k partial_i K_{jl}(x-y) + partial_k partial_j K_{il}(x-y)] omega_l(y) dy

The directional derivative along xi:

    (D_xi S)_{ij}(x) = xi_k(x) partial_k S_{ij}(x)
        = (1/2) xi_k(x) integral [partial_k partial_i K_{jl}(x-y) + partial_k partial_j K_{il}(x-y)] omega_l(y) dy
                                                                                         (1.4)

This is a principal value singular integral. The kernel is:

    M_{ij,l}(z, xi) = (1/2) xi_k [partial_k partial_i K_{jl}(z) + partial_k partial_j K_{il}(z)]    (1.5)

---

## 2. The Singly-Projected Kernel: Contraction with xi_k

### 2.1 Computing xi_k partial_k partial_i K_{jl}

From (1.3):

    xi_k partial_k partial_i K_{jl}(z) = (1/(4 pi)) epsilon_{jlm} r^{-4} 
        [-3 delta_{km} hat{z}_i xi_k - 3 delta_{ik} hat{z}_m xi_k - 3 delta_{im} hat{z}_k xi_k + 15 hat{z}_i hat{z}_k hat{z}_m xi_k]

Evaluating the contractions:

    delta_{km} xi_k = xi_m
    delta_{ik} xi_k = xi_i
    hat{z}_k xi_k = (xi . hat{z})    (denote this as cos(phi) where phi is the angle between xi and hat{z})

So:

    xi_k partial_k partial_i K_{jl}(z) = (1/(4 pi)) epsilon_{jlm} r^{-4}
        [-3 xi_m hat{z}_i - 3 xi_i hat{z}_m - 3 delta_{im} (xi . hat{z}) + 15 hat{z}_i hat{z}_m (xi . hat{z})]
                                                                                         (2.1)

### 2.2 The singly-projected strain gradient kernel

From (1.5):

    M_{ij,l}(z, xi) = (1/2) [xi_k partial_k partial_i K_{jl}(z) + xi_k partial_k partial_j K_{il}(z)]

By (2.1), the second term is obtained by swapping i and j:

    xi_k partial_k partial_j K_{il}(z) = (1/(4 pi)) epsilon_{ilm} r^{-4}
        [-3 xi_m hat{z}_j - 3 xi_j hat{z}_m - 3 delta_{jm} (xi . hat{z}) + 15 hat{z}_j hat{z}_m (xi . hat{z})]

Therefore:

    M_{ij,l}(z, xi) = (1/(8 pi)) r^{-4} {
        epsilon_{jlm} [-3 xi_m hat{z}_i - 3 xi_i hat{z}_m - 3 delta_{im}(xi . hat{z}) + 15 hat{z}_i hat{z}_m (xi . hat{z})]
      + epsilon_{ilm} [-3 xi_m hat{z}_j - 3 xi_j hat{z}_m - 3 delta_{jm}(xi . hat{z}) + 15 hat{z}_j hat{z}_m (xi . hat{z})]
    }                                                                                    (2.2)

This is the kernel for (D_xi S)_{ij}(x) = PV integral M_{ij,l}(x-y, xi(x)) omega_l(y) dy.

### 2.3 Angular form

Write M_{ij,l}(z, xi) = r^{-4} Omega_{ij,l}(hat{z}, xi) where:

    Omega_{ij,l}(hat{z}, xi) = (1/(8 pi)) {
        epsilon_{jlm} [-3 xi_m hat{z}_i - 3 xi_i hat{z}_m - 3 delta_{im} c + 15 hat{z}_i hat{z}_m c]
      + epsilon_{ilm} [-3 xi_m hat{z}_j - 3 xi_j hat{z}_m - 3 delta_{jm} c + 15 hat{z}_j hat{z}_m c]
    }                                                                                    (2.3)

where c = xi . hat{z} = cos(phi).

**Mean-zero property verification:** For the CZ theory to apply, the angular kernel must have zero mean on S^2:

    integral_{S^2} Omega_{ij,l}(hat{z}, xi) d sigma(hat{z}) = 0

Using the standard spherical integrals:

    integral_{S^2} hat{z}_a d sigma = 0
    integral_{S^2} hat{z}_a hat{z}_b d sigma = (4 pi / 3) delta_{ab}
    integral_{S^2} hat{z}_a hat{z}_b hat{z}_c d sigma = 0    (odd-order moments vanish)

Each term in Omega_{ij,l} is linear or cubic in hat{z}. The linear terms (hat{z}_i, hat{z}_j, hat{z}_m alone, or c = xi_a hat{z}_a) integrate to zero over S^2. The cubic term hat{z}_i hat{z}_m c = hat{z}_i hat{z}_m hat{z}_a xi_a also integrates to zero (third moment). And the term delta_{im} c integrates to delta_{im} integral xi . hat{z} d sigma = 0.

**Confirmed:** The kernel has zero mean on every sphere, as required by CZ theory.

---

## 3. The Double Projection: Contraction with xi_l

### 3.1 The key computation

When omega(y) = |omega(y)| xi(y), the integrand in the singular integral for (D_xi S)_{ij} becomes:

    M_{ij,l}(x-y, xi(x)) omega_l(y) = M_{ij,l}(x-y, xi(x)) |omega(y)| xi_l(y)

In the near-field where xi(y) approximately equals xi(x) = xi, this becomes:

    M_{ij,l}(z, xi) xi_l |omega(y)| = r^{-4} Omega_{ij,l}(hat{z}, xi) xi_l |omega(y)|

We need to compute the doubly-projected angular kernel:

    Omega_{ij}^{(2)}(hat{z}, xi) := Omega_{ij,l}(hat{z}, xi) xi_l                    (3.1)

### 3.2 Computing the double projection

From (2.3):

    Omega_{ij}^{(2)} = (1/(8 pi)) {
        epsilon_{jlm} xi_l [-3 xi_m hat{z}_i - 3 xi_i hat{z}_m - 3 delta_{im} c + 15 hat{z}_i hat{z}_m c]
      + epsilon_{ilm} xi_l [-3 xi_m hat{z}_j - 3 xi_j hat{z}_m - 3 delta_{jm} c + 15 hat{z}_j hat{z}_m c]
    }

Now compute each epsilon contraction with xi:

**Term A:** epsilon_{jlm} xi_l xi_m = 0

This vanishes because epsilon_{jlm} is antisymmetric in l,m while xi_l xi_m is symmetric.

**Term B:** epsilon_{jlm} xi_l xi_i hat{z}_m = xi_i (xi x hat{z})_j

where (xi x hat{z}) denotes the cross product. So epsilon_{jlm} xi_l hat{z}_m = (xi x hat{z})_j.

**Term C:** epsilon_{jlm} xi_l delta_{im} c = epsilon_{jli} xi_l c = (xi x e_i)_j c = -(e_i x xi)_j c

More precisely: epsilon_{jlm} delta_{im} = epsilon_{jli}. So this term is epsilon_{jli} xi_l c = (xi x hat{e}_i)_j * c, where hat{e}_i is the unit vector in the i-th direction. Actually, epsilon_{jli} xi_l = -(xi x hat{e}_j)_i ... let me be more careful.

We have epsilon_{jlm} xi_l delta_{im} = epsilon_{jli} xi_l. Now epsilon_{jli} = -epsilon_{jil} = epsilon_{ijl}. The vector with components epsilon_{jli} xi_l (over j) is: (xi x hat{e}_i). Let me verify: [xi x hat{e}_i]_j = epsilon_{jab} xi_a (hat{e}_i)_b = epsilon_{jab} xi_a delta_{bi} = epsilon_{jai} xi_a = epsilon_{jai} xi_a.

And epsilon_{jli} xi_l = epsilon_{jli} xi_l. Note epsilon_{jli} = epsilon_{lij} (cyclic) = -epsilon_{ilj} = epsilon_{ijl}. Hmm, let me just use the direct definition.

epsilon_{jlm} delta_{im} xi_l = epsilon_{jli} xi_l.

Now [a x b]_j = epsilon_{jab} a_a b_b. If we want epsilon_{jli} xi_l = epsilon_{jla} xi_l delta_{ai} = [xi x hat{e}_i]_j? No: [xi x hat{e}_i]_j = epsilon_{jab} xi_a delta_{bi} = epsilon_{jai} xi_a = epsilon_{jai} xi_a.

And epsilon_{jli} xi_l. Let me relabel: set a = l, then epsilon_{jai} xi_a. Yes! epsilon_{jli} xi_l = epsilon_{jai} xi_a = [xi x hat{e}_i]_j.

Wait, epsilon_{jli} = epsilon_{jli}. Relabeling l -> a: epsilon_{jai} xi_a. And [xi x hat{e}_i]_j = epsilon_{jab} xi_a (hat{e}_i)_b = epsilon_{jai} xi_a. Yes. So:

    epsilon_{jlm} xi_l delta_{im} = [xi x hat{e}_i]_j

But this is in terms of coordinate basis vectors. Let me write it as a cross product differently. Note that epsilon_{jai} = -epsilon_{jia}, so epsilon_{jai} xi_a = -epsilon_{jia} xi_a = -[hat{e}_i x xi]_j = [xi x hat{e}_i]_j. Good.

**Term D:** epsilon_{jlm} xi_l hat{z}_i hat{z}_m c = hat{z}_i c (xi x hat{z})_j

Since epsilon_{jlm} xi_l hat{z}_m = (xi x hat{z})_j.

Now collecting the terms in the first brace of Omega_{ij}^{(2)}:

    epsilon_{jlm} xi_l [-3 xi_m hat{z}_i - 3 xi_i hat{z}_m - 3 delta_{im} c + 15 hat{z}_i hat{z}_m c]

    = -3 * 0 (Term A, vanishes)
      - 3 xi_i (xi x hat{z})_j (Term B)
      - 3 [xi x hat{e}_i]_j c (Term C)
      + 15 hat{z}_i c (xi x hat{z})_j (Term D)

So the first brace gives:

    First = -3 xi_i (xi x hat{z})_j - 3 c [xi x hat{e}_i]_j + 15 c hat{z}_i (xi x hat{z})_j    (3.2a)

By symmetry (swapping i and j, and noting the second brace has epsilon_{ilm}):

    Second = -3 xi_j (xi x hat{z})_i - 3 c [xi x hat{e}_j]_i + 15 c hat{z}_j (xi x hat{z})_i   (3.2b)

**Therefore:**

    Omega_{ij}^{(2)}(hat{z}, xi) = (1/(8 pi)) {
        -3 xi_i (xi x hat{z})_j - 3 xi_j (xi x hat{z})_i
        - 3 c [xi x hat{e}_i]_j - 3 c [xi x hat{e}_j]_i
        + 15 c [hat{z}_i (xi x hat{z})_j + hat{z}_j (xi x hat{z})_i]
    }                                                                                    (3.3)

### 3.3 Simplification using the cross product structure

Let us define the vector:

    q = xi x hat{z}                                                                     (3.4)

Then q is perpendicular to both xi and hat{z}, with |q| = sin(phi) where phi is the angle between xi and hat{z}. Also c = cos(phi) = xi . hat{z}.

Note that [xi x hat{e}_i]_j = epsilon_{jab} xi_a delta_{bi} = epsilon_{jai} xi_a. This is the (i,j) component of the antisymmetric tensor epsilon_{jai} xi_a. Equivalently, it is the matrix representation of the cross-product operator xi x : for any vector v, (xi x v)_j = epsilon_{jab} xi_a v_b. Applied to hat{e}_i: (xi x hat{e}_i)_j = epsilon_{jai} xi_a.

The symmetric combination [xi x hat{e}_i]_j + [xi x hat{e}_j]_i = epsilon_{jai} xi_a + epsilon_{iaj} xi_a = (epsilon_{jai} + epsilon_{iaj}) xi_a.

Now epsilon_{jai} = -epsilon_{ija} (one transposition) and epsilon_{iaj} = -epsilon_{ija} (... let me just compute). epsilon_{jai} and epsilon_{iaj}: using the rule that epsilon_{abc} is fully antisymmetric with epsilon_{123} = 1.

epsilon_{jai} = sign of permutation (j,a,i) of (1,2,3).
epsilon_{iaj} = sign of permutation (i,a,j) of (1,2,3).

Note (i,a,j) is obtained from (j,a,i) by swapping the first and third elements, which is one transposition. So epsilon_{iaj} = -epsilon_{jai}.

Therefore: epsilon_{jai} + epsilon_{iaj} = epsilon_{jai} - epsilon_{jai} = 0.

**The symmetric part of the cross-product term vanishes identically:**

    [xi x hat{e}_i]_j + [xi x hat{e}_j]_i = 0                                         (3.5)

This is a fundamental identity: the map v -> xi x v is antisymmetric (it generates rotations about xi), so its symmetric part is zero.

This eliminates the middle line of (3.3), giving:

    Omega_{ij}^{(2)}(hat{z}, xi) = (1/(8 pi)) {
        -3 [xi_i q_j + xi_j q_i]
        + 15 c [hat{z}_i q_j + hat{z}_j q_i]
    }                                                                                    (3.6)

where q = xi x hat{z} and c = xi . hat{z}.

### 3.4 Further simplification

We can decompose hat{z} in the (xi, q, hat{z}_perp) frame. Since hat{z} = c xi + (hat{z} - c xi), and the component of hat{z} perpendicular to xi in the plane of (xi, hat{z}) is:

    hat{z} = c xi + s hat{n}

where s = sin(phi), hat{n} = (hat{z} - c xi)/s is the unit vector perpendicular to xi in the (xi, hat{z}) plane. Note that q = xi x hat{z} = s (xi x hat{n}), so |q| = s and q is perpendicular to both xi and hat{n}.

Substituting hat{z}_i = c xi_i + s hat{n}_i into (3.6):

    15 c [hat{z}_i q_j + hat{z}_j q_i] = 15 c [(c xi_i + s hat{n}_i) q_j + (c xi_j + s hat{n}_j) q_i]
        = 15 c^2 [xi_i q_j + xi_j q_i] + 15 c s [hat{n}_i q_j + hat{n}_j q_i]

So:

    Omega_{ij}^{(2)} = (1/(8 pi)) {
        (-3 + 15 c^2) [xi_i q_j + xi_j q_i]
        + 15 c s [hat{n}_i q_j + hat{n}_j q_i]
    }                                                                                    (3.7)

Using -3 + 15 c^2 = 3(5 c^2 - 1):

    Omega_{ij}^{(2)} = (3/(8 pi)) {
        (5 c^2 - 1) [xi_i q_j + xi_j q_i]
        + 5 c s [hat{n}_i q_j + hat{n}_j q_i]
    }                                                                                    (3.8)

### 3.5 Key structural observation

**The doubly-projected kernel Omega_{ij}^{(2)} is entirely in the q-direction as a tensor factor.** Every term has a q_j or q_i factor. This means:

    Omega_{ij}^{(2)} = q_j V_i + q_i V_j                                               (3.9)

where V is a vector in the (xi, hat{n}) plane:

    V_i = (3/(8 pi)) [(5 c^2 - 1) xi_i + 5 c s hat{n}_i]                              (3.10)

Since q = xi x hat{z} is perpendicular to xi, the tensor Omega_{ij}^{(2)} is a symmetric tensor with one index necessarily perpendicular to xi. In particular:

    Omega_{ij}^{(2)} xi_i xi_j = 2 (q . xi)(V . xi) = 0                               (3.11)

because q . xi = 0 (q is perpendicular to xi by definition of the cross product).

**Physical meaning:** The double contraction of D_xi S with xi vanishes at leading order in the near-field. That is, xi . (D_xi S) xi = 0 for the doubly-projected kernel. This is the cancellation. It says that the component of D_xi S that directly drives the stretching rate Q = xi . S xi along the vorticity direction has an *exact cancellation* in the doubly-projected singular integral.

However, this does NOT mean D_xi S = 0. The *other* components of D_xi S (those with at least one index perpendicular to xi) are nonzero and have the full O(r^{-4}) singularity.

### 3.6 Comparison with the singly-projected kernel

For the singly-projected kernel Omega_{ij,l}(hat{z}, xi) (equation (2.3)), the contraction xi_i xi_j Omega_{ij,l} is NOT zero in general. Specifically:

    xi_i xi_j Omega_{ij,l} = (1/(8 pi)) xi_i xi_j {
        epsilon_{jlm} [-3 xi_m hat{z}_i - 3 xi_i hat{z}_m - 3 delta_{im} c + 15 hat{z}_i hat{z}_m c]
      + epsilon_{ilm} [-3 xi_m hat{z}_j - 3 xi_j hat{z}_m - 3 delta_{jm} c + 15 hat{z}_j hat{z}_m c]
    }

This involves epsilon_{jlm} xi_j, which is nonzero for generic l (it is (xi x hat{e}_l)_... -- a cross product). So the singly-projected kernel does have a nonzero xi-xi component. The double projection kills this specific component.

**This is the precise cancellation from the self-referential structure.** The fact that both the differentiation direction and the vorticity direction are xi means that the leading (most dangerous) component of D_xi S -- the one that appears in dQ/dt = d(xi . S xi)/dt -- has an extra cancellation.

---

## 4. Angular Integrals and Effective Cancellation

### 4.1 The key angular integral

Consider the near-field contribution to (D_xi S)_{ij}(x_*) where omega(y) approximately equals Omega xi (constant direction and magnitude in a ball B_rho(x_*)):

    (D_xi S)_{ij}^{near} approx Omega * PV integral_{B_rho} r^{-4} Omega_{ij}^{(2)}(hat{z}, xi) d^3y
                          = Omega * PV integral_0^rho integral_{S^2} r^{-4} Omega_{ij}^{(2)}(hat{z}, xi) r^2 d sigma dr
                          = Omega * PV integral_0^rho r^{-2} dr * integral_{S^2} Omega_{ij}^{(2)}(hat{z}, xi) d sigma(hat{z})
                                                                                         (4.1)

**But the angular integral integral_{S^2} Omega_{ij}^{(2)}(hat{z}, xi) d sigma vanishes.**

Proof: From (3.8), Omega_{ij}^{(2)} involves terms with hat{z}_a hat{z}_b hat{z}_c (cubic) and hat{z}_a (linear) -- both are odd-degree spherical harmonics. Their integrals over S^2 vanish:

    integral_{S^2} hat{z}_a d sigma = 0
    integral_{S^2} hat{z}_a hat{z}_b hat{z}_c d sigma = 0

More explicitly, q = xi x hat{z} is linear in hat{z}, and the products involving c = xi . hat{z} introduce additional hat{z} factors. Every term in Omega_{ij}^{(2)} is an odd function of hat{z} (degree 1 or degree 3 in hat{z} components), so the integral over S^2 vanishes.

**This is the standard CZ mean-zero property.** It is NOT a new cancellation from the double projection. Any CZ kernel has zero angular mean. The double projection preserves this property but does not enhance it.

### 4.2 Beyond the constant-omega approximation

The near-field integral for the actual (non-constant) omega is:

    (D_xi S)_{ij}^{near} = PV integral_{B_rho} M_{ij,l}(x_* - y, xi) omega_l(y) dy

With omega_l(y) = |omega(y)| xi_l(y), we write:

    omega_l(y) = Omega xi_l + [|omega(y)| xi_l(y) - Omega xi_l]
               = Omega xi_l + [|omega(y)| - Omega] xi_l + |omega(y)| [xi_l(y) - xi_l]

The first term (Omega xi_l) gives the doubly-projected integral which vanishes by CZ mean-zero.

The second term involves Delta_omega(y) := |omega(y)| - Omega, the deviation of the vorticity magnitude from its maximum value. Near the maximum x_*, |omega(y)| = Omega - (1/2) |y - x_*|^2 |nabla^2 |omega|| + ... (since nabla |omega| = 0 at the maximum). So:

    |Delta_omega(y)| <= C |y - x_*|^2 Omega / r_c^2

where the curvature of |omega| at the maximum is of order Omega / r_c^2 (for a Burgers vortex profile |omega| ~ Omega exp(-r^2/(4 r_c^2))).

The contribution from the magnitude variation:

    I_{ij}^{(mag)} = integral_{B_rho} r^{-4} Omega_{ij}^{(2)}(hat{z}, xi) Delta_omega(y) dy    (4.2)

Since Delta_omega ~ -C r^2 Omega / r_c^2 near the maximum (note it is NEGATIVE since we are at the max):

    |I_{ij}^{(mag)}| ~ (Omega / r_c^2) integral_0^rho r^{-4} |Omega_{ij}^{(2)}| r^2 * r^2 dr
                     = (Omega / r_c^2) integral_0^rho |Omega_{ij}^{(2)}| dr

Since |Omega_{ij}^{(2)}| ~ 1 (it is a bounded angular function):

    |I_{ij}^{(mag)}| ~ (Omega / r_c^2) * rho                                           (4.3)

The third term involves the variation of the vorticity direction. With |xi(y) - xi(x_*)| <= |nabla xi| * |y - x_*| <= kappa |y - x_*| (where kappa = |D_xi xi| is the curvature of vortex lines, but more generally |nabla xi| could be larger):

    I_{ij}^{(dir)} = integral_{B_rho} M_{ij,l}(z, xi) |omega(y)| [xi_l(y) - xi_l] dy

This involves M_{ij,l} (the singly-projected kernel, not the doubly-projected one), since the direction variation breaks the double projection. Its magnitude:

    |I_{ij}^{(dir)}| ~ Omega |nabla xi| integral_0^rho r^{-4} * r * r^2 dr = Omega |nabla xi| integral_0^rho r^{-1} dr
                      = Omega |nabla xi| log(rho / epsilon)                              (4.4)

where epsilon is the PV cutoff (which disappears in the PV limit for the CZ kernel, but the logarithm indicates the borderline nature of this integral).

Actually, more carefully: M_{ij,l} is a CZ kernel of homogeneity -4 in R^3. For a function f with |f(y)| <= C |y - x_*|, the PV integral integral M_{ij,l}(x_* - y) f(y) dy converges absolutely (the integrand is |y|^{-4} * |y| * |y|^2 d|y| = |y|^{-1} d|y|, which is logarithmically divergent). The PV integral is well-defined but produces a log:

    |I_{ij}^{(dir)}| ~ C Omega |nabla xi| * rho    (after PV cancellation absorbs the log)
                                                                                         (4.5)

Actually, I need to be more precise. For a CZ kernel K of degree -(n) in R^n (here n = 3, degree -4 is degree -(n+1)), the operator f -> PV integral K(x-y) f(y) dy maps Lip to L^infty with bound C ||f||_{Lip}. Since the function [xi_l(y) - xi_l(x_*)] is Lipschitz with constant |nabla xi|:

    |PV integral_{B_rho} M_{ij,l}(x_*-y) |omega(y)| [xi_l(y) - xi_l(x_*)] dy|
        <= C Omega |nabla xi| rho^0 (Lip norm of CZ operator on B_rho)                  (4.5')

Wait, this is not quite right either. The CZ operator on a ball of radius rho with a Lipschitz function:

    PV integral_{B_rho} K(z) g(z) dz    where |g(z)| <= L |z|, |z| = r

The integrand is |K| |g| ~ r^{-(n+1)} * L r * r^{n-1} dr = L r^{-1} dr, which gives L log(rho/epsilon) before PV cancellation. After PV cancellation (using mean-zero of K on spheres), the integral of the odd part of g cancels, and we are left with the even part of g. For a Lipschitz function, the even part is O(|z|^2 L / |z|) = O(L |z|) at best, giving:

    |PV integral_{B_rho} K(z) g(z) dz| <= C L rho (not a log)                          (4.5'')

So the direction-variation contribution is:

    |I_{ij}^{(dir)}| <= C Omega |nabla xi| rho                                         (4.6)

### 4.3 Total near-field estimate

Combining (4.3) and (4.6):

    |(D_xi S)_{ij}^{near}| <= C Omega rho / r_c^2 + C Omega |nabla xi| rho            (4.7)

Using |nabla xi| ~ kappa at the vorticity maximum (where nabla |omega| = 0, so the dominant contribution to |nabla xi| comes from the curvature of vortex lines):

    |(D_xi S)^{near}| <= C Omega rho (1/r_c^2 + kappa)                                 (4.8)

### 4.4 The far-field estimate

For |y - x_*| > rho, the standard CZ estimate gives:

    |(D_xi S)^{far}| <= C ||nabla omega||_{L^p(B_rho^c)} (by CZ on the complement)

More precisely, D_xi S is a CZ operator of nabla omega (since nabla S = nabla^2 u and nabla^2 u is a CZ operator of nabla omega). On the far-field:

    |(D_xi S)^{far}(x_*)| <= C integral_{|y-x_*| > rho} |nabla omega(y)| / |y - x_*|^3 dy
                            + (contributions from distant vorticity regions)

For the Burgers vortex model, |nabla omega| ~ Omega/r_c for r ~ r_c and decays exponentially for r >> r_c. So:

    |(D_xi S)^{far}| ~ C (Omega/r_c) integral_rho^infty r^{-3} r^2 dr (if rho < r_c; but rho > r_c for our application)

For rho >> r_c (the interesting regime):

    |(D_xi S)^{far}| ~ C (Omega / r_c) * (r_c / rho)^2 * r_c = C Omega r_c^2 / rho^2  (4.9)

(The vorticity is concentrated in B_{r_c}, so the far-field sees a localized source at distance rho.)

### 4.5 Total estimate and optimization

Combining near-field (4.8) and far-field (4.9):

    |D_xi S| <= C Omega rho / r_c^2 + C Omega r_c^2 / rho^2                           (4.10)

(dropping the kappa rho term which is subdominant when kappa << 1/r_c).

Optimizing over rho: set rho / r_c^2 = r_c^2 / rho^2, giving rho^3 = r_c^4, i.e., rho = r_c^{4/3}.

    |D_xi S|_{opt} <= C Omega r_c^{4/3} / r_c^2 = C Omega / r_c^{2/3} = C Omega (Omega/nu)^{1/3}
                    = C Omega^{4/3} / nu^{1/3}                                          (4.11)

This gives |D_xi S| ~ Omega^{4/3} / nu^{1/3}, which corresponds to delta = 1/3 in the framework |D_xi S| <= C Omega^{1+delta}.

**Wait.** This is BETTER than the dimensional estimate delta = 1/2 (which gives Omega^{3/2}/nu^{1/2}). But delta = 1/3 < 1/2, so this is *worse* for the coupled bootstrap (which needs delta > 1/2).

**Something is wrong.** Let me recheck.

The issue is that the near-field estimate (4.8) uses the fact that the *leading term* vanishes (the constant-omega integral is zero by CZ mean-zero), and the first correction comes from the variation of omega. But this variation is ALWAYS present for any CZ singular integral, not just for the doubly-projected one. The standard CZ estimate also uses the mean-zero property to cancel the constant part of the integrand.

Let me redo this more carefully.

### 4.6 Corrected near-field analysis

The standard CZ argument for bounding nabla^2 u at a point x_*:

    nabla^2 u(x_*) = PV integral K(x_* - y) nabla omega(y) dy

where K is a CZ kernel of degree -3. Writing nabla omega(y) = nabla omega(x_*) + [nabla omega(y) - nabla omega(x_*)] and using the mean-zero property:

    PV integral_{B_rho} K(x_* - y) nabla omega(x_*) dy = 0 (mean-zero)

    integral_{B_rho} K(x_* - y) [nabla omega(y) - nabla omega(x_*)] dy ~ ||nabla^2 omega||_{L^infty} * rho

Wait, this gives the WRONG scaling for the dimensional estimate. Let me reconsider.

The correct CZ estimate is:

    ||nabla^2 u||_{L^p} <= C_p ||nabla omega||_{L^p}

This is a *global* L^p bound. For pointwise bounds at a specific point x_*, we use:

    |nabla^2 u(x_*)| = |PV integral K(x_* - y) nabla omega(y) dy|
                     <= C ||nabla omega||_{L^infty} + (tail term)

The constant C comes from the CZ kernel and does not involve a log. This bound gives:

    |nabla S(x_*)| <= C ||nabla omega||_{L^infty}

At the vorticity maximum, |nabla omega(x_*)| = |omega| |nabla xi| (since nabla |omega| = 0). But the relevant L^infty norm is the *global* maximum of |nabla omega|, which is typically achieved NOT at x_* but at a distance ~ r_c from x_*, where:

    |nabla omega|_{max} ~ Omega / r_c = Omega^{3/2} / nu^{1/2}

This gives the dimensional estimate |nabla S| ~ Omega^{3/2} / nu^{1/2}, confirming delta = 1/2.

**Now, what does the double projection buy?** The issue is that D_xi S involves a SPECIFIC contraction (xi_k partial_k S_{ij}) of the full gradient nabla S. The question is whether this specific contraction is smaller than the full gradient.

The double projection analysis showed that xi_i xi_j (D_xi S)_{ij} vanishes at the doubly-projected level (equation (3.11)). But (D_xi S)_{ij} itself, as a tensor, has the same magnitude as (nabla S)_{ij} -- the cancellation only affects specific components.

Let me reconsider the problem from scratch.

---

## 5. Reframing: What the Double Projection Actually Constrains

### 5.1 The tensor structure of the cancellation

From (3.9), the doubly-projected kernel has the form:

    Omega_{ij}^{(2)} = q_j V_i + q_i V_j

where q = xi x hat{z} is perpendicular to xi. This means:

1. (D_xi S)_{ij} at leading order (when omega(y) = Omega xi in the near-field) has the form of a symmetric tensor with one index necessarily perpendicular to xi.

2. In particular, the xi-xi component vanishes: xi_i xi_j (D_xi S)_{ij} = 0.

3. The nonzero components are the xi-perp and perp-perp components.

Now, D_xi S = (xi . nabla) S appears in the curvature equation through the term:

    2 eta . (D_xi S) xi                                                                (5.1)

where eta = D_xi xi is the curvature vector (perpendicular to xi). This contracts D_xi S with xi on one side and eta (perpendicular to xi) on the other. From the structure (3.9):

    eta_i (D_xi S)_{ij} xi_j = eta_i [q_j V_i + q_i V_j] xi_j
                              = (eta . V)(q . xi) + (eta . q)(V . xi)
                              = 0 + (eta . q)(V . xi)                                   (5.2)

since q . xi = 0. So:

    |eta . (D_xi S) xi| = |eta . q| |V . xi|                                           (5.3)

Now |eta . q| <= |eta| |q| = kappa |q| = kappa sin(phi), and:

    V . xi = (3/(8 pi)) [(5 c^2 - 1) + 0] = (3/(8 pi))(5 cos^2(phi) - 1)             (5.4)

(since hat{n} . xi = 0).

**The angular dependence:** The factor sin(phi)(5 cos^2(phi) - 1) in the integrand introduces a specific angular pattern. However, for the CZ operator, we integrate this over all directions hat{z} with the vorticity distribution, so this angular factor is part of the kernel, not a separate suppression.

### 5.2 What matters for Theorem CB

Theorem CB (from coupled-bootstrap-attempt.md) requires a bound on |D_xi S|, not on specific contractions of it. The cancellation in the xi-xi component (equation 3.11) does NOT reduce |D_xi S| as a tensor norm.

To see this concretely: |D_xi S|^2 = sum_{ij} (D_xi S)_{ij}^2. The cancellation says (D_xi S)_{xi xi} = 0 where subscript xi xi denotes the component along xi in both indices. But the full Frobenius norm |D_xi S| includes all 6 independent components (for a symmetric tensor), and only 1 of the 6 is suppressed by the double projection. The other 5 are not constrained.

More precisely, in an orthonormal frame (xi, e_a, e_b) where e_a, e_b are perpendicular to xi:

    (D_xi S) has components:
    - (D_xi S)_{xi xi} = 0 (cancelled)
    - (D_xi S)_{xi a}, (D_xi S)_{xi b}: nonzero, O(r^{-4}) angular kernel
    - (D_xi S)_{aa}, (D_xi S)_{ab}, (D_xi S)_{bb}: nonzero, O(r^{-4}) angular kernel

The Frobenius norm:

    |D_xi S|^2 = (D_xi S)_{xi a}^2 + (D_xi S)_{xi b}^2 + (D_xi S)_{aa}^2 + (D_xi S)_{ab}^2 + (D_xi S)_{bb}^2

This sum is reduced by the absence of one term compared to the generic case where (D_xi S)_{xi xi}^2 would also appear. The reduction is at most a constant factor (5/6 of the generic value), not a logarithmic improvement.

### 5.3 Could the component cancellation still help?

The term that appears in the curvature evolution is eta . (D_xi S) xi, which we showed (equation 5.3) involves only the components (D_xi S)_{xi,perp}. These components ARE nonzero and have the full CZ magnitude.

However, there is a subtlety: the curvature evolution equation (from coupled-bootstrap-attempt.md, equation (B)) has the source term |D_xi S| in the sense of |2 eta . (D_xi S) xi| <= 2 kappa |D_xi S|. The bound |D_xi S| here is the OPERATOR norm of D_xi S as a bilinear form, not the Frobenius norm. But even the operator norm is not reduced: the (xi, perp) block of D_xi S has the full magnitude.

---

## 6. Verification on the Burgers Vortex

### 6.1 The Burgers vortex

The Burgers vortex has:

    omega = Gamma/(4 pi nu) exp(-s r^2 / (4 nu)) hat{e}_z

where s is the axial strain rate, r is the cylindrical radius, and Gamma is the circulation. The core radius is r_c = (2 nu/s)^{1/2}. The vorticity magnitude is:

    |omega(r)| = Omega exp(-r^2/(2 r_c^2))    where Omega = Gamma/(4 pi nu) = Gamma s / (8 pi nu^2) * r_c^2

(I use a common parameterization; the exact prefactor depends on conventions.)

The vorticity direction is xi = hat{e}_z everywhere (constant).

### 6.2 D_xi S for the straight Burgers vortex

Since xi = hat{e}_z is constant:

    D_xi S = (hat{e}_z . nabla) S = partial_z S

For the Burgers vortex, the flow is:

    u = (-s x/2, -s y/2, s z) + u_theta(r) hat{e}_theta

where u_theta(r) = Gamma/(2 pi r) (1 - exp(-r^2/(2 r_c^2))). The strain tensor S is:

    S = diag(-s/2, -s/2, s) + (symmetric part of nabla(u_theta hat{e}_theta))

Since u_theta depends only on r (not z), the strain S is independent of z. Therefore:

    **D_xi S = partial_z S = 0**                                                        (6.1)

For the *straight* Burgers vortex, D_xi S vanishes identically. This is expected: the flow is z-independent, and xi = hat{e}_z, so the derivative along xi is zero.

### 6.3 D_xi S for a curved Burgers vortex

For a Burgers vortex with axis curvature kappa (and torsion tau), the flow is NOT z-independent. The matched asymptotic expansion (Callegari-Ting 1978) gives corrections of order kappa r_c to the straight-tube profile.

At the tube center (r = 0), the leading contribution to D_xi S comes from the curvature-induced variation of the strain field along the axis:

    D_xi S ~ kappa * (strain from the bent tube profile)

The strain from the bent tube is of order |S| ~ Omega (the vorticity magnitude determines the strain via Biot-Savart). So:

    |D_xi S| ~ kappa Omega                                                              (6.2)

This is |omega|^{1+0} (delta = 0) when kappa is bounded -- dramatically better than the CZ estimate. But as discussed in the three-practical-paths.md analysis (Path 3), this relies on the tube being thin (kappa r_c << 1) and the curvature kappa being bounded.

For the question of this computation (double projection cancellation), the Burgers vortex test is uninformative because D_xi S = 0 for the straight tube. The cancellation is "perfect" but vacuous -- it says nothing about the general case.

### 6.4 What the Burgers test actually tests

The Burgers vortex trivially satisfies D_xi S = 0 because of the axial symmetry, not because of the double projection mechanism. Any axially-symmetric flow with vorticity along the axis has D_xi S = 0. The double projection cancellation (Section 3) is a different phenomenon: it is a cancellation in the angular kernel that occurs for ANY flow where xi is locally constant, not just axially symmetric flows.

To test the double projection mechanism, we need a flow where:
1. xi is approximately constant in a ball of radius rho >> r_c
2. |omega| varies on scale r_c within this ball
3. The flow is NOT axially symmetric (so D_xi S is nonzero from the omega-magnitude variation)

Such a configuration would be: two parallel vortex tubes with the same axis direction (so xi approximately equals hat{e}_z in a large region) but different core positions (so the strain gradient along z is nonzero from the tube-tube interaction). For this configuration, the double projection analysis predicts that the xi-xi component of D_xi S from the interaction vanishes, but the other components do not.

---

## 7. The Fundamental Obstruction

### 7.1 Why the angular cancellation cannot produce a logarithmic gain

The core issue can be stated precisely:

**Theorem (Negative result):** Let T be a Calderon-Zygmund singular integral operator on R^3 with kernel K(z) = |z|^{-(n+1)} Omega(hat{z}) (where n = 3). Let P be any fixed projection that contracts one or more indices of K with a fixed unit vector xi. The projected operator Tf_P(x) = PV integral P[K(x-y)] f(y) dy satisfies the same L^p bounds as T:

    ||Tf_P||_{L^p} <= C_P ||f||_{L^p}

where C_P <= C (the constant of the unprojected operator). The projection can reduce the constant but does not change the operator norm by more than a bounded factor.

**Proof:** The projected kernel P[K] is again a CZ kernel (homogeneous of the same degree, with zero angular mean). The CZ theory gives the same type of L^p bound. The constant depends on the L^2(S^2) norm of the projected angular kernel, which is at most the L^2(S^2) norm of the original.

For our double projection: the projected angular kernel Omega_{ij}^{(2)} has L^2(S^2) norm:

    ||Omega_{ij}^{(2)}||_{L^2(S^2)}^2 = integral_{S^2} |Omega_{ij}^{(2)}(hat{z}, xi)|^2 d sigma

This is a specific fraction of the unprojected norm, but a POSITIVE fraction. It does not vanish (which would require the angular kernel to be identically zero after projection, which it is not -- see (3.8)).

**The angular cancellation from the double projection is a constant-factor improvement, not a logarithmic one.**

### 7.2 Why the near-field cancellation cannot produce a logarithmic gain

The near-field analysis (Section 4) showed that the leading term in the near-field integral vanishes (because the CZ kernel has zero angular mean). The first nonvanishing contribution comes from the variation of omega(y) around the value Omega xi, which is of two types:

1. **Magnitude variation** (|omega(y)| - Omega): this is O(r^2 / r_c^2) near the maximum.
2. **Direction variation** (xi(y) - xi(x_*)): this is O(r |nabla xi|).

The magnitude variation gives a contribution of order Omega rho / r_c^2 (equation 4.3), and the direction variation gives Omega |nabla xi| rho (equation 4.6).

These are EXACTLY the same estimates one would get for ANY CZ singular integral acting on a smooth function -- the near-field is controlled by the variation of the integrand, not by any special property of the kernel projection. The double projection only affects which components of the kernel are active, not the overall magnitude of the near-field integral.

**The near-field cancellation from the CZ mean-zero property is already used in the standard dimensional estimate.** There is no additional cancellation to be extracted.

### 7.3 The deep reason

The fundamental reason the angular cancellation cannot provide a logarithmic gain is:

**The CZ theory is already sharp.** The Calderon-Zygmund bounds for singular integrals are optimal -- there exist functions that saturate the L^p bounds. Projecting the kernel can reduce the norm by a constant factor, but the homogeneity of the kernel (which determines the scaling with respect to the function's magnitude and spatial extent) is unchanged. A logarithmic gain would require the projected kernel to have a DIFFERENT homogeneity or a DIFFERENT regularity property from the original, neither of which is achieved by a finite-rank angular projection.

More concretely: a logarithmic gain in the near-field would require the angular integral of Omega_{ij}^{(2)} against a specific function of hat{z} (determined by the vorticity distribution) to have a higher-order zero. But the vorticity distribution is arbitrary (within the constraints of the NS equations), so no such higher-order zero is guaranteed.

---

## 8. What IS Gained: The Component Constraint

### 8.1 The precise structural result

While the double projection does not reduce the scalar magnitude of D_xi S, it does constrain the tensor structure. The result from Section 3:

**Proposition.** Let omega be a divergence-free vector field in R^3, and let S be the strain determined from omega via Biot-Savart. Let xi = omega/|omega| be the vorticity direction. Then at any point x where omega(x) is nonzero and xi(y) = xi(x) + O(epsilon) for |y - x| < rho:

    xi_i xi_j (D_xi S)_{ij}(x) = O(epsilon) * |D_xi S|(x) + O(rho / r_c^2) * |omega(x)|

In words: the xi-xi component of D_xi S is suppressed relative to the other components, with the suppression controlled by the local alignment error epsilon and the near-field curvature of the vorticity profile.

### 8.2 Relevance to the vorticity dynamics

The quantity xi . S xi = Q (the Rayleigh quotient) controls the stretching rate. Its derivative along xi is:

    D_xi Q = D_xi(xi . S xi) = (D_xi xi) . S xi + xi . (D_xi S) xi + xi . S (D_xi xi)
           = 2 eta . S xi + xi . (D_xi S) xi

The proposition says xi . (D_xi S) xi is suppressed, so:

    D_xi Q approx 2 eta . S xi                                                         (8.1)

This means the along-axis variation of the stretching rate is controlled by the curvature vector eta dotted into S xi, not by the full D_xi S. This is a genuine structural result: the stretching rate Q varies along vortex lines primarily through the geometric coupling of curvature to the strain, not through the direct gradient of strain.

However, this result does NOT close Theorem CB, because Theorem CB requires a bound on |D_xi S| (the full tensor), not just on xi . (D_xi S) xi.

### 8.3 Could a modified Theorem CB use the component constraint?

If we could reformulate the coupled bootstrap to only require a bound on the "dangerous" component eta . (D_xi S) xi (rather than the full |D_xi S|), the double projection would help. From (5.3):

    |eta . (D_xi S) xi| <= |eta| |V . xi| |q|_{avg} ~ kappa * |D_xi S|_{transverse}

This is the same order as kappa |D_xi S|. The suppression is only in the factor of kappa (curvature), which is already present in the standard estimate.

Could we close a bootstrap on kappa using only eta . (D_xi S) xi instead of |D_xi S|? The curvature equation (from coupled-bootstrap-attempt.md) has:

    dK/dt <= C Omega K + 2 |eta . (D_xi S) xi|                                         (8.2)

The source term is 2 |eta . (D_xi S) xi|, which by the above is bounded by 2 kappa |D_xi S|. If |D_xi S| ~ Omega^{3/2}/nu^{1/2} (the dimensional estimate), then:

    dK/dt <= C Omega K + 2 K Omega^{3/2}/nu^{1/2}

This gives dK/dt <= K (C Omega + 2 Omega^{3/2}/nu^{1/2}). This is linear in K, so K grows exponentially (not super-exponentially). But the exponential rate depends on Omega, and if Omega blows up, K blows up at most at the same rate. This is the same structure as the original coupled bootstrap -- the kappa factor in the source term is already accounted for in the standard analysis.

---

## 9. Honest Assessment

### 9.1 Does the cancellation work?

**No, not for the intended purpose.** The double projection (contracting the Biot-Savart kernel with xi on both the differentiation index and the vorticity index) produces:

1. A real angular cancellation: the xi-xi component of the doubly-projected kernel vanishes identically (equation 3.11).
2. A structural constraint on D_xi S: it is a symmetric tensor with zero xi-xi component (at leading order in the alignment parameter).
3. A specific factored form of the kernel (equation 3.9) where one tensor index is necessarily perpendicular to xi.

However, these cancellations produce only a **constant-factor reduction** in the effective CZ norm, not a logarithmic gain. The surviving angular modes (the 5 nonzero components out of 6) have the same homogeneity as the original kernel, and the CZ singular integral with the projected kernel satisfies the same type of L^p bounds.

### 9.2 Where exactly does it fail?

The failure occurs at the transition from Step 2 to Step 3 in the original computation outline:

- Step 2 (angular structure): correctly computed. The doubly-projected angular kernel has a specific form (3.8) with the q-direction factored out.

- Step 3 (extra cancellation): the angular integral of |Omega_{ij}^{(2)}|^2 over S^2 does not vanish. It is a positive fraction of the unprojected integral. The "extra cancellation" is a constant, not a logarithm.

- Step 4 (near-field / far-field): the near-field estimate does NOT gain a log from the double projection. The CZ mean-zero property (which cancels the constant-omega part of the integrand) is already used in the standard CZ estimate. The first nonvanishing correction is from the variation of omega, which has the same scaling for the projected and unprojected kernels.

### 9.3 Is the cancellation only a constant?

**Yes.** The double projection reduces the effective dimensionality of the kernel's angular support (from rank 6 to rank 5 in the symmetric tensor components), but this is a constant-factor improvement. The exact improvement factor depends on the angular distribution of vorticity in the near-field:

- Best case (all vorticity along xi): the cancelled component was the largest, giving a factor of ~2 improvement.
- Worst case (vorticity perpendicular to xi): the cancelled component was zero anyway, giving no improvement.

In no case is the improvement logarithmic.

### 9.4 Does the far-field dominate?

For the near-field / far-field decomposition with the optimal rho (equation 4.10):

    |D_xi S| <= C Omega rho/r_c^2 + C Omega r_c^2/rho^2

The minimum is at rho = r_c^{4/3} giving |D_xi S| ~ Omega^{4/3}/nu^{1/3}. But this estimate is WRONG because it uses the near-field approximation (omega approximately equals Omega xi on B_rho) with a ball of radius rho = r_c^{4/3} >> r_c, where the approximation fails (omega has decayed exponentially). The correct estimate must account for the exponential decay of omega outside the core.

With the corrected near-field (accounting for the Gaussian profile of omega), the near-field contribution from |y - x_*| < rho with rho >> r_c is dominated by the contribution from the core (|y - x_*| ~ r_c), and the standard CZ estimate gives:

    |D_xi S(x_*)| <= C integral |nabla omega(y)| / |x_* - y|^2 dy ~ C (Omega/r_c) / r_c = C Omega / r_c^2

Wait, this is incorrect dimensionally. The correct CZ bound for the operator nabla S = nabla^2 u at a point:

    |nabla^2 u(x_*)| is a CZ-type bound that depends on the specific distribution of omega. For a Gaussian vortex:

    |nabla S(x_*)| ~ Omega / r_c (from the gradient of the Gaussian within the core)

Hmm, let me be precise. S is an operator of order -1 applied to omega (via Biot-Savart + symmetrization), so nabla S is an operator of order 0 (a CZ operator) applied to omega. At a point:

    |nabla S(x_*)| is bounded by the BMO norm of omega times a log, or by the L^infty norm of omega times a CZ constant. More precisely, by the CZ maximal function estimate:

    |nabla S(x_*)| <= C ||omega||_{L^infty}^{1-3/p} ||nabla omega||_{L^p}^{3/p}    for p > 3

For p = infinity: |nabla S| <= C ||nabla omega||_{L^infty} which is C Omega/r_c = C Omega^{3/2}/nu^{1/2}.

This recovers the dimensional estimate. The near-field / far-field decomposition with the double projection does not improve on this, as shown in Section 7.

### 9.5 What is the actual logarithmic factor?

There is no logarithmic factor from the double projection mechanism. The estimate |D_xi S| <= C |omega|^{3/2}/nu^{1/2} remains sharp (up to constants) for the doubly-projected integral, exactly as for the singly-projected one.

### 9.6 Final verdict for Path 1

**The directional cancellation in the Biot-Savart kernel is real but quantitatively insufficient for the NS regularity problem.** It provides:

- A **structural insight**: the most dangerous component of D_xi S (the one that directly drives D_xi Q) is suppressed.
- A **constant-factor improvement**: the effective CZ norm is reduced by a bounded factor.
- **No logarithmic gain**: the scaling |D_xi S| ~ |omega|^{3/2}/nu^{1/2} is not improved.

The reason is fundamental: CZ singular integrals with projected kernels satisfy the same type of bounds as unprojected ones. Angular projections change constants, not exponents. A logarithmic gain requires a structural input that goes beyond the algebraic form of the kernel -- it would require a dynamical input (such as the feedback between D_xi S and omega through the NS evolution) or a geometric input (such as a quantitative tube structure with controlled interactions) that constrains the vorticity distribution in a way that the angular kernel analysis alone cannot capture.

---

## 10. Implications and Redirections

### 10.1 What this computation rules out

Any approach to the logarithmic gain in Theorem CB that relies solely on the angular structure of the Biot-Savart kernel for D_xi S is insufficient. This includes:

- Double projection arguments (xi_k ... xi_l contraction)
- Triple projection arguments (adding more xi contractions does not help further; the kernel is already factored through the q-direction)
- Incompressibility-based angular cancellations (the divergence-free condition is already encoded in the CZ kernel)

### 10.2 What remains viable

The computation does NOT rule out:

1. **Path 2 (Logarithmic Gronwall):** This approach uses the PDE evolution of D_xi S, not the Biot-Savart representation. The parabolic smoothing and the localization to high-vorticity sets could provide a logarithmic gain through the De Giorgi/Brezis-Gallouet mechanism. This is independent of the angular kernel structure.

2. **Path 3 (Hasimoto + LIA):** This approach uses the tube geometry to bound D_xi S directly (equation 6.2: |D_xi S| ~ kappa Omega), bypassing the CZ estimate entirely. The challenge is extending this from the single-tube model to the full NS dynamics.

3. **Hybrid approaches:** Combining the structural result (the xi-xi component of D_xi S is suppressed) with the PDE evolution of the non-suppressed components could yield a more refined bootstrap. Specifically, if the curvature equation only sources from eta . (D_xi S) xi (which involves the suppressed combination), and if the non-suppressed components of D_xi S are independently controlled by the enstrophy dissipation, there might be a path.

### 10.3 The structural result as a building block

The key positive output is equation (8.1):

    D_xi Q approx 2 eta . S xi

This shows that the along-vortex-line variation of the stretching rate is controlled by the curvature vector, not by the full strain gradient. In a bootstrap where kappa is the controlled quantity, this provides a *closed* expression for D_xi Q in terms of already-controlled quantities. The challenge is that Theorem CB requires a bound on D_xi S (the full tensor), not just D_xi Q.

A potential modification: could one formulate a version of Theorem CB that only requires control of D_xi Q (or equivalently, of the rate of change of stretching along vortex lines)? This would be a different conditional regularity theorem, potentially provable with the tools developed here. The question is whether such a condition is sufficient for regularity.

From the coupled bootstrap: the curvature equation involves eta . (D_xi S) xi, not the full |D_xi S|. If we define:

    Phi := xi . (D_xi S) xi = D_xi Q - 2 eta . S xi

Then Phi = 0 (by the double projection cancellation, at leading order). The curvature source term is:

    eta . (D_xi S) xi = (1/2)(D_xi Q - Phi) = (1/2) D_xi Q    (when Phi = 0)

So the curvature equation becomes:

    dK/dt <= C Omega K + kappa |D_xi Q|                                                 (10.1)

And D_xi Q = 2 eta . S xi <= 2 kappa |S| <= 2 C_1 kappa Omega, giving:

    dK/dt <= C Omega K + C_1 kappa^2 Omega = (C + C_1 kappa) Omega K                   (10.2)

This is linear in K with coefficient depending on K itself through the kappa^2 term. The kappa^2 Omega term makes this a Riccati equation in K:

    dK/dt <= C Omega K + C_1 Omega K^2

This can blow up in finite time if Omega grows fast enough. Setting K = 1/w transforms to dw/dt >= -C Omega w - C_1 Omega, which gives w(t) >= w(0) exp(-C integral Omega dt) - C_1 integral Omega ..., and blowup of K occurs when w hits zero. This happens if integral Omega dt diverges, which is exactly the BKM criterion. So the reformulated bootstrap ALSO does not close without an independent bound on integral Omega dt.

**This confirms that the double projection, even when combined with the curvature bootstrap structure, does not close the regularity argument.**

---

## 11. Summary of Computations

| Item | Result | Status |
|------|--------|--------|
| Singly-projected kernel M_{ij,l}(z, xi) | Explicit formula (2.2) | Computed |
| Doubly-projected kernel Omega_{ij}^{(2)} | Factored form (3.8): (q tensor V + V tensor q) with q = xi x hat{z} | Computed |
| xi-xi component of doubly-projected kernel | Vanishes identically: xi . Omega^{(2)} xi = 0 | Confirmed |
| Angular integral of doubly-projected kernel | Vanishes (CZ mean-zero, odd harmonics) | Confirmed |
| Near-field cancellation | Same as standard CZ; no additional log gain | Confirmed |
| Burgers vortex test | D_xi S = 0 for straight tube (trivially, by symmetry) | Verified |
| Net improvement from double projection | Constant factor (component suppression), NOT logarithmic | **Negative result** |

### Bottom line

The logarithmic improvement needed for Theorem CB cannot be obtained from the angular structure of the Biot-Savart kernel alone. The double projection xi_k ... xi_l produces a genuine algebraic cancellation (the xi-xi component of D_xi S vanishes), but this is a rank-1 reduction in a rank-6 symmetric tensor, yielding at most a constant-factor improvement. The CZ singular integral theory is already optimal for kernels of a given homogeneity, and angular projections do not change the homogeneity.

The path to a logarithmic gain, if one exists, must exploit either:
- The **temporal structure** of the NS equations (parabolic smoothing, enstrophy dissipation) -- Path 2
- The **geometric structure** of high-vorticity regions (tube geometry, bounded curvature) -- Path 3
- Some **nonlinear coupling** between the double projection cancellation and the vorticity dynamics that this linear analysis does not capture

The computation is complete. The cancellation mechanism, while algebraically elegant, does not close the gap.
