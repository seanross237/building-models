# Exploration 001: 4-Point Tree-Level MHV Amplitude — Three-Way Computation

## Mission Context

We are investigating whether the amplituhedron framework (and related positive geometry approaches to scattering amplitudes) is merely a computational tool for QFT, or reveals deeper physical structure. The first step is to establish computational ground truth by computing specific amplitudes via multiple methods and verifying agreement.

## Your Specific Goal

**Implement the spinor-helicity formalism in Python and compute the 4-point tree-level MHV (Maximally Helicity Violating) amplitude in N=4 super Yang-Mills theory via three independent methods. Verify numerical agreement. Characterize computational cost.**

This is a COMPUTATION task, not a research/survey task. You should spend most of your time writing and running code, not searching the web. Use web searches only to look up specific formulas or conventions you need.

## The Three Methods

### Method 1: Parke-Taylor Formula (Analytic Baseline)

The color-ordered tree-level MHV amplitude for n gluons in any gauge theory is given by the Parke-Taylor formula:

A_n^MHV(1⁻, 2⁻, ..., i⁻, ..., j⁻, ..., n⁺) = ⟨ij⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩...⟨n1⟩)

For n=4 with helicities (1⁻, 2⁻, 3⁺, 4⁺):
A_4 = ⟨12⟩⁴ / (⟨12⟩⟨23⟩⟨34⟩⟨41⟩) = ⟨12⟩³ / (⟨23⟩⟨34⟩⟨41⟩)

where ⟨ij⟩ are spinor brackets. This is the known answer. It can also be derived from color-ordered Feynman rules (4-gluon vertex + 3 channels with 3-gluon vertices).

### Method 2: BCFW Recursion

The BCFW recursion relation (Britto, Cachazo, Feng, Witten 2004, arXiv:hep-th/0501052) computes tree amplitudes from on-shell lower-point amplitudes. For a [1,2⟩ shift:

A_4(1⁻, 2⁻, 3⁺, 4⁺) = sum over poles of (A_L × 1/P² × A_R)

For 4-point, there's a single BCFW term (one factorization channel). The deformed momenta are:
- |1̂⟩ = |1⟩ + z|2⟩,  |2̂] = |2] - z|1]
- z is fixed by the on-shell condition of the internal propagator.

Implement this and evaluate numerically.

### Method 3: Positive Geometry / Grassmannian

The amplituhedron approach computes the same amplitude from the geometry of the positive Grassmannian G+(k,n). For 4-point tree-level MHV (k=2, n=4):

The amplitude is obtained from the canonical form (volume form) of the amplituhedron A_{n,k,L=0} in momentum-twistor space. For k=2, n=4, the amplituhedron is a convex polygon in 2D (after projection), and its canonical form is:

Ω = ⟨Y d²Y⟩⟨Y d²Y⟩ / (⟨Y Z₁Z₂⟩⟨Y Z₂Z₃⟩⟨Y Z₃Z₄⟩⟨Y Z₄Z₁⟩)

where Z_i are momentum twistors and Y is a point in G(2,4).

Equivalently, via the Grassmannian integral:
A_{n,k} = ∫ d^(k×n)C / (M₁ M₂ ... M_n) × δ^(k×4)(C·Z̃) × δ^(k×2)(C·η̃)

For k=2, n=4: the integral localizes to a sum over residues at poles of the minors. There is exactly 1 residue for the 4-point MHV case.

**Key references:**
- Arkani-Hamed, Trnka: "The Amplituhedron" arXiv:1312.2007
- Arkani-Hamed, Bourjaily, Cachazo, Goncharov, Postnikov, Trnka: "Grassmannian Geometry of Scattering Amplitudes" (the textbook)
- Elvang, Huang: "Scattering Amplitudes in Gauge Theory and Gravity" (textbook, Cambridge 2015) — Chapter 2 for spinor-helicity, Chapter 3 for BCFW, later chapters for Grassmannian

## Implementation Requirements

1. **Spinor-helicity infrastructure**: Implement a Python module with:
   - Complex 2-component spinors |i⟩, |i]
   - Angle brackets ⟨ij⟩ and square brackets [ij]
   - Momentum construction: p_i^{αα̇} = |i⟩[i| (massless on-shell momenta)
   - Momentum conservation check: Σ p_i = 0
   - Mandelstam variables: s = (p₁+p₂)², t = (p₂+p₃)², u = (p₁+p₃)²

2. **Specific kinematics**: Choose a concrete set of 4 massless momenta satisfying momentum conservation. For example, in the center-of-mass frame with energy E:
   - p₁ = E(1, 0, 0, 1), p₂ = E(1, 0, 0, -1), p₃ = E(1, sin θ, 0, cos θ), p₄ = -p₁-p₂-p₃
   - Or generate random spinors and construct momenta from them (ensuring p₄ = -p₁-p₂-p₃)

3. **Numerical evaluation**: Compute A_4 from all three methods at the SAME kinematic point. Compare. The results should agree up to an overall normalization convention.

4. **Cost characterization**: For each method, document:
   - Number of terms in the computation
   - Number of algebraic operations
   - How the complexity would scale to n-point (even if you don't compute n-point)
   - Any conceptual advantages/disadvantages

## Success Criteria

- **SUCCESS**: All three methods implemented in working Python code, evaluated at a concrete kinematic point, and producing the same numerical answer (up to normalization). The code is saved to `code/` and is reproducible.
- **PARTIAL SUCCESS**: Two of three methods agree. Third has an identified bug or convention mismatch.
- **FAILURE**: Cannot implement the methods in code, or get irreconcilable disagreements.

## Failure Path

If you find that the Grassmannian/amplituhedron computation is too complex to implement from published formulas alone, explain the STRUCTURAL reason — what exactly is needed that you couldn't find? What formula is missing? What convention is ambiguous? This information is more valuable than a vague "it was hard."

## Output

Write your report to: `explorations/exploration-001/REPORT.md`
Write your summary to: `explorations/exploration-001/REPORT-SUMMARY.md`
Save all code to: `explorations/exploration-001/code/`

Target report length: 300-500 lines. Include all key equations and every code snippet inline in the report, plus the full scripts in code/.
