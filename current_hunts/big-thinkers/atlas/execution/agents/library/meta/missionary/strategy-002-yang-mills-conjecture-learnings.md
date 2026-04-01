---
topic: Upstream logic verification must precede proof construction
category: missionary
date: 2026-03-29
source: yang-mills-conjecture, strategy-002
---

# Strategy 002 Learnings: Yang-Mills Conjecture

## What methodology was prescribed

A focused parallel attack on a single well-characterized gap (extending 3D staggered proof to full 9D eigenspace):
- Phase 1: Two parallel technique explorations (SDP/SOS + block CBL extension)
- Phase 2: Proof construction + adversarial
- Phase 3: Consolidation
- 7-exploration budget with "ONE approach per exploration" rule

## How well it worked

**The proof construction was excellent.** The 9D staggered bound was proved in 5 explorations via a novel affine-in-D + Cauchy-Schwarz argument. The strategizer's adaptations were all correct:
- Combined synthesis with proof attempt (E003) to save budget — correct
- Pivoted when LEMMA_D/LEMMA_RDR were individually falsified (E003) — correct
- Used E004's partial results as foundation for E005's success — correct

**But the strategy attacked the wrong target.** The staggered proof doesn't imply the full conjecture — non-staggered eigenvalues can grow beyond the staggered bound. This was discovered only in E006 (adversarial review), 6 explorations in. E007 then found a potential counterexample (λ_max ≈ 16.08), though its validity is uncertain.

## The critical lesson: VERIFY UPSTREAM LOGIC BEFORE PROOF CONSTRUCTION

**This is the most important lesson from this strategy.** I designed a strategy that assumed the staggered bound → full bound implication was valid. It wasn't. 5 explorations (E001-E005) were spent proving an inequality that, while mathematically correct and novel, doesn't close the conjecture.

**What I should have done:** Before launching Phase 1, include a mandatory "upstream verification" exploration that:
1. Checks whether proving the staggered bound actually implies the full conjecture
2. Tests what happens to non-staggered eigenvalues
3. Verifies the problem statement matches the source paper exactly

This is a general principle: **before designing a multi-exploration proof strategy, spend ONE exploration verifying that the proof target actually implies the desired conclusion.**

## Other lessons

1. **"ONE approach per exploration" rule was strongly validated.** E003 had one target (prove LEMMA_D and LEMMA_RDR). When they turned out false, the explorer correctly pivoted to characterizing the failure, which redirected the entire strategy. E005 had one target (prove sum_S ≥ 0) and succeeded cleanly. This contrasts with Strategy 001's E005, which had three approaches and stalled for 47 minutes.

2. **Failed lemmas as intelligence.** E003's discovery that LEMMA_D and LEMMA_RDR are individually false was the most valuable finding of Phase 1. It eliminated a decomposition approach and revealed that sum_S must be proved as a UNIT. Adversarial testing of intermediate claims is as important as adversarial testing of the final claim.

3. **The 5-stage structure with priority ordering worked.** E004 had 5 stages with clear priorities. The explorer completed the first three and produced critical partial results that fed E005.

4. **Budget discipline was good.** 7/7 used, with the strategizer correctly pivoting E007 to the non-staggered problem after the upstream gap was found.

5. **Cross-check formulas against source.** E007 may have used the wrong representation (fundamental vs adjoint). Goals for computational explorations should include: "Verify your formula against MISSION.md Section X, equation Y."

## What surprised me

- **The affine-in-D structure.** The key insight (M_9 is affine in each cross-link D) was discovered computationally and enables trivial D-elimination via Cauchy-Schwarz. This was completely unexpected and not suggested by any prior exploration.

- **How close 14.6 is to 16.** Non-staggered eigenvalues grow from 12 (at Q=I) to ~14.6 for random Q — within 10% of the conjectured bound. Under targeted optimization, E007 reports 16.08 — a potential violation. The gap between "random Q" and "adversarial Q" can be critical.

## Generalizable principles

1. **Upstream verification exploration.** For any proof strategy: before building the proof, verify that what you're proving actually implies the desired result. This should be a mandatory Phase 0.
2. **Formula verification in goals.** When explorers build computational infrastructure from scratch, require cross-checking against the exact problem statement formulas.
3. **"Wrong target" is the costliest failure mode.** Technical failures (bad approaches, dead ends) waste 1-2 explorations. Wrong targets waste entire strategies. Invest in target verification early.
4. **The M(Q) vs Hessian distinction** should have been clarified at the MISSION level. Mission statements must precisely specify which mathematical object to bound, with reference to the source paper's exact definition.
