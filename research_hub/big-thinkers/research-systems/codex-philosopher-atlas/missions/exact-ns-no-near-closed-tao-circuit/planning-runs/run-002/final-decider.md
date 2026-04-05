# Final Decision Memo - exact-ns-no-near-closed-tao-circuit / run-002

## Decision

Choose refined Chain 03 as the single execution winner.

Winning base text:
`refined/chain-03.md`

Canonical output:
`winning-chain.md`

## Why Chain 03 Wins

Chain 03 has the best overall next-step profile on the stated criteria.

- Highest presentable-result floor. Even failure is valuable and clean:
  exact non-isolability,
  forced packet growth,
  leakage overload,
  template drift,
  coefficient misordering,
  or timing collapse.
- Highest execution fit. It asks for one frozen witness on one frozen ledger,
  instead of first requiring family-level closure or a joint theorem-ready
  comparison sheet.
- Best novelty ceiling relative to cost. If `F_SS(1/12)` survives honest exact
  closure and dynamics while retaining both promoted Step-6 gates, that is
  more surprising and more presentable than a narrow calibration result.
- Strong useful floor on failure. A sharp constructive failure atlas directly
  narrows the live search space and strengthens later obstruction-side work.
- Clean staging. It does not depend on first settling the whole joint
  frontier, and it avoids the quantifier inflation that still shadows the
  broader synthesis and leakage-audit branches.

The judgment scores reinforce this choice:

- Chain 03 presentable-result estimate: `0.74`
- Chain 01 presentable-result estimate: `0.67`
- Chain 02 presentable-result estimate: `0.64`

## Why The Other Chains Lose

### Chain 01

Chain 01 is the right later synthesis branch, not the right next branch. Its
honest form still depends on closing two smaller exact ledgers before the
joint question becomes theorem-ready. That makes it more likely to end in a
bounded deferral memo than in a strong immediate result.

### Chain 02

Chain 02 has a respectable obstruction floor, but its most likely outputs are
currency audit, scope correction, or a narrow calibration/minimality memo. All
of those are useful, but they are less likely than Chain 03 to produce either
a visibly strong positive result or a vivid mission-shaping negative result in
the very next execution slot.

## Elements Merged Into The Winner

Two low-cost improvements from the losing chains should be carried into the
winning chain.

- From Chain 01: Step 1 must explicitly freeze the Step-6 authority sheet and
  log any earlier threshold drift, especially the leakage-side `L_cross`
  mismatch, rather than letting record ambiguity leak into the audit.
- From Chain 02: all leakage comparisons must remain in one frozen same-currency
  protocol, with no silent bookkeeping retuning during the dynamic test.

These additions improve rigor without widening the branch or damaging its
bounded constructive character.

## Execution Consequence

The next branch should therefore be a strict witness-local exact audit of
`F_SS(1/12)`, using only the promoted Step-6 gates `G_tmpl` and `G_leak` as
hard pass/fail criteria, forbidding discretionary repair, and packaging the
result symmetrically as either witness-local anti-obstruction evidence or a
constructive failure atlas.
