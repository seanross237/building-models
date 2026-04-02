# Projected And Vorticity Rewrites Must Pay Localization Debt

Status: `INFERRED`

The first explicit package-mismatch risk in the fixed-protocol rewrite audit is
counting projected, Lamb-vector, or vorticity identities as gains before
paying the debts created by localization.

Under the frozen protocol, an identity such as

`P[(u . ∇)u] = -P(u x omega)`

does not earn credit merely in its global or unlocalized form. Once the cutoff
is fixed, any attempt to move it through Helmholtz projection, Calderon-Zygmund
reconstruction, or Biot-Savart reinsertions creates nonlocal and commutator
costs that belong in the candidate's own ledger.

So operator placement after localization is the branch's first circularity
check: if the apparent gain disappears once those costs are restored, the
rewrite was only cosmetic.

The later Step-6 vorticity / Biot-Savart screen sharpens the candidate-level
consequence. For that route, the only honest localized insertion point is a
formal attempt to rewrite velocity-side factors inside `I_flux[phi]` through
`omega` after localization. Once the inherited Biot-Savart and commutator
costs are restored, no separate estimate-level gain remains.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-005-exploration-002-compatibility-localization-protocol.md`
- `missions/beyond-de-giorgi/library-inbox/step-006-exploration-002-tao-screen-vorticity-biot-savart.md`
