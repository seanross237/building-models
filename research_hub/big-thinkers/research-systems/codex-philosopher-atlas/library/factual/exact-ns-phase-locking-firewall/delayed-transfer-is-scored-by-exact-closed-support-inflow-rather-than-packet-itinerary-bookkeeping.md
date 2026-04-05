# Delayed Transfer Is Scored By Exact Closed-Support Inflow Rather Than Packet-Itinerary Bookkeeping

Status: `INFERRED` metric freeze

The branch should score delayed transfer on one exact closed support `S` with
one predeclared partition `A / B / R`, where `R := S \\ (A union B)`, fixed
before any trajectory is judged.

For each `X subset S`, the scoring observable is

`J_X(t) = E_X(t) - E_X(0) + 2 nu int_0^t D_X(s) ds`,

with
`E_X(t) = sum_{m in X} |a_m(t)|^2`
and
`D_X(t) = sum_{m in X} |k_m|^2 |a_m(t)|^2`.

This makes `J_X` the exact cumulative nonlinear inflow into `X` after removing
viscous loss on the same subset.
The branch therefore measures transfer on the closed-support energy ledger
itself, rather than on packet-itinerary or route-labeled bookkeeping.

That freeze also forbids relabeling the target and spectator sets after a run
is seen, which keeps later positive and negative claims on one invariant
partition.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-003-metric-sheet-and-step-2-readiness-verdict.md`
