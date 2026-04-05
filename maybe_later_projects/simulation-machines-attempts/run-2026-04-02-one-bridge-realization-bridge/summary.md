# One-Bridge Realization Bridge Summary

## Goal

Continue the exact-screen branch at the point where the local Step-9 memo
stopped:

```text
missing same-currency explicit realization protocol
```

The narrow question here was:

```text
Does the repo already contain a nearby explicit wavevector/helicity realization
that can be bridged into the Step-7 one-bridge role ledger?
```

## Artifact

The executable bridge is:

- `bridge_one_bridge_realization.py`

It imports the older exact-helical singleton audit from:

- `codex-atlas/.../helical_support_audit.py`

and maps its five roles

```text
a1, a2, a3, a4, a5
```

to the Step-7 one-bridge roles

```text
A_n, B_n, C_n, D_n, E_n.
```

## Candidate Explicit Realization Recovered

The bridged candidate is:

```text
A_n = (1,0,0),   sigma =  +1
B_n = (2,0,0),   sigma =  +1
C_n = (0,1,0),   sigma =  -1
D_n = (1,1,0),   sigma =  +1
E_n = (2,2,0),   sigma =  +1
```

with the exact Waleffe/Leray helical coefficient formula already implemented in
that older audit.

So this bridge **does** partially close the Step-9 source-basis gap:

- explicit wavevector family: yes
- fixed helicity assignment: yes
- exact coefficient formula: yes

## Main Result

The bridge does **not** rescue the carried one-bridge stress-test branch.

On this candidate:

- `A_n + C_n -> D_n` survives as an exact desired internal witness;
- `C_n + D_n -> A_n` survives only after a conjugate adjustment, as
  `bar_C_n + D_n -> A_n`;
- `A_n + A_n -> B_n` has no nonzero internal witness;
- `A_n + A_n -> C_n` has no nonzero internal witness;
- `B_n + C_n -> C_n` has no exact internal witness;
- `D_n + D_n -> E_n` has no nonzero internal witness;
- external emissions appear immediately and abundantly.

The top external emissions are already of size about

```text
0.4349, 0.4268, 0.3838, ...
```

so this candidate is not finitely isolated even before any later recursive
closure audit.

## Interpretation

This is a useful bridge, but only a partial one.

What it establishes:

- the repo is not completely empty on the realization side;
- an explicit five-role wavevector/helicity candidate already exists in a
  sibling exact-helical audit;
- the source-basis gap from Step 9 is therefore narrower than
  “no explicit realization exists anywhere.”

What it does **not** establish:

- a same-currency promoted realization for the carried `F_SS(1/12)` witness;
- an explicit realization of the full Step-7 desired core;
- a finite-closure convention;
- or any reversal of the Step-8 / Step-9 stop verdicts.

The best honest reading is:

```text
the old singleton exact-helical audit supplies a concrete realization candidate,
but it realizes only part of the Step-7 core and still leaks immediately, so it
is evidence about the shape of the missing realization protocol, not the
protocol itself
```

## Best Next Step

The next sharp continuation from here is:

1. treat this explicit singleton realization as a source-basis bridge only,
2. ask whether any packet-level lift of it can realize the full Step-7 core on
   the same exact coefficient currency,
3. or else conclude more strongly that the exact-screen branch is blocked not
   just by missing provenance, but by a deeper mismatch between the carried
   screening witness and currently available explicit helical realizations.
