# Admissible Enlargement Of The Four-Orbit Mirror-Parallelogram Cluster Shows It Is Only An Over-Pruned Second-Budget Pseudo-Survivor

Status: `INFERRED` artifact-check verdict with `VERIFIED` admissible
enlargement policy

The second-budget mirror / parallelogram cluster

`S_par = { plus/minus a, plus/minus b, plus/minus (a+b), plus/minus (a-b) }`

is not a genuine finite exact support on this branch.
It only looks stable if the first closure-forced orbit
`a+2b`
or
`a-2b`
is suppressed after the Step-3 closure audit.

The admissible artifact check is to restore one such forced orbit, for example

`plus/minus (a+2b)`,

while keeping the same support semantics, helical basis,
conjugate-completion rule, and recursive-closure convention, and then
recompute closure from scratch.

That enlargement does not rescue the cluster.
On the enlarged ledger, active ordered pairs such as
`(a+2b, b)` and `(a+2b, -a)` immediately force

`a+3b`

and

`2b`,

which lie outside the original four-orbit second-budget ledger.

So the mirror / parallelogram cluster is only an over-pruned pseudo-survivor.
Restoring its first forced orbit reproduces the same spillover instead of
producing a second-budget exact fixed point.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-003-exploration-003-enlargement-audit-and-budget-limited-verdict.md`
