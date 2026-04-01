# Direction Regularity Is Prior Art, Not A Standalone Novelty Claim

Status: `VERIFIED` with `INFERRED` consequence

The local geometry corpus already treats vorticity-direction regularity as an
existing conditional-regularity framework. The mission context explicitly names
the Constantin-Fefferman route, and the refined geometry chain says the branch
must benchmark against Constantin-Fefferman-Majda style direction coherence and
later vorticity-direction coherence work before claiming novelty.

The repository's theorem-level boundary is still headline-only. It records that
sufficiently regular vorticity direction implies regularity, but it does not
reconstruct the full hypotheses, norms, or proof details of the cited
direction-coherence literature.

The consequence is operational: a later step may not call a route new if it
only restates that sufficiently regular or coherent vorticity direction yields
regularity, or if it reaches that statement only by importing stronger
`nabla xi`-type control. To stay live, the branch would need a new
Navier-Stokes-specific bridge from localized direction coherence to full
stretching control or to a persistence mechanism that is not already absorbed
by the known criterion family.

Step-015 sharpens that benchmark into the branch's primary theorem-facing
comparator and endpoint family. Before package choice, the only explicit
geometry-facing theorem endpoint family already named on disk is the
`Constantin-Fefferman / direction-regularity` comparator; `full stretching`
remains the live mechanism target, not a separately frozen endpoint.

Under the current record, the only non-absorbed delta that can still be
written is a genuinely dynamic Navier-Stokes-specific persistence bridge:
coherent tube persistence on intense regions would have to produce
criterion-scale direction input and also speak to full stretching. If that
bridge needs hidden Eulerian component matching, forbidden relocalization, or
stronger `nabla xi` control, then the route has already fallen back into the
comparator family instead of clearing it.

Filed from:
- `missions/beyond-de-giorgi/library-inbox/step-002-exploration-001-geometry-prior-art-benchmark.md`
- `missions/beyond-de-giorgi/library-inbox/step-015-exploration-001-endpoint-currency-and-candidate-claim.md`
- `missions/beyond-de-giorgi/library-inbox/step-015-exploration-002-admissibility-comparator-and-verdict.md`
