---
topic: Ask what replaces the bottleneck in alternative formulations
category: goal-design
date: 2026-03-30
source: "vasseur-pressure strategy-001 meta-exploration-008"
---

## Lesson

When a bottleneck appears in one formulation and you investigate whether an alternative formulation avoids it, always include the question: **"What is the NEW bottleneck?"** The answer "does an equivalent bottleneck appear?" is far more informative than either result alone. If the same numerical barrier reappears from a different mechanism, this reveals whether the obstruction is formulation-specific or structural.

## Evidence

- **vasseur-pressure exploration 008** — The goal asked whether the vorticity-based De Giorgi approach (Vasseur-Yang 2021) avoids the pressure bottleneck (beta < 4/3). The answer: yes, the pressure is genuinely eliminated. But the goal also asked "what is the NEW bottleneck?" — and the answer was a 4/3 barrier from a completely different source (trilinear form: 1/2 + 5/6 = 4/3, from the quadratic nonlinearity). This revealed that the 4/3 is NOT a pressure artifact but a structural property of the NS nonlinearity — the single most important finding of the exploration. Without the "what replaces it?" question, the report would have concluded "pressure eliminated, success" when the actual answer is "pressure eliminated, same barrier reappears, structural."

## Design Pattern

When the goal investigates an alternative approach that aims to remove a known obstruction:

1. **Ask whether the obstruction is present** ("Does the pressure bottleneck P_k^{21} appear?")
2. **Ask what replaces it** ("If not, what IS the bottleneck? Trace the limiting exponent to its new source.")
3. **Ask whether the replacement has the same numerical value** ("Is the new barrier the same 4/3, or a different value?")
4. **Request a comparison table** (old formulation vs. new formulation: source, mechanism, numerical value, context)

## Why This Matters

The most valuable negative results are those that explain WHY the answer is negative. "The 4/3 reappears" is a negative result. "The 4/3 reappears because 1/2 + 5/6 = 4/3, and this decomposition is structural to quadratic nonlinearity" is a deep negative result that reframes the entire mission. The decomposition into "derivative cost" (1/2) and "nonlinear factor" (5/6) is actionable — it tells you exactly what would need to change for the barrier to move.

## When to Apply

Any exploration testing an alternative approach to a known barrier: reformulations, variable changes, different function spaces, altered proof techniques. The "what replaces it?" question is especially important when the alternative approach is designed specifically to eliminate the barrier — because successful elimination without checking for replacement barriers gives a false sense of progress.

## Related

- `comparison-exploration-pattern.md` — structuring direct comparisons between approaches
- `investigate-why-on-discrepancies.md` — following the cause of discrepancies
- `specify-failure-paths.md` — turning negative results into positive leads
