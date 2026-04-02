---
topic: The preferred exact-NS transfer-coherence observable fails the minimal-support audit
confidence: computed
date: 2026-04-01
source: "exact-ns-phase-locking-firewall strategy-001 exploration-002 report"
---

## Finding

The preferred phase-locking burden

```text
C_ell = (sum_{tau in T_ell} T_{tau,ell}) / (sum_{tau in T_ell} |T_{tau,ell}|)
```

already fails on the smallest honest exact supports.

With one active exact transfer term, `C_ell` is forced to `+/-1`, so it is tautological rather than a genuine coherence burden. On the first nontrivial exact cluster with two distinct ordered inputs feeding the same receiver mode, exact phase tuning keeps the receiver gain positive while driving `C_ell` arbitrarily close to `0`.

## Exact Identity

For each ordered helical triad contribution `tau` into receiver band `ell`,

```text
T_{tau,ell} = W_{tau,ell} cos Theta_{tau,ell}.
```

So

```text
C_ell
  = (sum_{tau in T_ell} T_{tau,ell})
    / (sum_{tau in T_ell} |T_{tau,ell}|).
```

If `T_ell` contains exactly one nonzero term, then

```text
C_ell = T_{tau,ell} / |T_{tau,ell}| = +/- 1.
```

Thus the smallest one-triad setting with a genuine phase variable cannot test whether low coherence is compatible with positive transfer. The observable collapses to a sign bit.

## First Nontrivial Exact Cluster

The first honest cancellation test is the smallest sign-closed exact cluster with two distinct ordered transfer inputs feeding the same receiver mode. One explicit exact-helical realization is

```text
target k = (2,1,0)
pair 1   = (1,0,0) + (1,1,0)
pair 2   = (2,0,0) + (0,1,0)
signs    = (sigma_k, sigma_p1, sigma_q1, sigma_p2, sigma_q2)
         = (1, -1, 1, 1, -1).
```

Its exact helical coefficients satisfy

```text
|c1| = 0.178839197367
|c2| = 0.383750455201.
```

Choose phases so that

```text
Theta_1 = 0,
Theta_2 = pi,
```

which yields

```text
T_1 = +W_1,
T_2 = -W_2.
```

By tuning one source amplitude, the report produced families with positive residual net gain

```text
net = T_1 + T_2 > 0
```

but

```text
eps = 1e-2: C_ell = 2.88e-2
eps = 1e-3: C_ell = 2.80e-3
eps = 1e-4: C_ell = 2.80e-4.
```

So the numerator sees only the small residual signed gain, while the denominator keeps the full absolute transfer mass of both channels.

## Consequence

This is a model-level failure, not a theorem-search shortfall. The same burden variable dies in the only two minimal ways available:

- on one exact transfer term it is too trivial,
- on the first multi-input exact cluster it is already too weak.

No larger delayed-threshold or larger-support campaign is justified unless a new structural invariant replaces this cancellation-ratio burden.

## Relationship To Other Entries

- `exact-ns-transfer-coherence-phase-observable.md` records the Phase 0 gate that selected `C_ell / D_ell` as the preferred intrinsic phase observable before this minimal-support audit killed it.
- `exact-singleton-tao-circuit-nonembeddability.md` is a sibling minimal-support negative on a different exact-NS firewall line; there the object dies by triad closure, whereas here the burden variable dies by tautology plus first-cluster cancellation.
