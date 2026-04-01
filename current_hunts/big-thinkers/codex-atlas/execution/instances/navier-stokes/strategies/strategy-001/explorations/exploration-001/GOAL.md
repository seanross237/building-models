# Exploration 001: Catalog of Load-Bearing Inequalities in 3D Navier-Stokes Regularity Theory

## Mission Context

We are investigating the 3D incompressible Navier-Stokes equations on the periodic torus T³. The long-term goal is to identify which analytical estimates in regularity theory have the most slack (largest gap between the proven bound and what actually happens in flows), then tighten them.

This is the FIRST exploration of the mission. There is no prior work to build on. You are building the foundational catalog from scratch.

## Your Goal

Produce a comprehensive catalog of every **load-bearing inequality** in the major 3D Navier-Stokes regularity results. "Load-bearing" means: the inequality is used as a step in a regularity/partial regularity proof, and if it were tighter, the proof would give a stronger result.

For EACH inequality, extract (at theorem-level precision):

1. **Exact mathematical statement** — the precise inequality with function spaces, norms, exponents, and constants. Use standard notation (||·||_{L^p}, ||·||_{H^s}, etc.)
2. **Source** — the original paper where it appears or is first used in the NS context (author, year, theorem/lemma number if possible)
3. **Where it enters the proof** — which regularity result uses it, at which step, and what it enables
4. **What it bounds** — what physical/analytical quantity (energy, enstrophy, vorticity, pressure, etc.)
5. **Scaling behavior** — how the bound and the actual value scale with Reynolds number Re (or equivalently with viscosity ν). Does the gap grow, shrink, or stay constant as Re → ∞?
6. **Constant status** — is the constant explicit (computed, with a value) or existential ("there exists C > 0")? If explicit, what is the best known value? If existential, is a sharp constant known for the underlying functional inequality?
7. **Sharpness** — is the inequality known to be sharp (equality attained by some function)? If so, by what function? If the equality-attaining function is NOT a NS solution, note this — that's a source of potential slack.

## Specific Targets (minimum — find more if they exist)

### A. Functional Inequalities (building blocks)
- **Ladyzhenskaya inequality** (3D): ||u||_{L⁴} ≤ C ||u||^{1/4}_{L²} ||∇u||^{3/4}_{L²}
- **Gagliardo-Nirenberg-Sobolev interpolation** inequalities used in NS (the full family, not just Ladyzhenskaya)
- **Sobolev embedding** bounds (H¹ ↪ L⁶ in 3D, etc.)
- **Agmon's inequality** (if used in NS regularity arguments)
- **Calderón-Zygmund** estimates for the pressure (relating ∇²p to ω or ∇u)

### B. Energy and Enstrophy Estimates
- **Energy inequality** for Leray-Hopf weak solutions
- **Enstrophy evolution** equation and the estimates on the vortex stretching term
- **Higher-order energy estimates** (H^s norms)

### C. Regularity Criteria
- **Prodi-Serrin-Ladyzhenskaya criteria**: u ∈ L^p_t L^q_x with 2/p + 3/q ≤ 1 ⟹ regularity. What interpolation inequalities underpin this?
- **Beale-Kato-Majda** criterion: regularity controlled by ∫₀ᵀ ||ω||_{L^∞} dt
- **Any other conditional regularity criteria** and their supporting estimates

### D. Partial Regularity (CKN)
- **Caffarelli-Kohn-Nirenberg (1982)**: the local energy inequality, ε-regularity lemma, the covering/geometric argument
- What are the key estimates in the CKN proof? The ε-threshold, the energy decay estimates, the parabolic cylinder covering
- **Lin (1998)** and **Ladyzhenskaya-Seregin (1999)** simplifications — did they tighten any estimates?

### E. Endpoint/Critical Results
- **Escauriaza-Seregin-Šverák (2003)**: L³ endpoint. The backward uniqueness estimates, Carleman inequalities. What are the key bounds?
- **Seregin (2012)** and subsequent improvements

### F. Gronwall-Based Growth Estimates
- Where does the Gronwall lemma appear in NS regularity arguments?
- What exponential growth does it produce, vs. what actually happens?

### G. The Tao Obstruction (Important Context)
- **Tao (2016)**: Any proof of NS regularity must use specific structural properties of the NS nonlinearity (not just scaling, energy estimates, and general PDE techniques). Which of the above estimates depend on the specific NS nonlinearity, and which are "generic"? This classification is critical for identifying where slack might be exploitable vs. where it reflects a fundamental barrier.

## Output Format

Organize your report as follows:

### Part 1: Master Catalog Table
A table with columns: **ID | Inequality Name | Exact Statement | Source | Used In | Bounds What | Scaling (Re) | Constant Status | Sharpness | Tao Category (generic / NS-specific)**

### Part 2: Detailed Entries
For each inequality, a detailed entry with the full information from points 1-7 above.

### Part 3: Structural Analysis
- Which inequalities form chains (output of one feeds input of another)?
- Where do the chains have the most accumulated slack (multiplicative constants compounding)?
- Which inequalities are used in multiple regularity results (highest leverage)?
- Honest assessment: which estimates do you think have the most room for tightening, and why?

### Part 4: Gaps and Ambiguities
- Where are conventions inconsistent across authors?
- Where is the exact constant genuinely unknown vs. just not computed?
- What inequalities might you be missing?

### Part 5: Next Steps Recommendation
- Rank the top 5 inequalities by expected slack (most slack first)
- For each, what specific computation would quantify the slack?
- What would constitute a genuine breakthrough if one of these could be tightened?

## Critical Instructions

- **Write section by section.** If you have been searching for more than 20 minutes without writing, STOP and write a partial section with [INCOMPLETE] markers. After each major search batch (2-3 searches), write what you found so far.
- **Distinguish paper-sourced claims from your own reasoning.** If a claim comes from a specific paper, cite it. If it's your inference, say so.
- **If any inequality's exact statement is ambiguous or convention-dependent** in the literature, note the ambiguity and the different conventions. This is a positive finding, not a gap.
- **Be honest about what you don't know.** "I could not find the sharp constant for X" is more useful than silence.
- **Prioritize precision over breadth.** Getting 8 inequalities exactly right is better than 20 vague descriptions.

## Success Criteria
- At least 8 distinct load-bearing inequalities cataloged with exact mathematical statements
- Each inequality has all 7 fields filled (or explicitly marked as unknown)
- The Tao generic/NS-specific classification is attempted for each
- A ranked list of top 5 by expected slack is produced

## Failure Criteria
- Fewer than 5 inequalities cataloged
- Inequalities stated only in words without precise mathematical formulations
- No structural analysis of how inequalities chain together

## File Paths
- Write your detailed report to: REPORT.md (in this exploration directory)
- Write a concise summary (1-2 pages) to: REPORT-SUMMARY.md (in this exploration directory)
