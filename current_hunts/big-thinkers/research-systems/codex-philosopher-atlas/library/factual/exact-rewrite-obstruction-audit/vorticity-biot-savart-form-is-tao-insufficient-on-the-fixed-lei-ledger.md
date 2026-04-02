# Vorticity Biot Savart Form Is Tao-Insufficient On The Fixed LEI Ledger

Status: `INFERRED`

Within the Step-2 Tao screen for the fixed exact-rewrite audit, the
`vorticity transport / Biot-Savart form`

does not produce a smaller coefficient on the frozen localized LEI target
`I_flux[phi]`.

The exact equation sheet is

`partial_t omega - Delta omega + (u . nabla)omega - (omega . nabla)u = 0`,

with exact velocity reconstruction

`u = curl (-Delta)^(-1) omega`.

Its apparent gain is only a relocation of the same quadratic interaction to a
vorticity-side representation. The native vorticity equation does not itself
act on the frozen LEI cutoff-flux bundle. To touch `I_flux[phi]`, the
candidate must first reconstruct every velocity-side factor through
Biot-Savart and then recover pressure through the same nonlocal quadratic
velocity package.

The Step-006 exploration-002 audit sharpens the verdict in two ways. First,
it makes the insertion point explicit: after localization, the only honest move
is to rewrite velocity-side factors inside `I_flux[phi]` through `omega`, so
the candidate never reaches a new estimate outside the frozen flux bundle.
Second, it shows that any apparent rescue by stretching, alignment, tube
structure, or related geometry-facing observables has already drifted into a
different branch rather than saving this rewrite on its own ledger.

The Step-014 exact-and-localized-equations report sharpens that further: the
candidate reaches the full theorem-facing burden only after full velocity and
pressure reconstruction, schematically

`I_flux[phi] = integral integral (|BS[omega]|^2 + 2 p[omega]) BS[omega] . nabla phi`.

So the native equation acts on a surrogate, while the full frozen burden is
recovered only after the exchange step where Biot-Savart, Riesz, nonlocality,
admissibility, and cutoff-commutator debts all re-enter.

The Step-014 exchange and prior-art audit closes the comparator question too:
the current packet still provides no theorem-facing mathematical delta beyond
the same vorticity transport plus Biot-Savart representation already on disk.
It names no localized transfer lemma turning `omega`-side substitution,
velocity reconstruction, and pressure recovery into a positive-margin smaller
full `I_flux[phi]` coefficient after Biot-Savart, reconstruction, and cutoff
debt are paid. So the packet is best recorded as recycled prior art with its
exchange path absent.

Under the branch rule, that leaves the candidate classified as
`reject as Tao-insufficient`.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-002-tao-screen-vorticity-biot-savart.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-003-unified-tao-verdict.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-002-exact-and-localized-equations.md`
- `missions/beyond-de-giorgi/library-inbox/step-014-exploration-003-exchange-prior-art-and-verdict.md`
