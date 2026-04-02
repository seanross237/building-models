# Exploration 002 Goal - Recursive Closure And Spillover Audit

## Objective

Run the recursive exact closure audit on each canonical second-budget seed and
decide whether any seed reaches a genuine finite fixed point inside the
two-triad shared-mode budget.

## Success Criteria

- Track the closure order explicitly:
  conjugates,
  forced helical sectors,
  and newly forced nonzero triad interactions.
- Record the exact support ledger for every apparent survivor or the decisive
  spill / exactness-failure reason for every dead seed.
- Make the closure result concrete enough for a later enlargement audit.

## Failure Criteria

- The report leaves the first decisive new wavevector or sign-sector forcing
  ambiguous.
- The closure verdict depends on over-pruning spectators or suppressing active
  ordered pairs.

## Local Context

- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/code/closure_audit.py`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-003.md`

## Constraints

- Keep every closure-forced mode in the ledger immediately.
- Treat Step-2 one-triad spill modes as inherited clues, not as automatic
  proofs for every second-budget seed.
- Do not derive projected ODEs yet.
