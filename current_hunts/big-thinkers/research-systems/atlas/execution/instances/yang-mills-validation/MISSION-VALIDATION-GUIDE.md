# Mission Validation Guide

## Tier 1: Mathematical Coherence
- Conventions are consistent with SZZ throughout (S = −(β/N) Σ Re Tr)
- Every step in the β < 1/6 proof chain is explicitly verified, not assumed
- When checking prior work, state what YOU verified vs what you're taking on trust

## Tier 2: Rigor and Reproducibility
- Independent rederivation of the proof, not just reading and nodding
- All numerical tests include: lattice size, number of configurations, configuration types, observed range, and comparison to claimed bound
- Code for larger-lattice tests must be provided and runnable

## Tier 3: Novelty Assessment
- The CNS comparison must be based on reading the actual paper, not abstracts or summaries
- "We couldn't find X in the paper" is weaker than "we found they use Y instead, which differs because Z"
- If the result is a rediscovery, say so clearly and identify what (if anything) is still novel

## Tier 4: Significance
- A confirmed novel result at β < 1/6 is publishable
- A found error in the proof chain is extremely valuable — better to find it now
- Extension to SU(3) (positive or negative) is significant either way
- The d=5 anomaly resolution clarifies the scope of the approach

## Tier 5: Defensibility
- The validation itself must be adversarial — actively look for errors, not confirmation
- Convention errors are the most likely failure mode (factors of 2, N vs 2N, 1/N factors)
- The B_□ formula was corrected once already — verify the correction is correct
