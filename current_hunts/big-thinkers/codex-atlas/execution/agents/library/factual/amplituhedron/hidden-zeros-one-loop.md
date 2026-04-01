---
topic: Hidden zeros at one-loop — big mountains, unitarity biconditional, loop-to-tree factorization
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-005; Backus, Rodina arXiv:2503.03805 (PRL 2025)"
---

## Context

Backus and Rodina (Princeton/BIMSA) extend the hidden zeros program from tree-level to one-loop
in Tr(φ³) theory (arXiv:2503.03805, PRL 2025). This is the strongest evidence that the emergence
program extends beyond N=4 SYM and beyond tree level.

**Key obstacle at loop level:** Loop integrands are ambiguous — contact terms and tadpoles create
scheme dependencies. The **surface integrand** technology (arXiv:2408.11891) resolves this by
working on a "punctured momentum disk" where loop momenta live on the boundary.

## One-Loop Kinematic Variables

The one-loop setup extends the kinematic mesh with new variables:
- **Y^±_i**: loop momentum variables attached to external leg i, with two parities ±
- The loop mesh is a "punctured n-gon" where the puncture represents the loop momentum

One-loop versions of c_{i,j} at the diagonal:
```
c_{i,i} = X_{i,i} − Y^−_i − Y^+_i
c_{i+1,i} = X_{i+1,i} − X_{i,i} − X_{i+1,i+1} + Y^−_{i+1} + Y^+_i
```

## Definition: Big Mountain Zeros

One-loop hidden zeros correspond to **maximal triangles ("big mountains")** on the one-loop mesh:

The (i,±)-zero imposes:
```
c_{m,k} = 0, for m ∈ {k, k+1, ..., i-1}, for each k = 1, 2, ..., n
```

At n-points there are **2n big mountain zeros** (n for each parity ±). These replace the
tree-level causal diamond structure. Their existence in the actual loop integrand is proved.

## The Main Theorem: Unitarity ↔ Hidden Zeros

**Theorem (proved, assuming locality):**

> A local one-loop Tr(φ³) surface integrand is **unitary if and only if it satisfies the big
> mountain zeros**.

This biconditional is the central result:
- **Unitarity ⟹ zeros** (Appendix E): The physical integrand satisfies the zeros. Proved.
- **Zeros ⟹ unitarity** (Section 4): Any local integrand satisfying the zeros must be unitary. Proved.

Hidden zeros are a perfect characterization of unitarity (given locality) at one-loop.

## Uniqueness Without Locality or Unitarity

The most ambitious result (Section 4, "Without Assuming Locality"):

Starting from a **generic, non-local, non-unitary ansatz** for the n-point one-loop integrand
(at 4-points: ~6,500 free parameters), imposing the 2n = 8 big mountain zeros:

**Result (numerically verified at 4-points):** The zeros reduce the ansatz to the **unique
physical integrand**. Both locality AND unitarity emerge simultaneously from the zeros.

This shows hidden zeros contain ALL the information needed to fix the amplitude, without
pre-assuming any physical principle. This is the strongest claim — currently **proved only at
4-points numerically** and conjectured for general n.

### The Reduced Ansatz (Assuming Locality)

With locality assumed, the ansatz reduces to:
```
M_n = a^+ I^+_n + a^− I^−_n
```
(2 free parameters). The zeros force a^+ = a^−, uniquely fixing the integrand.

## Loop-to-Tree Factorization

Near an (i,∓)-zero with only c_* ≠ 0:
```
I_n(c_* ≠ 0) = (1/Y^∓_i + 1/Y^±_{i-1}) × A_{n+2}
```

where A_{n+2} is a **tree-level** (n+2)-point amplitude with kinematic variables from the mesh.

This is remarkable: a one-loop integrand near its zeros factorizes onto tree-level objects. The
loop structure collapses to a simpler tree structure at the zero locus.

## NLSM at One-Loop

For the Non-Linear Sigma Model, zeros alone are **not sufficient** to fix the integrand. Instead:

Imposing **factorization near zeros** (the formula above, adapted for NLSM) uniquely fixes the
NLSM one-loop integrand, without assuming locality or unitarity. **Verified at 4-points.**
Conjectured for general n.

## Explicit Integrands (Appendix F of arXiv:2503.03805)

**2-point surface integrand:**
```
I^{Tr(φ³)}_2 = 1/(Y^+_1 Y^+_2) + 1/(Y^+_1 X_{1,1}) + 1/(Y^+_2 X_{2,2}) + (Y^+ ↔ Y^−)
```

**3-point surface integrand:**
```
I^{Tr(φ³)}_3 = [1/(Y^+_1 X_{1,1}) × (1/X_{2,1} + 1/X_{1,3}) + (cyclic)]
             + [1/(Y^+_2 Y^+_3 X_{3,2}) + (cyclic) + 1/(Y^+_1 Y^+_2 Y^+_3)] + (Y^+ ↔ Y^−)
```

## Critical Limitation: Surface Kinematics ≠ Momentum Space

The one-loop zeros are defined in **surface kinematics** (Y^± variables), NOT in standard
momentum-space loop momenta (ℓ^μ). The results are statements about surface integrands, not
standard Feynman integrals.

Whether any analogous structure exists in ordinary Feynman integral language is **explicitly
left open** by the authors as "likely non-trivial." The hidden zeros loop results and the
surfaceology framework are deeply intertwined — nearly inseparable at loop level.

## Status Summary

| Claim | Status |
|-------|--------|
| Big mountain zeros exist in Tr(φ³) and NLSM at 1-loop | **Proved** |
| Unitarity ↔ zeros in Tr(φ³) (local ansatz) | **Proved** |
| Zeros fix Tr(φ³) uniquely (non-local ansatz) | **Conjectured** (4-pt numerical) |
| NLSM uniquely fixed by factorization at 1-loop | **Conjectured** (4-pt numerical) |
| Yang-Mills at 1-loop via zeros | **Not yet treated** |
| Two-loop and beyond | **Open** |
| Loop zeros in standard momentum space | **Unknown** |
