# Exploration 002 Summary: 6-Point NMHV Tree Amplitude

## Goal
Compute A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) in N=4 SYM via BCFW recursion ([1,2⟩ shift, 3 channels) and Grassmannian G(3,6) residues. Compare term-by-term structure between the two methods.

## What Was Tried
1. **6-particle kinematics** — "3+3 balanced" construction (two 3-body clusters in a shared rest frame)
2. **MHV baseline** — Parke-Taylor formula for all 15 MHV configurations at 6 points
3. **BCFW [1,2⟩ shift** — pole-finding, sub-amplitude assembly for all 3 channels
4. **BCFW [2,4⟩ cross-check** — independent BCFW shift to verify [1,2⟩ result
5. **BCFW [3,4⟩ cross-check** — attempted; all channels structurally zero
6. **Grassmannian G(3,6)** — not attempted (no verified BCFW target to validate against)

## Outcome: PARTIAL SUCCESS / INCONCLUSIVE

### What worked:
- **Kinematics [VERIFIED]**: Momentum conservation to 10⁻¹⁶, masslessness to 10⁻¹⁷ for all tested seeds
- **MHV baseline [COMPUTED]**: All 15 Parke-Taylor amplitudes at 6 points computed without errors
- **Channel 3 structural zero [VERIFIED]**: For [1,2⟩ shift, channel {1̂,6,5,4}|{2̂,3} is exactly zero because λ_K ∝ −λ_{1̂} at the pole — confirmed numerically to machine precision

### What failed:
- **BCFW not verified**: [1,2⟩ shift gives Total = −8030−3626i (seed=42) but [2,4⟩ shift gives −543−259i — a ~93% disagreement. At least one implementation has wrong cyclic color orderings in the sub-amplitudes.

## Verification Scorecard
- **[VERIFIED]**: 2 claims (kinematics generation, Channel 3 structural zero)
- **[COMPUTED]**: 1 claim (MHV baseline, 15 amplitudes)
- **[CONJECTURED]**: 1 claim (BCFW channel values — may be wrong)
- **[CHECKED]**: 0

## Key Takeaway
The sub-amplitude cyclic color ordering is the critical unsolved problem. BCFW for 6-point NMHV requires knowing the correct cyclic traversal direction for internal-momentum insertions in 4- and 5-particle sub-amplitudes. Without this, all three BCFW implementations disagree. The Grassmannian computation is blocked until BCFW is verified.

## Proof Gaps Identified
- **Cyclic color ordering rule**: For a BCFW channel {L}|{R} with internal momentum K, what is the correct cyclic ordering of particles in A_L(K, ...) and A_R(-K, ...)? The rule is: "K appears adjacent to the shifted particles, with the remainder in their original cyclic order." This needs to be implemented carefully — errors of ±1 position in the cyclic order change the Parke-Taylor denominator.
- **No analytic ground truth**: Without an independent formula (e.g., R-invariant / momentum twistor 5-bracket formula), there is no way to verify which BCFW shift is correct.

## Unexpected Findings
- The [3,4⟩ shift (both applied to particles 3⁻ and 4⁺) gives ALL channels zero — this is not a known degenerate case but seems to follow from structural zeros in each channel independently. Either the BCFW formula for this shift has a boundary term at z→∞ (shift doesn't vanish), or all channels genuinely vanish and the non-vanishing comes from the residue at infinity. This is surprising and worth understanding.
- The sign of the BCFW pole z* = −P²(0)/(2P(0)·q) is computed correctly by the numerical formula, but naive analytic derivation can introduce a sign error through the relation s₂₃ = ⟨23⟩[23] (positive) and 2P·q = ⟨24⟩[23]. Any analytic shortcut assuming s₂₃ appears as −⟨23⟩[23] will get the wrong sign for z*.

## Computations Identified for Next Exploration
1. **Implement momentum twistor R-invariant formula**: A₆^NMHV = A₆^MHV × Σ R(a,b,c,d,e) where R are 5-bracket functions. This gives the answer directly without BCFW recursion, providing a ground truth.
2. **Fix BCFW with explicit diagram**: Draw the BCFW diagram for each channel, read off the cyclic order from the diagram (not from set notation), implement accordingly.
3. **Implement Grassmannian G(3,6)**: Once BCFW is verified — set up 3×6 C matrix in gauge (I₃|C'), solve C·λ̃ = 0, compute 3 residues at positroid cells, compare to BCFW channels.
