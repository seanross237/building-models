# Lamb Vector Projected Form Is Tao-Insufficient Once Localization Debt Returns

Status: `INFERRED`

Within the Step-2 Tao screen for the fixed exact-rewrite audit, the
`Lamb-vector / Helmholtz-projected form`

`(u . nabla)u = nabla(|u|^2 / 2) - u x omega`

does not shrink the same frozen localized LEI coefficient after localization
debt is restored.

The report sharpened the exact equation sheet. Starting from Navier-Stokes and
writing `omega = curl u`, one gets

`partial_t u - Delta u - u x omega + nabla pi = 0`, with `pi = p + |u|^2 / 2`,

or after Helmholtz projection,

`partial_t u - Delta u - P(u x omega) = 0`.

The attractive feature is the exact separation of the gradient part and the
Lamb-vector remainder, with the pointwise orthogonality
`u . (u x omega) = 0` as the best-case local cancellation. But once the fixed
CKN cutoff is inserted and the equation is paired against `u phi`, that same
orthogonality only removes the raw Lamb-vector term; the gradient piece
returns immediately as

`nabla pi . (u phi) = - pi u . nabla phi`.

Because `pi = p + |u|^2 / 2`, the localized packet therefore recreates the
same frozen LEI cutoff-flux bundle `((|u|^2 / 2) + p) u . nabla phi`, up to
the standard normalization. Projection, pressure recovery, nonlocality, and
cutoff commutators still belong to the candidate's own debt ledger. So the
rewrite weakens to an identity-level restatement rather than a smaller
coefficient on `I_flux[phi]`.

The Step-014 exchange and prior-art audit sharpens the same verdict. On the
repository record, the current packet adds no theorem-facing mathematical
delta beyond the same decomposition and the same favorable anchor case already
audited in Step 006. It also supplies no transfer lemma converting projected
Lamb-vector or localized Beltrami-deficit control into a positive-margin
smaller full `I_flux[phi]` coefficient after pressure, projection, and cutoff
debt are restored. That leaves the packet best recorded as recycled prior art
with its exchange path absent.

Under the branch rule, that leaves the candidate classified as
`reject as Tao-insufficient`.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-001-tao-screen-divergence-lamb.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-002-exact-and-localized-equations.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-003-exchange-prior-art-and-verdict.md`
