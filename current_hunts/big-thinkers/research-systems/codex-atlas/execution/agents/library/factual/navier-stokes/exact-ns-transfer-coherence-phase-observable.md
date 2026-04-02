---
topic: Exact helical transfer-coherence ratio is the preferred intrinsic phase observable for delayed transfer
confidence: computed
date: 2026-04-01
source: "exact-ns-phase-locking-firewall strategy-001 exploration-001 report; exact-ns-phase-locking-firewall strategy-001 exploration-002 report"
---

## Finding

The phase-locking continuation does **not** live on the old packet-sign family. In the exact helical Fourier law, each ordered triad contribution to one scale-transfer ledger already carries an intrinsic phase. The preferred Phase 0 firewall object is therefore the exact signed-transfer versus absolute-transfer ratio on a fixed smooth scale interface, not a packet statistic and not a raw phase-concentration average.

This gate passes, but only narrowly: the later minimal-support audit kills the frozen pair `(C_ell, E_ell^transfer)`. On one exact active transfer term, `C_ell` is identically `+/-1`; on the first exact two-input cluster, `C_ell` can be driven arbitrarily close to `0` while receiver gain stays positive. So this entry records the right Phase 0 object, not a surviving theorem line.

## Exact Phase Law

For each ordered helical triad term

```text
tau = (k, p, q, s_k, s_p, s_q),
```

the exact transfer contribution has the form

```text
T_tau(t)
  = Re( overline{u_{s_k}(k,t)} C_tau u_{s_p}(p,t) u_{s_q}(q,t) )
  = W_tau(t) cos Theta_tau(t),
```

with

```text
W_tau(t)
  = |C_tau| |u_{s_k}(k,t)| |u_{s_p}(p,t)| |u_{s_q}(q,t)|,

Theta_tau
  = arg u_{s_p}(p) + arg u_{s_q}(q) - arg u_{s_k}(k) + arg C_tau
  mod 2pi.
```

So the sign of the exact triad contribution is carried by the intrinsic phase variable `Theta_tau`, while the amplitudes only weight the population.

## Preferred Observable

Fix a smooth kernel `G`, one interface scale `ell`, and one scale ratio `rho > 1`. Let `T_{tau,ell}` be the exact signed contribution of triad term `tau` to the forward-transfer ledger across `ell -> ell/rho`, and let `T_ell` be the sign-closed population of all ordered helical triad terms in that ledger.

Define

```text
C_ell(t)
  = (sum_{tau in T_ell} T_{tau,ell}(t))
    / (sum_{tau in T_ell} |T_{tau,ell}(t)|),

D_ell(t) = 1 - C_ell(t).
```

Equivalently,

```text
C_ell(t)
  = (sum_tau W_{tau,ell}(t) cos Theta_{tau,ell}(t))
    / (sum_tau W_{tau,ell}(t) |cos Theta_{tau,ell}(t)|).
```

Interpretation:

- `C_ell ~ 1` means the exact triad population is phase-aligned in the constructive forward-transfer direction.
- `C_ell ~ 0` means strong cancellation inside that same exact transfer ledger.
- `D_ell` is the corresponding transfer-coherence defect.

## Why This Survives

The observable keeps the exact helical transfer ledger rather than replacing it with packet roles or witness-triad bookkeeping.

Its invariance ledger is clean:

- translation/gauge factors cancel on `k = p + q`, so `Theta_tau` is intrinsic modulo `2pi`,
- conjugate-pair bookkeeping does not matter once the population is taken sign-closed and the observable is written in terms of the real transfer contributions `T_{tau,ell}`,
- packet refinement is irrelevant because no packet decomposition appears,
- desired-channel relabeling is irrelevant because the population is "all exact triad terms in the fixed interface ledger," not a chosen witness subset.

## Backup Observable

The admissible backup on the same triad population is the raw phase-concentration statistic

```text
A_ell(t)
  = |sum_{tau in T_ell} W_{tau,ell}(t) exp(i Theta_{tau,ell}(t))|
    / sum_{tau in T_ell} W_{tau,ell}(t).
```

It is weaker as a firewall object because it does not distinguish concentration around forward-transfer-maximizing phases from concentration around phases that still cancel the signed ledger.

## Preferred Companion Event

The delayed-transfer companion event is the global spectral analogue of the older localized event `E_flux`:

```text
E_ell^transfer:
an earlier quiet interval for the exact forward-transfer ledger across ell,
followed by a short-window positive transfer burst and abrupt gain of the
exact receiver-band energy between ell and ell/rho.
```

The physical-space event scaffold remains useful, but the spatial cutoff is no longer preferred here because it breaks the clean exact helical triad population needed for the phase ledger.

## Relationship To Other Entries

- `exact-ns-transfer-coherence-minimal-support-failure.md` records the follow-up negative: the preferred `C_ell / D_ell` object is definable but too tautological on one triad and too weak on the first two-input cluster.
- `exact-ns-physical-space-delayed-transfer-event.md` records the earlier localized delayed-transfer scaffold that this entry reuses only as an event-shape anchor.
- `packetized-tao-circuit-noncanonical.md` and `exact-ns-helical-sign-canonicity-failure.md` explain why the phase-locking line had to leave packet bookkeeping behind.
- `exact-ns-delayed-transfer-precursor-pair.md` and `exact-ns-delayed-transfer-precursor-no-backward-memory.md` record the physical-space precursor line whose scale-interface logic survives here, even though the preferred phase-coupled event is now global spectral rather than localized.
