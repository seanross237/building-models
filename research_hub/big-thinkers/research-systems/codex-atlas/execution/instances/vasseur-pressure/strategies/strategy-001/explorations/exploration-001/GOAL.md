<!-- explorer-type: standard -->

# Exploration 001: Extract the Precise Definition of Beta from Vasseur (2007)

## Goal

Read Vasseur (2007) — "Regularity criterion for 3D Navier-Stokes equations in terms of the direction of the velocity" (but note: the key result is actually about pressure, in the Appendix / Conjecture 14 area — the title may be misleading). The paper may also be cited as Vasseur (2007, Math. Nachr.) or a closely related paper. Search for: **Vasseur, De Giorgi iteration, Navier-Stokes, pressure exponent**.

If the specific paper is hard to find, the key result is sometimes attributed to or discussed in:
- Vasseur (2010), "A new proof of partial regularity of solutions to Navier-Stokes equations" (Nonlinear Diff. Eqs. Appl.)
- Cheskidov & Shvydkoy (2014), or related papers on De Giorgi methods for NS
- The general framework of De Giorgi-Nash-Moser iteration applied to NS pressure

**What EXACTLY is the pressure exponent beta?** Extract the precise mathematical definition at the equation level. Specifically:

### Required Deliverables

1. **The exact mathematical definition of beta.** In the De Giorgi iteration for NS, the pressure term enters with some integrability exponent. What is the functional inequality? What does beta parametrize? Write the key inequality in full, with all norms, exponents, and domains specified. Use the notation from the paper.

2. **What does beta > 3/2 give you?** State the EXACT theorem or conjecture: if the pressure satisfies [what condition with beta > 3/2], then [what conclusion — L^∞ bound on weak solutions? Full regularity? Partial regularity improvement?]. Include the theorem/conjecture number and equation numbers from the paper.

3. **What is the current value beta = 4/3?** Where does this come from? Is it from the standard Calderón-Zygmund bound on pressure (Δp = -∂_i∂_j(u_i u_j) → CZ theory)? Or from something else? Trace the 4/3 to its origin — which specific estimate produces it?

4. **What is Conjecture 14 (or the Appendix result)?** State it precisely. Is it a conjecture or a conditional theorem? What exactly would need to be proved to close the gap from 4/3 to 3/2?

5. **The De Giorgi iteration structure.** At which step of the iteration does the pressure exponent beta appear? What role does it play — does it control convergence of the iteration? Does it determine the integrability gain per step? Write enough of the iteration structure that a reader can see WHERE beta enters and WHY its value matters.

6. **A computable specification of beta_effective.** Given a velocity field u(x,t) on a periodic 3D grid and its associated pressure p(x,t), write the mathematical formula for computing beta_effective as a ratio of actual-to-bound for the specific inequality that beta parametrizes. This should be:
   - `beta_effective = [actual value of some quantity] / [theoretical bound on that quantity]`
   - Or, if beta is not naturally a ratio, describe what measurement from DNS would quantify "how much slack is available" in the pressure term relative to the De Giorgi threshold.
   - Include a Python function skeleton `compute_beta_effective(u, p, params) -> float` with clear mathematical comments explaining each step.

7. **DNS computability assessment.** Can beta_effective be meaningfully computed from DNS data on a finite grid? Potential obstacles:
   - Does the De Giorgi iteration require infinite-resolution limit operations?
   - Is beta defined via a supremum over all level sets that can't be discretized?
   - Does the iteration involve non-local operations that don't have grid analogues?

   Give a clear YES/NO/PARTIALLY answer with justification. If NO, explain the structural obstacle. If PARTIALLY, explain what aspects can be computed and what can't.

### What to Distinguish

- **Vasseur's own claims** vs. your interpretation. Flag every statement as [VASSEUR] or [INTERPRETATION].
- **Beta (the exponent in the De Giorgi framework)** vs. **CZ slack (the ratio of CZ bound to actual pressure norm)**. These CAN decouple. Never conflate them.
- **Worst-case bound** vs. **typical-case value**. If beta = 4/3 is a worst-case, say so. If it's tight, say so.

### Context from Prior Work

This exploration is part of a mission investigating the Navier-Stokes regularity problem via Vasseur's pressure approach. Prior findings from a different angle:

- **The enstrophy approach is a dead end.** The logical circle (regularity ↔ BKM condition ↔ enstrophy bounded) cannot be broken by enstrophy bounds alone. This motivates the pressure-based approach.
- **CZ pressure bound is universally 7.6-17.5× tight** across all tested initial conditions (Taylor-Green, anti-parallel tubes, random Gaussian, Kida vortex) and Reynolds numbers (Re=100-5000). This near-tightness is unexplained.
- **Current beta = 4/3, need beta > 3/2 for regularity.** The gap to close is 1/6.
- The CZ bound comes from: Δp = -∂_i∂_j(u_i u_j) and CZ theory gives ||p||_{L^q} ≤ C_q ||u|²||_{L^q} = C_q ||u||²_{L^{2q}}.

### Success Criteria

✅ **Success:** All 7 deliverables answered with equation-level precision. The computable specification is mathematically well-defined. The DNS computability assessment is clear.

❌ **Failure:**
- Cannot locate the relevant paper/result → report what you searched for and what you found
- Beta turns out to be a qualitatively different object than expected → describe what it actually is
- The De Giorgi iteration is too complex to summarize meaningfully → provide the key inequality where beta enters and explain the obstacle

### Output Format

Structure your report with sections matching deliverables 1-7. Use LaTeX notation for equations. Cite specific theorem numbers, equation numbers, and page references from the paper(s) you read.
