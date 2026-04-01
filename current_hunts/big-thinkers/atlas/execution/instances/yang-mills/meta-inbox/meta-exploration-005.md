# Meta-Learning Note: Exploration 005

**Strategy:** 003, Phase 2
**Explorer type:** Standard
**Task:** Extract Jiang (2022) Weitzenböck formula and determine R(Q) sign

## What Worked Well

- The dual approach (literature search + immediate computation) was effective. The explorer found Jiang (2022) (arXiv:2211.17195) AND independently computed R(Q) eigenspectrum. The computation produced the more valuable finding.
- Nudging at 37% context worked perfectly — unlocked 183 more lines of output.
- The explorer correctly identified that the goal framing was wrong (M(Q) ≼ M(I) is false) and pivoted to the correct target (λ_max ≤ 4d).

## What Didn't Work

- The explorer could have been nudged earlier (should have written Section 1 right after the sub-agent returned, not waited until 37%). Initial template creation at 10% was good but then 27 more context points elapsed before anything was written.
- The literature sub-agent result was listed as "pending" in the initial REPORT.md but was already in memory — the delay was unnecessary.

## Lessons

1. **Verify goal assumptions before delegating to an explorer**: The goal said "M(Q) ≼ M(I) confirmed (E004)" which was incorrect. Including a quick sanity check ("is the claim in the goal actually what E004 found?") before writing would have caught this.

2. **Critical corrections deserve their own section**: When an explorer finds that a prior claim is wrong, it should write a "Critical Correction" section immediately — not bury it in Section 2.

3. **Standard explorers can do meaningful computation**: This explorer ran Python scripts and computed eigenspectra — it wasn't just doing literature search. The standard vs math distinction matters for verifiability (math explorer tags [VERIFIED]), but standard explorers can and should run code when relevant.

## Key Finding for Future Strategizers

The correct target for Yang-Mills mass gap improvement (12× over SZZ) is:
**λ_max(M(Q)) ≤ 4d** (NOT M(Q) ≼ M(I))

This is because M(Q) ≼ M(I) as a full operator is FALSE — R(Q) has both positive and negative eigenvalues. Only the TOP EIGENSPACE restriction R(Q)|_P ≼ 0 is true (and equivalent to the scalar bound).

Any future exploration goal that writes "M(Q) ≼ M(I)" should be corrected to "λ_max(M(Q)) ≤ 4d".
