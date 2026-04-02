# Exploration 002 Report - Recursive Closure And Spillover Audit

## Goal

Run the recursive exact closure audit on each canonical first-budget seed from
Exploration 001.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-002/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-001/explorations/exploration-002/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-001/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-01.md`
- `missions/exact-ns-phase-locking-firewall/planning-runs/run-001/attacks/chain-02.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-002.md`
- `library/factual/navier-stokes/recursive-exact-closure-must-use-the-full-active-ledger-and-exact-projected-helical-coefficients.md`
- `library/factual/navier-stokes/closure-forced-spectators-belong-on-the-exact-support-ledger-from-the-first-pass.md`
- `library/factual/navier-stokes/exact-support-search-object-is-a-finite-canonical-helical-support-sheet-with-mandatory-conjugate-completion.md`
- `library/factual/exact-ns-phase-locking-firewall/step-2-is-well-posed-once-the-phase-ledger-search-class-and-metric-sheet-are-frozen.md`

## Operational Note

- `[VERIFIED]` The strategizer launched
  `codex-patlas-exact-ns-phase-locking-firewall-step-002-explorer-002`
  through `bin/launch-role.sh` with sentinel
  `explorations/exploration-002/REPORT-SUMMARY.md`.
- `[VERIFIED]` No summary sentinel landed during a bounded wait.
- `[INFERRED]` This report is therefore completed directly from the anchored
  local record.

## Frozen Closure Rule

- `[VERIFIED]` Step 1 froze the closure order:
  1. add mandatory conjugates;
  2. test every ordered pair on the full active ledger against exact projected
     helical interactions;
  3. add every nonzero forced target mode with its conjugate completion;
  4. repeat until a fixed point or budget spill.
- `[VERIFIED]` Closure-forced spectators belong on the support ledger from the
  first pass.

## Start From A Canonical Seed

Take one honest first-budget seed from Exploration 001:

```text
tau_0 = ((k, sigma_k), (p, sigma_p), (q, sigma_q)),
k = p + q,
p != q,
p not parallel to q.
```

### Pass 0 - mandatory conjugate completion

- `[VERIFIED]` The exact seed immediately enlarges to the mirror-complete
  active ledger

  ```text
  S_0 = { ±(k, sigma_k), ±(p, sigma_p), ±(q, sigma_q) }
  ```

  in the frozen representative convention.
- `[INFERRED]` This is already more than the raw seed diagram, but it is still
  inside the current first-budget audit because conjugate completion is part of
  the exact realization, not an admissible enlargement.

### Pass 1 - interactions that stay on the original triad orbit

- `[INFERRED]` The ordered pairs

  ```text
  (p, q) -> k,
  (k, -p) -> q,
  (k, -q) -> p
  ```

  and their mirrors only reproduce the original triad orbit.

### Pass 1 - self-pairs do not save the budget

- `[INFERRED]` Self-pairs such as `(p, p)` do **not** force `2p` because the
  Step-1 ambient scalar has the form

  ```text
  Gamma_{r,p,p}(u)
    = -i overline{u^(r)} · [ (p · u^(p)) P_r u^(p) ],
  ```

  and divergence-free data give `p · u^(p) = 0`.
- `[INFERRED]` So the honest obstruction does not come from self-doubling; it
  comes from distinct off-orbit pairs created by conjugate completion.

## First Spillover Modes

### 1. The conjugate-cross pair `(p, -q)`

- `[INFERRED]` Because `p` and `q` are noncollinear, the target wavevector

  ```text
  r := p + (-q) = p - q
  ```

  is nonzero and distinct from
  `±p`,
  `±q`,
  `±k`.
- `[INFERRED]` The corresponding exact interaction is not identically zero:

  ```text
  Gamma_{r,p,-q}(u)
    = -i overline{u^(r)} · [ ((-q) · u^(p)) P_r u^(-q) ].
  ```

  Since `q` is not parallel to `p`, the factor `(-q) · u^(p)` is not forced to
  vanish by incompressibility, so at least one target helical sign sector on
  `r = p - q` is live.
- `[INFERRED]` Therefore recursive closure must add at least one mode on
  `p - q` together with its conjugate completion.

### 2. The forward pairs `(k, p)` and `(k, q)`

- `[INFERRED]` The same ledger also contains

  ```text
  s := k + p = 2p + q,
  t := k + q = p + 2q,
  ```

  again nonzero and again distinct from the original triad orbit in every
  honest noncollinear seed.
- `[INFERRED]` So even if one tried to suppress the `p - q` branch by a special
  coefficient choice, the mirror-complete ledger still presents other
  off-orbit pairs that force new wavevectors.

## Why The New Wavevectors Are Genuinely Outside The Budget

- `[INFERRED]` If `p - q` were equal to one of
  `±p`,
  `±q`,
  `±k`,
  then simple algebra would force
  `p = 0`,
  `q = 0`,
  `p = q`,
  or collinearity, all excluded by the seed catalog.
- `[INFERRED]` The same algebra excludes `2p + q` and `p + 2q` from the
  original orbit unless one collapses back into a degenerate collinear case.
- `[INFERRED]` So the current-budget negative does **not** depend on a delicate
  coefficient table. It is already earned by the frozen exact closure rule plus
  nondegenerate one-triad geometry.

## Seed-by-Seed Verdict

### Excluded non-seeds

- `[INFERRED]` Repeated-wavevector and collinear cases:
  `exactness failure at seed definition`.
  They do not enter the live closure audit because they are not exact active
  triads with nonzero projected coefficient.

### Live canonical seeds

- `[INFERRED]` Sign-sheet class `(+++)`:
  `budget spill`.
  Decisive reason:
  conjugate completion creates off-orbit active pairs, and `(p, -q)` already
  forces at least one new mode on `p - q`.
- `[INFERRED]` Sign-sheet class `(++-)`:
  `budget spill`.
  Decisive reason:
  same as above; the closure rule tests nonzero projected interactions on the
  full mirror-complete ledger, not only the visually tidy seed orbit.
- `[INFERRED]` Sign-sheet class `(+--)`:
  `budget spill`.
  Decisive reason:
  same as above.

## Companion / Spectator Ledger

- `[VERIFIED]` Mandatory representation companions:
  the mirror-complete partners on
  `-k`,
  `-p`,
  `-q`.
- `[INFERRED]` First closure-forced spectator wavevector orbits:
  at minimum

  ```text
  ±(p - q),
  ±(2p + q),
  ±(p + 2q).
  ```

- `[INFERRED]` Additional helical sign sectors on the original wavevectors may
  also be forced on the first pass, but the budget-limited negative does not
  need a sharper sign-by-sign table because the new-wavevector spill is already
  decisive.

## Exploration Verdict

- `[INFERRED]` No canonical first-budget seed reaches a genuine finite fixed
  point inside the one-triad-orbit budget.
- `[INFERRED]` Every honest seed dies the same way:
  **recursive closure spills outside the current budget on the first honest
  pass once conjugate-completed off-orbit pairs are tested**.
- `[INFERRED]` This is a current-budget result only.
  I am **not** claiming a theorem that one-triad seeds generate infinite
  closure, only that they do not stay inside the frozen first budget.

## Dead Ends / Rejections

- `[INFERRED]` The cosmetically tidy six-mode picture
  `±p, ±q, ±k`
  was rejected as an exact survivor because it ignores mirror-cross pairs like
  `(p, -q)` that the Step-1 closure rule explicitly requires.
- `[VERIFIED]` First-generation-only closure was rejected because the branch
  already froze fully recursive exact closure in Step 1.
