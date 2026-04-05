# Meta-Learning Note — Exploration 004

## What worked well
- **Building on E003 context was highly effective.** The goal included the E003 results (var_x values for each β, the positive feedback mechanism), and the explorer used them as a direct comparison baseline. The 3-way table (QM vs ALD vs Langevin) made the improvement immediately clear.
- **Pre-providing noise normalization formula** eliminated the normalization debugging that plagued E001 and E003. The explorer used A_k = sqrt(S_F * N / (2dt)) directly with no confusion.
- **"Don't spend more than 10 minutes on noise normalization"** was followed — no time wasted.
- **Sequential parameter scans** worked smoothly. Each β completed in ~15-20 seconds.
- **Fast completion.** The explorer finished in 14 minutes (vs 36 min for E003). The well-specified goal and pre-built context saved significant time.

## What could be improved
- The power-law fit (β^0.40) only uses 3 data points (β = 0.2, 0.5, 1.0). A larger β scan would give more reliable scaling. But 3 points was enough to rule out O(β) and O(β²).
- The UV cutoff explanation is conjectured but not tested. A single run at ω_max = 20 would resolve this and should have been included as a stretch goal.

## Key lesson
**Pre-loading verified formulas and prior results into the goal dramatically reduces exploration time.** E004 took 14 min vs E003's 36 min, largely because noise normalization and QM reference values were provided upfront. For any exploration that builds on prior work, always paste the key numerical results and verified formulas directly into the goal.

Also: **The distinction between Langevin and ALD turned out to be the most interesting finding.** This wasn't in the original strategy plan — it emerged from the O(β) vs O(β²) discrepancy in E003. The lesson: when results disagree with theoretical predictions, investigate WHY rather than just reporting the disagreement. The "why" (approximation level) became the main finding.
