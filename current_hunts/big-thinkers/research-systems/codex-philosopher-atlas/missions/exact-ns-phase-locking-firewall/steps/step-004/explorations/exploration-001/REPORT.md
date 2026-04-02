# Exploration 001 Report - Canonical Third-Budget Seed Classification

## Goal

Classify the canonical connected three-triad repeated-wavevector cross-scale
seed families for the third budget under the frozen Step-1 equivalence rules
and the Step-2 / Step-3 lower-budget exclusions.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-004.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-002-recursive-closure-and-spillover-audit.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-003-exploration-001-canonical-second-budget-seed-classification.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-004/explorations/exploration-001/code/three_triad_seed_catalog.py`
- `missions/exact-ns-phase-locking-firewall/steps/step-004/explorations/exploration-001/code/output/three_triad_seed_catalog_summary.txt`

## Operational Note

- `[VERIFIED]` The strategizer launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-004-explorer-001`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` No summary sentinel landed.
- `[VERIFIED]` The launcher status file records
  `codex exec exited with status 1`,
  so this report is completed directly from the anchored local record and the
  local abstract-classification artifact.

## Findings

### 1. Frozen meaning of the current rung

- `[VERIFIED]` Step 1 froze the third rung of the escalation ladder as:

  ```text
  three-triad clusters with one repeated wavevector across two scales.
  ```

- `[VERIFIED]` Decision `decision-004.md` carries that wording forward and asks
  specifically for connected three-triad clusters with one repeated wavevector
  orbit across two distinct scale levels.
- `[INFERRED]` On the frozen support-sheet semantics, the clean current-budget
  interpretation is:
  **one repeated wavevector orbit up to conjugation is allowed as the defining
  reuse mechanism of the seed cluster**.
  If more than one orbit is repeated, the picture is no longer the declared
  single-repeated-orbit rung.

### 2. Abstract connected three-triad classes

- `[VERIFIED]` The artifact
  `code/three_triad_seed_catalog.py`
  enumerates connected unlabeled 3-edge support hypergraphs and finds exactly
  `9` abstract connected three-triad classes.
- `[VERIFIED]` Among those `9` classes, only one has degree sequence

  ```text
  [3,1,1,1,1,1,1].
  ```

  That is the unique class with exactly one repeated orbit and no second
  repeated orbit.
- `[INFERRED]` Connectedness explains the uniqueness:
  if a three-edge connected support graph has only one repeated orbit at all,
  that orbit must lie in **all three** seed triads.
  A degree-2 repeated orbit would only connect two triads and leave the third
  disconnected.

### 3. Canonical representative family

- `[INFERRED]` Every honest third-budget seed therefore reduces to one
  canonical wavevector family:

  ```text
  T_star(a,b,c,d)
    = { (a,b,a+b), (a,c,a+c), (a,d,a+d) }.
  ```

- `[INFERRED]` Here:
  1. `[a]` is the unique repeated orbit up to conjugation;
  2. `[b]`,
     `[c]`,
     `[d]`
     are pairwise distinct partner orbits up to conjugation; and
  3. the cross-scale condition is a parameter restriction inside this family:
     at least two distinct shell levels must appear among the partner or output
     orbits.
- `[INFERRED]` Shell span, angle data, and low-dimensional coincidence loci are
  continuous parameters inside this single star family.
  They do not create extra current-budget wavevector families unless they force
  a second repeated orbit.

### 4. What is not a genuine third-budget seed

| Candidate picture | Status | Decisive reason |
| --- | --- | --- |
| three-triad support on `4` or `5` orbits | `disguised lower-budget artifact` | `[INFERRED]` it adds no genuinely new support beyond the exhausted first / second budgets |
| any three-triad picture with a pair-intersection of size `2` | `outside current rung` | `[INFERRED]` a shared pair repeats at least two orbit classes, so the seed is no longer single-repeated-orbit |
| connected three-triad chain / cycle with degree sequence not equal to `[3,1,1,1,1,1,1]` | `outside current rung` | `[INFERRED]` more than one orbit is reused across the cluster |
| inert helical decoration on the same wavevector picture | `not a new seed family` | `[VERIFIED]` Step 1 froze finite helical supports as the exact objects, but extra sign occupancy on the same wavevector support does not create a new wavevector seed family |

- `[INFERRED]` Concrete excluded examples include:
  1. the mirror-augmented picture

     ```text
     { (a,b,a+b), (a,-b,a-b), (a,c,a+c) },
     ```

     because `[b]` also repeats; and
  2. any support entirely contained in the old four-orbit or five-orbit
     second-budget dead supports.

## Canonical Catalog

| Family | Canonical representative | Support size up to conjugation | Status | Decisive reason |
| --- | --- | --- | --- | --- |
| single-repeated-orbit three-arm star | `{ (a,b,a+b), (a,c,a+c), (a,d,a+d) }` | `7` | `live canonical family` | `[INFERRED]` unique connected three-triad class with exactly one repeated orbit |
| support-size `4` / `5` three-triad pictures | varies | `4` or `5` | `reject` | `[INFERRED]` lower-budget artifact or inert decoration |
| shared-pair / parallelogram-core add-ons | varies | `6` | `reject` | `[INFERRED]` repeats more than one orbit and recycles the exhausted shared-mode core |
| chain / cycle pictures with multiple reused orbits | varies | `6` or `7` | `reject` | `[INFERRED]` not the declared single-repeated-orbit rung |

## Exploration Verdict

- `[INFERRED]` The honest third-budget wavevector catalog has **one** canonical
  family only:
  the connected three-arm star with a single repeated orbit.
- `[INFERRED]` Any apparent extra family either:
  1. collapses back into the already exhausted first or second budgets; or
  2. repeats more than one orbit and therefore leaves the declared current rung.
