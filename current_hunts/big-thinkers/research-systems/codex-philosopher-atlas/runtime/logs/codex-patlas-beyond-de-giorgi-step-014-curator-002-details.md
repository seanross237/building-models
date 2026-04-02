# Curator Log: Step 014 Exploration 002

Date: `2026-04-01`
Session: `codex-patlas-beyond-de-giorgi-step-014-curator-002`

Processed inputs:
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-002-exact-and-localized-equations.md`
- `missions/beyond-de-giorgi/meta-inbox/meta-step-014-exploration-002.md`

Atomic findings filed:
- The `Lamb-vector / Helmholtz-projected` candidate still returns to the full
  frozen LEI cutoff-flux bundle at the first localization step: pairing the
  exact equation against `u phi` kills `u x omega`, but
  `pi = p + |u|^2 / 2` recreates the same `((|u|^2 / 2) + p) u . nabla phi`
  burden.
- The `vorticity transport / Biot-Savart` candidate does not act natively on
  the frozen LEI burden. It reaches that burden only after full velocity and
  pressure reconstruction, so the exchange step itself carries the decisive
  nonlocal debt.
- For rewrite audits on a frozen burden, the audit should derive the native
  equation first and charge debt at the first localization step rather than
  after narrating a pre-localized gain.
- The difference between acting on the frozen burden natively and only acting
  on it after reconstruction is itself a reusable obstruction-screening test.

Meta handling:
- Folded the repeated "first localization step" lesson into the existing
  localization-exactness note instead of creating a duplicate standalone meta
  file.
- Added one new obstruction-screening note for the native-versus-post-
  reconstruction burden distinction because that rule was not yet on disk as a
  separate reusable check.

Duplicate handling:
- Did not file a separate factual note for the shared verdict "both active
  candidates return to the same frozen burden" because that conclusion was
  already represented by the existing Step-2 rejection notes and the branch
  stop memo inside `exact-rewrite-obstruction-audit/`.
- Did not file a separate meta note for "record debt at the first localization
  step" because that lesson sharpened the existing
  `ask-which-identities-remain-exact-after-localization.md` entry directly.

Index status:
- Updated `library/factual/exact-rewrite-obstruction-audit/INDEX.md` and
  `library/factual/INDEX.md`.
- Updated `library/meta/obstruction-screening/INDEX.md` and
  `library/meta/INDEX.md`.

Conflict resolution:
- Reused the existing factual topic
  `library/factual/exact-rewrite-obstruction-audit/` rather than creating a
  new Step-014 topic, because the report sharpens the already-filed Step-2
  audit of the same rewrite branch.
- Filed the new "native versus reconstructed burden" lesson under
  `library/meta/obstruction-screening/` rather than
  `library/meta/exploration-goal-design/`, because it functions as an
  operational screening rule rather than as a prompt-design preference.

Task compliance:
- Wrote the receipt
  `missions/beyond-de-giorgi/meta-inbox/meta-step-014-exploration-002-curation-receipt.md`.
- Retained the inbox report.
