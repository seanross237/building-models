# Curator Log - codex-patlas-beyond-de-giorgi-step-014-curator-001

Date: `2026-04-01`

Inputs reviewed:
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-001-candidate-slate.md`
- `missions/beyond-de-giorgi/meta-inbox/meta-step-014-exploration-001.md`

Atomic findings extracted:
1. Once the exact-rewrite shortlist and the fixed `I_flux[phi]` burden ledger
   are already frozen on disk, Step 2 should choose its active slate from that
   existing three-family table rather than reopen branch-adjacent families.
2. The two active Step-2 candidates are `Lamb-vector / Helmholtz-projected
   form` and `vorticity transport / Biot-Savart form` because each still names
   a nontrivial claimed route back to the same localized cutoff-flux bundle.
3. `divergence / stress form` is reserve-only because its most honest
   localization route returns directly to the same stress-against-`grad phi`
   burden and therefore functions mainly as a control comparator.
4. `strain / pressure-Hessian` and similar branch-adjacent families should be
   omitted from this slate because they were not part of the frozen
   exact-rewrite-native shortlist.
5. The report's operational note about a missing wrapper summary is already
   covered by existing workflow-monitoring guidance about launcher stalls and
   should not be refiled as a new branch fact.
6. The meta lesson strengthens the existing bounded-shortlist rule: once a
   shortlist is frozen, keep at least one reserve comparator and spend active
   slots only on candidates with a nontrivial route back to the same burden.

Filing decisions:
- Added one factual entry under `library/factual/exact-rewrite-obstruction-audit/`
  because Step 014 contributes a new reusable slate-selection result on top of
  the already-filed shortlist and candidate-level Tao verdicts.
- Updated the existing meta entry
  `library/meta/obstruction-screening/use-a-bounded-shortlist-to-make-likely-collapse-an-earned-later-claim.md`
  because the meta note sharpens shortlist discipline rather than justifying a
  separate new note.
- Did not add separate factual entries for the frozen three-family shortlist,
  the fixed `I_flux[phi]` target, or the candidate-level Lamb-vector,
  vorticity, and divergence verdicts because those claims were already filed
  elsewhere and Step 014 uses them as support for the new slate freeze.
- Did not add a workflow-monitoring entry for the missing wrapper summary
  because the repository already records the launcher-stall versus research
  outcome distinction.

Duplicate handling:
- Reused the existing shortlist entry
  `step-1-exact-rewrite-family-is-bounded-to-three-candidates.md`.
- Reused the existing architecture and burden-ledger entries under
  `library/factual/exact-rewrite-architecture-screening/`.
- Reused the existing candidate-level Tao-screen verdicts for divergence,
  Lamb-vector, and vorticity rather than duplicating them in separate files.
- Reused the existing workflow-monitoring rule
  `distinguish-launcher-stalls-from-research-inconclusiveness.md` for the
  operational note in the report.

Indexes updated:
- `library/factual/exact-rewrite-obstruction-audit/INDEX.md`
- `library/factual/INDEX.md`
- `library/meta/obstruction-screening/INDEX.md`
- `library/meta/INDEX.md`

Inbox deletion:
- Not requested by task; no inbox files were deleted.
