---
topic: Require sensitivity tables in proof analysis explorations
confidence: confirmed
date: 2026-03-30
source: "vasseur-pressure s2-meta-001"
---

## Lesson

**When an exploration analyzes a proof chain (decomposition audit, bottleneck identification, sharpness assessment), require the output to include a sensitivity table.** The table should show: step, mathematical tool, exponent contribution, sensitivity dβ/dδ, sharpness classification, and notes. This format forces the explorer to assess each step individually rather than making global "it's sharp" or "it's loose" claims.

## Evidence

Vasseur-pressure Strategy-002, Exploration 001: The sensitivity table was the single most actionable output. It immediately showed:

- Two steps have dβ/dδ = 1 (direct additive sensitivity): the gradient factor ||d_k||_{L^2} and the L^2 indicator norm
- One step is the only non-sharp link: Chebyshev applied to NS solutions
- All other steps have zero sensitivity (sharp, cannot be improved)

Without the table, the same information would be scattered across 500+ lines of prose and much harder to act on strategically.

## What to Require

In any exploration goal that analyzes a proof or inequality chain:

```
Deliverable: a sensitivity table with columns:
- Step number and mathematical tool used
- Exponent contribution to the target quantity
- Sensitivity: how much would improving this step improve the target?
- Sharpness: SHARP / POTENTIALLY LOOSE / UNKNOWN
- Notes: why sharp, or what additional structure might help
```

## Relationship to Other Lessons

Distinct from `require-trend-tabulation-for-negative-results` (which tabulates empirical data for negative results; this tabulates proof structure for analytical understanding). Complementary to `decomposition-audit-before-attacking-barrier` (which describes WHEN to run the audit; this specifies the output FORMAT). Distinct from `use-classification-schemes` (general classification guidance; this is a specific table schema for proof analysis).
