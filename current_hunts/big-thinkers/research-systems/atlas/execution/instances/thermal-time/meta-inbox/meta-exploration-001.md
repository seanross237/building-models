# Meta-Learning Note — Exploration 001
**Date:** 2026-03-27 | **Written by:** Strategizer (thermal-time, strategy-001)

## What the exploration did
Phase 1 foundation: cataloged modular Hamiltonians for four systems (Rindler/BW, Bell state, thermal HO, CFT interval), formalized TTH for a bipartite product state, identified the autocorrelation C(t) as a discriminating observable, ran Python computation in truncated Fock space.

## What worked well
- **Explicit computation from the start**: The explorer wrote working Python (Fock space truncation, matrix log, KMS verification) and produced numerical results. The comparison table at the end of the report was exactly what the strategy needed.
- **Identifying the central ambiguity**: The explorer correctly flagged the normalization question (τ = t vs. τ = β×t) without resolving it, marking it as open. This was the right call — it's a literature question that needed dedicated attention.
- **Scope**: Four systems + computation + comparison table in one exploration was about right. Would have been too shallow with fewer, too rushed with more.

## What didn't work well
- **The GOAL.md I designed was more complex than what the explorer used**: The explorer used the simpler GOAL.md that was already in the directory (not the one I designed in this session). This suggests the explorer simplified the scope appropriately, but means I should calibrate: an explorer can handle 4 sub-parts in one exploration if each part is well-defined.

## Lessons for future goals
1. When the key question is normalization (a convention question), put it in its own exploration — it requires careful paper-reading that competes with computation time.
2. Asking for a "comparison table" as a deliverable is effective — it forces the explorer to produce a structured output the strategizer can directly use.
3. The GOAL.md should explicitly state: "compare local modular flow vs. FULL QM (H_AB dynamics), not just free oscillator" — exploration-001 compared against the free oscillator, which is the wrong baseline.
