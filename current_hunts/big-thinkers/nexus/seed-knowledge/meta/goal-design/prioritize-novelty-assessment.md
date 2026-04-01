---
topic: Prioritize novelty assessment as first task when a theory is identified
category: goal-design
date: 2026-03-27
source: "classicality-budget strategy-001 meta-exploration-003; stochastic-electrodynamics strategy-001 meta-exploration-003; classicality-budget strategy-002 meta-exploration-006, meta-exploration-007, meta-exploration-009"
---

## Lesson

When a specific theory, framework, or derivation has been identified, make novelty assessment the FIRST exploration task — before validation, predictions, or extensions. Knowing whether the result is genuinely new reframes everything: it determines whether to invest in stress-testing the theory or in finding what's new about the DERIVATION within an existing program.

Don't assume a result is new just because you derived it independently.

## Evidence

- **classicality-budget strategy-001 exploration 003** — Prioritizing novelty assessment as Task 1 in a three-task structure (novelty → validation → predictions) was efficient. Discovering that the structural form of the classicality budget already existed (Tank 2025) while the physical content (Bekenstein connection) was novel reframed the entire research direction: the value shifted from "we invented a new bound" to "we found a new physical reason why an existing bound applies."

- **stochastic-electrodynamics strategy-001 exploration 003** — Prioritizing novelty assessment confirmed again: knowing whether the SED anharmonic program was an existing research program reframed everything. The key insight was "We haven't invented a new theory — we've found a new reason why an existing theory must be correct." This distinction between theory-novelty and derivation-novelty determined how to position subsequent numerical validation work.

## Distinction from Divergent Survey Pattern

The divergent survey pattern (`methodology/divergent-survey-pattern.md`) includes novelty assessment as Part (d) of a 4-part Phase 1 survey. THIS lesson is about doing novelty assessment as a DEDICATED Task 1 when you already have a specific result in hand — it's about sequencing, not about including novelty in surveys.

## Variant: Thorough Novelty Check for Clean Universal Constants

When an exploration discovers a clean universal dimensionless constant (e.g., 1/(540 ln2) or
ζ(3)/(24π⁴)) as a new result, the novelty assessment should explicitly search for that specific
constant in the existing literature — not just for the framework or concept. Such constants
often exist *implicitly* in prior formulas without having been named or highlighted.

The risk: a 5-line derivation yields a number that an expert "could have derived in five minutes"
and that may appear under a different name elsewhere. The goal should explicitly ask: "Does this
specific constant appear (explicitly or implicitly) in [field] X literature?"

**Use LITERAL STRING search for the numeric value.** Searching for "1/(540 ln2)" or "7.21
Schwarzschild radius" as a literal string is more decisive than searching for the concept. If
the number doesn't appear verbatim in literature, it hasn't been published as a named result.
This approach is definitive in a way that conceptual searches are not.

- **classicality-budget strategy-001 exploration 006** — Discovered S_Hawking = 1/(540 ln2) and
  ⟨N⟩ = ζ(3)/(24π⁴) as universal BH constants. The explorer reported these as NOVEL based on
  search results, but acknowledged "an expert in BH thermodynamics could derive them in five minutes."
  A more thorough search specifically targeting these constants (and the parent identity T_H × r_s = const)
  in BH thermodynamics literature would have strengthened the novelty assessment.
- **classicality-budget strategy-002 exploration 002** — Follow-up thorough check (18 papers,
  11 literal-string queries): zero results for "1/(540 ln2)" and "7.21 Schwarzschild radius"
  in any indexed source. The literal string search was definitively conclusive.

