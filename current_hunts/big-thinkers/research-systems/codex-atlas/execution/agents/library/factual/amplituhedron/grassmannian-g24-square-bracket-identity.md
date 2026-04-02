---
topic: Grassmannian G(2,4) localization and square-bracket/angle-bracket identity
confidence: verified
date: 2026-03-27
source: amplituhedron strategy-001 exploration-001
---

## Finding

The Grassmannian integral G(2,4) for the 4-point MHV amplitude fully localizes to a single residue, and the minors at the solution yield a "square bracket representation" of the amplitude. This representation is algebraically identical to the Parke-Taylor formula for any 4-particle massless kinematics satisfying momentum conservation.

## Setup

The Grassmannian integral for G(k,n) = G(2,4):

```
L_{4,2} = ∫ d^{2×4}C / (vol(GL(2)) × M₁M₂M₃M₄) × δ⁴(C·λ̃) × δ⁴(C⊥·λ)
```

where M_i are consecutive 2×2 minors of C (cyclic Plücker coordinates).

**Gauge fixing**: C = (I₂ | C'). Fixes GL(2), leaves 4 free parameters.

**Delta function localization**: C·Λ̃ = 0 (Λ̃ = 4×2 matrix of λ̃ spinors) gives 4 equations for 4 unknowns. Solution via 2×2 linear algebra:

```
M = [λ̃₃ | λ̃₄]
c_{a,3}, c_{a,4} = −M⁻¹ · λ̃_a  for a = 1, 2
```

**Complementary constraint**: C⊥·Λ = 0 satisfied automatically by momentum conservation (verified to < 10⁻¹⁵).

## Key Result: Minors at Solution [COMPUTED]

At the localization point, the minors expressed in square brackets are:

```
M₁ = 1                    (gauge choice)
M₂ = (23) = [14]/[34]     (verified numerically)
M₃ = (34) = [12]/[34]     (verified numerically)
M₄ = (41) = −[23]/[34]    (verified numerically)
```

Product: M₁M₂M₃M₄ = −[12][14][23]/[34]³

Therefore: **1/(M₁M₂M₃M₄) = −[34]³/([12][14][23])**

## Key Algebraic Identity [COMPUTED]

The square-bracket representation equals the Parke-Taylor angle-bracket formula:

```
−[34]³ / ([12][14][23])  =  ⟨12⟩³ / (⟨23⟩⟨34⟩⟨41⟩)
```

This identity holds for **any** 4-particle massless kinematics satisfying momentum conservation. Verified across **10 kinematic points** to machine precision.

The identity follows from:
- s_{ij} = ⟨ij⟩[ij] (Mandelstam in terms of brackets)
- Schouten identity for both angle and square brackets
- Momentum conservation: s₁₂ = s₃₄, s₁₄ = s₂₃, s+t+u = 0

## Momentum Twistors [COMPUTED]

Momentum twistors Z_i = (λ_i, μ_i) with μ_i = x_i · λ_i via dual coordinates x_{i+1} = x_i − |i⟩[i|.

For COM E=1, θ=π/3:
- Z₁ = (2, 0, 0, 0)
- Z₂ = (0, 2, 0, 0)
- Z₃ = (−1.5, −0.866, 3.0, 1.732)
- Z₄ = (0.866, −1.5, −1.732, 3.0)
- Four-bracket: ⟨1234⟩ = det(Z₁,Z₂,Z₃,Z₄) = 48.0

**⟨1234⟩ ≠ 0 confirms momentum twistors are in general position** — required for the amplituhedron to be well-defined.

## Scaling

| Amplitude class | Number of Grassmannian residues |
|---|---|
| MHV (k=2), any n | 1 (always single residue) |
| NMHV (k=3), general n | E(n−3, k−1) = Eulerian number |
| General (n,k) | Eulerian number E(n−3, k−1) |

For MHV, the Grassmannian computation is O(n) — same as Parke-Taylor.

## Geometric Interpretation

The Grassmannian result makes manifest that the amplitude is the **canonical form of a geometric object** (the amplituhedron), not just an algebraic expression. The amplitude lives naturally in Grassmannian/momentum-twistor space; the spinor-bracket formulas are projections of this geometric data. The square-bracket vs. angle-bracket duality reflects coordinate-system independence of the canonical form.
