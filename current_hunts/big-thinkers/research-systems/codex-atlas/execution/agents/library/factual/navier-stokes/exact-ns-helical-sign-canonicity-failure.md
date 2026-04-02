---
topic: Splitting packet sign defect into `SD_part` and `SD_target` does not canonize the exact-NS helical packet object
confidence: checked
date: 2026-04-01
source: "exact-ns-helical-sign-bottleneck strategy-001 exploration-001 report"
---

## Finding

The proposed `SD_part` / `SD_target` split sharpens the sign-defect language for the old packetized Tao-circuit backup, but it still does not produce one theorem-facing exact-NS object. The refined observables move under harmless choices that do not change the underlying exact Navier-Stokes data, so the correct verdict remains a Phase 0 **canonicity failure**.

## Why The Sign Split Still Fails

### `SD_part` is not representative-invariant

On the natural conjugate-pair quotient

```text
{(k, sigma), (-k, -sigma)},
```

the family itself is canonical but its sign label is not. If `SD_part` is defined by choosing one representative from each pair, flipping a representative changes the global sign balance while leaving the exact support, exact solution segment, and exact triad magnitudes unchanged.

Counting both members does not rescue the statistic. Conjugation then pairs equal-weight opposite-sign contributions, so the global sign-balance defect trivializes instead of becoming meaningful.

### `SD_part` also moves under harmless packet refinement

The participation weight for a mode family is defined by summing triad weights over the triads that touch that family. If one packet is harmlessly refined into subfamilies with the same union support and the same Tao-role label, those participation masses are redistributed across a different family list. So the minority-helicity participation score is still refinement-dependent unless an extra refinement convention is imposed.

### `SD_target` and `Leak` still depend on non-canonical desired-triad bookkeeping

`SD_target` only becomes concrete after specifying which exact target triads count as the desired Tao edges inside the packets.

- If every role-compatible exact triad counts as desired, harmless support refinement changes the desired set.
- If only a witness subset counts, that witness choice is an extra convention rather than exact NS data.

Because the desired / internal-leakage / external-leakage split is defined relative to that target set, the same instability propagates to `Leak`.

## Consequence

The sign refinement therefore does not repair the earlier packet non-canonicity result. It makes the remaining freedoms easier to name:

- conjugate-pair representative choice for `SD_part`,
- packet support and refinement choice,
- desired-triad witness bookkeeping for `SD_target`,
- and the induced leakage ledger.

Later quantitative work on this object family would still be testing bookkeeping choices rather than one frozen theorem-facing packet object.

## Relationship To Other Entries

- `packetized-tao-circuit-noncanonical.md` records the broader packet-level negative that this sign-focused follow-up sharpens.
- `exact-helical-near-closed-tao-circuit-definition.md` is the earlier Phase 0 definition gate that made the singleton exact object precise before the packet fallback failed.
- `exact-singleton-tao-circuit-nonembeddability.md` records the stronger negative on the preferred singleton object that forced attention onto the packet backup in the first place.
