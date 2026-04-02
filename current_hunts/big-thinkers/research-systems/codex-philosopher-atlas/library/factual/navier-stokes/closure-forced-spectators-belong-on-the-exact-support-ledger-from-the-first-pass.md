# Closure-Forced Spectators Belong On The Exact Support Ledger From The First Pass

Status: `VERIFIED` spectator-inclusion requirement with `INFERRED` ledger
policy

Modes forced by recursive closure belong on the exact support ledger from the
start, even when they are not part of the desired core seed. The ledger may
label `core seed`, `mandatory representation companions`, and
`closure-forced spectators`, but those labels are bookkeeping only.

Once a spectator is closure-forced, it cannot be pruned from the support or
left out of later exact dynamics without turning the candidate into a truncated
model. A reduced system that keeps only the desired core while omitting
closure-forced spectators is therefore not an exact survivor of the same
search class.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`
