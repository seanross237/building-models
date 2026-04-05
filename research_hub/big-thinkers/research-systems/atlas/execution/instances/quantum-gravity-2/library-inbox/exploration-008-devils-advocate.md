# Exploration 008 — Devil's Advocate: Attacking the Unified QG+F–AS Framework

## Goal
Ruthlessly attack the unified framework claiming QG+F and Asymptotic Safety are the same UV-complete theory. Find every weakness. Rate each attack FATAL/SERIOUS/MODERATE/MINOR. Perform 5-tier validation.

## Status: COMPLETE

---

## Attack 1: Is This Trivially True? (The Tautology Attack)

### The Charge

The unified framework claims: "QG+F and AS are two descriptions of a single UV-complete theory." But consider: QG+F IS the perturbative treatment of four-derivative gravity. AS IS the non-perturbative treatment of (some truncation of) gravity that includes four-derivative terms. Saying "the perturbative and non-perturbative treatments of the same action are the same theory" is like saying "algebra and geometry are both mathematics." It's true, but vacuous.

### Prosecution

The tautology is real but partial. Here's the genuinely trivial part:

1. **Same action ≠ deep insight.** If you write down $S = \int \sqrt{-g}(R + R^2 + C^2)$ and then study it perturbatively (QG+F) vs. non-perturbatively (FRG/AS), OF COURSE you get "the same theory." That's definitional. The framework report (exploration 007) even says: "Both descriptions predict Starobinsky inflation because they describe the same $R^2$ term in the action." This is not a prediction — it's a tautology.

2. **The "QCD analogy" masks the tautology.** The elaborate QCD parallel table (§1 of framework) makes the claim feel deep. But in QCD, nobody says "perturbative QCD and lattice QCD are the same theory" as if that's a discovery. They're both QCD. The discovery would be if perturbative QCD somehow *couldn't* be the weak-coupling limit of the lattice theory. Analogously, the real question isn't whether QG+F and AS *could* be the same theory — it's whether they *must* be.

### Defense (what saves it from being pure tautology)

The claim has non-trivial content in exactly three places:

- **The ghost mechanism.** QG+F removes the ghost by fiat (fakeon prescription). AS might remove it dynamically (confinement). If these are the same mechanism at different couplings, that's genuinely new. But this hasn't been shown.
- **The fixed point question.** Whether the AF fixed point IS the NGFP (Codello-Percacci) or connects TO it (SWY) is a real mathematical question with a non-trivial answer. The framework proposes a specific answer (SWY picture with connecting trajectory) that could be wrong.
- **The analyticity bridge.** Claiming the fakeon average continuation solves AS's Wick rotation problem is a concrete methodological prediction. It could fail.

### Verdict: **MODERATE**

The framework is ~60% tautology and ~40% genuine conjecture. The tautological part (same action, same inflation, overlapping regimes) provides no new physics. The non-trivial part (ghost bridge, fixed point connection, analyticity resolution) is where all the real content lives — and those parts are precisely the parts that are unproven.

---

## Attack 2: The QCD Analogy Is Broken

### The Charge

The framework's structural backbone is the QCD analogy. It maps asymptotic freedom → strong coupling → confinement in QCD onto asymptotic freedom → strong coupling → ghost confinement in gravity. But this analogy has at least seven known failure points, and the framework treats them as minor inconveniences rather than potential deal-breakers.

### The Seven Breakdown Points — Assessed Honestly

**(a) No compact gauge group.**
QCD confinement is intimately tied to the compact gauge group SU(3) and its center symmetry Z(3). The Wilson loop area law, which is the criterion for confinement, depends on this compactness. Gravity's diffeomorphism group is non-compact and infinite-dimensional. There is no gravitational Wilson loop with an area law. There is no center symmetry. The entire mathematical machinery of confinement (center vortices, monopoles, dual superconductor picture) has no gravitational analog. **This is not a minor detail — it removes the primary theoretical mechanism for confinement.**
Severity: HIGH.

