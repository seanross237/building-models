---
topic: Explorers reason well but cannot perform novel computations
category: system-behavior
date: 2026-03-27
source: "strategy-004 meta-s4-003, strategy-004 meta-s4-004, strategy-004 meta-s4-001"
---

## Lesson

Explorers can evaluate formulas with given inputs and reason about whether computations would work, but they cannot perform novel calculations that nobody has published. The best prediction extraction results come when you give the explorer a FORMULA to evaluate. When a prediction requires a computation nobody has done, the explorer correctly identifies the missing step but can't fill it. This is valuable -- it precisely identifies what needs to be computed -- but don't expect the explorer to be the one to compute it.

## Evidence

- **strategy-004 exploration s4-003** — Part A (evaluate b using given critical exponents) succeeded. Part B (derive delta-3 from RG trajectory) failed because the calculation hasn't been done in the literature. Explorer correctly identified the gap.
- **strategy-004 exploration s4-004** — Explorer correctly identified that the fakeon prescription doesn't affect UV divergences through three independent arguments. This was reasoning about the structure of a calculation, not performing it.
- **strategy-004 exploration s4-001** — Explorer used published fixed-point values to derive a numerical estimate. The computation was evaluating an existing formula, not deriving a new one.

## When to apply

When designing prediction extraction or technical investigation goals. If the prediction requires a novel calculation, frame the goal as "identify what computation is needed and what it would tell us" rather than "perform the computation." Also: killing a non-prediction (showing something is suppressed from ~0.01 to ~10^-14 by RG running) is as valuable as finding a real prediction.
