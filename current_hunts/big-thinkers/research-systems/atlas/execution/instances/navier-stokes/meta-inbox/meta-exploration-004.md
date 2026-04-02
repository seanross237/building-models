# Meta-Learning: Exploration 004 (Vortex Stretching Decomposition)

## What Worked Well
- **Specifying the exact decomposition formulas in the goal**: The explorer didn't need to derive the decomposition — just implement and compute it. This saved significant context.
- **Requiring a verification check (α_geom × α_Lad × α_sym = total)**: This caught an important correction — the original estimates from exploration 002 were significantly wrong (geometric factor was ~5.3 not ~9; Ladyzhenskaya factor was ~31 not ~18.6). The consistency check made this visible immediately.
- **Prioritizing Part B (alignment statistics) over Part C (sharp constant)**: Part B produced the most scientifically interesting results. Part C was completed but the survey approach (testing known fields) was less informative than a systematic optimization would be.
- **Math explorer was the right choice**: Every claim is backed by code. The eigendecomposition + alignment statistics required substantial computation.

## What Could Be Improved
- **Exploration 002's decomposition was wrong**: The initial factor estimates came from rough back-of-envelope calculations. Future strategy: always run a dedicated decomposition exploration before trusting component estimates.
- **Part C (sharp constant) was too limited**: The survey of known fields found C_{L,div-free} = 0.279 but didn't attempt systematic optimization. A separate exploration with gradient descent over Fourier modes would be more informative.
- **Missing: what happens in turbulent regime?** Both Re=100 and Re=1000 show transitional alignment (extensional dominant). Published DNS shows intermediate-dominant alignment in turbulence. This transition is important but wasn't captured.

## Key Lesson
- **Require consistency checks in decomposition explorations.** The α × β × γ = total check is trivially stated but catches real errors. Always include multiplicative/additive consistency checks when asking for factor decompositions.
- **Correcting wrong priors is the highest-value output.** Exploration 004's most important result was showing that exploration 002's rough estimates were wrong — Ladyzhenskaya dominates, not Hölder. This changes the entire strategic direction. Design explorations that can correct priors, not just confirm them.