**(b) No color charge analog.**
In QCD, confinement confines colored objects — quarks and gluons carry color quantum numbers, and only color-singlet combinations (hadrons) appear as physical states. The spin-2 ghost carries no analogous quantum number. What is being "confined"? The ghost has the same quantum numbers as the graviton (spin-2, couples to stress-energy). There is no selection rule that separates "ghost-like" from "graviton-like" states at the non-perturbative level. The concept of "confining the ghost" has no rigorous meaning without a quantum number to enforce it.
Severity: HIGH.

**(c) Universal coupling.**
In QCD, color-neutral objects (photons, leptons) don't feel the strong force. This provides a clean separation between confined and unconfined sectors. Gravity couples universally to all energy-momentum. There is no gravitational analog of a "color-neutral" object that decouples from the confining dynamics. This means the transition between perturbative and non-perturbative regimes affects everything, not just the ghost — making the clean QCD-style phase picture much harder to sustain.
Severity: MODERATE.

**(d) No lattice proof of ghost confinement.**
QCD confinement was conjectured in the 1970s and confirmed by lattice QCD in the 1980s–90s. Lattice confirmation is the gold standard. No lattice formulation of four-derivative gravity exists. CDT exists but doesn't include the $C^2$ term and doesn't address ghost confinement. The conformal mode problem (Euclidean action unbounded below) makes naive lattice approaches ill-defined. After 10+ years of the analogy being proposed (Holdom-Ren 2015), there is zero non-perturbative evidence specific to the gravitational spin-2 ghost.
Severity: HIGH.

