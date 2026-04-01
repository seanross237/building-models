---
topic: BCFW cyclic color-ordering failures at 6-point NMHV
confidence: provisional
date: 2026-03-27
source: amplituhedron strategy-001 exploration-002
---

## Finding

Two independent BCFW implementations of A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) — using the [1,2⟩ shift and the [2,4⟩ shift — disagree by ~93%, indicating bugs in cyclic color ordering or helicity assignments.

---

## The Disagreement

| Shift | Total amplitude (seed=42) |
|-------|--------------------------|
| [1,2⟩ | −8029.9 − 3626.0i |
| [2,4⟩ | −542.6 − 259.3i |
| Ratio − 1 | ≈ 0.93 (93% relative disagreement) |

The [1,2⟩ result breaks down as: Ch1 = −24.8−14.8i, Ch2 = −8005.1−3611.2i, Ch3 = 0 (structural zero).
The [2,4⟩ result breaks down as: Ch3 = −772.9−262.9i, Ch4 = +230.3+3.6i.

These are fundamentally incompatible — a correct BCFW recursion must give the same amplitude independent of shift choice.

---

## Diagnosed Sources of Error

**1. Cyclic color ordering of sub-amplitudes (most likely)**
The Parke-Taylor formula is cyclic-order-sensitive. The color ordering of the internal particle K and −K must match the original color-ordered amplitude. An incorrect traversal direction (e.g., K→5→6→1̂→K instead of K→1̂→6→5→K) changes the denominator product ⟨12⟩⟨23⟩...⟨n1⟩.

**2. Helicity assignment of internal particle K (likely at multi-particle poles)**
At multi-particle poles (not just 2-particle poles), both K⁺ and K⁻ can give non-zero sub-amplitudes. The wrong helicity assignment produces incorrect values.

**3. Overall sign conventions**
Bracket antisymmetry (⟨41⟩ = −⟨14⟩) can introduce overall signs when the cyclic ordering is traversed in either direction. Already encountered at 4-point (see bcfw-recursion-sign-detail.md).

---

## Complexity Jump: 6-pt NMHV vs 4-pt MHV

| Feature | 4-pt MHV | 6-pt NMHV |
|---------|----------|-----------|
| BCFW channels | 1 | 3 (1 trivially zero) |
| Sub-amplitude types | A₃^MHV × A₃^MHV | A₃^aMHV × A₅^aMHV, A₄^MHV × A₄^MHV |
| Helicity labels tracked | 2 | 6 + internal K |
| Cyclic ordering errors possible | No (only 1 configuration) | Yes (multiple orderings per channel) |
| Independent verifications | 3 methods agree | 2 BCFW shifts DISAGREE |

At 4-point, there is essentially one cyclic ordering for each sub-amplitude because the particle count is minimal. At 6-point, each 4- or 5-particle sub-amplitude has multiple valid cyclic orderings and the correct one must be derived from the original color ordering by tracking which particles go to which side of the cut.

---

## Path to Resolution

The correct procedure:
1. Implement the R-invariant / momentum twistor 5-bracket formula for A₆^NMHV as the independent ground truth.
2. Verify one BCFW shift against this ground truth.
3. Then compare the Grassmannian G(3,6) residue computation against the verified BCFW.

Two BCFW shifts cannot cross-validate each other — they share the same underlying difficulty (cyclic ordering conventions), so errors can be consistent across both implementations while still being wrong.

---

## Note on Pole Signs

The numerical pole formula `z* = −P²(0) / (2 P(0)·q)` gives a sign that may differ from naive analytic expressions like z₃* = [23]/[13]. The discrepancy comes from sign conventions in computing s₂₃ = ⟨23⟩[23] and 2P·q = ⟨24⟩[23]. The numerical formula is correct; analytic formula signs require careful convention tracking.

**Status: [CONJECTURED]** — the cyclic ordering diagnosis is conjectured; the disagreement itself is verified.
