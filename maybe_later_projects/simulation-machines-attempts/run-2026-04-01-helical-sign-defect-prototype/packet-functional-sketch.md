# Packet Functional Sketch

## Why This Sketch Exists

The singleton sign-defect prototype suggests that one scalar `SignDefect` is
probably too coarse.

On the killed singleton support:

- the lowest-leakage nontrivial sign patterns are the most globally
  near-homochiral ones;
- but the only surviving desired activation triad is still obligatorily
  heterochiral.

So the route appears to need **two** sign-sensitive quantities, not one:

1. a global packet-level minority-helicity participation defect;
2. a target-edge heterochirality defect on the load-bearing Tao channels.

## Start From The Existing Packet Object

Use the packet-level exact object already defined in

- `codex-atlas/.../exploration-001/REPORT.md`

namely

```text
NCTC = (S, {P_A,P_B,P_C,P_D,P_A_next}, G_target, Θ, u|I).
```

All definitions below stay inside the same exact helical-triad ledger.

## Exact Triad Weights

For an exact helical triad contribution

```text
τ = ((p,s_p),(q,s_q) -> (k,s_k))
```

with coefficient `C_τ`, define its instantaneous magnitude

```text
W_τ(t) := |C_τ u_{s_p}(p,t) u_{s_q}(q,t)|.
```

This is the same absolute-magnitude bookkeeping style already used in the exact
`Drive` and `Leak` functionals.

## Functional 1: Packet Minority-Helicity Participation

Because the exact packet support is sign-closed, this functional should be
computed on a fixed representative of each conjugate-pair family rather than on
both members of every pair. Otherwise the global sign balance trivializes.

For each representative active mode family `m` in that conjugate-pair quotient,
define its participation weight

```text
Part_m(t) := Σ_{τ touches m} W_τ(t),
```

where the sum ranges over all target and spectator ledger terms touching `m`.

Then define the packet-level minority-helicity participation defect on `I` by

```text
SD_part(I)
  := min_{η in {+,-}}
       ∫_I Σ_{m with sign(m) != η} Part_m(t) dt
       ------------------------------------------------
       ∫_I Σ_m Part_m(t) dt.
```

Interpretation:

- `SD_part(I)` is small when the active packet ledger is globally dominated by
  one helical sign;
- this is the packet lift of the prototype `SignDefect_mode`.

## Functional 2: Desired-Edge Heterochirality Defect

Let `T_target` be the exact target-triad set realizing the Tao-role hypergraph
`G_target`.

Define

```text
SD_target(I)
  := ∫_I Σ_{τ in T_target} 1_{not all signs in τ equal} W_τ(t) dt
      -------------------------------------------------------------
      ∫_I Σ_{τ in T_target} W_τ(t) dt.
```

Interpretation:

- `SD_target(I)` measures how much the desired Tao-like drive depends on
  heterochiral triads;
- this is the packet lift of the singleton observation that the surviving
  activation edge is entirely heterochiral.

## Recommended Composite Cost

The prototype suggests not collapsing these immediately to one number.

The first packet mission should track the pair

```text
(Leak(I), SD_part(I), SD_target(I))
```

or at most a two-parameter cost such as

```text
Cost_{λ,μ}(I) := Leak(I) + λ SD_part(I) + μ SD_target(I).
```

The reason to keep both sign terms visible is structural:

- `SD_part` sees whether low leakage is pushing the whole packet family toward
  one-sign dominance;
- `SD_target` sees whether the load-bearing Tao edges still require mixed-sign
  triads even after that global push.

## Sharper Theorem Shape Suggested By The Prototype

The singleton experiment suggests the packet theorem may want to look more like

```text
low Leak forces low SD_part,
but Tao-like desired drive forces positive SD_target.
```

That is a more informative shape than a bare scalar lower bound.

Possible theorem targets:

1. `Leak(I) <= ε0` implies `SD_part(I) <= δ(ε0)` for all admissible packet
   families.
2. Every Tao-like admissible packet family has `SD_target(I) >= c1 > 0` on the
   activation window.
3. The three quantities cannot simultaneously satisfy

```text
Leak(I) small,
SD_part(I) very small,
SD_target(I) very small.
```

4. Failing a positive obstruction, minimizing sequences for
   `Cost_{λ,μ}` are compact up to the exact symmetries.

## Why This Matters

This is the first concrete refinement suggested by the follow-up computation:

- the route should probably not optimize a single vague `SignDefect`;
- it should distinguish
  - global sign coherence on the active packet family, and
  - heterochiral dependence of the desired Tao-like edges.

That makes the next packet-stage mission sharper and less likely to collapse
back into ambiguous modeling.
