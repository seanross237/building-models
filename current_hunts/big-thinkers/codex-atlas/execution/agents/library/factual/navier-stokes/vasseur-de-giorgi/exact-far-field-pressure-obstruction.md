---
topic: Exact far-field pressure obstruction is a decomposition mismatch, not Vasseur's literal bottleneck
confidence: verified
date: 2026-03-31
source: "far-field-pressure-harmonic-loophole exploration-001; Vasseur 2007 Section 4 Proposition 3"
---

## Finding

The surviving "far-field harmonic loophole" is **not** the literal bottleneck term in Vasseur's De Giorgi recurrence.

- In Vasseur's notation, the harmonic/nonlocal term is `P_{k1}` and it is already favorable.
- The load-bearing obstruction is the **local non-divergence pressure term** `P_{k21}`.
- Therefore the only coherent surviving loophole is an **alternative near/far decomposition** in which a harmonic far-field piece absorbs part of what Vasseur isolates as the bad local interaction.

## Exact Pressure Split

On the interior ball, Vasseur decomposes

```text
P = P_{k1} + P_{k2},
```

with `P_{k1}` harmonic on the local ball and

```text
-ΔP_{k2} = Σ_{i,j} ∂_i∂_j (φ_k u_i u_j).
```

He then writes

```text
P_{k2} = P_{k21} + P_{k22} + P_{k23},
```

where

```text
-ΔP_{k21}
= Σ_{i,j} ∂_i∂_j [ φ_k u_j (1 - v_k/|u|) u_i (1 - v_k/|u|) ].
```

This is the term whose non-divergence pairing fixes the recurrence exponent.

## Exact Recurrence Slot

The dangerous contribution is

```text
I_k
= ∫∫ |P_{k21}| |div(u v_k/|u|)| dx dt
≤ ||P_{k21}||_{L^q}
   ||d_k||_{L^2}
   ||1_{v_k>0}||_{L^{2q/(q-2)}}.
```

The three factors scale as

```text
||P_{k21}||_{L^q} ≤ C_q,
||d_k||_{L^2} ≤ U_{k-1}^{1/2},
||1_{v_k>0}||_{L^{2q/(q-2)}} ≤ C^k U_{k-1}^{5(q-2)/(6q)}.
```

Hence

```text
I_k ≤ C_q C^k U_{k-1}^{4/3 - 5/(3q)},
```

so the load-bearing arithmetic is

```text
U_{k-1}^0 × U_{k-1}^{1/2} × U_{k-1}^{5/6} = U_{k-1}^{4/3}.
```

## Why the Pressure Factor Stays Fixed

The source of `P_{k21}` contains the bounded factors `u(1-v_k/|u|)`, so Calderon-Zygmund yields only

```text
||P_{k21}||_{L^q} ≤ C_q,
```

with no positive power of `U_{k-1}`. This is the exact sense in which the pressure coefficient remains at energy scale rather than De Giorgi scale.

By contrast, the harmonic/nonlocal term `P_{k1}` already satisfies a favorable Step 4 estimate with exponent

```text
β_nonlocal = (5/3)(1 - 1/p) > 3/2
```

for the relevant regime `p > 10`.

## Consequence for the "Far-Field Harmonic Loophole"

The loophole survives only as a **decomposition mismatch** question:

1. Can one replace Vasseur's split by a near/far split `p = p_near + p_far` with `Δp_far = 0` on the working cylinder?
2. Can that alternative split absorb part of the dangerous contribution that Vasseur packages into local `P_{k21}`?
3. Does harmonic control of `p_far` change the pairing from a fixed energy-scale coefficient to a genuinely `U_k`-dependent one?

If the answer to any step is no, the loophole collapses.

## Tao-Filter Form

For transfer to averaged Navier-Stokes or Tao-style filtering, the only live test is:

- the averaged pressure must admit the same near/far decomposition with harmonic `p_far` on the local cylinder,
- the harmonic oscillation/Harnack gain must survive averaging,
- the gain must act on the **bad pairing itself**, not merely on the already-harmless harmonic term `P_{k1}`.

## Relationship to Prior Entries

- Corrects the shorthand in `h1-pressure-dead-end.md`: "far-field term `P_{k21}`" is not literal Vasseur notation.
- Sharpens `beta-current-value-four-thirds.md`: the surviving pressure-side loophole is a decomposition mismatch, not improvement of Vasseur's harmonic term.
