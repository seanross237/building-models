# Constant Harmonic Mode Is Automatically Killed

Status: `INFERRED`

Let `F_k = v_k phi_k^2 e_hat` and `psi_k = div(F_k)`, so

`I_p^far = -\iint p_far psi_k`.

For any constant harmonic function `h(x) = c`,

`-\int h psi_k dx = \int grad h . F_k dx = 0`

because `grad h = 0`. Equivalently,

`\int psi_k dx = \int div(F_k) dx = 0`.

Constant subtraction is therefore already built into the
localization/test-structure pairing.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-001-exploration-001-far-field-obstruction-reconstruction.md`
