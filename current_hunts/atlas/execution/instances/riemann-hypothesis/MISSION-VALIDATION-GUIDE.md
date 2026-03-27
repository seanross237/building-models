# Mission Validation Guide

## Tier 1: Novelty
- The finding is not a restatement of known results or a literature summary
- If it combines existing results, the combination itself is new and non-obvious
- A domain expert in analytic number theory would recognize a fresh contribution

## Tier 2: Mathematical Rigor
- Claims follow from their premises without gaps
- Computations are reproducible — code is provided or steps are explicit
- Citations are accurate (paper, authors, theorem/equation numbers)
- No hand-waving at critical steps — if a step is hard, say so rather than glossing over it
- When a claim depends on a computation, **do the computation** rather than reasoning about what the result "should" be. Explorers have full shell access and can write code (Python, scipy, numpy, sympy, mpmath). A numerically verified result is stronger than an analytical sketch.

## Tier 3: Evidence
- Claims are backed by computation, explicit citation, or formal argument — not just plausibility
- Numerical results include precision estimates and convergence checks
- Analytical results identify exactly where existing proofs break down and what would be needed to extend them

## Tier 4: Significance
- The finding advances a proof strategy — it narrows the search space, connects previously unrelated results, eliminates a class of approaches, or provides new evidence
- Not just "interesting if true" — there is a clear line from this finding to progress on RH
- Partial results are valued if they close off dead ends or tighten bounds

## Tier 5: Defensibility
- The strongest counterargument has been identified and addressed
- Prior art search was thorough — the claim hasn't been published before
- The result survives adversarial review: devil's advocate attacks don't collapse it
- Limitations are stated honestly — what the result does NOT show is as clear as what it does
