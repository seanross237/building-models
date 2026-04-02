# Meta-Learning Note: S003 Exploration 001 — Off-Diagonal Form Factor

## What Worked Well

**Literature extraction was successful:** The explorer found and parsed Berry-Keating (1999) SIAM Rev. paper from a PDF, extracting the correct formulas for R¹_c and R²_c (eqs 4.23, 4.27-4.28). The instruction to find the formulas in specific named papers worked.

**Formula error self-correction:** The explorer diagnosed the wrong formula (wrong kernel giving Δ₃ ∝ L) and found the correct Σ₂ → Δ₃ route. It saved intermediate results as .npz files throughout. The GUE ground truth computation was done correctly with 20 matrix trials.

**Incremental computation with multiple intermediate results:** The explorer produced many code files (compute_delta3.py, delta3_correct.py, delta3_final.py, verify_delta3_formula.py) and .npz files. This allowed partial results to be recovered even before REPORT.md was written.

## What Didn't Work Well

**Very long thinking loops:** The explorer spent 30+ minutes in "Elucidating" mode between computation runs. REPORT.md stayed at 190 lines for 15+ minutes. Required multiple nudges.

**delta3_final.py computation was slow:** The script ran for 10+ minutes and hit the timeout. The bottleneck was computing R1_c and R2_c functions at many (L, r) grid points, each involving expensive prime sums and zeta function evaluations.

**Formula bug consumed a lot of exploration time:** ~20 minutes were spent implementing, running, and debugging the wrong Δ₃ kernel formula before finding the correct Σ₂ → Δ₃ route. If the goal had provided the CORRECT formula from the start (and marked the common wrong formulas), this would have been avoided.

## Lessons

**For goals involving Berry-Keating formulas:** The (L-r)³(2L²+rL-r²) kernel formula is WRONG. The correct Δ₃ formula is:
1. Σ₂(L) = L + 2∫₀ᴸ (L-r)(R₂(r)-1) dr
2. Δ₃(L) = (2/L⁴) ∫₀ᴸ (L³-2L²r+r³) Σ₂(r) dr

Future goals should provide this correct route explicitly and flag the wrong formula as a known pitfall.

**The perturbative regime discovery is the key result:** The surprise finding was that the Berry-Keating perturbative corrections require ⟨d⟩ >> 1, i.e., T >> 10^{10}. This is a genuinely important finding about the validity range of the semiclassical approximation. Goals should ask explorers to check the validity of asymptotic expansions explicitly.

**Nudging strategy that worked:** The phrase "STOP running new computations. You have sufficient results. Write the report with what you have." was effective. The explorer immediately responded: "The computation completed. R1_c blows up (numerical issue), R2_c gives only 1.6% gap closure. Let me write the complete report now." This is a strong, direct instruction pattern.

**Computation timeout was too short:** R1_c and R2_c functions involve prime sums over 300-500 primes and zeta function evaluations at each grid point. For a grid of 200 L-values × 3000 r-values, that's 600,000 function evaluations. 10 minutes is too short. Use 20-30 minute timeouts for goals involving prime sum computations.

## Verdict

The exploration succeeded in its core goal: extracting the off-diagonal formula and computing a number. The number (1.6% gap closure from R2_c) is negative but informative. The discovery of the perturbative regime breakdown (T >> 10^{10}) is the most valuable finding.
