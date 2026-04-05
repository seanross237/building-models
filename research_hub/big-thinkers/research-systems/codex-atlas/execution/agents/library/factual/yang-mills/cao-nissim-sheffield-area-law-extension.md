---
topic: Cao-Nissim-Sheffield area law extension — threshold doubled to β < 1/24
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-002 exploration-001; Cao-Nissim-Sheffield arXiv:2509.04688 (Sept 2025); Cao-Nissim-Sheffield arXiv:2505.16585 (May 2025)"
---

## Overview

Two 2025 papers by Sky Cao, Ron Nissim, and Scott Sheffield extend the SZZ strong-coupling result and prove Wilson's area law at a doubled coupling threshold (β < 1/24 vs. SZZ's β < 1/48). These are the sharpest rigorous area law results for continuous gauge groups to date.

**Note on attribution:** arXiv:2509.04688 was previously misattributed in the library to Adhikari-Suzuki-Zhou-Zhuang. The correct authors are Cao-Nissim-Sheffield (confirmed by exploration-001 direct paper fetch).

---

## CNS Sept 2025 (arXiv:2509.04688)

**Title:** "Dynamical approach to area law for lattice Yang-Mills"
**Authors:** Sky Cao, Ron Nissim, Scott Sheffield

### Main Theorem (Theorem 1.6)

For d ≥ 2, N ≥ 2, G ∈ {U(N), SU(N), SO(2(N-1))}:

```
β < β*_G  ⟹  Wilson's area law: |⟨W_ℓ⟩| ≤ C exp(−c · area(ℓ))
```

where:
- β*_{SU(N)} = β*_{U(N)} = **1/(8(d-1))**
- β*_{SO(2(N-1))} = 1/(16(d-1)) − 1/(8N(d-1))
- **In d=4: β < 1/24 for SU(N) and U(N)** — doubles the SZZ mass gap threshold

### How the Improved Threshold Arises

CNS applies the Bakry-Émery argument to the **σ-model on vertices** instead of Yang-Mills on edges.

| Method | System | Hessian bound | Threshold (d=4) |
|--------|---------|---------------|-----------------|
| SZZ (2023) | YM on **edges** | 8(d-1)Nβ | β < 1/48 |
| CNS Sept 2025 | σ-model on **vertices** | 4(d-1)Nβ | β < 1/24 |

The vertex Hessian bound is exactly half because each vertex has 2(d-1) edges (not plaquettes). The diagonal and off-diagonal contributions are each 2(d-1)Nβ, totaling 4(d-1)Nβ — compared to 2+6=8 for edges.

Bakry-Émery curvature for the σ-model:
```
K_S^{A,B} = N/2 − 4N(d-1)β > 0  iff  β < 1/(8(d-1)) = 1/24 (d=4)
```

### Area Law Derivation Method

CNS uses the **Durhuus-Fröhlich (1980)** slab condition rather than Chatterjee's Definition 2.3 (both yield area law; CNS found DF80 more direct). The σ-model on a height-1 slab satisfies exponential decay of covariances uniform in boundary conditions A, B:

```
|Cov_{A,B}(f,g)| ≤ C₁ e^{−C₂ d(x,y)}
```

with C₁, C₂ depending only on G, d, β (not on A, B, or volume). Area law follows by slab decomposition of Yang-Mills.

**Uniformity in boundary conditions** (Proposition 3.2): The Bakry-Émery constant K_S^{A,B} > 0 for any choice of boundary fields A, B ∈ U(N)^{E+_{Λ_{d-1}}}. This is the uniformity that drives area law.

### Limitation: N-Dependence

The string tension constant c decays with N (from SZZ Remark 4.12: c_N ~ K_S/d(g) where d(g) = N²-1). The May 2025 paper addresses this.

### Relation to Chatterjee's Approach

Remark 1.1 in CNS: "There is also the recent work [Cha21], which shows that a different version of mass gap (see Definition 2.3 therein) implies area law. In principle, it may be possible to also verify this assumption starting from the Bakry-Emery condition, but we found it more direct to verify the condition of [DF80]."

---

## CNS May 2025 (arXiv:2505.16585)

**Title:** "Expanded regimes of area law for lattice Yang-Mills theories"

### Main Theorem (Theorem 1.2)

For G = U(N), there exists β₀(d) > 0 (N-independent) such that for all β ≤ β₀(d) and all N ≥ 1:
```
|⟨W_ℓ⟩| ≤ C_{1,d} C_N^{|ℓ|} exp(−C_{2,d} area(ℓ))
```

**Key improvement:** C_{1,d} and C_{2,d} depend only on d — NOT on N. This resolves the N-dependence problem of the Sept 2025 paper.

