# Exploration 001: Deep Extraction of the Shen-Zhu-Zhu Proof Technique

## Mission Context
This is a YANG-MILLS mission. We are attacking the Yang-Mills Millennium Prize Problem (existence and mass gap for 4D quantum Yang-Mills theory). This is strategy-002, focused entirely on the Shen-Zhu-Zhu (SZZ) 2023 result and its potential extensions.

**Do not conflate with other missions in this repository** (there are also missions on the Riemann Hypothesis, amplituhedron, and other topics — ignore all of those).

## Background

The Shen-Zhu-Zhu paper (CMP 400, 2023; arXiv:2204.12737) proved the first mass gap result for CONTINUOUS gauge groups (SU(N)) — but only at strong coupling (β < 1/48 in 4D). This is currently the most promising starting point for extending the Yang-Mills mass gap result.

**What we already know (from prior explorations):**
- SZZ use the Bakry-Émery approach: they verify that the lattice Yang-Mills Gibbs measure has positive "Ricci curvature" in a Bakry-Émery sense. This curvature condition on the measure implies a Poincaré inequality, which implies exponential decay of correlations (mass gap).
- The bound β < 1/(16(d-1)) = 1/48 in d=4 arises from a competition between SU(N)'s intrinsic Ricci curvature and the negative curvature contributed by the interaction terms in the Wilson action.
- At weak coupling (β ≫ 1/48), gauge field fluctuations dominate and the Bakry-Émery curvature bound fails — the positive Ricci curvature of SU(N) cannot control the system.
- SZZ's result is used as a key ingredient in proving the area law in the 't Hooft limit (Adhikari-Suzuki-Zhou-Zhuang, arXiv:2509.04688, 2025).

**What we do NOT yet know (this exploration's task):**
- The EXACT Bakry-Émery curvature calculation — the step-by-step derivation of 1/(16(d-1))
- Precisely what condition on the curvature tensor is verified, and where the calculation breaks at larger β
- Whether SZZ's mass gap satisfies Chatterjee's "strong mass gap" condition (see below)
- What the best possible extension strategy is

## Your Task

Read the Shen-Zhu-Zhu paper (arXiv:2204.12737) and any necessary background. Then answer the following questions with theorem-level precision:

### Question 1: The Exact Proof Technique

Extract the EXACT Bakry-Émery curvature calculation from SZZ:

a) **What is the configuration space?** What manifold does the Yang-Mills Gibbs measure live on? Is it (SU(N))^E for some edge set E, with a product structure?

b) **What is the Bakry-Émery condition they verify?** Write down the inequality. What is the curvature lower bound κ they prove? Is κ > 0 for β < 1/(16(d-1))?

c) **How does the factor 1/(16(d-1)) arise?** Identify the specific inequality in the proof where this constant appears. What two quantities are being balanced? (E.g., is it the Ricci curvature of SU(N) itself vs. a Hessian of the action?)

d) **What does the Bakry-Émery condition imply?** What Poincaré or log-Sobolev constant do they get? What does this give for the mass gap (spectral gap of the Langevin/heat semigroup)?

e) **Where exactly does the proof fail at β ≥ 1/(16(d-1))?** Is it a sign change in the curvature? A failure of the tensor to be positive definite? Identify the SPECIFIC step and the SPECIFIC term that causes the breakdown.

### Question 2: What Would Need to Change for Larger β?

a) **Is the bound tight?** Does the proof actually fail at β = 1/48, or is it just the method that fails? (I.e., is there numerical or other evidence that the mass gap continues to exist past β = 1/48?)

b) **What is the minimum change that would extend the method?** For example:
   - Could a tighter Ricci curvature estimate work?
   - Could a different stochastic process (not Langevin on the bare action) work, e.g., Langevin on an effective/RG-improved action?
   - Could an additional term in the Bakry-Émery calculation (e.g., from a convexity improvement via a change of variables) shift the bound?
   - Are there known improvements to Bakry-Émery curvature estimates (e.g., Ollivier-Ricci curvature, entropic curvature) that might give better bounds?

c) **Specifically for the RG+Bakry-Émery idea:** Could one apply the Bakry-Émery argument to an effective action obtained after one step of Balaban-style RG blocking (block-spin transformation)? Would the effective action have a HIGHER effective β in the Bakry-Émery curvature calculation? If so, this might extend the regime.

### Question 3: The Chatterjee Combination

Chatterjee (CMP 385, 2021) proved: "strong mass gap ⟹ area law for gauge groups with nontrivial center (e.g., SU(3) with center Z₃, SU(2) with center Z₂)."

The "strong mass gap" condition requires: there exists C, Δ > 0 such that for all gauge-invariant functions f, g:
  |Cov(f(x), g(y))| ≤ C ||f||_∞ ||g||_∞ exp(-Δ|x-y|)
uniformly for all boundary conditions and in infinite volume.

a) **Does SZZ's result satisfy the "strong mass gap" definition?** SZZ proves exponential decay of correlations at β < 1/48. Does their proof hold:
   - Uniformly for all (or any) boundary conditions? Or only for specific boundary conditions (e.g., periodic/torus)?
   - In infinite volume, or only in finite volume with finite-volume corrections?

b) **If SZZ satisfies the strong mass gap condition at β < 1/48**, then combining with Chatterjee gives: "For SU(N) with nontrivial center at β < 1/48, Wilson's area law holds." Has this been stated explicitly in the literature? Is it truly new?

c) **What is the exact statement of the combined theorem?** Write it out precisely. What group (SU(2)? SU(N)? SU(3)?) and what coupling regime?

## Success Criteria

**Success:** You have extracted:
1. The exact Bakry-Émery curvature inequality from SZZ with the specific constant showing how 1/(16(d-1)) arises
2. The specific mathematical step that fails at β ≥ 1/(16(d-1))
3. A clear assessment of whether SZZ satisfies Chatterjee's strong mass gap condition (with theorem or counterargument)
4. At least one specific proposal for extending the method to larger β

**Failure:** You cannot find the paper or cannot extract the specific curvature calculation (e.g., it is hidden in a complicated computation that requires more background). If this happens, report: (a) what you did find, (b) what background is missing, (c) what references would help.

**Partial success:** You extract 2 of the 4 success criteria with precision, and identify what additional work would complete the rest.

## Constraints

- This is a LITERATURE EXTRACTION task, not a computation. Read arXiv:2204.12737 deeply.
- Also check the follow-on paper arXiv:2509.04688 (Adhikari-Suzuki-Zhou-Zhuang 2025) which uses SZZ as an ingredient — this may clarify how SZZ's result is applied.
- Check Chatterjee's original paper (CMP 385, 2021; arXiv:2003.01943) for the exact strong mass gap definition.
- Write section-by-section as you find results. Do not wait until the end to write.
- This exploration directory is at: `explorations/exploration-001/` relative to your working directory.

## Output Format

Write a detailed REPORT.md covering:
1. Exact SZZ proof technique (with equations)
2. The specific β < 1/(16(d-1)) derivation
3. What fails at larger β
4. Extension strategies
5. The Chatterjee combination assessment
6. Novel claims (if any), clearly labeled

Then write a concise REPORT-SUMMARY.md (1-2 pages max) with:
- The single most important finding
- The answer to "does SZZ+Chatterjee give a novel theorem?"
- The most promising direction for extending β beyond 1/48
