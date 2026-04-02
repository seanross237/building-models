# Singleton Step-7 Obstruction Scan Summary

## Goal

Sharpen the April 2 one-bridge realization memo at the exact point where it
stopped:

```text
was the bridged candidate merely a bad singleton choice, or is the Step-7 core
already obstructed much earlier on singleton exact supports?
```

## Artifact

The executable audit is:

- `singleton_step7_obstruction_scan.py`

It does two things on the same exact coefficient currency as the older
singleton helical audit:

1. records the wavevector-level singleton obstructions forced by the Step-7
   exact core equations themselves;
2. exhaustively scans all `5! * 2^5 = 3840` role permutations and helicity
   assignments on the old five-vector support.

## Structural Obstructions

Before any coefficient optimization, three exact singleton obstructions already
appear:

- `A_n + A_n -> B_n` and `A_n + A_n -> C_n` force
  `k_B = 2 k_A = k_C`,
  so the exact singleton core collides the `B_n` and `C_n` wavevectors.
- `B_n + C_n -> C_n` forces `k_B = 0`,
  so the exact amplifier edge cannot occur on nonzero Fourier support.
- `A_n + C_n -> D_n` together with `C_n + D_n -> A_n` forces `2 k_C = 0`,
  so the return leg cannot coexist exactly with the activation leg on nonzero
  singleton support; it needs a conjugate adjustment.

So a full exact singleton realization of the Step-7 desired core is ruled out
already at wavevector arithmetic level.

## Exhaustive Scan Result

The scan confirms the obstruction concretely on the old five-vector support:

- assignments scanned: `3840`
- full exact realization found: `no`
- full exact-or-conjugate realization found: `no`
- best exact coverage: `1/6`
- best exact-plus-conjugate coverage: `2/6`

Even more sharply, across the entire scan the only Step-7 desired pairs that
ever appear at all are:

- exact: `A_n + C_n -> D_n` or `C_n + D_n -> A_n`
- conjugate-adjusted: the same two edges, swapped

No assignment on this singleton support ever realizes any version of:

- `A_n + A_n -> B_n`
- `A_n + A_n -> C_n`
- `B_n + C_n -> C_n`
- `D_n + D_n -> E_n`

The best rows still have large external spill:

- `external_abs_sum = 15.749879`
- `max_external_abs = 0.434933`

so the explicit singleton support is not remotely close to a finitely isolated
exact Step-7 carrier.

## Interpretation

This strengthens the April 2 bridge result in a useful way.

The earlier memo showed one explicit singleton candidate failing to realize
most of the Step-7 core. This scan shows that failure is not just a poor role
assignment or poor helicity choice on the old five-vector support.

The honest local conclusion is now:

```text
the Step-7 exact desired core is already singleton-obstructed in general, and
the old explicit five-vector support cannot realize more than a tiny fragment
of it even after exhaustive relabeling and helicity search
```

## Consequence For The Branch

This does not solve the Step-9 source-basis problem, but it sharpens it.

What is now less plausible:

- rescuing the carried `F_SS(1/12)` branch by a different singleton relabeling
  of the old explicit five-vector audit;
- or treating the April 2 bridge failure as merely an unlucky candidate.

What remains the right next question:

- if the branch is to reopen constructively, it likely needs a genuinely
  packet-level or multi-mode same-currency realization protocol rather than
  another singleton exact support.
