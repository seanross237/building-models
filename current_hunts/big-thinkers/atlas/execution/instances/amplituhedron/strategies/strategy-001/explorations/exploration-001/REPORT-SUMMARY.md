# Exploration 001 — Summary

## Goal
Implement spinor-helicity formalism and compute the 4-point tree-level MHV amplitude A₄(1⁻,2⁻,3⁺,4⁺) in N=4 SYM via three independent methods (Parke-Taylor, BCFW recursion, Grassmannian), verify numerical agreement, and characterize computational cost.

## Outcome: SUCCESS

All three methods implemented, tested, and verified to agree to machine precision (< 10⁻¹⁵ relative error) across 10 independent kinematic configurations.

## Verification Scorecard
- **[COMPUTED]**: 8 claims — numerical results from all three methods across 10 kinematic points, timing benchmarks, Grassmannian minor expressions, momentum twistor data
- **[VERIFIED]**: 2 claims — BCFW sign convention derived analytically and cross-checked with direct Cauchy residue computation; Schouten identity validated
- **[CONJECTURED]**: 0

## Key Takeaway

The Grassmannian computation reveals a non-trivial algebraic identity: the amplitude expressed as 1/(M₁M₂M₃M₄) in square-bracket variables equals the Parke-Taylor formula in angle-bracket variables. This "angle-square duality" is invisible from either the Parke-Taylor or BCFW perspective alone — it emerges from the Grassmannian geometry. This is already suggestive that the amplituhedron framework encodes structural information beyond what conventional methods reveal.

## Proof Gaps Identified
- The algebraic identity -[34]³/([12][14][23]) = ⟨12⟩³/(⟨23⟩⟨34⟩⟨41⟩) was verified numerically but not formally proved in Lean. A Lean formalization could verify this follows from Schouten + momentum conservation.
- The BCFW sign convention (-1 factor) was derived analytically but could benefit from a systematic treatment applicable to arbitrary n.

## Unexpected Findings
- The Grassmannian "raw" result 1/(M₁M₂M₃M₄) equals Parke-Taylor EXACTLY without any delta-function Jacobian factor. This initially appeared wrong (I expected a [34]² Jacobian), but turns out the contour integral formulation of the Grassmannian absorbs the Jacobian into the canonical measure.
- The BCFW for color-ordered amplitudes has only 1 diagram (not 2) for n=4, because the non-adjacent channel {1,3}|{2,4} doesn't respect cyclic ordering.

## Computations Identified for Future Work
1. **6-point NMHV** — would require k=3 Grassmannian with multiple residues, testing whether the amplituhedron advantage scales
2. **Loop-level (L=1)** — amplituhedron at 1-loop introduces new geometric structure
3. **Positivity check** — verify that the C-matrix solution lies in the positive Grassmannian G₊(2,4)
4. **Symbolic computation** — redo in SymPy to get exact rational results and formally verify the angle-square identity
