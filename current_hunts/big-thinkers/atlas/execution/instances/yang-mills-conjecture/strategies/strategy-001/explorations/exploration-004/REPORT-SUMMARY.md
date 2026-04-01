# Exploration 004 — Report Summary

## Goal
Synthesize findings from E001 (maximal tree gauge), E002 (per-plaquette structure), and E003 (SO(3) representation theory). Rank proof routes, produce a concrete proof outline, and identify the single hardest step.

## What Was Tried
Careful reading and cross-referencing of all three Phase 1 reports. Assessment of four candidate proof routes (cube-face inequality, parallelogram pairing, single-link induction, quadratic form + Morse-Bott). Algebraic analysis of the cross-links=I formula and its generalization. Cross-checking proof outline against known special cases and dead ends.

## Outcome: Successful synthesis

**Best route: Route A (Cube-face inequality)**

The 96 plaquettes partition cleanly into 16 groups of 6 (one per vertex x as base vertex; 16×6=96). If each group satisfies ∑_{μ<ν} |B_{(x,μ,ν)}(Q)|² ≤ 64, then total ≤ 1024 = 4d|v|², giving λ_max ≤ 16.

**What is proved**: The cube-face bound ≤ 64 is established for the "cross-links=I" case via the formula F_x = 32 + 8⟨n,W⟩ − |A|² where W = ∑w_μ (sum of back-propagated directions), A = ∑s_μ w_μ (staggered version). The bound follows: 8⟨n,W⟩ ≤ 32 (triangle ineq) and −|A|² ≤ 0.

**What is not proved**: The cube-face bound for GENERAL Q with arbitrary cross-links (12 additional link variables per vertex that appear in partial holonomies).

## Key Takeaway

The entire proof reduces to a single unproved lemma:

**Lemma 5**: For all Q ∈ SU(2)^64 and all vertices x: ∑_{μ<ν} |B_{(x,μ,ν)}(Q,v)|² ≤ 64

Evidence for this: 0 violations in 160,000 numerical tests; adversarial gradient ascent converges to Q=I (achieving exactly 64). The maximum observed was 48.3, far below 64.

The mechanism (staggered sign structure, A = ∑s_μ w_μ → 0 at Q=I since ∑s_μ = 0) should generalize, but the explicit formula for general cross-links has not been derived.

## Leads Worth Pursuing

1. **Priority 1 — Symbolic expansion of F_x**: Write F_x = ∑|a(p_μ + q^{μν}) + b(n + r^{μν})|² for general cross-links, expand symbolically, determine if it takes the form 32 + 8⟨n,W̃⟩ − |Ã|² ≤ 64. This is a ~50-100 line computation (sympy/Mathematica) that could complete the proof or identify the precise obstruction.

2. **Quick verification**: Check that F_x = 64 for ALL 16 vertices on a single-link configuration (the single-link theorem gives total=1024, so each F_x should be exactly 64 for the null vector). This is a ~10-line computation and would give strong structural evidence.

3. **Monotonicity check**: Verify whether F_x decreases (or stays ≤ 64) as cross-links are varied away from I. If ∂F_x/∂(cross-link) ≤ 0 at maxima, that would prove Lemma 5 by showing maximum of F_x over cross-links is at cross-links=I.

4. **Route D algebraic sub-step**: Prove the 16 Fourier circulant blocks of M_perp are each negative definite algebraically (the entries are explicit integers). This is a machine-checkable certificate for the second-order result, though it doesn't close the global gap.

## Other Routes Assessed

- **Route B (Parallelogram pairing)**: Blocked. The parallelogram identity requires paired plaquettes to share identical partial holonomies (R_1, R_2, R_3). Active and inactive planes at the same vertex involve different links; no natural pairing exists generically.
- **Route C (Single-link induction)**: Blocked (confirmed by E001). No inductive structure.
- **Route D (Quadratic form + Morse-Bott)**: Second-best. M_perp < 0 is proved locally. The Fourier circulant proof is a clean algebraic sub-result. But the global extension requires ruling out all critical points outside U(1)_n^64 — a hard topological argument.

## Unexpected Findings

**Cross-links only help**: The numerical maximum of F_x for GENERAL Q (48.3) is far below the maximum for cross-links=I (which can approach 64). This suggests cross-links reduce the bound rather than threaten it. If formalized, this monotonicity would prove Lemma 5 cleanly.

**Single-link configurations predict per-vertex tightness**: The single-link theorem (E001) says the global sum = 1024 exactly for the null vector. Combined with the cube-face partition (16 groups, each ≤ 64, sum = 1024), every vertex must achieve exactly 64. This is a non-trivial per-vertex prediction that was not previously identified.

## Computations Identified

1. **Symbolic expansion of F_x for general Q** [PRIORITY]: Parameterize 16 link variables at vertex x, expand F_x symbolically, find the general formula. ~50-100 line sympy script. Would either complete the proof or identify the precise obstruction. MEDIUM difficulty.

2. **Fourier circulant algebraic proof** [MEDIUM PRIORITY]: Prove each of the 16 Fourier blocks of M_perp is negative definite using the explicit integer entries. Machine-checkable. ~30 lines. Gives algebraic certificate for the local result. EASY-MEDIUM.

3. **Single-link per-vertex cube check** [QUICK]: For a single-link perturbation at each of the 64 edges, compute all 16 cube-face sums F_x for the null vector. Verify each = 64. ~10 lines. EASY.
