# Distinct Off-Orbit Pairs Not Self-Pairs Drive The First Budget Spill

Status: `INFERRED` first-spill mechanism read

For the canonical one-triad seeds on this branch, self-pairs are not the first
reason the support spills outside the one-triad budget.

In the Step-1 ambient exact interaction scalar,

`Gamma_(r,p,p)(u) = -i overline{u^(r)} dot [ (p dot u^(p)) P_r u^(p) ]`,

divergence-free data give `p dot u^(p) = 0`.
So the self-pair `(p, p)` does not force `2p`, and the same obstruction read
applies to the corresponding same-wavevector doubling pairs.

The decisive first spill instead comes from distinct off-orbit pairs created
by mandatory conjugate completion.
On the mirror-complete ledger, `(p, -q)` already forces `p - q`, with
`(k, p)` and `(k, q)` giving backup off-orbit targets.

So the tidy six-mode picture
`plus/minus p, plus/minus q, plus/minus k`
fails because it ignores mirror-cross pairs that the frozen exact closure rule
requires, not because self-doubling had already enlarged the support.

Filed from:
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-002-recursive-closure-and-spillover-audit.md`
