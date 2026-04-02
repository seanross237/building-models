---
topic: Holographic reformulation of the classicality budget — resolves structural catch-22
confidence: verified
date: 2026-03-27
source: classicality-budget strategy-001 exploration-007
---

## Summary

The classicality budget R ≤ S_max/S_T can be derived using the Ryu-Takayanagi (RT) formula
and holographic quantum error correction (HQEC), replacing the problematic bulk tensor product
with the boundary tensor product (always valid). This resolves the **structural component** of
the catch-22 (Exploration 004) for AdS BHs in the semiclassical regime.

---

## The Structural Catch-22 (From E004)

The non-holographic budget derivation requires:
> H_total = H_S ⊗ H_E (Axiom 1 — the bulk tensor product)

But this tensor product fails precisely where the budget gives interesting predictions:
- Near BH horizons: firewall, island formula, entanglement wedge geometry
- At Planck scale: spatial Hilbert space factorization ill-defined

**Catch-22**: Valid domain (ordinary QM) and interesting domain (gravitational physics) don't overlap.

---

## The Holographic Derivation

**Setup**: Let φ(x) be a bulk operator in asymptotically AdS spacetime with dual boundary CFT
of total entropy S_max. Let S_T = log₂(dim H_x) be the information content of φ(x)'s local
degrees of freedom.

**Key ingredients**:
1. **RT formula**: S(R_k) = Area(γ_{R_k})/(4G_N) — entropy of boundary region
2. **HQEC reconstruction condition**: φ(x) can be reconstructed from boundary region R_k iff
   x ∈ W(R_k) (entanglement wedge). This requires dim(H_{R_k}) ≥ 2^{S_T}.
3. **Boundary spatial tensor product**: For disjoint boundary regions R_1,...,R_R:
   H_{R_1} ⊗ ... ⊗ H_{R_R} ⊂ H_CFT  [standard QFT on boundary manifold — always valid]
4. **Total boundary entropy**: dim(H_CFT) ≤ 2^{S_max}

**Derivation**:
```
Step 1: Each R_k can reconstruct φ(x)  →  dim(H_{R_k}) ≥ 2^{S_T}
Step 2: R_k disjoint  →  ∏_k dim(H_{R_k}) ≥ 2^{R·S_T}
Step 3: Product fits in H_CFT  →  2^{R·S_T} ≤ 2^{S_max}
Step 4: R · S_T ≤ S_max  →  R ≤ S_max/S_T   ∎
```

**Holographic Classicality Budget**: **R ≤ S_max/S_T**

(The non-holographic version has −1 term: R ≤ S_max/S_T − 1. In the holographic version, the
bulk operator contributes negligibly to total boundary entropy for S_T << S_max, making the
−1 negligible. Same formula, slightly cleaner.)

---

## Why This Resolves the Catch-22

The critical replacement:

| Non-holographic | Holographic |
|-----------------|-------------|
| H_S ⊗ H_E (bulk tensor product — fails near BHs) | ⊗_k H_{R_k} (BOUNDARY tensor product — always valid) |

The boundary CFT lives on a fixed manifold with no gravity, no topology change, no black holes.
Spatial tensor product decomposition is always valid there. The bulk near-horizon physics
(firewall, island, entanglement wedge transitions) all happen in the BULK, not the boundary.

**For AdS BHs in the semiclassical regime, the budget is now derivationally sound** where the
non-holographic budget was not.

---

## Near-Horizon Redundancy from RT Geometry

In AdS₃/CFT₂, a bulk point at depth z (in AdS units, boundary circle length L = 1) requires
a boundary interval of minimum length l_min = 2z for reconstruction. Maximum independent
fragments that fit on the full boundary:

  R ≤ floor(L/(2z))

| Bulk depth z/L | Max redundancy R |
|----------------|-----------------|
| 0.01 (center)  | 50              |
| 0.10           | 5               |
| 0.30           | 1               |
| ≥ 0.50 (horizon) | 0             |

**R decreases continuously from >>1 at the bulk center to 0 at the horizon.** This is the
holographic version of R_δ ≈ −1 (E005) — same qualitative result, but now from RT surface
geometry rather than Hawking radiation sparseness.

---

## Page-Time Classicality Transition (Conjectured)

The island formula [Almheiri et al. 2019]:
- **Before Page time**: Entanglement wedge of Hawking radiation does NOT include BH interior.
  No boundary region can reconstruct interior facts. R = 0 for all interior operators.
- **After Page time**: An "island" appears inside the BH in the entanglement wedge of collective
  exterior radiation. The interior becomes reconstructable — but only collectively.

**QD interpretation [CONJECTURED]**: The Page time marks the onset of the first "environmental
witness" of interior facts. Before Page time: no QD-classical reality for interior (R = 0).
After Page time: collective verification possible (R_collective ≥ 1). But true redundancy
(R >> 1, many independent fragments each knowing the same fact) remains R ≈ 0 — the interior
just barely enters the entanglement wedge of the full exterior radiation.

---

## Holographic vs. Operational Budget: The Discrepancy

| Version | S_max used | R for solar-mass BH | Derivationally valid near BHs? |
|---------|-----------|--------------------|---------------------------------|
| Non-holo (Bekenstein, E002) | S_BH = 10⁷⁷ bits | 10⁷⁷ | No (bulk tensor product fails) |
| Operational (Hawking, E005) | S_Hawking = 0.003 bits | −0.997 | No (bulk tensor product fails) |
| Holographic (RT, E007) | S_BH = 10⁷⁷ bits | 10⁷⁷ | YES (boundary tensor product valid) |

The holographic budget gives S_max = S_BH (the theoretical maximum across all time), not
S_Hawking (the instantaneous accessible entropy). Using S_max = S_Hawking in the holographic
framework recovers the near-zero operational result. The two frameworks are consistent.

---

## Validity Conditions and Limits

**The holographic budget IS valid when**:
- Spacetime is asymptotically AdS (conformal boundary exists)
- Bulk described by semiclassical gravity (large N, weak G_N)
- S_T << S_max (light operator)

**The holographic budget is NOT valid for**:
- **De Sitter space** (positive Λ, our universe): no established holographic duality
- **Planck-scale physics**: RT formula receives O(1) quantum corrections; budget remains formally
  inaccessible at sub-Planck scales
- **Generic non-AdS spacetimes**: no boundary to define fragments

---

## Status of the Two Catch-22 Components

| Component | Status |
|-----------|--------|
| Structural: derivation uses bulk tensor product | **RESOLVED** — uses boundary tensor product |
| Regime: budget tight at sub-Planck scale | NOT resolved — Planck scale inaccessible to both derivations |
| Near-BH derivational validity | **RESOLVED** for AdS, semiclassical |
| Applicability to our universe (de Sitter) | MIXED — holographic framework uncertain |
