# Exploration 003: Lee-Wick Quantum Gravity — Full Viability Assessment

## Mission Context

We are developing a novel quantum gravity theory. Our landscape survey (exploration 001) identified Lee-Wick quantum gravity as the #2 most promising candidate. It escapes our no-go theorem because it uses meromorphic propagators with complex conjugate poles, not entire functions. Exploration 002 eliminated our #1 candidate (Bianconi's entropic action). Lee-Wick QG is now the top construction target.

## Your Specific Goal

Provide a comprehensive assessment of Lee-Wick quantum gravity as a complete theory of quantum gravity. This is NOT about Lee-Wick theories in particle physics (Lee-Wick Standard Model, etc.) — it's about GRAVITY specifically.

### Task 1: Reconstruct the Theory
- Find the key papers on Lee-Wick GRAVITY (not Lee-Wick particle physics): Modena, Rachwał, and collaborators; also Anselmi's comparison of Lee-Wick vs fakeon quantization
- What is the action? What is the propagator structure?
- The graviton propagator should be: G(p²) = 1/p² - 1/(p² + M²) or similar with complex conjugate poles
- What is the CLOP (Cutkosky-Landshoff-Olive-Polkinghorne) prescription for handling the complex poles?
- How does this differ from the fakeon prescription?
- What is the spectral dimension d_s of this theory?

### Task 2: Unitarity Status (THE KEY QUESTION)
This is the most important question. The higher-loop unitarity of Lee-Wick theories is debated:
- What is the current status (2024-2026)? Has it been proven or disproven at all loop orders?
- At tree level, Lee-Wick theories are unitary (complex poles don't contribute to absorptive parts). What about loops?
- What specifically goes wrong at higher loops, if anything?
- Are there recent papers (2023-2025) that settle the question?
- Is there a difference between real Lee-Wick theories (real masses) and complex Lee-Wick theories (complex conjugate masses)?

### Task 3: Tier 1 Validation
- **Correct DOF**: Does it have the massless spin-2 graviton?
- **Unitarity**: (From Task 2)
- **Ghost freedom**: Are the complex poles truly harmless? What about the Cutkosky rules?
- **UV completion**: Is it UV-finite or merely super-renormalizable? What exactly needs to be renormalized?
- **Diffeomorphism invariance**: Yes/No?
- **Renormalizability**: Super-renormalizable by construction. What is the degree of divergence?

### Task 4: Tier 2 Validation
- Does it recover Newton's law? What does the Newtonian potential look like with complex poles?
- Does it reduce to GR at low energies?
- PPN parameters?
- GW speed = c?

### Task 5: Comparison to QG+F
Provide an explicit point-by-point comparison:

| Property | QG+F (Fakeon) | Lee-Wick QG |
|----------|---------------|-------------|
| Action | ? | ? |
| Propagator | ? | ? |
| Ghost resolution | Fakeon (removed from internal+external) | CLOP (removed from external only) |
| Renormalizability | Renormalizable | Super-renormalizable |
| Unitarity | Proven (Anselmi) | ? |
| d_s | 2 | ? |
| Predictions: r | [0.0004, 0.0035] | ? |
| Predictions: n_s | ~0.967 | ? |
| Microcausality | Violated at Planck scale | ? |

### Task 6: Novelty Assessment
- Is "Lee-Wick quantum gravity" an existing active research program with its own community?
- How many papers? By whom?
- What is its status in the broader QG community?
- What has NOT been computed yet (gaps)?

### Task 7: Overall Verdict
- Does Lee-Wick QG pass Tier 1? Tier 2?
- Is it a genuinely distinct theory from QG+F, or the same theory with a different name?
- If distinct: what is the sharpest observational difference?
- Is this worth pursuing as our primary construction target?

## Success Criteria
- Clear unitarity verdict (proven/disproven/open, with specific references)
- Explicit comparison table with QG+F
- Assessment of whether this is a viable independent QG program

## Failure Criteria
- Confusing Lee-Wick gravity with Lee-Wick Standard Model
- No assessment of unitarity beyond tree level
- Vague comparison to QG+F

## Relevant Context

**The no-go theorem (from strategy 001):**
For Lorentz-invariant theories with propagator f(p²)/p² where f is an unbounded entire function with no zeros, d_s → 0. Lee-Wick theories ESCAPE this because their propagators are meromorphic (have complex poles), not entire.

**QG+F benchmark:**
- Action: S = ∫ d⁴x √(-g) [M_P²R/2 - (1/2f₂²)C²_μνρσ + (1/6f₀²)R²]
- Propagator: 1/p² + fakeon(1/(p²+M₂²)) (spin-2) + standard(1/(p²+M₀²)) (spin-0)
- Fakeon prescription: the massive spin-2 pole is quantized with a modified iε prescription that makes it neither particle nor ghost
- This differs from Lee-Wick CLOP prescription which removes complex poles from asymptotic states but allows them in internal lines
- Unitarity: proven for fakeon (Anselmi-Piva 2018)
- d_s = 2, renormalizable, passes all Tier 1-3 tests
- Prediction: r ∈ [0.0004, 0.0035], n_s ≈ 0.967
- Key tension: n_s vs ACT DR6 (2.3σ)

**Lee-Wick propagator structure (from exploration 001):**
G(p²) = 1/p² - 1/(p²+M₁²) + 1/(p²+M₂²) - ... with alternating signs and complex conjugate mass poles. With N pairs of complex poles, UV behavior is ~ 1/p^{2(N+1)}, giving d_s = 2(N+1). For N=1 (simplest case), d_s = 4 (better than QG+F's d_s = 2 for UV purposes).

The Lee-Wick and fakeon prescriptions give DIFFERENT S-matrix elements at loop level, making them physically distinct theories.

## Instructions
- Write your report to `explorations/exploration-003/REPORT.md`
- Write your summary to `explorations/exploration-003/REPORT-SUMMARY.md`
- **IMPORTANT: Write to REPORT.md after EVERY web search or significant finding.** Don't batch your writing.
- Use web search extensively — this is a technical topic where recent papers matter
