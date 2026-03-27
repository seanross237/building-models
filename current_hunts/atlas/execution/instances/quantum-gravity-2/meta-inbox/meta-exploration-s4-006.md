# Meta-Learning: Exploration S4-006 (Devil's Advocate)

## What worked
- Giving the full prediction catalog WITH specific attacks to mount produced a thorough assessment
- The 6 named attacks gave the explorer a clear structure to follow
- Asking for severity ratings (FATAL/SERIOUS/MODERATE/COSMETIC) forced clear judgments
- The null hypothesis test was essential — it showed that H₀ explains everything the framework claims

## What didn't
- Report was 558 lines (over the 400-line target) — the explorer was very thorough, which is good for a devil's advocate but means some parts could have been tighter

## Lesson
1. Devil's advocate explorations should ALWAYS include the null hypothesis test. Without it, you can attack individual predictions without asking the most important question: "does the framework add anything beyond its components?"
2. The b parameter precedent (E003 showed b suppressed from ~10⁻² to ~10⁻¹⁴ by RG running) should always be cited when assessing NGFP predictions that have "correct sign but unknown magnitude." The lesson: correct sign is cheap; correct magnitude is what matters.
3. The distinction between "research program" and "predictive framework" is the sharpest way to characterize a theory that identifies important calculations but hasn't performed them.
