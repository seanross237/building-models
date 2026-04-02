# Exploration 004: Emergent Locality and Unitarity from the Amplituhedron

## Mission Context

The amplituhedron computes scattering amplitudes in N=4 SYM without assuming locality or unitarity — they emerge from geometry. Prior explorations established: (1) three computation methods agree at 4-point (exploration 001), (2) positive geometry extends broadly at tree-level but the full amplituhedron requires UV finiteness, specific to N=4 SYM (exploration 003). The UV finiteness requirement is already a Tier 3 finding — the geometry encodes physical content, not just computational efficiency.

Now we probe the deepest claim: locality and unitarity are EMERGENT, not fundamental. What does this mean concretely? What are the physical consequences?

## Your Goal

**Investigate precisely how locality and unitarity emerge from the amplituhedron geometry. Identify whether this emergence has physical consequences — predictions, constraints, or observable signatures that differ from assuming locality/unitarity as axioms.**

## What to Cover

### Part 1: The Mechanism of Emergence

1. **What geometric property encodes locality?** In the amplituhedron, poles of the canonical form correspond to factorization channels (physical propagators). Locality = poles occur only at physical singularities. How is this guaranteed geometrically?

2. **What geometric property encodes unitarity?** Residues at poles give products of lower-point amplitudes (factorization). How does the amplituhedron geometry guarantee this?

3. **Where exactly in the standard amplituhedron construction do locality and unitarity appear?** Cite specific results — Arkani-Hamed & Trnka's original papers, and any subsequent proofs.

### Part 2: Beyond Locality and Unitarity

4. **Can the amplituhedron be deformed to produce non-local amplitudes?** If you change the positivity conditions (e.g., relax the requirement that the C-matrix lies in G₊(k,n)), what happens? Do you get objects that violate locality but are still mathematically well-defined?

5. **"Spurious" poles and non-planar terms.** Individual BCFW terms have spurious poles (non-physical singularities) that cancel in the sum. The amplituhedron makes each term manifestly well-defined. How does this relate to locality?

6. **Non-adjacent channels.** In the amplituhedron, poles correspond to boundaries of the positive region. Non-adjacent factorization channels (which violate cyclic ordering) don't appear. Is this a consequence of planarity, or of something deeper?

### Part 3: Physical Consequences

7. **Does emergent locality constrain UV completions?** If locality is emergent from positive geometry, does this constrain which UV completions of non-UV-finite theories are possible? Could this explain why gravity needs special UV behavior?

8. **Connection to holography and emergent spacetime.** The amplituhedron lives in a higher-dimensional space (momentum-twistor space) without a spacetime interpretation. Does this connect to holographic ideas about emergent spacetime?

9. **Predictions from non-locality.** Are there any amplituhedron-based predictions for Planck-scale non-locality or modified dispersion relations?

10. **Comparison to other "emergent locality" programs.** How does the amplituhedron's emergent locality compare to: (a) string theory's UV softness, (b) noncommutative geometry, (c) causal set discreteness?

### Part 4: Novel Insight Assessment

11. **Is the "emergent locality" claim genuinely new physics, or just a reformulation?** Be brutally honest. If assuming L/U as axioms and deriving them from geometry give the SAME predictions for all observables, then emergence is reformulation, not new physics. What evidence exists either way?

## Key References to Check

- Arkani-Hamed, Trnka "The Amplituhedron" arXiv:1312.2007 (original)
- Arkani-Hamed, Trnka "Into the Amplituhedron" arXiv:1312.7878
- Arkani-Hamed, Thomas, Trnka "Unwinding the Amplituhedron in Binary" arXiv:1704.05069
- Herrmann, Trnka "SAGEX Review Chapter 7: Positive Geometry" arXiv:2203.13018 (2022 review)
- Any 2023-2026 papers on emergent locality/unitarity in positive geometry context

## Output Format

Use the assessment format:

| Claim | Evidence For | Evidence Against | Status |
|-------|-------------|-----------------|--------|
| ... | ... | ... | Established / Supported / Speculative / Refuted |

## Success Criteria

- **SUCCESS**: Clear characterization of how L/U emerge, with at least one concrete example. Honest assessment of whether this is new physics or reformulation.
- **PARTIAL**: Mechanism described but physical consequences unclear.
- **FAILURE**: Vague philosophical discussion without specific examples.

## Output

Report: `explorations/exploration-004/REPORT.md` (target 300-500 lines)
Summary: `explorations/exploration-004/REPORT-SUMMARY.md`
