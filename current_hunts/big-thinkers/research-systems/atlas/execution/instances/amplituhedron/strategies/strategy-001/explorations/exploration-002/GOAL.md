# Exploration 002: 6-Point NMHV Tree Amplitude — BCFW vs Grassmannian

## Mission Context

We're building computational ground truth for the amplituhedron vs QFT relationship. Exploration 001 verified 4-point MHV agreement across Parke-Taylor, BCFW, and Grassmannian methods. Now we push to the first case where the Grassmannian has MULTIPLE residues: the 6-point NMHV (Next-to-MHV) amplitude.

## Your Goal

**Compute the 6-point NMHV tree-level amplitude A₆(1⁻,2⁻,3⁻,4⁺,5⁺,6⁺) in N=4 SYM via two methods: (1) BCFW recursion and (2) Grassmannian residues. Compare the term-by-term structure, not just the final answer. Characterize how many terms each method produces and whether the Grassmannian decomposition matches or differs from the BCFW decomposition.**

This is a COMPUTATION task. Write modular scripts. Run each piece separately. Update REPORT.md after each computation step — do NOT wait until the end.

## Method 1: BCFW Recursion for 6-Point NMHV

Use [1,2⟩ shift. The recursion generates terms by factorizing on internal propagators. For 6-point NMHV, the BCFW produces 3 terms (factorization channels: {6,1}|{2,3,4,5}, {5,6,1}|{2,3,4}, and {4,5,6,1}|{2,3}). Each term is a product of lower-point on-shell amplitudes.

The BCFW terms can be expressed in terms of R-invariants (also called 5-brackets [abcde]):

A₆^NMHV = A₆^MHV × (R₁₄₆ + R₂₅₁ + R₃₆₂)

where R_rst = [r-1, r, s-1, s, t] are dual-conformal invariants (momentum-twistor 5-brackets).

**Key reference:** Drummond, Henn, Korchemsky, Sokatchev "Dual superconformal symmetry of scattering amplitudes in N=4 SYM" (arXiv:0807.1095). Also: Arkani-Hamed, Cachazo, Cheung, Kaplan "A Duality for the S Matrix" (arXiv:0907.5418).

## Method 2: Grassmannian for 6-Point NMHV

The Grassmannian integral for G(3,6) (k=3, n=6):

L_{6,3} = ∫ d^{3×6}C / (vol(GL(3)) × M₁M₂M₃M₄M₅M₆) × δ^(3×4)(C·λ̃) × δ^(3×2)(C·η̃)

where M_i are consecutive 3×3 minors.

**Gauge fix:** Set C = (I₃ | C') where C' is 3×3. The delta functions localize to a specific solution C*. The amplitude is a sum over RESIDUES at poles of 1/(M₁...M₆) — these correspond to cells of the positive Grassmannian.

For n=6, k=3 tree level, there are **three residues** (matching the 3 BCFW terms). Each residue corresponds to a positroid cell of G₊(3,6).

The key test: do the 3 Grassmannian residues match the 3 BCFW/R-invariant terms one-to-one? Or does the Grassmannian provide a different decomposition?

## What to Compute

1. **Generate 6-particle kinematics** satisfying momentum conservation. Use the spinor-helicity infrastructure from exploration-001 (at `explorations/exploration-001/code/spinor_helicity.py`). Extend it to handle n particles.

2. **Compute A₆^MHV** via Parke-Taylor as baseline: A₆^MHV = ⟨12⟩⁴/(⟨12⟩⟨23⟩⟨34⟩⟨45⟩⟨56⟩⟨61⟩)

3. **Compute BCFW** terms individually. For each of the 3 factorization channels, compute the shifted momenta, on-shell internal propagator, sub-amplitudes, and the contribution. Sum and compare to baseline.

4. **Compute Grassmannian residues** individually. Gauge-fix C, solve the delta-function constraints, identify the 3 poles, compute each residue.

5. **Compare term-by-term**: Do the 3 BCFW terms correspond to the 3 Grassmannian residues? If so, provide the explicit mapping. If not, characterize the difference.

6. **Count complexity**: How many algebraic operations for each method? How would this scale to 8-point, 10-point?

## Implementation Notes

- Break your code into MODULAR scripts. One for kinematics, one for BCFW, one for Grassmannian. Run each separately.
- The 6-point calculation is substantially more complex than 4-point. Don't try to write a single monolithic script.
- If the full Grassmannian computation is too complex, implement as much as you can and clearly document what's missing and why.
- Use the known R-invariant expressions as cross-checks.

## Success Criteria

- **SUCCESS**: Both BCFW and Grassmannian computed and agree. Term-by-term correspondence characterized.
- **PARTIAL**: BCFW works but Grassmannian incomplete. Clear documentation of what blocked the Grassmannian.
- **FAILURE**: Neither method produces correct results for 6-point NMHV.

## Output

Report: `explorations/exploration-002/REPORT.md` (target 300-500 lines)
Summary: `explorations/exploration-002/REPORT-SUMMARY.md`
Code: `explorations/exploration-002/code/`
