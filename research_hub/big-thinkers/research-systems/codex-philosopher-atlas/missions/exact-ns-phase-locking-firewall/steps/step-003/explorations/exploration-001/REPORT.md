# Exploration 001 Report - Canonical Second-Budget Seed Classification

## Goal

Classify the canonical second-budget seed families for two-triad shared-mode
clusters under the frozen Step-1 equivalence rules and the Step-2 first-budget
exclusions.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-001/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/REASONING.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/REASONING.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-003.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-002-recursive-closure-and-spillover-audit.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-003-enlargement-audit-and-budget-limited-verdict.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-001/code/shared_mode_seed_catalog.py`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-001/code/output/shared_mode_seed_catalog_summary.txt`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/shared_mode_closure_audit.py`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/output/shared_mode_closure_audit_summary.txt`

## Operational Note

- `[VERIFIED]` The strategizer launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-003-explorer-001`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` No summary sentinel landed during a bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Working Notes

### Initial setup

- Created or repaired the report in place and then re-read the frozen Step-1
  equivalence sheet, the Step-2 rung-1 exclusions, and the controller memo
  before classifying second-budget seeds.
- Added reproducible artifact
  `code/shared_mode_seed_catalog.py`
  to make the overlap-type reduction explicit rather than relying only on
  diagram intuition.

## Findings

### 1. Frozen object and inherited exclusions

- `[VERIFIED]` The exact search object remains a finite helical support ledger
  with mandatory conjugate completion and recursive closure, not a packet-role
  family.
  Source:
  `steps/step-001/RESULTS.md`,
  `library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`.
- `[VERIFIED]` Step 2 already froze the rung-1 exclusions that carry forward
  here:
  repeated-wavevector and collinear pseudo-triads are not honest live seeds,
  and the six-wavevector one-triad picture
  `{ ±p, ±q, ±(p+q) }`
  is a dead pseudo-survivor rather than a reusable exact support.
  Source:
  `steps/step-002/RESULTS.md`,
  `steps/step-002/explorations/exploration-002/REPORT.md`,
  `steps/step-002/explorations/exploration-003/REPORT.md`.
- `[INFERRED]` So every honest second-budget seed must be a connected pair of
  **distinct** nondegenerate exact triad orbits.

### 2. Common-input normal form

- `[INFERRED]` Let `[v] := {v, -v}` denote one independent wavevector orbit up
  to conjugation.
  Take any two exact triad orbits sharing at least one orbit `[p]`.
  By the frozen triad-orbit relabeling and conjugation freedoms, each triad
  can be rewritten with `[p]` used as an input orbit.
- `[INFERRED]` Therefore every connected second-budget candidate admits the
  canonical ordered presentation

  ```text
  tau_1 : k = p + q,
  tau_2 : r = p + s,
  ```

  with the constituent live-triad conditions

  ```text
  p x q != 0,
  p x s != 0.
  ```

- `[INFERRED]` This is only a canonicalization layer.
  It does not make `p` intrinsically privileged.
  It only removes hidden representative choices before comparing families.

### 3. Abstract support classification

- `[VERIFIED]` The artifact
  `code/shared_mode_seed_catalog.py`
  classifies abstract pairs of triad orbits as pairs of 3-element supports with
  nonempty intersection, modulo vertex relabeling.
  Output:
  `code/output/shared_mode_seed_catalog_summary.txt`.
- `[VERIFIED]` That classifier finds exactly three overlap classes:
  1. intersection size `3`:
     same triad orbit twice;
  2. intersection size `2`:
     two distinct triads sharing two independent orbit classes;
  3. intersection size `1`:
     two distinct triads sharing exactly one independent orbit class.
- `[INFERRED]` Because the first class is not a genuinely new second triad, the
  honest connected second budget contains exactly **two** wavevector seed
  families.
  The disconnected intersection-size-`0` case is outside the current budget by
  definition.

### 4. Dead and out-of-budget pictures

- `[INFERRED]` **Disguised rung-1 repeat:**
  if the two triad orbits use only the same three independent wavevector
  orbits up to conjugation, then the second orbit is not genuinely new.
  Representative:

  ```text
  tau_1 : k = p + q,
  tau_2 : k = p + q.
  ```

  Status:
  `reject as disguised first-budget dead seed`.
- `[INFERRED]` **First-budget pseudo-support reuse:**
  any candidate contained entirely in

  ```text
  { [p], [q], [p + q] }
  ```

  only redraws the already-dead six-wavevector one-triad picture.
  Step 2 already ruled that object out.
- `[INFERRED]` **Disconnected add-on:**
  a two-triad pair with no shared independent orbit is not a shared-mode
  cluster and belongs to a later budget.
- `[INFERRED]` **Inert helical decoration:**
  adding extra helical sign sectors on wavevector orbits already present in one
  of the live wavevector families changes the exact helical sheet but does not
  create a third wavevector seed family.

