# Exploration 002 Summary

## Goal

Run the recursive exact closure audit on each canonical one-triad first-budget
seed and decide whether any seed reaches a genuine finite fixed point inside
the current budget.

## What I Tried

- Started from the canonical live seed catalog from Exploration 001:
  `(+++)`,
  `(++-)`,
  `(+--)`
  on a nondegenerate noncollinear triad
  `k = p + q`.
- Applied the frozen Step-1 closure rule in order:
  mandatory conjugate completion first,
  then every ordered pair on the full active ledger,
  then every nonzero forced target mode with its conjugate completion.
- Saved and ran
  `code/closure_audit.py`
  to evaluate the exact projected helical coefficient directly on one generic
  scalene triad and one equal-length noncollinear triad.

## Outcome

`succeeded`

## One Key Takeaway

No honest first-budget seed survives.
After mirror completion, the off-orbit pair `(p, -q)` already forces the new
wavevector orbit `±(p - q)`; representative exact coefficient checks also keep
both target helical sectors live there, so all three canonical sign-sheet
classes end with the same sharp status:
`budget spill`.

## Leads Worth Pursuing

- Treat Chain Step 3 as unearned at this budget. There is no one-triad exact
  survivor to inherit.
- If controller wants more than the current-budget negative, the next clean
  move is an explicit enlargement or next-budget decision, not a silent reuse
  of the cosmetically tidy mirror-complete triad.
- If later work revisits these seeds, keep both target helical sectors live on
  the first new wavevector orbits
  `±(p - q)`,
  `±(2p + q)`,
  `±(p + 2q)`
  unless an exact pruning identity is written down.

## Unexpected Findings

- The equal-length noncollinear representative did not provide a cancellation
  loophole: the direct coefficient check still produced nonzero seed and
  off-orbit interactions in all three canonical sign-sheet classes.
- Self-pairs are not the source of the spill. The decisive forcing comes from
  distinct off-orbit pairs created by mandatory conjugate completion.

## Computations Worth Doing Later

- If controller escalates, rerun the same direct coefficient audit on the first
  admissible enlargement family so the next budget starts with a concrete
  sign-sector ledger rather than only a wavevector sketch.
- If controller wants a sharper theorem-style negative later, derive or import
  an exact symbolic formula for the projected helical coefficients on the
  forced targets instead of relying only on representative numeric checks.
