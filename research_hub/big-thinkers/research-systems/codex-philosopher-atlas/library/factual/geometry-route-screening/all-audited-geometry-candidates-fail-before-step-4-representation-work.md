# All Audited Geometry Candidates Fail Before Step-4 Representation Work

Status: `VERIFIED` audit result with `INFERRED` consequence

Using the fixed Step-3 package together with the completed Step-4 dynamic
audits, the geometry branch has no remaining `dynamically plausible` route.

The audited candidate table is:

- primary hybrid `direction coherence + tube persistence`:
  `informative but dynamically weak`
- comparators `vorticity-direction coherence` and `tube coherence / persistence`:
  `informative but dynamically weak`
- fragility screen `local Beltrami / alignment`:
  `static-only`
- fragility hybrids `Beltrami deficit + concentration` and
  `Beltrami deficit + anisotropy`:
  `informative but dynamically weak`

This means the earliest honest branch-kill condition is already met before any
Step-4 kernel-level representation work. Proceeding anyway would be blind
momentum rather than an earned next step.

The only visible rescue routes are exactly the disallowed ones already exposed
by the audit:

- tube-adapted relocalization rather than the neutral Eulerian package
- tuned threshold or time-window choices that keep selecting a favorable core
- stronger derivative control than the bounded package contains

Without a genuinely new ingredient, the correct posture is to stop or replan
the branch rather than choose a stretching representation anyway.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-004-exploration-003-fragility-screen-kill-memo.md`
