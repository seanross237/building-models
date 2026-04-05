# Exploration 002 Goal - Exact Search Class, Closure, And Escalation Freeze

## Objective

Freeze the exact search object and support class for this branch, together with
the closure convention, admissible enlargements, smallest-first ordering, and
explicit escalation ladder that Chain Step 2 must inherit.

The report must answer:

- what exact object Step 2 is allowed to enumerate:
  finite Fourier supports,
  finite helical supports,
  or a sharper justified alternative;
- how recursive exact closure is defined, including conjugate completion,
  Leray-projection effects, and all newly forced triad interactions;
- how spectator modes are included from the start rather than treated as late
  diagnostics;
- what counts as an admissible enlargement rather than a silent change of
  model; and
- what smallest-first ordering and escalation ladder Step 2 must follow.

## Success Criteria

- The report freezes one exact search object with no hidden packet relabeling.
- Recursive closure and spectator inclusion are explicit enough for Step 2 to
  run an audit without inventing new rules.
- At least one admissible enlargement rule and one escalation ladder land in
  concrete terms.

## Failure Criteria

- The search object still depends on packet-style cherry-picking.
- Closure is only first-generation rather than recursive.
- The enlargement rule or smallest-first ordering remains too vague to control
  later negative claims.

## Relevant Context

- `missions/exact-ns-phase-locking-firewall/steps/step-001/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-02.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/selected/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `library/factual/navier-stokes/INDEX.md`
- `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`

## Constraints

- Do not enumerate actual recursively closed survivors yet.
- Do not derive exact reduced dynamics yet.
- Do not treat spectator channels as optional late-stage bookkeeping.
- Do not let Tao-role packet language silently override a support-level search.

## Deliverables

- `REPORT.md`
- `REPORT-SUMMARY.md`
