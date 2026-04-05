# Robustness Audits May Keep Several Honest Survivors With Different Statuses

When a frozen candidate slate is audited for robustness, do not force a
single global veto or a single survivor.
A tiered audit can honestly return several survivors on the same ledger with
different statuses, such as `stable after canonicalization` for candidates
whose dependence sits entirely in a predeclared packet sheet and
`use-case-limited but honest` for candidates that survive only on a narrower
fixed-window problem.

The point of the audit is to make each burden explicit, not to pretend that
every non-symmetry-free survivor has the same failure mode.
This works best when the candidate table is kept fixed and each candidate
keeps its own downstream gate instead of drifting into a pure representation
argument.

Filed from:
- `missions/exact-ns-no-near-closed-tao-circuit/meta-inbox/meta-step-003-exploration-002.md`
