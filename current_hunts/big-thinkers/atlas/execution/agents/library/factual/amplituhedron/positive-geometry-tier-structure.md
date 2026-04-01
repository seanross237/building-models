---
topic: Three-tier structure of positive geometry extensions and the UV finiteness wall
confidence: verified
date: 2026-03-27
source: amplituhedron strategy-001 exploration-003 (synthesis)
---

## Finding

Positive geometry extensions form a three-tier structure based on how much geometric machinery is achievable. The deepest structural result is the **UV finiteness wall**: loop-level positive geometry requires UV finiteness, and UV finiteness alone is not sufficient (also need Yangian symmetry).

---

## The Three-Tier Structure

### Tier 1 — Full Amplituhedron (All-Loop, All-Multiplicity)
**Applies to**: Planar N=4 SYM; ABJM (3D N=6, via N=4 dimensional reduction).
**Requirements**: Yangian symmetry, planarity, maximal SUSY (UV finiteness).
**Scope**: Very narrow — only these two theories.
**Depth**: Maximum — locality and unitarity are DERIVED not assumed; Yangian organizes all-loop structure; geometry of positive Grassmannian directly encodes quantum corrections.

Note on ABJM: The ABJM amplituhedron (arXiv:2306.00951) is constructed by sign change + symplectic reduction from the N=4 one. Not truly independent — the N=4 parent structure is essential. Only bipartite-graph negative geometries survive the projection.

### Tier 2 — Scattering Forms / Partial Positive Geometry (Primarily Tree Level)
**Applies to**: Bi-adjoint ϕ³ (associahedron — cleanest), ϕ⁴ (Stokes polytopes), multi-scalar ϕ^p (accordiohedra), YM tree amplitudes (scattering forms), gravity tree amplitudes (CHY pushforward), cosmological wavefunctions (cosmological polytopes), string amplitudes (stringy canonical forms, associahedral grid).
**Requirements**: Tree-level, planarity/color-ordering. Yangian symmetry NOT required.
**Scope**: Broad at tree level — most planar theories accessible.
**Depth**: Moderate — gives efficient computations and structural insights (BCJ origin, KLT geometry) but doesn't reveal the same depth as Tier 1.

### Tier 3 — Structural Insights Only (Partial, Messy, or Conjectural)
- **Non-planar N=4**: Zero conditions hold (2016 evidence) but no complete geometric formulation
- **1-loop YM**: Corolla polynomial provides partial geometry but requires polynomial decoration
- **N<4 SUSY**: On-shell diagram Grassmannian structure exists but measure is deformed (not a canonical form)
- **Gravity multi-loop**: KLT structure partially geometric via associahedral grid (2025) but no graviton amplituhedron

### Complete Failures
- **Color-full QCD**: Non-planar, UV-divergent at loop level, quarks break cyclic color structure, confinement
- **Non-planar theories at loop level**: No amplitude/Wilson loop duality
- **Theories with explicit Lorentz violation or background dependence**: No known framework

---

## The UV Finiteness Wall

> **Positive geometry at loop level requires UV finiteness.**

UV divergences produce poles in the loop integrand that are NOT logarithmic singularities on boundaries of a geometric object. They are "extra" poles that break the canonical form interpretation. This is structural, not technical.

The only 4D theories UV-finite at all loops: N=4 SYM (planar, confirmed) and N=8 SUGRA (believed UV-finite, unproven at all loops). N=8 SUGRA is UV-finite but has **no amplituhedron** — demonstrating that UV finiteness is necessary but NOT sufficient. The additional requirement is **Yangian (dual conformal) symmetry**, which gravity backgrounds do not preserve.

---

## Positive Geometry as General Principle — Verdict

**IS a general principle for tree-level amplitudes** in:
- Planar/color-ordered theories
- With UV-finite tree amplitudes
- Connected via CHY or KLT (scalars, gauge, string, gravity — all accessible)

**Is NOT a general principle for loop-level amplitudes** in theories with UV divergences.

---

## Open Problems (2025 Status)

1. **Gravituhedron**: No complete geometric object after 5+ years. G-invariants (Trnka 2020) hint at structure but no polytope found. Major open problem.
2. **Non-planar amplituhedron**: "Zero conditions" conjecture (2016) holds non-planarly; no geometry constructed.
3. **Inflation / de Sitter**: Cosmological polytopes work for flat FRW; extension to dS with gravitons unknown.
4. **ϕ³ at loop level**: Bi-adjoint ϕ³ in 6D is UV divergent; no positive geometry for loop amplitudes.
5. **Non-perturbative physics**: No framework for confinement, condensates, or strong-coupling dynamics.
