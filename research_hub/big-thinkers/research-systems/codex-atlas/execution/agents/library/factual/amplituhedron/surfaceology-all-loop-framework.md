---
topic: Surfaceology — all-loop scattering from moduli spaces of decorated surfaces
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-005; arXiv:2309.15913 (Arkani-Hamed et al. 2023); arXiv:2412.21027 (Arkani-Hamed, Frost, Salvatori 2024); arXiv:2408.11891 (Arkani-Hamed et al. 2024)"
---

## What Is Surfaceology?

**Surfaceology = scattering amplitudes from integrals over moduli spaces of surfaces decorated
with kinematic data.**

The surfaceology program (arXiv:2309.15913, "All Loop Scattering As A Counting Problem") is the
overarching framework in which both the hidden zeros program and the ABHY associahedron live.

Key elements:
- **Curves on surfaces**: Physical amplitudes correspond to specific curves drawn on oriented
  surfaces
- **Counting problem**: For Tr(φ³) at all loops, the integrated amplitude equals a sum over
  ways to fill a polygon with curves satisfying combinatorial rules — a literal counting problem
  with no Feynman diagrams involved
- **All-loop**: The framework handles all genera simultaneously via generating functions
- **Surface functions**: The fundamental objects, F(surface), generate amplitudes when integrated

## The Counting Problem Structure

For Tr(φ³) n-point L-loop amplitude:
- Represent the n external particles as marked points on a polygon boundary
- The amplitude = sum over all ways to draw L non-crossing curves inside the polygon satisfying
  specific combinatorial rules (connected, weighted by the kinematic variables X_{i,j})
- At tree level: genus-0 surface → sum over triangulations → ABHY associahedron canonical form
- At loop level: higher genus → new combinatorial objects

## The Cut Equation (arXiv:2412.21027)

A universal **recursion relation** for surface functions:

```
F(surface) = Σ_{cuts} F(left piece) × F(right piece)
```

The "Cut Equation" generates planar integrands at all loop orders for colored theories from
lower-order surface functions. This provides a complete, Feynman-diagram-free definition of the
integrand at any loop order.

## Surface Kinematics for Loop Integrands (arXiv:2408.11891)

For loop integrands (as opposed to integrated amplitudes), the surface kinematics framework
introduces:
- **Punctured disk**: The surface with a boundary representing loop momentum
- **Y^± variables**: Loop-momentum analogs attached to external legs (two parities ± per leg)
- **Surface integrands**: Canonical forms on these generalized kinematic spaces
- These replace standard loop momenta ℓ^μ with a more geometric, basis-independent description

**Canonical Yang-Mills integrand**: arXiv:2408.11891 constructs the first canonical 1-loop
n-gluon integrand in non-SUSY YM theory with well-defined single-loop cuts at all multiplicities.
This solves the long-standing gauge ambiguity problem for loop-level YM amplitudes.

## Relationship to the Amplituhedron

| Feature | Amplituhedron | Surfaceology / Hidden Zeros |
|---------|--------------|----------------------------|
| Theory | N=4 SYM only | Tr(φ³), NLSM, YM (non-SUSY) |
| Space | Auxiliary twistor space | Kinematic space directly |
| Loops | All loops (in principle) | All loops (Cut Equation) |
| Status | Complete for N=4 SYM | Developing; loop-level conjectural |
| Approach | Positive geometry in G(k,n) | Canonical forms on surface moduli |

They are NOT competitors — they address different theories. Surfaceology generalizes the ABHY
approach, which was the precursor to the amplituhedron program. The amplituhedron is the "Tier 1"
full positive geometry for N=4 SYM; surfaceology is the broader framework for non-SUSY theories.

## Geometric Home of Hidden Zeros

Hidden zeros are a **feature of the surface integral approach**: they emerge naturally because
the canonical form on the surface has specific vanishing properties at its boundaries.

- **Tree-level zeros** (causal diamonds) = specific degeneration limits of the polygon
- **Loop-level zeros** (big mountains) = specific degeneration limits of the punctured disk

The surfaceology framework is the geometric HOME of hidden zeros; the zeros encode what happens
when the surface reaches its boundary structure.

## Why Surfaceology Matters

1. **Theory-agnostic**: Works for any colored theory expressible via CHY/planar Mandelstam invariants
2. **All-loop**: Formal framework covers all genera; not restricted to UV-finite theories
3. **No Feynman diagrams**: The counting problem and cut equation bypass diagrams entirely
4. **Unifies tree and loop**: The same surface framework handles both regimes
5. **Applicable to non-SUSY**: Yang-Mills, pions, bi-adjoint scalars — without Yangian symmetry

## Current Limitations

- The all-loop counting theorem is fully proved only for Tr(φ³)
- YM and NLSM at loop level require additional structure (scaffold, surface kinematics)
- Surface kinematics ≠ standard momentum space — translation is "likely non-trivial"
- Multi-loop results are formal (generating functions) rather than explicit computed integrands
- Gravity not covered (double-copy structure present but not yet in surfaceology language)
