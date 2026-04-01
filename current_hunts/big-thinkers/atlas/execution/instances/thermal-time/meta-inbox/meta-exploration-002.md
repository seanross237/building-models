# Meta-Learning Note — Exploration 002
**Date:** 2026-03-27 | **Written by:** Strategizer (thermal-time, strategy-001)

## What the exploration did
Resolved the normalization ambiguity (τ = β×t confirmed by three papers), then computed ΔK_A = K_A - βH_A for the globally coupled Gibbs state. Found ΔK_A ≠ 0 at O(λ²), with squeezing structure and period shift prediction Δτ/τ ≈ 0.68λ².

## What worked well
- **Literature first, then computation**: The explorer correctly resolved the normalization from the literature before doing the computation — this prevented building on a shaky foundation.
- **Analytic proof of O(λ¹) vanishing**: The explorer didn't just note the numerical O(λ²) fit — it gave the analytic argument (⟨q_B⟩=0 for thermal state). This is exactly what "rigor" means for this kind of result.
- **Distinguishing C_local_TTH from C_free_QM**: The explorer correctly noted in its leads that the proper comparison requires C_full_QM (evolved under H_AB), not just C_free (evolved under H_A). Good self-awareness about what the exploration didn't complete.
- **Sub-agent for literature**: The explorer used a tmux sub-agent for the literature survey on normalization. This worked well — allowed parallel literature search while doing computation.

## What didn't work well
- **The period shift (0.68λ²) was compared against the WRONG baseline**: C_local_TTH was compared to C_free (H_A evolution), not C_full (H_AB evolution). The 6.4% period shift claim is therefore not yet a valid comparison against standard QM. This is the most important gap in exploration-002.
- **Squeezing structure reported but not fully interpreted**: The band-2 off-diagonal ΔK_A was identified as squeezing but the physical origin (Bogoliubov transformation of normal modes) wasn't derived. A deeper exploration would connect ΔK_A to the normal mode transformation.

## Lessons for future goals
1. **Always specify the exact baseline**: A GOAL.md must say "compute C_full_QM = Tr[ρ_AB x_A(τ) x_A(0)] where x_A(τ) evolves under the FULL H_AB" — not just "standard QM." Explorers default to the free theory.
2. **When you find an O(λ²) correction, identify its coefficient analytically**: The numerical 0.68 is useful but the explorer identified the 2nd-order Duhamel formula as the next step. That analytic formula would be more convincing.
3. **The literature normalization question took ~1/3 of the exploration**: If you have both a literature question and a computation in one goal, budget accordingly. In this case the computation was the main payload and the literature part resolved cleanly — worked fine.
