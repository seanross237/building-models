# Exploration 002 Summary

## Goal

Operationalize the Tao screen for the geometry route by classifying the local
candidate ingredients into:

- transport or propagation structure
- exact algebraic structure
- multiscale coherence or concentration structure

and then deciding which concrete candidates remain live enough to justify Step
2.

## What Was Tested

- Read the required mission, chain, planning, attack, judgment, and obstruction
  files named in the exploration brief.
- Reused the step-001 screening rule mechanically:
  - what estimate changes?
  - what exact term or coefficient becomes smaller?
- Applied that rule to:
  - local Beltrami deficit or alignment
  - vorticity-direction coherence
  - tube coherence or persistence
  - the locally suggested hybrids:
    - Beltrami deficit plus concentration
    - Beltrami deficit plus anisotropy
    - direction coherence plus tube persistence

## Outcome

`succeeded`

The Tao-screen table was produced and it yields a narrowed positive result:
the geometry route survives Step 1 only in a hybrid transport-plus-coherence
form. Static Beltrami-style geometry does not survive as a primary route.

## One Key Takeaway

The mechanical discriminator is:

A geometry candidate only survives if it names a smaller piece of the full
stretching mechanism `S omega . omega` that Tao-style averaging would plausibly
destroy. If it only improves local alignment language, concentration language,
or the Lamb-vector side, it is not live.

## Bucket-By-Bucket Verdicts

- Transport or propagation structure: `live`
  Reason: this is the clearest place where Tao-style averaging can plausibly
  destroy a genuinely NS-specific ingredient, but only when persistence is tied
  to a full-stretching target rather than to static tube imagery.
- Exact algebraic structure: `weak but informative`
  Reason: the right target would be an exact link from a geometric observable to
  `S omega . omega`, but the concrete local Beltrami family still lands on the
  wrong object and does not shrink nonlocal strain.
- Multiscale coherence or concentration structure: `weak but informative`
  Reason: pure concentration or static coherence collapses, but coherence can
  still matter when paired with transport/persistence.

## Concrete Candidate Verdicts

- Local Beltrami deficit or alignment: `collapsed to Tao-robust/static geometry`
- Vorticity-direction coherence: `weak but informative`
- Tube coherence or persistence: `weak but informative`
- Beltrami deficit plus concentration: `weak but informative`
- Beltrami deficit plus anisotropy: `weak but informative`
- Direction coherence plus tube persistence: `live`

## Whether A Synthesis Exploration Is Justified

Yes, but only narrowly.

The only primary survivor worth carrying into Step 2 synthesis is:

- `direction coherence plus tube persistence`

Two secondary comparators may still be useful when fixing scenario class and
localization, but not as standalone routes:

- `vorticity-direction coherence`
- `tube coherence or persistence`

Beltrami-based candidates should not be treated as primary survivors.

## Leads Worth Pursuing

- Fix Step 2 around a single test question:
  can direction coherence persist along a coherent tube family strongly enough
  to make a full stretching contribution, including the exterior/inter-scale
  part, smaller in one fixed representation?
- Choose localization and scenario class to stress that question directly,
  rather than to rescue Beltrami language.

## Unexpected Findings

- The strongest live content is not a single geometric observable but a hybrid:
  coherence plus persistence.
- Beltrami survives only as a fragility screen or diagnostic comparator, not as
  an operational control route.

## Computations Worth Doing Later

- After Step 2 fixes scenario class and localization, write one explicit
  kernel-level representation of `S omega . omega` and test whether the hybrid
  observable can shrink:
  - the local/self-induced term
  - the exterior/nonlocal term
  - the localization interaction term
