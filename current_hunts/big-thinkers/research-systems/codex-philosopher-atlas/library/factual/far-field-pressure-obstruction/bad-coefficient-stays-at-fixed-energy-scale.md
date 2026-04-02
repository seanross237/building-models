# Bad Coefficient Stays At Fixed Energy Scale

Status: `VERIFIED`

The operative inherited estimate is

`I_p^far <= C_far 2^{12k/5} U_k^{6/5}`

with

`C_far = ||p_far||_{L^\infty(Q_k)} ~ ||u||_{L^2}^2 / r_k^3`.

For this branch, the concrete `L^\infty` and `U_k^{6/5}` estimate is the live
formula carried forward, not the earlier schematic `sigma_far` placeholder.
What remains bad is the coefficient: it sits at fixed energy scale instead of
shrinking with `U_k`.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-001-exploration-001-far-field-obstruction-reconstruction.md`
