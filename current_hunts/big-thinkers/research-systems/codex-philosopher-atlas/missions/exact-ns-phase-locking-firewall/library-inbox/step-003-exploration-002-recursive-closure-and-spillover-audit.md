# Exploration 002 Report - Recursive Closure And Spillover Audit

## Goal

Run the recursive exact closure audit on each canonical second-budget seed and
decide whether any seed reaches a genuine finite fixed point inside the
two-triad shared-mode budget.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-003.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-002-recursive-closure-and-spillover-audit.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/shared_mode_closure_audit.py`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/output/shared_mode_closure_audit_summary.txt`

## Operational Note

- `[VERIFIED]` The strategizer launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-003-explorer-002`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-002/REPORT-SUMMARY.md`.
- `[VERIFIED]` No summary sentinel landed during a bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record and the local Step-3 coefficient audit script.

## Frozen Closure Rule

- `[VERIFIED]` Step 1 already froze the closure order:
  1. mandatory conjugate completion;
  2. test every ordered pair on the full active ledger;
  3. add every nonzero target helical sector with its conjugate completion;
  4. repeat until fixed point or budget spill.
- `[VERIFIED]` Closure-forced spectators belong on the support ledger from the
  first pass.

## Family A - Generic Five-Orbit Shared-Mode Fan

Take the canonical seed

```text
T_gen(a,b,c) = { (a,b,a+b), (a,c,a+c) }
```

with five distinct wavevector orbits

```text
a, b, c, d := a+b, e := a+c.
```

### Pass 0 - conjugate completion

- `[VERIFIED]` The active ledger becomes

  ```text
  S_0 = { ±a, ±b, ±c, ±d, ±e }.
  ```

### Pass 1 - seed-orbit pairs

- `[INFERRED]` Ordered pairs already on the two seed orbits reproduce the seed
  triads:

  ```text
  (a,b) -> d,
  (d,-b) -> a,
  (d,-a) -> b,
  (a,c) -> e,
  (e,-c) -> a,
  (e,-a) -> c.
  ```

### Pass 1 - decisive cross-pair forcing

- `[INFERRED]` The first genuinely new tests come from mixing the two seed
  triads across the shared-mode ledger:

  ```text
  (d, c)  -> a + b + c,
  (d,-c)  -> a + b - c,
  (e,-b)  -> a - b + c.
  ```

- `[INFERRED]` On an honest generic five-orbit seed, at least one of those
  three targets is outside the seed ledger.
  If all of them were folded back into the existing support by coincidences,
  the cluster would drop onto a lower-dimensional coincidence locus already
  quotient-identified in Exploration 001 as either the mirror/parallelogram
  subfamily or a first-budget artifact.
- `[VERIFIED]` The representative coefficient audit on the orthogonal sample
  geometry

  ```text
  a = (1,0,0), b = (0,1,0), c = (0,0,1)
  ```

  found:
  all `32/32` seed sign assignments are live, and `32/32` force at least one
  new target helical sector on these cross-pair targets.
  Representative magnitudes include

  ```text
  (d,c) -> a+b+c:
  |C_+| = 0.557678,
  |C_-| = 0.149429.
  ```

### Family-A verdict

- `[INFERRED]` The generic five-orbit family dies by `budget spill`.
- `[INFERRED]` Decisive reason:
  cross-triad ordered pairs on the conjugate-complete ledger force a new
  wavevector orbit on the first honest pass, with at least one live target
  helical sector.

## Family B - Four-Orbit Mirror / Parallelogram Subfamily

Take the canonical mirror seed

```text
T_par(a,b) = { (a,b,a+b), (a,-b,a-b) }.
```

Write

```text
d := a+b,
e := a-b.
```

### Pass 0 - conjugate completion

- `[VERIFIED]` The active ledger becomes

  ```text
  S_0 = { ±a, ±b, ±d, ±e }.
  ```

### Pass 1 - decisive ordered pairs

- `[INFERRED]` The most economical off-orbit tests are

  ```text
  (d, b)   -> a + 2b,
  (e,-b)   -> a - 2b.
  ```

- `[INFERRED]` Both target wavevectors are outside
  `{ ±a, ±b, ±d, ±e }`
  unless one collapses back into the excluded repeated-wavevector or collinear
  cases.
- `[VERIFIED]` The representative coefficient audit on

  ```text
  a = (1,0,0), b = (0,1,0)
  ```

  found:
  all `32/32` seed sign assignments are live, and `32/32` force at least one
  new target helical sector.
  Representative magnitudes include

  ```text
  (d,b) -> a+2b:
  |C_+| = 0.473607,
  |C_-| = 0.026393.
  ```

### Family-B verdict

- `[INFERRED]` The mirror / parallelogram family also dies by `budget spill`.
- `[INFERRED]` Decisive reason:
  the first honest closure pass already forces
  `a+2b`
  or
  `a-2b`
  beyond the four-orbit seed ledger.

## Dead And Non-Honest Cases

- `[INFERRED]` Duplicate or disconnected two-triad drawings:
  `representation artifact`, not live seeds.
- `[INFERRED]` Any seed drawn entirely inside the first-budget mirror-complete
  one-triad picture:
  `disguised first-budget dead seed`, not a genuine second-rung survivor.

## Exploration Verdict

- `[INFERRED]` No canonical second-budget seed reaches a genuine finite fixed
  point inside the two-triad shared-mode budget.
- `[INFERRED]` Every honest seed family dies by the same budget-level
  obstruction:
  **recursive exact closure forces a new wavevector orbit on the first honest
  pass once the full conjugate-complete ledger is tested**.
- `[INFERRED]` This is still a current-budget statement only.
  It does not claim that the full recursive closure is infinite, only that the
  support does not stay inside the frozen second budget.
