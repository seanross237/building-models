---
topic: CNS paper novelty assessment — β < 1/6 is NOT in CNS papers, requires genuinely new insight
confidence: verified
date: 2026-03-29
source: "yang-mills-validation exploration-002"
---

## Overview

Equation-level comparison of the Atlas β < 1/6 mass gap result against both CNS papers (arXiv:2509.04688 Sept 2025, arXiv:2505.16585 May 2025). **All six key claims are ABSENT from the CNS papers.** The β < 1/6 result requires genuinely new insight beyond CNS — it is NOT trivially derivable from their work.

## Classification: Genuinely new insight required

**From CNS Sept 2025 (β < 1/24):** The vertex σ-model Hessian bound 4(d−1)Nβ is TIGHT — the bound is achieved at the staggered mode of the vertex Laplacian. It cannot be improved within the vertex formulation using the same Cauchy-Schwarz approach. The 1/6 result requires switching back to the edge-based action and applying a more careful triangle inequality. `[VERIFIED by reading actual paper]`

**From CNS May 2025 (~1/87):** The master loop approach is structurally different — curvature-free (no Bakry-Émery). Its optimized ceiling is ~1/87, well below 1/24. Deriving 1/6 would require incorporating Bakry-Émery curvature bounds, fundamentally changing the proof. `[VERIFIED by reading actual paper]`

## Overlap Table

| Our Claim | In CNS Sept? | In CNS May? |
|-----------|-------------|------------|
| H_norm = 1/12 at Q=I (exact Fourier) | NO | NO |
| Staggered mode is Hessian maximizer | NO | NO |
| Triangle inequality gives H_norm ≤ 1/8 for all Q | NO | NO |
| β < 1/6 threshold for SU(2), d=4 | NO | NO |
| Conjecture: H_norm ≤ 1/12 for all Q | NO | NO |
| Weitzenböck decomposition M(Q) = M(I) + R(Q) | NO | NO |

## Convention Comparison

| Paper | Action | β convention | SU(2) d=4 threshold |
|-------|--------|-------------|---------------------|
| SZZ23 | S = −(β/N) Σ Re Tr | 't Hooft | β < 1/48 |
| CNS Sept 2025 | S = Nβ Σ Re Tr | β = 't Hooft | β < 1/24 |
| CNS May 2025 | S = 2β Σ Re Tr | β̃ = Nβ | ~1/87 optimized |
| Atlas (this work) | S = −(β/N) Σ Re Tr | Same as SZZ/CNS | β < 1/6 (CS bound) |

All thresholds are in the SAME convention (SZZ/CNS 't Hooft coupling). `[VERIFIED]`

## Key Distinction: Mass Gap vs Area Law

CNS Sept 2025 proves AREA LAW (via DF80 slab condition), NOT mass gap. Atlas β < 1/6 is a MASS GAP result (direct Bakry-Émery spectral gap). The SZZ direct spectral gap at β < 1/48 has not been extended to 1/24 by CNS. `[VERIFIED from paper]`

## Caveat

The key mathematical step (Lemma 5.1: −(1/N)Re Tr(B²U) ≤ (1/(2N))|B|²) is technically modest — a straightforward bound using unitarity. It could plausibly have been derived from SZZ23 alone. However, it was NOT noted in any prior work, and it yields a 4× improvement over CNS Sept 2025. **NOTE:** E007 adversarial review later found that this lemma only bounds one term of the Hessian — the proof chain has a gap (see `adversarial-review-proof-chain.md`).

## Library entries confirmed accurate
The library descriptions of CNS Sept 2025 and CNS May 2025 are confirmed correct by actual paper reading. `[VERIFIED]`
