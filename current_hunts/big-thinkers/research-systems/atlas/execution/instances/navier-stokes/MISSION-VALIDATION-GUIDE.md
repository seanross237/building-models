# Mission Validation Guide

## Tier 1: Mathematical Coherence
- The function spaces are specified precisely (Sobolev, Lebesgue, Besov) — not just "smooth" or "regular"
- The domain is stated for every result (R³, T³, bounded domain with boundary conditions)
- Claims distinguish between strong solutions, mild solutions, and Leray-Hopf weak solutions
- The viscosity ν is tracked — results should state whether they hold for all ν > 0 or specific regimes
- Scaling dimensions are correct: if a quantity has units, dimensional analysis is consistent

## Tier 2: Rigor and Reproducibility
- Analytical arguments have no hand-waving at critical steps — if an estimate is hard, say so
- Computations are reproducible: simulation code is provided with parameters, resolution, and convergence checks
- Citations are accurate (paper, authors, theorem/equation numbers)
- Numerical results include resolution dependence, convergence rates, and error estimates
- When a claim depends on a computation, **do the computation** rather than arguing about what the result "should" be
- Spectral methods and pseudospectral dealiasing are used correctly — aliasing errors are addressed

## Tier 3: Novelty
- The finding is not a restatement of known results or a literature summary
- If it combines existing results, the combination itself is new and non-obvious
- A researcher in PDE analysis or fluid dynamics would recognize a fresh contribution
- "Fresh" means: a new estimate, a new obstruction identified, a new connection between techniques, a new computational result, or a new blow-up criterion — not a new way of phrasing something known

## Tier 4: Significance for the Regularity Problem
- The finding advances a proof strategy — it doesn't just describe the problem, it changes what we know about it
- There is a clear logical path from this result to progress on NS regularity or blow-up
- Partial results are valued if they: close off dead ends, tighten regularity criteria, identify which estimates are loose, or connect the nonlinearity structure to regularity
- Negative results (this approach cannot work because X) are valuable if X is specific and provable
- Tao's 2016 obstruction is the benchmark: any regularity proof must use something his averaged NS doesn't have

## Tier 5: Defensibility
- The strongest counterargument has been identified and addressed
- Prior art search was thorough — the result hasn't been published before
- The result survives adversarial review
- Limitations are stated honestly — what the result does NOT show is as clear as what it does
- Any dependence on unproven conjectures or numerical evidence is explicitly flagged
- Numerical claims distinguish between "observed in simulation" and "proved"
