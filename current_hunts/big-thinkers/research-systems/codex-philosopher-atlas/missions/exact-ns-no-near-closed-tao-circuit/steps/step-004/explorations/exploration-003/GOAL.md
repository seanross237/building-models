# Exploration 003 Goal - Build The Pro-Circuit Dossier And Decide Step-5 Readiness

## Objective

Using the same frozen family ledger and pass/fail sheet from
`exploration-001`, build the construction-facing Step-4 dossier for the
pro-circuit families and then decide whether Chain Step 5 is now well posed as
one honest repair pass.

The dossier must test the three surviving candidates on fixed explicit families
covering:

- engineered helical sign patterns
- sparse triad geometries
- scale-separated packets
- families where leakage exists but may be dynamically negligible

## Required Output

Produce a report that does all of the following:

1. Records the exact interaction data used on each pro-circuit family:
   helical coefficient/sign ledger,
   desired-channel forcing,
   classwise spectator forcing,
   and event-time traces where relevant.
2. Applies the same admissibility filters and thresholds from
   `exploration-001` without retuning.
3. Reports, for each candidate on each pro-circuit family, whether the
   candidate passes, fails, or remains ambiguous.
4. Compares the pro-circuit outcomes against the anti-circuit dossier from
   `exploration-002` without changing the burden currency.
5. States whether Step 5 is well posed, and if so which candidates move into
   the one honest repair pass and what exact issue each repair may address.

## Success Criteria

- The report gives a balanced exact-packet comparison rather than only a
  negative obstruction memo.
- Any positive evidence is scoped to the fixed packet families and does not
  overclaim theorem consequences.
- The final Step-5-readiness verdict is explicit:
  either one repair pass is well posed,
  or the branch should stop at Step 4 with the sharpest earned negative memo.

## Failure Criteria

- The exploration fails if it rescues a candidate by changing the sign sheet,
  spectator partition, finite window, or thresholds after seeing a favorable
  family.
- It fails if it treats an engineered-sign or scale-separated family as a
  global near-circuit witness without comparing it against the anti-circuit
  dossier on the same ledger.
- It fails if the Step-5-readiness verdict is vague about what a repair may or
  may not change.

## Key Local Context

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-001/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-004/explorations/exploration-002/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/refined/chain-03.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-001-REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `library/factual/exact-ns-tao-circuit-near-closure-screening/step-4-is-well-posed-because-two-candidates-are-stable-after-canonicalization-and-the-third-remains-an-honest-admission-filter.md`

## Constraints

- Do not reopen broad mission planning.
- Do not start the Step-5 repair pass itself.
- Keep the final verdict inside the Step-4 buckets:
  `survives`,
  `fails`,
  or
  `remains ambiguous`,
  with one named reason each.
