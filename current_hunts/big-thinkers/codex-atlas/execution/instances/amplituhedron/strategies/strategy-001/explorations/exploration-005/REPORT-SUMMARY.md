# Exploration 005 Summary: Hidden Zeros in Positive Geometry

## Goal
Deep dive into the hidden zeros program: understand what they are, the March 2025 paper (arXiv:2503.03805), how far the program extends beyond N=4 SYM, and whether it represents a new principle of QFT.

## What Was Done
Systematic literature survey of ~15 papers: the original hidden zeros paper (arXiv:2312.16282 by Arkani-Hamed, Cao, Dong, Figueiredo, He), the March 2025 PRL paper (arXiv:2503.03805 by Backus & Rodina), the uniqueness/UV-scaling equivalence paper (arXiv:2406.04234 Rodina PRL 2025), the double-copy extension (arXiv:2403.10594), the surfaceology framework papers (arXiv:2309.15913, arXiv:2412.21027), the canonical YM integrand (arXiv:2408.11891), cosmological extension (arXiv:2503.23579), and the massive theories constraint (arXiv:2601.16860). Full technical extraction of formulas, definitions, theorems, and limitations.

## Outcome: SUCCESS

Clear technical account of hidden zeros: definition, geometric origin, formulas, scope, and limitations. Honest assessment of the program's reach.

## Key Takeaway

**Hidden zeros are a new, powerful characterization of physical amplitude properties (locality, unitarity, soft theorems) that makes them visible geometrically and allows relaxing them as axioms.** They are defined as follows: at n points in Tr(φ³), pick any "causal diamond" in the kinematic mesh and set all non-planar Mandelstam invariants c_{i,j} inside that diamond to zero — the amplitude vanishes. This is invisible from Feynman diagrams but obvious from the ABHY associahedron geometry.

**The key results, in order of strength:**
1. **Proved (tree level):** Zeros exist and uniquely determine Tr(φ³) amplitudes (equiv. to enhanced UV scaling). Three theories (Tr(φ³), pions, gluons) are unified by a unique kinematic shift δ.
2. **Proved (1-loop, assuming locality):** Unitarity ↔ big mountain zeros in Tr(φ³) surface integrands. This is a biconditional, not just implication.
3. **Conjectured and numerically verified at 4-points:** Big mountain zeros from a non-local, non-unitary ansatz (~6,500 parameters) uniquely fix the Tr(φ³) loop integrand; locality and unitarity emerge. NLSM fixed by factorization near zeros.
4. **Open:** 2-loop and beyond; Yang-Mills at 1-loop; standard momentum-space formulation of loop zeros.

**Critical boundary:** The loop-level results live in "surface kinematics" (not standard Feynman loop momenta). The zeros are defined via Y^± variables on a punctured disk — not directly translatable to conventional amplitudes. Whether any analog exists in momentum space is explicitly open.

**Constraint on universality:** A January 2026 paper shows hidden zeros survive massive deformations ONLY when mass is symmetry-protected (SSB, not explicit). This means zeros are probes of symmetry structure, not universal features.

## Comparison to Main Mission (Amplituhedron in N=4 SYM)

The hidden zeros program is the **natural generalization** of the amplituhedron philosophy to non-SUSY theories:
- Amplituhedron: auxiliary twistor space, N=4 SYM only, all loops in principle, proved (Inventiones 2025)
- Hidden zeros / surfaceology: kinematic space, non-SUSY colored theories, loop-level conjectural, actively being proved

They are NOT competitors — they address different theories. The surfaceology framework (curves on surfaces) is the common parent, with the amplituhedron as a special case (N=4 SYM) and hidden zeros as the non-SUSY branch.

## Unexpected Findings

1. **The δ-deformation is unique.** There is a theorem that the shift X_{e,e} → X_{e,e}+δ, X_{o,o} → X_{o,o}−δ is the ONLY kinematic shift preserving hidden zeros. This uniqueness — that a one-parameter family connects three seemingly different theories — is a deeper structural result than I expected. It says these three theories (scalar, pion, gluon) form a one-dimensional family in "theory space," unified by a shared amplitude function.

2. **Factorization near zeros is NOT standard factorization.** Near a zero with c_* ≠ 0, the amplitude factorizes as (1/X_B + 1/X_T) × A^{down} × A^{up}. This is NOT the usual 1/(momentum²) × A_L × A_R pole factorization. It's a completely new algebraic structure — the kinematic analog of a soft theorem, but more general.

3. **Loop zeros decompose back to tree-level objects.** The one-loop factorization formula gives: I_n → (1/Y^∓_i + 1/Y^±_{i-1}) × A_{n+2}^{tree}. A loop integrand, near its zero, factorizes onto a TREE-LEVEL amplitude. This is reminiscent of BCFW but for the zeros rather than the poles.

4. **Hidden zeros extend to cosmological wavefunctions** (arXiv:2503.23579). The same vanishing structure appears in early-universe correlators. This is far outside the original scattering amplitude context and suggests the zeros are a feature of field theory mathematics broadly.

5. **20+ follow-up papers in 2 years** (2024-2026). The rate of progress is remarkable — hidden zeros were introduced in December 2023 and there are already papers on higher-derivative gravity, massive theories, partial waves, BCFW recursion from zeros, cosmological wavefunctions, and fermionic theories. This is a genuinely active frontier.

## Leads Worth Pursuing

1. **arXiv:2510.11070** (Zhou, Oct 2025): Hidden zeros for higher-derivative YM (F³) and GR (R², R³). This connects to our main mission's finding about quadratic gravity — does the R² gravity hidden zero structure say anything about what makes that theory special? Worth checking if these zeros constrain the coefficient of R² in any way.

2. **The surface kinematics ↔ momentum space question**: The loop-level results live in surface kinematics. Finding the momentum-space translation (if any) would make these results concrete for standard QFT calculations. This seems like the central technical challenge for the field.

3. **Yang-Mills at 1-loop**: Explicitly left open in arXiv:2503.03805. The surface kinematics paper (arXiv:2408.11891) defines the YM integrand; the hidden zeros for it should follow. This would be a major result — emergence of locality/unitarity from zeros in a theory directly relevant to the Standard Model.

## Computations Identified

None required — this was a literature survey. However, a natural computation would be: verify the hidden zero conditions for the 5-point Tr(φ³) amplitude explicitly by substituting c_{1,3} = c_{1,4} = 0 into the 5-term amplitude formula and confirming cancellation. This would be a 10-line Python script, confirming the basic mechanism concretely.
