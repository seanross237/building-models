---
topic: Exact delayed-transfer event's preferred precursor pair is earlier cumulative positive forward flux on the predecessor slab
confidence: checked
date: 2026-04-01
source: "exact-ns-hidden-precursor-firewall strategy-001 exploration-002 report; exact-ns-hidden-precursor-firewall strategy-001 exploration-003 report"
---

## Finding

For the exact-Navier-Stokes delayed-transfer event `E_flux`, the preferred earlier warning is not Lamb-vector geometry, not vortex stretching, and not a second copy of the event itself. It is the earlier cumulative positive forward flux through the same coarse-graining interface, measured on the disjoint predecessor slab of the already-declared event cylinder.

## Preferred Pair

Using the exact forward-transfer rate `Pi_ell` from `exact-ns-physical-space-delayed-transfer-event.md`, the preferred precursor observable is

```text
P_flux^-(R_-)
  = integral_{t_* - Delta}^{t_* - delta} integral_{B_r(x_*)} (Pi_ell(x,t))_+ dx dt.
```

The preferred earlier region is not a new cone or enlarged ball. It is the literal earlier part of the same parabolic cylinder:

```text
R_- = B_r(x_*) x [t_* - Delta, t_* - delta].
```

The intended "no earlier warning" regime is therefore

```text
P_flux^-(R_-) <= epsilon_prec.
```

## Why This Pair Survives

- It stays on exact Navier-Stokes itself and uses the same transfer observable `Pi_ell` that defines the later event.
- It is dynamically tied to the later witness activation: the witness channel only rises if forward transfer through the same interface has already accumulated.
- It is less tautological than reusing the event window itself: the precursor is measured on a disjoint earlier interval and drops the later witness-gain clause.
- It avoids a second region-design exploration: once the event cylinder is fixed, the least-arbitrary earlier region is the predecessor slab of that same cylinder.

So the gate passes, but only narrowly: the surviving precursor remains close to the event family, yet it is sharp enough to support a real theorem or counterexample test.

Exploration-003 later sharpened the limitation: this pair is still the preferred candidate, but the exact filtered-energy identity has no backward-memory term linking the earlier slab to the later witness window, so the clean no-hidden-transfer route is structurally closed.

## Backup And Rejected Alternatives

The only live backup is earlier Duchon-Robert activity on the same predecessor slab:

```text
P_DR^-(R_-)
  = integral_{t_* - Delta}^{t_* - delta} integral_{B_r(x_*)} (D_ell(u)(x,t))_+ dx dt.
```

It stays backup only because it is one step less directly tied to the selected witness channel and slides more easily into a generic singularity-detection framing.

Rejected preferred families:

- Lamb / near-Beltrami geometry — too fragile under perturbation and too pressure-adjacent to anchor the preferred precursor.
- Vortex stretching / enstrophy production — too generic and not naturally tied to the declared scale interface or witness channel.
- "Same burst quantity, slightly earlier" — rejected as the tautological version of the precursor.

## Next Honest Attack

With the pair fixed, the next exploration should not reopen precursor selection.

Exploration-003 resolved the most natural exact-identity target negatively: a no-hidden-transfer theorem of the form

```text
P_flux^-(R_-) <= epsilon_prec  =>  E_flux is impossible
```

does **not** follow from the exact filtered-energy balance, because the later witness identity never sees the earlier slab `R_-`.

So the honest continuations after the pair-selection gate are now:

1. add an explicit extra hypothesis that would supply temporal memory,
2. produce a faithful counterexample where `P_flux^-(R_-)` stays small but `E_flux` still occurs,
3. or switch to a different precursor family only if it repairs the missing memory link rather than merely changing vocabulary.

## Relationship To Other Entries

- `exact-ns-physical-space-delayed-transfer-event.md` defines the later exact-NS event whose preferred earlier warning this entry fixes.
- `exact-ns-delayed-transfer-precursor-no-backward-memory.md` records the structural negative on the identity-only no-hidden-transfer theorem for this frozen pair.
- `tao-averaged-ns-delayed-transfer-circuit.md` gives the reduced five-role delayed-transfer mechanism that motivates looking for a hidden precursor at all.
- `near-beltrami-negative-result.md` records the fragility that keeps Lamb / near-Beltrami geometry out of the preferred precursor slot.
