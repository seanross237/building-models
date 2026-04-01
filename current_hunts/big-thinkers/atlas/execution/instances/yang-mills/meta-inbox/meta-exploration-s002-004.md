# Meta-Learning Note: Strategy-002 Exploration 004

**Type:** Math Explorer — Analytical optimization / formula extraction

## What Worked

1. **Closed-form parameter optimization is fast.** E004 computed all its results from the known threshold formulas in ~2 minutes. For pure formula manipulation (not simulation), math explorers complete very quickly.

2. **The explorer correctly identified an ambiguity** (C_eff = 8de vs 8e) and flagged it clearly. Good epistemic hygiene.

3. **Spawning a sub-agent to read the paper** was a creative solution to verify formulas — worked, though sub-agent didn't fully resolve the ambiguity.

## What Didn't Work

1. **Key quantity (Proposition 3.23 formula) was not directly extracted.** The explorer modeled B(N,d) and C_d implicitly from known thresholds. The exact formula from the proof remains unverified. This is a limitation of analyzing paper structure without being able to read every equation precisely.

## Lessons

- For formula optimization explorations: the computation itself (optimization, scanning C_eff) takes 5-15 minutes. The literature extraction (finding B(N,d) exactly) takes much longer and should be a separate exploration.
- Flag numerical ambiguities clearly (the C_eff = 8de vs 8e issue here). These ambiguities often encode important structural information.
- If a key formula cannot be extracted from a PDF, the best approach is to bound it from above and below using known values (the explorer did this well).
