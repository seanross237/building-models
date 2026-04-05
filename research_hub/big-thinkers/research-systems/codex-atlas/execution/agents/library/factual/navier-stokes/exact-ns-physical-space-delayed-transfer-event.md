---
topic: Exact Navier-Stokes admits a physical-space delayed-transfer event defined by localized forward flux burst and subscale witness gain
confidence: checked
date: 2026-04-01
source: "exact-ns-hidden-precursor-firewall strategy-001 exploration-001 report; exact-ns-hidden-precursor-firewall strategy-001 exploration-002 report; exact-ns-hidden-precursor-firewall strategy-001 exploration-003 report"
---

## Finding

The faithful physical-space exact-Navier-Stokes analogue of Tao's delayed-abrupt-transfer mechanism is not a packet circuit, a pressure criterion, or a standalone trigger observable. It is a localized interscale handoff across one coarse-graining interface.

The preferred event is a short-window burst of positive forward flux into smaller scales together with abrupt growth of a local subscale witness channel after an earlier quiet interval.

## Exact Event

For a smooth filter `G_ell`, define

```text
u_bar_ell = G_ell * u,
tau_ell(u,u) = overline(u tensor u)_ell - u_bar_ell tensor u_bar_ell,
Pi_ell = - grad u_bar_ell : tau_ell(u,u).
```

Here `Pi_ell(x,t) > 0` is the exact local forward transfer rate from resolved scales `> ell` into unresolved scales `< ell`.

To keep a named output channel, fix `rho > 1` and define on a ball `B_r(x_*)`

```text
W_{ell,rho,r}(t)
  = (1/2) integral_{B_r(x_*)}
      (|u_bar_{ell/rho}|^2 - |u_bar_ell|^2)(x,t) dx.
```

Let

```text
F_ell(t) = integral_{B_r(x_*)} (Pi_ell(x,t))_+ dx.
```

On the parabolic cylinder `Q = B_r(x_*) x [t_* - Delta, t_*]`, the localized delayed-transfer event
`E_flux(x_*, t_*; ell, rho, r, Delta, delta)` occurs when

1. the earlier window stays quiet:

```text
sup_{t in [t_* - Delta, t_* - delta]} F_ell(t) <= eta_flux,
sup_{t in [t_* - Delta, t_* - delta]} W_{ell,rho,r}(t) <= eta_w,
```

2. the final short window carries a forward-flux burst:

```text
integral_{t_* - delta}^{t_*} F_ell(t) dt >= A_flux,
```

3. the subscale witness channel activates:

```text
W_{ell,rho,r}(t_*) - W_{ell,rho,r}(t_* - delta) >= A_w.
```

This gives one exact-NS event with a named output channel, spacetime localization, baseline regime, threshold window, and measurable hidden-until-threshold clause.

## Why This Is The Preferred Object

The Tao map is:

- delayed trigger logic -> earlier small `Pi_ell^+`
- conduit switch-on -> short-window burst of `Pi_ell^+`
- next-carrier activation -> abrupt rise of `W_{ell,rho,r}`

The event is faithful because it keeps the dynamical object as the exact Navier-Stokes solution. The filter kernel, interface scale, scale ratio, region, and thresholds are observability conventions applied to the exact solution, not a reduced dynamical model.

## Backup And Scope

A localized Duchon-Robert inertial-dissipation burst on the same parabolic cylinder is a defensible backup event, but only as backup. It is more singularity-facing and less clearly a "next carrier" witness than the flux-plus-witness event above.

Exploration 002 sharpened the precursor side without changing the event: the preferred earlier warning is cumulative positive `Pi_ell` mass on the predecessor slab

```text
R_- = B_r(x_*) x [t_* - Delta, t_* - delta]
```

while earlier Duchon-Robert activity on that same slab remains backup only.

This entry is now the event-side definition. Exploration-003 closed the clean no-hidden-transfer route negatively for the selected same-family precursor pair: the exact filtered balance has no backward-memory term linking the earlier slab to the final witness window. The remaining honest continuations are extra-memory hypotheses, faithful counterexamples, or a genuinely different precursor family.

Later phase-locking work reused this event only as a **shape anchor**. The same smooth scale-interface and delayed-transfer logic survived, but the preferred phase-coupled companion dropped the spatial cutoff to preserve a clean exact helical triad ledger. That global spectral continuation is recorded in `exact-ns-transfer-coherence-phase-observable.md`.

## Relationship To Other Entries

- `tao-averaged-ns-delayed-transfer-circuit.md` gives the reduced five-role delayed-transfer mechanism whose physical-space exact-NS analogue this entry fixes.
- `packetized-tao-circuit-noncanonical.md` explains why the continuation moved away from packet canonization and toward an exact-NS physical-space event.
- `exact-trigger-object-not-standalone.md` records the failed trigger-only narrowing on the older helical-object branch.
- `exact-ns-delayed-transfer-precursor-pair.md` records the preferred earlier-warning pair on the predecessor slab of the same event cylinder.
- `exact-ns-delayed-transfer-precursor-no-backward-memory.md` records the structural negative on the identity-only no-hidden-transfer theorem for that pair.
- `exact-ns-transfer-coherence-phase-observable.md` records the later phase-locking continuation that keeps the same interface philosophy but replaces localized physical-space bookkeeping by a global spectral transfer ledger.
