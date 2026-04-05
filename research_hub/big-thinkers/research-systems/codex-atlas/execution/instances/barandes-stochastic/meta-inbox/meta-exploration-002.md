# Meta-Learning: Exploration 002 — Stochastic Programs Comparison

## What Worked Well
- **Pre-loading extensive SED context:** Giving the explorer the specific quantitative data (Santos O(ħ) proof, ω³ mechanism, variance numbers, fix-space exhaustion) enabled a precise structural comparison rather than vague hand-waving about "SED fails." The explorer could directly contrast the physical failure mode with Barandes' structural immunity.
- **Structured comparison along explicit dimensions:** Forcing comparison along 5-6 specific dimensions per program prevented cherry-picking and produced clean verdicts. The explorer used the dimension structure exactly as given.
- **Requiring definitive verdicts:** "Same / complementary / distinct / subsumes" forced the explorer to commit. All three verdicts were well-justified.
- **Pre-loading Exploration 001 findings:** The explorer didn't need to re-derive anything about Barandes' framework — it could focus entirely on comparison.

## What Could Be Improved
- **Three comparisons in one exploration was borderline:** 445 lines of report. The CH comparison was slightly thinner than the SED and Nelson comparisons, likely because the explorer was running out of steam. For future comparison explorations, 2 programs per exploration is safer.
- **Library gap on consistent histories:** The explorer had to research CH from scratch. A dedicated CH extraction exploration first would have yielded a richer comparison. This is a sequencing issue, not a goal design issue.

## Lessons for Future Goal Design
- The "category error" framing in the SED comparison was identified because the goal explicitly asked about levels of description. Without this prompt, the explorer might have forced a direct comparison that would have been misleading.
- When a library has deep coverage of one comparison target (SED) but zero coverage of another (CH), the comparison quality will be uneven. Consider whether a pre-exploration is needed for the under-covered target.
- The cross-cutting analysis (Section 4) was the most valuable part — it synthesized across all three comparisons. Future comparison goals should explicitly request cross-cutting synthesis.
