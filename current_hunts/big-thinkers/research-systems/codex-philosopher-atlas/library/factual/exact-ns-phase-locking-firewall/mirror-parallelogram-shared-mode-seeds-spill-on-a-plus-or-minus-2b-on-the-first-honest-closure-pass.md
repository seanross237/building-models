# Mirror Parallelogram Shared-Mode Seeds Spill On A Plus Or Minus 2b On The First Honest Closure Pass

Status: `INFERRED` current-budget closure verdict with `VERIFIED`
representative sign-sheet coefficient audit

For the mirror/parallelogram shared-mode seed family
`T_par(a,b) = {(a,b,a+b), (a,-b,a-b)}` with
`d := a+b`
and
`e := a-b`,
the conjugate-complete starting ledger is
`S_0 = {plus/minus a, plus/minus b, plus/minus d, plus/minus e}`.

On that ledger, the first economical off-orbit closure tests are
`(d, b) -> a+2b`
and
`(e, -b) -> a-2b`.
Both targets lie outside
`{plus/minus a, plus/minus b, plus/minus d, plus/minus e}`
unless the seed collapses into the already excluded repeated-wavevector or
collinear cases.

The representative coefficient audit at
`a = (1,0,0)`,
`b = (0,1,0)`
found that all `32/32` seed sign assignments remain live and all `32/32`
force at least one new target helical sector. One sample coefficient pair on
`(d, b) -> a+2b` is
`|C_+| = 0.473607`,
`|C_-| = 0.026393`.

So the tidy four-orbit mirror/parallelogram shared-mode picture also spills on
the first honest recursive-closure pass and does not define a finite fixed
point inside the frozen second budget.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-003-exploration-002-recursive-closure-and-spillover-audit.md`
