---
topic: CNS master loop approach — optimized ceiling β₀(4) = 1/87, curvature structurally absent
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-002 exploration-003, exploration-004; Cao-Nissim-Sheffield arXiv:2505.16585 (May 2025); SZZ arXiv:2204.12737 (2023)"
---

## Overview

Deep analysis of the CNS May 2025 master loop paper (arXiv:2505.16585), Proposition 3.23. The optimized ceiling of the master loop approach is β₀(4) = 1/(32e) ≈ 1/87 — a factor of 4e/3 ≈ 3.6× below the Bakry-Émery threshold of 1/24. Crucially, the two approaches are **parallel, not hierarchically related**: curvature is structurally absent from the master loop proof.

---

## Master Loop Mechanics Summary

The proof reduces to a **contraction estimate** for the master loop operator G acting on Wilson string expectations:
```
‖Gf‖_{λ,γ,ρ} ≤ (2dBλ + 2dB/(λN²) + 4dβγ/(λρN)) · ‖f‖
```
Three sub-estimates (Lemma 3.20):
- **(3.4) Splitting term:** ≤ 2dBλ · ‖f‖
- **(3.5) Merger term:** ≤ 2dB/(λN²) · ‖f‖
- **(3.6) Deformation term:** ≤ 4dβγ/(λρN) · ‖f‖

Contraction requires the sum ≤ 1/2. The proof uses norm parameters λ, γ, ρ.

---

## Optimized Parameter Analysis [DERIVED]

### λ = 1/N is Already Optimal

Minimizing the splitting + merger sum over λ:
```
d/dλ [2dBλ + 2dB/(λN²)] = 0  ⟹  λ* = 1/N
```
The paper's choice λ = 1/N is provably optimal. No improvement possible.

### ρ = 1/e is Required (Not Just Conservative)

The boundary term in Proposition 3.24 requires ρ = e⁻¹ specifically:
```
sup_{K≤B} e^{-(B-K)} |φ(∅,K)| ≤ Z_{Λ,β,N,B}
```
The choice ρ = 1/e is a **proof requirement**, not a conservative choice.

### γ = 1 is the Optimal Achievable Choice

The norm requires γ ≥ 1. Setting γ = 1 (minimum), the deformation term (3.6) gives:
```
4dβ·1/(λ·ρ·N) = 4dβ·1/((1/N)·(1/e)·N) = 4dβe
```
Contraction requires 4dβe ≤ 1/2:
```
β ≤ 1/(8de) = 1/(32e) ≈ 0.01150 ≈ 1/87   [d=4]
```
The paper's original conservative choice (γ = (10³dβ)⁻¹, requiring γ ≥ 1 → β ≤ 1/(10³d) = 1/4000) used a much more conservative γ.

---

## Threshold Table for CNS May 2025 [d=4]

| Source | Formula | β₀(4) | Notes |
|--------|---------|--------|-------|
| Proof (eq. 2.2, conservative) | 10^{-10d}/d | ~2.5×10⁻⁴¹ | "Somewhat arbitrary" constants |
| Structural (Theorem 3.2, γ≥1) | 1/(10³d) | 1/4000 | Truncated model structural threshold |
| Theorem 4.1 formula | ~1/(2×10^6 d²) | ~3×10⁻⁸ | From explicit α prefactor |
| **Optimized (γ=1, λ=1/N, ρ=1/e)** | **1/(8de)** | **1/(32e) ≈ 1/87** | **[DERIVED: Prop 3.23]** |
| CNS Sept 2025 (Bakry-Émery) | 1/(8(d-1)) | 1/24 | Best known threshold |

**Hard ceiling:** β₀(4) = 1/(32e) ≈ 1/87 cannot be improved without changing the proof structure.

---

## Gap Analysis

```
Gap = (1/24) / (1/(32e)) = 32e/24 = 4e/3 ≈ 3.624
```

The gap factor is exactly **4e/3** [COMPUTED]. This is the factor by which the effective contraction constant must change to close the gap — it is not a simple integer ratio.

---

## Critical Correction: Remark 1.4 is About Signed Cancellations, NOT Curvature

**[VERIFIED from paper text]**

The goal description and some library entries previously described Remark 1.4 as involving "curvature input" to the master loop. **This is incorrect.**

The actual Remark 1.4 asks about extending to **β ~ c_d N** (the large-N regime studied by the Sept 2025 CNS dynamical paper). It identifies that the key obstacle is in the **merger term** (3.5): the bound uses the unsigned count |M±| ≤ 2dB. If positive and negative surface contributions cancel (signed cancellations), the effective B factor could be reduced, allowing larger β.

**The proposed extension requires exploiting signed cancellations in the merger term — not curvature.**

Note that at β ~ c_d N, this signed-cancellation approach would still be needed BEYOND the deformation term constraint (the deformation term already binds at β = 1/87). So Remark 1.4's route requires a fundamentally different norm structure.

---

## Curvature is Structurally Absent from the Master Loop Proof

The Ricci curvature κ = N/2 of U(N)/SU(N) is **irrelevant** to the master loop contraction:
- The proof uses only: (1) algebraic identities for loop equations, (2) combinatorial bounds on loop operations, (3) the truncated partition function bound
- No Riemannian geometry of the group manifold enters anywhere
- The curvature κ does NOT appear in Lemma 3.20, Proposition 3.23, or Proposition 3.24

**Quantitative impossibility of curvature enhancement** [COMPUTED]:

| N | κ = N/2 | δ_norm needed to reach 1/24 | Feasibility |
|---|---------|---------------------------|-------------|
| 2 (SU(2)) | 1.0 | 2.624 | Impossible (> 1) |
| 3 (SU(3)) | 1.5 | 1.750 | Impossible (> 1) |
| 10 | 5.0 | 0.525 | Barely possible |

For SU(2) and SU(3) (the physically relevant cases), curvature input to master loop cannot bridge the gap to 1/24.

---

## Structural Picture: Two Parallel Approaches

| Feature | Master Loop (CNS May 2025) | Bakry-Émery (CNS Sept 2025) |
|---------|---------------------------|------------------------------|
| Threshold d=4 | ~1/87 (optimized) | 1/24 |
| String tension constant | **N-independent** | Decays with N |
| Proof structure | Algebraic/combinatorial | Riemannian geometry |
| Curvature used? | No | Yes (κ = N/2) |
| Extension to β ~ c_d N | Via signed cancellations (open) | Not needed (already at 1/24) |

**The gap (factor 4e/3) is the "free lunch" from positive curvature that Bakry-Émery exploits.**

---

## Route to β ~ c_d N (per Remark 1.4)

For the master loop to match Bakry-Émery's β range, the authors describe the path as:
- Exploit signed cancellations in the merger term to reduce the effective 2dB factor
- This requires a new norm incorporating signed surface weights (not just absolute weights)
- A fundamentally different proof structure — not just parameter tuning

This is acknowledged as an open problem; the current Proposition 3.23 structure cannot be extended by parameter optimization alone.
