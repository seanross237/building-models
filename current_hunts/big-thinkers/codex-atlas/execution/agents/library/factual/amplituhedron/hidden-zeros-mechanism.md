---
topic: Hidden zeros — technical mechanism, causal diamonds, and factorization structure
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-005; Arkani-Hamed et al. arXiv:2312.16282 JHEP 10(2024)231"
---

## The ABHY Kinematic Setup

The ABHY framework (arXiv:1711.09102) introduces two types of variables for n-point kinematics:

- **Planar variables** X_{i,j} = (p_i + p_{i+1} + ... + p_{j-1})² — correspond to diagonals of an n-gon
- **Non-planar variables** c_{i,j} = −2p_i · p_j — the actual Mandelstam invariants for non-adjacent particles

The c_{i,j} are related to planar variables by a "lattice Laplacian" on the kinematic mesh:

```
c_{i,j} = X_{i,j} + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j}
```

The n-point **kinematic mesh** is an (n-1)×(n-1) grid of kinematic variables X_{i,j}. The
associahedron lives where all X_{i,j} > 0 and all c_{i,j} ≥ 0. Physical amplitudes are the
canonical form on this associahedron — the unique form with simple poles only on boundaries.

## Definition of Hidden Zeros

**Hidden zeros theorem** (proved for Tr(φ³) in arXiv:2312.16282):

> Choose any **causal diamond** in the kinematic mesh: pick a point X_B (bottom) and follow the
> two lightlike rays up from X_B, bouncing off the mesh boundaries, until they meet at X_T (top).
> Set all c_{i,j} variables INSIDE this causal diamond to zero. The n-point tree-level Tr(φ³)
> amplitude **vanishes exactly**.

This is "hidden" because individual Feynman diagrams contribute nonzero at this locus — the
cancellation requires summing all diagrams and is invisible diagram-by-diagram. The associahedron
makes it manifest: the zero locus corresponds to the associahedron degenerating to a lower-dimensional
polytope at a specific boundary.

## Explicit 5-Point Example

The 5-point amplitude:
```
A_5 = 1/(X_{1,3}X_{1,4}) + 1/(X_{2,4}X_{2,5}) + 1/(X_{1,3}X_{3,5})
    + 1/(X_{1,4}X_{2,4}) + 1/(X_{2,5}X_{3,5})
```

**Hidden zero:** Set c_{1,3} = 0 AND c_{1,4} = 0. These form a causal diamond in the 5-point
mesh. Result: A_5 = 0 exactly (verified by summing the five fractions — each nonzero, total zero).

## Factorization Near Zeros

When approaching the zero locus with one c_{i,j} small but nonzero:

**General factorization formula (eq. 3.8 of arXiv:2312.16282):**
```
A_n(c_* ≠ 0) = (1/X_B + 1/X_T) × A^{down} × A^{up}
```

where A^{down} and A^{up} are lower-point amplitudes with momenta determined by the mesh geometry.

This is a **new type of factorization** — NOT the usual factorization on a physical pole (which
gives 1/p² × A_L × A_R). No classical-field-theory counterpart. The "telescope" decomposition of
the canonical form at the boundary of the associahedron.

**5-point example:**
```
A_5 → (1/X_{1,3} + 1/X_{2,5}) × (1/X_{1,4} + 1/X_{3,5})
```
when only c_{1,4} → 0 with c_{1,3} finite. Both factors are sub-amplitudes from the lower level.

## Geometric Origin

Causal diamonds correspond to specific 2D sublattices of the kinematic mesh. Setting all c_{i,j}
in a diamond to zero forces the amplitude to live on a specific boundary of the ABHY associahedron
where the polytope degenerates. The factorization near zeros is the canonical form's "telescope"
decomposition at the boundary — the canonical form separates into a product of lower-dimensional
canonical forms. This geometric explanation is the only known explanation of why the zeros exist
at all.

The authors of arXiv:2312.16282 note: "a clear interpretation of our zeros in familiar physical
terms is still lacking." The zeros are NOT related to momentum going on-shell (poles), not standard
soft limits, not any symmetry of the Lagrangian. They are visible only from the geometry.

## Relationship to the Adler Zero

For the Non-Linear Sigma Model (pions), the hidden zeros are a strict generalization of the
standard Adler zero. The Adler zero: A → 0 when any single external momentum p_i → 0. The NLSM
hidden zeros require a full causal diamond of c_{i,j} to vanish — a different and more constraining
condition. The Adler zero follows as a special case (soft limit = specific sub-case of diamond
conditions), but the general hidden zero is stronger.

## Why "Hidden"?

1. Not visible from individual Feynman diagrams (each nonzero)
2. Not predicted by any Lagrangian symmetry
3. Not related to known on-shell conditions
4. Not derivable from soft theorems
5. Only visible from the geometry of kinematic space (associahedron)

The word "hidden" is precise: these zeros are structural consequences of positive geometry that
Lagrangian quantum field theory is blind to.
