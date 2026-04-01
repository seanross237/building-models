---
topic: Surfaceology — survey of new results 2023–2026
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-007; arXiv:2309.15913, arXiv:2311.09284, arXiv:2403.04826, arXiv:2406.04411, arXiv:2412.21027, arXiv:2504.21676, arXiv:2505.17179, arXiv:2512.17019, arXiv:2503.07707, arXiv:2412.19881, arXiv:2603.03425, arXiv:2602.15102"
---

## Finding

A rapid-growth program produced ~15 confirmed results in roughly 2.5 years (Sep 2023 – Mar 2026). This file surveys the major results beyond the foundational framework and YM integrand (see other files in this folder).

## Result Summary Table

| Result | Paper | Status |
|---|---|---|
| All-loop colored φ³ amplitudes = counting problem | arXiv:2309.15913 | Proved |
| Non-planar φ³ at all loops | arXiv:2311.09284 | Proved (explicit through 2-loop) |
| NLSM = Tr(φ³) with δ-shift | arXiv:2403.04826 | Proved |
| Colored Yukawa all-loop formula | arXiv:2406.04411 | Proved |
| Cut equation for NLSM (all-order recursion) | arXiv:2412.21027 | Proved |
| Cosmohedra for cosmological wavefunctions | arXiv:2412.19881 | Proved (tree-level) |
| Hidden zeros ↔ unitarity (biconditional) | arXiv:2503.03805 | Proved (1-loop, with locality assumption) |
| Superstring amplitudes = bosonic string combinations | arXiv:2504.21676 | Proved (SciPost Physics 2025) |
| Surface soft theorem at 1-loop | arXiv:2505.17179 | Proved (JHEP) |
| Gluon leading singularities from curve covers | arXiv:2512.17019 | Proved |
| Monte Carlo sampling for loop amplitudes | arXiv:2503.07707 | Demonstrated (10-loop φ³) |
| Inverse KLT kernel as surface integrand | arXiv:2602.15102 | Proved (Feb 2026) |
| Combinatorics of cosmohedron; UV divergences | arXiv:2603.03425 | Proved (Mar 2026) |

## Key Selected Results

### Cut Equation (arXiv:2412.21027)

Defines *surface functions* G_S as generating functions for all MCG-inequivalent triangulations. The cut equation:
```
∂_{x_C} G_S = G_{S\C}
```
where S\C is the surface obtained by cutting S along curve C. Single equation generates all-loop planar integrands for colored theories and NLSM to all orders. Computed explicit all-order planar NLSM integrands through 4 loops without spurious poles.

### NLSM δ-Shift (arXiv:2403.04826)

```
A_NLSM = A_{Tr(φ³)} |_{X_{e,e} → X_{e,e}+δ, X_{o,o} → X_{o,o}−δ}
```
The NLSM field U = Φ + i√(1−Φ²) parametrizes the unit circle via the same function generating Catalan numbers (counting triangulations). The Adler zero (soft pion vanishing) is manifest at the **integrand** level via a "surface-soft limit" that geometrically identifies boundary points of the surface polygon.

### Yukawa Fermion Extension (arXiv:2406.04411)

Fermionic numerators repackaged as combinatorial determinants:
```
A^{L-loop} = ∑_{subsets S, |S|=2^L}  det(M_S)  × (scalar amplitude)
```
All-loop, all-genus, all-multiplicity formula for colored Yukawa theory established.

### String Theory Connection

**Surfaceology is "string theory written combinatorially."** The string amplitude formula:
```
A_string = ∫ [d^E t / MCG]  exp(−α' ∑_C X_C · u_C(t))
```
In the limit α'→0, u_C → step function (equals 0 or 1 on triangulation cones), recovering QFT. The fatgraph surface IS the worldsheet — surfaceology provides an algebraic/combinatorial parametrization of string moduli space without ever writing a worldsheet CFT. Superstrings accommodated as gauge-invariant combinations of bosonic string amplitudes (arXiv:2504.21676, SciPost 2025).

### n and L Decoupling (arXiv:2311.09284)

A "surprising fact": higher-loop contributions reduce to tadpole-like amplitudes (single-particle-per-trace) that combine with tree results to generate all-n amplitudes at L loops. The dependence on particle number n and loop order L is effectively decoupled — invisible in Feynman diagrams.

### Cosmological Extension

**Cosmohedra** (Figueiredo et al., arXiv:2412.19881, Dec 2024): new polytopes whose canonical forms compute cosmological wavefunctions in Tr(φ³) theory. Constructed by "blowing up" associahedron faces.

**Combinatorics of the Cosmohedron** (Ardila-Mantilla, Arkani-Hamed, arXiv:2603.03425, Mar 2026): proves cosmohedron faces biject with "Matryoshkas" (nested polygon structures); connects to UV divergences in loop-integrated Feynman amplitudes. Demonstrates surfaceology extends beyond S-matrix observables to cosmological wavefunctions.

### Monte Carlo Sampling (arXiv:2503.07707)

Reformulated the curve integral as a Monte Carlo sampling problem using tropical importance sampling. Computed Tr(φ³) amplitudes up to **10-loop order** in 2D. Sample count grows far slower than the number of Feynman diagrams — demonstrating computational advantages of the surface formulation at high loop order.

### Inverse KLT Kernel (arXiv:2602.15102, Feb 2026)

The inverse KLT kernel (connecting open and closed string amplitudes) has a surface integrand formulation via Berends-Giele-type recursion. Unifies cubic scalars and NLSM to all loop orders via kinematic α'-shifts, extending KLT duality to the loop-integrated level.
