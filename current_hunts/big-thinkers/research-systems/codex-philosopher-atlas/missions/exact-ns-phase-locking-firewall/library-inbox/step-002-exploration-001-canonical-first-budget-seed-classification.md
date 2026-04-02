# Exploration 001 Report - Canonical First-Budget Seed Classification

## Goal

Classify the canonical seed families at the first Step-2 budget:
one exact triad orbit as the seed object on the frozen canonical helical
support sheet, modulo the Step-1 equivalence and admissibility rules.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-002/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/REASONING.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/HISTORY-OF-REPORT-SUMMARIES.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-002.md`
- `missions/exact-ns-phase-locking-firewall/MISSION.md`
- `missions/exact-ns-phase-locking-firewall/CHAIN.md`
- `library/factual/navier-stokes/INDEX.md`
- `library/factual/navier-stokes/exact-support-search-object-is-a-finite-canonical-helical-support-sheet-with-mandatory-conjugate-completion.md`
- `library/factual/navier-stokes/packet-audits-must-separate-true-symmetries-canonicalization-and-substantive-model-changes.md`
- `library/factual/exact-ns-phase-locking-firewall/coefficient-corrected-triad-phase-orbit-ledger-is-the-best-current-intrinsic-object.md`

## Operational Note

- `[VERIFIED]` The strategizer launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-002-explorer-001`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` No summary sentinel landed during a bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Frozen Equivalences To Respect

- `[VERIFIED]` Step 1 froze the first-budget search object as one exact triad
  orbit on a finite canonical helical support sheet with mandatory conjugate
  completion, not as a packet-role object.
- `[VERIFIED]` Step 1 also froze the admissible quotient operations:
  triad-orbit relabeling,
  real-valued conjugate completion,
  helical-sign relabeling,
  gauge conventions,
  and normalization / canonicalization changes that do not alter the exact
  support object.
- `[VERIFIED]` The controller memo for `decision-002` explicitly asks Step 2 to
  classify the first-budget seed families for one exact triad orbit and then
  audit recursive closure on that catalog.

## Excluded Non-Seeds

### 1. Repeated-wavevector seeds

- `[INFERRED]` If `p = q`, then the ambient exact interaction scalar from
  Step-1 Exploration 001,

  ```text
  Gamma_{k,p,q}(u)
    := -i overline{u^(k)} · [ (q · u^(p)) P_k u^(q) ],
  ```

  collapses because `q = p` and every divergence-free mode satisfies
  `p · u^(p) = 0`.
- `[INFERRED]` So a repeated-wavevector "triad" is not an honest exact active
  triad with nonzero projected coefficient at all.
- `[PROPOSED]` Status:
  `excluded from the first-budget catalog`.

### 2. Collinear seeds

- `[INFERRED]` If `p` and `q` are collinear, then `q · u^(p) = 0` for the same
  reason:
  a divergence-free Fourier mode at `p` is orthogonal to the line spanned by
  `p`, hence to any collinear `q`.
- `[INFERRED]` So a collinear wavevector triple cannot support the nonzero
  projected interaction coefficient required by the Step-1 seed definition.
- `[PROPOSED]` Status:
  `excluded from the first-budget catalog`.

## Honest First-Budget Seed Catalog

- `[INFERRED]` Every honest first-budget seed therefore has:
  1. a nonzero exact wavevector triad relation

     ```text
     k = p + q,
     p != 0,
     q != 0,
     p != q,
     p not parallel to q;
     ```
  2. one canonical representative ordering, taken here as

     ```text
     |p| <= |q|,
     ```

     with conjugation choosing the mirror class only once;
  3. one helical sign-sheet class modulo the frozen equivalences.

### Canonical sign-sheet families

- `[INFERRED]` After quotienting by:
  1. conjugation / mirror representative choice,
  2. global helical-sign relabeling,
  3. and the `p <-> q` symmetry inside the triad relation,
  the eight raw sign triples reduce to three canonical classes for the ordered
  tuple

  ```text
  (sigma_k, sigma_p, sigma_q):
  ```

  1. `(+++)`
  2. `(++-)`
  3. `(+--)`
- `[INFERRED]` The local record does **not** support collapsing `(++-)` and
  `(+--)` further without importing a stronger target/input permutation rule
  than Step 1 actually freezes, so this report keeps all three classes.

### Why this catalog is honest

- `[INFERRED]` Any honest first-budget seed with nonzero projected coefficient
  must first survive the nondegeneracy screen above, and every such seed then
  reduces to one ordered noncollinear wavevector triad plus one of the three
  sign-sheet classes.
- `[INFERRED]` This is not a cherry-picked subset:
  the only omitted cases are repeated-wavevector or collinear configurations
  that fail the exact-seed condition itself.
- `[INFERRED]` Isosceles versus scalene geometry is **not** treated as a
  separate seed family at this budget because the closure audit below depends
  only on
  `p != q`
  and noncollinearity, not on a finer shell-ratio split.

## Exploration Verdict

- `[INFERRED]` The first-budget catalog is well defined from the local record.
- `[INFERRED]` Honest Step-2 seed families are:
  nondegenerate one-triad helical seeds
  `k = p + q`
  on the canonical helical support sheet,
  with one of the three sign-sheet classes
  `(+++)`,
  `(++-)`,
  `(+--)`
  after quotienting the frozen equivalences.
- `[INFERRED]` Repeated-wavevector and collinear cases are not dead survivors;
  they are not first-budget seeds at all because the exact projected
  interaction coefficient is already zero there.

## Dead Ends / Rejections

- `[VERIFIED]` Packet-role catalogs were rejected because Step 1 froze support
  sheets, not packet identities, as the search object.
- `[INFERRED]` A sharper geometry split by shell ratio was rejected at this
  budget because the local record does not need it to distinguish the honest
  seeds from the excluded non-seeds or to run the closure audit.
