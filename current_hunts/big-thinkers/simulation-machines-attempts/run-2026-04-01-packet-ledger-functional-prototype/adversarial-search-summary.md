# Adversarial Packet Search Summary

## Goal

Stress-test the current best exploratory packet route by searching for packet
families that make both

```text
Leak small
SD_target small
```

inside the same exact-ledger framework.

This search starts from the best current core sign pattern

```text
(a1,a2,a3,a4,a5) = (+,+,-,+,+)
```

and varies:

- which of the strongest one-step external representative mode pairs are added,
- and which Tao-role packet each added pair is assigned to.

The search object is implemented in:

- `search_adversarial_packet_families.py`

## Search Space

- top `6` external representative mode pairs from the core support
- subset sizes `1` through `4`
- each added pair assigned to one of its top `3` incidence-weight packet labels

Total tested families:

```text
767
```

## Main Results

### 1. No low-leak / low-SD_target family appeared in the searched region

The best family by leak had

```text
Leak ≈ 7.5893
SD_target ≈ 0.8747
```

So the search found lower leakage than the earlier source-incidence baseline,
but not lower desired-edge heterochirality.

### 2. The best `SD_target` under practical leak thresholds stayed large

Best `SD_target` found under selected leak thresholds:

```text
Leak <= 10:  SD_target ≈ 0.8362
Leak <= 12:  SD_target ≈ 0.7530
Leak <= 15:  SD_target ≈ 0.7530
Leak <= 20:  SD_target ≈ 0.7425
```

So within the tested family class, lowering `SD_target` materially required
accepting noticeably larger leakage.

### 3. The first visible Pareto tradeoff is encouraging for the bottleneck route

In the searched families, the Pareto front in `(Leak, SD_target)` behaves like:

- very low `Leak` comes with very high `SD_target`
- modestly lower `SD_target` appears only once `Leak` is allowed to rise

This is not a theorem, but it is exactly the shape one would hope to see if a
sign-sensitive bottleneck is real.

## Interpretation

This is the strongest evidence so far on this route, but it is still
exploratory.

What it supports:

- the packet-stage story is no longer just the singleton clue
- `SD_target` looks more robust than `SD_part`
- the most promising next theorem candidate is about a lower bound on
  desired-edge heterochirality under low leakage, not about global sign
  coherence alone

What it does **not** support yet:

- a canonical packet theorem object
- a proof-quality lower bound
- any direct progress on regularity itself

## Best Next Step

The sharpest continuation now looks like:

1. keep the source-incidence family as the best exploratory object,
2. use the adversarial search result as evidence that `SD_target` is the right
   bottleneck quantity,
3. try to prove or tightly justify a statement of the form

```text
Leak <= eps  =>  SD_target >= c(eps)
```

for a restricted but faithful packet family class.
