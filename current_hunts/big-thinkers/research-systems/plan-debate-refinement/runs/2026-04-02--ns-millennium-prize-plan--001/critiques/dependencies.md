# Dependencies Critique

## Strongest Objections

- The plan starts with theorem targets before it has established the objects those theorems are supposed to talk about. `frozen one-bridge ledger`, `template-defect`, `leakage sheet`, `shell-crossing exact triads`, and `canonical extraction lemma` are all treated as if they already exist, but the draft never supplies provenance, definitions, or stability checks for them.
- Route ordering is circular. Route 5 needs a canonical extraction lemma, but Routes 1-3 are themselves written in terms that already presuppose canonicity, same-currency comparison, and exact transfer bookkeeping. The plan is asking the route that depends on extraction to be enabled by routes that already require extraction-grade structure.
- The main success criteria are not executable dependencies. Phrases like `sharp witness`, `repaired leakage sheet`, and `exact recursive-spill theorem` sound concrete, but they hide the prerequisite work: locking the object definitions, fixing the comparison currency, and proving the bookkeeping is reconstructible from source material.
- The plan assumes the status file frontier names can be freely renamed into a new local vocabulary. That is a dependency risk, not a stylistic choice. If `one-bridge ledger` is not exactly the same object class as the status file’s live frontier, the draft is no longer anchored to the authoritative picture it claims to follow.
- The sidecar phase is not schedulable as written. It says each non-Tao direction should get one precise lemma target and one obstruction test, but it never defines how those targets are selected, what inputs they inherit from the main ledger work, or when a sidecar counts as comparable progress.

## Missing Assumptions Or Prerequisites

- A frozen glossary mapping every draft object back to the status-file frontier terms, with one canonical definition per object.
- A provenance audit for every named quantity and family: where it comes from, what source artifact defines it, and whether it survives harmless refinement and relabeling.
- A dependency graph showing which lemmas require which definitions, and which definitions are upstream blockers for later routes.
- A preflight check that the ledger artifacts actually exist in the workspace or source corpus, and that the plan is not relying on internal shorthand that only makes sense to the author.
- A stated currency model for comparisons across `friendly` and `hostile` families. The draft uses that language repeatedly, but never says what is being held fixed when families are compared.
- A gate that says whether Route 5 is truly conditional on Routes 1-3, or whether it is a separate program that should be blocked until a different extraction project exists.

## Concrete Revisions

- Add a Phase 0a before any theorem work: freeze definitions, provenance, and comparison currency for every object mentioned in Routes 1-5.
- Split Route 1 into two steps: first prove the packet-family objects are canonical and reconstructible, then attempt the exact identities. Do not let formula-chasing start before object validation.
- Split Route 2 into hostile-family canonicalization and leakage-transfer. The lower-bound theorem is premature until the hostile family is pinned down in the same currency as the friendly family.
- Add an explicit `blocked until` list under Route 5. If canonical extraction is not produced by earlier routes, Route 5 should stay off the active board rather than being treated as a latent option.
- Require every route to declare inputs, upstream lemmas, downstream use, and a failure mode. If any item cannot be filled in, the route is not dependency-complete enough to execute.
- Tighten the kill criteria so they fire not only on canonicity failure, but also on undefined bookkeeping, missing provenance, or inability to reconstruct the ledger from source material.

## Salvageability

The plan is salvageable without a full rewrite, but only if it is converted from a theorem-first outline into a dependency-first program. As written, it is circular in the places that matter most, so nobody can honestly tell where to start or what would count as a valid upstream prerequisite being met.
