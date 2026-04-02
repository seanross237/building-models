---
topic: Exact delayed-transfer precursor pair has no backward-memory link in the filtered-energy identity
confidence: checked
date: 2026-04-01
source: "exact-ns-hidden-precursor-firewall strategy-001 exploration-003 report"
---

## Finding

For the frozen physical-space pair consisting of the later event `E_flux` and the earlier precursor

```text
P_flux^-(R_-)
  = integral_{t_* - Delta}^{t_* - delta} integral_{B_r(x_*)} (Pi_ell)_+ dx dt,
```

the exact filtered local energy balance is too time-local to prove a theorem of the form

```text
P_flux^-(R_-) <= epsilon  =>  E_flux is impossible.
```

The later witness gain is controlled only by terms on the final window `[t_* - delta, t_*]`. The earlier slab `R_-` never appears in the exact identity.

## Exact Obstruction

Using the event from `exact-ns-physical-space-delayed-transfer-event.md`, subtract the filtered balances at scales `ell/rho` and `ell` and integrate over the final window. Schematically,

```text
W(t_*) - W(t_* - delta)
  = integral_{later} (Pi_ell - Pi_{ell/rho})
    + boundary transport terms
    + viscous band terms.
```

Every exact control term lives on the later window itself. None contains the earlier cumulative precursor slab `R_-`.

So the preferred pair fails for a structural reason stronger than "no proof found": the exact balance has no backward-memory term tying the earlier slab to the later burst.

## Why Small Earlier Flux Does Not Contradict The Event

The failure is dynamical time-locality:

- the balance law controls change over the chosen window, not over a disjoint earlier slab,
- `E_flux` can be realized by a burst concentrated entirely inside the final window,
- boundary transport can feed the later witness without forcing earlier interior buildup,
- viscous terms are also confined to the later window.

Because `P_flux^-` only measures earlier cumulative forward transfer, small `P_flux^-(R_-)` is compatible with a later same-scale burst.

## Consequence

The preferred physical-space precursor pair does **not** support a no-hidden-transfer firewall theorem by exact-identity methods alone.

Rescuing such a theorem would require extra input absent from the exact balance itself, for example:

- a one-sided temporal persistence or modulus-of-continuity bound for `Pi_ell`,
- a monotonicity principle for a cumulative transfer quantity,
- a transport estimate forcing later witness gain to come from earlier interior buildup,
- or a different precursor family with genuine built-in memory rather than a disjoint earlier slice.

## Relationship To Other Entries

- `exact-ns-delayed-transfer-precursor-pair.md` records why this pair was still the best theorem-facing precursor candidate before the structural memory audit.
- `exact-ns-physical-space-delayed-transfer-event.md` defines the later flux-plus-witness event whose preferred precursor theorem this entry closes negatively.
- This entry leaves the event definition and pair selection intact, but kills the identity-only no-hidden-transfer route for that pair.
