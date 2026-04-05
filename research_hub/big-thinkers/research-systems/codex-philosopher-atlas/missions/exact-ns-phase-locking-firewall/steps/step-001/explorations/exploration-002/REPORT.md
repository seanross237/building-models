# Exploration 002 Report - Exact Search Class, Closure, And Escalation Freeze

## Goal

Freeze the exact search object and support class for Chain Step 2, together
with the recursive closure convention, spectator inclusion rule, admissible
enlargements, smallest-first ordering, and escalation ladder.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/winning-chain.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/refined/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/selected/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-02.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/judgments/chain-01.md`
- `missions/exact-ns-no-near-closed-tao-circuit/atlas-source/atlas-anatomy-exploration-002-REPORT.md`
- `library/factual/navier-stokes/INDEX.md`
- `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/conjugate-completion-is-mandatory-canonicalization-not-primary-packet-identity.md`
- `library/factual/navier-stokes/helical-signs-amplitude-normalization-and-phase-anchor-belong-to-the-frozen-packet-sheet.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`

## Operational Note

- `[VERIFIED]` The strategist launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-001-explorer-002`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-002/REPORT-SUMMARY.md`.
- `[VERIFIED]` The session wrote only an initial report skeleton within the
  bounded wait and did not produce the summary sentinel.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Working Notes

### Note 1 - Branch-level reset away from packet identity

- `[VERIFIED]` The inherited
  `library/factual/navier-stokes/support-means-a-role-labeled-helical-packet-with-mandatory-conjugate-completion.md`
  belongs to an older packet-centered mission family.
- `[VERIFIED]` The current chain and judgment explicitly reset this branch to
  finite Fourier/helical mode supports unless an exact invariant packet
  representation is written explicitly.
- `[INFERRED]` Packet notes remain useful here only as cautions about
  canonicalization versus substantive model changes. They do not freeze this
  branch's primary search object.

### Note 2 - The live branch-level requirements are uniform

- `[VERIFIED]` Recursive closure must be exact and genuinely recursive.
- `[VERIFIED]` Spectator channels belong in the closure audit from the start.
- `[VERIFIED]` "Smallest" must be explicit and negative claims must stay
  bounded to the budget actually searched.

## Frozen Search Object

- `[INFERRED]` The exact object Step 2 should enumerate is a **finite canonical
  helical support sheet with mandatory conjugate completion**.
- `[INFERRED]` Concretely, the primary seed object is a finite set `R` of
  helical representatives `(k, sigma)` on one frozen helical basis and one
  frozen conjugate-representative convention. Step 2 should not start from
  role-labeled packets or desired channels.
- `[INFERRED]` The realized exact support is not `R` alone. It is the
  recursively closed support generated from `R` after mandatory real-valued
  completion.
- `[INFERRED]` The underlying bare Fourier support is only a shadow ledger.
  Two supports with the same wavevector set but different helical sign sheets
  count as different exact objects for this branch.
- `[VERIFIED]` Why not packet-level identity:
  the branch documents explicitly warn that packet language is acceptable only
  if exact invariance is written explicitly, and the current task forbids
  silently letting Tao-role packet language override a support-level search.
- `[INFERRED]` Why not bare Fourier support:
  the local record repeatedly treats helical sign data as part of the exact
  coefficient and transfer law. Enumerating only wavevectors would erase
  branch-relevant distinctions before the exact audit even begins.
- `[INFERRED]` Allowed use of packet language:
  predecessor-mission packet families may be used as templates or fixtures only
  after translation into explicit helical support ledgers. They are not the
  search object itself.

## Closure Convention

- `[VERIFIED]` Recursive exact closure is mandatory. The current chain,
  refined chain, attack, and judgment all reject first-generation-only closure.
- `[INFERRED]` Frozen closure operator for a canonical seed `R`:
  1. form `S_0 = Comp(R)` by mandatory conjugate completion in the frozen
     helical representation;
  2. given `S_n`, inspect every ordered pair of active modes in `S_n`;
  3. for each exact triad relation `k = p + q` and each target helical sign
     `tau`, if the exact Leray-projected helical interaction coefficient for
     `((k, tau), (p, sigma), (q, rho))` is not identically zero, add
     `(k, tau)` and its conjugate completion to `S_{n+1}`;
  4. repeat until `S_{n+1} = S_n` or the support spills beyond the current
     budget.
- `[INFERRED]` Leray projection is part of the closure test itself. Step 2 must
  use the exact projected coefficient law, not a schematic support graph.
- `[INFERRED]` Any mode added at one stage immediately participates in the next
  closure pass against the entire active set. That is what "recursive" means in
  operational terms.
- `[INFERRED]` Repeated-mode or degenerate triad cases are not exemptions. If
  the exact coefficient is nonzero in the frozen representation, the mode is
  forced into the closure ledger.

## Spectator Inclusion Rule

- `[VERIFIED]` Spectators belong in closure from the start. The attack and
  judgment record makes this non-optional.
- `[INFERRED]` Step 2 should use one support ledger with three bookkeeping
  labels:
  `core seed`,
  `mandatory representation companions`,
  and
  `closure-forced spectators`.
- `[INFERRED]` The label `spectator` is descriptive only. It does not authorize
  pruning the mode from the exact support or from the later exact dynamics.
- `[INFERRED]` Any Step-2 candidate that writes reduced dynamics only for the
  desired core while leaving closure-forced spectators off-ledger should be
  rejected as a truncated model, not accepted as an exact survivor.

## Admissible Enlargements

- `[VERIFIED]` The branch needs at least one admissible enlargement rule, and
  the packet-audit note distinguishes real enlargements from silent model
  changes.
- `[INFERRED]` An admissible enlargement must preserve:
  the same exact object type,
  the same helical basis,
  the same conjugate-completion rule,
  the same recursive closure convention,
  and support-level identity with no Tao-role relabeling.
- `[INFERRED]` Mandatory enlargement rule 1:
  add one new independent helical representative to the seed ledger,
  keep shell span fixed if possible,
  then recompute full recursive closure from scratch.
- `[INFERRED]` Mandatory enlargement rule 2, used only after rule 1 is
  exhausted at fixed shell span:
  widen the shell-span budget by one occupied dyadic shell while preserving the
  same helical support semantics and closure rule, then recompute closure.
- `[VERIFIED]` Non-admissible moves:
  changing the helical sign sheet,
  changing the helical basis convention,
  switching to packet/grouped support identity,
  relaxing recursive closure,
  or redefining the support by desired channels or Tao roles.

## Smallest-First Ordering

- `[VERIFIED]` The planning record requires "smallest" to be explicit.
- `[PROPOSED]` Step 2 should order candidates lexicographically by the budget
  tuple

  ```text
  B = (N_closed, ShellSpan, Depth, ParamDim)
  ```

  where:
  `N_closed` is the number of independent canonical helical representatives in
  the fully recursively closed support, counting conjugate pairs once;
  `ShellSpan` is the occupied dyadic-shell span of that closed support;
  `Depth` is the number of closure iterations needed to reach the fixed point;
  and `ParamDim` is the residual dimension of the geometry/sign family after
  quotienting exact symmetries and frozen canonicalization choices.
- `[INFERRED]` The primary size coordinate must be `N_closed`, not raw seed
  size. Otherwise a tiny seed that explodes under closure could be mislabeled
  as "small."

## Escalation Ladder

- `[PROPOSED]` The explicit escalation ladder Step 2 should inherit is:
  1. exhaust canonical representatives of the current budget tuple `B`;
  2. inside the current `ShellSpan`, run the mandatory one-generator admissible
     enlargements and re-close recursively;
  3. if no survivor remains, increase `N_closed` by one and restart at the
     smallest available `ShellSpan`, `Depth`, and `ParamDim`;
  4. after that size rung is exhausted, increase `ShellSpan` by one occupied
     shell;
  5. only after smaller `N_closed` and `ShellSpan` rungs are exhausted should
     the search admit higher `Depth` or `ParamDim` families.
- `[INFERRED]` This ladder satisfies the branch requirement that failure remain
  class-limited unless it survives the declared escalation route.
- `[INFERRED]` The record does not justify freezing a more specific numeric
  first budget here. The honest freeze is the ordering axes and escalation rule,
  not an invented first nontrivial triad-cluster size.

## Exploration Verdict

- `[INFERRED]` Step 2 should enumerate finite canonical helical support sheets
  with mandatory conjugate completion and recursive exact closure.
- `[INFERRED]` Packet families remain diagnostic templates only, not primary
  support identity.
- `[INFERRED]` Spectator modes are part of the exact support ledger from the
  first closure pass onward.
- `[INFERRED]` The branch now has a concrete search object, closure rule,
  admissible enlargement policy, smallest-first ordering, and escalation ladder
  sharp enough for Step 2 to inherit without inventing new rules.

## Failed Attempts And Dead Ends

- `[VERIFIED]` The launched explorer did not finish a summary sentinel.
- `[INFERRED]` Retaining the predecessor mission's packet object as the primary
  search class was rejected because it would reintroduce role-labeled
  canonicalization at the object-definition stage.
- `[INFERRED]` Freezing a numeric first budget was also rejected because the
  local record names the relevant ordering axes but does not support one unique
  first nontrivial count sharply enough to freeze here without guesswork.
