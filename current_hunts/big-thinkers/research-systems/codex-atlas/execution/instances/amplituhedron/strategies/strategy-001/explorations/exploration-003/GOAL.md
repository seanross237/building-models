# Exploration 003: Positive Geometry Beyond N=4 SYM — Extension Map

## Mission Context

The amplituhedron computes scattering amplitudes in N=4 super Yang-Mills from pure geometry — no fields, no Lagrangian, no Feynman diagrams. We've verified this works at 4-point tree level (exploration 001: three methods agree to 10⁻¹⁵). The question: does this extend to realistic theories?

## Your Goal

**Map exactly where the positive geometry / amplituhedron framework extends beyond N=4 SYM and where it breaks. For each extension, characterize WHAT works, WHAT breaks, and WHY.**

This is a RESEARCH task (survey + analysis), not a computation task. You should search the literature systematically and produce a clear map. But be concrete — cite specific papers and explain specific obstacles.

## What to Cover

### 1. The Amplituhedron Itself (N=4 SYM Only)

- What features of N=4 SYM make the amplituhedron possible? (Dual conformal symmetry? Yangian symmetry? Planarity? Maximal SUSY?)
- Which of these features are essential vs. convenient?

### 2. Reduced SUSY: N=1 and N=2 SYM

- Do BCFW recursion relations work for N<4? (Yes — BCFW works for any gauge theory.)
- Is there a positive geometry for N=1 or N=2 amplitudes?
- What was found by Heslop, Lipstein, or others on N<4 geometric structures?
- What specifically prevents an "N=1 amplituhedron"?

### 3. Pure Yang-Mills (No SUSY)

- BCFW recursion works for pure YM tree-level gluon amplitudes.
- Does any positive geometry formulation exist for pure gluon amplitudes?
- What about the "all-line shift" or "all-multiplicity" results — do they have geometric interpretations?
- What are the specific obstacles? (No dual conformal symmetry? IR divergences? Non-planar structure?)

### 4. The Associahedron and Bi-Adjoint Scalars

- Bai & He (arXiv:1709.09066) showed that bi-adjoint scalar amplitudes m(α|β) are canonical forms of associahedra.
- Arkani-Hamed, Bai, He, Yan "Scattering Forms and the Positive Geometry of Kinematics, Color and the Worldsheet" — scattering forms.
- Does this work for realistic scalar field theories? What about Yukawa or gauge theories?
- Is the associahedron the "universal" positive geometry from which others are derived?

### 5. Gravity (SUGRA)

- Is there an amplituhedron for graviton amplitudes?
- Cachazo, He, Yuan (CHY formula) provides gravity amplitudes from scattering equations. Is there a geometric interpretation?
- KLT relations connect gravity to gauge theory amplitudes. Does the amplituhedron squared give gravity?

### 6. QCD-Like Amplitudes

- Multi-parton amplitudes in QCD use color-ordered decomposition.
- Does positive geometry help with QCD amplitudes in any regime?
- What about the leading color (planar) limit of QCD?

### 7. Cosmological Polytopes

- Arkani-Hamed, Benincasa (arXiv:1709.02813) — cosmological polytopes for flat-space wavefunction coefficients.
- Does this genuinely extend to inflationary cosmology?
- What are the status and limitations?

## Output Format

For each extension, provide a structured assessment:

| Feature | Status | Key Reference | What Breaks |
|---------|--------|---------------|-------------|
| ... | Works / Partial / Fails / Unknown | arXiv:... | ... |

Then a SYNTHESIS section addressing: Is positive geometry a general principle of quantum field theory, or is it special to a small class of highly symmetric theories? What is the evidence either way?

## Success Criteria

- **SUCCESS**: Clear map of 5+ extensions with specific characterizations of what works/breaks. At least one case where the geometric approach reaches results standard methods can't.
- **PARTIAL**: Map of 3+ extensions but some are unclear or superficial.
- **FAILURE**: Vague philosophical discussion without specific examples or papers.

## Important Notes

- Name specific papers and authors. Cite arXiv numbers.
- Don't just say "it works" or "it doesn't work" — explain the mechanism or obstacle.
- Focus on 2019-2026 developments. The field has evolved rapidly.
- If you find any case where the geometric approach can do something standard methods CANNOT, flag it prominently.

## Output

Report: `explorations/exploration-003/REPORT.md` (target 300-500 lines)
Summary: `explorations/exploration-003/REPORT-SUMMARY.md`
