# Step 1: Comparative Proof Architecture Analysis

## Objective

Compare three independent proofs of CKN partial regularity at the structural level. The goal is NOT to list individual inequalities or measure constant sharpness — the adversarial review established that individual constant sharpness is irrelevant to CKN's qualitative conclusion. The goal IS to identify where the proof strategies agree (fundamental constraint) and where they differ (proof-specific constraint).

## The Three Proofs to Compare

1. **Caffarelli-Kohn-Nirenberg (1982)** — The original. Uses direct energy estimates with cutoff functions to localize.
2. **Lin (1998)** — Simplified proof. Uses compactness arguments, fewer explicit estimates.
3. **Vasseur (2007)** — Alternative proof. Uses De Giorgi iteration, avoids cutoff functions entirely.

Also read Scheffer (1976-1980) for context on the dimension bound and Ladyzhenskaya-Seregin (1999) as another simplification.

## What to Extract for Each Proof

For each of the three proofs:

1. **The epsilon-regularity criterion** — What scaled quantity must be small for regularity to follow? What is the precise statement?
2. **The covering argument** — How does the proof estimate the size of the singular set? What geometric structure (parabolic cylinders, balls, cubes) is used?
3. **The localization mechanism** — How does the proof pass from global to local? Cutoff functions? Compactness? Iteration?
4. **The scaling exponents** — What powers of the radius r appear in the key estimates? These determine the dimension bound on the singular set.
5. **Free-parameter vs. fixed-constant estimates** — Which estimates use Young's inequality with a free epsilon (absorption estimates, intentionally lossy) vs. estimates with fixed optimal constants?

## Key Question

**Does every proof strategy produce dimension <= 1 for the singular set through the same scaling route, or do they arrive there through different mechanisms?**

If the same scaling exponents appear in all three proofs, the dimension-1 bound is likely fundamental to this class of arguments. If different scaling appears, one strategy may offer a path to improvement.

## Success Criteria

A comparative table that clearly shows, for each proof:
- The epsilon-regularity criterion (precise mathematical statement)
- The covering argument structure
- The localization mechanism
- The critical scaling exponents
- Where each proof introduces the estimate that controls the singular set dimension

With a clear assessment: do these three independent proof strategies all converge on the same structural bottleneck, or does one of them avoid a constraint the others hit?

## Kill Condition

If all three strategies reduce to the same covering argument with the same scaling exponents (specifically: parabolic 5-dimensional scaling giving Hausdorff dimension <= 1), report this as the finding. It means the constraint is fundamental to epsilon-regularity approaches, and improvement requires a genuinely different proof architecture. This is a valid and informative negative result.

## Context

This is Step 1 of a 4-step chain. The output feeds into Step 2, where a Math Explorer will measure the regularity-relevant quantities identified here in resolved DNS. The scaling exponents from this step will be compared against numerically observed scaling.

## What This Step Does NOT Need to Do

- Do NOT try to measure slack numerically (that's Step 2)
- Do NOT try to prove anything new (that's Step 4)
- Do NOT audit individual inequality constants — the adversarial review established this is uninformative
- Do NOT focus on a single proof version — the comparison across strategies is the whole point
