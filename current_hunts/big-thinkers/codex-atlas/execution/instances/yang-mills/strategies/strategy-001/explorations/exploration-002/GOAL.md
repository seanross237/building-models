# Exploration 002: Constructive QFT — What Works in 2D/3D and What Breaks in 4D

## Mission Context

We are investigating the Yang-Mills Existence and Mass Gap Millennium Prize Problem. This requires rigorously constructing a quantum Yang-Mills theory in 4 spacetime dimensions. Constructive quantum field theory has succeeded in rigorously constructing several interacting QFTs in lower dimensions (2D, 3D) but has never succeeded in 4D for any interacting theory. Understanding precisely why is essential for identifying what new ideas might be needed.

## Your Task

Produce a **precision technical map** of constructive QFT results relevant to Yang-Mills, identifying exactly which techniques succeed in lower dimensions and exactly which steps fail or are missing in 4D. Not a narrative overview — specific theorems, specific failure modes.

## Specific Deliverables

### 1. Catalog of rigorous QFT constructions in 2D and 3D

For each major construction, identify:
- The theory constructed (scalar φ⁴, Yukawa, Yang-Mills, etc.)
- Spacetime dimension
- The method used (cluster expansions, correlation inequalities, RG, etc.)
- The main result (theorem statement or closest equivalent)
- Paper reference (authors, year, journal)

Priority constructions to locate:
- **Glimm & Jaffe**: φ⁴₂ (2D scalar field theory) — the first rigorous construction
- **Glimm & Jaffe**: φ⁴₃ and related results
- **Feldman & Osterwalder**: Yukawa₂
- **Balaban, Imbrie, Jaffe**: Yang-Mills₂ (if this exists)
- **Magnen & Sénéor, Rivasseau**: Various results in 2D/3D
- **Brydges, Fröhlich, Seiler**: Lattice gauge theories
- **Any construction of Yang-Mills₃** (3D Yang-Mills)

### 2. The 4D wall — what specifically breaks

For each technique that works in lower dimensions, identify what happens when you try to extend it to 4D:
- **Classification for each technique:**
  - WORKS IN 4D — technique extends (unlikely but check)
  - FAILS DUE TO [specific mathematical reason] — e.g., "cluster expansion diverges because..."
  - REQUIRES MODIFICATION — technique could work with [specific new ingredient]
  - UNKNOWN — no one has attempted the extension

Key areas where the 4D extension is expected to fail:
- Ultraviolet divergences: why are 4D divergences qualitatively harder than 2D/3D?
- Renormalizability vs. super-renormalizability: what's the precise technical consequence?
- Borel summability: does it hold/fail in 4D YM?
- Large field problems: how do they manifest differently in 4D?
- Gauge invariance complications: how does gauge symmetry interact with constructive methods?

### 3. The role of asymptotic freedom

Asymptotic freedom (Gross-Wilczek-Politzer, 1973) is unique to non-abelian gauge theories in 4D. It provides perturbative UV control. Analyze:
- Does asymptotic freedom help or hinder constructive approaches?
- What rigorous results exist about asymptotic freedom beyond perturbation theory?
- Is there a constructive proof of asymptotic freedom (not just perturbative)?

### 4. The mass gap specifically

Separate from the existence problem:
- In lower-dimensional constructions, how was the mass gap (or its absence) established?
- What techniques for proving mass gaps exist? (Correlation length bounds, spectral gap methods, etc.)
- Which of these have been attempted for 4D Yang-Mills?

### 5. State of the art

What is the closest anyone has come to a rigorous 4D interacting QFT? Consider:
- φ⁴₄ (4D scalar field theory) — the triviality results (Aizenman, Fröhlich)
- 4D Yang-Mills partial results
- Any other 4D interacting theories

## Success Criteria

This exploration SUCCEEDS if it produces:
- A catalog of at least 5 rigorous lower-dimensional constructions with theorem-level specificity
- Identification of at least 3 specific techniques that fail in 4D, each with a mathematical reason
- A clear statement of what "triviality" means for φ⁴₄ and its implications for Yang-Mills
- Assessment of which 4D obstacles are specific to Yang-Mills vs. generic to all 4D QFTs

## Failure Criteria

This exploration FAILS if it produces:
- Only narrative ("4D is harder because there are more divergences")
- No specific theorem references
- No distinction between Yang-Mills-specific and generic 4D obstacles

If you cannot access specific papers, state what's missing and what the key references are. Be **honest** about the level of precision you can achieve — don't fabricate theorem statements.

## Output

Write your findings to:
- `REPORT.md` in this exploration directory (target: 400-600 lines, with per-section detail)
- `REPORT-SUMMARY.md` — a concise (50-100 line) summary of key findings
