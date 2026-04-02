# Global Adversarial Packet Search Summary

## Goal

Broaden the earlier adversarial packet-family search from one favored core sign
pattern to all `32` sign assignments on the exact five-role core support.

The question was:

```text
Was the earlier low-Leak / high-SD_target tradeoff a local artifact of one sign
choice, or does it survive a broader search?
```

The search object is implemented in:

- `search_adversarial_packet_families_all_signs.py`

and reuses the same restricted family class as the earlier run:

- top `6` one-step external representative mode pairs from each core support
- subset sizes `1` through `4`
- each added pair assigned to one of its top `3` incidence-weight packet labels

## Search Size

Using `10` workers, the global scan tested

```text
31,978
```

expanded packet families across all `32` core sign patterns.

## Main Results

### 1. The first stronger bottleneck slogan was too strong globally

The earlier single-pattern search suggested that low `Leak` might force very
large `SD_target` throughout the searched class.

The all-sign scan weakens that claim.

The globally lowest-leak families found were actually based on fully
homochiral cores:

```text
Leak ≈ 7.1878
SD_target ≈ 0.7624
```

So low leakage in this searched class is not confined to the old
`minority_count = 1` sign patterns.

### 2. Minority-count-2 cores can lower `SD_target` substantially

The best `SD_target` found under practical leak thresholds came from
`minority_count = 2` families.

Best values found globally:

```text
Leak <=  8:  SD_target ≈ 0.6994
Leak <= 10:  SD_target ≈ 0.6134
Leak <= 12:  SD_target ≈ 0.5709
Leak <= 15:  SD_target ≈ 0.5089
Leak <= 30:  SD_target ≈ 0.4162
```

So the searched class does admit materially lower desired-edge heterochirality
than the first single-pattern run suggested.

### 3. The route still keeps a real signal in the truly low-leak regime

The weakening is real, but it does not flatten the obstruction entirely.

Inside the searched family class:

- very low `Leak` still does not drive `SD_target` anywhere near `0`
- the global Pareto front still shows a real tradeoff
- the low-leak corner remains meaningfully heterochiral

The honest empirical remnant is therefore threshold-sensitive:

```text
for genuinely low leakage in this restricted class,
SD_target stays bounded away from 0,
but the bound is much weaker than the earlier single-pattern search implied
```

## Representative Extremizers

### Best leak found globally

Core sign pattern:

```text
(a1,a2,a3,a4,a5) = (+,+,+,+,+)
```

Added pairs and packet assignments:

```text
(-2,-1,0,-), (-1,-2,0,-), (-1,1,0,-), (-1,1,0,+)
-> (C, A, A, A)
```

Metrics:

```text
Drive_target ≈ 9.0094
Leak ≈ 7.1878
SD_target ≈ 0.7624
```

### Best `SD_target` found under `Leak <= 15`

Core sign pattern:

```text
(a1,a2,a3,a4,a5) = (+,-,-,+,-)
```

Added pairs and packet assignments:

```text
(-3,-2,0,+), (-1,-2,0,-)
-> (A, A)
```

Metrics:

```text
Drive_target ≈ 2.9321
Leak ≈ 14.8310
SD_target ≈ 0.5089
```

The desired drive in that family is concentrated on:

- `A,A->B`
- `A,B->A`
- `A,C->D`
- `C,D->A`

## Interpretation

This is still not a theorem object.

What the scan supports:

- the packet-sign route still has a real mechanistic signal
- `SD_target` remains more decision-relevant than `SD_part`
- the tradeoff is real but weaker than the first single-pattern search implied

What the scan does **not** support:

- a broad claim that low `Leak` forces very large `SD_target`
- a general theorem candidate on the current non-canonical packet object
- confidence that the packet-sign route should dominate the repo's broader
  prize-facing search

## Updated Read

The best honest continuation after this scan is narrower than before:

1. treat the packet-sign search as a mechanism probe on a restricted family
   class,
2. if one wants a packet-level empirical statement at all, phrase it only as a
   stricter-threshold envelope,
3. do not confuse that with a prize-facing theorem object,
4. keep the cleaner theorem-facing effort on the two frozen exact packet
   screens or on a more intrinsic non-packet object class.
