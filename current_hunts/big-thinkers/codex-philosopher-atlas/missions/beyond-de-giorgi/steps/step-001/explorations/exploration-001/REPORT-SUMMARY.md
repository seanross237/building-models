# REPORT SUMMARY

## Goal

Reconstruct the exact surviving far-field pressure pairing for the
`beyond-de-giorgi` Step 1 obstruction, identify which harmonic modes are
already killed by the localization/test structure, isolate the true bad
coefficient, and state what would actually have to get smaller for progress.

## What I Checked

- `missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`

I reconstructed the pressure identity, inserted the `p = p_local + p_far`
split, separated the full far-field pairing from the dominant `grad phi_k` term,
and then checked which harmonic polynomial modes are automatically annihilated by
`div(v_k phi_k^2 e_hat)`.

## Outcome

Succeeded.

The explicit reconstruction is:

- Full pairing:
  `I_p^far = -\iint p_far div(v_k phi_k^2 e_hat)`.
- Expanded form:
  `I_p^far = -\iint p_far (e_hat · grad v_k) phi_k^2`
  `          - 2 \iint p_far v_k phi_k (e_hat · grad phi_k)`
  `          - \iint p_far v_k phi_k^2 div(e_hat)`.
- Dominant live term:
  `I_p^far,main = - 2 \iint p_far v_k phi_k (e_hat · grad phi_k)`.
- Operative inherited estimate:
  `I_p^far <= C_far 2^{12k/5} U_k^{6/5}`,
  with
  `C_far ~ ||u||_{L^2}^2 / r_k^3`.

Mode bookkeeping:

- [INFERRED] Constant harmonic mode is already killed by the divergence pairing.
- [INFERRED] Affine harmonic modes are not killed generically.
- [INFERRED] Higher harmonic modes are also not killed generically.

## One Key Takeaway

The obstruction is coefficient-side, not exponent-side: the live issue is the
fixed coefficient `C_far ~ ||u||_{L^2}^2 / r_k^3`, not the `U_k^{6/5}` power.
Controlling only harmonic smoothness or oscillation modulo constants is cosmetic
because constants are already annihilated.

## Leads Worth Pursuing

- Any Step 2 candidate must produce a smaller effective coefficient
  `C_far,eff(k)` for the full pairing, not just for `p_far` modulo constants.
- If a quotient norm is tried, it has to neutralize only modes truly killed by
  the pairing and still control the surviving affine-and-higher content.
- A toy remote-shell countermodel remains worth doing later: compute the
  harmonic polynomial induced on the inner cylinder and test whether its pairing
  coefficient is still comparable to shell energy.

## Unexpected Findings

- The copied pressure-dissection note contains both a schematic far-field
  exponent line and a later concrete `6/5` bound; `chain-01.md` makes clear that
  the concrete `I_p^far <= C_far 2^{12k/5} U_k^{6/5}` formula is the operative
  one for this mission.
- The required source anchors do not support any generic cancellation beyond the
  constant mode.

## Live Target Quantity For Step 2

Yes: the only live target is a genuinely smaller coefficient-side control for
the full far-field pairing, for example an effective `C_far,eff(k)` in

`|I_p^far| <= C_far,eff(k) 2^{12k/5} U_k^{6/5}`,

with `C_far,eff(k)` materially better than `||u||_{L^2}^2 / r_k^3` from
admissible Navier-Stokes data.

## Computations Worth Doing Later

- Build the explicit remote-shell harmonic-polynomial model requested by
  `chain-01.md` to test whether any local oscillation/Campanato/BMO-type norm is
  truly smaller than the shell-energy scale on the surviving pairing.
