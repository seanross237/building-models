---
topic: The sharp singleton-support exact-NS Tao-circuit object is structurally impossible
confidence: computed
date: 2026-04-01
source: "exact-ns-no-near-closed-tao-circuit strategy-001 exploration-002 report"
---

## Finding

The cleanest exact-mode version of a Tao-like near-closed circuit already fails before any coefficient-ratio or leakage estimate is attempted. The obstruction is structural wavevector non-embeddability.

## Exact Obstruction

In the preferred singleton-support helical model, the desired channels include

```text
a1^2 -> a2,
a1^2 -> a3,
a2 a3 -> a3.
```

Exact triad closure forces

```text
k2 = ± 2 k1,
k3 = ± 2 k1,
```

so roles 2 and 3 must occupy the same conjugate wavevector pair. Once that happens, the amplifier channel

```text
a2 a3 -> a3
```

cannot satisfy exact triad closure for any conjugate-sign arrangement. Thus the target monomial pattern is not embeddable on singleton exact supports.

## Consequence

This is stronger than the earlier firewall slogan "spectator leakage may be too large." The sharpest exact object dies at the level of static support geometry:

- no coefficient hierarchy needs to be computed,
- no leakage lower bound is needed,
- no helicity choice rescues the object.

So the exact singleton Tao-circuit theorem program is closed negatively.

## Relationship To Other Entries

- `exact-helical-near-closed-tao-circuit-definition.md` records the Phase 0 definition gate that produced this preferred singleton object.
- `exact-ns-triadic-coefficient-rigidity.md` now becomes a conditional observation: coefficient rigidity matters only for refined packet models, because the singleton object is already impossible.
- `packetized-tao-circuit-noncanonical.md` explains why the backup packet version does not rescue the mission as one theorem-facing object.