**Different method:** Master loop equations / string duality (completely distinct from Bakry-Émery). The threshold β₀(d) is implicit (N-independent existence result, not an explicit formula like 1/24).

### Optimized Threshold (Proposition 3.23 Analysis)

Deep analysis of Proposition 3.23 (via yang-mills strategy-002 exploration-004) establishes that the **optimized ceiling** of the master loop approach is:
```
β₀(4)_max = 1/(32e) ≈ 1/87   [DERIVED]
```

This is a factor of **4e/3 ≈ 3.6×** below the CNS Sept 2025 Bakry-Émery threshold of 1/24.

**Parameter analysis:**
- λ = 1/N is proven optimal (minimizes splitting + merger sum; cannot be improved)
- ρ = 1/e is required by the boundary term in Proposition 3.24 (not conservative — a proof requirement)
- γ = 1 is the optimal achievable choice (norm requires γ ≥ 1; γ=1 gives the ceiling β₀(4) = 1/(32e))

The paper's published conservative choice (γ = (10³dβ)⁻¹, requiring γ ≥ 1 → β ≤ 1/4000) was far from the optimized ceiling. The explicit threshold table in the paper (eq. 2.2) gives β ≤ 10^{-10d}/d ≈ 2.5×10⁻⁴¹.

### N-Independence vs. β-Range Tradeoff

| Feature | Master Loop (CNS May 2025) | Bakry-Émery (CNS Sept 2025) |
|---------|---------------------------|------------------------------|
| β threshold (d=4) | β₀(4)_max ≈ 1/87 (optimized) | 1/24 |
| String tension constant | **N-independent** | Decays with N |
| Proof structure | Algebraic/combinatorial (master loops) | Riemannian geometry (Bakry-Émery) |
| Curvature used? | No | Yes (κ = N/2) |

**The gap (factor 4e/3) is the "free lunch" from positive curvature that Bakry-Émery exploits.** The master loop gives N-independence at the cost of a narrower β range.

### Critical Correction: Remark 1.4 Is About Signed Cancellations

**[VERIFIED from paper text]** Remark 1.4 of arXiv:2505.16585 asks about extending to β ~ c_d N (the large-N regime). The key obstacle is NOT curvature input — the master loop proof is **curvature-free** (Ricci curvature κ=N/2 does not appear in Lemma 3.20, Proposition 3.23, or Proposition 3.24).

The actual obstacle identified in Remark 1.4: the merger term (3.5) bound uses the unsigned count |M±| ≤ 2dB. If **positive and negative surface contributions cancel** (signed cancellations), the effective B factor could be reduced, allowing larger β. This requires a fundamentally different norm structure incorporating signed surface weights — not parameter optimization.

---

## Current State of the Field (as of early 2026)

| Result | Regime | Method | Reference |
|--------|--------|--------|-----------|
| Mass gap | β < 1/48 (d=4) | Bakry-Émery (edges) | SZZ 2023 |
| Area law (SU(N), U(N), SO(2N)) | β < 1/24 (d=4) | Bakry-Émery (vertices) | CNS Sept 2025 |
| Area law (U(N), N-independent) | β ≤ β₀(d)_max ≈ 1/87 (optimized) | Master loop + string duality | CNS May 2025 |
| Mass gap and area law, ALL β | Open | — | — |

**Note:** β₀(d)_max ≈ 1/87 is the optimized ceiling of the master loop approach (Prop 3.23 analysis, [DERIVED]). The paper's own published threshold is far more conservative (β ~ 10^{-41}).

---

## Open Questions

1. **Mass gap at β < 1/24?** SZZ gives mass gap at β < 1/48; CNS gives area law at β < 1/24 via DF80, but does not directly give infinite-volume mass gap at the 1/24 threshold.
2. **Master loop to full 't Hooft regime?** Remark 1.4 of arXiv:2505.16585 identifies the path: exploit signed cancellations in the merger term (not curvature input — the proof is curvature-free). Requires a new norm with signed surface weights.
3. **Path from 1/24 to all β > 0?** No known approach.
4. **Sharper Hessian bound?** CNS halved the SZZ Hessian bound by switching from edges to vertices. Numerics (strategy-002 E005-006) show the actual Hessian is 29-138× below even the CNS vertex bound. A √(# plaquettes) scaling would tighten substantially. [See also: szz-lemma-4-1-hessian-slack.md]
5. **Combining master loop (N-independence) with Bakry-Émery (β range)?** Four speculative routes: (A) use Bakry-Émery at fixed N, then take N→∞ using master loop N-independence; (B) extend master loop to β ~ 1/87 via signed cancellations; (C) Bakry-Émery with a tighter Hessian reaching β₀ > 1/87; (D) hybrid: master loop for string tension, Bakry-Émery for mass gap separately.
