---
topic: Fix observability conventions before precursor search
category: goal-design
date: 2026-04-01
source: "exact-ns-hidden-precursor-firewall strategy-001 meta-exploration-001; exact-ns-hidden-precursor-firewall strategy-001 meta-exploration-002; exact-ns-hidden-precursor-firewall strategy-001 meta-exploration-003"
---

## Lesson

Once Phase 0 has defined an event on the exact PDE using coarse-graining or another observability layer, freeze those observability conventions before asking for a precursor.

Hold fixed the scale interface, witness channel, baseline region geometry, and window structure. If the event already comes with a canonical cylinder, prefer the literal earlier slab of that same object as the precursor region instead of inventing new geometry. Once one precursor pair survives, freeze that pair too and make the next exploration test one theorem target on it. Otherwise the follow-on work quietly redefines the event or reopens precursor selection indefinitely.

After that, the **first theorem-facing audit** should be: does the exact identity for the later event contain any backward-memory term involving the earlier slab? If not, stop. The mission does not yet have a precursor theorem problem; it has a memory-defect problem.

## Evidence

- **exact-ns-hidden-precursor-firewall exploration-001** — The exact-NS delayed-transfer event only became theorem-facing after the mission fixed the coarse-graining interface `ell`, the band witness `W_{ell,rho,r}`, the region `B_r(x_*)`, and the windows `Delta, delta`. These were observability conventions, not model changes.
- Once that object was fixed, the next honest question was one precursor observable on the same interface/witness pair. Changing filter, scale ratio, or witness at the same time would have moved the target and made any precursor claim ambiguous.
- The report also identified the main adversarial risk: a candidate precursor could merely predict generic cascade activity. Keeping the event definition fixed is what makes the "delayed transfer vs generic cascade" challenge testable.
- **exact-ns-hidden-precursor-firewall exploration-002** — Reusing the same parabolic cylinder and splitting off the earlier slab `B_r(x_*) x [t_* - Delta, t_* - delta]` was the least-arbitrary region choice. It prevented region design from becoming a second exploration inside the precursor search.
- **exact-ns-hidden-precursor-firewall exploration-002** — Lamb / Beltrami and vortex-stretching worked best as adversarial checks, not as co-equal live candidates. Keeping one primary precursor pair plus one explicit backup was what let the exploration finish cleanly.
- After the pair was selected, the next honest step was no longer "search for more precursors." It was "attack one theorem target on the frozen pair": lower bound, no-hidden-transfer, or counterexample.
- **exact-ns-hidden-precursor-firewall exploration-003** — The preferred same-family precursor `P_flux^-` looked natural once the pair was frozen, but the decisive question was simpler: does the earlier slab `R_-` appear anywhere in the exact filtered balance for the later witness gain? It does not. That killed the pair structurally before any backup vocabulary was worth promoting.
- The same follow-on fixed the escalation rule: backup observables less directly tied to the witness should only be promoted if they repair the missing memory link rather than merely rename the same mechanism family.

## Goal Pattern

1. State the already-defined event verbatim.
2. Freeze the observability conventions that define it: filter kernel, interface scale, scale ratio, spatial region, time windows, and output witness.
3. If the event already specifies a canonical cylinder or window structure, default the precursor region to the disjoint earlier slab of that same object unless there is a concrete reason not to.
4. Ask for exactly one primary precursor observable and, at most, one clearly marked backup.
5. Require an explicit explanation of why the primary observable tracks delayed transfer rather than generic cascade activity.
6. Once a pair survives, freeze it and make the next goal attack exactly one theorem target on that pair.
7. Before any large computation or backup search, inspect the exact identity governing the later event and ask whether the earlier region or slab appears in any exact term.
8. If there is no backward-memory term or monotonicity principle linking the earlier slab to the later event, stop and classify the pair as structurally defective unless the goal explicitly introduces an extra hypothesis.
9. Only evaluate backup observables if they plausibly repair that memory defect rather than restating the same-family activity in different words.
10. Treat any proposal that changes the interface, witness, or baseline geometry as a new definition task, not as a precursor result.

## Why This Matters

Precursor missions fail when both the event and the precursor are moving targets. Fixing observability conventions, then freezing the selected pair, turns the next phase into a one-object theorem question instead of another definition campaign.

But same-family precursors can still fail for a deeper reason: the exact identity for the later event may have no backward memory at all. Running that audit immediately prevents fake progress where the mission keeps renaming earlier activity without ever obtaining a real theorem link.

## Distinction from Related Entries

- `one-task-per-exploration.md` is about task count. This entry is about holding the target event fixed.
- `check-faithful-support-shrinkage-before-narrowing.md` asks whether a narrowed object changed at all. This entry assumes the event already exists and tells you how not to move it during the precursor search.
- `definition-extraction-gates-computation.md` explains why a Phase 0 definition gate matters. This entry governs the next step after that gate succeeds.
- `ask-what-replaces-the-bottleneck.md` asks what new obstruction appears after a reformulation. This entry is earlier: first check whether the candidate precursor pair has any exact memory link at all.
