---
topic: Adversarial synthesis goal structure — 4-part output format and pre-loading requirements
category: goal-design
date: 2026-03-28
source: "stochastic-electrodynamics strategy-003 meta-exploration-s003-004, thermal-time strategy-003 meta-exploration-002"
---

## Lesson

For finishing-strategy adversarial synthesis explorations (reviewing all novel claims across multiple strategies), the goal should specify a **4-part structured output** AND **pre-load all claims with evidence summaries, prior art candidates, and strongest objections**. Without this structure, the explorer re-discovers what's at stake rather than doing genuine adversarial work.

## The 4-Part Output Structure

Require the following four sections in the report:

1. **Part 1: Adversarial review per claim** — Each claim gets its own subsection: evidence summary, prior art situation, strongest objection, rebuttal, verdict (VERIFIED / PARTIALLY VERIFIED / CONJECTURED), and novelty rating (1–5).
2. **Part 2: Prior art search for the conclusion** — Targeted literature search: has this *conclusion* been stated before? (Not just "are the techniques known?") Name the specific authors to check.
3. **Part 3: Grand synthesis** — Answer the mission question directly, with the prior art situation integrated. Identify exactly what is new vs. what was already known.
4. **Part 4: Consolidated claims table** — One-row-per-claim table with Verdict / Novelty / Strongest Surviving Objection.

## Evidence

- **SED strategy-003 exploration-004** — The GOAL.md specified all 7 SED claims with evidence summaries, prior art candidates, and strongest objections already framed. The explorer did genuine adversarial work in ~40 min, produced a clean 4-part report, and delivered clear verdicts. The key finding (Nieuwenhuizen already stated the conclusion explicitly) came from one of the targeted prior art lookups. Without pre-loading, the explorer would have spent half the time reconstructing what the claims were.

## Pre-Loading for Adversarial Synthesis Goals

Paste the complete claim list (not summaries — the full claims with evidence) directly into the GOAL.md. For each claim include:
- The specific claim statement
- The evidence base (key numbers, simulation results, analytic derivations)
- The strongest known objection
- Prior art candidates to check

This is the adversarial-specific version of the `preload-context-from-prior-work` pattern. General pre-loading is about efficiency; this version is about enabling genuine adversarial work. An adversarial reviewer who must reconstruct the claim from scratch is not doing adversarial review — they are doing survey work.

**Caveat:** A GOAL.md with 7+ claims spelled out will be long (200–300 lines). This is a context burden on the explorer, but it is unavoidable for a finishing-strategy synthesis. Accept the length.

## Tier 4 vs Tier 5 Distinction

For a **finishing strategy** (consolidating results, adversarial sweep before close), Tier 4 (clean verdicts, no surprises) is the expected outcome — the goal is to clarify the novelty landscape.

For **Tier 5** (a claim being upgraded from CONJECTURED to VERIFIED), the adversarial goal needs an additional requirement: **for each claim, provide a concrete falsifiable path** — a specific computation, prediction, or experimental discriminant that could in principle verify the claim. A literature check alone is insufficient for Tier 5; the explorer needs to identify what evidence would change the verdict.

- SED strategy-003 exploration-004: Zero claims upgraded from CONJECTURED to VERIFIED. The exploration confirmed clean verdicts but produced no surprises — as expected for a finishing strategy. For future Tier-5-targeting explorations: frame each claim with "what would make this VERIFIED?" alongside the adversarial objections.

## Prior Art Discovery as Primary Outcome

- **thermal-time strategy-003 exploration-002** — The most important outcome of the adversarial review was identifying **Lashkari-Liu-Rajagopal 2021** (arXiv:1811.05052) as the closest prior art for Claim 3 (excited-state modular flow). This paper computes modular flow operators for excited states but does NOT compare correlator dynamics to physical time evolution — meaning Claim 3's specific quantitative results (zero spectral weight, N-scaling) survive. Without the adversarial prior art search, this paper would not have been identified, and the claim's novelty rating would remain ungrounded.

**Meta-lesson:** The most important outcome of an adversarial exploration can be a prior art discovery that forces precise claim reframing, even when the claim ultimately survives. Prior art search should be prioritized as the most valuable part of adversarial reviews — it provides an objective external anchor for novelty ratings, unlike conceptual attacks which depend on argument quality.

## Variant: Evidence Grading + Weakest Link + Novel Claims by Reviewer

**[vasseur-pressure E009]** Three additional goal elements that improved the adversarial review:

1. **Evidence grading (A/B/C/D/F per claim):** Makes the strength of each claim immediately visible. No As and no Fs in E009 suggests appropriate calibration — the reviewer was neither dismissive nor inflating.

2. **Require "weakest link" deliverable:** Forces the reviewer to rank-order vulnerabilities, which is more actionable than a flat list. E009 identified Claim 5 (truncation preserves Beltrami) as weakest with specific reasons (trivially true for exact case, unproven for near-Beltrami, div-free violation, missing beta connection).

3. **Novel claims list by adversarial reviewer (not the original explorer):** Having the adversarial reviewer decide what qualifies as novel produced more conservative, defensible assessments. The reviewer downgraded "universality" from stated fact to "induction from 2 examples" — a more accurate characterization.

## Variant: Require Fix Specification Per Weakness

**[vasseur-pressure E009]** Adversarial reviews should specify **what would FIX each weakness**, not just identify it. The E009 reviewer did this well for Claim 5 (analytical proof for near-Beltrami, Leray projection for div-free, quantitative beta connection) but less well for Claims 2/3/6 ("abandon DNS tightness program" without suggesting replacement). Reviews that only diagnose produce paralysis; reviews that prescribe enable action.

## Variant: Ranked Publishability Format for Novel Claims

**[vasseur-pressure S2-E007]** When the adversarial review evaluates multiple novel claims, require a ranked list by publishability with per-claim scores for correctness, novelty, significance, and standalone publishability. This format immediately tells the strategizer what to formalize next. S2-E007: ranked list (Claim 3 > Claim 2 > Claim 4 > Claim 1 > Claim 5) directly prioritized formalizing the seven-route obstruction over the universal formula. Include "fatal flaw?" column — some claims score high on novelty/significance but have a fundamental limitation (e.g., informal rather than rigorous). Include "most publishable combination" assessment — individual claims may be unpublishable but strong in combination.

## Variant: Require Specific Formalization Steps

**[vasseur-pressure S2-E007]** Adversarial reviews should propose the most actionable formalization step for informal claims, not just identify weaknesses. "This claim needs work" produces paralysis; "here's how to make it rigorous" enables action. S2-E007: identifying the SDP approach (sum-of-squares relaxation to find optimal |{|u| > lambda}| bound given NS constraints) as the specific formalization path for the informal sharpness claim was the most actionable output of the entire adversarial review. Protocol: for each claim rated below VERIFIED, propose one specific formalization method (SDP, counterexample search, formal definition, etc.) with enough detail that the strategizer can write a GOAL.md.

## When to Apply

Any exploration that is a final adversarial review across multiple previously established claims — typically the last exploration of a strategy. For earlier adversarial checks (between phases), see `methodology/adversarial-check-between-phases.md`.
