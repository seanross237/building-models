# Exploration 002 Summary - Audit The Three Step-2 Candidates And Decide Step-4 Readiness

## Goal

Audit the three promoted Step-2 candidates against the frozen Step-3 taxonomy
and decide whether Chain Step 4 is now well-posed.

## What Was Tried

- checked the Step-1 packet-language and feature freezes
- checked the Step-2 candidate sheets, interaction templates, and downstream
  gates
- imported the Step-3 taxonomy from `exploration-001`
- tested each candidate against the three required tiers:
  true exact symmetries,
  canonicalization dependence,
  and substantive model drift

## Outcome

- `[INFERRED]` `Template-Defect Near-Closure` is
  `stable after canonicalization`.
- `[INFERRED]` `Windowed Spectator-Leakage Budget` is
  `stable after canonicalization`.
- `[INFERRED]` `Delayed-Threshold Itinerary` is
  `use-case-limited but honest`.
- `[VERIFIED]` No Step-3 kill condition fired.
- `[VERIFIED]` Chain Step 4 is now well-posed.

## Key Takeaway

The robustness audit does not collapse the candidate family. It sharpens it:
two candidates survive as canonicalization-stable exact packet objects, while
the itinerary candidate survives only as a narrow finite-window admission
filter.

## Final Robustness Matrix

| Candidate | Classification | Short reason |
| --- | --- | --- |
| `Template-Defect Near-Closure` | `stable after canonicalization` | the defect observable depends on one frozen packet sheet, not on post hoc packet rewrites |
| `Windowed Spectator-Leakage Budget` | `stable after canonicalization` | the main robustness burden is the frozen spectator partition and normalization, not hidden model drift |
| `Delayed-Threshold Itinerary` | `use-case-limited but honest` | the candidate is genuinely finite-window and sheet-dependent, but those limits were frozen up front |

## Leads Worth Pursuing

- `Windowed Spectator-Leakage Budget` should be the first Step-4 obstruction gate
  because it keeps the cleanest same-currency exact leakage ledger.
- `Template-Defect Near-Closure` should be the parallel Step-4 role-template
  audit because it is the best theorem-facing exact comparison object once the
  packet sheet is fixed.
- `Delayed-Threshold Itinerary` should be kept only as a construction-facing
  admission filter with no threshold or window retuning.

## Unexpected Findings

- The robustness audit did not force any Step-2 candidate into
  `fatally arbitrary`.
- The behavior-based itinerary candidate survives only because Step 1 and Step 2
  had already frozen the sign/phase sheet, spectator screen, and finite window.

## Computations Worth Doing Later

- compute the exact helical coefficient and sign ledger for the fixed
  pro-circuit and anti-circuit packet families used by
  `Template-Defect Near-Closure`
- compute the closed interaction ledger and classwise leakage ratios on the same
  normalized packet families for `Windowed Spectator-Leakage Budget`
- compute fixed-window event-time traces with frozen thresholds and no retuning
  for `Delayed-Threshold Itinerary`

## Step-4 Readiness

- `[VERIFIED]` Chain Step 4 is now well-posed.
- `[INFERRED]` Surviving candidates for Step 4:
  `Template-Defect Near-Closure`,
  `Windowed Spectator-Leakage Budget`,
  `Delayed-Threshold Itinerary`.
