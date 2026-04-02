# Packet Ledger Functional Prototype Summary

## Goal

Push the helical sign-defect route one step beyond the singleton clue by
evaluating exact-ledger packet functionals on a genuinely non-singleton packet
family.

The packet-level exact object reused here is the one from:

- `codex-atlas/.../exploration-001/REPORT.md`

The functionals are:

- `Drive_target`
- `Leak`
- `SD_part`
- `SD_target`

implemented in:

- `packet_ledger_functionals.py`

## Baseline

On the old singleton-pair packet family with the best prior sign pattern

```text
(a1,a2,a3,a4,a5) = (+,+,-,+,+)
```

the prototype gives

```text
Drive_target ≈ 0.5303
Leak ≈ 34.58
SD_part ≈ 0.2560
SD_target ≈ 0.6667
```

The old qualitative singleton clue survives in this packet-language baseline:
the lowest-leak sign patterns still occur at `minority_count = 1`.

## Two Non-Singleton Lifts Tested

### 1. Shell-sign nearest-anchor family

This lift adds four one-step external representative mode pairs from the old
singleton audit:

```text
(2,1,0), (1,2,0), (0,2,0), (2,3,0)
```

and assigns each to the Tao-role packet of the nearest same-shell same-sign core
anchor.

Result:

```text
Leak ≈ 139.40
SD_part ≈ 0.1104
SD_target ≈ 0.6667
```

Interpretation:

- This is too crude.
- It makes the packet family globally more one-sign, but leakage blows up badly.
- So the naive geometry-first packet lift is not a promising object.

### 2. Source-incidence family

This lift uses the same four one-step external representative mode pairs, but
assigns each added pair to the Tao-role packet with the largest exact source
incidence weight among the core-support triads that generate it.

This is still heuristic, but it is more exact-ledger-native than nearest-anchor
geometry.

Result for the same core sign pattern:

```text
Drive_target ≈ 7.1898
Leak ≈ 9.3564
SD_part ≈ 0.4203
SD_target ≈ 0.8619
```

Interpretation:

- The packet lift now activates several desired packet edges:
  - `A,A->B`
  - `A,B->A`
  - `A,C->D`
  - `B,C->C`
  - `C,D->A`
- Leakage drops sharply compared with the singleton baseline.
- Desired-edge heterochirality remains high, not low.
- Global sign coherence does **not** improve in lockstep with lower leakage on
  this better packet family; `SD_part` is actually higher than the singleton
  baseline.

That is the first real packet-stage refinement of the singleton clue:

```text
packetization can reduce leakage without eliminating strong heterochiral
dependence of the load-bearing desired edges.
```

## 32-Sign Scan Of The Source-Incidence Family

Using `scan_incidence_families.py`:

- the best leak still occurs at `minority_count = 1`
- the top family has

```text
Leak ≈ 9.3564
SD_part ≈ 0.4203
SD_target ≈ 0.8619
```

- `minority_count = 2` patterns are the next best
- the fully one-sign patterns are **not** optimal on leak in this packet lift

So the old singleton slogan

```text
lower leakage pushes toward more global sign coherence
```

survives only weakly after a non-singleton packet lift.

What survives more robustly is:

```text
even when a non-singleton packet lift reduces leakage substantially and
activates more desired packet edges, the desired-edge heterochirality defect
stays large.
```

## Current Read

This route is still alive, but the emphasis shifts:

- `SD_target` now looks more robust than `SD_part`
- the better packet family reduces leak a lot while keeping `SD_target` high
- that suggests the sharper next bottleneck candidate may be:
  - low-leakage packet families can exist at least heuristically,
  - but the load-bearing desired Tao-like drive still seems to need a large
    heterochiral component

## Limits

- This is still not a canonical packet object.
- The source-incidence lift is deterministic but heuristic.
- The added-mode amplitudes remain implicit unit weights; this is still a
  structural exact-ledger computation, not a true exact-NS solution segment.
- No theorem has been proved.

## Best Next Step

The strongest next continuation now looks like:

1. keep the source-incidence packet lift as the current best exploratory object,
2. treat the nearest-anchor lift as a negative control,
3. focus the next theorem-shaped question more on `SD_target` than on
   `SD_part`,
4. ask whether any low-leakage faithful packet family can drive `SD_target`
   genuinely small.
