# Fixed Wavevector Sheet Search Summary

## Goal

Continue the exact-screen branch from the April 2 bridge artifact without
changing the explicit wavevector family.

The narrow question was:

```text
If we keep the old explicit five-wavevector singleton support fixed, can some
other helicity sheet or primary conjugate-representative convention realize the
full Step-7 one-bridge desired core?
```

This is a cleaner continuation than introducing a new support immediately,
because Step 9 says the branch is blocked by missing same-currency explicit
realization data.

## Artifact

The executable search is:

- `search_fixed_wavevector_sheets.py`

It fixes the explicit singleton support already imported in the bridge artifact:

```text
A_n = (1,0,0)
B_n = (2,0,0)
C_n = (0,1,0)
D_n = (1,1,0)
E_n = (2,2,0)
```

and then scans:

- all `32` helicity sign sheets on that support;
- all `32` primary conjugate-representative conventions for the five roles.

So the total search size is:

```text
32 * 32 = 1024
```

configurations, all on the same exact coefficient currency.

## Main Result

The fixed explicit singleton family cannot realize the Step-7 desired core.

The sharp outcomes are:

- full exact coverage of the six desired Step-7 role-pairs never occurs;
- the best any configuration achieves is `1 / 6` desired pairs at once;
- only two desired pairs ever appear anywhere in the whole search:
  - `C_n + D_n -> A_n`
  - `A_n + C_n -> D_n`
- the other four desired pairs never appear on this fixed support under any
  helicity sheet or primary representative convention:
  - `A_n + A_n -> B_n`
  - `A_n + A_n -> C_n`
  - `B_n + C_n -> C_n`
  - `D_n + D_n -> E_n`

The best configuration found is:

```text
sigma:
  A_n = +1, B_n = +1, C_n = +1, D_n = +1, E_n = +1

representatives:
  A_n -> a1
  B_n -> a2
  C_n -> bar_a3
  D_n -> a4
  E_n -> a5
```

and even there:

- exact desired coverage is only `1 / 6`;
- internal spectator load is about `0.4268`;
- external leak is about `15.5861`;
- total leak in the script's absolute-value ledger is about `16.0128`.

## Structural Reason The Search Fails

The failed pairs are not all failing for the same reason.

On this fixed support:

- `A_n + A_n -> B_n` and `D_n + D_n -> E_n` have the right wavevector sums,
  but they are same-source helical self-interactions, so the Waleffe/Leray
  coefficient vanishes identically there;
- `A_n + A_n -> C_n` is impossible already at the wavevector level, because
  two copies of the chosen `A_n` representative can only add to the chosen
  `B_n` representative on this support, not to `C_n`;
- `B_n + C_n -> C_n` is also impossible already at the wavevector level,
  because adding the nonzero `B_n` representative to the chosen `C_n`
  representative can never return the same `C_n` target.

So the fixed-wavevector search is not merely saying

```text
we did not find the right sign sheet
```

It is saying that four of the six desired Step-7 pairs are blocked on this
family by rigid support geometry or same-mode helical degeneracy.

## Interpretation

This is a stronger negative than the earlier one-candidate bridge.

The earlier bridge showed:

```text
one explicit candidate does not rescue the branch
```

This search shows the sharper statement:

```text
the entire fixed explicit singleton wavevector family already on disk is too
misaligned with the Step-7 one-bridge desired core to rescue the branch by
helicity-sheet or representative-sheet adjustment alone
```

So the local Step-9 source-basis gap is now narrower and more specific.
The branch is not blocked only because "no explicit realization was written
down." It is also blocked because the nearest explicit singleton family already
available in the repo is structurally incapable of carrying most of the
desired one-bridge core.

## Best Honest Next Step

The next continuation from here is:

1. stop treating the old singleton support as a likely rescue source for the
   Step-7 carried branch;
2. if the exact-screen route continues, move to an explicit packet-level lift
   or a newly frozen wavevector family designed in the same currency as the
   Step-7 roles from the start;
3. otherwise treat this as stronger evidence that the constructive `F_SS(1/12)`
   line is blocked by a genuine realization mismatch, not just a bookkeeping
   omission.
