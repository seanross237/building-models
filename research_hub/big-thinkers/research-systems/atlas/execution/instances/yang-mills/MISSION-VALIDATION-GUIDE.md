# Mission Validation Guide

## Tier 1: Mathematical Coherence
- Definitions are precise — not informal physics language but mathematically rigorous statements
- The specific axiom system being targeted is identified (Wightman, Osterwalder-Schrader, Haag-Kastler) and used consistently
- Claims about existence, uniqueness, or bounds are stated as formal mathematical propositions
- The gauge group is specified for every result (SU(2), SU(3), or general compact simple G)

## Tier 2: Rigor and Reproducibility
- Analytical arguments have no hand-waving at critical steps — if a step is hard, say so
- Computations are reproducible: code is provided or steps are fully explicit
- Citations are accurate (paper, authors, theorem/equation numbers)
- Lean formalizations compile, or the exact point of failure and missing lemma are identified
- Numerical results include precision estimates, convergence checks, and lattice size dependence
- When a claim depends on a computation, **do the computation** rather than arguing about what the result "should" be

## Tier 3: Novelty
- The finding is not a restatement of known results or a literature summary
- If it combines existing results, the combination itself is new and non-obvious
- A researcher in constructive QFT or lattice gauge theory would recognize a fresh contribution
- "Fresh" means: a new bound, a new obstruction identified, a new connection between approaches, a new formalization, or a new computational result — not a new way of phrasing something known

## Tier 4: Significance for the Mass Gap Problem
- The finding advances a proof strategy — it doesn't just describe the problem, it changes what we know about it
- There is a clear logical path from this result to progress on Yang-Mills existence and/or mass gap
- Partial results are valued if they: close off dead ends, tighten bounds, formalize prerequisites, or connect previously unrelated approaches
- Negative results (this approach cannot work because X) are valuable if X is specific and provable

## Tier 5: Defensibility
- The strongest counterargument has been identified and addressed
- Prior art search was thorough — the result hasn't been published before
- The result survives adversarial review
- Limitations are stated honestly — what the result does NOT show is as clear as what it does
- Any dependence on unproven conjectures is explicitly flagged
