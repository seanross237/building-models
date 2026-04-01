# Exploration 002 Goal

## Objective

Fix the compatible solution class, theorem-hypothesis constraints, and one
frozen localization protocol for the architecture selected in `exploration-001`.

This exploration must make the later estimate comparison honest: all exact
rewrites must be tested in the same weak-solution package and with the same
cutoff / projection / commutator bookkeeping.

## Inputs To Inherit

Assume `exploration-001` selects one final architecture and one named bad term.
If that exploration has not landed yet, work conditionally from the most likely
 choice:

- architecture:
  `local-energy flux/localization`
- provisional target:
  the localized cutoff-flux contribution in the local energy inequality.

## Required Questions

Answer all of the following from local repository sources:

1. What is the correct solution class for this audit?
   Likely options include:
   - suitable weak solutions,
   - Leray-Hopf weak solutions with LEI available,
   - or a stricter class if the chosen architecture forces it.
2. What theorem-hypothesis compatibility constraints are non-negotiable for the
   chosen architecture to make sense?
3. What is the first explicit circularity or package-mismatch risk?
   Examples:
   - smuggling in stronger regularity than the architecture starts with,
   - switching to a vorticity-only formulation that loses the LEI package,
   - or assuming projection identities that cease to be exact after
     localization.
4. What single localization protocol is fairest for the rewrite audit?
   This must fix:
   - cutoff placement,
   - localization region,
   - and where projection / Calderon-Zygmund / commutator costs are charged.
5. What would count later as an illegitimate mid-branch protocol change?

## Working Hypothesis To Test, Not Assume

The strategizer's provisional protocol is:

- solution class:
  `suitable weak solutions` in the Leray-Hopf energy class, with the local
  energy inequality available
- region:
  one parabolic cylinder `Q_r(x_*, t_*) = B_r(x_*) × (t_* - r^2, t_*)`
- cutoff:
  one standard nonnegative smooth cutoff `φ` supported in `Q_r`, equal to `1`
  on the inner half-cylinder, with `|∇φ| ~ 1/r` and
  `|∂_t φ| + |Δφ| ~ 1/r^2`
- bookkeeping:
  every candidate pays its own localization cost after insertion into the same
  cutoff package; any projection or CZ move after localization must pay the
  resulting commutator / nonlocality cost in the same ledger.

Confirm, refine, or reject this protocol from the source record.

## Success Criteria

- One solution class is fixed and source-justified.
- One frozen localization protocol is fixed in explicit enough detail that
  later steps cannot quietly alter it.
- One explicit package-mismatch or circularity risk is named.
- One sentence states what later would count as an illegitimate protocol
  change.

## Failure Criteria

- The chosen architecture cannot be stated honestly in one stable weak-solution
  package.
- The localization protocol remains ambiguous enough that candidate comparisons
  would be unfair.

If failure occurs, say so directly and explain whether the step should trigger
an early kill.

## Source Priorities

Use the local repository only. High-priority anchors:

- `missions/navier-stokes/library-inbox/ckn-1982-proof-architecture.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `missions/beyond-de-giorgi/planning-runs/run-003/refined/chain-01.md`
- `missions/beyond-de-giorgi/planning-runs/run-003/judgments/chain-01.md`
- `missions/beyond-de-giorgi/MISSION.md`
- `missions/beyond-de-giorgi/steps/step-001/RESULTS.md`
- `missions/beyond-de-giorgi/steps/step-004/RESULTS.md`
- `library/meta/exploration-goal-design/when-hidden-normalization-is-a-risk-start-with-the-least-adapted-localization-that-keeps-the-scenario-visible.md`
- any other local file that directly supports the chosen architecture

## Output Requirements

Write:

- `REPORT.md`
- `REPORT-SUMMARY.md`

Use source-based labels such as `[VERIFIED]`, `[INFERRED]`, and `[PROPOSED]`.
Keep the protocol concrete and narrow.
