# Canonical One-Triad Seeds Spill Outside The First Budget On The First Honest Closure Pass

Status: `INFERRED` current-budget closure verdict

For the Step-2 first budget, every honest canonical seed from the frozen
catalog
`k = p + q`,
`p != q`,
`p not parallel to q`
spills outside the one-triad orbit on the first honest recursive-closure pass
once mandatory conjugate completion is enforced.

The mirror-complete active ledger starts at

`S_0 = { plus/minus k, plus/minus p, plus/minus q }`.

On that ledger, the exact full-pair closure rule already forces off-orbit
targets. The mirror-cross pair `(p, -q)` produces the new wavevector
`p - q`, while the forward pairs `(k, p)` and `(k, q)` produce
`2p + q` and `p + 2q`.
For every noncollinear honest seed, those wavevectors are nonzero and lie
outside the original triad orbit.

So the first closure-forced spectator ledger already contains, at minimum,

`plus/minus (p - q), plus/minus (2p + q), plus/minus (p + 2q)`,

and no live canonical sign-sheet class
`(+++)`,
`(++-)`,
or
`(+--)`
reaches a finite fixed point inside the one-triad budget.

This is only a current-budget negative.
It does not claim that one-triad seeds generate an infinite closure tower in
general, only that they do not stay inside the frozen first budget.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-002-recursive-closure-and-spillover-audit.md`
