# `F_SS(1/12)` Witness Freeze Summary

## Goal

Pivot from the weaker packet-sign mechanism probe to the cleaner exact-screen
branch already frozen in the local Step-6 handoff.

The narrow target here was:

```text
freeze one reproducible witness/authority sheet for
  F_SS(1/12),
  G_tmpl(P_n; I),
  G_leak(P_n; I)
```

without reopening packet semantics, witness choice, threshold tuning, or
currency drift.

## Artifact

The executable artifact is:

- `freeze_fss_authority_sheet.py`

It reads the existing local numeric sources:

- Step-4 pro-circuit dossier checker
- Step-5 repair-sheet lock

and prints one same-currency witness/authority snapshot.

## Verified Outputs

For the frozen witness

```text
F_SS(mu = 1/12)
```

the script confirms:

```text
int_I D_on  = 1
Delta_tmpl  = 1/6
Delta_spec  = 1/6
L_tot       = 1/4
L_mirror    = 1/12
L_companion = 1/12
L_feedback  = 1/24
L_cross     = 1/24
```

against the controlling repaired Step-7 authority sheet:

```text
Delta_tmpl  <= 1/4
Delta_spec  <= 49/256
L_tot       <= 1/4
L_mirror    <= 1/12
L_companion <= 1/12
L_feedback  <= 1/16
L_cross     <= 1/24
```

The one variance note is historical only:

- some earlier Step-4 / Step-5 helper artifacts still carry `L_cross = 1/12`,
- but the controlling later Step-5 / Step-6 / Step-7 branch sheet freezes
  `L_cross <= 1/24`.

## Main Findings

### 1. `F_SS(1/12)` is an unambiguous friendly witness on the repaired sheet

`F_SS(1/12)` passes both repaired hard gates with no rescue:

- it passes repaired `G_tmpl`
- it passes repaired `G_leak`

and it saturates the obstruction-facing entries

- `L_tot`
- `L_mirror`
- `L_companion`
- `L_cross`

on the repaired authority sheet.

### 2. `F_SL(1/16)` still matters and cannot be discarded

The exact-screen branch is not a one-witness story.

The frozen boundary-friendly witness

```text
F_SL(rho = 1/16)
```

still supplies the repaired maxima for:

- `Delta_tmpl = 1/4`
- `Delta_spec = 49/256`
- `L_feedback = 1/16`

So the clean authority sheet is:

- one carried constructive witness `F_SS(1/12)`
- one carried boundary-friendly witness `F_SL(1/16)`
- one repaired same-currency gate pair `G_tmpl`, `G_leak`

### 3. The branch is operationally cleaner than the packet-sign branch

Unlike the packet-sign route, this branch already has:

- one frozen packet sheet
- one fixed window `I = [0, 1]`
- one frozen `D_on` / `D_off` split
- one repaired threshold sheet
- one explicit historical variance note instead of live threshold choice

That does **not** make it a prize proof route.
But it does make it a cleaner theorem-facing branch than the current
sign-defect packet search.

## Honest Interpretation

This run does not derive exact closure or any finite-window dynamics.

What it earns:

- the Step-7 witness-freeze branch is genuinely well-posed
- `F_SS(1/12)` can be frozen on the repaired authority sheet without changing
  burden currency
- the controlling `L_cross <= 1/24` authority can be stated cleanly, with the
  older `1/12` entries demoted to historical variance only
- the next honest step on this branch is exact closure bookkeeping and not
  another family search

What it does **not** earn:

- an exact dynamical pass
- a near-circuit theorem
- any direct regularity proof progress

## Best Next Step

If this exact-screen branch is the current prize-facing default, the next real
move is:

1. keep the frozen witness `F_SS(1/12)`,
2. keep the repaired branch `G_tmpl` / `G_leak` sheets exactly as authority,
3. move to the Step-7 / Chain-Step-2 question:
   derive exact closure-forced bookkeeping on that same frozen ledger without
   allowing repair-by-extension.
