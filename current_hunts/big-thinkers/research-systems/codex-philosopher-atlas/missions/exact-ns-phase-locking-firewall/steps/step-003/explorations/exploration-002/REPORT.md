# Exploration 002 Report - Recursive Closure And Spillover Audit

## Goal

Run the recursive exact closure audit on each canonical second-budget seed and
decide whether any seed reaches a genuine finite fixed point inside the
two-triad shared-mode budget.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-003.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/shared_mode_closure_audit.py`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/output/shared_mode_closure_audit.json`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/output/shared_mode_closure_audit_summary.txt`

## Method

- `[VERIFIED]` I inherited the frozen Step-1 / Step-2 rules:
  mandatory conjugate completion,
  full-ledger recursive closure,
  immediate inclusion of closure-forced spectator modes,
  and no projected ODE derivation yet.
- `[COMPUTED]` I replaced the placeholder probe with
  `code/shared_mode_closure_audit.py`,
  a pure-stdlib audit that:
  1. samples small integer shared-mode seeds to recover the orbit-level family
     patterns;
  2. checks seed exactness for every raw orbit-sign assignment on canonical
     representatives;
  3. runs pass-by-pass helical closure with conjugates implicit; and
  4. records both on-budget helical-sector forcing and off-budget spill modes.
- `[COMPUTED]` The radius-2 catalog sample found only two orbit-level
  patterns:
  `support size = 5, triad overlap = 1` and
  `support size = 4, triad overlap = 2`.
  No third honest pattern appeared.

## Canonical Seed Families

- `[CHECKED]` Two distinct exact triad orbits that share at least one
  wavevector orbit can only do one of three things at orbit level:
  1. share exactly one orbit, giving a five-orbit support;
  2. share exactly two orbits, giving a four-orbit support; or
  3. share all three orbits, which is just the Step-2 one-triad orbit again.
- `[CHECKED]` So the honest second-budget catalog has exactly two families:
  1. **five-orbit shared-vertex family**:
     two triads share one orbit only, canonical form

     ```text
     d = a + b,
     e = a + c,
     support = {±a, ±b, ±c, ±d, ±e}.
     ```

  2. **four-orbit shared-edge family**:
     two distinct triads on a four-orbit support, canonical form

     ```text
     d = a + b,
     e = a - b,
     support = {±a, ±b, ±d, ±e}.
     ```

- `[CHECKED]` Any extra orbit identification inside the five-orbit form drops
  into the four-orbit family or recycles the Step-2 one-triad picture, so the
  catalog is honest rather than cherry-picked.

## Closure Audit

### Family 1 - Five-Orbit Shared-Vertex

- `[COMPUTED]` I audited two canonical representatives of the same orbit-level
  family:
  1. `generic`:

     ```text
     a = (1,0,0), b = (0,1,0), c = (0,0,1),
     d = (1,1,0), e = (1,0,1);
     ```

  2. `forward_collision`:

     ```text
     a = (1,0,0), b = (0,1,0), c = (0,2,0),
     d = (1,1,0), e = (1,2,0),
     ```

     which is the special subcase where the first forward target
     `d + b = a + 2b`
     collapses onto the existing orbit `e`.
- `[COMPUTED]` For both representatives, all `32/32` raw orbit-sign
  assignments are honest exact seeds and all `32/32` spill on the **first**
  closure pass.

#### Pass 0 ledger

- `[COMPUTED]` Start with one orbit-sign sector on each seed orbit
  `{a, b, c, d, e}` and immediately add their conjugates.
  No orbit is dropped.

#### Pass 1 - forced helical sectors on the seed ledger

- `[COMPUTED]` On every tested sign assignment, the first full pair scan forces
  the missing opposite helical sector on **every** seed orbit before closure
  can stop.
- `[COMPUTED]` For the all-plus `generic` assignment, the explicit forced
  sectors are:

  ```text
  d- from (a, b) -> d,
  e- from (a, c) -> e,
  b- from (a, -d) -> -b,
  c- from (a, -e) -> -c,
  a- from (b, -d) -> -a.
  ```

- `[COMPUTED]` So the exact ledger is already larger than the raw seed picture
  even before using the new spill orbits.

#### Pass 1 - family-wide spill reason

- `[CHECKED]` The forward pairs

  ```text
  (d, b) -> a + 2b,
  (e, c) -> a + 2c
  ```

  are the uniform family-wide witnesses.
- `[CHECKED]` If `a + 2b` stays inside the five-orbit support, then it can only
  coincide with `±c` or `±e`.
  In each of those four cases, the second forward target `a + 2c` cannot equal
  `±b` or `±d` without forcing `a` parallel to `b`, which is excluded by the
  seed definition.
  Therefore at least one of

  ```text
  a + 2b, a + 2c
  ```

  lies outside the budget support for every honest five-orbit seed.
- `[CHECKED]` For either witness pair, the two source wavevectors are
  noncollinear and the target is not parallel to the right input, so the exact
  projected interaction vector is nonzero.
  Hence at least one target helical sector on the outside orbit is forced.
- `[COMPUTED]` The representative computations show the spill is usually even
  stronger.
  For the all-plus `generic` assignment, the same first pass already forces

  ```text
  ±(a-b), ±(a-c), ±(2a+b), ±(2a+c), ...
  ```

  with both target helical sectors live on the displayed witnesses.

#### Five-orbit verdict

- `[COMPUTED]` No tested raw sign assignment reaches an inside-budget fixed
  point.
- `[CHECKED]` No honest five-orbit shared-vertex seed can survive:
  the first honest pair scan both completes the missing seed-orbit helicities
  and forces at least one new wavevector orbit outside the two-triad budget.

### Family 2 - Four-Orbit Shared-Edge

- `[COMPUTED]` I audited the canonical representative

  ```text
  a = (1,0,0), b = (0,1,0),
  d = a + b = (1,1,0),
  e = a - b = (1,-1,0),
  ```

  with seed triads

  ```text
  (d, a, b), (e, a, -b).
  ```

- `[COMPUTED]` All `16/16` raw orbit-sign assignments are honest exact seeds
  and all `16/16` spill on the first closure pass.

#### Pass 0 ledger

- `[COMPUTED]` Start with one orbit-sign sector on each seed orbit
  `{a, b, d, e}` and add conjugates immediately.

#### Pass 1 - forced helical sectors on the seed ledger

- `[COMPUTED]` Every tested sign assignment forces the missing opposite helical
  sector on all four seed orbits on the first pass.
- `[COMPUTED]` For the all-plus assignment, the explicit witnesses are:

  ```text
  d- from (a, b) -> d,
  e- from (a, -b) -> e,
  b- from (a, -d) -> -b,
  a- from (b, -d) -> -a.
  ```

#### Pass 1 - family-wide spill reason

- `[CHECKED]` The forward pair

  ```text
  (d, b) -> a + 2b
  ```

  is already enough.
- `[CHECKED]` The target `a + 2b` cannot equal
  `±a`,
  `±b`,
  `±d = ±(a+b)`,
  or
  `±e = ±(a-b)`
  unless `a` becomes parallel to `b` or one vector vanishes.
  Those are excluded by honest seed admission.
- `[CHECKED]` Since `d` and `b` are noncollinear and the projected interaction
  term is nonzero, at least one helical sector on `a + 2b` is forced.
- `[COMPUTED]` The representative ledger again spills more strongly than the
  minimal proof needs:
  the all-plus assignment also forces

  ```text
  ±(2a+b), ±(2a-b), ±(a+2b), ±(a-2b)
  ```

  on that same first pass.

#### Four-orbit verdict

- `[COMPUTED]` No tested raw sign assignment reaches an inside-budget fixed
  point.
- `[CHECKED]` No honest four-orbit shared-edge seed can survive:
  pass 1 already forces the missing seed-orbit helicities and a new wavevector
  orbit outside the budget.

## Consolidated Verdict

| Family | Raw orbit-sign assignments checked | Exact seeds | First-pass helical-sector completion | First-pass spill | Status |
| --- | ---: | ---: | --- | --- | --- |
| five-orbit shared-vertex | 32 | 32 | `[COMPUTED]` yes, all 5 seed orbits | `[COMPUTED]` yes, all 32 assignments | `dead` |
| four-orbit shared-edge | 16 | 16 | `[COMPUTED]` yes, all 4 seed orbits | `[COMPUTED]` yes, all 16 assignments | `dead` |

- `[COMPUTED]` No canonical second-budget seed reaches a genuine finite fixed
  point inside the two-triad shared-mode budget.
- `[CHECKED]` The obstruction is sharper than a vague “more modes appear”
  statement:
  **the very first honest recursive-closure pass forces the missing helical
  sectors on the seed ledger and simultaneously forces new wavevector orbits
  outside the budget.**
- `[VERIFIED]` This is only a second-budget obstruction memo.
  It does **not** claim a mission-level impossibility result,
  does **not** derive projected ODEs,
  and does **not** self-escalate to the next ladder rung.

## Budget-Limited Verdict For Controller Review

- `[COMPUTED]` Apparent survivors after the honest closure pass:
  `none`.
- `[CHECKED]` Dead-seed reasons:
  1. five-orbit shared-vertex:
     first-pass helical-sector completion plus first-pass spill by at least one
     of
     `a + 2b` or `a + 2c`;
  2. four-orbit shared-edge:
     first-pass helical-sector completion plus first-pass spill by
     `a + 2b`.
- `[COMPUTED]` Chain Step 3 is **not** well posed on the second budget,
  because no genuinely invariant finite support survives to inherit exact
  dynamics work.