**Require identification of "closest prior work."** The goal should ask for the paper that gets
CLOSEST to the result even if it doesn't contain it. This produces: (a) the best citation for
"prior art" in any eventual paper, and (b) a clear statement of what specifically is new (e.g.,
"Gray et al. use ζ(3) for emission rate, not sphere occupation number — these are genuinely
different quantities"). This was the origin of the Kim (2021) and Gray et al. (2016) leads.

- **classicality-budget strategy-002 exploration 002** — Requiring "closest prior work" produced
  Kim 2021 (arXiv:2112.01931) and Gray et al. 2016 (arXiv:1506.03975) as genuinely valuable
  citation context for any eventual paper on the BH universal constants.

**Require documentation of adjacent papers.** Ask for papers that are in the NEIGHBORHOOD of
the target connection, even if they don't make the connection itself. These are valuable for
citation context and for clarifying "conceptually adjacent but different" distinctions.

- **classicality-budget strategy-002 exploration 001** — Requiring adjacent papers documentation
  produced Ferté & Cao (2023) and AJMP (2026) as adjacent QD↔HQEC papers, providing citation
  context even though neither made the explicit connection.

**~18 papers is the right scope** for a thorough numerical-constant novelty search. Fewer than
~7 (as in strategy-001 E007) is insufficient. More than ~20 produces diminishing returns for
this task type.

## Variant: Embed "Verdict on Novelty" as Mandatory Section in Any Mathematical Exploration

Even when novelty assessment is NOT a dedicated Task 1 (because the goal has multiple components), include "give a verdict on novelty" as a required OUTPUT SECTION. Without this, explorers present mathematical results without distinguishing "new perspective on known physics" from "genuinely new physics." The explicit question forces this honesty even mid-exploration.

- **classicality-budget strategy-002 exploration 004** — The island formula + QD computation produced the result "Page-time interior classicality" — which is actually a RESTATEMENT of HQEC entanglement wedge reconstruction in QD language, not new physics. The "verdict on novelty" section in the goal forced the explorer to make this honest assessment. Without it, the result might have been presented as a new prediction. The distinction "restatement vs. new organizing insight" was correctly drawn because the novelty verdict was required.
**Pattern:** Even for computationally focused goals where novelty is not the main point, add: "Include a section: Is this result genuinely new physics, a new perspective on known physics, or a restatement? Cite the closest prior work." This takes one paragraph for the explorer but produces much more honest, citable output.

## Variant: "Find the Closest Prior Work" Is Sharper Than "Has This Been Published?"

Framing the novelty search as **"find the paper that comes CLOSEST to this result"** is more effective
than simply asking "has this been published?" The closest-prior-work framing:
1. Produces a specific equation-level comparison: "that paper used X, ours uses Y — different because..."
2. Identifies the precise novelty gap even when the overall verdict is "novel"
3. Prevents false negatives: a narrative summary might say "Milgrom connected de Sitter temperature
   to MOND" — correct but misleading, because Milgrom used the EXCESS temperature not the ratio

The Milgrom 1999 example illustrates the value: a naive search might conclude "Milgrom connected de
Sitter temperature to MOND in 1999 — not novel." But asking "what exactly did Milgrom use?" revealed
he used the EXCESS temperature T_dS − T_GH, giving a different interpolation function
(μ_excess = √(1+x²) − 1) and a different a₀ prediction (2cH₀ vs. cH₀). The specific identity
T_U/T_dS = μ_standard was NOT Milgrom's result.

- **compton-unruh strategy-001 exploration-005** — Asking for the closest prior work (Milgrom 1999)
  immediately exposed the precise distinction: excess vs. ratio, different μ formula, different a₀.
  Without this comparison, a narrative summary might have suggested "Milgrom basically did this in
  1999," which would be wrong. Six papers were checked and a web search returned zero results for the
  specific ratio + MOND interpolation combination. The structured closest-prior-work comparison is
  what makes the novelty verdict defensible.

## Variant: Search for Whether the CONCLUSION Has Been Stated — Not Just the Technique

For adversarial synthesis explorations, frame the prior art search as: **"Has this *conclusion* been stated before?"** — not just "are these techniques known?" These are very different questions, and confusing them can cost an entire strategy cycle.

**Technique-level prior art:** "Has anyone computed a convergence law for the SED quartic oscillator?" → Answer: no prior simulation.
**Conclusion-level prior art:** "Has anyone stated that SED cannot substitute for quantum mechanics?" → Answer: yes — Nieuwenhuizen (2020) explicitly, Santos (2022) implicitly.

- **SED strategy-003 exploration-004** — The adversarial synthesis found that Nieuwenhuizen (2020) had already explicitly concluded "SED is not a basis for quantum mechanics" in the hydrogen context, and Santos (2022) had implied the same via the O(ħ²) framework. The mission's grand synthesis conclusion was therefore NOT novel at the conceptual level — only at the quantitative multi-system level. This was identified during the adversarial synthesis, not before it. **A prior conclusion-level search at the start of strategy-003 would have prevented designing the grand synthesis as potentially novel and would have redirected the framing toward "systematic quantification of a known result" from the outset.**

**Practical implementation:** For any adversarial synthesis goal where the mission is building toward a central conclusion, add to the goal's prior art section: "Search specifically for whether the main conclusion (e.g., 'field quantization is necessary for nonlinear quantum systems') has been stated explicitly by the most prominent researchers in this field. Name the 3–5 most prominent researchers and ask whether they have stated this conclusion." This is a 1-paragraph addition to the goal that can save a strategy cycle.

**Key distinction:** Technique prior art is found by searching for methods and formulas. Conclusion prior art requires reading the conclusions sections of papers by domain leaders. Searching for the technique ("SED quartic oscillator simulation") will not find the conclusion ("SED is not a basis for QM") stated in a hydrogen paper.

## When to apply

Whenever a strategizer has identified a specific formula, construction, or theory and is about to invest in validation or extension. The novelty check should come first, before committing resources to stress-testing. For clean numerical constants, request an explicit literal-string search for that specific value. Always request identification of closest prior work and adjacent papers — even when the verdict is "not published." Frame the search as "find the closest prior work and explain what exactly it does differently."

**For multi-system synthesis missions:** Also run a conclusion-level prior art check before framing the grand synthesis as potentially novel. Ask: has this conclusion been stated by the 3–5 most prominent researchers in the field?

**NEW variant: equation-level comparison for novelty (yang-mills-validation E002):** Don't ask "does Paper X have this result?" — ask "what is Paper X's exact formula/bound, and can it be improved to get our result?" The equation-level framing forces identification of precisely where approaches diverge. Applied to CNS papers: identified that their vertex Hessian bound 4(d-1)Nβ is TIGHT in their formulation, pinpointing the exact mathematical step that is new in our approach.
