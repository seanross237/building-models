# Exploration 003 Goal - Enlargement Audit And Budget-Limited Verdict

## Objective

Using the closure audit from Exploration 002, run the required admissible
enlargement check on any apparent first-budget survivor, or package a clean
budget-limited negative if no honest survivor remains.

The report must answer:

- what apparent survivor, if any, still looks alive after the closure pass;
- what admissible enlargement test is applied to it and what happens after
  closure is recomputed from scratch;
- whether any genuinely invariant finite support remains for Chain Step 3; and
- what budget-limited verdict controller should inherit.

## Success Criteria

- Every apparent survivor gets an explicit enlargement audit.
- The final verdict is either one frozen survivor ledger for Step 3 or one
  sharp first-budget obstruction memo.
- The verdict is class-limited and does not self-escalate to the next budget.

## Failure Criteria

- The report promotes a cosmetically tidy but over-pruned support.
- Enlargement changes the object class instead of staying inside the frozen
  support semantics.
- The final verdict overclaims beyond the first budget.

## Relevant Context

- `missions/exact-ns-phase-locking-firewall/steps/step-002/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-002.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-003/REPORT.md`
- `library/factual/navier-stokes/admissible-enlargements-must-preserve-support-semantics-and-recompute-recursive-closure-from-scratch.md`
- `library/factual/navier-stokes/smallest-first-exact-support-searches-should-order-by-closed-size-shell-span-depth-and-family-dimension.md`

## Constraints

- Do not start the next budget.
- Do not derive ODEs.
- Keep the final claim at the current budget only.

## Deliverables

- `REPORT.md`
- `REPORT-SUMMARY.md`
