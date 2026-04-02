# Exploration 002 Report - Recursive Closure And Spillover Audit

## Goal

Run the recursive exact closure audit on each canonical third-budget seed and
decide whether any seed reaches a genuine finite fixed point inside the
three-triad repeated-wavevector cross-scale budget.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-004.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-001-exploration-002-exact-search-class-closure-and-escalation-freeze.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-002-exploration-002-recursive-closure-and-spillover-audit.md`
- `missions/exact-ns-phase-locking-firewall/library-inbox/step-003-exploration-002-recursive-closure-and-spillover-audit.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-004/explorations/exploration-002/code/three_triad_closure_audit.py`
- `missions/exact-ns-phase-locking-firewall/steps/step-004/explorations/exploration-002/code/output/three_triad_closure_audit_summary.txt`

## Operational Note

- `[VERIFIED]` The strategizer launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-004-explorer-002`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-002/REPORT-SUMMARY.md`.
- `[VERIFIED]` No summary sentinel landed.
- `[VERIFIED]` The launcher status file records
  `codex exec exited with status 1`,
  so this report is completed directly from the anchored local record and the
  local Step-4 closure artifact.

## Frozen Closure Rule

- `[VERIFIED]` Step 1 already froze the closure order:
  1. mandatory conjugate completion;
  2. test every ordered pair on the full active ledger;
  3. add every nonzero target helical sector with its conjugate completion;
  4. repeat until fixed point or budget spill.
- `[VERIFIED]` Closure-forced spectators belong on the support ledger from the
  first pass.

## Canonical Family - Single-Repeated-Orbit Three-Arm Star

Take the canonical seed

```text
T_star(a,b,c,d) = { (a,b,a+b), (a,c,a+c), (a,d,a+d) }.
```

Write

```text
p := a+b,
q := a+c,
r := a+d.
```

### Pass 0 - conjugate completion

- `[VERIFIED]` The active ledger becomes

  ```text
  S_0 = { ±a, ±b, ±c, ±d, ±p, ±q, ±r }.
  ```

### Pass 1 - seed-orbit pairs

- `[INFERRED]` Ordered pairs already on the seed orbits reproduce the three
  seed triads and their mirrors:

  ```text
  (a,b) -> p,
  (a,c) -> q,
  (a,d) -> r
  ```

  together with the inverse mirror relations.

### Pass 1 - immediate mirror-cross spill

- `[INFERRED]` The cheapest new targets already come from mirror-cross pairs on
  the conjugate-complete ledger:

  ```text
  (-a, b) -> b-a,
  (-a, c) -> c-a,
  (-a, d) -> d-a.
  ```

- `[INFERRED]` Those targets are outside the seed ledger on every honest
  single-repeated-orbit star, because landing back on the old support would
  force an additional repeated orbit or a lower-budget collapse.

### Pass 1 - backup positive-positive cross-scale witnesses

- `[INFERRED]` The more thematic cross-scale ordered pairs also force new
  targets:

  ```text
  (p, c) -> a+b+c,
  (q, d) -> a+c+d,
  (r, b) -> a+b+d.
  ```

- `[INFERRED]` In a generic star those are also outside the seed ledger.
  If one of them folds back onto an existing seed orbit, that only moves the
  geometry onto a low-dimensional coincidence locus and forces additional
  on-budget sign sectors before the spill continues.

### Representative coefficient audit

- `[VERIFIED]` The local audit script checked two representative geometries:
  1. `three_arm_generic`,
     with distinct partner shells and no low-dimensional coincidence; and
  2. `three_arm_bridge_guard`,
     with the coincidence
     `d = b + c`
     so that
     `(p, c) -> r`
     lands on-budget.
- `[VERIFIED]` On both representatives:
  `128/128`
  helical sign assignments were live seed assignments,
  `128/128`
  assignments forced at least one new on-budget sign sector,
  and
  `128/128`
  assignments forced at least one new spill orbit.
- `[VERIFIED]` Representative coefficient magnitudes on the positive-positive
  witness pairs were:

  ```text
  generic:
  (p,c) -> a+b+c: |C_+| = 1.284457, |C_-| = 0.129757
  (q,d) -> a+c+d: |C_+| = 1.330787, |C_-| = 0.118351
  (r,b) -> a+b+d: |C_+| = 0.388761, |C_-| = 0.019487

  bridge guard:
  (p,c) -> a+d:   |C_+| = 0.557678, |C_-| = 0.149429
  (r,b) -> a+2b+c: |C_+| = 0.524377, |C_-| = 0.052973
  (q,d) -> a+b+2c: |C_+| = 0.808013, |C_-| = 0.058013
  ```

### Low-dimensional coincidence guard

- `[INFERRED]` The coincidence

  ```text
  d = b + c
  ```

  does **not** rescue the family and does **not** create a new budget family.
- `[VERIFIED]` In the bridge-guard representative, the ordered pair

  ```text
  (p,c) -> r
  ```

  only forces an additional on-budget sign sector on `r`.
- `[INFERRED]` But the same guard still spills immediately through

  ```text
  (r,b) -> a+2b+c
  ```

  and also through the mirror-cross pair

  ```text
  (-a,c) -> c-a.
  ```

## Dead-Seed Verdict Table

| Seed family | Closure status | Decisive failure reason |
| --- | --- | --- |
| generic single-repeated-orbit three-arm star | `budget spill` | `[INFERRED]` mirror-cross pairs already force `b-a`, `c-a`, or `d-a`, with positive-positive cross-scale pairs giving additional spill witnesses |
| low-dimensional bridge coincidence inside the same family | `budget spill` | `[INFERRED]` even when one cross-scale target folds back on-budget, other ordered pairs still force `a+2b+c`, `a+b+2c`, or a mirror-cross difference orbit |

## Exploration Verdict

- `[INFERRED]` No honest third-budget seed reaches a genuine finite fixed point
  inside the single-repeated-orbit three-triad budget.
- `[INFERRED]` The sharpest earned obstruction is:
  **the conjugate-complete three-arm ledger already forces new orbit classes on
  the first honest closure pass, and low-dimensional coincidences only change
  which orbit spills first, not whether spill occurs.**
