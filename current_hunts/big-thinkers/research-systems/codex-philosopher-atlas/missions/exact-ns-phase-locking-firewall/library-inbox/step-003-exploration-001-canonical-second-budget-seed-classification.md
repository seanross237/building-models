# Exploration 001 Report - Canonical Second-Budget Seed Classification

## Goal

Classify the canonical second-budget seed families for two-triad shared-mode
clusters under the frozen Step-1 equivalence rules and the Step-2 first-budget
exclusions.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/REASONING.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/REASONING.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-003.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-002-recursive-closure-and-spillover-audit.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-003-enlargement-audit-and-budget-limited-verdict.md`

## Operational Note

- `[VERIFIED]` The strategizer launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-003-explorer-001`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-001/REPORT-SUMMARY.md`.
- `[VERIFIED]` No summary sentinel landed during a bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Canonical Representative Form

- `[INFERRED]` Let the first live triad orbit be represented as

  ```text
  T_1 = (a, b, a + b),
  ```

  with
  `a != 0`,
  `b != 0`,
  `a` not parallel to `b`,
  and the associated helical signs chosen on the frozen canonical sheet.
- `[INFERRED]` Any connected second triad orbit sharing one mode with `T_1`
  can, after the frozen quotient operations
  (conjugation,
  triad relabeling,
  and representative change inside the same mirror-complete orbit),
  be written as

  ```text
  T_2 = (a, c, a + c).
  ```

- `[INFERRED]` The honest second-budget seed question is therefore:
  for which choices of `c` does the cluster

  ```text
  T(a,b,c) = { (a,b,a+b), (a,c,a+c) }
  ```

  define a genuinely new two-triad shared-mode seed rather than a duplicate,
  a first-budget artifact, or an inert helical decoration?

## Non-Seeds And Inert Decorations

### 1. Exact duplicate of the first triad

- `[INFERRED]` If
  `c = b`,
  then `T_2 = T_1`.
  That is not a new second-budget seed.
- `[INFERRED]` Adding another helical sign sector on the same one-triad
  wavevector picture is also not a new geometric seed.
  It changes the helical ledger on the already-failed first-budget support but
  does not create a new shared-mode cluster.

### 2. Disguised first-budget pseudo-support

- `[INFERRED]` If the second triad lives entirely on the mirror-complete
  one-triad picture

  ```text
  { ±a, ±b, ±(a+b) },
  ```

  then the picture is not genuinely second-rung.
  A canonical example is

  ```text
  (a, -a-b, -b),
  ```

  which only reuses the first-budget pseudo-survivor
  `{ ±a, ±b, ±(a+b) }`
  under a different representative.
- `[VERIFIED]` Step 2 already froze that six-wavevector picture as a
  pseudo-survivor that fails the admissible-enlargement audit.
  It cannot be revived here as if it were a new exact support.

### 3. Disconnected add-ons

- `[INFERRED]` A second triad that does not remain connected to the first
  through a genuinely shared helical mode orbit is outside the current budget.
  The second rung is specifically the connected shared-mode cluster budget.

## Genuine Second-Budget Seed Families

### Family A - Generic five-orbit shared-mode fan

- `[INFERRED]` If the two-triad cluster has five distinct wavevector orbits up
  to conjugation, then after the frozen equivalence reductions it is captured
  by

  ```text
  T_gen(a,b,c) = { (a,b,a+b), (a,c,a+c) }
  ```

  with five distinct orbit representatives

  ```text
  a, b, c, a+b, a+c.
  ```

- `[INFERRED]` This is the honest generic second-rung family:
  the second triad contributes two genuinely new nonshared wavevector orbits
  beyond the first-budget pseudo-support.

### Family B - Four-orbit parallelogram / mirror subfamily

- `[INFERRED]` If one extra coincidence reduces the cluster to four distinct
  wavevector orbits up to conjugation, then after re-centering the repeated
  orbit and applying the same quotient rules the cluster reduces to the
  canonical mirror form

  ```text
  T_par(a,b) = { (a,b,a+b), (a,-b,a-b) }.
  ```

- `[INFERRED]` Geometrically this is the parallelogram subfamily.
  It is genuinely new at the second budget because it adds one new wavevector
  orbit beyond the first-budget mirror-complete one-triad support, but it is
  lower-dimensional than the generic five-orbit fan.

## Equivalence Reductions Used

- `[VERIFIED]` From Step 1 and Step 2:
  quotient by conjugation,
  triad relabeling,
  helical-basis / gauge conventions,
  and canonical representative changes that do not alter exact support
  identity.
- `[INFERRED]` Additional Step-3 seed reductions:
  1. if a two-triad picture stays inside the first-budget pseudo-support, it is
     not a new second-budget seed;
  2. if a four-orbit cluster can be re-centered to the mirror form
     `T_par(a,b)`,
     do not count its other shared-mode drawings as separate families;
  3. if a picture differs only by adding extra helical sectors on the same
     already-failed one-triad wavevector support, treat it as an inert
     decoration rather than a new seed family.

## Exploration Verdict

- `[INFERRED]` The honest second-budget catalog has exactly two genuinely new
  geometric seed families:
  the generic five-orbit shared-mode fan
  `T_gen(a,b,c)`
  and the four-orbit mirror / parallelogram subfamily
  `T_par(a,b)`.
- `[INFERRED]` Duplicate one-triad drawings, disconnected add-ons, and any
  cluster contained entirely in the first-budget pseudo-support are not live
  second-rung seeds.
- `[INFERRED]` This catalog is honest because it classifies by exact support
  identity after the frozen quotient operations, not by cosmetic diagram shape.
