# Exact Surviving Far-Field Pairing

Status: `VERIFIED`

The exact far-field contribution inherited by the beyond-De Giorgi branch is

`I_p^far = -\iint p_far div(v_k phi_k^2 e_hat)`

with expansion

`I_p^far = -\iint p_far (e_hat . grad v_k) phi_k^2`
`          - 2 \iint p_far v_k phi_k (e_hat . grad phi_k)`
`          - \iint p_far v_k phi_k^2 div(e_hat)`.

Inside this full pairing, the dominant live term is

`I_p^far,main = - 2 \iint p_far v_k phi_k (e_hat . grad phi_k)`.

The `(e_hat . grad v_k) phi_k^2` piece is absorbed into dissipation and the
`div(e_hat)` piece is lower order, but the full obstruction still sits in the
complete divergence pairing above.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-001-exploration-001-far-field-obstruction-reconstruction.md`
