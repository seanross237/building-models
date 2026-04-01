# Step-1 Exact Rewrite Family Is Bounded To Three Candidates

Status: `VERIFIED` shortlist with `INFERRED` final bounding

The Step-1 exact-rewrite family for the fixed localized LEI branch is bounded
to three candidates:

- divergence / stress form, using `(u . nabla)u = div(u otimes u)` when
  `div u = 0`
- Lamb-vector / Helmholtz-projected form, using
  `(u . nabla)u = nabla(|u|^2 / 2) - u x omega` and
  `P((u . nabla)u) = -P(u x omega)`
- vorticity transport / Biot-Savart form, with any vorticity-side relocation
  required to repay the full Biot-Savart and localization cost in the same
  ledger

Each candidate stays admissible only if its apparent simplification survives
the unchanged cutoff, projection, and nonlocal bookkeeping. Otherwise the
rewrite is cosmetic rather than a genuine branch gain.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-005-exploration-003-gain-currency-candidate-family.md`
