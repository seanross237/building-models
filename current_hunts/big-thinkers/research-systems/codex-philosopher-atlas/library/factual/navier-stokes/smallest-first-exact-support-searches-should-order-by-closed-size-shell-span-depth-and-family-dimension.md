# Smallest-First Exact Support Searches Should Order By Closed Size Shell Span Depth And Family Dimension

Status: `VERIFIED` need for an explicit `smallest` rule with `PROPOSED`
budget ordering

When an exact-support search claims to test the `smallest` candidates first, it
should order canonical candidates by the closed-support budget tuple
`(N_closed, ShellSpan, Depth, ParamDim)`. Here `N_closed` counts independent
canonical helical representatives after full recursive closure, `ShellSpan`
measures occupied dyadic-shell span, `Depth` counts closure iterations to the
fixed point, and `ParamDim` records the residual family dimension after
quotienting exact symmetries and frozen canonicalization.

Negative claims should only escalate along that declared ladder: exhaust the
current tuple, run admissible one-generator enlargements inside the current
shell span and re-close, then increase `N_closed`, then `ShellSpan`, and only
after smaller rungs are exhausted admit higher `Depth` or `ParamDim`.
Otherwise the branch overstates how much of the class has actually been
searched.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`
