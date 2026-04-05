# Exploration 003 Report

## Goal

Apply at least one admissible enlargement test to every apparent second-budget
survivor, or package a clean current-budget negative if no honest survivor
remains after the closure audit.

## Sources Used

- `missions/exact-ns-phase-locking-firewall/steps/step-001/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/RESULTS.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-002/explorations/exploration-003/REPORT.md`
- `missions/exact-ns-phase-locking-firewall/controller/decisions/decision-003.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-001/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/GOAL.md`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/shared_mode_closure_audit.py`
- `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-002/code/output/shared_mode_closure_audit_summary.txt`
- `library/factual/navier-stokes/admissible-enlargements-must-preserve-support-semantics-and-recompute-recursive-closure-from-scratch.md`
- `library/factual/navier-stokes/recursive-exact-closure-must-use-the-full-active-ledger-and-exact-projected-helical-coefficients.md`
- `library/factual/navier-stokes/closure-forced-spectators-belong-on-the-exact-support-ledger-from-the-first-pass.md`
- `library/factual/navier-stokes/smallest-first-exact-support-searches-should-order-by-closed-size-shell-span-depth-and-family-dimension.md`

## Operational Note

- `[VERIFIED]` This exploration was completed from the frozen local record and
  local computation artifacts.
- `[VERIFIED]` No web search was needed because the question is entirely about
  frozen branch-local rules and current-step support audits.

## Working Notes

### Note 1 - Frozen enlargement rule and scope guard

- `[VERIFIED]` Step 1 froze the admissible enlargement policy:
  stay inside the same exact support object class,
  keep the same helical basis,
  keep mandatory conjugate completion,
  keep full-ledger recursive closure,
  add one new independent helical representative,
  then recompute closure from scratch.
- `[VERIFIED]` Step 2 already killed the first budget only.
  Decision `decision-003.md` explicitly moves the branch to the second budget
  and explicitly forbids treating a rung-2 failure as a mission-level
  obstruction.
- `[VERIFIED]` The present step is therefore limited to the two-triad
  shared-mode budget and must end either with frozen supports for Chain Step 3
  or with a budget-limited negative plus controller review.

### Note 2 - What closure audit actually landed for the second budget

- `[VERIFIED]` No finished Step-3 exploration report has landed yet for the
  seed-classification or closure-audit explorations.
  The only landed second-budget closure artifact in the local record is
  `shared_mode_closure_audit.py` with its summary file.
- `[VERIFIED]` That landed artifact audits two named canonical families:
  `generic_fan` and `mirror_parallelogram`.
- `[VERIFIED]` Its summary records:
  `generic_fan` has `32/32` live seed sign assignments and `32/32`
  assignments with at least one forced new target;
  `mirror_parallelogram` has `16/16` live seed sign assignments and `16/16`
  assignments with at least one forced new target.
- `[INFERRED]` On the landed closure record, no honest second-budget survivor
  remains after the first full recursive-closure pass.
  The only objects that still look tempting are the cosmetically tidy raw
  two-triad ledgers before one keeps every closure-forced new orbit.

### Note 3 - Explicit admissible enlargement tests

- `[PROPOSED]` Because the landed closure artifact leaves no honest survivor,
  the enlargement audit is logically aimed at the only apparent survivors:
  the tidy representative two-triad ledgers of the landed families.
- `[VERIFIED]` I wrote
  `missions/exact-ns-phase-locking-firewall/steps/step-003/explorations/exploration-003/code/admissible_enlargement_audit.py`
  and ran it.
  The script does the following for each representative family:
  1. tests every sign assignment on the seed ledger;
  2. finds a first-pass forced new orbit on the conjugate-completed active
     ledger;
  3. adds one admissible new representative on that orbit;
  4. recomputes the full first-pass closure from scratch on the enlarged
     ledger; and
  5. checks whether further new target orbits are still forced.
- `[VERIFIED]` The output files are:
  `code/output/admissible_enlargement_audit.json`
  and
  `code/output/admissible_enlargement_audit_summary.txt`.

#### Landed-family enlargement results

| Family | Live seed assignments | First-pass forced new targets | Still forces new targets after one admissible enlargement | Verdict |
| --- | --- | --- | --- | --- |
| `generic_fan` | `32/32` | `32/32` | `32/32` | `fails enlargement` |
| `mirror_parallelogram` | `16/16` | `16/16` | `16/16` | `fails enlargement` |

- `[VERIFIED]` Representative `generic_fan` enlargement test:
  the script picks the first admissible new orbit forced by the
  conjugate-completed ledger,

  ```text
  (-a, c) -> c - a.
  ```

  After adding that one new orbit and recomputing closure from scratch, the
  enlarged ledger still forces

  ```text
  (-a, b) -> b - a,
  ```

  with nonzero projected coefficients
  `|C_+| = 0.603553`,
  `|C_-| = 0.103553`
  in the canonical representative check.
- `[VERIFIED]` Representative `mirror_parallelogram` enlargement test:
  the script picks the first admissible new orbit

  ```text
  (-d, -e) -> -2a,
  ```

  and after that one-orbit enlargement the enlarged ledger still forces

  ```text
  (-d, e) -> -2b,
  ```

  with nonzero projected coefficients
  `|C_+| = 0.853553`,
  `|C_-| = 0.146447`
  in the canonical representative check.
- `[INFERRED]` These are clean admissible-enlargement failures, not merely
  restatements of the first-pass spill.
  The same support semantics were kept, one new orbit was added, closure was
  rerun from scratch, and the enlarged ledgers still forced genuinely new
  orbits.

### Note 4 - Guard checks on the missing-classification gap

- `[INFERRED]` Because the seed-classification report did not land, there was a
  real risk that a low-dimensional edge case might have been missed by the
  `generic_fan` / `mirror_parallelogram` split.
- `[VERIFIED]` I therefore added two extra representative guards to the same
  script:
  `generic_fan_collinear`
  and
  `edge_overlap_chain`.
- `[VERIFIED]` Both guards fail in the same way on every live sign assignment:

  | Guard case | Live seed assignments | Still forces new targets after one admissible enlargement |
  | --- | --- | --- |
  | `generic_fan_collinear` | `32/32` | `32/32` |
  | `edge_overlap_chain` | `16/16` | `16/16` |

- `[INFERRED]` These extra checks do **not** by themselves prove a full new
  seed catalog.
  They do show that the most obvious classification-gap subfamilies also do not
  rescue a second-budget survivor on the current local record.

## Findings

- `[VERIFIED]` Every apparent survivor that can honestly be read off the landed
  second-budget closure audit fails an explicit admissible enlargement test.
- `[INFERRED]` No genuine second-budget support is earned for Chain Step 3 on
  the current record.
- `[INFERRED]` The sharpest earned current-budget negative is:
  **two-triad shared-mode ledgers remain non-closed even after one admissible
  one-orbit enlargement, because full recursive closure still forces additional
  new target orbits on the enlarged support.**

## Dead Ends And Failed Attempts

- `[VERIFIED]` The Step-3 classification and closure exploration reports did
  not land, so I could not quote a finished sibling narrative report.
  I had to reconstruct the current closure picture from the landed code artifact
  and verify the enlargement step directly.
- `[INFERRED]` I initially treated the two landed named families as the whole
  second-budget catalog.
  Before accepting that, I checked the most obvious missing edge cases
  (`generic_fan_collinear` and `edge_overlap_chain`) with fresh computation.
- `[VERIFIED]` I did not start the next budget and did not derive projected
  ODEs.

## Budget-limited verdict for controller review

- `[INFERRED]` Honest post-closure survivors at the current budget:
  `none` on the landed local record.
- `[VERIFIED]` Explicit enlargement checks were carried out on the only
  apparent survivors visible in that record:
  the tidy representative ledgers for `generic_fan` and
  `mirror_parallelogram`.
  Both still forced additional new target orbits after one admissible
  one-orbit enlargement and a fresh closure pass.
- `[INFERRED]` Chain Step 3 is therefore **not** genuinely earned at the
  second-budget level on the current record.
- `[VERIFIED]` The verdict must stay class-limited:
  this is a second-budget negative plus controller review,
  not a mission-level obstruction and not an automatic self-escalation to the
  next rung.
