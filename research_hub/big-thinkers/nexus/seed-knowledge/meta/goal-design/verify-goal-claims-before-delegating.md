---
topic: Verify goal claims before delegating to an explorer
category: goal-design
date: 2026-03-28
source: "yang-mills s003-meta-exploration-005, yang-mills s003-meta-exploration-s003-007"
---

## Lesson

Before writing a GOAL.md that cites a prior exploration's result (e.g., "M(Q) ≼ M(I) confirmed by E004"), the strategizer must verify that the cited claim actually matches what the exploration found. Incorrect goal framing wastes exploration budget: the explorer either attempts to prove something false, or must first discover the error and then pivot.

## Evidence

- **yang-mills strategy-003 exploration-005** — The GOAL.md stated "M(Q) ≼ M(I) confirmed numerically (E004)." This was wrong: E004 only confirmed λ_max(M(Q)) ≤ 4d (spectral radius bound), NOT the full operator ordering M(Q) ≼ M(I). The explorer had to discover and correct this error, wasting significant effort before pivoting to the correct target.

- **yang-mills strategy-003 exploration-007** — Same false goal (prove M(Q) ≼ M(I)). The explorer spent significant effort on four approaches (A/B/C/D) before confirming the target was false. A quick numerical sanity check (5 lines of Python: compute eigenvalues of M(Q)−M(I) for 3 random Q) would have caught this immediately.

## Two-Level Fix

### Level 1: Strategizer Verification

Before writing a GOAL.md that cites a prior result, re-read the relevant REPORT.md (or REPORT-SUMMARY.md) and verify:
- Does the claim match what was actually proved/computed?
- Is the statement the same or strictly weaker than what's being cited?
- Could there be a stronger reading the strategizer is inadvertently importing?

**Specific anti-pattern:** Confusing λ_max(A) ≤ λ_max(B) (scalar bound) with A ≼ B (operator ordering). These are very different mathematical statements.

### Level 2: Explorer Pre-Screening

For proof explorations, include in GOAL.md:

> "First: compute X for 3-5 random examples. If X fails in any example, the claim is FALSE — do not attempt to prove it. Instead, characterize when and why it fails, and identify the correct (weaker) statement."

This costs ~5 minutes and prevents the explorer from spending an entire exploration on a false target.

## Relationship to Other Patterns

- Distinct from **preload-context-from-prior-work.md** (which is about providing prior findings, not verifying them)
- Distinct from **include-trivial-control-checks.md** (which is about validating computation correctness, not goal correctness)
- Complements **specify-failure-paths.md** (which tells the explorer what to do if the goal fails; this entry is about preventing the goal from being wrong in the first place)

## Variant: Define Key Mathematical Objects at MISSION Level

When a mission involves bounding or proving properties of a specific mathematical operator, define that operator with an **exact formula** at the MISSION or strategy level — not just by name. Ambiguity in operator definition can waste multiple explorations.

- **yang-mills-conjecture strategy-002 exploration-007** — The distinction between M(Q) = Σ B_□^T B_□ (the "covariant curl squared") and the Wilson action Hessian H(Q) was not clarified at the MISSION level. The two operators differ by a curvature correction C(Q) that is NOT positive semidefinite: H(Q) = M(Q) − C(Q). This distinction was discovered in the 7th exploration of the second strategy. Had it been clarified upfront with exact formulas, explorations would have been properly targeted from the start, and the S002-E007 potential counterexample (which may stem from computing the wrong operator) would have been caught immediately.

**Template:** In MISSION.md or strategy-level GOAL.md, include:
> **Target operator:** M(Q) = Σ_□ B_□(Q)^T B_□(Q), where B_□(Q,v) = v₁ + Ad_{Q₁}(v₂) − Ad_{Q₁Q₂Q₃⁻¹}(v₃) − Ad_{U_□}(v₄) and Ad_g(v) = gvg⁻¹.
> **NOT:** the Wilson action Hessian H(Q) (which differs by a curvature correction).

## Variant: Verify Analytical Predictions Independently

**NEW variant: verify analytical predictions independently (yang-mills-validation E005):** When GOAL.md contains an analytical prediction (e.g., "H_norm ≤ 1/18 for SU(3)"), the explorer should re-derive it from first principles before using it as a sanity check target. E005: the goal predicted 1/18 (using N), but independent computation at Q=I gave 1/27 (using N²). The explorer correctly identified the discrepancy because it computed before checking. Anti-pattern: trusting GOAL.md formulas without re-derivation.
