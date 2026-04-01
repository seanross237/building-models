# Meta-Learning Note: Strategy-002 Exploration 009

**Type:** Math Explorer — Eigenvalue computation + numerical verification

## What Worked

1. **Full matrix computation worked cleanly.** 192×192 Hessian in ~10 minutes, eigvalsh confirmed λ_max = 4β exactly (under SZZ convention). The L=2 lattice choice was right — small enough for fast computation, large enough to capture the staggered mode.

2. **Convention identification was critical.** E009 found that λ_max = 8β or 4β depending on the S normalization convention. The explorer correctly identified which convention matches SZZ (S = -(β/N)Re Tr) and confirmed H_norm = 1/12 only under this convention. Always ask math explorers to report which conventions they used and verify against the reference paper.

3. **d=5 surprise finding was genuine.** The explorer went beyond d=4 and found that the staggered mode is NOT the maximum eigenvector for d=5 (residual = 0.98, true λ_max = 5β > 4.8β). This is a useful falsification of the "d-independent staggered mode is always worst case" assumption.

4. **Cross-validation with finite differences.** The explorer validated the analytical Hessian against numerical second derivatives (max error 2.4×10⁻⁶). This is good practice for any Hessian computation.

## What Didn't Work

1. **Only 5 random Q tested.** The random Q test (5 configs giving λ_max ≈ 2β < 4β) is meaningful but weak. 5 samples isn't sufficient to say Q=I is the global worst case. The GOAL.md should have asked for 50-100 random configs.

2. **REPORT.md didn't grow after initial 25 lines for a long time.** The explorer wrote 25 lines, then spent ~10 more minutes computing before writing more. Incremental writing instruction needed.

## Key Lessons

- **Always specify "verify your convention against the reference paper" in goals involving Yang-Mills.** The 1/N factor in the action is the single most common source of factor-of-2 errors.
- **For random Q tests, ask for ≥ 50 configs, not 5.** "5 random configs" is anecdotal; "50 random configs" gives statistical confidence.
- **Check non-standard dimensions as part of every lattice computation.** E009's d=5 finding was unexpected and valuable — it shows the d=4 result is not easily generalizable.
