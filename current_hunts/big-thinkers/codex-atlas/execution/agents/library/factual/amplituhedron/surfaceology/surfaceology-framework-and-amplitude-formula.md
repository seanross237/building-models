---
topic: Surfaceology — framework definition and amplitude formula
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-007; arXiv:2309.15913, arXiv:2311.09284"
---

## Finding

"Surfaceology" is a program (founded arXiv:2309.15913, Sep 2023; Arkani-Hamed, Frost, Salvatori, Plamondon, Thomas) that reformulates QFT scattering amplitudes as integrals over — or counting problems on — **combinatorial surfaces** (fatgraphs/ribbon graphs). The foundational claim: colored scalar theory amplitudes at **all loop orders and all multiplicities** are encoded in a single combinatorial counting problem. This is the first completely non-perturbative-in-topology formula for an entire QFT's perturbative expansion.

## Fundamental Objects

**Fatgraphs (ribbon graphs):** A fatgraph is a graph with a cyclic ordering on the edges at each vertex. With n external lines, E internal edges, L loops:
```
E = n + 3(L − 1)
```
A fatgraph defines a surface (via its Euler characteristic), with genus g.

**Curves and turn matrices:** Each fatgraph has *curves* — paths on the surface encoded via a 2×2 matrix product:
```
M(C) = ∏_{turns along C} M_turn(y_i)
```
Turn matrices:
```
M_L(y) = [[1, 0], [y, y]]   (left turn / "peak")
M_R(y) = [[1, 1], [0, y]]   (right turn / "valley")
```
Curve momentum:
```
P_C^μ = p_start^μ + ∑_{right turns} p_{from left}^μ
```

**Headlight functions (u-variables):** For each curve C:
```
u_C = M(C)₁₂ · M(C)₂₁ / (M(C)₁₁ · M(C)₂₂)    ∈ [0, 1]
```
These satisfy a remarkable constraint: for any curve C and all curves D intersecting it,
```
u_C + ∏_D u_D^{n(C,D)} = 1
```
where n(C,D) is the intersection number. This is the exchange relation of a **cluster algebra** associated with the surface, and positively parametrizes a compactification of **Teichmüller space** (Fock-Goncharov coordinates).

**Schwinger parameters from tropicalization:** Tropicalizing the u-variables:
```
α_C = −Trop(u_C) = Trop(M₁₁) + Trop(M₂₂) − Trop(M₁₂) − Trop(M₂₁)
```
(Trop: replace products with sums, sums with min)

## The Amplitude Formula

The amplitude (pre-loop-integration):
```
A = ∫ d^D ℓ_1 ··· d^D ℓ_L  ∫ [d^E t / MCG]  exp(−∑_C α_C(t) · (P_C² + m²))
```

After Schwinger parametrization and loop integration:
```
A = ∫ [d^E t / MCG]  (π^L / U(α))^{D/2}  exp(F(α)/U(α))
```
where U and F are the standard Symanzik polynomials, but now the Schwinger parameters α_C come directly from the curve structure.

## The First Miracle

Within each *cone* of the g-vector fan, α_C becomes a linear function of the integration variables t. Integrating exp(−S) over a cone yields exactly one Feynman propagator:
```
∫_{cone} d^E t  e^{−S} = ∏_{i=1}^E  1/(P_{C_i}² + m²)
```
**Each cone = exactly one Feynman diagram.** Integrating over all cones = integrating over all fatgraphs = the complete sum over Feynman diagrams — organized by a single geometric construction.

The counting problem inside each fatgraph: computing the partition function (F-polynomial) by a product of 2×2 matrices — the "downhill closure" rule determines valid subsets. This is literally a counting problem over surface structures.

## Non-Planar Extension (arXiv:2311.09284)

For genus-g contributions:
```
E = n + 3L + 2g
```
Non-planar amplitudes arise from fatgraphs on higher-genus surfaces. The mapping class group (MCG) of the surface creates infinite redundancy, resolved by the **Mirzakhani kernel** K(t), which encodes the MCG symmetry directly in the integrand without needing a fundamental domain. All-multiplicity, all-loop, non-planar formulas explicit through 2-loop order.

## Key Mathematical Structures Involved

- **Tropical geometry** — u-variables tropicalize to Schwinger parameters; connects to tropical Grassmannians
- **Cluster algebras** — u-variable equations are cluster exchange relations; the surface is a cluster variety
- **Teichmüller space** — the positive region (all u_C ∈ (0,1)) is a compactification of decorated Teichmüller space
- **Triangulations** — a triangulation of the surface (maximal non-crossing curves) corresponds to a cone in the g-vector fan, i.e., a Feynman diagram
