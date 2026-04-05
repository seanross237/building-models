# Exploration 002 Goal - Audit The Three Step-2 Candidates And Decide Step-4 Readiness

## Objective

Use the frozen Step-3 taxonomy from `exploration-001` to audit the three
promoted Step-2 candidates:

- `Template-Defect Near-Closure`
- `Windowed Spectator-Leakage Budget`
- `Delayed-Threshold Itinerary`

For each candidate, decide:

- which parts of the candidate are invariant under the true exact-symmetry
  tier
- which dependencies on frozen canonicalization are acceptable
- which sensitivities are honest use-case limits
- which sensitivities would be fatal signs of arbitrariness, circularity,
  threshold gerrymandering, or averaged-model importation

Then produce one exact classification for each candidate:

- `symmetry-stable`
- `stable after canonicalization`
- `use-case-limited but honest`
- `fatally arbitrary`

and decide whether Chain Step 4 is now well-posed.

## Success Criteria

- Each of the three promoted candidates receives exactly one of the four
  robustness classifications.
- The report separates:
  true-symmetry instability,
  canonicalization dependence,
  and substantive model drift.
- The report states explicitly which Step-1 and Step-2 freezes are doing real
  work for each candidate.
- The report states whether each Step-2 downstream gate remains meaningful
  after the robustness audit.
- The report names the exact missing data Step 4 would need next for each
  surviving candidate.
- The report ends with a clean verdict:
  `Chain Step 4 is now well-posed`
  or
  `the branch should stop here`,
  together with the earned negative failure bucket if the step fails.

## Failure Criteria

- Any candidate is left at slogan level rather than receiving one concrete
  robustness classification.
- The report mixes canonicalization dependence with substantive model changes.
- A candidate is rescued by changing packet semantics, spectator partitions,
  thresholds, time windows, or Tao-like features after the fact.
- The report softens the conclusion into one aggregate score instead of an
  explicit candidate-by-candidate matrix.

## Required Local Context

- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/GOAL.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-001/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/RESULTS.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-no-near-closed-tao-circuit/steps/step-003/explorations/exploration-001/REPORT-SUMMARY.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-001-feature-ledger.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-001-exploration-002-packet-language-memo.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-001-candidate-family.md`
- `missions/exact-ns-no-near-closed-tao-circuit/library-inbox/step-002-exploration-002-interaction-templates-and-gates.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/controller/decisions/decision-005.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`
- `library/factual/tao-circuit-feature-ledger/destroyed-by-averaging-means-loss-under-averaged-circuit-freedoms-not-under-canonical-relabeling.md`
- `library/meta/obstruction-screening/a-tao-screen-can-be-operational-on-an-exact-but-noncoercive-ledger-if-it-is-only-used-as-an-admission-filter.md`
- `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`

## Constraints

- Use only local repository materials.
- Do not run the full normalized packet dossier from Step 4.
- Keep the packet object fixed:
  the canonical one-bridge role-labeled helical packet family with mandatory
  conjugate completion.
- Keep the shared five-channel interaction core fixed.
- Do not invent new candidate notions unless the only honest conclusion is that
  one Step-2 candidate splits for a sharply stated robustness reason.
- If the branch should stop, use only the allowed negative buckets:
  `not well-defined`,
  `not robust after canonicalization`,
  or
  `not useful for the target theorem or counterexample question`.

## Output

Write:

1. `REPORT.md` containing:
   - the candidate-by-candidate robustness audit
   - one exact robustness classification per candidate
   - a downstream-gate stability note for each candidate
   - the Step-4 readiness verdict
2. `REPORT-SUMMARY.md` containing:
   - goal
   - what was checked
   - outcome
   - one key takeaway
   - the final robustness matrix
   - whether Chain Step 4 is now well-posed
