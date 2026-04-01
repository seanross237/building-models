# Mission Validation Guide

## Tier 1: Mathematical Coherence
- All statements use the SZZ conventions (S = −(β/N) Σ Re Tr, |A|² = −2Tr(A²))
- The corrected B_□ formula is used (backward edges include own link in holonomy)
- Claims distinguish between "for all Q" and "for Q=I" — the conjecture is about ALL Q

## Tier 2: Rigor and Reproducibility
- Any claimed proof must have zero hand-waving at critical steps
- All proof attempts must be tested computationally on at least L=2 and L=4 lattices
- If a step uses an inequality, verify it numerically for 50+ random configurations
- Every intermediate claim must be tagged: [PROVED], [COMPUTED], [CHECKED], or [CONJECTURED]

## Tier 3: Novelty
- A proof of Conjecture 1 would be novel — no existing paper proves λ_max(M(Q)) ≤ 4d for all Q
- Partial results (e.g., proving for new families of Q beyond pure gauge/flat/uniform/single-link) count as progress
- New structural insights about WHY the conjecture is hard are valuable (but must be specific, not vague)

## Tier 4: Significance
- A complete proof gives β < 1/4 (12× SZZ, 6× CNS) — immediately significant
- A partial proof that tightens the bound from 1/8 toward 1/12 for all Q is useful
- A precise obstruction characterization ("the proof requires X, and X is equivalent to Y") that reduces the problem is useful
- Reproducing known results is NOT useful — the prior mission already catalogued the landscape

## Tier 5: Defensibility
- The proof must handle the worst case (adversarial Q), not just typical or random Q
- The known special cases (pure gauge, flat, uniform, single-link) must be recovered as consequences
- The proof must NOT require per-plaquette bounds stronger than |B_□|² ≤ 16 (which is false)
- Any claimed proof survives adversarial review: dedicated exploration to find counterexamples or logical gaps
