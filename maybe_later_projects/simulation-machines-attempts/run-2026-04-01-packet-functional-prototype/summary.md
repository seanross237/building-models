# Packet Functional Prototype

## Goal

Take the exact packet object already defined in

- `codex-atlas/.../exploration-001/REPORT.md`

and turn it into a small reusable ledger prototype that computes:

- `Drive_target`
- `Leak_in`
- `Leak_out`
- `Leak`
- packet-level global minority-helicity participation `SD_part`
- desired-edge heterochirality dependence `SD_target`

## Best Reuse Point

The best existing exact definition artifact is the packet-level object from

- `codex-atlas/execution/instances/exact-ns-no-near-closed-tao-circuit/strategies/strategy-001/explorations/exploration-001/REPORT.md`

not the later `codex-nexus` v0 packet spec.

Reason:

- the `codex-atlas` artifact already fixes the exact objects `S`, packet
  partition, `G_target`, `Drive_e`, `Leak_in`, `Leak_out`, and `Leak`;
- the `codex-nexus` artifact is useful as a canonicity stress-test record, but
  it is already the failed clustered exact-mode family rather than the cleanest
  exact functional base.

So this prototype builds on the old exact helical ledger and treats the
`codex-nexus` material only as a warning about what not to smuggle back in.

## Important Structural Refinement

The exact packet support is sign-closed. If one defines global sign-defect by
counting both members of every conjugate pair, the defect becomes trivial and
cannot detect the intended asymmetry.

So the prototype computes `SD_part` on a **conjugate-pair representative
quotient**:

- each representative mode family carries one packet label and one reference
  helical sign;
- individual triad legs still know whether they use the representative or its
  conjugate.

This is the minimal correction needed for a usable packet-level sign-defect.

## Files

- `packet_ledger.py`
  - generic exact-ledger dataclasses and functionals.
- `singleton_sanity_check.py`
  - converts the old singleton exact support audit into a degenerate packet
    ledger and verifies that the new functionals reproduce the expected squeeze.
- `scan_singleton_sign_patterns.py`
  - runs the full `32`-sign singleton scan through the packet-ledger prototype.

## Expected Singleton Sanity Check

On the old singleton support:

- the chosen sign pattern should have finite `Leak` with smallish `SD_part`
  relative to the available sign patterns;
- `SD_target` should be `1.0`, because the surviving desired activation triad is
  entirely heterochiral.

That sanity check does **not** make the singleton route live again. It only
verifies that the packet functionals capture the mechanism shape we want before
we try to lift them to genuine packet families.

## What The Packet Prototype Already Confirms

Using the quotient-based packet ledger on the full singleton sign scan:

- the best finite packet-ledger leak still occurs at `minority_count = 1`;
- sign patterns with larger minority count have worse finite leak on average;
- the surviving desired drive keeps `SD_target = 1.0`, so the desired edge
  remains fully heterochiral in this prototype as expected.

So the new packet-level implementation preserves the old sign-sensitive signal
while fixing the sign-closed-support counting bug.
