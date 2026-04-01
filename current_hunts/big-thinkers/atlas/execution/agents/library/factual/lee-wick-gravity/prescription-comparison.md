---
topic: lee-wick-gravity/prescriptions
confidence: verified
date: 2026-03-24
source: exploration-003-lee-wick-qg-assessment (strategy-002)
---

# Four Prescriptions for Complex Poles in Quantum Gravity

## Context

When a gravitational propagator has complex poles (as in Lee-Wick quantum gravity), how those poles are handled in loop integrals is a choice — the **prescription**. Different prescriptions give physically inequivalent theories with different S-matrices. The definitive comparison was published by Anselmi, Briscese, Calcagni & Modesto (arXiv:2503.01841, JHEP05(2025)145) — co-authored by both the fakeon creator AND the LW QG creator.

## The Four Prescriptions

| Prescription | Lorentz Inv. | Optical Theorem | Power-Counting | Analyticity |
|---|---|---|---|---|
| By-the-book (Wick rotation) | ✓ | ✗ | ✓ | ✓ |
| Lee-Wick-Nakanishi (LWN/CLOP) | **✗** | ✓ | Patch-wise | ✗ |
| **Fakeon/AP** | **✓** | **✓** | **✓** | ✗ |
| Direct Minkowski | ✓ | ✗ | ✗ | ✓ |

**Only the fakeon/AP prescription satisfies both Lorentz invariance and the optical theorem (unitarity).**

## By-the-Book (Wick Rotation)

Standard Wick rotation from Euclidean space. Preserves Lorentz invariance and analyticity, but fails the optical theorem — ghost poles contribute to the absorptive part, violating unitarity. Also preserves standard power counting for renormalization.

## LWN/CLOP (Lee-Wick-Nakanishi)

The original Lee-Wick prescription, formalized by Cutkosky, Landshoff, Olive & Polkinghorne (CLOP). Loop energy is integrated along a complex contour that avoids the ghost poles, while spatial momenta remain real.

**Fatal flaw — Lorentz invariance violation:** Under a Lorentz boost, spatial momentum components acquire imaginary parts, but the CLOP prescription constrains spatial momenta to ℝ^(D-1). This incompatibility was first noticed by **Nakanishi in 1971** and confirmed in the 2025 paper. The violation is not a small correction — it's a fundamental inconsistency at the quantum level.

Additional problems:
- Power counting works only "patch-wise" (region by region), not globally
- Analyticity properties are non-standard
- Renormalization requires ad hoc region-by-region treatment

## Fakeon/AP (Average Continuation)

Anselmi-Piva prescription. Fixes the CLOP problem via **domain deformation**: both energy AND spatial momenta integrate on complex paths, preserving Lorentz covariance. The key formula:

    ℳ_AP(p²) = ½[ℳ(p² − iε) + ℳ(p² + iε)]

This "average continuation" removes ghosts from ALL states (internal and external) — they become **purely virtual** (fakeons). The prescription:
- Preserves Lorentz invariance (by construction, domain deformation is covariant)
- Satisfies the optical theorem (proven to all orders by Anselmi & Piva 2018)
- Maintains standard power counting (global, not patch-wise)
- Sacrifices standard analyticity (the average is not analytic across the ghost threshold)

## Direct Minkowski

Computes loop integrals directly in Minkowski space without Wick rotation. Preserves Lorentz invariance and analyticity but fails both the optical theorem and standard power counting. The least useful prescription.

## Why the Prescription Matters for Gravity

The action of Lee-Wick QG and QG+F can be the SAME (for the four-derivative case). The prescription is what makes them different physical theories:
- Same action + CLOP prescription = Lee-Wick QG → **not viable** (Lorentz violation + unitarity failure)
- Same action + fakeon prescription = QG+F → **viable**

The prescription determines the S-matrix, the physical spectrum, and whether the theory is consistent. It is not a technical detail — it is the defining physical choice.

Sources: Anselmi, Briscese, Calcagni & Modesto (arXiv:2503.01841, JHEP05(2025)145); Anselmi & Piva (arXiv:1703.04584); Nakanishi (1971)
