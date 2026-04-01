---
topic: 4-step adversarial proof review structure with steelman and limitations query
category: goal-design
date: 2026-03-29
source: "barandes-stochastic strategy-001 meta-exploration-005, yang-mills-conjecture meta-exploration-007, yang-mills-conjecture strategy-002 meta-exploration-006"
---

## Lesson

For adversarial reviews of a **specific proof** (as opposed to multi-claim synthesis reviews), use a 4-step structure in the goal: (1) trace the proof step by step, (2) identify the key assumption, (3) check whether that assumption is derived or imported, (4) check prior art for the same result. This structure produced a clear, definitive circularity analysis in barandes-stochastic E005.

## The 4-Step Structure

1. **Trace the proof step by step** — Write out every assumption and inference. Forces the explorer to engage with the actual mathematics, not a summary.
2. **Identify the key assumption** — Which single assumption does the most work? Name it explicitly. (In E005: the unistochastic assumption = Born rule QM.)
3. **Check if derived or imported** — Is this assumption derived from the framework's axioms, or imported from standard QM? This is the circularity test. Ask specifically: "is [X] assumed or derived?"
4. **Check prior art** — Has the same result been proved before from similar or different assumptions? List specific papers to check but add "and any others you find."

## Steelman Requirement

**Always require a steelman when the adversarial review is likely to produce a negative result.** Without being forced to construct the best case, the explorer will stop at "it's circular/it's known/it fails." The steelman often contains the most nuanced and accurate assessment.

In E005, the steelman produced the "Level 2+" classification — more accurate than either the raw adversarial ("it's circular") or the original constructive exploration ("it's novel"). It also identified three concrete paths to Level 3 that the adversarial review alone would not have.

**Include "grade the steelman"** — this prevents the explorer from constructing either a strawman or an uncritically strong defense. The grading was honest in E005.

## Ask About the Paper's Own Limitations

Include the specific question: **"Does the paper itself acknowledge limitations? Quote them."** This reveals the authors' awareness and honesty, which calibrates the overall assessment. In E005, the paper's own conclusion explicitly admitted it had not yet "bypassed the quantum side" — this was the most honest sentence in the paper and confirmed the circularity finding.

Explorers may find this independently, but making it a specific question ensures it's addressed.

## Variant: Check the Full Logical Chain

After verifying each proof step, **check the reduction chain from what's actually proved to what's claimed**. A proof may be internally correct (every algebraic step verified) yet fail to establish the full claim because the reduction from the proved statement to the target has gaps.

In yang-mills-conjecture E007: the 5-step algebraic proof for the per-vertex bound was correct (13 VERIFIED), but the chain from per-vertex bound → staggered mode bound → full operator bound had a gap. The proof established staggered mode Rayleigh quotient <= 4d, but the full conjecture requires lambda_max(M(Q)) <= 4d for ALL eigenvectors (the 9-dimensional top eigenspace contains 6 non-staggered modes not covered by the per-vertex argument).

**Specific sub-lesson for matrix inequalities:** When a proof claims an operator norm bound (lambda_max <= C) but actually proves a quadratic form bound (v^T M v / |v|^2 <= C for v in a subspace), verify that the subspace covers the full eigenspace. The two statements are equivalent only when the subspace includes ALL top eigenvectors.

**Add as Step 5 to the 4-step structure:** (5) Check whether the proved statement actually implies the claimed conclusion, or only a weaker version.

## Variant: Structure First, Computation Second

**Check the logical structure of the proof chain BEFORE investing in computational verification.** The most important gaps are structural (does the proved statement imply the claimed conclusion?) not computational (are the arithmetic steps correct?). In yang-mills-conjecture S002-E006, an independent adversarial review found that all B1-B9 identities were computationally correct (errors < 3e-12) — but the structural gap (staggered bound ≠ full lambda_max bound) was the critical finding. Sequencing logical chain analysis first would have identified the gap earlier and saved verification effort.

**Prioritization for adversarial proof reviews:** (1) Check logical chain (proved ⇒ claimed?), (2) Check structural assumptions, (3) Computational verification of individual steps.

## Distinction from Other Adversarial Entries

- **adversarial-synthesis-goal-structure** — Multi-claim finishing-strategy review (different scope: reviewing ALL claims across strategies vs. reviewing ONE proof)
- **adversarial-explorations-need-null-hypothesis** — Content requirement for adversarial explorations (what to test), not structural format
- **adversarial-check-between-phases** — Timing of adversarial checks (when to run), not how to structure them

## Evidence

- **barandes-stochastic E005** — The 4-step structure + steelman produced a definitive circularity analysis of the Tsirelson claim, graded steelman arguments honestly, and identified specific Level 2→3 transition conditions. Asking about Theta ("is it assumed or derived?") gave the explorer a specific target with a clear, definitive answer. The steelman was essential: without it, the verdict would have been "it's circular" rather than the more accurate "Level 2+ with genuine explanatory value."
