---
topic: Require pre-analysis sanity checks in matrix construction goals
category: goal-design
date: 2026-03-27
source: "riemann-hypothesis strategy-002 meta-exploration-001, yang-mills s003-meta-exploration-001"
---

## Lesson

For goals that construct matrices and then analyze their spectral statistics, include an explicit **pre-analysis sanity check step**: "Before running statistical analysis, verify that (a) the matrix is Hermitian and non-degenerate (no all-zero eigenvalue sets), and (b) the spacing distribution looks roughly bell-shaped — if either check fails, stop and diagnose."

Without this, explorers proceed through full statistical analysis on degenerate or structurally trivial matrices (e.g., all eigenvalues = 0), producing meaningless numerical outputs that appear to be findings.

## Evidence

- **riemann-hypothesis strategy-002 exploration-001** — Two constructions (C2a/C2b: Dirichlet χ₄/χ₈ phases) failed silently at the construction level: the odd-character antisymmetric raw matrix Hermitianized to exactly zero (all 500 eigenvalues = 0). The exploration proceeded to compute spacing statistics — returning all spacings = 1.0 identically, and χ² = 190.7 against all distributions — before diagnosing the failure. A one-check "verify std(eigenvalues) > threshold" at construction time would have caught this immediately, saved compute, and prevented a row of garbage in the comparison table.

## What the Sanity Check Should Include

Include these steps in the goal explicitly:

1. **Hermitian structure:** Compute max|H − H†|; flag if > numerical tolerance.
2. **Non-degeneracy:** Verify std(eigenvalues) > 0.01 × mean|eigenvalues|. Flag if degenerate (e.g., all-zero from antisymmetric Hermitianization).
3. **Spacing distribution shape:** After unfolding, check that the spacing histogram is not uniform or all-zeros. β_rough = 0 (all spacings identical) or β_rough = negative immediately flags a construction failure.
4. **Eigenvalue count:** Confirm N valid eigenvalues were computed (no NaN/Inf).

Include in goal: "After constructing each matrix, verify non-degeneracy before running spectral statistics. If any matrix is degenerate (std(eigenvalues) near zero) or the spacing distribution is clearly wrong, report the construction failure and skip that variant."

## Variant: Verify Spectral Statistics Formula Against the Correct Finite-N GUE Range

For spectral rigidity Δ₃ and similar statistics with known finite-size corrections, **include a GUE-control sanity check in the goal**: "Verify the GUE control gives Δ₃_sat in the expected finite-N range before analyzing experimental ensembles." This catches subtle formula bugs and prevents false anomaly claims from comparing against the wrong (infinite-N) baseline.

**Critical finite-N vs. infinite-N distinction (verified, N=500):**
- Infinite-N GUE theory: Δ₃_sat ≈ 0.566 at L≈37
- Finite-size N=500 GUE: Δ₃_sat ≈ 0.22–0.26
- These differ by ~2.3×. Comparing any matrix's Δ₃_sat against infinite-N theory produces spurious "anomalous rigidity" claims.

**Template for goal:** "Run GUE control first. Verify Δ₃_sat ∈ [0.22, 0.26] for N=500. If outside this range, the formula is wrong — stop and diagnose before running other ensembles."

- **riemann-hypothesis strategy-002 exploration-009** — The GOAL.md formula (sampling Δ₃ at eigenvalue positions only, i.e., `mean(residuals²)/L`) underestimated Δ₃ by ~50×. The explorer independently diagnosed the bug because the GUE control gave Δ₃_sat ≈ 0.01 — impossible given the known finite-N range (~0.22–0.26). The sanity check served as both a quality gate and a debugging scaffold.

**Secondary lesson:** Explorers CAN self-diagnose subtle formula bugs when given expected-output context. The sanity check that catches the bug is more valuable than explicit error messages, because it lets the explorer identify the structural reason (staircase integration vs. residuals-only sampling).

**C1 rigidity retraction:** Prior explorations reported C1 Δ₃_sat = 0.285 as "anomalous" (50% of GUE). E009 showed: (a) the correct C1 value is 0.243 ± 0.017; (b) H_flat (no arithmetic) gives 0.256 ± 0.010; (c) GUE control gives 0.227 ± 0.010; (d) all three are indistinguishable. The "anomaly" was an artifact of comparing against infinite-N GUE theory. *From RH s002-meta-009.*

## When to Apply

Any goal that (a) constructs a matrix from a formula or function, then (b) runs RMT spectral statistics on it. Especially important when testing multiple constructions in one exploration — a silent failure in one construction produces a confusing row in the comparison table and can consume debugging time.

Applies broadly beyond matrix RMT: any pipeline with "construct object → run analysis" steps benefits from intermediate validity checks between stages.

## Variant: Verify Derived Formulas Against Finite Differences

When goals involve Hessian, tangent vector, or other differential formulas, include: "Verify the formula by computing d/dε [quantity] via finite differences (ε = 10⁻⁴) and comparing against the analytical expression." This catches formula transcription errors that are invisible at Q=I but cause spurious results for Q ≠ I.

- **yang-mills strategy-003 exploration-001** — The GOAL.md B_□ formula had incorrect transport matrices for backward edges 3 and 4. Finite-difference verification (error < 2×10⁻⁹) caught the error and identified the correct formula. Without this check, subsequent explorations would have produced spurious violations of the inequality at Q ≠ I.

**Template:** "After implementing the formula, verify against finite differences at one random configuration. Expected agreement: < 10⁻⁶. If mismatch, derive the correct formula from first principles before proceeding."

## Relationship to Other Lessons

Distinct from `specify-failure-paths.md` (which is about what to investigate if the overall approach fails). This is about a runtime check inserted between construction and analysis — a structural step in the goal's task sequence, not a fallback for overall failure.
