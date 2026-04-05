# Exploration 001 Summary

## Goal

Identify a very small candidate family of exact phase/coherence objects built
from exact Fourier or helical interaction data, then classify each candidate as
`intrinsic`,
`canonically representable but non-intrinsic`,
or
`inadmissible`
under an explicit equivalence and admissibility test.

## What I Tried

- Read the Step-1 mission brief and the winning-chain / intrinsic-audit
  planning notes first.
- Pulled the predecessor mission's exact-NS support and canonicalization rules
  to define the allowed quotient operations honestly.
- Proposed three candidate classes directly on exact helical/Fourier triad
  data and screened each one against conjugation, helical-basis conventions,
  gauge choices, normalization changes, and forbidden desired-channel labels.

## Outcome

`succeeded`

## One Key Takeaway

The best surviving intrinsic object is the exact triad interaction phase class
`P_[k,p,q](u) = Gamma_{k,p,q}(u) / |Gamma_{k,p,q}(u)|`
on the mirror triad class.
The raw interaction scalar `Gamma_[k,p,q](u)` is exact but only
canonically representable after freezing normalization, and any family/window
coherence object is inadmissible at Step 1 because it imports external
annotation.

## Leads Worth Pursuing

- Carry the intrinsic object forward as a finite ledger of triad-local phase
  classes on exact closed supports, not as a one-number score.
- Let later steps build support-level or time-window diagnostics only after the
  support and dynamics are frozen.
- Use the surviving intrinsic object to test whether closure-forced spectator
  triads destroy compatibility of the active `P_[k,p,q]` values before any
  delayed-transfer event can land.

## Unexpected Findings

- The exact survivor is smaller than the planning prose first suggests:
  a single triad-local phase class already survives the admissibility quotient,
  so support-level aggregates are downstream diagnostics, not the primary
  object.
- The predecessor mission's packet-support canonicalization rules are still
  useful here, but only as equivalence discipline, not as the object being
  promoted.

## Computations Worth Doing Later

- Derive the exact evolution law for the active triad-local phase classes on
  the smallest recursively closed supports that survive Step 2.
- Compare those intrinsic phase classes against later support-level or
  time-window summaries to see which compatibility information gets lost in
  aggregation.