### 5. Genuine second-budget family A - shared parallelogram

- `[INFERRED]` If the two triads share **two** independent wavevector orbits up
  to conjugation, then after relabeling they collapse to the canonical form

  ```text
  tau_1 : p + q -> k := p + q,
  tau_2 : p + (-q) -> r := p - q.
  ```

  Independent-orbit ledger:

  ```text
  { [p], [q], [p + q], [p - q] }.
  ```

- `[INFERRED]` This is the natural canonical form of the first forced
  shared-mode enlargement already hinted at by Step 2 through the orbit
  `p - q`.
- `[INFERRED]` Apparent alternatives such as

  ```text
  (p + q, p, q) together with (2p + q, p, p + q),
  (p + q, p, q) together with (q, p, q - p),
  ```

  are not new families.
  They are the same abstract intersection-size-`2` pattern after rechoosing
  which two orbit classes are regarded as the shared pair.
- `[INFERRED]` Status:
  `live canonical second-budget seed family`
  provided both constituent triads are nondegenerate.

### 6. Genuine second-budget family B - generic fan

- `[INFERRED]` If the two triads share **exactly one** independent wavevector
  orbit up to conjugation, then after relabeling they collapse to the
  canonical form

  ```text
  tau_1 : p + q -> k := p + q,
  tau_2 : p + s -> r := p + s,
  ```

  with independent-orbit ledger

  ```text
  { [p], [q], [s], [p + q], [p + s] }.
  ```

- `[INFERRED]` The defining condition is simply that the second triad is
  distinct and that its only shared orbit with the first is `[p]`.
  Any extra coincidence would drop the orbit count to `4` and move the seed
  into the shared-parallelogram family.
- `[INFERRED]` Shell ratio,
  angle data,
  and isosceles versus scalene placement remain continuous parameters **inside**
  this family rather than separate families at the current classification
  level.
- `[INFERRED]` Status:
  `live canonical second-budget seed family`
  provided both constituent triads are nondegenerate.

### 7. Helical-sheet remarks

- `[INFERRED]` A canonical seed family at this rung is therefore:
  one of the two wavevector families above,
  together with a helical sign assignment on the named seed modes of that
  representative ledger.
- `[VERIFIED]` The downstream Step-3 closure-audit scaffold already tests both
  representative families,
  `generic_fan` and `mirror_parallelogram`,
  across all `32/32` sign assignments used in that script, and every tested
  assignment remains a live seed.
  Source:
  `steps/step-003/explorations/exploration-002/code/shared_mode_closure_audit.py`,
  `steps/step-003/explorations/exploration-002/code/output/shared_mode_closure_audit_summary.txt`.
- `[INFERRED]` So no helical sign choice is excluded at seed admission here.
  Different sign sheets remain different exact helical supports,
  but they do **not** create a third shared-mode wavevector family or turn a
  disguised rung-1 picture into a genuinely new second-rung seed.

## Canonical Catalog

| Candidate picture | Canonical representative | Orbit count up to conjugation | Status | Decisive reason |
| --- | --- | --- | --- | --- |
| same triad orbit twice | `((p+q), p, q)` and `((p+q), p, q)` | `3` | `reject` | `[INFERRED]` no genuinely new triad orbit appears |
| disconnected two-triad pair | `((p+q), p, q)` and `((r+s), r, s)` with no shared orbit | `6` | `outside current budget` | `[INFERRED]` not a shared-mode cluster |
| shared parallelogram | `((p+q), p, q)` and `((p-q), p, -q)` | `4` | `live canonical family` | `[INFERRED]` two distinct triads share two orbit classes up to conjugation |
| generic fan | `((p+q), p, q)` and `((p+s), p, s)` with exact one shared orbit | `5` | `live canonical family` | `[INFERRED]` two distinct triads share exactly one orbit class |

## Failed Attempts / Dead Ends

- `[INFERRED]` The first common-input case split produced several apparently
  different four-orbit pictures:
  `s = -q`,
  `s = k`,
  `r = q`,
  `r = -k`,
  and related variants.
  The abstract overlap classifier showed that keeping these as separate
  families would only preserve hidden representative choices.
- `[INFERRED]` I did **not** promote helical-sign occupancy variants on a fixed
  wavevector family into separate seed families.
  That would confuse exact-object distinctness with the narrower task of
  canonical shared-mode family classification.

## Exploration Verdict

- `[INFERRED]` The honest connected second-budget catalog contains exactly two
  genuinely new wavevector seed families:
  the four-orbit **shared parallelogram** family and the five-orbit
  **generic fan** family.
- `[INFERRED]` Everything else at this rung is either:
  a disguised first-budget repeat,
  a disconnected add-on outside the shared-mode budget,
  or a helical-sheet decoration on one of those two underlying wavevector
  families.
- `[INFERRED]` The equivalence reductions are now explicit enough for
  Exploration 002 to cite them directly when running closure and spillover
  audits.
