# Final Report: Strategy 001

## Executive Verdict

The far-field pressure harmonic loophole is **closed negatively**.

- [VERIFIED] The literal `beta = 4/3` bottleneck in Vasseur's De Giorgi recurrence is the **local non-divergence pressure term** `P_{k21}`, not the harmonic nonlocal term `P_{k1}`.
- [CHECKED] The loophole therefore survived only as a decomposition question: could an alternative near/far split move part of that dangerous interaction into a harmonic far-field component?
- [CHECKED] Tao's averaged Navier-Stokes does **not** preserve that mechanism in a clean form. The averaged equation is written through an averaged projected bilinear operator, not a local Poisson pressure law with a usable harmonic far-field split.
- [VERIFIED] Even so, the loophole does **not** survive. A minimal explicit model shows that harmonic far-field structure alone does not make the pressure pairing `U_k`-dependent. Constant and affine harmonic modes remain fixed by exterior data, not by the local De Giorgi quantity.

Mission-level judgment:

```text
loophole closed because harmonicity does not create U-dependence
```

## Directions Tried

### 1. Exact obstruction reconstruction

- [VERIFIED] Exploration 001 reconstructed the actual recurrence slot:

```text
I_k ≤ ||P_{k21}||_{L^q} ||d_k||_{L^2} ||1_{v_k>0}||_{L^{2q/(q-2)}}
    ≤ C_q C^k U_{k-1}^{4/3 - 5/(3q)}.
```

- [VERIFIED] The load-bearing arithmetic is

```text
U_{k-1}^0 × U_{k-1}^{1/2} × U_{k-1}^{5/6} = U_{k-1}^{4/3}.
```

- [CHECKED] This clarified the key mismatch: the mission's "far-field harmonic" language is not Vasseur's literal notation. `P_{k1}` is already harmonic and favorable; the bad term is local `P_{k21}`.

### 2. Tao filter

- [VERIFIED] Tao's ordinary bilinear operator is

```text
B(u,v) = -(1/2) P[(u·∇)v + (v·∇)u].
```

- [VERIFIED] Tao's averaged equation replaces this with an averaged operator `\tilde B` built from rotations, dilations, and order-zero Fourier multipliers applied to copies of `B`.
- [CHECKED] That keeps cancellation but loses the clean local Poisson pressure structure the loophole would need.
- [CHECKED] Verdict of this phase: the loophole is **Tao-incompatible**, so Tao alone does not close the mission.

### 3. Minimal falsification model

- [VERIFIED] Exploration 003 used the simplest possible model: a local ball `B_1`, a larger ball `B_2`, and a harmonic far-field pressure determined by boundary data on `∂B_2`.
- [VERIFIED] With constant boundary data, `p_far ≡ 1` on `B_1`, hence for any nonnegative local test function `ψ`,

```text
∫_{B_1} p_far ψ dx = ∫_{B_1} ψ dx,
```

which is independent of the local De Giorgi quantity.

- [CHECKED] Subtracting the constant mode does not save the route: affine harmonic modes still produce pairings controlled by exterior data, not by `U`.

## Strongest Findings

1. [VERIFIED] The surviving pressure-side loophole was a **decomposition mismatch**, not an overlooked weakness in Vasseur's harmonic estimate.
2. [CHECKED] The Tao filter showed the loophole depends on genuinely NS-specific local elliptic structure, because averaged NS does not preserve the needed local harmonic far-field decomposition.
3. [VERIFIED] The minimal model closes the route anyway: harmonicity controls smoothness and oscillation, but not the scaling coefficient. Exterior harmonic modes can stay nonzero while the local De Giorgi quantity is arbitrarily small.

## Negative Results and Dead Ends

- [VERIFIED] Reinterpreting the existing Vasseur harmonic term `P_{k1}` cannot help; it is already on the favorable side of the recurrence.
- [CHECKED] The Tao filter does not provide an early negative result because the loophole is Tao-incompatible rather than Tao-compatible.
- [VERIFIED] The only remaining positive hope was that harmonicity itself could force `U`-dependence. The minimal model falsified exactly that claim.

## Strongest Counterargument

The strongest counterargument is that the true Navier-Stokes far-field pressure is not an arbitrary harmonic function; perhaps the quadratic NS source imposes hidden compatibility conditions that tie exterior harmonic amplitude to the local level-set energy.

Response:

- [CHECKED] That would require extra NS-specific structure beyond harmonicity alone.
- [VERIFIED] The loophole under investigation was precisely the claim that **harmonicity** of the far-field piece could do the work.
- [CHECKED] Once harmonicity alone is shown insufficient, the loophole as stated is closed. Any further positive route would be a different mechanism and should be treated as a new mission, not a continuation of this one.

## Recommended Next Move for the Missionary

- [CHECKED] Mark this lead closed.
- [CHECKED] Do not spend more budget on generic harmonic far-field pressure refinements inside the De Giorgi / epsilon-regularity family.
- [CHECKED] If pressure is revisited at all, it should be under a new mission with a different claimed mechanism, not "harmonic far-field pressure by itself."

## Claims Worth Carrying Forward

- [VERIFIED] The exact obstruction is local `P_{k21}`, with recurrence arithmetic `0 + 1/2 + 5/6 = 4/3`.
- [CHECKED] Tao's averaged NS destroys the local harmonic far-field structure, so the loophole is NS-specific rather than generic.
- [VERIFIED] Harmonic far-field structure alone does not create `U`-dependence; constant and affine harmonic modes provide the minimal countermodel.
