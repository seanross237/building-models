# Meta-Learning Note: Strategy-003 Exploration-002 (E-Hydrogen)

**Date:** 2026-03-27
**Explorer type:** Math explorer
**Goal:** SED hydrogen T_ion(L) with physical τ = 2.6×10⁻⁷ a.u.

## What Worked Well

1. **Providing the physical τ formula explicitly** (τ = 2/(3 × 137.036³)) in the GOAL.md eliminated any ambiguity. The explorer computed it numerically before coding and confirmed 2.591×10⁻⁷ a.u.

2. **The memory-management guidance** (chunked FFT instead of pre-generating full array) was very helpful. The explorer implemented 2^17-point FFT chunks with a C library for the inner loop, achieving excellent performance.

3. **Specifying the run order** (lowest L first) and giving time estimates was useful. The explorer ran efficiently.

4. **The comparison table with E003** in the GOAL.md helped the explorer immediately verify the 60× correction was working correctly.

## What Didn't Work As Expected

1. **The timeout warning was right but incomplete**: The GOAL.md warned about memory for 10,000-period runs. The explorer solved this with C compilation + chunking, which was better than I suggested. But the 10-minute timeout DID fire once (likely on one of the early long runs). The explorer recovered and completed all runs.

2. **The "streaming ZPF" suggestion** in the GOAL.md was the right direction but the explorer found an even better solution (pre-generating 2^17-chunk with FFT for each chunk). The hint helped but wasn't the exact solution.

## Key Lesson

**For numerical simulations where the main bottleneck is computation speed**: Providing explicit performance estimates AND the memory bottleneck analysis (not just the physics) in the GOAL.md enables the explorer to make good engineering decisions. The explorer's C-library solution was much faster than a pure Python approach would have been. The GOAL.md's memory analysis directly led to the chunked approach.

## Unexpected Outcomes Worth Flagging

1. T_ion(L) power law exponent 6.44 is much larger than expected — worth theoretical analysis in a future exploration.
2. L=1.0 does eventually ionize (18/20 in 50,000 periods) — this is a key physical result.
3. The non-simple τ-scaling (26-89× vs expected 60×) suggests the physics is richer than a simple diffusion model.

## No Major Problems

Completed all 7 L values, all sanity checks passed, all in ~24 seconds total compute time.
