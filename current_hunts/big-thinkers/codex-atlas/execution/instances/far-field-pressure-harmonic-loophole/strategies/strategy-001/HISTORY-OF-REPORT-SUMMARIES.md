# History Of Report Summaries

## Exploration 001

# Exploration 001 Summary: Reconstruct the Exact Far-Field Pressure Obstruction

- Goal: reconstruct, in equations, the exact pressure obstruction behind the mission's far-field harmonic loophole and isolate the statement needed for the Tao filter.
- What I tried: reconciled Vasseur's actual pressure decomposition with the later H^1/far-field framing, using the local library notes and the prior Vasseur strategy reports.
- Outcome: succeeded.
- Key takeaway: the literal `beta = 4/3` bottleneck in Vasseur is the **local non-divergence term `P_{k21}`**, while the mission's loophole language is about an **alternative harmonic far-field split**. The real question for the next exploration is whether such a harmonic far-field decomposition can absorb the dangerous contribution that Vasseur isolates as local.
- Exact obstruction recovered:
  `I_k ≤ ||P_{k21}||_{L^q} ||d_k||_{L^2} ||1_{v_k>0}||_{L^{2q/(q-2)}}` with
  `||P_{k21}||_{L^q} ≤ C_q`, `||d_k||_{L^2} ≤ U_{k-1}^{1/2}`, and `||1_{v_k>0}|| ≤ C^k U_{k-1}^{5(q-2)/(6q)}`, giving
  `I_k ≤ C_q C^k U_{k-1}^{4/3 - 5/(3q)} -> U_{k-1}^{4/3}`.
- Leads worth pursuing: Tao-filter the **alternative harmonic far-field decomposition**, not the already-favorable Vasseur harmonic term `P_{k1}`.
- Unexpected finding: the H^1 dead-end note uses "far-field" language in a way that is not literally consistent with Vasseur's notation; this appears to be a conceptual shorthand rather than a literal identification of `P_{k21}` as a far-field term.
- Computations worth doing later: if the Tao filter leaves the loophole alive, compute the alternative far/near split explicitly in a Wolf-type local pressure framework and test whether any part of the Vasseur `P_{k21}` contribution is truly moved into a harmonic component.

## Exploration 002

# Exploration 002 Summary: Tao Filter for the Harmonic Far-Field Pressure Loophole

- Goal: decide whether the mission's harmonic far-field pressure loophole is Tao-compatible, Tao-incompatible, or still unclear.
- What I tried: compared the loophole reconstructed in exploration 001 against Tao's averaged bilinear operator formulation, using Tao's primary bilinear-operator definition plus the repo's prior Tao notes.
- Outcome: succeeded.
- Key takeaway: the loophole is **Tao-incompatible**. Tao's averaged equation preserves only the projected bilinear operator structure and cancellation, not the local Poisson pressure law or a clean near/far harmonic pressure split on the working cylinder.
- Exact finding: ordinary NS uses `-Δp = ∂i∂j(u_i u_j)`, while Tao's model is written as `∂_t u = Δu + \tilde B(u,u)` with `\tilde B` an average of rotated/dilated/multiplier-modified copies of the Euler bilinear operator. No canonical local pressure equation of the same form survives.
- Leads worth pursuing: because Tao does not close the route, exploration 003 should build a minimal explicit model of harmonic far-field pressure and test whether harmonicity can ever make the pressure pairing `U_k`-dependent rather than merely changing constants.
- Unexpected finding: the decisive structural break is not rotation or dilation, but the order-zero Fourier multipliers in Tao's averaging, which are nonlocal and therefore destroy the local harmonicity structure the loophole needs.
- Computations worth doing later: if exploration 003 is run, formulate the model in a Wolf-style local harmonic+particular pressure split and test whether any analogue of the Vasseur `P_{k21}` contribution can actually move into the harmonic component.

## Exploration 003

# Exploration 003 Summary: Minimal Falsification Model for Harmonic Far-Field Pressure

- Goal: test, in the smallest explicit model, whether a harmonic far-field pressure piece can make the pressure pairing genuinely `U`-dependent.
- What I tried: used a local ball `B_1`, a larger ball `B_2`, and a harmonic far-field component determined by exterior / boundary data; then paired it against a nonnegative local test function.
- Outcome: succeeded.
- Key takeaway: **harmonicity does not create `U`-dependence**. With constant boundary data on `∂B_2`, the harmonic far-field pressure is `p_far ≡ 1` on `B_1`, so the local pairing is just `∫_{B_1} ψ`, independent of the local De Giorgi quantity `U`.
- Leads worth pursuing: none for this loophole as stated. Any surviving positive route would need extra NS-specific structure beyond harmonicity alone.
- Unexpected finding: even subtracting the constant mode does not save the mechanism; affine harmonic modes still produce exterior-data-scale pairings independent of `U`.
- Computations worth doing later: only if one wants a stronger publication-grade version, one could embed the same argument into a Wolf-style local harmonic+particular decomposition, but it is not needed for the mission verdict.
