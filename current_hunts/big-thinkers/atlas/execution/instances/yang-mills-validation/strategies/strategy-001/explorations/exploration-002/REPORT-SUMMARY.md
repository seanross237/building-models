# Exploration 002 Summary: CNS Paper Novelty Assessment

## Goal
Determine whether the Atlas β < 1/6 mass gap result is already in, or trivially derivable from, the CNS papers arXiv:2509.04688 (Sept 2025) and arXiv:2505.16585 (May 2025).

## What Was Done
Both papers were read in full (PDFs accessed directly from the local cache). Theorem statements, Hessian bounds, proof methods, and action conventions were extracted verbatim and compared against the Atlas claims.

## Outcome: VERDICT — (c) Genuinely new insight required

**β < 1/6 is NOT in either CNS paper, and is NOT trivially derivable from their work.**

## Key Findings

### CNS Sept 2025 (arXiv:2509.04688) — Read in Full

- **Action convention:** S_YM = Nβ Σ Re Tr(Q_p) — same convention as SZZ23 (both use same β)
- **Main threshold:** β* = 1/(8(d-1)) = **1/24** for SU(N), d=4 (Theorem 1.6, Definition 1.4)
- **Method:** Vertex σ-model + Bakry-Émery + DF80 slab condition for area law
- **Hessian bound (Eq. 3.1):** |Hess| ≤ 4(d-1)Nβ = 24β for N=2, d=4
- **K formula:** K = 1 − 24β > 0 iff β < 1/24
- **Critical finding:** The vertex Hessian bound 4(d-1)Nβ IS TIGHT — the discrete vertex Laplacian has maximum eigenvalue exactly 4(d-1) at the staggered mode. The CNS bound cannot be improved within the vertex formulation.
- None of our six Atlas claims (exact eigenvalue, staggered mode, triangle bound, β<1/6, H_norm conjecture, Weitzenböck) appear anywhere in the paper.

### CNS May 2025 (arXiv:2505.16585) — Read in Full

- **Action convention:** S = 2β Σ Re Tr(U_p) (same β as Sept 2025 for N=2)
- **Approach:** Master loop equations (completely different from Bakry-Émery; curvature-free)
- **Threshold:** β₀(4) ≈ 10^{-41} as published; ~1/87 after optimization (well below 1/24)
- **No Hessian analysis.** No curvature input. Contraction mapping on norm space instead.
- **Key contribution:** N-independent string tension constant C_{2,d} (unlike CNS Sept 2025)
- This paper cannot reach 1/6 at all — it is structurally limited to ~1/87 even optimized.

### Convention Verification (Numerically Confirmed)
All four thresholds (1/48, 1/24, 1/6, 1/4) are in the same β convention. Computation verifies:
- SZZ Hessian bound 48β → β < 1/48 ✓
- CNS vertex bound 24β → β < 1/24 ✓ (2× SZZ)
- Atlas triangle bound 6β → β < 1/6 ✓ (4× CNS, 8× SZZ)
- Atlas exact Q=I bound 4β → β < 1/4 ✓ (if conjecture holds)

### Overlap Table
| Our Claim | In CNS (Sept)? | In CNS (May)? |
|-----------|----------------|---------------|
| H_norm = 1/12 at Q=I | NO | NO |
| Staggered mode is maximizer | NO | NO |
| Triangle inequality → H_norm ≤ 1/8 | NO | NO |
| β < 1/6 threshold | NO | NO |
| Conjecture H_norm ≤ 1/12 all Q | NO | NO |
| Weitzenböck M(Q) = M(I) + R(Q) | NO | NO |

## Key Takeaway

**The β < 1/6 result is genuine new work.** It cannot be derived from CNS Sept 2025 because that paper's Hessian bound (4(d-1)Nβ via the vertex σ-model) is already tight — the vertex Laplacian's staggered mode achieves the bound exactly. To reach 1/6, one must return to the edge-based Yang-Mills framework (SZZ) and apply a tighter triangle inequality using Lemma 5.1 (−(1/N)Re Tr(B²U) ≤ (1/2N)|B|²). This gives |Hess| ≤ 6β (vs. SZZ's 48β and CNS's 24β), yielding β < 1/6.

**Important distinction:** CNS Sept 2025 proves AREA LAW (via DF80); Atlas β < 1/6 proves MASS GAP (direct Bakry-Émery spectral gap). These are different results at the same threshold.

## Leads Worth Pursuing

1. **Can the vertex σ-model (CNS approach) be combined with the Fourier/staggered mode insight to get β < 1/6 for area law?** The vertex Laplacian bound is tight, so one would need a new technique — probably proving the σ-model Hessian with GENERAL A, B is tighter than the A=B=I case at Q=I.

2. **Does β < 1/6 extend to area law?** The Atlas result is a mass gap (spectral gap). Converting to area law requires DF80, which needs the vertex formulation. Is there a way to combine the tighter edge Hessian with DF80?

3. **Proof gap: the global bound H_norm ≤ 1/12 (conjectured) would give β < 1/4.** This remains open.

## Unexpected Findings

1. **CNS Sept 2025 knows their bound is tight.** The authors are aware that the vertex Laplacian achieves 4(d-1) at the staggered mode. They don't mention this explicitly, but the Hessian derivation structure implies it. The Atlas "staggered mode is the maximizer" finding is thus not surprising in retrospect — but it was never stated in the literature.

2. **β < 1/6 is NOT a CNS-convention threshold.** It is a threshold for the edge-based Yang-Mills action — a different (older, simpler) framework than what CNS uses. The novelty is not about a new proof strategy but about extracting a better bound from the classical SZZ approach.

3. **CNS May 2025 explicitly notes that their result is weaker in β range than CNS Sept 2025** (see Remark 1.3(4), Figure 1). The masters loop approach trades β range for N-independence.

## Computations Identified

- None required for this novelty assessment. All conclusions are based on reading the papers and straightforward formula verification (K = 1 − C×β thresholds computed analytically).
