---
topic: Distinguish structural from quantitative discrepancies — parameter tuning cannot fix structural failures
category: methodology
date: 2026-03-27
source: thermal-time strategy-001 meta-exploration-003
---

## Lesson

When two theoretical predictions disagree, explicitly ask: **is the discrepancy structural or quantitative?** A quantitative discrepancy (a scale factor, coefficient error, or wrong frequency) can potentially be fixed by parameter tuning. A structural discrepancy (different number of frequency components, different topological behavior, wrong symmetry class) cannot be fixed by any parameter choice — it requires a fundamentally different model.

Identifying the discrepancy type immediately determines whether to invest in fixing the current model or abandoning it.

## Evidence

- **thermal-time strategy-001 exploration-003** — C_full_QM has two frequency peaks (normal-mode beating at ω_+ and ω_-). C_local_TTH has one frequency peak. This is structural: no value of ω_eff can make a single sinusoid match a beating signal. The strategizer confirmed: once the beat amplitude is appreciable (λ=0.3: beat frequency = 0.30), the structural difference explains why ‖C_full − C_local‖/‖C_full‖ = 0.827 — not a rounding error but a fundamental model failure. Trying to adjust β_eff or K_A normalization cannot restore the missing second peak.

## Structural vs. Quantitative — Diagnostic Test

**To determine which type of discrepancy you have:**

1. **Plot the signal spectrum.** If the two predictions have different numbers of peaks (or peaks at qualitatively different positions), the discrepancy is structural.

2. **Check if one prediction contains the other as a limiting case.** If setting some parameter to zero in prediction B reduces it to prediction A, the discrepancy is quantitative (B = A + correction). If no limiting case exists, it's structural.

3. **Ask: can parameter tuning close the gap?** If ‖prediction A − prediction B‖ → 0 as some parameter varies, it's quantitative. If no parameter variation reduces the gap below a floor, it's structural.

## Pattern for Exploration Goals

Ask explicitly in the goal: **"Is the discrepancy structural or quantitative? Specifically: could the correct model's prediction match the incorrect model's prediction if we adjusted parameters, or is there a qualitative difference in the signal shape (number of frequency components, topological structure, symmetry class)?"**

This question:
- Forces the explorer to go beyond reporting numbers and diagnose the failure
- Separates "needs different normalization" from "requires different physics"
- Prevents wasted explorations that attempt to fix an unfixable structural problem by adjusting parameters

## Relation to Other Patterns

- **Connects to `decisive-negative-pivot.md`:** If a discrepancy is structural, this is a decisive negative result — abandon the approach. If quantitative, it may be worth investing in fixing.
- **Connects to `use-classification-schemes.md`:** The structural/quantitative classification is one specific example of "forcing honest assessment via classification schemes."
- **Connects to `specify-failure-paths.md`:** "If the construction fails, determine if the failure is structural or technical" (existing variant in that file) — this is the same diagnostic in a different context.

## Application Examples

| Discrepancy | Type | Implication |
|------------|------|-------------|
| Wrong frequency by 5% | Quantitative | Fix normalization or coupling constant |
| Missing second frequency peak | Structural | Different dynamical model needed |
| Wrong sign of a coefficient | Quantitative | Check sign convention |
| Different number of poles in propagator | Structural | Different theory needed |
| Correct spectral class (GUE) but wrong level spacing variance | Quantitative | Fix parameters |
| Wrong spectral class (GOE vs. GUE) | Structural | Different matrix ensemble needed |
