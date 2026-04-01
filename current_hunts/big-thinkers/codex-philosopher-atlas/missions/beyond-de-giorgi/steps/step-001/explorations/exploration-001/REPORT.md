# Exploration 001 Report — Exact Far-Field Pressure Obstruction Reconstruction

## Goal

Reconstruct the exact surviving far-field pressure pairing for the `beyond-de-giorgi`
step from the copied `vasseur-pressure` and related Navier-Stokes architecture
materials, and state precisely:

- the exact live formula for `I_p^far`
- which pressure pieces or harmonic modes are already annihilated by the
  localization/test structure
- what the actual bad coefficient is
- what quantity would need to become smaller for there to be real progress

## Required Source Anchors

- `missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
- `missions/vasseur-pressure/steps/step-001/RESULTS.md`
- `missions/vasseur-pressure/steps/step-002/RESULTS.md`
- `missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
- `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`

## Method

I am extracting the exact formulas and cancellation structure from the required
source anchors, then separating:

- the full far-field pairing
- the modes already killed by the test/localization structure
- the surviving affine-or-higher harmonic content
- the true coefficient-side obstruction

## Findings Log

### Initial Setup

- Created report skeleton before formula extraction, per role instructions.

### Source-Based Reconstruction

#### 1. Pressure term before the near/far split

From `missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
lines 101-117:

- [VERIFIED] The pressure contribution in the localized De Giorgi inequality is

  `I_p = \iint (e_hat · grad p) v_k phi_k^2`

  and, after integration by parts,

  `I_p = -\iint p div(v_k phi_k^2 e_hat)`.

- [VERIFIED] Expanding the divergence gives

  `div(v_k phi_k^2 e_hat) = (e_hat · grad v_k) phi_k^2 + 2 v_k phi_k (e_hat · grad phi_k) + v_k phi_k^2 div(e_hat)`.

- [VERIFIED] Therefore

  `I_p = -\iint p (e_hat · grad v_k) phi_k^2`
  `      - 2 \iint p v_k phi_k (e_hat · grad phi_k)`
  `      - \iint p v_k phi_k^2 div(e_hat)`.

- [VERIFIED] The same source marks the second term

  `- 2 \iint p v_k phi_k (e_hat · grad phi_k)`

  as the "MAIN pressure error," while the first is absorbed into dissipation and
  the third is lower order.

#### 2. Exact far-field pairing

Let

`p = p_local + p_far`

with `p_far` the harmonic/non-local part from
`missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
lines 184-195 and
`missions/navier-stokes/library-inbox/vasseur-2007-proof-architecture.md`
lines 157-166.

Then the exact surviving far-field pairing is:

`I_p^far = -\iint p_far div(v_k phi_k^2 e_hat)`

that is,

`I_p^far = -\iint p_far (e_hat · grad v_k) phi_k^2`
`          - 2 \iint p_far v_k phi_k (e_hat · grad phi_k)`
`          - \iint p_far v_k phi_k^2 div(e_hat)`.

- [VERIFIED] This is the full far-field pairing inherited from the general
  pressure identity above.
- [VERIFIED] The dominant live term is

  `I_p^far,main = - 2 \iint p_far v_k phi_k (e_hat · grad phi_k)`,

  because the source explicitly identifies the `grad phi_k` term as the main
  pressure error.

#### 3. Operative bound actually carried forward

Two formula layers appear in the copied pressure-dissection note:

- [VERIFIED] A schematic line at
  `exploration-002-pressure-dissection-de-giorgi.md:190-197` says
  `I_p^far <= C_far 2^{12k/5} U_k^{sigma_far}` with a generic `sigma_far`.
- [VERIFIED] The same file later gives the concrete bound

  `I_p^far <= ||p_far||_{L^infty} ||v_k||_{L^1} 2^k`
  `        <= C_far 2^{12k/5} U_k^{6/5}`,

  with

  `C_far = ||p_far||_{L^infty(Q_k)} ~ ||u||_{L^2}^2 / r_k^3`.

- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-001/attacks/chain-01.md`
  lines 9-13 treats this concrete `6/5` estimate as the key inherited formula.

Conclusion:

- [VERIFIED] The live formula to carry into `beyond-de-giorgi` Step 1 is

  `I_p^far <= C_far 2^{12k/5} U_k^{6/5}`,

  with

  `C_far ~ ||u||_{L^2}^2 / r_k^3`.

- [INFERRED] The schematic `sigma_far` line is not the operative obstruction for
  this step; the chain itself adopts the explicit `L^infty`/`6/5` version.

#### 4. Which harmonic modes are already annihilated?

Define

`F_k := v_k phi_k^2 e_hat`,
`psi_k := div(F_k)`.

Then

`I_p^far = -\iint p_far psi_k`.

Because `phi_k` is a compactly supported localization,

`- \int h(x) psi_k(x,t) dx = \int grad h(x) · F_k(x,t) dx`

for each fixed `t` and each harmonic polynomial `h`.

From this:

- [INFERRED] **Constant harmonic mode is already killed.**
  If `h(x) = c`, then `grad h = 0`, so
  `-\int c psi_k dx = 0`.
  Equivalently, `\int psi_k dx = \int div(F_k) dx = 0`.

- [INFERRED] **Affine harmonic modes are not killed generically.**
  If `h(x) = a + b · x`, then
  `-\int h psi_k dx = b · \int F_k dx`
  `= b · \int v_k phi_k^2 e_hat dx`,
  and there is no source-supported structural reason for this vector moment to
  vanish.

- [INFERRED] **Higher harmonic modes also survive generically.**
  For quadratic-and-higher harmonic pieces, the pairing becomes moments of
  `F_k` against the corresponding gradients. No cancellation mechanism in the
  required source anchors annihilates these modes wholesale.

- [INFERRED] Therefore the only mode already annihilated automatically by
  `div(v_k phi_k^2 e_hat)` is the constant mode. Affine-or-higher harmonic
  content remains live unless an additional NS-specific cancellation is found.

#### 5. Full pairing versus dominant live term

- [VERIFIED] Full far-field object:

  `I_p^far = -\iint p_far div(v_k phi_k^2 e_hat)`.

- [VERIFIED] Dominant live term inside it:

  `- 2 \iint p_far v_k phi_k (e_hat · grad phi_k)`.

- [INFERRED] This distinction matters for mode subtraction:
  constant subtraction is harmless because the full divergence pairing kills
  constants, but subtracting only a constant does not neutralize the affine or
  higher harmonic pieces that still feed the `grad phi_k`-driven main error.

#### 6. What is actually bad?

From
`missions/vasseur-pressure/steps/step-001/RESULTS.md` lines 25-38 and
`missions/vasseur-pressure/library-inbox/exploration-002-pressure-dissection-de-giorgi.md`
lines 275-283:

- [VERIFIED] Local pressure already closes:
  `I_p^local <= C 2^{6k/5} U_k^{8/5}`.

- [VERIFIED] Far-field pressure is isolated as the sole obstruction.

- [VERIFIED] The bad coefficient is

  `C_far = ||p_far||_{L^infty(Q_k)} ~ ||u||_{L^2}^2 / r_k^3`,

  i.e. a fixed energy-class constant, not a quantity shrinking with `U_k`.

- [VERIFIED] `chain-01.md` lines 11-13 states the obstruction exactly:
  the issue is not the `U_k^{6/5}` power anymore; the issue is coefficient
  smallness.

#### 7. What would need to become smaller for real progress?

- [INFERRED] Real progress would mean replacing the current coefficient-side
  bound by some effective coefficient `C_far,eff(k)` satisfying

  `|I_p^far| <= C_far,eff(k) 2^{12k/5} U_k^{6/5}`

  with `C_far,eff(k)` genuinely smaller than the fixed-energy-scale quantity
  `||u||_{L^2}^2 / r_k^3`, or at least tied to admissible data in a way that can
  become small/summable.

- [INFERRED] Merely controlling `p_far` modulo constants is cosmetic, because
  the constant mode is already annihilated by the pairing.

- [INFERRED] Harmonic smoothness by itself is also cosmetic unless it yields a
  smaller coefficient for the **full** pairing, including the surviving affine
  and higher harmonic content. This is exactly the warning in
  `chain-01.md:19-21`.

- [VERIFIED] `missions/vasseur-pressure/steps/step-002/RESULTS.md` lines 17-21
  confirm that even the attempted `H^1` replacement norms remain fixed
  energy-class constants and therefore do not improve the coefficient side of
  the De Giorgi estimate.

## Formula Sheet

1. [VERIFIED] Full far-field pairing:

   `I_p^far = -\iint p_far div(v_k phi_k^2 e_hat)`.

2. [VERIFIED] Expanded form:

   `I_p^far = -\iint p_far (e_hat · grad v_k) phi_k^2`
   `          - 2 \iint p_far v_k phi_k (e_hat · grad phi_k)`
   `          - \iint p_far v_k phi_k^2 div(e_hat)`.

3. [VERIFIED] Dominant live term:

   `I_p^far,main = - 2 \iint p_far v_k phi_k (e_hat · grad phi_k)`.

4. [INFERRED] Modes already killed by the test/localization structure:

   constants only.

5. [INFERRED] Surviving harmonic content:

   affine and higher harmonic modes, because the pairing reduces to moments of
   `F_k = v_k phi_k^2 e_hat`, not just to oscillation modulo constants.

6. [VERIFIED] Operative estimate inherited by this mission:

   `I_p^far <= C_far 2^{12k/5} U_k^{6/5}`.

7. [VERIFIED] Actual bad coefficient:

   `C_far ~ ||u||_{L^2}^2 / r_k^3`.

8. [INFERRED] Quantity that must improve for genuine progress:

   a smaller coefficient-side control on the full far-field pairing, not merely
   smoother or smaller killed modes.

## Open Questions

- Exact normalization/sign conventions for the pressure term across the copied
  notes.
- Whether the dominant surviving term is presented as a single integral or only
  after a harmonic/Taylor decomposition.

## Dead Ends / Failed Attempts

- The copied pressure-dissection note contains a schematic far-field line with a
  generic `sigma_far`, but later in the same file the concrete operative bound is
  `I_p^far <= C_far 2^{12k/5} U_k^{6/5}`. I am treating the latter as the live
  obstruction because `chain-01.md` explicitly carries that formula forward.