**(e) Conformal mode problem.**
The Euclidean gravitational action is unbounded below due to the conformal mode. This has no QCD analog (QCD's Euclidean action is bounded). This means the path integral measure is fundamentally different, and techniques that work in QCD (importance sampling, Monte Carlo) face qualitatively new obstacles in gravity.
Severity: MODERATE.

**(f) Ghost is UV-specific.**
In QCD, confinement is a property of the fundamental theory — quarks are always confined at low energies. In gravity, the "ghost" only exists in the UV-complete four-derivative theory. At low energies (GR), there is no ghost to confine. The confining dynamics must therefore operate only in a specific energy range ($E \sim M_P$), which is unlike QCD where confinement persists all the way down to zero energy.
Severity: LOW (this is actually a feature of the framework, not a bug).

**(g) Non-perturbative uncertainty.**
Anselmi himself acknowledged (JHEP 01, 2026, 104) that non-perturbative effects introduce "a new type of uncertainty." In QCD, the non-perturbative sector is precisely defined (lattice QCD gives numerical answers). In QG+F, the non-perturbative sector is acknowledged to be uncertain. This is not an analogy — it's an admission that the most important regime of the theory is not under control.
Severity: MODERATE.

### Cumulative Assessment

The analogy is not merely imperfect — it fails on the specific points that matter most. The three highest-severity breakdowns (a, b, d) all concern the **confinement mechanism itself**: no compact gauge group, no quantum number to confine, no lattice evidence. These aren't details of the analogy — they're the entire point of the analogy. Without confinement being established, the QCD parallel is decorative, not structural.

The framework report acknowledges these issues (§5.2) but treats them as "open problems" rather than potential falsifiers. A more honest assessment: the QCD analogy is an inspirational metaphor being treated as a structural proof.

### Verdict: **SERIOUS**

The analogy is load-bearing (the framework would collapse without it) and broken at its most critical joints (confinement mechanism). Not FATAL because confinement *could* occur through a non-QCD mechanism, but the framework doesn't provide one — it relies on the QCD analogy for the very thing the analogy can't deliver.

---

## Attack 3: The "INCONCLUSIVE" Results May Actually Be Failures

### The Charge

The prosecution (explorations 001–006) rated two key results INCONCLUSIVE:
- Fixed point compatibility (AF ↔ NGFP connection)
- Ghost fate at strong coupling

The framework treats INCONCLUSIVE as "not yet proven, but consistent." But there's a darker reading: decades of FRG work have NOT found a connecting trajectory, and decades of non-perturbative work have NOT shown spin-2 ghost confinement. At what point does absence of evidence become evidence of absence?

### The Fixed Point Trajectory

**The situation:** SWY (2022) found two distinct fixed points in fourth-order gravity. They did NOT compute a connecting trajectory. Their 2023 follow-up computed AF → IR flows but did not check whether these pass near the NGFP. The Codello-Percacci (2006) one-loop result that sees only one fixed point may be an artifact of low-order truncation.

**The uncomfortable question:** If the AF and NGFP are genuinely distinct fixed points (SWY picture), then the unified framework requires a specific RG trajectory connecting them. The FRG community has been computing trajectories in higher-derivative gravity for over a decade. No one has found this trajectory — not because they weren't looking, but because the phase space is well-explored and no such trajectory has appeared.

**Counter-argument:** The full four-coupling ($f_2, f_0, G, \Lambda$) phase space has NOT been exhaustively mapped. SWY worked in a specific truncation; others have worked in different truncations. The absence of the trajectory may reflect truncation limitations, not its non-existence. This is plausible.

**But:** If the trajectory doesn't exist, the SWY version of the unified framework is dead. The Codello-Percacci version (one fixed point) survives but is less interesting — it reduces to the tautology of Attack 1.

### The Spin-2 Ghost Confinement

**The situation:** The Becker et al. (2017) scalar ghost decoupling result is 9 years old. It has NOT been extended to spin-2 in the intervening decade. The Draper et al. (2020) complex pole tower is for a general truncation, not specifically the Stelle ghost. No one has done the obvious calculation: compute the full spin-2 sector of the graviton propagator in the $C^2$-extended FRG.

**The uncomfortable question:** Why hasn't this calculation been done? Two possibilities:
1. It's technically very hard (FRG for higher-spin form factors is cutting-edge).
2. Preliminary attempts didn't give the "right" answer and were not published (publication bias).

Possibility 1 is generous. Possibility 2 is cynical but not unreasonable — publication bias is well-documented in physics.

**The honest assessment:** After a decade of work, the absence of a result is mildly negative evidence. It's not strong evidence of absence (the calculation is genuinely difficult), but it's not nothing either.

### Verdict: **SERIOUS**

Both INCONCLUSIVE results involve calculations that are well-defined, technically feasible (hard but not impossible), and have been on the community's radar for years. The fact that they remain unresolved after a decade is weakly negative. The framework's viability hinges entirely on these two unresolved calculations — making it, in its current state, more of a conjecture than a framework.

---

## Attack 4: The Novel Predictions Are Unfalsifiable

### The Charge

The framework claims seven novel predictions (§4 of the construction). Let's assess each one for actual testability:

| # | Prediction | Testable? | When? |
|---|-----------|-----------|-------|
| 1 | Fakeon average continuation resolves AS Wick rotation | In principle (computation) | Could be done now — but it's a theoretical calculation, not an observation |
| 2 | Ghost confinement scale = $M_P$ | No — requires Planck-scale physics | Never (with foreseeable technology) |
| 3 | BH evaporation phase transition | Requires observing Planck-mass BHs | PBH searches ~2030s–2040s (speculative) |
| 4 | Sharpened $r$ prediction | Yes — CMB | LiteBIRD ~2036–2037 |
| 5 | Spectral dimension profile | In principle (lattice computation) | Requires lattice 4-derivative gravity (doesn't exist) |
| 6 | Six-derivative couplings from NGFP | In principle (computation) | Could be done now (theoretical) |
| 7 | Higgs mass consistency | Already tested (retrodiction) | Already happened — not a prediction |

### Assessment

- **Prediction 4** ($r$ sharpening) is the only genuinely testable prediction with a foreseeable experiment (LiteBIRD). But even this is weak: the framework predicts $r \in [0.0004, 0.004]$, which is essentially the same range as standalone QG+F. The "sharpening" (NGFP determines $b$) requires a computation that hasn't been done. Without the computation, the prediction is no sharper than QG+F alone.

- **Predictions 1, 5, 6** are "computable" — they could be tested by theoretical calculations. But these are consistency checks, not experimental predictions. A theory that can only be tested by doing more theory is not making experimental predictions.

- **Predictions 2, 3** require Planck-scale observations. They are unfalsifiable with any foreseeable technology.

- **Prediction 7** is a retrodiction (Higgs mass already measured). It adds no predictive power.

### The Deeper Problem

The framework inherits the "one-prediction problem" from QG+F (see explanatory-debts-catalog.md, Debt #7): the only experimentally accessible prediction is $r$ from CMB, and even that won't sharply discriminate the unified framework from standalone QG+F or standalone AS, because all three predict $r \sim 0.003$.

**What would a genuinely novel, testable prediction look like?** Something that:
- Only the unified framework predicts (not QG+F alone or AS alone)
- Is experimentally accessible before ~2040
- Has a specific numerical value (not a range spanning an order of magnitude)

The framework has zero predictions meeting all three criteria.

### Verdict: **SERIOUS**

The framework's novel predictions are either untestable (Planck-scale), uncomputed (theoretical consistency checks), or not genuinely novel (same $r$ range as components). This is not FATAL — many theoretical frameworks in quantum gravity face this problem — but it means the framework cannot be experimentally distinguished from its components for the foreseeable future.

---

## Attack 5: Alternative Explanations — Shared Features ≠ Same Theory

### The Charge

The framework's strongest evidence is that QG+F and AS share multiple features: $d_s \to 2$ in the UV, Starobinsky inflation, asymptotic freedom in higher-derivative couplings, resolution of perturbative unitarity problems. But shared features don't imply identity. Consider:

- QCD and gravity both have asymptotically free couplings. They are obviously different theories.
- String theory and AS both predict $d_s \to 2$ in the UV. They are very different frameworks.
- Multiple inflationary models predict $r \sim 0.003$. They are not all the same theory.

### The Alternative Interpretation

QG+F and AS could be two different theories that:
1. Start from the same classical action (four-derivative gravity)
2. Apply different quantization procedures (fakeon prescription vs. FRG)
3. Get compatible results in overlap regions (because they start from the same action — see Attack 1)
4. Diverge in non-overlap regions (Planck-scale, where neither is under control)

Under this interpretation:
- The Starobinsky inflation agreement is trivial (same $R^2$ term)
- The $d_s \to 2$ agreement is trivial (same propagator structure)
- The BH agreement at large $r$ is trivial (both reduce to GR)
- The ghost fate and fixed point connection are the ONLY non-trivial questions — and both are unresolved

This is a "minimal interpretation" — it accepts all the data but doesn't invoke unification. It's more parsimonious because it doesn't require ghost confinement, connecting trajectories, or the phase transition mechanism. It just says: "Two approximation schemes applied to the same action agree where they overlap. Of course they do."

### What Would Distinguish Same-Theory from Compatible-But-Different?

The critical test is whether the two descriptions make **contradictory predictions** in any regime, or **jointly constrain** each other in ways that neither does alone. The framework claims joint constraints (e.g., NGFP determines $b$ parameter for inflation). But these constraints require computations that haven't been done.

Without those computations, the "unified framework" and the "two-compatible-theories" interpretation are empirically indistinguishable.

### Verdict: **MODERATE**

The alternative interpretation is viable and more parsimonious. The unified framework goes beyond it only in unproven conjectures. However, this attack doesn't kill the framework — it just shows that the unification claim is currently underdetermined. The framework remains a *hypothesis* that could be confirmed or refuted by the missing calculations.

---

## Attack 6: The Fakeon Average Continuation Claim Is Circular

### The Charge

The framework's boldest methodological prediction (Novel Prediction #1) is: "The fakeon average continuation resolves AS's Wick rotation problem." But this claim assumes what it's trying to prove.

### The Circularity

1. The average continuation is derived from the fakeon prescription.
2. The fakeon prescription is part of QG+F.
3. Applying it to AS assumes QG+F's quantization scheme is correct for the non-perturbative theory.
4. But whether QG+F's quantization scheme is correct for the non-perturbative theory is precisely the question the unified framework is trying to answer.

In other words: "IF QG+F and AS are the same theory, THEN the average continuation resolves AS's Wick rotation problem. And the average continuation resolving AS's Wick rotation problem is evidence that they're the same theory." This is circular.

### Defense

The circularity can be broken if the average continuation is tested independently:
- Apply the average continuation to an AS calculation where the standard Wick rotation fails.
- Check whether the result is physically sensible (positive spectral weight, unitary, correct low-energy limit).
- If it works, that's independent evidence — not circular.

This test has not been performed. No one has applied the average continuation to FRG effective actions. The prediction is therefore not circular in principle but untested in practice.

### Additional Problem: Why Fakeon Rather Than Lorentzian AS?

AS already has its own resolution to the Wick rotation problem: Lorentzian AS (D'Angelo et al. 2024), which works directly in Lorentzian signature without any Wick rotation. If AS can solve its own problem without QG+F's help, then the average continuation is not needed and the "novel prediction" dissolves.

### Verdict: **MODERATE**

The circularity is real but breakable. The bigger problem is that the prediction is untested AND potentially unnecessary (Lorentzian AS exists). This weakens the prediction from "bold and novel" to "one possible approach among several, currently untested."

---

## Attack 7: What Do the Actual Researchers Think?

### The Charge

If QG+F = AS is such a natural identification, the leading researchers in both programs should have noticed and endorsed it. What do they actually say?

### Anselmi's Position (QG+F side)

Damiano Anselmi, the architect of the fakeon program, has NOT endorsed the identification QG+F = AS. His recent publications (2024–2026) focus on:
- Asymptotically local QFT (arXiv:2410.21599) — relating local and nonlocal QFTs
- Classicized dynamics (JHEP 01, 2026, 104) — acknowledging non-perturbative uncertainty
- Causality abandonment (arXiv:2601.06346) — radical philosophical reorientation

He acknowledges that non-perturbative effects exist and matter, but does NOT point to AS as the non-perturbative completion. His program actively avoids engaging with AS. This is telling: the person who best understands QG+F does not see AS as its natural partner.

### Reuter/Wetterich's Position (AS side)

The AS community treats four-derivative gravity as a truncation within their framework, not as a separate theory to be unified with. SWY (2022) explicitly frame asymptotic freedom as "a viable *alternative* to asymptotic safety" — not as a complement to it. Wetterich's work with Platania on fictitious ghosts (2020) suggests the ghost might be a truncation artifact, which would make the fakeon prescription unnecessary rather than complementary.

### Salvio's Position (QQG)

Salvio and collaborators have called quantum quadratic gravity "a concrete realization of asymptotic safety" — but this is the Codello-Percacci one-fixed-point picture, not the SWY two-fixed-point picture. Salvio's "QQG = AS" is closer to the tautology of Attack 1 than to the substantive unification of exploration 007.

### Holdom-Ren's Position

Holdom and Ren (2015, 2016, 2024) are the closest to the unified framework's vision. They explicitly propose the QCD analogy and ghost confinement. But even they describe this as a "conjecture" and acknowledge the lack of evidence. Their work is inspirational, not confirmatory.

### The Significance

**No leading researcher in either QG+F or AS has endorsed the specific unified framework proposed in exploration 007.** Anselmi doesn't engage with AS. The AS community sees AF as alternative, not complementary. The closest advocates (Holdom-Ren) call it a conjecture. This doesn't make the framework wrong — important ideas often come from outside both camps — but it means the framework has no community of experts backing its specific claims.

### Verdict: **MODERATE**

The lack of expert endorsement is not fatal (novel frameworks are often unendorsed initially) but should temper confidence. The framework is a synthesis that neither community has attempted, possibly because both communities see obstacles that the framework hand-waves past.

---

## 5-Tier Validation

### Tier 1: Novel — Is this framework genuinely new?

**Assessment:** The specific five-bridge structure (ghost, fixed point, inflation, BH, analyticity) with the SWY two-fixed-point interpretation and the QCD analogy as organizing principle has not been published as a unified package. Individual elements exist in the literature (Holdom-Ren analogy, Codello-Percacci identification, Draper et al. confinement). The synthesis is new; the components are not.

**Rating: MARGINAL.** Novel as synthesis, not novel in components. The framework's originality lies in *combining* known ideas, not in new physics or mathematics. This is legitimate — many important contributions are syntheses — but the bar for a "novel framework" should include at least one new calculation or result.

### Tier 2: Consistent — Is the framework internally consistent?

**Assessment:** The framework is internally consistent within its stated assumptions. There are no logical contradictions. The two interpretations (Codello-Percacci vs. SWY) are presented as alternatives, not contradictions. The regime structure is self-consistent. Bridge mechanisms are compatible.

However, there is a tension: the framework needs the ghost to be simultaneously (a) a well-defined perturbative degree of freedom (for QG+F) and (b) dynamically confined/removed (for AS). The framework resolves this by invoking energy-scale dependence (fakeon at high $E$, confined at $E \sim M_P$). This is consistent but unproven — it's exactly the QCD analogy, and whether it works for gravity is the central open question.

**Rating: PASS.** No internal contradictions. The unproven assumptions are acknowledged as open problems.

### Tier 3: Explanatory — Does it explain things neither QG+F nor AS alone explains?

**Assessment:** The framework claims to explain:
1. Why QG+F and AS coexist (they're the same theory) — but this might be trivial (Attack 1)
2. BH evaporation endpoint (phase transition mechanism) — but this requires ghost confinement (unproven)
3. AS's Wick rotation problem (average continuation) — but Lorentzian AS may already solve this (Attack 6)
4. Why the Planck scale is special ($\Lambda_{\text{ghost}} = M_P$) — genuinely interesting but tautological if $m_2$ is set by hand

The strongest explanatory gain is the BH evaporation phase transition with a specific dynamical trigger (Bonanno 2025 instability at $r_H \approx 0.876/m_2$). This genuinely goes beyond either framework alone. But it's a single result, not a systematic explanatory advantage.

**Rating: MARGINAL.** Some explanatory power, mostly contingent on unproven conjectures. The BH phase transition is the best genuinely novel explanation.

### Tier 4: Predictive — Does it make predictions beyond either framework alone?

**Assessment:** Per Attack 4, the framework's seven novel predictions decompose as:
- 1 experimentally testable ($r$ from CMB) — but not sharper than QG+F alone without the $b$ computation
- 3 theoretically computable (average continuation, spectral dimension, six-derivative couplings) — but uncomputed
- 2 experimentally inaccessible (ghost confinement scale, BH phase transition)
- 1 retrodiction (Higgs mass)

No prediction is both novel to the unified framework AND experimentally accessible AND numerically specific.

**Rating: FAIL.** The framework does not currently make any prediction that goes beyond what its component theories predict individually and that can be tested.

### Tier 5: Testable — Can any prediction be tested with foreseeable technology?

**Assessment:** The CMB prediction ($r$) is testable by LiteBIRD (~2036–2037), but it's not specific to the unified framework. PBH remnant searches are speculative (2030s–2040s). The theoretical consistency checks could be done now but aren't experimental tests.

The framework could become more testable if the NGFP $b$ parameter were computed, giving a specific $r$ value. But that computation hasn't been done.

**Rating: MARGINAL.** Testable in principle via CMB, but the test doesn't discriminate the unified framework from its components. Testable via theoretical computation (which could be done now), but no one has done it.

---

## Severity Summary

| Attack | Rating | Key Issue |
|--------|--------|-----------|
| 1. Tautology | **MODERATE** | ~60% trivially true, ~40% genuine conjecture |
| 2. QCD analogy broken | **SERIOUS** | Load-bearing analogy fails at its most critical points (confinement mechanism) |
| 3. INCONCLUSIVE → failure | **SERIOUS** | Central conjectures unresolved after a decade; mildly negative evidence |
| 4. Unfalsifiable predictions | **SERIOUS** | No genuinely novel AND testable AND specific prediction |
| 5. Shared features ≠ same theory | **MODERATE** | More parsimonious alternative exists; unification is underdetermined |
| 6. Circular average continuation | **MODERATE** | Circularity breakable in principle but untested; Lorentzian AS may make it unnecessary |
| 7. No expert endorsement | **MODERATE** | Neither community endorses the specific synthesis |

### 5-Tier Results

| Tier | Rating |
|------|--------|
| Novel | **MARGINAL** |
| Consistent | **PASS** |
| Explanatory | **MARGINAL** |
| Predictive | **FAIL** |
| Testable | **MARGINAL** |

---

## Overall Verdict

### Is the framework viable?

**Yes, barely.** The framework is internally consistent and intellectually interesting. It is not killed by any single attack. But it is severely weakened by the cumulative weight of multiple SERIOUS attacks:

1. The QCD analogy — the framework's structural backbone — is broken at its most critical joint (confinement mechanism). Without an alternative mechanism for ghost removal, the framework is an analogy, not a theory.

2. The two central conjectures (connecting trajectory, spin-2 confinement) have been open for a decade with no resolution. The framework is exactly as strong as these conjectures — and currently, they are unsupported.

3. The framework makes no prediction that is simultaneously novel, testable, and specific. It cannot currently be distinguished from the simpler hypothesis: "QG+F and AS are compatible but separate theories applied to the same action."

### What would change this assessment?

Three calculations could dramatically strengthen the framework:

1. **Compute the AF → NGFP trajectory** in full four-coupling FRG. If it exists: SERIOUS → MODERATE for Attack 3 (fixed point part). If it doesn't exist (in the SWY picture): the framework needs the Codello-Percacci picture, which reduces to near-tautology.

2. **Compute the spin-2 ghost propagator** in $C^2$-extended FRG. If the ghost pole dissolves into complex towers: SERIOUS → MINOR for Attack 2 and Attack 3 (ghost part). If the ghost pole persists: the framework is effectively dead.

3. **Compute the NGFP $b$ parameter** for inflation. If it gives a specific $r$ value distinguishable from standalone QG+F: SERIOUS → MODERATE for Attack 4. If $b \approx 0$ (as most models suggest): the prediction collapses to standalone Starobinsky.

### Bottom Line

**The unified QG+F–AS framework is a well-constructed conjecture that currently lacks both theoretical proof and experimental testability.** It is not wrong — no evidence contradicts it — but it is also not right — no evidence specifically supports the unification claim over the simpler compatible-but-separate interpretation. Its fate depends entirely on two unperformed calculations (connecting trajectory, spin-2 confinement). Until those are done, it should be treated as a *speculative hypothesis*, not a framework.

**Overall rating: VIABLE BUT UNSUBSTANTIATED.**

Three SERIOUS attacks, four MODERATE attacks, one PASS and three MARGINAL ratings on the 5-tier scale, and one FAIL (Predictive). The framework survives devil's advocacy, but just barely — and only because it makes no claims strong enough to be definitively refuted.

---

*Explorer 008 — Devil's Advocate assessment complete.*
