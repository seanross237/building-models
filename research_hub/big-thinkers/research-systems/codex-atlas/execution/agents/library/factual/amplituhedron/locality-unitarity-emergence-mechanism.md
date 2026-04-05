---
topic: Locality and unitarity emergence from amplituhedron geometry
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-004; Arkani-Hamed & Trnka arXiv:1312.2007 JHEP 2014; Arkani-Hamed & Trnka arXiv:1906.10700 JHEP 2020; Arkani-Hamed, Thomas, Trnka arXiv:1704.05069 JHEP 2018; Arkani-Hamed, Hodges, Trnka arXiv:1408.3410 JHEP 2015; Damgaard et al. arXiv:1905.04216 JHEP 2019; Huang, Shi, Zhang arXiv:2303.03035 JHEP 2023"
---

## The Central Mechanism

**Locality** and **unitarity** emerge from the amplituhedron's geometry via a single principle: the canonical form Ω_{n,k,L} has logarithmic singularities *only* on the boundaries of the amplituhedron, and these boundaries are exactly the physical singularities.

### Locality

Physical poles ↔ codimension-1 boundaries of the amplituhedron.

The amplituhedron A_{n,k,L} is defined as the image of the positive Grassmannian G₊(k,n) under a map determined by external data Z_i ∈ M_{+}(k+4, n). The canonical form is the unique differential form with logarithmic singularities on *all* boundaries and no poles elsewhere.

The "extended positivity" condition (all relevant minors positive) automatically eliminates non-physical boundaries. A codimension-1 surface separates "legal" (physical) singularities from "illegal" (non-local, non-physical) ones. The amplituhedron lies entirely on the legal side — its boundaries are exactly physical propagator singularities.

**Concrete 4-point example** (A_{4,2,0}): The canonical form is:
```
Ω = ⟨Yd²Y⟩ / (⟨YZ₁Z₂⟩⟨YZ₂Z₃⟩⟨YZ₃Z₄⟩⟨YZ₄Z₁⟩)
```
Poles at ⟨YZ₁Z₂⟩ = 0 (s₁₂ channel), ⟨YZ₂Z₃⟩ = 0 (s₂₃ channel), etc. — all adjacent, all physical. Residues at ⟨YZ₁Z₂⟩ = 0 factorize as (3-point) × (3-point) — unitarity at the boundary. The non-adjacent channel ⟨YZ₁Z₃⟩ = 0 never appears because cyclic positivity prevents it.

**Momentum amplituhedron** (Damgaard-Ferro-Lukowski-Parisi, JHEP 2019): Boundaries classified explicitly as collinear limits, soft limits, and multiparticle factorization channels — adjacent only. No boundaries at non-adjacent channels.

**Landau singularities**: The positivity constraints systematically reduce potential Landau singularities at two loops from O(n⁴) to O(n³), providing structural understanding that Feynman methods make laborious (Arkani-Hamed, Langer, Yelleshpur Srikant, Trnka, arXiv:1612.02708, JHEP 2017).

### Unitarity

Unitarity = boundary factorization. Proved rigorously for all n, L, k by Arkani-Hamed & Trnka (arXiv:1906.10700, JHEP 01(2020)069).

The optical theorem (Im(A) = Σ_cuts ∫ A_L × A_R) becomes:
- **Discontinuity across branch cut** = residue of canonical form on a codimension-1 boundary
- **Factorization** = that boundary decomposes as a product of "left amplituhedron" × "right amplituhedron"

This factorization is **not assumed** — it follows from the positivity conditions. When external data is restricted to a codimension-1 boundary (loop momentum put on-shell), the geometry factorizes into two independent positive regions — one for each side of the cut.

For MHV (k=0) the proof is complete and explicit. For higher-MHV sectors, the proof requires defining L/R amplituhedra for NkMHV data, which the authors provide and prove.

**ABJM extension** (Huang, Shi, Zhang, arXiv:2303.03035, JHEP 2023): Emergent unitarity proved for ABJM theory at all loops, four points. Vanishing of cuts involving odd-point amplitudes follows from the "bipartite" geometry — not assumed, forced by the structure.

### Binary Code Perspective (Sign Flips)

The cleanest formulation (Arkani-Hamed, Thomas, Trnka, arXiv:1704.05069, JHEP 2018):

The amplituhedron A_{n,k} is characterized by sign-flip count: for any reference direction, projections of external data undergo exactly 2k sign flips as you traverse cyclic order. This uniquely characterizes the physical region.

- **Locality as consequence**: A non-physical pole would correspond to a zero of the canonical form in a sign-flip direction not corresponding to a face of the maximal-sign-flip region — automatically absent because it would reduce the sign-flip count below 2k.
- **Unitarity as consequence**: Boundaries of the sign-flip region have a product structure (left-part sign-flips + right-part sign-flips add independently). The authors state explicitly: "The locality and unitarity of scattering amplitudes are easily derived as elementary consequences of this binary code."

## Planarity as Derived Property

Cyclic positivity (the amplituhedron's definition) → planarity → adjacent-only factorization channels. These three are equivalent. Per Arkani-Hamed & Trnka (1312.2007 §7): "Planarity (the restriction to planar / color-ordered amplitudes) is itself a *derived* property from the amplituhedron, not an input assumption."

Note: The prerequisites entry (positive-geometry-prerequisites.md) correctly treats planarity as a *prerequisite* for the amplituhedron's existence — both are simultaneously true from different vantage points.

## Deformed Amplituhedron: Relaxing Positivity

Replacing G₊(k,n) with G(k,n) (dropping positivity) generates a "deformed amplituhedron" whose canonical form gains poles at non-physical singularities — locations where minors change sign. These become boundaries of the relaxed region but NOT of the physical amplituhedron. This demonstrates that positivity is precisely the condition screening out non-local singularities.

The deformed amplituhedron (Arkani-Hamed, Hodges, Trnka, arXiv:1408.3410 §10) has outstandingly simple topological properties but does NOT compute physical amplitudes.

## UV Finiteness Connection

The amplituhedron is a bounded region in projective space (momentum-twistor space is projective). It has **no UV boundaries** (boundaries at loop momentum → ∞). UV divergences would appear as poles at such UV boundaries — but none exist. Therefore, any theory admitting a full amplituhedron formulation must be UV-finite. This geometrically selects exactly N=4 SYM and ABJM. See also: positive-geometry-tier-structure.md (UV finiteness wall).
