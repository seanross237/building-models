# Exploration 002 — SED Extension Landscape: What's Been Computed, What's Open

## Mission Context

We are investigating Stochastic Electrodynamics (SED) — the program that derives quantum mechanical results from classical electrodynamics plus a real, Lorentz-invariant zero-point radiation field with spectral density ρ(ω) = ℏω³/(2π²c³).

SED successfully reproduces several QM results: harmonic oscillator ground state, Casimir effect, van der Waals forces, blackbody spectrum. The mission's goal is to push SED into territory where it either succeeds or fails in a quantitatively precise way — producing a number where SED and QED/QM either agree or disagree, with the discrepancy characterized.

## Your Task

This is a **literature survey and critical analysis task.** We need to map the landscape of SED computations to choose the best extension direction for our next explorations.

### Part 1: What has been computed in SED?

For each of these systems, research and summarize what the SED literature has actually calculated:

1. **Hydrogen atom / Coulomb problem in SED**
   - Key authors: de la Peña & Cetto, D.C. Cole, Boyer
   - Has anyone computed the ground state energy? What did they get?
   - Cole & Zou (2003, 2004) did numerical simulations — what were their results? Did the electron remain bound? Did it give -13.6 eV?
   - What are the known obstacles? (runaway solutions, classical collapse, Abraham-Lorentz instability)
   - Is this problem genuinely open or has it been settled (positively or negatively)?

2. **Anharmonic oscillator in SED**
   - Has anyone computed the quartic oscillator V(x) = ½mω₀²x² + λx⁴ in SED?
   - If not, is there a fundamental reason it hasn't been done, or is it just unstudied?
   - What would the QM comparison be? (Standard QM perturbation theory gives well-known corrections to the harmonic oscillator energy levels.)

3. **Multi-particle systems / entanglement in SED**
   - Two coupled oscillators sharing the same ZPF — has this been studied?
   - Marshall & Santos, Dechoum et al. — what did they find about Bell inequalities in SED?
   - The critical question: can SED reproduce Bell-inequality-violating correlations? What's the current status of this debate?
   - Is there a clean two-particle calculation where SED and QM make different predictions?

4. **Anomalous magnetic moment (g-2) in SED**
   - Has anyone attempted this? Boyer has worked on SED electrodynamics — any vertex correction attempts?
   - What would the SED prediction for the electron g-factor be? Can it even be formulated?

5. **Other SED calculations not in the standard four**
   - Lamb shift in SED?
   - Compton scattering in SED?
   - Tunneling / barrier penetration?
   - Anything else that tests SED vs. QM discriminatingly?

### Part 2: Discriminating power assessment

For each system above, assess:
- **Tractability:** Can this be computed in a single exploration (a few hours of coding + analysis)?
- **Discriminating power:** Will the result clearly separate SED from QED/QM? (Quantity where they agree to 10 decimal places = not interesting. Quantity where they diverge at leading order = very interesting.)
- **Novelty:** Has this specific calculation been done before? If yes, can we improve on it? If no, is it because it's hard or because nobody thought to try?

### Part 3: Recommendation

Based on Parts 1 and 2, recommend the single best extension direction for our next exploration. The recommendation should include:
1. Which system to compute
2. What specific quantity to calculate (be precise — "energy" is too vague, "ground state energy of quartic oscillator to second order in λ" is right)
3. What the QM comparison value is
4. Why this is the best use of our exploration budget
5. What the likely outcome is (will SED agree or disagree?)

Also recommend a second-choice direction in case the first proves intractable.

## Success Criteria

- At least 4 of the 5 systems in Part 1 are researched with specific paper references (author, year, arXiv or journal)
- The Cole & Zou hydrogen simulations are specifically discussed with their numerical results
- The Bell inequality / entanglement status is assessed with references to specific no-go results
- A clear, justified recommendation is provided for the next computation

## Failure Criteria

- If the survey reveals that SED has already been definitively falsified for all candidate systems, that is a valuable result. Document the specific falsification results with citations.
- If the survey reveals that one specific extension has been computed and gives a clean SED≠QM result, report that as a discovery — it means someone else already found the boundary.

## Deliverables

Write your findings to:
- `explorations/exploration-002/REPORT.md` — full detailed report (target 300-500 lines)
- `explorations/exploration-002/REPORT-SUMMARY.md` — concise summary (30-50 lines)

## Important Notes

- **Cite specifically.** For every claim about what SED predicts, give author, year, and ideally arXiv ID or journal reference.
- **Distinguish settled from open.** For each system, clearly state whether the SED result is (a) computed and matches QM, (b) computed and disagrees with QM, (c) partially computed with no definitive result, or (d) not computed at all.
- **Be honest about community reception.** SED is not mainstream. Most QFT physicists believe it cannot work beyond linear systems. Report the mainstream view alongside the SED practitioners' view.
- **Focus on computability.** We care most about quantities that can actually be calculated in a subsequent exploration. Grand theoretical arguments about whether SED can work are less useful than specific numbers.

## Context from Library

The library has one relevant entry:
- **Nelson's stochastic mechanics** is closely related to SED. Nelson showed QM is equivalent to conservative diffusion with diffusion coefficient ℏ/2m. Known limitation: single-time distributions match QM, but multi-time correlations fail (Blanchard et al. 1986, Grabert-Hänggi-Talkner). This is a warning flag — if Nelson's approach fails for correlations, SED (which provides the physical noise source for Nelson's abstract diffusion) may fail too.

The library has NO SED-specific entries. This exploration will be filling a gap.
