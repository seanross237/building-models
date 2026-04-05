# Exploration 002: CNS Paper Analysis — Novelty and Overlap Assessment

## Mission Context

A prior research program claims to have proved a mass gap for lattice SU(2) Yang-Mills at β < 1/6, improving on both SZZ (β < 1/48) and CNS (β < 1/24). We need to verify the novelty claim by reading the actual CNS papers.

Two CNS papers are central:
1. arXiv:2509.04688 (Cao-Nissim-Sheffield, September 2025) — "Dynamical approach to area law"
2. arXiv:2505.16585 (Cao-Nissim-Sheffield, May 2025) — "Expanded regimes of area law"

## Goal

Read both CNS papers carefully and determine whether the claimed β < 1/6 result is:
(a) Already in their papers
(b) Trivially derivable from their framework
(c) Requires genuinely new insight beyond their work

This is NOT a literature survey. It is a targeted, equation-level comparison.

## Tasks

### Task 1: Fetch and Read arXiv:2509.04688 (September 2025)
Fetch the paper from arXiv (try https://arxiv.org/abs/2509.04688 and the PDF).

For this paper, answer precisely:
1. **What is their main theorem?** State it exactly with all conditions.
2. **What technique do they use?** Is it the same Bakry-Émery approach as SZZ, or something different?
3. **What is their sharpest threshold for SU(2), d=4?** Extract the exact number.
4. **What is their Hessian bound?** If they improve SZZ's Lemma 4.1, how? Do they use a vertex reformulation, or something else?
5. **Do they compute the exact Hessian eigenvalues at Q=I?** Do they identify the staggered mode?
6. **Do they use Fourier analysis on the lattice?**
7. **Is there any mention of β < 1/6 or better?** Search the paper thoroughly.

### Task 2: Fetch and Read arXiv:2505.16585 (May 2025)
Same questions for this paper.

Additionally:
1. **Is this the same technique as the September paper?** Or a completely different approach?
2. **What is the relationship between "area law" and "mass gap"?** Are they proving the same thing as SZZ, or a different quantity?
3. **Does this paper use master loop equations?** If so, what is the ceiling on their threshold?

### Task 3: Convention Comparison
Both CNS and SZZ may use different conventions. For each paper:
1. What is their action convention? S = −β Σ Re Tr? Or S = −(β/N) Σ Re Tr? Or something else?
2. When they say "β < 1/24", is this in the same convention as our "β < 1/6"?
3. Are they proving area law (exponential decay of Wilson loops) or spectral gap (mass gap), or both?

### Task 4: Overlap Analysis
For each of our claimed novel results, determine if CNS already has it:

| Our Claim | In CNS? | Details |
|-----------|---------|---------|
| H_norm = 1/12 at Q=I | ? | Do they compute this? |
| Staggered mode is the maximizer | ? | Do they identify this? |
| Triangle inequality gives H_norm ≤ 1/8 for all Q | ? | Do they improve the triangle bound? |
| β < 1/6 threshold | ? | Do they reach this number? |
| Conjecture: H_norm ≤ 1/12 for all Q | ? | Do they state or prove this? |
| Weitzenböck decomposition M(Q) = M(I) + R(Q) | ? | Do they use this? |

### Task 5: What Prevents CNS from Reaching 1/6?
If CNS doesn't reach β < 1/6, explain precisely why:
- Is it a fundamental limitation of their technique?
- Is it because they didn't try the triangle inequality improvement?
- Could their framework be trivially extended to get 1/6 or better?

## Prior Context from Library

The library records about CNS:
- **Sept 2025 (2509.04688):** Uses vertex sigma-model + Bakry-Émery. Hessian bound 4(d−1)Nβ (exactly half the SZZ edge bound). Threshold doubled to β < 1/24 in d=4. Uses Durhuus-Frohlich slab condition.
- **May 2025 (2505.16585):** Uses master loop equations / string duality. Completely different from Bakry-Émery. Optimized ceiling β₀(4) ≈ 1/87. Curvature is structurally absent from master loop proof.

Verify these library entries against the actual papers. The library entries are from prior explorers who may not have read the papers carefully.

## Success Criteria
- [ ] Both papers fetched and read (at least abstract + main theorem + proof method sections)
- [ ] Precise threshold for each paper stated with convention
- [ ] Overlap table filled in with YES/NO/PARTIALLY for each claim
- [ ] Clear verdict: is β < 1/6 (a) in their papers, (b) trivially derivable, or (c) genuinely new?

## Failure Criteria
- Cannot access papers → report what sections you could access and what remains uncertain
- Papers use a fundamentally different convention → report the conversion factor

## What to Write
Write REPORT.md and REPORT-SUMMARY.md in your exploration directory. Include exact theorem statements from the papers with equation numbers where possible.
